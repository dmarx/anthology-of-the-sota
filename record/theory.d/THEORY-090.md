---
number: 90
status: Proposed
formerly:
- THEORY-tmpsbx36
promote_when: >-
  The unification shown to hold where probing and steering are done, in
  intermediate layers, and not only at the output: steering vectors built
  from word-pair directions through the whitened map matching or beating
  vectors fitted from activations, on more than one model family, measured
  against a null rather than read off a heatmap. LIT-526's null on
  cross-lingual transport is the one test so far and it went the other way.
  The theorems are not in question; whether real models satisfy their
  premises is.
title: 'A concept''s shared word-pair direction, its linear probe and its steering vector are one object, related by an inner product under which causally separable concepts are orthogonal'
version: 1
tags:
- concept-geometry
- analysis-and-evaluation
date: '2026-09-23'
source:
- LIT-606
explains:
- SOTA-378
summary: >-
  Park, Choe and Veitch (2024), [LIT-606](../literature.d/LIT-606.md) — the output-space direction
  that counterfactual word pairs share is provably a logit-linear probe, and
  the input-space direction is provably a steering vector that leaves
  separable concepts alone. Training fixes neither space's inner product, so
  cosine similarity is arbitrary. The inner product that makes separable
  concepts orthogonal maps one direction onto the other, and one member of
  that family is the inverse unembedding covariance. Proved under stated
  assumptions and shown on LLaMA-2 7B.
extended_by:
- THEORY-034
---

# THEORY-090: A concept's shared word-pair direction, its linear probe and its steering vector are one object, related by an inner product under which causally separable concepts are orthogonal

## Source

Park, Choe and Veitch (2024), [LIT-606](../literature.d/LIT-606.md), read as [NOTE-328](../notes.d/NOTE-328.md).

## The account

"Concepts are linear" is used in three senses. **Subspace**: the differences
between word pairs that change only one concept (king/queen, man/woman) lie
along one direction. **Measurement**: a linear probe reads the concept off
the representation. **Intervention**: adding a vector changes the concept
and nothing else.

In the unembedding space, the subspace direction *is* a probe: the log-odds
of queen over king is linear in the context representation, with that
direction as coefficient. In the embedding space, the subspace direction
*is* a steering vector: adding it raises the target concept's probability and
leaves every concept that can vary independently of it unchanged.

What joins the two spaces is an inner product, and training does not supply
one. Any invertible linear map on unembeddings, with its inverse transpose on
embeddings, leaves every prediction unchanged. So "these two concepts have
cosine 0.1" is a fact about a coordinate system, not about the model. The
account picks the inner products under which causally separable concepts are
orthogonal. Under any of them, a concept's unembedding direction maps to its
embedding direction, which makes the probe and the steering vector the same
vector. If separable concepts are uncorrelated over words drawn uniformly
from the vocabulary, the inverse covariance of the unembedding rows is one
such product.

## What it explains

- Why probes and steering vectors for the same concept keep turning out
  related. They are one object seen from two spaces.
- Why cosine similarity between concept directions varies between models
  that behave alike. It is not identified, and on Gemma-2B (tied embeddings)
  it fails where the whitened product works.
- Why a fitted probe can be less clean than the pair direction. The probe
  absorbs correlated off-target concepts, and the pair direction does not.

## Where it is weak

- **The premises are idealizations.** Exact cones of differences, concepts
  read deterministically off one output token, and d − 1 separable concepts
  completing a basis. Real directions are approximate, and one of 27 tested
  concepts (thing⇒part) has none.
- **Covariance is one member of a family.** D = I is chosen, not derived.
- **The evidence stops at the output.** Intermediate-layer steering and
  probing, where the practice lives, is future work in the source. [LIT-526](../literature.d/LIT-526.md)
  tested the whitened product for cross-lingual concept transport across 17
  models and found no benefit over spectral regularization (p = 0.95).
- **Orthogonality is read off heatmaps** of 27 concepts on two models.

## Relation to other accounts

[THEORY-034](THEORY-034.md) builds on this: it adds a threshold to each direction and reads
concepts as intersections of half-spaces. [THEORY-063](THEORY-063.md) locates contextual
concept directions in the low-variance tail of the same unembedding
covariance this account whitens by. It does not say whether whitening is
right, and its source's null is against one use of it. [THEORY-089](THEORY-089.md) says why
word vectors trained on co-occurrence have linear offsets at all. This
account says what an offset means once it exists, and needs no mechanism for
it.

<!-- inactive-ok-file: THEORY-034, THEORY-063, THEORY-089 — Proposed, named to place this account among its neighbours, not cited as established -->
