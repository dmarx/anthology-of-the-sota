---
number: 336
status: Read
formerly:
- NOTE-tmp651x9
paper: LIT-625
title: 'Stable Video Diffusion'
version: 1
date: '2026-09-24'
summary: >-
  At fixed architecture and a fixed step count, a video model pretrained on a
  curated quarter of a 9.8M-clip pool is preferred by human raters to one
  trained on the whole pool, and the lead survives high-quality fine-tuning
  (Elo +127 against +89 over an image-only start at 10k steps). Almost every
  result is a preference bar from 64 prompts with no numbers in the text, and
  two of the curation choices the paper shipped lost its own ablation.
---

<!-- inactive-ok-file: SOTA-333 SOTA-386 SOTA-389 SOTA-390 — Proposed, and cited here to weigh the evidence for them; this document is part of that evidence, not an endorsement -->

# NOTE-336: Stable Video Diffusion

Read in full from arXiv v1 (25 Nov 2023), appendices A–E included. The
figures themselves were not viewed: this environment cannot render PDF
pages, and the extracted text carries only the Figure 4e Elo labels and the
Figure 9a table. Every number below is from the text, a table or those labels.

## Contribution

A data study inside a model report. The architecture is held at Video LDM's
(temporal convolution and attention after every spatial layer of SD 2.1),
and the paper asks what the training data does. It names three stages:
image pretraining, video pretraining on a large curated set at low
resolution, and high-quality fine-tuning. It builds a curation pipeline
(cascaded cut detection, three synthetic captioners, optical flow, OCR, CLIP
aesthetics and similarity) and tests each filter by training small models
and ranking them on human preference. The released models (SVD, SVD-XT) are
the output of that pipeline, not its evidence.

## Key insight

**Curation was measured at fixed compute, not at fixed data.** Every
threshold model trains for exactly 40k steps at batch 256, "roughly
corresponding to 10M training examples seen" (App. E.2.2). A filtered subset
is therefore seen for more epochs than the unfiltered pool. LVD-10M-F has
2.3M clips against LVD-10M's 9.8M (Table 1), about four passes against one.
"Curation beats quantity" here means that at a fixed budget, repeating
cleaner clips beats seeing more raw ones once.

## Assumptions

- **Human preference is the measure.** "There are no equally powerful
  off-the-shelf representations available in the video domain" (§3.3), so
  every curation decision is ranked by raters, not by a metric.
- **Axes are independent.** Each annotation is thresholded "while not
  filtering for any other types" (App. E.2.2). The combination is tested only
  once, as LVD-10M-F against LVD-10M.
- **Small-model results transfer.** The ablation recipe differs from the
  released model: SD 2.1's discrete linear schedule with offset noise and
  v-parameterization, not the EDM preconditioning used at scale (App. E.2.1).
- 2023 latent U-Net video models: 1521M parameters, 656M of them temporal
  (App. D.2).

## Key results

**How preference was measured** (App. E.1). For each ablation axis, samples
from every model on 64 fixed prompts. Every pair of models is compared on
every prompt, with on average three votes per prompt per task from different
annotators. The two tasks are visual quality and prompt following. Order is
randomized and attention checks are used. Multi-model axes become Elo scores
(K = 1, R_init = 1000, bootstrapped over 1000 shuffled orders, Eqs. 15–17),
and "aggregated" is the average of the two tasks. Two-model comparisons are
shown as preference fractions. No confidence intervals are reported.

**What the threshold study held fixed** (App. E.2.1–E.2.2). SD 2.1 U-Net
with Video LDM temporal layers, all layers trained. AdamW at 1e-4, batch 256,
8 frames at 256×256, exactly 40k steps. 10% text dropout. Sampling with 50
DDIM steps at guidance scale 12. Starting pool LVD-10M, a random 9.8M
subset of LVD. The bottom 12.5%, 25% and 50% were removed on one axis at a
time: CLIP score, aesthetics, OCR text area, optical flow. Captioners were
compared instead of thresholded.

**What the threshold study found** (Fig. 17, text only):
- CLIP score: remove 50%, the best model
- aesthetics: remove 25%, chosen on the quality task
- text area: remove 25%, best on quality and on average
- motion: remove 25%, **chosen although the unfiltered model ranked
  higher on the aggregate.** The authors attribute the loss to prompt
  following, which they judge "less important" for this axis
- captions: CoCa, an image captioner run on the mid-frame, "clearly" beat
  the video captioner V-BLIP and the LLM merge of the two. The shipped
  mixture samples CoCa 0.5, V-BLIP 0.25, LLM 0.25, a weighting that was not
  itself tested

**Image initialization** (§3.2, Fig. 3a). Two identical models on "a 10M
subset of LVD", one with SD 2.1 spatial weights and one random. The
recipe is App. E.2.1's; resolution, frame count and steps for this pair are
not stated. The image-initialized model is preferred on prompt alignment,
quality and aggregate. The bar heights are not in the text.

**Curation, combined filters** (Figs. 3b, 4a–d). LVD-10M-F is preferred to
LVD-10M, WebVid-10M and InternVid-10M on both tasks. The text cites
"Figure 4b" for both of the last two. At 50M, curated beats uncurated
(Fig. 4c). LVD-50M-F beats LVD-10M-F "for the same number of steps" (Fig.
4d), which is the one place dataset size is shown to help.

**Persistence through fine-tuning** (§3.4, Fig. 4e, App. E.2.3). Three
models, identical except initialization: SD 2.1 with no video pretraining,
uncurated-50M video weights, curated-50M video weights. All are fine-tuned
on 250K high-fidelity clips at 512×512, 8 frames, for 50k steps. The Elo
labels are relative to the last-ranked model, the image-only start:

| checkpoint | image-only | uncurated-50M | curated-50M |
|---|---|---|---|
| 10k steps | 0 | +89 | +127 |
| 50k steps | 0 | +70 | +103 |

**Multi-view** (§4.5, Fig. 9a). This is the only prior ablation with
numbers: 50 GSO objects, 12k steps each.

| init | LPIPS ↓ | PSNR ↑ | CLIP-S ↑ |
|---|---|---|---|
| SVD (video prior) | 0.14 | 16.83 | 0.89 |
| SD 2.1 (image prior) | 0.18 | 15.06 | 0.83 |
| random | 0.22 | 14.20 | 0.76 |

**Other.** Zero-shot UCF-101 FVD 242.02 against baselines' own published
numbers (Table 2, App. E.4). Processing raises clips per video from 2.65 to
11.09 (Fig. 2). LVD has 577M clips and LVD-F 152M (Table 1).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Image-initialized spatial layers beat random ones at equal video training | weak | Fig. 3a bars with no numbers; recipe partly unstated; initialization also carries SD 2.1's pretraining compute |
| C2 | A curated quarter of the pool beats the whole pool at a fixed step budget | weak | Fig. 3b bars; 64 prompts, ~3 votes per prompt per task |
| C3 | The curation advantage holds at 50M clips | weak | Fig. 4c bars |
| C4 | The pretraining-data advantage persists through 50k steps of HQ fine-tuning | moderate | Fig. 4e Elo labels; the curated–uncurated gap goes from 38 to 33 |
| C5 | Video pretraining before HQ fine-tuning beats fine-tuning an image model directly | moderate | Fig. 4e: the image-only start ranks last at both checkpoints |
| C6 | Filtering the most static 25% of clips improves the model | weak | contradicted on the aggregate by the paper's own ablation (App. E.2.2) |
| C7 | Image-captioner captions train a better video model than video-captioner captions | weak | Fig. 17 with no numbers; 8 frames at 256²; V-BLIP captions are short |
| C8 | A video prior beats an image prior for multi-view fine-tuning | moderate | Fig. 9a numbers; one run, 50 objects |
| C9 | Shifting the noise distribution toward more noise is "essential" at high resolution | weak | asserted (§2, §4.1), citing Hoogeboom et al.; no ablation |
| C10 | Linearly increasing guidance across frames reduces artifacts | weak | "found it helpful" (App. D.4.1); no comparison |
| C11 | SVD image-to-video is preferred to Gen-2 and Pika | weak | Fig. 6 bars; visual quality only; 64 SDXL conditioning images (App. E.3) |

## Method

Cut detection is run as a cascade at three frame rates and thresholds, to
catch fades (App. C, Fig. 11, qualitative only). Clips are snapped to
keyframes. Farnebäck flow is computed at 2 fps for pretraining and RAFT for
the fine-tuning set. OCR (CRAFT) is run on three frames, and clips whose text
area exceeds 7% are dropped. CLIP aesthetics and similarity are taken on the
first, middle and last frames. At scale: SD 2.1 is fine-tuned to EDM
preconditioning for 31k steps. Video pretraining is 150k steps at 14×256×384
(batch 1536, P_mean = −1.2), then 100k steps at 320×576 with P_mean = 0.
Fine-tunes raise P_mean further, to 0.5–1.0 (App. D.2–D.4). Frame rate and
motion score are micro-conditions. Image-to-video replaces text with the
CLIP image embedding and concatenates a noise-augmented conditioning latent,
copied across time, with no mask.

## Concepts

- **LVD / LVD-F / LVD-10M-F** — the raw pool (577M clips), its filtered
  version (152M), and the random 9.8M subset and its filtered 2.3M version
  used for ablation.
- **Aggregated** — the mean of the quality and prompt-following Elo, the
  score on which the motion filter lost. Stage III's set is 250K clips in the
  ablation and ~1M for the released models.

## Connections

Extends Video LDM ([LIT-621](../literature.d/LIT-621.md)) by un-freezing the spatial layers and adding a
data study. It uses EDM preconditioning ([LIT-075](../literature.d/LIT-075.md)) for the released models
and imports the high-noise shift from simple diffusion. Emu Video ([LIT-635](../literature.d/LIT-635.md)),
concurrent, reaches image-first conditioning from the text-to-video side and
calls SVD's factorization "similar".

## Recommendations

- **R1** — When curating video pretraining data, pick each filter's threshold
  with small matched runs, and test the combined filter against the unfiltered
  pool at the same step budget. *Topic:* data-pipeline. *Status:*
  experimental. *Strength:* weak. *Conditions:* the effect is shown at fixed
  steps, so part of it may be repetition of clean data; human preference
  only.
- **R2** — Pretrain on large curated video before high-quality fine-tuning
  rather than going straight from an image model to the fine-tuning set.
  *Topic:* training-optimization. *Status:* experimental. *Strength:*
  moderate. *Conditions:* 8-frame, 512² ablation; one seed.
- **R3** — Do not treat motion filtering as settled. Report it on quality
  and prompt following separately. Here the 25% filter ranked below no
  filter on the aggregate, and the per-task values are not given.
  *Topic:* data-pipeline. *Status:* experimental. *Strength:* weak.

## Bearing on the record

- **[SOTA-386](../practices.d/SOTA-386.md): confirms the "before" half only, and weakly.** Fig. 3a is the
  source the practice cites, and the practice's condition that it "reports
  only a preference chart with no counts" is accurate. SVD does not train on
  images alongside video. §2 gives a study-design reason: joint image-video
  training "amplifies the difficulty of separating the effects of image and
  video data". So [LIT-625](../literature.d/LIT-625.md) is not evidence for the "alongside" clause. Fig. 9a
  gives adjacent numeric support: PSNR 15.06 against 14.20 for an image prior
  against none on multi-view. Fig. 4e adds that image initialization alone is
  not enough: the model that skipped video pretraining ranked last.
- **[SOTA-389](../practices.d/SOTA-389.md): a contrary datum the practice should state.** In SVD's
  caption ablation the image captioner beat the video captioner (App. E.2.2).
  It is small-scale, its values are unreadable, and V-BLIP's captions are
  short (Fig. 13). It is still the only other controlled caption-source
  comparison here, and it points the other way.
- **[SOTA-263](../practices.d/SOTA-263.md):** SVD adopts the direction (P_mean −1.2 → 0 → up to 1.0 as
  resolution rises) and calls it essential without testing it. That is
  adoption.
- **[SOTA-187](../practices.d/SOTA-187.md):** latent, with a frame-wise image autoencoder. No test.
- **[SOTA-266](../practices.d/SOTA-266.md), [SOTA-333](../practices.d/SOTA-333.md), [SOTA-390](../practices.d/SOTA-390.md):** no bearing. SVD is an EDM U-Net with
  factorized temporal layers.
- **Should produce:** a Proposed data-pipeline practice on curated video
  pretraining sourced to C2 and C4, with R1's conditions, and R2 as a
  condition of it or a sibling. Neither exists. [LIT-625](../literature.d/LIT-625.md) is cited only by
  [SOTA-386](../practices.d/SOTA-386.md).

## Limitations

- No figure in §3 carries a number in the text except Fig. 4e. Preference
  margins, and so effect sizes, cannot be stated.
- About three votes per prompt per task on 64 prompts, with no CI, and no
  second seed anywhere.
- The ablation recipe (linear schedule, offset noise, v-prediction, 256²,
  8 frames) is not the released one (EDM, 14–25 frames, 576×1024).
- The thresholds were not chosen by one rule. The stated rule is "best-
  performing"; aesthetics and motion were judged on quality alone, and the
  motion threshold was kept against its ranking.
- "Competitive with closed-source" (abstract) is said of the text-to-video
  model. The closed-source comparison is of the image-to-video model, on
  quality only (App. E.3).

## Open questions

- How much of C2 is repetition? A curated-vs-uncurated comparison at equal
  epochs would separate cleaning from reuse.
- Does the CoCa-over-V-BLIP result survive a strong video captioner?
- Why does fine-tuning shrink every lead (127 → 103, 89 → 70)? The lead
  may wash out with more stage-III steps.

## Corrections to the LIT note

- **"Cascaded cut detection finds about 4× more clips per video than a
  single pass (Fig. 2)."** Fig. 2 compares the raw data's clips, "obtained
  from metadata", with the processed output: 2.65 against 11.09 clips per
  video. The cascade against a single-pass detector is shown only
  qualitatively (Fig. 11). Fix: "Processing yields about 4× more clips per
  video than the raw metadata cuts, 2.65 → 11.09 (Fig. 2)."
- **"The curated-pretrained model gains more Elo than the uncurated one:
  +127 against +89 at 10k steps and +103 against +70 at 50k."** These are
  not gains over fine-tuning. They are each model's Elo above the
  image-only-initialized model at that checkpoint, and both leads shrink
  from 10k to 50k. Fix: "After the same stage III, the curated-pretrained
  model leads the image-initialized one by 127 Elo at 10k steps and 103 at
  50k, against 89 and 70 for the uncurated one (Fig. 4e)."
- **"Every curation claim rests on about three votes per pair."** It is
  about three votes per prompt, per task, per pair, over 64 prompts (App.
  E.1.1). That is roughly 190 votes per task per model pair, which is small,
  but not three. Fix accordingly.
