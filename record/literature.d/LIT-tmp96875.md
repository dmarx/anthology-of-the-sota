---
status: Active
title: 'Repurposing Diffusion-Based Image Generators for Monocular Depth Estimation'
version: 1
tags:
- vision-and-graphics
- adaptation-and-tuning
- generative-modeling
- data-pipeline
date: '2026-09-25'
published: '2023-12-04'
arxiv: '2312.02145'
first_author: 'Ke'
keywords:
- 'monocular-depth-estimation'
- 'marigold'
- 'affine-invariant-depth'
- 'test-time-ensembling'
- 'synthetic-training-data'
- 'latent-diffusion-fine-tuning'
implementations:
- 'Marigold (prs-eth/marigold-v1-0)'
corrected_by:
- LIT-687
summary: >-
  Ke, Obukhov, Huang, Metzger, Daudt and Schindler (CVPR 2024),
  [ARXIV-2312.02145](https://arxiv.org/abs/2312.02145). Marigold fine-tunes Stable Diffusion v2's U-Net on 74K
  synthetic images to denoise a depth latent conditioned on the image latent,
  with the VAE frozen. It samples 50 DDIM steps and ensembles 10 runs, and
  ranks first on average across five zero-shot depth benchmarks. Its
  step-count curve, one step at ≈34% NYUv2 AbsRel, was measured under
  diffusers' default **leading** spacing, which the paper never names. That is
  the scheduler bug LIT-687 corrects. The claim that a generative prior is
  what helps is not tested.
---

<!-- inactive-ok-file: SOTA-414 SOTA-299 THEORY-052 — Proposed; the practice that replaces
     this paper's recipe, and two documents whose promote_when this paper is
     named as not meeting -->

# LIT-tmp96875: Repurposing Diffusion-Based Image Generators for Monocular Depth Estimation

Ke, Obukhov, Huang, Metzger, Daudt and Schindler (2023; CVPR 2024) — [ARXIV-2312.02145](https://arxiv.org/abs/2312.02145)

## Key takeaways

**The recipe.** The backbone is Stable Diffusion v2 with text conditioning
disabled, trained with the v-objective. Depth is normalized per image by its
2nd and 98th percentiles, replicated to three channels and encoded by the
**frozen** VAE. The image latent and the noisy depth latent are concatenated,
with the first layer duplicated and halved. Only the U-Net is trained, on
Hypersim (54K) and Virtual KITTI (20K) mixed 90/10, with annealed
multi-resolution noise, for 18K iterations: "approximately 2.5 days on a
single Nvidia RTX 4090". Inference is "the DDIM scheduler … 50 steps …
aggregate results from 10 inference runs", with scale and shift aligned
across members and a median merge.

**Main result (AbsRel %, zero-shot):**

| | NYUv2 | KITTI | ETH3D | ScanNet | DIODE |
| --- | --- | --- | --- | --- | --- |
| DPT | 9.8 | 10.0 | 7.8 | 8.2 | **18.2** |
| HDN | 6.9 | 11.5 | 12.1 | 8.0 | 24.6 |
| Marigold, no ensemble | 6.0 | 10.5 | 7.1 | 6.9 | 31.0 |
| Marigold, ensemble of 10 | **5.5** | **9.9** | **6.5** | **6.4** | 30.8 |

**Single-variable ablations** (NYUv2 and KITTI *training* splits, one run
each):
- Annealed multi-resolution noise beats Gaussian noise, 7.7 → 5.6 NYUv2 AbsRel.
- A 10-member ensemble cuts NYUv2 error by "≈8%".
- More denoising steps help, with the "elbow point … always under 10 steps".

## Traps

- **The step curve is a scheduler artifact at its low end.** The paper never
  names its timestep spacing. The released config
  (`prs-eth/marigold-v1-0`) is `DDIMScheduler`, `steps_offset: 1`, with no
  `timestep_spacing` key, so it ran diffusers' default, **leading**: one step
  visits `t = 1` on pure noise. The Fig. 7 readings (≈34% NYUv2 and ≈60% KITTI
  AbsRel at one step) are that mismatch. The paper reads them as "As
  expected, we obtain better results when using more denoising steps".
  [LIT-687](LIT-687.md), with the same weights and trailing spacing, gets 5.7 at one
  step, and finds that more steps then make results worse. The splits differ,
  train against test, but the gap is far larger than a split could explain.
- **"Over 20% performance gains in specific cases"** is NYUv2 against HDN, with
  the ensemble. On DIODE, Marigold is far behind DPT (30.8 against 18.2).
  Without the ensemble it loses KITTI to DPT.
- **"74K training samples"** leaves out Stable Diffusion's LAION pretraining,
  which the table's own footnote admits.
- **The objective is written as ε in §3 and trained as v in §4.** The released
  config says `v_prediction`.
- **The generative prior is asserted, not isolated.** "a comprehensive,
  encyclopedic representation of the visual world" has no arm from a
  non-generative initialization on the same data.
- **Ablations were tuned on the NYUv2 and KITTI training splits**, whose test
  splits then appear in the main table.

## Standing in the anthology

Filed as substrate on 2026-09-25. [LIT-687](LIT-687.md) corrects it on three points:
the step-count conclusion, multi-step denoising as beneficial, and the need
for the generative formulation. It does not overturn ensembling.
[SOTA-414](../practices.d/SOTA-414.md) carries the replacement recipe, which reuses
Marigold's data, conditioning and frozen VAE. [SOTA-416](../practices.d/SOTA-416.md)
can now cite the cost of leading spacing as Marigold's own authors measured it
without knowing: ≈34% NYUv2 AbsRel at one step.

Lin et al. ([LIT-tmp6c6lg](LIT-tmp6c6lg.md)) named the leading-spacing flaw seven months
before this paper was posted. Marigold inherited a library default and never
chose it. That is why the paper cannot be expected to mention it, and why the
record keeps it as a case study.

No relation to [LIT-107](LIT-107.md): Marigold compares the original MiDaS and DPT,
not v3.1. [SOTA-299](../practices.d/SOTA-299.md) and [THEORY-052](../theory.d/THEORY-052.md) both
say, in their own `promote_when`, that a transfer result of this kind would
not move them.
