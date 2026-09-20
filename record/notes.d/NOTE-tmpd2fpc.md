---
status: Read
paper: LIT-tmp5xe2h
title: 'Diffusion Beats AR in Data-Constrained Settings'
version: 1
date: '2026-09-19'
summary: >-
  Refits [LIT-166](../literature.d/LIT-166.md)'s data-constrained scaling law with the objective swapped
  from autoregressive to masked diffusion. The half-life of data reuse `R*`
  goes from 31.93 to 512.85. Diffusion loses badly at Chinchilla-optimal
  compute and wins past a crossover given in closed form.
---

# NOTE-tmpd2fpc: Diffusion Beats AR in Data-Constrained Settings
<!-- inactive-ok-file: SOTA-124 — Proposed, and named to say this result does NOT bear on it -->
<!-- inactive-ok-file: SOTA-157 — Proposed, and the practice this reading should produce a specialization of -->
<!-- inactive-ok-file: SOTA-173 — Proposed, and the practice this reading tests from outside its own source -->

## Contribution

Establishes that the much-quoted "diffusion language models need 16x the
compute of autoregressive ones" is a statement about the *single-epoch*
regime and does not survive into the data-constrained one. By running both
objectives over the same corpus at matched compute across epoch counts up to
800, it separates compute efficiency from data efficiency — which every prior
comparison had conflated — and finds the two orderings go opposite ways. It
also fits the first data-constrained scaling law for masked diffusion, in
[LIT-166](../literature.d/LIT-166.md)'s parametric form, so the two families' reuse constants are
directly comparable numbers rather than impressions.

## Key insight

**Repeating a corpus is only wasteful relative to the objective you repeat it
under.** Autoregressive training commits to one factorization, so the *n*-th
pass over a document presents very nearly the prediction problem the first
pass did. Masked diffusion samples a new masking pattern each time, so the
*n*-th pass is a different problem drawn from the same document. The
consequence is that "how many epochs is too many" is not a property of the
data at all — it is a property of how much fresh prediction problem the
objective can manufacture from a fixed corpus, and that quantity differs by
sixteen times between the two families.

## Assumptions

- **Fixed unique-token budget, unbounded epochs.** The whole setting. Results
  say nothing about the single-epoch regime except that AR wins it.
- **Matched everything but the objective**: same C4 English corpus, GPT-2 BPE,
  2048-token sequences, Chinchilla-style joint width/depth scaling, and
  [LIT-166](../literature.d/LIT-166.md)'s hyperparameter configuration including its epoch-adaptive
  learning-rate schedule. Attention masking and input corruption are the only
  deliberate differences.
- **The scaling law inherits [LIT-166](../literature.d/LIT-166.md)'s form**, including the assumption that
  the utility of a token on its `k`-th repetition decays geometrically as
  `exp(-(k-1)/R*)`. `R*` is only meaningful under that assumed shape.
- **Fitted unique-token regimes are 25M, 50M and 100M.** The 500M run is a
  single extrapolation check, not part of the fit.
- No instruction tuning, no RL, no downstream adaptation — pretraining loss
  and zero-shot benchmarks only.

## Key results

- **`R*` (half-life of data reuse)** — 512.85 for masked diffusion, 31.93 for
  autoregressive. *Holds when:* fitted over the three unique-token regimes
  above with the geometric-decay form assumed.
- **Crossover in the 100M-unique-token regime** — at the single-epoch
  compute-optimal point, validation loss 10.65 (diffusion) vs 7.07 (AR); at
  each family's best multi-epoch configuration, 3.55 (diffusion, ~500 epochs)
  vs 3.71 (AR, ~50 epochs). AR's curve turns up past its optimum; diffusion's
  does not turn up anywhere inside the budget.
- **Critical compute threshold** — the FLOPs at which diffusion matches AR
  follows a power law in unique-token count, given in closed form. *Holds
  when:* read as an extrapolation from three fitted regimes.
- **Repetition tracks fresh data** for about 4 epochs (AR) and about 100
  epochs (diffusion) before the curves separate from the all-unique-data
  ideal.
- **Downstream results follow validation loss** on the reported benchmark
  suite, in both the 100M and 500M unique-token regimes.
- **Negative result (Appendix 7)** — adding random token masking and
  attention dropout to the AR arm does not close the gap; AR still overfits
  quickly and still trails diffusion trained past 500 epochs.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Masked diffusion extracts useful signal from repeated data over far more epochs than autoregressive training | strong | `R*` fit across three unique-token regimes, hundreds of models, plus the contour sweep in §4.1 |
| C2 | Diffusion's reported compute disadvantage is an artifact of single-epoch evaluation | strong | the crossover is measured directly at matched compute in §4.1 |
| C3 | The compute at which diffusion overtakes AR is predictable in closed form from the unique-token count | moderate | power-law fit over three regimes, all under 100M unique tokens; one 500M check |
| C4 | The mechanism is implicit data augmentation from varied token orderings | weak | an interpretation; the direct test (masking + dropout on the AR arm) does not reproduce the benefit |
| C5 | Diffusion does not overfit repeated data at all | weak | true within this compute budget, and the authors say observing it may simply require more compute |

## Method

Two training arms over one corpus. The autoregressive arm is standard causal
next-token prediction. The diffusion arm is masked diffusion: sample a
masking rate, mask that fraction of tokens, predict them from the rest,
optimizing the usual likelihood lower bound. Beyond the attention mask and
the input corruption every other variable is held fixed.

The sweep varies three factors independently — unique data (25M/50M/100M),
parameter count (7M–2.5B) and epoch count (up to 800) — which is what lets
data reuse be separated from model scaling. Validation loss is reported at
each configuration **without early stopping**, so the overfitting is visible
rather than hidden by a stopping rule.

Scaling laws are then fit in [LIT-166](../literature.d/LIT-166.md)'s parametric form, yielding `R*` and the
optimal-model-size constant per family, and the critical-compute frontier is
derived by setting the two fitted losses equal.

## Concepts

- **`R*`, half-life of data reuse** — [LIT-166](../literature.d/LIT-166.md)'s learned constant: the epoch
  count past which additional repetition yields significantly diminished
  returns, under an assumed geometric decay of per-repetition utility.
- **Effective unique data** — the sum of geometrically decayed per-epoch
  contributions, used in place of raw token count in the scaling law.
- **Critical compute** — the training FLOPs at which the fitted diffusion and
  AR losses are equal, for a given unique-token count. Positive excess favors
  AR, negative favors diffusion.
- **Data-constrained setting** — as used here, a *fixed* unique corpus with
  repetition as the only way to spend more compute. Not the same as "not
  enough data for Chinchilla".

## Connections

Extends [LIT-166](../literature.d/LIT-166.md) in the most direct sense available: the same law, the same
corpus, the same recipe, one variable changed. It stands to the masked
diffusion language-model line — [LIT-217](../literature.d/LIT-217.md) and its descendants — as an argument
for *when* that line is worth taking, which those papers do not supply,
having compared on capability rather than on data efficiency.

It also touches the vision literature's long-standing use of multi-epoch
training with aggressive augmentation, which the authors invoke as the
contrast case: vision has always repeated data and always augmented, and
language modeling adopted neither habit because single-epoch training on web
text made both unnecessary.

## Recommendations

- **R1** — When the unique corpus is fixed and compute is not the binding
  constraint, train a masked diffusion model rather than an autoregressive
  one. *Topic:* objective choice. *Status:* experimental. *Strength:*
  moderate. *Applies when:* past the critical-compute threshold for your
  unique-token count; below it the recommendation reverses.
- **R2** — Do not read single-epoch compute comparisons as data-efficiency
  comparisons. *Topic:* evaluation. *Status:* standard. *Strength:* strong.
  *Applies when:* comparing any two objectives under a fixed corpus.
- **R3** — When training diffusion under data constraints, spend added
  compute on epochs rather than on parameters much further than AR practice
  would suggest: the best configurations here sit at ~500 epochs.
  *Topic:* budget allocation. *Status:* experimental. *Strength:* moderate.
  *Applies when:* the corpus is small enough that 500 epochs is affordable.

## Bearing on the record

- **Should produce a practice** for R1. The record holds [SOTA-157](../practices.d/SOTA-157.md) (train as
  masked diffusion from the start) as `Proposed` for want of a reason to
  prefer it; this is a conditional reason with a stated boundary.
- **Confirms [SOTA-171](../practices.d/SOTA-171.md)'s number and relocates it.** The four-epoch bound is
  reproduced here for AR — and is shown to be a fact about the autoregressive
  objective rather than about repetition.
- **Tests [SOTA-173](../practices.d/SOTA-173.md) and does not confirm it.** Two of that practice's three
  augmentation families, applied to the AR arm in exactly the setting it
  describes, do not close the gap. The practice claims delay rather than
  removal and so is not refuted, but this is the first evidence in the record
  bearing on it from outside its own source.
- **Does not bear on [SOTA-124](../practices.d/SOTA-124.md)**, which is about a single high-quality source
  inside a mixture, not a whole corpus.

## Limitations

- The largest model is 2.3B and it did not converge; the fitted law comes
  entirely from regimes at or below 100M unique tokens. Nothing establishes
  that the crossover survives at frontier corpus sizes, which is where the
  data constraint is actually arriving.
- "No overfitting" is bounded by the compute spent. The authors say so.
- The implicit-augmentation mechanism is asserted and then, in the one place
  it is tested, not reproduced by explicit augmentation of the AR arm. That
  leaves the *why* open even though the *whether* is well measured.
- Inference cost is not accounted anywhere. A masked diffusion model that
  wins on training data efficiency still pays per-token sampling costs the AR
  model does not, and no comparison here is at matched serving cost.
- C4 English only, one tokenizer, one architecture family.

## Open questions

- Does the crossover hold at 10B+ unique tokens? A single fitted law at a
  fourth regime an order of magnitude up would settle whether the exponent is
  real or local.
- Is the advantage really orderings? An AR arm trained with *full* permutation
  augmentation — not masking and dropout, but genuine factorization
  randomization — would test C4 as stated rather than a weakened version.
- What does the crossover look like at matched *total* cost including
  inference? That is the number a practitioner actually spends.
