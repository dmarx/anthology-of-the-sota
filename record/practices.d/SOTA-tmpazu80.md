---
status: Active
consensus: emerging
consensus_note: >-
  Two groups with no authors in common report the same shape within a
  fortnight (LIT-tmp81or2, LIT-tmpiq6kc), on different model families, against
  different RL implementations and published third-party checkpoints, and both
  cite earlier reports of the same effect. Nobody has published a defence of
  pass@1-only reporting; what keeps this short of `converged` is that the
  practice it corrects is still what almost every post-training result does.
title: 'Report pass@k as well as pass@1 after post-training: reinforcement learning raises one and lowers the other'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
source:
# Two independent groups, and the order matters: LIT-tmp81or2 is the
# controlled comparison with the mechanism (entropy collapse, measured), and
# LIT-tmpiq6kc is the scale evidence and the accuracy-histogram account of
# where the ceiling comes from.
- LIT-tmp81or2
- LIT-tmpiq6kc
introduced_by:
- LIT-tmpiq6kc
implementations: []
summary: >-
  Ba et al. and Hayes et al. (2026), [LIT-tmp81or2](../literature.d/LIT-tmp81or2.md) and [LIT-tmpiq6kc](../literature.d/LIT-tmpiq6kc.md). GRPO
  finishes below its own base model on pass@16 and pass@32 in 15 of 18
  comparisons while improving pass@1; across Qwen2.5, Qwen3 and published RL
  checkpoints up to 32B the base model overtakes the RL checkpoint at large k.
  A post-training result reported at pass@1 alone cannot distinguish a model
  that learned something from one that stopped trying anything else.
---

# SOTA-tmpazu80: Report pass@k as well as pass@1 after post-training: reinforcement learning raises one and lowers the other

## Source

Ba et al. (2026), [LIT-tmp81or2](../literature.d/LIT-tmp81or2.md) — [ARXIV-2608.27351](https://arxiv.org/abs/2608.27351); Hayes et al.
(2026), [LIT-tmpiq6kc](../literature.d/LIT-tmpiq6kc.md) — [ARXIV-2608.12679](https://arxiv.org/abs/2608.12679).

## The measurement, and why one number hides it

Pass@1 is single-sample accuracy. Pass@k is the probability that at least one
of `k` sampled responses is correct — at large `k` it measures the breadth of
the output distribution rather than the quality of its mode. Reinforcement
learning with verifiable rewards moves these two in **opposite directions**,
and reporting only the first makes a narrowing look like an improvement.

The numbers are not marginal:

- GRPO finishes **below its own base model** on both pass@16 and pass@32 in
  **15 of 18 comparisons**, while improving average pass@1 ([LIT-tmp81or2](../literature.d/LIT-tmp81or2.md)).
- Across Qwen2.5-Instruct 1.5B–7B and Qwen3 1.7B–8B, RL's pass@k curves
  plateau and the **base model overtakes the RL checkpoint** at large `k`.
  The same holds at 7B, 14B and 32B against published checkpoints — OatZero
  and SimpleRL-Zoo, not the authors' own RL runs ([LIT-tmpiq6kc](../literature.d/LIT-tmpiq6kc.md)).

## Where the loss comes from, which is the part worth understanding

Bin prompts by the fraction of `k` samples answered correctly. RL increases
the mass in the all-correct bin, which is what its objective asks for. It
**also increases the mass in the all-wrong bin** relative to the base model:
prompts the base model could sometimes solve become prompts it never solves.
That is a hard ceiling on pass@k which no additional sampling can lift, and it
is invisible to pass@1 because the same optimization is adding wins elsewhere.

The diagnostic that makes it legible is **progressions and regressions** —
count prompts the base model got wrong and the tuned model gets right,
separately from the reverse. Pass@1 nets them; the net can be positive while
the regressions are permanent.

The mechanism on the training side is entropy collapse, and it is directly
observable: under GRPO, held-out token-level entropy falls sharply over
training while pass@16 and pass@32 decline with it; under evolution
strategies, entropy barely moves and all three metrics rise
([LIT-tmp81or2](../literature.d/LIT-tmp81or2.md)).

## Conditions

**This is about post-training that reshapes the output distribution**, which
is what RLVR does by construction. It is not a claim that every fine-tuning
method collapses coverage — the same two papers are there because evolution
strategies do not.

**It matters most where test-time sampling is the deployment**: verifiable
domains, agentic retries, best-of-n, majority voting, search over candidate
solutions. If the model answers once and the answer ships, pass@1 is the
metric and this practice costs you an extra evaluation for information you
will not use.

**Use an unbiased low-variance estimator** rather than measuring pass@k by
repeated trials — [LIT-tmpiq6kc](../literature.d/LIT-tmpiq6kc.md) uses the standard one over `n` sampled
responses per problem, and the naive approach needs many trials per `k` to
control variance.

## What this does not say

It does not say RLVR is a mistake. It says RLVR has a cost that the standard
report does not show, and that the cost is paid in a currency some deployments
spend and others do not.

<!-- inactive-ok-block: SOTA-129 is Active and named as the recipe stage this
     practice qualifies rather than contradicts -->
It does not disturb [SOTA-129](SOTA-129.md), which makes RLVR the third stage of the
reasoning recipe. It qualifies what that stage delivers: pass@1, and less
coverage than the model had going in.

Nor does it settle what to do about it. The two papers point in different
directions — one proposes running GRPO and ES in sequence to buy both ends,
the other argues for ES outright — and both are one experiment each.

## Known implementations

- None as a reporting convention. Both source papers report it; nothing else
  in this record's corpus does.
