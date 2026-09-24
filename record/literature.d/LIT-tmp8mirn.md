---
status: Active
title: 'One-step Diffusion with Distribution Matching Distillation'
version: 1
tags:
- generative-modeling
- inference-optimization
- vision-and-graphics
date: '2026-09-24'
published: '2023-11-01'
arxiv: '2311.18828'
first_author: 'Yin'
keywords:
- 'distribution-matching-distillation'
- 'one-step-generator'
- 'fake-score'
- 'real-score'
- 'regression-loss'
- 'variational-score-distillation'
implementations:
- 'CausVid'
- 'Self Forcing'
extends:
- LIT-036
compared_against:
- LIT-038
- LIT-062
- LIT-067
- LIT-075
- LIT-093
- LIT-636
summary: >-
  Yin et al., MIT and Adobe (2023), [ARXIV-2311.18828](https://arxiv.org/abs/2311.18828). DMD distills a diffusion
  model into a one-step generator by descending an approximate KL(p_fake ‖
  p_real), whose gradient is the difference of a frozen "real" score and an
  online "fake" score. It adds an LPIPS regression loss onto precomputed
  teacher ODE outputs. It reaches 2.62 FID on ImageNet-64 and 11.49 on
  zero-shot COCO-30k. The ablation that makes the regression loss look
  necessary ran its no-regression arm at a different learning rate, and its
  mode-collapse evidence is qualitative.
extended_by:
- LIT-631
- LIT-tmpcjcg4
---
<!-- inactive-ok-file: SOTA-392, SOTA-394, SOTA-395 — Proposed practices this paper bears on; named as what the paper informs, not as settled advice -->


# LIT-tmp8mirn: One-step Diffusion with Distribution Matching Distillation

Yin, Gharbi, Zhang, Shechtman, Durand, Freeman and Park, MIT and Adobe
Research (2023) — [ARXIV-2311.18828](https://arxiv.org/abs/2311.18828). Known as "DMD". Read at v4 (Oct 2024).

## Key takeaways

- **The generator gradient is a difference of two scores.** The loss is
  D_KL(p_fake ‖ p_real) (Eq. 1), the reverse direction. Its gradient is
  (s_fake − s_real) · dG/dθ (Eq. 2), evaluated on noised generator outputs
  with t ~ U(0.02T, 0.98T) (Eq. 7). A frozen copy of the teacher gives
  s_real. A second copy, trained online on generator samples with the
  ordinary denoising loss, gives s_fake (Eqs. 5–6, Alg. 1). The generator is
  initialized from the teacher and has no time input (§3.1).
- **A regression loss is added.** The generator is also regressed with LPIPS
  onto teacher outputs from the same noise (Eq. 9, λ_reg = 0.25). The pairs
  come from a deterministic ODE solver: 18 Heun steps for CIFAR-10, 256 for
  ImageNet, 50 PNDM steps for LAION (§3.3). The datasets are 100K pairs
  (CIFAR-10 conditional), 25K (ImageNet-64), 500K (LAION 6.25+) and 12M
  (LAION 6+) (App. B).
- **Both terms matter in the ablation** (Table 2 left, FID on CIFAR-10 /
  ImageNet-64): full DMD 2.66 / 2.62, without distribution matching 3.82 /
  9.21, without regression 5.58 / 5.61. The no-regression arm ran at a
  learning rate of 1e-5 "to prevent training divergence" (App. C.2). The
  full model used 5e-5 on CIFAR-10 and 2e-6 on ImageNet (App. B.1–B.2), so
  the arms differ in learning rate as well as loss.
- **Headline results.** ImageNet-64: 2.62 FID in one step against the EDM
  teacher's 2.32 at 512 passes (Table 1). Zero-shot COCO-30k from SD v1.5 at
  guidance 3: 11.49 against 8.78 for the 50-step teacher, 0.09s against
  2.59s at batch 1 (Table 3). At guidance 8: 14.93 FID and CLIP 0.320
  against the teacher's 13.45 and 0.322 (Table 4).
- **The weighting is its own.** Normalizing the gradient by the mean
  absolute denoising error (Eq. 8) gives 2.66 FID on CIFAR-10, against 3.60
  and 3.71 for the DreamFusion and ProlificDreamer weightings (Table 2
  right). An L2 regression loss instead of LPIPS gives 2.78 against 2.66
  (App. I).

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"To ensure all modes are preserved"** (§3.3) rests on a 2D toy (Fig. 3),
  one qualitative image grid with a repeated grey car (Fig. 5b), and the FID
  row above. There is no recall, coverage or diversity metric anywhere in
  the paper. The stated mechanism is that the score "is invariant to scaling
  of probability density" and s_real is unreliable at low noise (§3.3). The
  paper does not use the words "reverse KL" or "mode-seeking".
- **The regression ablation is not matched.** The no-regression arm changed
  its learning rate (App. C.2). DMD2 (the successor) later removes the loss
  and recovers 2.61 on ImageNet by updating the fake score five times per
  generator step. It also reports the naive no-regression run at 3.48, not
  5.61 (DMD2 Table 3). The loss was needed for this training recipe. That
  does not make it necessary to the method.
- **"Outperforms all published few-step diffusion approaches"** (abstract).
  Unconditional CIFAR-10 gives DMD 3.77 against Consistency Models' 3.55
  (App. Table 6). Baseline numbers in Tables 1 and 6 are copied from Song et
  al., not rerun.
- **The guidance-8 model was tuned by hand during training.** App. Table 5
  logs twelve changes over two weeks on about 80 A100s. Regression weight
  went 0.1, 0.5, 1 and back to 0.25, max DM step went from 980 to 500, and
  the pair count and VAE decoder also changed. FID moved from 23.88 to 14.93.
  The authors say the schedule "may not be the most efficient or optimal".
- **"20 FPS"** is stated for FP16 inference in the abstract and §4.3. No
  table measures it. Table 3's 0.09s latency is at batch 1 without that
  qualifier.

## Standing in the anthology

The record depended on this paper before holding it. CausVid ([LIT-631](LIT-631.md))
distills its causal video student with this objective, and Self Forcing
([LIT-629](LIT-629.md)) scores whole rollouts with it ("DF + DMD", Table 2 there). [SOTA-394](../practices.d/SOTA-394.md)
and [SOTA-395](../practices.d/SOTA-395.md) are built on those comparisons. [SOTA-394](../practices.d/SOTA-394.md) notes that "the
record does not hold DMD or DMD2", and [LIT-631](LIT-631.md) and [NOTE-343](../notes.d/NOTE-343.md) say the same.
This filing and DMD2's retire that gap.

It bears on [SOTA-394](../practices.d/SOTA-394.md)'s diversity condition. CausVid calls its diversity loss
"characteristic of reverse KL" ([LIT-631](LIT-631.md), §6). The objective here is the
reverse KL, but this paper puts its mode-dropping risk on score scale
invariance and low-noise score error. It shows the risk only qualitatively.
Nothing here measures what reverse KL costs in diversity.

It bears on [SOTA-392](../practices.d/SOTA-392.md)'s open condition. That practice asks whether its
distillation balance holds under distribution matching. App. Table 6 puts
DMD at 3.77 unconditional CIFAR-10 FID against 4.85 for 2-Rectified Flow
with distillation. Those numbers are copied across papers and are not a
controlled test.

It uses LPIPS ([LIT-095](LIT-095.md)) for the regression loss, EDM ([LIT-075](LIT-075.md)) and SD v1.5
([LIT-062](LIT-062.md)) as teachers, and FID from [LIT-611](LIT-611.md).

Filed without a `NOTE`: the takeaways come from one full reading done for
this filing, of the main text and Appendices A–J. The videos were not
viewed.
