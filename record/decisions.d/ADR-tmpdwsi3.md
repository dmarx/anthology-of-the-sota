---
status: Proposed
title: 'Notes imported from another project enter as unread literature'
version: 1
tags:
- record
- migration
date: '2026-09-15'
summary: >-
  Seventy-four paper notes arrived from a separate project on decentralized
  training, in its own schema, carrying 187 recommendations. The papers are
  filed as LIT at `Deferred`; the readings are not filed as NOTE documents,
  the recommendations are a backlog rather than practices, and the foreign
  `research_implications` are dropped. The reason is measured rather than
  cautious: checking the 74 notes' identifiers against arXiv and CrossRef
  found three that name a different paper than the one they describe, which
  is the failure the NOTE status vocabulary was written to prevent.
---

# ADR-tmpdwsi3: Notes imported from another project enter as unread literature

## Context

Seventy-four paper notes arrived from a separate research project — one about
decentralized and communication-efficient training, gossip SGD, Langevin
dynamics and the mean-field theory of wide networks. They are YAML, in that
project's own v2 schema, and each carries `contribution`, `key_insight`,
`assumptions`, `key_results`, `claims`, `method`, `concepts`, `connections`,
`recommendations`, `research_implications`, `limitations` and
`open_questions`.

Six of the papers are already in this record. Sixty-eight are not. Across the
batch there are 187 entries under `recommendations`, and that project's own
`SCHEMA.md` describes the field as *"General-purpose, project-agnostic
practitioner advice. Preserved for reuse beyond this project"* — an explicit
invitation to carry them somewhere like here.

The obvious mapping is one-to-one and almost entirely wrong. Each note looks
like a `LIT` plus a `NOTE`; each recommendation looks like a
`SOTA`. Taken literally that is 68 new notes, 68 new readings
and up to 187 new practices, in one contribution, none of them read here.

Before filing anything, the batch's identifiers were checked against the
sources that can check them: 60 arXiv ids through the arXiv API, and the 14
non-arXiv papers through CrossRef. Four findings, on the only field a machine
can verify:

- **`1805.01361`** is described as Mei, Montanari and Nguyen's *A Mean Field
  View of the Landscape of Two-Layer Neural Networks*. That identifier is a
  paper on hyperspectral regression for water parameters, by different
  authors. The paper the note describes is `1804.06561`, which arrived in the
  same batch under its own note.
- **`1906.08632`** is described as Goldt et al.'s *hidden manifold model*.
  That identifier is a different Goldt paper — *Dynamics of stochastic
  gradient descent for two-layer neural networks in the teacher-student
  setup*. The hidden-manifold paper is `1909.11500`, which is not in the
  batch.
- **`2102.11742`** is given a title and an author that belong to no paper;
  the note's own `contribution` field then says, in prose, that the papers it
  actually means are three others.
- **Wolfowitz (1963)** is placed in the *Annals of Mathematical Statistics*.
  It is Proceedings of the American Mathematical Society 14(5).

Three notes out of sixty describe a paper other than the one they name. The
remaining mismatches were transliterations, `et al.` in an author list, and
two papers retitled between arXiv versions.

## Decision

**The papers enter as `LIT` at `Deferred`. Nothing else in the notes is
filed.** Four parts:

**1. Sixty-eight LIT documents, all `Deferred`.** The status vocabulary
already has the right word — *"in the corpus, not yet read closely enough to
place"* — and that is the literal truth about every paper in this batch.
Title, authors, date and identifier come from arXiv or CrossRef, not from the
imported note, and each body carries a one-line statement of what the paper
established plus the first few sentences of its own abstract. Nothing in them
is this record's reading, and none of them claims to be.

**2. The imported readings do not become `NOTE` documents.** [ADR-025](ADR-025.md) makes
the absence of a NOTE mean the paper is unread, which is exactly the state
this batch is in — so the honest filing costs nothing and needs no new
machinery. The reason not to convert them is written into `luria.yaml` beside
the NOTE statuses, about two notes this record has already been burned by:
*"[LIT-052](../literature.d/LIT-052.md) and [LIT-025](../literature.d/LIT-025.md) each carried a plausible-looking set of takeaways that
turned out not to be about their paper, and eight practices were built on
them."* That is not an analogy to the present case. It is the present case,
measured at three in sixty, arriving in a batch twenty-five times the size.

**3. The 187 recommendations are a backlog, not practices.** A practice names
a `source:`, and a practice sourced to a paper nobody here has read is the
failure mode the NOTE vocabulary exists to prevent. They are also not uniform:
a large share are specific to that project's own system despite the schema's
claim — they name its experiments and its components by name — and another
share is advice to a *theorist* about proof technique rather than to a
practitioner about training. Which of the rest survive is a question per
recommendation, answerable only by reading the paper, and it is filed as an
issue rather than guessed at here.

**4. The `research_implications` are dropped entirely.** They answer five
questions from that project's `synthesis/research_agenda.md`. They are good
answers to questions this record did not ask, and transcribing them would put
another project's agenda into this one's documents under the guise of
findings.

## Consequences

**The record gains a branch of the literature it did not have and could not
cite.** Before this, `distributed-optimization` was thirteen topics' worth of
practice with almost no papers behind the decentralized half of it. Local SGD,
gossip SGD, Byzantine-robust aggregation, gradient compression, the mean-field
limit and the consensus results underneath all of it are now citable by code.

**`Deferred` is load-bearing, and the indexes will show it.** Sixty-eight
unread notes is a visible, countable debt rather than a silent one, and each
one names the reading that would clear it. A reader who wants to know what
this record actually asserts about gossip SGD can tell at a glance that the
answer is still nothing.

**Three papers are filed with a correction in the body.** Where the imported
note named the wrong paper, the note here files the paper the identifier
actually points at and says what the import claimed. `1805.01361` is not filed
at all: the note describing it was about `1804.06561`, which is filed, and a
second document for the same paper under a stranger's identifier would be a
duplicate with a false citation.

**Whether consensus mathematics belongs here is answered as scope, not
excluded as off-topic.** Wolfowitz (1963) on products of stochastic matrices,
Jadbabaie et al. on switching topologies, and the Fokker-Planck variational
scheme make no claim any of the thirteen topics can express on their own. They
are filed anyway, on the argument [ADR-032](ADR-032.md) already made for
benchmarks and infrastructure: the record files what its papers cite. The
difference is that nothing here cites them *yet* — the work that does is in
another project — and `Deferred` is precisely how the record says so. If no
document here ever reaches for them, their status will still be saying that in
a year, which is the outcome this scheme is for.

**This is the second import, and it is filed differently from the first.**
[ADR-008](ADR-008.md)'s migration brought the pre-record YAML in wholesale and
`Active`, because it *was* this project's own corpus. This batch is somebody
else's, and the difference in provenance is the whole of the difference in
status.

## Alternatives considered

**File the readings as `NOTE` documents.** The cheapest route, and it would
have asserted — sixty-eight times — that this record read papers it has not
opened. The measured error rate makes that assertion false on at least three
of them and unverified on the rest.

**File the recommendations as practices, at `Proposed`.** `Proposed` is about
the *evidence* being early, not about the filer not having checked. It would
put 187 recommendations into the registry on the authority of a secondary
source, which is the one thing [DP-001](../../docs/design-principles.md#dp-1) is
against.

**File nothing until the papers are read.** This keeps the record honest by
keeping it empty, and it discards the half of the import that is cheap and
checkable. An identifier, a title and a date verified against arXiv are worth
having on their own: they are what makes the papers citable, and citability is
what lets the practice work happen incrementally instead of all at once.

**Keep the foreign schema as a fourth family.** Two topic vocabularies were
the problem [ADR-026](ADR-026.md) spent a decision removing. A second note
format, with its own status words and its own agenda field, would be that
again with more moving parts.
