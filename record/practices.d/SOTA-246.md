---
number: 246
status: Proposed
formerly:
- SOTA-tmp8ornu
promote_when: >-
  Self-influence used to clean a language-model pretraining or instruction
  corpus at a scale where the corpus cannot be inspected by hand, with what it
  surfaced characterised against what a loss-ranked or heuristic pass
  surfaced. A negative result at that scale would be as useful. What would not
  move it: another classification benchmark with synthetically flipped labels,
  which is the regime this is already established in and the easiest kind of
  error to find.
title: 'Find mislabelled training data by self-influence, not by training loss'
version: 1
consensus: emerging
consensus_note: >-
  Two groups with competing methods report it, and the second evaluates
  against the first rather than in isolation, which is stronger than the usual
  single-source case. It is not settled: every evaluation in the record uses
  synthetic label corruption at classification scale, and no training report
  here says it cleaned its corpus this way.
tags:
- data-pipeline
- analysis-and-evaluation
date: '2026-09-17'
source:
- LIT-403
- LIT-400
- LIT-402
introduced_by:
- LIT-403
implementations:
- 'TracIn'
summary: >-
  Koh and Liang (2017), [LIT-403](../literature.d/LIT-403.md), with [LIT-400](../literature.d/LIT-400.md) — rank training
  points by their influence on their own loss and inspect from the top.
  Mislabelled examples are strong proponents of themselves, so they sort to
  the front; high training loss does not separate them nearly as well.
explained_by:
- THEORY-018
---

# SOTA-246: Find mislabelled training data by self-influence, not by training loss

## Source

Koh and Liang (2017), [LIT-403](../literature.d/LIT-403.md) — the method and the dataset-repair
experiment. Pruthi et al. (2020), [LIT-400](../literature.d/LIT-400.md) — the same recommendation from
a different estimator, with the mechanism. Bae et al. (2022), [LIT-402](../literature.d/LIT-402.md) —
the correction to what an influence estimate measures, in `source:` because
without it this practice rests on an explanation the field abandoned.

## The instruction

Score each training example against **itself**: the influence of the point on
its own loss. Sort descending. Inspect from the top.

The obvious alternative is to sort by training loss — the examples the model
gets wrong. It works less well, and the reason it works less well is the
interesting part.

## Why self-influence separates errors and loss does not

A mislabelled example is a **strong proponent of itself**. Strong because it
is an outlier: nothing else in the corpus supports its label, so the model
has to move specifically for it. A proponent because the movement does reduce
its loss — with respect to the wrong label it carries.

High training loss picks up two populations that self-influence separates: the
genuinely mislabelled, and the genuinely hard. Both have high loss. Only the
first is an example the model had to be dragged toward on its own.

On Enron1 spam with 10% of labels flipped, inspecting in influence order
repaired the dataset after checking fewer points than the highest-loss
ordering or random inspection, over 40 repeats, with no access to test data.
On CIFAR-10 with 10% of labels changed to the highest-scoring incorrect class,
TracIn's self-influence recovered more of the corruption at a fixed inspection
budget than influence functions or representer points.

## The explanation under it was replaced and the practice was not

<!-- inactive-ok-block: THEORY-017 — Rejected on purpose, and this paragraph is about
     the rejection. Citing the successor alone would lose the fact that something moved. -->
`THEORY-017` — the account this method was derived from, that an
influence estimate approximates what would happen if you removed the point and
retrained — is `Rejected` for neural networks. `THEORY-018` replaces it:
what the estimate tracks is the proximal Bregman response function.

That would be a reason to withdraw this practice if it needed the
counterfactual. It does not. **It needs an ordering over training points**, and
[LIT-402](../literature.d/LIT-402.md) says explicitly that the PBRF supports the use cases that
motivated influence functions, naming mislabelled-example detection as one.
The practice is filed knowing which of its foundations moved.

## Conditions

**Every evaluation in the record is synthetic label corruption at
classification scale.** Labels flipped at random, or to the most confusable
class — a clean, adversarial, well-posed kind of error. Whether self-influence
separates *natural* annotation noise, ambiguity or systematic annotator bias
is untested here, and those are the errors real corpora have.

**Nothing here is at language-model scale.** Enron1 is 4,147 documents;
CIFAR-10 is 50,000 images. [LIT-401](../literature.d/LIT-401.md) shows the machinery reaches 52B
parameters, and nobody has pointed it at corpus cleaning.

**Pick the estimator by what you have, not by which paper you prefer.** TracIn
needs saved checkpoints, per-example gradients and a loss, and no curvature.
Influence functions need only the final model, and an inverse-Hessian
approximation good enough to be worth the trouble — EK-FAC, at scale. Which
constraint binds is usually decided by how the training was operated rather
than by a judgement about methods.

**Self-influence is the cheap diagonal, and cheapness is the argument.** The
full influence matrix answers far more and costs far more; this practice needs
one number per training example, which is why it is the use case that has
survived every reinterpretation of what the number means.

## Known implementations

- **TracIn** — the released self-influence implementation, evaluated on this
  use case directly.
