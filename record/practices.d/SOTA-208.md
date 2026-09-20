---
number: 208
status: 'Superseded'
formerly:
- SOTA-tmpu69f8
title: 'Factorize long-sequence attention into a local window and a second head that escapes it'
version: 1
superseded_by:
- SOTA-138
tags:
- attention-techniques
date: '2026-09-13'
source:
- LIT-225
# The same paper, in both fields: Child et al. stated the recommendation and
# ran the experiments for it (ADR-029). Populated here because the
# distinction is cheap to state at filing time and impossible to recover
# later.
introduced_by:
- LIT-225
implementations:
- LIT-225
summary: >-
  Child et al. (2019), [LIT-225](../literature.d/LIT-225.md) — [ARXIV-1904.10509](https://arxiv.org/abs/1904.10509). Superseded: the field
  went to exact attention made fast ([SOTA-086](SOTA-086.md), [SOTA-087](SOTA-087.md)) and then to sparsity
  that is LEARNED rather than fixed ([SOTA-138](SOTA-138.md)). What survives is the
  connectivity requirement — a window alone is not the design — which every
  hybrid the record recommends is an instance of.
---

<!-- inactive-ok-file: ADR-029 — Proposed. Every mention here names it as the decision that added `introduced_by:`, which is the field this document uses; the citation is to the reasoning, not a claim the decision is settled -->

# SOTA-208: Factorize long-sequence attention into a local window and a second head that escapes it

## Source

Child et al. (2019), [LIT-225](../literature.d/LIT-225.md) — [ARXIV-1904.10509](https://arxiv.org/abs/1904.10509).

Split causal attention across `p = 2` heads whose patterns, composed, connect
every pair of positions within `p + 1` steps. The first head is a **local
window** — the previous `l` positions, with the stride `l` chosen close to
`sqrt(n)`. The second head is the **escape**, and it takes one of two shapes:

- **strided** — attend to every `l`-th position — for data whose structure is
  periodic, which is images and some music;
- **fixed** — cells at the end of each block of `l` summarize it and are
  visible to every later block, with `c` in `{8, 16, 32}` such cells for
  `l` in `{128, 256}` — for data that has no such periodicity, which is text.

Integrate them by alternating one pattern per residual block, by merging both
into one head, or across the heads of a multi-head layer.

## The condition, which is the part worth keeping

**The window is half of the design and the paper says so.** Its connectivity
criterion — every pair connected within `p + 1` steps — is what the second
head exists to satisfy, and a stack of purely local layers is named in the
text as a *softening* of that criterion, a possibly useful inductive bias
rather than the thing being recommended.

**Which escape you need is a property of the data, and getting it wrong costs
more than not being sparse at all.** On enwik8 at 12,288 context, strided
attention reached 1.13 bits per byte where dense attention reached 1.00; the
fixed pattern reached 0.99. The same strided pattern won on CIFAR-10 (2.80
against dense 2.82). One mechanism, two datasets, opposite verdicts — the
failure is the escape's shape against the data's structure, and nothing about
the window changed between them.

## Why it is superseded, and by what

Two separate things replaced it and neither is "sparsity was wrong":

- **Exact attention got fast.** [SOTA-086](SOTA-086.md) and [SOTA-087](SOTA-087.md) made the quadratic
  kernel memory-efficient rather than approximating it, which removed most of
  the reason to accept an approximation at the lengths people actually train.
- **Sparsity came back learned.** [SOTA-138](SOTA-138.md) trains the pattern with an indexer
  rather than fixing it in the architecture, which is the direct successor to
  this claim: same goal, and the pattern is no longer a hyperparameter chosen
  by inspecting the data.

The record holds one side of that disagreement. **This practice is the other
side, stated by the paper that ran it**, and it is filed rather than omitted
because the enwik8 result above is the cleanest evidence the corpus has for
what a hand-chosen pattern risks — which is the argument for [SOTA-138](SOTA-138.md).

## What did not get superseded

<!-- inactive-ok-block: SOTA-176 — Proposed, named as one instance among five of the pairing this paper requires, not relied on -->

The window-plus-escape pairing. Every hybrid in this record is an instance of
it, reached independently and with a different escape each time: designated
global tokens ([LIT-033](../literature.d/LIT-033.md)), emergent attention sinks ([LIT-191](../literature.d/LIT-191.md)), NoPE global
layers ([SOTA-153](SOTA-153.md)), long-term slots under one softmax ([SOTA-176](SOTA-176.md)), a gated
linear-attention state ([LIT-204](../literature.d/LIT-204.md)). None of them is a stack of local layers,
and this is the paper that says why none of them can be.

## Known implementations

- GPT-3, which reports *"alternating dense and locally banded sparse attention
  patterns in the layers of the transformer, similar to the Sparse
  Transformer"* ([LIT-035](../literature.d/LIT-035.md)). Adoption rather than evidence, per [DP-005](../../docs/design-principles.md#dp-5).
