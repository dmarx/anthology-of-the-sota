---
status: Read
paper: 'LIT-tmp3l6xc'
title: 'Talk like a graph'
version: 1
date: '2026-10-22'
summary: >-
  How a graph is written as text changes a frozen LLM's accuracy on basic
  graph questions by tens of points. Listing each node's neighbours helps
  most on neighbourhood and degree questions. The structure of the graph
  also moves results, through strong priors such as "graphs have cycles".
  Read in full, v1.
---

# NOTE-tmpovagj: Talk like a graph

## Contribution

A factorial study of graph-to-text encodings, prompting methods, question
wording, model size and graph generator for frozen LLMs, and the GraphQA
benchmark that came out of it.

## Key insight

**Put the information the question needs next to the thing it is asked
about.** A per-node neighbour list makes a node's neighbours and degree one
contiguous span. An edge list scatters them across the prompt. Named-entity
encodings bury them in sentences. The encoding that wins changes with the
task, because counting edges is easier when every edge is one item.

## Key results

- PaLM 62B, zero-shot, connected nodes: incident 53.8, edge list 19.8,
  named encodings 4.0–8.8, letters with arrows 16.4 (Table 1)
- PaLM 62B, CoT, node degree: incident 75.0, edge list 71.2, all named
  encodings 14.6–17.8
- Average rank over tasks: incident is first under zero-shot CoT, few-shot,
  CoT and CoT-BAG, and last under zero-shot (Table 5)
- PaLM 2 L, zero-shot: incident 88.0 on connected nodes and 85.0 on degree.
  On edge count it gets 6.6, against 36.8 for the edge list (Table 11)
- Cycle check: 91.7% on complete graphs, 5.9% on path graphs (Table 4).
  Disconnected nodes: about 0% (§3.5)

## Limitations

- **One model family** (PaLM, PaLM 2, two Flan-PaLM 2 checkpoints), greedy
  decoding, one run per cell, and no intervals
- **Basic tasks on 5–20-node graphs.** Multi-step algorithms are not tested
- **Prompting and encoding interact.** The best encoding under zero-shot is
  not the best under CoT, so a single recommended encoding needs its
  prompting method stated
