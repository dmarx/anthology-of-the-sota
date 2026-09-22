---
number: 320
status: Proposed
formerly:
- SOTA-tmpyf7w7
promote_when: >-
  The warmup-free result at a scale where warmup is known to be load-bearing —
  a billion-parameter-plus language model pretrained with the spectral cap and
  no warmup, against the same model with its usual warmup, reporting final
  loss and any divergence. What would NOT meet it: another architecture at
  300M or below, or a paper showing the cap helps *alongside* warmup. The
  claim is that warmup becomes unnecessary, and it has only been tested where
  warmup is cheap to do without.
consensus: unreplicated
consensus_note: >-
  One group, one paper, five configurations across three architectures. The
  record holds two Active practices that recommend warmup (SOTA-008,
  SOTA-100), and this is the first document in it that says warmup can be
  dropped outright rather than shortened or reshaped. That disagreement is
  real and unadjudicated, and the scales do not overlap.
title: 'Bound the learning rate by the ratio of the update''s spectral norm to the weight''s, and drop warmup'
version: 1
tags:
- training-optimization
- model-stability
date: '2026-09-22'
source:
- LIT-521
introduced_by:
- LIT-521
explained_by:
- THEORY-062
implementations: []
summary: >-
  Qi et al. (2025), [LIT-521](../literature.d/LIT-521.md) — if
  `α_t > τ·σ₁(W_{t−1})/σ₁(∇W_t)`, truncate the step to that value; otherwise
  use the schedule. Weyl's inequality makes this a direct cap on how fast a
  weight's largest singular value can grow. ViT-B, ViT-L, GPT-S, Swin-S and
  Swin-B all train **without any warmup** and match or beat warmed-up AdamW.
---
<!-- inactive-ok-file: THEORY-062 — Proposed, filed in this same
     contribution; this practice declares `explained_by:` on it and the
     sentence citing it says the account is one group's correction of
     another's. -->

<!-- inactive-ok-file: SOTA-319 — Proposed, named as one of three
     alternative remedies this paper does not compare against. -->

# SOTA-320: Bound the learning rate by the ratio of the update's spectral norm to the weight's, and drop warmup

## Source

Qi, He, Ye, Li, Zi, Dai, Zou and Xiao (2025),
[LIT-521](../literature.d/LIT-521.md) — read as [NOTE-266](../notes.d/NOTE-266.md). ICLR 2025.

## Do this

At each step, after computing the update `∇W_t` that the optimizer would
apply:

    if α_t > τ · σ₁(W_{t−1}) / σ₁(∇W_t):
        α_t ← τ · σ₁(W_{t−1}) / σ₁(∇W_t)

Take both spectral norms from power iteration capped at **3 iterations**; the
source reports 2 as sufficient. Then run a plain cosine decay from the maximum
learning rate, with **no warmup at all**.

**Why this is the right quantity.** Weyl's inequality gives
`σ₁(W_{t−1} + ∇W_t) ≤ σ₁(W_{t−1}) + σ₁(∇W_t)`, so the ratio is exactly the
handle on how much a single step can inflate the largest singular value. `τ`
is the budget: the step may grow `σ₁` by at most a `τ` fraction of what it
already is.

## What it buys

| | ViT-B 86M | ViT-L 307M | GPT-S 125M | Swin-S 50M | Swin-B 88M |
|---|---|---|---|---|---|
| AdamW, with warmup | 80.22 | 81.65 | 2.848 | 83.02 | 83.48 |
| this, no warmup | **80.58** | **81.82** | **2.840** | **83.14** | 83.44 |

The warmups removed are 60 epochs for ViT, 20 for Swin and 2000 steps for
GPT-S. Four of five configurations improve slightly; Swin-B is 0.04 worse.
Without the cap, the same models trained without warmup crash.

## Why `Proposed`

**It contradicts two `Active` practices in this record and the scales do not
meet.** [SOTA-008](SOTA-008.md) and [SOTA-100](SOTA-100.md) both say to use warmup, the second
proportionally to model size. This says a spectral cap makes it unnecessary —
demonstrated at 50M to 307M, which is below where those practices were
established and far below where warmup is expensive to get wrong. Neither side
has tested the other's regime.

**One group, no comparison against the alternatives.** The baseline is AdamW
with warmup. The three other remedies for the same underlying failure —
[SOTA-192](SOTA-192.md), [SOTA-131](SOTA-131.md), [SOTA-319](SOTA-319.md) — do not
appear, so "this works" is established and "this is what to reach for" is not.

**`τ` replaces the hyperparameter it removes.** The paper ablates four values
per architecture and the curves are not flat. Trading a warmup length for a
threshold is a real trade, not a free removal, and the source does not claim
otherwise.

## Conditions

**Two power iterations per matrix per step is not free**, though it is on
parameters rather than activations. The source does not report the wall-clock
overhead separately.

**It caps the step, so it interacts with the schedule.** The rule overrides
the scheduled learning rate whenever the ratio test fires, which is mostly
early. Read it as an automatic warmup derived from the weights rather than as
no warmup at all — the paper's framing is "without warmup" and the mechanism
is closer to "warmup computed rather than guessed".

**Demonstrated on ViT, Swin and GPT-2-small.** Nothing on a modern
decoder-only model at scale, and nothing with a different optimizer.

**The account it comes with is one group's correction of another's.**
[THEORY-062](../theory.d/THEORY-062.md) holds that spectral energy concentration, not
low entropy, is what crashes a run. If that is wrong the practice may still
work, since capping `σ₁` growth suppresses both candidate failure modes.

## Known implementations

None beyond the authors' own runs.
