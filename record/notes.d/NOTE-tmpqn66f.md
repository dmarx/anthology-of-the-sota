---
status: Read
paper: LIT-tmp7pep0
title: 'Mean Field Analysis of Neural Networks: A Law of Large Numbers'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
summary: >-
  With 1/N scaling of the output layer and a time rescaling t = k/N (so that
  one unit of continuous time corresponds to N SGD steps), the N hidden units
  behave like an interacting particle system whose empirical measure μ^N_t
  converges to a deterministic measure-valued process μ̄_t satisfying a
  McKean-Vlasov / Fokker-Planck PDE.
---
# NOTE-tmpqn66f: Mean Field Analysis of Neural Networks: A Law of Large Numbers

## Contribution

Proves a law of large numbers for one-hidden-layer neural networks trained
by SGD: as width N and SGD iterations grow jointly (with time scaled as t =
k/N), the empirical distribution of parameters converges to the
deterministic solution of a nonlinear PDE (a Wasserstein gradient flow of
the population loss). Unlike concurrent work (Mei-Montanari-Nguyen), the
proof does not assume the neural network gradient is globally Lipschitz or
bounded, only moment conditions on data and initialization. Also establishes
propagation of chaos: parameters become asymptotically independent.

## Key insight

With 1/N scaling of the output layer and a time rescaling t = k/N (so that
one unit of continuous time corresponds to N SGD steps), the N hidden units
behave like an interacting particle system whose empirical measure μ^N_t
converges to a deterministic measure-valued process μ̄_t satisfying a
McKean-Vlasov / Fokker-Planck PDE. The 1/N normalization in the hidden layer
plays the role of a learning-rate decay, enabling convergence at constant
step size. The mean-field limit is a gradient flow of the population loss in
Wasserstein space.

## Assumptions

- Activation σ ∈ C²_b(ℝ): twice continuously differentiable and bounded
  (rules out ReLU)
- Data (x_k, y_k) i.i.d. from π with E[||x||⁴] + E[|y|⁴] < ∞
- Parameters initialized i.i.d. from μ̄_0 with E[exp(q|c_0|)] < C and
  E[||w_0||⁴] < C
- IID data across SGD iterations (satisfied in our homogeneous colocated IID
  setting)
- Single hidden layer, squared loss, constant learning rate α
- Output layer scaled by 1/N (mean-field parameterization)

## Key results

- **Theorem 1.2 (Law of Large Numbers).** μ^N converges in distribution in
  D_E([0,T]) to the unique deterministic μ̄ satisfying the measure evolution
  equation (1.7), a nonlinear first-order PDE which is a Wasserstein
  gradient flow of L̄(p) = (1/2)E[(Y - <cσ(w·X), p>)²]
  *Holds when:* Requires time rescaling t = ⌊Nt⌋/N (N SGD steps per unit
  time); holds for any finite T under Assumption 1.1
- **Theorem 1.6 (Propagation of Chaos).** The joint law ρ^N of N trained
  parameters is μ̄-chaotic: for any fixed k, the first k marginals converge
  to μ̄⊗k. Parameters become asymptotically independent.
  *Holds when:* Follows from LLN + Tanaka-Sznitman theorem given
  exchangeability
- **Corollary 1.4.** If μ̄_t has density p(t,c,w), then p solves ∂_t p = -α
  div_θ(p ∇_θ v(θ,p)) where v is the functional derivative of L̄
  *Holds when:* Requires p vanishes at infinity

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | As width N → ∞, the trained neural network converges in probability to a deterministic function despite random initialization and random SGD data order | strong | Theorem 1.2 + numerical experiments on MNIST showing parameter distribution stabilizing at N=10k, 100k, 250k |
| C2 | 1/N scaling of the output layer substitutes for learning-rate decay, enabling convergence with constant α | strong | Mathematical structure of the proof; the rescaling t=k/N compensates for step size |
| C3 | The mean-field training dynamics are a gradient flow of the population loss in Wasserstein space | strong | PDE (1.8) has divergence form div(p ∇v); connection to Jordan-Kinderlehrer-Otto |
| C4 | Hidden units become asymptotically independent (propagation of chaos) | strong | Theorem 1.6 |
| C5 | The approach handles non-globally-Lipschitz, non-globally-bounded neural networks, unlike Mei-Montanari-Nguyen | moderate | Proof technique uses structure of SGD + moment bounds from Lemma 2.1 |

## Method

**Mean-field analysis via weak convergence of measure-valued processes.**

(1) Write SGD updates and form empirical measure ν^N_k = (1/N)Σδ_{c^i_k,
w^i_k}. (2) Rescale time μ^N_t = ν^N_⌊Nt⌋ viewed as a càdlàg process in
measure space. (3) Prove relative compactness via compact containment
(moment bounds) and regularity (increments controlled by 1/N). (4) Identify
any limit point satisfies the McKean-Vlasov PDE (1.7) using Taylor expansion
of test functions and vanishing martingale terms. (5) Prove uniqueness of
the PDE solution via a Banach fixed-point contraction argument in
Wasserstein-4 space on short intervals, extended to [0,T]. (6) Derive
propagation of chaos from exchangeability + deterministic limit.

- 1/N output layer scaling (mean-field parameterization)
- Time rescaling t = k/N
- Moment bounds via exponential moment of |c_0|
- Wasserstein contraction for uniqueness

## Concepts

- **mean-field parameterization** — Neural network g^N(x) = (1/N)Σ c^i
  σ(w^i·x) with 1/N scaling on the output layer; this scaling makes the
  empirical measure of parameters the natural state variable.
- **propagation of chaos** — Joint law of N exchangeable particles is
  q-chaotic if, for every k, the k-marginal converges weakly to the product
  measure q^⊗k as N→∞.
- **measure evolution equation** — Weak form PDE (1.7) characterizing μ̄_t
  as a deterministic flow in P(ℝ^{1+d}) driven by the gradient of the
  population loss functional.
- **Wasserstein gradient flow** — Evolution ∂_t p = -α div(p ∇v[p]) where v
  is the functional derivative of the energy; here the energy is the
  population MSE loss.

## Connections

**Builds on.**

- Ethier & Kurtz, Markov Processes: Characterization and Convergence —
  Provides the weak convergence machinery (Skorokhod space, relative
  compactness criteria) used throughout.
- Scaling limit: Exact and tractable analysis of online learning algorithms
  (Wang, Mattingly, Lu) — Prior weak-convergence-based analysis of online
  learning algorithms that this paper's approach parallels.
- Sznitman, Topics in propagation of chaos — Framework for propagation of
  chaos applied here to derive asymptotic parameter independence.

**Related.**

- A mean field view of the landscape of two-layer neural networks (Mei,
  Montanari, Nguyen) ([LIT-tmp8li9l](../literature.d/LIT-tmp8li9l.md)) — Concurrent work deriving a similar
  mean-field PDE limit under stronger (globally Lipschitz, bounded)
  assumptions; this paper relaxes those.
- Neural Networks as Interacting Particle Systems (Rotskoff, Vanden-Eijnden)
  ([LIT-tmpy2bnh](../literature.d/LIT-tmpy2bnh.md)) — Concurrent interacting-particle-system view of wide
  neural networks.
- On the global convergence of gradient descent for over-parameterized
  models using optimal transport (Chizat, Bach) ([LIT-tmpge342](../literature.d/LIT-tmpge342.md)) —
  Complementary global convergence result for the mean-field gradient flow.
- Mean field analysis of deep neural networks (Sirignano, Spiliopoulos) —
  Follow-up extending LLN to deep networks.

## Recommendations

- **R1** — Use 1/N (mean-field) output-layer scaling when studying very wide
  networks; it substitutes for learning-rate decay and yields a nontrivial
  deterministic training limit.
  *Topic:* parameterization · *Strength:* strong · *When:* When width N is large
  and one wants a feature-learning (non-NTK) regime.
- **R2** — Expect that for very wide single-hidden-layer nets, the
  distribution of parameters (not individual parameter values) is the
  meaningful object to track.
  *Topic:* analysis · *Strength:* strong · *When:* Wide networks with i.i.d.
  initialization.
- **R3** — At large width, treat hidden units as approximately independent
  (propagation of chaos) when deriving heuristic scaling laws.
  *Topic:* modeling · *Strength:* moderate · *When:* Mean-field
  parameterization, large N.

## Bearing on the record

The law-of-large-numbers half, and the clearest statement of the object that
actually moves: the distribution of parameters, not the parameters.

## Limitations

- Single hidden layer only; multilayer extension appears in follow-up
  (1903.04440).
- Requires bounded C² activation — excludes ReLU, the practically dominant
  choice.
- Constant learning rate and squared loss; other loss functions not treated.
- No rate of convergence in N (qualitative LLN only); rates require CLT
  (Sirignano-Spiliopoulos 2019).
- Mean-field 1/N parameterization differs from the standard 1/√N (NTK)
  parameterization used in practice.
- IID data assumption; heterogeneous/non-IID data not addressed.

## Open questions

- What is the rate of convergence of μ^N to μ̄ as a function of N?
- Does the PDE admit a global minimizer of the population loss, and does the
  flow converge to it?
- How to extend to ReLU and other non-smooth activations?
- How to incorporate Langevin-type noise / finite-batch fluctuations into
  the mean-field framework?
