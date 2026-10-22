---
status: Proposed
promote_when: >-
  An independent group adds a fully adjacent last layer, or another global
  last step such as a virtual node, to message-passing models on a
  graph-level task with long-range dependencies, retunes both arms under
  the same budget, and reports the gain together with a matched-cost
  alternative such as a wider model or a deeper readout. Re-running the
  source's untuned QM9 configurations does not satisfy this, nor does a
  node-classification result on short-range graphs.
consensus: unreplicated
consensus_note: >-
  One group's result, on published configurations it did not retune. The
  largest effect is on QM9. Topping et al. (LIT-tmp0hkly) ran the same
  layer as a baseline on node classification and found it mixed: best on
  Cornell and Pubmed, 1.8 points worse than nothing on Citeseer. That is a
  different setting, not a replication. Whether global layers or virtual
  nodes are now standard on long-range graph tasks has not been assessed
  here.
title: 'On a graph-level task that depends on interactions between distant nodes, make the last message-passing layer fully adjacent before reaching for a wider model'
version: 1
tags:
- graphs-and-networks
- model-architecture
date: '2026-10-22'
source:
- LIT-tmpt6hyo
introduced_by:
- LIT-tmpt6hyo
implementations:
- 'tech-srl/bottleneck'
summary: >-
  Alon and Yahav (2020), [LIT-tmpt6hyo](../literature.d/LIT-tmpt6hyo.md) — in the last layer only, connect
  every pair of nodes, keeping the layer type, the weights and the
  hyperparameters. On QM9, with eight-layer models tuned by Brockschmidt,
  this cut mean error by 42% across six GNNs, where doubling the width cut
  it by 5.5%. On NCI1 and VarMisuse the gains are mostly within one
  standard deviation. Making every layer fully adjacent was far worse.
  Proposed: one group, no retuning, and a quadratic cost in the last layer.
explained_by:
- THEORY-tmpk02h3
---

# SOTA-tmps0jek: On a graph-level task that depends on interactions between distant nodes, make the last message-passing layer fully adjacent before reaching for a wider model

## Source

Alon and Yahav (2020), [LIT-tmpt6hyo](../literature.d/LIT-tmpt6hyo.md). Read as [NOTE-tmp198gc](../notes.d/NOTE-tmp198gc.md). The reason is
[THEORY-tmpk02h3](../theory.d/THEORY-tmpk02h3.md).

## The practice

Alon and Yahav ([LIT-tmpt6hyo](../literature.d/LIT-tmpt6hyo.md)) took GNNs that Brockschmidt had tuned over
500 configurations for QM9 and changed one thing: in the K-th layer, every
node is a neighbour of every other. With the original code, configuration
and five seeds per target, mean relative error fell by 39.5% for R-GIN,
44.6% for R-GAT and 47.4% for GGNN, and by 42% over six GNN types.

- **Change the last layer only.** The first K − 1 layers keep the
  molecular graph. With every layer fully adjacent, GCN's error on QM9
  rose by more than 1500%
- **Prefer it to more width.** Doubling GCN's hidden size from 128 to 256
  cut error by 5.5%, against 43.4% for the fully adjacent layer at the
  original size. Di Giovanni et al. ([LIT-tmpggqnq](../literature.d/LIT-tmpggqnq.md)) prove why: width
  multiplies every node pair's sensitivity alike
- **Prefer it to more depth when the graphs are already covered.** QM9
  models used 8 layers, and 90% of graphs have diameter 8 or less. Ten
  layers gave no gain
- **Half the edges keep most of it.** A random half of the fully adjacent
  edges cut error by 31.5%, and a quarter by 8.4%

## Conditions

- **Graph-level tasks with long-range dependencies.** The large effect is
  on QM9, where targets depend on atoms on opposite sides of a molecule.
  GIN on ENZYMES gained 8.1 points, but the averaged gains on NCI1 (4.8%
  less error) and VarMisuse are mostly within one standard deviation
- **Not for short-range node classification.** In Topping et al.'s
  ([LIT-tmp0hkly](../literature.d/LIT-tmp0hkly.md)) GCN experiments the same layer helped several
  heterophilic graphs and cost 1.8 points on Citeseer
- **Cost.** The last layer is quadratic in the number of nodes. QM9
  molecules have about 18
- **Untuned on purpose.** The source kept the base hyperparameters to rule
  out tuning as the cause. A retuned comparison, as [SOTA-349](SOTA-349.md) asks for
  graph transformers, has not been run here
