---
status: Read
paper: LIT-634
title: 'Open-Sora 2.0'
version: 1
date: '2026-09-24'
summary: >-
  An 11B video model initialized from FLUX, trained mostly at 256px, and
  adapted to 768px as text/image-to-video. The "$200k" is 4,160 H200
  GPU-days for one final run on HunyuanVideo's VAE. The 4×32×32 Video DC-AE
  is a separate, unconverged experiment whose cost is outside that figure.
  Every training-strategy choice that makes the run cheap is asserted, not
  ablated.
---

# NOTE-tmpkcmy8: Open-Sora 2.0

Read in full from arXiv v3 (2 March 2026), appendices A–I included, and
checked against v1 (12 March 2025). The two agree on every number. v3 moves
the batch-size tables (v1 Tables 5–6) into Appendix D. It turns v1's
cost table (Table 4, with dollar estimates) into a figure labelled "GPU
hours (in H100)". It drops v1's derivation of the 115K-token figure, adds
an inference-time scaling section (§5.4, App. G), and fixes v1's
self-contradictory Stage 3 learning-rate sentence. Figs. 1 and 10 were read
from extracted labels. Their bar-to-label assignment is inferred, as noted
below.

## Contribution

A cost-accounted recipe: one full training run for an 11B text/image-to-video
model, priced at $199.6K (Table 2), with the choices that keep it cheap.

- **FLUX initialization.**
- **Most compute at 256px.**
- **An image-to-video route to 768px.**
- **Heavy data filtering.**
- **DP/ZeRO-2/CP systems work.**

Separately, a 4×32×32 **Video DC-AE** and an account of why adapting the
generator to it is hard.

## Key insight

**Buy resolution with image conditioning.** Motion is learned cheaply at
256px, and the expensive 768px stage is run as T/I2V, so the model "focus[es]
more on motion generation" while the first frame supplies detail (§4.1.4).
At inference, FLUX draws the first frame (§7). The pipeline's quality claims
are therefore claims about text-to-image-to-video.

## Assumptions

- **H200 rental at $2 per GPU-hour, one run** (Table 2 caption). Nothing
  upstream is priced: FLUX, the autoencoders, data, captioning, failed runs
  and search.
- **Competitor costs can be estimated from public information** (Fig. 6,
  marked *).
- **Information downsampling ratio predicts reconstruction.** D_info =
  D_T·D_H·D_W·3/C_out (§4.3.1) is "hypothesize[d]" as a lower bound, citing
  DC-AE.

## Key results

- **Cost (Table 2).**

  | stage | data | CP | iterations | GPUs | GPU-days | USD |
  |---|---|---|---|---|---|---|
  | 256px T2V | 70M | 1 | 85K | 224 | 2240 | $107.5K |
  | 256px T/I2V | 10M | 1 | 13K | 192 | 384 | $18.4K |
  | 768px T/I2V | 5M | 4 | 13K | 192 | 1536 | $73.7K |
  | total | | | | | 4160 | $199.6K |

  Each row is GPU-days × 24 × $2, and the table checks exactly. 256px is 63%
  of the compute and 768px is 37%.
- **The $200k model uses HunyuanVideo's VAE.** Patch size 2 (Table 3), which
  §3.2 says "is still required when the HunyuanVideo autoencoder is used".
  Stage 3 runs at CP = 4 with buckets up to 76,032 tokens (Table 5), the
  HunyuanVideo-VAE token count (App. F.1). The DC-AE adaptation runs, 17K
  iterations on 160 GPUs plus 8K iterations (§4.3.3), are not in Table 2.
- **Cost comparison (Fig. 6; v1 Table 4).** Open-Sora: 224 GPUs and 100k
  GPU-hours. Step-Video: 2,992* GPUs and 500k* hours ($1M*). Movie Gen:
  6,144 GPUs and 1.25M* hours ($2.5M*). The ratios are 5× and 12.5×. The
  text says "5–10×".
- **Autoencoders (Table 1).**

  | model | down | D_info | ch | LPIPS | PSNR | SSIM |
  |---|---|---|---|---|---|---|
  | HunyuanVideo VAE | 4×8×8 | 48 | 16 | 0.046 | 30.240 | 0.856 |
  | StepVideo VAE | 8×16×16 | 96 | 64 | 0.082 | 28.719 | 0.818 |
  | Video DC-AE | 4×32×32 | 96 | 128 | 0.051 | 30.538 | 0.863 |
  | Video DC-AE | 4×32×32 | 48 | 256 | 0.049 | 30.777 | 0.872 |

  The table does not state the evaluation resolution or set. The AEs train
  on 32-frame, 256px clips (§4.4).
- **DC-AE speed (Fig. 4, 768px, 128 frames).**
  - Training: 2×8 samples in 28.6 s against 2×2 in 37.2 s, which is the
    stated 5.2× throughput.
  - Generation: 162 s against 1656 s, the ">10×".
  - Tokens: 19K against 76K (App. F.1).
- **Resolution cost (Tables 4–5).** 101–129 frames: 3.2 videos/s at 256px
  against 0.08 at 768px (CP = 4), which is the stated 40×. Image buckets at
  256, 768 and 1024px appear in stages 1–2, and at 768px in stage 3.
- **Objective (§4.2.1).** Straight path. t is logit-normal, then shifted
  t ← αt/(1+(α−1)t) with α ∝ T×H×W, in training and inference.
- **Systems (§6).** MFU 38.19% for stages 1–2 (DP + ZeRO-2) and 35.75% for
  stage 3 (ZeRO-2 + CP = 4). ">99%" utilization (App. H.2).
- **Evaluation.**
  - 100 prompts, 10 evaluators, one generation per model (§7).
  - Open-Sora wins at least two of three aspects against each of six
    models (Fig. 1).
  - The per-model triples, read in label order, are HunyuanVideo
    55.3/53.0/44.8 (visual quality, prompt following, motion) and Runway
    Gen-3 Alpha 64.2/77.7/60.9. That assignment is inferred from extracted
    text.
  - VBench gap to Sora: 4.52% down to 0.69% (§7). All of these use the
    FLUX-first T2I2V pipeline.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | One final run costs $199.6K at $2 per H200-hour | strong | Table 2 arithmetic; the scope is stated in the caption |
| C2 | Training is 5–10× cheaper than Movie Gen and Step-Video | weak | competitor figures are estimates; the stated numbers give 5× and 12.5×; H100/H200 units are mixed |
| C3 | FLUX initialization works "despite it being a distilled model" | weak | "empirically find", no comparison (§4.1.1) |
| C4 | Low-resolution training learns motion efficiently | weak | observation (§4.1.3) |
| C5 | Adapting to 768px is "significantly more efficient" as I2V than T2V | weak | "We find", no numbers (§4.1.4) |
| C6 | High-quality data "can substantially enhance training efficiency" | weak | "we hypothesize" (§4.1.2) |
| C7 | A 4×32×32 × 128 DC-AE reconstructs close to HunyuanVideo's VAE | moderate | Table 1, own evaluation, conditions unstated |
| C8 | Doubling spatial compression needs 4× channels; 4× temporal compression needs none | weak | "we find", no table (§4.3.1) |
| C9 | The DC-AE gives 5.2× training and >10× generation speed at 768px | moderate | timed (Fig. 4) |
| C10 | High-channel AEs slow diffusion convergence | weak | observation plus citations (§4.3.2) |
| C11 | The DC-AE-adapted model underperforms the original and did not converge | moderate | stated by the authors, shown qualitatively (§4.3.3, Fig. 13) |
| C12 | Decoupled image/text guidance, oscillated and scaled linearly, is best | weak | "we find", heat map only (§5.2, Fig. 8) |
| C13 | Open-Sora 2.0 is "comparable to" HunyuanVideo and Gen-3 Alpha | weak | 100 prompts; a T2I2V pipeline against T2V baselines (§7, Figs. 1 and 10) |
| C14 | Most compute should go to low resolution because 768px is 40× slower | moderate | the throughput is measured (Tables 4–5); the quality consequence is not |

## Method

Filter hierarchically (preprocessing, then aesthetic, VMAF motion, blur, OCR
and jitter scores). Caption 256px clips with LLaVA-Video and 768px clips with
Qwen 2.5 Max, and append the motion score to every caption (§§2.2, 5.3).

Initialize an MMDiT-style model (19 dual and 38 single blocks, width 3072)
from FLUX, with T5-XXL and CLIP-L as text encoders. Train 256px T2V, then
256px T/I2V, then 768px T/I2V. The image or video condition is
channel-concatenated with a mask channel (k → 2k+1), with 12.5%
image-condition dropout (§5.1). AdamW, ε = 10⁻¹⁵, no weight decay, clip at
1. The learning rate is 5×10⁻⁵ then 3×10⁻⁵, and 10⁻⁵ in stage 3 (§4.2).

## Concepts

- **D_info** — pixels × 3 per latent value. It is used to match AEs at equal
  information rate, not token rate.
- **D_token** — AE compression × patch size. It is 1024 for HunyuanVideo's
  VAE with patch 2 and 4096 for DC-AE with patch 1 (App. F.1). §4.3.1's
  "16x D_token" leaves out the patch. Including it, the ratio is 4×.
- **Guidance oscillation** — alternating g_img and 1 on even steps after
  step 10 of 50 (§5.2).

## Connections

It inherits HunyuanVideo's VAE and tiling code ([LIT-620](../literature.d/LIT-620.md)), FLUX's
architecture and weights, DC-AE's residual pixel-shuffle blocks, and
PixArt's AE-swap adaptation. It measures Step-Video's VAE ([LIT-624](../literature.d/LIT-624.md))
independently and finds it well behind HunyuanVideo's, contrary to
Step-Video's own Table 15. Its DC-AE convergence difficulty sits beside
LTX-Video's ([LIT-618](../literature.d/LIT-618.md)) claim that 1:8192 works, and neither tests the other.

## Recommendations

- **R1** — Report training cost per stage, with GPU type, rate and scope,
  and say what is excluded. *Topic:* analysis-and-evaluation. *Status:*
  standard. *Strength:* moderate. *Conditions:* a final-run figure is not a
  model's cost.
- **R2** — Compare autoencoders at equal information rate (D_info), not
  only equal spatial-temporal downsampling. *Topic:*
  representation-and-encoding. *Status:* standard. *Strength:* moderate.
  *Conditions:* Table 1's pairing is the example. The underlying "lower
  bound" is a hypothesis.
- **R3** — Guide image and text separately in I2V, with a small image scale.
  *Topic:* generative-modeling. *Status:* experimental. *Strength:* weak.

## Bearing on the record

- **[SOTA-386](../practices.d/SOTA-386.md)** — adoption, as recorded, with a new variant: initializing
  from a *distilled* image model. Images are in every stage (Tables 4–5).
  Untested.
- **[SOTA-263](../practices.d/SOTA-263.md)** — "higher-resolution and longer-duration videos are more
  susceptible to noise", so t is shifted with α ∝ T×H×W (§4.2.1). Together
  with LTX-Video this is two reports that say they shifted *for this
  reason*, which is the literal text of `promote_when`. It is still
  adoption, and extends the argument to duration without testing it. It is
  flagged for the curator.
- **[SOTA-266](../practices.d/SOTA-266.md)** — Open-Sora 2.0 states the logit-normal (§4.2.1). The
  `consensus_note` ("Wan is the only video report that states it") is
  wrong.
- **[SOTA-389](../practices.d/SOTA-389.md)** — adoption. LLaVA-Video is video-native. The Qwen 2.5 Max
  swap is justified by "fewer hallucinations", not measured.
- **[SOTA-390](../practices.d/SOTA-390.md)** — adoption (§3.2). No comparison.
- **[SOTA-187](../practices.d/SOTA-187.md) / [SOTA-305](../practices.d/SOTA-305.md)** — Table 1 is a good instance of [SOTA-305](../practices.d/SOTA-305.md)'s
  equal-rate comparison. The DC-AE story is a caution for [SOTA-187](../practices.d/SOTA-187.md): at high
  channel counts reconstruction improved and generation did not (§4.3.2).
- **[SOTA-333](../practices.d/SOTA-333.md)** — does not move. It explicitly moves away from replacing
  noisy inputs with the condition, because that gives "inconsistent
  timesteps" (§5.1). That is the opposite choice to LTX-Video's per-token
  timesteps, and it is untested.

## Limitations

- **Nothing on the training strategy is ablated**: FLUX, low resolution
  first, I2V adaptation, data quality.
- **The headline comparisons are T2I2V against T2V**, on 100 prompts.
- **The DC-AE loss sentence is uninterpretable.** "A loss of 0.5, compared
  to 0.1 for the untrained model" (v3; v1 has "initialization model")
  reports loss rising from 0.1 to 0.5 over training.
- **Table 1 does not say at what resolution or on what data** it was
  measured.

## Open questions

- What would the same run cost from a non-distilled or randomly initialized
  image model?
- Is I2V adaptation actually cheaper, and by how much?
- Does latent distillation to DINOv2 (§4.3.3) fix the high-channel
  convergence problem, or only help?

## Corrections to the LIT note

- **Wrong:** "The efficiency case rests on a 4×32×32 autoencoder, but the
  evaluated model runs on HunyuanVideo's VAE" (summary). The same framing
  recurs in "The efficiency claim and the evaluated model don't match".
  **Fix:** the $200k run *is* the HunyuanVideo-VAE model (patch 2, CP = 4,
  76K-token buckets; Tables 2, 3 and 5), so the $200k does not rest on the
  DC-AE. The DC-AE is a further efficiency experiment (§4.3). Its 5.2× and
  >10× speedups and its adaptation cost are outside Table 2, and the model
  it produced is unconverged and weaker.
- **Misattributed:** "The authors 'hypothesize' that adapting from 256px to
  768px is much more efficient as image-to-video." **Fix:** the efficiency
  is stated as a finding ("We find that adapting … is significantly more
  efficient", §4.1.4), with no numbers. The hypothesis is the explanation
  (that conditioning lets the model "focus more on motion generation").
- **Imprecise:** "a short 768px stage run as image-to-video". **Fix:** the
  stage is T/I2V with 12.5% image-condition dropout (§5.1). It is short in
  iterations (13K) but not in compute: 1,536 GPU-days, 37% of the total.
- **Version note:** "Appendix D gives image buckets … The main text never
  says so" holds for v3. In v1 the same tables are main-text Tables 5–6
  (§4.2).
