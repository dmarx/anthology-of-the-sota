---
status: Read
paper: LIT-tmpd7q1v
title: 'Evaluating Large Language Models Trained on Code'
version: 1
date: '2026-09-17'
summary: >-
  Read for the metric rather than the benchmark. The paper defines `pass@k`
  and the unbiased estimator 1 - C(n-c,k)/C(n,k), and argues explicitly why
  the naive repeated-trials measurement is biased downward — which is the
  convention [SOTA-210](../practices.d/SOTA-210.md) already recommends while calling it "the standard one"
  and citing nobody.
---

# NOTE-tmp33m0o: Evaluating Large Language Models Trained on Code

Read from [LIT-tmpd7q1v](../literature.d/LIT-tmpd7q1v.md) — [ARXIV-2107.03374](https://arxiv.org/abs/2107.03374).

## Why this one was read and the other two benchmarks were not

[ADR-032](../decisions.d/ADR-032.md) says a benchmark note needs no reading, and that absence of a
`NOTE` honestly signals the paper is unread ([ADR-025](../decisions.d/ADR-025.md)). GSM8K and MMLU are
filed on their abstracts and carry no note, which is the accurate statement
of what was done.

This one was read, because the record turned out to depend on a section of it.

## The metric, and the estimator the record was already using

Section 2 opens by "defining the `pass@k` metric, and explain[ing] its
advantages over standard match-based metrics" — so functional correctness and
`pass@k` arrive together, as one proposal about how code generation should be
evaluated at all.

The estimator is the part that matters here. Generate `n ≥ k` samples
(n=200, k≤100 in the paper), count the `c` that pass, and compute

    pass@k := E_problems [ 1 − C(n−c, k) / C(n, k) ]

with an explicit argument for why the obvious alternative is wrong:

> While the top expression may look correct, it underestimates the true value
> by a considerable margin. The unbiased estimator may have a slightly higher
> variance initially but allows for a fair comparison across different numbers
> of samples.

There is an appendix, *Estimating pass@k*, devoted to it.

## What this does to the record

[SOTA-210](../practices.d/SOTA-210.md) recommends reporting `pass@k` alongside `pass@1`, and says:

> **Use an unbiased low-variance estimator** rather than measuring pass@k by
> repeated trials — [LIT-234](../literature.d/LIT-234.md) uses **the standard one** over `n` sampled
> responses per problem, and the naive approach needs many trials per `k` to
> control variance.

"The standard one" is this estimator, and the clause about naive trials is a
compression of the argument quoted above. So the record was recommending a
metric and an estimator whose defining paper it did not hold — [DP-007](../principles.d/DP-007.md)'s
trunk exactly: the convention is so settled that nobody was prompted to file
its origin, and the practice that depends on it cites the paper that *used*
it rather than the one that *defined* it.

[SOTA-210](../practices.d/SOTA-210.md) gains that citation in this change. Its recommendation is
unchanged.

## What I did not take from it

Codex itself — the model, its training, the Copilot deployment. That is a
model report inside a benchmark paper, and nothing in this record is argued on
it.

Also not taken: the 28.8% and 70.2% figures as anything but period detail.
They are what made the case for sampling repeatedly in 2021; quoting them now
would be quoting a model, not a finding.
