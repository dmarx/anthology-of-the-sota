---
status: Active
title: 'On the Bottleneck of Graph Neural Networks and its Practical Implications'
version: 1
tags:
- graphs-and-networks
- model-architecture
- analysis-and-evaluation
date: '2026-10-22'
published: '2020-06-09'
arxiv: '2006.05205'
first_author: 'Alon'
keywords:
- 'over-squashing'
- 'bottleneck'
- 'long-range-interaction'
- 'fully-adjacent-layer'
- 'problem-radius'
implementations:
- 'tech-srl/bottleneck'
summary: >-
  Alon, Yahav (ICLR 2021), [ARXIV-2006.05205](https://arxiv.org/abs/2006.05205). A node's receptive field grows
  exponentially with depth, and its messages must squeeze into a fixed-size
  vector. The paper calls this over-squashing. On a synthetic tree task,
  GCN and GIN stop fitting the training set at depth 4 (GCN 70%), and GAT
  and GGNN at depth 5. Making only the last layer fully adjacent, with no
  new weights and no retuning, cuts QM9 error by 42% on average over six
  GNNs, against 5.5% from doubling the width. The gains on NCI1, ENZYMES
  and VarMisuse are smaller and often within one standard deviation.
compared_against:
- LIT-tmp0hkly
extended_by:
- LIT-tmp0hkly
---

<!-- inactive-ok-file: SOTA-tmps0jek — the practice this paper is the source of, Proposed until a second group reproduces the fully-adjacent result -->

# LIT-tmpt6hyo: On the Bottleneck of Graph Neural Networks and its Practical Implications

Alon and Yahav, Technion (ICLR 2021) — [ARXIV-2006.05205](https://arxiv.org/abs/2006.05205)

## Key takeaways

- **The bottleneck** (§3): a task with problem radius r needs at least r
  layers to avoid under-reaching. The receptive field then grows
  exponentially in r, and the information from all of it has to pass
  through fixed-length node vectors
- **Tree-NeighborsMatch** (§4.1, Figure 3): a binary tree of depth r with
  the target at the root, solvable in principle. Training accuracy: GCN and
  GIN fit r ≤ 3 perfectly and GCN reaches 70% at r = 4. GAT and GGNN fit
  r = 4, and at r = 5 no GNN fits the data. The paper's explanation is
  that GAT and GGNN can ignore the irrelevant half of the incoming edges at
  the last step
- **A hidden-size bound** (§5, Figure 4): to tell apart all the label
  arrangements, 2^{32d} > (2^r)!/2^{2^r−1}, so d = 32 cannot fit r > 7.
  Empirically, even d = 512 fits r = 7 at most
- **The fully adjacent last layer** (§4.2–4.4): connect every pair of nodes
  in the K-th layer only, keeping the layer type, the weights and the
  original hyperparameters. QM9 (Table 1, 5 seeds): relative error falls by
  39.5% for R-GIN, 44.6% for R-GAT and 47.4% for GGNN, and by 42% averaged
  over six GNNs
- **Controls on QM9** (§4.2, Appendix B): doubling the hidden size gives
  5.5%, so width is not the fix. Ten layers instead of eight give no gain,
  so reach is not the fix: 90% of graphs have diameter ≤ 8, and the models
  use 8 layers. Making every layer fully adjacent gives more than 1500%
  higher error, so the graph matters. Half the edges in the last layer
  give 31.5%
- **Other benchmarks** (Tables 2 and 3): GIN on ENZYMES goes from 59.6 to
  67.7, and on NCI1 from 80.0 to 81.5. Averaged over GNNs, error falls 12%
  on ENZYMES and 4.8% on NCI1. On VarMisuse every model gains on
  SeenProjTest, and R-GCN+FA sets 88.4 and 83.8. Two models drop on
  UnseenProjTest

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22). It names over-squashing and separates it from
over-smoothing (Appendix E). Over-smoothing can occur with no
over-squashing, as on a triangle, and over-squashing with no
over-smoothing, as in the tree task.

**What the fully adjacent layer measures.** The paper says it cannot
measure over-squashing directly, so it measures whether "breaking the
bottleneck" helps. The QM9 gain is large and controlled for width, reach
and tuning. It is evidence that a global interaction step helps those
models on that task, and the bottleneck reading is the paper's
interpretation. Several of the largest QM9 drops are on targets whose base
error has a standard deviation larger than its mean (U for R-GIN:
18.71 ± 23.36). On NCI1 and VarMisuse most gains are within one standard
deviation. It sources [SOTA-tmps0jek](../practices.d/SOTA-tmps0jek.md).

**Formalized and retested by Topping et al.** ([LIT-tmp0hkly](LIT-tmp0hkly.md)), who bound
the Jacobian between distant nodes and run +FA as a baseline for node
classification. There it helps on several heterophilic graphs and loses
1.8 points on Citeseer. Di Giovanni et al. ([LIT-tmpggqnq](LIT-tmpggqnq.md)) prove the
paper's point about width: it raises the sensitivity bound for the whole
network, not for the pairs the topology starves. The account is
[THEORY-tmpk02h3](../theory.d/THEORY-tmpk02h3.md).

Read — [NOTE-tmp198gc](../notes.d/NOTE-tmp198gc.md).
