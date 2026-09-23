---
number: 321
status: Read
formerly:
- NOTE-tmprglmr
paper: LIT-583
title: 'AlphaFold 2'
version: 1
date: '2026-09-23'
summary: >-
  Near-experimental protein structure accuracy at CASP14, a calibrated
  confidence head, self-distillation on confident predictions, and a hard
  dependence on alignment depth below about 30 sequences. Main text and
  Methods read. The supplementary methods (architecture details, ablation
  descriptions) were not read.
---

# NOTE-321: AlphaFold 2

## Contribution

A structure predictor that reaches atomic accuracy in most cases,
validated blind at CASP14 and on post-cutoff PDB chains.

## Key insight

**Reason jointly over the alignment and pairwise geometry, then build
coordinates end to end.** The pair representation is updated with
triangle-consistent operations, and the whole network is iterated on its own
output.

## Key results

- CASP14 backbone: 0.96 Å median against 2.8 Å for the next best
- pLDDT vs lDDT-Cα: r = 0.76. pTM vs TM-score: r = 0.85 (10,795 chains)
- Self-distillation on about 350,000 predicted structures improves the
  network (Figure 4a, magnitude plotted)
- Alignment depth below about 30 sequences: accuracy drops sharply. Above
  about 100: small gains. Without both metagenomic databases: −6.1 GDT, with
  a few targets losing more than 20

## Limitations

- **Needs an alignment.** Orphan and designed proteins are the weak case
- **Poor on chains shaped by partners** in heteromeric complexes
- **Ablations only as plots**, from three seeds of the baseline
- **Supplementary methods not read**
