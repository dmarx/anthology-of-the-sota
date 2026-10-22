---
status: Read
paper: 'LIT-tmpdsg6j'
title: 'GraphToken'
version: 1
date: '2026-10-22'
summary: >-
  A per-task GNN encoder that writes soft tokens for a frozen LLM solves
  GraphQA's counting and degree tasks almost perfectly. It is weak on
  listing a node's neighbours. Its prompting baselines come from a
  different model's averages over encodings. Read in full, with the
  appendix probe tables scanned.
---

# NOTE-tmpasyzx: GraphToken

## Contribution

Graph-conditioned soft prompting: a GNN trained through a frozen LLM's loss
to produce the input embeddings that stand for a graph. It comes with a
comparison of seven encoder architectures and of positional against learned
node features.

## Key insight

**Let a model that can count do the counting.** A GNN, or a set-sum over
nodes or edges, computes counts and degrees exactly. The LLM only has to
read the answer off a few embeddings, instead of parsing a serialized
graph.

## Key results

- GraphQA test accuracy (Table 1): node count 0.996, node degree 0.962,
  cycle check 0.956, reachability 0.932, edge existence 0.738, shortest
  path 0.638, edge count 0.426, triangle counting 0.348, connected nodes
  0.264
- Encoders (Table 2): MPNN and MHA are strongest overall. NodeSet and
  EdgeSet win the count they sum, and no encoder wins everywhere
- Learned identity features beat Laplacian encodings for most encoder–task
  pairs (Figure 3)
- Probes of frozen encoders on all 8-node graphs: bipartiteness 95.03 from
  HGT trained on triangle counting (Table 4)

## Limitations

- **Baselines are not same-model.** The prompting rows equal the PaLM 62B
  encoder-averages from [LIT-tmp3l6xc](../literature.d/LIT-tmp3l6xc.md). GraphToken runs on Flan-PaLM 2 S
- **One encoder trained per task** on 1,000 graphs, selected per task. No
  multi-task encoder is reported
- **Connected nodes** (0.264) is far below what a well-chosen text encoding
  reaches on PaLM 2 S in [LIT-tmp3l6xc](../literature.d/LIT-tmp3l6xc.md) (81.6%)
- **No intervals or repeated runs**, and the LLM and benchmark both come
  from the authors' group
