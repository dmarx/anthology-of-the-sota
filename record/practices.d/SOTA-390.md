---
number: 390
status: Proposed
formerly:
- SOTA-tmpjc9ma
promote_when: >-
  A second controlled comparison of joint 3D against factorized 2D+1D
  attention in a video diffusion transformer, with reported numbers (FVD,
  a human preference rate, or a per-frame metric), with architecture,
  parameter count, data and steps held fixed, by a group other than
  CogVideoX's. Step-Video ran one at 4B and reported "better, particularly
  high motion" with no numbers, which does not count. A report that adopts
  full attention without the comparison does not count either.
consensus: converged
consensus_note: >-
  Every video transformer in the record after CogVideoX uses full
  spatio-temporal attention: HunyuanVideo (LIT-620), Step-Video (LIT-624),
  Wan (LIT-619), Movie Gen (LIT-626), Open-Sora 2.0 (LIT-634).
  HunyuanVideo justifies it by citation, and Step-Video by an unquantified
  4B comparison. Per DP-005, that is adoption. The field agrees and has
  measured it once. Read as of 2026-09.
title: 'In a video diffusion transformer, attend over space and time jointly rather than factorizing, and budget for the cost'
version: 2
history:
- version: 2
  date: '2026-09-24'
  note: >-
    Corrected against a full reading of CogVideoX (NOTE-346). The
    ablation's whole reported result is that factorized attention's FVD is
    "much higher than 3D attention in early steps", and that factorized
    attention is "unstable and prone to collapse". v1 said everything else
    was held fixed, that full attention won on training loss, and that the
    model used 2×2 patches. The text states none of these. The cost is
    1.08× to 2.30× inference time depending on resolution, not a flat 2.3×.
    The ablation is absent from v1, and v2 was not checked. Added
    AnimateDiff's plug-in compatibility as a condition.
tags:
- attention-techniques
- generative-modeling
- vision-and-graphics
date: '2026-09-24'
source:
- LIT-622
introduced_by:
- LIT-622
implementations:
- 'CogVideoX'
- 'HunyuanVideo'
- 'Step-Video-T2V'
- 'Wan2.1'
- 'Movie Gen'
---

# SOTA-390: In a video diffusion transformer, attend over space and time jointly rather than factorizing, and budget for the cost

## Source

Yang, Teng et al. (2024), [LIT-622](../literature.d/LIT-622.md) — CogVideoX.

## The claim

The early video models factorized attention to save compute: spatial
attention within each frame, then temporal attention across frames at each
position. VDM ([LIT-627](../literature.d/LIT-627.md)), Video LDM ([LIT-621](../literature.d/LIT-621.md)) and Make-A-Video
([LIT-632](../literature.d/LIT-632.md)) all do this. **In a transformer over a compressed latent,
attend over all space-time tokens at once.**

CogVideoX compares the two in its video DiT (Fig. 8). The text reports
the whole result in two sentences. With factorized 2D+1D attention, "the
FVD will become much higher than 3D attention in early steps", and
factorized attention "is unstable and prone to collapse". The only setup
it gives is the evaluation: FVD on 500 WebVid test videos. Model size,
steps, resolution, patch size, parameter matching and FVD values are not
stated. The loss curve (Fig. 10b) is cited without comment.

The cost is measured. Table 8 gives inference time for one DiT forward
step on an H800. Full attention is 1.08× the factorized time at 256×384,
1.67× at 480×720 and 2.30× at 768×1360. The ratio grows with resolution
because attention is quadratic in tokens.

Budget for that cost, because it grows. Attention is quadratic in token
count, so it dominates at video lengths. Wan ([LIT-619](../literature.d/LIT-619.md) §4.3) measures
attention at up to 95% of step time at 1M tokens. That is why the line
turns to context parallelism (2D ring and Ulysses) and to more aggressive
latent compression (Step-Video [LIT-624](../literature.d/LIT-624.md), LTX-Video [LIT-618](../literature.d/LIT-618.md)). Full attention
decides the systems design as well as the quality.

## Conditions

- **One comparison, reported in words.** The evidence is a direction
  ("much higher… in early steps") and an instability observation. It is not
  clear whether the FVD gap lasts past early training. The ablation is not
  in the paper's first arXiv version. Step-Video ([LIT-624](../literature.d/LIT-624.md)) ran a 4B
  comparison and reports "better, particularly high motion" with no numbers.
  So the record has two unquantified agreements and no measured margin.
- **The cost grows with resolution.** At 256×384 full attention is nearly
  free (1.08×). At 768×1360 it is 2.30×, and it keeps rising with token
  count. No report says where factorizing becomes worth it again.
- **The motivation is motion.** Factorized attention can relate two
  positions in different frames only through an intermediate step, and
  large motion is where related content changes position. That is an
  argument, not a measurement.
- **Full attention gives up plug-in compatibility.** AnimateDiff ([LIT-633](../literature.d/LIT-633.md))
  keeps the image model's spatial layers seeing one frame at a time so that
  personalized image checkpoints can be dropped in. Joint 3D attention
  removes that option. This is a reason some systems factorize on purpose.
- **The inverse question is untested.** Nothing in the record tests whether
  a factorized model given the extra compute back, as depth or width, would
  close the gap.
