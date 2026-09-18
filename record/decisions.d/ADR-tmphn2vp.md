---
status: Active
title: 'Unbound is never the resting state: the relation is evidence that a tag is missing'
version: 1
supersedes:
- ADR-048
tags:
- record
- taxonomy
date: '2026-09-18'
summary: >-
  An unbound relation is a defect with exactly two readings — the invariant
  is missing, or the relation is wrong — and never a third where the answer
  is to note that somebody looked. Twenty-two unbound relations and ten
  unbound lines are now **zero**, by naming what twenty-one documents were
  already about. Also removes a `groups.primary_topic` block that constrained
  nothing and had silently drifted from the vocabulary. Rejected: an
  acknowledgement directive, and dropping `analysis-and-evaluation`.
---

<!-- inactive-ok-file: ADR-048 — Superseded by this decision, which reverses
     its verdict on the seven crossings it left standing; every mention names
     it as the superseded document, deliberately -->

<!-- inactive-ok-file: ADR-035 — Proposed, and cited for the relaxation that
     turned a constraint into a fossil, which is a fact about what it did -->

<!-- inactive-ok-file: ADR-036 — Superseded, and named as the first of the two
     passes whose verdict this reverses -->

<!-- inactive-ok-file: ADR-027 — Superseded, and named only as the precedent
     for adding a kind of work when a document wants one -->

<!-- inactive-ok-file: SOTA-107 — Rejected, and SOTA-108, both named in the
     table of documents that gained a tag; a retired claim still has a
     subject, which is the point being made about them -->

<!-- inactive-ok-file: SOTA-108 — see above -->

# ADR-tmphn2vp: Unbound is never the resting state: the relation is evidence that a tag is missing

## Context

`ADR-036` sorted twenty-four unbound relations into four kinds and left
twenty-two standing with reasons. `ADR-048` re-examined them, bound six, and
left sixteen — reporting the largest remaining block, seven crossings where a
paper that *measures* something meets a paper that *does* it, as a defect in
the invariant rather than in the documents:

> So the invariant is over-strong where one end is `analysis-and-evaluation`.
> Fixing that is a change to what the chain asserts, not to a tag.

That is wrong, and I then made it worse by proposing an `unbound-ok:`
acknowledgement directive to luria (`LU-#297`, closed) so the crossings could
be marked deliberate. Both moves treat the report as a noticeboard.

**It is a defect detector.** A relation asserts that two documents have
something in common. If a chain exists, the commonality exists — the author
could see it, which is why they wrote the relation. So an unbound relation is
one of exactly two things, and both need fixing:

- **the invariant is missing** — nothing names what the line has in common; or
- **the relation is wrong** — the chain asserts a commonality that is not there.

There is no third case. `invariants.py`'s own docstring says so and both
earlier passes read past it: *"Its usual reading is not that the documents are
mis-related but that the vocabulary is missing a word."*

## Decision

**Unbound is never the resting state.** Every finding gets one of the two
verdicts above. A recurring finding is not evidence that the report is
over-strong; it is evidence that nobody has answered it yet.

**Twenty-one documents gained a tag they were already about.** All of them
passed `ADR-046`'s test — true independent of the edge — and the relation is
what pointed at them:

| line | gained | on |
|---|---|---|
| evolution strategies for LLM post-training | `adaptation-and-tuning` | `LIT-230`, `LIT-233`, `LIT-235`, `LIT-236` |
| the same, as optimizer work | `training-optimization` | eight more of its sixteen members |
| SSM / delta-rule sequence mixing | `attention-techniques` | `LIT-161`, `LIT-165` |
| early-training instability | `model-stability` | `SOTA-008`, `SOTA-009`, `SOTA-100` |
| batch size | `training-optimization` | `SOTA-031` |
| the flash-attention kernels | `systems-optimization` | `SOTA-085`, `SOTA-086`, `SOTA-087`, `SOTA-106`, `SOTA-107`, `SOTA-108`, `SOTA-161` |
| query/key interventions | `attention-techniques` | `SOTA-131`, `SOTA-192` |

**Result: 0 unbound relations and 0 unbound lines**, from 22 and 10.

**`SOTA-085`'s standing request is answered.** Its frontmatter recorded a tag
removed for binding its edge to `SOTA-083`, with the note that the crossing
*"should keep showing up until someone answers it."* It has: flash attention
is a custom kernel, `systems-optimization` is what that document's own body
is about, and the tag was missing rather than forbidden.

**The `groups.primary_topic` block is removed from all three schemes.** It
listed thirteen of the fourteen topics under `require: any` — which luria
documents as *"the group is a label, not an axis"*, constraining nothing. Its
comment still claimed *"the topic consolidation, enforced… exactly one
primary per practice"*, true before `ADR-035` relaxed it from `exactly-one`.
Once inert, its membership drifted: `tiny-models` was added to the vocabulary
and never to the list, so the config quietly asserted that a document about
small models has no primary topic. `DP-002` names the shape — a field every
record shares is a comment with a schema — and an inert one that has stopped
being true is worse than that.

## Alternatives considered

- **An `unbound-ok:` directive.** Filed upstream, then withdrawn and closed.
  It reasons by symmetry with `inactive-ok:` and the analogy fails: a citation
  of a retired document is a legitimately permanent situation, and an unbound
  relation is a defect. The directive would have let a record silence exactly
  the findings the report exists to raise, and the ones most likely to be
  silenced are the recurring ones — which is to say the ones with a real
  structural defect behind them.
- **Drop `analysis-and-evaluation` from the vocabulary**, since it names a
  kind of work where the others name subjects. Rejected on measurement: 91
  documents carry it and for 74 it is the only tag — and those 74 are
  benchmark and evaluation notes where it *is* the subject. They declare no
  relations and produce no findings. Exactly 8 documents carried it alone
  **and** sat in a chain, and those 8 were the whole problem. The tag is
  fine; it was standing in for a subject in eight places.
- **Change what the chain asserts** — `ADR-048`'s proposal, and `ADR-036`'s
  before it. It would have hidden twenty-one genuinely missing tags.
- **Add more kinds of work to the vocabulary**, so the axis
  `analysis-and-evaluation` belongs to is properly populated. Not rejected —
  deferred, because nothing here needed one. The rule that makes it safe is
  the one this decision establishes: a kind-of-work tag never stands in for
  the subject of a document that is about something. Add a kind when a
  document wants it, as `ADR-027` did.

## Consequences

**The report is now silent, and that is the point.** Every future finding is
new, and the two verdicts are the whole vocabulary for answering it. The
next unbound relation means something is wrong today rather than joining a
standing backlog a reader has to re-derive.

**`tags[0]` ordering is still load-bearing and still unguarded.** Removing the
inert group does not change that; `LU-#229` is where the guard is asked for.
The reasoning that was buried in the group's comments now sits on the `tags`
field where it applies.

**Two decisions were reversed to get here**, and both were reasoned. The
lesson worth carrying is narrower than "they were wrong": each treated a
recurring finding as evidence about the *checker*. A check that keeps firing
on the same input is usually right about the input.
