---
status: Proposed
promote_when: >-
  A group other than this one, prompting a model family other than PaLM,
  compares a per-node neighbour-list serialization with a flat edge list on
  neighbourhood and degree questions, with the prompt otherwise fixed. It
  reports the difference with variation over sampled graphs and prompt
  wordings. A benchmark or system that simply adopts the neighbour-list
  format does not satisfy this, and neither does a learned graph encoder,
  which answers a different question.
consensus: unreplicated
consensus_note: >-
  One group and one model family: PaLM 62B, PaLM 2 XXS–L and two Flan-PaLM 2
  checkpoints, each cell run once at temperature 0. GraphToken
  (LIT-tmpdsg6j) is from the same group and replaces text encodings rather
  than comparing them. How often graph-to-text pipelines use per-node
  neighbour lists has not been assessed here.
title: 'When putting a graph into a frozen LLM prompt to ask about a node''s neighbours or degree, write each node followed by its neighbours, with integer ids, not a flat edge list or named-entity relations'
version: 1
tags:
- graphs-and-networks
- representation-and-encoding
- in-context-learning
date: '2026-10-22'
source:
- LIT-tmp3l6xc
introduced_by:
- LIT-tmp3l6xc
implementations: []
summary: >-
  Fatemi et al. (2023), [LIT-tmp3l6xc](../literature.d/LIT-tmp3l6xc.md) — "Node 2 is connected to nodes 0, 1,
  3" puts a node's neighbourhood in one span. On PaLM 62B it beats an edge
  list on connected-nodes and degree questions under all five prompting
  methods: 53.8 against 19.8 zero-shot on connected nodes, 75.2 against
  66.8 on degree with CoT-BAG. On PaLM 2 L zero-shot the gap is 88.0 against
  55.6 and 85.0 against 49.6. Integer ids beat names on numeric answers by
  far more. It is task-specific: the edge list wins on edge count, and on
  the smallest PaLM 2 the advantage disappears.
---

# SOTA-tmpjux0f: When putting a graph into a frozen LLM prompt to ask about a node's neighbours or degree, write each node followed by its neighbours, with integer ids, not a flat edge list or named-entity relations

## Source

Fatemi et al. (2023), [LIT-tmp3l6xc](../literature.d/LIT-tmp3l6xc.md). Read as [NOTE-tmpovagj](../notes.d/NOTE-tmpovagj.md).

## The practice

The comparison is [LIT-tmp3l6xc](../literature.d/LIT-tmp3l6xc.md)'s. Fatemi, Halcrow and Perozzi wrote the
same graphs as text in nine ways. They asked PaLM 62B and four sizes of
PaLM 2 six basic questions with five prompting methods. Its "incident"
encoding writes one line per node, listing that node's neighbours. On PaLM
62B it beats the plain edge list on both neighbourhood questions under
every prompting method. On connected nodes the scores are 53.8 against
19.8 zero-shot and 41.0 against 20.6 with CoT-BAG. On node degree they are
25.0 against 12.4 zero-shot and 75.2 against 66.8 with CoT-BAG (Table 1).
On PaLM 2 L zero-shot the gap is 88.0 against 55.6 on connected nodes and
85.0 against 49.6 on degree (Table 11). Encodings with people's names do
far worse on both: 4.0–8.8 on connected nodes and 14.6–17.8 on degree with
CoT, on PaLM 62B.

- **One line per node, listing its neighbours,** when the question is about
  a node's neighbours, degree, or anything computed from them
- **Integer node ids** when the answer is a number. Names help only some
  yes/no questions, and not reliably
- **Re-check the choice for each task.** For edge count, the edge list is
  better: 36.8 against 6.6 on PaLM 2 L zero-shot, and 25.2 against 21.4 on
  PaLM 62B with CoT
- **State the prompting method with the encoding.** Ranked over all six
  tasks, incident is the best encoding under zero-shot CoT, few-shot, CoT
  and CoT-BAG, and the worst under plain zero-shot (Table 5)

## Conditions

- **Not at the smallest scale.** On PaLM 2 XXS the edge list matches or
  beats incident on degree (80.8 against 55.0 with CoT) and on connected
  nodes zero-shot (17.6 against 11.2). From PaLM 2 XS upwards, and on PaLM
  62B, incident leads
- **Small graphs**, 5–20 nodes, and basic look-up and counting questions.
  Whether the format still helps when the neighbour lists run to thousands
  of tokens is untested
- **It does not rescue questions the format does not make local.** Edge
  existence stays near the majority rate, and listing disconnected nodes is
  about 0% under every encoding
- **A trained encoder can beat any text format on counting**, though not
  here on neighbour listing. GraphToken ([LIT-tmpdsg6j](../literature.d/LIT-tmpdsg6j.md)) reaches 0.962 on
  degree and 0.264 on connected nodes, where incident text on PaLM 2 S
  reaches 81.6. That is a different intervention, and it needs gradient
  access to the model
