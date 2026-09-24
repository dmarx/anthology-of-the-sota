---
status: Active
title: 'Make-A-Video: Text-to-Video Generation without Text-Video Data'
version: 1
tags:
- generative-modeling
- vision-and-graphics
- multimodal-learning
date: '2026-09-24'
published: '2022-09-01'
arxiv: '2209.14792'
first_author: 'Singer'
keywords:
- 'text-to-video'
- 'pseudo-3d-convolution'
- 'image-prior-transfer'
- 'frame-interpolation'
- 'unlabeled-video'
- 'unclip'
implementations: []
extends:
- LIT-070
compared_against:
- LIT-627
- LIT-tmpyt5og
summary: >-
  Singer et al., Meta AI (2022), [ARXIV-2209.14792](https://arxiv.org/abs/2209.14792). An unCLIP text-to-image
  model is extended into video with identity-initialized temporal layers
  trained on video whose captions are discarded. Text alignment comes
  entirely from images. That limits it: it "can not learn associations
  between text and phenomenon that can only be inferred in videos". The
  paper has no ablations, and its title describes the training signal, not
  the data.
---

# LIT-tmpff3eg: Make-A-Video: Text-to-Video Generation without Text-Video Data

Singer et al., Meta AI (2022) — [ARXIV-2209.14792](https://arxiv.org/abs/2209.14792)

## Key takeaways

- **The design.** It builds on an unCLIP-style text-to-image model ([LIT-070](LIT-070.md)):
  a prior, a 64px decoder, and super-resolution to 256px and 768px. 1D
  temporal convolutions and 1D temporal attention are added after every
  spatial layer and initialized as the identity, so training starts from the
  image model (§3.2).
- **Text alignment comes from images, and motion from unlabeled video.** The
  prior is trained on 2.3B English LAION pairs and never sees video. The
  temporal layers learn from WebVid-10M and HD-VILA clips with their text
  thrown away.
- **Results.** Zero-shot MSR-VTT FID is 13.17 and CLIPSIM 0.3049 (Table 1).
  Zero-shot UCF-101 FVD is 367.23 (Table 2). Human raters prefer it to VDM
  ([LIT-627](LIT-627.md)) 84% on quality over 28 prompts (Table 3).
- **Frame rate as a curriculum.** It conditions on fps and trains from high
  fps (less motion) to low fps (more motion). This is asserted.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"Without text-video data"** describes the training signal, not the
  data. WebVid-10M is a captioned stock-footage set whose captions were
  discarded, and HD-VILA pairs its clips with speech transcripts.
- **The consequence is stated, in the discussion.** The model "can not learn
  associations between text and phenomenon that can only be inferred in
  videos", for example the direction of a wave. This is the design's real
  limit, and it is not in the abstract.
- **There are no ablations.** Starting from the image model "significantly
  accelerates the T2V training process" (§1) is the first advantage listed
  in the abstract, and no run without it exists. Every table is a
  system-level comparison.
- **§3.4 contradicts itself.** It says the prior was "trained on images
  alone (no aligned text)", but the prior is trained on text-image pairs.
- **The resolution is overstated.** Footnote 1 says the 768px output is
  downsampled to 512px "for a cleaner aesthetic".

## Standing in the anthology

This is the far end of [SOTA-386](../practices.d/SOTA-386.md)'s claim: an image model supplies all the
text knowledge, and video supplies only motion. The paper shows what that
costs. Anything about text and motion together cannot be learned. That is
why later reports train on captioned video, and why Movie Gen found video
captions beat frame captions almost entirely on motion alignment ([LIT-626](LIT-626.md),
Table 8b).

It supplies no controlled evidence for [SOTA-386](../practices.d/SOTA-386.md). It starts from an image
model and never trains without one.

Filed without a `NOTE`: the takeaways come from one full reading done for
this filing.
