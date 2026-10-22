---
status: Read
paper: 'LIT-tmpt6hyo'
title: 'The bottleneck of GNNs'
version: 1
date: '2026-10-22'
summary: >-
  Over-squashing: exponentially many messages forced through fixed-size
  vectors. GNNs stop fitting a synthetic tree task at depth 4–5. A fully
  adjacent last layer cuts QM9 error 42% without retuning, where doubling
  width gives 5.5%. Main text and appendices B and E read, the
  rest skimmed.
---

# NOTE-tmp198gc: The bottleneck of GNNs

## Contribution

A name and a test for the failure of message passing on long-range tasks,
distinct from over-smoothing, and the observation that tuned published
models suffer from it.

## Key insight

**Depth buys reach and costs capacity.** To hear a node r hops away you
need r layers. By then the information of exponentially many nodes is
arriving through one fixed-size vector, and the network fits short-range
signals instead.

## Key results

- Tree-NeighborsMatch training accuracy: GCN and GIN fit r ≤ 3, GAT and
  GGNN fit r ≤ 4, and nothing fits r = 5 (Figure 3)
- Combinatorial bound: d = 32 cannot fit r > 7. Empirically, d = 512 fits
  r = 7 at most (Figure 4)
- QM9, last layer fully adjacent, no retuning: −42% mean relative error
  over six GNNs. Doubling width gives −5.5%, 10 layers give nothing, and
  all layers fully adjacent give +1500%. Half the FA edges give −31.5%
- ENZYMES: GIN 59.6 → 67.7, above the structure-free baseline's 65.2.
  NCI1: GIN 80.0 → 81.5
- VarMisuse: +FA improves every model on SeenProjTest, with a best of
  88.4

## Limitations

- **Over-squashing is inferred, not measured.** The evidence is that a
  bottleneck-breaking change helps
- **The synthetic task is built to have the bottleneck.** Edges point
  toward the root and the answer requires every leaf
- **The cost of the fully adjacent layer is not reported.** It is
  quadratic in nodes: cheap on QM9 (~18 nodes), less so on VarMisuse,
  whose graphs average 1,742–3,986 nodes by split
- **Many non-QM9 gains are within one standard deviation**
- **No comparison to the earlier global-interaction fixes** the paper
  itself lists, such as virtual edges and supersource nodes
