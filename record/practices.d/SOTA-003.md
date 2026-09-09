---
number: 3
status: 'Active'
title: 'Learning rate typically 1e-4 to 1e-3 for most tasks'
version: 1
tags:
- training-optimization
date: '2026-08-24'
published: '2014-12-01'
source:
- LIT-001
summary: >-
  Kingma et al. (2014), [LIT-001](../literature.d/LIT-001.md) — [ARXIV-1412.6980](https://arxiv.org/abs/1412.6980).
---

# SOTA-003: Learning rate typically 1e-4 to 1e-3 for most tasks

## Source

Kingma et al. (2014), [LIT-001](../literature.d/LIT-001.md) — [ARXIV-1412.6980](https://arxiv.org/abs/1412.6980).

## What the range is anchored to

Adam normalises each parameter's step by its own gradient scale, so the
learning rate stops being a step size in the loss's units and becomes closer
to a bound on the *relative* change per step. That is why a range this narrow
transfers across problems at all — it is not a coincidence, and it is the main
practical argument for adaptive methods.

## Where it does not transfer, which is most of what this record is about

The number depends on batch size, on the schedule, and above all on the
parameterisation. A transformer trained at the scales the rest of this
registry describes does not use a rate picked from this range by inspection:

<!-- inactive-ok-block: SOTA-144, SOTA-159 — Proposed, cited as the µP line that makes the rate measured rather than chosen; the proposals are the point -->
- under µP ([SOTA-144](SOTA-144.md), [SOTA-159](SOTA-159.md)), the whole point is that the rate transfers
  from a small proxy model, so it is *measured* rather than chosen;
- with warmup and decay ([SOTA-008](SOTA-008.md), [SOTA-009](SOTA-009.md)), the quoted rate is a peak that
  the run is at only briefly;
- with Muon or another matrix-aware optimizer ([SOTA-121](SOTA-121.md)), the AdamW-tuned rate
  is deliberately made to carry over, which is a statement about that
  optimizer rather than this range.

So this practice is a reasonable starting point for a small model with no
tuning budget, and the record should not read it as advice for the runs it
otherwise documents. Kept because it is true in its scope.

<!-- inactive-ok-block: SOTA-041 — Rejected in #114; named here because this paragraph used to assert its claim as fact -->
This paragraph used to add that larger models are *less* sensitive to the
choice, citing [SOTA-041](SOTA-041.md). That practice is retired: Kaplan reports the
opposite — larger models need a **smaller** rate to avoid divergence, and
carry an explicit `LR(N)` rule for it. So the reason a 2020-era range survives
is not that the choice stopped mattering; it is that nobody re-fit it, and
the modern answer is a parameterisation that transfers the rate rather than a
range that holds.
