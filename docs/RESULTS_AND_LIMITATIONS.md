# Results and limitations

## Results

Five distinct MoT checkpoints produce mAP50 `0.160366 ± 0.002928` and mAP50-95 `0.083112 ± 0.001834` (mean ±
sample SD). In the same five-seed set, global dominant-expert agreement is `0.526042` and token top-1 agreement is
`0.435361`, with pronounced differences across six layers.

All 960 same-checkpoint determinism rows passed. That supports repeatable routing export in the recorded environment
while leaving cross-seed route identity only partially reproduced.

EsMoE n=3 reports mAP50 `0.160010 ± 0.003501` and mAP50-95 `0.083680 ± 0.002003`. MoA n=1 reports `0.158440` and
`0.081640`; no MoA between-seed SD is estimated. The architecture comparison is descriptive.

## Limitations coupled to each result

| Observation | Required limitation |
|---|---|
| MoT detection metrics vary little across five seeds | Five seeds remain protocol-specific and do not establish universal stability. |
| Cross-seed route agreement is moderate or low globally | Agreement is not causal evidence for accuracy and depends on metric/layer. |
| One layer reaches dominant agreement 1.0 | Token agreement remains below 1.0; a layer result does not generalize to the model. |
| Entropy is near its three-expert maximum | Entropy is not an agreement or stability measure. |
| Same-checkpoint repeated export agrees | Export repeatability is not cross-seed reproducibility. |
| EsMoE and MoT means are close | Unequal n and precision prevent balanced inference or equivalence claims. |
| MoA provides a control value | n=1 cannot estimate variance or cross-seed stability. |

## General evidence boundaries

- One dataset, one 30-epoch protocol, and one fixed 32-image routing split are represented.
- Independent training seed is the highest experimental unit.
- Pairwise rows share seeds and are not independent experiments.
- Expert selection frequency does not establish semantic specialization.
- Deterministic settings have environment- and kernel-level limits.
- Checkpoints, datasets, raw logs, and large raw JSON are absent from public Git.
- PR #216 was Open and Ready for review on 2026-08-03; it was not merged, and upstream acceptance is not implied.
- No SOTA, causal, or universal architecture claim is supported.

Read [Methods](METHODS.md), [Routing stability](ROUTING_STABILITY.md), and
[Architecture controls](ARCHITECTURE_CONTROLS.md) alongside the public tables.
