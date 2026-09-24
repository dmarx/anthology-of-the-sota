---
number: 210
status: Active
formerly:
- SOTA-tmpazu80
consensus: emerging
consensus_note: >-
  Two groups with no authors in common report the same shape within a
  fortnight (LIT-230, LIT-234), on different model families, against
  different RL implementations and published third-party checkpoints, and both
  cite earlier reports of the same effect. Nobody has published a defence of
  pass@1-only reporting; what keeps this short of `converged` is that the
  practice it corrects is still what almost every post-training result does.
title: 'Report pass@k as well as pass@1 after post-training: reinforcement learning raises one and lowers the other'
version: 3
history:
- version: 2
  date: '2026-09-17'
  note: >-
    Names the source of the estimator it recommends. The practice called it
    "the standard one" and cited the paper that USES it rather than the one
    that defines it; LIT-388 is where pass@k and the unbiased estimator
    are introduced. The recommendation is unchanged.
- version: 3
  date: '2026-09-24'
  note: >-
    Adds a bound on the metric this practice recommends. Li et al.
    (LIT-650) define `n@k` — solved with `n` submissions from `k`
    samples — and state that `pass@k = k@k` is an upper bound, because it
    scores a system allowed to submit everything it generates. The
    recommendation is unchanged and so is the finding it rests on, which is a
    comparison of base against tuned on the same metric. What is added is
    what the number means for a deployment with a selection step, which is
    the deployment this practice's own conditions section says it matters
    most for. Also adds the false-positive rate on HumanEval, since this
    practice names LIT-388 as the metric's source.
tags:
- analysis-and-evaluation
- adaptation-and-tuning
date: '2026-09-15'
source:
# Two independent groups, and the order matters: LIT-230 is the
# controlled comparison with the mechanism (entropy collapse, measured), and
# LIT-234 is the scale evidence and the accuracy-histogram account of
# where the ceiling comes from.
- LIT-230
- LIT-234
introduced_by:
- LIT-234
implementations: []
summary: >-
  Ba et al. and Hayes et al. (2026), [LIT-230](../literature.d/LIT-230.md) and [LIT-234](../literature.d/LIT-234.md). GRPO
  finishes below its own base model on pass@16 and pass@32 in 15 of 18
  comparisons while improving pass@1; across Qwen2.5, Qwen3 and published RL
  checkpoints up to 32B the base model overtakes the RL checkpoint at large k.
  A post-training result reported at pass@1 alone cannot distinguish a model
  that learned something from one that stopped trying anything else.
---

# SOTA-210: Report pass@k as well as pass@1 after post-training: reinforcement learning raises one and lowers the other

## Source

Ba et al. (2026), [LIT-230](../literature.d/LIT-230.md) — [ARXIV-2608.27351](https://arxiv.org/abs/2608.27351); Hayes et al.
(2026), [LIT-234](../literature.d/LIT-234.md) — [ARXIV-2608.12679](https://arxiv.org/abs/2608.12679).

## The measurement, and why one number hides it

Pass@1 is single-sample accuracy. Pass@k is the probability that at least one
of `k` sampled responses is correct — at large `k` it measures the breadth of
the output distribution rather than the quality of its mode. Reinforcement
learning with verifiable rewards moves these two in **opposite directions**,
and reporting only the first makes a narrowing look like an improvement.

The numbers are not marginal:

- GRPO finishes **below its own base model** on both pass@16 and pass@32 in
  **15 of 18 comparisons**, while improving average pass@1 ([LIT-230](../literature.d/LIT-230.md)).
- Across Qwen2.5-Instruct 1.5B–7B and Qwen3 1.7B–8B, RL's pass@k curves
  plateau and the **base model overtakes the RL checkpoint** at large `k`.
  The same holds at 7B, 14B and 32B against published checkpoints — OatZero
  and SimpleRL-Zoo, not the authors' own RL runs ([LIT-234](../literature.d/LIT-234.md)).

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
([LIT-230](../literature.d/LIT-230.md)).

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
repeated trials — [LIT-234](../literature.d/LIT-234.md) uses it over `n` sampled responses per problem,
and the naive approach needs many trials per `k` to control variance.

The estimator is `1 − C(n−c, k) / C(n, k)` over `n ≥ k` samples of which `c`
pass, and it is [LIT-388](../literature.d/LIT-388.md)'s, which is also where `pass@k` is defined. That
paper makes the argument this practice was compressing: the naive form "may
look correct" but "underestimates the true value by a considerable margin",
and the unbiased one trades a little early variance for comparability across
different sample counts.

## What `pass@k` is an upper bound on

`pass@k` scores a system that may submit every sample it draws. Almost
nothing does. Li et al. (`LIT-650`) name the general form — **`n@k`**,
the fraction of problems solved with `n` submissions drawn from `k` samples —
and state the relation plainly:

> `pass@k = k@k`, and is an upper bound metric for using `k` samples.

So `pass@k` measures **whether a correct sample exists in the pile**, not
whether the system can find it. Between the two sits a selector, and the
selector is where the loss is: in their setting, filtering candidate programs
on the example tests given in the problem statement **removes about 99% of
samples**, and on roughly **10% of problems no sample survives the filter at
all**.

None of that disturbs the finding above. The base-versus-tuned comparison is
run on the same metric in both arms, so an upper bound applied to both still
shows RL moving the two numbers in opposite directions. What it changes is the
reading of the magnitude. This practice's conditions say the coverage matters
*"where test-time sampling is the deployment — verifiable domains, agentic
retries, best-of-n, majority voting, search over candidate solutions"* — and
every one of those has a selection step. **Coverage you cannot select from is
not coverage you can spend**, so `pass@k` overstates what post-training took
away as well as what it left.

Where the deployment has a submission or verification budget, report `n@k` at
that budget beside `pass@k`. The gap between them is the part of the problem
that is yours rather than the model's.

## A note on the benchmark this metric came with

`LIT-388` defines `pass@k` and is also HumanEval. Li et al. hand-checked fifty
HumanEval problems their model solved and found **30% false positives** —
programs passing every test and not correct — on 7.77 tests per problem. That
is about the benchmark rather than the metric, and it is recorded in
`LIT-388`'s own note with the qualifications it needs. It is named here
because this practice sends a reader to that benchmark for the estimator, and
a reader arriving at `pass@k` should know what a "pass" was measured to be
worth.

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
