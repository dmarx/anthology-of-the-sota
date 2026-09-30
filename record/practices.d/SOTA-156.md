---
number: 156
status: Proposed
formerly:
- SOTA-tmpvlopd
promote_when: >-
  A pretraining report at the scale where the schedule question is actually
  open — LIT-131 and LIT-145 disagree above 1B parameters and 1T tokens —
  that trains under Schedule-Free and says so; or a schedule comparison that
  includes it as an arm with its own peak learning rate swept, against cosine
  and against WSD swept the same way. The AlgoPerf win is a fixed-rules
  result on workloads far below that, so more of it would not move this.
consensus: unreplicated
consensus_note: >-
  One group, one method, one competitive benchmark. Nobody has published a
  disagreement, which is what separates unreplicated from contested: the
  field has not looked rather than looked and differed.
title: 'Train without a learning-rate schedule: average the iterates so no stopping time need be fixed'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    LIT-682 (ScheduleFree+, same author) added as a second source.
    Its admissions changed two passages. "No additional hyperparameter" was
    false at scale: plain Schedule-Free hits a cliff at 2M-token batches
    without inner momentum, and its small weight decay was compensating for
    gradient-norm drift. And the comparison against WSD has now been run by
    the method's author, not by an outside group. The promote_when is not
    met, because ScheduleFree+ is a different optimizer and stops at 1B/1T.
    Status and consensus are unchanged.
tags:
- training-optimization
date: '2026-09-07'
source:
# The paper is the only evidence there is. Filed as a list because the
# practice that later gains a replication needs somewhere to put it
# (ADR-010) — and gaining one is exactly what promote_when is waiting for.
- LIT-213
- LIT-682
introduced_by:
- LIT-213
implementations:
- 'facebookresearch/schedule_free'
summary: >-
  Defazio et al. (2024), [LIT-213](../literature.d/LIT-213.md) — scheduling and iterate averaging
  are one mechanism, and the averaged form needs no stopping time T, no
  schedule shape and no hyperparameter beyond what AdamW already has. Filed
  `Proposed`: the evidence is a third-party competitive benchmark at
  workloads far below the scale where this record's schedule question is open.
---

# SOTA-156: Train without a learning-rate schedule: average the iterates so no stopping time need be fixed

## Source

Defazio et al. (2024), [LIT-213](../literature.d/LIT-213.md) — [ARXIV-2405.15682](https://arxiv.org/abs/2405.15682).

Every schedule in this record works around the same fact: a schedule that
knows the stopping step T outperforms one that does not. Cosine handles it by
fixing the token budget in advance; warmup-stable-decay ([SOTA-140](SOTA-140.md)) handles it
by deferring the decay so the budget can stay open. Schedule-Free removes the
dependency instead. The method follows from a theory unifying scheduling and
iterate averaging as the same operation, and the averaged form is the one
that does not need to know when it will stop.

What you actually run is Schedule-Free AdamW: no schedule and no warmup shape
to pick. The original paper said no hyperparameter beyond AdamW's either, and
at scale that did not hold. See the large-batch and weight-decay conditions
below.

## Conditions, and what is not established

The evidence is one paper, and its strongest part is external: Schedule-Free
AdamW was the core of the winning entry to the **MLCommons 2024 AlgoPerf
Algorithmic Efficiency Challenge, Self-Tuning track** — a third-party
benchmark with fixed rules, which is a different kind of claim from a
self-reported sweep, and results span convex problems to large-scale deep
learning.

It is also the reason this is `Proposed` rather than `Active`. AlgoPerf's
workloads top out far below the scale at which [LIT-131](../literature.d/LIT-131.md) and [LIT-145](../literature.d/LIT-145.md) disagree
about schedules at all, so a win there is evidence about robustness under
fixed rules, not about behaviour at 2.8T. No frontier training report in this
record trains under it.

One comparison is specifically *not* established and should not be read in:
whether Schedule-Free was measured against a tuned warmup-stable-decay arm.
The paper's case is made against schedules that fix T; [SOTA-140](SOTA-140.md)'s case is
that WSD does not have to. Both claim the open budget. [LIT-682](../literature.d/LIT-682.md) has
since run them against each other, from 120M to 2B, and WSD lost at every
size. But the arm that won was ScheduleFree+, not Schedule-Free AdamW. It is
a package with inner momentum, Polyak steps and AdamC weight decay, set
against AdamW arms, by the method's own author. So it is a comparison, but
not the independent one this practice's `promote_when` asks for.

**Large batch: restore inner momentum.** The original removed the base
optimizer's momentum. ScheduleFree+ reports that without it Schedule-Free
"hits a scaling 'cliff' at 2M tokens per batch", where AdamW's cliff is at
4M. Its cleanest single-variable result (Fig. 3a, 120M) is that β1 = 0.9
removes the cliff. The original's experiments ran at batch sizes too small to
see it.

**Weight decay is not AdamW's.** The original's best results needed an
"unusual" small weight decay. By its author's later account, that was
"compensating for gradient norm drift, in a somewhat hacky way": averaging
shrinks the weight norm and so raises the effective learning rate. The fix
in ScheduleFree+ changes the weight decay to an AdamC-style one with values of
5–50. Either way, do not carry over AdamW's weight decay unchanged.

## Against [SOTA-140](SOTA-140.md), which is the practice this would displace

The overlap is exact and the mechanism is not. [SOTA-140](SOTA-140.md)'s headline practical
property is that the total token count need not be fixed when training
starts, because the decay can be launched from any stable-stage checkpoint.
Schedule-Free delivers the same property with no decay phase to launch, and
without WSD's condition that the peak learning rate be re-tuned for a
constant stage — because there is no constant stage.

The two are not filed as `compared_against` each other, deliberately: that
relation records a comparison somebody *ran*, and this one has not been run.

## Known implementations

- `facebookresearch/schedule_free`; the winning MLCommons 2024 AlgoPerf
  Self-Tuning entry. No production training report in this record.
