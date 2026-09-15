---
status: Read
paper: LIT-tmp9pcfv
title: 'Hyper-ES'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-15'
summary: >-
  Argues from two lemmas that full-parameter ES cannot work at LLM scale —
  random perturbations concentrate near orthogonality to any useful descent
  direction, and the leftover orthogonal components accumulate as a random
  walk away from the pretrained weights — and replaces the search space with
  the span of a few cheap GRPO-derived LoRA directions, searched by CMA-ES.
---

# NOTE-tmp12jd3: Hyper-ES

## Contribution

The first paper in the ES post-training line to argue that the line's premise
is wrong, and to say why in a form that can be checked. Its positive
contribution is a method, but its durable contribution is the two lemmas: a
concentration argument for why random directions in a billion-dimensional
space are useless, and a random-walk argument for why the useless components
do not cancel.

## Key insight

**ES's problem at LLM scale is not that it cannot measure a reward — it is
that it is measuring the reward of a direction that is almost surely
irrelevant.** In high dimensions the angle between a random vector and any
fixed direction concentrates near 90°, and the population size grows far more
slowly than the ambient dimension, so enlarging the population does not
rescue it. The population still contains members with different rewards —
which is why ES *appears* to be working — but reward differences among
near-orthogonal directions do not mean a useful direction was found. The
update is then assembled mostly out of components orthogonal to anything that
reduces loss, and those accumulate.

The fix follows from stating the problem that way: stop asking ES to
*discover* directions and give it good ones to *combine*.

## Assumptions

- **High dimension with a population far smaller than it** — the concentration
  argument needs `N ≪ d`, which is the LLM regime by an enormous margin.
- **A single "useful" direction `u`** against which orthogonality is measured.
  The lemmas are stated against one descent direction; a useful *subspace*
  would weaken the conclusion and is not considered.
- **Mean-zero cross terms across iterations** for the random-walk result —
  stated explicitly, and it is what makes the orthogonal displacement grow
  like `√T` rather than cancel.
- **The useful component is negligible** — assumed, in the step that makes
  drift dominate. This is the conclusion of Lemma 1 being carried into Lemma 2
  as a premise, which is legitimate but means the two are one argument rather
  than two.
- The method assumes a gradient path exists and is affordable: fewer than ten
  GRPO steps per direction, on separable data subsets.

## Key results

- **Lemma 1 (high-dimensional angles concentrate near orthogonality).** A
  practical ES population is dominated by perturbations whose angle to the
  loss-reducing direction is close to `π/2`. *Holds when:* `N ≪ d` and the
  perturbations are isotropic.
- **Lemma 2 (orthogonal random walk).** With the useful component negligible
  and the orthogonal components having nonzero second moment, the accumulated
  orthogonal displacement after `T` steps grows rather than cancelling — the
  squared norm adds across iterations under the mean-zero cross-term
  assumption. *Holds when:* the cross terms across iterations are mean-zero.
- **Method.** Run fewer than ten GRPO steps on each of several data subsets to
  obtain `M` LoRA deltas as basis directions; apply CMA-ES to **layer-wise
  DARE-TIES merging coefficients** over their span. Search dimension falls to
  a few hundred coefficients.
- **Arithmetic reasoning, Qwen2.5-0.5B-Instruct**: 57.13% average against
  GRPO+LoRA's 56.23%, CMA-ES+LoRA's 52.76%, Average Merge's ~52%, base
  47.88%. On GSM8K, SVAMP, MultiArith and GSM-Hard.
- **Qwen2.5-1.5B-Instruct**: 74.26% average against GRPO+LoRA's 73.51% and
  Average Merge's 72.36%.
- **Budget**: direction generation consumes 17,920 samples for Qwen2.5-Instruct
  and 12,544 for DeepSeek-R1-Distill, against roughly 20,000 and 14,000 for
  the GRPO/CMA-ES baseline — the "10% fewer gradient updates" claim.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Random perturbations in a billion-dimensional space are near-orthogonal to any fixed useful direction | strong | Lemma 1; a standard concentration fact, correctly applied |
| C2 | Orthogonal components accumulate as random-walk drift rather than cancelling | moderate | Lemma 2, under an assumed mean-zero cross-term condition |
| C3 | Therefore full-parameter ES is ineffective at LLM scale | weak | the inference C1 + C2 → C3 assumes a single useful direction and no useful subspace; the paper never runs full-parameter ES at the scale it is arguing about |
| C4 | Searching a span of gradient-derived directions beats GRPO-LoRA | moderate | ~1 point on two model scales, four benchmarks; consistent, small |
| C5 | Hyper-ES is a gradient-free method | not claimed, and false | it is gradient-seeded; the saving is 10% fewer backpropagation steps, not none |

## Method

Three stages. (1) Partition the training data — by reasoning-hop count for
GSM8K-Aug, by category for DeepScaleR — and run `<10` GRPO steps at batch size
256 on each subset from a shared base, producing `M` LoRA deltas (`M = 7` for
Qwen2.5-Instruct, `M = 5` for DeepSeek-R1-Distill). (2) Treat the deltas as
basis directions. (3) Run CMA-ES over layer-wise DARE-TIES merging
coefficients, a few hundred parameters, to find the best combination.

## Concepts

- **Descent direction merging** — the paper's framing: adaptation as choosing
  coefficients over a basis of cheap gradient-derived deltas.
- **DARE-TIES** — the model-merging scheme whose coefficients are the search
  variables; layer-wise rather than global weighting is what the paper claims
  over uniform merging.

## Connections

It cites Qiu et al., Sarkar et al. and Sun et al. as the ES-for-LLM line it is
responding to, and takes the catastrophic-forgetting reports of Hoy et al. and
Abdi et al. as corroboration of its drift argument. It is worth noting that
[LIT-tmp81or2](../literature.d/LIT-tmp81or2.md) measures that same drift, agrees it is 40× GRPO's, and
reaches the opposite conclusion about what it implies. Lineage is on the LIT.

## Recommendations

- **R1** — If your ES budget is small and you can afford a few gradient steps,
  spend them on constructing a basis rather than on the final update.
  *Topic:* post-training. *Status:* experimental. *Strength:* moderate.
  *Applies when:* the data partitions into subsets that produce meaningfully
  different deltas.
- **R2** — Weight a model merge layer-wise rather than uniformly, and search
  the weights. *Topic:* adaptation. *Strength:* moderate. This is where the
  paper's largest margin is — against Average Merge, not against GRPO.
- **R3** — Do not read a spread of rewards across an ES population as evidence
  that the search is finding useful directions. *Topic:* post-training.
  *Strength:* moderate, and it is the most transferable thing here.

## Bearing on the record

Filed as [LIT-tmp9pcfv](../literature.d/LIT-tmp9pcfv.md), `corrects:` [LIT-211](../literature.d/LIT-211.md), and it is the
`contested_by:` on [SOTA-154](../practices.d/SOTA-154.md) — the document that makes that practice's
consensus `contested` rather than merely unreplicated.

The full reading sharpens rather than softens what the LIT note already said.
**C3 is the weak link and it is weak for a specific reason:** Lemma 1 is about
the angle to *a* fixed direction, and [LIT-tmp81or2](../literature.d/LIT-tmp81or2.md) reports that ES's gains
concentrate in a sparse subset of coordinates — LayerNorm weights and
attention projections — which is a useful *subspace*, and a random direction's
projection onto a subspace of dimension `k` behaves very differently from its
projection onto a line. Two papers, four months apart, measuring the same
geometry and drawing opposite conclusions from it.

<!-- inactive-ok-block: THEORY-tmp38myz — Proposed, and this section is the
     record's own reconciliation; naming the account is the point -->
And the scale reading stands: every model here is at 1.5B or below, which is
where [THEORY-tmp38myz](../theory.d/THEORY-tmp38myz.md) says the density of task-improving perturbations has
not yet arrived. Lemma 1 is a formal statement of the needle-in-a-haystack
regime, and the dispute may be about which regime each group was measuring in.

## Limitations

The paper states none at length. From this reading: it never runs the method
it declares ineffective; its ES baseline is CMA-ES over LoRA; its margin over
GRPO-LoRA is about one point; it compares against a parameter-efficient
baseline rather than full fine-tuning GRPO; and the strongest evidence it
offers for its own construction is against merging baselines rather than
against RL.

## Open questions

- **Does Lemma 1 survive a subspace formulation?** What would close it: the
  same concentration argument stated against a `k`-dimensional useful
  subspace, with `k` estimated from the sparse coordinate set
  [LIT-tmp81or2](../literature.d/LIT-tmp81or2.md) identifies.
- **Does the argument have a scale at which it stops applying?** Both lemmas
  are dimension-asymptotic and would, read naively, get *worse* with scale —
  while the empirical line reports ES getting *better*. Something in the
  argument does not track the observation, and neither paper says what.
- **Does the method beat full-parameter ES above 1.5B?** Never tested, and it
  is the comparison the paper's own thesis calls for.
