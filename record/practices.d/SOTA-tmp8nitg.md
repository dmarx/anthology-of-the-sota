---
status: Proposed
promote_when: >-
  A data schedule of this shape run on a natural corpus rather than a
  synthetic population, with the out-of-distribution cost measured as well as
  the knowledge gain; or a pretraining report that says it up-weighted
  frequent entities early and flattened later. What would not move it:
  another demonstration that imbalance shortens a plateau, which is
  established here and is only half the trade-off.
consensus: unreplicated
consensus_note: >-
  One group, a synthetic biography task, and the schedule is tuned in the
  setting it is evaluated in. The mechanism behind it is unusually well
  established for an unreplicated result — the plateau's identity is shown
  by intervention, not inferred.
title: 'Start the training distribution imbalanced and flatten it, rather than holding it uniform throughout'
version: 1
tags:
- data-pipeline
date: '2026-09-20'
source:
- LIT-tmpbtdlg
introduced_by:
- LIT-tmpbtdlg
implementations: []
summary: >-
  Zucchet et al. (2025), [LIT-tmpbtdlg](../literature.d/LIT-tmpbtdlg.md) — two quantities move in opposite
  directions. Plateau length is governed by how often the *most* common
  entities appear; acquisition speed after the plateau by how often the
  *least* common ones do. So imbalance buys an early exit from the plateau
  and costs the tail, and a schedule that starts imbalanced and flattens
  beats every fixed distribution tested.
explained_by:
- THEORY-tmp8a4gm
---

# SOTA-tmp8nitg: Start the training distribution imbalanced and flatten it, rather than holding it uniform throughout
<!-- inactive-ok-file: SOTA-130 — Proposed, and named as one of the task-stage curricula this is not -->

## Source

Zucchet et al. (2025), [LIT-tmpbtdlg](../literature.d/LIT-tmpbtdlg.md) — [ARXIV-2503.21676](https://arxiv.org/abs/2503.21676).

## The trade-off is the practice

Learning factual recall passes through a long plateau — the model sits at
exactly the loss an ideal model with no entity-specific knowledge would
reach, for a time that grows almost linearly with the number of entities.

Two measured quantities govern the two sides of it, and they point opposite
ways:

- **Plateau length is set by the frequency of the most common entities.**
  Concentrate the distribution and the plateau is shorter.
- **Acquisition speed after the plateau is set by the frequency of the least
  common entities.** Flatten the distribution and the tail is learned faster.

So no fixed distribution is right. The optimum imbalance grows as the plateau
takes a larger share of the budget — larger populations, shorter runs — and a
**schedule that starts imbalanced and flattens beats the best fixed choice**,
because it takes each quantity where it is cheap.

For a fixed distribution the measured optimum is an inverse power law with
exponent between 1 and 2, roughly independent of population size. That is
this setting's number and the direction is the transferable part.

## Why it is not just another curriculum

The record holds curriculum practices — [SOTA-129](SOTA-129.md), [SOTA-130](SOTA-130.md), [SOTA-123](SOTA-123.md) —
and all of them order *task stages*: pretrain, then SFT, then RL. This orders
the **distribution within a stage**, and it is justified by two measured
quantities with opposite signs rather than by an intuition about difficulty.
That makes it falsifiable in a way "easy examples first" is not: if plateau
length did not track head frequency, or acquisition did not track tail
frequency, the recommendation would collapse.

The source calls it a rare case of a curriculum genuinely helping
self-supervised learning, and that framing is worth keeping — the general
record on curricula in this setting is poor.

## The mechanism is what makes it more than a fit

[THEORY-tmp8a4gm](../theory.d/THEORY-tmp8a4gm.md) is the account: the plateau is the attention extraction
circuit being built, and until it exists the error at the attribute token
does not reach the name tokens, so the key-value store cannot learn.
Concentrating the distribution gets that circuit built on fewer entities;
the circuit then transfers, and the tail can be learned once it exists.

That is why the schedule works in the direction it does, rather than the
other way round, and it predicts where the practice should stop applying:
wherever the plateau is not a shared prerequisite being built.

## Conditions, and why this is `Proposed`

**Synthetic biographies, with an exactly known population size.** A natural
corpus does not expose that quantity, and nothing here shows the plateau is
present or measurable in one.

**The schedule is tuned in the setting it is evaluated in**, so its margin
over the best fixed distribution is optimistic.

**The out-of-distribution cost is not measured, and the neighbouring
literature says there is one.** The source itself cites Park et al., who find
low task diversity shortens plateaus and yields solutions that generalise
worse out of distribution. The schedule is proposed as mitigating the
overfitting this causes, and that mitigation is checked on in-distribution
knowledge only. A reader adopting this is trading against something nobody
has priced.

Excessive imbalance is separately reported to hurt, through overfitting, so
the recommendation has an interior optimum and is not "more imbalance is
better".

## Known implementations

- None. No pretraining report in the record describes scheduling its entity
  frequency distribution.
