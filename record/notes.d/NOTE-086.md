---
number: 86
status: Read
formerly:
- NOTE-tmpwuo1b
paper: LIT-240
title: 'ESSAM'
version: 1
date: '2026-09-15'
summary: >-
  Transposes sharpness-aware minimization into zeroth order — step against the
  reward-weighted direction, recompute the update at that neighbouring point,
  apply it at the original — and closes most of standard ES's gap to GRPO on
  GSM8K while keeping inference-level GPU memory.
---

# NOTE-086: ESSAM

## Contribution

Shows that ES's weakness on mainstream reasoning benchmarks is a
generalization problem rather than an optimization one, by fixing it with a
generalization technique. SAM normally needs a gradient to locate the
adversarial neighbour; this obtains the direction from the reward-weighted ES
aggregate instead, so the whole method stays forward-pass only and keeps ES's
memory profile.

## Key insight

**The ES aggregate is already a direction estimate, so it can play the role
SAM's gradient plays.** Standard SAM perturbs toward higher loss, recomputes
the gradient there, and applies it at the original point. ESSAM does the same
with the sign flipped for a reward objective: move against the
reward-increasing direction into the neighbourhood, recompute perturbations
and rewards at that point, and use *that* direction to update the original
parameters. The solution is pushed toward regions where reward stays high
across a neighbourhood rather than at a point — which is what plain ES, fitting
a reward estimated from a finite population, tends not to do.

## Assumptions

- **A verifiable scalar reward**; GSM8K accuracy throughout.
- **The flat-minima hypothesis is imported, not tested here** — that flatter
  solutions generalize better is taken from the SAM literature and no
  sharpness measurement of the resulting checkpoints is reported.
- **Two evaluation rounds per iteration**, since the neighbourhood probe needs
  its own population evaluation.
- Memory comparisons assume PPO with a critic and value head, and GRPO with a
  reference model — the standard configurations.

## Key results

- **GSM8K average across Qwen2.5-Instruct at 0.5B, 1.5B, 3B and 7B**: ESSAM
  **78.27%**, standard ES 75.97%, PPO 77.72%, GRPO 78.34%. ESSAM beats PPO on
  average and is a fraction behind GRPO, surpassing both on some individual
  models.
- **The gain over standard ES is 2.3 points**, which is the comparison the
  method is actually about.
- **Memory**: identical footprint to plain ES — inference level — reported as
  a 10–18× reduction against PPO and GRPO. This is the figure [LIT-231](../literature.d/LIT-231.md) cites
  for ES's "10× space-efficiency".
- **Training trends**: ESSAM reported as showing better trends than standard
  ES and higher test accuracy, which the paper reads as improved
  generalization.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | A sharpness-aware step improves ES on GSM8K | strong for this setup | 2.3 points over standard ES across four model scales |
| C2 | ESSAM is comparable to PPO and GRPO | strong | 78.27 vs 77.72 and 78.34; the paper says comparable and means it |
| C3 | ESSAM keeps inference-level memory | strong | structural — forward passes only — and measured |
| C4 | The gain comes from seeking flat regions | weak | no sharpness measured; the mechanism is asserted by analogy to SAM |
| C5 | The gain is not simply the extra evaluations | not established | no ablation separates the SAM step from the doubled evaluation budget |

## Method

Per iteration: generate a population with Gaussian perturbations and compute
reward-weighted aggregation as in standard ES; step the parameters in the
*opposite* direction of reward increase to reach a neighbouring point; at that
point draw fresh perturbations and rewards and form a new update direction;
apply that direction to the original parameters. Full-parameter, zeroth-order,
forward passes only.

## Concepts

- **Sharpness-aware maximization** — the reward-objective form of SAM: prefer
  parameters whose reward is high across a neighbourhood.
- **Neighbourhood probing** — the first of the two stages, and the thing that
  costs the extra evaluations.

## Connections

It positions itself against ES's reported underperformance on GSM8K, cites
zeroth-order SAM work for prompt tuning as the nearest precedent, and inherits
its efficiency framing from the ES-at-scale line. Lineage is on the LIT.

## Recommendations

- **R1** — If ES underperforms on a reasoning benchmark, suspect
  generalization before optimization; the reward estimated from a finite
  population is a thing a method can overfit. *Topic:* post-training.
  *Strength:* moderate.
- **R2** — Where memory is the binding constraint rather than wall clock, ES
  at inference-level footprint is a real option at 7B and below. *Topic:*
  post-training. *Strength:* moderate.
- **R3** — Not filed, and worth stating as a non-recommendation: the two-stage
  update doubles evaluations per iteration, and nobody has checked whether
  spending that budget on more directions would do as well.

## Bearing on the record

Filed as [LIT-240](../literature.d/LIT-240.md), `extends:` [LIT-211](../literature.d/LIT-211.md).

<!-- inactive-ok-block: SOTA-211 is Active... (see note) — Proposed, and named
     as the practice this paper's design points away from -->
**Its most useful role here is as a counterweight to [SOTA-211](../practices.d/SOTA-211.md).** That
practice says do not spend two evaluations on one direction, because the
antithetic pair's second evaluation buys nothing when responses are
regenerated. ESSAM also spends a second round of evaluations — on a
neighbourhood probe rather than an antithetic partner — and gets 2.3 points
for it. The two are not in conflict, and the contrast sharpens the real
question: **not whether to spend more evaluations, but on what.** The record
now holds two answers, and only one of them has been tested against the
other's alternative.

**It is a small, unlooked-for corroboration of the scale pattern.** The paper's
framing is that plain ES overfits its sampled rewards, and its per-model table
is weakest at 0.5B — which is what a low density of task-improving
perturbations looks like from inside a method that is trying to fit them.

## Limitations

Stated: none at length. From this reading: one benchmark; no sharpness
measurement to support the stated mechanism; and no ablation separating the
SAM step from the extra evaluations, which is the first thing a sceptic would
ask and the one thing that would settle C4 and C5.

## Open questions

<!-- inactive-ok-block: SOTA-211 — Proposed, and named as the practice this paper contrasts with rather than supports -->
- **Does the same budget spent on more directions do as well?** The obvious
  control, and the one that connects this paper to [SOTA-211](../practices.d/SOTA-211.md).
- **Are the resulting solutions actually flatter?** Measurable, and unmeasured.
- **Does it survive a second benchmark?** GSM8K alone, four models of one
  family.
