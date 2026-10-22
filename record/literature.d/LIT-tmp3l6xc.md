---
status: Active
title: 'Talk like a Graph: Encoding Graphs for Large Language Models'
version: 1
tags:
- graphs-and-networks
- representation-and-encoding
- in-context-learning
date: '2026-10-22'
published: '2023-10-06'
arxiv: '2310.04560'
first_author: 'Fatemi'
keywords:
- 'graph-encoding'
- 'graphqa'
- 'graph-reasoning'
- 'prompting'
- 'graph-structure'
implementations: []
summary: >-
  Fatemi, Halcrow, Perozzi (ICLR 2024), ARXIV-2310.04560. The paper writes
  a graph as text in nine ways and asks PaLM 62B and PaLM 2 XXS–L six basic
  questions about graphs of 5–20 nodes, with five prompting methods
  (GraphQA). Encoding matters most where an answer needs one node's
  neighbourhood. On PaLM 62B zero-shot, listing each node's neighbours
  ("incident") gets 53.8% on connected nodes, against 19.8% for an edge list
  and 4.0–8.8% for named-entity encodings. It matters little for edge
  existence, where every PaLM 62B configuration is below the 54% majority,
  and the edge list beats incident on edge count. The headline "4.8% to 61.8%" is
  the gap between the best and worst of the nine encodings, not a gain over
  a sensible default.
---

# LIT-tmp3l6xc: Talk like a Graph: Encoding Graphs for Large Language Models

Fatemi, Halcrow, Perozzi, Google Research (ICLR 2024) — ARXIV-2310.04560

## Key takeaways

- **The setup** (§3, Appendix A): nine graph-to-text encodings. They combine
  integer, English-name, TV-character, politician or letter node labels with
  edges written as pairs, "X and Y are friends" sentences, arrows, or one
  line per node listing its neighbours (incident). The six tasks are edge
  existence, node degree, node count, edge count, connected nodes and cycle
  check, plus disconnected nodes. The prompting methods are zero-shot,
  zero-shot CoT, few-shot, CoT and CoT with NLGraph's Build-a-Graph
  instruction (LIT-tmpkrsn9). Each configuration is decoded once at
  temperature 0
- **Encoding** (Table 1, PaLM 62B): incident is best on node degree and
  connected nodes under every prompt. Under CoT it scores 75.0 on degree,
  against 71.2 for the edge list and 14.6–17.8 for the named encodings.
  Ranked over all tasks (Table 5), incident is best under four prompting
  methods and last under zero-shot (6.16), where politician names rank first
  (3.50)
- **Integer ids versus names:** integer labels help the tasks whose answer
  is a number (degree, node and edge count). Names do better on some yes/no
  tasks, such as Game of Thrones names on edge existence
- **Scale** (Figure 3, Tables 6–11): PaLM 2 L zero-shot with incident
  reaches 88.0 on connected nodes and 85.0 on degree. The edge list reaches
  100.0 on node count. On edge count incident falls to 6.6, against 36.8 for
  the edge list. Averaged over encodings, edge existence stays near the
  majority rate at every size, though incident under few-shot reaches 73.2
  on PaLM 2 L
- **Prompting** (Table 1): zero-shot CoT is worse than zero-shot on these
  tasks. On PaLM 62B cycle check, the averages over encodings are 32.3 and
  76.0, and 82% of the graphs have a cycle
- **Graph structure** (Table 4): zero-shot cycle check is 91.7% on complete
  graphs and 5.9% on path graphs, so the model mostly says "yes". Few-shot
  CoT lifts path graphs to 19.7%. Listing disconnected nodes is about 0%
  with every method (§3.5)
- **Question wording** (Table 2): asking "how many friends" instead of "what
  degree" helps PaLM 2 XXS (edge existence 42.8 to 60.8). On PaLM 62B under
  CoT the same change lowers edge existence from 46.6 to 38.6

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own review, 2026-10-22).
It sources SOTA-tmpjux0f, a Proposed practice to serialize a graph as
per-node neighbour lists with integer ids for neighbourhood and degree
questions.

**What the headline measures.** The abstract's "boost performance by 4.8% to
61.8%" is the δ column of Table 1, the spread between the best and the
worst of nine encodings under one prompting method. The 61.8 is node degree
under CoT-BAG, incident (75.2) against the social-network encoding (13.4). Against the
obvious default, an edge list, the incident gain under the same prompt is
8.4 points on degree. It is 34.0 on connected nodes zero-shot, and it is
negative on edge count. All results are for one model family (PaLM and PaLM
2), with no repeated runs or intervals. The arXiv text is v1, and the
camera-ready may differ.

**Its benchmark reused by the same group.** GraphToken (LIT-tmpdsg6j) trains
a graph encoder for a frozen LLM on GraphQA. Its prompting baselines match,
to the digit, this paper's PaLM 62B averages over all nine encodings.

**Bearing on SOTA-281.** As in NLGraph, zero-shot CoT underperforms plain
zero-shot here. These are basic look-up and counting tasks, which the paper
says need no multi-step reasoning.

Read — NOTE-tmpovagj.
