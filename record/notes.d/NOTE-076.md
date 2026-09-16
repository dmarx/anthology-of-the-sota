---
number: 76
status: Read
formerly:
- NOTE-tmpaf2ab
paper: LIT-230
title: 'Understanding Evolution Strategies for LLM Reasoning'
version: 1
date: '2026-09-15'
summary: >-
  Three questions about what ES post-training does rather than whether it
  wins: it raises pass@1 and pass@k together where GRPO trades one for the
  other, its 40x larger parameter drift is functionally sparse and does not
  produce broad forgetting, and the population size needed for stable training
  falls as the model grows.
---

# NOTE-076: Understanding Evolution Strategies for LLM Reasoning

## Contribution

Turns the ES-versus-GRPO question from a leaderboard into a characterization.
Three things nobody had established: that the two methods occupy different
points on a pass@1/pass@k trade-off rather than one dominating, that ES's
alarming parameter drift is concentrated enough to be harmless on held-out
tasks, and that the population size ES needs *falls* as models grow. The third
is a scaling claim and the most consequential.

## Key insight

**GRPO and ES are not two ways to do the same thing; they change different
parts of the network and leave the output distribution in different shapes.**
GRPO's largest updates land in token embeddings and the language-model head —
the input and output faces, which is what token-level gradient optimization
would do — and it concentrates the output distribution, raising pass@1 while
collapsing entropy and coverage. ES's largest updates land in **LayerNorm
weights and attention projections** — rescaling hidden states and rerouting
information — and leave entropy roughly intact. Once you see that, "which is
better" stops being the right question.

## Assumptions

- **A verifiable reward** throughout; every task is scored by an answer
  checker.
- **Matched update budgets** between ES and GRPO for the comparisons, and a
  single shared budget split across two stages for the sequential variant.
- The diversity theory assumes finite entropy and Fisher information, common
  local support and sufficient smoothness, and is a **local** analysis —
  small `σ`, expansions around the center.
- The forgetting result is conditioned on **held-out benchmark evaluation**,
  not on continual multi-task training; the paper says so and flags the longer
  horizon as future work.
- The functional-sparsity result is **post hoc**: the performance-preserving
  coordinate subspace is identified after training, not predicted before it.

## Key results

- **Lemma 1 (perturbations induce policy diversity).** For fixed prompt and
  population size, the induced policy displacement is governed by the
  prompt-conditioned Fisher information, in a small-`σ` limit.
- **Lemma 2 (diversity improves correct-answer discovery).** One independent
  sample per population member beats matched sampling from a single policy,
  with equality iff the member policies coincide and the local gap
  proportional to a verifier-projected Jensen–Shannon divergence. *Holds
  when:* the smoothness and support conditions of Appendix A.
- **Lemma 3 (reward weighting).** Normalized weights from a monotone transform
  of realized fitness improve population success when fitness correlates
  positively with member success.
- **Proposition.** Conditions under which the population-level coverage
  advantage is preserved in the updated center policy.
- **The headline empirical result.** GRPO falls below its own base model on
  **both pass@16 and pass@32 in 15 of 18 comparisons** in the Easy Setting,
  while improving average pass@1. ES improves average pass@1, pass@16 and
  pass@32 in both settings. GRPO's average pass@1 gain is larger; ES's
  pass@16 and pass@32 are higher.
- **Training dynamics.** On held-out GPQA during GSM8K post-training of
  Qwen2.5-1.5B-Instruct, token-level entropy declines substantially under GRPO
  and changes modestly under ES; GRPO ends below the base model on pass@16 and
  pass@32 and ES ends above.
- **Parameter drift.** Relative whole-model distance: GRPO 0.0475 against full
  ES 1.933 (≈40×) for Qwen2.5-1.5B-Instruct; 0.0954 against 4.185 (≈44×) for
  Llama-3.2-3B-Instruct.
- **Functional sparsity.** At a threshold within the magnitude range of a
  single ES update, 77.6–93.0% of nonzero updates fall below it. Zeroing them
  leaves target-task pass@1 broadly stable, degrading only at high update
  sparsity.
- **Where the updates land.** In DeepSeek-R1-Distill-Qwen-1.5B, 117 of 144
  maximum-magnitude coordinates are LayerNorm weights and 24 are
  attention-projection biases; normalization parameters are 72 and 80 of the
  100 largest updates in the two models examined. GRPO's largest update is an
  order of magnitude smaller and its top 100 are entirely in token embeddings
  (Llama-3.2-3B) or the LM head (DeepSeek-R1-Distill).
- **Population-size scaling.** On GSM8K at update 300, only `N = 30` stays
  within 0.5% of the `N = 30` reference at 0.5B, while both `N = 10` and
  `N = 20` clear it at 1.5B and 3B; the `N = 10`-to-`N = 30` gap shrinks with
  scale.
- **Estimator.** Antithetic ES is algebraically identical to two-point ZO
  under matched objectives and perturbations. Two-point ES gives no
  training-reward or held-out advantage on GSM8K; the appendix finds raw
  variance reduction for SST-2 but not reliably for regenerated GSM8K rewards.
- **Reward normalization.** Z-scoring population rewards beats no
  normalization throughout the evaluated updates.
- **Perturbation scale.** Two-sided failure — too small overfits the observed
  rewards and traps the search near a local optimum; too large destabilizes
  and collapses performance.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | GRPO improves pass@1 and degrades large-`k` pass@k, often below base | strong | 15 of 18 comparisons, plus entropy trajectories, plus prior reports it cites |
| C2 | ES improves pass@1, pass@16 and pass@32 together | strong | both settings, four models |
| C3 | ES's coverage advantage follows from population diversity | moderate | Lemmas 1–3 and a proposition, all local; the empirics are consistent but do not isolate the mechanism |
| C4 | ES's large parameter drift does not cause broad forgetting | moderate | held-out evaluations, single-task horizon only |
| C5 | ES's gains live in a sparse larger-magnitude coordinate subset | strong | magnitude-thresholding ablation across four models |
| C6 | ES adapts through normalization and attention parameters, GRPO through embeddings and the LM head | moderate | update-magnitude localization on two models; a clean measurement, a small sample |
| C7 | The population size needed for stable ES falls with model scale | moderate | three scales, one family, one task, a 0.5% band |
| C8 | Two-point antithetic estimation does not pay on reasoning tasks | moderate | one matched GSM8K run plus a variance diagnostic contrasting SST-2 |
| C9 | Sequential GRPO→ES buys both ends of the trade-off | weak | the paper calls it "an intuitive method"; one budget split, Pareto trade-offs reported |

## Method

Two settings. *Easy*: Qwen2.5-1.5B-Instruct, Llama-3.2-3B-Instruct and
Qwen2.5-7B-Instruct, two epochs of GSM8K post-training. *Hard*:
DeepSeek-R1-Distill-Qwen-1.5B, one epoch of DeepScaleR. Evaluation on GSM8K,
CSQA, HotpotQA, Countdown, GPQA and MBPP at pass@1, pass@16, pass@32 and
maj@k. Full-parameter one-point ES with z-scored rewards; sequential
compositions split one update budget equally between stages in both orders.

## Concepts

- **Solution coverage** — what large-`k` pass@k measures: the breadth of the
  output distribution rather than the quality of its mode.
- **Entropy collapse** — the narrowing of the token distribution under
  RL-style optimization, here measured on a held-out task during training.
- **Functional sparsity** — large parameter movement whose *effect* is carried
  by few coordinates.
- **Approximately performance-preserving coordinate subspace** — the paper's
  term for the coordinates that survive magnitude thresholding.

## Connections

It positions ES against GRPO as two mechanisms for the same verifiable-reward
objective, cites Qiu, Sarkar and Zheng as the line it is analysing, and
answers the catastrophic-forgetting reports of Hoy et al. and Abdi et al. with
a measurement. Its population-scaling argument cites Frankle and Carbin and
Gan and Isola together. Lineage is on the LIT.

## Recommendations

<!-- inactive-ok-block: SOTA-211 — Proposed, filed in this same change from this reading and named as where its recommendation landed -->
- **R1** — Report pass@k as well as pass@1. *Topic:* evaluation. *Status:*
  standard. *Strength:* strong. Filed as [SOTA-210](../practices.d/SOTA-210.md).
- **R2** — Use one fitness evaluation per ES direction on reasoning tasks.
  *Topic:* post-training. *Strength:* moderate. Filed as [SOTA-211](../practices.d/SOTA-211.md).
- **R3** — Z-score population rewards before weighting perturbations.
  *Topic:* post-training. *Strength:* moderate. Not filed — one ablation.
- **R4** — Expect a smaller ES population to suffice as the model grows, and
  tune it downward rather than up. *Topic:* post-training. *Strength:*
  moderate. Not filed — three scales, one family.
- **R5** — Do not infer forgetting from parameter drift; measure held-out
  performance. *Topic:* evaluation. *Strength:* moderate.

## Bearing on the record

<!-- inactive-ok-block: SOTA-211 — Proposed, filed in this same change from this reading and named as where its recommendation landed -->
Filed as [LIT-230](../literature.d/LIT-230.md). It is the primary source for [SOTA-210](../practices.d/SOTA-210.md) and a
corroborating source for [SOTA-211](../practices.d/SOTA-211.md).

<!-- inactive-ok-block: THEORY-006 — Proposed, and this paragraph is
     precisely about what does and does not satisfy its promotion condition -->
**It bears on [THEORY-006](../theory.d/THEORY-006.md) and does not promote it, which is worth being
exact about.** Its population-scaling section reasons that larger models hold
more performance-preserving subsets, "making task-improving perturbations
denser around pretrained weights, consistent with Frankle and Carbin (2018);
Gan and Isola (2026)" — citing the account — and then confirms a *consequence*:
fewer directions suffice at larger scale. That is an independent group finding
a prediction of the account holds. It is **not** what the promotion condition
asks for: it does not repeat the density measurement, it uses the same Qwen2.5
family, and it offers no mechanism predicting where the transition sits. The
condition stays as written.

<!-- inactive-ok-block: SOTA-154 is Active; named as the practice whose
     dissent this paper measures from the other side -->
It also cuts against [LIT-231](../literature.d/LIT-231.md)'s case against [SOTA-154](../practices.d/SOTA-154.md) in a specific
way. That paper's Lemma 1 concerns the angle between a random perturbation and
a single useful *direction*. This paper's C5 and C6 say the gains live in a
sparse, identifiable *subspace* — LayerNorm and attention projections — and the
geometry of projecting onto a subspace is not the geometry of projecting onto
a line. Both papers measure the drift and agree on its magnitude; they
disagree on what it means.

## Limitations

Stated: the single-task horizon for the forgetting result, and that the
sequential composition is intuitive rather than principled. From this reading:
the diversity theory is local and the empirical coverage advantage is not
traced to it; the population-scaling claim runs to 3B on one family; and C6's
localization, which is the most interesting finding here, rests on two models.

## Open questions

- **Does the coverage gap close with scale?** Everything here is ≤7B. What
  would close it: the same pass@k comparison at 30B+, where
  [LIT-234](../literature.d/LIT-234.md) has RL data but no entropy trajectories.
- **Is the LayerNorm/attention concentration causal?** What would close it:
  restricting ES to those parameters and recovering the gains, which the
  thresholding ablation approaches but does not run prospectively.
- **Does the population-size result hold outside Qwen2.5 and GSM8K?** One
  family, one task, a 0.5% band.
