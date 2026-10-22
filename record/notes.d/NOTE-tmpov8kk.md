---
status: Read
paper: 'LIT-tmpf1ndc'
title: 'Exphormer'
version: 1
date: '2026-10-22'
summary: >-
  Sparse attention over input edges, a random expander and virtual nodes,
  inside GPS. Beats GPS's linear-attention variants and often full
  attention, and scales to 169k-node graphs; which components help varies
  by dataset. Read in full; the cited expander theorems were not checked.
---

# NOTE-tmpov8kk: Exphormer

## Contribution

A sparse attention pattern for graph transformers with linear cost, built
from the graph's own edges, a random regular expander and virtual nodes,
with spectral and universality arguments for why it can stand in for full
attention.

## Key insight

**Sparse attention designed for sequences does not suit graphs; one
designed from the graph does.** An expander has few edges yet behaves
spectrally like the complete graph and has logarithmic diameter, so a few
layers of attention over it can reach every node.

## Key results

- Beats GPS-Performer and GPS-BigBird on all four datasets compared, and
  full-attention GPS on three (Table 2)
- LRGB: PascalVOC-SP 0.398, COCO-SP 0.346, Peptides-func 0.653,
  Peptides-struct 0.248, PCQM-Contact 0.364 (Table 3)
- ogbn-arxiv 72.44% with GCN plus Exphormer, against 71.35% for GCN alone;
  dense GPS is out of memory (Tables 4, 15)
- Per-dataset ablation: expanders help the superpixel graphs and virtual
  nodes the molecular ones, and using both can hurt (Table 5, Appendix D)

## Limitations

- **The headline model differs by dataset**, chosen from the ablation
- **Baselines copied from LRGB and GPS**, with one-at-a-time tuning of
  Exphormer's own settings
- **Universality needs a virtual node or a Hamiltonian path**, which the
  permutation-based expander used in the main tables does not guarantee
- **Gains over full-attention GPS are small** on most datasets, and partly
  configuration (GPS rerun at Exphormer's settings closes about half the
  CIFAR10 gap)
