# Research question

The primary question is whether similar detection performance across independently trained MoT seeds also implies
that the internal routing explanation is reproducible.

The study separates four questions:

1. How variable are mAP50 and mAP50-95 across five independently trained MoT seeds?
2. Do those seeds agree on dominant experts and token top-1 routing for the same fixed validation images?
3. Does routing agreement vary across the six captured MoT layers?
4. How do the MoT detection results compare descriptively with EsMoE and MoA controls under the recorded protocol?

The highest experimental unit is one independently trained seed/checkpoint. Images, tokens, layers, export repeats,
and seed pairs support measurement but do not increase the number of independent training repetitions.

The evidence may show coexisting performance stability and routing disagreement. It does not by itself explain why
that coexistence occurs, prove that routing instability causes accuracy loss, or establish fixed expert semantics.
