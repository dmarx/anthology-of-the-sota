---
status: Proposed
promote_when: >-
  A reported ablation (in the main text or by another group) of a
  generative structure model with and without regression-model distillation
  data, measuring hallucination in disordered regions on a disorder
  benchmark. The source's evidence is an Extended Data figure not read here
  and the phrase "greatly reduced".
title: 'When a structure predictor is made generative, add a regression model''s predictions to the training data so disordered regions are learned as disorder rather than invented structure'
version: 1
tags:
- generative-modeling
- data-pipeline
- biomolecular-modeling
date: '2026-09-23'
source:
- LIT-tmpzy774
introduced_by:
- LIT-tmpzy774
consensus: unassessed
consensus_note: >-
  Specific to the move from regression to diffusion heads in structure
  prediction. Whether later diffusion structure models adopted it, and
  whether it transfers to other generative models of structured data, has
  not been assessed here.
implementations:
- AlphaFold 3
summary: >-
  Abramson et al. (2024), [LIT-tmpzy774](../literature.d/LIT-tmpzy774.md) — a diffusion head generates
  plausible compact structure even where the protein has none. AlphaFold-
  Multimer, a regression model, renders the same regions as extended loops.
  Mixing its predictions into training teaches the generative model that
  convention, and "greatly reduced" hallucination. Remaining hallucinations
  are flagged by low confidence but do not look disordered.
---

# SOTA-tmp3m2p6: When a structure predictor is made generative, add a regression model's predictions to the training data so disordered regions are learned as disorder rather than invented structure

## Source

Abramson et al. (2024), [LIT-tmpzy774](../literature.d/LIT-tmpzy774.md). Read as [NOTE-tmp0bufb](../notes.d/NOTE-tmp0bufb.md).

## The practice

- **Expect a generative head to fill gaps with plausible structure.** The
  data under-determines disordered regions, and a sampler resolves that by
  inventing structure
- **Distill from a model that regresses to the mean there.** AlphaFold-
  Multimer's predictions put disorder in an extended, recognizable form.
  Adding them to training teaches the generative model to do the same
- **Rank against it at inference too.** AF3 adds a solvent-accessible
  surface term to its ranking to favor extended over compact inventions

## Conditions

- **The evidence is the source's word and an Extended Data figure** that
  was not read here
- **It imports the teacher's convention, not ground truth.** Extended loops
  are how AF2-style models draw disorder, not what disordered proteins look
  like
