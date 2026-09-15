---
status: Proposed
promote_when: >-
  A third group reporting the comparison at matched evaluation cost on a
  reasoning task, or either estimator adopted in a released ES post-training
  implementation. What would not satisfy this: a result on a supervised
  non-reasoning benchmark, where the paired coupling the antithetic estimator
  depends on is not broken and the finding is expected to reverse.
consensus: emerging
consensus_note: >-
  Two groups with no authors in common, arriving from an empirical variance
  diagnostic (LIT-tmp81or2) and from an estimator derivation (LIT-tmpcjyw1),
  reach the same instruction within a fortnight. Neither has been replied to,
  and the practice they argue against is what the reference implementation of
  LIT-tmp4zb0l ships.
title: 'Spend one fitness evaluation per evolution-strategies direction, not an antithetic pair'
version: 1
tags:
- training-optimization
date: '2026-09-15'
source:
# Two independent arguments for one instruction. LIT-tmpcjyw1 is primary: it
# derives an estimator that provably preserves the expected field at half the
# cost, which is a stronger claim than the observation that the second
# evaluation does not pay.
- LIT-tmpcjyw1
- LIT-tmp81or2
introduced_by:
- LIT-tmpcjyw1
implementations: []
summary: >-
  Kaya and Hashemi (2026), [LIT-tmpcjyw1](../literature.d/LIT-tmpcjyw1.md), and Ba et al. (2026), [LIT-tmp81or2](../literature.d/LIT-tmp81or2.md) —
  the antithetic pair's variance reduction depends on both evaluations sharing
  randomness, which autoregressive regeneration breaks. Replace the pair with
  a leave-one-out baseline computed from the population mean the score
  centering already needs: same expected update, one evaluation per direction,
  twice as many directions per budget, and half the estimator MSE in
  transformer blocks.
---

# SOTA-tmph4wug: Spend one fitness evaluation per evolution-strategies direction, not an antithetic pair

## Source

Kaya and Hashemi (2026), [LIT-tmpcjyw1](../literature.d/LIT-tmpcjyw1.md) — [ARXIV-2609.10980](https://arxiv.org/abs/2609.10980); Ba et al.
(2026), [LIT-tmp81or2](../literature.d/LIT-tmp81or2.md) — [ARXIV-2608.27351](https://arxiv.org/abs/2608.27351).

## What the antithetic pair was for, and why it stops paying here

Standard practice evaluates both `θ + σE` and `θ − σE` for each direction and
subtracts. The subtraction cancels whatever the two evaluations share — the
reward offset, and every even-order term of the local expansion — which is a
real variance reduction, and it is why two-point zeroth-order estimators are
the default on supervised tasks.

**The cancellation depends on the pair sharing randomness, and reasoning tasks
break that.** A supervised objective re-scores fixed data, so the paired
evaluations differ only in the perturbation. A reasoning objective
*regenerates* an autoregressive response, and an early-token divergence sends
the two rollouts down different paths. [LIT-tmp81or2](../literature.d/LIT-tmp81or2.md) measures exactly this:
raw variance reduction on SST-2, but not reliably on regenerated GSM8K
rewards, and no training-reward or held-out advantage from the second
evaluation.

## The replacement, which is cheaper than it sounds

[LIT-tmpcjyw1](../literature.d/LIT-tmpcjyw1.md)'s LOO-ROLL removes the population-level reward offset with a
**leave-one-out baseline** instead of an antithetic partner. The point is that
this baseline is free: it comes from the population mean that ES score
centering already computes. No extra fitness evaluations, no extra
model-sized state, no extra communication rounds, and the expected update
field is unchanged before standardization.

So the same evaluation budget funds `N` independent directions where it
previously funded `N/2` antithetic ones. At equal evaluation cost that
**halves estimator MSE in transformer blocks**.

Measured end to end across ten matched-wall-time post-training settings on
models up to 8B: seven improvements in individual paired tests, three
unresolved, **no significant loss**, five gains surviving Holm correction.
GSM8K accuracy rises at both 0.6B and 8B.

## Conditions, and one place this reverses

**Reasoning and other regenerating objectives.** The whole argument rests on
the paired coupling being weak. On a supervised task that re-scores fixed
data, the coupling holds, the antithetic estimator does its job, and
[LIT-tmp81or2](../literature.d/LIT-tmp81or2.md) measures the variance reduction working. Do not carry this
across.

**The two sources argue for slightly different things.** Ba et al. use plain
one-point estimation and find the second evaluation buys nothing. Kaya and
Hashemi derive a leave-one-out baseline that provably preserves the expected
field. The shared instruction is *don't spend two evaluations on one
direction*; the leave-one-out construction is the better-supported way to act
on it, which is why it is the primary source.

**It is a change to the estimator, not to the search.** Population size,
perturbation scale and reward normalization are separate decisions, and
[LIT-tmp81or2](../literature.d/LIT-tmp81or2.md) reports that the perturbation scale has a two-sided failure
mode — too small overfits the sampled rewards into a local optimum, too large
destabilizes training.

## Where this sits

<!-- inactive-ok-block: SOTA-154 is Active; named as the practice this one is
     an implementation decision inside -->
This is an implementation decision inside [SOTA-154](SOTA-154.md) rather than an
alternative to it, and inside [LIT-tmp4zb0l](../literature.d/LIT-tmp4zb0l.md)'s low-rank machinery in
particular — whose reference implementation ships the antithetic pairs this
practice argues against. It is filed separately because it is a claim about
the estimator, and someone running any ES variant faces it.

## Known implementations

- None released. [LIT-tmpcjyw1](../literature.d/LIT-tmpcjyw1.md)'s LOO-ROLL is implemented on top of
  [LIT-tmp4zb0l](../literature.d/LIT-tmp4zb0l.md)'s codebase, retaining seed-based perturbation
  reconstruction, layerwise updates and the existing weight synchronization.
