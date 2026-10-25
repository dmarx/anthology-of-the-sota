---
status: Read
paper: 'LIT-tmpmiegg'
title: 'LSPE'
version: 1
date: '2026-10-22'
summary: >-
  Random-walk return probabilities make a strong positional encoding with no
  sign ambiguity, and most of the ZINC gain comes from putting them at the
  input. A learnable positional channel adds a smaller, slower gain. OGB
  gains are under 2%. Main text and the experimental appendices read; the
  related-work and model-equation appendices skimmed.
---

# NOTE-tmp40ei9: LSPE

## Contribution

RWPE, a cheap positional encoding from a node's k-step return
probabilities, and LSPE, an architecture that carries a positional state
alongside the structural one and updates both in every layer.

## Key insight

**Give the network a coordinate that needs no symmetry learned around
it.** Laplacian eigenvectors are unique per node but carry an arbitrary
sign, so a network must learn 2^k sign flips. RWPE is not always unique,
but is well defined and, on molecules, mostly distinct per node. On ZINC
the second wins clearly.

## Key results

- ZINC, GatedGCN (Table 3): no PE 0.251, LapPE 0.202, RWPE at input 0.122,
  RWPE with LSPE 0.100, with final concatenation 0.093. RWPE at the final
  layer only, 0.249. The positional loss gives 0.090 (Table 1)
- ZINC, other models (Table 1): PNA 0.141 to 0.095, SAN 0.181 to 0.104,
  GraphiT 0.181 to 0.106. Sparse GNNs beat transformers
- OGB (Table 1): MOLTOX21 and MOLPCBA gains of 0.003–0.006 AUC or AP
- Uniqueness (§A.3): RWPE is not unique for every node. For example, 30
  ZINC validation graphs with 24 nodes have 21 distinct encodings each
  (87.5%). Best k is 20 for ZINC and 16 for MOLTOX21
- IMDB-B, IMDB-M, CIFAR10 superpixels: gains of 0.7–4.0 points (Table 4)

## Limitations

- **The named contribution is the smaller effect.** The learnable channel
  takes 0.122 to 0.093 on ZINC, and costs about 1.7× epoch time
- **The reason RWPE beats LapPE is asserted, not isolated.** Sign
  ambiguity and information content change together in Table 3
- **One benchmark carries the result.** ZINC's features are bare atom and
  bond types. Where features already encode rings (OGB), gains shrink
- **Four seeds,** and the CIFAR10 baseline is taken from an earlier paper
