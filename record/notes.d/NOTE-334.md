---
number: 334
status: Read
formerly:
- NOTE-tmp012dg
paper: LIT-626
title: 'Movie Gen'
version: 1
date: '2026-09-24'
summary: >-
  At 5B, flow matching beats v-prediction diffusion on quality by 3.3 annotation
  σ, but on text alignment by only 1.9σ. Video-native captions beat
  captions stitched from three frames on alignment by 2.9σ. Every σ in the
  paper is rater variance, and each ablation arm was trained once. The Llama 3
  block beats a DiT block that differs only in norm, activation and bias.
  The scaling claim rests on image-only runs covering less than a quarter of a
  decade of compute.
---

<!-- inactive-ok-file: SOTA-333 SOTA-386 SOTA-389 SOTA-390 — Proposed, and cited here to weigh the evidence for them; this document is part of that evidence, not an endorsement -->

# NOTE-334: Movie Gen

Read in full from arXiv 2410.13720v2 (26 Feb 2025): §§1–8 and Appendices A–D.
Everything was read, including audio (§6), personalization (§4), editing (§5)
and the audio-metric correlation study (C.3). The only unread material is the
videos behind the go.fb.me links. No claim below depends on them.

## Contribution

This paper reports two foundation models. Movie Gen Video is a 30B joint
text-to-image and text-to-video transformer that works in the latent space
of an 8×8×8 temporal autoencoder (TAE). Movie Gen Audio is a 13B
video-and-text-to-audio DiT. Three post-trained variants follow:
personalization, instruction editing trained without paired video-editing
data, and audio extension. The report is unusual for its field because it
runs **controlled human-rated ablations** of the objective, the captioner
and the block design (Table 8). It also measures its own rater variance
(Table 40) and releases non-cherry-picked generations on two public
benchmarks.

## Key insight

**Keep the parts simple and LLM-shaped, then scale them.** The generator is a
Llama 3 block with three changes: cross-attention to text, adaLN for the
timestep, and bidirectional attention (§3.1.3). It trains with a
straight-path flow-matching objective. Most of the paper's measured gains
come from what surrounds that core: captions, curation, supervised
fine-tuning (SFT) and evaluation. The report does not isolate the
architecture as a cause of its quality.

## Assumptions

- Human pairwise A/B judgments with a majority vote of 3 raters (6 for
  realness and aesthetics) are the measure of quality. The paper says FVD
  and IS "do not correlate" with them and shows no numbers (§3.5.3).
- The σ used to call a result significant is **rater variance only**. It
  comes from repeating one A/B annotation four times on 381 prompts
  (App. C.1). Seed and training-run variance are not estimated.
- Ablation findings at 5B, 352×192 and 4–8 s transfer to the 30B, 768 px,
  16 s model. The paper asserts this and does not test it.

## Key results

- **Table 8, 5B ablations.** Values are net win rates (win% − loss%) on
  Movie Gen Video Bench-Mini (381 prompts). "Every aspect of the model except
  for the design decision being tested is held constant" (§3.6.2). The σ
  column divides each value by Table 40 (text faithfulness 3.74, overall
  5.07):

  | ablation | Q | A | Q/σ | A/σ |
  |---|---|---|---|---|
  | (a) flow matching vs v-pred, zero-terminal-SNR diffusion | 16.53 | 7.08 | 3.26 | 1.89 |
  | (b) LLaMa3-Video captions vs LLaMa3-FramesRewrite | −0.80 | 10.80 | 0.16 | 2.89 |
  | (c) Llama 3-like block vs DiT block | 18.63 | 12.60 | 3.67 | 3.37 |

  Under the paper's own rubric (significant beyond 2σ, moderate between 1σ
  and 2σ, on par within 1σ; Table 6 caption), the (a) alignment win is
  *moderate*. The paper never applies σ to Table 8. The division is this
  note's.
- **The caption sub-results are in prose only.** (b)'s gain is "most of the
  increase coming from motion alignment (+10.7%) particularly on prompts that
  require … a high degree of motion (+16.1%)" (§3.6.2). No σ is given, and
  the sentence does not say whether +16.1 is motion alignment or total
  alignment on the high-motion subset. Raters preferred the video captions
  themselves 67% to 15%.
- **The arms.** The frame baseline captions the first, middle and last
  frames, and LLaMa rewrites them into one caption. Both arms train on the
  same 21M landscape videos (§3.6.2). The DiT arm differs from the Llama 3
  arm only in norm (LayerNorm vs RMSNorm, with its eps and affine),
  activation (SiLU vs SwiGLU) and FC biases (Table 9).
- **Scaling (Table 10).** Four sizes (5B, 9B, 17B, 30B) were trained on the
  256 px text-to-image stage only, over 1e22 to 1.7e22 FLOPs. Parabola
  minima are plotted on an *overlaid* Llama 3 law.
- **SFT** beats the pre-trained model by +34.65 overall and +9.97 on
  alignment (Table 7). The final model also averages several SFT runs, and
  that step is not ablated (§3.3).
- **TAE vs frame-wise AE** (Table 11). On video, PSNR is 32.25 vs 34.11 and
  FID 1.4872 vs 0.9352. On images, PSNR is 32.16 vs 30.83. The baseline has
  8 latent channels and the TAE has 16, and the paper attributes the image
  gain to that difference.
- **Outlier penalty loss (OPL)** (Table 13). Video PSNR goes from 31.11 to
  31.93, but image FID gets *worse*, 0.568 → 0.614. Table 12 compares 2.5D
  and 3D TAEs: 3D gains 0.29 dB PSNR, and its FID is worse (4.715 vs 3.678).
- **External comparisons (Table 6)**, overall quality: +35.02 vs Runway
  Gen3, +60.58 vs Luma, +8.23 vs Sora (σ ±5.07) and +3.87 vs Kling 1.5. It
  loses to Kling on motion completeness (−10.04). The Sora arm used 500
  linear steps and a manual best-of-5 (App. C.2), where §3.4 describes
  50-step linear-quadratic sampling as the comparison setting.
- **Editing (§5).** Backtranslation beats standard fine-tuning on the
  model's own edits: 70.23 overall and 44.66 text, as win rates where 50 is
  a tie (Table 21). Stage II is preferred to Stage I 89.29 overall
  (Table 22). The TGVE+ win rate against EVE is 74.38 overall (Table 18).
- **Audio.** Most Table 30 margins are large. Against ElevenLabs on real
  videos, overall 13.2±21.5 and naturalness 8.7±21.5 fall inside their CIs.
  The 13B-vs-9B scaling step is 11.0±21.3 (Table 35). The 300M point in
  that table is a different architecture (Vyas et al.).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Flow matching beats v-pred ZTSNR diffusion on video quality at 5B | moderate | Table 8a, 3.3σ annotation; one run per arm, one scale |
| C2 | …and on text alignment | weak | Table 8a, 1.9σ, moderate by the paper's rubric |
| C3 | The FM advantage "hold[s] across a range of model sizes" | weak | asserted, no data (§3.6.2) |
| C4 | Video-native captions improve alignment with no quality cost | moderate | Table 8b, A 2.9σ, Q 0.16σ |
| C5 | The caption gain is mostly motion alignment | weak | prose-only sub-axis numbers, no σ, ambiguous subset |
| C6 | The Llama 3-style block beats the DiT block | moderate | Table 8c, for the bundle in Table 9 only |
| C7 | Llama 3 scaling laws predict media-model sizes | weak | image-only, 4 sizes, under a quarter decade, overlaid law |
| C8 | The TAE is "comparable" to a frame-wise AE on video at 8× more compression | moderate | Table 11, 1.86 dB PSNR gap, channels confounded |
| C9 | OPL improves reconstruction | moderate | Table 13 video; image FID contradicts "improves both" |
| C10 | Small curated SFT gives a large quality gain | moderate | Table 7, 6.8σ; compute and averaging not controlled |
| C11 | 50 linear-quadratic steps emulate 250 or 1000 linear steps | weak | asserted; Fig. 10 shows motivation, not a match |
| C12 | Validation loss tracks human judgment | weak | Fig. 15, 4 checkpoint pairs, consistency sign mixed |
| C13 | Initializing from text-to-image beats joint training from scratch | weak | asserted, "significantly worse", no numbers (§3.2.2) |
| C14 | Backtranslation beats fine-tuning on the model's own edits | moderate | Table 21, no CI, text alignment falls |
| C15 | Audio quality improves with scale to 13B | weak | Table 35, last step's CI includes 0, first step confounded |

## Method

The TAE inflates an image VAE with 1D temporal convolution and attention,
uses symmetric replicate padding, and trains with OPL (r = 3, weight 1e5).
The objective is X_t = t·X₁ + (1 − (1 − σ_min)t)·X₀ with σ_min = 1e−5, where
the model predicts velocity. Timesteps t are logit-normal(0, 1), "as in
prior work (Esser et al., 2024)" (§3.1.2). Patches are 1×2×2, and factorized
learnable position embeddings are added at every layer. Three text encoders
feed the model: UL2, ByT5 and Long-prompt MetaCLIP. The recipe is 256 px
text-to-image, then joint 256 px, then 768 px, with images at 1:10 in the
joint stages (Table 3). SFT follows, with model averaging. A 7B upsampler
takes output to 1080p. Sampling is Euler with the linear-quadratic
schedule, plus LLaMa3 prompt rewriting. Parallelism combines TP, SP, CP and
FSDP (Fig. 8). TP is 4 in every video stage and CP at most 2 (Table 3). Wan
([LIT-619](../literature.d/LIT-619.md)) argues for CP instead of TP.

## Concepts

- **Net win rate**: win% − loss%, in [−100, 100]. It is not the editing
  section's win rate, where 50 is a tie.
- **Linear-quadratic t-schedule**: the first 25 steps of an N-step linear
  schedule, followed by 25 quadratically spaced steps.
- **Cross-paired data**: a reference face from another clip of the same
  person. It trades identity score for natural expression (Tables 15, 17).

## Connections

Extends Emu Video's multi-stage recipe and its quality-tuning idea from Emu.
It uses the SD3 objective and timestep distribution, with no ablation of the
distribution itself. The audio DiT shares one timestep MLP across layers
with per-layer biases and asserts this "saves parameters without sacrificing
performance" (§6.1.2). Wan ([LIT-619](../literature.d/LIT-619.md)) later ablates the same design. Wan's
audio model also cites Movie Gen for frame-rate-matched additive video
conditioning. The report's video DiT is Llama-shaped while its audio model
is a plain DiT, so its own evidence for "Llama beats DiT" is applied to one
of its two models.

## Recommendations

- **R1. Train the video generator with straight-path flow matching and
  logit-normal timesteps rather than v-prediction diffusion.** *Topic:*
  generative-modeling. *Status:* standard. *Strength:* moderate for
  quality, weak for alignment. *Conditions:* the evidence is one 5B run per
  arm, rated by humans. The path and the timestep distribution changed
  together.
- **R2. Caption training video with a model that sees the video.**
  *Topic:* data-pipeline. *Status:* experimental. *Strength:* moderate.
  *Conditions:* the baseline was 3 frames rewritten into one caption, and
  the captioner was fine-tuned for the job.
- **R3. Finish with SFT on a small, manually curated set.** *Topic:*
  adaptation-and-tuning. *Status:* standard. *Strength:* moderate.
  *Conditions:* shown for video (Table 7) and audio (Table 36). Continued
  training compute is not matched.
- **R4. Measure rater variance by repeating annotations, and read
  pairwise results against it.** *Topic:* analysis-and-evaluation.
  *Status:* experimental. *Strength:* moderate as method. *Conditions:*
  this σ misses training variance, so it is a floor on the real
  uncertainty.
- **R5. Add an outlier penalty to the autoencoder loss when decoded
  output shows spot artifacts.** *Topic:* representation-and-encoding.
  *Status:* experimental. *Strength:* weak. *Conditions:* the effect was
  measured on the paper's TAE, and image FID got worse.

## Bearing on the record

- **[SOTA-266](../practices.d/SOTA-266.md) is confirmed with a narrower reading.** Table 8a is
  16.53/7.08, and [SOTA-266](../practices.d/SOTA-266.md) quotes it correctly as +16.5/+7.1. It also
  correctly notes that the alignment margin is under 2σ (1.89). The
  ablation changes **both halves together**, the straight path and the
  logit-normal, against v-pred diffusion, so it supports the combined
  practice and cannot separate the halves. **[SOTA-266](../practices.d/SOTA-266.md)'s `consensus_note` is
  wrong** where it says that for the logit-normal "Wan is the only video
  report that states it". Movie Gen §3.1.2 states logit-normal(0, 1), and
  its audio model uses it too (§6.1.1).
- **[SOTA-389](../practices.d/SOTA-389.md) is confirmed, with one precision fix.** Its numbers are all in
  the text: +10.8, −0.8, 67% vs 15%, +10.7 and +16.1. The +10.7 and +16.1
  come from §3.6.2 prose, not Table 8b, and have no σ. [SOTA-389](../practices.d/SOTA-389.md) presents
  +16.1 as motion alignment on high-motion prompts. The sentence can also
  be read as total alignment on that subset. The baseline was
  "FramesRewrite" (3 frames), not per-frame captions in general.
- **[SOTA-386](../practices.d/SOTA-386.md) adopts, without evidence.** Movie Gen asserts that
  initializing from text-to-image beats joint training from scratch at
  equal GPU hours and shows no numbers (§3.2.2). This matches [SOTA-386](../practices.d/SOTA-386.md)'s
  note of "unshown experiments".
- **[SOTA-390](../practices.d/SOTA-390.md) adopts.** The paper uses full bidirectional attention and
  never compares it with factorized attention in the generator. Its one 2.5D
  vs 3D test is in the autoencoder (Table 12). There 3D is marginally
  better on SSIM and PSNR and worse on FID, and 2.5D was kept for cost.
  That result is adjacent to [SOTA-390](../practices.d/SOTA-390.md) and not evidence for it.
- **[SOTA-187](../practices.d/SOTA-187.md) adopts.** Table 11 compares two latents, not latent against
  pixel.
- **[SOTA-333](../practices.d/SOTA-333.md) is unaffected.** The audio extension's segment-level
  autoregressive generation is not per-token noise.
- **[SOTA-034](../practices.d/SOTA-034.md) (SwiGLU)** gets no clean evidence. Table 8c bundles SwiGLU
  with RMSNorm and bias removal.
- **Should produce:** R3 (curated SFT, two modalities, one group) and R4
  (rater-variance protocol). A backtranslation-for-editing practice is also
  possible, but its evidence is a single comparison (C14).

## Limitations

- One training run per ablation arm, and σ covers raters only.
- All ablations are at 5B and 352×192. Their transfer to 30B is assumed.
- The architecture ablation varies norm, activation and bias only. adaLN,
  cross-attention and bidirectional attention are shared by both arms.
- **Label and text inconsistencies:** Table 40 swaps the σ values of motion
  completeness and naturalness relative to Table 6 (3.98/1.68 vs
  1.68/3.98). The text says 3D TAE and OPL "improve" metrics that Tables 12
  and 13 show getting worse. Table 15's cross-paired row (71.79) differs
  from Table 14's matching row (71.91).
- Editing and personalization results have no CIs. The audio CIs are wide,
  often ±20.
- No weights were released.

## Open questions

- Does the FM win survive a second seed, and does it come from the path or
  from the logit-normal?
- Would a frame captioner given as many tokens as the video captioner close
  the caption gap? Caption detail and "watching video" are not separated.
- Would a DiT block with SwiGLU and RMSNorm match the Llama block? If so,
  8c is about two components, not a family.

## Corrections to the LIT note

- [LIT-626](../literature.d/LIT-626.md) says: "**Sampling.** A 50-step linear-quadratic schedule matches
  250 linear steps (Fig. 10)." Fig. 10 plots per-step change in block
  input/output and the two schedules. It shows no quality comparison. The
  match is asserted in §3.4.2 ("closely approximate") with no metric. The
  sentence should read: "…is asserted to match 250 linear steps (§3.4.2).
  Fig. 10 shows the motivation, not a measurement."
- [LIT-626](../literature.d/LIT-626.md) says: "Video captions beat frame captions by +10.8 on alignment,
  almost all of it motion alignment (+16.1 on high-motion prompts; Table
  8b)." Table 8b holds only −0.80 and 10.80. The motion figures are prose in
  §3.6.2, the paper says "most", not "almost all", and the baseline
  captions three frames. The sentence should read: "…by +10.8 on alignment
  (Table 8b), most of it motion alignment (+10.7, and +16.1 on high-motion
  prompts; §3.6.2, no σ)."
