---
number: 61
status: 'Active'
title: 'Use largest batch that maintains >80% sample efficiency'
version: 2
history:
# inactive-ok-block: SOTA-062 — Superseded in this same change; named here
# because it carried the identical mis-tag from the identical source
- version: 2
  date: '2026-09-20'
  note: >-
    Retagged from `model-architecture` to `training-optimization`. This is a
    batch-size practice, `batch size` is named in the training-optimization
    blurb, and nothing in the model-architecture blurb covers it — the same
    mis-filing SOTA-062 carried, from the same source paper, and correct to
    fix on its own terms. The recommendation, status and source are
    unchanged.
tags:
- training-optimization
date: '2026-08-24'
source:
- LIT-061
introduced_by:
- LIT-061
summary: >-
  Fedus et al. (2021), [LIT-061](../literature.d/LIT-061.md) — [ARXIV-2112.10684](https://arxiv.org/abs/2112.10684).
compared_against:
- SOTA-062
---

# SOTA-061: Use largest batch that maintains >80% sample efficiency

## Source

Fedus et al. (2021), [LIT-061](../literature.d/LIT-061.md) — [ARXIV-2112.10684](https://arxiv.org/abs/2112.10684).

## The 80% is a stopping rule, not a measurement

Sample efficiency falls as batch grows — more samples per step buy a
progressively smaller improvement per sample ([SOTA-092](SOTA-092.md), [SOTA-093](SOTA-093.md)). Throughput
rises over the same range. The practice says to keep raising the batch while
the sample-efficiency loss stays inside a fifth, and stop there.

That is a defensible way to trade the two, and it is worth being clear that
the threshold is a *risk appetite* rather than an optimum. Nothing in
[LIT-061](../literature.d/LIT-061.md) shows that 80% is where the exchange rate turns; it is a line drawn
across a smooth curve so that a decision can be made without re-deriving the
curve each time.

## Cost and condition

Measuring it requires the counterfactual — how the run would have progressed
at the smaller batch — which nobody has for the run they are actually doing.
In practice it is estimated from small-scale sweeps and assumed to transfer,
which is exactly the assumption [SOTA-037](SOTA-037.md)'s body warns about in a different
context.

For an MoE model, which is [LIT-061](../literature.d/LIT-061.md)'s setting, there is an extra term the
title does not carry: expert routing means a larger batch also gives each
expert more tokens per step, so the batch interacts with load balance
<!-- inactive-ok-block: SOTA-148 — Proposed, cited as the load-balance interaction a sparse model adds to this trade -->
([SOTA-148](SOTA-148.md)) rather than only with gradient noise. That is a reason the answer
for a sparse model is not the answer for a dense one of the same size.
