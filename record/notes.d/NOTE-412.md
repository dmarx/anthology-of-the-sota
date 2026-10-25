---
number: 412
status: Read
formerly:
- NOTE-tmpqyoo1
paper: 'LIT-814'
title: 'GraphSAGE'
version: 1
date: '2026-10-22'
summary: >-
  Learned aggregators over a sampled, fixed-size neighborhood give node
  embeddings for unseen nodes and graphs, beating raw features and
  DeepWalk on three inductive benchmarks. The trainable aggregators beat a
  GCN-style mean in a six-setting test. Every cell is a single run. Main
  text read in full, appendix skimmed.
---

# NOTE-412: GraphSAGE

## Contribution

An inductive formulation of graph convolution: a learned function that
embeds a node from its sampled neighborhood, rather than a lookup table
of per-node embeddings. Neighbor sampling bounds the per-batch cost, which
made the method usable on graphs with hundreds of thousands of nodes.

## Key insight

**Learn the aggregation, not the embedding.** A function of a node's
features and its neighbors' features transfers to nodes and graphs it
never saw. A trained embedding table does not, and re-fitting it for each
new node is what makes DeepWalk 100–500× slower at test time.

## Key results

- Supervised micro-F1 on unseen nodes (Table 1), citation / Reddit / PPI:
  raw features 0.575 / 0.585 / 0.422, DeepWalk + features 0.701 / 0.691 /
  n.a., GraphSAGE-pool 0.839 / 0.948 / 0.600, GraphSAGE-LSTM 0.832 / 0.954
  / 0.612
- The GCN-style aggregator trails the others (0.772 / 0.930 / 0.500). LSTM,
  pool and mean each beat it in a Wilcoxon test over six settings
  (p = 0.02). LSTM against pool is not significant (p = 0.46), and LSTM is
  about 2× slower
- Unsupervised GraphSAGE, trained with a random-walk co-occurrence loss, is
  close to supervised on Reddit (0.907 against 0.954 for LSTM)
- K = 2 layers beat K = 1 by 10–15%. Larger sampled neighborhoods show
  diminishing returns (Figure 2B)

## Limitations

- **Single runs.** No seeds, no spread, and hyperparameter ranges chosen on
  held-out subsets of two of the three datasets
- **The significance test is underpowered**, as the authors say: six
  settings, three datasets
- **Uniform sampling only.** Non-uniform samplers are left to future work
- **The concatenation and the aggregator are confounded** in the
  comparison with GraphSAGE-GCN, which differs in both
