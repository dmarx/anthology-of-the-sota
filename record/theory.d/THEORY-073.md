---
number: 73
status: Proposed
formerly:
- THEORY-tmpgrdfw
title: 'Training passes through stages marked by changes in loss-landscape degeneracy, and the loss curve does not show them'
version: 1
tags:
- analysis-and-evaluation
- in-context-learning
- training-optimization
- capability-thresholds
date: '2026-09-22'
source:
- LIT-543
- LIT-544
extends:
- THEORY-075
promote_when: >-
  The stage division is reproduced on a model somebody else trained, for a
  purpose other than studying it — a checkpoint series from a public training
  run — and the boundaries again coincide with structural or behavioural
  changes identified independently. Two case studies by the method's own
  authors is what `Proposed` is for; a third from outside is what would settle
  it. A second paper agreeing that degeneracy is interesting would not.
summary: >-
  Hoogland et al. ([LIT-543](../literature.d/LIT-543.md)) estimate the local learning coefficient
  through training and take critical points of that curve as stage boundaries.
  In a 2-layer language transformer the five stages land on bigrams, n-grams,
  previous-token heads and the induction circuit; in an in-context regression
  transformer they land on the acquisition of in-context learning and then its
  **deterioration**. The claimed advantage over a progress measure is that no
  mechanistic hypothesis is needed in advance. The evidence is coincidence
  across two models, and the authors call it suggestive.
---

# THEORY-073: Training passes through stages marked by changes in loss-landscape degeneracy, and the loss curve does not show them

<!-- The relation to THEORY-075 is `extends`, not `corrects`: the
     foundations say the exponent is the right complexity measure, and this
     says the exponent moves in structured ways during training. Same
     mechanism, applied further. -->

## The account

If `λ` measures how degenerate the loss landscape is around the current
parameters, then watching `λ` through training watches something the loss does
not report: not how well the model fits, but how much room it has to vary
without changing what it computes. The claim is that this quantity moves in
distinguishable periods, that the boundaries between them are real, and that
they coincide with the formation and reorganisation of internal structure.

The method inverts the usual order. A progress measure is built from a
hypothesis about the mechanism and then tracked. Here the boundaries are found
first, from one setting-agnostic curve, and interpreted second — which is why
the paper calls degeneracy an "unsupervised" alternative, and why it is honest
that "once a change is detected through its effect on degeneracy, it remains to
interpret the change".

## What was measured

**Two-layer attention-only language transformer.** Five stages ending at
`t = 900 / 6.5k / 8.5k / 17k / 50k`, with
`Δλ̂ = +26.4 / +22.5 / −1.57 / +8.62 / +1.77` against
`Δℓ̂ = −2.33 / −1.22 / −0.18 / −0.40 / −0.34`. Bigram statistics, then common
n-grams, then previous-token heads, then the induction circuit of Olsson et al.
A single training run recapitulates the progression Olsson et al. found across
*fully-developed models of increasing depth*.

**In-context linear regression transformer.** Five stages ending at
`t = 1k / 40k / 126k / 320k / 500k`, with
`Δλ̂ = +21.4 / +149 / −12.3 / −44.1 / +3.56`. The model learns the optimal
context-independent prediction, then acquires in-context learning — and then
**loses it** across LR3 and LR4 while specializing to its pre-training task
distribution, with layer-normalization weights collapsing to zero, all while
the loss keeps falling.

**In a toy model, the same structure is derived rather than observed.**
[LIT-544](../literature.d/LIT-544.md) shows that in the Toy Model of Superposition the critical points
governing the posterior's phases are the same ones that explain SGD's plateaus
— which is the closest thing to a mechanism this account has.

## Why it is `Proposed`

**The evidence is coincidence, and the authors say so.** "Suggestive evidence
that degeneracy and development are linked." Stage boundaries land near
structural changes in two models; nothing derives one from the other, and with
five boundaries per model the argument is qualitative.

**Two case studies, labelled as two case studies.** "We do not claim that the
structural and behavioral developments we observed in each setting are
universal phenomena." Neither model is large, and for both of them the final
stage had no change the authors could find.

**The stage rule is a convention.** "Critical points of the LLC curve" is
reasonable and is a choice; the estimator is an SGLD sample with a localizing
radius, so the curve's fine structure is partly the sampler's.

**And the decreases are unexplained.** `λ` falls in some stages, in both
models. Saddle-to-saddle theory predicts complexity increasing; the transitions
sketched in the source's own §5 are increases. Lowering `λ` at constant loss
also lowers the free energy, so it is permitted — but, in the authors' words,
"providing a full theoretical account of these stages is an open problem". An
account of development that cannot say why development sometimes runs backwards
is incomplete on its own terms.

## What it is up against, and what it is not

**It is a rival to `LIT-085`'s progress measures and the source names it as
one.** `SOTA-200` records that those measures are computed by projecting onto
five frequencies the network was reverse-engineered to be using, and are
meaningless without that reverse-engineering. This needs no such prerequisite —
and returns a boundary rather than a mechanism, which is less than the
reverse-engineering gives.

**It is not a claim that `λ` explains the stages.** Only that it finds them.
Whether the degeneracy change causes the structural change, is caused by it, or
is the same event under two descriptions, is not addressed.
