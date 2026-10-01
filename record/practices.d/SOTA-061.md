---
number: 61
status: 'Active'
title: 'Use largest batch that maintains >80% sample efficiency'
version: 3
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
- version: 3
  date: '2026-10-01'
  note: >-
    Re-sourced, and the origin left empty. Both relations named LIT-061
    (Artetxe et al., misattributed in the Source line to Fedus et al.),
    whose only statement about batch size is that it was set "according to
    the model size following Brown et al. (2020)": no measurement of sample
    efficiency and no 80%. The trade the rule draws a line across is
    McCandlish et al. (LIT-017); that the line has to be found by
    measurement is Shallue et al. (LIT-058). Neither, nor Kaplan et al.,
    states an 80% threshold, so introduced_by is empty under ADR-053. The
    recommendation and status are unchanged.
tags:
- training-optimization
date: '2026-08-24'
# Was LIT-061 (Artetxe et al.), which borrows GPT-3's batch sizes in one
# sentence and measures nothing about sample efficiency. Moved to the work
# that evidences the trade: McCandlish's steps/examples hyperbola, which
# defines the data efficiency this rule thresholds, and Shallue's measurement
# that the maximum useful batch varies by workload and must be found.
source:
- LIT-017
- LIT-058
# Deliberately empty (ADR-053). Was LIT-061. Searched: LIT-061 (Artetxe et
# al. 2021), LIT-017 (McCandlish et al. 2018), LIT-058 (Shallue et al. 2018)
# and LIT-028 (Kaplan et al. 2020), full text, for an 80% / four-fifths
# sample-efficiency threshold; none states one, and a web search turned up
# no other origin. McCandlish's own compromise point, B_crit, sits at 50%.
# Naming the paper that first drew the line at 80% refutes this.
introduced_by: []
summary: >-
  McCandlish et al. (2018), LIT-017 — [ARXIV-1812.06162](https://arxiv.org/abs/1812.06162). The
  steps/examples trade the rule thresholds; the 80% line itself has no
  published origin the record can name.
---

# SOTA-061: Use largest batch that maintains >80% sample efficiency

## Source

McCandlish et al. (2018), [LIT-017](../literature.d/LIT-017.md) — [ARXIV-1812.06162](https://arxiv.org/abs/1812.06162).

Shallue et al. (2018), [LIT-058](../literature.d/LIT-058.md) — [ARXIV-1811.03600](https://arxiv.org/abs/1811.03600).

**The 80% threshold has no published origin that this record can name**, and
`introduced_by:` is empty to say so ([ADR-053](../decisions.d/ADR-053.md)). The practice was filed against
Artetxe et al. ([LIT-061](../literature.d/LIT-061.md)), whose only sentence on the subject sets
batch size and learning rate "according to the model size following Brown
et al. (2020)" — a borrowed setting, with no measurement of sample efficiency
and no threshold. McCandlish, Shallue and Kaplan ([LIT-028](../literature.d/LIT-028.md)) do not state one
either. What the two sources evidence is the trade the rule draws a line
across, not where the line goes.

[LIT-017](../literature.d/LIT-017.md) is the trade. Steps and examples to a given loss lie on a hyperbola,
`(S/S_min − 1)(E/E_min − 1) = 1`, with the critical batch size defined off it
as `B_crit = E_min/S_min`; training at `B_crit` takes twice the minimum steps
and twice the minimum data, and above it there are diminishing returns from
more parallelism. At a fixed batch `E = B·S`, so the same equation gives
`E/E_min = 1 + B/B_crit`: 80% sample efficiency is `B = B_crit/4`, at five
times the minimum number of steps. That is arithmetic on the paper's
equation, not a number the paper reports, and it puts this rule well short of
the paper's own compromise point, which sits at 50%.

[LIT-058](../literature.d/LIT-058.md) is why the threshold has to be read off a measurement. Across 35
workloads it found the same three regions — perfect scaling, diminishing
returns, maximal data parallelism — and that "the maximum useful batch size
varies significantly between workloads and depends on properties of the
model, training algorithm, and data set", so the batch where efficiency
starts to fall cannot be inherited from someone else's run.

## The 80% is a stopping rule, not a measurement

Sample efficiency falls as batch grows — more samples per step buy a
progressively smaller improvement per sample ([SOTA-092](SOTA-092.md), [SOTA-093](SOTA-093.md)). Throughput
rises over the same range. The practice says to keep raising the batch while
the sample-efficiency loss stays inside a fifth, and stop there.

That is a defensible way to trade the two, and it is worth being clear that
the threshold is a *risk appetite* rather than an optimum. Nothing in the
record shows that 80% is where the exchange rate turns. [LIT-017](../literature.d/LIT-017.md)'s curve is
smooth, and the one point on it the paper singles out, `B_crit`, is at 50% —
so 80% is a line drawn across that curve so that a decision can be made
without re-deriving the curve each time.

<!-- inactive-ok-block: SOTA-062 — Superseded, named as the other answer to the same question -->
[SOTA-062](SOTA-062.md) answered the same question, how large a batch, from a different
input: scale it with model size, sub-linearly. This practice reads the answer
off measured sample efficiency instead, which is closer to the quantity that
matters. The model-size rule is now superseded, because at a fixed token
budget the dependence of critical batch size on model size very nearly
vanishes ([SOTA-258](SOTA-258.md)). No paper compared the two rules head to head; they are
alternatives the record holds side by side.

## Cost and condition

Measuring it requires the counterfactual — how the run would have progressed
at the smaller batch — which nobody has for the run they are actually doing.
In practice it is estimated from small-scale sweeps and assumed to transfer,
which is exactly the assumption [SOTA-037](SOTA-037.md)'s body warns about in a different
context.

For an MoE model — the setting of [LIT-061](../literature.d/LIT-061.md), the paper this practice was
first filed against — there is an extra term the title does not carry. That
paper gives each expert a capacity of `C·B/E` tokens for a batch of `B`
tokens over `E` experts, and notes that expert parameters see an `E`-times
smaller batch than the dense ones, rescaling their gradients by `1/√E` to
match. So a larger batch also gives each expert more tokens per step, and the
batch interacts with load balance
<!-- inactive-ok-block: SOTA-148 — Proposed, cited as the load-balance interaction a sparse model adds to this trade -->
([SOTA-148](SOTA-148.md)) rather than only with gradient noise. That is a reason the answer
for a sparse model is not the answer for a dense one of the same size.
