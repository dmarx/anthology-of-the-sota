---
status: 'Active'
title: 'Evaluating Large Language Models Trained on Code'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-17'
published: '2021-07-07'
arxiv: '2107.03374'
first_author: 'Chen'
keywords:
- 'benchmark'
- 'code-generation'
- 'pass-at-k'
- 'functional-correctness'
implementations:
- 'HumanEval'
- 'Codex'
summary: >-
  Chen et al. (2021), [ARXIV-2107.03374](https://arxiv.org/abs/2107.03374). Introduces HumanEval, which measures
  FUNCTIONAL correctness of generated programs against unit tests rather than
  textual similarity — and defines `pass@k` along with the unbiased estimator
  the record already recommends without citing. The benchmark is the
  better-known half; the metric is the half this anthology was leaning on.
---

# LIT-tmpd7q1v: Evaluating Large Language Models Trained on Code

Chen et al. (2021) — [ARXIV-2107.03374](https://arxiv.org/abs/2107.03374)

## What it measures

**Functional correctness**: a generated program is right if it passes the unit
tests, not if it resembles a reference solution. The paper is explicit that
this is the point of departure from "standard match-based metrics", and it is
why HumanEval displaced BLEU-style code evaluation.

164 hand-written problems, each a docstring plus tests. Hand-written
deliberately — the paper built them rather than scraping, because a scraped
Python benchmark is contaminated by construction against a model trained on
GitHub.

## What `pass@k` is, and why the estimator matters

`pass@k` is the probability that at least one of `k` samples passes. The naive
measurement — draw `k`, check, repeat — is what the paper argues against:

> While the top expression may look correct, it underestimates the true value
> by a considerable margin. The unbiased estimator may have a slightly higher
> variance initially but allows for a fair comparison across different numbers
> of samples.

So they generate `n ≥ k` samples (n=200, k≤100), count the `c` that pass, and
compute `1 − C(n−c, k) / C(n, k)`.

**This is the estimator [SOTA-210](../practices.d/SOTA-210.md) calls "the standard one" without saying
whose.** That practice also compresses this paper's variance argument into a
clause. The convention it recommends is defined here.

## What it is insensitive to

- **Single functions from docstrings.** Not architecture, not multi-file
  change, not debugging existing code.
- The paper names its own model's failure modes, which double as the
  benchmark's blind spots at the time: "difficulty with docstrings describing
  long chains of operations and with binding operations to variables."
- **Tests certify behaviour, not quality.** A solution that passes can be
  unreadable, quadratic, or unsafe, and the metric cannot tell.
- 164 problems is small, so differences of a point or two are noise.

## Standing in the anthology

Filed under [ADR-032](../decisions.d/ADR-032.md), which admits benchmarks and says a benchmark note will
usually carry no practice. This one is admitted for a stronger reason than
the usual: **the record recommends its metric.** HumanEval appears in five
practices and twelve documents, and until now the anthology had the
convention and not the paper that defines it — the trunk shape [DP-007](../principles.d/DP-007.md)
describes, where what everyone agrees on has no arrival event.

Carries no practice of its own; [SOTA-210](../practices.d/SOTA-210.md) is where the recommendation lives,
and this note is what it should have been citing.
