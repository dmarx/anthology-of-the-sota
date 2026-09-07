---
status: Proposed
title: 'What `source:` holds, and what the Source section is for'
version: 1
tags:
- record
date: '2026-09-07'
issue: '#63'
summary: >-
  [ADR-010](ADR-010.md) made `source:` a list without saying what fills it, so the corpus
  grew two conventions: [SOTA-132](../practices.d/SOTA-132.md) counts adopters as support, [SOTA-150](../practices.d/SOTA-150.md) counts
  them as consensus data. This settles it — `source:` holds work that produced
  evidence about the claim, and adoption without a test is consensus data,
  which `consensus.yaml` already implies by admitting adopters who did not
  choose deliberately. The Source *section* is argument and may name
  non-sources, so prose is not a subset of the field; the field is a subset of
  the prose, which is checkable and found three defects. Rejected: adopters as
  support, a subset lint in the other direction, and leaving it undecided.
---

# ADR-tmpudmra: What `source:` holds, and what the Source section is for

## Context

[ADR-010](ADR-010.md) made `source:` a list, and its argument was countability: a reader
should be able to tell "rests on one unreplicated claim" from "rests on four
independent groups". It did not say what fills the list.

Two conventions grew in the gap, and both are defensible readings.

**[SOTA-132](../practices.d/SOTA-132.md) counts adopters as support.** Its `source:` comment says so:

> Primary: the controlled comparison against full attention. The rest is what
> corroborates it — the shipped 3:1 layouts and the module they use
> ([ADR-010](ADR-010.md)).

**[SOTA-150](../practices.d/SOTA-150.md) counts adopters as consensus data.** Its `source:` holds five
origin papers; the adopters are in its `consensus_note`:

> Four labs and every frontier model the record holds from 2024 on: DeepSeek
> ([LIT-160](../literature.d/LIT-160.md), [LIT-139](../literature.d/LIT-139.md)), Moonshot ([LIT-132](../literature.d/LIT-132.md), [LIT-131](../literature.d/LIT-131.md)), Alibaba ([LIT-182](../literature.d/LIT-182.md), [LIT-136](../literature.d/LIT-136.md))
> and NVIDIA ([LIT-183](../literature.d/LIT-183.md)).

Under two conventions the list is not countable, which is the property [ADR-010](ADR-010.md)
was filed to get. `SOTA-150` reading `converged` on five sources and
`SOTA-132` reading its value on six mean different things, and only a reader
who opens both can tell.

The cost came due in [#58](https://github.com/dmarx/anthology-of-the-sota/issues/58). That pass needed a rule and there was none, so
one was invented mid-pass — *if this paper were retracted tomorrow, would the
practice need rewriting?* It works. It was also nowhere a contributor would
look, and thirteen practices were corrected under a rule that existed in a
commit message.

**Two attempts to mechanise it failed, and the failures are the useful part.**
Measured against the corpus:

| candidate check | fires | why it is wrong |
|---|---|---|
| codes in `consensus_note` / `promote_when` ⊆ structured fields | 22 | `SOTA-122`'s `promote_when` names `LIT-153` *precisely to say it does not count* |
| codes in the `## Source` section ⊆ `source:` | 17 | `SOTA-124`'s Source section names `LIT-166` and `LIT-175` as the positions it argues with |

Neither violation is always wrong. A check written before this decision would
have enforced whichever convention its author held and generated false
findings against the other half of the corpus.

## Decision

**`source:` holds the work that produced evidence about the claim.** The test,
promoted from [#58](https://github.com/dmarx/anthology-of-the-sota/issues/58)'s practice to the record's rule: *if this document were
retracted, would the practice need rewriting?* That admits the origin of the
claim and independent corroboration of it. It excludes contrast, alternatives,
components that have practices of their own, and asides.

**Adoption without a test is consensus data, not support.** This is the
disagreement above, and `consensus.yaml` already contains the answer. Its
blurb for `converged` reads:

> the field agrees and dissent is marginal, **whether or not each adopter made
> the choice deliberately**

A non-deliberate adopter is evidence about the field, not evidence about the
claim. Ten laboratories shipping a design is not ten results; it is one
belief, held ten times. So the line is not *who* published but *what they
did*: a report that ran the comparison is a source, and a report that shipped
the design is consensus data. Kimi Linear ablating NoPE against RoPE at
matched configuration is a source. Qwen shipping a 3:1 interleave without
reporting the alternative is not.

**`consensus_note` may name work absent from `source:`, and that is the
division of labour rather than a defect.** It follows that [ADR-010](ADR-010.md)'s
countability claim needs restating: consensus is countable against sources
*and* adopters, not against `source:` alone. What makes it countable at all is
a group count, which this record does not store — filed upstream as
[luria#209](https://github.com/dmarx/luria/issues/209).

**The `## Source` section is argument, not enumeration.** It says what each
source contributes and how they fit, and it may name non-sources provided it
names them as such — `SOTA-124` naming the position it argues with is correct
prose and correct filing at once. So the prose is *not* a subset of the field.

**The field is a subset of the prose.** Every declared source must be
discussed somewhere in the body. A source the document never explains is a
source no reader can evaluate and no later contributor can re-triage, and it
is the one direction that is always wrong.

## The check that follows

`source:` ⊆ codes cited in the body. Measured before adopting it: **150 of 153
practices already satisfy it**, and all three exceptions are real defects.

- `SOTA-109` sources `LIT-100` and its body cites only `LIT-024`, the design
  it replaced. The paper the recommendation comes from is named in the field
  and nowhere in the prose.
- `SOTA-121` — "use Muon" — sources `LIT-159`, the work that introduced Muon,
  and never mentions it.
- `SOTA-150` sources `LIT-160` and never mentions it.

Three for three, on a corpus of 153, against a rule that holds 98% of the time
without anyone having stated it. That is the profile a lint wants and the two
rejected candidates did not have.

## Alternatives considered

**Adopters count as support.** `SOTA-132`'s convention, and the one that
looks right: a design running in four frontier models plainly *is* evidence of
something. It loses because of what it is evidence *of*. A converged practice
would accumulate every model report that ships it, `source:` would become a
roster, and the question a reader actually brings — which paper should I read
— would drown in it. `consensus.yaml`'s own admission that adopters may not
have chosen deliberately is the record already conceding the point.

**A subset lint in the prose→field direction.** The obvious mechanisation,
tried twice, rejected on measurement rather than taste: 22 and 17 false
findings respectively. Recorded here because it will look like a good idea
again — the intuition that prose naming a paper implies the field should too
is exactly wrong in a record whose documents argue with the literature.

**Annotated references, so the section can be generated.** The reason the
Source section is hand-written is that the field cannot carry the qualifier;
*"Hägele et al., for the comparison against cosine"* is the load-bearing half.
Structuring the qualifier would make drift impossible rather than detectable.
Not taken here, because luria's [ADR-011](ADR-011.md) says **do not add a qualifier to the
relation** — a condition beside a checked reference is prose in a data field,
so nothing evaluates it and nothing notices when it stops holding. A
descriptive note is not a condition, and the distinction may hold, but
re-opening that line deserves its own argument.

**Leave it undecided.** The status quo, and it has a running cost: [#58](https://github.com/dmarx/anthology-of-the-sota/issues/58) is
correcting a quarter of the registry under a rule invented for the occasion,
and the next pass would invent a different one.

## Consequences

The rule reverses one change made the same day it was written, which is the
clearest evidence it decides something. `SOTA-142` gained `LIT-119` under
[#62](https://github.com/dmarx/anthology-of-the-sota/pull/62) on the strength of its own sentence — Falcon-H1-Tiny "is the record's
independent adoption ... which is what moves this from one group's result to a
practice". Under this decision that adoption moves the *consensus* and not the
evidence, because Falcon-H1-Tiny used the power law rather than testing it.
Corrected in the same contribution.

`SOTA-132`'s shipped-layout entries are the remaining case and are left to
[#58](https://github.com/dmarx/anthology-of-the-sota/issues/58), which is still working through the architecture cluster.

Three practices gain a sentence about a source they had been declaring in
silence.

What this obliges: a practice that adds an adopter must ask whether the
adopter ran the comparison, and the answer belongs in the prose either way.
That is a judgement per source, which is the cost of having the list mean one
thing.
