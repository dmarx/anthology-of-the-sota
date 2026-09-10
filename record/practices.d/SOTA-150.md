---
number: 150
status: Active
formerly:
- SOTA-tmpstbim
consensus: converged
consensus_note: >-
  Four labs and every frontier model the record holds from 2024 on: DeepSeek
  (LIT-160, LIT-139), Moonshot (LIT-132, LIT-131), Alibaba (LIT-182, LIT-136)
  and NVIDIA (LIT-183). The one dense frontier recipe in the corpus is Llama 3
  (LIT-179), from 2024. Dissent is not marginal because nobody argues — it is
  marginal because the people still training dense at this scale are doing it
  for reasons other than believing it wins on compute.
title: 'Make the feed-forward layers a sparse mixture of experts once the model is large enough to be compute-bound'
version: 3
history:
- version: 2
  date: '2026-09-07'
  note: >-
    LIT-160 removed from the source list. DeepSeek-V3 demonstrates the
    recipe at 671B and does not compare it against a matched dense model, so
    it is evidence about the field — where the consensus_note already
    counted it. `converged` is unaffected: it rests on four labs and every
    frontier model since 2024, all of which are adoption by design.
- version: 3
  date: '2026-09-10'
  note: >-
    Corrected `published:`, which is derived from the primary source and
    had gone stale: LIT-170's date survived the re-source that put
    LIT-188 first. Found by the #119 backfill. The recommendation and
    the source list are unchanged.
tags:
- model-architecture
date: '2026-09-07'
published: '2017-01-01'
source:
# The four works that established the claim. LIT-160 came out: DeepSeek-V3
# demonstrates the recipe at 671B without comparing it against a dense model
# of matched cost, which is adoption (ADR-017), and the consensus_note
# already counts it among the four labs.
- LIT-188
- LIT-187
- LIT-189
- LIT-170
implementations:
- DeepSeek-V3
- DeepSeek-V4
- Kimi K2
- Kimi K3
- Qwen3
- Nemotron 3 Nano
summary: >-
  Shazeer et al. (2017), [LIT-188](../literature.d/LIT-188.md) — route each token to a few of
  many feed-forward experts instead of running one dense feed-forward for
  every token, so total parameters and per-token compute stop being the same
  number. Measured against dense by [LIT-170](../literature.d/LIT-170.md) seven years later:
  DeepSeekMoE 16B matches LLaMA2 7B at roughly 40% of the compute, 145B
  approaches the same team's dense 67B at 28.5%.
extended_by:
- SOTA-148
- SOTA-149
- SOTA-180
---

# SOTA-150: Make the feed-forward layers a sparse mixture of experts once the model is large enough to be compute-bound

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

## Where the width goes, once you have said yes

This practice answers *whether* to make the feed-forward layers sparse. It
does not answer where the parameters should sit, and [LIT-196](../literature.d/LIT-196.md) argues that
the second question has a different answer than the field's defaults assume.

Its premise is a roofline result: at latency-critical batch sizes the
per-expert token count is small, arithmetic intensity is low, and expert
computation is **bandwidth-bound rather than compute-bound**. Optimising
accuracy per FLOP is then optimising against the wrong constraint, and
accuracy *per parameter* — memory footprint, weight-loading bandwidth,
routing traffic, sharding — is what binds. LatentMoE follows that by
down-projecting tokens into a narrow latent space before the routed experts
and keeping those experts' weights there, while routing and the shared
experts stay at full width; dispatch volume and weight-loading bandwidth both
fall by the width ratio, and the saving is spent on more experts rather than
on a smaller model.

Worth carrying here because it is the base Kimi K3's expert layer is built on
([LIT-131](../literature.d/LIT-131.md)), and because the premise is the sort of claim that silently decides
an architecture. Not filed as its own practice: one originating lab with one
outside adopter, and no independent comparison against a conventional MoE at
matched serving conditions.

## The line this came from

The record now holds it end to end, which it did not when this practice was
first drafted:

| | | |
|---|---|---|
| [LIT-188](../literature.d/LIT-188.md) | 2017 | the sparsely-gated layer itself, between LSTM layers, and the auxiliary balancing loss that came with it |
| [LIT-187](../literature.d/LIT-187.md) | 2020 | into the transformer, sharded across 2048 TPUs; top-2 routing with a capacity factor |
| [LIT-189](../literature.d/LIT-189.md) | 2021 | top-1 routing, a float32 router for stability, a trillion parameters |
| [LIT-170](../literature.d/LIT-170.md) | 2024 | many small experts plus a shared one, and the dense comparisons above |
| [LIT-160](../literature.d/LIT-160.md) | 2024 | the recipe at frontier scale — 671B total, 37B active, trained end to end and reported in full, which is what made the argument load-bearing rather than a scaling study |

Reading the granularity argument across them is the reason the whole line is
worth holding: GShard says route to two experts, Switch says one, DeepSeekMoE
says many small ones and take more of them. Three answers to how finely the
router should choose, and the record recommends the third
([SOTA-149](SOTA-149.md)).

<!-- inactive-ok-block: SOTA-148 — Proposed, named as the far end of the
     load-balancing argument this line opens -->

The same span covers load balancing.
[LIT-188](../literature.d/LIT-188.md) introduces an auxiliary loss
to keep experts evenly used, because the gate self-reinforces; seven years
later [SOTA-148](SOTA-148.md) recommends taking that loss back out and using
a bias instead. The record holds both ends of that argument.
