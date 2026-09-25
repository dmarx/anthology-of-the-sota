---
status: Read
paper: LIT-tmpzn7w1
title: 'EDM2'
version: 1
date: '2026-09-25'
summary: >-
  Magnitude-preserving layers plus forced weight normalization take the ADM
  U-Net from FID 8.00 to 2.56 on ImageNet-512 at equal compute, in a
  cumulative single-model ladder whose steps are all far larger than FID's
  noise. Post-hoc EMA reconstructs any averaging length from two stored
  power-function averages, and what it shows is that the best length depends
  on architecture, learning rate, guidance weight and the metric — the last
  by 2% against 14% under guidance.
---

<!-- inactive-ok-file: SOTA-tmp9x33t, SOTA-tmpui8n0 — Proposed practices filed from this reading; named as what it produced, not relied on -->
<!-- inactive-ok-file: SOTA-282, SOTA-156, SOTA-408 — Proposed; named in Connections and Bearing as neighbours this paper does not source -->

# NOTE-tmpod74g: EDM2

## Contribution

Two independent contributions on top of EDM ([LIT-075](../literature.d/LIT-075.md)). First, a redesign of
the ADM denoiser that makes every operation preserve the expected magnitude
of activations, and keeps weight norms fixed during optimization so the
effective learning rate is set by the schedule rather than by drift; it is a
drop-in replacement for ADM and sets ImageNet-512 records at a fraction of
the compute. Second, a way to choose the EMA profile after training, which
turns the EMA length from a hyperparameter fixed before a run into a quantity
that can be swept densely and cheaply — and the sweeps are the second half of
the paper.

## Key insight

Training dynamics are unbalanced in ways nobody set on purpose — activations
and weights grow, the effective learning rate decays unequally across
layers, the loss weighting drifts off equal — and each imbalance can be
removed by construction rather than compensated for with normalization. Once
magnitudes are standardized, quantities that used to be accidents (the
residual/main-path blend, the skip/decoder balance, the per-layer learning
rate) become explicit hyperparameters. The EMA half says the same thing about
averaging: the best length is a property of the whole setup, so a length
chosen in advance is always a guess.

## Assumptions

- **One architecture family.** Everything in the ladder is the ADM U-Net
  under the EDM framework. The discussion asks whether it would help RIN or
  DiT and does not try.
- **Image data only.** ImageNet-512 in the latent space of the Stable
  Diffusion VAE (standardized to σ_data = 0.5 by per-channel shift and
  scale), and ImageNet-64 in pixel space. Class-conditional.
- **Magnitude preservation is on expectation, under independence.** The layer
  scalings assume uncorrelated inputs of equal variance. The authors say the
  assumption need not hold exactly because the aim is to cut the link from
  weight to activation magnitude, and add pixel normalization in the encoder
  because correlations violate it.
- **FID protocol.** 50k samples against the full training set; each reported
  figure is **the minimum of three evaluations** of one trained model, with
  run-to-run variation "typically in the order of ±2%". One training run per
  configuration.
- **Deterministic 2nd-order EDM sampler, 32 steps** (63 NFE) throughout.

## Key results

- **Ladder (Table 1, ImageNet-512, ~300M, 2^31 images, no guidance).** A 8.00
  → B 7.24 → C 6.96 → D 3.75 → E 3.02 → F 2.71 → G 2.56. Gflops stay
  100–102 throughout B–G. Each FID is at that config's own best EMA length
  (Fig. 5a), which is the fair comparison and is only affordable with post-hoc
  EMA.
- **Magnitude-preserving learned layer (D).** For output channel `i`,
  `ŵ_i = w_i / ‖w_i‖₂`, gradients through the norm, no learned gain, weights
  initialised `N(0,1)`, learning rate raised to 0.01. Removes activation drift
  (Fig. 3) and makes the weight norm irrelevant to the forward pass.
- **Forced weight normalization (E).** After every step, reset
  `w_i ← √N_j · w_i / ‖w_i‖`; keep the on-use normalization too, so the
  gradient is projected to the tangent plane *before* Adam sees it. Without
  the second normalization Adam's variance estimate includes the normal
  component and the step is "considerably smaller than intended" (Fig. 23).
  With the effective LR now equal to the nominal one, a constant LR no longer
  anneals, so an inverse-square-root decay `α_ref / √max(t/t_ref, 1)` is
  added (Algorithm 1 is the whole implementation).
- **Fixed-function layers (G).** SiLU divided by 0.596; Fourier features
  scaled by √2; residual sums as `((1−t)a + tb)/√((1−t)²+t²)` with **t = 0.3**
  in blocks and 0.5 in the embedding; decoder concatenation rebalanced so the
  skip and main path contribute equally regardless of channel counts; learned
  zero-initialised gains only at the output and on the conditioning. Dropout
  can then be disabled at small sizes; it is re-enabled at M and above,
  which overfit without it (Fig. 12).
- **Records (Table 2).** EDM2-XS…XXL: 3.53 → 1.91 unguided, 2.91 → 1.81
  guided; prior bests 2.99 (VDM++) and 2.41 (StyleGAN-XL). ImageNet-64
  (Table 3): 1.58 (S) and 1.33 (L), vs EDM's 2.22 deterministic.
- **Power-function EMA.** `θ̂_γ(t) = (γ+1)/t^{γ+1} ∫₀ᵗ τ^γ θ(τ) dτ`, updated
  as EMA with `β_γ(t) = (1 − 1/t)^{γ+1}`; reported by relative width
  `σ_rel`, upper-bounded at ≈0.289. Initial weights get zero weight;
  doubling training doubles the profile.
- **Post-hoc reconstruction.** Store `σ_rel` 0.05 and 0.10 averages every
  4096 steps (~8M images) in fp16; solve `Ax = b` with closed-form inner
  products (Algorithm 3). 160–512 snapshots give near-perfect reconstruction
  over `σ_rel ∈ [0.015, 0.25]`; error ~`O(1/n⁴)` in snapshot count.
- **EMA findings.** The optimum differs by config and sharpens B → G (Fig.
  5a); per-tensor sweeps in B improve FID by up to ~10% (7.24 → ~6.5), in G
  nothing does (Fig. 5b); the optimum drifts longer through training (5c);
  it depends "very strongly" on guidance (Fig. 6); with post-hoc EMA, a
  learning-rate decay `t_ref ∈ [30k, 160k]` stays within 10% of the best FID,
  whereas at a fixed 13% EMA the worst case is 72% worse (Fig. 13, A.4).
- **Metric disagreement (A.5, Fig. 14).** Unguided, FID prefers 13% and
  FD_DINOv2 19%; at guidance 1.4, **2% against 14%**, and each metric rates
  the other's optimum as "terrible". FD_DINOv2 also wants guidance 1.9 where
  FID wants 1.4. The improvement B → G holds in both metrics.
- **Guidance with a small model (A.3, Table 4).** An XS unconditional model
  guides XXL as well as larger ones; very short EMAs are typically best when
  sampling with guidance.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Normalizing weights on use (magnitude-preserving learned layers) is the largest single improvement to the ADM U-Net here, 6.96 → 3.75 | strong | Table 1 D; one run, but a 46% change against ±2% evaluation noise, and Fig. 3 shows the mechanism |
| C2 | Forced weight normalization with an explicit LR decay improves further, 3.75 → 3.02 | moderate | Table 1 E; one run; confounded with introducing the inverse-sqrt schedule in the same step |
| C3 | Removing group norms and magnitude-preserving the fixed-function layers adds 3.02 → 2.56 | moderate | Table 1 F, G; each step bundles several changes, and F's gain is partly the pixel norms added back |
| C4 | The learned per-noise-level loss weighting helps | weak | bundled into B with retuned LR, batch, β₂, noise distribution and removed attention; no isolated arm |
| C5 | The design transfers beyond the ADM U-Net | weak | none in the paper — posed as an open question in §5; no DiT or non-image experiment |
| C6 | Post-hoc EMA reconstructs arbitrary power-function profiles accurately from two stored averages | strong | closed-form derivation (App. C) and the measured `O(1/n⁴)` reconstruction error |
| C7 | The optimal EMA length depends on architecture, training time, learning rate and guidance | strong | dense post-hoc sweeps, Figs. 5, 6, 13; shaded min/max over three evaluations |
| C8 | The optimal EMA length depends on the evaluation metric, by up to 7× under guidance | moderate | Fig. 14, one model size (S); FD_DINOv2 evaluated once per point |
| C9 | Optimal EMA scales as `σ_rel ∝ 1/(α_ref² t_ref)`, and shortens with capacity and simpler data | weak | §4, presented by the authors as "anecdotal" and left for future work |
| C10 | A much smaller unconditional model suffices for classifier-free guidance | moderate | Table 4, one conditional model (XXL), ImageNet-512 |
| C11 | The guided/unguided gap in prior work is partly an EMA artefact | weak | a postulate from Fig. 6; no prior model is re-evaluated |

## Method

1. Start from ADM under EDM; retune (batch 2048, LR 2e-4, β₂ 0.99, log-normal
   noise `P_mean = −0.4, P_std = 1.0` for latents) and replace the static loss
   weight with a learned `u(σ)` that divides each noise level's loss by its
   own running value (a continuous Kendall et al. multi-task weighting).
2. Strip biases and learned norm scales; cosine attention.
3. Normalize every weight vector on use; initialise `N(0,1)`.
4. Re-normalize stored weights after every step; inverse-sqrt LR decay.
5. Remove group norms; add pixel norms at encoder-block inputs.
6. Scale every fixed-function op to preserve unit magnitude; blend residuals
   at `t = 0.3`; learned gains only where the loss needs a non-unit scale.
7. Throughout: track two power-function EMAs and snapshot them; choose the EMA
   length per config, per guidance weight and per metric after training.

## Concepts

- **Effective learning rate** — the relative size of an update to a weight
  vector, `‖Δw‖/‖w‖`. Under on-use weight normalization it decays as the
  weights grow, without anybody scheduling it.
- **Forced weight normalization** — renormalizing the stored parameter to a
  fixed norm after each step, as distinct from normalizing on use.
- **EMA length `σ_rel`** — the standard deviation of the averaging profile
  relative to training time; 10% corresponds to `γ ≈ 6.94`.
- **Post-hoc EMA** — synthesizing an averaged model for a profile not tracked
  during training, as a linear combination of stored averages.

## Connections

Extends EDM ([LIT-075](../literature.d/LIT-075.md)): same preconditioning, same sampler, same noise
parameterization; the baseline is EDM's ImageNet-64 recipe transplanted to
latents. It reports that EDM's loss weight, which equalises gradient
magnitudes across noise levels at initialization, stops doing so as training
proceeds — a correction to how [SOTA-188](../practices.d/SOTA-188.md) had described it.

Compared against ADM ([LIT-699](../literature.d/LIT-699.md)), DiT ([LIT-448](../literature.d/LIT-448.md)), simple diffusion / U-ViT
([LIT-660](../literature.d/LIT-660.md)) and VDM++ ([LIT-692](../literature.d/LIT-692.md)) in Tables 2–3, by quoting their published
numbers; only EDM is re-run.

The forced weight normalization is the image-diffusion precursor of the
hypersphere constraint in nGPT ([LIT-472](../literature.d/LIT-472.md), [SOTA-282](../practices.d/SOTA-282.md)), ten months earlier:
both re-project weights after every step and both delete most normalization
layers. Nobody has compared them. The paper places itself in the
weight-normalization lineage (Salimans and Kingma; van Laarhoven; NFNets;
LARS and Fromage as optimizers aiming at the same relative-update effect),
none of which the record holds.

On averaging, it cites SWA ([LIT-673](../literature.d/LIT-673.md)) as model averaging and otherwise treats
EMA of weights as given.

## Recommendations

- **R1** — Choose the EMA length after training from stored power-function
  averages, and re-choose it for each guidance weight and each metric you
  report. *Topic:* training-optimization. *Status:* experimental.
  *Strength:* strong for the mechanism, moderate for the claim that it
  matters outside image diffusion. *Applies when:* the model is evaluated on
  weight averages at all.
- **R2** — In a diffusion U-Net, normalize weights on use and force them back
  to fixed norm after every step, preserve magnitude through every fixed
  operation, and replace data-dependent normalization. *Topic:*
  model-architecture. *Status:* experimental. *Strength:* strong on ADM,
  untested elsewhere. *Applies when:* training an ADM-style denoiser from
  scratch; it requires re-deriving the learning rate (0.01) and adding an
  explicit decay.
- **R3** — Guide a large conditional diffusion model with a much smaller,
  separately trained unconditional one. *Topic:* inference-optimization.
  *Status:* experimental. *Strength:* moderate. *Applies when:* you can afford
  a second training run for the unconditional model.

## Bearing on the record

- **Produces** [SOTA-tmp9x33t](../practices.d/SOTA-tmp9x33t.md) (R1) and [SOTA-tmpui8n0](../practices.d/SOTA-tmpui8n0.md) (R2), both `Proposed`.
  R3 is recorded in [SOTA-424](../practices.d/SOTA-424.md) rather than filed: one table, one model.
- **[SOTA-188](../practices.d/SOTA-188.md)** — not a new source, but one sentence was wrong. The practice
  said the loss weight "cancels `c_out`'s scaling so that every noise level
  contributes equally"; EDM2 shows that holds at initialization and drifts
  after, and replaces it with an adaptive weighting. It also confirms the
  practice's own Conditions: moving to VAE latents moved the useful noise
  region, and `P_mean, P_std` had to be refitted (−0.4, 1.0 against −1.2,
  1.2). [SOTA-188](../practices.d/SOTA-188.md) is edited to say both.
- **[SOTA-424](../practices.d/SOTA-424.md)** — its "capacity question the paper does not answer" is half
  answered here: the unconditional score, at least, needs far less capacity
  than the conditional one. Its "pick the weight by which metric" rule gains
  a second instance (FID 1.4 vs FD_DINOv2 1.9). Edited as prose; not a source,
  because EDM2 does not train one network for both scores, which is what the
  practice recommends.
- **[SOTA-337](../practices.d/SOTA-337.md)** — relevant and not a source. The FID/FD_DINOv2 disagreement
  arises with **no ImageNet classifier anywhere in the pipeline**, from
  tuning EMA and guidance alone, which is outside that practice's stated
  condition. It suggests the condition may be too narrow: tuning a
  hyperparameter against FID is itself a way to fit its feature space. That
  is one figure, and is left here rather than widening the practice.
- **[SOTA-307](../practices.d/SOTA-307.md)** — EDM2 reports the minimum of three evaluations, which is a
  biased estimator, and states ±2% variation, which is that practice's
  threshold. The ladder's steps are far beyond it; the XL/XXL gaps (1.96 vs
  1.91, 1.85 vs 1.81) are at it.
- **[SOTA-408](../practices.d/SOTA-408.md), [SOTA-156](../practices.d/SOTA-156.md)** — the other averaging practices. Neither is sourced
  by this paper; the post-hoc machinery would apply to any averaging profile,
  which the authors say and do not test.
- **A trunk with no document.** No practice here says "sample from an average
  of the weights" at all. EDM2 calls it "indispensable" and has no no-EMA arm,
  so it cannot source one; it is the shape [DP-007](../../docs/design-principles.md#dp-7) describes, and the paper to
  file it from is not in the record.

## Limitations

- One run per configuration; the ladder is cumulative, so each step's gain is
  measured given every step before it, and several steps bundle changes.
- No transfer test to transformer denoisers, text-conditional models, or any
  non-image domain. The authors raise the question themselves.
- The EMA observations beyond Figs. 5, 6, 13 and 14 are explicitly
  "anecdotal".
- FD_DINOv2 disagreement is shown for the S model only.
- The record FIDs are minima over three evaluations.

## Open questions

- Does magnitude preservation with forced weight normalization help a DiT, or
  a language model? A same-backbone comparison against its usual
  normalization at matched compute would settle it — and would also be the
  first comparison against nGPT's hypersphere design.
- Would per-tensor EMA lengths help architectures that, like config B, have
  tensors disagreeing about the optimum?
- Which metric's EMA optimum produces the better images? The authors lean to
  FD_DINOv2 on a "cursory assessment"; a human study would decide it.
