---
status: 'Active'
title: 'On-line learning in soft committee machines'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
published: '1995-10-01'
doi: '10.1103/PhysRevE.52.4225'
first_author: 'Saad'
keywords:
- 'teacher-student'
- 'online-learning'
- 'soft-committee-machine'
- 'plateaus'
implementations: []
summary: >-
  Saad and Solla (1995), [DOI:10.1103/PhysRevE.52.4225.](https://doi.org/10.1103/PhysRevE.52.4225.) The exact learning
  dynamics of a soft committee machine under online gradient descent,
  including the symmetric plateau and the specialization that ends it.
---
# LIT-tmptmtm6: On-line learning in soft committee machines

Saad and Solla (1995) — [DOI:10.1103/PhysRevE.52.4225](https://doi.org/10.1103/PhysRevE.52.4225)

## Key takeaways

Derives exact ODEs governing learning dynamics of two-layer neural networks
(soft committee machines) in the teacher-student setup using statistical
mechanics. Reduces high-dimensional stochastic weight dynamics to a closed
low-dimensional system for order parameters Q (student-student overlap) and
R (student-teacher overlap). Characterizes two distinct learning phases: (1)
plateau phase — all students learn identical weights (unspecialized); (2)
specialization phase — students differentiate and align to distinct teacher
neurons. This is the foundational paper that the Goldt et al. 2020 framework
extends to ReLU/hidden-manifold data.

- **Exact ODE system for Q, R.** In the thermodynamic limit the overlaps
  obey a closed ODE system: dR/dt = η (1 - R²) ⟨σ'(u) σ'(u*)⟩ dQ/dt = η²
  ⟨σ'(u)²⟩ + 2η (R - Q) ⟨σ'(u)²⟩ where u and u* are the pre-activations of
  student and teacher respectively, and angle brackets denote expectations
  over the Gaussian data distribution.
  *Holds when:* General K, M hidden units; exact for erf activation
- **Plateau phase characterization.** A long plateau exists where dR/dt ≈ 0
  and dQ/dt ≈ 0. All student-teacher overlaps are equal during this phase;
  the network is effectively one-layer. Plateau duration scales as ~ log(d)
  / η. Learning resumes only when symmetry breaks spontaneously.
  *Holds when:* Observable for K ≥ M (realizable regime)
- **Generalization error formula.** Test MSE = f(Q(t), R(t)) exactly. For
  the realizable case, ε_gen(t) → 0 as R(t) → 1. The floor is set by the
  noise variance σ².
  *Holds when:* Realizable case K ≥ M; noise-free teacher

## What the evidence does not cover

- Thermodynamic limit d → ∞; finite-d deviations can be significant for d <
  100.
- Online SGD only; minibatch requires additional noise analysis.
- Erf activation; ReLU results are approximate.
- Two-layer only.

## Standing in the anthology

Read — the reading is [NOTE-tmphaoje](../notes.d/NOTE-tmphaoje.md). Arrived in the imported batch, which
brought in the teacher-student line, which solves the learning dynamics
exactly in a solvable model.
