---
number: 343
status: Read
formerly:
- NOTE-tmpj1xug
paper: LIT-631
title: 'CausVid'
version: 2
history:
- version: 2
  date: '2026-09-24'
  note: >-
    DMD and DMD2 are now filed; the parenthetical saying neither was held is
    replaced with their codes. The reading is otherwise unchanged.
date: '2026-09-24'
summary: >-
  Distilling a bidirectional video DiT into a 4-step block-causal student
  with distribution matching gives a streaming generator: 1.3s to the first
  frame and 9.4 fps, against 219.2s and 0.6 fps for the teacher. At equal
  initialization a bidirectional teacher makes a better causal student
  than a causal one (VBench 94.7 / 64.4 / 30.1 against 91.9 / 61.7 / 28.2).
  The causal teacher is also the weaker model, so the paper's
  error-accumulation explanation is not isolated.
---

<!-- inactive-ok-file: SOTA-333 SOTA-386 SOTA-389 SOTA-390 — Proposed, and cited here to weigh the evidence for them; this document is part of that evidence, not an endorsement -->

# NOTE-343: CausVid

Read in full from arXiv v4 (23 Sep 2025): the main text, the supplementary
section bound into the PDF (VBench-Long Table 7, Figs. 10–11), and all
tables. Figures were read from captions. Fig. 7 (user study) and Fig. 8
(imaging quality over 30 s) give no values in the text, so none are quoted
from them. The video results on the project page were not viewed.

## Contribution

A recipe for turning a pretrained bidirectional video diffusion
transformer into a few-step autoregressive generator, with four parts:

- **Block-causal attention:** bidirectional within a chunk of latent
  frames and causal across chunks (Eq. 5).
- **Initialization:** the student is first regressed onto the teacher's
  ODE endpoints.
- **Asymmetric distillation:** the causal student is trained with DMD
  against a *bidirectional* teacher.
- **KV caching** at inference.

The paper also shows zero-shot image-to-video, streaming video-to-video
and prompt switching.

## Key insight

**The teacher does not have to share the student's constraint.** DMD
matches distributions, not trajectories, so teacher and student can have
different architectures (§2). That lets the causal student learn from a
teacher that sees the whole clip. The paper argues that a causal teacher
would pass its own accumulated errors on.

## Assumptions

- **A strong bidirectional teacher exists** with the same architecture as
  the intended student, apart from the mask. The teacher here is "similar
  to CogVideoX". Its parameter count is not stated. §5.1 calls CogVideoX-5B
  "similarly scaled".
- **A 3D VAE that encodes 16 frames into a 5-latent-frame chunk.** The
  chunk size and the latency floor both follow from this (§5, §6).
- **Training length is 10 s at 352×640 and 12 fps.** Longer videos are
  produced by sliding-window inference over 10 s segments (§5.1).
- **Four fixed denoising steps** at timesteps [999, 748, 502, 247].

## Key results

- **Ablation** (Table 4), all 10 s videos, temporal quality / frame
  quality / text alignment on VBench:

  | model | steps | scores |
  |---|---|---|
  | bidirectional teacher | 100 | 94.6 / 62.7 / 29.6 |
  | causal, fine-tuned from teacher | 100 | 92.4 / 60.1 / 28.5 |
  | no ODE init, bidirectional teacher | 4 | 93.4 / 60.6 / 29.4 |
  | ODE init, no teacher | 4 | 92.9 / 48.1 / 25.3 |
  | ODE init, causal teacher | 4 | 91.9 / 61.7 / 28.2 |
  | ODE init, bidirectional teacher | 4 | 94.7 / 64.4 / 30.1 |

- **Speed** (Table 3), 10 s, 120 frames, 640×352, one H100, including text
  encoder and VAE: first-frame latency 1.3 s and 9.4 fps. The teacher takes
  219.2 s at 0.6 fps, CogVideoX-5B 208.6 s at 0.6 fps, and Pyramid Flow
  6.7 s at 2.5 fps. Fig. 1's caption says 128 frames for the same 219 s.
- **Short video** (Table 1, 128 MovieGen prompts): 94.7 / 64.4 / 30.1. The
  best other model is MovieGen at 91.5 / 61.1 / 28.8. Each model is run at
  its own length.
- **Long video, about 30 s** (Table 2): 94.9 / 63.4 / 28.9. FIFO-Diffusion
  scores 93.1 / 57.9 / 29.9 and is higher on text alignment.
- **VBench-Long** (Table 7, 946 prompts): total 84.27, against Gen-3's
  82.32. Temporal flickering is 96.24, the lowest in the table (others
  98.57–99.30). Dynamic degree is 92.69, the highest.
- **Zero-shot tasks:** image-to-video 92.0 / 65.0 / 28.9 against
  CogVideoX-5B's 87.0 / 64.9 / 28.9 (Table 6). Video-to-video 93.2 / 61.7 /
  27.7 against StreamV2V's 92.5 / 59.3 / 26.9 on 60 DAVIS videos (Table 5).
- **Training cost:** 1,000 ODE pairs and 3,000 iterations at 5e-6 for the
  initialization, then 6,000 DMD iterations at 2e-6. Guidance scale 3.5 and
  a DMD2 update ratio of 5. About 2 days on 64 H100s (§5).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | A bidirectional teacher gives a better causal student than a causal teacher | moderate | Table 4, one controlled pair. One seed (seed 0), VBench on 128 prompts, no variance |
| C2 | The reason is that the causal teacher's error accumulation transfers to its student | weak | Fig. 8 curves only. The causal teacher is also worse at 10 s (92.4 / 60.1 / 28.5 against 94.6 / 62.7 / 29.6), and §4.2 gives "weaker teacher" as a reason too. The ablation does not separate them |
| C3 | ODE-regression initialization improves the distilled student | moderate | Table 4: 93.4 / 60.6 / 29.4 → 94.7 / 64.4 / 30.1, one pair |
| C4 | The 4-step student matches or exceeds its 100-step teacher | weak | Table 4 scores are within 0.1–1.7 points. The user study (Fig. 7) is 29 prompts × 3 ratings per pair with values only in the figure. Flicker and diversity are worse by the authors' account |
| C5 | Streaming at 1.3 s latency and 9.4 fps on one H100 | strong | Table 3, a direct measurement that includes the VAE and text encoder |
| C6 | The method "effectively mitigates error accumulation" | weak | Table 2 compares against other models at about 30 s. Fig. 8 has no values. §6 reports degradation on "extremely long" videos. The 14-minute video is one example with "slight overexposure" |
| C7 | The student is less diverse and flickers more | weak | Asserted in §5.2 and §6. Flicker is consistent with Table 7. Diversity is not measured |
| C8 | Image-to-video and video-to-video work zero-shot | weak | One table each against one or two baselines (Tables 5, 6) |

## Method

1. Initialize the student from the teacher's weights with the block-causal
   mask. Generate 1,000 ODE solution pairs from the bidirectional teacher,
   and regress the student onto the clean endpoints at the four student
   timesteps (Eq. 6).
2. Train with DMD (Alg. 1). Split a sampled video into chunks and give each
   chunk its own timestep from the 4-step set. Noise the chunks, predict
   the clean video with the block-causal mask, re-noise at one random t,
   and update the student with the score difference between the frozen
   teacher (s_data) and an online critic (s_gen). The critic is trained on
   the student's outputs with the denoising loss.
3. Infer chunk by chunk (Alg. 2). Denoise a chunk in 4 steps against the KV
   cache. Then run one forward pass on the *clean* output at t = 0 and
   append its keys and values to the cache.

The causal-teacher baseline is the teacher with causal masks, fine-tuned
with a per-chunk independent timestep "following Diffusion Forcing". At
inference it is "conditioned on the previously generated clean chunks"
(§4.2).

## Concepts

- **Asymmetric distillation:** a teacher and student that differ in
  attention structure. Here the difference is bidirectional against causal.
- **Block-causal attention:** a chunk of k latent frames attends to itself
  and to earlier chunks (Eq. 5). With a KV cache no mask is needed at
  inference (§4.4).
- **Latency and throughput:** time to the first frame, and frames per
  second after it. CausVid reports both (Table 3). Self Forcing later
  defines "real time" by requiring both ([LIT-629](../literature.d/LIT-629.md)).

## Connections

It extends DMD ([LIT-tmp8mirn](../literature.d/LIT-tmp8mirn.md)) and DMD2 ([LIT-tmpcjcg4](../literature.d/LIT-tmpcjcg4.md)) from images to
causal video. It borrows per-chunk independent noise from Diffusion Forcing
([LIT-554](../literature.d/LIT-554.md)). Self Forcing ([LIT-629](../literature.d/LIT-629.md)) replicates it inside its own framework as
"DF + DMD". It argues that CausVid's DMD loss matches the wrong
distribution, because the student's training outputs come from noised
ground-truth context rather than its own rollouts.

## Recommendations

- **R1.** To distil a causal few-step video generator, use a bidirectional
  teacher, not a causally fine-tuned one. *Topic:* generative-modeling.
  *Status:* experimental. *Strength:* moderate (C1). *Conditions:* one
  ablation. The effect may be teacher quality rather than teacher
  causality (C2).
- **R2.** Initialize a few-step student by regressing onto teacher ODE
  endpoints before distribution matching. *Topic:* training-optimization.
  *Status:* experimental. *Strength:* moderate (C3). *Conditions:* one
  controlled pair, with the student and teacher at the same architecture.
- **R3.** Report first-frame latency and throughput separately, end to end
  including the VAE. *Topic:* analysis-and-evaluation. *Status:* standard.
  *Strength:* moderate. *Conditions:* §6 shows the VAE sets the latency
  floor, so a diffusion-only timing understates it.

## Bearing on the record

| practice | disposition |
|---|---|
| [SOTA-333](../practices.d/SOTA-333.md) per-token noise in training, noised history at rollout | adopts the training half only. Adds a quality-over-time curve for that half without the rollout half |
| [SOTA-386](../practices.d/SOTA-386.md) images before and alongside video | adoption. Distillation uses "a mixed set of image and video datasets following CogVideoX" (§5), untested |
| [SOTA-187](../practices.d/SOTA-187.md) train in a compressed latent | adds a condition. Temporal compression sets a streaming latency floor: five latent frames before any pixel (§6) |
| [SOTA-390](../practices.d/SOTA-390.md) full 3D attention | no test. The teacher is CogVideoX-like, and the student restricts attention causally across chunks |
| [SOTA-206](../practices.d/SOTA-206.md) keep a multi-step option | not addressed. The student is fixed at 4 steps |
| [SOTA-266](../practices.d/SOTA-266.md), [SOTA-389](../practices.d/SOTA-389.md) | no bearing. The teacher's objective and captions are not described |

On [SOTA-333](../practices.d/SOTA-333.md), the note's consensus text says CausVid "adopts per-chunk
independent noise when training its causal student". That is right, and
it applies twice. Alg. 1 line 5 gives the student per-chunk timesteps, and
the causal teacher is fine-tuned "following Diffusion Forcing". Both roll
out on clean context. Alg. 2 caches keys and values from G(x_0, 0), and
§4.2 says the causal teacher conditions on "clean chunks". The Table 4
causal row, with Fig. 8's orange curve, is therefore per-token-noise
training with clean-history rollout at transformer scale, by a group other
than Diffusion Forcing's. It degrades over time. That fits [SOTA-333](../practices.d/SOTA-333.md)'s claim
that the rollout half matters, but it does not test it: there is no
noised-history arm and no teacher-forcing arm, and Fig. 8 has no values.
It does not meet `promote_when`.

[SOTA-333](../practices.d/SOTA-333.md)'s consensus note could add that CausVid itself rolls out on clean
context, so its "adoption" is of the training half only.

## Limitations

- **One seed, no variance,** VBench on 128 prompts for the main and
  ablation tables.
- **Teacher quality and teacher causality are confounded** in the central
  ablation (C2).
- **Cross-model comparisons** (Tables 1, 2, 6) run different models at
  different lengths. The paper notes this for Table 1.
- **Degradation beyond about 30 s** is conceded in §6. Long-video evidence
  is one 14-minute example.
- **No diversity measurement** despite conceding the loss. Reverse KL is
  named as the cause.
- **Model size and teacher training** are not described, and the video
  data is an internal set of about 400K clips.

## Open questions

- Does a causal teacher trained to the bidirectional teacher's quality
  still give a worse student?
- How much of the error-accumulation effect would noised-history rollout
  remove from the causal baseline?
- How much diversity does the reverse-KL objective cost? §6 names EM
  distillation and score implicit matching as alternatives.

## Corrections to the LIT note

- **Summary: "The controlled result is that a bidirectional teacher makes a
  better causal student than a causal one, which avoids inheriting the
  teacher's error accumulation."** The first half is the controlled result.
  The second half is the authors' explanation, and the ablation cannot
  separate it from the causal teacher simply being weaker (92.4 / 60.1 /
  28.5 against 94.6 / 62.7 / 29.6 at 10 s, Table 4). Fix: "…than a causal
  one. The authors attribute this to error accumulation, but the causal
  teacher is also the weaker model, and the ablation does not separate the
  two."
- **"The user study is 29 prompts × 3 raters."** The text says 3 ratings
  per prompt per model pair "from different evaluators", or 87 ratings per
  pair (§5.1). Fix: "29 prompts, 3 ratings each per model pair (87 per
  pair)".
