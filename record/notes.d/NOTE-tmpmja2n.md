---
status: Read
paper: LIT-627
title: 'Video Diffusion Models'
version: 1
date: '2026-09-24'
summary: >-
  A standard Gaussian diffusion model with a space-time factorized 3D U-Net
  generates video. Appending 0, 4 or 8 independent frames to each training
  video takes text-to-video FVD from 202.28 to 68.11 to 57.84 at fixed batch
  size and steps, but the added frames are extra per-step compute and the
  paper's own gloss is "more independent examples in a batch". Reconstruction
  guidance beats the replacement method for autoregressive extension, 136
  against 451 FVD.
---

# NOTE-tmpmja2n: Video Diffusion Models

Read in full from arXiv 2204.03458v2 (22 Jun 2022): main text, the
Appendix A hyperparameter tables and the figure captions. The paper has no
other appendix. Samples are on a project page, which was not viewed. It is
not needed for any claim below.

## Contribution

This is the first diffusion model for video. It makes two claims. Video
needs "essentially the standard formulation" of Gaussian diffusion plus an
architecture change, a 3D U-Net factorized over space and time. And that
architecture can be masked to run on single images, which allows **joint
image-video training** (§3). The paper also adds **reconstruction
guidance**, a way to sample a conditional p(x_b | x_a) from a model trained
unconditionally. It is used for autoregressive extension, temporal
interpolation and spatial super-resolution (§3.1).

## Key insight

**Factorization is what makes joint training cheap.** Every 3×3 convolution
becomes 1×3×3, spatial attention treats frames as batch, and a temporal
attention block with relative position embeddings follows each spatial one
(§3, Fig. 1). The paper names the advantage it cares about: the model can be
switched to independent images "simply by removing the attention operation
inside each time attention block". The factorization is justified as "known
to be a good choice in video transformers for its computational efficiency",
with citations. It is not ablated.

**Replacement conditioning is missing a term.** Replacing the conditioning
latents with forward-process samples updates z_b along E[x_b | z_t], not
E[x_b | z_t, x_a]. The missing part is (σ_t²/α_t)∇ log q(x_a | z_t). The paper
approximates q(x_a | z_t) as a Gaussian around the model's own
reconstruction of x_a, which gives a guidance gradient with weight w_r
(Eq. 7).

## Assumptions

- **The data is a fixed block of frames.** Every model generates 16 frames
  (9 for the 128×128 model). Longer or larger outputs come only from
  conditional sampling at test time (§3.1).
- **Images are frames of other videos from the same dataset.** In the joint
  training experiment the "images" are "random independent image frames"
  from "random videos within the same dataset". A separate image corpus is
  left to future work (§4.3.1).
- **The Gaussian approximation in reconstruction guidance** is exact only as
  t → 0 with a perfect model. For larger t the text says "empirically we
  find it to be good" (§3.1).
- ε-prediction with a cosine schedule for most models, v-prediction for BAIR
  and Kinetics. Log-SNR range [−20, 20] throughout (§2, App. A).

## Key results

- **Joint training, text-to-video, small model, 16×64×64** (Table 4; FVD
  against train/validation):

  | image frames per video | FVD | FID-avg | IS-avg |
  |---|---|---|---|
  | 0 | 202.28 / 205.42 | 37.52 / 37.40 | 7.91 / 7.58 |
  | 4 | 68.11 / 70.74 | 18.62 / 18.42 | 9.02 / 8.53 |
  | 8 | 57.84 / 60.72 | 15.57 / 15.44 | 9.32 / 8.82 |

  The same small model is used in all three arms: 128 base channels, batch
  128, 200k steps on 64 TPU-v4 (App. A.4). No seeds or error bars.
- **Classifier-free guidance** (Table 5, large model, 8 image frames). At
  frameskip 1, FVD is 41.65, 50.19 and 163.74 at guidance weight 1, 2 and 5.
  At frameskip 4 it is 56.71, 54.28 and 185.89. IS-avg rises monotonically in
  both. There is no w = 0 row.
- **Reconstruction guidance against replacement**, extending 16 frames to 64
  (Table 6). FVD is 136.22 against 451.45 at w = 2 and 133.92 against 456.24
  at w = 5. FID-first is identical across methods (16.34 and 16.33 at w = 2),
  as it should be, since the first block is sampled the same way.
- **UCF-101 unconditional, 16×64×64:** FID 295 ± 3, IS 57 ± 0.62, against a
  real-data IS of 60.2 (Table 1). It trains "on all 13,320 videos".
- **BAIR, 1→15 frames:** FVD 66.92 with the Langevin sampler at 256 steps
  (Table 2). **Kinetics-600, 5→11:** FVD 16.2 ± 0.34 and IS 15.64. It rises
  to 16.9 under the with-replacement protocol other papers used (§4.2,
  Table 3).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Appending independent frames to video batches improves text-to-video sample quality | moderate | Table 4: monotone across 0/4/8 on every metric, one model, one run each, no error bars |
| C2 | The gain in C1 comes from the frames being *images* rather than from more examples or compute per step | weak | not isolated. Frames per step rise from 16 to 24 at fixed batch and steps, and §4.3.1 itself calls it "a memory optimization to fit more independent examples in a batch" |
| C3 | Joint training works by reducing minibatch gradient variance and "speed[s] up optimization" (abstract) | weak | asserted. No gradient statistic or training curve appears anywhere |
| C4 | Reconstruction guidance gives more coherent extensions than replacement | strong | Table 6: 3.3× lower FVD at two guidance weights, first-frame metrics identical as a control, Fig. 4 |
| C5 | Classifier-free guidance improves video sample quality | weak | Table 5 has no unguided row. FVD worsens with weight at frameskip 1. Only IS-type metrics improve monotonically |
| C6 | Factorized space-time attention is a good architecture for video diffusion | weak | adopted by citation to video transformers. Not ablated |
| C7 | The model is state of the art on UCF-101, BAIR and Kinetics-600 | moderate | Tables 1–3 against literature numbers. Protocol differences are named for Kinetics and UCF |

## Method

Take an image diffusion U-Net and make each convolution space-only 3D. Keep
spatial attention per frame and insert a temporal attention block after each
spatial one. Condition on text through BERT-large embeddings with attention
pooling (§4.3). For joint training, concatenate K independent frames to each
16-frame video and mask temporal attention so that they only attend to
themselves. To sample conditionally, run the unconditional model on
[x_a, x_b] and add −(w_r α_t/2)∇‖x_a − x̂_a‖² to the x_b prediction (Eq. 7).
Alternate ancestral steps with a Langevin corrector (Eq. 5, δ = 0.1). For
super-resolution, apply the same penalty to a differentiable downsample of
the prediction (Eq. 8).

## Concepts

- **Joint image-video training.** In this paper it means frames from other
  clips of the *same* video dataset, appended to a video with temporal
  attention masked. It does not mean an image corpus. The meaning changed in
  later work.
- **Replacement method.** Conditioning by overwriting the known part of the
  latent with forward-process samples at each step. It fixes the marginals
  and leaves out the conditional score term.
- **Reconstruction guidance.** A guidance gradient built from the model's
  own reconstruction of the conditioning data.
- **Frameskip.** The temporal stride of the training data. Frameskip-4
  models make low-frame-rate keyframes for the cascade (Fig. 2).

## Connections

It extends the Gaussian diffusion and classifier-free guidance line (it
cites DDPM, VDM-Kingma and Ho & Salimans) directly to video. Reconstruction
guidance corrects the imputation approach of Song et al.'s SDE paper. Its
factorized U-Net and joint training are what Make-A-Video ([LIT-632](../literature.d/LIT-632.md)) and
Video LDM ([LIT-621](../literature.d/LIT-621.md)) build on and compare against. Make-A-Video's related
work criticises VDM for sampling images "from random videos" rather than
using text-image data. That criticism is aimed at exactly the thing this
paper left to future work.

## Recommendations

- **R1. Mix independent frames into video diffusion batches.** Mask
  temporal attention so they act as images. *Topic:* training-optimization.
  *Status:* standard. *Strength:* moderate. *Conditions:* shown at 16×64×64
  with a small U-Net. The arms are not compute-matched per step, so this is
  evidence that adding frames helps and not that images beat an equal amount
  of extra video.
- **R2. Use reconstruction guidance when conditioning an unconditionally
  trained diffusion model on part of a sample.** Do not overwrite the known
  part. *Topic:* generative-modeling. *Status:* standard. *Strength:* strong
  within the paper. *Conditions:* w_r > 1. It pairs best with a
  predictor-corrector sampler, and a model trained conditionally avoids the
  problem entirely.
- **R3. Tune classifier-free guidance weight against a video metric, not
  only per-frame ones.** *Topic:* analysis-and-evaluation. *Status:*
  standard. *Strength:* moderate. *Conditions:* Table 5 shows IS and FVD
  choosing different weights.

## Bearing on the record

| practice | disposition |
|---|---|
| [SOTA-386](../practices.d/SOTA-386.md) images before and alongside video | **confirmed with a narrower reading** — C1 |
| [SOTA-390](../practices.d/SOTA-390.md) full 3D attention in video DiTs | background only. This is one of the factorized models it replaces, and nothing here tests the choice |
| [SOTA-333](../practices.d/SOTA-333.md) per-token noise, noised history | adjacent, does not move it |
| [SOTA-307](../practices.d/SOTA-307.md) FID as an error bar over seeds | Table 4 is the kind of single-run table it warns about. The gaps are large enough (202 → 58) to survive it |
| [SOTA-266](../practices.d/SOTA-266.md), [SOTA-187](../practices.d/SOTA-187.md), [SOTA-389](../practices.d/SOTA-389.md) | no bearing. Pixel-space, ε/v-prediction, and captions are not studied |

**[SOTA-386](../practices.d/SOTA-386.md).** Its first bullet says "Same model, same videos, with
independent frames appended to each video and temporal attention masked for
them. FVD falls from 202 with none to 58 with eight". That is accurate. Two
things should be added to its Conditions.
(1) **The arms differ in work per step.** At batch 128 and 200k steps, the
8-frame arm denoises 24 frames per example against 16. The paper describes
the change itself as fitting "more independent examples in a batch". The
table therefore cannot separate *images help* from *more, less correlated
frames per step help*. (2) The practice's Conditions already say that VDM's
images are frames of its own videos. That is correct, and Video LDM's
Table 1 has the same property (see that note). So neither of the two
numbered controlled sources tests a separate image corpus.

**[SOTA-333](../practices.d/SOTA-333.md).** The replacement method conditions an unconditionally trained
model on *noised* history, and it fails badly (Table 6). That is not
evidence against [SOTA-333](../practices.d/SOTA-333.md), whose model is *trained* with per-token noise. It
does show that noising the context at inference is not enough on its own.

**Should produce:** R2 has no practice. Reconstruction guidance (or
training conditionally) against replacement is a controlled, 3×-scale
result, and the record holds nothing on conditioning a diffusion model on
part of its own output.

## Limitations

- **One run per arm, one scale.** Table 4 is the small model at 64×64. The
  large model is only ever run with images (8 frames, or 7 at 128×128).
- **Not compute-matched** (C2). Neither is any claim that joint training is
  "important for sample quality" (§3).
- **The text-to-video data is a private 10M captioned-video set** with no
  external baseline. Results cannot be reproduced, and the models were not
  released (§6).
- UCF-101 training uses all 13,320 videos, the test split included. This is
  common for unconditional UCF but worth knowing next to a SOTA claim.
- The explanation in the abstract (C3) is the paper's most quoted sentence
  and its least supported.

## Open questions

- Does the joint-training gain survive when the no-image arm gets the same
  frames per step as extra video, or the same wall clock?
- Does a separate, larger image corpus help more than same-dataset frames?
  The paper names this as future work.
- Where does the 4 → 8 frame curve flatten? The gain from 4 to 8 (68 → 58)
  is much smaller than from 0 to 4.

## Corrections to the LIT note

- **[LIT-627](../literature.d/LIT-627.md) says:** "This is a controlled comparison with one seed at one
  scale." **Fix:** "It is controlled for model, data, batch size and steps
  (App. A.4), but not for frames processed per step: the 4- and 8-frame arms
  denoise 20 and 24 frames per example against 16. The paper reports no seed
  count and no variance." The paper never says "one seed". It gives single
  numbers with no error bars.
- **[LIT-627](../literature.d/LIT-627.md) says:** "At frameskip 1, FVD gets worse with guidance: 41.65 at
  w=1…". The numbers are right. **Add:** Table 5 has no unguided (w = 0) row.
  Under Eq. 6, w = 1 is already guided, so the table shows FVD worsening as
  the weight rises. It does not compare guidance against none.
