---
status: Read
paper: LIT-637
title: 'Imagen Video'
version: 1
date: '2026-09-24'
summary: >-
  A seven-model pixel-space cascade whose one well-measured result is that
  guided progressive distillation to 8 steps per stage cuts sampling from
  618s to 35s. The CLIP metrics cannot tell the two apart: they fall slightly
  under constant guidance, rise under oscillating guidance, and rate every
  sample above the real videos. Joint image-video training, the choice later
  reports copied, is asserted without a number.
---

# NOTE-tmpr6vzj: Imagen Video

Read in full from arXiv v1 (5 Oct 2022), the only version supplied. The paper
has no appendix. Figures 11 and 13 are plots whose values are not given in
the text, and they were not viewed, because PDF pages could not be rendered
here. Where a result rests on them, this note gives its direction only.

## Contribution

Scales Video Diffusion Models ([LIT-627](../literature.d/LIT-627.md)) to 128 frames at 1280×768 and 24 fps
by cascading. The cascade has a base model (5.6B, 16×40×24 at 3 fps), three
temporal super-resolution models (1.7B, 780M, 630M) and three spatial ones
(1.4B, 1.2B, 340M): 11.6B diffusion parameters on a frozen T5-XXL (4.6B)
(§2.2, Fig. 6). The rest is transfer. v-prediction, noise conditioning
augmentation, classifier-free guidance, and progressive distillation with
guidance are all carried from the image work of the same group into video.
The paper tests two of them.

## Key insight

**The cascade makes every stage separately trainable and separately
distillable.** Each super-resolution model conditions on an upsampled,
noise-augmented copy of the previous stage's output. It can be trained in
parallel on resized real video and applied to other generators' output
(§2.2, §2.5). The distillation result depends on this: each of the seven
stages is distilled on its own to 8 steps.

## Assumptions

- Pixel space throughout. No autoencoder; the highest-resolution stage is
  fully convolutional, trained on crops (§2.3).
- Space-time separable Video U-Net (Fig. 7). The base model uses temporal
  attention and the super-resolution models temporal convolution.
- Continuous-time cosine schedule with v-parameterization for every model
  (§2.1, §2.4).
- Data: 14M internal video-text pairs, 60M internal image-text pairs and
  LAION-400M (§3). The paper never says any weight is initialized from
  Imagen. It extends Imagen's design "to the time domain" (§5).

## Key results

**Distillation** (Table 1). Samples are 128 frames at 320×192 and 24 fps.
The highest spatial stage is not in the evaluated pipeline. Values are the
mean ± standard error over four runs.

| base guidance | base steps | SR steps | CLIP score | CLIP R-precision | time |
|---|---|---|---|---|---|
| constant w = 6 | 256 | 128 | 25.19 ± .03 | 92.12 ± .53 | 618s |
| oscillate (15, 1) | 256 | 128 | 25.02 ± .08 | 89.91 ± .96 | 618s |
| constant w = 6 | 256 | 8 | 25.29 ± .05 | 90.88 ± .50 | 135s |
| oscillate (15, 1) | 256 | 8 | 25.15 ± .09 | 88.78 ± .69 | 135s |
| constant w = 6 | 8 | 8 | 25.03 ± .05 | 89.68 ± .38 | 35s |
| oscillate (15, 1) | 8 | 8 | 25.12 ± .07 | 90.97 ± .46 | 35s |
| ground truth | | | 24.27 | 86.18 | |

About 18× faster in wall time and about 36× in FLOPs, because the distilled
models no longer need two evaluations per step for guidance (§3.4). The
paper's own reading: "For all models, generated samples obtain better
perceptual quality metrics than the original ground truth data."

**v-prediction vs ε-prediction** (§3.3, Figs. 12–13). This is one
comparison, on the 80×48 → 320×192 spatial stage. Under ε-prediction there
are "unnatural global color shifts across frames" at 200k steps (Fig. 12,
qualitative). First-frame FID converges "much more slowly" (Fig. 13, curves
only). FVD is not reported because it is "excessively noisy for the
ε-prediction model".

**Scaling the base model** (§3.2, Fig. 11). At 500M, 1.6B and 5.6B, made by
raising base channel count and depth, FVD and CLIP score both improve over
training, each computed on 4096 samples. No values appear in the text. The
authors read this as "contrary to" Imagen's finding of limited benefit from
scaling the image U-Net.

**Asserted, not measured:**
- joint image-video training "significantly increases the overall quality of
  video samples" (§2.6)
- images teach styles the videos lack (Fig. 8, qualitative)
- temporal attention in the super-resolution models brought no "significant
  improvements" over convolution (§2.3)
- spatial attention in the early stages "improve[s] sample fidelity"
  (§2.3)
- oscillating guidance "significantly helps" with saturation, and is applied
  only up to the 80×48 stage because it added artifacts beyond (§2.6.2)
- frozen T5-XXL embeddings are "critical" for alignment (§2.2)

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Guided progressive distillation to 8 steps per stage keeps CLIP metrics within about 2.4 R-precision points at ~18× the speed | moderate | Table 1, four runs with SE; the metrics exceed ground truth, so they are weak judges of quality |
| C2 | Under oscillating guidance, full distillation does not lower the metrics | moderate | Table 1: 25.02 → 25.12, 89.91 → 90.97 |
| C3 | v-prediction converges faster than ε-prediction and avoids cross-frame colour shift in video super-resolution | weak | one stage, curves and a qualitative figure; same authors as the parameterization |
| C4 | The base video model improves with size up to 5.6B | weak | Fig. 11 curves, no values; one run per size |
| C5 | Joint training with a separate image corpus significantly improves video quality | weak | asserted, "consistent with" VDM |
| C6 | Temporal convolution suffices in super-resolution stages | weak | "initial experiments", no numbers |
| C7 | Oscillating guidance reduces saturation | weak | asserted; Table 1 shows lower metrics for it at full steps |
| C8 | Guided samples score above real videos on CLIP score and R-precision | strong | Table 1 |

## Method

Continuous-time Gaussian diffusion with Kingma et al.'s formulation, trained
with the ε-loss written through v-parameterization (Eq. 2, §2.4). The
sampler is ancestral with a stochasticity knob γ, or DDIM for distillation.
Super-resolution conditioning concatenates the bilinearly or
frame-repeat-upsampled input on channels, with Gaussian noise augmentation
at a random SNR. SNR is fixed at 3 or 5 at sampling. Joint training packs
independent images into a video-length sequence and masks temporal
convolutions and temporal attention for them. Distillation has two stages:
first into a single model that absorbs guidance, then progressive halving.
After that comes a stochastic N-step sampler that takes a 2× DDIM step and
then a noise step back.

## Concepts

- **TSR / SSR** — temporal and spatial super-resolution diffusion models,
  each conditioned on the text and on the previous stage's output.
- **Oscillating guidance** — a constant high guidance weight for early steps,
  then alternating high (e.g. 15) and low (e.g. 1) weights.
- **Conditioning augmentation** — noise the conditioning video at a random
  SNR in training, and tell the model the level.

## Connections

The video model is VDM ([LIT-627](../literature.d/LIT-627.md)) scaled, with Imagen's text conditioning and
cascade. Its parameterization and distillation come from Progressive
Distillation ([LIT-067](../literature.d/LIT-067.md)) and Meng et al., and Ho and Salimans are authors of
both this paper and [LIT-067](../literature.d/LIT-067.md). Emu Video ([LIT-635](../literature.d/LIT-635.md)) compares against its
released samples and calls its seven-stage cascade what factorization
avoids.

## Recommendations

- **R1** — To make a guided cascade fast, distill guidance into each stage
  and then halve its steps progressively. Distill the super-resolution
  stages first: that alone takes 618s to 135s. *Topic:*
  inference-optimization. *Status:* standard. *Strength:* moderate.
  *Conditions:* judged by CLIP metrics that rate samples above real data;
  evaluated at 320×192.
- **R2** — Do not use CLIP score or R-precision to certify that a faster
  sampler lost no quality when guidance is on. Here they exceed the ground
  truth. *Topic:* analysis-and-evaluation. *Status:* experimental.
  *Strength:* moderate.

## Bearing on the record

- **[SOTA-386](../practices.d/SOTA-386.md): confirms the practice's condition as written.** This is the
  report that adds a separate image corpus, 60M internal pairs plus
  LAION-400M, and its evidence for it is one sentence (§2.6). It is also
  not an instance of "before": no image-model initialization is stated.
  Imagen Video is joint training from scratch, by the text.
- **[SOTA-195](../practices.d/SOTA-195.md): supportive, not independent.** The v-prediction comparison is
  real but small: one stage, curves only, one run. Ho and Salimans wrote
  both this paper and [SOTA-195](../practices.d/SOTA-195.md)'s source, [LIT-067](../literature.d/LIT-067.md). It should be counted as
  the same group applying its own parameterization.
- **[SOTA-202](../practices.d/SOTA-202.md) (clamp the prediction at every sampling step):** a
  qualification. At large guidance weights static clipping to the data range
  "leads to significant saturation artifacts". Dynamic thresholding was "not
  sufficient" here (§2.6.2). Clamping is necessary and not the whole fix
  under strong guidance. This is asserted, not measured.
- **[SOTA-187](../practices.d/SOTA-187.md):** a counter-design, a pixel-space cascade. It runs no
  comparison against a latent model.
- **[SOTA-390](../practices.d/SOTA-390.md):** Imagen Video is space-time separable throughout. The claim
  that temporal convolution matches temporal attention in super-resolution
  stages is unmeasured and concerns conditioning-heavy stages. It is no
  evidence on joint 3D attention.
- **[SOTA-266](../practices.d/SOTA-266.md), [SOTA-333](../practices.d/SOTA-333.md), [SOTA-389](../practices.d/SOTA-389.md):** no bearing.
- **Should produce:** possibly a Proposed inference-optimization practice
  from R1, sourced jointly with [LIT-067](../literature.d/LIT-067.md) and Meng et al. if those are in the
  record.

## Limitations

- No external comparison of any kind.
- Every quantitative result except Table 1 is a plot without stated values.
- The distillation evaluation stops at 320×192, below the final 1280×768
  stage.
- Neither the model nor the code was released (§4).

## Open questions

- How much does the separate image corpus contribute, against frames drawn
  from the training videos, as in VDM? This is the question [SOTA-386](../practices.d/SOTA-386.md) needs,
  and it is answerable only by someone who runs it.
- Does the distilled cascade lose quality that a human, or a metric not
  saturated by guidance, would see?

## Corrections to the LIT note

- **"This is independent support for [SOTA-195](../practices.d/SOTA-195.md)."** It is not independent. Ho
  and Salimans are authors of both Imagen Video and Progressive Distillation
  ([LIT-067](../literature.d/LIT-067.md)), the practice's source. It is also a single super-resolution
  stage with first-frame FID curves and a qualitative figure. Fix: "The same
  group's video result agrees with [SOTA-195](../practices.d/SOTA-195.md): on one super-resolution stage,
  v-prediction converges faster and avoids cross-frame colour shift (Figs.
  12–13, curves only)."
- **Hedge: "'Without any noticeable loss in perceptual quality' (§2.7) sits
  next to R-precision falling 2.4 points in Table 1."** This is true only
  under constant guidance. Under oscillating guidance, full distillation
  raises both metrics (CLIP 25.02 → 25.12, R-precision 89.91 → 90.97), and
  every generated row scores above ground truth (24.27, 86.18). The hedge
  should say that the metrics cannot settle the claim either way. The
  summary's "at a small metric cost" should read "at a small metric cost
  under constant guidance and none under oscillating guidance".
- **"With only the base model's size changed (500M, 1.6B, 5.6B)."** The paper
  says the scaling was done "by increasing the base channel count and depth".
  It does not state what else was held fixed. Fix: "Scaling the base model's
  width and depth (500M, 1.6B, 5.6B) improves FVD and CLIP score (Fig. 11,
  curves only)."
