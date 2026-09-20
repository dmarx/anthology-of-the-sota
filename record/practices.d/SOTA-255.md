---
number: 255
status: Proposed
formerly:
- SOTA-tmp9rfqy
promote_when: >-
  A second group sweeping weight decay under a fixed corpus at
  above-Chinchilla parameter-to-token ratios and reporting where the optimum
  landed; or a pretraining report that says it raised weight decay for this
  reason. What would not move it: a paper reporting a better loss with a
  different weight decay at a Chinchilla-optimal ratio, which is the regime
  this practice says the inherited value was chosen for.
consensus: unreplicated
consensus_note: >-
  One group, one corpus, one set of parameter counts. The multiple is
  reported rather than derived, so a practitioner still has to sweep — but
  the direction is the finding and it is unambiguous.
title: 'Tune weight decay upward when pretraining over a repeated corpus, rather than inheriting the customary value'
version: 1
tags:
- model-stability
- training-optimization
date: '2026-09-19'
source:
- LIT-441
introduced_by:
- LIT-441
implementations: []
summary: >-
  Kim et al. (2025), [LIT-441](../literature.d/LIT-441.md) — with the corpus fixed and parameters
  past Chinchilla-optimal, the weight decay of 0.1 everyone inherits from
  GPT-3 is far too small: loss turns upward as parameters or epochs are
  added. Tuned jointly with learning rate and epoch count, the optimum is
  roughly 30x larger, and loss becomes monotone in parameter count with a
  steeper exponent than Chinchilla's.
---

# SOTA-255: Tune weight decay upward when pretraining over a repeated corpus, rather than inheriting the customary value
<!-- inactive-ok-file: SOTA-173 — Proposed, and named as one of the positions this practice says was measured at one setting of weight decay -->

## Source

Kim et al. (2025), [LIT-441](../literature.d/LIT-441.md) — [ARXIV-2509.14786](https://arxiv.org/abs/2509.14786).

## What goes wrong without it

Fix a corpus — 200M tokens, in the study — and spend compute by adding epochs
and parameters. Loss falls, then rises. Tuning the epoch count separately at
each parameter count does not prevent it. The recipe is not saturating; it is
overfitting, and past a point every additional parameter makes the model
worse.

That failure is what bounds the data-constrained recipes the record already
holds. It is also, on this evidence, an artifact of a hyperparameter nobody
tunes.

## The finding is the magnitude

The weight decay in general use is **0.1**, inherited from GPT-3 and carried
forward through recipe after recipe. Searched jointly with learning rate and
epoch count by coordinate descent at each parameter count, the optimum for
the most over-parameterized models is **roughly 30x that**.

With it, two things change:

- Loss becomes **monotone in parameter count** — the turn upward disappears,
  so adding parameters is once again always worth doing if you can afford it.
- The resulting power law has parameter exponent **≈0.23** where Chinchilla's
  is ≈0.34 — meaning the returns to model size are *larger*, not smaller,
  once the data is being used properly.

## Why this is the cheapest thing to try first

The record's three positions on repetition — [SOTA-171](SOTA-171.md)'s four epochs,
[SOTA-173](SOTA-173.md)'s objective augmentation, and the diffusion route — all answer
"how far may a corpus be repeated" with a number or an intervention. This
answers it with a hyperparameter, and the intervention costs one sweep rather
than a change of objective or of architecture.

<!-- inactive-ok-block: SOTA-124 — Proposed, and named because it is one of
     the three positions this variable is uncontrolled in -->
It also says something uncomfortable about the dispute itself: [SOTA-124](SOTA-124.md),
[SOTA-171](SOTA-171.md) and [SOTA-173](SOTA-173.md) between them report one setting of weight decay, and
on this evidence the answer moves with it. None of those measurements is
wrong; they may all be measurements of the under-regularized case.

## Not a claim about AdamW

[SOTA-001](SOTA-001.md) and the decoupled-decay line are about the *mechanism* — how weight
decay should be applied so that it does not interact with the adaptive step.
This is about the *value*, in a regime the customary value was never chosen
for. Nothing here disputes decoupling; it says the constant that decoupling
made meaningful has been copied rather than picked.

## Conditions, and why this is `Proposed`

One group, one corpus of 200M tokens, models up to 1.4B. Frontier pretraining
is several orders of magnitude away on both axes.

**"30x" is a measurement, not a rule.** The paper gives no way to predict the
optimum from the parameter-to-token ratio, so the practice is really "sweep
it, and sweep upward" — the direction is the reusable part. A practitioner
who sets 3.0 because it is 30 times 0.1 has taken a number out of one
experiment.

The regime matters. This is about parameter-to-token ratios *above*
Chinchilla with repeated data. At or below the compute-optimal ratio the
inherited value is not shown to be wrong, and the failure this fixes does not
arise.

## Known implementations

- None in the record. Every pretraining report the record holds that states a
  weight decay states something near 0.1.
