---
status: Active
title: 'Neural Message Passing for Quantum Chemistry'
version: 1
tags:
- graphs-and-networks
- model-architecture
- biomolecular-modeling
- physical-sciences
date: '2026-10-22'
published: '2017-04-04'
arxiv: '1704.01212'
first_author: 'Gilmer'
keywords:
- 'mpnn'
- 'message-passing'
- 'qm9'
- 'molecular-property-prediction'
- 'set2set'
- 'virtual-node'
implementations: []
summary: >-
  Gilmer, Schoenholz, Riley, Vinyals, Dahl (ICML 2017), [ARXIV-1704.01212](https://arxiv.org/abs/1704.01212).
  Message Passing Neural Networks name the common form of eight earlier
  graph models: T rounds of messages summed over neighbors, a node update,
  and a permutation-invariant readout. An MPNN with edge-network messages,
  set2set readout and explicit hydrogens reaches chemical accuracy on 11 of
  13 QM9 targets, with an average error ratio of 0.68 against 1.35 for the
  best hand-engineered baseline. That is one random split, with no
  repeated runs.
extended_by:
- LIT-tmp0mr1k
---

# LIT-tmpk1b2y: Neural Message Passing for Quantum Chemistry

Gilmer, Schoenholz, Riley, Vinyals, Dahl, Google Brain, Google and
DeepMind (ICML 2017) — [ARXIV-1704.01212](https://arxiv.org/abs/1704.01212)

## Key takeaways

- **The framework** (Eqs. 1–3): m_v = Σ_{w∈N(v)} M_t(h_v, h_w, e_vw),
  h_v ← U_t(h_v, m_v), and ŷ = R({h_v^T}) with R invariant to node order.
  Duvenaud's fingerprints, gated graph networks, interaction networks,
  molecular graph convolutions, deep tensor networks and the Laplacian
  methods, GCN among them, are each written as a choice of M, U and R
- **The best variant** (§5, §8): an "edge network" message A(e_vw)·h_w, in
  which a network maps the edge vector to a d × d matrix, a GRU update with
  weights tied across steps, and a set2set readout. Explicit hydrogen
  nodes and the full edge vector (bond type plus distance) mattered for
  several targets
- **QM9** (Table 2, error ratio = MAE ÷ chemical accuracy, below 1 is
  accurate): the single best model averages 0.68 and is below 1 on 11 of
  13 targets. A five-model ensemble averages 0.52. The best of five
  hand-engineered baselines (HDAD) averages 1.35, GG-NN 1.36
- **Without spatial input** (Table 3): GG-NN 3.47, + virtual edges 2.90, +
  a master node 2.62, + set2set 2.57. These runs used a partial-charge
  input that is itself a DFT output, so they are not deployable settings
- **Per-target training** beat joint training on all 13 targets by up to
  40%. A "towers" variant, k smaller copies mixed each step, helped on 12
  of 13 targets

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22).

<!-- inactive-ok-block: SOTA-tmpzd1sw — Proposed, and named as the practice this paper sources, not relied on -->
The framework, more than the QM9 result, is what this record holds the
paper for. Its reformulation of GCN ([LIT-582](LIT-582.md)) as a message function
c_vw·h_w, with c_vw = (deg(v)·deg(w))^{-1/2}·A_vw, is the frame the later
graph documents here use. The graph-network framework filed alongside it
([LIT-tmp0mr1k](LIT-tmp0mr1k.md)) generalizes it with edge and global updates. Its master
node is the "virtual node" that OGB's molecular baselines add
([LIT-tmp3qfj0](LIT-tmp3qfj0.md)), and it sources [SOTA-tmpzd1sw](../practices.d/SOTA-tmpzd1sw.md).

**What "chemical accuracy" means here.** It is measured against DFT
labels, not experiment. For HOMO the stated DFT error is 2.0 eV and
chemical accuracy is 0.043 eV, so matching DFT to chemical accuracy is not
matching nature, which the paper says plainly. All results are on one
random 10k/10k validation/test split, with 50 random hyperparameter trials
per target and no repeated seeds.

Read — [NOTE-tmp2catj](../notes.d/NOTE-tmp2catj.md).
