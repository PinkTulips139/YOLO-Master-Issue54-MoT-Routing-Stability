# Key commit map

The six commits below were read from the audited source branch. Each listed non-merge commit is authored by
`PinkTulips139`; the merge commit records the contributor's normal merge of reviewed upstream main.

## `e4c202fec6115f6e0c52173a19cbd4efce050093`

- Subject: `feat(issue54): add phase3 architecture controls report`
- Parent: `d21654cb2cc5986c0e255c00300b473f7df9a297`
- Relation: adds the formal EsMoE/MoA/MoT controls report, run/summary CSVs, manifest, checksums, index, and builder.
- Changed files: `.gitattributes`; `docs/issue54/PHASE3_RESULTS_INDEX.md`; five files under
  `docs/issue54/phase3_architecture_controls/`; `scripts/issue54/build_phase3_architecture_controls_report.py`.
- Ownership/type: personal Issue #54 contribution; not a merge; evidence and report-generation commit.

## `0faded9e966b75300f9ab83b1e295962b0dbd42d`

- Subject: `feat(issue54): add isolated Phase 3 runners and queues`
- Parent: `2a211bbd5cdfba1832bc5cb22f4ab7d99ec4634f`
- Relation: adds isolated MoT/control seed runners, strict serial queues, MoT report builder, and queue/runner tests.
- Changed files: five files under `scripts/issue54/`; three `tests/test_phase3_*.py` files.
- Ownership/type: personal Issue #54 contribution; not a merge; execution governance and test commit.

## `a15e43773026b60c1b07a1c746d750793b91df15`

- Subject: `merge: integrate upstream main into issue54 routing stability`
- Parents: `0faded9e966b75300f9ab83b1e295962b0dbd42d` and `a13938ce9cc8f761136384e935e7c65fefa4cfee`.
- Relation: normal non-force merge of the reviewed Tencent upstream main snapshot into the Issue #54 branch.
- Changed files: merge integration is represented by its two-parent topology; no standalone first-parent file list is
  assigned as a new research feature.
- Ownership/type: personal merge commit; **merge commit**; not presentation-only.

## `178701a54bc05f9bd7955d2b8f3ac7e4635e587e`

- Subject: `fix(issue54): restore cross-version mixture compatibility`
- Parent: `a15e43773026b60c1b07a1c746d750793b91df15`
- Relation: restores Torch 1.8 autocast fallback, export-safe scatter, routing protocol compatibility, MoA sparse
  aliases/normalization, and related tests/config compatibility.
- Changed files: `tests/test_mot.py`, `tests/test_routing_diagnostics.py`, `tests/test_torch_legacy_compat.py`,
  `ultralytics/cfg/__init__.py`, `ultralytics/nn/modules/_numeric.py`, two MoA files, `moe/protocol.py`, and two MoT
  files.
- Ownership/type: personal changes to upstream-derived code plus tests; not a merge; exact patch is
  [cross_version_compatibility.patch](../patches/cross_version_compatibility.patch).

## `09c9e0e80fef1b7d64001e4d244b13bb33189197`

- Subject: `fix(issue54): stabilize MoT gradients and legacy reductions`
- Parent: `178701a54bc05f9bd7955d2b8f3ac7e4635e587e`
- Relation: makes positive exploration execute all experts so its weights have a real gradient path, preserves
  sparse behavior when exploration is zero, and replaces unsupported multi-dimension reductions with a legacy-safe
  helper.
- Changed files: `tests/test_mot.py`, `tests/test_mot_sparse_parity.py`, and
  `ultralytics/nn/modules/mot/block.py`.
- Ownership/type: personal changes to upstream-derived code plus tests; not a merge; exact patch is
  [mot_gradients_legacy_reductions.patch](../patches/mot_gradients_legacy_reductions.patch).

## `dd490a80840dd70836e9363e14630039c7086a87`

- Subject: `docs(issue54): add verified routing evidence and visuals`
- Parent: `09c9e0e80fef1b7d64001e4d244b13bb33189197`
- Relation: adds the recovered formal routing evidence, source provenance, checksums, formal reports, two PR figures,
  and deterministic PR visual builder.
- Changed files: 11 formal evidence files under `docs/issue54/phase3_mot_routing/`, two PNG files under
  `docs/issue54/pr_assets/`, and `scripts/issue54/build_pr216_visuals.py`.
- Ownership/type: personal evidence-curation contribution; not a merge; **presentation/evidence-only commit** with no
  runtime model change.

These records establish authorship and topology for the requested commits only. They do not assert that the PR is
merged into Tencent/YOLO-Master.
