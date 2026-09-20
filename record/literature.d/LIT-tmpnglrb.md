---
status: Active
title: 'The Lattice Representation Hypothesis of Large Language Models'
version: 1
tags:
- representation-and-encoding
date: '2026-09-20'
published: '2026-03-01'
arxiv: '2603.01227'
first_author: 'Xiong'
keywords:
- 'linear-representation-hypothesis'
- 'formal-concept-analysis'
- 'concept-lattice'
- 'embedding-geometry'
- 'steering'
implementations: []
summary: >-
  Xiong (2026), [ARXIV-2603.01227](https://arxiv.org/abs/2603.01227). If concepts are linear directions
  with thresholds, each concept is a half-space, and intersecting half-spaces
  gives a concept lattice — so conceptual inclusion, intersection and union
  become geometric meet and join. Tested on WordNet sub-hierarchies. The
  Linear Representation Hypothesis gives binary concepts; this is the
  set-theoretic structure over them.
---

# LIT-tmpnglrb: The Lattice Representation Hypothesis of Large Language Models
<!-- inactive-ok-file: THEORY-tmpbqmje — Proposed, and filed in this same contribution from this note -->

## Key takeaways

- **The gap it is filling is compositional, not existential.** The Linear
  Representation Hypothesis establishes that a concept is a direction. What
  it does not give is *inclusion, intersection and union* — the set-theoretic
  relations that make conceptual knowledge a hierarchy rather than a bag of
  features.
- **The construction is one step.** A linear attribute direction plus a
  separating threshold is a **half-space**. A concept defined by several
  attributes is the intersection of their half-spaces. Order those regions by
  inclusion and you have a lattice, with a well-defined greatest lower bound
  (**meet**) and least upper bound (**join**) for any pair.
- **Meet is intersection; join is the conic hull** of the two concepts'
  attribute directions — the smallest region covering both. Both are
  operations on embeddings, not on symbols.
- **A canonical form exists** when the attribute directions are linearly
  independent.
- **Soft versions are defined**, with fuzzy projection profiles, because
  real embeddings do not sit cleanly on one side of a threshold.
- **Evidence is WordNet sub-hierarchies**: LLM embeddings are reported to
  encode concept lattices and their logical structure, supporting
  generalisation (join) and refinement (meet).

## Standing in the anthology

**It formalises a bridge the record has no documents on either side of.** The
`representation-and-encoding` topic holds fourteen notes, all about
tokenisation and positional encoding. Nothing on concept geometry, nothing on
the Linear Representation Hypothesis this paper unifies with Formal Concept
Analysis, nothing on steering.

[THEORY-tmpbqmje](../theory.d/THEORY-tmpbqmje.md) records the account. **No practice is filed from it**, and
that is deliberate: the paper establishes a structure and demonstrates it on
a curated ontology, and nothing here says what to do differently when
training or serving a model. The obvious candidate — steer by constructing
meets and joins of attribute directions — is not evaluated as an
intervention, only as a geometry.

**The missing antecedent is the interesting part.** This paper's whole
premise is the Linear Representation Hypothesis, which the record does not
hold. Filing the elaboration before the thing elaborated is backwards, and
[LIT-tmpglvdv](LIT-tmpglvdv.md), filed in the same contribution, stands on the same absent
foundation. Two arriving papers pointing at one gap is how the record has
been finding trunks all week; this one is named in the curation entry rather
than closed, because closing it is a unit of its own.

## What it does not establish

WordNet is a hand-built ontology with exactly the clean hierarchical
structure the hypothesis predicts, which makes it the friendliest possible
test and not a severe one. Whether the lattice structure holds for concepts
nobody curated — the ones a model learns and no taxonomy names — is the
question, and it is not asked here.

The canonical form requires linearly independent attribute directions, which
is a condition on the concepts chosen rather than a property of the
embedding space.
