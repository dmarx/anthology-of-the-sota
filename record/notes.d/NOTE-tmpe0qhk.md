---
status: Read
paper: LIT-099
title: 'PaLM 2 Technical Report'
version: 1
tags:
- training-optimization
date: '2026-09-09'
summary: >-
  Independently re-derives compute-optimal scaling at larger compute than Chinchilla and lands on the same answer — grow data and parameters roughly 1:1, against the earlier 3:1 model-first trend. States the inference-economics corollary plainly: for a fixed training and inference budget, train a smaller model on more tokens rather than making the architecture inference-efficient.
---

# NOTE-tmpe0qhk: PaLM 2 Technical Report

## Contribution

A model report, and for this record its value is one section. **Section 2
derives scaling laws independently, at larger compute than Hoffmann et al.,
and reproduces their conclusion**: data and parameters should grow "roughly
1:1", against the previous trend of scaling the model about **3× faster than
the dataset**.

Independent replication at greater scale is the strongest evidence a scaling
claim can get, and it is what makes this more than a product announcement.

## Key insight

The report draws the inference-economics conclusion the scaling result implies
and most papers leave implicit:

> we find that it is more beneficial to invest more compute in training a
> smaller model compared to modifying a model's architecture to be more
> inference-efficient. In effect, we find that it is generally more efficient
> to train a smaller model with more tokens, for a fixed inference and
> training budget.

That is a claim about **where to spend engineering effort**, not just about
allocation: over-training a smaller model dominates architectural
inference-efficiency work under a joint budget. It is the sharpest statement
of that trade in the corpus, and it comes from a group that had the option to
do either.

They also name the data mixture as decisive: translation pairs were a *minor*
part of the mixture and were enough to put the model on par with production
translation services.

## Assumptions

- **The scaling study is separate from the shipped models.** The report says
  explicitly that Section 2's model sizes and FLOPs "do not reflect the model
  sizes and FLOPs used in PaLM 2 models". So the scaling conclusion is
  transferable; the model's own configuration is undisclosed.
- Parameter counts, token counts, mixture proportions and architecture are all
  withheld — this is a report, not a reproducible recipe.
- "Roughly 1:1" is a fit, with the usual sensitivity of such fits.

## Key results

- **Independent 1:1 confirmation at larger compute** than Hoffmann et al.
  (Section 2.1), plus downstream-metric scaling analysis (2.2) — the
  under-appreciated half, since 1:1 is derived on loss and the question is
  whether it holds for what people measure.
- **Train smaller, train longer, for a fixed *inference* budget too** — the
  quotation above.
- **A varied objective and architecture improvements mattered**, but less than
  the mixture; the report ranks them.
- **Memorization is measured with injected canaries**: an *interleave* canary
  (two pre-training documents interleaved in batches of N = 50 tokens,
  preserving some linguistic structure) and a *shuffle* canary (one real
  document with all tokens shuffled). Designed as a middle ground between
  fully random outliers and minimally edited real text.
- Multilingual results throughout, including C2-level language proficiency
  exams taken under simulated conditions with third-party raters.
- Bias and toxicity are disaggregated by language: toxic-response rates range
  0–3.5% in the best case and 1–17.9% in the worst across English, German and
  Portuguese; 91.4% on disambiguated BBQ with 3% of disambiguated questions
  still producing a representational harm.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Data and parameters should scale ~1:1 | strong | independent derivation at larger compute than the original |
| C2 | Over-training a smaller model beats architectural inference-efficiency work under a joint budget | moderate | stated as a finding; the supporting comparison is not shown |
| C3 | Data mixture dominates architecture for final quality | moderate | ranked qualitatively; translation is the given instance |
| C4 | Canary design can span the outlier/realistic spectrum | strong | the two constructions, and the reasoning for them |
| C5 | Toxicity and bias vary substantially by language | strong | measured and disaggregated |

## Method

For the part that matters here: fit scaling laws on a separate family of
models across compute budgets; check the fit against downstream metrics as well
as loss. For memorization: inject interleave and shuffle canaries at controlled
rates per language bin, keeping totals low enough not to affect downstream
performance.

## Concepts

- **Independent replication of a scaling law** — rare, and the reason this
  section is worth more than its length.
- **Joint training-and-inference budget** — the frame that makes C2 a
  decision rather than a preference.
- **Canaries between random and real** — a memorization-measurement design
  that does not choose between detectability and realism.

## Connections

The third point on the allocation arc the record now carries end to end:
`LIT-028` and `LIT-040` (sub-linear, 2020) → Chinchilla (1:1, 2022) → **this
(1:1 independently, at larger compute, 2023)**. `LIT-040` is where the
sub-linear conclusion is derived; this is where the correction is confirmed by
a different group.

<!-- inactive-ok-block: SOTA-160 — Proposed, named as the practice this claim bears on rather than relied on -->
C2 speaks directly to `SOTA-160` (treat the pretraining token budget and the
post-training quantization plan as one decision) — same shape of argument,
different lever, and neither cites the other.

## Recommendations

- **R1** — Scale data and parameters roughly 1:1. *Topic:* training
  optimization. *Strength:* strong, and this is the confirming instance rather
  than the originating one.
- **R2** — Under a joint training-and-inference budget, over-train a smaller
  model before reaching for inference-efficient architecture. *Strength:*
  moderate, and the more actionable claim.
- **R3** — Check that a scaling law derived on loss holds on the downstream
  metric you actually care about. *Topic:* analysis and evaluation.
  *Strength:* strong.
- **R4** — Measure memorization with canaries designed along the
  realism/detectability axis, not only random strings. *Strength:* moderate.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice**,
because the record already sources the 1:1 allocation to Chinchilla, which is
correct — this is the confirmation, not the origin.

The reading's value is completing a chain. The record held the corrected
answer without holding either the superseded one it replaced (now `LIT-040`)
or the independent confirmation that settled it (here). A reader asking "how
confident should I be in 1:1?" now has all three documents and can see that the
answer changed once and then held under replication at greater scale.

<!-- inactive-ok-block: SOTA-160 — Proposed, named as the practice this claim bears on rather than relied on -->
R2 is the loose end worth naming: it is a live claim about where to spend
effort, it bears on `SOTA-160`, and neither the report nor the record shows the
comparison behind it.

The document's takeaways — "architecture improvements", "training efficiency
gains", "scaling strategy updates", "evaluation methodology" — could describe
any model report ever written. It was also tagged `model-architecture`, which
is the one thing this report deliberately does not disclose; retagged
`training-optimization`.

## Limitations

- Sizes, token counts and mixture proportions are all withheld. Nothing here
  is reproducible.
- C2, the most actionable claim, is asserted without the supporting comparison.
- The scaling study uses models unrelated to the shipped ones, so its
  applicability to PaLM 2 itself is asserted.
- Benchmark results are a 2023 snapshot and have no value now; the scaling
  section and the canary design are what survive.

## Open questions

- What exactly does C2 trade off? "More compute on a smaller model" versus
  "inference-efficient architecture" is a comparison with numbers behind it
  somewhere, and they are not in the report.
- The downstream-metric scaling analysis (2.2) is the part everyone needs and
  nobody replicates: does a loss-derived 1:1 hold for capability metrics with
  thresholds and discontinuities?
