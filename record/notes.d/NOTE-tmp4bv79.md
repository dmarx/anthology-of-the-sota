---
status: Read
paper: LIT-tmpfb0m4
title: 'SEDD'
version: 1
date: '2026-09-25'
summary: >-
  Score entropy makes the ratio view of discrete diffusion trainable and
  gives it a likelihood bound; with it, absorbing-state diffusion reaches a
  near-tie with a retrained autoregressive model on LM1B. "Beats GPT-2" is 3
  of 5 zero-shot sets against a model trained on different data. The
  controlled result that lasts is that masking beats uniform corruption on
  every table.
---

<!-- inactive-ok-file: SOTA-157 — Proposed, and named as the practice this reading adds a corroborating source to, for one comparison only -->
<!-- inactive-ok-file: SOTA-254 — Proposed, and named for the inference-cost figure this paper reports, not as a practice it sources -->

# NOTE-tmp4bv79: SEDD

## Contribution

Discrete diffusion had three ways to learn its reverse process — mean
prediction (D3PM), ratio matching and concrete score matching — and none was
competitive on language. SEDD adds a fourth, score entropy, which learns the
ratios `p_t(y)/p_t(x)` directly with a loss that respects their positivity,
has a denoising form that trains at about AR cost, and bounds the likelihood.
Afterwards, a discrete diffusion model is within one perplexity point of a
same-size retrained transformer on LM1B, and beats D3PM and Plaid by wide
margins at matched architecture.

## Key insight

The discrete analogue of the score is the vector of probability ratios to
Hamming-distance-1 neighbours. Score matching's ℓ2 loss is the wrong
divergence for positive quantities, and the Bregman divergence of `−log`
fixes it: its gradient is the ℓ2 gradient rescaled by `1/s`, a log barrier.
Because the model learns ratios, conditioning on any subset of positions is
Bayes' rule on the same network, and infilling needs no retraining.

## Assumptions

- Forward process a CTMC `dp_t/dt = Q_t p_t` with `Q_t = σ(t) Q` and tokens
  perturbed independently (eq. 11, 13). Only two `Q` are tractable at
  GPT-2 vocabulary size: uniform and absorbing.
- Consistency (Prop. 3.2) needs full support and `w_xy > 0`, infinite data
  and capacity.
- Tweedie τ-leaping is optimal only among τ-leaping rules (independent
  simultaneous token updates) and only if the scores are exact (Thm. 4.2).
- GPT-2-small/medium-sized DiT with RoPE, ~5–10% more parameters than GPT-2
  from time conditioning; batch 512, LR 3e-4, EMA 0.9999; no hyperparameter
  or architecture search (C.4); OWT training length not reported.

## Key results

- **Score entropy** (Def. 3.1): `L_SE = E_x Σ_{y≠x} w_xy (s_θ(x)_y − (p(y)/p(x)) log s_θ(x)_y + K(p(y)/p(x)))`,
  `K(a) = a(log a − 1)`. Denoising form (Thm 3.4) and ELBO
  `−log p_0^θ(x_0) ≤ L_DWDSE(x_0) + D_KL(p_{T|0}(·|x_0) ‖ p_base)` (Thm 3.6).
- **text8 (Table 2)**: SEDD Absorb ≤1.39 BPC, Uniform ≤1.47, D3PM Absorb
  ≤1.45; AR 1.23.
- **LM1B (Table 3)**: Absorb ≤32.79, Uniform ≤40.25, DiffusionBert ≤63.78,
  D3PM Absorb ≤77.50; retrained AR 31.98.
- **GPT-2 zero-shot (Table 1)**: small — Absorb beats GPT-2 on WikiText2,
  PTB, WikiText103, loses LAMBADA (50.92 vs 45.04) and 1BW (79.29 vs 75.20);
  medium — same pattern. Absorb beats Uniform, Plaid and D3PM everywhere.
- **Concrete score matching ablation** (D.1): 3–4× higher loss.
- **Generation (Fig. 1)**: un-annealed Gen PPL matches GPT-2 at 32× fewer
  steps than 2048, 6–8× better at 2048; log-linear steps–quality frontier for
  Absorb, not for Uniform (Fig. 2, App. D.2).
- **Conditional (Table 5)**: MAUVE 0.957 standard prompting, 0.942 infill;
  GPT-2 nucleus-0.95 0.955, un-annealed 0.802.
- **Cost (§6)**: matches AR inference time at ~100 steps in unoptimized code;
  4–6× larger batch without a KV cache.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Score entropy recovers the true ratios and bounds the likelihood | strong | Prop. 3.2, Thm. 3.4, Thm. 3.6, proofs in App. A |
| C2 | Absorbing (mask) corruption beats uniform for language | strong | every table, same architecture and recipe |
| C3 | SEDD beats prior diffusion LMs by large margins | strong | Tables 1–3; Plaid and D3PM retrained with matched specifications on GPT-2 tasks |
| C4 | SEDD is competitive with autoregressive models on perplexity | moderate | LM1B: bound ≤32.79 against exact 31.98 with a retrained AR |
| C5 | SEDD beats GPT-2 | weak | 3/5 sets at each size; different training corpus, training length unreported, GPT-2 re-scored by a changed protocol |
| C6 | SEDD generates better un-annealed samples than GPT-2 at far fewer steps | moderate | Fig. 1; un-annealed baseline, GPT-2 Large as judge, sampling precision not reported |
| C7 | Score entropy is needed; concrete score matching does not train | moderate | App. D.1, one ablation |

## Method

Denoising score entropy weighted by the forward rates (eq. 10), with
log-linear or geometric total-noise schedules; the network output is
exponentiated for positivity and, for absorbing, scaled by `e^σ − 1`.
Sampling by Euler or Tweedie τ-leaping; conditioning by clamping the
prompted positions.

## Concepts

- **Concrete score** — the vector `[p_t(y)/p_t(x)]_{y≠x}`, the discrete
  analogue of `∇ log p_t` (Meng et al.).
- **Score entropy** — the Bregman divergence of `−log`, generalizing
  cross-entropy to positive, unnormalized values.
- **Tweedie τ-leaping** — a τ-leaping step using the learned ratios to
  approximate the optimal denoiser.
- **Annealing** — temperature, nucleus, thresholding; SEDD is compared
  without it.

## Connections

Generalizes Meng et al.'s concrete score matching; its implicit form
coincides with Campbell et al.'s CTMC loss, and the ELBO follows Benton et
al. MDLM ([LIT-tmptr16a](../literature.d/LIT-tmptr16a.md)) re-derives SEDD's ELBO explicitly (its Suppl. C.2,
noting SEDD cites rather than derives it), shows the masked-diffusion score can
be extracted from a mean-prediction model, and beats SEDD at matched training
on every likelihood table. [LIT-479](../literature.d/LIT-479.md) measures SEDD Uniform and SEDD Absorb as
baselines.

## Recommendations

- **R1** — Among discrete diffusion processes for language, use absorbing
  (mask) corruption. *Topic:* generative modeling. *Status:* standard.
  *Strength:* strong. *Applies when:* optimizing likelihood or many-step
  sample quality.
- **R2** — Compare diffusion and AR generations both annealed and un-annealed,
  with the judge model named. *Topic:* analysis and evaluation. *Strength:*
  moderate.

## Bearing on the record

- [SOTA-157](../practices.d/SOTA-157.md) — a corroborating source for **absorbing over uniform**, which
  is what "masked" in the practice's title asserts and which [LIT-217](../literature.d/LIT-217.md) does not
  test. Not a source for preferring diffusion to autoregression: the
  controlled LM1B comparison is a bound against an exact value and the AR
  side is lower, and the GPT-2 comparison holds neither data nor training
  length fixed. That line in the practice is now explicit.
- [SOTA-254](../practices.d/SOTA-254.md) — not a source. Its section on inference cost gains one
  data point from §6: parity with AR wall-clock at about 100 steps, in
  unoptimized code, at batch sizes where the KV cache is the constraint.
- [LIT-479](../literature.d/LIT-479.md) — compared against this paper, SEDD Uniform and SEDD Absorb both;
  declared there. MDLM declares its own comparison.

## Limitations

- No hyperparameter search; models ≤ GPT-2 medium; OWT training budget not
  given.
- The GPT-2 baseline differs in training data and was re-scored without a
  sliding window; 1BW was not recomputed.
- Sampling numerical precision not reported, so the Gen PPL advantage is
  open to the low-precision artefact [LIT-479](../literature.d/LIT-479.md) guards against.
- Uniform diffusion was not given its own schedule tuning, so "absorb beats
  uniform" is at the absorbing-favoured log-linear setting as much as it is a
  property of the processes. [LIT-479](../literature.d/LIT-479.md)'s later uniform-state results (Duo
  29.9/25.2 against SEDD Uniform 40.3/29.7) show how much of that gap was
  recipe — and that masked diffusion still leads after it (MDLM 27.0/23.2).

## Open questions

- Does the near-tie with AR on LM1B survive with the AR arm tuned and at
  larger scale? MDLM's retrained comparison at the same size says no.
- How much of the absorbing–uniform gap is intrinsic? [LIT-479](../literature.d/LIT-479.md)'s regime split
  (uniform wins below ~32 steps) says the answer depends on the step budget.
