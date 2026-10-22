---
status: Active
title: 'Exphormer: Sparse Transformers for Graphs'
version: 1
tags:
- graphs-and-networks
- attention-techniques
- model-architecture
date: '2026-10-22'
published: '2023-03-10'
arxiv: '2303.06147'
first_author: 'Shirzad'
keywords:
- 'exphormer'
- 'sparse-attention'
- 'expander-graphs'
- 'virtual-nodes'
- 'graph-transformer'
- 'graphgps'
implementations: []
compared_against:
- LIT-tmpwijfh
- LIT-tmpynksg
summary: >-
  Shirzad, Velingker, Venkatachalam, Sutherland, Sinop (ICML 2023),
  [ARXIV-2303.06147](https://arxiv.org/abs/2303.06147). Replaces full attention inside GPS with attention over
  the input edges, a random regular expander graph and a few virtual nodes,
  O(|V|+|E|) in all. It beats GPS's Performer and BigBird variants on all
  four datasets compared and full-attention GPS on CIFAR10 (74.7 against
  72.3), and runs ogbn-arxiv (169k nodes), where GPS is out of memory. On
  LRGB it gains most on PCQM-Contact (MRR 0.364 against 0.334). Which
  sparse components help is chosen per dataset: the molecular LRGB models
  use no expander at all.
---

# LIT-tmpf1ndc: Exphormer: Sparse Transformers for Graphs

Shirzad, Velingker, Venkatachalam, Sutherland, Sinop, UBC and Google
(ICML 2023) — [ARXIV-2303.06147](https://arxiv.org/abs/2303.06147)

## Key takeaways

- **The attention graph** (§3.2, Figure 1): each node attends to its
  neighbors in the input graph, to its neighbors in a random d-regular
  expander built from d/2 random permutations, and to a few virtual nodes
  connected to everything. Learned edge-type embeddings tell the three
  apart. It replaces the global attention block of a GPS layer and keeps
  GPS's message-passing block
- **The theory** (§4, Appendix E): a d-regular ε-expander spectrally
  approximates the complete graph, random walks on it mix in O(log n) steps
  and its diameter is O(log n), so O(log n) stacked layers can connect
  every pair. Theorem E.3 gives universal approximation if there is a
  virtual node, or if the expander contains a Hamiltonian path
- **Against other sparse attention** (Table 2): it beats GPS-Performer and
  GPS-BigBird on CIFAR10, MalNet-Tiny, PascalVOC-SP and Peptides-func, and
  full-attention GPS on the first three (PascalVOC-SP F1 0.398 against
  0.374). On Peptides-func it ties it (AP 0.653 against 0.654)
- **LRGB** (Table 3): F1 0.398 on PascalVOC-SP and 0.346 on COCO-SP, MAE
  0.248 on Peptides-struct and MRR 0.364 on PCQM-Contact, against GPS's
  0.375, 0.341, 0.250 and 0.334. All models are near 500k parameters
- **Scale** (Table 4, Remark 5.2): 72.44% on ogbn-arxiv, where GPS and SAN
  run out of memory (the leaderboard best then was 79.66%), and batch size
  256 on MalNet-Tiny where full-attention GPS fails at 16 on a 40 GB A100

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22). Its ablation without the message-passing layer
corroborates [SOTA-tmpy8eal](../practices.d/SOTA-tmpy8eal.md).

**Against GPS.** It is `compared_against` GPS ([LIT-tmpwijfh](LIT-tmpwijfh.md)), whose
framework it runs in and whose attention block it replaces. Its Table 1
and Table 2 GPS rows are GPS's published numbers. The appendix also reruns
GPS in Exphormer's own 5-layer ESLapPE setting, which lifts GPS on CIFAR10
from 72.3 to 73.5 (Table 10), so part of the main-table margin (74.7
against 72.3) is configuration. Exphormer still leads that rerun.

**Its LRGB baselines had the same handicap.** It is `compared_against` the
Long Range Graph Benchmark ([LIT-tmpynksg](LIT-tmpynksg.md)): Table 3 copies every baseline
row from that paper and the GPS row from GPS, so its message-passing
baselines are the untuned, linear-head models [LIT-579](LIT-579.md) later retuned. Its
own hyperparameters were set by a one-at-a-time "linear search" over many
settings (Appendix B.1). The paper predates [LIT-579](LIT-579.md) (arXiv v2, July 2023)
and could not have used the retuned baselines. Comparing numbers across
the two papers, which neither ran: [LIT-579](LIT-579.md)'s tuned GCN (AP 0.686, MAE
0.246) beats Exphormer on both Peptides tasks, and its tuned GPS on
PascalVOC-SP and COCO-SP (F1 0.444 and 0.388) beats Exphormer's 0.398 and
0.346, which were run without feature normalization. [LIT-579](LIT-579.md) prints
Exphormer's reported superpixel scores beside its own, without rerunning
them.

**What the headline omits.** "Exphormer" is not one architecture across the
tables. The ablation (Table 5) shows that the reported model is the best
subset of components per dataset: on PascalVOC-SP the headline 0.398 has no
virtual nodes and the full model scores 0.368; on Peptides-struct the
headline 0.248 has no expander and the full model scores 0.264. The LRGB
configurations (Table 8) use an expander only on the two superpixel sets,
so on Peptides and PCQM-Contact the long-range component is virtual nodes,
not expanders. And without a virtual node the universality theorem needs
the expander to contain a Hamiltonian path, which the Hamiltonian-cycle
construction guarantees and the permutation construction used for the main
tables does not. The superpixel models have no virtual node.

Read — [NOTE-tmpov8kk](../notes.d/NOTE-tmpov8kk.md).
