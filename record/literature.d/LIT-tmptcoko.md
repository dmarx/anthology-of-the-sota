---
status: Active
# arXiv v1 (2025-03-11) was titled "Neural Network/de Sitter Space
# Correspondence"; v3 (2025-07-31), the version read, renamed it. The title
# here is the current one, which is what the id resolves to.
title: 'Synaptic Field Theory for Neural Networks'
version: 1
tags:
- analysis-and-evaluation
- training-optimization
date: '2026-10-01'
published: '2025-03-11'
arxiv: '2503.08827'
first_author: 'Lee'
keywords:
- 'synaptic-field-theory'
- 'field-theory'
- 'de-sitter-space'
- 'continuum-limit'
- 'gradient-descent-dynamics'
- 'momentum'
summary: >-
  Lee, Lee and Yi (2025), ARXIV-2503.08827 — a hep-th proposal with no
  experiments. Gradient descent with momentum, `Ẅ + γẆ + ∂C/∂W = 0`, follows
  from an action weighted by `e^{γt}`, the volume factor of de Sitter space
  with Hubble rate `H = γ/d`. Treat the weight indices as spatial coordinates
  and take the continuum limit, and training becomes a field theory with the
  data as external sources. Only toy networks give a local one: periodic,
  nearest-neighbour wiring with linear or quadratic activations.
---

# LIT-tmptcoko: Synaptic Field Theory for Neural Networks

Lee, Lee and Yi (2025) — ARXIV-2503.08827 (hep-th). First posted as "Neural
Network/de Sitter Space Correspondence".

## Key takeaways

- **The construction.** Plain gradient flow `Ẇ = −η ∂C/∂W` has no action.
  The paper treats it as the high-friction limit of the momentum equation
  `Ẅ + γẆ + ∂C/∂W = 0`, which follows from `S = ∫dt e^{γt} [½Ẇ² − C]`.
  Reading `e^{γt}` as `√−g` in `d+1` dimensions identifies a constant Hubble
  rate `H = γ/d`, i.e. de Sitter space. The weights' indices (neuron,
  synapse, layer) become spatial coordinates `x` and the weights a field
  `w(t, x)`. Expanding the cost as a series in the weights, the coefficients
  that depend on the training data act as external sources (Table 1 gives the
  dictionary).
- **For ordinary architectures the result is non-local**, and the authors say
  so. The quadratic and higher terms couple every pair of index positions.
  Their conclusion is that the indexing convention and the architecture fix
  the geometry of the field theory, and that "it is unclear whether typical
  architectures and indexing conventions yield geometries that are useful for
  analysis".
- **Two toy networks give local theories.** A one-layer perceptron with
  linear activation, each output wired to its two neighbouring inputs and
  periodic boundaries, gives a free scalar field with data-dependent stiffness
  `K(x)` and mass-like term `J(x)`. A two-layer version with quadratic
  activation gives two coupled fields, one per layer, with couplings listed
  to second order in the fields and in derivatives. In it only the last
  layer's field acquires a mass. The mass comes from the activation's
  constant term, which only those weights couple to.
- **What is not there.** No experiment and no prediction about a trained
  network are checked. The continuum limit is heuristic: the lattice spacing
  is absorbed into the sources. The NTK-based duality of Krippendorf and
  Spannowsky (2022), which reached a de Sitter correspondence for the
  network's *outputs*, is acknowledged as prior work in v3.

## Standing in the anthology

The record's nearest neighbour is THEORY-009. It also replaces a network's
weights with a continuum, but there the continuum is the empirical
distribution of a wide two-layer network's neurons, following a gradient
flow (LIT-271 among its sources). That replacement buys a theorem: the risk
is convex in the distribution. This paper's continuum is over weight indices
and buys no consequence yet. It is a dictionary, offered as a way into
field-theoretic tools.

It also argues against relying on a constant tangent kernel. The paper's
reason for working at the level of parameters is that the empirical NTK is
constant "only in restricted cases". THEORY-070 and THEORY-076 make the same
point in their own terms, where the interesting dynamics are those that leave
the kernel regime. The paper does not test that.

Nothing in the record depends on it, and it does not inform a practice. It
is filed as a seed for the analysis-and-evaluation shelf on training
dynamics, and as a pointer to the physics-of-learning literature the record
otherwise reaches only through LIT-694.

Unread — no NOTE.
