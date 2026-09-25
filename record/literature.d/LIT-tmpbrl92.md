---
status: Active
title: 'Analysis of dropout learning regarded as ensemble learning'
version: 1
tags:
- model-stability
date: '2026-09-25'
published: '2017-06-20'
arxiv: '1706.06859'
first_author: 'Hara'
keywords:
- 'dropout'
- 'ensemble-learning'
- 'soft-committee-machine'
- 'teacher-student'
- 'on-line-learning'
- 'l2-regularization'
extends:
- LIT-394
summary: >-
  Hara, Saitoh and Shouno (2017), ARXIV-1706.06859. In a teacher-student
  soft-committee machine (erf units, N = 1000, 100 student units, one fixed
  set of N inputs reused), dropout at p = 0.5 reaches lower test MSE than an
  ensemble of two independently trained 50-unit halves. Its residual error is
  about that of SGD with a tuned L2 penalty. The title says analysis, but no
  analytic result is derived. Everything is simulation curves averaged over
  10 trials, with no numbers or spread reported.
---

# LIT-tmpbrl92: Analysis of dropout learning regarded as ensemble learning

Hara, Saitoh and Shouno (2017) — ARXIV-1706.06859

## Key takeaways

**The framing.** At test time a dropout network sums units that were trained
on this step and units that were not, scaled by `p`. At `p = 0.5` the paper
reads that as an ensemble of two half-networks. The difference from ordinary
ensemble learning is that the split into halves is redrawn at every step.

**The setting.** A teacher-student soft-committee machine: hidden-to-output
weights fixed at +1, `g(x) = erf(x/√2)`, i.i.d. zero-mean unit-variance inputs,
and the thermodynamic limit assumed for the setup. The teacher has 2 hidden
units and the student 100. Overfitting is induced by reusing a fixed set of
`N` inputs, since on-line learning with fresh inputs cannot overfit.

**The two comparisons (Figs. 5 and 6, 10 trials each).**
- Dropout (one 100-unit student, `p = 0.5`) reaches a lower test MSE than an
  ensemble of two 50-unit students trained independently and averaged. The
  architectures are matched. The paper concludes that redrawing the split
  every step beats fixing it.
- Dropout's residual error is "almost the same" as SGD with L2, from which the
  paper concludes that "the regularization effort of dropout learning is the
  same as the L2 regularization".

## Traps

- **No analysis in the analytic sense.** The teacher-student setup is the one
  statistical mechanics uses to derive order-parameter equations. None are
  derived. The results are learning curves, and the key comparison sets
  Fig. 5(a) against Fig. 5(b), which are separate panels.
- **"Dropout learning has no tuning parameter" is false.** `p` is one, and only
  `p = 0.5` is run.
- **The L2 update as printed subtracts `α‖J‖²`, a scalar, from a vector.**
  Presumably `αJ` was meant. `α` is not reported.
- **The "same as L2" result is not evidence against THEORY-015.** The inputs
  here are i.i.d. with unit variance. In that setting the data-scaled
  penalties THEORY-015 collects (inputs scaled by magnitude or standard
  deviation) reduce to something close to plain L2. So this setup could not
  have told the two apart.

## Standing in the anthology

Filed so that the 09/17 dropout cluster is complete. The result is weak. It
is one toy model with qualitative curves and no analytic content, and it
sources nothing.

It bears on THEORY-016, and the direction matters. THEORY-016 warns against
reading "dropout is an ensemble" as the reason dropout helps. This paper's
one clear finding points the same way: dropout beats the ensemble it is
supposed to be. So the ensemble reading does not explain its advantage, which
comes from the redrawn split. The paper does not identify a mechanism for
that. It extends Hinton et al.'s 2012 proposal (LIT-394), which it cites as
the method.
