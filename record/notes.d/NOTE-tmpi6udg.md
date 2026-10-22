---
status: Skimmed
paper: LIT-tmp1wiuo
title: 'GraphCL'
version: 1
date: '2026-10-22'
summary: >-
  SimCLR-style contrastive pre-training for graph-level GNNs with four graph
  augmentations. Augmentation is necessary and its best choice depends on
  the domain; gains are modest and mixed in transfer. Main text and all
  tables read; Appendices A–G, including the mutual-information derivation
  and node-classification results, not read.
---

# NOTE-tmpi6udg: GraphCL

## Contribution

Four graph augmentations, a contrastive framework that uses them for GNN
pre-training, and a systematic study of which pairs of augmentations help on
which kinds of graphs, in semi-supervised, unsupervised, transfer and
adversarial settings.

## Key insight

**An augmentation encodes a claim about what does not change a graph's
label, and that claim is domain knowledge.** Dropping a node or taking a
subgraph is safe almost everywhere it was tried. Perturbing edges is safe
for social networks and not for molecules, where an edge is a bond. Pairing
two different augmentations makes the contrastive task harder, its loss
falls more slowly, and it helps more.

## Key results

- No augmentation: contrastive pre-training is often worse than none
  (Figure 2)
- Best augmentation pair over training from scratch, 10% labels: +2.10
  NCI1, +3.15 PROTEINS, +7.11 COLLAB, +1.85 RDT-B (§4.1)
- Edge perturbation lowers NCI1 accuracy at every perturbation ratio tried
  (Figure 4A)
- Transfer ROC-AUC: best mean on 4 of 9 tasks, below no pre-training on
  Tox21, ToxCast and MUV (Table 5)

## Limitations

- **Augmentation pools were chosen per data category** from the analysis
  section, on datasets that are also in the comparison
- **Copied baselines** in the unsupervised and transfer tables
- **Small benchmarks** with spreads that overlap the best result in many
  cells
- **Not read**: the appendices, so the mutual-information argument and the
  node-classification results are not assessed here
