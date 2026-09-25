---
number: 366
status: Read
formerly:
- NOTE-tmp700wg
paper: LIT-709
title: 'Primer'
version: 1
date: '2026-09-25'
summary: >-
  Squaring the feed-forward ReLU and adding a causal width-3 depthwise
  convolution after each per-head Q/K/V projection makes decoder-only LMs
  reach a vanilla baseline's quality in 1.75–2.3× less compute at 35M, at
  least 1.8× at 110M and 4.2× at 537M. That last figure is at fixed size, where
  the factor grows with training length. At 1.9B, against a GELU baseline,
  it takes ⅓ of the compute.
  Both changes cost step time and are paid for in the accounting. Squared
  ReLU beats SwiGLU in exactly one figure, at 110M. Against the SwiGLU +
  RMSNorm baseline the saving is about 2×, and it vanishes on
  encoder–decoder masked LM.
---

<!-- inactive-ok-file: SOTA-158 — Proposed; named as the practice squared ReLU's unbounded range is in tension with, not relied on as settled -->

# NOTE-366: Primer

Read in full from arXiv v2 (24 Jan 2022). That covers §§1–5 and Appendix A
in full: the primitives vocabulary, graph construction, halving hurdles,
search details, the program listings (Figs. 13–25, read from their
annotations), the exact LM1B, T5 and one-shot tables (Tables 4–6), the
ablation and insertion study, the training details, the power-law
derivation, masked LM, carbon, the Evolved Transformer comparison and the
practical discussion. Figures 5–11 and 26–27 were read from axes, legends and
captions. Tables 5, 7 and 8 lost their numeric cells in extraction, so for
those the text and captions are the source.

## Contribution

A search space made of TensorFlow primitives, not transformer blocks, run
with regularized evolution. Fitness is LM1B perplexity after a fixed
24-TPUv2-hour budget, so a change that slows each step but saves enough steps
wins. The search found Primer. Insertion and ablation in two codebases reduce
it to two transferable changes, Primer-EZ: squared ReLU and MDHA. These are
then dropped, untuned, into T2T, T5 and Lingvo at 20M–1.9B parameters.

## Key insight

**Judge an architecture change in time-to-quality, not steps or FLOPs.** Both
Primer-EZ changes make a step slower. Both win because the sample-efficiency
gain outruns the step-time cost. The search was built to find exactly that
trade, which its predecessor (Evolved Transformer, sample-efficiency
objective) could not see (App. A.14).

## Assumptions

- Decoder-only autoregressive LM. The encoder–decoder result is a footnote
  that goes the other way (App. A.12).
- Baseline hyperparameters (Adafactor, 10K warmup at 0.01, rsqrt decay,
  regularization off) applied unchanged to Primer (App. A.8).
- "Speedup" is the ratio of accelerator time to reach the vanilla
  baseline's final perplexity. It is hardware- and library-specific, and the
  authors say savings "vary across setups" (App. A.15).
- Fixed-size comparisons (§§4.2–4.4) inflate with training length. The
  compute-optimal comparison (Fig. 7) gives a constant factor.

## Key results

- **Table 4** (LM1B, ~35M, ± over runs). T2T/TPUv2: Primer-EZ 2.34 ± 0.04,
  Primer 2.12, Transformer++ 1.37, +GELU 1.23, **+MDHA only 1.76 ± 0.06**,
  +separable conv 1.54. V100: Primer-EZ 2.03, Transformer++ 1.54. T5/TPUv2:
  Primer-EZ 1.75, Primer 1.72, Transformer++ 1.33, Evolved Transformer 1.23.
- **Fig. 26**: insertion into vanilla and ablation from Primer, in T2T and
  T5. Squared ReLU, MDHA and 12× projection help in all four cells. Shared
  QK hurts. Pre/post norm and the custom norm are mixed.
- **Fig. 5 right** (C4, 110M, T5, 525K steps): squared ReLU gives the lowest
  perplexity of ReLU, GELU, Swish, ReGLU, SwiGLU and squared ReLU.
- **Fig. 7**: the compute-optimal frontiers (23M–385M) are roughly parallel
  in log–log, so the saving is a constant factor there (App. A.9).
- **Fig. 9 / Table 5** (C4, PG19, 110M): Primer and Primer-EZ are ≥ 1.8×
  vanilla at the end of training. Switch + Primer-EZ is 1.5× (0.6 ppl).
  Synthesizer + squared ReLU is 2.0× (0.7 ppl).
- **Table 1** (537M, exact T5 regime): original T5 reaches 13.25 at 15.7K
  TPUv3-h, T5++ at 4.6K and Primer at 3.8K. T5++ reaches 12.69 at 16.5K and
  Primer at 8.3K. Primer reaches 12.35 at 17.3K.
- **Table 6** (1.9B, proprietary data, full Primer against Transformer +
  GELU, 5 checkpoints). At ⅓ compute: 5 tasks better, 1 worse, 21 equal. At
  equal compute: 15 better, 2 worse, 10 equal.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Primer-EZ reaches a vanilla Transformer's quality in substantially less compute for decoder-only LM | strong | Table 4 with run variance across three hardware/library settings. Fig. 9 on two datasets. Table 1 at 537M |
| C2 | It also beats a strong SwiGLU + RMSNorm baseline | moderate | Tables 1 and 4. The margin is 1.2–2× and shrinks at the shorter budget (1.2× at 13.25 in Table 1) |
| C3 | Squared ReLU beats SwiGLU and ReGLU | weak | One bar chart (Fig. 5 right), 110M, one codebase, no variance, parameter matching unstated |
| C4 | MDHA alone gives a large speedup | moderate | Table 4, 1.76× in T2T at 35M, and Fig. 26 in both codebases. Not isolated at larger scale |
| C5 | Depthwise-after-pointwise beats separable, and wider kernels do not help | moderate for the order at 35M (1.76 vs 1.54); weak for width | Table 4. The width result is stated in §3 without a table |
| C6 | Savings grow with compute | strong at fixed size, as the authors caution | Fig. 10. At compute-optimal size the factor is constant (Fig. 7) |
| C7 | Gains transfer to one-shot downstream tasks | moderate | Table 6, 5 checkpoints, t-tests. Against a GELU baseline on proprietary data. No SwiGLU arm at 1.9B |
| C8 | The changes transfer to MoE and Synthesizer | moderate | Fig. 9, one configuration each |
| C9 | The changes help encoder–decoder masked LM | contradicted by its own appendix | App. A.12: Primer-EZ is no better than Transformer++, single runs |

## Method

Regularized evolution (population 100, tournament 10) over DNA programs of
TF primitives. The search is seeded with the Transformer, split into
subprograms ("conceptual initialization"), because 78% of random programs
of that length fail to train. Four halving hurdles and a 7-hour proxy for
24 hours cut the cost 21×. About 25K individuals are evaluated, and the top
100 are retrained to pick the winner. The search cost ~2.14E21 FLOPs.

## Concepts

- **Primer-EZ** — a Transformer with only squared ReLU and MDHA. The authors
  recommend it as the starting point.
- **MDHA** — multi-DConv-head attention: `d_conv(proj(x), width 3, causal)`
  per head, for each of Q, K and V.
- **Transformer++** — RMSNorm plus SwiGLU, the T5-benchmarked strong baseline.
- **Speedup factor** — the fraction of the baseline's full compute a model
  needs to match the baseline's final quality, inverted.

## Connections

The search baselines are the Transformer ([LIT-008](../literature.d/LIT-008.md)) and SwiGLU from GLU
variants ([LIT-030](../literature.d/LIT-030.md)), the latter inside Transformer++ and directly in Fig. 5.
It reruns T5 ([LIT-425](../literature.d/LIT-425.md)) exactly at 537M and grafts Primer-EZ onto Switch
Transformer ([LIT-189](../literature.d/LIT-189.md)). The power-law framing borrows Kaplan et al.
([LIT-028](../literature.d/LIT-028.md)). Depthwise convolutions in transformers precede it
(LightConv, [LIT-020](../literature.d/LIT-020.md)), but not placed after each head's projection.
PowLU ([LIT-200](../literature.d/LIT-200.md)) later objects to SwiGLU on the ground that it behaves like
x² for large inputs. That is squared ReLU's asymptote exactly.

## Recommendations

- **R1.** For decoder-only LM pretraining, try squared ReLU in place of the FFN
  activation. It is cheaper than a GLU (no third matrix) and was better in
  the one direct test. *Topic:* model-architecture. *Status:* experimental.
  *Strength:* weak (C3), though adoption at small scale is wide.
  *Applies when:* decoder-only, ordinary precision.
- **R2.** Add a causal width-3 depthwise convolution after each head's Q, K
  and V projections. *Topic:* attention-techniques. *Status:* experimental.
  *Strength:* moderate at ≤ 537M (C4).
- **R3.** Report architecture comparisons in time-to-target at a named
  training length. Say whether the model is at compute-optimal size, because
  fixed-size speedups grow with the budget. *Topic:*
  analysis-and-evaluation. *Strength:* strong. It is the paper's own caution
  (C6).

## Bearing on the record

| document | disposition |
|---|---|
| [SOTA-034](../practices.d/SOTA-034.md) | **contested on quality, weakly.** Its consensus note said nobody disputes SwiGLU's quality. This paper does, in Fig. 5, at 110M. Added to `contested_by` with a section that sizes the evidence. The recommendation stands: one figure, one scale, confounded with MDHA everywhere else |
| [SOTA-158](../practices.d/SOTA-158.md) | **tension, not edited.** Squared ReLU is unbounded and grows quadratically, which is exactly what the practice says to bound in low precision. Primer never tests narrow formats. Anyone adopting R1 at scale in FP8 is on [SOTA-158](../practices.d/SOTA-158.md)'s ground |
| none | **MDHA has no practice**, and no document in the record holds the short-causal-convolution-before-mixing idea. R2 is a candidate, better evidenced here than R1 |
| [LIT-200](../literature.d/LIT-200.md) | its "SwiGLU ≈ x² for large inputs" diagnosis names the property this paper chose on purpose. The two are not in conflict, because they measure different things: quality at bf16/fp32 against range at low precision |

## Limitations

- Largest model 1.9B, and that run has no SwiGLU baseline. The authors say
  the scale is "orders of magnitude smaller" than the frontier.
- Speedups are wall-clock on TPUs in TensorFlow. The depthwise convolution's
  cost on GPU kernels at long context is not measured beyond one V100 table
  at 35M.
- Short contexts throughout: 64 on LM1B and 512–1024 elsewhere.
- No hyperparameter retuning for either side. The authors present this as
  conservative, and it is. It also means nothing is known about how the
  optimum moves.
- Encoder–decoder: no gain over Transformer++ (App. A.12).

## Open questions

- Does squared ReLU still beat SwiGLU at matched parameters and FLOPs above
  1B, with seeds? That is what would move [SOTA-034](../practices.d/SOTA-034.md).
- Is MDHA's gain the same thing a short causal convolution buys recurrent and
  hybrid layers, namely local token mixing before the global mixer? Does it
  survive RoPE, which Primer did not use?
- Does squared ReLU's quadratic range cause the outlier problems [LIT-200](../literature.d/LIT-200.md)
  reports for SwiGLU once trained in FP8?
