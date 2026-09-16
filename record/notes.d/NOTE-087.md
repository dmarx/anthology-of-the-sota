---
number: 87
status: Read
formerly:
- NOTE-tmpbtwav
paper: LIT-242
title: 'Evolution Strategies as a Scalable Alternative to Reinforcement Learning'
version: 1
date: '2026-09-15'
summary: >-
  Shared random seeds let every worker reconstruct every other worker's
  perturbation, so an ES update costs one scalar per worker instead of a
  gradient — which turns 11 hours on 18 cores into 10 minutes on 1,440. The
  paper also argues that the policy-gradient estimator's variance grows with
  episode length while ES's does not, and that ambient parameter count is not
  the dimension that matters.
---

# NOTE-087: Evolution Strategies as a Scalable Alternative to Reinforcement Learning

## Contribution

Rehabilitates a class of algorithms the field had written off, by changing
what you optimize for. ES was known to be data-inefficient against policy
gradients and that was taken as settling the matter. This paper's move is to
observe that ES's communication cost can be made almost zero, so the
comparison that matters is not data per update but **wall clock at a given
budget of machines** — and on that axis a method needing 3–10× more data wins
by two orders of magnitude.

## Key insight

**Synchronize the random seeds and the gradient never has to travel.** Each
worker perturbs by `ε_i` drawn from a seed the others know, evaluates, and
broadcasts a single scalar return. Every worker then reconstructs every
perturbation locally and applies the same update. Policy gradients must ship
whole gradients between workers; ES ships `n` floats.

That is the whole of it, and it reframes the method. ES is not a better
optimizer than policy gradients — the paper is explicit that it needs more
data — it is an optimizer whose parallel efficiency is so much higher that
data efficiency stops being the binding constraint when you have machines.

## Assumptions

- **Episodic tasks with a scalar return.** Only the total return of an episode
  is used; the method never sees individual rewards or their timing.
- **Gaussian perturbations in parameter space**, with fixed `σ`, and the
  objective read as a Gaussian-smoothed version of the true one.
- **Enough parallel workers for the argument to pay.** On one machine ES is
  roughly par with RL; the result is about the slope, not the intercept.
- **Reparameterizations that the LLM line has since dropped.** Virtual batch
  normalization is called out as necessary: "without these methods ES proved
  brittle in our experiments".
- In practice perturbations are drawn from a large pre-instantiated noise
  block indexed randomly, so they are **not strictly independent across
  iterations** — stated, and reported not to matter.

## Key results

- **Parallel scaling.** 3D humanoid walking: ~11 hours on one 18-core machine,
  **10 minutes on 1,440 cores across 80 machines**, with linear speedup in
  cores. Run on ordinary EC2, no special networking.
- **Atari.** Competitive with A3C's published one-day results after one hour
  of ES; better on 23 games, worse on 28. Fixed hyperparameters across all
  Atari environments.
- **Data efficiency.** 3–10× more data than A3C, partly offset by ~3× less
  computation from no backpropagation and no value function. On MuJoCo, within
  10× of TRPO's data for matched policy performance.
- **§3.1, the variance argument.** For a REINFORCE-style estimator with a good
  baseline, the policy-gradient term `∇ log p(a;θ)` is a sum of `T`
  uncorrelated pieces, so its variance grows nearly linearly with episode
  length. The ES term `∇ log p(θ̃;θ)` is **independent of `T`**. Hence ES's
  advantage on long horizons, delayed rewards, and where no good value
  function is available — and hence why the usual mitigations (discounting,
  value approximation) are described as trading variance for bias.
- **§3.2, the dimensionality argument.** ES resembles randomized finite
  differences, and worst-case theory says steps scale linearly with dimension.
  The paper's rebuttal: what matters is the **intrinsic dimension of the
  optimization problem**, not the parameter count. Concatenating a regression's
  features with themselves doubles parameters and changes nothing, and ES
  behaves identically given `σ` and the learning rate halved. Empirically,
  larger networks did slightly *better*.
- **Invariance to action frequency.** Atari Pong at frame-skip {1,2,3,4}
  produces near-identical learning curves, each converging in around 100
  weight updates.
- **Exploration.** On MuJoCo humanoid, ES finds a wide variety of gaits —
  walking sideways, walking backwards — never observed under TRPO.
- **Robustness.** One fixed hyperparameter set across all Atari environments,
  another across all MuJoCo, with one binary exception.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Shared seeds reduce ES communication to one scalar per worker | strong | structural, and the scaling curve confirms the consequence |
| C2 | ES achieves linear speedup to 1,440 cores | strong | measured, 7 repetitions, median reported |
| C3 | ES is competitive with A3C and TRPO at equal wall clock | moderate | 23 wins / 28 losses on Atari against published numbers, not re-run baselines |
| C4 | ES needs 3–10× more data | strong, and the authors lead with it | measured |
| C5 | PG estimator variance grows with `T`, ES's does not | strong as analysis | derived under simple-Monte-Carlo assumptions with a good baseline |
| C6 | Parameter count is not the dimension that governs ES | moderate | a clean argument, a synthetic example, and one empirical observation on Atari network sizes |
| C7 | ES explores differently, not just more | moderate | the gait observation is qualitative and striking |
| C8 | ES suits low-precision and inference-only hardware | not tested | argued from the absence of backpropagation; nine years later ESSA demonstrates it |

## Method

Per iteration: each of `n` workers samples `ε_i ~ N(0,I)` from a known seed,
evaluates `F(θ_t + σ ε_i)`, and broadcasts the scalar. Each worker then
reconstructs all `ε_j` and applies
`θ_{t+1} ← θ_t + α (1/nσ) Σ_j F_j ε_j`. Antithetic sampling is used for
variance reduction; fitness is rank-shaped; virtual batch normalization is
applied to the policy network. At the extreme, workers may perturb disjoint
parameter subsets, which reduces to pure finite differences and leaves the
update equations unchanged.

## Concepts

- **Smoothing in parameter space vs action space** — the paper's framing of
  the ES/PG distinction. Both add noise to make a non-smooth decision problem
  differentiable; they differ only in where.
- **Common random numbers** — the seed-sharing scheme, and the actual
  contribution.
- **Intrinsic dimension of the optimization problem** — as distinct from the
  parameter count.
- **Antithetic (mirrored) sampling** — evaluating `+ε` and `−ε` as a pair.

## Connections

It places itself in the natural-evolution-strategies family, notes the
estimator is also known as simultaneous perturbation stochastic approximation,
parameter-exploring policy gradients, or zero-order gradient estimation, and
distinguishes itself from CMA-ES, which it describes as successful in low to
medium dimension. Downstream, [LIT-211](../literature.d/LIT-211.md) carries it to LLM fine-tuning and
everything else in this record's line descends through that. Lineage is on the
LIT.

## Recommendations

- **R1** — Where workers are cheap and interconnect is not, compare optimizers
  on wall clock at a fixed machine budget rather than on data efficiency.
  *Topic:* training. *Strength:* strong, and it is the paper's real argument.
- **R2** — Share random seeds rather than perturbations or gradients.
  *Strength:* strong; universally adopted in this line.
- **R3** — Prefer ES where episodes are long, rewards are delayed or sparse,
  or no good value function exists. *Strength:* moderate, and derived in §3.1.
- **R4** — Do not size an ES problem by parameter count. *Strength:* moderate.
- **R5** — Reparameterize the policy before concluding ES is brittle. Virtual
  batch normalization was necessary here and the LLM line has quietly dropped
  it. *Strength:* moderate, and worth someone re-testing.

## Bearing on the record

Filed as [LIT-242](../literature.d/LIT-242.md), `extended_by:` [LIT-211](../literature.d/LIT-211.md).

**It is the trunk the bibliography sweep found**, cited by ten of the twelve
papers in this line and absent until now. The record held nine descendants, a
practice recommending the technique, and two theory documents explaining why
it works.

<!-- inactive-ok-block: THEORY-007 — Proposed, and this paragraph is about
     that account's precedence, which is what the citation is for -->
**§3.2 states [THEORY-007](../theory.d/THEORY-007.md)'s claim in 2017.** That the ambient parameter count
is not what governs ES, that intrinsic dimension is, and that larger networks
do better rather than worse — all three are here, with an argument and an
observation. [LIT-236](../literature.d/LIT-236.md) adds the mechanism (a low-dimensional curvature-active
subspace and the degeneracy it induces), the measurement across scales, and
the link to rise-then-decay. Those are real additions. But the record filed
that account without knowing its central claim was nine years old, which is
the sweep's second finding and is now written into both documents.

<!-- inactive-ok-block: SOTA-211 — Proposed, and named as the practice that
     argues against a convention this paper introduced -->
**It is also where [SOTA-211](../practices.d/SOTA-211.md)'s target comes from.** Antithetic sampling enters
the line here, as variance reduction, on control tasks where the paired
evaluations share their randomness. The argument against it is specific to
regenerating autoregressive responses and does not reach back to this paper.

**What it does not do is displace [SOTA-154](../practices.d/SOTA-154.md)'s `introduced_by:`.** This
recommends ES over policy gradients for control tasks trained from scratch;
the practice recommends it for LLM fine-tuning, a claim this paper does not
make and whose feasibility the field doubted until [LIT-211](../literature.d/LIT-211.md). Same sentence,
different claim, and the field's doubt is the evidence that they are different.

## Limitations

Stated: the data-efficiency deficit, and that the larger-networks observation
is a hypothesis. From this reading: everything is control tasks with small
networks, so the dimensionality argument is made at a scale where it could not
fail interestingly; the Atari comparison is against published numbers rather
than re-run baselines; and the reparameterization dependence is reported
without being characterized.

## Open questions

- **Does virtual batch normalization still matter?** It was necessary here and
  no paper in the LLM line mentions it. Either the finding did not transfer or
  nobody checked.
<!-- inactive-ok-block: THEORY-007 — Proposed, and named as the account whose
     promotion condition still asks for what this paper left open -->
- **What is the intrinsic dimension, concretely?** §3.2 is an argument for the
  distinction mattering, not a measurement — and [THEORY-007](../theory.d/THEORY-007.md)'s promotion
  condition still asks for the same thing nine years on.
- **Does the frame-skip invariance have an LLM analogue?** Invariance to the
  temporal resolution of the decision problem should say something about
  sequence length or reasoning-trace length, and nobody in this line has asked.
