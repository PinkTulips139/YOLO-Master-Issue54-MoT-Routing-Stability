# Tencent/YOLO-Master Issue #54 contribution

## Task context

- Issue: <https://github.com/Tencent/YOLO-Master/issues/54>
- Topic: MoT ablation, routing interpretability, mixed architecture exploration, and stability/boundary testing.
- Public state at the 2026-08-03 snapshot: Open.

## Delivered research scope

The audited Issue #54 branch implements a controlled multi-seed study rather than treating images or tokens as
independent repetitions. Formal evidence covers five MoT seeds, three EsMoE control seeds, and one MoA control seed
on VisDrone2019-DET.

MoT routing evidence uses the same 32 validation images, six MoT layers, and three experts for each checkpoint. The
analysis aligns records across seeds and computes dominant agreement, token top-1 agreement, Jensen-Shannon
divergence, route entropy context, and expert utilization.

## Engineering scope

- Versioned manifest and routing-record schemas.
- Formal experiment registry and duplicate-checkpoint rejection.
- Isolated seed runners and strict serial queues.
- Deterministic fixed-image routing export and same-checkpoint repeat audit.
- Architecture control report generation without fabricated routing evidence.
- AMP dtype, Torch 1.8, export scatter, exploration-gradient, reduction, routed-protocol, and MoA sparse compatibility.
- Tests for boundaries, sparse/dense parity, DDP contracts, routing diagnostics, queues, and legacy compatibility.

## Evidence-bounded completion

The resulting evidence supports a cautious conclusion: detection performance is relatively stable across the five
MoT seeds, while internal routing agreement is only moderate or low overall and differs by layer.

It does not establish scenario-specific expert semantics, causal effects of routing instability, universal MoT
superiority, MoA cross-seed stability, or state of the art.

## Relevant upstream entry points

The audited branch contains `scripts/issue54/run_phase3_seed.py`, `run_phase3_formal_queue.py`,
`run_phase3_control_seed.py`, `run_phase3_controls_queue.py`, `export_mot_routing.py`,
`analyze_cross_seed_routing.py`, and report builders. They belong to the separate upstream-derived checkout and are
not copied wholesale into this portfolio.
