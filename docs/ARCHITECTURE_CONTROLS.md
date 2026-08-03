# Architecture controls

## Recorded scope

| Architecture | Model key | Seeds | Precision | mAP50 | mAP50-95 |
|---|---|---:|---|---:|---:|
| EsMoE | `v10` | 3 | AMP | `0.16001 ± 0.00350` | `0.08368 ± 0.00200` |
| MoA | `v10_moa` | 1 | AMP | `0.15844` | `0.08164` |
| MoT | `v10_mot` | 5 | FP32 | `0.16037 ± 0.00293` | `0.08311 ± 0.00183` |

All runs use VisDrone2019-DET, 30 epochs, batch 8, and image size 640. Sample standard deviation is used for EsMoE
and MoT. MoA has only one independent seed, so its SD fields are intentionally blank.

![Descriptive architecture performance](../results/figures/architecture_performance.png)

## Descriptive reading

MoT and EsMoE have close mean detection metrics under this protocol. Their mean difference is about `+0.00036`
for mAP50 and `-0.00057` for mAP50-95 (MoT minus EsMoE). These small mixed-direction differences are not a formal
significance test.

MoA seed 0 records mAP50 `0.15844` and mAP50-95 `0.08164`. A single run may serve as an architecture control, but it
cannot estimate between-seed variance or demonstrate cross-seed stability.

## Comparison boundaries

- Seed counts are unequal: 5, 3, and 1.
- Precision modes differ: MoT FP32; EsMoE and MoA AMP.
- No balanced factorial design or formal hypothesis test is reported.
- Only MoT has routing evidence.
- Similar means do not establish model equivalence.
- The results do not show universal superiority of MoT, EsMoE, or MoA.

Use the [architecture table](../results/tables/architecture_summary.csv) and
[checkpoint index](../results/tables/checkpoint_index.csv) as the authoritative public values.
