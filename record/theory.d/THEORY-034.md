---
number: 34
status: Proposed
formerly:
- THEORY-tmpbqmje
promote_when: >-
  The lattice recovered for concepts nobody curated — clustered from a model's
  own embeddings rather than taken from an ontology built to have hierarchical
  structure. That is the severe test and it is cheap. Or the construction used
  to steer: building a compound concept's direction by meet or join and showing
  the intervention behaves as the geometry predicts. What would not settle it:
  another curated hierarchy recovered, which is the same friendly test again.
title: 'Concepts sit in embedding space as intersections of half-spaces, so inclusion, intersection and union are geometric operations'
version: 2
history:
- version: 2
  date: '2026-09-23'
  note: >-
    The Linear Representation Hypothesis it stands on is filed as
    THEORY-090, which this extends. The trunk section is rewritten to
    say so. The account is unchanged.
tags:
- concept-geometry
- representation-and-encoding
date: '2026-09-20'
source:
- LIT-460
explains: []
extends:
- THEORY-090
summary: >-
  Xiong (2026), [LIT-460](../literature.d/LIT-460.md) — a linear attribute direction plus a
  separating threshold is a half-space, a concept is the intersection of its
  attributes' half-spaces, and the resulting regions form a complete lattice.
  Conceptual refinement is geometric meet, generalisation is join. Evidence is
  WordNet, which is a hand-built hierarchy and so the friendliest test there is.
---

# THEORY-034: Concepts sit in embedding space as intersections of half-spaces, so inclusion, intersection and union are geometric operations
<!-- inactive-ok-file: THEORY-036 — Proposed, and filed in this same contribution; named as standing on the same absent trunk -->

## Source

Xiong (2026), [LIT-460](../literature.d/LIT-460.md) — [ARXIV-2603.01227](https://arxiv.org/abs/2603.01227).

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
it. Everything here is downstream of that premise, which the record now
holds as [THEORY-090](THEORY-090.md). That account's own evidence stops at the output
space, and [LIT-526](../literature.d/LIT-526.md)'s null is against one of its uses.

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

Both this and [THEORY-036](THEORY-036.md), filed in the same contribution, stand on the
**Linear Representation Hypothesis**. When they were filed the record held no
document for it and said so here. It now holds Park, Choe and Veitch
([LIT-606](../literature.d/LIT-606.md)) and their account ([THEORY-090](THEORY-090.md)), which this one
`extends`: that account makes an attribute a direction, and this one adds the
threshold. The lattice paper builds on that account's causal inner product
([NOTE-210](../notes.d/NOTE-210.md)), under which separable attributes are orthogonal. That is what
makes the canonical form's linear-independence condition more than a
convenience. The two accounts share their weak point: neither is tested
beyond curated concepts.

<!-- inactive-ok-file: THEORY-090 — Proposed, named as the antecedent account this document had said was missing -->
