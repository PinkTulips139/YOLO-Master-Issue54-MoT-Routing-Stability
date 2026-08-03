# Experiment protocol and evidence classes

The public protocol is recorded in [formal_protocol.yaml](../configs/formal_protocol.yaml). Evidence classes are not
interchangeable.

| Class | Meaning | May support formal conclusions? |
|---|---|---|
| `formal` / `passed` | Completed predeclared run with valid manifest, finite metrics, checkpoint hash, and required artifacts | Yes, within protocol |
| `control` | Formal EsMoE or MoA architecture comparison without fabricated MoT routes | Detection comparison only |
| `diagnostic` | Engineering evidence used to locate a failure or calibrate a workflow | No |
| `smoke` | Small execution/integration check | No |
| `failed` | Run or implementation did not satisfy completion/validity gates | No |
| `not_executed` | Planned command or missing-data state that did not run | No |
| `routing-only` | Export from an already trained checkpoint | Routing evidence only; not a new seed |
| `repeated export` | Same checkpoint/input exported again for determinism | Repeatability check; not a new seed |

## Formal detection protocol

- Dataset: VisDrone2019-DET.
- Epochs: 30.
- Batch: 8.
- Image size: 640.
- MoT: FP32 seeds 0-4.
- EsMoE: AMP seeds 0-2.
- MoA: AMP seed 0.

## Formal routing protocol

- Model: `v10_mot` only.
- Split: `val-fixed32`.
- Images: 32 fixed identities.
- Layers: six, in architecture order.
- Experts: three.
- Seed pairs: ten unordered pairs.
- Same-checkpoint repeated export: required determinism audit.

## Counting and inference

One independently trained seed/checkpoint is one repetition. Images, tokens, layers, pairwise rows, and repeated
exports are nested measurements. They cannot substitute for independent training seeds or inflate n.

## Publication gate

Public derivatives must be finite, schema-valid, path-sanitized, linked to formal source hashes, and free of raw
weights/data/logs. Any uncertain source or license remains excluded and is recorded in
[MISSING_ARTIFACTS.md](../MISSING_ARTIFACTS.md).
