# Methods

## Formal MoT set

Five `v10_mot` models were independently trained with seeds 0-4 on VisDrone2019-DET for 30 epochs, batch 8, image
size 640, and FP32. Manifest validation requires distinct experiment identity, logical seed, and checkpoint SHA256.

## Fixed-image routing export

Each formal checkpoint was evaluated on the same `val-fixed32` manifest: 32 fixed validation images, six captured
MoT layers, and three experts (`LocalConvTransformer`, `WindowTransformer`, and `DeformableTransformer`). Export
records carry experiment, checkpoint, image, layer, expert, dataset, split, and status identity.

## Cross-seed alignment

Records are aligned only when dataset/version, split, image identity, model variant, and layer agree. Five seeds
produce ten unordered seed pairs. Each pair has 32 × 6 = 192 aligned image-layer comparisons, for 1,920 formal rows.

## Metrics

- Dominant-expert agreement: whether two seeds have the same most-used expert in an aligned image-layer record.
- Token top-1 agreement: fraction of aligned tokens assigned to the same top-1 expert.
- Jensen-Shannon divergence: symmetric distribution difference for aligned expert probabilities.
- Route entropy: uncertainty/dispersal within a routing distribution; not an agreement metric.
- Expert utilization: selected-token share for each layer/expert, summarized across five seeds.

The utilization output has 18 formal summary rows (6 layers × 3 experts) and 90 per-seed entries (5 × 6 × 3).
Seed pairs are used for agreement and JSD, not utilization replication.

## Determinism audit

Repeated same-checkpoint exports generated 960 recorded checks, all marked passed. This checks export repeatability
for the recorded environment; it does not make independently trained seeds identical and does not guarantee every
CUDA kernel is bitwise deterministic in every environment.

## Architecture controls

EsMoE `v10` has three AMP seeds, MoA `v10_moa` has one AMP seed, and MoT `v10_mot` has five FP32 seeds. All use 30
epochs, batch 8, image size 640, and VisDrone2019-DET. Architecture statistics are descriptive because seed counts
and precision modes are unequal. Sample SD is reported only for n≥2.

## Integrity gates

All nine formal checkpoints must exist in the original formal environment, match their manifests, be unique, and
link to finite final metrics. The public repository retains metadata and hashes, not checkpoint binaries.
