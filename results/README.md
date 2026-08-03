# Results guide

The public evidence package contains six compact formal tables and five deterministic figures. The landing page
uses only the first three figures; utilization and pairwise views remain here and in the routing document.

## Tables

- `architecture_summary.csv`: descriptive architecture-level performance.
- `mot_seed_metrics.csv`: five independent MoT runs and checkpoint identities.
- `mot_layer_stability.csv`: six-layer agreement summary.
- `expert_utilization_summary.csv`: 6 layers × 3 experts.
- `pairwise_seed_summary.csv`: ten seed pairs, aggregated over aligned images and layers.
- `checkpoint_index.csv`: nine metadata-only formal checkpoint records.

## Figures

- `architecture_performance.png`: EsMoE n=3, MoA n=1, MoT n=5.
- `mot_seed_performance.png`: five independently trained MoT seeds.
- `mot_layer_routing_stability.png`: dominant and token top-1 agreement over six layers.
- `expert_utilization_heatmap.png`: cross-seed mean utilization; every layer sums to approximately one.
- `pairwise_routing_agreement.png`: ten descriptive seed-pair aggregates, not ten training replicates.

Every figure is generated from `results/tables/` by `scripts/analysis/build_portfolio_figures.py`.
