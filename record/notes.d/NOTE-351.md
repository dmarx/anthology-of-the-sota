---
number: 351
status: Read
formerly:
- NOTE-tmptd1wq
paper: LIT-635
title: 'Emu Video'
version: 1
date: '2026-09-24'
summary: >-
  Generating a first frame and conditioning the video on it beats direct
  text-to-video at matched data, steps and trainable parameters (70.5% /
  63.3% human win rate). Five one-change ablations with majority-of-5 votes
  on 307 prompts are the most controlled design evidence in the early video
  line. The freeze-versus-fine-tune result (55.0 / 58.1) is near chance, and
  by construction it cannot see the first frame.
---

<!-- inactive-ok-file: SOTA-251 SOTA-333 SOTA-386 SOTA-389 SOTA-390 — Proposed, and cited here to weigh the evidence for them; this document is part of that evidence, not an endorsement -->

# NOTE-351: Emu Video

Read in full from arXiv v2 (2 Aug 2024), appendices 1–5 included. v1 (Nov
2023) was compared on the ablation table, the freezing paragraph, the
image-animation table and the human-evaluation analysis. They match except
where noted under *Versions*. The appendix line plots (App. Figs. 1–2)
were not viewed, because PDF pages could not be rendered here. Their values
are not in the text beyond the one the caption states.

## Contribution

Text-to-video is factorized into text-to-image, then image-plus-text to
video, with one latent diffusion U-Net doing both. The spatial layers (2.7B)
come from the Emu text-to-image model and stay frozen. Only 1.7B temporal
parameters train, and the image step runs the same network with its temporal
layers off. The report isolates five design decisions, each against the
same model without it, and introduces JUICE, a rating template that makes
raters give reasons. It reports that JUICE raises inter-rater agreement.

## Key insight

**A stronger condition makes an easier task.** The model "only needs to
predict how the image will evolve". Because the first frame comes from the
frozen image model at inference, the image model's style range reaches the
video without joint image-video training. The factorized-vs-direct
comparison is the evidence: "the pretrained T2I model, training data, number
of training iterations, and trainable parameters are held constant" (§4.1).

## Assumptions

- A strong frozen text-to-image model exists; everything here builds on it.
- Video only: 34M licensed clips, "not filtered for text-frame similarity or
  aesthetics" (§4). No images are trained on beyond the frozen initialization.
- Frame-wise 8-channel image VAE, 8× spatial downsampling (App. Table 2).
- Human pairwise preference is the measure. Automatic metrics "do not
  reflect improvements in quality" (§3.2).

## Key results

**How preference was measured.** Pairwise A/B on quality and on
faithfulness. Each comparison is decided by the majority vote of 5 raters,
using JUICE (§3.2, App. 3). Raters pick reasons, are shown training examples
that favour each side, and see positions randomized. On Emu Video against
Make-A-Video, JUICE moves Fleiss' κ from 0.004 with a naive template to 0.31.
Split votes fall 28% and unanimous votes rise 24% (App. Fig. 4). No
confidence intervals are reported anywhere.

**The ablations** (Table 1). All use the 8-frame setting and the 307-prompt
Make-A-Video set. Each is a win rate for adopting the decision against the
same model without it:

| decision | quality | faithfulness | held fixed, per §4.1 |
|---|---|---|---|
| factorized vs direct T2V | 70.5 | 63.3 | T2I init, data, iterations, trainable parameters |
| zero terminal SNR at 512px | 96.8 | 88.3 | against "the standard noise schedule" |
| 256px then 512px vs 512px only | 81.8 | 84.1 | "the same training budget" |
| HQ fine-tune on 1.6K clips | 65.1 | 79.6 | the model before fine-tuning |
| frozen vs fine-tuned spatial | 55.0 | 58.1 | same conditioning images; unfrozen only in the 512px stage |

Three details decide how to read them:
- **Zero SNR is confounded as reported.** The 512px stage switches from
  ε-prediction to v-prediction and turns on zero-terminal-SNR rescaling (App.
  Table 3). The text names only the schedule as the difference.
- **The freezing test cannot see the first frame.** "For a fair comparison,
  the same conditioning images I are used across both models" (§4.1). The
  fine-tuned model's own image generation is never used. So the test excludes
  the place where fine-tuning spatial layers is most likely to cost quality,
  the text-to-image step. The unfreezing covers only the 15K-iteration 512px
  stage.
- **Multi-stage.** The 256px stage takes 4× the budget of the 512px stage,
  which is 3.5× slower per iteration (§4.1). About 70K iterations, one epoch,
  is best. Both fewer and more lose to it after the same 512px fine-tune (App.
  Fig. 1, values not stated).

**Data scaling** (App. Fig. 2). With the same steps and 10% of the data, the
model wins "∼43%" against the full-data model on both axes.

**The HQ set** (§3.3). 1.6K of 34M clips pass all three tests: CLIP(f₁) >
0.25, aesthetic(f₁) > 5.7, and a minimum windowed H.264 motion score > 0.5.
Generated motion score depends on guidance. At text scale 8 and image scale
2 it is 0.61 before HQ fine-tuning and 12.7 after. At image scale 1 it is
2.87 and 14.9 (App. Table 4).

**Against other systems** (Fig. 2, postprocessed to matched dimensions).
Quality win rates: Imagen Video 81.8, Make-A-Video 96.8, Align Your Latents
92.3, PYOCO 90.5. Faithfulness against Imagen Video is 56.4. Baselines are
their authors' released, probably best, samples on their own prompt sets
(App. Table 7: 55 to 307 prompts). Without postprocessing the averages rise
from 91.8 / 86.6 to 93.8 / 93.1, which the authors attribute to rater bias
(App. Table 10). Image animation is compared on 65 prompts (Table 3). The
win rates are 96.9 / 96.9 against VideoComposer, 72.3 / 73.9 against SVD and
69.2 / 66.1 against I2VGen-XL. The abstract's "preferred 96% over prior work"
is the VideoComposer row.

**UCF-101 zero-shot** (Table 2): FVD 317.1 and IS 42.7, against PYOCO's
355.2 and 47.8.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Factorized generation beats direct T2V at matched init, data, steps and trainable parameters | moderate | Table 1a; 307 prompts, majority of 5, κ 0.31, no CI |
| C2 | Zero terminal SNR is critical for 512px video | moderate | Table 1b is large, but v-prediction changes in the same stage |
| C3 | Low-resolution-first training beats high-resolution-only at equal budget | moderate | Table 1c |
| C4 | Fine-tuning on 1.6K high-motion, high-aesthetic clips improves both axes, mostly faithfulness | moderate | Table 1d; the set is selected on three criteria together |
| C5 | Freezing spatial layers is better than fine-tuning them | weak | Table 1e: 55.0 / 58.1 with no CI, and conditioning images held fixed |
| C6 | About 70K iterations at 256px is optimal | weak | App. Fig. 1; values unstated |
| C7 | 10% of the data costs little at fixed steps | weak | App. Fig. 2; one stated value, "∼43%" |
| C8 | JUICE improves inter-rater agreement | moderate | κ 0.004 → 0.31 on one comparison |
| C9 | Emu Video beats prior text-to-video systems | weak | released baseline samples, different prompt sets, no CI |
| C10 | Zero SNR helps factorized generation more than direct generation | weak | stated with no numbers (§4.1) |
| C11 | Identity-initialized temporal layers converge 2× faster | weak | "preliminary experiments" (§3.3) |

## Method

Input: noised video latents, the first-frame latent zero-padded in time, and
a binary mask, concatenated on channels (Fig. 3). A 1D temporal convolution
follows every spatial convolution and 1D temporal attention every spatial
attention, identity-initialized. The model has frozen T5-XL and CLIP text
encoders. The schedule is quadratic β with 1000 steps and DDIM with 250
steps at inference. Guidance is ordered: image first, then text (App. Eq.
1). A separate interpolation model, initialized from F, turns 8 frames at
4fps into 37 at 16fps. It is used on two halves of a 16-frame video to give
65 frames.

## Concepts

- **Factorized generation** — the video model is conditioned on the text and
  an explicit image rather than on text alone. At inference the image comes
  from the same network with temporal layers off.
- **JUICE** — "justify your choice": raters must pick reasons (pixel
  sharpness, motion smoothness, object consistency and others).
- **Win rate** — the share of prompts on which the majority of 5 raters
  prefer the named model.

## Connections

Builds on Emu (image) and Make-A-Video's temporal-layer design ([LIT-632](../literature.d/LIT-632.md)).
It borrows zero terminal SNR from Lin et al. ([LIT-tmp6c6lg](../literature.d/LIT-tmp6c6lg.md)) and v-prediction from
[LIT-067](../literature.d/LIT-067.md). It names SVD ([LIT-625](../literature.d/LIT-625.md)) as concurrent with "similar factorization".
Movie Gen ([LIT-626](../literature.d/LIT-626.md)) extends it.

## Recommendations

- **R1** — At high resolution, rescale the noise schedule to zero terminal
  SNR, together with a parameterization that can train there. *Topic:*
  generative-modeling. *Status:* standard. *Strength:* moderate.
  *Conditions:* 512px video latents; tested together with the switch to
  v-prediction.
- **R2** — Spend most of the video training budget at low resolution, then
  move to the target resolution. *Topic:* training-optimization. *Status:*
  experimental. *Strength:* moderate. *Conditions:* one matched-budget
  comparison; the optimum sits near one epoch at 256px.
- **R3** — Finish with a very small high-motion, high-aesthetic fine-tune,
  and measure motion at the guidance settings you ship. *Topic:*
  adaptation-and-tuning. *Status:* experimental. *Strength:* moderate.
- **R4** — Report inter-rater agreement for any human preference result, and
  make raters justify their choices. *Topic:* analysis-and-evaluation.
  *Status:* experimental. *Strength:* moderate.

## Bearing on the record

- **[SOTA-386](../practices.d/SOTA-386.md): the adjacent condition is stated correctly, but it needs one
  more sentence.** Emu Video shows no images during video training, and its
  55.0 / 58.1 is recorded in the practice as a narrow win for freezing. The
  practice should add that the fine-tuned model's spatial layers were
  unfrozen only for the 15K-iteration 512px stage, and that both arms were
  fed the same conditioning images. The comparison is silent on whether
  unfreezing damages the text-to-image step, which is the reason to freeze.
  C1 is adjacent support for the practice's premise that keeping the image
  model's knowledge matters. It is not a test of "before" or "alongside".
- **[SOTA-263](../practices.d/SOTA-263.md): supporting mechanism, different fix.** Emu Video's reason for
  zero terminal SNR is the one [SOTA-263](../practices.d/SOTA-263.md) gives for shifting. "The residual
  signal is higher for high resolution video frames, due to redundant pixels
  across both space and time" (§3.2). Table 1b is the only controlled video
  number in the record for acting on it. The practice could cite it as a
  second remedy for the same failure.
- **[SOTA-195](../practices.d/SOTA-195.md):** the switch to v-prediction at 512px goes with zero SNR,
  because at zero SNR an ε-prediction implies no estimate of the clean
  signal. That is consistent with [SOTA-195](../practices.d/SOTA-195.md), but not a separate test of it.
- **[SOTA-251](../practices.d/SOTA-251.md):** Table 1c is video-diffusion evidence for training at low
  resolution first. It does not test [SOTA-251](../practices.d/SOTA-251.md)'s decay-phase timing.
- **[SOTA-187](../practices.d/SOTA-187.md), [SOTA-266](../practices.d/SOTA-266.md), [SOTA-333](../practices.d/SOTA-333.md), [SOTA-389](../practices.d/SOTA-389.md), [SOTA-390](../practices.d/SOTA-390.md):** no bearing. It is a
  latent U-Net with factorized temporal layers, ε/v diffusion, no
  recaptioning and one-shot generation.
- **Should produce:** a Proposed practice for zero terminal SNR at high
  resolution (R1), unless [SOTA-263](../practices.d/SOTA-263.md) is widened to hold it. Also possibly a
  data-pipeline practice for a tiny HQ fine-tune set, which would need
  Movie Gen's evidence to reach `Active`.

## Limitations

- One seed per arm and no CI. κ = 0.31 is only fair agreement on the usual
  Landis–Koch reading.
- The paper releases no weights or code, so none of this can be re-run.
- Comparisons to prior work use each baseline's released samples. The
  authors note these "are likely to be the 'best'".
- The HQ fine-tune set combines three filters, so motion filtering is not
  isolated.
- 8-frame ablations, 16-frame final model, 512px square.

## Open questions

- Does unfreezing hurt the first frame? Rerun Table 1e with each arm
  generating its own conditioning image.
- How much of Table 1b is the schedule and how much is v-prediction?
- How does freezing compare with joint image-video training? The paper
  contrasts them in words (§3.2), and nobody has run the comparison.

## Versions

v1 compared image animation against three methods: VideoComposer, Pika and
Gen2. The rows for SVD, VideoCrafter and I2VGen-XL, including the 72.3 / 73.9
against SVD, were added in v2. v1 does not mention SVD. The Table 1
ablation values, the freezing paragraph and the κ values are unchanged.

## Corrections to the LIT note

- **"The multi-stage schedule, the high-quality fine-tune and motion
  filtering are all tested here first."** Motion filtering is not tested on
  its own. The 1.6K set is selected on motion, aesthetics and CLIP similarity
  together, and Table 1d tests the resulting fine-tune as a whole. Fix: "the
  multi-stage schedule and a high-quality fine-tune on a motion-,
  aesthetic- and CLIP-filtered set are tested here."
- **"a very small curated fine-tune set (SVD and Movie Gen)."** SVD's
  stage-III sets are 250K clips ([LIT-625](../literature.d/LIT-625.md) §3.4) and about 1M (its §4.2, App.
  D.3), roughly 150× to 600× Emu Video's 1.6K. They are small relative to
  SVD's 152M pretraining set, not in Emu Video's sense. Fix accordingly.
- **"The motion score rises from 0.61 to 12.7 after fine-tuning."** These are
  generated-video scores at text guidance 8 and image guidance 2. At image
  guidance 1 they are 2.87 → 14.9 (App. Table 4). Fix: state the guidance
  setting.
