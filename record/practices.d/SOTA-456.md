---
number: 456
status: Active
formerly:
- SOTA-tmpy8eal
consensus: emerging
consensus_note: >-
  Two groups in this record build graph transformers this way and ablate
  it: GPS (LIT-842) and Exphormer (LIT-821), which runs inside
  GPS's codebase, so the second is independent in authorship but not in
  implementation. Graphormer (LIT-843) is a competing design with no
  local layer, whose attention bias can itself represent message passing.
  How widely the hybrid is used beyond these papers has not been assessed.
title: 'In a graph transformer, keep a local message-passing layer beside global attention in every block, rather than relying on attention and positional encodings alone'
version: 1
tags:
- graphs-and-networks
- model-architecture
- attention-techniques
date: '2026-10-22'
source:
- LIT-842
- LIT-821
introduced_by:
- LIT-842
implementations:
- GraphGPS
summary: >-
  Rampášek et al. (2022), [LIT-842](../literature.d/LIT-842.md) — in GPS ablations on six datasets,
  removing the message-passing layer from each block costs more than
  removing global attention: ZINC MAE 0.070 to 0.217 without it, unchanged
  without attention. Exphormer ([LIT-821](../literature.d/LIT-821.md)) finds the same with sparse
  attention on five more. Shown at benchmark scale, up to 6M parameters;
  whether it holds with much more data, or against attention biased by
  graph distance, is open.
---

# SOTA-456: In a graph transformer, keep a local message-passing layer beside global attention in every block, rather than relying on attention and positional encodings alone

## Source

Rampášek et al. (2022), [LIT-842](../literature.d/LIT-842.md). Read as [NOTE-415](../notes.d/NOTE-415.md).
Shirzad et al. (2023), [LIT-821](../literature.d/LIT-821.md). Read as [NOTE-408](../notes.d/NOTE-408.md).

## The practice

The recommendation is GPS's ([LIT-842](../literature.d/LIT-842.md)), and its evidence is the paper's
own ablation, which removes one component at a time from the best
configuration. Each GPS layer runs a message-passing layer with edge
features and a global attention layer in parallel and sums them. Without
the message-passing layer, ZINC MAE rises from 0.070 to 0.217, the
PCQM4Mv2 subset from 0.116 to 0.329, MalNet-Tiny accuracy falls from 92.6
to 73.9, CIFAR10 from 72.3 to 68.9, PascalVOC-SP F1 from 0.374 to 0.276 and
Peptides-func AP from 0.654 to 0.633. Without global attention the losses
are smaller everywhere, and zero on ZINC.

Exphormer ([LIT-821](../literature.d/LIT-821.md)) is a second group's test of the same claim with a
different attention block. Its sparse attention already attends over the
input edges, and still, removing the message-passing layer costs accuracy
on all five datasets it reports: CIFAR10 74.8 against 72.9 at best without
it, MalNet-Tiny 94.0 against 92.2, CLUSTER 78.1 against 76.9 (Tables
10–14).

- **Every block, not a front end.** GPS argues that message-passing layers
  placed only before the transformer, as in GraphTrans, can lose
  information early. That argument is not ablated: no sequential variant
  was run
- **Edge features go through the local layer.** In GPS they enter nowhere
  else, so dropping the local layer drops them, which is part of what the
  ablation measures
- **Choose the local layer per dataset.** GatedGCN, GINE and PNA trade
  places across datasets in the same ablations

## Conditions

- **Benchmark scale.** Models of up to about 500k parameters, and 6M on the
  PCQM4Mv2 subset. GPS itself suggests the local layer may matter less with
  far more data, citing Graphormer's result on the full PCQM4Mv2
- **The alternative tested is attention with node positional encodings.**
  Attention with a structural bias over distances, as in Graphormer
  ([LIT-843](../literature.d/LIT-843.md)), can represent message passing by itself, and was not
  compared at matched settings
- **The size of the benefit varies.** On Peptides-func it is 0.02 AP; on
  ZINC and MalNet-Tiny it is most of the result
- **Untuned baselines elsewhere in these papers do not touch this claim.**
  [SOTA-349](SOTA-349.md) concerns their comparisons with other models; this one rests on
  ablations within each model
