"""Build deterministic public artifact and file-level provenance manifests."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_REPOSITORY = "https://github.com/PinkTulips139/YOLO-Master.git"
SOURCE_BRANCH = "issue54-mot-routing-stability"
SOURCE_COMMIT = "dd490a80840dd70836e9363e14630039c7086a87"
PORTFOLIO_VERSION = "v1.0.1"
PORTFOLIO_REPOSITORY = (
    "https://github.com/PinkTulips139/YOLO-Master-Issue54-MoT-Routing-Stability"
)
MANIFEST_DIR = ROOT / "results" / "manifests"
SOURCE_MANIFEST = ROOT / "provenance" / "SOURCE_MANIFEST.csv"

FORMAL_SOURCES = {
    "results/tables/architecture_summary.csv": (
        "docs/issue54/phase3_architecture_controls/phase3_architecture_summary.csv",
        "44b9feb6e14c19652893293c20c97515d588dd3e7b33a3c30d498e3dbfb5f75f",
    ),
    "results/tables/checkpoint_index.csv": (
        "docs/issue54/phase3_architecture_controls/phase3_architecture_run_metrics.csv",
        "f6cf472a31733b8dcb964e657b8c373b9f38b4efbdaff9792dfa49dc6f6b8c65",
    ),
    "models/MODEL_INDEX.csv": (
        "docs/issue54/phase3_architecture_controls/phase3_architecture_run_metrics.csv",
        "f6cf472a31733b8dcb964e657b8c373b9f38b4efbdaff9792dfa49dc6f6b8c65",
    ),
    "results/tables/mot_seed_metrics.csv": (
        "docs/issue54/phase3_mot_routing/reports/phase3_mot_seed_metrics.csv",
        "8a6080b4fe0ffc57aa68c455fc315d62f3c33b51e77793e07cadda8ac7745024",
    ),
    "results/tables/mot_layer_stability.csv": (
        "docs/issue54/phase3_mot_routing/reports/phase3_mot_layer_stability.csv",
        "ae455515b35ea33d46766bce8a73bd783588d2664542a7dbcf3bafcbc010a87e",
    ),
    "results/tables/expert_utilization_summary.csv": (
        "docs/issue54/phase3_mot_routing/reports/phase3_mot_expert_utilization.csv",
        "74dd65253338883015c484cc4c148b43a0923524b473008df75b927e003994f4",
    ),
    "results/tables/pairwise_seed_summary.csv": (
        "docs/issue54/phase3_mot_routing/reports/phase3_mot_pairwise_agreement.csv",
        "0a181bc7d05f67a3098761c90a6825c27bfa51a37659ecf41345b50dd0c97618",
    ),
}


def sha256(path: Path) -> str:
    """Return the SHA256 digest of a file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path: Path, text: str) -> None:
    """Write normalized UTF-8 text with one terminal newline."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def generated_outputs() -> list[str]:
    """Return result outputs governed by the formal report manifest."""
    patterns = (
        "results/tables/*.csv",
        "results/figures/*.png",
        "docs/assets/*.png",
    )
    paths: list[str] = []
    for pattern in patterns:
        paths.extend(
            path.relative_to(ROOT).as_posix() for path in sorted(ROOT.glob(pattern))
        )
    return sorted(paths)


def build_report_manifest() -> None:
    """Write the formal-source and public-derivative hash map."""
    payload = {
        "schema_version": 1,
        "report_type": "issue54_public_portfolio",
        "source_branch": SOURCE_BRANCH,
        "source_commit": SOURCE_COMMIT,
        "formal_inputs": {
            "phase3_cross_seed_routing.json": "b7049cdbac25c346ac8deb37b505d92bd37406f197458a8f045677c1eba9f7f2",
            "phase3_formal_registry.json": "3b3f22cd0339dfab372a0b8c27c55dfea4a0b22b57e13a3d92ed8675b7d28540",
            "phase3_mot_report_manifest.json": "4933d684160d349ccc04a1ec2124548cce7a0a3ecfe1d6a853e741b633c9fa5d",
            "phase3_architecture_report_manifest.json": "d2355a4f65b4783efa2b819910c6ef34da0cbe02ba7365531860cbc34eef8a61",
        },
        "public_outputs": {path: sha256(ROOT / path) for path in generated_outputs()},
        "counting_rule": "Independent training seed is the highest experimental unit; images, tokens, layers, and seed pairs do not increase n.",
    }
    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
    write_text(MANIFEST_DIR / "REPORT_MANIFEST.json", text)


def build_sums() -> None:
    """Write checksums for formal public tables and deterministic PNG outputs."""
    paths = generated_outputs()
    lines = [f"{sha256(ROOT / path)}  {path}" for path in paths]
    write_text(MANIFEST_DIR / "SHA256SUMS", "\n".join(lines))


def artifact_type(path: str) -> str:
    """Return a compact artifact type label."""
    suffix = Path(path).suffix.lower()
    return {
        ".csv": "table",
        ".png": "figure",
        ".json": "manifest",
        ".md": "report",
        ".patch": "patch",
        ".yaml": "config",
        "": "checksums",
    }.get(suffix, "artifact")


def build_public_artifact_manifest() -> None:
    """Write the compact manifest for public evidence artifacts."""
    selected = generated_outputs()
    selected.extend(
        [
            "configs/formal_protocol.yaml",
            "configs/visdrone_issue54_public.yaml",
            "models/MODEL_INDEX.csv",
            "patches/cross_version_compatibility.patch",
            "patches/mot_gradients_legacy_reductions.patch",
            "provenance/RAW_EVIDENCE_INDEX.csv",
            "results/manifests/FORMAL_EVIDENCE_HASHES.md",
            "results/manifests/REPORT_MANIFEST.json",
            "results/manifests/SHA256SUMS",
        ]
    )
    selected = sorted(set(selected))
    fields = (
        "path",
        "type",
        "size_bytes",
        "sha256",
        "source",
        "formal_status",
        "publication_reason",
    )
    target = MANIFEST_DIR / "PUBLIC_ARTIFACT_MANIFEST.csv"
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for relative in selected:
            path = ROOT / relative
            source = FORMAL_SOURCES.get(relative, ("public portfolio derivation", ""))[
                0
            ]
            writer.writerow(
                {
                    "path": relative,
                    "type": artifact_type(relative),
                    "size_bytes": path.stat().st_size,
                    "sha256": sha256(path),
                    "source": source,
                    "formal_status": "formal_derivative"
                    if relative.startswith("results/")
                    else "supporting",
                    "publication_reason": "compact auditable evidence or deterministic reproduction support",
                }
            )


def classification(path: str) -> str:
    """Classify each public file by origin."""
    if path == "LICENSE":
        return "upstream_provided"
    if path.startswith("patches/") and path.endswith(".patch"):
        return "user_modified_upstream"
    if (
        path.startswith("results/")
        or (path.startswith("docs/assets/") and path.endswith(".png"))
        or path == "provenance/SOURCE_MANIFEST.csv"
    ):
        return "generated_artifact"
    if path in {"models/MODEL_INDEX.csv", "provenance/RAW_EVIDENCE_INDEX.csv"}:
        return "public_metadata_only"
    if path == "THIRD_PARTY_NOTICES.md":
        return "third_party_reference"
    return "user_added"


def source_record(path: str) -> tuple[str, str, str, str, str, str, str, str]:
    """Return source fields for one destination path."""
    if path in FORMAL_SOURCES:
        source_path, source_hash = FORMAL_SOURCES[path]
        return (
            SOURCE_REPOSITORY,
            SOURCE_BRANCH,
            SOURCE_COMMIT,
            source_path,
            "PinkTulips139 / formal evidence",
            "AGPL-3.0",
            "generated",
            source_hash,
        )
    if path == "LICENSE":
        return (
            SOURCE_REPOSITORY,
            SOURCE_BRANCH,
            SOURCE_COMMIT,
            "LICENSE",
            "GNU Free Software Foundation / upstream copy",
            "AGPL-3.0",
            "copied",
            sha256(ROOT / path),
        )
    if path.startswith("patches/") and path.endswith(".patch"):
        commit = (
            "178701a54bc05f9bd7955d2b8f3ac7e4635e587e"
            if "cross_version" in path
            else "09c9e0e80fef1b7d64001e4d244b13bb33189197"
        )
        return (
            SOURCE_REPOSITORY,
            SOURCE_BRANCH,
            commit,
            f"commit:{commit}",
            "PinkTulips139 / modified upstream",
            "AGPL-3.0",
            "generated",
            "",
        )
    if path.startswith("results/figures/") or (
        path.startswith("docs/assets/") and path.endswith(".png")
    ):
        return (
            PORTFOLIO_REPOSITORY,
            "main",
            PORTFOLIO_VERSION,
            "results/tables + figure builder",
            "PinkTulips139",
            "AGPL-3.0",
            "generated",
            "",
        )
    return (
        PORTFOLIO_REPOSITORY,
        "main",
        PORTFOLIO_VERSION,
        "",
        "PinkTulips139",
        "AGPL-3.0",
        "generated" if classification(path) == "generated_artifact" else "authored",
        "",
    )


def public_files() -> list[str]:
    """Return all public files outside Git internals and local caches."""
    ignored_parts = {".git", ".ruff_cache", ".pytest_cache", "__pycache__"}
    return sorted(
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and not (set(path.relative_to(ROOT).parts) & ignored_parts)
    )


def build_source_manifest() -> None:
    """Write one provenance row for every public file, with a non-hashed self row."""
    fields = (
        "destination_path",
        "source_repository",
        "source_branch",
        "source_commit",
        "source_path",
        "classification",
        "author_or_origin",
        "license",
        "copied_or_generated",
        "formal_or_diagnostic",
        "source_sha256",
        "public_sha256",
        "notes",
    )
    files = [
        path for path in public_files() if path != "provenance/SOURCE_MANIFEST.csv"
    ]
    with SOURCE_MANIFEST.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for relative in files:
            (
                repository,
                branch,
                commit,
                source_path,
                origin,
                license_name,
                mode,
                source_hash,
            ) = source_record(relative)
            formal = (
                "formal"
                if relative in FORMAL_SOURCES or relative.startswith("results/")
                else "not_applicable"
            )
            writer.writerow(
                {
                    "destination_path": relative,
                    "source_repository": repository,
                    "source_branch": branch,
                    "source_commit": commit,
                    "source_path": source_path,
                    "classification": classification(relative),
                    "author_or_origin": origin,
                    "license": license_name,
                    "copied_or_generated": mode,
                    "formal_or_diagnostic": formal,
                    "source_sha256": source_hash,
                    "public_sha256": sha256(ROOT / relative),
                    "notes": "No checkpoint, dataset, raw log, or private path is embedded.",
                }
            )
        writer.writerow(
            {
                "destination_path": "provenance/SOURCE_MANIFEST.csv",
                "source_repository": PORTFOLIO_REPOSITORY,
                "source_branch": "main",
                "source_commit": PORTFOLIO_VERSION,
                "source_path": "",
                "classification": "generated_artifact",
                "author_or_origin": "PinkTulips139",
                "license": "AGPL-3.0",
                "copied_or_generated": "generated",
                "formal_or_diagnostic": "not_applicable",
                "source_sha256": "",
                "public_sha256": "",
                "notes": "Self-referential SHA256 intentionally omitted; all other public files are hashed.",
            }
        )


def main() -> None:
    """Generate all public manifests in dependency order."""
    build_report_manifest()
    build_sums()
    build_public_artifact_manifest()
    build_source_manifest()
    print(f"PASS: generated public manifests for {len(public_files())} files")


if __name__ == "__main__":
    main()
