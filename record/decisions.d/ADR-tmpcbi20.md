---
status: Proposed
title: 'Readings made in another context port into the record; their agenda does not'
version: 1
tags:
- record
- migration
date: '2026-09-15'
summary: >-
  Seventy-four paper notes arrived from a separate project on decentralized
  training. They are this record's own readings, made under a different
  agenda, and their schema turns out to be the NOTE schema — the same twelve
  fields in the same order. So they port: 70 NOTE documents and 67 new LIT
  notes. What does not port is decided by scope rather than by trust — one
  field answers another project's five questions, 17 recommendations name that
  project's own system, and 6 are advice on proof technique. Metadata comes
  from arXiv and CrossRef in every case, because three readings were bound to
  the wrong identifier and one citation was invented outright.
---

# ADR-tmpcbi20: Readings made in another context port into the record; their agenda does not

## Context

Seventy-four paper notes arrived from a separate research project — one about
decentralized and communication-efficient training, gossip SGD, Langevin
dynamics and the mean-field theory of wide networks. They are YAML, in that
project's own v2 schema, and each carries `contribution`, `key_insight`,
`assumptions`, `key_results`, `claims`, `method`, `concepts`, `connections`,
`recommendations`, `research_implications`, `limitations` and
`open_questions`.

They are not a secondary source. They are **this record's own readings, made
in a different context** — the same work that produces a NOTE here, done for a
different project, against a different agenda.

That is legible in the schema itself. Set the incoming fields beside the
section headings this record's NOTE documents have used since [ADR-025](ADR-025.md) and they
are the same list, in the same order:

| incoming field | NOTE section |
|---|---|
| `contribution` | `## Contribution` |
| `key_insight` | `## Key insight` |
| `assumptions` | `## Assumptions` |
| `key_results` | `## Key results` |
| `claims` | `## Claims` |
| `method` | `## Method` |
| `concepts` | `## Concepts` |
| `connections` | `## Connections` |
| `recommendations` | `## Recommendations` |
| `research_implications` | `## Bearing on the record` |
| `limitations` | `## Limitations` |
| `open_questions` | `## Open questions` |

Eleven of the twelve are the same field under two names. The twelfth is the
one that differs in substance rather than in spelling, and it is where the
whole decision lives.

## Decision

**Port the readings. Retarget the one field that answers someone else's
question. Take every identifier from a resolver.**

**1. Seventy NOTE documents, `Read`.** Eleven sections transcribe. The order
is the schema's own, so nothing is rearranged and nothing is summarized away —
theorem statements keep their rate expressions, claims keep their strength and
support, assumptions keep the ones that do not hold in a colocated cluster.

**2. Sixty-seven new LIT notes, `Active` but for one.** The papers the record
did not hold. Six were already here; four of those six had no reading and now
have one.

**3. `research_implications` is rewritten, not transcribed, into `## Bearing
on the record`.** The source field answers five questions from that project's
`synthesis/research_agenda.md` — critical batch size, fault tolerance, cluster
topology, Langevin versus large-batch, power smoothing. Those are good answers
to questions this record did not ask. The section that replaces them answers
the question this record does ask: what may a practice here rest on, and does
one exist yet. Seventy of those were written fresh.

**4. Twenty-three of the 187 recommendations are marked as not filed, in
place, with the reason.** Seventeen name that project's own system and
experiments by name — *"when fitting MSE curves from our gossip
experiments"*, *"map the GELS gossip coupling strength to the Kuramoto
coupling K"* — despite the schema calling the field project-agnostic. Six are
advice to a theorist about proof technique: use the bounded-Lipschitz metric,
check a log-Sobolev inequality uniformly in `N`, work in a rigged Hilbert
space. They stay visible in the note, struck rather than deleted, because a
reader who disagrees with the cut should be able to see what was cut.

**5. Every title, author, date and identifier comes from arXiv or CrossRef.**
Not from the reading. This is the part of the earlier, more suspicious
decision that survives contact with the truth, and the reason is four
findings from checking all seventy-four against the resolvers:

- **`1805.01361`** carries a reading of Mei, Montanari and Nguyen. That
  identifier is a paper on hyperspectral water regression. The reading is
  real and is of `1804.06561`, which arrived in the same batch under its own
  reading — so the two are merged into one note, and the wrong identifier is
  not filed.
- **`1906.08632`** carries a reading labelled with the title of Goldt et
  al.'s hidden-manifold paper. The reading is of the paper the identifier
  names — their teacher-student dynamics paper — so the identifier is right
  and the title was wrong. Filed under arXiv's title, with the discrepancy in
  the note.
- **`2102.11742`** carries a reading that binds to no paper: its title and
  one of its authors belong to none, and its own first paragraph says the
  work it means is three others. **The paper is filed at `Deferred` with no
  note.** This is the one case where absence is the right answer, and [ADR-025](ADR-025.md)
  already makes absence mean unread.
- **Wolfowitz (1963)** is given a journal, a volume, a page range and a DOI.
  The DOI resolves to nothing; the journal is wrong. That is a citation
  invented rather than mistaken, and it is the one finding here that bears on
  trust rather than on labelling.

Three identifier errors in sixty, and one fabricated citation in fourteen. The
content is this record's own work and ports; the bibliography around it does
not, and is replaced.

## Consequences

**The record gains a branch of the literature it did not have, read.** Local
SGD and its descendants, decentralized and gossip SGD, Byzantine-robust
aggregation, gradient compression, volunteer-scale training, the mean-field
account of wide networks, the teacher-student line, permutation symmetry, and
the consensus results underneath all of it — 67 papers, 70 readings.

**`## Bearing on the record` is now a section that can be wrong, and that is
the point.** Transcribing the source field would have produced seventy
paragraphs about another project's experiments, all of them true and none of
them about this record. Writing seventy fresh ones produces seventy claims
about what this record could assert and does not, each of which a reader can
check against the registry.

**The earlier decision in this contribution was wrong and is replaced.** It
read the batch as a secondary source of unknown provenance, filed all 68
papers at `Deferred`, filed no readings, and sent all 187 recommendations to a
backlog issue on the grounds that a practice may not be sourced to an unread
note. The rule is right; the premise was not, because the papers were not
unread. The three identifier errors that decision leaned on are real, and they
are labelling errors in this record's own filing rather than evidence about a
stranger's care — which is a reason to rebind them, not a reason to distrust
seventy readings.

**Two papers already had readings and did not get a second.** `LIT-017`
(McCandlish et al.) and `LIT-028` (Kaplan et al.) carry `NOTE-062` and
`NOTE-017`. The incoming readings of both are largely about fitting curves
from another project's experiments, so nothing was lost; but the record now
has two readings of two papers in two places, and only one of each is filed.

## Alternatives considered

**File the papers unread, as the first pass in this contribution did.** It
asserts something false — that nobody here has read them — in order to avoid
asserting something uncertain. `Deferred` is for papers nobody got to, and
these are not those.

**Transcribe `research_implications` as-is.** It is the cheapest option and it
imports another project's agenda into this one's documents in the voice of
findings. A reader would have had no way to tell which of five questions a
paragraph was answering, or that the questions were not this record's.

**Port the readings but not the recommendations.** Splitting them would have
put the advice a paper gives somewhere other than the reading of that paper,
which is exactly the separation [ADR-025](ADR-025.md) created the NOTE scheme to avoid.

**Drop the 23 excluded recommendations silently.** Struck-in-place costs three
words per line and leaves the cut auditable. Deleting them makes the note look
like the paper gave less advice than it did.
