---
status: Active
title: 'Benchmarks, model reports and infrastructure are literature, and the record files them'
version: 1
tags:
- record
date: '2026-09-15'
summary: >-
  The bibliography sweep found that benchmark papers, model and technical
  reports, and training or serving infrastructure are 9 of the 27 most-cited
  references the record lacks — GSM8K alone cited by 9 of 12 papers. Every
  pass had declined them silently and none had said why. They are admissible
  `LIT` documents: a note records a paper's standing in the anthology, and a
  benchmark the record's practices are argued on has standing.
---

# ADR-tmpf2vie: Benchmarks, model reports and infrastructure are literature, and the record files them

## Context

The bibliography sweep over the twelve evolution-strategies papers extracted
144 distinct arXiv identifiers and found 117 of them absent from the record.
Ranked by how many of the twelve cite each, a category appears repeatedly near
the top and had never been discussed:

- **Benchmarks and datasets** — GSM8K (9 of 12), MBPP (3), HellaSwag, ARC-C,
  GPQA, MATH, MATH-500, HumanEval, WinoGrande, ROCStories, OlympiadBench,
  Countdown.
- **Model and technical reports** — the Qwen2.5 technical report (4 of 12),
  DeepSeek-V3, Llama, OLMo.
- **Infrastructure** — verl / HybridFlow (3 of 12), Brax, and the RL
  environment suites.

Nine of the twenty-seven most-cited missing references are one of these three.

**The record was already half-doing it, inconsistently.** [LIT-119](../literature.d/LIT-119.md)
(Falcon-H1-Tiny), [LIT-130](../literature.d/LIT-130.md) (Olmo 3) and [LIT-222](../literature.d/LIT-222.md) (the CoreWeave training
benchmarks whitepaper) are already `Active` notes, and the practice registry
cites model reports as adoption evidence throughout. What had never been filed
was the benchmark and infrastructure end — not by decision, but because no
pass had a reason to and none wrote down that it was declining them.

That is precisely the failure [DP-008](../../docs/design-principles.md#dp-8) describes: a scope boundary that exists
in what the corpus happens to contain rather than in anything anyone decided,
invisible because a subject the list cannot express produces nothing rather
than an argument. And [DP-009](../../docs/design-principles.md#dp-9) says which way to lean when a claim arrives with
nowhere to go: **treat it as evidence about the categories until someone shows
otherwise.**

## Decision

**Benchmarks, datasets, model and technical reports, and training or serving
infrastructure are admissible `LIT` documents.** The record files them.

The argument is the scheme's own definition. A `LIT` note records **a paper's
standing in the anthology** — not whether it contains a recommendation, which
is the `SOTA` scheme's business, and not whether it explains something, which
is `THEORY`'s. A paper the record's practices are argued on has standing. Two
consequences that were already true and unstated:

- **A practice's evidence is bounded by the benchmark it was measured on.**
  [SOTA-210](../practices.d/SOTA-210.md) says report pass@k as well as pass@1 and rests on results
  measured on GSM8K, MATH-500 and OlympiadBench. What those benchmarks
  measure, and what they are known to be insensitive to, is part of what that
  practice claims — and there is nowhere to write it down.
- **A model report is the adoption evidence `consensus:` is counted from.**
  [DP-005](../../docs/design-principles.md#dp-5) separates adoption from evidence and sends adoption to
  `consensus:`; the things being counted there are model reports, and the
  record has been counting documents it does not hold.

## What this does not decide

**It is not a mandate to file a benchmark catalogue.** The trigger for filing
remains the one the sweep supplies: **something in the record cites it.** A
benchmark nothing here is argued on has no standing to record, and filing one
would be the "category added to admit a single document" that [DP-008](../../docs/design-principles.md#dp-8)'s
corollary forbids — arrived at from the other direction.

**It does not change the topic vocabulary.** All three kinds fit the thirteen:
a benchmark paper is `analysis-and-evaluation` by its blurb's own terms, a
model report takes the topic of what it is a report *about*, and
infrastructure is `systems-optimization` or `distributed-optimization`. No new
word is needed, which is the test [DP-008](../../docs/design-principles.md#dp-8) sets for whether a scope change is
really a vocabulary change.

**It does not lower the bar for `SOTA` or `THEORY`.** A benchmark paper will
usually carry no practice and no explanation, and that is the normal case
rather than a defect — the same shape as [LIT-019](../literature.d/LIT-019.md) and [LIT-039](../literature.d/LIT-039.md), which say in
their own bodies that they carry no practice deliberately.

**It does not require a reading note.** Absence of a `NOTE` means the paper is
unread ([ADR-025](ADR-025.md)), and for a benchmark that is often the honest state: the
record may need to say what GSM8K is and what it does not measure without
anyone having read it closely enough to source a practice from.

## Consequences

**A backlog, named.** The sweep's ranking is the queue, and the top of it is
GSM8K (`ARXIV-2110.14168`, cited by 9 of 12), the Qwen2.5 technical report
(`ARXIV-2412.15115`, 4), MBPP (`ARXIV-2108.07732`, 3) and verl
(`ARXIV-2409.19256`, 3). Nothing is filed by this decision itself.

**The sweep gains a second purpose.** It was prescribed to find the papers a
filed work argues *with*. It also finds the benchmarks a filed work argues
*on*, and under this decision both are candidates.

**An honest cost.** The `LIT` scheme grows in a direction where most documents
will be short, carry no practice, and never be read closely. That is a
different kind of note from the ones the scheme was built for, and if it turns
out to dilute the reading list rather than ground it, the evidence will be a
`literature` index where most entries explain nothing — which is checkable,
and is the condition on which this decision should be revisited.

## Alternatives considered

**Keep declining them, and write that down instead.** Defensible: the record
is an anthology of practice, and a benchmark is an instrument rather than a
claim. Rejected because the record already holds model reports, already counts
them in `consensus:`, and already rests practices on benchmark results — so
the boundary would have had to be drawn between things the record treats
identically, and the only honest version of it would have removed documents
that are earning their place.

**Admit them as a separate scheme.** Rejected as the mechanism answering a
question it was not asked. The three schemes are distinguished by what a
document *is* — an instruction, an explanation, a paper's standing — and a
benchmark paper's standing is a paper's standing. A fourth scheme would be
splitting `LIT` by subject matter, which is what `tags:` is for.
