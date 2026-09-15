---
status: Active
title: 'An evolution-strategies update is mostly a loss-invariant random walk whose size grows with steps and shrinks with population'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
source:
# LIT-tmp4w505 derives it; LIT-tmpphacm is the independent confirmation that
# promoted it — a different group, a different model, and the population-size
# dependence tested directly rather than inferred.
- LIT-tmp4w505
- LIT-tmpphacm
explains:
- SOTA-154
summary: >-
  Hoy et al. (2026), [LIT-tmp4w505](../literature.d/LIT-tmp4w505.md), confirmed by [LIT-tmpphacm](../literature.d/LIT-tmpphacm.md) — an ES weight
  update splits into an
  on-manifold part that changes the loss and an off-manifold part that does
  not, and in a landscape with many flat directions the second dominates. Its
  squared norm grows as sigma^2 d T / N, so the drift that three papers in
  this record read as evidence of forgetting, of functional sparsity, and of
  a failing search is mostly a random walk that the loss cannot see.
---

# THEORY-tmpt76ks: An evolution-strategies update is mostly a loss-invariant random walk whose size grows with steps and shrinks with population

## Source

Hoy et al. (2026), [LIT-tmp4w505](../literature.d/LIT-tmp4w505.md).

## What was actually shown

Decompose the displacement an ES run accumulates into two parts: the
component lying in directions where the loss actually changes, and everything
else. The second part is loss-invariant by construction, so nothing in the
objective pushes back on it and it performs an unbiased random walk. The
paper gives its size: the squared norm of the off-manifold displacement grows
as

    ‖Δθ_off‖² ∝ σ² · d · T / N

with `σ` the perturbation scale, `d` the parameter dimension, `T` the number
of steps and `N` the population size. In a high-dimensional landscape where
most directions carry negligible curvature — which is what an LLM's loss
surface is — this term dominates the total displacement.

**What could have come out the other way.** The scaling is a prediction with
four handles, and the paper reports LLM weight matrices exhibiting the
predicted random-walk behaviour with the theoretical scaling matching
observation. It also predicts consequences that are separately checkable and
were separately observed: the ES update direction should look like a *random*
direction when probed on held-out tasks (it does, where GRPO's looks sharply
task-aligned); ES and GRPO directions should be nearly orthogonal (they are);
the loss should be flat along the ES displacement (it is); and the two
solutions should be linearly connected with no barrier despite all of that
(they are, on four tasks).

The last is the one that would have been hardest to explain away. Two
optimizers travelling in almost perpendicular directions, two orders of
magnitude apart in distance, landing in a basin with no wall between them is
a strange fact on any account except this one.

## What this explains, and how much

**It dissolves an argument three papers in this record were having without
realising it.** [LIT-tmppbfp5](../literature.d/LIT-tmppbfp5.md) measured ES drift at roughly 1000× GRPO's and
concluded it causes catastrophic forgetting. [LIT-230](../literature.d/LIT-230.md) measured it at
roughly 40×, found the performance gains survive zeroing most of it, and
concluded it is harmless. [LIT-231](../literature.d/LIT-231.md) measured the same geometry and concluded
the search is not finding anything at all. On this account all three are
looking at the off-manifold walk: it is genuinely enormous, it genuinely
carries almost no task information, and whether it is harmful is a question
about *what else* you were measuring, not about the drift.

<!-- inactive-ok-block: SOTA-tmpdcmgg — Proposed, filed from this account in
     this same change; naming it is the point -->
**And it makes the drift controllable**, which no previous document in this
line could. `T` and `N` are knobs a practitioner sets. Drift accumulates with
steps and falls with population size, so the same task accuracy bought with a
larger population and fewer steps costs less displacement. [SOTA-tmpdcmgg](../practices.d/SOTA-tmpdcmgg.md) is
that instruction, and [LIT-tmp4w505](../literature.d/LIT-tmp4w505.md)'s own continual-learning result — ES
"remains competitive sequentially when its iteration budget is controlled" —
is the first evidence it works.

<!-- inactive-ok-block: THEORY-006 — Proposed, named as the adjacent account this one sits beside rather than relies on -->
**On [SOTA-154](../practices.d/SOTA-154.md)** it supplies something the practice had been missing in a
different place from [THEORY-006](THEORY-006.md). That account says why there is anything
worth finding near the pretrained weights; this says what the search does with
the rest of the space while it looks.

## The confirmation that promoted this

Schweighofer et al. ([LIT-tmpphacm](../literature.d/LIT-tmpphacm.md)) took the scaling as a prediction and
tested the handle this account is most useful for. Raising the ES population
from 30 to 128 **cuts the update norm by about half** — which is what an
inverse dependence of the *squared* norm on `N` predicts for a 4.3× increase —
and prior-task degradation falls monotonically across population sizes 30, 128
and 256 (their Table 1). Their own summary: "the update norm is indeed
inversely proportional to the population size."

That is the promotion condition, met in the terms it was written in: an
independent group — no shared authors with [LIT-tmp4w505](../literature.d/LIT-tmp4w505.md) — on a different
model, Qwen2.5-3B rather than Qwen3-4B, with `N` varied directly at fixed `T`
rather than the dependence inferred from the algebra.

**One refinement arrived with it, and it sharpens the account rather than
qualifying it.** Even at population 256 or with an anchor penalty, ES update
norms stay an order of magnitude above GRPO's — yet the *distributional* shift
on prior tasks becomes comparable to GRPO's. So the harm is not carried by the
size of the walk: "it is the randomness of the drift unconstrained by the
target task that leads to prior task forgetting for ES, rather than the
magnitude of updates alone." Displacement is the thing that scales; what a
displacement costs depends on whether anything constrained its direction.

## What this does not say

**It does not say the off-manifold walk is harmless.** Loss-invariant means
invariant for *the objective being optimized*. Everything the training reward
does not measure — every prior capability, every held-out benchmark — is free
to degrade along exactly those directions, and [LIT-tmppbfp5](../literature.d/LIT-tmppbfp5.md) reports that it
does, on a long enough horizon. The account explains why the damage is
invisible to the training signal; it does not make it not damage.

**The validation is still narrow even after the confirmation.** Two models,
Qwen3-4B and Qwen2.5-3B, both below 5B, and the second paper varies `N` across
three values on one task. `d` and `σ` — the other two terms — have never been
varied against the prediction at all.

**The decomposition is cleaner than any measurement of it can be.**
"On-manifold" and "off-manifold" are exact only where the loss is exactly
flat; real directions have small nonzero curvature, and how the accounting
degrades as curvature grows is not characterized here.

**It does not adjudicate the failed replication.** [LIT-tmppbfp5](../literature.d/LIT-tmppbfp5.md) reports
GRPO ahead of ES on three of four tasks at 1B–1.5B. Nothing in this account
says who wins on accuracy; it says why the two winners look so different in
parameter space when they tie.
