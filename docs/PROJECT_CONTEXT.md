# Project context and ownership boundary

## Official context

- Upstream: [Tencent/YOLO-Master](https://github.com/Tencent/YOLO-Master).
- Task: [Issue #54](https://github.com/Tencent/YOLO-Master/issues/54), concerning MoT architecture comparison,
  routing interpretability, mixed-architecture exploration, and boundary stability.
- Related contribution: [PR #216](https://github.com/Tencent/YOLO-Master/pull/216).

## Independent portfolio position

This is an independent research portfolio by `PinkTulips139`, not an official Tencent repository. It extracts a
small, auditable evidence package from a read-only Issue #54 branch rather than copying Tencent/YOLO-Master.

The formal evidence snapshot is:

- branch `issue54-mot-routing-stability`;
- commit `dd490a80840dd70836e9363e14630039c7086a87`;
- audit date 2026-08-03 (Asia/Shanghai).

The current PR head is `cdffaaf3e30d1ff742c0cd32f7ce7c295f7a0ade`, after public-evidence slimming. On the dated
2026-08-03 snapshot, PR #216 was Open and Ready for review and CI run #234 had passed. The PR was not merged;
Ready for review and mergeability do not imply acceptance, official endorsement, or ownership of the upstream
framework. The formal scientific evidence remains anchored to `dd490a8` and its recorded provenance.

## Source boundaries

1. `upstream_provided`: unmodified upstream material, primarily the AGPL-3.0 license.
2. `user_added`: Issue #54 scripts/tests and portfolio documentation authored by the contributor.
3. `user_modified_upstream`: personal modifications to upstream-derived files, retained in exact patches.
4. `generated_artifact`: formal reports, public tables, figures, checksums, and manifests.
5. `third_party_reference`: notices and links describing separately licensed projects or data.
6. `public_metadata_only`: hashes and records without the corresponding private binary/raw artifact.
7. `private_only_excluded`: formal raw evidence indexed publicly but kept outside Git.

The authoritative file-level classification is [SOURCE_MANIFEST.csv](../provenance/SOURCE_MANIFEST.csv).

## What is not included

The repository excludes source-repository bulk code, checkpoint binaries, VisDrone data, raw images, raw logs,
TensorBoard, caches, archives, process state, private machine paths, and the large formal cross-seed JSON. See
[Artifact policy](ARTIFACT_POLICY.md) and [Missing artifacts](../MISSING_ARTIFACTS.md).

## Licensing

The audited upstream checkout carries AGPL-3.0, which is retained here. Upstream-derived files keep original
ownership. Dataset and dependency terms remain separate; no third-party content is relicensed by this portfolio.
