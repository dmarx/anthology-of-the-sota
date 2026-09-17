---
number: 173
status: Read
formerly:
- NOTE-tmpvmncl
paper: LIT-387
title: 'LoFTR: Detector-Free Local Feature Matching with Transformers'
version: 1
date: '2026-09-17'
summary: >-
  Remove the keypoint detector and match densely, coarse-to-fine, with
  descriptors conditioned on both images by cross attention. The argument is a
  failure mode rather than an efficiency: detectors cannot emit repeatable
  points in low-texture regions, so no downstream matcher can recover what was
  never proposed.
---

# NOTE-173: LoFTR: Detector-Free Local Feature Matching with Transformers

Read from [LIT-387](../literature.d/LIT-387.md) — [ARXIV-2104.00680](https://arxiv.org/abs/2104.00680).

## The argument, which is about where information is lost

Detection, description, matching — "sequentially" is the word the paper uses,
and the sequence is the problem. A detector proposes locations; everything
downstream is conditioned on that proposal. So the pipeline's ceiling is set
by the first stage, and the first stage fails in a specific, identifiable
place:

> the global receptive field provided by Transformer enables our method to
> produce dense matches in low-texture areas, **where feature detectors
> usually struggle to produce repeatable interest points**

Low-texture regions are not an unlucky corner case. They are walls, floors,
sky, road — a large fraction of indoor and outdoor scenes, and exactly where
reconstruction most needs help. A detector that emits nothing there hands the
matcher an empty set, and a better matcher cannot recover a correspondence
that was never proposed.

## The mechanism, and the thing it makes possible

Coarse dense matches first, then refinement of the good ones. Self and cross
attention rather than a cost volume, which distinguishes it from earlier dense
approaches.

The consequence worth keeping is **conditioning**: a location's descriptor
depends on the *other* image. A detect-then-describe pipeline structurally
cannot do this — description happens per image, before any pair exists, so a
descriptor must be a summary that is useful against every possible partner.
Attention lets it be a summary useful against this one.

That is a general point about staged systems, not about graphics: a stage
computed before its consumer exists must be conservative, and the cost of that
conservatism is invisible until somebody removes the stage.

## Where it sits in the record

Sources [SOTA-237](../practices.d/SOTA-237.md), and completes the middle of a three-step line the
record now holds end to end:

1. [LIT-386](../literature.d/LIT-386.md) — learn the matcher, keep the detector.
2. This — remove the detector, keep matching as a stage.
3. [LIT-385](../literature.d/LIT-385.md) and [LIT-384](../literature.d/LIT-384.md) — remove matching as a stage; it becomes an output
   of predicting geometry directly ([SOTA-236](../practices.d/SOTA-236.md)).

Each step removes the stage the previous step exposed as the limit, and each
removal was justified by a failure the earlier framing could not express. That
progression is the reason this line is worth holding in a record that is
mostly about language models.

## Not filed

The benchmark placements. "Outperforms by a large margin" and two first places
in visual localization are the evidence, and a practice that recommended LoFTR
by name would have dated the moment the next matcher appeared — which, given
step 3 above, it promptly did.
