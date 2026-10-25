---
number: 390
status: Read
formerly:
- NOTE-tmp71t54
paper: 'LIT-844'
title: 'Long Range Graph Benchmark'
version: 1
date: '2026-10-22'
summary: >-
  Five datasets argued to need long-range interaction, with untuned
  message-passing and transformer baselines at 500k parameters.
  Transformers lead clearly only on the two Peptides tasks. Read in full,
  appendices included.
---

# NOTE-390: Long Range Graph Benchmark

## Contribution

A benchmark suite for graph models that are meant to capture interactions
between distant nodes, with larger graphs than ZINC or the OGB molecule
sets, and a first set of baselines at a fixed 500k-parameter budget.

## Key insight

**A long-range benchmark needs big graphs and a task that depends on
distant nodes.** Small molecular graphs and tasks that count local
substructures let a local model win, so they cannot show whether global
attention helps. The paper argues its datasets qualify from graph
statistics and task design, and takes the transformers' lead as
confirmation.

## Key results

- Peptides-func AP: GatedGCN+RWSE 0.607, SAN+RWSE 0.644. Peptides-struct
  MAE: GatedGCN+RWSE 0.336, Transformer+LapPE 0.253 (Table 4)
- PascalVOC-SP F1: SAN+LapPE 0.323, GatedGCN 0.287, Transformer+LapPE
  0.269. COCO-SP: GatedGCN 0.264 best (Table 3)
- PCQM-Contact MRR: all models 0.316–0.335 (Table 5)
- 2-layer MPNNs fall well below 5- and 8-layer ones. A structural encoding
  helps a shallow GatedGCN much more than a deep one (Appendix D)
- A trained Transformer's attention reaches beyond the local neighborhood
  on all five datasets, and on MNIST mostly stays within 4 hops (Appendix E)

## Limitations

- **No hyperparameter search is described.** Models were sized to the
  budget with fixed depth (Table C.1). [LIT-579](../literature.d/LIT-579.md) shows this understated the
  message-passing baselines
- **Whether a task is long-range is argued, not tested.** The evidence is
  graph statistics and which models won
- **4 seeds, one budget.** SAN did not converge on COCO-SP in 60 hours
- **The PCQM-Contact metric as implemented** differed from its definition
  (raw against filtered MRR), found by [LIT-579](../literature.d/LIT-579.md)
