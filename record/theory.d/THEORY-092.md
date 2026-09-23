---
number: 92
status: Proposed
formerly:
- THEORY-tmpghqdh
promote_when: >-
  The mechanism measured, not only the gain. For example, show that
  smoothing's benefit to a method grows with how much of that method's
  similarity signal comes from rare contexts, or that removing rare
  contexts outright recovers most of the gain. The source argues the
  mechanism and shows only that PPMI, the method most exposed to it, gains
  most.
title: 'Raising context counts to the 3/4 power helps word representations because PMI overweights rare contexts, and smoothing lowers their association scores'
version: 2
history:
- version: 2
  date: '2026-09-23'
  note: >-
    `extends` THEORY-tmpismnk, the factorization result it uses to equate
    negative sampling with smoothed PMI, filed after it.
tags:
- signal-structure
- representation-and-encoding
date: '2026-09-23'
source:
- LIT-607
extends:
- THEORY-tmpismnk
explains:
- SOTA-375
summary: >-
  Levy, Goldberg and Dagan (2015), [LIT-607](../literature.d/LIT-607.md) — PMI divides by the context's
  probability, so a rare context seen once with a word gets a high score and
  crowds out the informative ones. Raising context counts to α = 0.75 before
  normalizing raises rare contexts' probability and lowers their PMI. That
  is why word2vec's smoothed negative distribution helps, and why the same
  smoothing helps PPMI most (up to 9.2 points) and SGNS least (at most 1.4).
---

# THEORY-092: Raising context counts to the 3/4 power helps word representations because PMI overweights rare contexts, and smoothing lowers their association scores

## Source

Levy, Goldberg and Dagan (2015), [LIT-607](../literature.d/LIT-607.md), §2.1, §3.2 and §6.2, read as
[NOTE-329](../notes.d/NOTE-329.md).

## The account

PMI(w, c) = log P(w, c) / (P(w) P(c)). A context that is rare overall has a
tiny P(c), so a single co-occurrence gives it a high score. In a Zipfian
vocabulary, the top-scoring contexts of a word are then often rare words that
appear with it by chance and not with its neighbours. This is PMI's known
weakness: it overweights infrequent events.

Smoothing replaces P(c) with count(c)^α / Σ count^α, for α < 1. Rare
contexts gain probability relative to frequent ones, so their PMI falls. In
SGNS the same exponent sets the distribution negatives are drawn from. Since
SGNS implicitly factorizes shifted PMI ([THEORY-tmpismnk](THEORY-tmpismnk.md)), drawing negatives from count^0.75 is
the same smoothing applied inside the objective.

## What it explains

- **Why the 3/4 exponent helps word2vec**, a result its source asserted
  without numbers ([SOTA-375](../practices.d/SOTA-375.md)).
- **Why smoothing helps PPMI most** (up to +9.2 on MSR analogies) and SGNS
  least (0 to +1.4). SGNS's sigmoid and frequency-weighted loss already damp
  extreme and rare cells, so it has less left to fix.
- **Why wide windows hurt PPMI and SVD.** More random co-occurrences with
  rare words enter the vector with high PMI (footnote 10).

## Where it is weak

- **Argued, not measured.** Nothing isolates rare contexts to show they are
  what smoothing fixes. The evidence is the pattern of gains across methods.
- **One alternative exponent.** Only α = 1 and 0.75 are compared, so the
  account explains why smoothing helps, not why 3/4 in particular.
- **GloVe cannot be tested.** Its learned biases absorb this kind of
  correction by construction.

## Relation to other accounts

[THEORY-089](THEORY-089.md) says word vectors behave linearly because they fit log
co-occurrence statistics. This account is about which of those statistics
are noise: the rare-context cells that PMI inflates. The two are compatible
and neither depends on the other.

<!-- inactive-ok-file: SOTA-375, THEORY-089 — Proposed; the practice this account explains and a neighbouring account -->
