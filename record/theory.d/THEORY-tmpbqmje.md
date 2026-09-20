---
status: Proposed
promote_when: >-
  The lattice recovered for concepts nobody curated — clustered from a model's
  own embeddings rather than taken from an ontology built to have hierarchical
  structure. That is the severe test and it is cheap. Or the construction used
  to steer: building a compound concept's direction by meet or join and showing
  the intervention behaves as the geometry predicts. What would not settle it:
  another curated hierarchy recovered, which is the same friendly test again.
title: 'Concepts sit in embedding space as intersections of half-spaces, so inclusion, intersection and union are geometric operations'
version: 1
tags:
- representation-and-encoding
date: '2026-09-20'
source:
- LIT-tmpnglrb
explains: []
summary: >-
  Xiong (2026), [LIT-tmpnglrb](../literature.d/LIT-tmpnglrb.md) — a linear attribute direction plus a
  separating threshold is a half-space, a concept is the intersection of its
  attributes' half-spaces, and the resulting regions form a complete lattice.
  Conceptual refinement is geometric meet, generalisation is join. Evidence is
  WordNet, which is a hand-built hierarchy and so the friendliest test there is.
---

# THEORY-tmpbqmje: Concepts sit in embedding space as intersections of half-spaces, so inclusion, intersection and union are geometric operations
<!-- inactive-ok-file: THEORY-tmpwwu1v — Proposed, and filed in this same contribution; named as standing on the same absent trunk -->

## Source

Xiong (2026), [LIT-tmpnglrb](../literature.d/LIT-tmpnglrb.md) — [ARXIV-2603.01227](https://arxiv.org/abs/2603.01227).

## What was actually shown

The construction is short enough to state completely.

The Linear Representation Hypothesis says an attribute is a direction in
embedding space. Add a **separating threshold** and the attribute becomes a
**half-space**. A concept defined by several attributes is then the
**intersection** of their half-spaces — a region rather than a vector.

Regions order by inclusion, and the resulting partial order is a complete
lattice: any two concepts have a greatest lower bound (**meet**) and a least
upper bound (**join**). Meet is intersection of the half-spaces — conceptual
refinement. Join is approximated by the conic hull of the combined attribute
directions — conceptual generalisation. A canonical form exists when the
attribute directions are linearly independent, and soft versions using fuzzy
projection profiles handle embeddings that do not sit cleanly on one side of
a threshold.

The empirical part: on WordNet sub-hierarchies, LLM embeddings are reported
to encode these lattices and their logical structure.

**The threshold is the whole move.** A direction gives a scalar; a direction
with a threshold gives a region; regions compose and scalars do not. That is
why this says something the Linear Representation Hypothesis does not.

## What this does not say

**The evidence is the friendliest test available.** WordNet is a hand-built
ontology with exactly the clean hierarchical structure the hypothesis
predicts. Recovering a lattice from concepts somebody constructed as a
lattice is weak evidence that the lattice is in the embeddings rather than in
the choice of concepts. The severe test — cluster a model's own
representations and look for the structure where nobody put it — is cheap and
is not run.

**It assumes the Linear Representation Hypothesis** and does not re-establish
it. Everything here is downstream of a premise with its own live disputes,
which this record holds no document for at all.

**Thresholds are assumed to exist and separate.** The soft version concedes
they do not, and the softening is a definitional choice rather than something
derived.

**Join is an approximation.** The conic hull is the least subsuming region
*under that construction*, not the least subsuming region.

**Nothing downstream is demonstrated.** The structure is shown, not used. The
obvious application — constructing a steering vector for a compound concept
by meet or join rather than searching for one — is available and untried, and
until somebody runs it this is a description of a geometry rather than a
capability.

**And linear independence is a condition on the concepts, not the space.**
The canonical form holds for sets of attributes that happen to be
independent; it says nothing about arbitrary concept collections.

## Why `explains:` is empty

It underwrites no practice in this record and should not pretend to. The
paper establishes a structure on a curated ontology; no recommendation about
training, serving or evaluating follows from it yet. A finding that
underwrites nothing *yet* is still a finding, and saying which is the honest
version.

## The trunk underneath

Both this and [THEORY-tmpwwu1v](THEORY-tmpwwu1v.md), filed in the same contribution, stand on the
**Linear Representation Hypothesis** — and the record holds no document for
it, nor for steering vectors, nor for concept directions generally. Filing
two elaborations of an absent foundation is backwards.

It is named here rather than quietly filled because closing it properly is a
unit of its own: the hypothesis has a literature, a causal-inner-product
formulation, and active disputes, and a single note asserting "concepts are
directions" would be the kind of thin filing this record exists to avoid.
