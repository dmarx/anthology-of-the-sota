---
status: Active
consensus: unassessed
consensus_note: >-
  Nobody has assessed where the field stands on this, and the record cannot
  cite a paper that measured the size of the effect. What it can cite is one
  search that did not hold anything out, published its own selection standard,
  and published the population statistics that let a reader see what the
  standard was worth. That is an instance, not an assessment, and the value
  says so.
title: 'Evaluate a search on tasks held out of its own fitness function, and report the gap against the tasks it selected on'
version: 1
tags:
- analysis-and-evaluation
- model-architecture
date: '2026-09-21'
source:
- LIT-493
# Deliberately empty, and the empty list is the claim: this record looked for
# the work that first stated the recommendation and could not name one. It is
# NOT the ADR-030 ambiguity that field was made required to remove — "the
# origin is the primary source" would be LIT-493, which is false, since
# Genesys is an instance of the failure and states no such recommendation.
# The gap is real and is what #241 stays open for. See ADR-tmpvlp2h.
introduced_by: []
implementations: []
summary: >-
  No source states this; it is filed on a priori grounds with one instance.
  Cheng, Clark and Richardson (2025), [LIT-493](../literature.d/LIT-493.md), searched 1,062
  pretrained designs against a fitness function of average downstream accuracy,
  then reported the top five on nine benchmarks drawn from the same pool and
  chosen — per its own Table 16 — for **largest standard deviation across the
  search population**. The best discovered design beats the best seed by
  **0.03** points.
---

<!-- inactive-ok-file: ADR-tmpvlp2h ADR-030 SOTA-256 SOTA-304 — all Proposed.
     ADR-tmpvlp2h is filed in this same contribution and is what permits this
     practice's empty `introduced_by:`; ADR-030 is named as the decision it
     amends, which is the opposite of citing it as settled. SOTA-256 and
     SOTA-304 are both named to say what this practice is NOT — the two
     nearest documents in the corpus, distinguished rather than relied on. -->

# SOTA-tmp0obtv: Evaluate a search on tasks held out of its own fitness function, and report the gap against the tasks it selected on

## Source

This practice has no source that argues for it, and its `introduced_by:` is
empty rather than filled with the paper below. Both are deliberate, and the
reasons are different from each other.

Cheng, Clark and Richardson (2025), [LIT-493](../literature.d/LIT-493.md) — read as
[NOTE-242](../notes.d/NOTE-242.md) — is cited as the **instance that made the gap visible**,
not as evidence for the recommendation. Genesys does not recommend holding
tasks out; it is a search that did not, and it published enough of its own
numbers that a reader can see what that cost. Citing it for the instance is
honest; citing it for the claim would not be, which is why `introduced_by:` is
empty and [ADR-tmpvlp2h](../decisions.d/ADR-tmpvlp2h.md) exists to say what an empty one means.

The recommendation itself rests on a fact about maximization rather than on a
measurement: the maximum of many noisy estimates is a biased estimate of the
maximum of the underlying quantities, and the bias grows with how many
candidates you took the maximum over. That is arithmetic. What nobody in this
record has measured is **how large it gets in this setting**, which is the
difference between knowing the sign and knowing the size.

## When this applies

You ran a search — over architectures, hyperparameters, data mixtures,
prompts, scaffolds, anything where a procedure proposes candidates and a
fitness function ranks them — and you are about to report how good the winners
are.

It applies with equal force to a search you ran by hand. A researcher who
tried forty variants and reports the best one on the metric they were watching
has done the same thing with a smaller `N` and no Table 16.

## Do this

**Name the fitness function in the paper, as a function.** What it scores,
over which tasks, aggregated how. This costs a sentence and it is what makes
everything below checkable by a reader.

**Hold tasks out before the search starts, and never let them into the loop.**
Not at selection time, not for early stopping, not for deciding which
checkpoint to keep, not for choosing which benchmarks to report. A task that
influenced any decision inside the search is part of the fitness function
whether or not it appears in its definition.

**Report both numbers and their difference.** Winners on the selected tasks,
winners on the held-out tasks, and the gap. The gap is the finding — it is the
only number in the paper that estimates how much of the improvement was
selection — and a search that reports it is making a stronger claim than one
that reports a higher score.

**Compare against the population, not only against baselines.** Publish the
candidate-to-candidate spread on every benchmark you report, so a reader can
put the margin next to it. Genesys does this, in Table 16, which is why its
own weakest claim is checkable from its own paper.

## The instance, and what it shows

Fitness is average downstream-task accuracy. 1,062 designs were pretrained and
verified at 14M–350M parameters. The five best were then reported on nine
benchmarks drawn from the same verification pool, selected by the standard the
paper states in Table 16: **largest standard deviation across the search
population**, and **best design beating random by over 5%**.

So the selection happens twice, and the second time is the unusual one. The
designs are chosen for scoring well on the pool; then the benchmarks are
chosen for being the ones the population spreads out on. A benchmark picked
because designs differ on it is, by construction, one where the best of 1,062
sits far above the middle.

What the paper's own tables then show:

| | average over the nine |
|---|---|
| best seed architecture (GPT) | 61.78 |
| best discovered design (Geogate) | **61.81** |
| five discovered designs, mean | **60.17** |
| five seed architectures, mean | **60.77** |

A margin of **0.03** at the top, and the discovered five average slightly
*below* the architectures they were bred from.

**An order-of-magnitude check, which is this record's arithmetic and not the
paper's.** Table 16 gives a design-to-design standard deviation of 0.0138 on
CoLA and SST2. If scores on such a benchmark were independent draws around a
population mean — they are not, and the fitness function selects on the
average rather than per-benchmark, so this overstates the effect — the
expected best of 1,062 draws sits about `sqrt(2 ln 1062)` ≈ 3.7 standard
deviations above that mean, which is around five points. The margins actually
reported on those two benchmarks run from half a point to two and a half.
The point is not that five points is the right number. It is that the
selection effect available on a benchmark chosen for its spread is of the same
order as, or larger than, the effect being reported, and no number in the
paper separates them.

## Why `Active` with no evidence behind it

Because the direction is not in question and the conditions are the whole
content. A practice is `Proposed` here when the record does not know whether
the recommendation is right. The record does know this one is right — a
comparison that shares a statistic with its own selection step is inflated,
which follows from what selection is — and holding tasks out costs a partition
made before the search rather than a second experiment.

What is unknown is the magnitude, and magnitude is what `consensus:` and the
conditions below are for. `unassessed` is the honest reading: nobody has
looked at what the field does here.

This is the record's first practice filed with an empty `introduced_by:`, and
the general form of the argument — selecting on a statistic and then reporting
it inflates the comparison — is far older than any paper in this corpus, is
standard in statistics, and is well known in the NAS and AutoML literature.
The record simply does not hold the paper that quantifies it. That is a gap in
the corpus and not a reason to leave the shelf empty.

## Conditions

**The size of the effect is unknown, here and generally.** Nothing in this
record estimates it. The practice tells you to produce the number; it cannot
tell you what to expect, and anyone claiming a typical magnitude is
extrapolating.

**Held-out tasks are not free.** A partition reserved before the search is
capacity the search does not get to use, and for a small verification pool
that trade may not be worth making. Say which choice you made.

**"Held out" is a property of the process, not of the task list.** Tasks
reserved at the start and then consulted once to decide which of two search
variants to publish are no longer held out. There is no way to check this from
outside, which is why naming the fitness function matters more than it looks.

**This is not the contamination problem, and not the reproducibility
problem.** Benchmark contamination is about training data overlapping test
data; this is about a *selection procedure* sharing a metric with its own
evaluation, and it happens with a perfectly clean split. It is also not
[SOTA-210](SOTA-210.md)'s or [SOTA-256](SOTA-256.md)'s shape: both of those say report the
other number, where this says do not measure with the thing you selected on.

**Genesys reports its own weakest claim honestly**, and the practice should
not be read as an accusation. Table 16 is published, the selection standard is
stated in the paper, the checkpoints are online, and the abstract says
"percentage point" where a less careful paper would have said "15×". A paper
that hands a reader the instrument to check it is the reason this gap could be
named at all — [DP-004](../../docs/design-principles.md#dp-4), since the query that found it was shaped like
the paper's own appendix. The separate practice taken from Genesys is
[SOTA-304](SOTA-304.md), and it is about code generation.

## What would put a measurement under this

Named in [#241](https://github.com/dmarx/anthology-of-the-sota/issues/241), which stays open. The designs, code and training runs are
public at `genesys.allen.ai` and `github.com/allenai/genesys`: score the five
discovered designs on tasks the fitness function never saw and report the gap
against Table 5. That is one evaluation run against published checkpoints, and
it would turn this instance into evidence — for this search, at least, which
is still not a general magnitude.

Failing that, the NAS and AutoML literature that quantifies search-phase
inflation is the `source:` this document wants, and filing it is what would
fill `introduced_by:`.

## Known implementations

None recorded. Reporting a held-out gap is rare enough in the searches this
record holds that an example would be worth filing on its own.
