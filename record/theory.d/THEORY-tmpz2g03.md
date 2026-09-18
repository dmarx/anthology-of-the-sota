---
status: Active
title: 'Influence functions on neural networks estimate the proximal Bregman response function, not leave-one-out retraining'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-17'
source:
- LIT-tmpyirk2
- LIT-tmpz6v6v
explains:
- SOTA-tmp8ornu
corrects:
- THEORY-tmp7738v
summary: >-
  Bae et al. (2022), [LIT-tmpyirk2](../literature.d/LIT-tmpyirk2.md) — the influence/retraining discrepancy
  decomposes into five terms, and the two that are genuinely approximation
  error are an order of magnitude smaller than the three that are not. What
  the estimate tracks closely is the effect of removing a point while holding
  predictions near the trained model's. So the method is not fragile; it was
  answering a different question.
---

# THEORY-tmpz2g03: Influence functions on neural networks estimate the proximal Bregman response function, not leave-one-out retraining

## Source

<!-- inactive-ok-block: THEORY-tmp7738v — Rejected, and named here as the
     account this one replaces; that is what the citation is for. -->
Bae, Ng, Lo, Ghassemi and Grosse (2022), [LIT-tmpyirk2](../literature.d/LIT-tmpyirk2.md). The account it replaces
is [THEORY-tmp7738v](THEORY-tmp7738v.md), published with the method in [LIT-tmpz6v6v](../literature.d/LIT-tmpz6v6v.md).

## What was actually shown

The experiment is a decomposition rather than a subtraction. Take the gap
between an influence estimate and leave-one-out retraining and insert the
approximations one at a time, measuring what each contributes:

1. **the warm-start gap** — retraining from the trained parameters is not
   retraining from scratch, and they are different counterfactuals
2. **the proximity gap** — an implicit regularizer pulling toward the trained
   solution
3. **the non-convergence gap** — the parameters are not a minimizer
4. **linearization error**
5. **solver error**

Terms 4 and 5 are the ones that are actually approximation error, and across
binary classification, regression, image reconstruction, image classification
and language modelling they are **at least an order of magnitude smaller** than
terms 1–3.

Terms 1–3 are precisely the difference between leave-one-out retraining and a
different object, the **proximal Bregman response function**: the effect of
removing a data point while keeping the model's predictions close to those of
the trained model. So the estimate's distance from the PBRF is only terms 4
and 5 — the small ones — and it tracks the PBRF closely while failing to track
retraining.

This could have come out the other way twice over. Terms 4–5 could have
dominated, in which case the method really would have been a bad
approximation; and the three gaps could have failed to assemble into a single
nameable object, in which case there would be no "different question", only
noise.

## What follows, including for a practice

The prevailing reading — influence functions are fragile on neural networks —
is wrong. They are accurate estimates of something other than what their name
and derivation suggest, and the PBRF is therefore a better standard to
evaluate them against than retraining is. [LIT-tmpmgsal](../literature.d/LIT-tmpmgsal.md) validates against the
PBRF for exactly this reason.

<!-- inactive-ok-block: SOTA-tmp8ornu — Proposed, and named here because this paragraph is
     about which practice the reinterpretation spares. -->
**And the use cases survive**, which the paper says in as many words: the PBRF
supports finding influential or mislabelled examples, and carrying out
data-poisoning analysis. That is why [SOTA-tmp8ornu](../practices.d/SOTA-tmp8ornu.md) is still a practice this
record makes. It needs an ordering over training points; it never needed the
counterfactual.

## The reading it invites and does not support

That the question has been settled. It has not — it has been *identified*.
Whether the PBRF is the quantity anyone actually wants to know about is
untouched here, and [LIT-tmpmgsal](../literature.d/LIT-tmpmgsal.md) explicitly declines to take it up as well,
while noting that a PBRF-targeted estimate should be expected to miss
genuinely nonlinear training phenomena such as circuit formation or
representational reorganisation.

So the honest position is narrower than "influence functions work": the
literature now validates against an object that has been named and not yet
argued for. That is a large improvement on validating against the wrong
object, and it is not the same as knowing the answer is useful.
