---
status: Proposed
promote_when: >-
  An independent comparison that tunes this and a strong Adam baseline
  separately and judges at the end of training rather than on intermediate
  checkpoints — the methodology LIT-156 applied to Muon — reporting whether
  the advantage survives, and in which of the domains the original paper
  claims it.
title: 'Halve the optimizer state by keeping momentum only and taking the sign of the update'
version: 1
tags:
- training-optimization
consensus: unreplicated
date: '2026-09-08'
source:
- LIT-090
implementations:
- Lion
summary: >-
  Chen et al. (2023), [LIT-090](../literature.d/LIT-090.md) — [ARXIV-2302.06675](https://arxiv.org/abs/2302.06675). Drop the second moment:
  keep one momentum tensor and take the sign of an interpolation between it
  and the gradient, so every parameter's update has the same magnitude and
  the optimizer carries half the state.
---

# SOTA-tmpougcm: Halve the optimizer state by keeping momentum only and taking the sign of the update

## Source

Chen et al. (2023), [LIT-090](../literature.d/LIT-090.md) — [ARXIV-2302.06675](https://arxiv.org/abs/2302.06675). The optimizer is Lion,
found by program search over optimizer programs rather than designed.

Adam carries two state tensors per parameter, a first and second moment. This
keeps only the first, and replaces the second moment's per-parameter scaling
with the **sign** of an interpolation between momentum and gradient — so
every parameter's update has identical magnitude and the adaptive scaling
disappears. Optimizer state halves, which at large parameter counts is the
term that decides what fits.

The reason it is in the record is not the memory saving on its own. It is
that the reported evidence spans four domains from one group in one paper:
ViT up to +2% on ImageNet with up to 5× less JFT pretraining compute; 88.3%
zero-shot ImageNet on vision-language contrastive training; better FID with
up to 2.3× less training compute on diffusion models; and on autoregressive
and masked language modelling, similar to or better than Adam. That is the
corpus's only cross-domain optimizer result, and until
<!-- inactive-ok: ADR-tmpqq6xc — Proposed, and named as the scope decision that makes this evidence admissible -->
[ADR-tmpqq6xc](../decisions.d/ADR-tmpqq6xc.md) three
quarters of it was outside the record's stated scope.

## Conditions

Two consequences of the sign update are recipe rather than trivia, and the
paper states both:

- **The gain grows with batch size.** At small batch the advantage is small
  or absent, so a comparison run at a convenient batch size is not a
  comparison of the method.
- **The learning rate must be smaller than Adam's**, because taking the sign
  makes the update norm larger. Carrying an Adam learning rate across is the
  obvious way to conclude the method does not work.

The paper also names its own limits, reporting settings where the improvement
is small or not statistically significant, and reports a production
deployment on Google's search-ads CTR model.

## Why `Proposed` rather than `Active`

Everything above is one group's report. The record holds no independent
comparison, and its recent experience with optimizer claims is a caution:
[LIT-156](../literature.d/LIT-156.md) tuned Muon and AdamW separately and judged at the end of training
rather than mid-run, and the advantage fell from roughly 2× to 1.1× at 1.2B —
having found that ranking two optimizers on intermediate checkpoints can
reverse the answer outright. Nobody has done that for this optimizer in the
record's evidence. `unreplicated` is the honest consensus reading: one group,
one result, nobody has agreed or disagreed.

## Where it sits among the record's optimizer advice

A different branch from the live recommendation, not a rival version of it.
[SOTA-165](SOTA-165.md) is the preconditioning line — treat the gradient as a matrix and
precondition it — which [SOTA-121](SOTA-121.md)'s Muon extends by orthogonalising the
momentum. This is not preconditioning at all: it is entrywise, and it throws
away magnitude information rather than reshaping it. The two answer the same
question ("what instead of Adam?") from opposite directions, and the record
holds no comparison between them, so none is asserted here.

## Known implementations

- Lion, and the Google production model the paper names
