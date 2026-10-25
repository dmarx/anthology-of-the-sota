---
number: 403
status: Read
formerly:
- NOTE-tmphp27d
paper: 'LIT-816'
title: 'Deeper insights into GCNs'
version: 1
date: '2026-10-22'
summary: >-
  A GCN layer is symmetric Laplacian smoothing. Repeated smoothing converges
  to a degree-scaled constant on each connected component, which is
  over-smoothing. The depth evidence is an untrained network on the karate
  club. Co- and self-training help GCNs at very low label rates. Read in
  full.
---

# NOTE-403: Deeper insights into GCNs

## Contribution

The first account of why GCN works, and of why it cannot simply be made
deep. It also offers two label-expansion methods for when labels are very
scarce.

## Key insight

**Graph convolution helps for the same reason it eventually hurts.**
Averaging over neighbours makes nodes in a cluster alike, which is what
separates the classes. Repeat the averaging and the clusters blur into each
other, until each connected component carries one vector scaled by degree.

## Key results

- Cora, 20 labels per class (Table 1): FCN 53.1 / 55.9, GCN 70.8 / 79.8
  for one / two layers
- Theorem 1: (I − αL_rw)^m and (I − αL_sym)^m converge to the
  component-indicator subspace (scaled by D^{-1/2} for L_sym) when no
  component is bipartite, for α ∈ (0, 1]
- Figure 2: untrained GCNs on the karate club separate the two classes at
  2 layers and mix them at 3–5
- Tables 3–5, mean of 50 runs (10 on PubMed): at a 1% label rate,
  Union reaches 69.9 on Cora and 59.1 on CiteSeer, against GCN+V's 62.3
  and 55.3. At 0.05% on PubMed, co-training reaches 68.3 against 57.5
- Table 6 (20 labels per class): on Cora the four methods are within a
  point of GCN+V (79.6–80.5 against 80.3). On Pubmed they are 0.8–2.2
  below it, and on CiteSeer only Intersection is above (69.9 against 68.9)

## Limitations

- **The theorem has no weights or nonlinearity.** It describes repeated
  smoothing, not a trained GCN
- **The depth evidence is qualitative.** One untrained network on 34 nodes.
  The paper attributes the accuracy loss of its own deeper trained models to
  overfitting, not to the theorem
- **The improvement percentages are relative.** "23% over GCN-V" at a 1%
  label rate on Cora is 56.9 → 69.9 points
- **Planetoid-era protocol.** Random splits with 1,000 test nodes, and
  hyperparameters copied from Kipf and Welling
