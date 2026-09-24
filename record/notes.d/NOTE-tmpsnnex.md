---
status: Read
paper: LIT-632
title: 'Make-A-Video'
version: 1
date: '2026-09-24'
summary: >-
  Make-A-Video extends an unCLIP text-to-image model to video with
  identity-initialized pseudo-3D conv and attention layers trained on video
  with no captions. Text reaches the video decoder only through one CLIP
  image embedding, so text-only-in-video associations cannot be learned, and
  the discussion concedes this. System-level results are strong (zero-shot
  UCF-101 FVD 367.23, MSR-VTT CLIPSIM 0.3049), and there is no ablation of
  any design choice, image initialization included.
---

# NOTE-tmpsnnex: Make-A-Video

Read in full from arXiv 2209.14792v1 (29 Sep 2022): all 13 pages. This
version has no appendix. Model sizes, training steps, compute and the fps
sampling schedule are not reported anywhere in it. That absence is itself a
finding (see Limitations), not a gap in the reading. Samples on the project
page were not viewed.

## Contribution

A text-to-video system that needs **no paired text-video data for
training**. The pieces are an unCLIP-style text-to-image model (§3.1), with
a prior P from text to CLIP image embedding, a 64px decoder D and super-res
SR_l to 256px and SR_h to 768px. It gets **pseudo-3D layers**: a 1D temporal
conv after each 2D conv and a 1D temporal attention after each spatial
attention, both initialized to the identity (§3.2, Fig. 3). A **masked
frame interpolation network** ↑F takes 16 frames to 76 (§3.3). An **fps
conditioning** input is sampled from high to low fps during training
(§3.4). The paper also contributes a 300-prompt human-evaluation set
(§4.1).

## Key insight

**Split what text can teach from what only video can teach.** "Learn what
the world looks like and how it is described from paired text-image data,
and learn how the world moves from unsupervised video footage" (abstract).
The architecture enforces the split. **The prior is the only component that
receives text** (§3.4), and the video decoder D^t is conditioned on a single
CLIP image embedding. So whatever the video stage learns about motion, it
cannot learn which *words* go with which motion. The discussion says so
directly: "our approach can not learn associations between text and
phenomenon that can only be inferred in videos", for example "a person
waving their hand left-to-right or right-to-left" (§5).

## Assumptions

- **Actions are largely inferable from stills.** The intro argues that "one
  can often infer actions and events from static images", citing
  image-based action recognition (§1).
- **Unlabeled video is enough for motion.** "Even without text
  descriptions, unsupervised videos are sufficient to learn how different
  entities in the world move" (§1). This is asserted.
- **Identity initialization preserves the image model at step 0.** At
  initialization the network "will generate K different images… each
  faithful to the input text but lacking temporal coherence" (§3.2.1).
- **Data:** 2.3B English image-text pairs, filtered for NSFW, toxicity and
  watermark probability > 0.5. D^t and ↑F train on WebVid-10M video only.
  SR_l^t trains on WebVid-10M plus HD-VILA-10M (three clips from each of
  3.1M videos) (§4.1).

## Key results

- **MSR-VTT zero-shot**, at 16×256×256 with one sample per prompt and all
  59,794 test captions: FID 13.17 and CLIPSIM 0.3049. CogVideo (English),
  run by the authors, scores 23.59 and 0.2631 (Table 1).
- **UCF-101 zero-shot:** IS 33.00, FVD 367.23 at 256×256, against CogVideo
  (English) 25.27 and 701.59. Class names are turned into one hand-written
  template sentence per class. **Fine-tuned:** IS 82.55, FVD 81.25, against
  TATS-base 79.28 and 278 (Table 2).
- **Human preference for Make-A-Video** (Table 3; quality / faithfulness):
  against VDM on VDM's 28 website prompts, 84.38 / 78.13, averaged over
  8 samples per prompt. Against CogVideo on DrawBench (200), 74.48–76.88 /
  68.75–73.37. On their own 300 prompts, 73.44–77.15 / 71.19–75.74. Each
  judgement is the majority of 5 annotators. Human evaluation runs at
  76×256×256, not at the 768px output.
- **Interpolation against FILM** (1 → 4 fps): raters choose Make-A-Video for
  more realistic motion 62% of the time on their set and 54% on DrawBench
  (§4.2). The number of comparisons is not given.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Starting from a T2I model "significantly accelerates the T2V training process" | weak | asserted (abstract, §1). No training curve and no from-scratch run |
| C2 | Text-video pairs are unnecessary for competitive zero-shot T2V | moderate | Tables 1–3 at system level, against CogVideo (which uses pairs). Confounded by model, data and resolution |
| C3 | The design cannot learn text associations that exist only in video | strong | conceded by the authors (§5), and it follows from the architecture: text enters only through P (§3.4) |
| C4 | Pseudo-3D conv plus temporal attention gives "better temporal information fusion compared to VDM" | weak | asserted (§2). No ablation, and the VDM comparison is a system comparison on 28 showcase prompts |
| C5 | A spatiotemporal SR_l^t "significantly outperform[s] per-frame super resolution" | weak | "in qualitative inspection" (§3.2). No numbers |
| C6 | The high-to-low fps curriculum helps | weak | described (§3.4). Never evaluated |
| C7 | The interpolation network gives more realistic motion than FILM | moderate | human preference 62% on their set. At 54% on DrawBench it is close to chance, and the count is unstated |
| C8 | Make-A-Video is state of the art in T2V "in all aspects" (abstract) | moderate | system-level wins on every table, with baselines of different scale, data and resolution, and some run by the authors |

## Method

Train the T2I stack on image-text pairs. Add a Conv1D after every Conv2D
(Eq. 2) and an Attn1D after every spatial attention on flattened spatial
dims (Eq. 3), each initialized to the identity (temporal projection zero).
Fine-tune on 16-frame clips sampled at random fps from 1 to 30, drawn from
a beta distribution that moves from high to low fps. Condition on fps.
Fine-tune D^t into ↑F with 4 extra input channels (masked RGB plus mask),
at frame skip 5. SR_l^t is spatiotemporal. SR_h stays per-frame with shared
noise across frames. Inference is ŷ = SR_h ∘ SR_l^t ∘ ↑F ∘ D^t ∘ P (Eq. 1).
The 768px output is downsampled to 512 "for a cleaner aesthetic"
(footnote 1).

## Concepts

- **Pseudo-3D layer.** A separable space-then-time conv or attention. The
  paper's name for factorization, with the temporal half started at
  identity so the image model is untouched at step 0.
- **"Without text-video data."** The *training signal* for video has no
  text. The video datasets used do come with text (WebVid captions),
  and that text is discarded.
- **Frame-rate conditioning.** fps as an input. It works as augmentation
  (more clips per video) and as control at inference.

## Connections

It extends unCLIP / DALL-E 2 ([LIT-070](../literature.d/LIT-070.md)), and its temporal attention follows
VDM ([LIT-627](../literature.d/LIT-627.md)). It contrasts itself with CogVideo, which freezes the image
model, where Make-A-Video fine-tunes it. The text is inconsistent on this:
§2 and §3.2.2 say spatial and temporal layers are trained jointly, while
§3.4 describes only adding and fine-tuning "the new temporal layers". It
criticises VDM for drawing images from its own videos rather than from
text-image data. Video LDM ([LIT-621](../literature.d/LIT-621.md)) is concurrent, trails it on UCF FVD
and CLIPSIM, and attributes the gap to HD-VILA data.

## Recommendations

- **R1. Do not route all of a video model's text conditioning through an
  image-level embedding** if the model must follow instructions about
  motion or direction. *Topic:* multimodal-learning. *Status:* standard.
  *Strength:* moderate. It rests on the authors' concession and the
  architecture, not on a measurement. Movie Gen's caption comparison
  ([SOTA-389](../practices.d/SOTA-389.md)) is the measured form.
- **R2. Initialize new temporal layers as the identity** so that training
  starts from the image model's behaviour. *Topic:* adaptation-and-tuning.
  *Status:* standard. *Strength:* weak. It is used, not ablated.
- **R3. Make the super-resolution stage temporally aware** at least at the
  first upsampling step. *Topic:* generative-modeling. *Status:* standard.
  *Strength:* weak here (qualitative only). Video LDM's Table 3 supplies the
  measurement.

## Bearing on the record

| practice | disposition |
|---|---|
| [SOTA-386](../practices.d/SOTA-386.md) images before and alongside video | adoption only. It starts from an image model and shows no images alongside video |
| [SOTA-389](../practices.d/SOTA-389.md) caption video with a video-native captioner | **confirms the mechanism statement**, quote checked |
| [SOTA-390](../practices.d/SOTA-390.md) full 3D attention | background. Factorized, not tested |
| [SOTA-187](../practices.d/SOTA-187.md) train in a learned latent | runs in pixel space. No bearing |
| [SOTA-266](../practices.d/SOTA-266.md), [SOTA-333](../practices.d/SOTA-333.md) | no bearing |

**[SOTA-386](../practices.d/SOTA-386.md).** Its consensus note lists Make-A-Video among reports that
"start from an image model or train on images, and none of them tests it".
That is correct. The paper has no run without image initialization, and
C1 is an assertion. It also shows no images once video training begins
(§3.4), so it is not an instance of the "alongside" clause.

**[SOTA-389](../practices.d/SOTA-389.md).** Its "Why the mechanism is plausible" section quotes §5
exactly. The reading adds one point: the limit is **architectural**, not
only about data. Text reaches D^t only through the prior's single image
embedding, so captioned video would not have fixed it without changing the
conditioning path.

**[SOTA-390](../practices.d/SOTA-390.md).** Make-A-Video justifies factorizing attention by feasibility:
"adding the temporal dimension to attention layers is outright infeasible
in terms of memory consumption" (§3.2.2). That is a cost argument at 2022
pixel-space scale, consistent with the practice's "budget for the cost".

**Should produce:** nothing new. R3 belongs with Video LDM's measured
result if it is ever filed.

## Limitations

- **No ablation of anything.** Initialization, pseudo-3D layers, fps
  curriculum, spatiotemporal SR and interpolation are all adopted or shown
  qualitatively.
- **No model sizes, compute or training lengths** anywhere in v1. The
  system comparisons cannot be normalized, and Video LDM can only "suspect"
  that Make-A-Video is much larger.
- **Baselines are uneven.** CogVideo is run by the authors. VDM is
  represented by its own showcase prompts. UCF-101 uses hand-written class
  templates.
- **The stated resolution is overstated**: 768px generated, 512px shown,
  256px evaluated.
- The paper is internally inconsistent on whether spatial layers are
  fine-tuned on video (§3.2.2 against §3.4), and on whether the prior sees
  text (§3.4 lists it among components "trained on images alone (no aligned
  text)" in the sentence after saying it is the only one that sees text).

## Open questions

- How much of the result is the image initialization? No from-scratch or
  frozen-spatial arm exists.
- Would a text pathway into D^t trained on video captions recover
  motion-direction prompts, at what cost to the "no text-video data" claim?
- Does the fps curriculum matter?

## Corrections to the LIT note

- **[LIT-632](../literature.d/LIT-632.md) says:** "The temporal layers learn from WebVid-10M and HD-VILA
  clips with their text thrown away." **Fix:** "The decoder's temporal
  layers and the interpolation network train on WebVid-10M only. HD-VILA-10M
  is used only for the spatiotemporal super-resolution network SR_l^t
  (§4.1)."
- **[LIT-632](../literature.d/LIT-632.md) says:** "The model "can not learn associations between text
  and phenomenon that can only be inferred in videos", for example the
  direction of a wave." **Fix:** "for example 'a person waving their hand
  left-to-right or right-to-left' (§5)". The paper's §1 names "the motion of
  waves at the beach" as something unlabeled video *can* teach, so "the
  direction of a wave" can be read as the opposite example.
