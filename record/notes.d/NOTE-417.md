---
number: 417
status: Skimmed
formerly:
- NOTE-tmpwj9aw
paper: 'LIT-804'
title: 'Graph networks'
version: 1
date: '2026-10-22'
summary: >-
  A position paper and a formalism: a GN block updates edges, nodes and a
  global attribute in turn, and MPNNs, non-local networks and
  self-attention are configurations of it. There are no experiments.
  Skimmed: abstract, §3 (the GN block), §4.2.1 (MPNN as a GN) and §5
  (discussion, limits) read, the rest of §2 and §4 skimmed, the appendix
  not read.
---

# NOTE-417: Graph networks

## Contribution

A single definition, the graph network block, general enough to state most
graph neural networks of 2018 as special cases, and an argument that
relational inductive biases are the route to combinatorial
generalization.

## Key insight

**Put the structural assumption in the input, not the architecture.** An
edge says that two entities interact, its absence says they do not, and a
shared per-edge and per-node function makes the same block run on any
graph.

## Key results

- No experiments of its own. The GN block and its update order are
  definitions (Algorithm 1)
- The mapping of an MPNN onto a GN (§4.2.1) and of non-local networks onto
  a GN on a fully connected graph (§4.2.2)

## Limitations

- **Evidence by review.** §5.1 lists other papers' generalization results
  to new sizes and new numbers of entities
- **The authors' own limits** (§5.2): learned message passing cannot be
  guaranteed to separate some non-isomorphic graphs, and graphs do not
  express recursion or control flow naturally. Where the graph comes from
  is left open
