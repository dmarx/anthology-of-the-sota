---
number: 43
status: Proposed
formerly:
- THEORY-tmp16mrv
promote_when: >-
  The coverage/cross-entropy divergence measured on a real pre-training run —
  checkpoints from a transformer on natural text, coverage estimated on a
  labelled downstream set, and cross-entropy shown to select a worse one. A
  further demonstration on a synthetic task, or another report that
  pre-training loss fails to predict downstream performance, is not it: the
  failure is already documented and this account's content is the mechanism,
  not the fact.
title: 'Cross-entropy pays an unbounded price for mass a learner never had, and that price grows with sequence length — which is why it drifts from what post-training needs'
version: 1
tags:
- analysis-and-evaluation
- training-optimization
date: '2026-09-21'
source:
- LIT-474
explains:
- SOTA-284
summary: >-
  Chen et al. (2025), [LIT-474](../literature.d/LIT-474.md) — KL charges `log(1/π̂)` for
  every response a well-generalizing learner happens not to cover, and that
  charge is unbounded; the coverage profile charges at most the missing mass
  itself. Sequence-level KL therefore grows linearly in sequence length where
  coverage does not, and next-token prediction optimizes coverage faster than
  it optimizes the loss on the screen.
---

<!-- inactive-ok-file: SOTA-284 — Proposed, and the practice this account
     explains; naming it in the `explains` table is the relation, not a claim
     that either is settled -->

# THEORY-043: Cross-entropy pays an unbounded price for mass a learner never had, and that price grows with sequence length — which is why it drifts from what post-training needs

## Source

Chen, Huang, Golowich, Malladi, Block, Ash, Krishnamurthy and Foster (2025),
[LIT-474](../literature.d/LIT-474.md) — read as [NOTE-223](../notes.d/NOTE-223.md).

## What it explains

| practice | what it says to do | what this says it is |
|---|---|---|
| [SOTA-284](../practices.d/SOTA-284.md) | select the post-training checkpoint on coverage, not validation cross-entropy | two metrics that agree until missing mass and sequence length pull them apart, which is exactly where the interesting checkpoints are |
| [SOTA-210](../practices.d/SOTA-210.md) | report pass@k as well as pass@1 | pass@k is an estimator of the quantity that actually gates post-training, and pass@1 is not |

## The account

The cleanest statement is a two-outcome model. Let `π*(1) = ε` for small `ε`,
and fit by maximum likelihood on `n` samples. With constant probability the
dataset contains no `1` at all, the estimator assigns it zero, and expected KL
divergence is **infinite**.

Nothing has gone wrong with the learner. It saw no evidence of an event and
did not predict it. But KL's penalty for an under-assigned outcome is
`log(π*/π̂)`, which diverges as `π̂ → 0`, so a learner that is behaving
correctly is charged without bound.

The coverage profile — how much mass the model puts where the data
distribution puts it, weighted by how many Best-of-N draws you get — has no
such term. Either the empirical frequency concentrated, or the missing mass is
small enough to write off against the mass you did capture. The worst it can
charge is what is actually missing.

**That asymmetry scales.** Over a sequence of `H` tokens, the opportunities
for a well-generalizing model to miss some tail response multiply, so
sequence-level KL accumulates them: for autoregressive linear models, KL grows
*linearly in `H`* for any proper estimator on some data distribution, and the
same linear growth appears empirically. Coverage does not — at convergence it
shows no `H` dependence at all.

So the two metrics do not merely differ by a constant. They diverge in the
direction of longer sequences, which is the direction everything has been
moving.

**And next-token prediction optimizes the better one anyway.** The coverage
bound for the maximum-likelihood estimator splits into a fine-grained term
that reads the class's complexity at a small scale, scaled by `1/N` and
carrying no sequence-length or density-ratio dependence, and a coarse-grained
term that reads complexity at a very large scale and captures the missing
mass. Both are tight. The `1/N` scaling means coverage converges *faster* the
further into the tail you look.

That is the coverage principle: the objective is implicitly doing the right
thing, and the number on the screen is measuring something else — something
that inherits a penalty the objective's own generalization behaviour does not.

## Why `Proposed`

Not because the theorems are in doubt. They are proved, with matching lower
bounds for the parts that matter.

Because the distance between the theorems' setting and a language model is
large and the paper says so. The formulation splits data into prompts and
responses, which the authors call "closer in spirit to supervised
fine-tuning"; the main theorem assumes realizability; the optimizer results
are for autoregressive linear models where the loss is convex in the
parameterization; the empirical content is one synthetic graph-reasoning task.

A proof about a model class the record's practices are not about is an
account offered, not an account established — which is what `Proposed` means
here, and the promotion condition names the measurement that would change it.

## What this does not say

**It does not say cross-entropy is useless.** It upper-bounds coverage, it is
estimable, and coverage is not — a footnote in the source concedes that
neither KL nor coverage is directly observable. The claim is about *when* the
bound goes slack: with missing mass, and increasingly with sequence length.

**It does not prove anything about Adam.** The source proves that *globally*
normalized SGD removes the sequence-length dependence, and then says
"somewhat speculatively" that Adam-like updates may inherit the benefit —
noting that Adam normalizes per coordinate, a difference the authors
themselves call important for deep models. This is the sentence most likely to
be quoted as a result. It is not one, and [SOTA-001](../practices.d/SOTA-001.md) gains nothing from it.

**It does not establish anything about RL**, only about Best-of-N. The source
states plainly that the minimal conditions for RL are unknown, and the bridge
is a cited empirical finding that BoN predicts post-RL performance.

**And the version it analyses is the conservative one.** For reasoning tasks
the object that matters is *answer*-level coverage, which is bounded by the
sequence-level profile and can be strictly smaller. The account is stated
about a quantity that is pessimistic relative to what a reasoning
practitioner needs.
