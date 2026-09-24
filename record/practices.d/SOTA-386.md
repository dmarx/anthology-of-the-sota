---
number: 386
status: Proposed
promote_when: >-
  A comparison that holds compute fixed and changes only whether image data
  is present: the same video model, data, steps and per-step token budget,
  trained with and without a separate image corpus, or initialized from an
  image model against from scratch at matched total compute. It should
  report a video metric or human preference with an interval. The
  qualitative agreement of every large report does not count, per DP-005.
formerly:
- SOTA-tmp3b17n
consensus: converged
consensus_note: >-
  Every video report in the record trains on images before or alongside
  video: Stable Video Diffusion (LIT-625), Movie Gen (LIT-626),
  HunyuanVideo (LIT-620), Step-Video (LIT-624) and Wan
  (LIT-619). The later four adopt it without testing it. Movie Gen and
  Step-Video mention unshown experiments. Wan justifies it by throughput.
  Imagen Video (LIT-637), Make-A-Video (LIT-632), Emu Video
  (LIT-635), AnimateDiff (LIT-633) and Open-Sora 2.0 (LIT-634)
  all start from an image model or train on images, and none of them tests
  it.
  LTX-Video (LIT-618 §2.5.4) trains on images alongside video, as one of
  its resolution-duration buckets. That is adoption, per DP-005. The field has
  converged, and no report has isolated the effect. Read as of 2026-09.
title: 'Show a video diffusion model images before and alongside video'
version: 4
history:
- version: 2
  date: '2026-09-24'
  note: >-
    Five more video reports were checked against this practice. None tests
    it. Imagen Video is the origin of the separate image corpus, asserted
    without numbers. Emu Video and AnimateDiff keep image knowledge by
    freezing instead, and Emu Video's freeze-against-fine-tune result is
    recorded as an adjacent condition.
- version: 3
  date: '2026-09-24'
  note: >-
    Status moves from Active to Proposed after full readings of all three
    sources (NOTE-347, NOTE-341, NOTE-336). None separates
    images from compute. VDM's image arms process 20 and 24 frames per step
    against 16, and the paper calls it "a memory optimization to fit more
    independent examples in a batch". Video LDM's pretrained arm gets 73K
    extra image-model steps and trains only temporal layers. SVD's init
    comparison states neither resolution nor steps. None uses a separate
    image corpus: VDM's and Video LDM's images are frames of their own
    videos. Imagen Video, read in full, is joint training with no stated
    image initialization.
- version: 4
  date: '2026-09-24'
  note: >-
    Adds W.A.L.T (ARXIV-2312.06662) Table 5 as a source. It is the only
    ablation found that switches a separate image corpus on and off: FVD
    598.8 → 344.5 at 419M. Compute is not stated, so promote_when is not met
    and the status stays Proposed.
tags:
- generative-modeling
- training-optimization
- vision-and-graphics
date: '2026-09-24'
source:
- LIT-627
- LIT-621
- LIT-625
- LIT-tmpwzgxl
introduced_by:
- LIT-627
implementations:
- 'Stable Video Diffusion'
- 'Movie Gen'
- 'HunyuanVideo'
- 'Step-Video-T2V'
- 'Wan2.1'
---

# SOTA-386: Show a video diffusion model images before and alongside video

## Source

Ho, Salimans et al. (2022), [LIT-627](../literature.d/LIT-627.md); Blattmann et al. (2023), [LIT-621](../literature.d/LIT-621.md);
Blattmann, Dockhorn, Kulal et al. (2023), [LIT-625](../literature.d/LIT-625.md). All three were read in
full as [NOTE-347](../notes.d/NOTE-347.md), [NOTE-341](../notes.d/NOTE-341.md) and [NOTE-336](../notes.d/NOTE-336.md).

## The claim

**Don't train a video diffusion model on video alone.** Either initialize its
spatial layers from a text-to-image model, or pretrain it on images first.
Then keep still images in the batch once video training starts.

Every video report in the record does some version of this. The three
comparisons that come closest to testing it all point the same way, and
none of them isolates the effect:

- **Adding frames to video batches** ([LIT-627](../literature.d/LIT-627.md), Table 4). Same model, data,
  batch size and 200K steps. FVD falls from 202 with no extra frames to 68
  with four and 58 with eight, with temporal attention masked for the extra
  frames. The extra frames are also extra compute: the arms process 16, 20
  and 24 frames per example. The paper calls the change "a memory
  optimization to fit more independent examples in a batch". The table
  cannot separate "images help" from "more independent frames per step
  help".
- **Image initialization against end-to-end training** ([LIT-621](../literature.d/LIT-621.md), Table 1).
  On driving scenes, FVD is 534 against 1155. The pretrained arm gets 73K
  image-model steps the other arm never gets (Table 7), and trains only its
  temporal layers while the other trains everything. Initialization,
  compute and freezing change together.
- **Image-initialized against random spatial layers** ([LIT-625](../literature.d/LIT-625.md), Fig. 3a).
  Human raters prefer the image-initialized model. The figure gives no
  counts, and the text states neither its resolution nor its step count.
- **A separate image corpus, on and off** ([LIT-tmpwzgxl](../literature.d/LIT-tmpwzgxl.md), W.A.L.T Table 5).
  Two 419M models trained with and without ~970M image-text pairs beside
  ~89M text-video pairs. Zero-shot UCF-101 FVD is 598.8 without images and
  344.5 with them. This is the only comparison that uses a separate image
  corpus. Steps, batch size and the video share of each batch are not
  stated, and it is a single run.

## Why it is `Proposed`

The practice is probably right, and the record cannot yet say it believes
it on this evidence. Each comparison gives the image arm more compute, or
bundles initialization with freezing, or states too little of its setup to
check. Only W.A.L.T uses the thing the practice recommends, a separate
image corpus, and it does not say what compute each arm got. VDM's and
Video LDM's "images" are frames drawn from their own video datasets. Every large report adopts the practice, and none of them tests it.
The `promote_when` asks for the one missing comparison.

## Conditions

- **What "images" means changed.** Every report since Imagen Video
  ([LIT-637](../literature.d/LIT-637.md) §2.6) trains on a separate, much larger image-text corpus. Imagen
  Video asserts that this "significantly increases the overall quality" and
  shows no numbers. Imagen Video also states no image initialization, so it
  is the "alongside" half without the "before" half.
- **Freezing is a third way to keep what the image model knows.** Emu Video
  ([LIT-635](../literature.d/LIT-635.md)) and AnimateDiff ([LIT-633](../literature.d/LIT-633.md)) freeze the image layers and show the
  video stages no images. Emu Video's controlled result is that freezing
  beats full fine-tuning narrowly, 55.0 / 58.1 on quality / faithfulness
  (its Table 1). Its unfrozen arm was unfrozen only during the 512px stage,
  and both arms were given the same conditioning images. So the test cannot
  see whether unfreezing damages the image model, which is the reason to
  freeze. Nobody compares freezing with joint image-video training.
- **SVD tests only the first half.** It initializes from an image model and
  never trains on images alongside video.
- **The large reports give a different reason.** Wan presents image-first
  pretraining as a throughput fix: long, high-resolution video starves the
  batch and causes "training instability caused by spikes in gradient
  variance". That is an argument about compute. It may be the real reason
  the practice works, and it is exactly what the three comparisons do not
  control for.
- **VDM's own explanation was never measured.** VDM says joint training works
  because it "reduces the variance of minibatch gradients", and shows no
  gradient statistics.
