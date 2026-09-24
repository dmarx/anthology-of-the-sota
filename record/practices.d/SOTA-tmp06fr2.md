---
status: Proposed
promote_when: >-
  A measurement of what selecting on the test split actually costs — the same
  design search run twice, once selecting on a held-out slice of train and
  once on the public validation set, with both evaluated on a third split.
  The cheapest version is a re-analysis of any existing hyperparameter sweep
  that logged validation and test numbers separately. What would NOT meet it:
  more papers adopting the convention, which is adoption rather than evidence
  (`DP-005`).
title: 'Hold out a slice of the training set for model selection instead of selecting on the validation split'
version: 1
tags:
- analysis-and-evaluation
- data-pipeline
date: '2026-09-24'
source:
- LIT-tmp5t7v1
introduced_by:
- LIT-tmp5t7v1
consensus: unassessed
consensus_note: >-
  Not assessed, and the reason is that the question is about a convention
  rather than a technique. Beyer et al. state the practice and their motive in
  one sentence and offer no measurement of the effect, which is why this is
  `Proposed` with an evidential `promote_when` rather than a consensus
  reading. What the record can say: a benchmark whose validation split has
  been public for over a decade has been selected against by everyone, and no
  document here has previously raised it.
implementations:
- big_vision
summary: >-
  Beyer et al. (2022), [LIT-tmp5t7v1](../literature.d/LIT-tmp5t7v1.md) — they train on the first 99% of
  ImageNet-1k and keep 1% as a "minival", stated as being "to encourage the
  community to stop selecting design choices on the validation (de-facto test)
  set." A convention, asserted rather than measured, and the record held no
  document on it.
---

# SOTA-tmp06fr2: Hold out a slice of the training set for model selection instead of selecting on the validation split

## Source

Beyer, Zhai and Kolesnikov (2022), [LIT-tmp5t7v1](../literature.d/LIT-tmp5t7v1.md), §2.

## When this applies

You are choosing anything — an architecture detail, a hyperparameter, an epoch
count, an augmentation level — on a benchmark whose "validation" split is
what results are reported on. ImageNet-1k is the case in front of us;
the pattern covers most long-lived public benchmarks.

## Do this

**Split the training set, not the evaluation set.** Beyer et al. train on the
first 99% of ImageNet-1k and select on the remaining 1%. The reported numbers
then come from a split nothing was chosen on.

The cost is 1% of training data. The thing bought is that the reported number
means what it is usually taken to mean.

## Why this is filed at all

Because the alternative is invisible and universal. A public benchmark's
validation split becomes a de-facto test set the moment results are reported
on it, and then every subsequent paper's design choices are selected against
it — not by anyone cheating, but because that is the number available. The
selection is distributed across the literature rather than happening inside
one study, which is exactly why no single paper's methods section looks wrong.

`SOTA-197` asks readers to account for test-set proximity to the training
data. This is the adjacent failure and the opposite direction: proximity of
the *selection* procedure to the reported split.

## Why it is only `Proposed`

**Nobody has measured the effect, including this paper.** Beyer et al. assert
the practice and its motive in a single sentence and move on; there is no
comparison of a search run against a minival versus against the validation
split. So what is established is that a credible group thinks the convention
is wrong and adopted the fix — which is a reason to consider it and not
evidence about its size.

The `promote_when` asks for the measurement, and the cheap version already
exists as data: any hyperparameter sweep that logged validation and test
numbers separately can be re-analysed for the gap.

## Limitations

- **1% of ImageNet-1k is about 12,800 images**, which is small enough that
  the minival is noisy for fine distinctions. The paper does not discuss
  sizing it, and a slice large enough to separate close candidates costs
  correspondingly more training data.
- **It does not help with a benchmark that has no separate test split at
  all**, which is most of them — the practice makes the reported number
  honest about *selection*, and says nothing about the many-papers-one-split
  problem underneath.
- **The record has no measurement of what this is worth**, which is stated
  rather than implied: this document exists because the convention had no
  representation here, not because its effect is known.
