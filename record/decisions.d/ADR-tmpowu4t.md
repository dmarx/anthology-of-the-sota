---
status: Proposed
title: 'The topic vocabulary has four recurring seams — options, not a decision'
version: 1
tags:
- taxonomy
date: '2026-09-09'
issue: '#107'
summary: >-
  [ADR-021](ADR-021.md) said to expect a fourth vocabulary decision. Declaring the relations
  the practice bodies argue produced 25 unbound edges, and they are not
  scattered: four topic pairs account for eighteen of them. This states the
  evidence and four options, and decides nothing — the choice is which kind of
  claim the vocabulary is failing to name, and that is a judgement about the
  subject rather than about the record.
---

# ADR-tmpowu4t: The topic vocabulary has four recurring seams — options, not a decision

## Context

[ADR-021](ADR-021.md) widened the practice vocabulary from seven topics to ten and closed
by naming the pattern: three decisions in a row about the same vocabulary,
governing a corpus that had grown past what it was written for. "Expect a
fourth."

The evidence for a fourth arrived from a direction that decision did not
anticipate. Working the [#107](https://github.com/dmarx/anthology-of-the-sota/issues/107) backlog put a body on 90-odd practices, and the
bodies kept arguing lineage — this builds on that, this is the same principle
from another source, this contradicts its own citation. Declaring those
relations in frontmatter took `docs/practice-lines.md` from 13 lines to 34 and
produced **25 unbound relations**: joins where the two documents share no
primary topic.

An unbound edge is not a defect. It is the finding the invariant was declared
to produce ([ADR-022](ADR-022.md)) and it usually means the vocabulary is short a word rather
than that the relation is wrong. What makes this a decision rather than a
worklist is that the failures repeat at the same seams:

| edges | seam |
|--:|---|
| 7 | `attention-techniques` / `model-architecture` |
| 5 | `distributed-optimization` / `model-architecture` |
| 3 | `model-stability` / `training-optimization` |
| 3 | `attention-techniques` / `systems-optimization` |

Eighteen of twenty-five, in four pairs. The remaining seven are singletons and
read like ordinary cross-topic work.

## What each seam is

**Attention against architecture (7).** Attention variants are architecture
decisions, and the vocabulary makes them a separate topic. Every line running
from an attention mechanism to the model it sits in crosses this.

**Distributed against architecture (5).** Sharding, parallelism degree and
batch size are architecture decisions once the model is large enough that they
determine what can be built. The topics separate the deployment from the
design, and the practices do not.

**Stability against training-optimization (3).** A monitoring practice splits
by whether it is read as being about the model or about the run — `SOTA-069`
(watch `exp(loss)`) and `SOTA-098` (watch validation loss) are the same act,
filed on opposite sides.

**Attention against systems-optimization (3).** The sharpest one. A fused
attention kernel is *both*: `SOTA-085` (use flash attention) is
`attention-techniques`, `SOTA-083` (hand-write critical kernels) is
`systems-optimization`, and the deciding factor is whether the practice's
source was an attention paper or a compiler paper. That is provenance leaking
into taxonomy.

## Options

**1. Add a topic for the kernel level.** Something like `kernels-and-scheduling`:
the claim about how an operation is *executed* on hardware, as distinct from
what operation the architecture calls for. Takes the fourth seam directly and
some of the second. Costs a fourth vocabulary decision in a row, and the
category is one most sources would not recognise as their subject.

**2. A filing rule instead of a topic.** State that a practice files under the
layer it *acts on*, not the field its source came from — a fused kernel is a
systems practice whatever paper introduced it. Cheap, needs no vocabulary
change, and would move perhaps half the straddling practices. It does not
help the first seam, where both readings are about the model.

**3. Relax `exactly-one` to `at-most-two`.** Lets a practice carry both topics
and binds most of these edges immediately. It also gives up what the
constraint buys: [ADR-003](ADR-003.md)'s one-primary rule is what makes the topic a *choice*
rather than a label set, and the derived `primary_topic` ([ADR-022](ADR-022.md)) reads the
first tag, so a second primary would need an ordering rule nobody would
remember.

**4. Accept the seams and stop treating them as findings.** Declare that
lineage legitimately crosses topics and narrow the invariant to the chains
where it does not — or drop it. Honest, and it discards the signal that
produced this document.

## What this decision is not

It is not a proposal to retag anything now. Two of the straddling practices
are already flagged for restatement on other grounds — `SOTA-060`'s title
merges two initialisation conventions, `SOTA-083` inverts its own source — and
retagging a practice whose claim is unsettled would tidy the symptom.

One retag did happen while this was being written, and it is the case that
shows why the rest are held.
<!-- inactive-ok: SOTA-130 — Proposed; named as the mis-tagged document this paragraph is about, not cited as advice -->
`SOTA-130` (skip the reasoning SFT stage) carried
`training-optimization` while the two practices it is a variation of and a
rival to — `SOTA-129` and `SOTA-126` — both carry `adaptation-and-tuning`. That
is not a seam in the vocabulary; it is one document filed wrong, and the
evidence is that the correct topic already existed and its siblings already
used it. The tell is worth naming: the mis-tag is *why the relation had never
been declared*. An edge that would have bound had the tag been right does not
appear in this report at all, so the twenty-five here are a floor. Where the
right topic exists and the neighbours agree, fix it; where the argument is
about which topic should exist, that is this decision.

It is also not a claim that ten topics is the wrong number. Three of the four
seams involve `model-architecture`, which may mean that topic is doing too
much rather than that a topic is missing.

## Consequences

Whichever option is taken, the unbound-lineage report is the instrument that
found this and should keep running: the count is not the signal, the
*repetition* is. A single new seam appearing three times is worth reading; a
one-off crossing is ordinary work.

If nothing is decided, the record still has the relations, which is the larger
gain — 103 of 189 practices now declare one, against 36 before this pass, and
the lines are readable whether or not their edges bind.
