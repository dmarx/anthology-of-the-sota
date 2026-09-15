---
status: Read
paper: LIT-tmpfjaya
title: 'The Blessing of Dimensionality in LLM Fine-tuning'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
summary: >-
  One geometric property — a fine-tuning landscape whose curvature lives in a
  few stiff directions amid a near-zero bulk — accounts for both why a
  population of thirty keeps working as models grow and why the training
  reward rises, peaks and decays under fixed hyperparameters, in GRPO as well
  as ES.
---

# NOTE-tmpp5iw8: The Blessing of Dimensionality in LLM Fine-tuning

## Contribution

Takes two facts that nobody had connected — small populations work at billion
scale, and training rewards are non-monotonic under fixed hyperparameters —
and derives both from one property of the landscape. The unification is the
contribution; either half alone would be a smaller paper, and the fact that a
geometric claim invented to explain sample efficiency also predicts a
training-curve shape in a *different optimizer* is what makes it worth
believing.

## Key insight

**Ambient dimension is the wrong denominator.** Classical zeroth-order
pessimism assumes improvement lies along essentially one direction, whose
probability mass under isotropic sampling vanishes as `d` grows. If instead
improvement depends only on a perturbation's projection onto a `k`-dimensional
curvature-active subspace, then every useful projection has a `(d−k)`-
dimensional preimage: **many ambient perturbations are the same perturbation
as far as the objective is concerned.** What governs random search is the mass
of the improvement-supporting set in `k` dimensions, and `d` drops out. The
paper's picture is a wheel of fortune rather than a needle in a haystack — and
the empirical prediction is sharp, because a real curse of dimensionality
would show up as the best-of-`N` knee sliding right with scale.

The second half follows from the same spectrum. Stiff modes relax fast and
pay out early; flat modes relax slowly and accumulate variance. Under fixed
stochasticity the reward rises while the stiff modes are paying, peaks when
they are exhausted, and then falls as the variance keeps filling the bulk.
**Rushing downhill before the valley floods.**

## Assumptions

- **A local quadratic approximation** around a near-optimal region, with
  constant step size and effective noise. The rise-then-decay analysis is
  local and says nothing about the global landscape.
- **A "bulk plus outliers" curvature spectrum**, imported from the
  overparameterized-network literature rather than measured here.
- **Isotropic Gaussian perturbations**, and — for the accessibility argument —
  that improvement is "primarily determined by" the projection onto the
  curvature-active subspace.
- **Headroom normalization** for the cross-scale comparison, since absolute
  gains necessarily shrink as a model's remaining room does.
- **A viable `σ` chosen per model.** The claim is that *some* sufficiently
  small scale works at every size, not that one scale does.
- Qwen2.5-Instruct only, 0.5B–7B, on GSM8K, ARC-C and WinoGrande.

## Key results

- **Best-of-`N` flattens beyond `N ≈ 30–40` on every task, with no systematic
  rightward shift as model size increases** across 0.5B–7B. This is the
  headline and it is a well-chosen non-result.
- **The flattening is not pool exhaustion.** With the candidate pool far
  larger than `N`, it reflects intrinsic diminishing returns of expected
  extrema — increasing `N` buys rarer tail events, not systematically larger
  gains.
- **A viable range of small `σ` keeps headroom-normalized improvement positive
  from 0.5B to 7B** at fixed `N = 30`. The requirement is locality, not precise
  tuning.
- **Rise-then-decay in ES at multiple population sizes**, with peak time and
  decay depth both varying systematically with stochasticity — which is what
  rules out overfitting or evaluation noise as the explanation.
- **Rise-then-decay in GRPO too**, on Qwen2.5-1.5B-Instruct, GSM8K, same 100
  training samples. Noisier, and present.
- **The quadratic model.** Diagonalizing the curvature decouples the dynamics
  into modes with per-mode contraction factors; a two-block spectrum (a few
  stiff directions, many near-flat) reproduces rise-then-decay in both
  simulation and closed form. **Larger `N` — smaller effective noise — raises
  the terminal plateau and suppresses late-time degradation.**
- **The degeneracy construction.** For a `k`-dimensional curvature-active
  subspace, the preimage of any fixed useful projection is an affine subspace
  of dimension `d − k`; accessibility depends only on geometry in the
  projected space.
- **Three named interventions**: early stopping near the peak; noise
  scheduling (raise `N`, cut `σ`, cut temperature, or otherwise reduce update
  noise over time); adaptive step sizes that shrink once curvature-active
  progress saturates.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Improving directions are degenerate — many ambient perturbations share a useful projection | moderate | a clean construction given the premise; the premise is the part not measured |
| C2 | Population requirements do not grow with model size | strong | best-of-`N` curves across three tasks and an order of magnitude of scale, with the artifact ruled out |
| C3 | A viable local `σ` persists across scales | strong | measured at fixed `N = 30`, headroom-normalized |
| C4 | Rise-then-decay is variance-driven, not overfitting | strong | peak time and decay depth both track stochasticity systematically |
| C5 | Rise-then-decay is not specific to ES | moderate | GRPO runs described as noisier and qualitatively similar; motivating evidence, not a study |
| C6 | Fine-tuning landscapes are low-dimensional in curvature | moderate | inferred from C1–C5; no spectrum computed |
| C7 | Spectral heterogeneity is what transformers actually have | not established | the toy model shows sufficiency, and the paper says so |
| C8 | Larger populations suppress late-time degradation | strong in the toy model, moderate in practice | analytic and simulated; the LLM runs vary `N` and show the peak/decay moving |

## Method

Use ES as a *geometric probe* rather than as an optimizer: Gaussian smoothing
gives a coarse-grained view of the landscape and the population size gives
controllable stochasticity, so sweeping `N` and `σ` reads out landscape
structure. Operationally, accessibility is measured by best-of-`N` improvement
over sampled perturbations, normalized by remaining headroom, swept across
`N`, `σ`, task and model size. The dynamics claim is supported by a local
quadratic stochastic-ascent model, diagonalized into independent modes, with a
two-block spectrum as the minimal example.

## Concepts

- **Low-dimensional in curvature** — what matters is not the parameter count
  but how many directions are meaningfully curvature-active, and that this
  count does not scale with model size.
- **Degeneracy** — the many-to-one map from ambient perturbations to their
  projections on the curvature-active subspace.
- **Accessibility** — the probability mass of the improvement-supporting set
  under the sampling distribution; the quantity that decides whether random
  search works.
- **Water-filling** — variance accumulating in flat directions as a rising
  level that progressively caps attainable performance.
- **Rise-then-decay as a diagnostic** — its presence indicates heterogeneous
  curvature and a variance-dominated late regime; its absence, under
  comparable stochasticity, suggests either little heterogeneity or variance
  already controlled.

## Connections

It sits against the classical zeroth-order literature it is arguing with, the
intrinsic-dimension and parameter-efficient fine-tuning line (which it reads
as evidence for the same low-dimensional structure), and the Hessian-spectrum
literature it borrows "bulk plus outliers" from. Downstream, [LIT-233](../literature.d/LIT-233.md) cites it
and builds a reconciliation on it. Lineage is on the LIT.

## Recommendations

<!-- inactive-ok-block: SOTA-tmpdcmgg — Proposed, and named as where this recommendation landed -->
- **R1** — Treat non-monotonic training reward as a diagnostic of
  heterogeneous curvature, not as a bug or as overfitting. *Topic:*
  post-training. *Strength:* moderate, and the most transferable idea here.
- **R2** — Stop near the peak of the target reward under fixed hyperparameters;
  the decay afterwards is variance, not learning. *Topic:* post-training.
  *Strength:* moderate. Filed into [SOTA-tmpdcmgg](../practices.d/SOTA-tmpdcmgg.md).
- **R3** — Schedule the noise down rather than leaving it fixed: raise `N`,
  cut `σ`, cut temperature over time. *Strength:* moderate, and untested end
  to end here.
- **R4** — Keep perturbations local. A viable `σ` exists at every scale tested
  and the requirement is locality rather than precise tuning. *Strength:*
  strong.
- **R5** — Do not size the ES population from the parameter count. It does not
  need to grow. *Strength:* strong.

## Bearing on the record

<!-- inactive-ok-block: THEORY-tmp4rcxw — Proposed, filed from this reading in this same change -->
Filed as [LIT-tmpfjaya](../literature.d/LIT-tmpfjaya.md) and [THEORY-tmp4rcxw](../theory.d/THEORY-tmp4rcxw.md).

<!-- inactive-ok-block: THEORY-006 — Proposed, and this paragraph is about the
     relation between the two accounts, which is what the citation is for -->
**It is the account [THEORY-006](../theory.d/THEORY-006.md) was built on top of, and the record filed them
in the wrong order.** [LIT-233](../literature.d/LIT-233.md) cites this paper and offers the
reconciliation in its own words: the thicket is "the intersection of (a) a
broad loss basin induced by pretraining and overparameterization, and (b) a
set of task-relevant directions that are effectively low-dimensional (or
low-rank) but embedded within the full parameter space". So the two accounts
are complementary by the later paper's construction — one about the basin, one
about the directions in it — and not the rivals they would look like filed
side by side without this note.

<!-- inactive-ok-block: THEORY-006 — Proposed, and this paragraph is the
     record of the disagreement between the two accounts -->
**They still disagree about scale, and it is a methodological disagreement
worth keeping open.** [THEORY-006](../theory.d/THEORY-006.md) measures the fraction of perturbations
improving by a margin at a *fixed* `σ = 1e-3` and finds it rising from 0% at
0.5B to 64% at 32B. This measures best-of-`N` accessibility with `σ` chosen
per model and headroom-normalized, and finds it flat from 0.5B to 7B. Those
are different quantities, and a `σ` that suits a 32B model need not suit a
0.5B one — which would produce exactly this pattern with no disagreement about
the underlying geometry at all. Nobody has run one protocol measuring both.

**It also bears on the scale-boundary table** in [SOTA-154](../practices.d/SOTA-154.md). That table reads
every negative ES result at ≤1.5B as evidence for a threshold. This paper
reports improvement accessible at 0.5B with a small enough `σ`, which is a
competing reading of the same region: not that the density is too low, but
that the perturbation scale was wrong. The table now says so.

## Limitations

Stated: the analysis is local; the toy model isolates rather than models. From
this reading: the curvature structure the paper is named for is never measured
— the Hessian spectrum is schematic and everything reported is a downstream
consequence; the GRPO rise-then-decay is motivating evidence rather than a
study; one model family; and three of seven authors are authors on
[LIT-211](../literature.d/LIT-211.md), so this is the ES-at-scale line explaining its own result.

## Open questions

- **What is `k`?** The whole account turns on the curvature-active dimension
  being small and scale-independent, and it is never measured. A Gauss-Newton
  or Hessian spectrum of a real fine-tuning landscape at two scales would
  settle it, and is what this account's promotion condition asks for.
- **Does the flat accessibility survive past 7B?** [LIT-233](../literature.d/LIT-233.md) measures a
  related quantity to 32B and finds it rising. One protocol, both metrics,
  0.5B to 32B, is the experiment the record wants.
- **Does noise scheduling actually work end to end?** Proposed in the
  discussion, derived from the toy model, and not run.
