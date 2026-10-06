---
status: Active
title: 'LUVE : Latent-Cascaded Ultra-High-Resolution Video Generation with Dual Frequency Experts'
version: 1
tags:
- generative-modeling
- vision-and-graphics
- adaptation-and-tuning
date: '2026-10-06'
published: '2026-02-12'
arxiv: '2602.11564'
first_author: 'Zhao'
keywords:
- 'ultra-high-resolution-video-generation'
- 'latent-cascade'
- 'video-latent-upsampler'
- 'implicit-neural-representation'
- 'dual-frequency-experts'
- 'low-frequency-expert'
- 'high-frequency-expert'
- 'lora'
implementations: []
extends:
- LIT-619 # every stage runs on Wan2.1-1.3B and its VAE latent
compared_against:
- LIT-619 # Wan2.1-720p and Wan2.1-1K are rows of Table 1
- LIT-tmpe78xc
summary: >-
  Zhao, Chen et al., Nanjing University and Meituan (2026), ICML 2026,
  [ARXIV-2602.11564](https://arxiv.org/abs/2602.11564). A 2K/4K cascade on Wan2.1-1.3B: generate at 720p, upsample
  the latent with a 22M-parameter learned upsampler, renoise, then refine at
  full resolution with two LoRA experts, low-pass inputs into attention for
  high-noise steps and high-pass into the FFN for low-noise steps. Against
  UltraWan and CineScale on the same base, VBench average is 84.34 against
  83.75 at best, and FIDpatch 41.03 against 48.64. Every number is one run.
  Two scores are from an MLLM judge, the FIDpatch reference set is the
  authors' own, and two plain LoRA experts score worse than no experts.
---

# LIT-tmppxw6w: LUVE : Latent-Cascaded Ultra-High-Resolution Video Generation with Dual Frequency Experts

Zhao, Chen, Li, Kang, Lu, Wei, Zhang, Yang and Tai, Nanjing University,
Meituan and Nanyang Technological University (2026), ICML 2026 —
[ARXIV-2602.11564](https://arxiv.org/abs/2602.11564). Read at v2 (27 May 2026), main text and Appendices A–I;
v1 is 12 Feb 2026.

## Key takeaways

- **Three stages** (§3.1, Fig. 3). Low-resolution motion generation runs
  Wan2.1-1.3B at 720p for 50 steps. Video latent upsampling maps the 720p
  latent to the 2K or 4K latent. High-resolution content refinement renoises
  it, skips S = 5 steps and denoises at full resolution for 45 steps
  (Table 9, App. A). The paper's claim against earlier cascades (FlashVideo,
  LaVie, Waver, Seedance, LongCat-Video) is that its high-resolution stage
  is there to fix content and semantics, not only to add detail (§3.1).
- **The latent upsampler** (§3.3, App. C). A VRT-style encoder, an MLP
  implicit-neural-representation upsampler queried at continuous (x, y, t)
  coordinates, and a light VRT decoder, about 22M parameters. It was trained
  on 20,000 UltraVideo clips downscaled 1.5×, 2× and 3×, 135k iterations at
  batch 2, with a latent L1 loss plus a decoded-pixel L1 and frame-difference
  loss on crops. Against latent and RGB interpolation at 2K (Table 5),
  FIDpatch is 41.03 against 47.80 and 51.75, at 0.922 s against 0.004 s and
  40.12 s. Without the pixel loss, decoded video shows blocks. Without the
  decoder, it blurs (Fig. 5).
- **Two experts split by timestep and frequency** (§3.4, Fig. 7). A power
  spectral density analysis of Wan2.1 latents shows low frequencies resolve
  first and high frequencies late (Fig. 6). The low-frequency expert is a
  LoRA on the frozen attention, fed a low-pass-filtered input and trained on
  t ∈ [0.417, 1]. The high-frequency expert is a LoRA on the frozen FFN, fed
  a high-pass input and trained on t ∈ [0, 0.417]. The first is trained on
  clips with HPS v3 above 6.5, and the second on the same clips sharpened by
  unsharp masking. Each trains 3K iterations at 1e-4, after a 15K-iteration
  stage at 1e-5 that adapts the base model to the higher resolution
  (§4.1).
- **Against other Wan2.1-1.3B high-resolution methods** (Tables 1–2).
  VBench average is 84.34 at 2K and 84.03 at 4K, against 83.75 for
  UltraWan-4K, 83.63 for CineScale-2K and 82.98 for Wan2.1 at 720p.
  FIDpatch is 41.03 and 39.87, against 48.64 to 67.72. Doubao-1.5 Pro scores
  Realism, Detailness and Alignment higher for LUVE at both resolutions.
- **Against video super-resolution on the base model's output** (Table 3).
  LUVE scores MUSIQ 58.01, MANIQA 0.410, NIQE 3.16 and DOVER 0.784. The best
  of RealBasicVSR, VEnhancer, STAR and FlashVSR on each are 56.54, 0.407,
  3.20 and 0.761.
- **Cost at 4K, 49 frames** (App. B, Tables 8, 10). Inference takes 91 min
  against 98 min for UltraWan and 132 min for CineScale, at 39.32 against
  44.52 and 40.50 GiB. The experts add 1 min and 0.43 GiB over the same
  pipeline without them.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"A substantial improvement in generative capability"** (Table 1
  caption). The VBench average leads by 0.59 over UltraWan-4K, and LUVE is
  not top on three of the five columns. UltraWan-1K has higher subject
  consistency (95.86 against 95.83) and UltraWan-4K higher imaging quality
  (71.44 against 71.33). Both Wan2.1-1K and UltraWan-1K have higher temporal
  flicker scores. The larger margins are in FIDpatch and the MLLM scores.
- **Two of the four Table 2 metrics are one commercial MLLM's 1–10 scores**
  (Doubao-1.5 Pro, App. H, prompts given). There is no human calibration
  of the judge, and no variance.
- **The FIDpatch reference set is the authors' own.** It is the 4K images of
  UltraHR-eval4k (App. F), from UltraHR-100K by the same first and
  corresponding authors. It is a still-image reference for video frames, 8
  frames from each of 250 videos, with 256×256 patches.
- **Plain LoRA experts make things worse** (Table 6). Two standard LoRA
  experts on the cascade score FIDpatch 47.03, against 46.48 with no
  experts. The frequency filtering, the attention/FFN placement and the
  curated data account for the move to 41.03. Within that, dropping the
  data selection gives 43.77 and dropping the unsharp-mask augmentation
  42.96, about as much as dropping either expert (43.86, 44.44). The gain
  is not attributable to the frequency split alone. Every ablation row is
  one run.
- **The efficiency explanation does not match its own table** (App. B). The
  speed advantage is credited to the upsampler and to experts that "impose
  lower computational overhead than standard LoRA-injected layers". Table 10
  shows the experts cost time. The schedules also differ: LUVE runs 45
  full-resolution steps against UltraWan's 50 and CineScale's 35 after a
  1080p first stage (Table 9). The GPU is not named for inference.
- **The 4K comparisons are at 29 frames** (App. B), UltraWan's limit, and
  the efficiency test at 49. Main-text "Ours-2K" is compared with
  UltraWan-1K and CineScale-2K, so not every row is at the same resolution.
- **The human study** (Table 4, App. E) is 60 prompts and 20 raters, with
  95% intervals whose lower bounds exceed 50% (Table 13). §4.2 calls it
  "pairwise comparisons". App. E describes four methods shown at once in a
  2×2 grid, and the table reports shares that sum to 100% across the four.
- **Smaller inconsistencies.** Table 10 is captioned as a skipped-steps
  ablation but holds the expert-cost comparison. Table 7's "Average" omits
  temporal flicker, so its 80.88 is not Table 1's 84.34 for the same model.
  The text layer of page 6 holds hidden captions for two extra figures,
  PSD against ground truth at 2K, that do not appear on the rendered page.
  The visible spectral evidence is Fig. 6, which is on the base model, not
  on LUVE's output. The project link (github.io/LUVE) has no user name.

## Which comparisons are like for like

- **Tables 1, 2, 4 and 8** compare methods built on the same Wan2.1-1.3B.
  UltraWan and CineScale were LoRA fine-tuned under their own protocols and
  data (App. B). LUVE trains on UltraVideo, the dataset UltraWan
  introduced.
- **Table 3** sets LUVE, which has a trained generator at high resolution,
  against off-the-shelf VSR models applied to the base model's 720p output.
  All four metrics are no-reference. It shows the cascade is better than
  upscaling, not that the experts are better than VSR training on the same
  data.
- **Tables 5–7** are internal ablations at 2K. They share data and
  schedule, and differ only in the named component.

## Standing in the anthology

It extends Wan ([LIT-619](LIT-619.md)) and compares against it. Every stage is
Wan2.1-1.3B: the 720p generator, the 16-channel VAE latent the upsampler
maps, and the frozen backbone the experts adapt. Table 1 shows what the
base model does when simply run larger. Wan2.1 at 1K scores VBench 79.79
against 82.98 at 720p, with imaging quality falling from 68.28 to 58.26 and
aesthetic quality from 56.46 to 49.89. LUVE's 2K output scores 84.34. Fig.
2 shows the failures behind that drop: static motion, repeated content and
blur. The experts are LoRA ([LIT-046](LIT-046.md)) adapters placed by module and fed
filtered inputs, not a new adaptation method.

It is one of the high-resolution routes Prism ([LIT-tmpe78xc](LIT-tmpe78xc.md)) reran as a
baseline. Prism argues for
native 2K training and treats a low-resolution-then-upscale pipeline as
the weaker baseline. LUVE's Table 6 points the other way at 1.3B scale: the
end-to-end high-resolution fine-tune scores FIDpatch 54.10, against 46.48
for the cascade before any expert is added. The two are not in conflict on
the evidence. LUVE's end-to-end arm is a 15K-iteration adaptation of a
small model, and Prism's dense 2K baseline is under-specified. But they are
two papers that report a dense model getting worse when run at higher
resolution and give different remedies. LUVE's Fig. 12 shows subject-token
cross-attention scattered across the canvas without the low-frequency
expert. Prism uses attention maps to blame dilution across redundant
tokens.

It is not a sparse attention paper. It does not group tokens into
spatiotemporal blocks for attention, choose block shapes, select blocks or
compare trainable with training-free sparsity. Its contribution to an
attention question is the placement finding that a global, low-frequency
correction belongs in the attention and a local, high-frequency one in the
FFN. Table 6 tests that only as one expert removed at a time, not as a
swap.

Filed without a NOTE: the takeaways come from one full reading of v2, main
text and Appendices A–I. Figs. 6, 9–16 are images, and only values stated
in the text or tables are quoted. v1 was not compared against v2.
