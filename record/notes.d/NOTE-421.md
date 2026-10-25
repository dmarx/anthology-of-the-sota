---
number: 421
status: Read
formerly:
- NOTE-tmpz3kcn
paper: LIT-806
title: 'Deep Graph Infomax'
version: 1
date: '2026-10-22'
summary: >-
  Contrasting node embeddings against a graph summary, with feature-shuffled
  graphs as negatives, trains GNN encoders without labels to linear-probe
  accuracy near supervised GCN on the citation graphs. An untrained encoder
  is nearly as good on Reddit and PPI. Read in full, appendices included.
---

# NOTE-421: Deep Graph Infomax

## Contribution

A self-supervised objective for GNN encoders that does not use random walks:
discriminate (node, summary) pairs from the real graph against pairs whose
node comes from a corrupted copy. It works transductively and inductively,
including on unseen graphs.

## Key insight

**Shuffling features across positions keeps every feature and every edge
but breaks which features sit where, so telling real from shuffled forces
the encoder to encode how a node's features relate to its neighborhood.**
The global summary gives the discriminator a reference point that is the
same for all nodes. Appendix B finds the encoder spends some dimensions on
pushing negatives down and keeps class information in the rest.

## Key results

- Linear probe accuracy: Cora 82.3 ± 0.6, Citeseer 71.8 ± 0.7, Pubmed
  76.8 ± 0.6, against copied supervised GCN figures of 81.5, 70.3 and 79.0
  (Table 2)
- Reddit micro-F1 0.940 and PPI 0.638, against 0.908 and 0.502 for the best
  unsupervised GraphSAGE (Table 2)
- Random-Init: 69.3, 61.9, 69.6 transductively; 0.933 Reddit, 0.626 PPI
  (Table 2)
- Removing the least class-relevant half of the 512 dimensions keeps
  accuracy near supervised GCN on Cora (Figure 6)

## Limitations

- **The inductive gains over an untrained encoder are small**: 0.007 on
  Reddit and 0.012 on PPI
- **The theory is for finite input sets and injective readouts**; the
  authors present it as intuition
- **Single Planetoid split** for the citation graphs, with baselines copied
  from earlier papers
- **The mean readout** is expected by the authors to weaken on larger graphs
- **Different encoders per setting** (1-layer GCN, 3-layer mean-pool with
  skips, dense skips on PPI), each chosen by the authors
