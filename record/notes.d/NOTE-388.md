---
number: 388
status: Read
formerly:
- NOTE-tmp6bkgl
paper: 'LIT-843'
title: 'Graphormer'
version: 1
date: '2026-10-22'
summary: >-
  A plain Transformer becomes a strong graph model once attention is
  biased by shortest-path distance and edge features and inputs carry node
  degree. The encodings cut PCQM4M-LSC error from 0.228 to 0.130 in the
  ablation. Read in full, appendices included.
---

# NOTE-388: Graphormer

## Contribution

The first graph transformer to top a large graph-level leaderboard
(OGB-LSC PCQM4M), with three structural encodings that let an unmodified
Transformer encoder use graph structure.

## Key insight

**Put the graph into the attention scores, not only into the node
features.** A learned bias per shortest-path distance lets every head
choose how far to look, down to masking all but the neighbors, which is
why message-passing layers are a special case.

## Key results

- PCQM4M-LSC validation MAE 0.1234 (47.1M parameters) against 0.1395 for
  GIN-VN (6.7M) (Table 1)
- Ablation: no encodings 0.2276, spatial 0.1427, plus centrality 0.1396,
  plus edge bias 0.1304; Laplacian PE alone 0.1483 (Table 5)
- ZINC MAE 0.122 at 489k parameters (Table 4)
- MolPCBA 31.39 and MolHIV 80.51 after pre-training on PCQM4M-LSC and
  FLAG augmentation (Tables 2–3)

## Limitations

- **Model sizes are not matched** except on ZINC, and the OGB results use
  pre-training the baselines mostly lack
- **The ablation is short** (100k of 1M steps) and on one dataset
- **Expressiveness is by construction and one example**, not a hierarchy
  result
- **Quadratic in the number of nodes**, plus all-pairs shortest paths
