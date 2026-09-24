---
status: Read
paper: LIT-620
title: 'HunyuanVideo'
version: 1
date: '2026-09-24'
summary: >-
  A 13B open text-to-video model whose one quantitative design argument is a
  pair of compute-optimal fits on a proxy family: the image fit puts more of
  each added FLOP into parameters (0.5634 against 0.4325), and the video fit,
  initialized from the image envelope, reverses it (0.3618 against 0.6289).
  No architectural or data choice is ablated, and the proxy differs from the
  shipped model in objective, text encoder and conditioning.
---

<!-- inactive-ok-file: SOTA-263 SOTA-333 SOTA-386 SOTA-389 SOTA-390 — Proposed, and cited here to weigh the evidence for them; this document is part of that evidence, not an endorsement -->

# NOTE-tmpj4gkm: HunyuanVideo

Read in full from arXiv v6 (11 March 2025): §§1–8, the contributor list and
the references. There are no appendices. The application sections (§7:
video-to-audio, image-to-video, avatar animation) were read, but they carry
no numbers beyond data sizes. The scaling-law figure (Fig. 10) was read from
its axis labels and the coefficients in §4.4.1–4.4.2. The per-point envelope
values are not in the text.

## Contribution

An open, fully documented video generation system: data pipeline, a causal
3D VAE trained from scratch, a FLUX-style dual-then-single-stream transformer
with a multimodal LLM as text encoder, progressive image-then-video training,
and inference acceleration. The paper's one quantitative design argument is a
**compute-optimal scaling fit for a text-to-video diffusion model**, done
image first and then video. No other video report in the record gives one.

## Key insight

**Size the video model from an image fit and a video fit, with the video
proxies initialized from the image-optimal checkpoints** (§4.4). The paper's
stated reason is that "video generation models typically rely on pre-trained
image models", so the video fit asks where to put compute *after* image
pretraining, not from scratch. That framing decides how to read the video
exponents. They describe an image-initialized continuation, not a video model
trained cold.

## Assumptions

- **The proxy's allocation transfers to the shipped model.** DiT-T2X uses
  T5-XXL, cross-attention, DDPM with v-prediction, and 256px data (§4.4.1).
  HunyuanVideo uses an MLLM, dual/single-stream blocks and flow matching
  (§§4.2, 4.3, 4.5.1). The transfer is never tested.
- **Chinchilla's envelope method applies to diffusion MSE loss.** The fit
  follows Hoffmann et al. (§4.4.1), applied to training loss, not to a
  sample-quality metric.
- **The fit covers only the first training stage.** The paper says "the
  amount of training tokens calculated by image and video scaling laws is
  only related to the first stage of training for images and videos
  respectively". Progressive-resolution scaling is "left explored in future
  work" (§4.4.2).

## Key results

- **Image fit (§4.4.1, Fig. 10a–c).** N_opt = a1·C^b1 and D_opt = a2·C^b2,
  with N and D in billions and C in PetaFLOPs:
  a1 = 5.48×10⁻⁴, **b1 = 0.5634**, a2 = 0.324, **b2 = 0.4325**. Seven sizes,
  S2 to G2, spanning 92M to 6.6B (Fig. 10 caption).
- **Video fit (§4.4.2, Fig. 10d–f).** a1 = 0.0189, **b1 = 0.3618**,
  a2 = 0.0108, **b2 = 0.6289**. Five sizes, B2 to G2 (Fig. 10d legend). Each
  starts from "the optimal image checkpoint (i.e., the model on the
  envelope)" for its size.
- **The exponents point in opposite directions.** The image fit gives more of
  each added FLOP to parameters. The video fit gives more to data.
  Both pairs sum to about 1 (0.9959 and 0.9907).
- **The 13B operating point.** The image fit gives 5.8×10⁷ PF and 740B tokens
  (Fig. 10b–c). The video fit gives 7.0×10⁷ PF and 928B tokens (Fig. 10e–f).
  Both check against the coefficients: 0.0108·(7.0×10⁷)^0.6289 ≈ 928. The
  size was chosen from these fits "taking into account the training
  consumption and inference cost" (§4.4.2), so 13B is a judgment, not a
  readout.
- **VAE (Table 1).** 4×8×8 into 16 channels. PSNR 33.14 on ImageNet 256² and
  35.39 on MCL-JCV (33×360×640), against CogVideoX-1.5's 31.73 and 33.22,
  Cosmos-VAE's 30.07 and 32.76, and FLUX-VAE's 32.70 (images only).
  Loss = L1 + 0.1·LPIPS + 0.05·adv + 10⁻⁶·KL (Eq. 1). Video to image 4:1.
- **Architecture (Table 2).** 20 dual-stream and 40 single-stream blocks,
  width 3072, FFN 12288, 24 heads of 128, 3D RoPE split (16, 56, 56).
- **Inference (§5).** Shift t′ = s·t/(1+(s−1)t), with s = 7 at 50 steps and
  s = 17 below 20 steps. At 10 steps it is compared against Movie Gen's
  linear-quadratic schedule by samples only (Fig. 11b). Guidance
  distillation, with the scale drawn from 1 to 8, gives "approximatively"
  1.9× (§5.2).
- **Human evaluation (Table 3).** 1,533 prompts, one generation per prompt,
  60 professional evaluators, five closed baselines. Overall 41.3% against
  37.7% for the next best. Motion quality 66.5%, the best. Visual quality
  95.7%, fourth of six. "Overall" is not defined.
- **Systems.** 5D parallelism (TP, SP, CP with Ring Attention, DP with
  ZeroCache). "Training stability is 99.5%" (§5.3.4).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | For the DiT-T2X(I) proxy, compute-optimal N and D scale as C^0.5634 and C^0.4325 | moderate | Chinchilla envelope over seven sizes (Fig. 10a–c). No held-out point, no fit error reported |
| C2 | For image-initialized DiT-T2X(V), N and D scale as C^0.3618 and C^0.6289 | moderate | same method over five sizes (Fig. 10d–f). Only "fits quite well" is said, and only of the image fit |
| C3 | The proxy fits size the shipped 13B flow-matching MLLM model correctly | weak | assumed; objective, encoder, conditioning and resolution all differ |
| C4 | The "optimal scaling approach" reduces compute "by up to 5×" | weak | asserted in §1, no experiment anywhere |
| C5 | The from-scratch causal VAE reconstructs better than prior 16-channel VAEs | moderate | PSNR only, one dataset each, authors' own evaluation (Table 1) |
| C6 | Fine-tuning with tiling randomly on or off removes tiling artifacts | weak | asserted (§4.1.2) |
| C7 | Full attention beats divided spatio-temporal attention | weak | by citation (§4.2) |
| C8 | A decoder-only MLLM with a token refiner beats T5 and CLIP as text encoder | weak | "MLLMs have shown superior performance", with no numbers (§4.3) |
| C9 | Image pretraining "significantly accelerates" video convergence | weak | "early experiments", not shown (§4.5.2) |
| C10 | A larger shift at fewer steps beats linear-quadratic at 10 steps | weak | two sample videos (Fig. 11b) |
| C11 | Guidance distillation gives about 1.9× | weak | one stated figure, no table (§5.2) |
| C12 | HunyuanVideo is rated best overall and best on motion among six systems | weak | one evaluation. "Overall" is undefined, there are no intervals, and competitors are anonymized (Table 3) |

## Method

Filter clips hierarchically (dedup, motion, OCR, clarity, aesthetics), from
256p up to 720p, each stage keeping between half and one-fifth of the last
(Fig. 4). Caption images and videos with an in-house VLM into structured
JSON, with a 14-class camera-movement classifier. Train the VAE from scratch.
Pretrain the transformer on 256px images, then on a 256/512px mix, then on
video and image jointly from 256px to 960px. Timesteps are logit-normal and
sampling uses a first-order Euler solver (§4.5.1). Finish with a human-curated
~1M-clip fine-tuning set (§3.1).

## Concepts

- **DiT-T2X** — the proxy family, X ∈ {I, V}. It is not the shipped
  architecture.
- **Mix-scale training** — several resolution anchors in each global batch,
  so that raising resolution does not degrade 256px generation (§4.5.2).
- **Token refiner** — bidirectional layers after the causal MLLM, to recover
  the bidirectional features T5 would have given (§4.3, Fig. 9).

## Connections

It borrows the dual/single-stream block from FLUX, the envelope method from
Hoffmann et al. ([LIT-068](../literature.d/LIT-068.md)), the logit-normal timestep density from SD3
([LIT-449](../literature.d/LIT-449.md)), and the linear-quadratic comparison from Movie Gen ([LIT-626](../literature.d/LIT-626.md)).
Step-Video ([LIT-624](../literature.d/LIT-624.md)), Open-Sora 2.0 ([LIT-634](../literature.d/LIT-634.md)) and LTX-Video ([LIT-618](../literature.d/LIT-618.md)) all
benchmark against it. Open-Sora 2.0 trains on its VAE.

## Recommendations

- **R1** — When sizing a video diffusion model that starts from an image
  model, fit the video allocation on image-initialized proxies, not cold
  ones. *Topic:* training-optimization. *Status:* experimental.
  *Strength:* weak. *Conditions:* one fit, on a proxy that differs from the
  target in four ways, and never validated at the chosen size.
- **R2** — Expect the video data exponent to exceed the parameter exponent
  after image initialization. Do not carry over an image or language
  allocation. *Topic:* training-optimization. *Status:* experimental.
  *Strength:* weak. *Conditions:* the loss is MSE, D counts latent tokens,
  and only the first stage is covered.
- **R3** — Raise the flow-matching sampling shift as the step count falls.
  *Topic:* inference-optimization. *Status:* experimental. *Strength:* weak.
  *Conditions:* the values 7 and 17 are for this model. The evidence is
  qualitative.

## Bearing on the record

- **[SOTA-266](../practices.d/SOTA-266.md)** — the `consensus_note` says "Wan is the only video report that
  states" the logit-normal. HunyuanVideo states it too: "sample t ∈ [0, 1]
  from a logit-normal distribution [21]" (§4.5.1). That is adoption, so the
  status does not move. The sentence is wrong and should be amended.
- **[SOTA-386](../practices.d/SOTA-386.md)** — adoption, as already recorded. The only support offered is
  "early experiments" (§4.5.2), which are not shown. The mix-scale
  observation, that 512px fine-tuning degrades 256px generation, is a
  distinct and unmeasured claim.
- **[SOTA-389](../practices.d/SOTA-389.md)** — adoption. Its in-house VLM captions video as well as
  images, and the paper runs no comparison.
- **[SOTA-390](../practices.d/SOTA-390.md)** — adoption, justified by citation (§4.2), as recorded.
- **[SOTA-187](../practices.d/SOTA-187.md)** — adoption. Nothing new.
- **[SOTA-263](../practices.d/SOTA-263.md)** — does not bear. HunyuanVideo shifts by step count, not by
  resolution.
- **[SOTA-333](../practices.d/SOTA-333.md)** — does not bear.
- **[SOTA-096](../practices.d/SOTA-096.md)** does not move. The operating points (740B and 928B tokens at
  13B) count latent tokens under an MSE loss, which is not the unit of the
  20-tokens-per-parameter rule.
- **Should it produce a practice?** Not yet. R1 and R2 would be `Proposed`
  at best: one fit, no validation, and no second group.

## Limitations

- **Nothing is ablated.** Every architecture, encoder, data and schedule
  choice is justified by citation, by "we found", or by samples.
- **The scaling fit's scope is narrow**: first stage only, 256px for the
  image family, and video resolution and frame count never stated. There is
  no fit quality for the video family and no test of the predicted optimum.
- **The two fits are not independent.** The video proxies start from the
  image envelope, so C in the video fit presumably excludes the image
  compute. The paper does not say.
- **Table 3's "Overall" is undefined**, and the competitors are anonymized
  except Gen-3 and Luma. Durations differ (5s against 6s for Gen-3).

## Open questions

- Does the video data exponent survive a cold start? Initializing from the
  image envelope is the obvious reason video would favour data.
- What does the fit predict for the shipped objective? Flow-matching MSE and
  v-prediction MSE are different losses.
- Where does the "up to 5×" come from?

## Corrections to the LIT note

- **Wrong:** "The video fit puts more of each added FLOP into data than into
  parameters, more lopsided than the image fit or [LIT-179](../literature.d/LIT-179.md)'s language fit."
  **Fix:** the image fit leans the *other* way, towards parameters
  (b1 = 0.5634 against b2 = 0.4325, §4.4.1). The video fit reverses it
  (0.3618 against 0.6289, §4.4.2). "More lopsided than the image fit" reads
  as though both lean towards data. The paper makes no comparison with any
  language fit. The Llama 3 comparison is the record's own, and needs its
  number cited from [LIT-179](../literature.d/LIT-179.md)'s paper; the value is not in this text. Units
  also differ (latent tokens and MSE, against text tokens and
  cross-entropy). Suggested wording: "The image fit favours parameters
  (0.563 against 0.433). The video fit, initialized from the image-optimal
  checkpoints, favours data (0.362 against 0.629)."
- **Imprecise:** "The proxy family is 'DiT-T2X' from 92M to 6.6B
  parameters." **Fix:** that range and the seven sizes are the image family.
  The video fit uses five sizes, B2 to G2 (Fig. 10d).
- **Misquoted:** "only the first stage of training". **Fix:** the text says
  the token amounts are "only related to the first stage of training for
  images and videos respectively" (§4.4.2).
- **Overstated:** "It sized the model at 13B." **Fix:** 13B was chosen from
  the fits "taking into account the training consumption and inference
  cost", not read off them.
- **Wrong:** "1,533 prompts rated once each by 60 professional raters."
  **Fix:** the "once" is generation: "we conducted inference only once,
  avoiding any cherry-picking" (§6.1). How many ratings each video received
  is not stated.
