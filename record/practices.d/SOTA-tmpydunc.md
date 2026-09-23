---
status: Proposed
promote_when: >-
  An independent retraining (for example OpenFold's) that reports what
  self-distillation adds, as a number, with and without it at matched
  compute. Or the same recipe improving a model outside protein structure,
  with the confidence filter ablated. AlphaFold's own evidence is one
  ablation shown as a plot.
title: 'When unlabelled inputs vastly outnumber labelled ones, retrain from scratch on the labelled data mixed with the model''s own high-confidence predictions for unlabelled inputs, under augmentation that stops it copying them'
version: 1
tags:
- data-pipeline
- training-optimization
- biomolecular-modeling
date: '2026-09-23'
source:
- LIT-tmpmz8pl
introduced_by:
- LIT-tmpmz8pl
consensus: unassessed
consensus_note: >-
  Noisy-student self-training predates AlphaFold, and later structure models
  use distillation sets (AlphaFold 3 among them). How much of the gain holds
  up in independent retraining has not been assessed here.
implementations:
- AlphaFold
summary: >-
  Jumper et al. (2021), [LIT-tmpmz8pl](../literature.d/LIT-tmpmz8pl.md) — about 100,000 solved structures and
  billions of sequences. AlphaFold 2 predicted structures for about 350,000
  unlabeled sequences, kept the confident ones, and retrained the same
  architecture from scratch on those plus the PDB. Cropping and alignment
  subsampling mean the student cannot just reproduce the teacher. The
  ablation shows a clear gain. The filter is the model's own calibrated
  confidence ([SOTA-tmpej1tr](SOTA-tmpej1tr.md)).
---

# SOTA-tmpydunc: When unlabelled inputs vastly outnumber labelled ones, retrain from scratch on the labelled data mixed with the model's own high-confidence predictions for unlabelled inputs, under augmentation that stops it copying them

## Source

Jumper et al. (2021), [LIT-tmpmz8pl](../literature.d/LIT-tmpmz8pl.md). Read as [NOTE-tmprglmr](../notes.d/NOTE-tmprglmr.md).

## The practice

- **Label the unlabeled pool with the trained model**, and keep only
  predictions the model is confident in. This needs a confidence estimate
  that tracks accuracy ([SOTA-tmpej1tr](SOTA-tmpej1tr.md))
- **Retrain from scratch, not by fine-tuning**, on a mixture of real labels
  and distilled ones
- **Make the student's input harder than the teacher's.** AlphaFold crops
  and subsamples the alignment, so reproducing a prediction requires
  re-deriving it
- **Keep the real labels in the mix.** Distilled data supplements the
  labeled set, it does not replace it

## Conditions

- **The confidence filter is load-bearing.** Without calibrated confidence,
  errors come back as training labels
- **One system, one plotted ablation.** The gain's size is not stated in
  text
<!-- inactive-ok-file: SOTA-tmpej1tr — Proposed, filed alongside as the confidence filter this practice depends on -->
