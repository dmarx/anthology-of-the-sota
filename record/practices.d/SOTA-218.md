---
number: 218
status: Active
formerly:
- SOTA-tmpntee6
consensus: unreplicated
consensus_note: >-
  One paper, but an unusually large one: 168,160 trained models across 35
  workloads, built to answer this question and no other. Nobody has replicated
  it at that scale and nobody needs to; what is missing is not a second
  measurement but a second workload family — it predates transformer
  language-model pretraining at scale.
title: 'Retune the learning rate, momentum and schedule at every batch size you compare, never by a scaling heuristic'
version: 2
history:
- version: 1
  note: >-
    Filed with the claim right and four of its supporting figures wrong — the
    run count inflated 426-fold, the workload and optimizer counts both
    understated, and the two batch-size ranges the paper reports separately
    merged into one. None of them came from the paper; all of them came from a
    reading nobody checked against it.
- version: 2
  note: >-
    Figures corrected against ARXIV-1811.03600, and the open tension with LAMB
    closed. The two papers were never in dispute — LIT-265 cites LIT-058
    approvingly — and THEORY-012 is the account that lets both stand.
tags:
- training-optimization
date: '2026-09-15'
source:
- LIT-058
introduced_by:
- LIT-058
implementations: []
summary: >-
  Linear scaling and square-root scaling are not batch-size rules; they are
  guesses about where the optimum moved, and they hold over a narrower range
  than the comparisons people use them for. A curve of steps-to-target against
  batch size drawn with transferred metaparameters is not a measurement of
  batch size at all — it is a comparison between one tuned configuration and
  several untuned ones, and the point where it bends is the point where the
  heuristic failed.
compared_against:
- SOTA-221
explained_by:
- THEORY-012
---

<!-- inactive-ok-file: THEORY-012 — Proposed, and cited here AS the
     Proposed account: a synthesis neither of its two papers states, whose
     `promote_when` names the experiment that would settle it. This practice
     does not rest on it — the retuning rule stands on LIT-058 alone — it
     rests on it only for why SOTA-221 is not a contradiction. -->

# SOTA-218: Retune the learning rate, momentum and schedule at every batch size you compare, never by a scaling heuristic

## What to do

When comparing batch sizes — for a scaling study, a hardware decision, or a
claim that large batches hurt generalization — tune the learning rate,
momentum and the full schedule *independently at each batch size*. Do not
transfer them by linear scaling, square-root scaling, or holding them fixed.
[LIT-058](../literature.d/LIT-058.md) tuned the initial learning rate, the momentum, and both decay
parameters by quasi-random search at every one of its 454 (workload, batch
size) pairs, and that is the standard the claim is stated at.

The corollary for reading other people's curves: a steps-to-result curve that
bends at some batch size is evidence about batch size only if the paper says
it retuned. If it scaled the learning rate linearly instead, the bend is
where linear scaling stopped being right.

## Why

**The heuristics fail, and they fail in the region people use them.** [LIT-058](../literature.d/LIT-058.md)
sweeps 35 workloads — six model families, seven data sets, and SGD, momentum
and Nesterov momentum — and finds no scaling rule that holds across them. Its
own words: it was "unable to find reliable support for any of the previously
proposed heuristics for adjusting the learning rate as a function of batch
size".

The two ranges it reports are worth keeping apart, because they are different
transitions. **Perfect scaling ends anywhere from a batch of 2^4 to 2^13**
depending on the workload, and the **maximum useful batch size runs from
roughly 2^9 to 2^16**. Where either falls cannot be read off the workload:
accurate prediction "must depend on a combination of non-obvious properties of
the model, optimizer, and data set", and the data set's contribution is the
smallest of the three — it does not track data set size in any consistent way,
which the paper checked directly by subsampling MNIST and ImageNet.

**Its comparative finding only exists because it retuned.** SGD with momentum,
and Nesterov momentum, extend the perfect-scaling regime to larger batch sizes
than plain SGD — which is invisible if momentum is held fixed while the batch
grows, since the paper tuned momentum as a metaparameter at every batch size.
It is a statement about the tuned optimum moving, and it does not survive a
heuristic that assumes it moved somewhere specific.

**Its survey of the literature is the same argument applied to other people's
results.** Several studies concluding that small batches generalize better used
an epoch budget, tuned at the smallest batch, and extrapolated by heuristic.
The paper's reading is that this "could just as easily be an artifact of the
learning rate heuristics" — and it finds no evidence that larger batches degrade
out-of-sample performance once the tuning is done properly. That is a separate
finding from the one this practice rests on, and it is the more commonly cited
of the two.

**This record has practices that were written from papers that did not.**
Several batch-size and warmup entries here descend from work that scaled the
learning rate with the batch and reported the result. They are not thereby
wrong, but their evidence is weaker than it reads, and the reason is this
paper.

## What this does not settle

**It predates transformer language-model pretraining.** The workloads are
image classification, an LSTM and a small transformer on LM1B. The claim is
methodological and should carry; the specific ranges should not be assumed to.

**Retuning is expensive, and the paper is what makes it expensive.** Its own
method — independent tuning at every batch size — is why it needed 168,160
trained models to produce 454 points. It gives no cheaper procedure and asks
for one in its future work: "methods to prospectively predict the scaling
behavior of a given workload without requiring careful metaparameter tuning at
several different batch sizes". [SOTA-198](SOTA-198.md) is that method, published two months
later and narrowing the range to an order of magnitude rather than to a batch
size. The two compose — measure the noise scale to find the decade, retune
inside it — and neither replaces the other.

[LIT-337](../literature.d/LIT-337.md)'s contrary claim, that a learning rate tuned for SGD transfers
unchanged to a compressed variant, is the kind of thing this practice says to
check rather than assume.

**It is narrower than it sounds, and [SOTA-221](SOTA-221.md) is the other half.** This is
a rule about *measurement*, not a prohibition on ever training without a sweep.
LAMB reaches a fixed BERT target at a batch of 32K on a square-root rule with no
per-batch-size tuning, and that is not a counterexample: [LIT-265](../literature.d/LIT-265.md) cites [LIT-058](../literature.d/LIT-058.md)
approvingly as its own motivation, reports those numbers under the heading
*untuned*, and says three times that tuning does better. A no-retuning result is
a claim about sufficiency for one target; this practice is about what a curve
means. [THEORY-012](../theory.d/THEORY-012.md) is the account under both, and it is where the reason
they do not collide is written down.
