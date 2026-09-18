---
status: Active
title: 'Program Synthesis with Large Language Models'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-18'
published: '2021-08-16'
arxiv: '2108.07732'
first_author: 'Austin'
keywords:
- 'benchmark'
- 'program-synthesis'
- 'mbpp'
implementations:
- 'MBPP'
- 'MathQA-Python'
summary: >-
  Austin et al. (2021), [ARXIV-2108.07732](https://arxiv.org/abs/2108.07732). Introduces MBPP — Mostly Basic Python
  Problems — short crowd-sourced tasks each with three test cases, the
  entry-level counterpart to HumanEval and the other half of the pair this
  record's code-generation results are reported on.
---

# LIT-tmpx3u6l: Program Synthesis with Large Language Models

Austin et al. (2021) — [ARXIV-2108.07732](https://arxiv.org/abs/2108.07732)

## Key takeaways

- **MBPP**: around a thousand short Python problems, crowd-sourced, each with a
  natural-language description and **three test cases** — deliberately basic,
  which is the point of the name and the reason it discriminates at a
  different part of the capability range than HumanEval
- Also introduces a Python-rewritten MathQA split, less used
- Correctness is measured by executing the tests, so a pass is a pass on three
  cases rather than a proof — the same bound HumanEval carries, and the reason
  `SOTA-210`'s `pass@k` estimator exists

## Standing in the anthology

**Carries no practice, deliberately** — `ADR-032`.

Filed as the other half of a pair the record already half-held: `LIT-388` is
HumanEval, filed in the benchmark unit, and ten documents here report MBPP
beside it. A code result quoted on one and not the other is a narrower claim
than it looks, and until now the record could name only one of them.

Unread — no `NOTE`.
