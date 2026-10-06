---
status: Active
title: 'Pyramidal Flow Matching for Efficient Video Generative Modeling'
version: 1
tags:
- generative-modeling
- flows-and-transport
- vision-and-graphics
- training-optimization
date: '2026-10-06'
published: '2024-10-08'
arxiv: '2410.05954'
first_author: 'Jin'
keywords:
- 'pyramidal-flow-matching'
- 'spatial-pyramid'
- 'temporal-pyramid'
- 'piecewise-flow'
- 'renoising'
- 'autoregressive-video-generation'
- 'blockwise-causal-attention'
- 'video-generation'
implementations:
- 'Pyramid Flow (pyramid-flow.github.io)'
extends:
- LIT-630 # the objective is flow matching's conditional regression, re-posed between resolutions
- LIT-636 # the linear noise-to-data path and the straightness argument for coupled endpoints
- LIT-449 # architecture and initial weights are SD3 Medium's MM-DiT
compared_against:
- LIT-622 # CogVideoX-2B and 5B rows in Table 1, Table 5 and the user study
summary: >-
  Jin, Sun et al., Peking University and Kuaishou (2024), ICLR 2025,
  ARXIV-2410.05954. One 2B DiT runs a flow whose early, noisy segments sit
  at 1/4 and 1/16 of the spatial tokens, and conditions each new latent
  frame on progressively downsampled history. A 10 s, 241-frame clip costs
  at most 15,360 training tokens against 119,040 at full sequence, and the
  whole 768p model took 20.7k A100 hours. VBench total is 81.72, above
  CogVideoX-5B (81.61) and below Kling (81.85) and Gen-3 (82.32). The
  efficiency ablations are one FID curve on images and pictures for video,
  each a single run, and the 20.7k hours start from SD3 Medium weights.
---

# LIT-tmpqhnq9: Pyramidal Flow Matching for Efficient Video Generative Modeling

Jin, Sun, Li, Xu, Xu, Jiang, Zhuang, Huang, Song, Mu and Lin, Peking
University, Kuaishou Technology and Beijing University of Posts and
Telecommunications (2024), ICLR 2025 — ARXIV-2410.05954. Read at v2
(15 Mar 2025), main text and Appendices A–D; v1 is 8 Oct 2024.

## Key takeaways

- **One flow crosses resolutions** (§3.2, Eqs. 5–11). The time axis is cut
  into K windows (K = 3 in every experiment, §4.1). Within window k the path
  runs from an upsampled, noisier latent at resolution 2^-(k+1) to a cleaner
  one at 2^-k, and only the last window is at full resolution. All windows
  are trained by one flow-matching loss in one DiT, with stages sampled
  uniformly per step (§3.4). Uniform windows put the cost near 1/K of a
  full-resolution flow.
- **The two endpoints share one noise draw** (Eqs. 9–10, App. C.4). Start and
  end of each window are built from the same n ~ N(0, I), so the target
  velocity is a difference along one noise direction. A toy 1-D experiment
  (Fig. 13) shows straighter, non-crossing trajectories than independent
  endpoints. That figure is the only evidence for the coupling.
- **Jumps between resolutions need corrective noise** (§3.2.2, App. A).
  Nearest-neighbour upsampling makes each 2×2 block perfectly correlated. A
  rescale plus block-structured noise with negative within-block covariance
  (γ = −1/3, the most decorrelating value that keeps the matrix
  semidefinite) matches the next window's Gaussian. That gives
  x̂_sk = (1 + s_k)/2 · Up(x̂_ek+1) + √3(1 − s_k)/2 · n′ with
  e_k+1 = 2s_k/(1 + s_k), so time rolls back slightly at each jump (Eq. 26).
  Without the noise, samples come out blurred with block artifacts (Fig.
  10, pictures only).
- **History is compressed too** (§3.3, Eqs. 16–17). Generation is
  autoregressive over latent frames. Older frames enter as condition at
  lower resolution, so most history sits at the coarsest scale. History
  latents get noise of strength U[0, 1/3] in training (§4.1), following
  Diffusion Forcing (LIT-554) and GameNGen. The paper puts the token saving
  at up to 1/4^K (§3.3).
- **The attention is dense, not sparse** (§3.4). The pyramids cut tokens
  enough that full-sequence attention is used, not factorized
  spatial/temporal attention, with a blockwise causal mask over latent
  frames. Bidirectional attention across frames gives subjects that change
  shape and colour over a 1 s clip (App. C.2, Fig. 11, pictures only).
  Spatial position encoding is extrapolated across the spatial pyramid and
  interpolated across the temporal one (Fig. 3b).
- **Cost** (§4.2, App. B, Table 4). The 3D VAE compresses 8×8×8. Training
  ran on 128 A100s in three stages: images, 50k steps at 1,536 GPU-hours;
  low-resolution video, 200k steps at 11,520; high-resolution 5–10 s video,
  50k steps at 7,680. The sum is the abstract's 20.7k. A 10 s, 241-frame
  clip needs at most 15,360 tokens per sample, against 119,040 for full
  sequence (§1). Inference for a 5 s 384p clip takes 56 s (§4.2).
- **Results** (Tables 1–2, 5–6, Fig. 4). VBench total is 81.72, quality
  84.74 and semantic 69.62. Total is the highest of the public-data models
  (next is T2V-Turbo at 81.01) and above CogVideoX-5B (81.61). It is below
  Kling (81.85) and Gen-3 Alpha (82.32). On EvalCrafter the final sum is 244,
  against 243 for VideoCrafter2 and 250 and 254 for Pika 1.0 and Gen-2.

## Where the hedges are

Per DP-010:

- **"Almost three times the convergence speed"** (Fig. 7 caption) is read
  off one FID curve, 3K MS-COCO prompts, 20k–60k steps of an early
  text-to-image run. The baseline matched tokens per batch, so the pyramid
  arm saw more samples per step. The gain is per step at equal tokens,
  which is the paper's argument, not a matched-sample comparison.
- **The temporal pyramid ablation has no number in the main text** (Fig. 8).
  It is frames from one pyramid run and one full-sequence run at 100k
  low-resolution steps, with the baseline "far from convergence". Fig. 12b
  adds an MSR-VTT FVD curve over 10k–50k steps with no stated values. The
  corrective-noise and causal-attention ablations (Figs. 10–11) are
  pictures only.
- **"Comparable performance to commercial competitors"** (§4.3). The
  quality score beats Gen-3 (84.74 against 84.11). The semantic score,
  69.62, is below every private-data model in Table 1 and below three of
  the four public-data ones. The authors put this down to coarse synthetic
  captions. The user study (Fig. 4: 50 VBench prompts, 20+ raters, 1,411
  choices in total) has Kling preferred on motion, 67.5% against 32.5%, and
  CogVideoX-5B and -2B preferred on semantics.
- **"Surpasses all the compared open-sourced baselines in these two
  benchmarks"** (§4.3). On EvalCrafter the margin over VideoCrafter2 is one
  point of final sum (244 against 243), and VideoCrafter2 leads on
  text-video alignment by 6.15. Table 6's raw metrics have no LaVie row,
  but LaVie appears in Table 2.
- **The compute comparison crosses hardware** (§4.2). Open-Sora 1.2 is said
  to need "more than two times the computation" from 4.8k Ascend and 37.8k
  H100 hours, against 20.7k A100 hours here. The 20.7k also excludes
  pretraining: the MM-DiT starts from SD3 Medium weights (App. B), and
  Open-Sora's figure is not stated on the same basis.
- **"Comparable" inference speed** (§4.2) gives 56 s for a 5 s 384p clip and
  no baseline time.
- **No seeds or variance** anywhere. Every benchmark number is one model,
  sampled once per prompt.
- **The face-consistency deficit is the temporal pyramid's** (App. C.1, D).
  EvalCrafter face consistency is the lowest in Table 6 (98.89). The
  authors attribute it to compressed history, and §D notes subject drift
  over long clips. The cost of the token saving is therefore measured only
  as this one metric.

## Which comparisons are like for like

- **Fig. 7 (spatial pyramid)** shares data, tokens per batch,
  hyperparameters and architecture with a standard flow-matching baseline
  (§4.4). It is the only matched quantitative comparison in the paper, and
  it is on images.
- **Fig. 8 and Fig. 12b (temporal pyramid)** are matched on setting and step
  count, not on compute. A full-sequence step costs more.
- **Tables 1–2, 5–6** are reported benchmark numbers for models with
  different data, sizes, frame rates and resolutions. Baselines' numbers are
  from the VBench and EvalCrafter leaderboards (App. B, Table 6 caption).
  Only CogVideoX-2B is the same size (2B).

## Standing in the anthology

It extends Flow Matching (LIT-630). Flow matching regresses a velocity onto
a conditional path, and this paper's §3.1 points out that the path need not
end at a standard Gaussian. Pyramidal flow uses that to make each window's
path run between two resolutions, with Eq. 11 the same regression on a
piecewise target. It extends Rectified Flow (LIT-636) in two ways. The path
inside each window is rectified flow's straight interpolation x_t = t·x1 +
(1 − t)·x0 with u = x1 − x0 (Eq. 3). The shared noise draw is justified by
rectified flow's argument that crossing trajectories are what bend a flow
(App. C.4). The piecewise construction is credited to PeRFlow, a piecewise
rectified flow. It does not reflow, and it measures straightness only in
the toy of Fig. 13.

It stands on SD3 (LIT-449) more directly than the abstract says. The 2B
MM-DiT is SD3 Medium's architecture, initialized from its weights, with T5
and CLIP text encoders (App. B). The authors blame the same initialization
for the low human-action score (App. C.1).

It compares against CogVideoX (LIT-622) on VBench and in the user study.
At the same 2B size, its total is 81.72 against CogVideoX-2B's 80.91, and
its quality score 84.74 against 82.18. CogVideoX-2B leads on semantic score
(75.83 against 69.62) and in the user study's semantic column (57.9% to
42.1%). Against the 5B model it is ahead on total by 0.11 and behind on
semantics by 7.42.

It bears on SOTA-187, which recommends training in a compressed latent
rather than at full resolution. This paper takes the same economy one step
further inside the latent: the noisy part of the trajectory runs at 1/4
and 1/16 of the latent tokens. It also bears on SOTA-263, which says that
more pixels need more noise. Here that relationship sets the design. The
low-noise end of each window is at higher resolution, and Eq. 26 rolls the
timestep back at each jump to keep the marginal Gaussian consistent. LTX-Video
(LIT-618) counts it among the 1:2048 compression models, against its own
1:8192.

For Prism (LIT-tmpe78xc), which reran it as a baseline at 2K, it is not an
attention method. It is a training recipe that reduces tokens, with dense
attention and a causal mask over frames. It does not group tokens into
spatiotemporal blocks for attention, choose a block shape, select blocks,
or compare trainable with training-free sparsity.

Filed without a NOTE: the takeaways come from one full reading of v2, main
text and Appendices A–D. Figs. 7, 12b and 13 are curves, and only values
stated in the text are quoted. v1 was not compared against v2.
