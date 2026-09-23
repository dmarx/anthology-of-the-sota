---
status: Active
title: 'Where Did the Gap Go? Reassessing the Long-Range Graph Benchmark'
version: 1
tags:
- analysis-and-evaluation
- model-architecture
date: '2026-09-23'
published: '2023-09-01'
arxiv: '2309.00367'
first_author: 'Tönshoff'
keywords:
- 'lrgb'
- 'graph-transformer'
- 'message-passing'
- 'hyperparameter-tuning'
- 'baselines'
implementations: []
compared_against:
- LIT-tmp95aa1
summary: >-
  Tönshoff, Ritzert, Rosenbluth, Grohe (2023), [ARXIV-2309.00367](https://arxiv.org/abs/2309.00367). On the
  Long-Range Graph Benchmark, graph transformers were reported to beat
  message-passing GNNs. After a basic hyperparameter sweep within the same
  500k-parameter budget, GCN, GINE and GatedGCN all beat GPS on
  Peptides-func and Peptides-struct. Most of the gain comes from a 2-layer
  prediction head instead of a linear one. On the superpixel datasets,
  input feature normalization accounts for at least half the gain of most
  models, and GPS stays ahead there. The link-prediction metric's code
  computed raw MRR where the paper specified filtered MRR.
---

# LIT-tmp4yk7i: Where Did the Gap Go? Reassessing the Long-Range Graph Benchmark

Tönshoff, Ritzert, Rosenbluth, Grohe, RWTH Aachen and Göttingen (2023) —
[ARXIV-2309.00367](https://arxiv.org/abs/2309.00367)

## Key takeaways

- **Peptides** (Table 1a): after tuning, GCN reaches AP 0.686 (reported
  0.593) and MAE 0.246 (reported 0.350). GINE and GatedGCN improve similarly.
  GPS re-tuned is unchanged (0.653, 0.251). Every MPGNN now beats GPS, and
  GCN matches the best published result on Peptides-struct
- **The head** (Figure 1b): swapping the linear prediction head for a
  2-layer MLP, with nothing else changed, accounts for most of the MPGNN
  gain, and almost all of it on Peptides-struct. GPS is insensitive to the
  head
- **Superpixels** (Table 2): channel-wise feature normalization helps every
  model. It accounts for at least half the gain for all but GatedGCN, where
  it mainly cuts seed variance. After tuning, GatedGCN reaches F1 0.388 on
  PascalVOC-SP, above GPS's originally reported 0.375. GPS itself rises to
  0.444 and stays ahead
- **PCQM-Contact:** the official code computes raw MRR, not the filtered MRR
  the benchmark defines. Self-loop candidates also bias the symmetric
  scoring function

## Standing in the anthology

**Filed from `#163`** ("graph representation / gnn"). It is
`compared_against` GIN ([LIT-tmp95aa1](LIT-tmp95aa1.md)), whose edge-feature variant GINE is
one of the retuned baselines. It sources [SOTA-tmp7wtf2](../practices.d/SOTA-tmp7wtf2.md).

**Scope of "the gap vanished".** It vanished on the two Peptides datasets.
On PascalVOC-SP and COCO-SP, tuned GPS still leads tuned MPGNNs, by 5.6 and
9.6 F1 points. The paper is a short preprint with a 500k-parameter budget,
and the LRGB paper it re-examines is not in the record.

Read — [NOTE-tmp1vdpi](../notes.d/NOTE-tmp1vdpi.md).
