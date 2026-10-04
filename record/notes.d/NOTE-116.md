---
number: 116
status: Read
formerly:
- NOTE-tmpe9vnx
paper: LIT-333
title: 'Git Re-Basin: Merging Models modulo Permutation Symmetries'
version: 2
history:
- version: 2
  date: '2026-10-03'
  note: >-
    Corrected against the ICLR 2023 text; the Limitations section lists each
    correction. Weight matching is coordinate descent over all layers, in
    random order and repeated until convergence (Algorithm 1, §3.2). It is
    not greedy layer-by-layer, and Appendix A.7 argues against greedy
    single-pass matching. Multi-model merging has its own algorithm,
    MergeMany (Algorithm 3, A.10). Zero barrier needs large width: none at
    1× width (§5.3), and a barrier remains on ImageNet (§5.1). The figures
    "2–5×", "0.01–0.1×", "within 1–2%", "20–40%", "90–100%", "5–20
    iterations", "1–4 samples" and "H > 10,000" are not in the paper and are
    removed. Activation matching is not the cheap approximation: weight
    matching is "orders of magnitude faster" and data-free, and the two
    "perform similarly" (Figure 2). The IID assumption is removed, since §5.4
    merges models trained on disjoint, biased data. Entezari et al. (LIT-251)
    is described as a conjecture, not a proved guarantee.
date: '2026-09-15'
summary: >-
  Entezari et al. conjecture that SGD solutions can be permuted so that their
  linear interpolation has no barrier. Git Re-Basin makes this actionable.
  Given two trained networks θ_A and θ_B, it finds permutations π that
  minimize ‖vec(θ_A) − vec(π(θ_B))‖², then interpolates θ_A with π(θ_B). The
  barrier disappears on MNIST and on wide ResNets on CIFAR-10. It does not
  at 1× width, and not on ImageNet.
---
# NOTE-116: Git Re-Basin: Merging Models modulo Permutation Symmetries

## Contribution

Develops three algorithms for finding the permutation that aligns two
independently trained networks before merging their weights (§3):

1. **Activation matching.** A per-layer linear assignment problem on the
   two models' activations over the training data.
2. **Weight matching.** Coordinate descent over all layers' permutations,
   using no data (Algorithm 1).
3. **Straight-through estimator.** Learns the permutation through the loss
   at the midpoint (Algorithm 2).

Demonstrates zero-barrier linear mode connectivity on MNIST, and between
independently trained ResNets on CIFAR-10 at large width, which the paper
calls the first such demonstration (§5.3). It shows barriers shrinking with
width, and LMC emerging only as training proceeds. It gives a counterexample
showing that LMC is a property of SGD-trained solutions, not of
architectures (§4, A.6).

## Key insight

Entezari et al. conjecture that SGD solutions can be permuted so that their
linear interpolation has no barrier. Git Re-Basin makes this actionable.
Given two trained networks θ_A and θ_B, it finds permutations π that minimize
‖vec(θ_A) − vec(π(θ_B))‖², then interpolates θ_A with π(θ_B). Solving that
jointly over all layers is NP-hard (Lemma 1), but fixing every layer but one
reduces it to a linear assignment problem. Cycling through the layers until
nothing changes is fast, "generally on the order of seconds to a few minutes"
(§3.2). That this works without any data is the surprise: weight matching is
"surprisingly competitive with data-aware methods". Whether a zero-barrier
permutation is found depends on width. 1× models did not show LMC, and wider
ones reached zero barrier (§5.3).

## Assumptions

- Same architecture. Different random initializations, data orders, and
  "potentially different hyperparameters or datasets" are allowed (§2).
- Sufficient width. Thin models are the first known failure mode (A.1).
- Trained past the early phase. LMC "is an emergent property of training"
  (§5.2).
- Solutions found by SGD-like training. The counterexample in §4/A.6 shows
  that non-SGD solutions need not be connectable.

## Key results

- **Empirical — Loss barriers after matching.** MNIST MLP: zero barrier with
  all three methods. After weight and STE matching the test-loss
  interpolation is convex, i.e. the midpoint beats both endpoints (§5.1).
  CIFAR-10: barriers after weight matching fall with width for VGG-16
  (widths up to 4×) and ResNet20 (1× to 32×), reaching zero for wide ResNet20
  (Figure 4). ImageNet ResNet50 (1×): no zero barrier, a 67% decrease
  relative to naive interpolation (§5.1).
  *Holds when:* sufficient width; "1×-sized models did not seem to exhibit
  linear mode connectivity" (§5.3). Not at initialization (§5.2).
- **Empirical — Merged model quality.** ImageNet ResNet50, BatchNorm
  statistics recomputed: weight matching 51.01% top-1, OT-Fusion 1.38%, and
  weight matching restricted to a single pass ∼7% (A.7.1). CIFAR-100 split
  into disjoint biased halves: the merged ResNet20 has lower test loss than
  either input but is "not competitive in terms of top-1 accuracy". It falls
  short of an ensemble and of full-data training, and is better calibrated
  (§5.4, Figures 10–11).
  *Holds when:* BatchNorm statistics recomputed after merging (A.4).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Permutation alignment gives zero-barrier linear interpolation between independently trained networks when they are wide enough; at standard (1×) width and on ImageNet a barrier remains. | strong | Figures 2 and 4; §5.1, §5.3 |
| C2 | Weight matching performs about as well as activation matching, is orders of magnitude faster, and needs no data; STE is best but very expensive. | moderate | Figure 2; §5.1 |
| C3 | Weight matching works on residual architectures (ResNet20, ResNet50) by coordinate descent over all layers until convergence; restricting it to one greedy pass collapses the ImageNet merge to ∼7% top-1. | moderate | §3.2; Figure 4; A.7.1 |

## Method

**Weight matching by permutation coordinate descent (Algorithm 1).**

The objective is argmax over π of Σ_ℓ ⟨W_ℓ^A, P_ℓ W_ℓ^B P_{ℓ−1}^⊤⟩_F (Eq. 2).
That is the "sum of bilinear assignments problem", NP-hard and with no
polynomial-time constant-factor approximation for L > 2 (Lemma 1). Holding
all other permutations fixed, one layer's best P_ℓ solves a linear
assignment problem:

P_ℓ = argmax_P ⟨P, W_ℓ^A P_{ℓ−1} (W_ℓ^B)^⊤ + (W_{ℓ+1}^A)^⊤ P_{ℓ+1} W_{ℓ+1}^B⟩_F.

Initialize every P_ℓ to the identity. Visit the layers in random order,
solving each one's assignment problem, and repeat until no permutation
changes. Algorithm 1 terminates (Lemma 2). On a V100 it took 3 s for a
3×512 MLP, 33 s for ResNet50 (1×) and 194 s for ResNet20 (32×). It
recovered a known random permutation exactly in 3–4 passes over the layers
(A.5).

- Linear assignment problem per layer, solved by standard polynomial-time
  algorithms (the paper cites Kuhn's Hungarian method, Jonker–Volgenant and
  Crouse).
- Each update uses the weights on both sides of the layer. The paper calls
  this "bi-directional", against the greedy uni-directional single-pass
  matching of prior work (A.7).
- The implementation handles bias terms, residual connections,
  convolutional layers and attention mechanisms (§3.2).

## Concepts

- **Weight matching** — Find π maximizing vec(θ_A) · vec(π(θ_B)) by
  permutation coordinate descent; each step is a linear assignment problem.
- **Activation matching** — Per layer, P = argmax ⟨P, Z^(A)(Z^(B))^⊤⟩_F over
  the activations of the training data, an OLS regression constrained to
  permutations. Each layer is independent, and a full pass over the data
  "may be unnecessary" (§3.1).
- **Merge** — Arithmetic mean of aligned weight tensors: θ_merged = 0.5 *
  (θ_A + π(θ_B)).
- **MergeMany** — Algorithm 3 (A.10). For each model in random order, align
  it to the mean of the others with Algorithm 1, and repeat until
  convergence. There is no anchor model.

## Connections

**Builds on.**

- The Role of Permutation Invariance in Linear Mode Connectivity of Neural
  Networks ([LIT-251](../literature.d/LIT-251.md)) — Entezari et al. state the conjecture and prove it
  only for one hidden layer at random initialization. This paper provides
  the algorithms that find the permutation and test the conjecture directly.

**Related.**

- Entezari et al. 2022 ([LIT-251](../literature.d/LIT-251.md)) — Called "an important intellectual
  ancestor" (A.2). The same appendix argues that Entezari's experiments do
  not themselves provide evidence for LMC, since they would also fit a world
  where all solutions have barriers. It notes that Entezari's simulated
  annealing "yields modest reductions in barrier" and takes days to run.

## Recommendations

- **R1** — For federated learning, gossip or model merging with weight
  averaging between networks that did not share a trajectory, align with
  weight matching before averaging. Run it to convergence over all layers,
  not as one greedy pass.
  *Topic:* gossip averaging · *Strength:* moderate · *When:* wide enough
  networks. The paper anticipates federated use because weight matching
  needs no data, but tests only checkpoint merging. Recompute BatchNorm
  statistics after merging.
- **R2** — When the input data is available and cost matters little,
  straight-through estimator matching gives the lowest barriers. Activation
  matching is about as good as weight matching and costs more, so it is
  not the cheap option.
  *Topic:* gossip averaging · *Strength:* moderate · *When:* a training-data
  pass is affordable; STE "is very computationally expensive" (Figure 2).

## Bearing on the record

Git Re-Basin supplies the algorithms for the alignment that Entezari et al.
conjectured was possible, and the first direct demonstration that it closes
the barrier on real networks. The cheap method is weight matching, which
needs no data. Activation matching performs similarly and is slower. The
demonstration holds at large width; at standard width and on ImageNet a
barrier remains. Together they are one practice and one theory.

## Limitations

- Weight matching approximates an NP-hard problem (Lemma 1). Coordinate
  descent terminates (Lemma 2) but is not guaranteed to reach the best
  permutation.
- Width: no LMC at 1× on CIFAR-10, and a remaining barrier on ImageNet
  ResNet50 (§5.1, §5.3). The paper cannot say whether its search fails on
  thin models or another invariance is at play.
- Known failure modes (A.1): insufficient width, early training, VGGs on
  MNIST, MNIST MLPs at badly chosen learning rates, ConvNeXt. BatchNorm
  needs recomputed statistics; GroupNorm is not permutation-invariant
  (A.4).
- MergeMany is shown only on MNIST MLPs, up to 32 models (A.10).
- *Corrected in v2 (2026-10-03):* previously "Greedy layer-by-layer is not
  globally optimal". Algorithm 1 is coordinate descent over all layers until
  convergence, and A.7 argues against greedy single-pass matching. The
  non-optimality is real, but it comes from Lemma 1.
- *Corrected in v2:* previously "Cost grows as O(H^3); prohibitive for very
  wide layers (H > 10,000)". The paper gives no complexity or width limit.
  Its timings are seconds to minutes, including a 32× wide ResNet20 (A.5).
- *Corrected in v2:* previously "multi-model alignment (N > 2) requires
  pairwise anchoring strategy". MergeMany (Algorithm 3) merges N models with
  no anchor.
- *Corrected in v2:* previously "Does not handle skip connections optimally —
  greedy approximation used". The paper says its implementation handles
  residual connections (§3.2) and reaches zero barrier on wide ResNet20.
- *Corrected in v2:* the quoted figures "2–5×", "0.01–0.1×", "within 1–2%",
  "20–40%", "90–100%", "5–20 iterations" and "1–4 samples" are not in the
  paper. The claim that activation matching is a cheaper approximation was
  backwards (Figure 2).

## Open questions

- For gossip with N workers, is MergeMany's align-to-the-mean-of-the-others
  usable incrementally, or does it need all models at once?
- Does alignment need to happen at every gossip step, or only at
  initialization?
- Is partial alignment (align only a subset of layers) sufficient to close
  the gap?
