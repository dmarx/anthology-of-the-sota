---
status: Read
paper: LIT-tmpnglrb
title: 'The Lattice Representation Hypothesis'
version: 1
date: '2026-09-20'
summary: >-
  A linear concept direction plus a threshold is a half-space; intersecting
  half-spaces gives a concept lattice, so inclusion, intersection and union
  become geometric meet and join on embeddings. Canonical form when the
  attribute directions are linearly independent. Evidence is WordNet
  sub-hierarchies, which is the friendliest available test.
---

# NOTE-tmpv05j0: The Lattice Representation Hypothesis

## Contribution

Supplies the compositional layer the Linear Representation Hypothesis lacks.
That hypothesis says a concept is a direction, which accounts for binary
features and for steering, and says nothing about how concepts relate to each
other — inclusion, intersection, union, the structure that makes conceptual
knowledge a hierarchy. This paper adds a threshold to each direction, which
turns a concept into a half-space, and observes that the intersection lattice
of half-spaces is exactly the structure Formal Concept Analysis studies. Meet
and join then become operations one can perform on embeddings.

## Key insight

**A threshold is the whole difference between a feature and a concept.** A
direction alone gives you a scalar per datapoint — more or less of some
attribute. Add a separating threshold and you have a *region*, and regions
compose: intersect two and you get the concept satisfying both attributes;
take the smallest region containing two and you get their generalisation. The
algebra of concepts that symbolic AI built explicitly turns out to be
available for free in a continuous embedding space, provided you are willing
to say where each attribute stops.

## Assumptions

- **The Linear Representation Hypothesis holds** — attributes are linear
  directions in embedding space. Everything is downstream of that and none of
  it is re-established here.
- **Each attribute admits a separating threshold**, which is what converts a
  direction into a half-space. Real embeddings do not separate cleanly, which
  is why soft versions are defined.
- **The canonical form requires linearly independent attribute directions** —
  a condition on the set of concepts chosen, not a property of the space.
- **Join is approximated by the conic hull** of the two concepts' attribute
  directions rather than computed exactly; it is the least region subsuming
  both only under that approximation.
- **WordNet sub-hierarchies** supply both the concepts and the ground-truth
  structure.

## Key results

- **Half-space construction**: a linear attribute direction with a separating
  threshold defines a concept region; a concept over several attributes is
  the intersection of their half-spaces.
- **The regions form a complete lattice** under inclusion — every pair has a
  greatest lower bound (meet) and a least upper bound (join).
- **Meet is intersection of half-spaces; join is the conic hull** spanned by
  the union of the two concepts' attribute directions.
- **A canonical form exists** when attribute directions are linearly
  independent.
- **Soft meet and join**, via fuzzy projection profiles, giving a degree to
  which a point is subsumed rather than a boolean.
- **WordNet evidence**: LLM embeddings are reported to encode the concept
  lattices and their logical structure, supporting coherent generalisation
  (join) and refinement (meet).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Linear directions with thresholds induce a concept lattice via half-space intersection | strong | a construction; it follows once the premises are granted |
| C2 | LLM embeddings actually encode such lattices | moderate | WordNet sub-hierarchies, which are hand-built to have this structure |
| C3 | Meet and join on embeddings correspond to conceptual refinement and generalisation | moderate | demonstrated on the same curated hierarchies |
| C4 | A canonical form exists under linear independence | strong | proved, under a stated condition |

## Method

Take the Linear Representation Hypothesis as given. Attach a separating
threshold to each attribute direction, making each attribute a half-space,
and define a concept as the intersection of the half-spaces of its
attributes.

Import Formal Concept Analysis's apparatus: objects, attributes, the
extent/intent duality, and the partial order by inclusion that makes the set
of formal concepts a complete lattice. Show the geometric construction
realises it.

Define meet as region intersection and join as the conic hull of the combined
attribute directions, then soften both with fuzzy projection profiles so they
apply to embeddings that do not sit cleanly on one side of a threshold.

Evaluate on WordNet sub-hierarchies: check whether LLM embeddings place
concepts so that the geometric meet and join recover the ontology's
refinement and generalisation relations.

## Concepts

- **Linear Representation Hypothesis** — semantic features and concepts are
  encoded as linear directions or subspaces. The premise, not held anywhere
  in this record.
- **Formal Concept Analysis** — the lattice theory of objects and attributes,
  with extent (objects having the attributes) and intent (attributes shared
  by the objects) as duals.
- **Half-space model** — a concept as the intersection of the half-spaces
  defined by its attribute directions and thresholds.
- **Meet / join** — greatest lower bound and least upper bound in the
  lattice; here, intersection and conic hull.

## Connections

Builds on the Linear Representation Hypothesis line, including the causal
inner product formulation under which causally separable concepts are
orthogonal — which is what makes the independence condition for the canonical
form more than a convenience.

Imports Formal Concept Analysis wholesale, which is an old and well-developed
symbolic framework, and the contribution is the bridge rather than either
side.

Sits adjacent to the steering literature: if concepts are regions and regions
compose, then a steering vector for a compound concept should be
constructible rather than found. The paper does not take that step.

## Recommendations

- **R1** — When reasoning about compound concepts in embedding space, treat
  them as intersections of half-spaces rather than as sums of directions.
  *Topic:* interpretability. *Status:* experimental. *Strength:* moderate.
  *Applies when:* the attributes have thresholds that separate.
- **R2** — Expect generalisation over concepts to need a conic hull rather
  than an average of directions. *Topic:* interpretability. *Status:*
  experimental. *Strength:* weak. *Applies when:* as above; the hull is
  itself an approximation here.

## Bearing on the record

- **Should produce a theory** and **no practice**. The paper establishes a
  structure and demonstrates it on a curated ontology; nothing here says what
  to do differently when training or serving. The obvious candidate — build
  steering vectors by meet and join — is not evaluated as an intervention.
- **Names the same absent trunk as [LIT-tmpglvdv](../literature.d/LIT-tmpglvdv.md).** The Linear
  Representation Hypothesis is this paper's premise and the record holds no
  document for it, nor for steering vectors, nor for concept geometry.
  Filing the elaboration before the thing elaborated is backwards and should
  be said so in writing.
- **First document in the record on concept geometry**, in a topic whose
  fourteen existing notes are all tokenisation and positional encoding.

## Limitations

- **WordNet is the friendliest possible test.** It is a hand-built ontology
  with exactly the clean hierarchical structure the hypothesis predicts.
  Whether the lattice holds for concepts nobody curated is the question and
  is not asked.
- Everything rests on the Linear Representation Hypothesis, which is assumed
  rather than tested, and which has its own live disputes.
- Thresholds are assumed to exist and separate; the soft version acknowledges
  they do not, and the softening is a definitional choice rather than a
  derived one.
- Join is an approximation. The conic hull is the least region under a
  construction, not the least region.
- No downstream task. The structure is demonstrated, not used.

## Open questions

- Does the lattice appear for concepts a model learned and no ontology names?
  That is the severe test and it is available — cluster embeddings, look for
  lattice structure, check nothing curated it.
- Can meets and joins be used to steer? The construction is there and the
  intervention is not run.
- How do the thresholds behave across models? If they are model-specific the
  geometry is a per-model fact; if they transfer it is a stronger claim than
  the paper makes.
