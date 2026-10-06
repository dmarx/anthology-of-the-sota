---
status: Active
title: 'Transform Trained Transformer for Accelerating Native 4K Video Generation'
version: 1
tags:
- attention-techniques
- generative-modeling
- vision-and-graphics
- adaptation-and-tuning
date: '2026-10-06'
published: '2025-12-15'
arxiv: '2512.13492'
first_author: 'Zhang'
keywords:
- 'native-4K-video-generation'
- 'multi-scale-window-attention'
- 'weight-sharing-window-attention'
- 'hierarchical-blocking'
- 'axis-preserving-full-attention'
- 'transformer-retrofit'
- 'step-and-CFG-distillation'
- 'efficient-VAE'
implementations:
- 'T3-Video (zhangzjn/T3-Video; APRIL-AIGC/T3-Video on Hugging Face)'
# Every T3-Video model is a Wan2.1-1.3B or Wan2.2-5B checkpoint with its
# self-attention forward pass rewritten; the weights are Wan's.
extends:
- LIT-619
# Table 5 and Table 9: UltraGen's released 4K model, scored and human-rated.
# Tables 5-7: official Wan and HunyuanVideo run at 4K and 720P.
# Table 7(c): T3 replaced by Swin's shifted windows, same recipe.
compared_against:
- LIT-tmp8ew94
- LIT-619
- LIT-620
- LIT-723
summary: >-
  Zhang, Zhu et al., Zhejiang University and Tencent Youtu (2025),
  ARXIV-2512.13492. Wan's full self-attention is replaced, with no new
  parameters, by the mean of two window attentions using the same weights. One
  attends a contiguous 3D window and the other a strided grid of the same size
  covering the whole video. Window shapes change from layer to layer in a
  five-layer cycle. After fine-tuning, the 4K DiT runs 21.4× faster than
  official Wan2.1-1.3B on one H20 (43× fewer MACs), and scores 71.72 against
  67.43 VQA over UltraGen on a 120-video benchmark the authors built. At 720P,
  the only resolution where full attention is a fair baseline, it falls short
  of Wan slightly (69.37 against 70.56). Every number is one run.
---

# LIT-tmpva88i: Transform Trained Transformer for Accelerating Native 4K Video Generation

Zhang, Zhu, Hu, Wang, Luo, Cao, Gan, Hu, Xue, Li, Wang and Liu, APRIL Lab
Zhejiang University, Tencent Youtu, NUS and PKU (2025) — ARXIV-2512.13492.
Read at v2 (5 October 2026; v1 15 December 2025), main text, impact statement
and references. v2 has no appendix: the metric definitions it points to
("see ??") are missing. The released `wan_video_dit.py` was read for the
window configuration, which the paper does not print.

## Key takeaways

- **The attention is two windows with the same weights** (§3.2, Alg. 1). Q, K
  and V are computed once. They are then attended twice with the original
  projections: once within contiguous windows of shape (m_t, m_h, m_w) (the
  "close" scale), and once within windows of the same size made of tokens
  taken at a stride that spans the whole latent (the "remote" scale). The two
  outputs are averaged before W_O. S = 2 scales is the default. A learnable
  scale weight was tried and did not help. This is the block-plus-grid pair of
  multi-axis attention, but run in parallel with shared weights rather than in
  sequence. The paper does not cite MaxViT. No parameter is added, so the
  module drops in for Wan's self-attention.
- **The windows are 3D, anisotropic and change from layer to layer** (§3.2,
  "MACs-restricted hierarchical strategy" and "axis-preserving
  full-attention"). The text gives only the principle: a different blocking
  every layer, repeated every five layers, with some layers kept full along one
  axis. The released code gives the 4K shapes for the Wan2.1-1.3B latent of
  21×136×240 tokens. Layer 5j: (1, 136, 240), full attention over each latent
  frame, where both paths coincide. Layer 5j+1: (21, 8, 8). Layer 5j+2:
  (21, 17, 6). Layer 5j+3: (7, 8, 30). Layer 5j+4: (3, 17, 40). Two of the
  five layers therefore span all 21 latent frames inside the window, and one
  is a purely spatial 2D window. For Wan2.2-5B (21×68×120) the shapes are
  (1, 68, 120), (21, 4, 6), (21, 4, 20), (7, 17, 8) and (3, 17, 15). The
  shapes are fixed per layer and do not depend on content.
- **MACs and wall clock** (Tables 1–3). With these shapes, DiT attention MACs
  at 2176×3840 fall from 43,299T to 1,007T (43.0×), and whole-DiT MACs from
  44,157T to 1,865T. Measured DiT latency for 50 steps with CFG on one H20
  with FlashAttention-2 falls from 39,662 s to 1,857 s (21.4×). End to end,
  including the decoder, it falls from 79,774 s to 4,166 s. At 720P the MAC
  reduction is 30.9× and the measured gain only 4.7×, which §3.6 attributes to
  low compute density from tiling. Inference at 4K and 81 frames peaks at
  59.5 GB.
- **Recipe** (§3.4, §4.1). Full fine-tuning at 720P on UltraVideo (42K
  clips), 5K iterations at batch 64 on H20s with lr 2e-5. Then 4K, either full
  fine-tuning (500 iterations are said to suffice) or rank-64 LoRA on the
  720P-tuned weights. LoRA straight from the official weights fails at ranks
  32, 64 and 128 (Fig. 7). Without fine-tuning, the transformed model makes
  noise. Close-only and remote-only variants fail to learn even with
  fine-tuning (Fig. 2, qualitative).
- **4K results** (Tables 5–6). On their 4K-VBench, T3-Video-T2V-1.3B scores
  VQA 71.72 and VTC 0.83, against UltraGen 67.43 / 0.75, HunyuanVideo 61.92 /
  0.68 and official Wan2.1 30.01 / 0.37. The LoRA variant scores 70.78 / 0.79.
  On Wan2.2-5B, T2V goes from 47.23 to 67.40 VQA and I2V from 65.13 to 68.84
  against the official models run at 4K. In the human study with 10
  evaluators, T3 is preferred to UltraGen on all four axes, 71.25% on video
  quality (Table 9).
- **The configuration matters** (Table 7, 720P, 5K iterations). Replacing T3
  with Swin's shifted windows (LIT-723) under the same recipe gives 67.34 /
  0.87 against 69.37 / 0.90. This is the paper's only comparison of window
  schemes. A layer schedule with only large block ratios (3 < ratio < 6) gives
  67.14, and one with only small ratios (1 < ratio < 3) gives 68.69, against
  69.37 for the mixed schedule. "Ratio" is not defined beyond these ranges.
- **The transformation is reversible** (§3.3, Table 7a, Fig. 4). Switching the
  720P T3 weights back to full attention and fine-tuning for 500 iterations
  gives 69.51 VQA, against 69.37 for T3 and 70.56 for official Wan.
- **Deployment add-ons** (§3.5, Tables 2, 4, 7e). DMD2-style (LIT-646) 8-step
  plus CFG distillation without the GAN loss cuts DiT time 12.5×. A 9.84M
  decoder ("eVAE") replaces Wan2.1's 73.3M one (LPIPS 0.0251 → 0.04). The
  combined deployment model renders 4K in 166.8 s, with 720P VQA falling from
  69.37 to 67.72.

## Where the hedges are

Per DP-010:

- **The 4K baselines are untuned or from the same group.** Table 5 compares a
  model fine-tuned at 4K with official Wan and HunyuanVideo run zero-shot at
  4K, and with UltraGen (LIT-tmp8ew94), whose first and corresponding authors
  are authors here. No full-attention Wan fine-tuned at 4K on the same data
  appears in Table 5. UltraWan, the one such model, is compared only in
  Table 8, with VBench videos downsampled to 1K.
- **The headline compares 81 frames with 29.** UltraGen's released 4K model
  generates 29 frames, so the +4.29 VQA and the human preference compare clips
  of different length. The "7× over UltraGen" speedup cannot be derived from
  any table, and Fig. 1's latency bars are for 81 frames, which UltraGen does
  not generate at 4K.
- **The paper misstates UltraGen's setup.** §3.2 says UltraGen and UltraWan
  "rely on 128 H20 GPUs" against T3's 64, but UltraGen's own Appendix C
  reports 32 H20 GPUs at batch 32. §3.2 also says UltraGen keeps full
  attention in its first and last two layers, which the UltraGen paper does
  not say.
- **Self-built benchmark, missing definitions.** 4K-VBench is 120 clips drawn
  at random from UltraVideo, whose remaining clips are the training set, with
  the same caption scheme. Five of the seven metrics (DoG, BM, RA, TDS, TEP)
  are defined in a reference that resolves to "??". The VBench table (Table 8)
  shows 66.66%, 100.0% and 00.00% in several dimensions, the signature of a
  handful of prompts per dimension.
- **One run each, small margins.** The Swin comparison (2.03 VQA), the
  layer-ratio ablation (0.68 for small ratios) and the 720P gap to full
  attention (−1.19) are all single runs with no variance reported.
- **"Linear" holds per layer only.** MACs scale linearly with resolution
  only if the window size is fixed. In the released code it is not: the
  window grows with the latent, and every fifth layer is full attention within
  each frame (32,640 tokens at 4K), so that layer stays quadratic in the frame
  size.
- **The regularization argument is not evidence.** §3.3's generalization bound
  is a heuristic (an ℓ0 constraint relaxed to Frobenius, a parameter-count
  bound). Nothing in the experiments tests it.
- **The window shapes are only in the code.** The paper states none of them,
  and the code ships only the 4K settings. The 720P shapes, which every
  ablation in Table 7 uses, are not given anywhere.

## Which comparisons are like for like

- **Table 7(a)** is the clean comparison of T3 against full attention: same
  base model, 720P, where official Wan is in distribution. T3 is 1.19 VQA and
  0.01 VTC below the dense model it was made from, at 4.7× lower DiT latency.
- **Table 7(c)** (T3 against shifted windows) and **7(d)** (layer schedules)
  share recipe, data and iterations, and are the only controlled comparisons
  of window patterns.
- **Tables 5 and 6** compare a fine-tuned model with untuned dense models at a
  resolution those models were never trained for. They show that fine-tuning
  at 4K helps. They do not isolate the attention change.
- **No controlled 3D-against-2D window comparison** and no comparison with a
  sparse-attention method appear. §2.3 says the authors "deliberately do not
  pursue" sparse attention, and §3.6 calls T3 compatible with STA and Sparse
  VideoGen without running either.

## Standing in the anthology

It is a retrofit of Wan (LIT-619): the 1.3B and 5B Wan checkpoints are the
whole model, and only the self-attention forward pass changes. Official Wan
also serves as the baseline at 720P and 4K. At 720P, where the comparison is
fair, the transformed model stays within about 1 VQA point of the original.
HunyuanVideo (LIT-620) is the other untuned dense baseline at 4K, scoring
61.92 VQA against T3's 71.72.

Its nearest neighbour is UltraGen (LIT-tmp8ew94), from an overlapping team,
which also turns a pretrained Wan-1.3B into a 4K model with local plus global
attention. The designs differ in two ways. UltraGen uses 2D spatial windows
that span all frames, plus a separate compressed global branch with its own
LoRA. T3 uses 3D windows whose shape changes by layer, with a strided global
path that shares weights. Against UltraGen's released 29-frame model, T3
reports +4.29 VQA and a 71% human preference on video quality, with the
frame-count caveat above.

Both papers ablate against Swin's shifted windows (LIT-723) and both find
them worse: here by 2.03 VQA at 720P. Multi-scale window attention with
shared weights is a third route to high resolution, besides cascades and the
learned, content-selected sparse attention of SOTA-138. Unlike that, it
chooses nothing from content: every token's neighbours are fixed by its
position and its layer. Prism (LIT-tmpe78xc) retrained it at 2K as a baseline.

Filed without a NOTE: the takeaways come from one full reading of v2. The
window shapes come from the released `wan_video_dit.py`, read as data and not
executed. Figures were read only through their captions and the text that
cites them.
