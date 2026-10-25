---
number: 383
status: Read
formerly:
- NOTE-tmp25kz1
paper: 'LIT-841'
title: 'One for All (OFA)'
version: 1
date: '2026-10-22'
summary: >-
  Text-embedded features and a prompt graph with class nodes let one GNN
  train on citation, knowledge-graph and molecule datasets together. It
  matches or beats per-dataset GNNs on most supervised tasks. Zero-shot
  transfer to unseen graphs is weak, and joint training hurts link tasks.
  Read in full, with the dataset-construction appendix skimmed.
---

# NOTE-383: One for All (OFA)

## Contribution

A recipe for one classification GNN across node, link and graph tasks and
across domains. Text descriptions embedded by a single language model give
the shared feature space. A prompt subgraph of task and class nodes gives
the shared task format and allows zero- and few-shot prediction.

## Key insight

**Make the task part of the input graph.** Class nodes with text and a
prompt node with the task description turn every task into scoring class
nodes. When datasets are mixed, the task text lets the model tell them
apart. Pooling without it loses about 4 points under joint training and
nothing when trained separately (Table 12).

## Key results

- Joint training beats the best of GCN, GAT and GIN on 8 of 10 supervised
  tasks. It is below them on Cora nodes (75.90 against 82.76) and Wiki-CS
  (78.34 against 79.63)
- Knowledge-graph relation classification jumps to about 95–98% from
  57–74%, and the per-dataset OFA does the same
- A larger encoder (Llama 2 13B) helps citation graphs. e5 helps molecules.
  No encoder is best everywhere
- FB15K237 20-way 0-shot: 70.20, against Prodigy's 5.11. HIV 0-shot AUC:
  35.67. WN18RR 5-way 0-shot: 30.96

## Limitations

- **Classification only.** Regression is out of scope (Appendix F)
- **Joint models are evaluated at the last epoch**, with 3 runs and no
  validation selection. Some node splits differ from the standard ones
- **Cross-domain benefit is mixed.** Joint training is worse than separate
  training on every link-level few/zero-shot setting and on PCBA few-shot
- **The text features do much of the work.** Baselines use native features,
  so feature quality and architecture are confounded
