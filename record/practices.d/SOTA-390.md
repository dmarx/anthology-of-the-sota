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
version: 1
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

CogVideoX compares the two in its video DiT, with everything else fixed
(Fig. 8), and full 3D attention wins on FVD and on training loss. It also
measures the cost. One forward pass at 768×1360 for 5s takes 9.60s with
full attention against 4.17s factorized, 2.3× slower (Table 8).

Budget for that cost, because it grows. Attention is quadratic in token
count, so it dominates at video lengths. Wan ([LIT-619](../literature.d/LIT-619.md) §4.3) measures
attention at up to 95% of step time at 1M tokens. That is why the line
turns to context parallelism (2D ring and Ulysses) and to more aggressive
latent compression (Step-Video [LIT-624](../literature.d/LIT-624.md), LTX-Video [LIT-618](../literature.d/LIT-618.md)). Full attention
decides the systems design as well as the quality.

## Conditions

- **One controlled comparison, with numbers in a plot.** The CogVideoX
  ablation appears only in the paper's third arXiv version. Its model size
  and step count are not stated in the text, and the figure's values were
  not extractable here, so this document states the direction and not the
  size. Step-Video's 4B comparison agrees and reports no numbers.
- **It assumes a compressed latent.** The comparison is made at 8×8×4
  compression with 2×2 patches. At higher token counts the 2.3× cost ratio
  grows, and no one reports where factorizing becomes worth it again.
- **The motivation is motion.** Step-Video's unquantified result says the
  advantage shows "particularly [in] high motion". Factorized attention can
  only relate two positions in different frames through an intermediate
  step, and large motion is exactly where related content changes position.
  That is an argument, not a measurement.
- **The record has no evidence on the inverse question.** No document tests
  whether a factorized model given the 2.3× compute back, as depth or width,
  would close the gap.
