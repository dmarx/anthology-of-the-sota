---
status: Active
title: 'Can Language Models Solve Graph Problems in Natural Language?'
version: 1
tags:
- graphs-and-networks
- in-context-learning
- analysis-and-evaluation
date: '2026-10-22'
published: '2023-05-17'
arxiv: '2305.10037'
first_author: 'Wang'
keywords:
- 'nlgraph'
- 'graph-reasoning'
- 'llm-benchmark'
- 'chain-of-thought'
- 'build-a-graph-prompting'
- 'spurious-correlations'
implementations:
- NLGraph
summary: >-
  Wang, Feng, He, Tan, Han, Tsvetkov (NeurIPS 2023), [ARXIV-2305.10037](https://arxiv.org/abs/2305.10037).
  NLGraph is a benchmark of 29,370 synthetic graph problems in natural
  language over eight tasks. Its standard set (5,902 problems) is used with
  text-davinci-003. With chain of thought (CoT), the model averages 84.6% on
  connectivity and 66.8% on cycle detection, where random is 50%. On
  topological sort, maximum flow, bipartite matching and Hamilton path, CoT,
  least-to-most and self-consistency mostly fail to beat plain few-shot or
  zero-shot prompting. When the two queried nodes are the degree-1 ends of a
  chain, CoT accuracy is 44.5 points below the general set. The paper's
  Build-a-Graph instruction adds 5.7 points on cycle and 4.3 on shortest
  path, and nothing on Hamilton path.
---

# LIT-tmpkrsn9: Can Language Models Solve Graph Problems in Natural Language?

Wang, Feng, He, Tan, Han, Tsvetkov, Xi'an Jiaotong, Washington and Notre
Dame (NeurIPS 2023, spotlight) — [ARXIV-2305.10037](https://arxiv.org/abs/2305.10037)

## Key takeaways

- **The benchmark** (Table 1): random graphs with controlled size and
  density for eight tasks: connectivity, cycle, topological sort, shortest
  path, maximum flow, bipartite matching, Hamilton path and simulating one
  sum-aggregation GNN layer. Easy, medium and hard subsets range from 5 to
  35 nodes. Answers are checked by a program, with partial credit on shortest
  path, maximum flow and the GNN task
- **Simple tasks** (Table 2, text-davinci-003): CoT averages 84.57 on
  connectivity, 66.75 on cycle and 51.51 on shortest path, against 50, 50
  and 17.81 for random. Plain few-shot does as well on connectivity (84.73)
  and better on cycle (70.33). CoT's clear gain over few-shot is on shortest
  path (51.51 against 35.51). Zero-shot answers cycle at exactly 50.00 on
  every subset
- **Harder tasks** (Figures 2–4): on topological sort and maximum flow, CoT,
  self-consistency and least-to-most mostly score below few-shot. On
  Hamilton path and bipartite matching, few-shot is 1.00 to 10.48 points
  below zero-shot, and more exemplars (up to 16) do not close the gap
- **Spurious cues** (Table 4): on 120 chain graphs, where the queried nodes
  are connected but rarely mentioned, CoT falls from 85.33 to 40.83 and
  few-shot from 83.33 to 45.00. Zero-shot CoT instead rises to 92.50. On 120
  clique pairs, which are frequently mentioned but disconnected, CoT and
  self-consistency barely move (−0.33, +0.66)
- **Build-a-Graph and Algorithmic prompting** (Table 5): BAG appends "Let's
  construct a graph with the nodes and edges first." Cycle average goes from
  66.75 to 72.44, shortest path from 51.51 to 55.76, and Hamilton path from
  24.00 to 22.34. Algorithmic prompting gains on medium and hard cycles but
  loses 7.3 points on easy ones. The abstract's "3.07% to 16.85%" are
  relative gains on single cells
- **Controls** (Table 7, shortest path only): replacing the BAG sentence with
  dots of equal length, or with "Examine each detail carefully", recovers
  part of the gain. The second one ties BAG on the easy subset (67.78)

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own review, 2026-10-22).
It is the first systematic benchmark of graph reasoning by language models
in the record. GraphQA, from Talk like a Graph ([LIT-tmp3l6xc](LIT-tmp3l6xc.md)), starts from
its design: Erdős–Rényi graphs, its BAG prompt as one of the prompting
methods, and a wider set of graph generators and text encodings.

**What the abstract compresses.** The quantitative results are for one
model, text-davinci-003, with a single run at temperature 0. GPT-3.5-turbo
and GPT-4 appear only in a qualitative look at 19 problems (Appendix E.3),
and fine-tuning OPT-2.7B produced unusable text (E.2). "A performance drop
of more than 40%" on the spurious-correlation cases holds for chains under
exemplar-based prompting. It does not hold for cliques, and it reverses for
zero-shot CoT. The BAG gains are a few points on the two easier tasks, and
the dot-length control covers only shortest path.

**Bearing on [SOTA-281](../practices.d/SOTA-281.md).** That practice says to try the single step-by-step
instruction first. Here zero-shot CoT is the worst method on shortest path
(8.89 exact match on easy, against 29.40 for zero-shot). Talk like a Graph
reports the same reversal on basic graph tasks. Both are conditions on that
practice, not evidence against it.

Read — [NOTE-tmpmot78](../notes.d/NOTE-tmpmot78.md).
