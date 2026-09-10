---
number: 68
status: Superseded
superseded_by: SOTA-035
status_note: >-
  SOTA-035 is the same recommendation with a real source and without the
  false qualifier — clipping is applied throughout training, not only early
title: 'Use gradient clipping during early training phase'
version: 2
history:
- version: 2
  date: '2026-09-09'
  note: >-
    Superseded by SOTA-035 rather than Rejected. The other four practices in
    the LIT-052 cluster claim things nothing in the record supports; this one
    names a genuinely universal practice, wrongly attributed and wrongly
    qualified. Something replaced it, so the status says so.
tags:
- training-optimization
date: '2026-08-24'
source:
- LIT-052
implementations:
- vision_transformer
- bert
summary: >-
  Tay et al. (2021), [LIT-052](../literature.d/LIT-052.md) — [ARXIV-2109.10686](https://arxiv.org/abs/2109.10686). Superseded by [SOTA-035](SOTA-035.md), which cites Pascanu et al. and drops the "early training" qualifier.
---

# SOTA-068: Use gradient clipping during early training phase

## Source

Tay et al. (2021), [LIT-052](../literature.d/LIT-052.md) — [ARXIV-2109.10686](https://arxiv.org/abs/2109.10686).

## Why this is superseded rather than rejected

The other four practices drawn from [LIT-052](../literature.d/LIT-052.md)'s replaced takeaways claim things
no paper in the record supports. This one is different: gradient clipping is
real, near-universal, and already in the record with a correct citation.
[SOTA-035](SOTA-035.md) recommends it from Pascanu et al. ([LIT-037](../literature.d/LIT-037.md)), where the argument
about exploding gradients was actually made.

So the failure here is narrower and worth separating from the other four. The
attribution is wrong — the source contains "gradient clip" zero times — and
the qualifier is wrong too.

## The qualifier is the part that would have misled

"During early training phase" implies clipping is a warmup-period measure to
be relaxed once the run settles. It is not. Clipping stays on for the whole
run in every frontier recipe in the record, because the spikes it exists to
bound are not confined to early training — a bad batch, a stale checkpoint
resume, or a data-mixture switch can produce one at any point, and by then the
practice as written would have had you turn the guard off.

That is why this needed a status change rather than a body explaining the
mistake. Left `Active`, it read as a live recommendation to stop clipping.
