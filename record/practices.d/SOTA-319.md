---
number: 319
status: Proposed
formerly:
- SOTA-tmpqevxe
promote_when: >-
  A comparison against the remedies that target the same failure — QK-norm
  (SOTA-192) or QK-clip (SOTA-131) — at a scale where the failure actually
  bites, reporting both stability and final quality. What would NOT meet it:
  another paper reporting that σReparam beats a plain baseline without those
  stabilizers. That is the result already held, and the open question is not
  whether spectral reparameterization helps but whether it is the instrument
  to reach for when two cheaper ones exist.
consensus: unreplicated
consensus_note: >-
  One group, five modalities inside the paper, and no adoption this record can
  find in a released model. The invariant it enforces is agreed and widely
  enforced — SOTA-192 is `converged` — but this particular instrument is not
  the one the field picked up, and the account behind it is disputed by
  LIT-521.
title: 'Reparameterize every linear layer by its spectral norm with a learned scalar'
version: 1
tags:
- model-stability
- training-optimization
date: '2026-09-22'
source:
- LIT-523
introduced_by:
- LIT-523
explained_by:
- THEORY-061
implementations:
- ml-sigma-reparam
summary: >-
  Zhai et al. (2023), [LIT-523](../literature.d/LIT-523.md) — replace each linear
  layer's `W` with `γ·W/σ(W)`, `γ` a learnable scalar initialized to 1 and
  `σ` the spectral norm from power iteration. A ViT-B trained this way reaches
  **82.2%** against a DeiT baseline's 81.8% with no pre-LN, no warmup, no
  weight decay and LARS in place of Adam. Spectral normalization without the
  scalar gets **69.81%**.
---
<!-- inactive-ok-file: THEORY-061 THEORY-062 — both Proposed, filed
     in this same contribution. This practice declares `explained_by:` on the
     first and the section citing both says the mechanism is disputed, which
     requires them to be unsettled rather than leaning on them. -->

<!-- inactive-ok-file: SOTA-320 — Proposed, filed in this same
     contribution and named as an untested sibling remedy. -->

<!-- inactive-ok-file: SOTA-122 SOTA-282 — both Proposed, named as the two
     practices this one overlaps without being either, in a paragraph that
     says nobody has compared the three. -->

# SOTA-319: Reparameterize every linear layer by its spectral norm with a learned scalar

## Source

Zhai, Likhomanenko, Littwin, Busbridge, Ramapuram, Zhang, Gu and Susskind
(2023), [LIT-523](../literature.d/LIT-523.md) — read as [NOTE-265](../notes.d/NOTE-265.md).

## Do this

Replace every linear layer's weight with

    Ŵ = γ · W / σ(W)

where `σ(W)` is the largest singular value and `γ` is a **learnable scalar
initialized to 1**. Compute `σ(W)` by power iteration on the parameters — two
matrix-vector products, no per-activation cost. At inference, evaluate `Ŵ`
once and freeze it; the layer then costs exactly what a linear layer costs.

**The learned scalar is not optional and is the whole method.** Removing it —
plain spectral normalization — drops ViT-B from 82.2% to **69.81%**. The point
is not to constrain the spectral norm to 1 but to make its *update rate*
independent of the matrix's dimensions, which plain normalization does not do
because it removes the degree of freedom entirely.

## What it buys

Not accuracy. Hyperparameters.

| ImageNet-1k, ViT-B | DeiT | σReparam |
|---|---|---|
| Top-1 | 81.8 | **82.2** |
| pre-LN | yes | **no** |
| LR warmup | yes | **no** |
| weight decay | yes | **no** |
| optimizer | Adam | **LARS** |

The same pattern holds across machine translation at 6 to 100 layers in
post-LN, speech recognition on LibriSpeech, image self-supervised learning and
language modelling. On ASR a well-tuned post-LN baseline still posts the best
single number (5.9 dev-clean WER against σReparam's 6.1–6.4); what σReparam
buys there is that the tuning stops mattering, across sweeps of learning rate,
warmup and initialization scale.

## Why `Proposed`

**The field picked different instruments for the same invariant.**
[SOTA-192](SOTA-192.md) (QK-norm) is `Active` and `converged`; [SOTA-131](SOTA-131.md)
(QK-clip) ships in the Kimi line. This acts on every linear layer rather than
on the query and key projections, and no one has compared it with either. A
practice whose closest competitors are both in production and never tested
against it is not something to recommend over them.

**The account behind it is disputed.** [THEORY-061](../theory.d/THEORY-061.md) holds
that low attention entropy is what breaks training.
[THEORY-062](../theory.d/THEORY-062.md) exhibits a stable network with near-zero
entropy. The remedy may work for a reason other than the one given, which does
not make it wrong and does mean the mechanism is not settled.

**Nothing at modern pretraining scale.** ViT-B/L/H and 100-layer MT models,
all from 2023.

## Conditions

**It changes the optimization geometry, not the model class.** Because `γ` is
free, the representable functions are unchanged; what changes is how the
optimizer moves through them. Do not expect it to act as a regularizer the way
constrained spectral normalization does.

**Power iteration is an approximation.** The main text does not state the
iteration count used. A neighbouring paper doing the same thing reports two
iterations as sufficient ([NOTE-266](../notes.d/NOTE-266.md)).

**One scalar per layer is a small but real parameter change**, and the
initialization at 1 matters — it makes the reparameterized layer match the
original at step zero, which is the same reasoning as [SOTA-051](SOTA-051.md)'s.

**It overlaps two practices the record already holds without being either.**
[SOTA-122](SOTA-122.md) learns per-row and per-column multipliers; [SOTA-282](SOTA-282.md) puts
matrices on the unit hypersphere with a learned per-dimension step. All three
strip a scale and learn it back, at three different granularities. Nobody has
compared them, and this record has not joined them.

## Known implementations

- `apple/ml-sigma-reparam`, the authors' release. No released model in this
  record is known to use it.
