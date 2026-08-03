#!/usr/bin/env python3
"""Build deterministic Issue #54 portfolio figures from validated public CSV tables."""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "results" / "tables"
FIGURES = ROOT / "results" / "figures"
ASSETS = ROOT / "docs" / "assets"

NAVY = "#17324D"
BLUE = "#21618C"
CYAN = "#1AA6B7"
TEAL = "#167D86"
GRAY = "#66737F"
LIGHT = "#EAF1F5"
ORANGE = "#D9822B"

OUTPUTS = (
    "architecture_performance.png",
    "mot_seed_performance.png",
    "mot_layer_routing_stability.png",
    "expert_utilization_heatmap.png",
    "pairwise_routing_agreement.png",
)


def read_csv(
    name: str, schema: tuple[str, ...], expected_rows: int
) -> list[dict[str, str]]:
    """Read one CSV and fail closed on schema, width, row count, or blank values."""
    path = TABLES / name
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != schema:
            raise ValueError(f"{name}: unexpected schema {reader.fieldnames!r}")
        rows = list(reader)
    if len(rows) != expected_rows:
        raise ValueError(f"{name}: expected {expected_rows} rows, found {len(rows)}")
    if any(None in row for row in rows):
        raise ValueError(f"{name}: malformed row width")
    return rows


def finite(value: str, field: str) -> float:
    """Parse a finite numeric value."""
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{field}: expected finite value")
    return number


def configure_style() -> None:
    """Apply a compact, GitHub-readable visual style."""
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 15,
            "axes.labelsize": 11,
            "axes.edgecolor": "#A9B4BE",
            "axes.labelcolor": NAVY,
            "axes.titlecolor": NAVY,
            "xtick.color": "#43515E",
            "ytick.color": "#43515E",
            "grid.color": "#D9E1E7",
            "grid.linewidth": 0.8,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def save(fig: plt.Figure, path: Path) -> None:
    """Save a PNG with fixed metadata and dimensions determined by the figure."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        path,
        dpi=100,
        facecolor="white",
        edgecolor="none",
        metadata={"Software": "Issue54 deterministic portfolio figure builder v1.0.0"},
    )
    plt.close(fig)


def architecture_figure(output: Path) -> None:
    """Plot architecture mAP with sample SD where statistically defined."""
    schema = (
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
    rows = read_csv("architecture_summary.csv", schema, 3)
    names = [row["architecture"] for row in rows]
    counts = [int(row["seed_count"]) for row in rows]
    colors = [BLUE, GRAY, CYAN]
    fig, axes = plt.subplots(1, 2, figsize=(12, 7.2))
    for ax, metric, std_field, title in (
        (axes[0], "mean_map50", "sample_std_map50", "mAP50"),
        (axes[1], "mean_map50_95", "sample_std_map50_95", "mAP50-95"),
    ):
        values = [finite(row[metric], metric) for row in rows]
        errors = [
            finite(row[std_field], std_field) if row[std_field] else 0.0 for row in rows
        ]
        bars = ax.bar(names, values, yerr=errors, color=colors, capsize=6, width=0.62)
        ax.set_title(title)
        ax.set_ylim(min(values) - 0.008, max(values) + 0.008)
        ax.grid(axis="y")
        ax.set_axisbelow(True)
        for bar, value, count in zip(bars, values, counts):
            suffix = "single seed" if count == 1 else f"n={count}, sample SD"
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value + 0.001,
                f"{value:.5f}\n{suffix}",
                ha="center",
                va="bottom",
                fontsize=9,
                color=NAVY,
            )
    fig.suptitle(
        "Architecture performance controls", fontsize=19, color=NAVY, fontweight="bold"
    )
    fig.text(
        0.5,
        0.03,
        "VisDrone2019-DET · 30 epochs · unequal independent-seed counts · descriptive comparison only",
        ha="center",
        color=GRAY,
    )
    fig.subplots_adjust(left=0.08, right=0.98, top=0.85, bottom=0.12, wspace=0.22)
    save(fig, output)


def seed_figure(output: Path) -> None:
    """Plot the two detection metrics for five independent MoT training seeds."""
    schema = (
        "seed",
        "map50",
        "map50_95",
        "checkpoint_sha256",
        "status",
        "epochs",
        "precision",
    )
    rows = read_csv("mot_seed_metrics.csv", schema, 5)
    seeds = [int(row["seed"]) for row in rows]
    metrics = (("map50", "mAP50", BLUE), ("map50_95", "mAP50-95", CYAN))
    fig, axes = plt.subplots(1, 2, figsize=(12, 7.2))
    for ax, (field, title, color) in zip(axes, metrics):
        values = [finite(row[field], field) for row in rows]
        mean = sum(values) / len(values)
        ax.plot(seeds, values, marker="o", markersize=8, linewidth=2.2, color=color)
        ax.axhline(
            mean, linestyle="--", linewidth=1.7, color=ORANGE, label=f"Mean {mean:.5f}"
        )
        ax.fill_between(seeds, values, [mean] * len(values), color=color, alpha=0.08)
        ax.set_title(title)
        ax.set_xlabel("Independent training seed")
        ax.set_xticks(seeds)
        ax.set_ylim(min(values) - 0.004, max(values) + 0.004)
        ax.grid(axis="y")
        ax.legend(frameon=False, loc="best")
        for seed, value in zip(seeds, values):
            ax.annotate(
                f"{value:.5f}",
                (seed, value),
                xytext=(0, 9),
                textcoords="offset points",
                ha="center",
                fontsize=9,
            )
    fig.suptitle(
        "MoT detection performance across five seeds",
        fontsize=19,
        color=NAVY,
        fontweight="bold",
    )
    fig.text(
        0.5,
        0.03,
        "Each point is a distinct checkpoint from an independently trained seed; images and tokens are not replicates.",
        ha="center",
        color=GRAY,
    )
    fig.subplots_adjust(left=0.08, right=0.98, top=0.85, bottom=0.13, wspace=0.22)
    save(fig, output)


def layer_figure(output: Path) -> None:
    """Plot cross-seed routing agreement in architecture order."""
    schema = (
        "layer",
        "dominant_agreement",
        "token_top1_agreement",
        "seed_count",
        "image_count",
        "seed_pair_count",
    )
    rows = read_csv("mot_layer_stability.csv", schema, 6)
    labels = [row["layer"].replace("model.", "") for row in rows]
    dominant = [finite(row["dominant_agreement"], "dominant_agreement") for row in rows]
    token = [
        finite(row["token_top1_agreement"], "token_top1_agreement") for row in rows
    ]
    x = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(12, 7.2))
    ax.plot(
        x,
        dominant,
        color=BLUE,
        marker="o",
        markersize=8,
        linewidth=2.4,
        label="Dominant expert agreement",
    )
    ax.plot(
        x,
        token,
        color=CYAN,
        marker="s",
        markersize=7,
        linewidth=2.4,
        label="Token top-1 agreement",
    )
    ax.axhline(
        sum(dominant) / len(dominant),
        color=BLUE,
        linestyle="--",
        alpha=0.55,
        label="Global dominant 0.526",
    )
    ax.axhline(
        sum(token) / len(token),
        color=CYAN,
        linestyle=":",
        alpha=0.75,
        label="Global token 0.435",
    )
    ax.set_xticks(x, labels)
    ax.set_xlabel("MoT layer (architecture order)")
    ax.set_ylabel("Cross-seed agreement")
    ax.set_ylim(0, 1.08)
    ax.set_title("Layer-level MoT routing stability", fontweight="bold")
    ax.grid(axis="y")
    ax.legend(frameon=False, ncol=2, loc="upper center")
    fig.text(
        0.5,
        0.035,
        "5 independent seeds · 32 fixed validation images · 10 seed pairs · entropy is not plotted as stability",
        ha="center",
        color=GRAY,
    )
    fig.subplots_adjust(left=0.09, right=0.98, top=0.88, bottom=0.14)
    save(fig, output)


def utilization_figure(output: Path) -> None:
    """Plot cross-seed mean expert utilization for six layers and three experts."""
    schema = ("layer", "expert", "mean_utilization", "sample_std", "seed_count")
    rows = read_csv("expert_utilization_summary.csv", schema, 18)
    layers = list(dict.fromkeys(row["layer"] for row in rows))
    experts = ["LocalConvTransformer", "WindowTransformer", "DeformableTransformer"]
    lookup = {
        (row["layer"], row["expert"]): finite(
            row["mean_utilization"], "mean_utilization"
        )
        for row in rows
    }
    matrix = np.array(
        [[lookup[(layer, expert)] for expert in experts] for layer in layers]
    )
    if not np.allclose(matrix.sum(axis=1), np.ones(len(layers)), atol=1e-9):
        raise ValueError("expert utilization rows must sum to one within each layer")
    fig, ax = plt.subplots(figsize=(12, 7.2))
    image = ax.imshow(matrix, cmap="Blues", vmin=0.0, vmax=1.0, aspect="auto")
    ax.set_xticks(range(3), ["LocalConv", "Window", "Deformable"])
    ax.set_yticks(range(6), [layer.replace("model.", "") for layer in layers])
    ax.set_xlabel("Transformer expert")
    ax.set_ylabel("MoT layer")
    ax.set_title("Cross-seed mean expert utilization", fontweight="bold")
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            color = "white" if matrix[i, j] > 0.55 else NAVY
            ax.text(
                j,
                i,
                f"{matrix[i, j]:.3f}",
                ha="center",
                va="center",
                color=color,
                fontweight="bold",
            )
    bar = fig.colorbar(image, ax=ax, fraction=0.035, pad=0.03)
    bar.set_label("Mean utilization")
    fig.text(
        0.5,
        0.035,
        "Formal 18-row summary: 6 layers × 3 experts; each row of the heatmap sums to 1.",
        ha="center",
        color=GRAY,
    )
    fig.subplots_adjust(left=0.16, right=0.92, top=0.88, bottom=0.14)
    save(fig, output)


def pairwise_figure(output: Path) -> None:
    """Plot the ten formal pairwise token-agreement aggregates as a symmetric matrix."""
    schema = (
        "seed_a",
        "seed_b",
        "dominant_agreement",
        "token_top1_agreement",
        "js_divergence",
    )
    rows = read_csv("pairwise_seed_summary.csv", schema, 10)
    matrix = np.full((5, 5), np.nan)
    np.fill_diagonal(matrix, 1.0)
    for row in rows:
        a, b = int(row["seed_a"]), int(row["seed_b"])
        value = finite(row["token_top1_agreement"], "token_top1_agreement")
        matrix[a, b] = matrix[b, a] = value
    if np.isnan(matrix).any():
        raise ValueError("pairwise table does not cover every seed pair")
    fig, ax = plt.subplots(figsize=(12, 7.2))
    image = ax.imshow(matrix, cmap="Blues", vmin=0.2, vmax=1.0)
    ax.set_xticks(range(5), [f"Seed {i}" for i in range(5)])
    ax.set_yticks(range(5), [f"Seed {i}" for i in range(5)])
    ax.set_title("Pairwise MoT token top-1 routing agreement", fontweight="bold")
    for i in range(5):
        for j in range(5):
            color = "white" if matrix[i, j] > 0.68 else NAVY
            ax.text(
                j,
                i,
                f"{matrix[i, j]:.3f}",
                ha="center",
                va="center",
                color=color,
                fontweight="bold",
            )
    bar = fig.colorbar(image, ax=ax, fraction=0.035, pad=0.03)
    bar.set_label("Token top-1 agreement")
    fig.text(
        0.5,
        0.035,
        "Upper/lower triangles mirror the same 10 seed pairs; pairs are descriptive comparisons, not independent runs.",
        ha="center",
        color=GRAY,
    )
    fig.subplots_adjust(left=0.14, right=0.9, top=0.88, bottom=0.14)
    save(fig, output)


def banner(output: Path) -> None:
    """Draw the 1600 × 500 repository banner without external assets."""
    fig, ax = plt.subplots(figsize=(16, 5))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.add_patch(
        FancyBboxPatch(
            (0, 0),
            16,
            5,
            boxstyle="round,pad=0.02",
            facecolor="#F6F9FB",
            edgecolor="#D7E2E9",
        )
    )
    ax.text(
        0.8,
        3.85,
        "YOLO-Master Issue #54",
        fontsize=27,
        fontweight="bold",
        color=NAVY,
        va="center",
    )
    ax.text(
        0.8,
        3.05,
        "Multi-Seed MoT Routing Stability",
        fontsize=22,
        color=BLUE,
        va="center",
    )
    ax.text(
        0.8,
        2.3,
        "Audited architecture controls and evidence integrity",
        fontsize=14,
        color=GRAY,
        va="center",
    )
    badges = (
        ("5", "MoT seeds"),
        ("6", "routing layers"),
        ("0.526", "dominant agreement"),
        ("0.435", "token agreement"),
    )
    for idx, (value, label) in enumerate(badges):
        x = 0.8 + idx * 2.45
        ax.text(x, 1.35, value, fontsize=18, fontweight="bold", color=TEAL)
        ax.text(x, 0.85, label, fontsize=10.5, color=GRAY)
    center = (12.6, 2.55)
    experts = (
        (14.6, 3.85, "Local"),
        (14.7, 2.45, "Window"),
        (14.4, 1.05, "Deformable"),
    )
    ax.add_patch(Circle(center, 0.55, facecolor=NAVY, edgecolor="none"))
    ax.text(
        *center,
        "MoT",
        color="white",
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
    )
    for x, y, label in experts:
        ax.plot(
            [center[0] + 0.45, x - 0.5],
            [center[1], y],
            color=CYAN,
            linewidth=2.2,
            alpha=0.85,
        )
        ax.add_patch(
            Circle((x, y), 0.48, facecolor="white", edgecolor=CYAN, linewidth=2)
        )
        ax.text(
            x,
            y,
            label,
            color=NAVY,
            ha="center",
            va="center",
            fontsize=9.5,
            fontweight="bold",
        )
    ax.text(
        12.45,
        0.35,
        "Independent research portfolio",
        fontsize=11,
        color=GRAY,
        ha="center",
    )
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    save(fig, output)


def build(figure_dir: Path, asset_dir: Path) -> None:
    """Build all outputs into explicit directories."""
    configure_style()
    architecture_figure(figure_dir / OUTPUTS[0])
    seed_figure(figure_dir / OUTPUTS[1])
    layer_figure(figure_dir / OUTPUTS[2])
    utilization_figure(figure_dir / OUTPUTS[3])
    pairwise_figure(figure_dir / OUTPUTS[4])
    banner(asset_dir / "repository-banner.png")


def sha256(path: Path) -> str:
    """Return the SHA256 of one file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_determinism() -> None:
    """Build twice in one environment and require byte-identical PNG outputs."""
    with tempfile.TemporaryDirectory(prefix="issue54-figures-") as tmp:
        root = Path(tmp)
        first = root / "first"
        second = root / "second"
        build(first / "figures", first / "assets")
        build(second / "figures", second / "assets")
        pairs = [
            (first / "figures" / name, second / "figures" / name) for name in OUTPUTS
        ]
        pairs.append(
            (
                first / "assets" / "repository-banner.png",
                second / "assets" / "repository-banner.png",
            )
        )
        mismatches = [
            (left.name, sha256(left), sha256(right))
            for left, right in pairs
            if left.read_bytes() != right.read_bytes()
        ]
        if mismatches:
            raise SystemExit(f"deterministic figure mismatch: {mismatches}")
    print(
        "PASS: two independent rebuilds produced byte-identical hashes for all six PNG files"
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Build twice in a temporary directory and compare bytes within the current environment.",
    )
    return parser.parse_args()


def main() -> None:
    """Build or verify the portfolio figures."""
    args = parse_args()
    if args.check:
        check_determinism()
        return
    build(FIGURES, ASSETS)
    print("PASS: generated five result figures and one repository banner")


if __name__ == "__main__":
    main()
