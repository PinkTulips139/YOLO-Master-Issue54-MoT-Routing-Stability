# Publication review report — v1.0.1

Audit and build date: 2026-08-03 (Asia/Shanghai).

## Outcome

This directory is a new independent research portfolio for Tencent/YOLO-Master Issue #54. It contains bilingual
landing pages, compact formal result tables, seven deterministic PNG assets, path-parameterized protocol records,
validation scripts, exact compatibility patches, model metadata, and file-level provenance.

It is not a copy of Tencent/YOLO-Master and contains no dataset, checkpoint, raw log, large cross-seed JSON,
compressed archive, private URL, or private absolute path.

## Read-only source audit

- Source branch: `issue54-mot-routing-stability`.
- Source HEAD: `dd490a80840dd70836e9363e14630039c7086a87`.
- Expected HEAD: exact match.
- Source worktree: clean before extraction and after read-only evidence audit.
- Active Git operations: none.
- Source residuals: ignored `.pytest_cache`, `.ruff_cache`, and `runs`; none copied.
- Issue #50 design reference: read-only; only portfolio presentation principles were reused.
- Prohibited Issue #50 original project: not accessed.

## Formal evidence

- MoT n=5 FP32, EsMoE n=3 AMP, MoA n=1 AMP.
- VisDrone2019-DET, 30 epochs, batch 8, image size 640.
- Routing: 32 fixed images, six layers, three experts, ten seed pairs.
- Nine mutually distinct formal checkpoint SHA256 values.
- MoT mAP50 `0.160366 ± 0.002928`; mAP50-95 `0.083112 ± 0.001834`.
- Global dominant agreement `0.5260416667`; token top-1 agreement `0.4353613281`.
- Same-checkpoint determinism: 960/960 passed.
- Source `SHA256SUMS`: every listed MoT/control entry passed.

## Public/private boundary

Public evidence includes six derived CSV tables, five result figures, a banner, a Social Preview, formal hashes, a
report manifest, source provenance, two exact patches, and validation/reproduction tooling.

Private archive copies include only the formal 3,112,098-byte cross-seed JSON and the 274,694-byte downloaded
provenance bundle, with private SHA256 records. The existing `Issue54-LocalArchive` remains unchanged.

## Visual review

- Banner: 1600 × 500; project title, five seeds, six layers, global agreements, three-expert routing motif, and
  independent-portfolio label.
- Result figures: 1200 × 720 each; deep blue/cyan/gray palette; no 3D or decorative AI imagery.
- Homepage embeds the banner and only three primary figures.
- Secondary utilization and pairwise figures remain in the result/routing pages.
- PNGs were visually inspected for clipping, overlap, legibility, and scientific labeling.

## Source and contribution records

The provenance manifest classifies every public file. The commit map records the six requested source commits,
including the two-parent merge and the presentation/evidence-only head commit. Two exact mail-format patches preserve
the cross-version and exploration-gradient/legacy-reduction fixes.

## License and citation

The audited upstream AGPL-3.0 license is copied. Third-party notices distinguish Tencent/YOLO-Master, Ultralytics,
VisDrone, PyTorch, Matplotlib, and other dependencies. The personal `CITATION.cff` cites this repository and links
the upstream project/Issue without guessing a YOLO-Master DOI.

## PR and screenshots

PR #216 was Open and Ready for review at current head `cdffaaf3` on 2026-08-03. CI run #234 passed all required
checks; conditional jobs were skipped rather than failed. The formal evidence remains anchored to `dd490a8`, and no
formal experiment result changed. No GitHub UI screenshot is claimed or fabricated. Manual capture instructions are
in `docs/screenshots/SCREENSHOT_CHECKLIST.md`.

## Validation gates

The release workflow validates numeric semantics, checkpoint uniqueness, sample-SD rules, complete layer/expert/pair
coverage, utilization sums, structured files, Markdown links, image decoding/dimensions, checksums, source-manifest
coverage, bilingual facts, repository size, forbidden content, deterministic PNG reproduction, Python compilation,
Ruff, Git whitespace, and clean-worktree state.

## Publication boundary

Version v1.0.1 may be published only after all local gates pass, the remote branch is confirmed to contain no unknown
commits, and tag `v1.0.0` is rechecked unchanged. Publication must use normal push only. No force, amend, reset,
clean, rebase, or history rewrite is authorized.

## Remaining manual items

1. Upload `docs/assets/social-preview.png` through the GitHub Social preview settings UI.
2. Optionally capture a safely cropped PR #216 CI #234 screenshot using the checklist.
3. Recheck PR #216 state before any future release or citation.
4. Keep checkpoint and dataset publication disabled until separate license/provenance approval exists.
