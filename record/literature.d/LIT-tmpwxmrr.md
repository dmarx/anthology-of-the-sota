---
status: Active
title: 'Sparse Distributed Memory and Related Models'
version: 1
tags:
- model-architecture
- analysis-and-evaluation
date: '2026-09-25'
published: '1992-04-01'
url: 'https://ntrs.nasa.gov/citations/19920021480'
first_author: 'Kanerva'
keywords:
- 'sparse-distributed-memory'
- 'associative-memory'
- 'correlation-matrix-memory'
- 'memory-capacity'
- 'signal-to-noise-ratio'
- 'cerebellum'
- 'cmac'
implementations: []
extends:
- LIT-666
summary: >-
  Kanerva (1992), RIACS TR 92.10, published in 1993 in Hassoun (ed.),
  *Associative Neural Memories* (Oxford). SDM restated as a matrix memory:
  a fixed random address matrix `A`, a wide layer of hard locations, and a
  modifiable contents matrix `C` trained by the outer-product rule. Stored
  words are weighted by the **overlaps of activation sets**. The activation
  probability that maximizes signal-to-noise is **`p = (2MT)^(-1/3)`**, and
  capacity is **about 10% of the number of locations** at one bit error in a
  thousand. This is the source of two of the three optimal radii `LIT-641`
  fits β against. The third, critical distance, is not in it.
extended_by:
- LIT-641
---
<!-- inactive-ok-file: THEORY-097 — Proposed, and named as the account whose
     fitted β this review's signal-to-noise and capacity analyses anchor. The
     note records where those criteria come from; it does not rest on the
     theory being settled. -->

# LIT-tmpwxmrr: Sparse Distributed Memory and Related Models

Kanerva — RIACS Technical Report 92.10, April 1992; published 1993 in M. H.
Hassoun (ed.), *Associative Neural Memories: Theory and Implementation*,
Oxford University Press — <https://ntrs.nasa.gov/citations/19920021480>

## Key takeaways

Read in full from the report version on NASA's Technical Reports Server
(NASA-CR-190553). Its title page says it is to appear in Hassoun's volume.
The published chapter was not compared against it.

- **SDM is a generalized random-access memory.** It has the same three
  registers as a RAM, but with long words (`N = U = 1,000` in the sample
  memory). `2ᴺ` locations cannot be built, so `M` hard locations are placed at
  a random sample of addresses (`M = 1,000,000`). Every location within
  Hamming radius `H` of the address is activated, not just one. A write adds
  the bipolar word into the up-down counters of every active location. A read
  sums the active locations' counters and thresholds each bit at zero, which
  is a majority rule. Set `H = 0`, give every address a location and make the
  counters one bit, and it *is* a RAM.

- **As a matrix memory, the weights are overlaps.** With data addresses `X`,
  activations `Y`, and stored words `W`, the contents are `C = YᵀW` and
  recall is `z(YYᵀW)`. The weight each stored word gets when one is retrieved
  is an entry of `YYᵀ`, the **number of locations the two addresses activate
  in common**. "The purpose of addressing through `A` is to produce (nearly)
  orthogonal activation vectors": if the rows of `Y` are orthogonal, recall
  is perfect. The report credits exact formulas for the overlap to Wang
  (unpublished) and Jaeckel (1988), and says only that it "decreases rapidly
  with increasing distance between the centers of activation."

- **It is a correlation-matrix memory with the input dimension blown up.**
  Anderson's and Kohonen's memories correlate the input variables directly.
  SDM correlates the `M` activation variables instead, taking the input from
  a thousand dimensions to a million. That makes capacity independent of the
  input dimension: "doubling the hardware doubles the number of words of a
  given size that can be stored." The expansion idea is traced to
  Rosenblatt's perceptron.

- **The signal-to-noise optimum.** Treat the overlaps as Poisson and the sum
  as Gaussian. The signal is `μ = pM` and the noise is
  `σ² = pM[1 + pT(1 + p²M)]`, so bit-fidelity is `Φ(μ/σ)`. Maximizing `μ/σ`
  gives **`p = (2MT)^(-1/3)`** as the best probability of activating a
  location. That value is optimal only for exact retrieval addresses. For
  noisy ones `p` should be "somewhat larger (typically, less than twice as
  large)", and for clustered data smaller. The noisy-address analysis is
  stated as a result and not carried out.

- **Capacity is about 10% of the locations.** Asymptotically,
  `T_max/M → 1/[Φ⁻¹(φ)]²`. That is 0.105 at fidelity `φ = 0.999`, and 0.096
  for the finite million-location memory. Keeler (1988) showed SDM and the
  outer-product Hopfield net have the same capacity per storage element, and
  the Hopfield `0.15N` corresponds to `φ = 0.995`. The practical guide is 1–5%
  of the number of hard locations, since noisy cues cost capacity.

- **It is a two-layer feed-forward net that is not trained like one.** `A`
  is the first layer's weights, fixed and binary. `C` is the second's. The
  hidden layer is far wider than the input, the reverse of a
  back-propagation net's, and activation is a step function that is mostly
  zeros. Training is fast, single-trial if need be. The cost is that
  applying it to a new problem "requires choosing an appropriate data
  representation": nothing learns one.

- **The cerebellum, with its discrepancies stated.** Mossy fibres are the
  address and granule cells the address decoders. The parallel-fibre
  synapses with Purkinje cells are the counters, and climbing fibres bring
  in the data bits. The cell counts fit, by Loebner's figures for the cat:
  billions of granule cells, about a hundred thousand parallel fibres through
  each Purkinje cell. **But a granule cell receives only three to five mossy
  fibres**, so activation there cannot be Hamming distance from a full
  address. That is Jaeckel's selected-coordinate design and Marr's and
  Albus's models, which the chapter covers next.

## Standing in the anthology

Filed as the second of two sources behind `THEORY-097`'s fitted β, and read
in full, unlike `LIT-666`.

**The finding is an attribution.** `LIT-641` §1 names three optimal
Hamming radii and cites this review for two of them. The **signal-to-noise**
optimum and the **memory-capacity** analysis are here (§3.6, §3.7). The
report also uses the more accurate variance, `σ² = pM[1 + pT(1 + p²M)]`,
which `LIT-641` Appendix B.4 notes replaces the book's. **Critical distance
is not here.** The report derives no convergence radius. It shows iterated
retrieval converging only in two figures, and defers noisy-address analysis
to Chou (1989). `LIT-641`'s own Appendix B.5 reproduces the critical-distance
curve as "Figure 7.3 from the SDM book", so it belongs to `LIT-666`. The
§1 citation of this review for it is a mis-citation, and the appendix gives
the right one. It does not move `LIT-641`'s result, which fits β against all
three wherever they come from.

This is `DP-010` in a small way: the travelled sentence cites the review,
and the source that actually has it is in the appendix.

What it offers the record beyond that is the matrix form. `z(YYᵀW)`, with
weights that are overlap sizes, is the shape `LIT-641` maps onto attention.
It is stated plainly here, more than two decades before attention.

Nothing here moves a practice.
