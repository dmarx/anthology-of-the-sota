---
status: Active
title: 'LongCat-Video Technical Report'
version: 1
tags:
- generative-modeling
- attention-techniques
- vision-and-graphics
- inference-optimization
- flows-and-transport
date: '2026-10-06'
published: '2025-10-25'
arxiv: '2510.22200'
first_author: 'Cai'
keywords:
- 'video-generation'
- 'video-continuation'
- 'long-video-generation'
- 'block-sparse-attention'
- 'ring-block-sparse-attention'
- 'coarse-to-fine-generation'
- 'multi-reward-grpo'
- 'block-causal-attention'
- 'kv-cache'
implementations:
- 'LongCat-Video (Meituan)'
# Its GRPO is Flow-GRPO's SDE sampling, policy ratio and KL for flow
# matching (A.1.1), modified in four named ways.
extends:
- LIT-779
# Wan2.2 in the internal MOS and GSB studies (Figs. 14-16), Wan2.1 and
# HunyuanVideo as VBench 2.0 rows (Table 8). It also uses Wan2.1's VAE.
compared_against:
- LIT-619
- LIT-620
summary: >-
  Meituan LongCat Team (2025), ARXIV-2510.22200. A 13.6B single-stream video
  DiT that treats T2V, I2V and continuation as one task. Its block sparse
  attention (BSA) cuts the latent into non-overlapping 4×4×4 token blocks,
  mean-pools each block's queries and keys, and lets each query block attend
  to the top-r key blocks by pooled score: 1/16 of them (93.75% sparsity)
  in the 720p refinement stage. Trained there for 500 iterations after 500
  dense ones, it takes refinement from 302.9 to 142.0 s at 189 frames.
  "Near-lossless" quality, the block-size sweep and top-r over top-p
  are asserted without numbers.
---

# LIT-tmpid6gf: LongCat-Video Technical Report

Meituan LongCat Team (contributors listed alphabetically, Xunliang Cai
first), Meituan (2025) — ARXIV-2510.22200. Read at v2 (28 Oct 2025; v1 25
Oct 2025), main text and Appendices A.1–A.3.

## Key takeaways

- **The model** (§3.1, Table 1). 48 single-stream blocks, width 4096, FFN
  16384, 32 heads, AdaLN-Zero, RMSNorm as QK-norm, 3D RoPE, 13.6B
  parameters. Video is encoded with Wan2.1's VAE (4×8×8), then patchified
  1×2×2, for 4×16×16 in total. Text is encoded with umT5.
- **One task, one model** (§3.2, Fig. 5). T2V, I2V and continuation differ
  only in the number of clean condition frames placed before the noisy
  ones, which get timestep 0 and no loss. Condition tokens attend only to
  themselves and skip cross-attention, so their keys and values are cached
  across sampling steps. Pretraining on continuation is credited with
  minutes-long generation without colour drift (Fig. 19, samples only).
- **BSA: the block** (§3.4.2, App. A.2.1, A.2.3). The latent sequence
  (T, H, W) is reordered into N_T × N_H × N_W blocks of t × h × w tokens,
  block-major and then [t, h, w] within each block. Here t = h = w = 4, so
  64 tokens per block in patchified latent units: 16 frames by 64 by 64
  pixels. The shape is fixed, the same for every layer, head and position.
  The kernel is fastest with 128-token query blocks and 1,024-token key
  blocks. 64 was kept for flexibility across resolutions and context
  parallelism.
- **BSA: the selection rule** (App. A.2.1, A.2.3). Q and K are mean-pooled
  within each block. The pooled score is Q_pool·K_poolᵀ/√d per head, and
  each query block keeps the top r key blocks by that score. All tokens of
  a query block share the same r key blocks, and attention within them is
  exact. There is no forced local window, sink or compressed branch. r is
  N_k/8 "during the distillation training phase" and N_k/16 for the
  refinement expert (93.75% sparsity, Table 7). Gradients flow only
  through the selected attention. The rule needs no extra parameters.
- **Top-r against CDF-p** (App. A.2.3). The authors also tried selecting
  key blocks in score order until the cumulative softmax reaches p. They
  report that this "yields better generation quality under high speedup
  ratios in a training-free setting". In training, the uneven number of
  blocks per query block costs time, so top-r was adopted. They report that
  trained top-r reached "lossless" adaptation.
- **Where BSA is trained** (§4.3, Table 7). In the refinement-expert LoRA:
  500 iterations with full attention at 720p (93 or 189 frames), then 500
  with BSA at 93.75%. The refinement stage upsamples a 480p 15 fps output
  to 720p 30 fps, re-noises it to t = 0.5, and denoises in 5 steps
  (§3.4.1).
- **Speed** (Table 2, one H800, FlashAttention-3). For 720p at 93 frames:
  1,429.5 s for 50 dense steps, 244.6 s with 16 distilled steps, 135.3 s
  with coarse-to-fine, 116.5 s with BSA (12.3× in total). For 720p at 189
  frames via coarse-to-fine: 302.9 s without BSA and 142.0 s with it.
  "Less than 10%" of dense attention compute is the sparsity setting. No
  attention-only timing is given.
- **Ring BSA** (App. A.2.2). Under context parallelism, each rank pools its
  own keys, the pooled keys are gathered to build the mask, and ring
  attention then runs on the selected blocks. Forward and backward passes
  are in Triton and released.
- **GRPO** (§3.3, App. A.1). It starts from Flow-GRPO's SDE sampling and
  makes four changes. All group members share one initial noise, and SDE
  noise is injected at one random step among the first 6 of 16. The
  diffusion term is clipped at τ = 0.45. The policy and KL losses are
  reweighted by √(t/(Δt(1−t))) and t/(Δt(1−t)) to cancel a vanishing
  gradient. Advantages are normalized by the maximum group standard
  deviation. Rewards are HPSv3 (two forms), a motion model run on
  grayscale video, and a text-alignment model, with equal weights. HPSv3
  alone produces static video (Fig. 9). Ablations are curves only (Fig. 7).
- **Evaluation** (§5). The benchmarks are internal. For I2V the MOS scores
  are visual quality 3.27 (best), image alignment 4.04, motion 3.59 and
  overall 3.17, against Seedance 1.0's best overall of 3.35. In the T2V GSB
  against PixVerse-V5 the overall count is 242 against 246. On VBench 2.0
  (Table 8) the total is 62.11, behind Veo3 (66.72) and Vidu Q1 (62.70), and
  Commonsense is 70.94 (best).

## Where the hedges are

Per DP-010:

- **"Near-lossless" sparse attention has no number behind it.** The only
  BSA measurements are latencies (Table 2). No table or curve compares
  refinement quality with and without BSA, at either sparsity. Neither the
  claim that block sizes from 64 to 1,024 made "no significant differences"
  nor the claim that CDF-p beats top-r without training comes with a table.
- **BSA was trained for 500 iterations, in a LoRA, on a refinement task.**
  That task starts from an upsampled video re-noised only to t = 0.5. The
  layout is already fixed, so it is a much easier setting for sparse
  attention than generation from noise. The evidence does not reach BSA in
  pretraining or full fine-tuning.
- **Where BSA runs is stated two ways.** A.2.3 gives a sparsity for "the
  distillation training phase" (N_k/8). Fig. 13 and §4.3 attach BSA only
  to the refinement expert, and Table 2's BSA rows are the refinement
  configurations.
- **The speedup from BSA is modest at 93 frames.** It is 135.3 against 116.5
  s (1.16×) end to end. At 189 frames it is 302.9 against 142.0 s (2.13×).
  The headline 10–12× comes mostly from distillation and coarse-to-fine.
- **The physics claim and its table disagree.** The text says leading on
  Commonsense shows the model "excels in aspects such as motion rationality
  and physical laws". On VBench 2.0's Physics dimension it scores 59.92,
  below HunyuanVideo (60.20), Wan2.1 (62.84) and every proprietary row
  except Sora-480p.
- **Internal benchmarks, internal judge.** The MOS is a 2:1 blend of human
  ratings and an in-house VLM judge, said to correlate above 0.92 with
  humans, with no table. Most comparative numbers are only in bar charts
  (Figs. 14–16). Competitor rows in Table 8 carry evaluation dates from
  2025-03 to 2025-09, so they appear to be leaderboard entries rather than
  reruns.
- **Coarse-to-fine "improves generation quality"** rests on a figure of
  samples (Fig. 10).

## Which comparisons are like for like

- **Table 2** is controlled for the system: same model, GPU and step counts,
  with one component toggled per row. It measures time only.
- **Nothing measures BSA against another sparse attention, or against
  dense attention, on quality.** The top-r and CDF-p remarks and the
  block-size remark are the authors' summaries of unshown runs.
- **Figs. 14–16 and Table 8** set the model against systems of different
  size and data, at their default settings.

## Standing in the anthology

It extends Flow-GRPO (LIT-779). Its SDE, transition density and KL term
(Eqs. 23–25) are Flow-GRPO's. Its changes respond to problems it reads off
that formulation. Injecting noise at every step spreads the reward across
all timesteps. The gradient scale κ(t, Δt) vanishes at high noise and with
the small steps that large timestep shifts produce. Group-specific standard
deviations inflate advantages in groups where the reward model is
uncertain. The fix of sharing initial noise and injecting it at a single
step is credited as concurrent with TempFlow-GRPO.

It compares against Wan (LIT-619) and HunyuanVideo (LIT-620) twice. In
the internal human studies, it is preferred to Wan2.2-T2V-A14B on overall
quality, on the strength of text alignment and motion (Fig. 15, counts in
the chart only). In VBench 2.0 (Table 8), its total of 62.11 is above
Wan2.1's 60.20 and HunyuanVideo's 55.30, while it trails both on Physics.
It uses Wan2.1's VAE unchanged.

**It is the BSA that Prism (LIT-tmpe78xc) builds on**, and the paper Prism
cites for it. As described here, BSA is the fixed-shape, mean-pooled,
top-r block attention that Prism's introduction attributes to it. Two
things here bear on Prism's claims. LongCat-Video already reports
exploring a cumulative-probability (top-p) rule and finding it better
without training, and rejected it for training because of load imbalance.
Prism's top-k ∪ top-p keeps a floor but pays the same uneven cost. In
Prism's Table 7 that cost is 10.6 against 9.8 minutes per step. LongCat-Video
also reports that block size made no significant difference (64–128 query,
64–1,024 key tokens) in its setting. Prism argues that block geometry matters.
Neither side shows a table for the point in dispute, and the settings
differ: 720p refinement from a fixed layout here, native 2K joint
video-audio there. Prism's description of this report as one that "scale[s]
the training data" understates it. In Prism's 2K retraining at 90%,
BSA is the worst trainable method (AQ 0.33 against full attention's 0.42).
That is not the "near-lossless" result claimed here, but the two papers
use BSA in very different settings.

For SOTA-138 it is an independent video example of the same ordering:
dense attention first, then sparse training from the dense weights. The
evidence is thin. The dense phase is 500 iterations of a LoRA, the
selection is a pooled score rather than a learned indexer, and nothing is
shown about whether the dense phase was needed. It is not filed as
evidence for the practice.

Filed without a NOTE: the takeaways come from one full reading of v2, main
text and Appendices A.1–A.3. The GRPO derivations in A.1.2 were checked
for their conclusions (Eqs. 6–8), not line by line. Figs. 7, 8, 14–16 and
20 are charts whose values are not printed, and only values given in the
text and tables are quoted.
