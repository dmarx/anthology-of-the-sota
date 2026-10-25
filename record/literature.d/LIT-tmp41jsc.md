---
status: Active
title: 'The Surprising Power of Graph Neural Networks with Random Node Initialization'
version: 1
tags:
- graphs-and-networks
- representation-and-encoding
- analysis-and-evaluation
date: '2026-10-22'
published: '2020-10-02'
arxiv: '2010.01179'
first_author: 'Abboud'
keywords:
- 'random-node-initialization'
- 'random-features'
- 'universality'
- 'expressive-power'
- 'weisfeiler-leman'
- 'synthetic-benchmark'
implementations: []
compared_against:
- LIT-tmptu505
- LIT-tmp6ppm0
summary: >-
  Abboud, Ceylan, Grohe, Lukasiewicz (IJCAI 2021), [ARXIV-2010.01179](https://arxiv.org/abs/2010.01179). A
  message-passing GNN with global readout whose initial node features are
  partly random can approximate any invariant function on graphs of a fixed
  size, with high probability, and stays invariant in expectation. On EXP,
  a synthetic set of 1-WL-indistinguishable pairs, a GCN with random
  initialization scores 96.6–98.0% against 50% without it. It converges far
  slower than a 3-WL-class GCN, needs delicate tuning, and is evaluated on no
  real benchmark.
---

# LIT-tmp41jsc: The Surprising Power of Graph Neural Networks with Random Node Initialization

Abboud, Ceylan, Grohe, Lukasiewicz, Oxford and RWTH Aachen (IJCAI 2021) —
[ARXIV-2010.01179](https://arxiv.org/abs/2010.01179)

## Key takeaways

- **Universality** (Theorem 1): for every invariant `f` on graphs of at
  most n nodes and every ε, δ, some MPNN with random node initialization
  (RNI) is within ε of `f` with probability at least 1 − δ. The proof
  individualizes nodes with the random values and then uses the fact that
  every sentence of two-variable counting logic can be computed by an MPNN
  with global readout. It holds with only one randomized dimension
- **The size of the construction** (Remark 1): the network is a disjunction
  over every individualized graph on which `f` is true, which the authors
  call "prohibitively large". The theorem is an existence result, not a
  recipe
- **EXP** (Table 1, 600 pairs, 10-fold CV): GCN-RNI 96.6–98.0% across four
  noise distributions, a plain GCN 50%, 3-GCN 99.7%. PPGN and the
  1-2-3-GCN-L of Morris et al., both higher-order models, score 50.0%
- **Partial randomization is better** (Figure 2): on CEXP, where half the
  pairs are distinguishable by 1-WL, fully random GCN-RNI stays below 60% on
  that half. Randomizing 12.5–87.5% of dimensions does best
- **The cost:** GCN-RNI needs over 100 epochs where 3-GCN needs about 10,
  and test accuracy varies widely across folds until about epoch 200
  (Figure 4). The authors report it "highly sensitive" to learning rate,
  activation and noise distribution

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22). It is `compared_against` Morris et al.
([LIT-tmptu505](LIT-tmptu505.md)): the 1-2-3-GCN-L from that paper is a baseline on EXP and
scores 50.0%. The authors attribute this to its relaxation to connected
node triples, which discards the disconnected triples where the EXP pairs
differ.

**What the evidence covers.** Every experiment is on EXP and CEXP, which
the authors built. The claim that partial RNI does not hurt on real data
is cited from earlier work, not measured here. Two later papers in the
record do measure it. In the TUD table of Bevilacqua et al.
([LIT-tmp6ppm0](LIT-tmp6ppm0.md)), an RNI model scores below plain GraphConv on PROTEINS (73.3
vs 73.9) and NCI1 (82.1 vs 82.4). On ZINC, Bouritsas et al. ([LIT-tmpo8g4p](LIT-tmpo8g4p.md))
report an MPNN with random features at 0.322 MAE against 0.254 without
them, though that model follows Sato et al.'s random features
([ARXIV-2002.03155](https://arxiv.org/abs/2002.03155)), the earlier work this paper builds on.

**"SAT" is narrower than it sounds.** EXP is framed as a satisfiability
task, but by construction the added planar component is always
satisfiable and the core pair alone decides the label. What a model has to
learn is to tell two fixed core structures apart.

Read — [NOTE-tmpeq1tm](../notes.d/NOTE-tmpeq1tm.md).
