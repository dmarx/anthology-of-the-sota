---
number: 259
status: Proposed
formerly:
- SOTA-tmp1t2ao
promote_when: >-
  A second group reporting that rescaling `beta_2` to hold the token half-life
  fixed removes a small-batch deficit, at any scale; or a training framework
  adopting the half-life as the exposed hyperparameter. What would not move
  it: a paper that tunes `beta_2` per batch size and reports the tuned values,
  which is consistent with the rule and does not test it.
consensus: unreplicated
consensus_note: >-
  One group. The mechanism is isolated cleanly — the rule reproduces and then
  removes a previously published small-batch deficit — and the authors say
  they do not know why a fixed token half-life transfers across model scales.
title: 'Hold Adam''s second-moment half-life fixed in tokens when the batch size changes, not beta_2'
version: 1
tags:
- training-optimization
date: '2026-09-20'
source:
- LIT-444
introduced_by:
- LIT-444
implementations: []
summary: >-
  Marek et al. (2025), [LIT-444](../literature.d/LIT-444.md) — `beta_2` is a decay per optimizer
  step, and a step is not a fixed amount of data. Changing batch size from
  `B` to `B'` while holding `beta_2` fixed changes the second moment's
  averaging window in tokens by the same factor. Hold the half-life fixed
  instead: `beta_2' = beta_2^(B'/B)`. `beta_1`'s default is fine.
---

# SOTA-259: Hold Adam's second-moment half-life fixed in tokens when the batch size changes, not beta_2
<!-- inactive-ok-file: SOTA-260 — Proposed, and filed in this same contribution as the practice this one is the safety condition for -->
<!-- inactive-ok-file: SOTA-261 — Proposed, and filed in this same contribution as the same move on a different hyperparameter -->

## Source

Marek et al. (2025), [LIT-444](../literature.d/LIT-444.md) — [ARXIV-2507.07101](https://arxiv.org/abs/2507.07101).

## The rule

Express the decay as a half-life in **tokens**:

    t_half = B · ln(2) / ln(1/beta)

Changing the batch size from `B` to `B'`, hold `t_2` fixed:

    beta_2' = beta_2^(B'/B)

Leave `beta_1` alone — its usual default works across batch sizes. It is
specifically the second moment that has to move.

## Why the default breaks

`beta_2` is a rate per optimizer step, and an optimizer step is not a fixed
quantity of data. Shrinking the batch by 512× while holding `beta_2 = 0.95`
shortens the window over which the second moment — the variance estimate the
update is divided by — is computed, by the same factor. The estimate is then
made from far too little data and the updates become erratic.

**This is the whole of "small batches are unstable".** The paper reproduces a
previously published result showing small batches underperforming with fixed
`beta_2`, applies the rule, and the deficit disappears with no other tuning.

## Why it is worth filing separately from the batch-size advice

Because it is true independently of whether you take [SOTA-260](SOTA-260.md)'s advice
about *which* batch size to use. Anyone who changes batch size for any reason
— a new cluster, a memory constraint, a fine-tuning run at a different scale —
is silently changing the averaging window unless they apply it. That includes
every transfer of a recipe from a paper to a different machine.

And it is the safety condition on the other practice: small batches without
this rule are the instability, not a demonstration of it.

## A constant with no unit attached

The general form of the finding is worth more than the rule. `beta_2 = 0.95`
is a number the field copies with an implicit denominator — a step — that
varies between every two runs that compare it. Naming the denominator makes
the constant transferable.

[SOTA-261](SOTA-261.md) is the same move on a different hyperparameter: weight decay
only means something against a learning rate and a step count, and the AdamW
timescale is what naming that denominator produces. Two papers, two
hyperparameters, one diagnosis — the numbers everyone copies are ratios whose
denominators were left out of the recipe.

## Conditions, and why this is `Proposed`

One group. The sweeps isolating the mechanism are at 30M parameters; the
scale checks are 124M and one 1.3B run.

**The authors say they do not know why it transfers across model scales.**
That is honest and it is a real limitation: the rule is an empirical
regularity with a plausible story, not a derivation, and a regularity of this
shape usually has an account waiting.

Untested against a batch-size *schedule*, which the authors name as an open
question — and the record recommends exactly such a ramp at [SOTA-093](SOTA-093.md), so
that gap is directly load-bearing here.

The square-root learning-rate rule is separately reported to overshoot badly
across wide batch ratios (32× prescribed against about 3× measured, from 1 to
1024), which is worth knowing alongside this but is not part of this
recommendation.

## Known implementations

- None. No framework in the record exposes a token half-life; they all expose
  `beta_2`.
