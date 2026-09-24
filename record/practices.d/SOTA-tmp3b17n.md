---
status: Active
consensus: converged
consensus_note: >-
  Every video report in the record trains on images before or alongside
  video: Stable Video Diffusion (LIT-tmprf8ak), Movie Gen (LIT-tmpsjfid),
  HunyuanVideo (LIT-tmpkcchp), Step-Video (LIT-tmpqns7l) and Wan
  (LIT-tmpbr2sl). The later four adopt it without testing it. Movie Gen and
  Step-Video mention unshown experiments. Wan justifies it by throughput.
  That is adoption, per DP-005, and it is why the evidence below is the three
  small controlled studies and not the large reports. Read as of 2026-09.
title: 'Show a video diffusion model images before and alongside video'
version: 1
tags:
- generative-modeling
- training-optimization
- vision-and-graphics
date: '2026-09-24'
source:
- LIT-tmpvcgyq
- LIT-tmpl3mo9
- LIT-tmprf8ak
introduced_by:
- LIT-tmpvcgyq
implementations:
- 'Stable Video Diffusion'
- 'Movie Gen'
- 'HunyuanVideo'
- 'Step-Video-T2V'
- 'Wan2.1'
---

# SOTA-tmp3b17n: Show a video diffusion model images before and alongside video

## Source

Ho, Salimans et al. (2022), [LIT-tmpvcgyq](../literature.d/LIT-tmpvcgyq.md); Blattmann et al. (2023),
[LIT-tmpl3mo9](../literature.d/LIT-tmpl3mo9.md); Blattmann, Dockhorn, Kulal et al. (2023), [LIT-tmprf8ak](../literature.d/LIT-tmprf8ak.md).

## The claim

**Don't train a video diffusion model on video alone.** Either initialize its
spatial layers from a text-to-image model, or pretrain it on images first.
Then keep still images in the batch once video training starts.

Three controlled comparisons support it, each changing one thing:

- **Adding images to video batches.** Same model, same videos, with
  independent frames appended to each video and temporal attention masked
  for them. FVD falls from 202 with none to 58 with eight ([LIT-tmpvcgyq](../literature.d/LIT-tmpvcgyq.md),
  Table 4).
- **Image initialization against end-to-end training.** Same architecture on
  driving scenes, with and without a pretrained image LDM underneath. FVD is
  534 against 1155 and FID 48 against 71 ([LIT-tmpl3mo9](../literature.d/LIT-tmpl3mo9.md), Table 1).
- **Image-initialized against random spatial layers.** Human raters prefer
  the image-initialized model ([LIT-tmprf8ak](../literature.d/LIT-tmprf8ak.md), Fig. 3a).

## Conditions

- **All three results are small.** The first is one seed of a small
  text-to-video model at 16×64×64. The second is a smaller model on driving
  scenes. The third reports only a preference chart with no counts in the
  text. No report tests the claim at the 10B+ scale where it is now always
  used.
- **What "images" means changed.** VDM's images are frames from its own
  videos, and it leaves a separate image corpus to future work. Every later
  report uses a separate, much larger image corpus. That is the version in
  use, and none of the three sources tests it.
- **The large reports give a different reason.** Wan presents image-first
  pretraining as a throughput fix: long, high-resolution video starves the
  batch and causes gradient-variance spikes. That is an argument about
  compute, not quality. The practice may be right for both reasons, and only
  the quality reason has been measured.
- **VDM's own explanation was never measured.** VDM says joint training works
  because it "reduces the variance of minibatch gradients". It shows no
  gradient statistics. Cite the FVD numbers, not the mechanism.
