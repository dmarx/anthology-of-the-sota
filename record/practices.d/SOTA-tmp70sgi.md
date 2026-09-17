---
status: Proposed
promote_when: >-
  The inversion demonstrated on a language-model pretraining corpus: a run
  that ranks examples or documents by a difficulty score, prunes from
  opposite ends at two token budgets, and reports which end won at which
  budget. A theoretical extension to next-token prediction would also move
  it, if it predicted a crossover point rather than asserting one exists.
  What would not move it: another vision-classification result, which would
  restate the finding inside the regime it is already established in; or a
  filtering result reporting a quality crossover, which is a different object
  ranked on a different axis and is already SOTA-170.
title: 'Discard the easy examples when data is abundant and the hard ones when it is scarce'
version: 1
consensus: unreplicated
consensus_note: >-
  One group, 2022, and no independent test of the inversion at any scale. The
  underlying claim that redundant examples can be pruned is widely accepted;
  the direction-flip is what nobody has re-run, and it is the part that
  changes what you do.
tags:
- data-pipeline
- training-optimization
date: '2026-09-17'
source:
- LIT-tmpy1abi
- LIT-tmpd1gpw
introduced_by:
- LIT-tmpy1abi
implementations: []
summary: >-
  Sorscher et al. (2022), [LIT-tmpy1abi](../literature.d/LIT-tmpy1abi.md) — power-law scaling in dataset size is
  evidence of redundancy, and given a difficulty ranking it can be beaten
  toward exponential. But which end of the ranking to discard flips with how
  much data you started with, and the fraction to discard has to grow with the
  corpus.
---

# SOTA-tmp70sgi: Discard the easy examples when data is abundant and the hard ones when it is scarce

## Source

Sorscher et al. (2022), [LIT-tmpy1abi](../literature.d/LIT-tmpy1abi.md) — [ARXIV-2206.14486](https://arxiv.org/abs/2206.14486), for the
inversion and the scaling result. Paul et al. (2021), [LIT-tmpd1gpw](../literature.d/LIT-tmpd1gpw.md) —
[ARXIV-2107.07075](https://arxiv.org/abs/2107.07075), for the upper cutoff in the Conditions below, which
is a correction to this instruction rather than a separate one.

## The claim under the claim

Error falls as a power law in dataset size. That is usually read as a budget
constraint. It can equally be read as a **measurement of how much the corpus
repeats itself**: if each new example taught something the others did not,
error would not fall so slowly.

Read that way, the exponent is a property of the data rather than of the
problem, and a ranking of which examples teach least is a way to attack it.
The paper shows — analytically for perceptron learning, empirically for
ResNets on SVHN, CIFAR-10 and ImageNet and a ViT fine-tuned on CIFAR-10 —
that error can then fall **exponentially** in the size of the pruned set.

## Why the direction flips

The instruction is not "keep the hard examples", which is what the pruning
literature is usually summarised as. It is that the right end to discard
depends on how much data you have relative to what the model needs:

- **Data abundant** — keep the hard examples. The easy ones are near-duplicates
  and their information is already paid for; the frontier is the decision
  boundary, and only the hard examples are near it.
- **Data scarce** — keep the easy ones. Hard examples carry fine-grained
  information about a boundary the model has no coarse fix on yet, so training
  on them overfits before the basics are in place. Here keeping the hardest
  examples does **worse than random pruning**, which is the result that makes
  this worth filing rather than assuming.

Predicted by the theory and confirmed outside it on a ResNet18 trained on
CIFAR-10 under EL2N.

## The fraction is a schedule, not a setting

The exponential regime is reached only if the **pruned fraction increases with
the initial dataset size**. Fix the fraction and the improvement decays back
to a power law. This is the part most likely to be dropped when the result is
repeated, and it is what makes the recommendation operational: a corpus that
doubles should be pruned harder, not by the same proportion.

There is a floor. At any nonzero misalignment between the ranking and the true
difficulty, the exponential regime crosses back to a power law once the pruned
set is small enough.

## Conditions

**Vision classification is the entire evidence base.** Every experiment here is
supervised image classification. The record's data practices are about
language-model pretraining corpora, and no result connects the two. This is
why the status is `Proposed`, and it is the whole of the reason.

**The metric is the hard part, and most metrics do not survive a scale
change.** The paper's own benchmark of ten difficulty metrics at ImageNet
scale finds that most of the ones that work at CIFAR scale do not, and that
the best performer needs a label for every example and substantial compute. A
difficulty ranking validated at one scale is not evidence at another — which
is the same caution this practice's own status is an instance of.

**The hard end has its own cutoff.** [LIT-tmpd1gpw](../literature.d/LIT-tmpd1gpw.md) finds that keeping *only*
the top-scoring examples is not optimal even on clean data, and that the
excluded window widens as label corruption rises, because the hardest examples
and the mislabelled ones are the same examples. So "keep the hard ones when
data is abundant" means keep a window, not a tail, and the corpus's noise rate
sets where the upper edge goes. Without a validation set to place it, that
paper counsels caution about keeping high scorers at all.

**Redundancy is not quality.** This ranks examples by what they teach, not by
whether they are good. A well-written document that says what a thousand
others say is exactly what this discards and exactly what a quality filter
keeps — so this does not compose with the record's filtering practices by
simply running both.

## A crossover the record has seen once before

[SOTA-170](SOTA-170.md) reports that aggressive filtering wins at a 1T-token horizon and
loses at 15T, and prescribes rephrasing rather than discarding once the corpus
will run out. That is a **sign change in a data-selection trade, driven by how
much data you have relative to what you intend to spend** — the same shape as
the inversion above, arrived at independently and measured on different
objects.

They are not the same claim and this practice does not assert that they are:
one ranks documents by quality, the other ranks examples by difficulty, and no
experiment joins them. What the pair is worth is a prior — when a
data-selection recommendation is stated without naming a data budget, suspect
it is the answer for one regime being quoted in the other.
