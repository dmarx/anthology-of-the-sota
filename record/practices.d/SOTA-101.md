---
number: 101
status: 'Active'
title: 'Use perplexity-based filtering for quality assessment'
version: 1
tags:
- data-pipeline
date: '2026-08-24'
published: '2023-12-01'
source:
- LIT-117
summary: >-
  Albalak et al. (2023), [LIT-117](../literature.d/LIT-117.md) — [ARXIV-2312.02406](https://arxiv.org/abs/2312.02406).
---

# SOTA-101: Use perplexity-based filtering for quality assessment

## Source

Albalak et al. (2023), [LIT-117](../literature.d/LIT-117.md) — [ARXIV-2312.02406](https://arxiv.org/abs/2312.02406).

## Perplexity as a signal, and what ODM does with it

[LIT-117](../literature.d/LIT-117.md)'s mechanism is a multi-armed bandit over data domains whose reward is
a perplexity-derived quantity computed **during** training, on the batches the
run is already taking. That is what makes it *online*: no separate proxy runs,
no held-out sweep, negligible added cost.

The signal it uses is learnability rather than quality. A domain whose loss is
falling fastest is where the next tokens buy the most, and that changes as
training proceeds — a domain worth over-sampling early can be exhausted later.
Perplexity is a proxy for that, not for whether the text is good.

## Where the title overstates it

"Quality assessment" is not what a perplexity number is. A high-perplexity
document can be noise or it can be rare and valuable, and the two are
indistinguishable to the model's own uncertainty — which is why
perplexity-based *filtering*, as distinct from perplexity-based *weighting*,
is a blunt instrument that preferentially discards unusual text.

The defensible version is the one the source supports: use perplexity to
decide *how much to sample from a domain*, continuously, and not to decide
what to discard. Those are different practices with different failure modes,
and the title names the weaker one.
