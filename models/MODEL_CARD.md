# Model card: Issue #54 formal checkpoint set

## Summary

This card describes nine metadata-only checkpoint records produced under the audited Issue #54 Phase 3 protocol:
EsMoE n=3, MoA n=1, and MoT n=5. No weights are distributed.

## Training protocol

- Task: VisDrone2019-DET object detection.
- Epochs: 30; batch: 8; image size: 640.
- MoT: FP32, seeds 0-4.
- EsMoE: AMP, seeds 0-2.
- MoA: AMP, seed 0.
- Highest experimental unit: one independently trained seed/checkpoint.

## Intended use

The metadata supports evidence auditing, figure reproduction, routing-stability review, and protocol comparison.
It may guide independent reproduction in a separately obtained YOLO-Master checkout.

## Out-of-scope use

This artifact is not a deployable detector, model-zoo release, safety-certified system, or claim of state of the
art. It should not be used to infer expert semantics, causal effects of routing stability, or general superiority
of one architecture.

## Metrics

The public tables report mAP50, mAP50-95, dominant-expert agreement, token top-1 agreement, Jensen-Shannon
divergence, route entropy context, and expert utilization. Between-seed standard deviation is reported only when
at least two independent training seeds exist.

## Limitations

Seed counts differ by architecture, MoA has only one seed, routing evidence exists only for MoT, and the routing
split contains 32 fixed validation images. Images, layers, tokens, and seed pairs are not independent training
replicates.

## Reproducibility notes

Checkpoint SHA256 values are recorded and unique, but hashes do not grant access or redistribution rights. Exact
reproduction also depends on the upstream revision, data preparation, environment, and deterministic-kernel
limits described in the documentation.
