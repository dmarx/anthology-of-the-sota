---
status: Active
title: 'Measuring Mathematical Problem Solving With the MATH Dataset'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-18'
published: '2021-03-05'
arxiv: '2103.03874'
first_author: 'Hendrycks'
keywords:
- 'benchmark'
- 'mathematics'
- 'step-by-step-solutions'
implementations:
- 'MATH'
- 'MATH-500'
- 'AMPS'
summary: >-
  Hendrycks et al. (2021), [ARXIV-2103.03874](https://arxiv.org/abs/2103.03874). 12,500 competition mathematics
  problems, each with a full step-by-step solution — which is why the dataset
  became a training signal as well as a benchmark, and why a result on it
  needs to say which it was used as.
---

# LIT-tmp5psie: Measuring Mathematical Problem Solving With the MATH Dataset

Hendrycks et al. (2021) — [ARXIV-2103.03874](https://arxiv.org/abs/2103.03874)

## Key takeaways

- **12,500 competition mathematics problems**, harder than grade-school word
  problems by construction — this is the benchmark that sits above GSM8K
  (`LIT-389`) in the pair the record reports on together
- **Every problem carries a full step-by-step solution.** That is the design
  decision with consequences: the dataset can be used to *teach* derivations,
  not only to score answers, and the paper ships `AMPS`, an auxiliary
  pretraining corpus, for exactly that
- **So "trained on MATH" and "evaluated on MATH" are both ordinary uses**, and
  a number quoted without saying which is ambiguous in a way a benchmark-only
  dataset's number is not
- **MATH-500** — the 500-problem subset most later work reports — is a
  downstream convention rather than this paper's split, and results on it are
  not directly comparable to results on the full set

## Standing in the anthology

**Carries no practice, deliberately** — `ADR-032`.

Six documents here report on it, almost always beside GSM8K and
OlympiadBench as one of a suite: `NOTE-082`'s accuracy comparison runs across
Countdown, GSM8K, MATH and OlympiadBench, and `SOTA-210`'s `pass@k` argument
rests on results measured on that family.

What the note is here to bound is the training-signal ambiguity above. The
record contains practices about reasoning traces in training data —
`SOTA-127` filters chain-of-thought out of tiny models' training data — and a
dataset whose problems ship with worked solutions is precisely the kind of
thing that lands on both sides of that line. Nothing here currently says so.

Unread — no `NOTE`.
