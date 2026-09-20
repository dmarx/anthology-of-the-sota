---
number: 239
status: 'Proposed'
formerly:
- SOTA-tmp7wadj
title: 'Order training data by skill prerequisite: teach the prerequisite and the dependent skill costs less data'
version: 1
tags:
- data-pipeline
promote_when: >-
  An ordered skill set demonstrated at pretraining scale rather than in
  continual-pretraining and fine-tuning regimes, or a frontier report stating
  that its data order was chosen by prerequisite structure. What would not
  move it: another online mixing method that happens to change proportions
  over time, which is reweighting rather than ordering; or a training-stage
  curriculum (pretrain, SFT, RL), which orders objectives and not data.
consensus: unreplicated
consensus_note: >-
  One group, one framework. The record has nothing to compare it against,
  because this is the only document here that answers *in what order* — every
  other `data-pipeline` practice answers what to include or in what
  proportion.
date: '2026-09-17'
source:
- LIT-392
introduced_by:
- LIT-392
implementations:
- LIT-392
summary: >-
  Chen et al. (2023), [LIT-392](../literature.d/LIT-392.md) — [ARXIV-2307.14430](https://arxiv.org/abs/2307.14430). Training data has a
  prerequisite structure, and it is exploitable: train on a prerequisite skill
  and the dependent skill is reachable with less data. Sample over skill
  mixtures online rather than fixing proportions in advance.
---

# SOTA-239: Order training data by skill prerequisite: teach the prerequisite and the dependent skill costs less data

<!-- inactive-ok-file: SOTA-166, SOTA-103, SOTA-129, SOTA-130 — Proposed or otherwise not in force, named in the axis distinction this practice turns on -->

## Source

Chen et al. (2023), [LIT-392](../literature.d/LIT-392.md) — [ARXIV-2307.14430](https://arxiv.org/abs/2307.14430).

## The claim

Data has an order, and the order is not arbitrary. The framing is explicit:
"just as humans acquire interdependent skills in a deliberate order, language
models also follow a natural order when learning a set of skills from their
training data."

What makes it a practice rather than an analogy is the consequence: ordered
skill sets exist, and "their existence enables more advanced skills to be
learned **with less data** when we train on their prerequisite skills."

So the recommendation is to model the prerequisite structure and sample
accordingly — online over skill mixtures, in continual pretraining where the
goal is many skills, and in fine-tuning where it is one.

## The axis this adds

The record's `data-pipeline` practices answer **what to include** and **in
what proportion**: filtering ([SOTA-170](SOTA-170.md)), deduplication ([SOTA-164](SOTA-164.md)),
proportions ([SOTA-166](SOTA-166.md), [SOTA-103](SOTA-103.md), [SOTA-238](SOTA-238.md)), repetition ([SOTA-171](SOTA-171.md)).
None answers **in what order**.

The distinction to hold, because the record's vocabulary invites collapsing
them:

- **Reweighting** changes how much of each domain, possibly over time. That is
  [SOTA-103](SOTA-103.md) and [SOTA-238](SOTA-238.md).
- **Ordering** changes what must come *before* what, because of a dependency
  between capabilities. That is this.
- **Staging** orders the objectives — pretrain, SFT, RL ([SOTA-129](SOTA-129.md), [SOTA-130](SOTA-130.md)).
  The record's existing uses of the word "curriculum" are all this third
  thing, and it is a different axis again.

## Conditions

`Proposed`, and the reason is scope rather than doubt. The evidence is in
continual-pretraining and fine-tuning regimes; nothing here demonstrates an
ordered skill set governing a pretraining run from scratch, which is where the
data-ordering question has the most money attached to it.

Identifying skills and their prerequisite structure is itself work, and the
framework defines a skill "in terms of the associated data" — so applying this
means committing to a decomposition of your corpus that you then have to
defend. That cost is real and the practice should not be read as free.
