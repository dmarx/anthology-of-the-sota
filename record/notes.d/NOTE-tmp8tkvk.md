---
status: Read
paper: LIT-624
title: 'Step-Video-T2V'
version: 1
date: '2026-09-24'
summary: >-
  A 30B text-to-video DiT on a 16×16×8 VAE. By the authors' own benchmark
  the VAE reconstructs about as well as HunyuanVideo's 8×8×4, and an
  independent measurement in Open-Sora 2.0 disagrees. Video DPO raises a
  tie-weighted preference score from 45% to 55% on 300 prompts. Every
  architecture comparison is reported without numbers, and the "state of
  the art" in the abstract is contradicted by the paper's own Table 9.
---

<!-- inactive-ok-file: SOTA-333 SOTA-386 SOTA-389 SOTA-390 — Proposed, and cited here to weigh the evidence for them; this document is part of that evidence, not an endorsement -->

# NOTE-tmp8tkvk: Step-Video-T2V

Read in full from arXiv v3 (24 February 2025): §§1–11, all tables,
references and the contributor list, including the §6 systems material the
LIT note skimmed. There are no appendices. The figures carry samples and
training curves without numeric labels. Fig. 10 (loss by stage) and Fig. 11
(filter funnel) could only be read from their captions.

## Contribution

Four things, in order of how well each is supported:

- **Systems measurements.** MFU, restart rates and fault taxonomy at the
  scale of thousands of H800s.
- **A deep-compression video VAE**, 8×16×16 with a dual-path pixel-unshuffle
  and channel-averaging design.
- **A video adaptation of Diffusion-DPO.**
- **A 30B model and a 128-prompt Chinese benchmark**, Step-Video-T2V-Eval.

The report is also unusually candid about what it does not know (§10).

## Key insight

**Put the compression in the autoencoder, not in the patchifier, and train
the autoencoder in stages.** First a 4×8×8 VAE without the dual path, then
dual-path modules spliced in after the mid-block and unfrozen gradually,
then a GAN loss once the other losses converge (§4.1.4). The
channel-averaging shortcut carries low-frequency structure, and the
convolution path carries detail (§4.1.2). That split is borrowed from DC-AE
(Chen et al. 2025) and extended to time.

## Assumptions

- **Its own reconstruction benchmark is representative.** Table 15 uses
  1,000 test videos of 50×480×768 "from various domains", chosen by the
  authors.
- **Human preference on 128 Chinese prompts measures quality.** The
  international baseline (Gen-3) received translated prompts (§9.3).
- **Training loss across data stages is comparable.** §8 reads step drops in
  loss at each dataset switch as learning. Loss measured on a different,
  cleaner dataset is not the same quantity.

## Key results

- **VAE (Table 15).** Video-VAE at 8×16×16: SSIM 0.9776, PSNR 39.37,
  rFVD 3.61. HunyuanVideo at 4×8×8: 0.9710, 39.56, 4.17. Cosmos-VAE at
  8×16×16: 0.8862, 34.82, 40.33. The latent channel count is never stated.
  [LIT-634](../literature.d/LIT-634.md)'s Table 1 lists it as 64.
- **Independent check.** Open-Sora 2.0 ([LIT-634](../literature.d/LIT-634.md), Table 1) measures this VAE
  at LPIPS 0.082, PSNR 28.719, SSIM 0.818, against HunyuanVideo's 0.046,
  30.240, 0.856. The evaluation set and resolution differ from Table 15's.
- **Model (Table 1, §4.3).** 48 layers, 48 heads of 128, FFN 24,576, and
  cross-attention to Hunyuan-CLIP (77 tokens) and Step-LLM, with the two
  concatenated. AdaLN-Single, RoPE-3D, QK-Norm, and a straight-path flow
  matching objective (Eq. 5). The pretraining timestep density is not stated
  ("a random timestep t ∈ [0, 1]").
- **Training (Table 6).** T2I at 256px: 253k iterations, 3.8B samples. T2VI
  at 192×320: 430k iterations, 644M samples. T2VI at 544×992: 46k
  iterations, 27.3M samples. The data pool is 2B video-text and 3.8B
  image-text pairs (§7.1).
- **DPO (§9.7).** 300 prompts, identical initial noise, three annotators,
  one point per preference and 0.5 each for "no preference". Result: 55%
  against 45%. β and the learning rate are unreported. The only stated
  reasoning is that β = 5,000 with lr 10⁻⁸ (Diffusion-DPO's) converges
  slowly (Eq. 9).
- **Turbo (§5).** 2-rectified-flow self-distillation on ~95,000 samples
  generated at 50 NFE. U-shaped timestep density p(u) ∝ e^{au} + e^{−au} with
  a = 5, and a linearly decaying CFG (Eq. 11). "Comparable sample quality
  with up to 10 times fewer steps" is shown by samples (Fig. 6).
- **Human evaluation.**
  - Against HunyuanVideo on its own benchmark: 59-22-47, 46-47-35 and
    54-41-33 across three annotators (Table 7).
  - On Movie Gen Bench: 615-313-361 against HunyuanVideo and 485-315-489
    against Movie Gen, over 1,289 evaluations with six annotators
    (Table 14).
  - It loses to T2VTopA on all three annotators (44-13-69, 41-13-72,
    46-25-55; Table 9). §9.3 ranks "T2VTopA > Step-Video-T2V > T2VTopB".
- **Systems.**
  - SEMU-estimated MFU is 31.79–36.47% across configurations (Table 2).
    The chosen TP8 + SP + ZeRO-1 is 0.88% below the optimum and measures
    32% in practice (§6.2.2).
  - Hardware restarts: 0.037 per 1k GPUs per day, against Llama 3.1's
    0.422 (Table 5).
  - Seven fatal hardware failures in a month (Table 4). 99% effective
    training time.
  - Channels-last VAE convolutions give "up to 7x" encode throughput
    (§6.2.3).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | A 16×16×8 VAE can match 8×8×4 VAEs on reconstruction | weak | own benchmark (Table 15). An independent measurement ([LIT-634](../literature.d/LIT-634.md) Table 1) finds it clearly worse |
| C2 | Video-DPO improves preference over the base model | moderate | a controlled comparison with fixed noise, but one run, 55/45 with ties counted half, and unreported hyperparameters (§9.7) |
| C3 | Smaller β with a larger learning rate converges faster than Diffusion-DPO's defaults | weak | the gradient-scaling argument (Eq. 9). No curves |
| C4 | DPO gains saturate because the preference data goes stale off-policy | weak | observation plus conjecture ("may stem from", §4.4) |
| C5 | T2I pretraining is necessary; T2V from scratch converges much slower | weak | early 4B experiments, not shown (§8) |
| C6 | 3D full attention beats spatial-temporal attention, "particularly" on high motion | weak | a 4B comparison, no numbers (§10.1) |
| C7 | DiT and MMDiT perform similarly | weak | early training curves, not shown. MMDiT was not trained long (§10.1) |
| C8 | Low-resolution video pretraining learns motion and high resolution learns detail | weak | observation (§8) |
| C9 | Averaging SFT checkpoints beats EMA | weak | "we found" (§8) |
| C10 | The TP8 + SP + ZeRO-1 configuration reaches 32% MFU at 540P | moderate | measured, and consistent with the simulator (Table 2, §6.2.2) |
| C11 | Hardware restart rate is about 1/11 of Llama 3.1's | moderate | measured over one month of one job, against another group's cluster (Table 5) |
| C12 | Step-Video is at parity with Movie Gen and ahead of HunyuanVideo on Movie Gen Bench | moderate | 1,289 blinded evaluations (Table 14). 204 against 129 frames and 540P are not controlled |
| C13 | Step-Video is "state-of-the-art … compared with … commercial engines" | weak | contradicted by Table 9 and §9.3 |
| C14 | Physics failures reflect "inherent limitations of diffusion models" | weak | asserted (§§10.3, 11) |

## Method

The Video-VAE's causal 3D encoder feeds two dual-path stages. The conv path
is a causal 3D convolution plus pixel-unshuffle. The shortcut path is a
grouped channel average after unshuffle. The two are summed (Eqs. 2–4). The
decoder mirrors this with pixel-shuffle and channel repetition, and uses
spatial GroupNorm to avoid flicker between chunks.

Training runs in cascade: T2I from scratch, T2VI at 192P then 540P with
hierarchically filtered subsets, T2V SFT on human-filtered clips with
checkpoint averaging, then DPO. VAE and text encoders run on separate
inference clusters and stream latents to the DiT job (StepRPC, §6.3).

## Concepts

- **Level-1 / Level-2 video foundation model** — translation from text to
  video, against prediction of future events. The paper places all current
  diffusion models at Level-1 (§1).
- **Metric-1 / Metric-2** — blinded win/tie/loss, and 1–5 scores on
  instruction following, motion smoothness, physical plausibility and
  aesthetics (§9.1).
- **Hybrid-grained load balance** — batch size per resolution set by FLOPs
  (Eq. 12, Table 3), then greedy image padding (§6.2.4).

## Connections

It extends Diffusion-DPO (Wallace et al.) and DPO ([LIT-169](../literature.d/LIT-169.md)) to flow
matching, and cites DC-AE for the channel-averaging idea. HunyuanVideo
([LIT-620](../literature.d/LIT-620.md)) is its main open baseline. Open-Sora 2.0 ([LIT-634](../literature.d/LIT-634.md)) later matches
its VAE's information ratio with a 128-channel DC-AE and measures its VAE
independently. It follows Movie Gen ([LIT-626](../literature.d/LIT-626.md)) on trimming clip edges, SFT
curation and checkpoint averaging.

## Recommendations

- **R1** — When applying Diffusion-DPO to a large video model, do not inherit
  β = 5,000 and lr 10⁻⁸. Lower β and raise the learning rate, and fix the
  initial noise and timestep across each pair. *Topic:* adaptation-and-tuning.
  *Status:* experimental. *Strength:* weak. *Conditions:* the values used
  are not reported.
- **R2** — Refresh preference data on-policy, or score it with a reward
  model, once the policy distinguishes the pairs easily. *Topic:*
  adaptation-and-tuning. *Status:* experimental. *Strength:* weak.
- **R3** — Validate a high-compression video VAE on someone else's
  benchmark before comparing it with lower-compression ones, and state the
  latent channel count. *Topic:* representation-and-encoding. *Status:*
  standard. *Strength:* moderate. *Conditions:* this report and [LIT-634](../literature.d/LIT-634.md)
  disagree about the same VAE.

## Bearing on the record

- **[SOTA-386](../practices.d/SOTA-386.md)** — adoption. The 4B from-scratch experiment is mentioned and
  not shown, as the `consensus_note` already says.
- **[SOTA-390](../practices.d/SOTA-390.md)** — the unquantified 4B comparison, exactly as `promote_when`
  records it. Does not move.
- **[SOTA-389](../practices.d/SOTA-389.md)** — Step-Video recaptions with an in-house VLM, SFT'd on camera
  movement (§7.1). The `consensus_note` should list it. It is adoption. The
  paper attributes T2VTopA's instruction-following lead to a "better video
  captioning model" (§9.3), which is belief, not measurement.
- **[SOTA-266](../practices.d/SOTA-266.md)** — the straight path is confirmed as adopted (Eq. 5). No
  logit-normal is stated for pretraining. The Turbo stage uses a U-shaped
  density instead, a different thing.
- **[SOTA-187](../practices.d/SOTA-187.md)** — adoption. Nothing new.
- **[SOTA-305](../practices.d/SOTA-305.md)** — a case for it. "8 times larger" compression (§9.6) counts
  tokens, not information. At 64 channels (per [LIT-634](../literature.d/LIT-634.md)) the information
  ratio is 96 against HunyuanVideo's 48, which is 2×.
- **[SOTA-333](../practices.d/SOTA-333.md)** — does not bear. Mixing autoregression and diffusion is
  listed as future work (§10.3).

## Limitations

- **No architecture comparison has a number.** The DiT/MMDiT and 3D/2D+1D
  comparisons were at 4B and early in training.
- **The VAE result is the authors' own benchmark** and is not replicated.
- **The DPO result is small and under-specified**: 300 prompts, three
  annotators, and ties folded into the score.
- **The 540P sample count disagrees**: 25.3M in §9.3 against 27.3M in
  Table 6 and §9.4.
- **The loss-drop reading in §8** ("may emulate human cognitive patterns")
  compares losses on different data.
- **Eq. 7 as printed omits the initial noise term.**

## Open questions

- Which VAE evaluation is right? The two disagree by about 11 PSNR points in
  absolute terms. On SSIM they flip the ranking against HunyuanVideo (0.9776
  against 0.9710 in Table 15, and 0.818 against 0.856 in [LIT-634](../literature.d/LIT-634.md)'s Table 1).
- What were β and the learning rate for Video-DPO?
- Does the 192P-heavy compute allocation (430k of 729k iterations) matter,
  or is it only affordable?

## Corrections to the LIT note

- **Unqualified:** "Compression doubles in each spatial dimension with no
  loss" (key takeaway) and "reconstructs as well as HunyuanVideo's 8×8×4"
  (summary). **Fix:** this holds on Step-Video's own benchmark (Table 15).
  [LIT-634](../literature.d/LIT-634.md) Table 1 measures the same VAE well below HunyuanVideo's (LPIPS
  0.082 against 0.046, PSNR 28.719 against 30.240). The temporal factor also
  doubles (8 against 4), and the latent is 64 channels against 16 (per
  [LIT-634](../literature.d/LIT-634.md)), so the information ratio is 2×, not 8×.
- **Imprecise:** "the DPO model is preferred 55% to 45%". **Fix:** it is a
  preference *score*, with "no preference" worth 0.5 to each side (§9.7).
  It is not a win rate, and the tie rate is not given.
