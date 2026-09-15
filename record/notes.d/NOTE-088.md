---
number: 88
status: Read
formerly:
- NOTE-tmpv3wri
paper: LIT-241
title: 'Proximal Policy Optimization Algorithms'
version: 1
tags:
- training-optimization
date: '2026-09-15'
summary: >-
  Clip the probability ratio to [1-eps, 1+eps] and take the minimum of the
  clipped and unclipped surrogate, so the objective is a pessimistic lower
  bound — which gives trust-region behaviour from first-order optimization,
  permits several epochs of minibatch SGD on one batch of collected data, and
  fits in a few lines of change to vanilla policy gradient.
---

# NOTE-088: Proximal Policy Optimization Algorithms

## Contribution

Makes trust-region reliability available without the trust region. TRPO
achieved stable policy updates with a hard KL constraint and paid for it in
complexity and in incompatibility with shared parameters and stochastic layers.
PPO obtains comparable behaviour from a modified objective that any
autodiff-based policy-gradient implementation can adopt, which is why it
became the default rather than why it is better.

## Key insight

**The clip does not do the work — the minimum does.** Clipping `r_t` to
`[1−ε, 1+ε]` removes the *incentive* to push the ratio outside that band, but
on its own it would still permit an unbounded step in the direction where
clipping has not yet bitten. Taking `min(unclipped, clipped)` makes the
surrogate a **pessimistic lower bound**: the change in the ratio is ignored
when it would improve the objective and counted when it would worsen it. The
objective agrees with the unclipped surrogate to first order at `θ_old` and
separates as the policy moves.

The consequence that matters in practice: because the surrogate bounds how far
the policy can usefully move, a single batch of collected experience supports
**several epochs of minibatch SGD** rather than one update. That is where the
sample-efficiency gain over vanilla policy gradient comes from, and it is a
statement about the objective rather than about the estimator.

## Assumptions

- **On-policy data**, with the ratio taken against the policy that collected
  it; the bound is what licenses reusing that batch a few times, not
  indefinitely.
- **An advantage estimator**, typically generalized advantage estimation or a
  truncated finite-horizon estimator, and therefore usually a learned value
  function.
- **`ε = 0.2`** is offered as a suggestion ("say, `ε = 0.2`"), not a swept
  result.
- The full objective assumes coefficients `c₁`, `c₂` balancing the value-
  function loss and entropy bonus against the surrogate, needed when policy
  and value function share parameters.

## Key results

- **The clipped objective is the best of the variants tested.** The paper
  compares surrogate objectives and reports the clipped-ratio version
  performing best.
- **The adaptive KL penalty is worse, and is included as a baseline.**
  `L_KLPEN` with `β` halved when measured KL falls below `d_targ/1.5` and
  doubled when it exceeds `d_targ × 1.5`: "we found that the KL penalty
  performed worse than the clipped surrogate objective, however, we've
  included it here because it's an important baseline." The scheme is robust
  to its own constants and to `β`'s initialization, since `β` adapts quickly.
- **Continuous control.** PPO outperforms the other online policy-gradient
  methods compared against.
- **Atari.** Significantly better sample complexity than A2C; comparable to
  ACER while being much simpler.
- **The combined objective.** `L_CLIP − c₁ L_VF + c₂ S[π]`, with `L_VF` a
  squared error against a value target and `S` an entropy bonus for
  exploration.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The clipped surrogate is a pessimistic lower bound on the unclipped one | strong | by construction, and illustrated by interpolation along the update direction |
| C2 | It permits multiple epochs per batch | strong | the mechanism is the bound; the gain is measured |
| C3 | It matches TRPO's reliability with first-order optimization | moderate | empirical across the benchmark suite of its time |
| C4 | The clipped objective beats the adaptive KL penalty | moderate | the paper's own comparison, one suite |
| C5 | `ε = 0.2` is a good default | weak | suggested, not swept |
| C6 | PPO is simpler to implement than TRPO | strong, and it is the real reason for adoption | "only few lines of code change" |

## Method

Alternate between collecting `T` timesteps of on-policy data under `π_old` and
performing several epochs of minibatch stochastic gradient ascent on
`L_CLIP+VF+S`. Compute advantages with a truncated estimator that does not
look beyond `T`. Optionally use the adaptive-`β` KL-penalized objective
instead of, or alongside, the clipped one.

## Concepts

- **Probability ratio `r_t(θ)`** — the likelihood of the taken action under
  the new policy over the old; equal to 1 at `θ_old`.
- **Surrogate objective** — a function of `θ` whose optimization stands in for
  improving the policy, valid while the policy stays near where the data was
  collected.
- **Pessimistic lower bound** — the effect of the `min`, and the mechanism
  that makes several epochs safe.
- **Adaptive KL penalty** — the variant with `β` tuned per update to hit a
  target divergence.

## Connections

It positions against deep Q-learning (unreliable on continuous control),
vanilla policy gradient (poor data efficiency), and TRPO (complicated,
incompatible with parameter sharing and noise). Downstream in this record,
[LIT-127](../literature.d/LIT-127.md) introduces GRPO as PPO with the critic removed and the baseline
taken from a group of sampled outputs. Lineage is on the LIT.

## Recommendations

- **R1** — Prefer the clipped surrogate to a KL penalty; the algorithm's own
  authors found the penalty worse and it introduces a coefficient to tune.
  *Topic:* post-training. *Strength:* moderate, and worth stating because so
  much later work tunes `β`.
- **R2** — Exploit the bound: run several epochs of minibatch SGD per
  collected batch rather than one update per sample. *Strength:* strong.
- **R3** — When policy and value share parameters, the objective is three
  terms; the entropy bonus is not optional decoration. *Strength:* moderate.

## Bearing on the record

Filed as [LIT-241](../literature.d/LIT-241.md), `extended_by:` [LIT-127](../literature.d/LIT-127.md).

<!-- inactive-ok-block: SOTA-146 — Proposed, and named as the practice that
     corrects an objective descended from this paper -->
**Three practices in this record are about modifications of this algorithm and
none of them could cite it.** [SOTA-145](../practices.d/SOTA-145.md) recommends taking the RL baseline from
a group of samples "instead of training a critic" — the critic is the `L_VF`
term here. [SOTA-146](../practices.d/SOTA-146.md) corrects three defects in the GRPO objective, which is
this paper's clipped ratio with a different advantage estimator. [SOTA-129](../practices.d/SOTA-129.md)
makes the family the third stage of the reasoning recipe. The sweep found this
paper cited by six of the twelve.

**It is the baseline the entire evolution-strategies line measures against**,
and one detail of that is worth recording. Papers in the line grid-search
PPO's KL coefficient `β` — [LIT-211](../literature.d/LIT-211.md) explicitly, noting RL "did not make much
progress if they were not set precisely". §4 here says the KL-penalized
variant is the *worse* of the two the authors tested. That does not invalidate
those comparisons, which are entitled to tune what they tune; it is the sort
of context a reader can only have if the record holds the parent, which is
this note's argument for existing.

## Limitations

Stated: none at length. From this reading: `ε = 0.2` is a suggestion rather
than a swept default; the comparison set is 2017's and says nothing about the
gradient-free question this record cares about; and the paper's advantage
over TRPO is substantially about implementability, which is a real reason for
an algorithm to win and not evidence that it optimizes better.

## Open questions

- **Does the clipped-beats-KL finding hold at LLM scale?** Every RLHF and
  RLVR recipe in this record carries a KL term, usually against a reference
  policy rather than the previous policy — a different use of the same idea,
  and nobody has asked whether §4's result transfers.
- **How many epochs per batch is right for reasoning?** The bound licenses
  several; the LLM literature mostly runs one or two and does not say why.
- **What does `ε` do at scale?** Untested here and load-bearing in every
  descendant.
