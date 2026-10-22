---
status: Active
title: 'Recipe for a General, Powerful, Scalable Graph Transformer'
version: 1
tags:
- graphs-and-networks
- model-architecture
- attention-techniques
- representation-and-encoding
date: '2026-10-22'
published: '2022-05-25'
arxiv: '2205.12454'
first_author: 'Rampášek'
keywords:
- 'gps'
- 'graphgps'
- 'graph-transformer'
- 'positional-encoding'
- 'structural-encoding'
- 'message-passing'
- 'linear-attention'
implementations:
- GraphGPS
compared_against:
- LIT-579
- LIT-tmpynksg
- LIT-tmpy7li2
- LIT-tmpf1ndc
summary: >-
  Rampášek, Galkin, Dwivedi, Luu, Wolf, Beaini (NeurIPS 2022),
  [ARXIV-2205.12454](https://arxiv.org/abs/2205.12454). A graph-transformer layer that sums a local
  message-passing layer and a global attention layer, then applies an MLP,
  on node features carrying positional or structural encodings. Removing
  the message-passing layer hurts on all six ablated datasets (ZINC MAE
  0.070 to 0.217). Removing attention matters less (ZINC unchanged,
  Peptides-func AP 0.654 to 0.616). ZINC MAE 0.070 and the LRGB results
  were state of the art when published. The best results use full
  quadratic attention, not the linear attention in the title.
---

# LIT-tmpwijfh: Recipe for a General, Powerful, Scalable Graph Transformer

Rampášek, Galkin, Dwivedi, Luu, Wolf, Beaini, Mila, NTU Singapore and
Valence Discovery (NeurIPS 2022) — [ARXIV-2205.12454](https://arxiv.org/abs/2205.12454)

## Key takeaways

- **The layer** (Eqs. 1–4, Appendix D): each GPS layer runs an MPNN with
  edge features (GatedGCN, GINE or PNA) and a global attention block
  (Transformer, Performer or BigBird) in parallel on the same input, adds
  each to a residual with batch norm, sums the two and applies a 2-layer
  MLP. Edge features enter only through the MPNN
- **A taxonomy of encodings** (Table 1): positional and structural
  encodings, each local, global or relative. The experiments use LapPE,
  RWSE, SignNet and PEG
- **The local layer carries most of the weight** (Table 2a, Appendix B):
  dropping the MPNN raises ZINC MAE from 0.070 to 0.217 and PCQM4Mv2-subset
  MAE from 0.116 to 0.329, and lowers CIFAR10 accuracy from 72.3 to 68.9,
  MalNet-Tiny from 92.6 to 73.9, PascalVOC-SP F1 from 0.374 to 0.276 and
  Peptides-func AP from 0.654 to 0.633. Dropping attention changes ZINC not
  at all and costs less elsewhere: CIFAR10 72.3 to 69.9, PascalVOC-SP 0.374
  to 0.302, Peptides-func 0.654 to 0.616
- **Linear attention costs accuracy** (Table 2a): Performer trails the full
  Transformer on CIFAR10 (70.7 against 72.3) and MalNet-Tiny, and BigBird
  is often no better than no attention at all (PascalVOC-SP 0.276,
  Peptides-func 0.585, both below the MPNN-only model)
- **Benchmarks** (Tables 3–6): ZINC MAE 0.070 (best in Table 3),
  PCQM4Mv2 validation MAE 0.0858 with 19.4M parameters against
  Graphormer's 0.0864 with 48.3M, and on LRGB F1 0.375 (PascalVOC-SP),
  0.341 (COCO-SP), AP 0.654 (Peptides-func), MAE 0.250 (Peptides-struct)
  and MRR 0.334 (PCQM-Contact, below SAN+LapPE's 0.335)

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22). It sources [SOTA-tmpy8eal](../practices.d/SOTA-tmpy8eal.md).

**Retuned by [LIT-579](LIT-579.md).** It is `compared_against` Tönshoff et al. ([LIT-579](LIT-579.md)),
whose subject is this paper's LRGB comparison. They re-tuned GPS with the
same sweep as the message-passing baselines. On Peptides-func and
Peptides-struct GPS did not move (AP 0.653, MAE 0.251), while tuned GCN,
GINE and GatedGCN all passed it, GCN to AP 0.686 and MAE 0.246. On
PascalVOC-SP and COCO-SP GPS gained 18% and 13% from feature normalization
and tuning, to F1 0.444 and 0.388, and stayed ahead of every tuned MPNN.
So the paper's Peptides lead was a baseline effect and its superpixel lead
was real but understated.

**Its LRGB baselines are LRGB's.** It is `compared_against` the Long Range
Graph Benchmark ([LIT-tmpynksg](LIT-tmpynksg.md)), a paper with six of the same authors: all
seven baseline rows of Table 6 are copied verbatim from that benchmark,
whose message-passing models were sized to the budget, not tuned. GPS itself
was configured by "line search" one hyperparameter at a time (Appendix
A.3), with a cosine schedule the baselines did not get. The comparison
therefore had the handicap [SOTA-349](../practices.d/SOTA-349.md) describes on one side only.

**Against Graphormer.** It is `compared_against` Graphormer
([LIT-tmpy7li2](LIT-tmpy7li2.md)). On ZINC at about 500k parameters GPS reaches MAE 0.070
against Graphormer-Slim's 0.122, both taken from the papers. On PCQM4Mv2
GPS-medium matches Graphormer (0.0858 against 0.0864) with 40% of the
parameters, and Graphormer's much lower training MAE (0.035 against 0.073)
suggests it overfits more. The paper also notes Graphormer does well on
the full PCQM4Mv2 without any local module, and suggests the need for one
may shrink with data.

**What the title omits.** "Linear complexity" describes the Performer and
BigBird variants. Every LRGB, ZINC, CIFAR10 and PCQM4Mv2 configuration in
Appendix A uses the full O(N²) Transformer, and the linear variants are
worse in most of the ablations (Performer is slightly better only on the
PCQM4Mv2 subset, 0.114 against 0.116). "Universal function approximator" is argued
by appeal to SAN's result with the full set of Laplacian eigenvectors, not
proved for the configurations run. And on PascalVOC-SP the LapPE the main
result uses hurts: without it F1 is 0.385, with PEG 0.396.

**Its attention swapped for a sparse one.** Exphormer ([LIT-tmpf1ndc](LIT-tmpf1ndc.md)) keeps
GPS's message-passing block and replaces the global attention with
attention over a virtual node, the graph's edges and an expander. In the
same codebase it beats full-attention GPS on CIFAR10, MalNet-Tiny and
PascalVOC-SP (F1 0.398 against 0.374), ties it on Peptides-func (AP 0.653
against 0.654), and runs on ogbn-arxiv, where GPS runs out of memory. Its
GPS rows are copied from this paper, not retuned.

Read — [NOTE-tmptgbtv](../notes.d/NOTE-tmptgbtv.md).
