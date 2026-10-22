---
status: Read
paper: 'LIT-tmpafjtk'
title: 'SignNet and BasisNet'
version: 1
date: '2026-10-22'
summary: >-
  Networks invariant to eigenvector sign (SignNet) and basis (BasisNet) by
  construction. On ZINC, a graded ablation puts the sign symmetry at the
  center of why raw Laplacian encodings underperform. BasisNet is never
  tested on a real graph task. Main text and experimental appendices read;
  the universality proofs skimmed.
---

# NOTE-tmpoxv45: SignNet and BasisNet

## Contribution

A characterization of continuous functions invariant to eigenvector sign
and basis choice, practical architectures built from it, and a proof that
these architectures subsume spectral graph convolutions and several earlier
graph positional encodings.

## Key insight

**Make the symmetry part of the architecture instead of an augmentation.**
`φ(v) + φ(−v)` is sign invariant for any φ, and `VVᵀ` is invariant to the
choice of basis. Random sign flipping asks the network to learn invariance
to 2^k configurations from samples. Processing each eigenvector separately
cuts that to 2, and the sum cuts it to none.

## Key results

- Universality of the unconstrained forms (Corollary 2, via a product-group
  decomposition, Theorem 1). The permutation-equivariant forms are not
  universal (Table 4)
- ZINC ablation, GatedGCN, k = 8 (Table 1): LapPE with flips 0.198,
  absolute values 0.204, canonical sign 0.298, `φ(v)` without the sum
  0.148, SignNet 0.121. All eigenvectors: 0.100
- GINE and PNA: LapPE with flips does no better than no PE; SignNet
  improves both. Best ZINC 0.084, ZINC-full 0.024 (Table 2)
- No edge features (Table 7): GIN 0.348 to 0.238, GAT 0.464 to 0.243
- Overhead: 8.2 s to 10.6 s per training iteration for GatedGCN, and
  eigenvectors for all of ZINC in 15 s

## Limitations

- **BasisNet is not tested on a real graph task,** only on fitting
  synthetic spectral filters with no test set (Appendix J.3)
- **Sign invariance alone is admitted to be insufficient** on graphs with
  repeated eigenvalues, which are most graphs in the datasets used
- **The best rows change the encoder and the number of eigenvectors
  together**
- **Four seeds,** and baselines in Table 2 are quoted from their papers
