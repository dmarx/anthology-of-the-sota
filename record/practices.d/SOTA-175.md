---
number: 175
status: Proposed
formerly:
- SOTA-tmpwavay
promote_when: >-
  A second group building syntax-aware FIM data and reporting against
  random-span FIM on real edits, or a released code model whose report says
  its FIM spans were chosen by parse tree. What would not move it: a better
  score on a synthetic FIM benchmark, which is the evaluation this paper
  argues is the wrong one.
consensus: unreplicated
consensus_note: >-
  One group, one paper, one benchmark of its own construction. Falcon-H1-Tiny
  follows the construction and keeps random splits alongside it for
  robustness, which is adoption of a hedged form rather than corroboration.
title: 'Mask whole syntactic units for code fill-in-the-middle, not random character spans'
version: 1
tags:
- data-pipeline
date: '2026-09-08'
source:
- LIT-126
implementations: []
summary: >-
  Gong et al. (2025), [LIT-126](../literature.d/LIT-126.md) — standard FIM masks random character spans,
  which produces training examples that rarely correspond to an edit anyone
  makes. AST-FIM masks whole syntactic units at scale, so the middle span is
  a coherent structure. Up to 5 points over random-character FIM at 1B and
  8B, and most useful on real editing.
---

# SOTA-175: Mask whole syntactic units for code fill-in-the-middle, not random character spans

## Source

Gong et al. (2025), [LIT-126](../literature.d/LIT-126.md) — [ARXIV-2506.00204](https://arxiv.org/abs/2506.00204).

Standard FIM treats code as text and masks random character spans. The
objection is about what that trains for: a random span rarely corresponds to
an edit anyone actually makes, so the model is practised at completing holes
of a shape it will not meet. AST-FIM masks whole syntactic units instead —
blocks, expressions, functions — at scale, so the middle span is a coherent
structure.

## The evaluation is half the contribution

**Real-FIM-Eval** is derived from more than 30,000 GitHub commits across 12
languages, so the held-out holes are real edits rather than synthetic ones.
That matters more than it usually would here, because the whole argument is
that the standard benchmark measures the wrong distribution — a paper making
that claim and then evaluating on the standard benchmark would be arguing
against itself.

At 1B and 8B, AST-FIM outperforms random-character FIM by up to 5 points on
standard FIM benchmarks, and is most useful on the real-world editing task.

## Conditions, and why this is Proposed

One group, one paper, and the benchmark that shows the effect most clearly is
the group's own. Falcon-H1-Tiny follows the construction for its FIM data —
and keeps random splits alongside it for robustness, which is adoption of a
hedged form rather than corroboration of the claim.

The parsing requirement is also a real condition: this needs a parser per
language, which is why it is a code practice and not a FIM practice.

## Known implementations

- Falcon-H1-Tiny, alongside random splits.
