---
number: 116
status: Read
formerly:
- NOTE-tmpe9vnx
paper: LIT-333
title: 'Git Re-Basin: Merging Models modulo Permutation Symmetries'
version: 1
tags:
- model-stability
date: '2026-09-15'
summary: >-
  The LMC conjecture (Entezari et al.) says permutation-aligned networks can
  be linearly interpolated without loss penalty. Git Re-Basin makes this
  actionable: given two trained networks θ_A and θ_B, find permutation
  matrices P* that minimize ||θ_A - P(θ_B)||_F, then average P*(θ_B) with θ_A.
---
# NOTE-116: Git Re-Basin: Merging Models modulo Permutation Symmetries

## Contribution

Develops three practical algorithms for finding the permutation that aligns
two independently trained neural networks before merging their weights: (1)
activation matching (match activations on a small batch), (2) weight
matching (Hungarian algorithm on weight matrices), (3) straight-through
estimator (differentiable relaxation). Demonstrates that aligned merging
achieves near-zero loss barriers across architectures (MLPs, CNNs, VGGs,
ResNets) and provides a practical toolkit for the permutation-alignment
problem.

## Key insight

The LMC conjecture (Entezari et al.) says permutation-aligned networks can
be linearly interpolated without loss penalty. Git Re-Basin makes this
actionable: given two trained networks θ_A and θ_B, find permutation
matrices P* that minimize ||θ_A - P(θ_B)||_F, then average P*(θ_B) with θ_A.
Weight matching via Hungarian algorithm is the most reliable method; it
solves a linear assignment problem layer by layer and achieves 90–100%
barrier elimination on standard benchmarks. The key observation is that
permutation alignment is a preprocessing step that costs O(H^3) per layer
but yields merged models comparable to individually trained ones.

## Assumptions

- IID training data (or at least similar marginal distributions)
- Same architecture and initialization scale
- Sufficient overparameterization for the LMC conjecture to hold

## Key results

- **Empirical — Weight Matching.** Hungarian-algorithm weight matching
  reduces loss barriers to near-zero on MLPs, VGGs, ResNets trained on
  CIFAR-10/100.
  *Holds when:* Baseline barrier ≈ 2–5× endpoint loss; aligned barrier ≈
  0.01–0.1× endpoint loss
- **Empirical — Merged model quality.** Merged (averaged after alignment)
  model achieves accuracy within 1–2% of individually trained models on
  CIFAR-10.
  *Holds when:* Without alignment: 20–40% accuracy degradation

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Permutation alignment before averaging recovers near-ensemble-quality merged models. | strong | Extensive empirical validation across architectures |
| C2 | Weight matching (Hungarian) is more reliable than activation matching. | moderate | Ablation across three methods |
| C3 | The method scales to ResNets with skip connections via a layer-by-layer greedy approach. | moderate | Empirical; optimality of greedy not guaranteed |

## Method

**Weight Matching via Hungarian Algorithm.**

For each layer ℓ (processed in order), solve: P*_ℓ = argmax_P trace(P^T
W_A^ℓ W_B^ℓ^T) where W_A^ℓ, W_B^ℓ are the weight matrices. This is a linear
assignment problem solved in O(H^3) by the Hungarian algorithm. After
finding P*_ℓ, permute B's neurons at layer ℓ (and compensate at layer ℓ+1).
Repeat until convergence (typically 5–20 iterations over all layers).

- Linear assignment problem (LAP) per layer
- Layer-by-layer greedy (not globally optimal but works well in practice)
- Compensation: permuting layer ℓ neurons requires compensating layer ℓ+1
  weights

## Concepts

- **Weight matching** — Find permutation P* = argmax_P trace(P^T W_A W_B^T);
  solved via Hungarian algorithm in O(H^3).
- **Activation matching** — Match neurons by similarity of their activation
  vectors on a reference batch; then solve LAP on the activation correlation
  matrix.
- **Merge** — Arithmetic mean of aligned weight tensors: θ_merged = 0.5 *
  (θ_A + P*(θ_B)).

## Connections

**Builds on.**

- The Role of Permutation Invariance in Linear Mode Connectivity of Neural
  Networks ([LIT-251](../literature.d/LIT-251.md)) — Entezari et al. prove the theoretical guarantee;
  this paper provides the practical algorithms to find the permutation.

**Related.**

- Entezari et al. 2022 ([LIT-251](../literature.d/LIT-251.md)) — Theoretical foundation for why
  alignment eliminates loss barriers.

## Recommendations

- **R1** — For gossip or federated learning with weight averaging, apply
  weight-matching (Hungarian) alignment per hidden layer before each
  averaging step.
  *Topic:* gossip averaging · *Strength:* strong · *When:* Two-layer or shallow
  networks. For deep networks, use layer-by-layer greedy. Overhead is O(L ×
  H^3) per gossip event — may be significant for large H.
- **R2** — For a cheap approximation, use activation matching on a small
  reference batch (1–4 samples); nearly as good as weight matching at lower
  cost.
  *Topic:* gossip averaging · *Strength:* moderate · *When:* When a shared
  reference batch is available at gossip time (e.g., each worker has IID
  data).

## Bearing on the record

Git Re-Basin supplies the algorithms for the alignment that Entezari et al.
showed was needed, including the cheap approximation: activation matching on
a handful of samples is nearly as good as weight matching. Together they are
one practice and one theory.

## Limitations

- Greedy layer-by-layer is not globally optimal; may miss the true minimum-
  barrier alignment.
- Cost grows as O(H^3); prohibitive for very wide layers (H > 10,000).
- Analysis assumes two models; multi-model alignment (N > 2) requires
  pairwise anchoring strategy.
- Does not handle skip connections optimally — greedy approximation used.

## Open questions

- For gossip with N workers, which worker serves as the alignment anchor?
  Random? Leader? Running average?
- Does alignment need to happen at every gossip step, or only at
  initialization?
- Is partial alignment (align only a subset of layers) sufficient to close
  the gap?
