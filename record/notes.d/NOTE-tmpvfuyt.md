---
status: Read
paper: LIT-tmpv8s1r
title: 'Emergence of stochastic flocking for the discrete Cucker-Smale model with randomly switching topologies'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
summary: >-
  The Cucker-Smale velocity update is a stochastic matrix multiplication on
  velocities: V[t+1] = (Id - (h/N)·L_{σ[t]}[t]) · V[t], where each factor is a
  row-stochastic matrix with ergodicity coefficient determined by the
  communication weight φ and position diameter. Flocking = the velocity
  diameter D(V[t]) → 0 a.s.
---
# NOTE-tmpvfuyt: Emergence of stochastic flocking for the discrete Cucker-Smale model with randomly switching topologies

## Contribution

Proves almost-sure asymptotic flocking (velocity consensus) for the discrete
Cucker-Smale model under IID randomly switching directed network topologies,
with Poisson and geometric dwelling-time processes explicitly verified. The
sufficient framework requires only: (A1) the union of all admissible
topologies has a directed spanning tree, and (A2) dwelling times are bounded
in probability. Extends the continuous CS result of [15] (arXiv:1911.07390)
to the discrete case and removes the compact-support assumption on the
switching-time distribution. This is the most directly applicable stochastic
flocking result for our gossip training setting: it proves velocity
consensus under exactly the kind of IID random topology switching that
gossip algorithms use.

## Key insight

The Cucker-Smale velocity update is a stochastic matrix multiplication on
velocities: V[t+1] = (Id - (h/N)·L_{σ[t]}[t]) · V[t], where each factor is a
row-stochastic matrix with ergodicity coefficient determined by the
communication weight φ and position diameter. Flocking = the velocity
diameter D(V[t]) → 0 a.s. The proof reduces to showing that the product of
sufficiently many such stochastic matrices eventually becomes scrambling
(positive ergodicity coefficient), which holds as long as the union topology
has a spanning tree and topologies are selected with nonzero probability.
The same union-spanning-tree condition that governs linear consensus
(Jadbabaie 2003, Tahbaz-Salehi 2008) governs nonlinear CS flocking — the
velocity alignment dynamics inherit the scrambling structure from the
topology, not from the nonlinear influence function φ. Crucially, the
communication weight φ only needs to decay slower than any power law: 1/φ(r)
= O(r^ε), not φ bounded away from zero. This is a MUCH weaker condition than
requiring φ > δ > 0 globally.

## Assumptions

- Finite admissible topology set: S_G = {G_1,...,G_{N_G}} with N_G < ∞.
- IID topology selection: P(σ[t_ℓ] = k) = p_k > 0 for all k; topologies
  selected i.i.d. at each switch.
- Dwelling times: t_{ℓ+1} - t_ℓ = 1 + T_ℓ where T_ℓ are independent nonneg
  integer r.v.'s.
- A1: Union topology ∪_k G_k has a directed spanning tree.
- A2: Dwelling times bounded in probability (see Theorem 3.1 for precise
  technical condition).
- Communication weight: φ: [0,∞) → R+ bounded, Lipschitz, monotone
  decreasing, φ(0) = κ.
- Slow-decay condition: 1/φ(r) = O(r^ε) for some ε > 0 (φ decays slower than
  any power law).
- Step size: 0 < hκ < 1 (coupling strength × step size < 1, ensures
  stochastic matrix structure).
- Coupling strength condition (Theorem 3.1): (M+N-1)·log(1/(1-hκ)) / min_k
  log(1/(1-p_k)) < 1.

## Key results

- **Theorem 3.1 — Stochastic flocking with probability one.** Under
  framework (A1)-(A2), if parameters N, h, κ, p_k, φ satisfy: (i) 0 < hκ < 1
  (ii) (M+N-1)·log(1/(1-hκ)) / min_k log(1/(1-p_k)) < 1 (iii) 1/φ(r) =
  O(r^ε) for ε < 1/(N-1) - (M+N-1)·log(1/(1-hκ))/[(N-1)·min_k
  log(1/(1-p_k))] then the discrete CS system exhibits asymptotic global
  flocking with probability one: P(ω: ∃ x^∞ > 0 s.t. sup_{0≤t<∞} D(X[t,ω]) ≤
  x^∞ AND lim_{t→∞} D(V[t,ω]) = 0) = 1.
  *Holds when:* N = number of agents, h = time step, κ = φ(0) = max
  coupling, M = dwelling-time bound constant, p_k = selection probability
  for topology G_k. The condition (ii) requires min topology probability p_k
  to be large enough relative to coupling strength hκ.
- **Proposition 4.1 — Velocity alignment rate.** For t ∈ [t*_{r(N-1)},
  t*_{(r+1)(N-1)}), the velocity diameter satisfies: D(V[t]) ≤ D(V[0]) ·
  exp[-(1-hκ)^{(M+N-1)(n+c log(N-1))} · (hφ(x^∞)/(N(1-hκ)))^{N-1} ·
  ((r+1)^{1+c(M+N-1)log(1-hκ)} - 1) / (1 + c(M+N-1)log(1-hκ))]. Convergence
  is super-exponential in r (faster than geometric).
  *Holds when:* c, n are framework parameters; x^∞ is the bounded position
  diameter; r is the block index.
- **Lemma 2.2 — Spanning tree implies scrambling product (from Wu 2006).**
  If A_1,...,A_{N-1} are N×N nonneg matrices with positive diagonals and
  each G(A_i) has a spanning tree, then the product A_1·A_2···A_{N-1} is
  scrambling (µ > 0).
  *Holds when:* N-1 matrices suffice regardless of N. This is the core
  algebraic lemma.
- **Proposition 5.1 — Poisson dwelling times satisfy (A2).** If T_ℓ ~
  Poisson(λ_ℓ) independently with λ_max = sup_ℓ λ_ℓ < ∞, then for any c > 0
  there exists M such that (A2) holds with p̃(n) → 0 as n → ∞.
  *Holds when:* λ_max < ∞ is the key condition — rates need not be equal.
- **Proposition 5.2 — Geometric dwelling times satisfy (A2).** If T_ℓ ~
  Geometric(p_ℓ) independently with p_min = inf_ℓ p_ℓ > 1/2, then for any c
  > 0 there exists M such that (A2) holds with p̃(n) → 0 as n → ∞.
  *Holds when:* p_min > 1/2 means each switch happens within 2 steps in
  expectation.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The union spanning tree condition (A1) is the ONLY topological condition needed for stochastic flocking. Individual topologies can be disconnected; only their union (over the admissible set) needs a spanning tree. | strong | Theorem 3.1 and proof via Lemma 2.2. No per-round connectivity is required. |
| C2 | The condition min_k p_k plays the role of a spectral gap: it determines how quickly the union topology is "seen" in expectation. The condition (ii) in Theorem 3.1 says the mixing rate hκ must be slow enough relative to the topology switching rate min_k p_k. | strong | Direct from the structure of condition (ii). Smaller p_k (rare topologies) requires smaller hκ. |
| C3 | Random topology switching with IID selection is EASIER for flocking than fixed topology, because any spanning-tree topology is eventually selected, contributing to the union. The randomness helps — it removes the need for any single topology to be connected. | strong | Contrast with deterministic switching (Jadbabaie 2003) which requires union over a window. Here, any topology can appear at any time. |
| C4 | The flocking result holds for ANY initial configuration (global flocking) when the slow-decay condition 1/φ(r) = O(r^ε) holds. This is vastly weaker than φ bounded away from zero (which would require finite position diameter). | strong | Proposition 4.2 and Lemma 4.3. The key is that velocity diameter decays faster than position diameter grows. |

## Method

**Discrete Cucker-Smale with IID random topology switching.**

N agents with position x_i ∈ R^d and velocity v_i ∈ R^d. At each step: 1.
Current topology σ[t] = k ∈ {1,...,N_G} is drawn IID with P(σ[t_ℓ] = k) =
p_k. 2. Topology held constant for dwelling time t_{ℓ+1} - t_ℓ = 1 + T_ℓ. 3.
Position update: x_i[t+1] = x_i[t] + h·v_i[t] 4. Velocity update: v_i[t+1] =
v_i[t] + (h/N) Σ_j χ^{σ[t]}_{ij} φ(||x_j[t]-x_i[t]||)(v_j[t]-v_i[t]) Matrix
form: V[t+1] = (Id - (h/N)·L_{σ[t]}[t]) · V[t] where each factor is row-
stochastic under hκ < 1.

- Stochastic matrix factor: (Id - (h/N)·L_k[t]) row-stochastic when hκ < 1;
  each row sums to 1
- Ergodicity coefficient µ(A) = min_{i,j} Σ_k min(a_{ik},a_{jk}): measures
  scrambling; µ>0 ↔ scrambling
- Scrambling implies velocity contraction: D(V[t+1]) ≤ (1-µ)·D(V[t])
- Product-of-scrambling: N-1 spanning-tree matrices multiply to a scrambling
  matrix (Lemma 2.2)
- Random spanning tree selection: A1+IID probabilities → each window of N-1
  topology blocks covers the union

## Concepts

- **velocity diameter** — D(V) = max_{1≤i,j≤N} ||v_i - v_j||. Flocking
  requires D(V[t]) → 0 as t → ∞. Position diameter D(X) = max ||x_i - x_j||
  must remain bounded (particles stay together).
- **asymptotic global flocking** — sup_{0≤t<∞} D(X[t]) ≤ x^∞ < ∞ AND
  lim_{t→∞} D(V[t]) = 0. Particles travel together (bounded spread) with
  asymptotically aligned velocities. "Global" means for ANY initial
  condition, not just nearby ones.
- **ergodicity coefficient (Dobrushin coefficient)** — µ(A) = min_{i,j} Σ_k
  min(a_{ik}, a_{jk}) for a nonneg matrix A. Measures "scrambling": µ(A) > 0
  iff A is scrambling (any two rows share a common positive entry). Key
  property: for stochastic A, D(AV) ≤ (1-µ(A))·D(V) — contraction of vector
  diameter. Also: µ(AB) ≥ µ(A)·µ(B) + ... — submultiplicative (products
  contract).
- **communication weight φ** — φ: [0,∞) → R+, bounded, Lipschitz, monotone
  decreasing; φ(||x_j - x_i||) = influence of j on i. In the original CS
  model: φ(r) = (1 + r²)^{-β}. The slow-decay condition 1/φ(r) = O(r^ε) is
  satisfied by power-law φ if β < 1/2 (unconditional flocking regime of
  Cucker-Smale 2007).
- **dwelling time** — The number of time steps t_{ℓ+1} - t_ℓ for which
  topology σ_ℓ is held fixed before the next topology switch. Written as 1 +
  T_ℓ where T_ℓ ≥ 0 is the "extra" time. Bounded dwelling times (A2) ensure
  switches happen often enough for the union topology to cover all spanning
  tree paths within a logarithmically growing window.

## Connections

**Builds on.**

- On the Stochastic Flocking of the Cucker-Smale Flock with Randomly
  Switching Topologies (Dong, Ha, Jung, Kim 2019 — continuous version) —
  Direct predecessor by the same authors. This paper (1912.11949) extends
  the continuous CS result to the discrete case and removes the compact-
  support assumption on switching times. The present paper's Theorem 5.1
  provides the improved continuous result.
- Emergent Behavior in Flocks (Cucker & Smale 2007) — The original CS model
  and flocking result (on complete graphs). Dong et al. generalize from
  complete graph to randomly switching directed topologies. The influence
  function φ is the same; the topology structure is the key extension.
- Synchronization and Convergence of Linear Dynamics in Random Directed
  Networks (Wu 2006) — Source of Lemma 2.2 (product of N-1 spanning-tree
  matrices is scrambling). This is the key algebraic tool that connects
  topology structure to ergodicity coefficients.
- Coordination of Groups of Mobile Autonomous Agents (Jadbabaie, Lin, Morse
  2003) — Establishes the union spanning-tree condition for deterministic
  switching in the linear (pure averaging) case. Dong et al. extend this to
  stochastic switching in the nonlinear CS (velocity-weighted) case. Both
  use the scrambling matrix mechanism.

**Related.**

- Consensus Over Random Networks (Tahbaz-Salehi & Jadbabaie 2008) — Tahbaz-
  Salehi/Jadbabaie proves linear consensus for IID random mixing matrices
  under E[W] spanning tree. Dong et al. prove NONLINEAR velocity consensus
  (CS flocking) under IID random topology selection with union spanning
  tree. Both use IID topology switching; Dong et al. handle the additional
  difficulty that mixing weights depend on agent positions.
- Gossip ULA / EXTRA SGLD ([LIT-tmpy820t](../literature.d/LIT-tmpy820t.md)) — Gossip ULA uses EXTRA correction
  to achieve gradient consensus (velocity consensus in our analogy). The
  topology conditions in Dong et al. justify why IID random gossip mixing in
  Gossip ULA achieves consensus even with time-varying position-dependent
  weights.

## Recommendations

- **R1** — For distributed optimization with IID random topology gossip,
  model the gradient update step as a CS velocity update: the gossip mixing
  matrix is the position-independent version of the CS influence matrix. The
  union spanning-tree condition guarantees gradient consensus (velocity
  alignment) almost surely, with convergence rate determined by the
  ergodicity coefficient of the N-step product matrix.
  *Topic:* Gossip optimization convergence via CS flocking analogy ·
  *Strength:* moderate · *When:* Exact mapping requires gradient updates to
  have the same structure as CS velocity updates. Most applicable when using
  gradient tracking (EXTRA-style) methods where the auxiliary variable
  dynamics have the stochastic matrix form of CS velocity evolution.
- **R2** — When designing stochastic gossip schedules, use Poisson or
  geometric inter-switch distributions for the topology switching times —
  both are proven to satisfy (A2) under mild conditions (λ_max < ∞ for
  Poisson, p_min > 1/2 for Geometric). These give almost-sure velocity
  consensus.
  *Topic:* Gossip dwelling time distribution design · *Strength:* strong ·
  *When:* IID topology selection; union spanning tree condition (A1)
  satisfied.

## Bearing on the record

Flocking under randomly switching topologies. Filed with the consensus line.

## Limitations

- Sufficient condition only — union spanning tree is not proven necessary
  for CS flocking (unlike Tahbaz-Salehi which has necessity for linear
  consensus).
- The coupling condition (ii) is joint in hκ and min p_k — it may be
  restrictive for large N or rare topologies.
- No gradient/optimization layer — pure velocity consensus without a loss
  function. Extension to SGD requires additional analysis of gradient noise
  interacting with the flocking dynamics.
- Position dependence of mixing weights φ(||x_i - x_j||) makes analysis
  harder than linear consensus; the slow-decay condition 1/φ(r) = O(r^ε) is
  a workaround for bounded position diameter.
- All-to-all interaction structure (Σ over all j=1..N) — in gossip SGD, each
  node only communicates with a few neighbors, giving a sparser mixing
  matrix than full CS.
- Only the discrete Euler discretization is analyzed; higher-order or
  adaptive integrators are not covered.

## Open questions

- Is the union spanning tree condition necessary for CS flocking under
  random switching, or is there a weaker E[W] spanning-tree condition
  (analogous to Tahbaz-Salehi)?
- How does the CS convergence rate depend on N, h, κ, and min p_k? Can this
  be made explicit for the gossip SGD application?
- Can the CS framework be extended to include gradient noise (stochastic
  gradients), giving a gossip-Langevin flocking theorem?
- Does local flocking (subgroup consensus without global consensus)
  correspond to mode-seeking in the gossip optimization landscape?
- What is the mean-field limit (N → ∞) of the stochastic CS model with
  random topologies? Does it give a PDE for the gradient distribution?
