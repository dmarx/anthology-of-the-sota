---
status: Active
title: "Evaluate graph models on a split that follows the application, by time, scaffold, species or target, and do not report a random split's score as the expected performance"
version: 1
tags:
- analysis-and-evaluation
- graphs-and-networks
date: '2026-10-22'
source:
- LIT-tmp3qfj0
# OGB states the recommendation for graph ML and measured it. Scaffold
# splits for molecules came earlier, from MoleculeNet, which is not in the
# record; OGB standardizes the hardest variant of them.
introduced_by:
- LIT-tmp3qfj0
consensus: unassessed
consensus_note: >-
  The measurement is one group's, repeated across nine datasets and three
  task types with ten seeds each. In this pass, LIT-tmp8wx7k adopts OGB's
  time split for COLLAB and a scaffold split for AQSOL, while
  LIT-tmprm7bo and LIT-581 use random splits by design, for what they test.
  How widely application-driven splits have replaced random ones has not
  been assessed here.
implementations:
- ogb
summary: >-
  Hu et al. (2020), [LIT-tmp3qfj0](../literature.d/LIT-tmp3qfj0.md) — for the same model at the same split
  ratio, a random split scores higher than the application's split on
  every dataset the authors checked: by 1.8 points on ogbn-arxiv, 9.7 on
  ogbn-products, 5.7 ROC-AUC on ogbg-molhiv, 22.5 on ogbg-ppa and 27.0
  Hits@20 on ogbl-ddi. On the random splits the train–test gap nearly
  vanishes. If the model will meet later data, new scaffolds, new species
  or new targets, split that way and report that number.
---

# SOTA-tmp2qn9u: Evaluate graph models on a split that follows the application, by time, scaffold, species or target, and do not report a random split's score as the expected performance

## Source

Hu et al. (2020), [LIT-tmp3qfj0](../literature.d/LIT-tmp3qfj0.md). Read as [NOTE-tmpxapd8](../notes.d/NOTE-tmpxapd8.md).

## The practice

The evidence is OGB's ([LIT-tmp3qfj0](../literature.d/LIT-tmp3qfj0.md)). For each of nine datasets the
authors ran their best baseline twice, once on the benchmark's
application-driven split and once on a random split with the same
proportions. The random split scored higher every time: ogbn-products
GraphSAGE 88.20 against 78.50%, ogbn-proteins 87.83 against 77.68
ROC-AUC, ogbn-arxiv GCN 73.54 against 71.74%, ogbl-ddi 80.88 against 53.90
Hits@20, ogbg-molhiv GIN 82.73 against 77.07, ogbg-molpcba 34.40 against
27.03 AP, ogbg-moltox21 86.03 against 77.57, ogbg-ppa 92.91 against 70.37%
and ogbg-code2 21.64 against 15.95 F1. The train–test gap on ogbn-proteins
is 0.27 points under a random split and 10.18 under the species split.

- **Split the way the model will be used.** By time when it predicts the
  future (papers, collaborations, knowledge-graph edits), by scaffold for
  molecules, by species for biological networks, by protein target for
  drug interactions, by project for code
- **Report the application split as the headline.** A random split's
  score is an interpolation estimate and overstates performance on the
  shifted data
- **Keep the random-split run as a diagnostic.** The gap between the two
  measures how much of the problem is distribution shift
- **Use the benchmark's own split and evaluator where one exists**, so
  that numbers are comparable. OGB's re-releases of three datasets after
  bugs and leakage show why the version matters too

## Conditions

- **The size of the gap is task-specific**: from 1.8 points on arXiv to 27
  on drug interactions. It cannot be assumed from another dataset
- **That a split matches deployment is argued, not measured.** The paper
  gives a reason for each split and no deployment data. Where no
  meaningful ordering exists, as for ogbl-biokg, a random split is what
  remains
- **This is about the test split, not about variance.** One fixed split
  still needs several seeds and a shared tuning protocol ([SOTA-350](SOTA-350.md))
