---
number: 127
status: Active
title: 'Filter chain-of-thought traces out of the training data of tiny specialized models'
version: 2
history:
- version: 2
  date: '2026-09-07'
  note: >-
    Sourced to LIT-123 as well as LIT-119. The mechanism the practice argues
    from — a model trained on reasoning beyond its capacity learns the cheaper
    pattern, which is repetition — is LIT-123's, and the source follows it
    explicitly. The recommendation is unchanged.
tags:
- data-pipeline
- tiny-models
date: '2026-09-05'
published: '2026-01-15'
source:
# The mechanism the practice's argument rests on is LIT-123's, followed
# explicitly by the source: a model trained on reasoning beyond its capacity
# learns the cheaper pattern, which is repetition.
- LIT-119
- LIT-123
summary: >-
  Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost. Reasoning traces interleaved with tool-calling data sent a 90M model into repetition loops; removing them fixed it at once.
---

# SOTA-127: Filter chain-of-thought traces out of the training data of tiny specialized models

## Source

Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost.

## The failure it fixes

When the tool-calling mix included sources carrying long chain-of-thought
traces between the calls, the 90M model produced repetition loops instead
of function calls — stuck on a phrase or a partial trace — visible directly
in BFCL-v3 generations. Removing all reasoning and thinking content from
those sources and keeping only the direct tool-calling examples fixed it
immediately. The authors' reading, following Pipis et al. (2025, [LIT-123](../literature.d/LIT-123.md)) on why
distilled small models loop more than their teachers: when the training
distribution carries reasoning patterns beyond the model's capacity, the
model learns the cheaper pattern, which is repetition. The same failure
appeared in the 90M reasoning model, which is more prone to the repetition
trap than the 0.6B one.

## Conditions

This is about models around 100M trained for a structured
target other than reasoning. It is not a claim against reasoning traces as
such — the reasoning models in the same release are trained on nothing
else — but a claim that a tiny model cannot carry both, and that the traces
are what to drop when the target is the call.

## Known implementations

- Falcon-H1-Tiny-Tool-Calling
