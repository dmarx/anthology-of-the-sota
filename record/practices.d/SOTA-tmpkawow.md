---
status: Proposed
consensus: unreplicated
consensus_note: >-
  Two halves with different support. The premise, that at fixed parameter
  count shape barely moves the loss, is Kaplan et al.'s and is now measured a
  second time, by a different group, at about 1/100,000 of the compute. The
  rule built on it, that throughput at constant size is the one lever left, is
  one group's. Many models ship without biases (PaLM, LLaMA), but that is
  adoption: none of them measured this. Read as of 2026-09.
promote_when: >-
  A second group, working under a fixed wall-clock or FLOP budget, compares a
  set of reshapes against a set of step-time cuts at constant parameter count,
  and reports downstream scores as well as loss. The step-time cuts must win
  and the reshapes must not. A paper that removes biases and reports a faster
  step would not settle it, because faster steps are not in doubt. The claim
  is that nothing else in the architecture pays.
title: 'Under a fixed compute budget, change the architecture only where it cuts step time at constant parameter count'
version: 1
tags:
- model-architecture
- training-optimization
- tiny-models
date: '2026-09-25'
source:
- LIT-tmpa75eq
- LIT-028
# LIT-tmpa75eq is the controlled study at small budget and states the rule.
# LIT-028 is the premise, shape insensitivity at fixed size, measured
# independently and at far larger scale (ADR-030).
introduced_by:
- LIT-tmpa75eq
implementations:
- 'cramming (no QKV or linear biases, no decoder bias, sparse token prediction)'
summary: >-
  Geiping and Goldstein (2023), [LIT-tmpa75eq](../literature.d/LIT-tmpa75eq.md). Under a 24-hour, one-GPU budget,
  every reshape tried (depth 4 to 24, deep-narrow, wide, funnel,
  FFN-every-k, shared layers) finishes within about 0.1 of the same MLM loss.
  A smaller model's extra throughput cancels its slower per-token learning.
  So the architecture changes that pay are the ones that make each step
  cheaper without changing how much the model learns per token: dropping
  biases, predicting only masked tokens, and pre-norm for the learning rate it
  permits.
---

<!-- inactive-ok-file: SOTA-190 — Proposed, named as the claim this practice's
     source bounds at small budget without refuting -->

# SOTA-tmpkawow: Under a fixed compute budget, change the architecture only where it cuts step time at constant parameter count

## Source

Geiping and Goldstein (ICML 2023), [LIT-tmpa75eq](../literature.d/LIT-tmpa75eq.md), on the premise
Kaplan et al. measured in [LIT-028](../literature.d/LIT-028.md).

## What to do

When the budget is fixed in time or FLOPs and you are choosing an
architecture, sort candidate changes into two kinds:

1. **Changes to shape at roughly constant size**: depth against width,
   head count, FFN frequency, funnels, layer sharing. Expect them to buy
   nothing in loss. Do not spend the budget searching them.
2. **Changes that make a step cheaper without changing the parameter count
   much**: removing QKV, linear-layer and decoder biases, predicting only the
   masked positions, fused or better-shaped kernels. Take these. Throughput
   is the one quantity at constant size that the scaling law does not
   already fix.

Pre-normalization belongs in the second group for a different reason. By
itself it "has no effect on performance". It stabilizes training enough to
allow the larger learning rate and short warmup, which is where the gain
comes from.

## Why

Per-token progress depends on parameter count and very little on shape. So
a smaller or reshaped model trades learning efficiency for tokens per second
at close to par: "smaller architectures make up for their slower learning
efficiency by higher throughput". From 4 to 24 layers, throughput falls more
than 5x while final MLM loss stays between 1.84 and 1.97. The trade has
nothing to offer. What does move the outcome is ingesting more tokens at the
*same* per-token efficiency, which means a faster step at the same size.

## Conditions

**One regime, and a small one.** MLM, sequence length 128, one GPU for 24
hours, 5 to 13 exaFLOP. The negative half ("shape buys nothing") has Kaplan
behind it at far larger scale. The positive half ("step time is the lever")
has one study.

**It is about loss, and downstream is noisier and not flat.** The same sweep
spans 79.1 to 81.7 MNLI-m. That is a larger spread than the loss suggests,
which is the gap [LIT-052](../literature.d/LIT-052.md) is about: shape can matter
downstream when it does not upstream. This practice's own source tested
[LIT-052](../literature.d/LIT-052.md)'s deep-narrow shape and found no gain at this budget (81.39 against
81.79). That is one run and one task, and it bounds
[SOTA-190](SOTA-190.md) at small budget without refuting it.

**Size is not free either.** The paper does find an optimal size "at a
budget of around 4B tokens", with small gains. Pick the size for the budget,
then apply this rule at that size.

**"Minimal cost" still has a cost.** Cramming dropped rotary embeddings
because their gain in loss was cancelled by the loss of speed, and kept 12
attention heads although fewer were faster, because fewer hurt fine-tuning.
The rule does not say throughput always wins. It says to weigh every change
per unit of wall-clock.

## Known implementations

- **cramming**, the source's own code.
- Bias-free linear layers are common in large language models (PaLM,
  LLaMA). That is adoption, recorded here as context. It is not evidence for
  this rule.
