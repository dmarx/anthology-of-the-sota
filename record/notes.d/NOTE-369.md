---
number: 369
status: Read
formerly:
- NOTE-tmpiw6ga
paper: LIT-710
title: 'Min-SNR weighting'
version: 1
date: '2026-09-25'
summary: >-
  Capping the x0-space loss weight at min(SNR, 5) speeds diffusion training
  under x0, ε and v prediction, and makes ε output trainable under weightings
  that otherwise diverge. The 3.4× headline is against constant-weighted
  x0-prediction. Against plain ε-MSE on a UNet, FID goes 8.55 → 7.32 at 200K
  iterations and 4.21 → 4.14 at 1M, single runs. The multi-task
  "conflicting gradients" account is motivated by one probe and a proxy
  objective, and is not tested against FID.
---

# NOTE-369: Min-SNR weighting

Read in full from arXiv v3 (11 Mar 2024). That covers §§1–5, the proof of
Theorem 1 (App. A), the target-conversion derivations (App. B), the
architecture, training and sampling settings (App. C), and the pixel-space
and EDM ablations (App. D.1). Figures 1, 2, 4, 5, 6, 8 and 9 were read from
axes, legends and the surrounding text. The sample grids (Figs. 7, 10–13)
were read from their captions only.

## Contribution

A fixed per-timestep loss weight, `w_t = min(SNR(t), γ)` in x0-space. It is
motivated by treating the T denoising timesteps as T tasks sharing one
network. It is compared under three prediction targets and two backbones
with the constant, SNR and truncated-SNR (`max(SNR, 1)`) weightings. It is
the fastest-converging of the four in every cell the paper runs.

## Key insight

**Where the weight sits in x0-space decides where training goes.** ε-MSE
already weights x0 error by SNR, which is huge at low noise. Constant x0
weighting ignores the low-noise end, and pure SNR weighting ignores the
high-noise end (Fig. 6). Capping SNR at a small γ gives the low-noise steps
equal weight with each other without letting them swamp the rest. Written on
the ε loss it is `min(γ/SNR, 1)`. That leaves ε-MSE alone at high noise and
down-weights the low-noise steps.

## Assumptions

- Variance-preserving diffusion, `α_t = √(1 − σ_t²)`, cosine schedule,
  T = 1000 discrete steps.
- **Targets are equivalent up to weight** (App. B): `‖ε − ε̂‖² = SNR·‖x0 − x̂0‖²`
  and `‖v − v̂‖² = (SNR + 1)·‖x0 − x̂0‖²`. The weighting is defined in
  x0-space and converted by these factors.
- The multi-task derivation assumes a first-order Taylor expansion (Eq. 7).
  It also assumes the per-step gradients are stable enough, after "a
  moderate number of iterations", for a stationary weight to stand in for a
  per-iteration Pareto solve (§1). That second assumption is asserted, not
  shown.
- Latent diffusion on SD's VAE (32×32×4) at 256. Pixel space at 64.

## Key results

- **Fig. 5** (ImageNet 256 latent, ViT-B, 1M iterations): Min-SNR-5 fastest
  under x0, ε and v. Time to FID 10 is 3.4× shorter than **x0 + constant**.
  **ε + constant and ε + Max-SNR-1 diverge.**
- **Fig. 6**: unweighted x0-MSE by timestep bin. Constant weighting does best
  at high noise and worst at low noise, and SNR weighting does the reverse.
  Min-SNR-5 is lowest in all four bins shown.
- **Table 1** (UNet, ~ViT-B FLOPs): x0 25.93 → 7.99 at 200K and 8.33 → 4.28
  at 1M. ε 8.55 → 7.32 at 200K and 4.21 → 4.14 at 1M.
- **Table 2** (γ ∈ {1, 5, 10, 20}): FID spread ≤ 0.57 in every row. UNet-ε is
  best at γ = 20 (4.12), not 5.
- **Table 5**: ViT-XL, x0 + Min-SNR-5, CFG 1.5, ~7M iterations, FID 2.06.
  ε + Min-SNR-5 gives 2.08 at 2.1M iterations. DiT-XL/2's published figure is
  2.27. UNet 395M at 1.4M iterations gives 2.81.
- **Tables 3–4**: CelebA-64 unconditional, UNet 1.60 and ViT-S 2.14.
  ImageNet-64 ViT-L 2.28.
- **App. D.1.1, Fig. 9**: EDM × `min(SNR, 5)/SNR` converges faster over 200M
  training images, short of EDM's full run.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Min-SNR-γ converges faster than constant, SNR and max(SNR,1) weighting | moderate | Fig. 5 and Table 1, one run per curve, two backbones, three targets, all in the same direction |
| C2 | The speedup is 3.4× | weak as a general number | Time to FID 10, x0-prediction, against the constant-weight x0 baseline only (Fig. 5 left). Against ε-MSE the UNet gap at 1M is 0.07 FID |
| C3 | It improves final quality, not only speed | weak | Table 1 end points differ by 0.07 (ε) on single runs. The large x0 gap reflects a poor baseline |
| C4 | It is robust to γ | moderate | Table 2, four γ in four settings, spread ≤ 0.57 FID |
| C5 | ε output with constant or max(SNR,1) weighting diverges | moderate | Fig. 5 centre, stated in the caption. Consistent with both weights being 1/SNR on the ε loss |
| C6 | Slow convergence is caused by conflicting gradients across timesteps | weak | Fig. 2: fine-tuning three bins raises loss at distant bins. Fig. 4: Min-SNR-5 scores near a per-iteration solver on the authors' Eq. 11 proxy. Neither measures gradient conflict against convergence |
| C7 | New ImageNet-256 FID record (2.06) | moderate, as a system result | Table 5, a different backbone, schedule and sampler from DiT's. The DiT number is taken from its paper, not re-run |
| C8 | 3.3× faster than DiT | weak | Iteration counts compared across codebases and optimizers. AdamW β = (0.99, 0.99) here |
| C9 | It helps inside EDM | weak | Fig. 9, one curve pair, truncated at 200M images |

## Method

Sample `t` uniformly and form `x_t = α_t x0 + σ_t ε`. Predict x0, ε or v.
Compute the plain MSE on that target and multiply by `min(SNR, γ)`,
`min(SNR, γ)/SNR` or `min(SNR, γ)/(SNR+1)` respectively. That is the whole
change. The Pareto solver of §3.3 (Frank–Wolfe or softmax-reparameterized
gradient descent on Eq. 11) is the reference it is compared to. It is not
part of the method.

## Concepts

- **SNR(t)** — `α_t²/σ_t²`. The paper writes weights in x0-space throughout,
  so its "SNR weighting" on an ε model is plain ε-MSE, and its "constant" is
  `1/SNR` on the ε loss.
- **Max-SNR-γ** — `max(SNR, γ)`, the truncated SNR of [LIT-067](../literature.d/LIT-067.md), γ = 1.
- **Pareto stationary** — no update direction lowers every timestep's loss at
  once (Theorem 1, from Désidéri's MGDA).

## Connections

It rewrites DDPM's ([LIT-036](../literature.d/LIT-036.md)) L_simple as SNR weighting in x0-space
and caps it. It runs Progressive Distillation's truncated-SNR weighting
([LIT-067](../literature.d/LIT-067.md)) as a baseline and beats it. It applies the cap inside EDM
([LIT-075](../literature.d/LIT-075.md)) and compares its ImageNet-256 result to DiT ([LIT-448](../literature.d/LIT-448.md)). Kingma &
Gao ([LIT-692](../literature.d/LIT-692.md)) later list its implied weighting,
`sech(λ/2)·min(1, γe^{−λ})` under a cosine schedule. That weighting is not
monotone.

## Recommendations

- **R1.** If you predict x0 or v, or see instability from over-weighted
  low-noise steps, weight the x0-space loss by `min(SNR, 5)`. *Topic:*
  generative-modeling. *Status:* experimental. *Strength:* moderate (C1, C4).
  *Applies when:* discrete VP diffusion, image or latent, training from
  scratch.
- **R2.** Expect little end-point change for ε-prediction with plain MSE.
  The gain there is early convergence. *Strength:* moderate (C2, C3).
- **R3.** Never pair ε output with an x0-space weight that is constant or
  bounded below at the noisy end. It puts `1/SNR` on the ε loss. *Strength:*
  moderate (C5).

## Bearing on the record

| document | disposition |
|---|---|
| [SOTA-195](../practices.d/SOTA-195.md) | **context added.** Its weighting paragraph offers [LIT-067](../literature.d/LIT-067.md)'s `max(SNR, 1)` and `SNR + 1`, and notes that v with unweighted MSE "picks the weighting for you". This paper runs both against `min(SNR, 5)`, and the cap converges faster under every target. It also finds `max(SNR, 1)` diverges with ε output. The practice's recommendation, to predict v, is untouched, since v + Min-SNR still trains. It is the default weighting that has a measured alternative. A paragraph now says so |
| [SOTA-188](../practices.d/SOTA-188.md) | **consistent, not edited.** EDM's λ(σ) is the weight App. D.1.1 multiplies by `min(SNR, 5)/SNR`, and the result is faster early convergence on one truncated curve. Too thin to qualify a practice sourced on EDM's full runs |
| [LIT-692](../literature.d/LIT-692.md), [THEORY-107](../theory.d/THEORY-107.md) | named this weighting before the record held it. Their classification of it as non-monotone is correct for the paper's cosine schedule. Nothing to change |
| none | **no practice recommends Min-SNR.** R1 is a candidate. Adoption is real (diffusers `--snr_gamma`, kohya-ss `--min_snr_gamma`), but the evidence is one group, and for the ε default it is mostly an early-training effect. A practice filed from it would be `Proposed`, with `promote_when` asking for a second group's end-of-training comparison against ε-MSE |

## Limitations

- Single runs everywhere. There are no seeds and no intervals, and the γ
  sweep's spread is of the same order as the effects it is used to dismiss.
- The headline baseline is chosen to be weak. Constant-weighted x0 is not
  what anyone trains by default.
- The EDM result stops at 200M images, and the authors say why.
- The theory is motivation. The weighting is fixed and nobody derived it from
  the Pareto objective: it was chosen, then scored on that objective.
- Every run uses uniform-t sampling with a cosine schedule. The interaction
  with non-uniform noise sampling ([SOTA-188](../practices.d/SOTA-188.md)'s log-normal, SD3's
  logit-normal) is not studied. There the weighting and the sampler are
  partly the same knob ([LIT-692](../literature.d/LIT-692.md)).

## Open questions

- Does the ε-prediction gain survive to convergence at scale, with seeds?
  That decides whether it is a practice or a warm-up trick.
- Is Min-SNR on uniform t equivalent to some non-uniform timestep sampler
  with plain MSE? The expectation is the same, but the gradient variance is
  not.
- Does the gradient-conflict account predict anything the weighting does not?
  For example, does per-bin gradient cosine similarity track the convergence
  gap?
