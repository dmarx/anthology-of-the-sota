---
status: Proposed
title: 'Fail the build on `source-mismatch`, and take the source invariant upstream'
version: 1
tags:
- mechanism
date: '2026-09-16'
summary: >-
  Two things about the check that binds a document to its paper. `fail_on`
  gains `source-mismatch` — at zero today, offline from the lockfile, and the
  check that would have failed the import in [#138](https://github.com/dmarx/anthology-of-the-sota/issues/138). And the invariant on
  `source:` that this decision first argued against is now argued FOR: a
  relation asserts a commonality and the invariant is how the record says
  what it is, which holds for a practice and its evidence as much as for two
  practices. It cannot be declared here yet — a chain over a cross-scheme
  relation raises `KeyError` in `luria index` — so it goes upstream with the
  measurement rather than being dropped.
---

# ADR-tmpme6k8: Fail the build on `source-mismatch`, and take the source invariant upstream

## Context

The unbound-lineage pass found fifteen mis-filed documents and summarised
eleven as *a claim inherits the topic of the document it was extracted from*.
That reads like a rule to enforce, and the mechanism looked available in
config: `chains` take an `invariant`, `source:` is a declared reference.

**The summary does not survive measurement.** Of 220 practices naming a
source, **167 — 76% — already share their source's topic**, which is the
ordinary correct case. Of the six practices that pass retagged, four had
inherited their source's topic and two — `SOTA-098`, `SOTA-099` — were wrong
in the opposite direction. The sentence described four documents and should
not be repeated as a rule.

**That is not an argument against the invariant, and the first draft of this
decision treated it as one.** It said the invariant on `source:` was rejected
by measurement, citing 73 unbound edges over 64 practices and calling them
"mostly the record doing what it decided to do". That was a topic-pair
histogram, not a reading. Read individually the 73 are four kinds:

| kind | n | what it is |
|---|--:|---|
| Multi-topic source | 16 | a model report or framework sourcing practices across three or more topics, which [ADR-032](ADR-032.md) admitted deliberately |
| Analysis paper as evidence | 14 | a practice resting on a paper filed `analysis-and-evaluation`, the kind-not-subject fact [#140](https://github.com/dmarx/anthology-of-the-sota/issues/140) documents |
| [ADR-026](ADR-026.md)'s filing rule working | ~10 | a practice takes its *kind*, its source takes the *domain* it was discovered in — the diffusion and vision papers |
| Everything else | ~33 | cross-layer fault lines, and some plain mis-filings |

The fourth row is the one that settles it. `LIT-112`, *Efficient Memory
Management for Large Language Model **Serving***, is filed
`attention-techniques` while all four practices drawn from it are
`inference-optimization`, whose blurb names cache layout and serving-time
decisions. `LIT-059` (CheckFreq) is `systems-optimization` while the four
checkpointing practices under it are `distributed-optimization`, whose blurb
names checkpointing. Neither is confirmed here — that needs a reading — but
they are exactly the shape of finding the pass in [#140](https://github.com/dmarx/anthology-of-the-sota/issues/140) acted on, reaching the
record through a second channel.

So the principle holds: **a relation asserts that its documents have something
in common, and the invariant is the record saying what.** That is as true of a
practice and its evidence as of two practices, and it does not stop being true
because some of the findings are known.

## Decision

**1. `lint.fail_on` gains `source-mismatch`, and only that.**

The dial has been `[]` since the record was built, so every finding is advice.
`source-mismatch` compares a recorded title against what the identifier
actually serves, reading the committed lockfile so it costs no network, and it
is at zero today — the precondition, because a dial turned on over existing
findings fails the next contributor for somebody else's backlog.

The reason is specific, not general: **it is the check that would have failed
the import in [#138](https://github.com/dmarx/anthology-of-the-sota/issues/138)**, whose three misbound identifiers were all
title-versus-identifier disagreements, caught by a hand-written script while
the lint printed a clean run.

Verified rather than assumed: retitling `LIT-045` to another paper's title
reports *"`arxiv: 2104.09864` resolves to 'RoFormer…', not 'A Mean Field
View…'"* and exits 1.

**`source-unchecked` is deliberately not promoted.** It fires when nothing has
verified an identifier and upstream could not be reached, so promoting it
converts an arXiv outage into a red build for a contribution that did nothing
wrong. A check earns enforcement by failing only on things that are in the
diff — `source-mismatch` fails on a disagreement the author introduced;
`source-unchecked` fails on something the author can only wait out.

**2. The `source:` invariant is right and cannot be declared here yet.**

Declaring it is three lines of config. It raises:

    File "luria/chains.py", line 214, in lines_of
        neighbours[other].add(code)
    KeyError: '[LIT-001](../literature.d/LIT-001.md)'

`chains.lines_of` indexes only documents in the chain's declared scheme, and
`source:` crosses from `SOTA` to `LIT`, so the first paper it walks is absent
from the index. The invariant machinery is not the problem; the chain walker
underneath it is. **`luria index` does not complete**, which makes this
unavailable to this record until the walker handles a cross-scheme relation —
or until the invariant can be declared without an `output:` view, which a
practice-to-paper chain does not really want anyway.

So it goes upstream with the measurement attached, rather than being recorded
here as a decision against it.

## Upstream

Two items, neither of which this record can fix:

**The cross-scheme chain crash**, above.

**Two docstrings state a reason for luria's default that is specific to this
record and now false.** `invariants.py` and `config.py`'s `Chain.invariant`
both explain why `invariant` is unset by default with: *"`source:` joins a
practice to its paper across two vocabularies that were separated on
purpose"*. [ADR-026](ADR-026.md) merged those two vocabularies into one. The default may
still be right — the 16 multi-topic sources and 14 analysis papers are real —
but the stated reason is a consumer's old state, and a general-purpose
library reasoning about one consumer's schema is worth flagging on its own.

## Consequences

**No new way for CI to fail on something outside a contributor's control.**
`source-mismatch` reads the committed lockfile, so it fails only on a
disagreement in the diff.

**The 73 crossings are a worklist, not a verdict.** They are recorded here
because nothing generates them today. Two named candidates — `LIT-112` and
`LIT-059` — and the [ADR-026](ADR-026.md) class, which is the one kind that should be
expected to stay.

**It does not cover the defect [#138](https://github.com/dmarx/anthology-of-the-sota/issues/138) actually shipped.** Sixty-seven duplicate
notes, correct titles, correct identifiers, green lint. That is `LU-#165`
upstream — *"Two documents can name the same source and nothing notices"* —
which asks for a `duplicate-source` finding and a `luria merge`, the latter
being the work done by hand in [#140](https://github.com/dmarx/anthology-of-the-sota/issues/140).

## Alternatives considered

**Declare the invariant on `source:` anyway.** `luria index` does not
complete. Not a judgement call.

**Record the invariant as rejected on measurement.** This decision's own first
draft. It was wrong about the findings and would have closed a question that
should stay open, on the authority of a histogram.

**`network: require`, or promoting `source-unchecked`.** Both make "nobody
could check" a failure, so a green run would mean verified rather than
remembered. Both were in the first draft and both fail the in-the-diff test.

**Promote more classes while the dial is open.** `retired-citations` and
`legacy-spellings` have open findings, so promoting them fails the next
contribution for a pre-existing backlog. `pending-documents` counts undecided
ADRs, which is a fact about deliberation rather than a defect.
