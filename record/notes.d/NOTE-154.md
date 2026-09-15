---
number: 154
status: Read
formerly:
- NOTE-tmpx5j6w
paper: LIT-273
title: 'Distributed Optimization with Gradient Tracking over Heterogeneous Delay-Prone Directed Networks'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
summary: >-
  Embedding the robustified Ratio Consensus protocol into ADD-OPT and
  augmenting the network graph with virtual delay nodes transforms a delayed
  directed network into a delay-free augmented network, allowing existing
  convergence proofs to apply with the augmented spectral radius replacing the
  original, at the cost of a smaller allowable step-size.
---
# NOTE-154: Distributed Optimization with Gradient Tracking over Heterogeneous Delay-Prone Directed Networks

## Contribution

This paper proposes R-ADD-OPT (Robustified ADD-OPT), the first distributed
optimization algorithm with gradient tracking that provably converges on
directed graphs in the presence of heterogeneous, time-invariant bounded
transmission delays, providing an explicit step-size range computable a
priori from the maximum delay.

## Key insight

Embedding the robustified Ratio Consensus protocol into ADD-OPT and
augmenting the network graph with virtual delay nodes transforms a delayed
directed network into a delay-free augmented network, allowing existing
convergence proofs to apply with the augmented spectral radius replacing the
original, at the cost of a smaller allowable step-size.

## Assumptions

- Local objective functions f^j are mu-strongly convex and L-smooth (twice
  differentiable with bounded Hessian eigenvalues).
- The directed communication graph is strongly connected (every node can
  reach every other node via directed paths).
- Transmission delays are heterogeneous but time-invariant and bounded by a
  known constant tau_bar.
- Column-stochastic weight matrix P is fixed (static topology); no dynamic
  graph changes are considered.
- Nodes have access to exact local gradients (no stochastic gradient noise;
  deterministic optimization setting).

## Key results

- **Theorem 1 (Linear convergence of R-ADD-OPT).** Under strongly-convex,
  L-smooth local objectives and bounded time-invariant delays tau_bar,
  R-ADD-OPT converges exponentially to the global optimum: ||z^k - x*||^2 <=
  C * rho(G)^k, where rho(G) < 1 for step-size alpha in (0, alpha_bar) and
  alpha_bar is computable from tau_bar, the spectral gap of the augmented
  mixing matrix, and the Lipschitz and strong-convexity constants.
  *Holds when:* Strongly convex, L-smooth objectives; strongly connected
  directed graph; time-invariant bounded delays; column-stochastic weights.
- **Step-size shrinkage with delay (Table II / Figure 3).** The maximum
  allowable step-size alpha_bar decreases as delay bound tau_bar increases;
  the second-largest eigenvalue sigma of the augmented mixing matrix
  approaches 1 as tau_bar grows, tightening the spectral gap and slowing
  convergence.
  *Holds when:* Example network with sigma = 0.599 (no delay), 0.877
  (tau=2), 0.963 (tau=5), 0.987 (tau=10).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | R-ADD-OPT converges exponentially (O(mu^k)) to the optimal solution for step-size alpha in (0, alpha_bar), where alpha_bar depends on the maximum network delay and can be computed a priori. | strong | Theorem 1 with formal proof showing spectral radius rho(G) < 1 for appropriate alpha, under strongly-convex, L-smooth local objectives and bounded delays. |
| C2 | Larger bounded delays require strictly smaller step-sizes to guarantee convergence, and the parameter sigma (second largest eigenvalue of the augmented matrix Xi) approaches 1 as the delay bound increases. | strong | Table II showing sigma values 0.599, 0.877, 0.963, 0.987 for delay bounds 0, 2, 5, 10 respectively; Figure 3 showing spectral radius vs step-size for different delays. |
| C3 | R-ADD-OPT empirically converges also for bounded time-varying delays with step-size bounded by the value for the maximum time-invariant delay. | weak | Simulation results only; formal proof for time-varying delays is identified as an open problem. |

## Method

**R-ADD-OPT (Robustified Accelerated Distributed Directed OPTimization).**

R-ADD-OPT modifies ADD-OPT by embedding the robustified Ratio Consensus
protocol to handle transmission delays. Each node maintains three state
variables: x^j (numerator state), y^j (denominator state), and w^j (gradient
tracking variable). At each iteration, x^j and y^j are updated using delayed
incoming values from in-neighbors weighted by column-stochastic weights
p_{ji}, minus a gradient tracking correction. The decision variable is z^j =
x^j / y^j (the ratio), which tracks the network-wide average. The gradient
tracker w^j accumulates the difference of local gradients to correct for
bias in the aggregated gradient, enabling linear convergence. Convergence
analysis proceeds by constructing an augmented graph with virtual nodes
representing each possible delay step, reducing the delayed system to a
delay-free augmented system.

- Robustified Ratio Consensus protocol for handling heterogeneous delays in
  directed graphs
- Gradient tracking variable w^j to correct locally aggregated gradients
- Delayed graph augmentation: adding n*tau_bar virtual nodes to absorb
  transmission delays
- Column-stochastic weight matrix P for directed communication
- Step-size bound alpha_bar computed from maximum delay, spectral
  properties, and Lipschitz constants

## Concepts

- **Gradient tracking** — Mechanism where each node maintains a variable
  tracking the network-wide average gradient, enabling linear convergence
  rates in decentralized optimization over directed graphs.
- **Ratio Consensus** — Distributed averaging protocol for directed graphs
  where each node maintains two iterates (x, y) and converges to the average
  of initial values via the ratio x/y.
- **Robustified Ratio Consensus** — Extension of Ratio Consensus that
  incorporates delayed messages from in-neighbors using stored historical
  values, enabling convergence under heterogeneous transmission delays.
- **Delayed graph augmentation** — Technique of adding n*tau_bar virtual
  nodes to model delay-prone links as extra edges in a larger delay-free
  graph, allowing standard convergence tools to apply.
- **ADD-OPT** — Accelerated Distributed Directed OPTimization algorithm that
  combines ratio consensus with gradient tracking for linear convergence on
  delay-free directed graphs.

## Connections

**Builds on.**

- ADD-OPT: Accelerated Distributed Directed Optimization (Xi, Xin, Khan
  2017) — R-ADD-OPT directly modifies ADD-OPT by replacing ratio consensus
  with its robustified delay-tolerant variant and re-deriving the
  convergence step-size range.
- Average Consensus in the Presence of Delays in Directed Graph Topologies
  (Hadjicostis & Charalambous 2013) — Borrows the augmented-graph
  representation for delayed directed networks that underlies the
  convergence analysis.

## Recommendations

- **R1** — Compute the allowable step-size alpha_bar a priori using the
  formula in Eq. 34 with the maximum observed or estimated delay bound
  tau_bar before deployment.
  *Topic:* step-size selection under delays · *Strength:* strong · *When:* When
  deploying R-ADD-OPT in a network with known or estimated maximum
  transmission delay.
- **R2** — Use the step-size that minimizes the spectral radius of G (not
  the maximum allowed step-size) for the best convergence rate.
  *Topic:* step-size tuning · *Strength:* moderate · *When:* When network delay
  statistics are known and convergence speed matters more than using a
  conservative bound.

## Bearing on the record

An a-priori step-size bound computed from the delay bound, which is the same
shape of result as Tsitsiklis et al. 1986 and forty years later. Filed for
the line.

## Limitations

- Convergence is proven only for strongly-convex local objectives; extension
  to nonconvex objectives (as in deep learning) is not addressed.
- Proof covers only time-invariant delays; the time-varying case is
  empirically validated but analytically open.
- The augmented-graph approach scales the problem size by a factor of (1 +
  tau_bar), increasing memory and computational overhead for large delays.
- The computable step-size bound may be conservative; the optimal step-size
  that minimizes spectral radius must be found numerically.

## Open questions

- Can a tight (non-conservative) step-size range be derived analytically for
  bounded time-varying delays?
- How can R-ADD-OPT be extended to nonconvex objectives as required for
  distributed deep learning?
- Is there an analogous robustification for push-sum-based methods (e.g.,
  Push-DIGing) that handles heterogeneous delays with similar guarantees?
