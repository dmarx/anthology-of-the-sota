---
number: 333
status: Read
formerly:
- NOTE-tmprmoo5
paper: LIT-619
title: 'Wan'
version: 2
history:
- version: 2
  date: '2026-09-24'
  note: >-
    Re-read in full, adding §5.2–5.7 (editing, text-to-image,
    personalization, camera control, real-time streaming, audio) and the
    benchmark tables in §4.6–4.7.1. Upgraded from `Skimmed` to `Read`, with
    a claims table, method, recommendations and a bearing section. Four
    corrections to v1: the matched adaLN comparison is against half-shared
    adaLN; named opponents do appear, on VBench and Wan-Bench; the SigLIP
    filter is described as needed for stable image-driven generation, not
    for stable training; and the Table 5 step labels (10k/15k) are the outlier
    against two statements of 100k/150k in the text.
date: '2026-09-24'
summary: >-
  An open 14B text-to-video recipe whose evidence is mostly systems
  measurement: 2D context parallelism cuts communication overhead from over
  10% to under 1%, and caching and 8-bit kernels give 1.62× and 1.27×. Its
  three modelling ablations run on 1.3B text-to-image. Two are read from
  training loss, and on FID one of them favours the rejected option. The
  applications in §5 are demonstrated almost entirely by figures.
---

<!-- inactive-ok-file: SOTA-333 SOTA-386 SOTA-389 SOTA-390 — Proposed, and cited here to weigh the evidence for them; this document is part of that evidence, not an endorsement -->

# NOTE-333: Wan

Read in full from arXiv 2503.20314v2 (19 Apr 2025), §1–7 including all of
§5. Figures whose values are not printed (Figs. 7, 12, 16, 17) could not be
read numerically. The claims resting on them are marked below. VACE and The
Matrix, which §5.2 and §5.6 defer to, were not read.

## Contribution

A complete, reproducible stack for an open video generator with
frontier-competitive benchmark scores. It covers curation, a dense-video
captioner, a 127M causal video VAE, a cross-attention DiT trained by flow
matching, a resolution curriculum, 2D context parallelism, inference
kernels, and seven applications on the same backbone. Weights are released
at 1.3B and 14B.

## Key insight

**At video sequence lengths, the systems constraint shapes the recipe.**
Attention takes up to 95% of step time at 1M tokens. Activation memory is
γLbsh with γ > 60, which puts a 14B DiT at over 8 TB at batch 1 (§4.3.1).
The report presents image-first pre-training, context parallelism over
tensor parallelism, and activation offloading over checkpointing as
consequences of that constraint. None of the three gets a quality argument.

## Assumptions

- Wan-Bench's weighted score tracks human preference. Its weights are
  Pearson correlations from over 5,000 human pairwise comparisons (§4.6),
  and the weights themselves are not published.
- Findings at 1.3B on text-to-image transfer to 14B video (§4.7.2).
- Training loss is a valid comparison across different adaLN layouts and
  text encoders (Figs. 16–17).

## Key results

- **Wan-VAE.** Compresses 4×8×8 into 16 channels with 127M parameters.
  Reconstruction is 2.5× faster than HunyuanVideo's VAE on the same
  hardware (Fig. 7: 720×720, 25 frames, 200 videos). PSNR is shown only as
  a plot. Halving the spatial-upsampler input channels cuts inference
  memory by 33% (§4.1.1).
- **Systems.** 2D context parallelism (CP), with Ring across machines and
  Ulysses within, brings communication overhead at 256K tokens on 16 GPUs
  from over 10% under Ulysses alone to under 1% (§4.3.2). Other gains:
  diffusion cache 1.62×, FP8 GEMM 1.13× on the DiT, and 8-bit
  FlashAttention above 1.27× at 95% MFU on H20 (§4.4). Native FA3-FP8
  "suffers from significant quality degradation", with no figure. The fix
  is INT8 for QKᵀ, FP8 for PV, and FP32 accumulation across blocks,
  because FP8 WGMMA's 14-bit accumulator overflows.
- **Ablations** (§4.7.2). All run on 1.3B, text-to-image, trained from
  scratch at global batch 1536:
  - *adaLN*, 200k steps, training loss (Fig. 16, no numbers). Full-shared
    1.5B at 35 layers beats half-shared 1.5B at 30 layers, which is the
    matched comparison. Non-shared 1.7B does not beat full-shared 1.5B.
  - *Text encoder*, training loss (Fig. 17). umT5 is lowest against
    Qwen2.5-7B-Instruct and GLM-4-9B, each with a token refiner. On FID
    (Table 6), umT5 scores 43.01, Qwen-VL-7B's last layer 43.72 and its
    second-last layer **42.91**.
  - *VAE vs VAE-D*, where a diffusion loss replaces reconstruction (Table
    5 FID): 42.60 vs 44.21, then 40.55 vs 41.16. The gap narrows from 1.61
    to 0.61.
- **Wan-Bench** (Table 2), weighted score: Wan 14B 0.724, Sora 0.700,
  CN-TopA 0.693, CN-TopB 0.690, Wan 1.3B 0.689, HunyuanVideo 0.673, Mochi
  0.639. Wan 14B is lowest of all seven on stylization (0.328). It is
  second-lowest on human artifacts (0.691 vs CN-TopA 0.833), and it trails
  Sora on large motion (0.415 vs 0.482).
- **VBench** (Table 4, external): Wan 14B 86.22, Sora 84.28, Wan 1.3B
  83.96, MiniMax 83.41, HunyuanVideo 83.24.
- **Human preference, text-to-video** (Table 3, win − loss). Overall: 44.0
  vs CN-TopA, 44.0 vs CN-TopB, 48.9 vs CN-TopC and 67.6 vs Runway, over
  about 5,560 rounds. Motion quality is the weakest axis, 9.7 to 16.1
  against the Chinese models. Fig. 1's win/draw/loss bars reproduce these
  gaps, for example 0.69 − 0.25 = 0.44.
- **Image-to-video** (Table 7, about 890 rounds). Overall 10.8 to 81.6.
  Matching is −4.2 against CN-TopA.
- **Captioner** (Fig. 4, F1 on 1,000 videos per dimension vs Gemini 1.5
  Pro). It is better on event, camera angle, camera motion, style and
  color, and worse on the other five. Camera motion is its lowest score:
  48.5 vs 41.4.
- **Applications** (§5.2–5.7). Personalization scores ArcFace 0.5526, second
  to CN-TopA's 0.5655 (Table 8). Editing, text-to-image, camera control and
  audio are shown only in figures. Real-time streaming reports 10–20×
  speedup, 8–16 FPS, and 8 FPS on one RTX 4090 in the text, where Fig. 31's
  caption says 20 FPS. It reports no quality metric.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | 2D CP cuts communication overhead from over 10% to under 1% at 256K tokens | moderate | one measured configuration, stated in text (§4.3.2) |
| C2 | Attention is up to 95% of step time at 1M tokens | moderate | cost model L(αbsh² + βbs²h), no profile shown |
| C3 | Wan-VAE is 2.5× faster than HunyuanVideo's VAE at competitive PSNR | moderate | Fig. 7, plot only |
| C4 | Shared adaLN spent on depth beats adaLN parameters at matched size | weak | training loss, figure without values, T2I at 1.3B |
| C5 | umT5 is the best text encoder | weak | training loss; on FID, Qwen-VL second-last layer is 0.10 better |
| C6 | A reconstruction-loss VAE beats a diffusion-loss VAE for generation | weak | Table 5, narrowing gap, step labels inconsistent |
| C7 | Image-first low-resolution pre-training is needed for throughput and stability | weak | asserted (§4.2.2) |
| C8 | Under 10% synthetic images "significantly degrade" the model | weak | asserted (§3.1) |
| C9 | The diffusion cache is "lossless" | weak | speedup measured, quality not reported |
| C10 | Wan 14B leads existing models | moderate | VBench (external) and Table 2; in Table 2 it is best on only 3 of 14 dimensions |
| C11 | Humans prefer Wan to commercial models | moderate | Tables 3 and 7, about 5,600 and 890 rounds; opponents anonymized, no CIs |
| C12 | First-frame similarity filtering is needed for image-to-video | weak | "early experiments", no threshold or numbers (§5.1.2) |
| C13 | Video and data scaling laws are demonstrated | weak | abstract only; two model sizes, no curve |
| C14 | The V2A model beats MMAudio | weak | five qualitative cases (Fig. 33) |

## Method

The DiT uses 1×2×2 patches, full spatio-temporal self-attention, and
cross-attention to umT5 embeddings of 512 tokens. One timestep MLP (Linear
plus SiLU) predicts six modulation parameters, shared across blocks, with a
learned bias per block (§4.2.1). The objective is rectified flow,
x_t = t·x₁ + (1 − t)·x₀, predicting x₁ − x₀. Timesteps are logit-normal,
with no parameters given (§4.2.2). The curriculum is 256 px text-to-image,
then image and video jointly at 192 px (5 s, 16 fps), 480 px and 720 px,
then post-training at 480 and 720 px. The optimizer is AdamW (weight decay
1e−3, learning rate 1e−4), with the rate lowered on plateaus of FID and
CLIP score. Image-to-video concatenates noise, the VAE latent of the
condition frame padded with zeros, and a mask along channels. A zero-init
projection absorbs the extra channels. CLIP image features enter through
decoupled cross-attention in SFT only. The same mask covers continuation,
first-last frame and interpolation. Personalization prepends K face frames
and inpaints, with no other change to the model (§5.4.1). Streaming
denoises a sliding window of tokens at staggered noise levels. It
re-enters generated tokens "at a noise level of 0" and is distilled to 4
LCM steps (§5.6).

## Concepts

- **Win rate gap**: win − loss, as Fig. 1 confirms. The captions of Tables
  3 and 7 call it a "proportion … preferred", which a −4.2 cannot be.
- **Concept decoupling** (VACE): splitting context frames by mask into
  reactive (F·M) and inactive (F·(1−M)) sequences before encoding.

## Connections

The objective and timestep distribution follow SD3. The I2V
channel-concat-with-zero-init follows SVD and CogVideoX. The personalized
video pipeline is the same pattern with frames prepended. The shared-adaLN
design is PixArt's adaLN-single. Movie Gen Audio ([LIT-626](../literature.d/LIT-626.md) §6.1.2) uses the
same design and asserts it costs nothing. Wan's audio model borrows Movie
Gen's frame-rate-matched additive video conditioning. Wan cites DALL-E 3 for
descriptive recaptioning. Movie Gen keeps TP = 4 alongside CP. Wan argues
CP's communication is lower than TP+SP and drops TP, a design disagreement
that neither report tests head to head.

## Recommendations

- **R1. For long-sequence, non-causal DiT training, shard the sequence
  with context parallelism: Ring Attention across nodes and Ulysses within
  a node.** *Topic:* distributed-optimization. *Status:* experimental.
  *Strength:* moderate. *Conditions:* measured at 256K tokens on 16 GPUs
  against Ulysses alone, not against TP+SP.
- **R2. When per-layer compute exceeds per-layer PCIe transfer, offload
  activations before recomputing them.** *Topic:* systems-optimization.
  *Status:* experimental. *Strength:* weak. *Conditions:* the transfer
  hides behind 1–3 layers of compute. This is argued, not measured.
- **R3. For 8-bit attention on Hopper, quantize QKᵀ to INT8 and PV to FP8,
  and accumulate across blocks in FP32.** *Topic:* numerics-and-precision.
  *Status:* experimental. *Strength:* weak. *Conditions:* the degradation
  and the fix are described with no quality numbers.
- **R4. Condition frame-to-video tasks through one channel-concatenated
  latent and mask with a zero-initialized projection.** *Topic:*
  generative-modeling. *Status:* standard. *Strength:* weak (adoption, no
  ablation). *Conditions:* first-frame similarity filtering was needed for
  image-to-video.

## Bearing on the record

- **[SOTA-386](../practices.d/SOTA-386.md) gets adoption only.** Image-first pre-training is justified by
  throughput and gradient variance, with no ablation (§4.2.2). The image
  corpus is "nearly ten times larger" than the video corpus (§5.3). This
  confirms [SOTA-386](../practices.d/SOTA-386.md)'s condition about the large reports.
- **[SOTA-266](../practices.d/SOTA-266.md) gets adoption only.** Wan states the logit-normal without
  parameters. [SOTA-266](../practices.d/SOTA-266.md)'s `consensus_note` calls Wan "the only video report
  that states it". Movie Gen §3.1.2 states it too.
- **[SOTA-390](../practices.d/SOTA-390.md) gets adoption.** Full spatio-temporal attention has no
  comparison. §4.3.1 is correctly cited for the 95% figure. The streaming
  variant limits attention to a temporal window, a quiet counterexample
  for unbounded length.
- **[SOTA-389](../practices.d/SOTA-389.md)'s Wan condition is confirmed.** The camera-motion finding is
  in §3.3.2. Fig. 4 sharpens it: even the dedicated captioner reaches only
  48.5 F1 on camera motion, its lowest dimension.
- **[SOTA-333](../practices.d/SOTA-333.md) is not moved.** Streamer trains with staggered per-token
  noise levels in a window but conditions on **clean** history (noise level
  0), the opposite of [SOTA-333](../practices.d/SOTA-333.md)'s rollout half. It reports no drift metric.
- **[SOTA-187](../practices.d/SOTA-187.md) gets adoption.** The VAE ablation compares two latents.
- **[SOTA-181](../practices.d/SOTA-181.md) (ring attention)** gets adjacent evidence: Wan keeps Ring
  only as the cross-node layer and uses Ulysses inside it.
- **Should produce:** R1, and a practice on shared timestep modulation
  once someone reports numbers. Wan's figure and Movie Gen's assertion are
  one weak ablation and one adoption.

## Limitations

- "Scaling laws" appears in the abstract and nowhere else. The only size
  comparison is 1.3B vs 14B on benchmarks.
- The ablations are small, on text-to-image, and two are read from training
  loss. The one FID comparison of text encoders favours an encoder that was
  not chosen.
- The synthetic-contamination claim and the curriculum have no experiment.
- Commercial opponents in the human studies are anonymized, and no CIs
  are given. VBench and Wan-Bench do name Sora, HunyuanVideo and Mochi.
- §5 applications are almost entirely qualitative. The editing numbers
  live in VACE, which is not part of this report.

## Open questions

- Does image-first, resolution-progressive pre-training help quality, or
  only throughput?
- Were the VAE runs 10k/15k or 100k/150k steps? The text says it trained
  "for 150,000 training steps until achieving convergence" and measured FID
  "at both 100,000 and 150,000 steps" (§4.7.2). Only Table 5's labels say
  10k/15k, so the table is the likelier error, but the report does not
  settle it.
- Does the Streamer's clean-history re-entry drift over the 15-minute
  rollouts in Fig. 30?

## Corrections to the LIT note

- [LIT-619](../literature.d/LIT-619.md) says: "All three ablations run on the 1.3B model, on
  text-to-image, and two of them are judged by training loss. On the one
  measured by FID (Table 6)…". Two ablations report FID: the VAE ablation
  (Table 5) and the Qwen-VL arm of the text-encoder ablation (Table 6). The
  sentence should read: "…two of them are judged mainly by training loss.
  The VAE ablation (Table 5) and the Qwen-VL arm of the text-encoder
  ablation (Table 6) report FID. On Table 6…"
- [LIT-619](../literature.d/LIT-619.md) says: "The comparisons against commercial models use anonymized
  opponents and the authors' own Wan-Bench." VBench (Table 4) is external
  and names Sora, Kling, Gen-3 and MiniMax. Wan-Bench (Table 2) names Sora.
  Only the human-preference opponents are anonymized. The sentence should
  read: "The human-preference comparisons use anonymized opponents. The
  named comparisons are Wan-Bench, the authors' own, and VBench, a public
  leaderboard."
- [LIT-619](../literature.d/LIT-619.md) says "blind human preference". The report does not say the
  raters were blinded (§4.7.1). Drop "blind".
- [LIT-619](../literature.d/LIT-619.md) says the report "attributes loss spikes to the resulting gradient
  variance". The report says "training instability caused by spikes in
  gradient variance" (§4.2.2). It does not mention loss spikes.
