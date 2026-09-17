---
number: 237
status: 'Active'
formerly:
- SOTA-tmp8nruj
title: 'Match densely without a keypoint detector, because the detector fails where matching is hardest'
version: 1
tags:
- vision-and-graphics
consensus: converged
consensus_note: >-
  Detector-free matching is what the visual-localization benchmarks are led by
  and what the modern geometry systems assume. Not `universal`: sparse
  detect-then-match is still the right answer under a tight compute budget, and
  nothing in this record measures that crossover. The stronger evidence is
  structural — [SOTA-236](SOTA-236.md)'s line removes the matching stage entirely, which only
  makes sense if the detector was already gone.
date: '2026-09-17'
source:
- LIT-387
introduced_by:
- LIT-387
implementations:
- 'LoFTR'
summary: >-
  Sun et al. (2021), [LIT-387](../literature.d/LIT-387.md) — [ARXIV-2104.00680](https://arxiv.org/abs/2104.00680). Establish dense matches
  coarse-to-fine instead of detecting keypoints, describing them and matching
  the descriptors. The detector sets the pipeline's ceiling, and it fails in
  low-texture regions — walls, floors, road — where it cannot emit repeatable
  points, so no downstream matcher can recover a correspondence that was never
  proposed.
---

# SOTA-237: Match densely without a keypoint detector, because the detector fails where matching is hardest

## Source

Sun et al. (2021), [LIT-387](../literature.d/LIT-387.md) — [ARXIV-2104.00680](https://arxiv.org/abs/2104.00680).

## The claim

The classical order is detect, describe, match, and the paper's word for it is
*sequentially*. That ordering is the problem, not the algorithms filling it:
everything downstream is conditioned on what the detector proposed, so the
first stage sets the ceiling.

And the first stage fails somewhere specific — low-texture regions, "where
feature detectors usually struggle to produce repeatable interest points".
Those are walls, floors, sky and road, not an unlucky corner case, and they
are where reconstruction most needs the help. **A matcher cannot recover a
correspondence that was never proposed**, so improving the matcher does not
touch this failure at all.

So: establish dense matches at a coarse level, refine the good ones, and let
attention rather than a cost volume do the work.

## The part that generalises past graphics

Descriptors become **conditioned on both images**. Self and cross attention
mean a location's representation depends on the image it is being matched
*to*.

A detect-then-describe pipeline structurally cannot do this. Description runs
per image, before any pair exists, so a descriptor has to be a summary useful
against *every* possible partner — conservative by construction. That cost is
invisible while the stage exists, because nothing in the pipeline can measure
what a less conservative descriptor would have bought.

**A stage computed before its consumer exists must be conservative, and the
price is only legible once the stage is removed.** That is the transferable
claim, and it is not about vision.

## Conditions

Dense matching costs more compute than sparse detect-and-match, and where the
budget is tight — embedded, real-time on modest hardware — detecting first is
still the right trade. Nothing in this record measures where that crossover
falls.

The evidence is one paper for the recommendation itself, which would normally
make this `unreplicated`. It is filed `converged` on structural grounds
instead: [SOTA-236](SOTA-236.md) records systems that remove the *matching stage entirely*
and recover correspondence as an output, which is a step that only makes sense
if the detector was already gone. The later line presupposes this one.

## The line this belongs to

Three steps, each removing the stage the previous step exposed as the limit:

1. [LIT-386](../literature.d/LIT-386.md) (SuperGlue) — learn the matcher instead of hand-designing
   the heuristics, and keep the detector.
2. **This** — remove the detector; the ceiling it imposed was the real limit.
3. [LIT-385](../literature.d/LIT-385.md) and [LIT-384](../literature.d/LIT-384.md) ([SOTA-236](SOTA-236.md)) — remove matching as a stage; predict
   geometry directly and recover matches from the output.

Each removal was justified by a failure the earlier framing could not express,
which is what makes this a line rather than a sequence of improvements.
