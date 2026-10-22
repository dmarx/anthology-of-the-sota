---
status: Active
title: 'Position: Graph Foundation Models are Already Here'
version: 1
tags:
- graphs-and-networks
- adaptation-and-tuning
date: '2026-10-22'
published: '2024-02-03'
arxiv: '2402.02216'
first_author: 'Mao'
keywords:
- 'graph-foundation-models'
- 'graph-vocabulary'
- 'transferability'
- 'expressiveness'
- 'scaling-laws'
- 'position-paper'
implementations: []
summary: >-
  Mao, Chen, Tang, Zhao, Ma, Zhao, Shah, Galkin, Tang (ICML 2024, position
  paper), [ARXIV-2402.02216](https://arxiv.org/abs/2402.02216). A graph foundation model needs a "graph
  vocabulary": units of graph structure that keep their meaning across
  datasets, so training on many graphs transfers positively. The paper
  reviews network-analysis, expressiveness and stability principles for
  node classification, link prediction and graph classification, and then
  data scaling, model scaling and the use of LLMs. It runs no experiments.
  The text qualifies the title: no existing model transfers across all
  graph tasks and domains, and the conclusion calls a universal one
  challenging. What is "here" is task- and domain-specific models such as
  ULTRA for knowledge-graph completion.
---

# LIT-tmpoyulj: Position: Graph Foundation Models are Already Here

Mao, Chen, Tang, Zhao, Ma, Zhao, Shah, Galkin, Tang, Michigan State,
Montréal/Mila, RPI, Snap and Intel Labs (ICML 2024) — [ARXIV-2402.02216](https://arxiv.org/abs/2402.02216)

## Key takeaways

- **Three kinds of GFM** (§2.1): task-specific (ULTRA, zero-shot
  knowledge-graph completion), domain-specific (DiG, chemistry) and
  "primitive" ones that generalize to a few datasets and tasks. OFA
  ([LIT-tmptwetd](LIT-tmptwetd.md)) is its example of a primitive one, and the paper notes that
  it needs every feature turned into text
- **The vocabulary argument** (§2.2): ULTRA is said to transfer for two
  reasons. Conditional message passing does not merge non-isomorphic node
  pairs. A graph of relations maps unseen relation types onto ones already
  learned. The paper generalizes this to two rules: a vocabulary should not
  collapse distinct structures, and it should be inclusive enough to absorb
  new ones
- **Per-task principles** (§3): homophily versus heterophily for nodes;
  triadic closure, global proximity and feature proximity for links, with
  expressive labeling tricks; motifs for graphs. Each comes with an
  "actionable step" that is a suggestion, not a tested result
- **Scaling** (§4): graph data is scarce and its construction choices
  conflict (ogbn-arxiv and arxiv-year share a graph and have opposite
  homophily). Scaling evidence is positive for molecules and materials and
  mixed elsewhere: a larger GAT underperforms on graph regression. LLMs used
  as feature encoders do not show scaling either
- **LLMs on graph problems** (§4.4): it cites NLGraph ([LIT-tmpkrsn9](LIT-tmpkrsn9.md)), Talk
  like a Graph ([LIT-tmp3l6xc](LIT-tmp3l6xc.md)) and GraphToken ([LIT-tmpdsg6j](LIT-tmpdsg6j.md)). It reads the
  last as showing that equivariance is not necessary when the decoder is an
  LLM

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own review, 2026-10-22).
It is a position paper and a map of the field, held for its taxonomy and its
framing. It contains no measurement of its own and sources nothing.

**The title and the text.** "Already here" travels. The sentences that bound
it are §2's "none of the current GFM have the capability to transfer across
all graph tasks and datasets from all domains" and the conclusion's
"constructing a universal GFM is challenging". The claim it supports is
narrower: models that transfer within one task or one domain exist, and a
shared vocabulary is the authors' account of why.

Skimmed — [NOTE-tmpbwjql](../notes.d/NOTE-tmpbwjql.md).
