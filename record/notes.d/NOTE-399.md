---
number: 399
status: Skimmed
formerly:
- NOTE-tmpe0x91
paper: 'LIT-813'
title: 'ESAN'
version: 1
date: '2026-10-22'
summary: >-
  A bag of subgraphs processed by a shared GNN is strictly more expressive
  than 1-WL. Ego-network policies take GIN from 0.252 to 0.102 MAE on
  ZINC; TUD and OGB gains are mostly within noise, and a GCN encoder fits
  more and tests worse. Main text and the results appendix read; the
  proofs were not.
---

# NOTE-399: ESAN

## Contribution

A general recipe for going past 1-WL with an ordinary GNN: process a
policy-defined bag of subgraphs with an architecture equivariant to both
node and subgraph permutations, and analyze it with WL variants defined on
bags.

## Key insight

**Two graphs 1-WL cannot tell apart often contain subgraphs it can.**
Delete an edge, a node, or look from each node's ego-network, and the
resulting multisets of 1-WL colorings differ. The subgraphs are aligned
on the original node set, which is what lets them share information across
the bag.

## Key results

- DS-WL and DSS-WL are strictly stronger than 1-WL for suitable policies
  (Theorem 1), and DS(S)-GNN reaches them on bounded graphs (Theorem 2).
  DSS is at least as strong as DS (Proposition 1)
- EXP and CEXP: 100% for every policy against 51.1 and 70.2 for GIN
  (Table 6). Sampling 5% of ego-subgraphs drops DS-GNN to 93.5 and 83.9 on
  them, while DSS-GNN stays at 97.7 or above under every policy (Table 8)
- ZINC12k: GIN 0.252, ego policies 0.102–0.126, deletion policies
  0.166–0.172 (Table 3)
- OGB with GIN: up to +2.4 AUC on MOLHIV, +3.0 on MOLTOX21 (Table 2). With
  GCN, DS-GNN loses test AUC on MOLHIV under every policy (Table 5)
- Per-epoch time about 2× GIN for DS-GNN, 3× for DSS-GNN (Table 11)

## Limitations

- **The real-data gain is concentrated on ZINC.** TUD and OGB differences
  are mostly within a standard deviation
- **Expressivity helps fitting before it helps testing.** The GCN rows show
  training AUC rising and test AUC falling
- **Sampling breaks invariance.** The paper measures that it does not hurt
  accuracy, and leaves its theory open
- **Not read:** the proofs in Appendices D and E
