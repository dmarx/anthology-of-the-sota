---
status: Read
paper: 'LIT-tmpkrsn9'
title: 'NLGraph'
version: 1
date: '2026-10-22'
summary: >-
  An instruction-tuned GPT-3 solves simple graph problems stated in prose
  well above chance. On harder ones, exemplars and chain of thought stop
  helping, and on chain graphs whose endpoints are rarely mentioned the
  model loses about half its accuracy. Main text and appendices read. The
  GPT-3.5/GPT-4 case tables were skimmed.
---

# NOTE-tmpmot78: NLGraph

## Contribution

A benchmark of graph-algorithm problems written in natural language, with
difficulty controlled by size and density and answers checked by a program.
It comes with a measurement of how standard prompting methods behave as the
algorithm gets harder.

## Key insight

**A model can answer "is there a path" without following one.** Mentions of
a node track its degree, and degree tracks connectivity in random graphs.
Chains (connected, rarely mentioned) and separate cliques (disconnected,
often mentioned) break that shortcut, and exemplar-prompted accuracy falls
on chains by up to 44.5 points.

## Key results

- Connectivity, CoT: 94.32, 82.17 and 77.21 on easy, medium and hard
  (Table 2). Cycle, few-shot: 80.00, 70.00, 61.00. Shortest path, CoT with
  self-consistency: 68.89 exact match on easy, 29.00 on hard
- GNN simulation (Table 3): CoT gives 31.00% exact match and 64.55% of
  nodes correct. Zero-shot and few-shot give 0% exact match
- Hamilton path and bipartite matching: few-shot trails zero-shot by 1.00 to
  10.48 points. Harder exemplars lower cycle accuracy (Figure 7)
- Shortest-path accuracy falls steadily as the optimal path gets longer
  (Figure 6)
- Build-a-Graph: +5.69 on the cycle average and +4.25 on shortest path,
  −1.66 on Hamilton path (Table 5)

## Limitations

- **One model quantitatively** (text-davinci-003), with one run per setting
  and no intervals, on the 5,902-problem standard set
- **The prompting fixes are small and partly generic.** A same-length run of
  dots, or an unrelated instruction, recovers part of the BAG gain on the
  one task where this was tested
- **Graphs are small**, up to 35 nodes, and random. Swapping "node" for
  "city" helps on easy problems and hurts on hard ones (Table 9)
