---
number: 84
status: Proposed
formerly:
- THEORY-tmprhu7e
promote_when: >-
  An experiment that separates the two roles, for example giving AlphaFold
  a deep alignment for the early recycling iterations and a shallow or empty
  one later (and the reverse). It should show that coarse fold accuracy
  depends on alignment depth and refinement does not. The source offers the
  account as a hypothesis to explain a depth threshold.
title: 'AlphaFold 2 needs the sequence alignment to find a protein''s coarse fold, not to refine it, so accuracy collapses below a minimum alignment depth and barely improves above it'
version: 1
tags:
- biomolecular-modeling
- analysis-and-evaluation
date: '2026-09-23'
source:
- LIT-583
summary: >-
  Jumper et al. (2021), [LIT-583](../literature.d/LIT-583.md) — accuracy falls steeply when the
  median alignment depth is below about 30 sequences and gains little above
  about 100. Dropping both metagenomic databases costs 6.1 GDT, almost all
  from a few targets losing 20 or more. The authors' hypothesis is that
  covariation in the alignment is needed early, to place the coarse fold,
  and that refinement to atomic accuracy does not depend on it. The
  threshold is measured. The two-stage account is not tested.
---

# THEORY-084: AlphaFold 2 needs the sequence alignment to find a protein's coarse fold, not to refine it, so accuracy collapses below a minimum alignment depth and barely improves above it

## Source

Jumper et al. (2021), [LIT-583](../literature.d/LIT-583.md), "MSA depth and cross-chain contacts".
Read as [NOTE-321](../notes.d/NOTE-321.md).

## The account

Co-evolving positions in an alignment indicate which residues touch. Given
enough sequences, the network can read out enough contacts to place the
fold, and the rest of the network then refines geometry from learned
physical regularities. Below a threshold, the contacts are too noisy to
place the fold, and refinement has nothing correct to refine. The result is
a threshold rather than a slope.

## What it explains

- The sharp drop below about 30 sequences and the plateau above about 100
  (Figure 5a)
- Why removing metagenomic databases hurts only the few targets they push
  across the threshold
- Why single-sequence protein language models ([LIT-505](../literature.d/LIT-505.md)) are the natural
  fix. They supply the coarse signal from learned priors instead of an
  alignment

## Where it is weak

- **Offered as a hypothesis.** The paper does not separate the two stages
- **The intermediate-structure trajectories** (Figure 4b) show some targets
  settling early and others late, which fits but does not test it
