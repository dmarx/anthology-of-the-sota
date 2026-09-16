---
status: Read
paper: LIT-185
title: 'EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test'
version: 1
date: '2026-09-16'
summary: >-
  EAGLE predicted the target model's features and then read tokens off them.
  That constraint is why feeding it more training data stopped helping. Drop
  it — predict tokens directly, fuse low, mid and high features instead of
  reusing the top layer, and simulate the multi-step draft during training so
  step two sees its own step-one output. The result is a scaling law for
  inference acceleration: more draft data, proportionally more speedup, up to
  6.5x. And it raises throughput 1.38x at batch 64, where speculation is
  supposed to stop paying.
---

<!-- inactive-ok-file: SOTA-tmpe5h20 — Proposed, and the practice this
     reading supports. Proposed because one target and one benchmark is
     what the paper has, which is stated in the practice's own
     promote_when. -->
<!-- inactive-ok-file: ADR-041 — Proposed, the resting state of most of
     this record's decisions, and cited as the rule under which this
     paper's architectural settings stay in the reading. -->

# NOTE-tmpoib77: EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test

## Contribution

A draft-model architecture and training procedure for speculative sampling
that, unlike its predecessors, keeps improving as its training data grows. The
paper's framing is diagnostic first: it observes that scaling EAGLE's data
stops helping, identifies the feature-prediction objective as the cause, and
removes it.

## Key insight

The draft's job is to propose *tokens*. EAGLE trained it to predict the target
model's *features* and derive tokens from them, which supplies a useful
training signal for multi-step drafting but constrains the draft's
expressiveness — so extra data buys little. Remove the constraint and step-one
acceptance improves immediately; but then step two receives a step-one output
far from the ground-truth feature it was trained against, and collapses.
**Training-time test** fixes that by running step one inside training, so the
distribution the draft sees at step two is the one it will actually face.

## Assumptions

- The target model's intermediate activations are accessible at serving time —
  low, mid and high layers, not just the final hidden state.
- The draft can be trained on a large corpus of target-model outputs; the
  scaling result is about the volume of that data.
- Acceptance is measured under standard speculative sampling, so the output
  distribution is the target's regardless of draft quality ([SOTA-227](../practices.d/SOTA-227.md)).
- Results are on LLaMA-Instruct-family and DeepSeek-R1-Distill targets; the
  architecture assumes a decoder stack whose layers can be tapped.

## Key results

- **Scaling law for inference acceleration.** With the feature constraint
  removed, increasing the draft's training data increases the speedup ratio
  proportionally — a curve the paper says "was never observed in the previous
  works".
  *Holds when:* MT-bench, LLaMA-Instruct 3.1 8B target, data scaled relative
  to ShareGPT.
- **Up to 6.5x speedup**, about **1.4x over EAGLE-2** at batch size 1, trained
  on roughly 8x more data than EAGLE.
  *Holds when:* temperature 0; five tasks across chat and reasoning models;
  MT-bench for chat, GSM8K for reasoning.
- **It raises throughput at batch 64.** In SGLang, a production framework,
  EAGLE-3 improves throughput by **40% (1.38x) at batch size 64** — against
  the common expectation that speculative sampling reduces throughput at large
  batch.
  *Holds when:* SGLang; batch 64; that hardware. One framework, one batch
  size.
- **Multi-layer fusion beats top-layer reuse.** Top-layer features are
  information-equivalent to the *next* token's logits, which makes predicting
  the next-next token from them hard; intermediate layers carry what is
  needed, and become usable only once the feature loss is gone.
  *Holds when:* the training-time-test architecture; the two changes are not
  ablated independently of each other.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | EAGLE's feature-prediction loss is what prevents it benefiting from more training data. | strong | Removing it raises first-token acceptance immediately (Figure 4); the diagnosis is confirmed by the fix working. |
| C2 | Simulating step one during training ("training-time test") is required once the feature loss is removed, or step two collapses. | strong | Acceptance at step two is very low without it and recovers with it. |
| C3 | Speedup scales with draft training data under the new architecture. | moderate | One target model, one benchmark, data scaled relative to ShareGPT; the trend is clear and the range is not large. |
| C4 | Speculative sampling can improve throughput at batch 64, not only latency at batch 1. | moderate | One production framework, one batch size, one target. Contradicts a widely held expectation, which is why it matters and why one measurement is thin. |

## Method

**EAGLE-3.**

The draft predicts tokens directly — no feature-prediction loss. Its input is
a fusion of low-, mid- and high-level features from the target model rather
than the top layer alone. During training, the draft's own step-one output is
fed into step two, so multi-step drafting is trained on the distribution it
will encounter rather than on ground-truth features.

- Direct token prediction, feature loss removed
- Multi-layer feature fusion from the target
- Training-time test: multi-step generation simulated during training
- Roughly 8x EAGLE's training data

## Concepts

- **Training-time test** — running the draft's own multi-step generation
  inside the training loop so later steps see their own earlier outputs. The
  paper's named contribution and the reason the other two changes work.
- **Feature prediction constraint** — training the draft to reproduce the
  target's hidden state. Useful scaffolding for multi-step drafting; a ceiling
  on expressiveness.
- **Acceptance rate `0-alpha`, `1-alpha`** — acceptance of the first and
  second draft tokens, tracked separately. Separating them is what exposed the
  step-two collapse.

## Connections

**Builds on.**

- [LIT-376](../literature.d/LIT-376.md) and [LIT-375](../literature.d/LIT-375.md) — speculative decoding and speculative sampling, the
  mechanism this accelerates and whose distributional guarantee it inherits.

## Recommendations

- **R1** — Train the draft on as much data as you can get; under this
  architecture the speedup keeps rising with it.
  *Topic:* draft training · *Strength:* moderate · *When:* You control the
  draft's training and can generate target-model outputs at volume.
- **R2** — Predict tokens directly rather than the target's features, and fuse
  features from several depths rather than reusing the top layer.
  *Topic:* draft architecture · *Strength:* strong · *When:* Building a draft
  model coupled to a known target.
- **R3** — Simulate the multi-step draft during training. Without it the
  second draft token's acceptance collapses once the feature loss is removed.
  *Topic:* draft training · *Strength:* strong · *When:* Any multi-step draft
  trained without a feature-matching objective.
- **R4** — Do not assume speculation is throughput-negative at serving batch
  sizes; measure it. This reports +40% at batch 64.
  *Topic:* when speculation pays · *Strength:* moderate · *When:* Production
  serving at moderate batch.

## Bearing on the record

Two things, and the second is a correction.

[SOTA-tmpe5h20](../practices.d/SOTA-tmpe5h20.md) is R1 filed: the scaling law is the paper's discovery and the
only one of its recommendations that is about *what to do* rather than about
how to build this particular draft. R2 and R3 are the architecture's internals
and stay here under [ADR-041](../decisions.d/ADR-041.md).

**R4 qualifies [SOTA-227](../practices.d/SOTA-227.md), which this record filed hours ago.** That practice
says speculation is "a latency technique" and that "at a batch size large
enough to saturate the arithmetic units the trade reverses", adding that
neither source measures the crossover and the record holds no measurement of
it. It does — it was in [LIT-185](../literature.d/LIT-185.md), unread, the whole time. One framework at one
batch size is not a refutation, but "the record has no measurement" was false
when written.

## Limitations

- The two architectural changes — direct token prediction and multi-layer
  fusion — are motivated together and not ablated apart, so their individual
  contributions are not separable from this paper.
- The scaling result is one target model on one benchmark over a limited data
  range. "Scaling law" is the paper's word for a trend, not a fitted exponent
  with a range of validity.
- The batch-64 throughput result is one framework, one batch size, one target.
  It is enough to make the common expectation unsafe; it is not enough to
  replace it with a new rule.
- Requires access to the target's intermediate layers, which rules it out for
  a target served behind an API.
- The draft is trained against a specific target. Nothing here says what
  happens to acceptance when that target is updated.

## Open questions

- Where does the throughput advantage actually end, as a function of batch
  size and hardware? The paper reports one point on a curve the field believes
  slopes the other way.
- Does the scaling law continue, and does it have the same exponent for
  reasoning targets as for chat targets?
- How much of the gain survives when the draft cannot see intermediate layers?
