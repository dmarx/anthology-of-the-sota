---
number: 227
status: Active
formerly:
- SOTA-tmp6mgiw
consensus: converged
consensus_note: >-
  Two independent groups derived it two months apart, and the record's own
  literature is the adoption count: LIT-131, LIT-135 and LIT-136 name
  speculative decoding in their notes, LIT-163 sells multi-token prediction
  partly on it, and LIT-185 is a paper about making the draft cheaper. Not
  `universal` because
  it is chiefly a latency technique, and where it stops paying on throughput
  is less settled than this document first said — see the conditions.
title: 'Decode with a draft model and an accept-reject rule, which is exactly lossless'
version: 1
tags:
- inference-optimization
date: '2026-09-16'
source:
- LIT-376
- LIT-375
introduced_by:
- LIT-376
implementations: []
summary: >-
  Autoregressive decoding runs one serial model pass per token and each pass
  is bounded by streaming the weights, so the arithmetic units idle. Have a
  cheap draft model guess the next `gamma` tokens, score all `gamma + 1`
  positions in one target pass, and keep a prefix under an accept-reject rule
  built so the output distribution is the target's exactly. 2x-3x at 11B and
  2-2.5x at 70B, with no retraining, no architecture change and nothing traded
  away.
extended_by:
- SOTA-tmpe5h20
---

# SOTA-227: Decode with a draft model and an accept-reject rule, which is exactly lossless

## What to do

Put a cheaper model in front of the one you are serving.

1. Draft `gamma` tokens by running the small model autoregressively.
2. Run the target **once**, scoring all `gamma + 1` prefixes in a single
   batched pass.
3. Walk the draft left to right. Accept position `i` when
   `r_i <= p_i(x)/q_i(x)` for `r_i ~ U(0,1)`, where `p` is the target's
   probability and `q` the draft's. At the first rejection, resample that
   position from the normalised positive part of `p - q` and stop.
4. If nothing was rejected you get a free extra token from the target's own
   distribution at position `gamma + 1`.

Any model that exposes logits over the same vocabulary is admissible as the
draft. The accept-reject rule — not the draft's quality — is what carries the
guarantee.

## Why it is free rather than a trade

**The distribution is exactly the target's.** This is the property that
matters and the one most summaries drop. You are not approximating the big
model with the small one; you are using the small one to *propose* and the big
one to *decide*, under a rule constructed so the composite sampler is unbiased.
[LIT-375](../literature.d/LIT-375.md) states the qualifier worth keeping — the guarantee holds "within
hardware numerics" — and [LIT-376](../literature.d/LIT-376.md) measures its results against **identical
outputs**.

**It cannot be slower in target evaluations.** Every parallel target pass
emits at least one token, so the count of serial target runs is bounded above
by what plain decoding would have taken. The only way to lose is the drafting
overhead.

**The compute it spends was already idle.** [LIT-376](../literature.d/LIT-376.md)'s premise, stated
outright: decoding "is often not bottlenecked on arithmetic operations, but
rather on memory bandwidth and communication, so additional computation
resources might be available". [LIT-375](../literature.d/LIT-375.md) measures the consequence — tokens
per second that "often exceeds the idealised ceiling on auto-regressive
sampling speed imposed by the memory bandwidth". The ceiling being beaten is
the one that made decoding slow in the first place.

**And the economics are computable in advance**, which is unusual. Let
`alpha = E(min(p, q))` be the acceptance rate and `c` the draft's per-run cost
relative to the target's. Then

    expected walltime improvement = (1 - alpha^(gamma+1)) / ((1 - alpha)(gamma*c + 1))

so `gamma` is chosen numerically rather than by habit, and a candidate draft
is evaluated on measured `alpha` and `c` rather than on its benchmark scores.
For a near-free draft the improvement approaches `1/(1 - alpha)`.

## Conditions

**It is chiefly a latency technique, and the batch size decides how much it
pays.** The whole argument rests on idle arithmetic. Serving one stream
against a large model, that is the regime, and as batch size grows the
speculative work increasingly competes with real work rather than filling a
gap. Neither source measures the crossover.

**But "the trade reverses" was too strong, and this record held the
counter-example while writing it.** [LIT-185](../literature.d/LIT-185.md) reports EAGLE-3 improving
throughput by **40% at batch size 64** in SGLang, noting explicitly that
speculative sampling "is often thought to reduce throughput at large batch
sizes". That is one framework at one batch size with a very good draft, so it
does not establish a new rule — but the first version of this practice said
the record held no measurement of the crossover, and the measurement was in
[LIT-185](../literature.d/LIT-185.md), unread, at the time. Treat the crossover as workload- and
draft-specific, and measure it rather than assuming its sign.

**Draft and target must share a tokenizer and vocabulary.** The rule compares
per-token probabilities from both models at the same positions.

**Acceptance is workload-dependent and drifts.** `alpha` is a property of the
draft-target *pair* on *your* prompts. A draft that is not retrained alongside
a target that keeps being post-trained will quietly get worse, and nothing in
either paper addresses that.

**2022-2023 infrastructure.** T5-XXL and LaMDA in one paper, Chinchilla in the
other. Neither interacts with paged attention ([SOTA-105](SOTA-105.md)) or continuous
batching ([SOTA-113](SOTA-113.md)), which attack the same bottleneck from different
directions and which this record holds separately without anything relating
the three.

**`gamma` fixed per loop leaves something on the table.** [LIT-376](../literature.d/LIT-376.md)
estimates up to ~60% further improvement from adapting it within a generation
and does not pursue it.

## What builds on this

The record already held two refinements of a practice it did not hold:

- **[LIT-185](../literature.d/LIT-185.md) (EAGLE-3)** is a method for driving the draft's cost toward the
  `c ≈ 0` regime by making it a single decoder layer matched to the target's
  structure. It is `Active` here and unread.
- **[SOTA-162](SOTA-162.md)** trains auxiliary multi-token-prediction heads, and one of its
  two arguments is that "the extra heads are a draft model for speculative
  decoding you did not have to train separately" — a claim that had no
  document behind it until now.

That ordering is [DP-007](../../docs/design-principles.md#dp-7)'s second failure mode exactly: the refinement filed
before the thing it refines. Filing this does not change either document's
content; it gives both something to stand on.

## Known implementations

None recorded as such. Three model reports in this record name speculative
decoding — [LIT-131](../literature.d/LIT-131.md), [LIT-135](../literature.d/LIT-135.md), [LIT-136](../literature.d/LIT-136.md) — which is adoption of the arrangement
rather than an independent measurement of it, and is counted in
`consensus_note` where counting is the right operation ([DP-005](../../docs/design-principles.md#dp-5)).

One correction while counting: [LIT-185](../literature.d/LIT-185.md)'s standing section says [LIT-135](../literature.d/LIT-135.md) and
[LIT-139](../literature.d/LIT-139.md) "ship the same arrangement". [LIT-135](../literature.d/LIT-135.md)'s note bears that out; **[LIT-139](../literature.d/LIT-139.md)'s
does not** — it records multi-token prediction carried over from its
predecessor and says nothing about a draft or about speculative decoding.
Either the note is short of what the paper does or the claim was extrapolated
from the neighbouring reports. It is left as it is here rather than repaired
from the same distance that produced it, and is the kind of thing [#87](https://github.com/dmarx/anthology-of-the-sota/issues/87)'s audit
should pick up next.
