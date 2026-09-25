---
status: Read
paper: LIT-tmptr16a
title: 'MDLM'
version: 1
date: '2026-09-25'
summary: >-
  Masked diffusion's ELBO is a schedule-weighted average of masked-LM losses,
  and with a modern recipe it is the best discrete diffusion language model at
  110M parameters. It does not beat autoregression in-domain, even with the
  AR baseline given half the optimizer steps; the paper's own checklist names
  that as its limitation.
---

<!-- inactive-ok-file: SOTA-157 — Proposed, and named as the practice this reading adds a corroborating source to, and corrects on what that source does and does not show -->
<!-- inactive-ok-file: SOTA-254 — Proposed, and named to say this reading does NOT source it -->

# NOTE-tmpiht70: MDLM

## Contribution

Before this, masked discrete diffusion for language was known through D3PM's
general framework, which needed full transition matrices, a numerically
fragile objective and continuous-time Markov chain theory to extend, and
which published at 76.90 perplexity on LM1B. MDLM shows that the masked
special case has a closed, simple continuous-time ELBO — a weighted average
of BERT's loss — and that a modern training recipe takes the same model
family to 27.04 at 33B tokens and 23.00 at 327B. What is true afterwards:
masked diffusion is a serious language model family, the objective to train
it with is known, and the gap to autoregression is a bounded, measured
number rather than a factor of three.

## Key insight

Two properties of the masking process, built into the network's output —
the mask token is never predicted, and an unmasked token is copied through —
set most terms of the diffusion KL to zero analytically. What is left is
cross-entropy on the masked positions, weighted by `α'_t/(1−α_t)`. After a
change of variables, the schedule drops out of the bound. So a masked
diffusion language model is a BERT trained over a *distribution* of masking
rates with the right weights. Sampling it ancestrally makes it a generator,
and the reweighting is what turns it from a heuristic into a likelihood
model.

## Assumptions

- **Absorbing-state forward process only.** The simplifications (SUBS,
  Rao-Blackwellization) depend on it; the paper states that focusing on
  masking is what makes them possible.
- **The reverse process factorizes independently across tokens** given the
  current latent sequence: `p_θ(z_s^{1:L} | z_t^{1:L}) = Π_ℓ p_θ(z_s^ℓ | z_t^{1:L})`.
  This is the property [LIT-479](../literature.d/LIT-479.md) later identifies as why masked models cannot
  revise a token once emitted.
- `α_t` strictly decreasing in `t`, `α_0 ≈ 1`, `α_1 ≈ 0`.
- Experiments at 110M parameters (DiT backbone with RoPE, from SEDD),
  context 128 on LM1B and 1024 on OWT; DNA at ~467K parameters on a Mamba
  backbone.
- **"Matched tokens" counts masked tokens only** (Suppl. D.2): the AR
  baseline gets half the optimizer steps, so MDLM sees twice the raw tokens.
  Constant LR 3e-4, no sweep, for all arms.

## Key results

- **Continuous-time NELBO** (eq. 10/11): `L = E_q ∫₀¹ α'_t/(1−α_t) Σ_ℓ log⟨x_θ^ℓ(z_t, t), x^ℓ⟩ dt`.
  Invariant to the form of `α_t` (Suppl. E.1.1); four schedules give 3.30 BPD
  on OWT, per-datapoint variance 1.81 (log-linear) to 7.57 (linear).
- **LM1B (Table 1)**: MDLM ≤27.04 (33B tokens), ≤23.00 (327B); SEDD ≤32.79
  (33B); AR retrained 22.32 (33B), 20.86 (327B).
- **OWT (Table 2)**: AR 17.54, SEDD ≤24.10, MDLM ≤23.21.
- **Zero-shot from OWT (Table 3)**: MDLM beats SEDD on 7/7 and AR on 3/7
  (Lambada 47.52 vs 51.28, Pubmed 41.89 vs 49.01, Arxiv 37.37 vs 41.73); AR
  wins PTB 82.05 vs 95.26, Wikitext 25.75 vs 32.83, LM1B 51.25 vs 67.01, AG
  News 52.09 vs 61.15. The table caption says "524B tokens" where Table 2 and
  Suppl. D.2 say 262B for the same 1M steps — the first counts raw tokens, the
  second masked ones.
- **Ablation (Table 8, LM1B)**: 27.04 full; 27.19 discrete-time T=1000; 28.56
  without carry-over; 28.51 without zero-masking (≡ D3PM's objective).
- **Time conditioning** does not matter (OWT 23.21 with, 23.05 without), which
  enables the caching sampler: 2× wall-clock at T=10k (60.4 vs 127.9 min).
- **Discrete T at evaluation**: 42.18 at T=10, 25.77 at 50, 23.15 at 1000,
  23.05 at ∞.
- **BERT → generator**: 327M tokens of MDLM fine-tuning take C4 PPL bound 78 →
  35, GLUE average 81.62 → 82.06 (AR 74.88, AR PPL 22).
- **Semi-AR decoding**: Gen PPL 27.18 vs SSD-LM 35.43 at 2048 tokens,
  ~25–30× faster.
- **DNA (Tables 6–7)**: MDLM ≤3.199 vs SEDD ≤3.216, Plaid ≤3.240; AR Mamba
  3.067. Genomic Benchmarks: diffusion fine-tuning roughly preserves MLM
  pretraining accuracy.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The masked-diffusion continuous-time NELBO is a schedule-weighted average of masked-LM cross-entropies | strong | derivation, §3.3–3.5, Suppl. B |
| C2 | The continuous-time bound is invariant to the noise schedule; only its variance depends on it | strong | change of variables, Suppl. E.1.1; Table 9 |
| C3 | MDLM is the best discrete diffusion LM at this scale, beating SEDD at matched training | strong | Tables 1–3, 6; retrained SEDD, same backbone and data |
| C4 | Most of the improvement over published D3PM comes from the training recipe, not the derivation | moderate | Table 8 plus §6's own statement; the D3PM baseline is also a smaller model (70M) |
| C5 | Masked diffusion approaches AR perplexity ("within 15–25%") | moderate | Tables 1–2; true, but with AR given half the steps and no sweep for either arm |
| C6 | Diffusion may be more robust out of domain | weak | 3/7 zero-shot wins; stated as a hypothesis |
| C7 | A pretrained BERT can be made generative by MDLM fine-tuning without losing GLUE performance | moderate | Table 4; one model, one run |
| C8 | Time conditioning is unnecessary, enabling a 2× caching speed-up | moderate | Tables 10, 12 |

## Method

Absorbing-state diffusion with the SUBS parameterization (mask logit set to
`−∞`; unmasked positions copied); continuous-time training of eq. 11 with a
log-linear schedule and a low-discrepancy (stratified) sampler for `t`;
ancestral sampling with caching when the network ignores `t`; semi-AR
generation by re-using the last `L − L'` tokens as a clamped prefix.

## Concepts

- **SUBS** — the substitution parameterization: zero masking probabilities
  plus carry-over unmasking.
- **Rao-Blackwellization** — the authors' term, "somewhat abusing" it, for
  analytically zeroing expectations the parameterization makes deterministic.
- **Tokens seen** — for diffusion, the expected number of *masked* tokens, `½`
  of the raw count under a log-linear schedule.

## Connections

A strict special case of D3PM's framework, derived variationally; Shi et
al. and Ou et al. reached the same objective concurrently (Ou et al. from
score matching). It borrows SEDD's backbone, schedule and data processing,
and beats SEDD. It extracts the concrete score SEDD learns (Suppl. C.3), so
score-based samplers apply. [LIT-479](../literature.d/LIT-479.md), from the same lab, builds its
uniform-state model on this codebase and measures against it.

## Recommendations

- **R1** — If training a discrete diffusion language model, use the absorbing
  (mask) process with the SUBS objective. *Topic:* generative modeling.
  *Status:* standard. *Strength:* strong. *Applies when:* the choice is among
  discrete diffusion processes, at likelihood.
- **R2** — Use a log-linear schedule and stratified `t` sampling; they change
  variance, not the bound. *Status:* standard. *Strength:* moderate.
- **R3** — Drop time conditioning and cache the denoiser across steps where
  nothing unmasks. *Status:* standard. *Strength:* moderate.
- **R4** — Report diffusion-versus-AR comparisons with the step count and
  raw-token count of each arm, not "tokens seen". *Topic:* analysis and
  evaluation. *Strength:* moderate. *Applies when:* any masked-objective
  comparison.

## Bearing on the record

- [SOTA-157](../practices.d/SOTA-157.md) — **corroborates the "masked" and not the "rather than
  autoregressively".** LLaDA ([LIT-217](../literature.d/LIT-217.md)) trains with this objective, and MDLM
  plus SEDD are the evidence that the masking process is the right discrete
  corruption. On diffusion versus AR, this is the controlled comparison from
  a second group that the practice's `promote_when:` asks for — though with
  the AR arm given half the steps and no sweep, so it does not meet that
  bar — and it goes the other way at 110M: AR wins in-domain by 10–32% in perplexity. Added
  as a corroborating source, and the practice now says which half it supports.
- [SOTA-254](../practices.d/SOTA-254.md) — not a source. Nothing varies the unique-token count.
  The LM1B gap narrowing from 4.7 to 2.1 points between 33B and 327B tokens
  is in the direction that practice predicts; it is not a test of it. The
  practice's statement that inference cost is "not accounted anywhere" is now
  slightly too strong: this paper and SEDD report wall-clock sampling numbers,
  though at matched sample quality and not at matched total cost.
- [LIT-479](../literature.d/LIT-479.md) — compared against this paper; the relation is declared there.

## Limitations

- The authors: *"Our method under-performs compared to autoregressive
  models."*
- 110M parameters; no scaling curve over model size.
- The AR arm's step budget is half of MDLM's; neither arm was tuned.
- Perplexities are upper bounds, evaluated with a single Monte Carlo sample
  of `t` per sequence and a low-discrepancy sampler.
- Generative perplexity for samples is reported without the numerical
  precision of sampling, which later work found matters for masked models.
- The zero-shot out-of-domain advantage is hypothesised, not explained.

## Open questions

- Does the in-domain AR gap close, persist or reverse with scale at matched
  optimizer steps rather than matched masked tokens?
- Is the out-of-domain advantage real robustness or an artefact of
  bound-versus-exact evaluation differing by dataset?
