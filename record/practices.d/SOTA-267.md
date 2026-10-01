---
number: 267
status: Proposed
formerly:
- SOTA-tmp8nitg
promote_when: >-
  A data schedule of this shape run on a natural corpus rather than a
  synthetic population, over several seeds, with the out-of-distribution cost
  measured as well as the knowledge gain; or a pretraining report that says
  it trained on a subset of its entities (or up-weighted frequent ones) early
  and widened later. What would not move it: another demonstration that
  imbalance shortens a plateau, which is shown here and is only half the
  trade-off.
consensus: unreplicated
consensus_note: >-
  One group, a synthetic biography task, a single seed for every schedule
  and distribution result, and the schedule is tuned in the setting it is
  evaluated in. The mechanism behind it is unusually well
  established for an unreplicated result — the plateau's identity is shown
  by intervention, not inferred.
title: 'Warm up on a subset of the entities before training on all of them, rather than holding one distribution fixed throughout'
version: 3
history:
- version: 2
  date: '2026-09-23'
  note: >-
    Appends `signal-structure`. A load-bearing part of this
    document is a property of the data: its mechanism is the frequency
    distribution of entities in the training data: the head sets the
    plateau, the tail sets acquisition speed, and the measured optimum is an
    inverse power law.
- version: 3
  date: '2026-09-30'
  note: >-
    Recommendation restated to what the source tested, following a
    re-reading of it done for the sibling record (nucleation's reading of the same paper). The
    title said "start the training distribution imbalanced and flatten it";
    the paper ran a uniform warm-up on a subset of individuals, then uniform
    on all, and no skewed distribution annealed toward flat. The "inverse
    power law with exponent between 1 and 2" is withdrawn (the sweep stops at
    1; the plateau-minimising exponent is 0.6–0.8), the head/tail frequency
    dependence is marked as the paper's argument rather than a measurement,
    plateau growth is given as the fitted 0.43·N^0.81, and the single seed
    is stated. Status stays `Proposed`. The old wording is kept in the
    marked notes.
tags:
- data-pipeline
- signal-structure
date: '2026-09-20'
source:
- LIT-450
introduced_by:
- LIT-450
implementations: []
summary: >-
  Zucchet et al. (2025), [LIT-450](../literature.d/LIT-450.md) — the paper argues two quantities move in
  opposite directions: plateau length is governed by how often the *most*
  common entities appear, acquisition speed after the plateau by how often
  the *least* common ones do. So concentration buys an early exit from the
  plateau and costs the tail, and a warm-up that trains on a subset of the
  entities first, then on all of them, beat the best fixed distribution
  tried, in single-seed runs on synthetic biographies.
explained_by:
- THEORY-028
---

# SOTA-267: Warm up on a subset of the entities before training on all of them, rather than holding one distribution fixed throughout
<!-- inactive-ok-file: SOTA-130 — Proposed, and named as one of the task-stage curricula this is not -->

## Source

Zucchet et al. (2025), [LIT-450](../literature.d/LIT-450.md) — [ARXIV-2503.21676](https://arxiv.org/abs/2503.21676).

## The trade-off is the practice

Learning factual recall passes through a long plateau — the model sits at
exactly the loss an ideal model with no entity-specific knowledge would
reach, for a time that grows with the number of entities — "almost linearly"
in the source's words, fitted as `0.43·N^0.81`, which is sublinear.

Two quantities govern the two sides of it, the source argues, and they point
opposite ways:

- **Plateau length is set by the frequency of the most common entities.**
  Concentrate the distribution and the plateau is shorter.
- **Acquisition speed after the plateau is set by the frequency of the least
  common entities.** Flatten the distribution and the tail is learned faster.

Neither dependence is isolated experimentally; the source derives them as an
"intuition" (§3.1) and measures their consequences. Those are what the
practice rests on. Sampling entities ∝ `i^(−α)` over `α ∈ [0, 1]` (1 is
Zipf), the plateau shortens as `α` rises to **0.6–0.8, whatever the
population**, and more imbalance than that hurts. The `α` that minimises
*final* loss grows as the plateau takes a larger share of the budget —
larger populations, shorter runs. So no fixed distribution is right.

**What was tested as a schedule is a warm-up**: train uniformly on a subset
of the entities for a few epochs, then uniformly on all of them. It beat the
best fixed distribution tried, by most when the population was large, because it
takes each quantity where it is cheap. The source's control argues it is not
just a smaller population in disguise: uniform training on a population of
83k scores 97.72% on it, which is 63.26% counted over 128k, against 94.92%
for the warm-up on 128k. The numbers are this setting's; the direction is
the transferable part.

The trade-off and the warm-up both originate in LIT-450. Zucchet et al.
derive the trade-off from their account of the plateau, sweep fixed
power-law distributions over several population sizes, and propose the
subset-first warm-up as the schedule that takes each side where it is cheap.

*Corrected 2026-09-30. This practice read "start the training distribution
imbalanced and flatten it", said a schedule of that shape beat the best fixed
choice, and gave the fixed optimum as "an inverse power law with exponent
between 1 and 2, roughly independent of population size". The source ran no
skewed-to-flat schedule and no exponent above 1, and the
population-independent optimum is the plateau-minimising one.*

## Why it is not just another curriculum

The record holds curriculum practices — [SOTA-129](SOTA-129.md), [SOTA-130](SOTA-130.md), [SOTA-123](SOTA-123.md) —
and all of them order *task stages*: pretrain, then SFT, then RL. This orders
the **distribution within a stage**, and it is justified by two quantities
with opposite signs rather than by an intuition about difficulty.
That makes it falsifiable in a way "easy examples first" is not: if plateau
length did not track head frequency, or acquisition did not track tail
frequency, the recommendation would collapse.

The source calls it a promising, "preliminary and task-specific" case of a
curriculum helping self-supervised learning, and notes it differs from
curriculum learning in that data complexity stays constant. That framing is
worth keeping — the general record on curricula in this setting is poor.

## The mechanism is what makes it more than a fit

[THEORY-028](../theory.d/THEORY-028.md) is the account: the plateau is the attention extraction
circuit being built, and until it exists the error at the attribute token
does not reach the name tokens, so the key-value store cannot learn.
Training on fewer entities first gets that circuit built sooner; the
circuit then transfers — the source's stated assumption — and the tail can be
learned once it exists.

That is why the schedule works in the direction it does, rather than the
other way round, and it predicts where the practice should stop applying:
wherever the plateau is not a shared prerequisite being built.

## Conditions, and why this is `Proposed`

**Synthetic biographies, with an exactly known population size.** A natural
corpus does not expose that quantity, and nothing here shows the plateau is
present or measurable in one.

**The schedule is tuned in the setting it is evaluated in**, so its margin
over the best fixed distribution is optimistic; for the largest population
the best warm-up setting lay at the edge of the grid searched.

**Every schedule and distribution result is a single seed.** Only the
three-phase figure uses five (App. B.3). That, with the synthetic setting, is
why this stays `Proposed` rather than moving either way: the evidence is an
early result, not a contrary one.

**The out-of-distribution cost is not measured, and the neighbouring
literature says there is one.** The source itself cites Park et al., who find
low task diversity shortens plateaus and yields solutions that generalise
worse out of distribution. The schedule is proposed as mitigating the
overfitting this causes, and that mitigation is checked on in-distribution
knowledge only. A reader adopting this is trading against something nobody
has priced.

Excessive imbalance is separately reported to hurt, "likely due to
overfitting", so
the recommendation has an interior optimum and is not "more imbalance is
better".

## Known implementations

- None. No pretraining report in the record describes scheduling its entity
  frequency distribution.
