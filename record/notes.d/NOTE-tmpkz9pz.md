---
status: Read
paper: LIT-tmpy1abi
title: 'Beyond neural scaling laws: beating power law scaling via data pruning'
version: 1
date: '2026-09-17'
summary: >-
  Power-law scaling of error in dataset size is a symptom of redundancy, not a
  ceiling. With a ranking of example difficulty and a pruning fraction that
  grows with the corpus, error can fall exponentially instead. Which end of
  the ranking to discard inverts with data abundance: keep hard examples when
  data is plentiful, easy ones when it is scarce.
---

# NOTE-tmpkz9pz: Beyond neural scaling laws: beating power law scaling via data pruning

<!-- inactive-ok-file: SOTA-tmp70sgi, SOTA-241, ADR-043 — the practice this reading files,
     the adjacent proxy practice named in the Bearing section for where R4 would have gone,
     and the decision that governs naming a deferral's condition instead of filing it. All
     Proposed; the reading is about what to file, so a Proposed target is the subject. -->

## Contribution

Power-law scaling of test error in dataset size is the empirical regularity
the whole scaling-law literature is built on, and it is brutal economics: a
drop from 3% error to 2% can cost an order of magnitude more data and energy.

This paper argues the exponent is not fundamental. **Power-law scaling in
dataset size is itself evidence that most examples are redundant** — if each
new example taught something new, error would not fall so slowly. Given a
ranking of which examples to discard first, the paper shows analytically (for
perceptron learning, via a statistical-mechanics teacher–student calculation)
and empirically (ResNets on SVHN, CIFAR-10 and ImageNet; a ViT fine-tuned on
CIFAR-10) that error can fall **exponentially** in the size of the pruned set.

It also does the unglamorous half: a benchmark of ten pruning metrics at
ImageNet scale, and a new one that needs no labels.

## Key insight

**A scaling exponent is a property of the corpus, not of the problem.** The
slow exponent is what redundancy looks like from the outside, so the way to
beat it is not more data but a better ordering of the data you have.

Two consequences follow, and the second is the surprising one. First, the
exponential regime is only reached if the **pruning fraction increases with
the initial dataset size** — a fixed fraction collapses back to a power law,
so the policy is a schedule rather than a setting. Second, **which end of the
ranking to discard depends on how much data you started with.**

## Assumptions

- The analytic result is for a **perceptron in a teacher–student setup**,
  solved in the thermodynamic limit, with difficulty measured as margin with
  respect to a *probe student* trained on a small subset. The probe's
  misalignment with the teacher is the angle `θ`.
- Difficulty must be **rankable before training on the pruned set**. Every
  empirical result inherits whatever the chosen metric actually measures.
- The empirical setting is **supervised image classification**. Nothing here
  is tested on language-model pretraining.

## Key results

- **Exponential scaling of error in pruned dataset size**, in theory and with
  empirical signatures in all four settings tested. It is conditional: at
  nonzero `θ` the exponential regime **crosses over back to a power law** once
  the pruned set gets small enough, so there is a floor.
- **The inversion.** With abundant data, keeping the hardest (smallest-margin)
  examples substantially beats random pruning; with scarce data, it does
  *worse* than random, and keeping the easiest examples is better. Confirmed
  outside the theory on a ResNet18 trained on CIFAR-10 under EL2N.
- **Ten metrics benchmarked on ImageNet, most of which fail there.** Metrics
  that perform well on CIFAR-scale data scale poorly; the best (memorization)
  is computationally intensive and needs a label per image.
- **A self-supervised prototype metric.** `k`-means in the embedding space of
  a SwAV-pretrained ResNet-50, difficulty = Euclidean distance to the nearest
  centroid. Matches or exceeds memorization down to 70–80% of ImageNet kept,
  with **no labels at all**, and is robust to `k` an order of magnitude either
  side of the class count.
- **20% of ImageNet is discardable at no cost**, and pruning to 60% leaves
  out-of-distribution accuracy intact against an accuracy-matched baseline.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Power-law scaling in dataset size can be beaten, toward exponential, given a good difficulty ranking | strong | analytic theory plus signatures on four setups |
| C2 | The exponential regime requires the pruned fraction to grow with the initial dataset size | strong | derived, and the Pareto frontier is computed |
| C3 | Keep hard examples when data is abundant, easy ones when scarce | strong | predicted by theory, confirmed on ResNet18/CIFAR-10 |
| C4 | Most existing difficulty metrics do not survive the move to ImageNet | strong | the benchmark is the paper's own experiment |
| C5 | A label-free prototypicality metric is competitive with the best supervised one | moderate | one metric, one dataset, holds to 70–80% kept |
| C6 | Pruning does not hurt OOD accuracy at matched IID accuracy | weak | 17 datasets, one metric, the authors call it suggestive |

## Method

Rank every example by a difficulty metric; discard from one end; train on
what remains. The contributions are which end, how much, and what metric.

For the label-free metric: embed the corpus with a self-supervised model,
`k`-means the embeddings, and score each example by distance to its nearest
centroid. Prototypical means easy.

## Concepts

- **Redundancy as the explanation of the exponent** — the reframing. A slow
  power law is a measurement of how much the corpus repeats itself.
- **Pruning fraction as a schedule** — the parameter that has to move with
  corpus size, not be tuned once.
- **Coarse-grained versus fine-grained information** — the mechanism behind
  the inversion. Easy examples locate the target function roughly; hard ones
  refine its decision boundary, and refinement is worthless before the rough
  location is had.
- **Prototypicality as difficulty** — easy examples are near-duplicates, hard
  ones are idiosyncratic outliers, and the distinction is visible in an
  embedding space without labels.

## Connections

The record's data practices are almost entirely about *quality*: which
documents are good enough to keep. This is about *redundancy*: which examples
teach something the others do not. The two can disagree — a high-quality
document that says what a thousand others say is exactly what this discards.

[SOTA-170](../practices.d/SOTA-170.md) is the nearest neighbour and the comparison is worth making
carefully. It reports that aggressive filtering wins at a 1T-token horizon
and loses at 15T, and prescribes rephrasing rather than discarding when the
corpus will run out. **That is a crossover in the sign of a data-selection
trade, driven by how much data you have relative to what you intend to
spend** — structurally the same shape as C3, reached from a different
direction and measured on different objects. They are not the same claim:
[SOTA-170](../practices.d/SOTA-170.md) ranks documents by quality and this ranks examples by difficulty,
and no experiment connects them. What the pairing offers is a reason to
expect crossovers of this kind rather than to be surprised by each one.

## Recommendations

- **R1** — Choose which end of the difficulty ranking to discard by how much
  data you have. *Topic:* data pipeline. *Strength:* strong within vision
  classification, untested elsewhere. *Applies when:* you can rank examples.
- **R2** — Increase the pruning fraction as the corpus grows, rather than
  fixing it. *Strength:* strong in theory, and it is what the Pareto frontier
  requires.
- **R3** — Do not trust a difficulty metric across a scale change; the
  benchmark's main finding is that most of them break. *Strength:* strong.
- **R4** — Use embedding prototypicality when labels are unavailable or
  expensive. *Strength:* moderate — one metric, one corpus.

## Bearing on the record

Sources [SOTA-tmp70sgi](../practices.d/SOTA-tmp70sgi.md), which carries R1 with R2 in its body. `Proposed`: the
evidence is vision classification at CIFAR and ImageNet scale, and every data
practice this record holds is about language-model pretraining corpora.

R3 is not filed as its own practice. It is a caution about the previous
paragraph rather than an independent instruction, and it lives in the
conditions of [SOTA-tmp70sgi](../practices.d/SOTA-tmp70sgi.md) where a reader will meet it at the moment it
matters.

R4 is not filed either, and that is a closer call. It is a real
recommendation with a real result behind it, but it is one metric on one
corpus, and the instruction that generalises — use a cheap proxy that only
has to preserve ordering — is already [SOTA-241](../practices.d/SOTA-241.md), filed from a different
paper in a different domain. Naming it here rather than filing it is the
deferral [ADR-043](../decisions.d/ADR-043.md) asks for: the condition is a second corpus.

## Limitations

- **Everything depends on the metric**, and the paper's own benchmark is the
  evidence that good metrics are scarce and expensive. The authors name this
  as the notable limitation.
- The theory is a perceptron. The empirics are image classification.
- The exponential regime has a floor: it crosses back to a power law.
- C6 (OOD) is offered tentatively by the authors and should not be quoted
  harder than they quote it.

## Open questions

- Does the inversion hold for language-model pretraining, where "example
  difficulty" has no agreed definition and the corpus is not labelled? That is
  the question the record needs answered and the one this paper cannot reach.
- Is the token horizon of [SOTA-170](../practices.d/SOTA-170.md) the same axis as `α_tot` here? If it is,
  two independent literatures are measuring one crossover.
