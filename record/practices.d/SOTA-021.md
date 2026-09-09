---
number: 21
status: Rejected
status_note: >-
  states no threshold and no response, and the smoothing it refers to is a
  mechanism from a paper the record had conflated with this one. Measuring
  landscape smoothness during training is not something the practice's
  source does or recommends; the finding it rests on is Santurkar et al.'s
  explanation of why batch normalization works, which is a fact about the
  technique rather than an instruction
title: 'Monitor loss landscape smoothness during training'
version: 1
tags:
- model-stability
date: '2026-08-24'
published: '2018-06-01'
source:
- LIT-015
summary: >-
  Santurkar et al. (2018), [LIT-015](../literature.d/LIT-015.md) — [ARXIV-1806.02375](https://arxiv.org/abs/1806.02375).
---

# SOTA-021: Monitor loss landscape smoothness during training

## Source

Santurkar et al. (2018), [LIT-015](../literature.d/LIT-015.md) — [ARXIV-1806.02375](https://arxiv.org/abs/1806.02375).

## Why this is retired rather than rewritten

Two problems, and either alone would be enough.

**It is not actionable.** "Monitor loss landscape smoothness during training"
names no signal you could plot, no threshold, and no response — the same gap
<!-- inactive-ok: SOTA-073, SOTA-074 — Rejected for the same reason as this one, and named as the precedent -->
that retired [SOTA-073](SOTA-073.md) and [SOTA-074](SOTA-074.md). Landscape smoothness is not a quantity
training loops compute; the nearest practical proxy is the Hessian
eigenvalue ratio in [SOTA-011](SOTA-011.md), which is expensive and periodic rather than
monitored.

**Its mechanism is another paper's.** Smoothing, predictive gradients and
Lipschitzness are Santurkar, Tsipras, Ilyas and Madry — *How Does Batch
Normalization Help Optimization?*, now filed in the record — and they were
attributed to [LIT-015](../literature.d/LIT-015.md) because that note carried the wrong author and
takeaways. The finding is real and it is an *explanation of why batch
normalization works*, not an instruction to anyone running a job.

The explanation survives where it belongs, in the literature note. What is
retired is the attempt to turn it into a practice.
