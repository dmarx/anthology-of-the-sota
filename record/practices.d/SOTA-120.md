---
status: Deferred
status_note: the paper is settled; how widely it is actually adopted is not
promote_when: >-
  A survey or a frontier training report that states which of the two it
  uses, rather than leaving the choice implicit in a config. The result is
  not in question; what is unmeasured is how many people act on it.
title: 'Prefer AdamW''s decoupled weight decay to L2 regularization added to the loss'
version: 1
tags:
- training-optimization
date: '2026-08-24'
published: '2017-11-01'
source:
- LIT-012
summary: >-
  Loshchilov et al. (2017), [LIT-012](../literature.d/LIT-012.md) — [ARXIV-1711.05101](https://arxiv.org/abs/1711.05101).
---

# SOTA-120: Prefer AdamW's decoupled weight decay to L2 regularization added to the loss

## Source

Loshchilov et al. (2017), [LIT-012](../literature.d/LIT-012.md) — [ARXIV-1711.05101](https://arxiv.org/abs/1711.05101).

## Why this is deferred

Carried over from the `sota_maybe` field, verbatim:

> I feel like everyone still uses vanilla Adam though...
>
> llama2 used - β₁=0.9, β₂=0.95

The claim above is not in doubt; its adoption is — which is why the
condition in `promote_when:` asks for a report that *states* the choice.
If the answer turns out to be that nobody decouples, this is superseded
rather than promoted.
