---
number: 386
status: Active
formerly:
- SOTA-tmp3b17n
consensus: converged
consensus_note: >-
  Every video report in the record trains on images before or alongside
  video: Stable Video Diffusion (LIT-625), Movie Gen (LIT-626),
  HunyuanVideo (LIT-620), Step-Video (LIT-624) and Wan
  (LIT-619). The later four adopt it without testing it. Movie Gen and
  Step-Video mention unshown experiments. Wan justifies it by throughput.
  Imagen Video (LIT-tmpzs77m), Make-A-Video (LIT-tmpff3eg), Emu Video
  (LIT-tmpyt5og), AnimateDiff (LIT-tmpp7r27) and Open-Sora 2.0 (LIT-tmprr82r)
  all start from an image model or train on images, and none of them tests
  it.
  That is adoption, per DP-005, and it is why the evidence below is the three
  small controlled studies and not the large reports. Read as of 2026-09.
title: 'Show a video diffusion model images before and alongside video'
version: 2
history:
- version: 2
  date: '2026-09-24'
  note: >-
    Five more video reports were checked against this practice. None tests
    it. Imagen Video is the origin of the separate image corpus, asserted
    without numbers. Emu Video and AnimateDiff keep image knowledge by
    freezing instead, and Emu Video's freeze-against-fine-tune result is
    recorded as an adjacent condition.
tags:
- generative-modeling
- training-optimization
- vision-and-graphics
date: '2026-09-24'
source:
- LIT-627
- LIT-621
- LIT-625
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

Ho, Salimans et al. (2022), [LIT-627](../literature.d/LIT-627.md); Blattmann et al. (2023),
[LIT-621](../literature.d/LIT-621.md); Blattmann, Dockhorn, Kulal et al. (2023), [LIT-625](../literature.d/LIT-625.md).

## The claim

**Don't train a video diffusion model on video alone.** Either initialize its
spatial layers from a text-to-image model, or pretrain it on images first.
Then keep still images in the batch once video training starts.

Three controlled comparisons support it, each changing one thing:

- **Adding images to video batches.** Same model, same videos, with
  independent frames appended to each video and temporal attention masked
  for them. FVD falls from 202 with none to 58 with eight ([LIT-627](../literature.d/LIT-627.md),
  Table 4).
- **Image initialization against end-to-end training.** Same architecture on
  driving scenes, with and without a pretrained image LDM underneath. FVD is
  534 against 1155 and FID 48 against 71 ([LIT-621](../literature.d/LIT-621.md), Table 1).
- **Image-initialized against random spatial layers.** Human raters prefer
  the image-initialized model ([LIT-625](../literature.d/LIT-625.md), Fig. 3a).

## Conditions

- **All three results are small.** The first is one seed of a small
  text-to-video model at 16×64×64. The second is a smaller model on driving
  scenes. The third reports only a preference chart with no counts in the
  text. No report tests the claim at the 10B+ scale where it is now always
  used.
- **What "images" means changed.** VDM's images are frames from its own
  videos, and it leaves a separate image corpus to future work. Every later
  report uses a separate, much larger image corpus. That is the version in
  use, and none of the three sources tests it. It first appears in Imagen
  Video ([LIT-tmpzs77m](../literature.d/LIT-tmpzs77m.md) §2.6), which asserts that it "significantly increases
  the overall quality" and shows no numbers.
- **Freezing is a third way to keep what the image model knows.** Emu Video
  ([LIT-tmpyt5og](../literature.d/LIT-tmpyt5og.md)) and AnimateDiff ([LIT-tmpp7r27](../literature.d/LIT-tmpp7r27.md)) freeze the image layers and
  show the video stages no images. Emu Video's controlled result is that
  freezing beats full fine-tuning only narrowly: 55.0 / 58.1 human win rate
  on quality / faithfulness (its Table 1). Nobody compares freezing with
  joint image-video training. The practice's "alongside" clause is untested
  against that alternative.
- **The large reports give a different reason.** Wan presents image-first
  pretraining as a throughput fix: long, high-resolution video starves the
  batch and causes gradient-variance spikes. That is an argument about
  compute, not quality. The practice may be right for both reasons, and only
  the quality reason has been measured.
- **VDM's own explanation was never measured.** VDM says joint training works
  because it "reduces the variance of minibatch gradients". It shows no
  gradient statistics. Cite the FVD numbers, not the mechanism.
