---
status: Active
title: 'Long Range Graph Benchmark'
version: 1
tags:
- graphs-and-networks
- analysis-and-evaluation
- model-architecture
date: '2026-10-22'
published: '2022-06-16'
arxiv: '2206.08164'
first_author: 'Dwivedi'
keywords:
- 'lrgb'
- 'long-range-interactions'
- 'graph-transformer'
- 'message-passing'
- 'benchmark'
- 'over-squashing'
implementations: []
compared_against:
- LIT-579
- LIT-tmpf1ndc
- LIT-tmpwijfh
summary: >-
  Dwivedi, Rampášek, Galkin, Parviz, Wolf, Luu, Beaini (NeurIPS 2022
  Datasets and Benchmarks), [ARXIV-2206.08164](https://arxiv.org/abs/2206.08164). Five datasets meant to need
  long-range interaction: PascalVOC-SP, COCO-SP, PCQM-Contact,
  Peptides-func and Peptides-struct. Peptides graphs average 150.9 nodes
  and diameter 57.0. At a 500k-parameter budget, transformers beat the
  best message-passing model on Peptides-func (AP 0.644 against 0.607) and
  Peptides-struct (MAE 0.253 against 0.336). The baselines were sized to
  the budget, not tuned, and [LIT-579](LIT-579.md) later closed both Peptides gaps.
---

# LIT-tmpynksg: Long Range Graph Benchmark

Dwivedi, Rampášek, Galkin, Parviz, Wolf, Luu, Beaini, NTU Singapore, Mila
and Valence Discovery (NeurIPS 2022 Datasets and Benchmarks) —
[ARXIV-2206.08164](https://arxiv.org/abs/2206.08164)

## Key takeaways

- **The datasets** (Tables 1–2): two superpixel node-classification sets
  built from Pascal VOC and MS COCO (about 477–479 nodes per graph, macro
  F1), one inductive link-prediction set of 3D atom contacts more than 5
  hops apart in the graph (PCQM-Contact, MRR), and 15,535 peptide graphs
  with a 10-label function task (Peptides-func, AP) and an 11-target
  3D-structure regression (Peptides-struct, MAE). Peptides graphs average
  150.9 nodes, mean shortest path 20.9 and diameter 57.0
- **What makes a task long-range** (§2) is argued, not measured: graph size,
  a task that depends on distant nodes, and a task that benefits from global
  structure such as positional encodings. The paper calls these
  "implications", not a test
- **Peptides** (Table 4, 4 seeds, about 500k parameters): the best
  message-passing model, GatedGCN+RWSE, reaches AP 0.607 and MAE 0.336.
  SAN+RWSE reaches AP 0.644 and Transformer+LapPE MAE 0.253. This is the
  largest gap in the paper
- **Superpixels** (Table 3): SAN+LapPE leads PascalVOC-SP at F1 0.323, ahead
  of GatedGCN at 0.287, but plain Transformer+LapPE (0.269) is behind
  GatedGCN. On COCO-SP GatedGCN (0.264) is best, and SAN did not converge
  within the 60-hour limit
- **PCQM-Contact** (Table 5): every model's MRR lies between 0.316 and
  0.335. The metric is specified as filtered MRR (§3.3)
- **Depth matters for message passing** (Appendix D): 2-layer MPNNs are much
  worse than the 5- and 8-layer ones in the main tables. A structural
  encoding helps a 2-layer GatedGCN a lot and a deep one little
  (Peptides-func AP 0.507 to 0.581 at 2 layers, 0.586 to 0.607 at 5)

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22). It is the benchmark Tönshoff et al. ([LIT-579](LIT-579.md)) re-ran,
and with that paper it is the case behind [SOTA-349](../practices.d/SOTA-349.md). GPS ([LIT-tmpwijfh](LIT-tmpwijfh.md)) and
Exphormer ([LIT-tmpf1ndc](LIT-tmpf1ndc.md)) report their long-range results on it.

**How the baselines were set, and what that did.** Appendix C says each
model's hyperparameters were chosen to fit a budget of about 500k
parameters, with depth fixed per dataset (5 or 8 message-passing layers, 4
transformer layers) and a learning rate between 0.0003 and 0.001. No sweep
is described. It is `compared_against` [LIT-579](LIT-579.md), which reran the same GCN,
GINE and GatedGCN in the same budget after a basic sweep. On Peptides-func
GCN went from this paper's AP 0.593 to 0.686, and on Peptides-struct from
MAE 0.350 to 0.246, past every transformer here and past GPS. Most of the
change came from replacing the linear prediction head, which [LIT-579](LIT-579.md) traces
to this benchmark's configuration, with a 2-layer MLP. [LIT-579](LIT-579.md) also found
that the official code computed raw MRR on PCQM-Contact instead of the
filtered MRR §3.3 defines. The arXiv v4 of this paper (November 2023) adds a
footnote pointing to that reassessment and leaves the tables as they were.

**What the headline omits.** "Transformers significantly outperform message
passing" holds on Peptides, and on PascalVOC-SP for SAN only. It does not
hold on COCO-SP, and on PCQM-Contact the spread is two hundredths of MRR.
That these tasks need long-range interaction is argued from dataset
statistics and from which models won, so a tuned local model matching the
transformers later weakens the characterization as well as the transformer
result.

Read — [NOTE-tmp71t54](../notes.d/NOTE-tmp71t54.md).
