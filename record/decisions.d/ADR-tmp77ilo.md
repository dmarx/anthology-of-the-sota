---
status: Proposed
title: 'capability-thresholds: whether a capability arrives abruptly is a claim, not a method'
version: 1
tags:
- taxonomy
- record
date: '2026-09-23'
issue: '#311'
summary: >-
  A nineteenth topic, `capability-thresholds`, for a capability that arrives
  abruptly rather than smoothly — emergence at scale, grokking, phase
  transitions — and the dispute about whether the discontinuity is real.
  `analysis-and-evaluation` was holding all nineteen such documents and is a
  word for methods, not for claims about the world. Rejected: leaving them
  there, which made the record's largest live controversy unbrowsable; and
  `emergence`, which names one axis of three.
---

<!-- inactive-ok-file: THEORY-072, THEORY-073, THEORY-074, SOTA-325, ADR-055 —
     all Proposed. The four THEORY/SOTA codes are named as the DOCUMENTS this
     decision retags or declines to retag, which is what a taxonomy decision
     has to enumerate; ADR-055 is cited for its rule about tag order, which
     holds whatever its own status. None is cited as a recommendation. -->
# ADR-tmp77ilo: capability-thresholds: whether a capability arrives abruptly is a claim, not a method

## Context

`luria` [#311](https://github.com/dmarx/luria/issues/311) made unbound relations a lint class, which put the `practice`
chain's one unbound line in front of a reader for the first time:

```
SOTA-036, SOTA-037, SOTA-038, SOTA-279, SOTA-280, SOTA-281
share no `tags` across the whole line
```

Reading it did not produce a tag for that line — [the diagnosis there is a
relation carrying two senses, and is separate work](#the-line-that-started-this). It produced a different
finding. Two of the six, `SOTA-037` ("LM in-context learning emerges at
scale") and `SOTA-279` ("...and only once the model is large enough; below
~100B it does nothing or hurts"), make a claim the vocabulary has no word for,
and a sweep for its siblings found **nineteen documents across all three
schemes**:

- the emergence debate itself — `LIT-470` *Emergent Abilities of Large
  Language Models* and `LIT-471` *Are Emergent Abilities a Mirage?*, with
  `THEORY-040` (a metric that composes or thresholds per-token error turns a
  smooth curve into a sharp one) and `SOTA-200` (check before believing it);
- the grokking line — `LIT-537`, `LIT-538`, `LIT-539`, `LIT-540`, `LIT-085`
  and `THEORY-069` through `THEORY-072`;
- the singular-learning-theory account of stagewise development — `LIT-543`,
  `LIT-544`, `THEORY-073` and `THEORY-074`.

**All nineteen carry `analysis-and-evaluation`, and for most it is the
primary.** That is the measurement: one topic absorbed an entire subject.

Its blurb is *"how to find out whether something worked — what to measure,
what a measurement cannot tell you, and which comparisons are unsound."* That
is a word for **methods**. "A capability appears above 100B parameters", "a
network generalises long after it has memorised", "the posterior changes phase
at n≈600" are claims about **what happens**. The dispute over whether an
emergent ability is real is a methodological argument, so
`analysis-and-evaluation` fits `LIT-471` and `SOTA-200` — it does not fit the
phenomenon they argue about, and filing both under one word makes the
disagreement invisible, which is the opposite of what this record is for.

## Decision

**A nineteenth topic: `capability-thresholds`.**

> a capability that arrives abruptly rather than smoothly — emergence at
> scale, grokking after long training, phase transitions in learning — which
> axis it turns on, and whether the discontinuity is real or an artefact of
> how it was measured

**One word, not three, and the axis is the reason.** Emergence turns on
*model scale*, grokking on *training time*, and an SLT phase transition on
*dataset size*. Three axes, and it is tempting to call them three subjects.
They are not: in every case the claim is that a curve has a knee, the argument
is whether the knee is in the phenomenon or in the plot, and the literature
already borrows across them — `THEORY-074` exists precisely to say that a
Bayesian and a dynamical transition are *different events*, a distinction that
is unstatable if each axis has its own topic. Naming the axis is the
document's job; naming the shape of the claim is the topic's.

**Nineteen documents retagged**, appended in every case but four. The four
primary moves are documents that are this claim and nothing else:

| document | why the primary moved |
|---|---|
| `LIT-470` | *Emergent Abilities of LLMs* — the paper that named the phenomenon |
| `LIT-471` | *Are Emergent Abilities a Mirage?* — the paper that disputed it |
| `LIT-538` | Power et al., the paper that named grokking |
| `THEORY-069` | the one `Active` grokking explanation; its whole content is that grokking is a regime |

Everywhere else `capability-thresholds` is appended, because
`primary_topic` derives `{tags[0]}` and a prepend silently refiles a document
([ADR-055](ADR-055.md)).

**What it does not take.** `SOTA-150` ("make the feed-forward layers a sparse
mixture of experts once the model is large enough to be compute-bound") is
conditioned on scale and is *not* this: the condition is an engineering
economics crossover, not a capability arriving. `LIT-542` (the Local Learning
Coefficient) and `SOTA-325` (measure degeneracy when the loss has saturated)
are the instrument and the method, and stay where they are. `THEORY-076`
(width scaling under the standard parametrization) is a training-dynamics
claim about a limit, not about a knee. Writing these down is the point: a
topic whose boundary is not tested is a topic that will absorb its neighbours,
which is how `analysis-and-evaluation` got here.

## The line that started this

It does not fix the line. `SOTA-037` and `SOTA-279` take the new tag;
`SOTA-036`, `SOTA-038`, `SOTA-280` and `SOTA-281` correctly do not, so the
intersection is still empty. That is the honest outcome and it is worth
stating, because the tempting move — reach for a word that makes the warning
go away — is the failure the vocabulary's own `alert` names. The line's actual
defect is that `extends` licenses three senses, one of which ("a rule that
only exists because the earlier one is followed") cannot preserve subject by
construction; that is its own decision and its own work.

## Alternatives considered

- **Leave them in `analysis-and-evaluation`.** Status quo, and the cost is
  measurable rather than theoretical: the record holds the field's largest
  live controversy about learning dynamics — three independent accounts of
  grokking, an emergence claim and its rebuttal, and a formal theory of
  staged development — and a reader browsing by topic cannot find it, because
  it is filed under the same word as "state the token count beside any
  reconstruction FID".
- **`emergence`.** The obvious name, and it smuggles in the answer. The whole
  dispute is whether "emergent" describes the model or the metric
  (`LIT-471`), and a topic asserting the contested reading would put the
  record on one side of an argument it is supposed to hold both sides of.
  `capability-thresholds` is neutral about whether the threshold is real, and
  the blurb says so explicitly.
- **Three topics, one per axis.** Splits `THEORY-074` — whose entire claim is
  that two of the axes are different events — across two topics that then
  cannot state the relation. It would also file the metric-artefact argument
  three times, once per axis, when it is one argument.
- **A broader `learning-dynamics`.** It would take these nineteen and another
  sixty besides — edge of stability, loss curves, warmup, the whole training
  half of the corpus — which is `training-optimization` with a different name.
  A topic most of the corpus could hold asserts nothing.
- **Wait for the domain/kind vocabulary split.** `LU-#298` would let `topics`
  be a union of sub-vocabularies, and a reasonable reading is that all of this
  should wait for it. It should not: `capability-thresholds` is a **kind of
  claim**, so it belongs in the kinds vocabulary whichever way that lands, and
  nineteen documents are mis-filed today.

## Consequences

**`analysis-and-evaluation` gets smaller and sharper**, which is the point,
and no document leaves it — every one of the nineteen keeps it, because the
methodological reading is real and additional. Fifteen of them gained a tag;
four were refiled.

**The topic is now nineteen and the count is written in four places.** This
decision updates `luria.yaml`'s header comment, the vocabulary's own `blurb`,
and the two sentences in `CLAUDE.md` that say "eighteen". The dated records —
curation entries and changelog fragments — keep their number, because they
were true when written.

**A boundary this sharp will be tested by the next filing**, and the test to
apply is the one in `CLAUDE.md`: would someone browsing `capability-thresholds`
be right to expect this document? A scale-conditioned *recommendation* is not
automatically a threshold *claim*, and `SOTA-150` is the worked example of the
difference.
