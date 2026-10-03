---
number: 131
status: Read
formerly:
- NOTE-tmplbko0
paper: LIT-251
title: 'The Role of Permutation Invariance in Linear Mode Connectivity of Neural Networks'
version: 2
history:
- version: 2
  date: '2026-10-03'
  note: >-
    Corrected against the ICLR 2022 text; the Limitations section lists each
    correction. The imported reading gave a "Theorem 1" that removes loss
    barriers when no neuron is dead. The paper's only theorem, Theorem 3.1
    (proof in Appendix D), is for a one-hidden-layer ReLU network at uniform
    random initialization. It bounds the output gap at one fixed input by
    Õ(h^{-1/(2d+4)}), and it has no dead-neuron condition. The reading said
    barriers vanish with alignment on ResNets and VGGs. The paper's simulated
    annealing found no permutation that reduced the barrier for either (§4).
    Unsupported content is removed: the claims that naive averaging "always"
    incurs a barrier, that width helps because units "agree by chance", and
    the IID assumption. The LMC and barrier definitions now follow Eq. 1, and
    the claims table and recommendation are restated at the strength the
    paper supports.
date: '2026-09-15'
summary: >-
  Conjectures that, for SGD solutions, the loss landscape has essentially one
  basin modulo permutation symmetry: permute the hidden units of one
  independently trained network appropriately and there would likely be no
  barrier on the linear path to another. The support is a theorem for a
  one-hidden-layer network at random initialization and indirect empirical
  evidence. The paper's own search did not find such permutations for deep
  networks.
---
# NOTE-131: The Role of Permutation Invariance in Linear Mode Connectivity of Neural Networks

## Contribution

States the conjecture that "if invariances are taken into account, there will
likely be no barrier on the linear interpolation of SGD solutions" (§1,
formalized as Conjecture 1 in §3.2). The authors call it "bold" and set out to
fail to refute it. Three kinds of support are offered:

- a theorem, Theorem 3.1, for a one-hidden-layer ReLU network at random
  initialization;
- a measurement of how barriers between independently trained networks vary
  with width, depth, architecture and dataset (§2.2);
- the "our model vs real world" comparison (§3.5, §4). Barriers between
  independently trained networks look like barriers between random
  permutations of one network, both before and after a permutation search.

The paper names implications for ensembling and distributed training (§1,
§5). It does not test them, and it does not find permutations that remove the
barrier between deep networks.

## Key insight

If the conjecture holds, two SGD solutions that look like different minima are
in the same basin after their hidden units are relabelled. Averaging their
weights without relabelling crosses a barrier that relabelling would remove.
The paper cannot search permutations well enough to show this directly. So it
compares independently trained networks with random permutations of one
trained network, a set that satisfies the conjecture by construction. The
two behave alike across width, depth, architecture and dataset (Figures 5, 7,
and over 3000 trained networks in Figure 1). The comparison is indirect.
Git Re-Basin ([LIT-333](../literature.d/LIT-333.md), Appendix A.2) points out that it is also what one would
see if every pair of solutions had a barrier.

## Assumptions

- The conjecture is about solutions SGD is likely to reach, at sufficient
  width. Conjecture 1 asserts "there exists a width h > 0" and does not
  estimate it.
- Theorem 3.1 holds at random initialization, with U and v sampled uniformly
  at 1/√d and 1/√h scale, for one input x with ‖x‖₂ = √d. It says nothing
  about trained networks.
- Only permutations are considered. The paper sets rescaling invariance aside
  on the grounds that SGD's implicit bias balances weight norms (§3.1).

## Key results

- **Theorem 3.1.** f(x) = v⊤σ(Ux) with h ReLU hidden units. U, U′ are
  uniform on [−1/√d, 1/√d], and v, v′ are uniform on [−1/√h, 1/√h]. For any
  x with ‖x‖₂ = √d, with probability 1 − δ there is a permutation of
  (v′, U′) such that the interpolated network's output at x differs from
  α f_{v,U}(x) + (1 − α) f_{v′,U′}(x) by Õ(h^{−1/(2d+4)}).
  *Holds when:* one hidden layer, random initialization, a single fixed
  input. The bound is on output, not loss, and there is no dead-neuron
  condition. The rate in h slows as the input dimension d grows.
- **Empirical — barriers without alignment.** Barriers increase fast with
  depth (Figure 3). For MLPs and Shallow CNNs they rise and then fall with
  width, peaking near the width needed to fit the training data, which the
  paper likens to double descent. For VGG and ResNet they saturate at a high
  value and do not change with width (§2.2, Figure 2). Lower test error goes
  with lower barrier for MLPs and Shallow CNNs. Deep networks have low test
  error and high barrier (Figure 4).
  *Holds when:* MLP, Shallow CNN, VGG and ResNet on MNIST, SVHN, CIFAR-10 and
  CIFAR-100 (ImageNet in Figure 4). Training-loss barrier, measured at α = ½.
- **Empirical — permutation search.** Simulated annealing over five networks
  did not significantly reduce pairwise barriers (Figure 6). Reduced to two
  networks, it lowered barriers for MLPs and Shallow CNNs on MNIST and SVHN.
  It reached zero for MNIST MLPs at depth 1 across widths, and at depths 2
  and 4 at width 2^10 (Figure 7). It did not help as depth grew. For VGG and
  ResNet, the search "were unable to find a permutation to reduce the
  barrier" (§4).
  *Holds when:* SA with the averaged model's train error as objective (SA2).
  A greedy functional-difference matching does better than SA (Appendix B).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Barriers between independently trained networks are statistically similar to barriers between random permutations of one network, across width, depth, architecture and dataset. | moderate | §3.5, §4, Figures 1, 5, 7; indirect evidence for the conjecture |
| C2 | Most SGD solutions can be permuted so that no barrier lies on the linear path between them (Conjecture 1). | weak | Conjecture. Proved only for one hidden layer at random initialization (Theorem 3.1). Search removed barriers only for shallow MNIST MLPs |
| C3 | Without alignment, depth increases the barrier, and for VGG and ResNet the barrier is saturated high regardless of width. | strong | §2.2, Figures 2–3 |

## Concepts

- **Loss barrier** — B(θ1, θ2) = sup over α ∈ [0,1] of L(αθ1 + (1−α)θ2) −
  [αL(θ1) + (1−α)L(θ2)] (Eq. 1). The excess is over the linear interpolation
  of the endpoint losses, not over their maximum. The experiments evaluate it
  at α = ½, which the paper found within 10^−4 of the supremum (footnote 3).
- **Linear Mode Connectivity (LMC)** — θ1 and θ2 are linearly mode connected
  if the barrier between them along the linear path is ≈ 0 (§2.1, following
  Frankle et al. 2020).
- **Permutation symmetry** — For any hidden layer, permuting the neurons
  (and correspondingly permuting the weights) yields an identical function.
  A width-H layer has H! equivalent representations.

## Connections

**Builds on.**

- Garipov et al. 2018 (Loss Surfaces, Mode Connectivity) — Prior work
  established that mode connectivity exists via nonlinear paths; this paper
  conjectures that it holds linearly once permutations are accounted for.

**Related.**

- Git Re-Basin: Merging Models modulo Permutation Symmetries ([LIT-333](../literature.d/LIT-333.md))
  — Ainsworth et al. provide practical algorithms (activation matching,
  weight matching, a straight-through estimator) to find the permutation, and
  are the first to reach zero barrier between independently trained ResNets.
  They credit this paper's conjecture as "an important intellectual ancestor",
  and argue in their Appendix A.2 that its experiments do not themselves
  provide evidence for LMC.

## Recommendations

- **R1** — Before averaging the weights of networks trained from different
  initializations, consider aligning their hidden-unit permutations. The
  paper names this as an implication of its conjecture (§5: "it is possible
  to use it to do weight averaging and build ensembles more efficiently").
  It does not test it, and its own search could not find the permutation
  for deep networks.
  *Topic:* weight averaging · *Strength:* weak · *When:* networks trained
  from different initializations. The paper's demonstrations are confined to
  shallow MLPs and Shallow CNNs.

## Bearing on the record

The claim that most of the loss barrier between two independently trained
networks is permutation rather than disagreement is this paper's conjecture.
This is a `THEORY` in this record's sense — a claim about why something works
— and the practice it would underwrite is that weights from separate runs
must be aligned before they are averaged, which touches every averaging
scheme in this batch. What this paper contributes is the conjecture and
indirect evidence. The demonstration that alignment closes the barrier on
real networks is [LIT-333](../literature.d/LIT-333.md)'s.

## Limitations

- The theorem covers a one-hidden-layer network at random initialization and
  bounds the output gap at one fixed input, not a loss barrier. An NTK
  extension is left to future work (§3.3).
- The paper's search found no barrier-reducing permutation for VGG or ResNet
  (§4, Appendix E.2). The paper names search strength as "the biggest
  limiting factor of our study" (§5).
- The width at which the conjecture would hold is not estimated.
- Image classification only. Language tasks are named as future work (§5).
- *Corrected in v2 (2026-10-03):* this section previously said the LMC
  conjecture was "only proved for the case where no neurons are dead". There
  is no such condition, and what is proved is Theorem 3.1 above, not the
  conjecture.
- *Corrected in v2:* previously "Analysis is for two-layer networks". The
  theorem is for one hidden layer *at random initialization*. The empirical
  analysis covers deep networks too (VGG up to 19 layers, ResNet up to 50).
- *Corrected in v2:* the Key results previously said barriers vanish after
  alignment on CIFAR-10, ResNets and VGGs. For VGG and ResNet the paper's
  search did not reduce the barrier at all (§4).
- *Corrected in v2:* removed claims the paper does not make — that naive
  averaging "always" incurs a barrier (Figure 2 shows small barriers for wide
  MNIST MLPs), that width helps because units "agree by chance", and an IID
  data assumption. The LMC concept previously used a max-of-endpoints
  definition; the paper's Eq. 1 uses the linear interpolation of the
  endpoint losses.

## Open questions

- What is the minimum width H such that random gossip averaging is loss-
  barrier-free?
- Does applying permutation alignment at every gossip step recover sync-SGD
  performance?
- How does alignment complexity (Hungarian matching is O(H^3)) scale in
  gossip?
