---
number: 418
status: Read
formerly:
- NOTE-tmpx964a
paper: LIT-809
title: 'node2vec'
version: 1
date: '2026-10-22'
summary: >-
  A two-parameter biased random walk generalizes DeepWalk. With p and q
  tuned on labels it gains 22% Macro-F1 on BlogCatalog and Wikipedia and 1.3%
  on PPI, and node-pair features from it beat link-prediction heuristics.
  Read in full.
---

# NOTE-418: node2vec

## Contribution

A second-order random walk whose return and in-out parameters interpolate
between local and outward exploration, with DeepWalk as the case p = q = 1,
and the first use of skip-gram node embeddings for link prediction, by
combining the two endpoint vectors with an element-wise operator.

## Key insight

**Which neighborhood a node's context should be is a property of the task,
so make it a hyperparameter.** Staying local captures structural roles, and
wandering out captures communities. The paper's evidence for the mapping is
a 77-node illustration (Les Misérables), and its evidence that the choice
matters is the spread in best (p, q) across three datasets.

## Key results

- Macro-F1 at 50% labeled: BlogCatalog 0.2581 against DeepWalk 0.2110,
  Wikipedia 0.1552 against 0.1274, PPI 0.1791 against 0.1768 (Table 2)
- Link prediction with the Hadamard operator: AUC 0.9680 on Facebook (tied
  with DeepWalk), 0.7719 on PPI, 0.9366 on arXiv, against 0.8289, 0.7126 and
  0.8315 for Adamic-Adar (Table 4)
- Performance saturates near d = 100 and grows with walks per node and walk
  length (Figure 5a)
- Linear scaling to one million nodes in under four hours (Figure 6)

## Limitations

- **Tuning is part of the method.** p and q get a 25-point grid with 10-fold
  CV on labels; DeepWalk is not tuned. The comparison credits the search,
  which is the claim, but no baseline gets an equivalent budget
- **No spreads** in any table, and three node-classification datasets
- **LINE is much weaker here than in its own paper**, under an equal-sample
  rule that disfavors it
- **The BFS/DFS-to-equivalence mapping is argued, not measured** beyond the
  case study
