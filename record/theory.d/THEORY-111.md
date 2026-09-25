---
number: 111
status: Superseded
formerly:
- THEORY-tmpwhyfx
superseded_by: SOTA-428
status_note: >-
  Retired as redundant rather than wrong. The claim — that a hyperparameter's
  apparent importance can belong to its interaction with a frozen averaging
  length — is already stated in SOTA-428's Conditions, in the same words the
  source uses: "Much of what looks like learning-rate sensitivity is EMA
  mismatch", with the same 72%-against-10% bracket behind it. A theory document
  restating a practice's own condition from the same single measurement adds a
  citation target and no claim. `superseded_by:` points at the practice because
  that is where the content lives, not because a practice supersedes a theory.
promote_when: >-
  The same 2×2 — one hyperparameter swept against a frozen versus a swept
  averaging length — run outside diffusion, on a metric that is not FID. The
  record's own averaging practices point at the settings: a ResNet classification
  sweep (SOTA-408's regime), a fine-tuning sweep (SOTA-409's), or a language-model
  pretraining run with checkpoints kept (SOTA-415's). The retroactive
  reconstruction in SOTA-432 means this can be measured on runs that already
  happened, so the experiment costs storage and evaluation rather than training. A
  negative result — a knob whose sensitivity is unchanged by sweeping the average
  — would bound the claim usefully rather than refute it.
title: 'A hyperparameter can look important because it is entangled with an averaging length you froze, so sensitivity attributed to one knob may belong to the pair'
version: 1
tags:
- analysis-and-evaluation
- training-optimization
date: '2026-09-25'
source:
- LIT-720
summary: >-
  Karras et al. (2023), [LIT-720](../literature.d/LIT-720.md), measured on EDM2-S / ImageNet-512: with the
  weight-averaging length pinned at 13%, varying the learning-rate decay across
  `t_ref ∈ [30k, 160k]` moves FID **by up to 72%**; sweeping the averaging length
  post hoc puts the whole bracket **within 10% of the optimum**. The decay's
  apparent importance was mostly a fact about the pair. Generalising: a
  sensitivity curve measured with a second knob frozen at a guess attributes the
  interaction to the knob being swept, and there is no way to tell from the curve.
---

<!-- inactive-ok-file: SOTA-415, SOTA-408 — Proposed, and named as the settings where this account's promote_when could be tested plus, for SOTA-415, a justification this account bears on. Neither is cited as support for the claim. -->

<!-- inactive-ok-file: SOTA-428, SOTA-432, LIT-720 — this account is Superseded as redundant: its claim is a SOTA-428 Conditions bullet. It cites SOTA-428 as its replacement and the other two retired documents of the same duplicate unit. -->

# THEORY-111: A hyperparameter can look important because it is entangled with an averaging length you froze, so sensitivity attributed to one knob may belong to the pair

## Source

Karras, Aittala, Lehtinen, Hellsten, Aila and Laine (2023), [LIT-720](../literature.d/LIT-720.md),
Figure 12 — reported as an aside about learning rates, not as a claim about
methodology.

## The account

A sensitivity sweep varies one hyperparameter and holds the rest fixed. That is
the right experiment when the rest are genuinely independent, and it silently
attributes any *interaction* to the knob being moved. The averaging length is an
unusually bad thing to hold fixed, for a structural reason: it is chosen before
the run, it is rarely reported, and its own optimum depends on the very quantities
being swept — so the fixed value is right for at most one cell of the sweep.

**The measurement.** EDM2-S on ImageNet-512, learning-rate decay `t_ref` against
FID:

| averaging length | FID across `t_ref ∈ [30k, 160k]` |
| --- | --- |
| fixed at 13% | up to **72%** worse than the optimum |
| swept post hoc | all **within 10%** of the optimum |

A sweet spot still exists — `t_ref = 70k` — so the decay is not *nothing*. But a
reader of the first row would conclude the learning-rate decay is a
high-sensitivity hyperparameter worth careful tuning, and a reader of the second
would conclude it is worth getting inside a factor of five. Most of what the first
row measures is the mismatch between a frozen average and the run it was frozen
for.

**Why the averaging length in particular.** [LIT-720](../literature.d/LIT-720.md) measures three things
that make a single fixed value indefensible: the optimum "differs considerably
between the configurations" of one model family; it *narrows* as the architecture
improves, so a stale value is wrong by more; and it "slowly shifts towards
relatively longer EMA as the training progresses", even though the length is
already defined relative to run length. A knob whose optimum moves with
architecture, training duration and the other hyperparameters is not a constant
anybody can set once.

## What follows if it is right

**Published sensitivity curves are a lower bound on how forgiving a
hyperparameter is, not an estimate of it.** Every such curve that was produced
with an averaging scheme fixed by convention — which is to say, most of them —
overstates the swept knob's importance by whatever the interaction contributes.

The direction is *usually* but not always knowable, and the difference is worth
stating. The swept curve is a pointwise lower bound on the frozen one, since at
each setting it takes the best available averaging length. That alone does not
bound the *range*: a lower envelope can in principle dip further at one point and
look more sensitive. What makes the bias one-directional in practice is how the
frozen value gets chosen — tuned at the configuration the authors settled on,
which is near the swept curve's own minimum. When that holds, the two curves share
a minimum and the frozen one has the larger spread. In this paper it holds: 13% is
the optimum at `t_ref = 70k`, the best setting.

**It is cheap to check retroactively.** Because the reconstruction in
[SOTA-432](../practices.d/SOTA-432.md) works from stored snapshots, the 2×2 can be run on training runs
that already finished, at the cost of storage and evaluation rather than compute.
That is unusual for a methodological claim and is what the `promote_when` asks
for.

## What this does not say

**Not that the learning-rate decay does not matter.** The sweet spot is real and
the paper reports it.

**Not a general claim about all frozen hyperparameters.** The argument turns on
specific properties of the averaging length — chosen pre-run, unreported, with an
optimum that tracks everything else. A knob without those properties may be
perfectly safe to hold fixed, and this account says nothing about which ones
those are.

**Not the same as the seed-variance argument.** [SOTA-307](../practices.d/SOTA-307.md) is about the *noise* in
a reported FID: retraining moves it more than resampling does, so a small gap is
inconclusive. This is about *bias* in a reported sensitivity: the curve is the
wrong shape, not noisy. A perfectly estimated FID at every point would leave this
intact. [THEORY-095](THEORY-095.md) is a third and separate thing — the estimator's own bias.

**Not evidence that uniform averaging is wrong.** [SOTA-415](../practices.d/SOTA-415.md) recommends a uniform
average partly because it has no hyperparameter to tune, and that is a real
benefit under a real constraint. What this account says is that the constraint is
avoidable, not that the choice made under it was mistaken.
