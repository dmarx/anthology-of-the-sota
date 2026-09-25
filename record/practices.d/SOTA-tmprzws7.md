---
status: Proposed
consensus: unassessed
consensus_note: >-
  Training students on teacher outputs is everywhere, but temperature, the
  T² factor and the loss weighting vary from user to user, and this record has
  not surveyed what current recipes set. That is adoption in any case, not
  evidence (DP-005). The recipe as written has one source, a workshop paper
  with one run per cell. Read as of 2026-09.
promote_when: >-
  A controlled comparison, by any group, of soft-target distillation across
  temperatures and with and without the T² factor at a matched student size,
  on a task other than MNIST. Another model shipping a distilled student would
  not settle it. Neither would a sequence-level distillation result, which is
  a different method.
title: "When distilling a classifier, match the teacher's temperature-softened outputs at the same temperature and keep a down-weighted hard-label term"
version: 1
tags:
- inference-optimization
- training-optimization
date: '2026-09-25'
source:
- LIT-tmpa3ip4
introduced_by:
- LIT-tmpa3ip4
implementations: []
summary: >-
  Hinton et al. (2015), [LIT-tmpa3ip4](../literature.d/LIT-tmpa3ip4.md). Soft-target cross-entropy at temperature `T`
  in both teacher and student, plus a hard-label cross-entropy at `T = 1` with
  a considerably lower weight. Multiply the soft term by `T²`, so the balance
  does not move when `T` changes. Start low for a small student. The paper's
  best realistic setting was `T = 2`, and a 30-unit MNIST net wanted 2.5–4.
explained_by:
- THEORY-tmpm6tyr
---

# SOTA-tmprzws7: When distilling a classifier, match the teacher's temperature-softened outputs at the same temperature and keep a down-weighted hard-label term

## Source

Hinton, Vinyals and Dean (2015), [LIT-tmpa3ip4](../literature.d/LIT-tmpa3ip4.md).

## What to do

- **Loss:** `T² · CE(softmax(v/T), softmax(z/T)) + λ · CE(y, softmax(z))`,
  with teacher logits `v`, student logits `z`, and `λ` well below the soft
  term's weight. The paper's speech run used "a relative weight of 0.5".
- **Temperature:** the same `T` in teacher and student during training, and
  `T = 1` at inference. Search `T`. Do not import `T = 20` from MNIST.
- **`T²`:** keep it. It holds the relative size of the two terms fixed as `T`
  changes, so a temperature sweep is not also a loss-weight sweep.

## Why

The soft term's gradients scale as `1/T²`. Without the factor, raising `T`
silently shrinks the soft term relative to the hard one. That is the whole
argument for `T²`. It is a derivation about keeping hyperparameter searches
comparable, not a measured gain in accuracy.

Low `T` ignores the teacher's very negative logits, and high `T` approaches
logit regression. Which is better depends on the student. A student with
capacity to spare (300 or more units on MNIST) was indifferent to anything
above 8. A starved one (30 units) needed 2.5–4.

## Conditions

- **Classification-style outputs, from 2015.** The evidence is a 2-layer MNIST
  net and one production acoustic model, one run each. Nothing here covers
  sequence-level generation. The record's language-model distillation
  evidence ([LIT-441](../literature.d/LIT-441.md)) uses sequence-level distillation, a
  different method.
- **None of the three instructions is ablated in the source.** `T²` is
  derived, the down-weighting is "we found", and the temperature evidence is
  one sweep on speech plus a sentence about MNIST. That is why this is
  `Proposed` despite its age.
- **Compression size.** Big-to-small was shown only on MNIST. The speech
  result compresses an ensemble into one member-sized model.

## Known implementations

- None recorded. The recipe is a standard component of many libraries, which
  is adoption and is not listed as evidence.
