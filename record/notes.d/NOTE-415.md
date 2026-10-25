---
number: 415
status: Read
formerly:
- NOTE-tmptgbtv
paper: 'LIT-842'
title: 'GPS recipe'
version: 1
date: '2026-10-22'
summary: >-
  A graph-transformer layer that runs message passing and global attention
  side by side. Ablations on six datasets show the message-passing half
  matters more than the attention half. Read in full, appendices included;
  the expressivity arguments are informal.
---

# NOTE-415: GPS recipe

## Contribution

A modular graph-transformer layer (GPS) and a taxonomy of positional and
structural encodings, with ablations of each component and results on 16
datasets. The GraphGPS codebase it released became the framework later
papers, LRGB and Exphormer among them, are built in.

## Key insight

**Run local message passing and global attention in parallel in every
layer, not one stage after the other.** The MPNN carries edge features and
local structure; attention spreads information across the graph. Putting
the MPNN only before the transformer, as GraphTrans does, risks losing
information early.

## Key results

- Without the MPNN: ZINC MAE 0.070 to 0.217, PCQM4Mv2-subset 0.116 to
  0.329, CIFAR10 72.3 to 68.9, MalNet-Tiny 92.6 to 73.9, PascalVOC-SP F1
  0.374 to 0.276, Peptides-func AP 0.654 to 0.633 (Tables B.1–B.6)
- Without global attention: ZINC unchanged at 0.070, PascalVOC-SP 0.374 to
  0.302, Peptides-func 0.654 to 0.616
- Performer and BigBird mostly trail full attention; BigBird often trails
  no attention
- LRGB: PascalVOC-SP 0.375, COCO-SP 0.341, Peptides-func 0.654,
  Peptides-struct 0.250, PCQM-Contact 0.334 (Table 6), all against LRGB's
  baselines copied unchanged
- PCQM4Mv2: GPS-medium 0.0858 with 19.4M parameters, against Graphormer
  0.0864 with 48.3M (Table 5)

## Limitations

- **Hyperparameters set by one-at-a-time search**, not a grid, against
  baselines taken from other papers. The authors say graph transformers are
  sensitive to hyperparameters
- **The scalable variants are not the accurate ones.** Every main-table
  configuration uses full attention
- **The expressivity claims are informal**: edge information reaching
  attention via the MPNN (Appendix C.2) and universality by appeal to SAN
- **Ablations change one component** from the best configuration, with 3–4
  seeds, so interactions between components are not measured
