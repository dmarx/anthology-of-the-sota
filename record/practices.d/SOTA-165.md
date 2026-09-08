---
status: Active
formerly:
- SOTA-tmpncfhm
consensus: emerging
consensus_note: >-
  The controlled comparison (LIT-156) tunes ten optimizers per-optimizer
  across four scales and finds every fastest one is matrix-preconditioned —
  which is a finding about the class from one group, corroborated by two
  frontier labs shipping a member of it (Kimi K3 and DeepSeek-V4, both on
  Muon). Not `converged`: the same paper reports the advantage shrinking
  with scale, and most released models still train on AdamW.
title: 'Precondition the gradient with matrices rather than entrywise scaling'
version: 1
tags:
- training-optimization
date: '2026-09-08'
published: '2025-09-01'
source:
# LIT-156 is the fair comparison that isolates the class. LIT-157 is the
# equivalence result that says why the class is the right unit — Shampoo at
# the 1/2 power *is* Adafactor in a rotated basis. LIT-158 is where the
# overhead budget was shown to be affordable, which is the condition the
# recommendation stands or falls on.
- LIT-156
- LIT-157
- LIT-158
extended_by:
- SOTA-121
implementations: []
summary: >-
  Wen et al. (2025), [LIT-156](../literature.d/LIT-156.md) — under per-optimizer tuning across ten
  optimizers and four scales, every fastest one multiplies gradients by
  matrices rather than scaling entrywise. A structural finding that survives
  a fair comparison, and the class the record's Muon practice is one member
  of. The advantage is 1.4× at 0.1B and 1.1× at 1.2B.
---

# SOTA-165: Precondition the gradient with matrices rather than entrywise scaling

## Source

Wen et al. (2025), [LIT-156](../literature.d/LIT-156.md) — [ARXIV-2509.02046](https://arxiv.org/abs/2509.02046), for the comparison;
Vyas et al. (2024), [LIT-157](../literature.d/LIT-157.md), for the equivalence that says why the class is
the right unit; Shi et al. (2023), [LIT-158](../literature.d/LIT-158.md), for the overhead budget.

AdamW scales each coordinate of the gradient by its own running statistic.
The alternative is to multiply the gradient by a *matrix* — a preconditioner
that mixes coordinates. Muon does it by orthogonalising a momentum matrix;
Shampoo and SOAP do it by approximating a second-moment matrix and inverting
it. The claim of this practice is that the family membership is what buys the
speed-up, not the particular route into it.

## Why the class and not the algorithm

Alternative optimizers had been reported at 1.4–2× AdamW for years without
adoption following. [LIT-156](../literature.d/LIT-156.md)'s thesis is that two faults explain the gap:
unequal hyperparameter tuning between challenger and baseline, and evaluation
too narrow or too early. It fixes both — ten optimizers, four scales
(0.1B–1.2B), data-to-model ratios from 1× to 8× Chinchilla, each **tuned
rather than handed the baseline's hyperparameters** — and reports two things
that matter here:

- **Optimal hyperparameters do not transfer between optimizers**, so blind
  transfer is the ordinary way a comparison becomes unfair.
- **Rankings flip mid-run**, so judgement belongs at the end of training.

After correcting for both, the fastest optimizers are the matrix-preconditioned
ones — Muon and SOAP among them. That is the positive result, and it is the
one that survives.

[LIT-157](../literature.d/LIT-157.md) supplies the reason the class is a real object rather than a
grouping: Shampoo implemented with the 1/2 power **is** Adafactor run in the
eigenbasis of Shampoo's preconditioner. A formal equivalence, not an analogy
— which makes "the useful part is the basis" a statement about mechanism.

## Conditions, and the one that is a trend

**The advantage shrinks with scale.** [LIT-156](../literature.d/LIT-156.md) measures it as inversely
proportional to model size: 1.4× over AdamW at 0.1B, 1.1× at 1.2B. Extending
that trend to "no advantage at the frontier" is the reader's inference and
not the paper's claim — 1.2B is small next to everything the record's recent
half describes, and the frontier adopters train far above it. But a reader
choosing an optimizer at 1B should expect 1.1×, not 2×.

**The overhead has to be paid, and it is affordable.** A matrix
preconditioner costs memory and compute per step. [LIT-158](../literature.d/LIT-158.md) is where that was
shown to be survivable at scale: distributing each parameter's preconditioner
blocks across ranks via DTensor, with an AllGather on the computed search
directions, brings it to **at most a 10% per-step wall-clock penalty** against
diagonal adaptive methods. A preconditioner replicated on every rank instead
of sharded is a different and worse proposition.

## Members

- [SOTA-121](SOTA-121.md) — Muon, the branch the record recommends on production evidence
  at trillion-parameter scale, and the one carrying its own correction
  ([SOTA-131](SOTA-131.md), QK-Clip).
- SOAP, filed separately and `Proposed`: the same family reached from the
  other direction, with a formal derivation and no production deployment.

Filing the trunk is what lets those two be siblings rather than rivals. They
are not competing claims about which algorithm wins; they are two routes into
the class this practice is about.

## Known implementations

- Muon: Kimi K3, DeepSeek-V4, Falcon-H1-Tiny.
- Distributed Shampoo: Meta's PyTorch implementation, validated on ImageNet
  ResNet-50.
- Against, by silence: most released models still train on AdamW.
