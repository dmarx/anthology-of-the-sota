---
number: 341
status: Read
formerly:
- NOTE-tmpeb8mt
paper: LIT-621
title: 'Video LDM (Align your Latents)'
version: 1
date: '2026-09-24'
summary: >-
  Video LDM makes a latent image diffusion model into a video model by
  inserting temporal layers and fine-tuning the decoder and upsampler on
  video. On driving scenes, an image-pretrained LDM with frozen spatial
  layers reaches FVD 534.17 against 1155.10 for the same design trained from
  scratch. The "images" are 1 fps frames of the same driving videos, and the
  pretrained arm gets 73K image steps the other does not. Decoder video
  fine-tuning cuts reconstruction FVD 390.88 → 32.94.
---

<!-- inactive-ok-file: SOTA-333 SOTA-386 SOTA-389 SOTA-390 — Proposed, and cited here to weigh the evidence for them; this document is part of that evidence, not an endorsement -->

# NOTE-341: Video LDM (Align your Latents)

Read in full from arXiv 2304.08818v2 (28 Dec 2023): main text and
Appendices A–I, including hyperparameter Tables 6–8 and the extra results in
Tables 9–14. The linked videos and project page were not viewed. No claim
below depends on them.

## Contribution

A recipe for video generation from a pretrained **latent** image diffusion
model. It interleaves temporal layers (3D-conv residual blocks and temporal
attention) with the frozen spatial layers and merges them through a learned
α. It then fine-tunes the autoencoder's **decoder** on video with a 3D-conv
discriminator and **temporally aligns the diffusion upsampler** too (§3).
The recipe is applied twice. A driving-scene model at 512×1024 is trained
from its own image LDM. A text-to-video model is built on Stable Diffusion
and trained on WebVid-10M. The paper also shows that temporal layers
trained on one checkpoint transfer to a DreamBooth-fine-tuned one (§4.2.1).

## Key insight

**Each stage that sees frames independently must be taught time: the
generator, the decoder, the upsampler.** The paper measures each one.
Temporal layers in the LDM (Table 1), video fine-tuning of the decoder
(Tables 3, 11) and a video-aware upsampler (Table 3) each cut FVD sharply
while leaving per-frame FID roughly unchanged. The pattern is one argument:
per-frame quality and temporal consistency are separable, and FID cannot see
the second.

## Assumptions

- **A good image model exists for the domain.** For driving it is trained on
  1 fps RDS frames at 128×256 (App. H.1). For text-to-video it is SD 1.4, 2.0
  or 2.1, **first fine-tuned on WebVid frames** because otherwise video
  training hits "out-of-distribution problems" (App. H.2).
- **The encoder can stay image-only.** Only the decoder gets temporal
  layers, so that the image LDM's latent space is unchanged (§3.1.1).
- **FVD is unreliable**, and the paper says so. It adds human studies for
  driving and mountain biking (App. G, I.2).
- **α is scalar** in the text-to-video model, which permits
  "convolutional-in-time" sampling. In the other models α varies along time
  (App. D).

## Key results

- **Ablation on driving scenes, smaller model, 128×256** (Table 1 right;
  configurations in Table 7):

  | arm | what differs | FVD | FID |
  |---|---|---|---|
  | Ours | image LDM pretrained (73K steps), spatial frozen, temporal 60K steps | 534.17 | 48.26 |
  | End-to-end LDM | no image pretraining; spatial and temporal trained together, 62K steps | 1155.10 | 71.26 |
  | Attention-only | temporal attention only, twice the attention layers, same trainable parameters | 704.41 | 50.01 |
  | Pixel baseline | pretrained pixel DM, 128 channels, video batch 1×2 GPUs | 639.56 | 59.70 |
  | Ours, context-guided | classifier-free guidance on context frames | 508.82 | 54.16 |

  One run each. Evaluation uses 2,048 generated videos (App. G).
- **Video fine-tuning barely hurts per-frame quality:** FID 47.00 with the
  temporal layers switched off (α = 1) against 48.26 with them on
  (App. I.3.2).
- **Decoder fine-tuning**, reconstruction FVD / FID from image-only to
  video-fine-tuned: driving 390.88 → 32.94 and 7.61 → 9.17 (Table 3). WebVid
  35.82 → 18.66 and 13.89 → 11.68 (Table 11). Mountain biking 73.78 → 25.55
  and 20.76 → 18.65 (Table 11). Adding an image discriminator raises driving
  FVD to 51.01 with FID 9.04 (Table 14).
- **Upsampler:** video 45.39 against frame-wise 165.98 FVD, with FID 19.85
  against 19.71 (Table 3).
- **Driving against LVG at 128×256:** FVD 389 against 478 and FID 31.6
  against 53.5. Conditioning lowers FVD to 356 but raises FID to 51.9
  (Table 1 left). Humans prefer it to LVG 54.02 / 40.23 unconditional and
  62.03 / 31.65 conditional, with 400 responses (Table 2, App. G).
- **Mountain biking against LVG:** FVD 118 is *worse* than LVG's 85.3, FID
  7.73 against 21.1 is better, and humans prefer it 54.2 to 42.2 (Table 13).
- **Text-to-video (SD 2.1):** UCF-101 zero-shot IS 33.45 and FVD 550.61,
  against Make-A-Video's 33.00 and 367.23 (Table 4). MSR-VTT CLIPSIM 0.2929
  against 0.3049 (Table 5). SD 1.4 scores IS 29.49, FVD 656.49 (from 2,048
  samples) and CLIPSIM 0.2848 (Tables 9–10).
- **Parameters (SD 2.x):** 3.1B in autoencoder plus diffusion. The paper
  counts 2.2B as "actually trained": 656M temporal plus 1,509M interpolation
  LDM (App. H.2.1).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Initializing from an image LDM gives a much better video LDM than training the same architecture end to end | moderate | Table 1: 534 against 1155 FVD. One run. The arms also differ in total compute (73K image steps) and in which layers train |
| C2 | The benefit in C1 comes from image *data* | weak | not tested. The image LDM is trained on 1 fps frames of the same RDS videos (App. H.1) |
| C3 | Video fine-tuning the decoder is necessary for temporal consistency | strong | three datasets, same direction, large margins (Tables 3, 11), plus a discriminator ablation (Table 14) |
| C4 | A temporally aligned upsampler is needed; frame-wise upsampling loses consistency | strong | Table 3, with FID as a within-table control |
| C5 | 3D-conv temporal layers beat attention-only at equal trainable parameters | moderate | Table 1, one run, batch sizes differ slightly (18 against 13 per GPU) |
| C6 | Latent beats pixel space for this recipe | weak | the pixel baseline differs in channels (128), steps and video batch (2 against 36) (Table 7) |
| C7 | Only a temporal alignment model needs training when building on an off-the-shelf LDM (abstract) | weak | contradicted by App. H.2: spatial layers fine-tuned on WebVid first, interpolation models train all parameters, decoder fine-tuned |
| C8 | Temporal layers transfer to DreamBooth checkpoints | weak | qualitative only (Fig. 8, 10). No metric |

## Method

Stage 1: an image LDM, either trained (driving) or taken from SD and
fine-tuned on WebVid frames. Stage 2: insert L temporal layers after spatial
blocks, reshaping (b t) c h w ↔ b c t h w around each. Merge with
α·z + (1−α)·z′ and train only φ on video under the image model's noise
schedule (Eq. 2). Prediction models take 0, 1 or 2 masked context frames
through a learned downsampler, with context guidance at sampling (Eqs. 3–4).
One interpolation model does T → 4T and 4T → 16T (1.875 → 7.5 → 30 fps).
Decoder: add temporal layers and train with a patch-wise 3D-conv
discriminator. Upsampler: a 4× DM trained on patches with noise augmentation
and applied convolutionally. DDIM throughout.

## Concepts

- **Temporal alignment.** The paper's term for teaching the frames of a
  batch to be one video (Fig. 2). The spatial model is left to render each
  frame.
- **α-merge.** A learned blend between spatial and temporal outputs. Setting
  α = 1 recovers the image model exactly.
- **Context guidance.** Classifier-free guidance on the conditioning frames
  of a prediction model. It trades FID for FVD (Table 1).
- **Convolutional in time / space.** Running the model on more frames or
  pixels than it was trained on. The paper calls the temporal version
  "fragile" (App. D).

## Connections

It builds on the LDM of Rombach et al. ([LIT-062](../literature.d/LIT-062.md)) and on the cascaded
upsamplers of Ho et al. Its masking for prediction and interpolation
borrows from VDM ([LIT-627](../literature.d/LIT-627.md)), MCVD and Harvey et al. It differs from VDM in
working in latent space, freezing a pretrained image model instead of
training jointly, and fine-tuning the decoder. It is concurrent with
Make-A-Video ([LIT-632](../literature.d/LIT-632.md)), which it trails on UCF FVD and CLIPSIM and
attributes the gap to HD-VILA data. Stable Video Diffusion ([LIT-625](../literature.d/LIT-625.md)) is the
same group's continuation.

## Recommendations

- **R1. When a latent video model is built on an image autoencoder,
  fine-tune the decoder on video with a video discriminator.** Keep the
  encoder fixed. *Topic:* representation-and-encoding. *Status:* standard.
  *Strength:* strong. *Conditions:* reconstruction FID can move either way
  (worse on driving, better on WebVid). Do not add an image discriminator.
- **R2. Make every per-frame stage of a cascade video-aware**, the
  upsampler included, and judge it on FVD, because FID will not see the
  failure. *Topic:* generative-modeling. *Status:* standard. *Strength:*
  strong.
- **R3. Start a video diffusion model from a pretrained image model rather
  than from scratch.** *Topic:* training-optimization. *Status:* standard.
  *Strength:* moderate. *Conditions:* shown on one domain with one run. The
  pretraining compute is extra, and the images were frames of the target
  videos.

## Bearing on the record

| practice | disposition |
|---|---|
| [SOTA-386](../practices.d/SOTA-386.md) images before and alongside video | **confirmed for "before"**, with conditions to add — C1, C2 |
| [SOTA-187](../practices.d/SOTA-187.md) train in a learned latent | weakly consistent (C6). Not a controlled pixel-vs-latent test |
| [SOTA-390](../practices.d/SOTA-390.md) full 3D attention | background. Factorized throughout, and not tested |
| [SOTA-307](../practices.d/SOTA-307.md) FID over seeds | every ablation here is a single run |
| [SOTA-266](../practices.d/SOTA-266.md), [SOTA-333](../practices.d/SOTA-333.md), [SOTA-389](../practices.d/SOTA-389.md) | no bearing. WebVid's own captions are used as is |

**[SOTA-386](../practices.d/SOTA-386.md).** Its second bullet says "Same architecture on driving scenes,
with and without a pretrained image LDM underneath. FVD is 534 against 1155
and FID 48 against 71". The numbers are right. Three things belong in its
Conditions, and none of them is in the practice or in [LIT-621](../literature.d/LIT-621.md) now:
(1) **the images are frames of the same RDS videos**, sampled at 1 fps
(App. H.1). Video LDM is therefore like VDM on the point the practice
already attributes to VDM alone. *Neither* numbered controlled source uses
a separate image corpus. (2) **The arms are not compute-matched.** The
pretrained arm gets 73K image-LDM steps at batch 640 frames on top of its
60K video steps. The end-to-end arm gets 62K video steps. (3) **They differ
in what is frozen.** "Ours" trains only the temporal layers. End-to-end
trains everything, so the comparison bundles initialization with freezing.
That matters for the practice's own third Condition about freezing as a
third route. The comparison does not say whether image-initialized *full*
fine-tuning does as well.

The practice does not cover the "alongside" clause: this paper shows no
images during video training.

**Should produce:** R1 and R2 have no practice. The decoder result is the
strongest evidence in the paper, since it is measured on three datasets.

## Limitations

- **The key ablation is one run at one small scale** on an in-house dataset.
  The driving data is mostly "relatively empty highway scenes" (App. E.1).
- **The headline text-to-video model is not the light recipe.** Spatial
  fine-tuning, full-parameter interpolation models and a fine-tuned decoder
  mean nearly every component except the encoder was trained on WebVid.
- **The samples come from different models than the metrics:** SD 1.4
  mostly, SD 2.0 at 1280×2048, SD 2.1 in Tables 4–5 (App. H.2).
- **"Up to 1280×2048"** is SD's 4× upscaler, trained on 320×320 crops and
  run at extended resolution (App. H.2).
- UCF-101 evaluation uses bare class names where Make-A-Video uses templates
  (App. G), so the two rows are not like for like.

## Open questions

- Does C1 hold with a separate image corpus, and with compute matched?
- Image-initialized frozen, image-initialized fully fine-tuned, and from
  scratch: which part of the 534 → 1155 gap is initialization and which is
  freezing?
- Why does conditioning on day/night and crowdedness raise FID from 31.6 to
  51.9 (Table 1 left)? The paper reports it and does not discuss it.

## Corrections to the LIT note

- **[LIT-621](../literature.d/LIT-621.md) says:** "Fine-tuning the decoder on video with a video
  discriminator cuts reconstruction FVD from 390.88 to 32.94 on driving
  scenes (Table 3), and on WebVid from 35.82 to 18.66 (Table 11).
  Reconstruction FID gets slightly worse." **Fix:** "Reconstruction FID gets
  slightly worse on driving (7.61 → 9.17) and slightly *better* on WebVid
  (13.89 → 11.68) and mountain biking (20.76 → 18.65)."
- **[LIT-621](../literature.d/LIT-621.md) says:** "In total about 2.2B of 3.1B parameters were trained."
  **Fix:** "The paper counts 2.2B of 3.1B as trained (App. H.2.1): the 656M
  temporal layers and the 1,509M interpolation model. That count leaves out
  the 865M spatial layers, which App. H.2 says were fine-tuned on WebVid
  frames first, and the fine-tuned decoder. Only the encoder and text
  encoder were never updated."
- **[LIT-621](../literature.d/LIT-621.md)'s key takeaway** on image pretraining is numerically correct but
  should add that the images are 1 fps frames of the same driving videos, and
  that the end-to-end arm gets no equivalent of the 73K image-pretraining
  steps (App. H.1, Table 7).
