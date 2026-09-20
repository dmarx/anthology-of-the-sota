---
number: 29
status: Proposed
formerly:
- THEORY-tmpijbl9
promote_when: >-
  A demonstration that the discontinuity appears for something other than
  factual memorisation — a capability, a skill, a benchmark — which is what
  the knapsack account predicts and what would separate it from a story about
  memorisation specifically. Or an intervention that manipulates capacity
  directly at fixed mixing ratio and moves the threshold where the account
  says it should. What would not settle it: another measurement of a
  threshold in this same setting, which establishes the phenomenon again and
  not the explanation.
title: 'A model of bounded capacity allocates it across datasets like a knapsack, so the optimum jumps rather than sliding'
version: 1
tags:
- training-optimization
date: '2026-09-20'
source:
- LIT-451
explains:
- SOTA-268
summary: >-
  Gu et al. (2025), [LIT-451](../literature.d/LIT-451.md) — a model with bounded capacity training
  on a mixture must decide how much capacity each dataset gets, and the
  allocation minimising total loss is a discrete choice. A discrete optimum
  moves discontinuously when its inputs move continuously, which is why
  knowledge acquisition has thresholds in model size and mixing ratio rather
  than the smooth scaling the single-dataset case shows.
---

# THEORY-029: A model of bounded capacity allocates it across datasets like a knapsack, so the optimum jumps rather than sliding
<!-- inactive-ok-file: THEORY-025 — Proposed, and the single-claimant case this account generalises -->
<!-- inactive-ok-file: SOTA-268 — Proposed, and filed in this same contribution as the practice this explains; also named in `explains:` -->

## Source

Gu et al. (2025), [LIT-451](../literature.d/LIT-451.md) — [ARXIV-2505.18091](https://arxiv.org/abs/2505.18091).

## What was actually shown

The empirical half is two thresholds, measured on Pythia models from 14M to
6.9B with synthetic biographies mixed into FineWeb-Edu or the Pile. At a
fixed mixing ratio, accuracy on the biographies stays at zero as the model
grows and then jumps past a critical size to over 60%. At a fixed model size,
the same happens as the mixing ratio rises.

**The control is what makes this a threshold rather than slow learning:**
below the critical ratio, extensive further training does not help. And the
contrast case is what makes it a property of mixing: the same dataset trained
on alone gives the smooth linear law prior work established.

The account offered is that a model has bounded capacity, is minimising
overall test loss, and must therefore choose how much capacity each dataset
gets. That is a discrete allocation problem — a knapsack — and the solution
to a discrete problem moves in jumps when its inputs move continuously. It is
formalised information-theoretically, and it yields a prediction that holds:
the critical mixing ratio follows a **power law in model size**.

That the prediction is quantitative and comes out right is the strongest
thing here. An account that only said "expect discontinuity" would fit the
data without risking anything.

## What this makes sense of

**Why a mixing recipe does not transfer across scale** ([SOTA-268](../practices.d/SOTA-268.md)).
Not because small models are noisy estimates of large ones, but because the
two can sit on opposite sides of a transition, so the small run is measuring
a different regime's answer.

**Why the single-dataset laws looked so clean.** The linear scaling of
knowledge in model size was measured by training on knowledge-dense data
alone, where nothing competes for the budget. [THEORY-025](THEORY-025.md)'s fixed-bit-budget
picture is the same single-claimant case: fill the budget, then substitute
generalisation. Add a second claimant and the allocation between them is
where the discontinuity lives.

## What this does not say

**It does not say the mechanism is isolated.** The account is consistent with
the measurements and no intervention separates it from alternatives. An
optimisation story — the small dataset's gradient signal being swamped until
some threshold — would produce similar curves, and nothing here rules it out.
That is why this is `Proposed` while the phenomenon it explains is
well-measured.

**It does not say anything about more than two datasets.** The knapsack is
interesting precisely when many domains compete, and every experiment here
has one knowledge-dense dataset against one web corpus. Whether the
transitions compose, interfere or smooth each other out is untouched.

**It does not establish the scope it implies.** If capacity allocation is
what produces the jumps, the jumps should appear for capabilities, skills and
benchmarks — anything competing for the same budget — not only for countable
factual memorisation. That is the account's most testable consequence and
nobody has tested it.

**It does not license the fitted constants.** The power law for the critical
ratio is fitted from 14M to 6.9B on one mixture. The shape of the problem
transfers; the numbers do not.

**And it says nothing about a corpus you did not synthesise.** Countable
biographies are what make capacity allocation observable. Whether Wikipedia
at 0.1% of a corpus sits above or below its own threshold in any real
pretraining run is the question this raises and cannot answer.

## Why `Proposed`

The phenomenon is strong and the explanation is a good fit that has not been
pried apart from its rivals. What `promote_when:` asks for is the prediction
that would distinguish the capacity account from an optimisation one: the
discontinuity showing up somewhere that is not memorisation at all.
