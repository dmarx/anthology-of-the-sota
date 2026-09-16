---
number: 12
status: Proposed
formerly:
- THEORY-tmpih985
promote_when: >-
  A steps-to-target curve for a layerwise-normalized optimizer drawn the way
  LIT-058 draws its curves — metaparameters tuned independently at every batch
  size — on at least one workload where a globally-conditioned optimizer's
  retuned curve is also drawn. If the layerwise curve holds perfect scaling
  further under equal tuning, this account is right. If the two retuned curves
  coincide and only the untuned gap differs, the mechanism is about a
  heuristic's robustness and not about where the scaling regime ends, and this
  document is wrong in the way that matters. A paper reporting only an untuned
  large-batch result, however large the batch, satisfies neither branch.
title: 'How far a batch-size scaling heuristic transfers is a property of the optimizer, not of the heuristic'
version: 1
tags:
- training-optimization
date: '2026-09-16'
source:
- LIT-058
- LIT-265
explains:
- SOTA-218
- SOTA-221
summary: >-
  Shallue et al. (2018), [LIT-058](../literature.d/LIT-058.md), found no learning-rate scaling rule that held
  across 35 workloads and concluded that practitioners must retune at every
  batch size. You et al. (2019), [LIT-265](../literature.d/LIT-265.md), then scaled BERT to 32K on a square-
  root rule with no retuning at all. The two results are usually read as a
  disagreement about heuristics. They are better read as one result about
  optimizers: a scaling rule is a guess about how the usable step size grows
  with the batch, that step is bounded by the worst-conditioned direction the
  optimizer does not normalize away, and an optimizer that normalizes more
  directions carries the same rule further.
---

# THEORY-012: How far a batch-size scaling heuristic transfers is a property of the optimizer, not of the heuristic

## The claim

A learning-rate scaling rule — multiply by `k`, by `sqrt(k)`, hold fixed — is a
guess about where the tuned optimum moved when the batch grew by `k`. Whether
the guess is right is not a property of the rule. It is a property of what
bounds the usable step size for the optimizer applying it.

For an optimizer with one global step size, that bound is set by the
worst-conditioned direction in the model: one layer whose curvature is far
above the rest caps the step for every layer. For an optimizer that normalizes
the update per layer, and again per coordinate within a layer, the bound is set
by something closer to the average. [LIT-265](../literature.d/LIT-265.md)'s Theorem 1 is the formal shape of
this — simplified LAMB converges at `O(1/sqrt(T))` with the constant carrying
`L_avg`, the mean per-layer smoothness, where the corresponding SGD bound
carries `L_inf`.

So the same rule can be right over a range and wrong past it, and where it
stops is where the optimizer's own bound stops moving proportionally. Read this
way, the two results that look like a contradiction are the same result seen
from either side:

- **The negative half.** [LIT-058](../literature.d/LIT-058.md) swept 35 workloads with SGD, momentum and
  Nesterov momentum — three optimizers, one family, one global step size — and
  found no heuristic that held across them. Its own summary is that it was
  "unable to find reliable support for any of the previously proposed
  heuristics".
- **The positive half.** [LIT-265](../literature.d/LIT-265.md) applied a square-root rule to a two-level
  normalized optimizer and carried BERT to a batch of 32K with no per-batch-size
  tuning, on the same workload where a grid-searched AdamW stops reaching the
  target past 16K.

Neither paper is a counterexample to the other. [LIT-058](../literature.d/LIT-058.md) never tested a
layerwise-normalized optimizer, because none of the ones it tested was; [LIT-265](../literature.d/LIT-265.md)
never swept 35 workloads.

## What was actually shown, and by whom

**[LIT-058](../literature.d/LIT-058.md) shows that the optimizer moves the boundary, not just the heuristic.**
This is the finding that makes the account more than a story, because it is a
controlled comparison inside one paper: SGD with momentum, and Nesterov
momentum, extend the perfect-scaling regime to larger batch sizes than plain
SGD on the same workloads — and the paper could only see it because it tuned the
momentum rather than holding it fixed. Its discussion says the rest out loud:
that accurate scaling predictions "must depend on a combination of non-obvious
properties of the model, optimizer, and data set", that model and optimizer are
plausibly responsible for the largest part of the variation, and that
"optimizers that estimate local curvature information might be able to benefit
more from large batches than optimizers that only use gradients". That last
sentence is this account, written by the paper usually cited against it.

**[LIT-265](../literature.d/LIT-265.md) shows that the two levels are both needed.** LARS is layerwise and
SGD-based; it works on ResNet-50 and fails on BERT at every batch size. LAMB
adds per-coordinate adaptivity underneath the same layerwise ratio and works on
both. Whatever is being normalized away, one level of it is not enough for a
model whose layers differ as much as an attention stack's do — which is the
mechanism's own prediction about where it should fail, coming out right.

**[LIT-265](../literature.d/LIT-265.md) also does not claim the heuristic is correct.** It reports its
large-batch numbers under the heading *untuned*, and says in three places that
manual tuning does better: at a batch of 16K, changing the fine-tuning learning
rate alone moves SQuAD F1 from the reported 91.345 to 91.688. The claim is that
the rule is good enough to reach a fixed target without a sweep. That is a
weaker claim than the one the record read into it, and it is the claim this
account needs.

## What rests on it

Two practices that read as a contradiction, and this is what lets them both
stand.

[SOTA-218](../practices.d/SOTA-218.md) — retune at every batch size you compare — is a rule about
*measurement*: a steps-to-target curve drawn with transferred metaparameters
measures the heuristic, not the batch size. [SOTA-221](../practices.d/SOTA-221.md) — change the
optimizer's conditioning rather than the scaling rule — is a rule about
*reaching a target*, and the no-retuning result it rests on is a claim about
sufficiency for one target rather than about the rule being correct. [LIT-265](../literature.d/LIT-265.md)'s
own tables are the demonstration that these are different claims: untuned LAMB
reaches the target, tuned LAMB beats it.

Without this account the record has to choose, and either choice is wrong.
Drop [SOTA-218](../practices.d/SOTA-218.md) and every large-batch optimizer paper reporting a good number
without a sweep counts as a refutation of it. Drop [SOTA-221](../practices.d/SOTA-221.md) and the
record holds a methodological rule with nothing to say to the person who
actually needs a bigger batch.

It also says what [SOTA-198](../practices.d/SOTA-198.md) is doing in the same neighbourhood without conflict.
The gradient noise scale is a prospective predictor of where the wall is —
[LIT-058](../literature.d/LIT-058.md) asks for exactly such a thing in its future-work section, two months
before [LIT-017](../literature.d/LIT-017.md) published one. This account is about what *moves* the wall.
Measuring where it is and changing where it is are different operations, and a
reader needs both.

## What this does not say

**It is a synthesis, and neither paper states it.** [LIT-058](../literature.d/LIT-058.md) gestures at it in a
discussion section and [LIT-265](../literature.d/LIT-265.md) supplies a theorem about one of its two halves.
Nothing here is a controlled test of the account itself, which is why the status
is `Proposed` and why `promote_when` names the experiment nobody has run: the
same curve, retuned at every point, for a layerwise optimizer and a global one
on one workload.

**"Conditioning" is doing more work than either paper licenses.** The `L_avg`
versus `L_inf` argument is proved for simplified LAMB only — no momentum, no
weight decay — and the connection between a smoothness constant in a
convergence bound and the empirical batch size at which a curve bends is an
analogy, not a derivation. The bound is worst-case and the curves are measured.

**It does not predict where any particular wall is.** If it is right, an
optimizer that normalizes more directions carries a rule further; it says
nothing about how much further, or about which of the many things an optimizer
can normalize matter. [LIT-058](../literature.d/LIT-058.md)'s central negative result — that the transitions
cannot be predicted from properties of the workload anyone has identified —
survives this account completely, and applies to it.

**It says nothing about solution quality.** Both papers are about steps to a
fixed target. [LIT-058](../literature.d/LIT-058.md) separately reports no evidence that larger batches degrade
out-of-sample performance; that is a different finding and is not what this
document rests on.
