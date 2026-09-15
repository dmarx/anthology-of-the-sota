---
status: Read
paper: LIT-tmpiq6kc
title: 'Beyond the Best Guess'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-15'
summary: >-
  Reinforcement learning raises pass@1 and lowers pass@k, eventually below the
  base model, because it increases the number of prompts solved in none of k
  samples; evolution strategies raise both and never fall below base at any k
  or scale tested, up to 32B against published RL checkpoints.
---

# NOTE-tmpbyaoe: Beyond the Best Guess

## Contribution

Establishes that RLVR's distribution collapse is a property of the paradigm
rather than of any one implementation, by showing the same pass@k saturation
against multiple RL algorithms and published third-party checkpoints, and
takes the ES comparison to 32B — the largest scale at which this record has
evidence for that line. Its second contribution is diagnostic: it locates the
loss in the accuracy histogram, which converts "coverage collapse" from a
curve shape into a countable thing.

## Key insight

**RL does not merely fail to improve hard prompts; it destroys prompts the
base model could sometimes solve.** Bin prompts by the fraction of `k`
responses answered correctly. RL raises the all-correct mass, as intended —
*and also raises the all-wrong mass above the base model's*. Those prompts
are now unsolvable at any sampling budget. That is a hard ceiling on pass@k,
and it is the reason the base model eventually overtakes its own RL-tuned
descendant: not because RL learned nothing, but because what it lost cannot be
recovered by sampling and what it gained saturates.

## Assumptions

- **Verifiable answers throughout** — the pass@k framing needs a checker, and
  every benchmark here is mathematical reasoning.
- **A fixed `n` samples per problem**, with pass@k computed by the standard
  unbiased low-variance estimator over the `n` responses rather than by
  repeated trials at each `k`.
- **Third-party RL checkpoints at the larger scales** — OatZero and
  SimpleRL-Zoo — which means those comparisons are against what people ship
  rather than against RL runs matched to the ES budget.
- ES here is [LIT-211](../literature.d/LIT-211.md)'s ES-at-Scale, applied by the same lab that published it.

## Key results

- **Pass@k across families.** ES beats RL on pass@k across Qwen2.5-Instruct
  1.5B/3B/7B and Qwen3 1.7B/4B/8B, with a crossover typically around `k = 4`,
  after which RL's curves plateau and ES's continue.
- **The base model overtakes RL.** For the Qwen2.5-Instruct models the base
  model passes the RL checkpoint at sufficiently large `k` — empirically
  confirming a prior report the paper cites.
- **ES never falls below base**, at any `k` or any model scale tested.
- **At 7B, 14B and 32B.** Qwen2.5-Math-7B, Qwen2.5-14B and Qwen2.5-32B on
  MATH500, OlympiadBench and Minerva against OatZero and SimpleRL-Zoo. ES
  ahead of OatZero on MATH500 at 7B; ahead of SimpleRL-Zoo on OlympiadBench at
  14B, where the base model also becomes competitive with SimpleRL-Zoo at
  large `k`; and at 32B on Minerva the ES advantage **grows with `k`**.
- **The accuracy-distribution mechanism.** RL increases mass in both the
  all-correct and the all-wrong bin relative to base; ES increases the
  all-correct mass and *reduces* the all-wrong mass, distributing gains across
  the partially-correct bins. Consistent across Qwen2.5, Qwen3 and Qwen2.5-Math
  from 1.5B to 32B.
- **Progressions and regressions.** The paper's proposed accounting: prompts
  gained versus prompts lost relative to base, reported separately rather than
  netted.
- **Downstream.** Voting results verify that the pass@k improvement carries
  into settings where answers are not directly verifiable.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | RLVR narrows the output distribution, lowering large-`k` pass@k | strong | multiple RL algorithms, multiple families, published checkpoints, 1.5B–32B |
| C2 | The base model can overtake its RL-tuned descendant at large `k` | strong | observed across Qwen2.5-Instruct and at 14B on OlympiadBench |
| C3 | RL increases the count of prompts solvable in none of `k` samples | strong | direct histogram measurement, consistent across scales |
| C4 | ES raises pass@1 and pass@k together and never falls below base | strong within this lab's setup | every model and benchmark tested, but one group and one ES implementation |
| C5 | The ES advantage persists as models scale | moderate | 7B/14B/32B against third-party checkpoints, not budget-matched |
| C6 | ES is the better post-training choice for discovery domains | moderate | follows from C1–C4 given the framing; the discovery setting itself is not measured |
| C7 | This is an independent replication of [SOTA-154](../practices.d/SOTA-154.md) | false | same group as [LIT-211](../literature.d/LIT-211.md), sharing an author and the method |

## Method

Fine-tune with ES-at-Scale; evaluate pass@k with the unbiased estimator over
`n` sampled responses per problem, using the same `n` as the prior work each
benchmark comes from. Compare against RL checkpoints — the authors' own at
1.5B–8B, and published OatZero and SimpleRL-Zoo checkpoints at 7B–32B.
Analyse via accuracy-distribution histograms, progression/regression counts,
and answer entropy.

## Concepts

- **Solution coverage** — the fraction of problems for which the model's
  output distribution contains *some* correct response; what pass@k approaches
  as `k` grows.
- **Distribution collapse** — the narrowing of that support under RL
  post-training.
- **Progressions / regressions** — prompts gained and lost relative to base,
  counted separately.
- **Best guess** — the paper's name for the pass@1 operating point, and the
  thing it argues is the wrong target for discovery.

## Connections

It sits alongside vector policy optimization, which trains for candidate-set
diversity and improves pass@k *at the cost of* pass@1 — the contrast the paper
draws for its own claim of improving both. It confirms Yue et al.'s earlier
report that base models can overtake RLVR models at large `k`. Its ES is Qiu
et al.'s. Lineage is on the LIT.

## Recommendations

- **R1** — Report pass@k, not only pass@1, and use the unbiased estimator.
  *Topic:* evaluation. *Status:* standard. *Strength:* strong. Filed as
  [SOTA-tmpazu80](../practices.d/SOTA-tmpazu80.md).
- **R2** — Count progressions and regressions separately rather than netting
  them into an accuracy delta. *Topic:* evaluation. *Strength:* strong, and
  cheap to adopt.
- **R3** — Where the deployment samples many candidates — verifiable domains,
  agentic retries, search — prefer a post-training method that preserves
  coverage. *Topic:* post-training. *Strength:* moderate.
- **R4** — Optimize the test-time-scaling objective directly if that is what
  you deploy. *Topic:* post-training. *Strength:* weak; the paper proposes
  this as future work rather than doing it.

## Bearing on the record

Filed as [LIT-tmpiq6kc](../literature.d/LIT-tmpiq6kc.md), `extends:` [LIT-211](../literature.d/LIT-211.md). It is `introduced_by:` on
[SOTA-tmpazu80](../practices.d/SOTA-tmpazu80.md) — it states the recommendation, where [LIT-tmp81or2](../literature.d/LIT-tmp81or2.md) supplies
the controlled comparison and the entropy mechanism.

<!-- inactive-ok-block: SOTA-129 is Active and named as the recipe stage this
     reading qualifies -->
**What it does to [SOTA-129](../practices.d/SOTA-129.md).** That practice makes RLVR the third stage of
the reasoning recipe. Nothing here says the stage should go; what it says is
that the stage has a cost nobody was reporting, and that the cost is paid in
solution coverage. [SOTA-tmpazu80](../practices.d/SOTA-tmpazu80.md) is where that lands.

<!-- inactive-ok-block: SOTA-154 is Active; this paragraph is about what does
     NOT count toward its promotion condition -->
**What it does not do for [SOTA-154](../practices.d/SOTA-154.md), deliberately recorded.** Cognizant AI
Lab, with Qiu among the authors of both this and [LIT-211](../literature.d/LIT-211.md), running that
paper's method. The promotion condition excluded "further results from the
same group" and this is exactly that. It extends the *scale* of the evidence
to 32B, which the practice's conditions section now reflects, and it is not a
second group. The independent corroboration of the coverage claim is
[LIT-tmp81or2](../literature.d/LIT-tmp81or2.md).

## Limitations

Stated: mathematical reasoning only; the discovery framing is motivation. From
this reading: the large-scale comparisons are against published checkpoints
rather than budget-matched RL, so they answer "does ES beat what people ship"
rather than "does ES beat RL under one protocol"; and every ES number comes
from one lab running one implementation.

## Open questions

- **Does an independent group see the same curves at 32B?** [LIT-tmp81or2](../literature.d/LIT-tmp81or2.md)
  replicates the shape but stops at 7B.
- **Is coverage preservation a property of ES, or of any method that does not
  optimize pass@1 directly?** What would close it: the same histogram analysis
  for a coverage-targeted RL objective such as vector policy optimization,
  which the paper cites but does not run.
- **Does the all-wrong-bin increase persist with KL regularization tuned to
  prevent it?** The obvious first defence of RLVR, and untested here.
