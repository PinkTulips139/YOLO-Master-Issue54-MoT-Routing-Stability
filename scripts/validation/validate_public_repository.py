"""Validate the Issue #54 public repository as a safe, complete publication tree."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
IGNORED_PARTS = {".git", ".ruff_cache", ".pytest_cache", "__pycache__"}
DENIED_SUFFIXES = {".pt", ".pth", ".ckpt", ".tar", ".gz", ".tgz", ".zip", ".7z", ".log"}
DENIED_NAMES = {"phase3_cross_seed_routing.json", ".env", "id_rsa", "id_ed25519"}
CLASSIFICATIONS = {
    "upstream_provided",
    "user_added",
    "user_modified_upstream",
    "generated_artifact",
    "third_party_reference",
    "public_metadata_only",
    "private_only_excluded",
}
REQUIRED = {
    "README.md",
    "README_CN.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "CITATION.cff",
    "REVIEW_ME.md",
    "docs/INDEX.md",
    "docs/ROUTING_STABILITY.md",
    "docs/ARCHITECTURE_CONTROLS.md",
    "results/tables/architecture_summary.csv",
    "results/tables/mot_seed_metrics.csv",
    "results/tables/mot_layer_stability.csv",
    "results/tables/expert_utilization_summary.csv",
    "results/tables/pairwise_seed_summary.csv",
    "results/tables/checkpoint_index.csv",
    "results/manifests/PUBLIC_ARTIFACT_MANIFEST.csv",
    "results/manifests/REPORT_MANIFEST.json",
    "results/manifests/SHA256SUMS",
    "provenance/SOURCE_MANIFEST.csv",
    "provenance/RAW_EVIDENCE_INDEX.csv",
    "scripts/analysis/build_portfolio_figures.py",
    "scripts/validation/validate_results.py",
    "scripts/validation/validate_public_repository.py",
    ".github/workflows/validate.yml",
}
PNG_DIMENSIONS = {
    "docs/assets/repository-banner.png": (1600, 500),
    "results/figures/architecture_performance.png": (1200, 720),
    "results/figures/mot_seed_performance.png": (1200, 720),
    "results/figures/mot_layer_routing_stability.png": (1200, 720),
    "results/figures/expert_utilization_heatmap.png": (1200, 720),
    "results/figures/pairwise_routing_agreement.png": (1200, 720),
}


def require(condition: bool, message: str) -> None:
    """Raise a publication error when a condition fails."""
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    """Return the SHA256 of one file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def public_files() -> list[Path]:
    """List repository files excluding Git and ignored local caches."""
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not (set(path.relative_to(ROOT).parts) & IGNORED_PARTS)
    )


def validate_required_and_size(files: list[Path]) -> None:
    """Validate required files, forbidden payloads, and repository size limits."""
    relative = {path.relative_to(ROOT).as_posix() for path in files}
    missing = sorted(REQUIRED - relative)
    require(not missing, f"missing required files: {missing}")
    require(
        not (
            {"data", "datasets", "runs"}
            & {
                path.parts[0].lower()
                for path in (item.relative_to(ROOT) for item in files)
            }
        ),
        "dataset/run directory found",
    )
    total = sum(path.stat().st_size for path in files)
    require(total < 20 * 1024 * 1024, f"repository exceeds 20 MiB: {total}")
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        require(path.stat().st_size > 0, f"empty public file: {rel}")
        require(path.stat().st_size < 5 * 1024 * 1024, f"file exceeds 5 MiB: {rel}")
        require(path.suffix.lower() not in DENIED_SUFFIXES, f"denied extension: {rel}")
        require(path.name.lower() not in DENIED_NAMES, f"denied filename: {rel}")
        if path.suffix.lower() == ".png":
            require(
                path.stat().st_size < 500 * 1024, f"PNG exceeds 500 KiB target: {rel}"
            )


def text_files(files: list[Path]) -> list[Path]:
    """Return files expected to decode as UTF-8 text."""
    binary = {".png", ".jpg", ".jpeg", ".gif", ".pdf"}
    return [
        path
        for path in files
        if path.suffix.lower() not in binary
        and path.name != "LICENSE"
        or path.name == "LICENSE"
    ]


def validate_sensitive_content(files: list[Path]) -> None:
    """Reject private absolute paths and common credential patterns."""
    windows_path = re.compile(
        r"\b[A-Za-z]:" + re.escape("\\") + r"[^\s'\"]+" + re.escape("\\")
    )
    unix_private_root = "/" + "root" + "/"
    token_markers = (
        "gh" + "o_",
        "github" + "_pat_",
        "AK" + "IA",
        "BEGIN " + "PRIVATE KEY",
    )
    for path in text_files(files):
        rel = path.relative_to(ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            raise AssertionError(f"non-UTF-8 text file: {rel}") from error
        require(not windows_path.search(text), f"Windows absolute path found: {rel}")
        require(unix_private_root not in text, f"private Unix path found: {rel}")
        for marker in token_markers:
            require(marker not in text, f"credential marker found in {rel}")


def validate_structured_files(files: list[Path]) -> None:
    """Parse every public CSV, JSON, YAML, and CFF file."""
    for path in files:
        suffix = path.suffix.lower()
        if suffix == ".csv":
            with path.open(encoding="utf-8", newline="") as handle:
                reader = csv.reader(handle)
                rows = list(reader)
            require(rows and rows[0], f"empty CSV schema: {path.relative_to(ROOT)}")
            width = len(rows[0])
            require(
                all(len(row) == width for row in rows),
                f"ragged CSV: {path.relative_to(ROOT)}",
            )
        elif suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
        elif suffix in {".yaml", ".yml", ".cff"}:
            parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
            require(
                isinstance(parsed, dict),
                f"structured mapping expected: {path.relative_to(ROOT)}",
            )


def validate_pngs() -> None:
    """Decode every required PNG and validate its exact dimensions."""
    for relative, expected_size in PNG_DIMENSIONS.items():
        path = ROOT / relative
        require(path.exists(), f"missing PNG: {relative}")
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            require(image.format == "PNG", f"not a PNG: {relative}")
            require(
                image.size == expected_size,
                f"{relative}: expected {expected_size}, found {image.size}",
            )


def markdown_links(path: Path) -> list[str]:
    """Extract Markdown link and image targets."""
    text = path.read_text(encoding="utf-8")
    return re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text)


def validate_markdown_links(files: list[Path]) -> None:
    """Validate every relative Markdown target without accessing the network."""
    for path in (item for item in files if item.suffix.lower() == ".md"):
        for target in markdown_links(path):
            target = target.strip().strip("<>").split("#", 1)[0]
            if (
                not target
                or re.match(r"^[a-z]+://", target, flags=re.IGNORECASE)
                or target.startswith("mailto:")
            ):
                continue
            resolved = (path.parent / target).resolve()
            require(
                resolved.is_relative_to(ROOT.resolve()),
                f"link escapes repository: {path} -> {target}",
            )
            require(
                resolved.exists(),
                f"broken relative link: {path.relative_to(ROOT)} -> {target}",
            )


def validate_sums() -> None:
    """Verify every SHA256SUMS entry."""
    sums = ROOT / "results" / "manifests" / "SHA256SUMS"
    seen: set[str] = set()
    for line in sums.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split(None, 1)
        relative = relative.lstrip("* ")
        require(relative not in seen, f"duplicate SHA256SUMS path: {relative}")
        seen.add(relative)
        path = ROOT / relative
        require(path.is_file(), f"SHA256SUMS target missing: {relative}")
        require(sha256(path) == expected, f"SHA256SUMS mismatch: {relative}")
    require(len(seen) == 12, f"expected 12 checksummed tables/PNGs, found {len(seen)}")


def validate_source_manifest(files: list[Path]) -> None:
    """Validate coverage, classification, targets, and public hashes in SOURCE_MANIFEST."""
    manifest = ROOT / "provenance" / "SOURCE_MANIFEST.csv"
    with manifest.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    destinations = [row["destination_path"] for row in rows]
    require(
        len(destinations) == len(set(destinations)),
        "duplicate SOURCE_MANIFEST destination",
    )
    expected = {path.relative_to(ROOT).as_posix() for path in files}
    require(
        set(destinations) == expected, "SOURCE_MANIFEST must classify every public file"
    )
    for row in rows:
        relative = row["destination_path"]
        require(
            row["classification"] in CLASSIFICATIONS,
            f"invalid classification: {relative}",
        )
        require((ROOT / relative).is_file(), f"manifest target missing: {relative}")
        if relative == "provenance/SOURCE_MANIFEST.csv":
            require(not row["public_sha256"], "SOURCE_MANIFEST self hash must be blank")
        else:
            require(
                row["public_sha256"] == sha256(ROOT / relative),
                f"manifest public hash mismatch: {relative}",
            )


def validate_bilingual_facts() -> None:
    """Validate critical English/Chinese numbers and status language."""
    english = (ROOT / "README.md").read_text(encoding="utf-8")
    chinese = (ROOT / "README_CN.md").read_text(encoding="utf-8")
    required_facts = ("0.16037", "0.08311", "0.526", "0.435", "5", "32", "6")
    for fact in required_facts:
        require(fact in english and fact in chinese, f"bilingual fact missing: {fact}")
    require(
        "not an official Tencent repository" in english,
        "English independent disclaimer missing",
    )
    require(
        "不是 Tencent 官方仓库" in chinese, "Chinese independent disclaimer missing"
    )
    require(
        "Draft" in english and "Draft" in chinese, "PR Draft status must be visible"
    )
    require(
        "PR #216 is merged" not in english and "PR #216 | Merged" not in english,
        "README may imply PR #216 merged",
    )
    require(
        250 <= len(english.splitlines()) <= 400,
        "README.md should contain 250-400 lines",
    )


def validate_git_clean(allow_dirty: bool) -> None:
    """Require a clean Git worktree unless explicitly validating pre-commit content."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    if not allow_dirty:
        require(
            not result.stdout.strip(), f"Git worktree is not clean:\n{result.stdout}"
        )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Skip the final clean-worktree gate during pre-commit validation.",
    )
    return parser.parse_args()


def main() -> None:
    """Run every public-repository validation gate."""
    args = parse_args()
    files = public_files()
    validate_required_and_size(files)
    validate_sensitive_content(files)
    validate_structured_files(files)
    validate_pngs()
    validate_markdown_links(files)
    validate_sums()
    validate_source_manifest(files)
    validate_bilingual_facts()
    validate_git_clean(args.allow_dirty)
    total = sum(path.stat().st_size for path in files)
    print(f"PASS: public repository validated ({len(files)} files, {total} bytes)")


if __name__ == "__main__":
    main()
