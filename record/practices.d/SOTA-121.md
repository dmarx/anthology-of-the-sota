---
status: Active
title: 'Use Muon with decoupled weight decay and AdamW-matched update RMS in place of AdamW'
version: 1
tags:
- training-optimization
- tiny-models
date: '2026-09-05'
published: '2026-01-15'
source:
# The blogpost is where the practice is stated as a recipe; LIT-122 is the
# production form and the scaling evidence; LIT-tmpxbtiq is the origin;
# LIT-tmpqpka6 is the outside comparison that puts a smaller number on it
# (ADR-010).
- LIT-119
- LIT-122
- LIT-tmpxbtiq
- LIT-tmpqpka6
summary: >-
  Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost. Stable at nearly the same optimal LR as AdamW, better evaluations; used for every Falcon-H1-Tiny model.
---

# SOTA-121: Use Muon with decoupled weight decay and AdamW-matched update RMS in place of AdamW

## Source

Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost.

Muon as modified in [ARXIV-2502.16982](https://arxiv.org/abs/2502.16982) ([LIT-122](../literature.d/LIT-122.md)): weight decay applied to the
orthogonalised update, and the update's RMS rescaled to match what AdamW
would produce, so that the learning rate and weight decay tuned for AdamW
carry over. Under that recipe the authors saw stable training at nearly the
same optimal learning rate as AdamW and better downstream evaluations, and
adopted it for every model in the series, at 90M and 0.6B.

Conditions: the comparison here is at tiny scale with a µP-parameterised
hybrid Mamba/attention model. The RMS matching is what makes the AdamW
hyperparameters transferable; without it the learning rate has to be
re-tuned. Muon applies to matrix parameters — embeddings, norms and other
vectors keep an Adam-style update.

At a trillion parameters this recipe alone let attention logits run past
1000; [SOTA-131](SOTA-131.md) is the addition that bounds them, and the chain is written
out there.

## How much it buys

Less than the record used to say, and the honest range is wide. [LIT-122](../literature.d/LIT-122.md)'s
scaling-law runs report roughly 2× the compute efficiency of AdamW. An
outside comparison tuning both optimizers separately and judging at the end
of training rather than mid-run ([LIT-tmpqpka6](../literature.d/LIT-tmpqpka6.md)) gets 1.4× at 0.1B, falling
to **1.1× at 1.2B** — and finds that ranking two optimizers on intermediate
checkpoints can reverse the answer, which is one way the larger figures were
reached.

The practice stands at 1.1×, for reasons the number does not carry: the gain
is free once the recipe is in place, Muon's smaller optimizer state and
hyperparameter transferability are not what that study measures, and every
frontier adopter in the record ([LIT-131](../literature.d/LIT-131.md), [LIT-132](../literature.d/LIT-132.md), [LIT-139](../literature.d/LIT-139.md)) trains far above
its largest scale. What should not be quoted any more is the 2×.

[LIT-tmp2hq9o](../literature.d/LIT-tmp2hq9o.md) argues the shrinkage is not intrinsic but an artefact of
constant decoupled weight decay fixing the equilibrium weight norm, and
recovers 20–30% by pinning the norms instead. If that holds up outside its
authors' group it changes this section again.

## Known implementations

- Falcon-H1-Tiny (all released checkpoints); Kimi K2, Kimi K3 and DeepSeek-V4 with the additions in [SOTA-131](SOTA-131.md)
