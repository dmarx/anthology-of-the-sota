---
status: Read
paper: LIT-tmp2udh1
title: 'Pre-training under infinite compute'
version: 1
date: '2026-09-19'
summary: >-
  Under a fixed 200M-token corpus and no compute limit, the standard recipe
  overfits; tuning weight decay to ~30x the customary 0.1 makes loss monotone
  in parameter count. Ensembling independently trained models then beats
  parameter scaling on asymptote, and distils back down at ~83% retention.
---

# NOTE-tmpc6v83: Pre-training under infinite compute
<!-- inactive-ok-file: SOTA-124 — Proposed, and named among the positions this reading says are measured at one setting of a variable -->
<!-- inactive-ok-file: SOTA-173 — Proposed, and named as the position this reaches independently and fixes more cheaply -->

## Contribution

Takes the limit the field is heading into — data fixed, compute unbounded —
and shows that the recipe everyone would reach for there fails, for a reason
that is fixable with a hyperparameter nobody tunes. It then establishes that
ensembling independently seeded models has a *lower loss asymptote* than
scaling a single model, which is a claim about the limit rather than about
any budget, and shows the ensemble distils into a single small model without
losing most of the benefit. Along the way it proposes evaluating scaling
recipes by their asymptote rather than at a chosen budget, which is a
methodological claim separable from the empirical ones.

## Key insight

**The number of epochs a corpus survives is not a property of the corpus; it
is a property of how hard you are regularizing.** The field's default weight
decay, 0.1, is an inherited constant from a compute-constrained,
data-abundant recipe where it was never load-bearing. Move to the opposite
regime and it becomes the thing that decides whether adding parameters helps
or hurts — at roughly 30x that value the loss curve stops turning up and
becomes a clean power law in parameter count, with a *steeper* exponent than
Chinchilla's. Every argument in the record about how many times a corpus may
be repeated has been conducted at one point in a hyperparameter space that
turns out to control the answer.

## Assumptions

- **200M seed tokens** for the main study, with 4 token counts swept for the
  data-scaling laws. All of it is small relative to frontier pretraining, and
  the largest single model is 1.4B.
- **The scaling laws are power laws with an asymptote**, `L(N) = A/N^α + E`,
  and every headline number is `E` — an extrapolated limit, not a measured
  loss. The composed result takes two such limits in sequence.
- Hyperparameters are "locally optimal" from coordinate descent: no single
  change to weight decay, learning rate or epoch count improves the model.
  That is weaker than a global optimum and the authors say so.
- **Ensemble members differ only in seed** (data order and initialization);
  the architecture and data are identical.
- Validation loss is the objective throughout, with downstream benchmarks
  checked afterwards rather than optimized for.

## Key results

- **Optimal weight decay is ~30x the standard 0.1** for the most
  over-parameterized models under data constraint. *Holds when:* the
  parameter-to-token ratio exceeds Chinchilla's, which is the whole regime
  under study.
- **The regularized recipe is a power law in parameter count** with exponent
  ≈0.23 and asymptote `E ≈ 3.43`, against Chinchilla's parameter exponent of
  ≈0.34 — so better use of the data buys *faster* returns to size, not
  slower.
- **Ensembling beats parameter scaling in the limit**: asymptote ≈3.34 as
  members `K → ∞` at fixed size, against ≈3.43 as `N → ∞`. Two 300M models
  beat one 600M. Even `K = 4` beats the parameter-scaling asymptote.
- **Ensemble members want different hyperparameters than a lone model** —
  more epochs, less weight decay each. Tuning for the `K → ∞` limit rather
  than for `K = 1` moves the asymptote from 3.34 to 3.17.
- **The two compose**: taking `K → ∞` and then `N → ∞` gives ≈3.13, against
  3.43 regularized and 3.75 unregularized.
- **Data efficiency**: the regularized recipe is ~2.29x and the joint recipe
  ~5.17x more data efficient than the standard one at 200M tokens. Fitted
  data-scaling laws across four token counts have similar exponents and
  asymptotes, implying a roughly constant multiple at all scales.
- **Distillation retains it**: an 8-member ensemble into a 300M student keeps
  ~83% of the gain and beats the parameter-scaling asymptote outright.
  Self-distillation at identical size and architecture also improves on its
  own teacher.
- **Downstream**: +9% average on PIQA, SciQ and ARC-Easy over the best
  unregularized model; on continued pretraining over MegaMath-Web-Pro, the
  ensembling recipe on 4B tokens beats default CPT on the full 73B.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Under data constraint the optimal weight decay is far above standard practice, and with it loss becomes monotone in parameter count | strong | coordinate-descent sweep at each parameter count, §3, with the resulting power-law fit |
| C2 | Ensembling independently seeded models achieves a lower loss asymptote than scaling one model | moderate | power-law fits in `K` at four parameter counts; the comparison is between two extrapolated limits |
| C3 | Ensemble members should be tuned for the many-member limit, not as single models | moderate | the hyperparameter ranking demonstrably reorders with `K`, §4.2 |
| C4 | The data-efficiency multiple persists at higher token counts | weak | four token counts, all ≤ a few hundred million, extrapolated by a fitted data-scaling law the authors call noisy |
| C5 | An ensemble's gain survives distillation into a single small model | moderate | one 8→1 distillation at 300M, ~83% retention |
| C6 | A monotone scaling recipe should be judged by its asymptote | moderate | argued rather than measured; it is the paper's evaluation protocol, and every comparison above depends on it |

## Method

Fix a 200M-token corpus. For each parameter count, run coordinate descent
over weight decay, learning rate and epoch count until no single-coordinate
change improves validation loss; this gives the *regularized recipe*. Fit
`L(N) = A/N^α + E` to the resulting losses and read `E` as the recipe's best
possible performance.

For the *ensembling recipe*, train `K` models identical except for seed and
average their logits. Fit `L(K) = A/K^α + E` and read the asymptote the same
way. Tune the members' hyperparameters against that asymptote rather than
against `K = 1` loss.

Compose by taking `K → ∞` at each fixed `N`, then fitting a second power law
over those asymptotes in `N`. Repeat the whole procedure at four seed-token
counts to get data-scaling laws, then interpolate to express each recipe's
advantage as an equivalent multiple of data.

## Concepts

- **Asymptote `E`** — the fitted limit of a scaling law as its variable goes
  to infinity. Used here as the figure of merit for a recipe, in place of
  loss at a compute budget.
- **Monotone scaling recipe** — one whose loss decreases in its scaling
  variable without turning up. The standard recipe is not monotone in
  parameter count under data constraint; that non-monotonicity is what
  regularization fixes and what makes the asymptote well defined.
- **Data efficiency improvement** — how much data the baseline recipe would
  need to match this recipe's loss, as a multiple, read off the fitted
  data-scaling laws.
- **Ensembling algorithm** — `K` independent training runs differing only in
  seed, logits averaged at inference. Total parameter count counted as `K·N`
  for comparison against a single model.

## Connections

Extends [LIT-166](../literature.d/LIT-166.md)'s data-constrained framing by attacking the failure mode
that work documented rather than its scaling law. Where [LIT-166](../literature.d/LIT-166.md) measured how
far repetition goes before returns diminish, this asks why it stops and
answers "under-regularization", which is an answer [LIT-166](../literature.d/LIT-166.md)'s sweep could not
have found because weight decay was not among its swept variables.

The ensembling explanation borrows Allen-Zhu and Li's multi-view account: the
data admits several sufficient feature sets, a single model is biased toward
learning one, and independently trained members happen to pick up different
ones. That also explains why members benefit from being individually *more*
overfit.

Distillation here is doing a different job than in the inference-efficiency
literature: not compressing a large model for serving, but recovering an
ensemble's data efficiency in one model. Self-distillation improving on its
own teacher at identical size is the strongest form of that observation.

## Recommendations

- **R1** — When pretraining over a fixed corpus with parameters beyond
  Chinchilla-optimal, tune weight decay upward rather than inheriting 0.1;
  the optimum found here is around 30x that. *Topic:* regularization.
  *Status:* experimental. *Strength:* moderate. *Applies when:*
  parameter-to-token ratio above Chinchilla and multiple epochs.
- **R2** — Spend surplus compute on an ensemble of independently seeded
  models rather than on one larger model, then distil the ensemble.
  *Topic:* budget allocation. *Status:* experimental. *Strength:* moderate.
  *Applies when:* data-constrained, and the inference cost is recoverable by
  distillation.
- **R3** — Tune ensemble members for the ensemble, not as standalone models:
  more epochs, less weight decay each. *Topic:* ensembling. *Status:*
  experimental. *Strength:* moderate. *Applies when:* the ensemble is large
  enough that the ranking has reordered.
- **R4** — Evaluate a monotone scaling recipe by its fitted asymptote rather
  than at a chosen compute budget. *Topic:* evaluation. *Status:*
  experimental. *Strength:* moderate. *Applies when:* compute is not the
  binding constraint and the recipe's loss is monotone in its scaling
  variable.

## Bearing on the record

- **Should produce practices** for R1 and R2. R4 is a claim about how to
  measure and belongs with the record's evaluation material rather than with
  its training advice.
- **Bears on [SOTA-171](../practices.d/SOTA-171.md), [SOTA-173](../practices.d/SOTA-173.md) and [SOTA-124](../practices.d/SOTA-124.md) jointly**, by naming a
  variable none of them controls for. All three argue about how far a corpus
  may be repeated; this says the answer moves with weight decay, and the
  three sources between them report one setting of it.
- **Complicates nothing about [SOTA-001](../practices.d/SOTA-001.md)** and the decoupled-decay line: the
  claim is about the *value*, in a regime AdamW's defaults were never chosen
  for, not about the mechanism.
- **Sits against the record's uniform assumption that one scales a single
  model.** No practice here recommends an ensemble; that is now a gap rather
  than a settled question.

## Limitations

- Every headline is an extrapolated asymptote, and the best one is an
  asymptote of asymptotes. The sensitivity analysis covers seed variance in
  the fits, not error in the double limit.
- 200M tokens and ≤1.4B parameters. Frontier pretraining is four to five
  orders of magnitude away on both axes, and the claim that the multiple
  holds there rests on four fitted points the authors themselves call noisy.
- "30x" is one number from one corpus at one set of parameter counts; the
  paper gives no rule for predicting it, so a practitioner still has to
  sweep.
- Ensembling is compared at matched *total parameters*, not at matched
  wall-clock or matched engineering effort. `K` independent runs is a
  different operational proposition from one run.
- No frontier-scale artifact exists trained this way, here or elsewhere in
  the record.

## Open questions

- Does the optimal weight decay have a predictable form in the
  parameter-to-token ratio? That would turn R1 from a sweep into a rule.
- Does ensemble scaling still beat parameter scaling once the members are
  large enough to be individually under-parameterized for the corpus? The
  crossing point is not measured.
- How much of the ensembling gain is multi-view and how much is variance
  reduction? Varying only the data order or only the initialization gets most
  of the benefit either way, which the multi-view account does not obviously
  predict.
