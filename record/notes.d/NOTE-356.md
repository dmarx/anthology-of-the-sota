---
number: 356
status: Skimmed
formerly:
- NOTE-tmpu66fa
paper: LIT-694
title: 'Rigor with Machine Learning from Field Theory to the Poincaré Conjecture'
version: 1
date: '2026-09-25'
summary: >-
  Stochastic, black-box ML can still yield rigorous results in mathematics and physics along two routes. The first is conjecture generation followed by human proof, or RL searches whose outputs can be checked exactly; this is how an RL/Bayesian-optimized ribbon verifier ruled out over 800 candidate counterexamples to the smooth 4D Poincaré conjecture. The second is importing ML theory, such as NNGP/NN-field-theory and gradient-descent metric flows that include Perelman's Ricci flow.
---

<!-- inactive-ok-file: LIT-694 — Deferred: this is the seeded skim of the paper, filed with it on 2026-09-25 -->

# NOTE-356: Rigor with Machine Learning from Field Theory to the Poincaré Conjecture

## Contribution

ML is powerful but stochastic, error-prone and opaque, which sits badly with fields that prize rigor and understanding. This Perspective describes ways to extract rigorous results anyway: using non-rigorous methods to generate conjectures, or using reinforcement learning to find solutions that can then be verified. It surveys uses from string theory to the smooth 4D Poincaré conjecture. It also describes direct bridges from ML theory: a neural-network-inspired approach to field theory, and a theory of metric flows induced by gradient descent that contains the Ricci flow used to prove the 3D Poincaré conjecture.

## Skim

*Abstract, figures and selected sections, read when the work was seeded. Not enough to state its assumptions or results exactly; a `Read` note replaces this one.*

- Conjecture generation (§2): supervised models find a predictive map, and attribution or white-box methods expose which features matter. An example is the knot-signature theorem (Davies et al.): gradient saliency picked out 3 of 12 invariants, experts refined the conjecture after counterexamples, and proved |2σ(K) − slope(K)| ≤ c·vol(K)·inj(K)⁻³ (§2.2, Eq. 2). The string-theory and algebraic-geometry precedents are in §2.1.
- RL as verifiable search (§2.2, Fig. 2): TRPO and A3C agents beat a random walker at unknotting braids. GNN agents work on Kirby diagrams / plumbing graphs.
- Smooth 4D Poincaré (§2.2): framed as "is this knot ribbon?", a game of Reidemeister moves plus band moves. A Bayesian-optimized agent became a state-of-the-art ribbon verifier (tested up to 70 crossings) and showed both knots ribbon in pairs sharing a 0-surgery, ruling out over 800 potential SPC4 counterexamples.
- ML theory to physics (§3.1): the NNGP correspondence (Neal) read as a free field theory, with interactions arising at finite width and correlated parameters (NN-FT correspondence).
- Metric flows (§3.2): a neural network representing a Riemannian metric (as in numerical Calabi–Yau metrics) induces a metric flow under gradient descent, which in a suitable limit contains Ricci flow. §3.3 on RG flows, optimal transport and Bayesian inference was not read.
- Outlook (§4): theoretical physics and pure mathematics are late adopters because they need rigor. The two avenues are rigorous applied ML (with a human in the loop) and applying ML theory.

## Open questions

- The "rigor" rests on verification being exact: a found move sequence is a certificate. The ML itself is never trusted. That design pattern (search with ML, verify exactly) is the transferable lesson and ties to the anthology's evaluation and verification themes.
- The claims are summaries of the authors' own and others' papers (refs. [20], [35], [39], [52]); check the originals for the 800-counterexample figure and the precise conditions of the Ricci-flow containment.
- The NN-FT correspondence (§3.1) is relevant to ML theory of infinite-width networks, but this is a perspective and gives no new proofs here.
