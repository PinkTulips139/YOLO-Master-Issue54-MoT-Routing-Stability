# Formal evidence index

## Audited source roots

- MoT routing evidence: `docs/issue54/phase3_mot_routing/` at source commit `dd490a8`.
- Architecture controls: `docs/issue54/phase3_architecture_controls/` at source commit `dd490a8`.
- Existing formal root is represented publicly as `${FORMAL_ROOT}`.

All entries listed by the two source `SHA256SUMS` files passed during the read-only audit. Exact hashes are preserved
in [FORMAL_EVIDENCE_HASHES.md](../results/manifests/FORMAL_EVIDENCE_HASHES.md).

## Source to public derivative

| Source evidence | Public derivative |
|---|---|
| Formal architecture summary CSV | `results/tables/architecture_summary.csv` |
| Formal architecture run metrics CSV | `results/tables/checkpoint_index.csv`, `models/MODEL_INDEX.csv` |
| Formal MoT seed metrics CSV | `results/tables/mot_seed_metrics.csv` |
| Formal layer stability CSV / cross-seed JSON | `results/tables/mot_layer_stability.csv` |
| Formal utilization CSV / cross-seed JSON | `results/tables/expert_utilization_summary.csv` |
| Formal pairwise CSV / cross-seed JSON | `results/tables/pairwise_seed_summary.csv` |
| Six public tables | Five result figures and repository banner |

## Raw evidence boundary

The 3,112,098-byte cross-seed JSON and 274,694-byte provenance bundle are not in public Git. Their SHA256, size,
placeholder private location, and public derivatives are recorded in [RAW_EVIDENCE_INDEX.csv](RAW_EVIDENCE_INDEX.csv).

No checkpoint, dataset, raw log, compressed archive, or private path is required to review the compact public
claims. Full experimental reproduction still requires separately controlled source/data/compute access.
