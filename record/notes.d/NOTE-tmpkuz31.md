---
status: Read
paper: LIT-028
title: 'Scaling Laws for Neural Language Models'
version: 1
tags:
- training-optimization
date: '2026-09-09'
summary: >-
  Loss is a power law in model size, dataset size and compute over seven orders of magnitude, and shape barely matters. Its learning-rate finding is the opposite of what the record recorded: larger models require a *smaller* rate to avoid divergence, and the paper carries an explicit LR(N) rule.
---

# NOTE-tmpkuz31: Scaling Laws for Neural Language Models

## Contribution

Established that language-model loss is a **power law** in each of model size,
dataset size and training compute, with trends spanning more than seven orders
of magnitude — and that architectural shape (width, depth) has "minimal
effects within a wide range" once non-embedding parameter count is fixed. From
those laws it derives how to allocate a fixed compute budget, and reaches the
conclusion that reorganised the field: train **very large models and stop well
short of convergence**.

## Key insight

If the loss depends on scale by a simple power law and barely on anything
else, then almost every design question becomes an allocation question. The
paper's own summary of the consequence is that larger models are
**significantly more sample-efficient**, so compute-optimal training means
spending on size rather than on passes over data — with data growing very
slowly, `D ∼ C^0.27`.

The part that aged worst is inseparable from the part that aged best: the
allocation is only as good as the fitting protocol, and Chinchilla later
showed this one held the learning-rate schedule in a way that penalised long
runs.

## Assumptions

- **WebText2**, decoder-only Transformers, Adam (Adafactor above 1B), a fixed
  `2.5×10⁵` steps at batch size 512 × 1024 tokens unless noted.
- **The learning-rate schedule was held fixed** — 3000-step linear warmup then
  cosine decay to zero — across runs of very different length. This is the
  methodological choice Chinchilla identified as the source of the wrong
  exponent.
- Compute is estimated as `C ≈ 6NBS`, excluding terms proportional to
  `n_ctx`, so the scalings "may be confounded" where `n_ctx ≳ 12·d_model`.
- The paper lists its own caveats, including that other hyperparameters
  (initialisation scale, momentum) may matter and were not swept.

## Key results

- **The power laws.** `L(N) = (N_c/N)^α_N` with `α_N ≈ 0.076`;
  `L(D) = (D_c/D)^α_D` with `α_D ≈ 0.095`, `D_c ≈ 5.4×10¹³` tokens;
  `L(C_min) = (C_c/C_min)^α_C` with `α_C ≈ 0.050`.
- **Shape barely matters.** Width, depth, heads and feed-forward ratio have
  minimal effect at fixed non-embedding `N` — the claim `LIT-052` later
  contradicts for *downstream* quality.
- **Compute-optimal allocation** (Eq. 1.7): `N ∝ C^(α_C/α_N)`,
  `B ∝ C^(α_C/α_B)`, `S ∝ C^(α_C/α_S)`, with data growing only as
  `D ∼ C^0.27`.
- **Critical batch size** `B_crit(L) = B*/L^(1/α_B)`, `B* ≈ 2×10⁸` tokens,
  `α_B ≈ 0.21` — depending on the **loss, not directly on model size**, and
  roughly doubling for every 13% decrease in loss.
- **`L(N, S_min)` fit** (Table 3): `α_N = 0.077`, `α_S = 0.76`,
  `N_c = 6.5×10¹³`, `S_c = 2.1×10³`.
- **Larger models are significantly more sample-efficient**, and
  compute-optimal training stops well short of convergence.
- **On learning rates** (Appendix D.6, and the reason this reading matters):
  - the choice of *schedule* is "mostly irrelevant, as long as the total
    summed learning rate is sufficiently large, and the schedule includes a
    warmup period and a final decay to near-vanishing learning rate" —
    measured in Figure 22 on a **3 million parameter model**;
  - **"larger models require a smaller learning rate to prevent divergence,
    while smaller models can tolerate a larger learning rate"**;
  - so they carried an explicit size-dependent rule:
    **`LR(N) ≈ 0.003239 − 0.0001395·log(N)`** (Eq. D.1), which they note
    "breaks down for `N > 10¹⁰` parameters";
  - and separately: "the optimal choice of learning rate **is sensitive to
    the target loss**."

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Loss is a power law in `N`, `D` and `C` over seven orders of magnitude | strong | the paper's central fits |
| C2 | Model shape has minimal effect at fixed parameter count | strong | measured — but on **upstream loss only** |
| C3 | Larger models are significantly more sample-efficient | strong | follows from the fits and is directly measured |
| C4 | Compute-optimal training means very large models stopped short of convergence | moderate | derived from C1 under a fixed schedule; **Chinchilla overturned the exponent** |
| C5 | The learning-rate *schedule* shape is mostly irrelevant given warmup and decay | weak | one scan, on a **3M-parameter** model, with run-to-run noise at 0.05 loss |
| C6 | Larger models need a **smaller** learning rate to avoid divergence | moderate | stated from their experience, with `LR(N)` as the implemented rule |
| C7 | `B_crit` depends on loss, not directly on model size | strong | Figure 10 |

## Concepts

- **`B_crit`, the critical batch size** — the point past which extra
  parallelism stops buying speed. A function of the *loss*, so two models of
  different size at the same loss want the same batch.
- **`C_min` / `S_min`** — compute and steps as they would be at, respectively,
  a batch far below and far above `B_crit`. The normalisation that makes the
  compute trend clean.
- **Sample efficiency** — loss reached per token seen. The quantity C3 is
  about, and distinct from compute efficiency.

## Connections

The paper this record measures everything else against. **Chinchilla**
re-derives C4 and overturns it, finding roughly 20 tokens per parameter.
**`LIT-052`** (*Scale Efficiently*) contradicts C2 by changing the measured
quantity from upstream loss to downstream fine-tuning. **µP** and the
learning-rate-transfer line are the modern answer to what `LR(N)` was
approximating by hand.

## Recommendations

- **R1** — Fit scaling laws before allocating a large budget. *Topic:*
  planning. *Status:* standard. *Strength:* strong. *Applies when:* the budget
  is large enough that the allocation matters more than the details.
- **R2** — Do not hold the learning-rate schedule fixed across runs of
  different length when fitting such laws. *Topic:* methodology. *Status:*
  standard. *Strength:* strong. *Applies when:* always — this is the mistake
  that cost this paper its headline exponent, learned from its correction.
- **R3** — Scale the learning rate **down** with model size. *Topic:*
  training. *Status:* standard. *Strength:* moderate. *Applies when:* no
  principled parameterisation is in use; `LR(N)` is a 2020 rule of thumb that
  breaks above `10¹⁰` parameters, and µP is the modern replacement.
- **R4** — Set batch size from the loss, not the model size. *Topic:*
  training. *Status:* standard. *Strength:* moderate. *Applies when:*
  choosing batch size; C7 says the loss is the right variable.

## Bearing on the record

**One confirmed, one inverted, one already corrected.**

| practice | disposition |
<!-- inactive-ok-block: SOTA-041 — Rejected in this same change; the table and the paragraphs below are the record of why -->
|---|---|
| [SOTA-040](../practices.d/SOTA-040.md) larger models are more sample efficient | confirmed — C3, and its body already flags the Chinchilla correction |
| [SOTA-041](../practices.d/SOTA-041.md) lr tuning less important for larger models | **inverted** |
| [SOTA-097](../practices.d/SOTA-097.md) optimal batch size scales as `C^(1/4)` | confirmed — Eq. 1.7, `α_C/α_B = 0.050/0.21 = 0.24`; re-sourced here from Chinchilla in [#113](https://github.com/dmarx/anthology-of-the-sota/issues/113) |

<!-- inactive-ok-block: SOTA-041 — Rejected in this same change; this paragraph is the evidence -->
**`SOTA-041` states the opposite of its source.** Kaplan says *"larger models
require a smaller learning rate to prevent divergence, while smaller models
can tolerate a larger learning rate"*, and carries an explicit size-dependent
rule, `LR(N) ≈ 0.003239 − 0.0001395·log(N)`, precisely because the right rate
is **not** size-independent. The word `insensitive` does not occur in the
paper.

Two conflations produced it:

1. **Schedule for rate.** What the paper calls mostly irrelevant is the
   *shape* of the decay, given a warmup and a final decay to near zero — not
   the peak rate. C5's evidence is one scan on a **3M-parameter** model.
2. **Direction.** "Less important for larger models" reverses C6. Larger
   models have *less* headroom, not more.

The practice's body reasons that the power-law fits "flatten near the optimum
as model size grows". That is a real idea and it is not in this paper; `flatten`
occurs once, about a different curve.

## Limitations

- C4 is wrong, by the paper's own successor, and the cause was a fixed
  schedule across variable-length runs — a methodological point worth more
  than the exponent.
- C5 rests on a single 3M-parameter scan with run-to-run noise at 0.05 loss,
  and the paper says averaging is needed to see smaller effects.
- `LR(N)` is admitted to break above `10¹⁰` parameters, which is below every
  frontier model in this record.
- C2 holds for upstream loss and fails downstream, per `LIT-052`.

## Open questions

- C5 is the weakest claim in the paper and the most quoted. The record's own
  later practices — WSD, decay-to-zero, the power scheduler — all say the
  schedule *does* matter. Is C5 simply false at scale, or true only in the
  narrow "given warmup and a final decay" sense it states?
- `B_crit` depends on loss rather than size (C7). Almost nothing in the record
  sets batch size that way. Why not?
