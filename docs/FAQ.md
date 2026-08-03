# FAQ

## Why can performance be stable while routing is less stable?

Different internal expert allocations can produce similar final predictions or compensate across layers. The study
observes coexistence; it does not identify a causal mechanism.

## Why are the 32 images not 32 independent repetitions?

All images are evaluated by the same trained checkpoint. The independent intervention/repetition is training a new
model seed. Images are nested measurements within each checkpoint.

## Why does MoA have no standard deviation?

MoA has one formal seed. Between-seed sample SD requires at least two independent seeds, so the SD fields are blank.

## Why are checkpoint binaries not published?

Hashes and metadata are enough to audit identity and duplicate counting. Weight redistribution also requires model,
upstream, and dataset-license review; a hash does not grant those rights.

## Why is the raw cross-seed JSON not in Git?

It is formal and only about 3.1 MB, but it expands to a very large review diff. Compact verified tables preserve the
public results, while its 3,112,098-byte size and SHA256 are indexed and the file remains in a private archive.

## Does an unmerged PR invalidate the personal repository?

No. A personal evidence portfolio can document completed work and reproducible results while clearly stating that
the upstream PR is Open and Draft. It must not imply Tencent acceptance or merge.

## What is the difference between entropy and agreement?

Entropy measures dispersal in a route's probability distribution. Agreement compares decisions between seeds.
High entropy is neither necessary nor sufficient for high cross-seed agreement.

## Are the ten seed pairs ten independent experiments?

No. The pairs reuse five trained seeds and are dependent descriptive comparisons. The independent seed count stays
five.

## Does same-checkpoint token agreement 1.0 prove cross-seed reproducibility?

No. It supports deterministic repeated export for the same checkpoint/input in the recorded environment. Cross-seed
agreement remains approximately 0.435 globally.

## Is MoT better than EsMoE or MoA?

This evidence does not support a general superiority claim. Means are close, seed counts differ, precision differs,
and MoA has only one seed. The comparison is descriptive and protocol-specific.
