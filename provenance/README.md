# Provenance guide

Provenance separates upstream code, personal contributions, generated artifacts, public metadata, and private-only
evidence.

- `SOURCE_MANIFEST.csv`: file-level destination/source/classification/hash record.
- `UPSTREAM_BASE.md`: audited upstream/fork boundary and revision.
- `BRANCH_MAP.md`: branch and merge topology relevant to Issue #54.
- `PR_STATUS.md`: dated PR #216 snapshot, never a live status claim.
- `FORMAL_EVIDENCE_INDEX.md`: formal source-to-public derivative map.
- `RAW_EVIDENCE_INDEX.csv`: placeholder-only index for private evidence.

Classification values are `upstream_provided`, `user_added`, `user_modified_upstream`, `generated_artifact`,
`third_party_reference`, `public_metadata_only`, and `private_only_excluded`.
