---
status: Active
title: 'DiTFastAttn: Attention Compression for Diffusion Transformer Models'
version: 1
tags:
- inference-optimization
- attention-techniques
- generative-modeling
date: '2026-10-06'
published: '2024-06-12'
arxiv: '2406.08552'
first_author: 'Yuan'
keywords:
- 'post-training-compression'
- 'diffusion-transformer'
- 'window-attention-residual-sharing'
- 'attention-sharing-across-timesteps'
- 'attention-sharing-across-cfg'
- 'compression-plan-search'
- 'training-free'
implementations:
- 'DiTFastAttn (project site nics-effalg.com/DiTFastAttn)'
summary: >-
  Yuan, Zhang, Lu et al., Tsinghua, Infinigence AI and SJTU (2024),
  [ARXIV-2406.08552](https://arxiv.org/abs/2406.08552), NeurIPS 2024. A training-free plan, chosen per layer and
  per step by a greedy search on output error, picks from three
  substitutes for attention. One is a 1D diagonal window plus a cached
  full-minus-window residual. The others reuse the previous step's output
  or the conditional branch's output in the unconditional pass. On
  PixArt-Sigma at 2048² the strongest setting keeps 24% of attention FLOPs
  and runs end to end in 22.3 against 39.9 s (1.79×), with FID 22.38
  against 23.67 and IS 49.34 against 51.89. On DiT-512 under its original
  250-step sampler, FID worsens from 3.16 to 4.52. Video results are
  qualitative only. One run per setting.
compared_against:
- LIT-tmpms9qj
- LIT-tmpmuiol
---

# LIT-tmp04qx6: DiTFastAttn: Attention Compression for Diffusion Transformer Models

Yuan, Zhang, Lu, Ning, Zhang, Zhao, Yan, Dai and Wang, Tsinghua University,
Infinigence AI and Shanghai Jiao Tong University (2024), NeurIPS 2024 —
[ARXIV-2406.08552](https://arxiv.org/abs/2406.08552). Read at v2 (18 Oct 2024), main text and Appendices
A.1–A.8. v1 is 12 Jun 2024.

## Key takeaways

- **Three redundancies, three substitutes** (§3.1–3.4, Fig. 2).
  - Window Attention with Residual Sharing (WA-RS, §3.2, Eqs. 1–2). At the
    first step r of a group, compute full attention O_r and window
    attention W_r and cache R_r = O_r − W_r. At each later step k in the
    group, compute only W_k and output W_k + R_r. The window is a fixed
    band along the diagonal of the attention matrix, 1/8 of the token count
    wide (§4.1). The motivation is Fig. 3a: the residual changes less from
    step to step than the window output does.
  - Attention Sharing across Timesteps (AST, §3.3). Reuse a layer's
    attention output from an earlier step.
  - Attention Sharing across CFG (ASC, §3.4). Reuse the conditional pass's
    attention output in the unconditional pass. The motivation is SSIM ≥
    0.95 between the two for some heads and steps (§1).
- **The plan is searched, not fixed** (§3.5, Alg. 1, App. A.2, A.7). For
  each step, then each layer, the search tries the strategies [AST,
  WA-RS+ASC, WA-RS, ASC] in order of compression. It keeps the first one
  whose mean relative absolute error on the model output stays under
  (i/|M|)·δ, where i is the layer index. If none passes, the layer stays
  dense. δ runs from 0.025 (D1) to 0.15 (D6). The searched plans differ
  between DiT and PixArt-Sigma (Fig. 5, Figs. 11–13). The authors read this
  as the reason a plan has to be searched per model. Search time is 3–5 min
  for DiT-512, 16–22 min for PixArt-1024 and 1h23m–1h50m for PixArt-2K
  (Table 6).
- **Image results** (Table 1, Tables 3–4; 50-step DPM-Solver, A100).
  - DiT-XL-2 512², ImageNet, 50K samples. Attention FLOPs fall from 100%
    to 34% (D6). IS falls from 408.16 to 352.20, and FID falls from 25.43
    to 16.80.
  - PixArt-Sigma 1024², COCO captions, 30K samples. At D6, 37% of
    attention FLOPs: FID 23.94 against 24.33, IS 52.73 against 55.65,
    CLIP 31.18 against 31.27. End to end it takes 10.31 against 12.76 s.
  - PixArt-Sigma 2048². At D6, 24% of attention FLOPs: FID 22.38 against
    23.67, IS 49.34 against 51.89, CLIP 31.28 against 31.47. Total time is
    22.27 against 39.86 s and attention time 10.13 against 27.57 s.
- **The savings grow with resolution** (Table 2). Alone, WA-RS keeps 77%,
  51% and 33% of attention FLOPs at 1K, 4K and 16K tokens, with latency at
  85%, 54% and 35%. ASC alone keeps 50% at every length. WA-RS and ASC
  together keep 38%, 26% and 16%.
- **The original DiT sampler is less forgiving** (Table 5; 250-step
  IDDPM, CFG 1.5). FID goes 3.16 / 3.09 / 3.10 / 3.54 / 4.52 and IS 219.97
  / 218.20 / 210.36 / 196.05 / 180.34 for raw, D1, D2, D3 and D4, while
  total time falls from 32.62 to 26.96 s.
- **Ablations** (§4.5, Fig. 9, DiT-XL-2-512, curves only). At equal
  attention FLOPs the combined plan beats each technique alone. AST is the
  best single technique until the search stops finding steps it can share.
  More sampling steps allow more compression at the same IS. Window
  attention without the cached residual drops IS sharply at the same
  compression.
- **Video** (§4.3, Fig. 7, App. A.3, Fig. 10). Open-Sora 1.1, 240p, 16
  frames, 200-step IDDPM. Compute reductions of 7.63% to 40.52% over five
  thresholds. Quality is judged by looking at the frames.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"Up to 76% of attention FLOPs and 1.8× end to end" is one setting at
  one resolution.** Both numbers are PixArt-Sigma at 2048² and D6 (Table 1,
  Table 4). At 1024² the same threshold gives 1.24× end to end (12.76 /
  10.31 s), and at 512² on DiT the attention module is a third of total
  time (2.26 of 6.66 s at batch 8). The paper says this in its own words:
  the method only reduces the cost of attention (Limitations).
- **On DiT-512 the main table's FID moves in the opposite direction to
  quality.** FID improves from 25.43 to 16.80 as compression rises while IS
  falls by 56 points (Table 1). The guidance scale of this 50-step setting
  is not stated. Under DiT's own setting (Table 5), D3 already moves FID
  from 3.16 to 3.54 and IS from 219.97 to 196.05, so the text's statement
  that D1–D3 "nearly matched" the original does not hold there.
- **No measure of distance from the uncompressed output.** Image quality
  is reported only as FID, IS and CLIP against the dataset. None of these
  checks that the compressed model produces the same image. Lower-than-raw
  FID at 2048² (22.38 against 23.67) is therefore not evidence of fidelity.
  The later papers that run it (below) report PSNR to the dense output,
  and it is between 21.4 and 24.6 dB.
- **A latency jump the FLOPs do not explain.** DiT-512 total time goes
  6.45 s at D2 to 2.89 s at D3 while attention FLOPs go from 69% to 59%
  (Table 1, Table 3). The non-attention part of the time falls from 4.40 to
  1.98 s, which attention compression cannot produce. The paper does not
  comment.
- **The video claim has no metric.** §4.3 lists five reductions for "D1
  through D6", from "five thresholds from 0.01 to 0.05", at a different
  threshold scale from the image results. App. A.3 is a subjective
  assessment by the authors. The reductions are labelled "computation"
  without saying whether this is attention or total.
- **The calibration set is not described.** Alg. 1 searches on model
  outputs, but the paper does not say how many prompts or class labels
  the plan is searched on, or whether they overlap the evaluation prompts.
- **No variance.** Each configuration is one run of 30K or 50K samples.
  Differences such as CLIP 31.27 against 31.25 are below any stated noise
  floor.
- **The memory cost is named but not measured.** AST stores earlier
  attention outputs (Limitations), and no table gives the extra memory.

## Which comparisons are like for like

- **Tables 1, 3–5** compare each compression setting with the same
  pretrained model, the same sampler and the same evaluation set. Nothing
  else changes. There is no comparison with another acceleration method:
  no token merging, no feature caching such as DeepCache, and no other
  sparse attention.
- **Table 2** isolates each technique at a fixed sequence length, as a
  ratio of attention FLOPs and latency to the dense kernel. It has no
  quality column.
- **Fig. 9 left** compares the techniques alone and combined at matched
  attention FLOPs on DiT-512. It is the only matched-budget comparison,
  and it is shown as curves.

## Standing in the anthology

It is the record's earliest training-free attention compression for
diffusion transformers. The models it runs on are DiT ([LIT-448](LIT-448.md)) and
PixArt-Sigma. Of its three parts, only the window is sparse attention in
the sense the later papers use. The window is a band on the flattened
token order. For an image in raster order, that is a run of neighbouring
rows, not a 2D tile. Two techniques reuse cached outputs across steps
or across the classifier-free guidance pair ([LIT-693](LIT-693.md)). Those are closer to
feature caching than to sparsity.

Two later papers run it as a baseline, and both take only part of it.
Sparse VideoGen ([LIT-tmpms9qj](LIT-tmpms9qj.md)) runs "DiTFastAttn (Spatial-only)" on
CogVideoX-v1.5 and HunyuanVideo at 720p and treats it as the spatial-head
half of its own spatial/temporal split. On CogVideoX-v1.5 text-to-video it
reaches 1.56× (338 against 528 s) at PSNR 23.20 and LPIPS 0.256 against
the dense output, where Sparse VideoGen reaches 2.28× at PSNR 29.99. On
HunyuanVideo it reaches 1.82× at PSNR 21.42, against 1.92× at 29.55. There its
Imaging Quality is the highest in the table (67.33 against 66.11 for dense
attention), so the low PSNR measures distance from the dense video and not
a loss on that metric.

VMoBA ([LIT-tmpmuiol](LIT-tmpmuiol.md)) runs it at a stated density of 0.50 on Wan 2.1-1.3B.
In the training-free setting at 33K tokens it is the closest to the dense
output by PSNR (22.67, against 16.00 for VMoBA), at 1.18× (89 against 103
s). At 76K tokens it reaches 1.31× at PSNR 24.50. Applied without training
to a fine-tuned full-attention model at 55K tokens, it lowers Subject
Consistency from 90.86 to 83.33 and Background Consistency from 94.69 to
88.59. VMoBA does not say which of the three techniques or which threshold
it ran. It says it removed caching "tricks", and AST, ASC and the residual
in WA-RS are all caches. DiTFastAttn has no density setting, so "0.50" is
VMoBA's description, not one of this paper's configurations.

SpargeAttention v1 ([LIT-tmpxwbvb](LIT-tmpxwbvb.md)) mentions it only in related work. It
says DiTFastAttn is limited to plain DiTs and does not work with MMDiT
models such as CogVideoX. Sparse VideoGen's table shows the window part
running on CogVideoX-v1.5.

For the record's questions about video block-sparse attention: it does not
group tokens into 2D or 3D tiles. Its window is 1D on the flattened
sequence, and its window size is fixed at 1/8 of the tokens. What is chosen
from content is which technique each layer uses at each step, by
calibration against output error. It has no top-k or top-p block
selection, and it is training-free throughout. The authors list that
as a limitation: it "cannot take advantage of training to avoid the
performance drop".

Filed without a NOTE: the takeaways come from one full reading of v2, main
text and Appendices A.1–A.8. Figs. 3–5 and 7–14 are heat maps, curves and
images, and only values in the text and Tables 1–6 are quoted. The
end-to-end ratios at 1024² and the non-attention times are this note's
arithmetic from Tables 3–4.
