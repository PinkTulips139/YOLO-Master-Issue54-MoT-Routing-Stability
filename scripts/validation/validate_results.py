"""Validate the compact formal Issue #54 result tables and counting semantics."""

from __future__ import annotations

import csv
import itertools
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "results" / "tables"


def rows(name: str, fields: tuple[str, ...], count: int) -> list[dict[str, str]]:
    """Read a CSV with an exact schema and row count."""
    path = TABLES / name
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        require(tuple(reader.fieldnames or ()) == fields, f"{name}: schema mismatch")
        result = list(reader)
    require(len(result) == count, f"{name}: expected {count} rows, found {len(result)}")
    require(all(None not in row for row in result), f"{name}: malformed width")
    return result


def require(condition: bool, message: str) -> None:
    """Fail closed when a validation condition is false."""
    if not condition:
        raise AssertionError(message)


def number(value: str, field: str) -> float:
    """Parse and validate a finite float."""
    parsed = float(value)
    require(math.isfinite(parsed), f"{field}: non-finite value")
    return parsed


def close(actual: float, expected: float, field: str, tolerance: float = 1e-10) -> None:
    """Validate a numeric value within an explicit tolerance."""
    require(
        math.isclose(actual, expected, rel_tol=0.0, abs_tol=tolerance),
        f"{field}: {actual} != {expected}",
    )


def validate_architecture_and_seeds() -> set[str]:
    """Validate architecture summaries, independent seeds, sample SD, and checkpoint uniqueness."""
    architecture_fields = (
        "architecture",
        "model_key",
        "seed_count",
        "precision",
        "mean_map50",
        "sample_std_map50",
        "mean_map50_95",
        "sample_std_map50_95",
        "statistical_scope",
    )
    architecture = rows("architecture_summary.csv", architecture_fields, 3)
    require(
        [row["architecture"] for row in architecture] == ["EsMoE", "MoA", "MoT"],
        "architecture order",
    )
    expected_counts = {"EsMoE": 3, "MoA": 1, "MoT": 5}
    for row in architecture:
        name = row["architecture"]
        require(int(row["seed_count"]) == expected_counts[name], f"{name}: seed count")
        if name == "MoA":
            require(
                not row["sample_std_map50"] and not row["sample_std_map50_95"],
                "MoA must not report SD",
            )
            require(
                "single-seed" in row["statistical_scope"],
                "MoA scope must state single-seed",
            )

    seed_fields = (
        "seed",
        "map50",
        "map50_95",
        "checkpoint_sha256",
        "status",
        "epochs",
        "precision",
    )
    seeds = rows("mot_seed_metrics.csv", seed_fields, 5)
    require(
        [int(row["seed"]) for row in seeds] == list(range(5)), "MoT seeds must be 0-4"
    )
    require(
        all(row["status"] == "passed" and row["epochs"] == "30" for row in seeds),
        "MoT formal status",
    )
    require(all(row["precision"] == "fp32" for row in seeds), "MoT precision")
    hashes = {row["checkpoint_sha256"] for row in seeds}
    require(
        len(hashes) == 5 and all(len(value) == 64 for value in hashes),
        "MoT checkpoint SHA256 uniqueness",
    )
    map50 = [number(row["map50"], "map50") for row in seeds]
    map95 = [number(row["map50_95"], "map50_95") for row in seeds]
    mot = next(row for row in architecture if row["architecture"] == "MoT")
    close(
        statistics.mean(map50),
        number(mot["mean_map50"], "mean_map50"),
        "MoT mean mAP50",
    )
    close(
        statistics.stdev(map50),
        number(mot["sample_std_map50"], "std_map50"),
        "MoT sample SD mAP50",
        5e-9,
    )
    close(
        statistics.mean(map95),
        number(mot["mean_map50_95"], "mean_map50_95"),
        "MoT mean mAP50-95",
    )
    close(
        statistics.stdev(map95),
        number(mot["sample_std_map50_95"], "std_map50_95"),
        "MoT sample SD mAP50-95",
        5e-9,
    )
    return hashes


def validate_routing() -> None:
    """Validate the six-layer, three-expert, ten-pair formal routing derivatives."""
    layer_fields = (
        "layer",
        "dominant_agreement",
        "token_top1_agreement",
        "seed_count",
        "image_count",
        "seed_pair_count",
    )
    layers = rows("mot_layer_stability.csv", layer_fields, 6)
    expected_layers = [
        "model.14.m.0",
        "model.14.m.1",
        "model.20.m.0",
        "model.20.m.1",
        "model.23.m.0",
        "model.23.m.1",
    ]
    require([row["layer"] for row in layers] == expected_layers, "layer set/order")
    for row in layers:
        require(
            (
                int(row["seed_count"]),
                int(row["image_count"]),
                int(row["seed_pair_count"]),
            )
            == (5, 32, 10),
            "layer counting scope",
        )
        for field in ("dominant_agreement", "token_top1_agreement"):
            require(0.0 <= number(row[field], field) <= 1.0, f"{field}: range")
    close(
        statistics.mean(
            number(row["dominant_agreement"], "dominant") for row in layers
        ),
        0.5260416666666666,
        "global dominant",
    )
    close(
        statistics.mean(number(row["token_top1_agreement"], "token") for row in layers),
        0.435361328125,
        "global token",
    )

    utilization_fields = (
        "layer",
        "expert",
        "mean_utilization",
        "sample_std",
        "seed_count",
    )
    utilization = rows("expert_utilization_summary.csv", utilization_fields, 18)
    experts = {"LocalConvTransformer", "WindowTransformer", "DeformableTransformer"}
    keys = {(row["layer"], row["expert"]) for row in utilization}
    require(len(keys) == 18, "utilization duplicate key")
    for layer in expected_layers:
        layer_rows = [row for row in utilization if row["layer"] == layer]
        require(
            {row["expert"] for row in layer_rows} == experts, f"{layer}: expert set"
        )
        require(
            all(int(row["seed_count"]) == 5 for row in layer_rows),
            f"{layer}: utilization seed count",
        )
        close(
            sum(
                number(row["mean_utilization"], "mean_utilization")
                for row in layer_rows
            ),
            1.0,
            f"{layer}: utilization sum",
            2e-12,
        )
        require(
            all(number(row["sample_std"], "sample_std") >= 0.0 for row in layer_rows),
            f"{layer}: sample SD",
        )

    pair_fields = (
        "seed_a",
        "seed_b",
        "dominant_agreement",
        "token_top1_agreement",
        "js_divergence",
    )
    pairs = rows("pairwise_seed_summary.csv", pair_fields, 10)
    observed = {(int(row["seed_a"]), int(row["seed_b"])) for row in pairs}
    expected = set(itertools.combinations(range(5), 2))
    require(
        observed == expected, "pairwise table must contain the ten unique seed pairs"
    )
    for row in pairs:
        for field in ("dominant_agreement", "token_top1_agreement"):
            require(0.0 <= number(row[field], field) <= 1.0, f"{field}: range")
        require(
            number(row["js_divergence"], "js_divergence") >= 0.0,
            "JSD must be non-negative",
        )
    close(
        statistics.mean(
            number(row["dominant_agreement"], "pair dominant") for row in pairs
        ),
        0.5260416666667,
        "pairwise dominant mean",
        1e-12,
    )
    close(
        statistics.mean(
            number(row["token_top1_agreement"], "pair token") for row in pairs
        ),
        0.435361328125,
        "pairwise token mean",
        1e-12,
    )


def validate_checkpoint_index(mot_hashes: set[str]) -> None:
    """Validate all nine metadata-only checkpoint records."""
    fields = (
        "architecture",
        "model_key",
        "seed",
        "epochs",
        "precision",
        "map50",
        "map50_95",
        "checkpoint_sha256",
        "public_checkpoint",
        "reason",
    )
    checkpoints = rows("checkpoint_index.csv", fields, 9)
    hashes = [row["checkpoint_sha256"] for row in checkpoints]
    require(
        len(set(hashes)) == 9 and all(len(value) == 64 for value in hashes),
        "all nine checkpoint hashes must be unique",
    )
    require(
        mot_hashes <= set(hashes), "checkpoint index must contain every MoT checkpoint"
    )
    require(
        all(row["epochs"] == "30" for row in checkpoints),
        "all formal checkpoints must record 30 epochs",
    )
    require(
        all(row["public_checkpoint"] == "false" for row in checkpoints),
        "checkpoint publication must be false",
    )
    require(
        all(
            row["reason"] == "metadata-only; checkpoint binary not included"
            for row in checkpoints
        ),
        "checkpoint reason",
    )


def validate_protocol_language() -> None:
    """Ensure the public protocol prevents pseudo-replication by images or tokens."""
    protocol = (ROOT / "configs" / "formal_protocol.yaml").read_text(encoding="utf-8")
    require(
        "highest_experimental_unit: independent_training_seed" in protocol,
        "highest experimental unit",
    )
    require(
        "image_count: 32" in protocol and "layer_count: 6" in protocol, "routing scope"
    )
    require("seeds: [0, 1, 2, 3, 4]" in protocol, "five MoT seeds")


def main() -> None:
    """Run the complete formal-result validation."""
    mot_hashes = validate_architecture_and_seeds()
    validate_routing()
    validate_checkpoint_index(mot_hashes)
    validate_protocol_language()
    print(
        "PASS: 9 checkpoints, 5 MoT seeds, 6 layers, 18 utilization rows, and 10 seed pairs validated"
    )


if __name__ == "__main__":
    main()
