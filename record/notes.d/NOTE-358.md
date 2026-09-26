---
number: 358
status: Read
formerly:
- NOTE-tmpb6qj9
paper: LIT-699
title: 'Diffusion Models Beat GANs'
version: 1
date: '2026-09-25'
summary: >-
  An ablated U-Net (ADM) and a classifier-gradient scale that trades recall for
  precision take diffusion past BigGAN-deep on ImageNet FID. The architecture
  search is single-run; every guided number is the best of a small scale sweep
  scored on the metric it reports; and the trade is non-monotone — a scale of 1
  makes an unconditional model's FID worse (26.21 → 33.03). The claim that large
  scales produce no adversarial examples is asserted in the introduction and
  checked only by eye and in Inception feature space.
---

<!-- inactive-ok-file: THEORY-109 — Proposed, and named here as the open question this paper's method is the subject of: this reading supplies evidence bearing on it and relies on no settled account from it. -->

# NOTE-358: Diffusion Models Beat GANs

Read in full from arXiv v4 (1 Jun 2021): the main text, all appendices A–M
including the throughput and compute tables (A), the conditional-process proof
(H), the hyperparameter tables (I) and the LSUN schedule sweep (J). Figures 2, 4,
5 and 11 were read from captions, axes and the surrounding text; the sample
grids (Figs. 1, 3, 6–10, 12–27) from their captions.

## Contribution

Two separable things. An architecture: the DDPM U-Net with more heads (64
channels each), attention at 32/16/8, BigGAN residual up/downsampling, and
adaptive group normalization, chosen by ablation — called ADM. And a sampler:
classifier guidance, which adds a scaled gradient of a noisy-image classifier to
each reverse step and so gives diffusion the fidelity–diversity knob GANs had in
truncation. Together they take FID on ImageNet 128, 256 and 512 below
BigGAN-deep's, with higher recall.

## Key insight

**The scale is the method.** At the theoretically grounded value `s = 1` guidance
on an unconditional model does not work — the classifier reports ~50% on samples
that visibly are not the class. Treating `s` as `p(y|x)^s` sharpening licenses
going far past 1, and once you do, `s` is a single dial that moves precision up
and recall down, with FID best somewhere in the middle. Everything the paper
reports for guided models is a point on that dial chosen by FID.

## Assumptions

- **The classifier's log-probability has low curvature relative to `Σ⁻¹`**
  (Eqs. 5–10), reasonable as the number of steps grows and `‖Σ‖ → 0`. That is
  what makes the conditional step a mean-shifted Gaussian.
- **The DDIM variant is a score-substitution**, not the same derivation: Eq. 14
  replaces `ε` by `ε − √(1−ᾱ_t)∇log p(y|x_t)`, adapted from Song et al. —
  [LIT-tmptxfkp](../literature.d/LIT-tmptxfkp.md), where the general form is the conditional reverse-time SDE.
- **A classifier trained on the diffusion model's own noising distribution**,
  with random crops against overfitting. An off-the-shelf clean-image classifier
  is not what is used.
- **Labels exist.** The method is class-conditional ImageNet; LSUN results use
  architecture alone.
- Pixel space throughout, 64–512 px, 1000 training steps, learned variances with
  the hybrid objective from Nichol & Dhariwal's IDDPM.

## Key results

- **Table 1** (ImageNet 128, batch 256, 250 steps; FID Δ at 700K / 1200K from
  15.33 / 13.21): depth 4 −0.21 / −0.48; 4 heads −0.54 / −0.82; multi-resolution
  attention −0.72 / −0.66; BigGAN up/down −1.20 / −1.21; **1/√2 residual rescale
  +0.16 / +0.25**; heads + multi-res + BigGAN −3.14 / −3.00.
- **Table 2** (700K): 1 head 14.08; more heads or fewer channels per head
  improve FID, 32 channels per head best (−1.36); 64 chosen for wall clock.
- **Table 3**: AdaGN 13.06, addition + GroupNorm 15.08.
- **Table 4** (ImageNet 256, 2M iterations): unconditional 26.21 → 33.03 (`s=1`)
  → 12.00 (`s=10`); conditional 10.94 → 4.59 (`s=1`) → 9.11 (`s=10`). Precision
  rises and recall falls with `s` in both.
- **Table 5**: ADM-G 2.97 / 4.59 / 7.72 at 128 / 256 / 512 (250 steps); 5.98 /
  5.44 / 8.41 at 25 DDIM steps; BigGAN-deep 6.02 / 6.95 / 8.43. Unguided ADM at
  256 is 10.94 and at 512 is 23.24 — **worse than BigGAN-deep without guidance**
  at both; at 128 it edges it, 5.91 vs 6.02. LSUN bedroom 1.90, horse 2.57, cat 5.57, all at 1000 steps.
- **Table 6**: guidance + upsampling 3.94 (256) and 3.85 (512); upsampling alone
  raises precision at constant recall, guidance trades recall away.
- **Table 14**: scales used — 1.0 / 0.5 / 1.0 / 4.0 at 64 / 128 / 256 / 512 with
  250 steps; 1.25 / 2.5 / 9.0 for 25-step DDIM at 128 / 256 / 512.
- **Tables 8–10**: 128×128 guided model beats BigGAN-deep's FID after 500K of
  4360K iterations; 256×256 after 750K of 1980K.
- **Table 7**: optimized throughput 29–41% of V100 peak; naive 18–25%.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Diffusion models beat GANs on ImageNet FID | strong for the guided models; for the unguided ones true at 64 and 128, false at 256 and 512 | Table 5, 50k samples, baselines re-scored in one codebase. Unguided ADM loses to BigGAN-deep at 256 (10.94 vs 6.95) and 512 (23.24 vs 8.43); the title's claim at those resolutions is carried by guidance |
| C2 | The ablated architecture changes each improve FID and compound | moderate | Table 1, one run per cell, two checkpoints that agree in sign. No seeds, no intervals. Fig. 2 on 10k samples |
| C3 | Rescaling residuals by 1/√2 hurts | weak | +0.16 / +0.25 FID, single run; the smallest effect in the table |
| C4 | AdaGN beats addition + GroupNorm | moderate | Table 3, 2.02 FID, one pair of runs at 700K |
| C5 | Classifier guidance trades diversity for fidelity through one scale | strong | Table 4 and Fig. 4: precision and IS rise, recall falls monotonically in `s` on both models |
| C6 | Guidance improves FID | conditional on the scale | Table 4: it worsens an unconditional model at `s = 1` and a conditional one at `s = 10` relative to `s = 1`. FID is non-monotone in `s` (Fig. 4) |
| C7 | Large scales do not produce adversarial examples | weak | One sentence in §1. Evidence is sample grids (Figs. 3, 8) and Inception-space nearest neighbours (App. C). No metric independent of a classifier; the precision/recall feature network is not stated |
| C8 | Guidance beats BigGAN truncation | moderate, and only on one axis | Fig. 5: "strictly better" on FID vs IS; on precision vs recall better only below a precision threshold |
| C9 | 25 DDIM steps match BigGAN-deep | moderate | Table 5, at separately tuned scales (Table 14); at 128 the margin is 5.98 vs 6.02 |
| C10 | Same or lower training compute than BigGAN-deep | weak | Table 10 converts BigGAN's TPU estimate at an asserted 2:1 rate and compares an early checkpoint's FID to a published range |
| C11 | Guidance and upsampling are complementary | moderate | Table 6, one configuration per cell; best FIDs at both resolutions come from the combination |

## Method

Train the ADM U-Net with `L_simple + λL_vlb` and learned interpolated variances,
Adam or AdamW at β = (0.9, 0.999), EMA 0.9999, fp16 activations with loss
scaling and fp32 weights, EMA and optimizer state (App. I). Train a classifier of
the U-Net's downsampling trunk plus attention pool on noised images at the same
schedule. Sample with Algorithm 1 (250 steps) or Algorithm 2 (DDIM, 25 steps),
scale chosen per resolution and sampler by a sweep on FID. For 256 and 512,
optionally generate at 64 or 128 with guidance and upsample with an unguided
ADM-U.

## Concepts

- **ADM / ADM-G / ADM-U** — the ablated diffusion model; with classifier
  guidance; the upsampling stack with the same architecture changes.
- **Gradient scale `s`** — multiplier on `∇log p(y|x_t)`; equivalent to guiding
  with `p(y|x)^s / Z`. Classifier-free guidance's `w` ([LIT-693](../literature.d/LIT-693.md)) has the same form
  but multiplies an implicit classifier's gradient, so equal values are not
  equal guidance.
- **AdaGN** — `y_s·GroupNorm(h) + y_b`, with `(y_s, y_b)` projected from the
  timestep and class embedding.

## Connections

It builds on DDPM ([LIT-036](../literature.d/LIT-036.md)) for the model and objective, on IDDPM for learned
variances and the upsampling stack, and on DDIM ([LIT-038](../literature.d/LIT-038.md)) for the 25-step
sampler; the guided-transition derivation is reviewed from Sohl-Dickstein et al.
([LIT-439](../literature.d/LIT-439.md)). It is compared against StyleGAN ([LIT-561](../literature.d/LIT-561.md)), StyleGAN2 ([LIT-560](../literature.d/LIT-560.md)) and
DDPM on LSUN with re-scored baselines. Classifier-free guidance ([LIT-693](../literature.d/LIT-693.md)) is the
successor that removes the classifier and cites ADM-G as the number to beat.
DiT ([LIT-448](../literature.d/LIT-448.md)) keeps the class-and-timestep modulation idea as adaLN and replaces
the U-Net.

## Recommendations

- **R1.** Treat any guidance scale as a precision–recall dial and report the
  scale beside every FID/IS. *Topic:* analysis-and-evaluation. *Status:*
  standard. *Strength:* strong (C5, C6). *Applies when:* any guided sampler.
- **R2.** Re-score baselines from their public samples in one codebase against
  a fixed reference set rather than copying reported FIDs. *Topic:*
  analysis-and-evaluation. *Status:* standard. *Strength:* moderate — stated
  practice, reason given, not itself measured here.
- **R3.** Do not treat the ADM U-Net's internals as settled design. *Topic:*
  model-architecture. *Status:* experimental. *Strength:* weak (C2, C3) —
  single-run ablation at one resolution.

## Bearing on the record

| document | disposition |
|---|---|
| [THEORY-109](../theory.d/THEORY-109.md) | **sharpened.** The suspicion concerns this paper's method, and this paper's own sentence against it (C7) is untested. Two facts it did not carry: the guiding classifier is a noisy-image U-Net trunk, not Inception-V3, so the concern is transfer between two ImageNet classifiers rather than attacking the scorer itself; and at `s = 1` the paper saw exactly the classifier-satisfied, visually-wrong shape the account predicts. Stays `Proposed` — neither fact is a classifier-free measurement |
| [LIT-693](../literature.d/LIT-693.md) | its account of the predecessor is correct (noisy-data classifier required; trade compared to truncation). Relation declared: it extends and was compared against this |
| [LIT-676](../literature.d/LIT-676.md), [SOTA-203](../practices.d/SOTA-203.md), [SOTA-410](../practices.d/SOTA-410.md) | **context added, no claim changed.** Their ImageNet table runs this model at classifier scale 8.0; the authors' own tuned 25-step DDIM scale at 256 is 2.5 (FID 5.44), and their widest sweep there stopped at 3.5. The table is a stress test at ~3× the tuned scale, which is what it is for — but its FIDs are not the model's quality, and a classifier scale of 8.0 is not the same knob as Stable Diffusion's CFG weight of 7.5 |
| [SOTA-307](../practices.d/SOTA-307.md) | consistent. Every ADM-G number is a per-cell scale sweep chosen on FID with nothing held out — the practice it recommends, and the reason it matters |
| [NOTE-340](NOTE-340.md) | its C7 caveat is strengthened: FM's "33% less image throughput" is measured against ADM's **class-conditional** 128×128 run (4360K × 256, Table 11), while FM's model is unconditional |
| [LIT-448](../literature.d/LIT-448.md) | "ablated its internals but left the high-level design intact" — correct (Tables 1–3) |
| [LIT-630](../literature.d/LIT-630.md), [LIT-692](../literature.d/LIT-692.md) | use the ADM U-Net as an instrument; nothing to correct |

## Limitations

- **No variance anywhere.** Ablations, scale sweeps and headline cells are single
  runs.
- **Every metric is Inception-based**, and the precision/recall feature network
  is not named. There is no human evaluation.
- **Scale selection is on the test metric** (App. I, Table 14).
- **Labels required** for guidance; the authors say so (§7).
- **Sampling cost.** 250 steps for headline numbers, 1000 for LSUN; the authors
  list it as the main limitation.
- **LSUN step-count reversal** (App. J): 1000 steps beat 250 "contrary to
  previous results", and the fix is a hand-swept schedule chosen on bedroom FID.

## Open questions

- Does guidance's FID gain survive a metric with no classifier in it? That is
  [THEORY-109](../theory.d/THEORY-109.md)'s `promote_when`, and nothing in this paper touches it.
- Would the architecture ranking in Table 1 survive seeds, given effects of
  0.2–0.8 FID?
- Why does `s = 1` fail on an unconditional model — the Taylor approximation, the
  classifier's calibration on noisy inputs, or something else? The paper reports
  it and moves on.
