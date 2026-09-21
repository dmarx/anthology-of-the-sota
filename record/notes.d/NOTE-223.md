---
number: 223
status: Read
formerly:
- NOTE-tmpxy07e
paper: LIT-474
title: 'The Coverage Principle'
version: 1
date: '2026-09-21'
summary: >-
  Reading it: the strongest thing here is not the theorem but the Bernoulli
  example, which shows KL going to infinity while coverage stays fine on a
  two-outcome model. That is the whole argument in four lines, and it explains
  why a metric everybody watches can be anti-correlated with what they want.
---

# NOTE-223: The Coverage Principle

## Contribution

A name and a theory for the gap between pre-training loss and post-training
success. The gap was already documented — several cited works report that a
better next-token predictor does not give a better post-trained model — and
this supplies the quantity that does predict it, proves the prediction is
tight in both directions for Best-of-N, and then shows that next-token
prediction optimizes that quantity anyway, faster than it optimizes the loss
being displayed.

What is true afterwards that was not before: "cross-entropy is a poor proxy
for downstream performance" stops being an empirical irritation and becomes a
statement about which term in a generalization bound you are paying for.

## Key insight

**Missing mass is the whole story, and the Bernoulli case shows it in four
lines.** Two outcomes, `π*(1) = ε`. With constant probability a small dataset
contains no `1`, so the MLE assigns it zero and expected KL is *infinite*.
Coverage, meanwhile, is fine: either the empirical frequency concentrates, or
the missing mass is small enough to write off.

KL charges `log(1/π̂)` for every response a well-generalizing learner happens
not to cover, and that charge is unbounded. Coverage charges at most the mass
itself. Everything else in the paper — the sequence-length dependence, the
faster tail convergence, the SGD failure — is that asymmetry at larger scale.

## Assumptions

- **Realizability** (`π* ∈ Π`) for the main theorem; misspecification is
  handled separately by convexity or by the tournaments.
- **Prompt/response split**, with the same prompt distribution at pre- and
  post-training. The authors call the first a simplification "closer in spirit
  to supervised fine-tuning" and the second straightforward to relax at the
  cost of a distribution-shift coefficient.
- **The pre-training distribution covers the downstream tasks.** Presupposed,
  and it is doing real work: the principle says coverage is *inherited*, so if
  the corpus has not got it, nothing here provides it.
- **Autoregressive linear models, single-pass SGD, one step per sequence** for
  everything in §5.
- **Best-of-N as the stand-in for post-training**, justified by cited evidence
  that BoN predicts post-RL performance rather than by anything proved here.

## Key results

- Coverage profile is **necessary and sufficient** for Best-of-N success.
- KL-to-coverage bound gives a test-time scaling law that is **exponential in
  sequence length**, which is the wrong shape — motivating the rest.
- Lower bound: for autoregressive linear models, sequence-level KL scales
  linearly in `H` for any proper estimator on some data distribution.
- Empirically (graph reasoning): KL at convergence is linear in `H`; coverage
  at convergence shows **no dependence on `H`**.
- Fig. 1: KL improves monotonically through training while **coverage can
  degrade**, and KL is the worse predictor of BoN performance at large `N`.
- Main theorem: coverage bound splits into a fine-grained term scaled by `1/N`
  with no `H` or density-ratio dependence, and a coarse-grained missing-mass
  term. Both tight.
- SGD on autoregressive linear models has `H`-dependent coverage, with a
  matching lower bound; **globally normalized SGD removes it**.
- Tournament selection attains near-best-in-class coverage without
  realizability.

## Claims

**Proved:** the necessity/sufficiency for BoN, the KL lower bound, the
coverage generalization bound and its tightness, the SGD lower bound and the
normalized-SGD upper bound, the tournament guarantees.

**Speculated, and labelled:** that Adam enjoys the same benefit. The text says
"somewhat speculatively", and notes that Adam normalizes per-coordinate rather
than globally — a difference the authors themselves call important for deep
models. This is the sentence most likely to be cited as though it were a
result.

**Assumed from elsewhere:** that BoN predicts post-RL performance. The bridge
from this paper to reinforcement learning rests entirely on that citation, and
the paper says the minimal conditions for RL are not known.

## Method

Theory, with a graph-reasoning task used to illustrate two of the theorems.
There is no empirical study here and the paper does not claim one.

## Concepts

*Coverage profile* `C_N`, indexed by the number of Best-of-N attempts;
*fine-grained* vs *coarse-grained* terms in the bound; *missing mass*;
*answer-level* versus *sequence-level* coverage; tournament estimators.

## Connections

- [SOTA-210](../practices.d/SOTA-210.md) — report pass@k as well as pass@1 — is the empirical
  practice this is the theory for. pass@k is an estimator of coverage at
  `N = k`, and "RL raises pass@1 and lowers pass@k" is, in this language, RL
  trading coverage for mode. Two groups found that; this explains what they
  found.
- The record's existing concern that an aggregate loss curve hides structure
  gets a second, sharper instance: here the curve is not hiding a subgroup,
  it is measuring a different quantity that happens to correlate until it
  does not.
- [SOTA-281](../practices.d/SOTA-281.md) samples several reasoning paths and takes the majority
  answer. That is coverage being spent, and answer-level coverage is the
  version of the quantity it needs — the weaker one this paper flags as the
  right object for reasoning tasks and does not analyse.

## Bearing on the record

One practice, `Proposed`: select the checkpoint you post-train from by
coverage rather than by validation cross-entropy. One account, `Proposed`.

The thing to resist is treating this as licence to say "cross-entropy does not
matter". It bounds coverage, it is estimable, and coverage is not. The claim
is narrower and more useful: cross-entropy's sensitivity to missing mass grows
with sequence length, so the gap between it and what you want widens exactly
where modern models live.

## Limitations

**The quantity it recommends is not observable.** A footnote says so. Coverage
can be estimated on a labelled set, which is what the tournaments do, and that
is a different and more expensive thing than reading a validation loss.

**The formulation is nearer SFT than pre-training**, by the authors' own first
bullet: real corpora are variable-length and unsegmented.

**The optimizer results are for linear models.** The interesting claim —
normalization buys horizon independence — is proved where the loss is convex
in the parameterization, which is the case a transformer is not.

**The empirical content is one synthetic task.** Figures 1 and 2 are
demonstrations, and a reader who wants to know whether coverage predicts
downstream success on a real model will not find it here.

**Answer-level coverage is what reasoning needs and is not what is analysed.**
§7.1 names this and moves on.

## Open questions

- Does the checkpoint-selection tournament beat cross-entropy validation on a
  real pre-training run? That is the one experiment that would turn this from
  an account into a practice, and it is not here.
- Is the Adam speculation true? Per-coordinate versus global normalization is
  exactly the difference the authors flag, and settling it would connect this
  to [SOTA-001](../practices.d/SOTA-001.md) rather than leaving a suggestive remark.
- What are the minimal conditions for RL, as opposed to Best-of-N? The paper
  asks this directly. Everything the record does with post-training assumes
  the answer is "roughly the same", and nobody has shown it.
