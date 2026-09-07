---
status: Active
consensus: converged
consensus_note: >-
  Four labs and every frontier model the record holds from 2024 on: DeepSeek
  (LIT-160, LIT-139), Moonshot (LIT-132, LIT-131), Alibaba (LIT-182, LIT-136)
  and NVIDIA (LIT-183). The one dense frontier recipe in the corpus is Llama 3
  (LIT-179), from 2024. Dissent is not marginal because nobody argues — it is
  marginal because the people still training dense at this scale are doing it
  for reasons other than believing it wins on compute.
title: 'Make the feed-forward layers a sparse mixture of experts once the model is large enough to be compute-bound'
version: 1
tags:
- model-architecture
date: '2026-09-07'
published: '2024-01-01'
source:
- LIT-tmp70cvq
- LIT-tmp2mas2
- LIT-tmpb4jjp
- LIT-170
- LIT-160
implementations:
- DeepSeek-V3
- DeepSeek-V4
- Kimi K2
- Kimi K3
- Qwen3
- Nemotron 3 Nano
summary: >-
  Shazeer et al. (2017), [LIT-tmp70cvq](../literature.d/LIT-tmp70cvq.md) — route each token to a few of
  many feed-forward experts instead of running one dense feed-forward for
  every token, so total parameters and per-token compute stop being the same
  number. Measured against dense by [LIT-170](../literature.d/LIT-170.md) seven years later:
  DeepSeekMoE 16B matches LLaMA2 7B at roughly 40% of the compute, 145B
  approaches the same team's dense 67B at 28.5%.
extended_by:
- SOTA-148
- SOTA-tmpa982c
---

# SOTA-tmpstbim: Make the feed-forward layers a sparse mixture of experts once the model is large enough to be compute-bound

A dense transformer runs every parameter for every token, so capacity and cost
rise together. A mixture of experts breaks that coupling: hold many
feed-forward experts, route each token to a few, and total parameters stop
determining per-token compute.

The ratios are the right way to read the claim, because an efficiency result
stated as a benchmark score hides what it cost
([LIT-170](../literature.d/LIT-170.md)):

| | |
|---|---|
| DeepSeekMoE 2B | matches GShard 2.9B, which has 1.5× the expert parameters and compute |
| DeepSeekMoE 16B | matches LLaMA2 7B at **~40%** of the compute |
| DeepSeekMoE 145B | approaches the same team's dense 67B at **28.5%** |

"Once the model is large enough to be compute-bound" is doing real work in the
title.

<!-- inactive-ok-block: SOTA-125 — Proposed, named as the opposite trade at
     the other end of the scale range -->

[SOTA-125](SOTA-125.md) is the record recommending the opposite at the other
end: at a tiny parameter budget, spend on depth and state width, not on
experts nobody can afford to hold in memory. Nothing here argues for sparsity
at small scale.

## Why this was not filed until now

The record has held this material for a while and deliberately left it
unfiled. [LIT-170](../literature.d/LIT-170.md) put the question plainly: whether the anthology carries MoE
routing as practice, "and it is not obvious it should, since the choice is
upstream of almost everything it does recommend."

That is the argument this practice answers rather than ignores. Being upstream
is a reason to say it *once*, clearly, rather than to leave it as the
unexamined premise of a dozen downstream recommendations — which is what it
had become.

<!-- inactive-ok-block: SOTA-146 — Proposed, and the point is that its caveat
     had no architecture behind it -->

[SOTA-146](SOTA-146.md) already carries a caveat about RL being unstable on
mixture-of-experts specifically, and until now that caveat qualified an
architecture the record had never recommended.

## The line this came from

The record now holds it end to end, which it did not when this practice was
first drafted:

| | | |
|---|---|---|
| [LIT-tmp70cvq](../literature.d/LIT-tmp70cvq.md) | 2017 | the sparsely-gated layer itself, between LSTM layers, and the auxiliary balancing loss that came with it |
| [LIT-tmp2mas2](../literature.d/LIT-tmp2mas2.md) | 2020 | into the transformer, sharded across 2048 TPUs; top-2 routing with a capacity factor |
| [LIT-tmpb4jjp](../literature.d/LIT-tmpb4jjp.md) | 2021 | top-1 routing, a float32 router for stability, a trillion parameters |
| [LIT-170](../literature.d/LIT-170.md) | 2024 | many small experts plus a shared one, and the dense comparisons above |

Reading the granularity argument across them is the reason the whole line is
worth holding: GShard says route to two experts, Switch says one, DeepSeekMoE
says many small ones and take more of them. Three answers to how finely the
router should choose, and the record recommends the third
([SOTA-tmpa982c](SOTA-tmpa982c.md)).

<!-- inactive-ok-block: SOTA-148 — Proposed, named as the far end of the
     load-balancing argument this line opens -->

The same span covers load balancing.
[LIT-tmp70cvq](../literature.d/LIT-tmp70cvq.md) introduces an auxiliary loss
to keep experts evenly used, because the gate self-reinforces; seven years
later [SOTA-148](SOTA-148.md) recommends taking that loss back out and using
a bias instead. The record holds both ends of that argument.
