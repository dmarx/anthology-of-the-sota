---
number: 131
status: Read
formerly:
- NOTE-tmplbko0
paper: LIT-251
title: 'The Role of Permutation Invariance in Linear Mode Connectivity of Neural Networks'
version: 1
tags:
- model-stability
date: '2026-09-15'
summary: >-
  For overparameterized networks, the loss landscape has essentially one basin
  modulo permutation symmetry. Two independently trained networks represent
  the same function with permuted neurons. Averaging their weights directly
  interpolates between permuted copies and crosses a loss barrier. If you
  first align the permutations, the interpolation stays in the flat basin.
---
# NOTE-131: The Role of Permutation Invariance in Linear Mode Connectivity of Neural Networks

## Contribution

Shows that two sufficiently wide neural networks trained from different
random initializations can be matched via neuron permutation such that the
loss along the linear interpolation between them is flat (no barrier). This
is the "linear mode connectivity" (LMC) conjecture, proved under the
condition that no neuron is dead. Provides the theoretical underpinning for
why naive weight averaging across workers degrades performance: without
permutation alignment, you traverse a high-loss barrier.

## Key insight

For overparameterized networks, the loss landscape has essentially one basin
modulo permutation symmetry. Two independently trained networks represent
the same function with permuted neurons. Averaging their weights directly
interpolates between permuted copies and crosses a loss barrier. If you
first align the permutations, the interpolation stays in the flat basin. The
width of the network controls how likely random alignment is: wider networks
have more neurons and a higher chance that some units agree by chance,
reducing (but not eliminating) the averaging penalty.

## Assumptions

- No dead neurons (all ReLU units activate on at least some inputs)
- Sufficient overparameterization (exact condition on width not tight)
- IID training data (permutation analysis is data-independent)

## Key results

- **Theorem 1.** If no neuron in either network is dead, there exists a
  permutation of one network's hidden units such that the linear
  interpolation between the permuted and original network has no loss
  barrier (LMC holds).
  *Holds when:* Condition: no dead neurons; applies to ReLU networks
- **Empirical.** Without permutation alignment, loss barriers scale with
  network depth and shrink (but do not vanish) with width. With alignment,
  barriers vanish.
  *Holds when:* Demonstrated on CIFAR-10, ResNets, VGGs

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Naive weight averaging (without permutation alignment) always incurs a loss barrier for ReLU networks. | strong | Theorem 1 + empirical validation |
| C2 | Permutation alignment before averaging eliminates the barrier in sufficiently wide networks. | strong | Theorem 1 |
| C3 | The barrier shrinks with width because wider networks have more alignment opportunities by chance. | moderate | Empirical; theoretical argument informal |

## Concepts

- **Linear Mode Connectivity (LMC)** — Two parameter vectors θ1, θ2 are
  linearly mode connected if loss(αθ1 + (1-α)θ2) ≤ max(loss(θ1), loss(θ2)) +
  ε for all α ∈ [0,1].
- **Permutation symmetry** — For any hidden layer, permuting the neurons
  (and correspondingly permuting the weights) yields an identical function.
  A width-H layer has H! equivalent representations.
- **Loss barrier** — The excess loss at the linear interpolation midpoint
  relative to the endpoint losses.

## Connections

**Builds on.**

- Garipov et al. 2018 (Loss Surfaces, Mode Connectivity) — Prior work
  established that mode connectivity exists via nonlinear paths; this paper
  shows it holds linearly after permutation alignment.

**Related.**

- Git Re-Basin: Merging Models modulo Permutation Symmetries ([LIT-333](../literature.d/LIT-333.md))
  — Ainsworth et al. provide practical algorithms (activation matching,
  weight matching) to find the permutation; this paper provides the
  theoretical foundation.

## Recommendations

- **R1** — Before averaging neural network weights (federated averaging,
  gossip, model ensembling), apply neuron permutation alignment to avoid
  traversing loss barriers.
  *Topic:* weight averaging · *Strength:* strong · *When:* ReLU networks;
  especially important for shallow/narrow networks where random alignment
  probability is low.

## Bearing on the record

Most of the loss barrier between two independently trained networks is
permutation rather than disagreement. This is a `THEORY` in this record's
sense — a claim about why something works — and the practice it underwrites
is that weights from separate runs must be aligned before they are averaged,
which touches every averaging scheme in this batch.

## Limitations

- LMC conjecture only proved for the case where no neurons are dead;
  practical guarantee.
- Width requirement for guaranteed alignment is not explicit (not a tight
  bound).
- Analysis is for two-layer networks; deeper networks are more complex.

## Open questions

- What is the minimum width H such that random gossip averaging is loss-
  barrier-free?
- Does applying permutation alignment at every gossip step recover sync-SGD
  performance?
- How does alignment complexity (Hungarian matching is O(H^3)) scale in
  gossip?
