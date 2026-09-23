---
status: Read
paper: LIT-tmp4yk7i
title: 'Where did the gap go?'
version: 1
date: '2026-09-23'
summary: >-
  Retuned message-passing baselines close the reported graph-transformer
  gap on LRGB's Peptides datasets, mostly by adding an MLP prediction head.
  Feature normalization lifts every model on the superpixel datasets. Read
  in full.
---

# NOTE-tmp1vdpi: Where did the gap go?

## Contribution

A re-run of the benchmark used to argue that graph transformers are needed
for long-range tasks, with baselines tuned as carefully as the proposal.

## Key insight

**The baselines were handicapped by configuration, not architecture.** A
linear readout cannot compute a target that depends non-linearly on
pooled graph features. A transformer layer's feed-forward block partly
compensates, and an MLP head fixes it more cheaply.

## Key results

- Peptides-func AP: GCN 0.593 to 0.686, GPS 0.654 to 0.653. Peptides-struct
  MAE: GCN 0.350 to 0.246, GPS 0.250 to 0.251
- The MLP head alone accounts for most of the MPGNN gain
- PascalVOC-SP F1 after tuning: GatedGCN 0.388, GPS 0.444. Normalization
  is at least half of most models' gain
- Filtered vs raw MRR on PCQM-Contact changes the scores substantially

## Limitations

- **A short preprint.** Positional encoding is tuned as a hyperparameter,
  with no separate ablation
- **GPS stays ahead on the vision datasets.** The closure is dataset-specific
- **Same parameter budget (500k)** as the benchmark, and larger models are
  not tested
