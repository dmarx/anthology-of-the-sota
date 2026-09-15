---
number: 121
status: Read
formerly:
- NOTE-tmphaoje
paper: LIT-346
title: 'On-line learning in soft committee machines'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
summary: >-
  The full weight dynamics compress onto two scalar order parameters per
  student- teacher neuron pair. The plateau phase — where R is nearly static
  despite ongoing gradient descent — arises because all students point in
  nearly the same direction, making the two-layer network effectively linear.
  Only once perturbations grow does the specialization phase begin and R
  accelerates toward 1.
---
# NOTE-121: On-line learning in soft committee machines

## Contribution

Derives exact ODEs governing learning dynamics of two-layer neural networks
(soft committee machines) in the teacher-student setup using statistical
mechanics. Reduces high-dimensional stochastic weight dynamics to a closed
low-dimensional system for order parameters Q (student-student overlap) and
R (student-teacher overlap). Characterizes two distinct learning phases: (1)
plateau phase — all students learn identical weights (unspecialized); (2)
specialization phase — students differentiate and align to distinct teacher
neurons. This is the foundational paper that the Goldt et al. 2020 framework
extends to ReLU/hidden-manifold data.

## Key insight

The full weight dynamics compress onto two scalar order parameters per
student- teacher neuron pair. The plateau phase — where R is nearly static
despite ongoing gradient descent — arises because all students point in
nearly the same direction, making the two-layer network effectively linear.
Only once perturbations grow does the specialization phase begin and R
accelerates toward 1. This produces an S-shaped MSE trajectory that CANNOT
be fit by a simple exponential or power law — the plateau and the
acceleration are distinct regimes.

## Assumptions

- Thermodynamic limit: input dimension d → ∞ (dynamics become deterministic)
- Online SGD: one sample per gradient step (batch size 1)
- IID Gaussian inputs
- Activation function: erf or smooth approximation; step-function limit
  handled separately
- Fixed teacher weights
- Constant learning rate η

## Key results

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

## Concepts

- **Student-teacher overlap R** — R_{jn} = W_j · W*_n / (||W_j|| ||W*_n||);
  cosine sim between student j and teacher n. R=1 means perfect alignment.
- **Student-student overlap Q** — Q_{ik} = W_i · W_k / (||W_i|| ||W_k||);
  Q=I means fully specialized students.
- **Plateau phase** — Early regime where all R_{jn} ≈ equal and all Q_{ik} ≈
  equal; network is effectively linear. Generalization barely improves.
- **Specialization phase** — Later regime where R_{jn} differentiate and
  Q_{ik} → δ_{ik}; each student aligns to a distinct teacher neuron. MSE
  drops rapidly.
- **Soft committee machine** — Two-layer network with smooth (erf-like)
  activation and equal output weights; the model studied throughout this
  paper.

## Connections

**Related.**

- Goldt et al. 2020 — hidden manifold model ([LIT-340](../literature.d/LIT-340.md)) — Modern
  extension of this framework to ReLU activations and structured (manifold)
  data; directly applicable to our experiments.
<!-- inactive-ok: LIT-364 — Deferred; the reading filed under that id was not of that paper -->
- Refinetti et al. 2021 ([LIT-364](../literature.d/LIT-364.md)) — Applies same ODE methods to
  classification and the interpolation threshold.

## Bearing on the record

The exact solution of online learning in a soft committee machine, and the
specialization plateau. Thirty years old and the direct ancestor of the
Goldt and Refinetti readings in this batch.

## Limitations

- Thermodynamic limit d → ∞; finite-d deviations can be significant for d <
  100.
- Online SGD only; minibatch requires additional noise analysis.
- Erf activation; ReLU results are approximate.
- Two-layer only.

## Open questions

- Can the ODE be extended to gossip: write coupled ODEs for per-worker
  overlaps R_i(t) with a gossip averaging operator?
- What is the perturbation to R from a single gossip step expressed in ODE
  terms?
