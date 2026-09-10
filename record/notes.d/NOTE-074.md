---
number: 74
status: Skimmed
formerly:
- NOTE-tmpzc2ud
paper: LIT-026
title: 'Advances and Open Problems in Federated Learning'
version: 1
tags:
- distributed-optimization
date: '2026-09-09'
summary: >-
  A 66,000-word multi-institution survey defining federated learning and cataloguing its open problems. Its durable contribution to this record is the cross-device / cross-silo distinction, which separates two settings with almost nothing in common operationally.
---

# NOTE-074: Advances and Open Problems in Federated Learning

**This note is `Skimmed`, not `Read`.** The paper is a ~66,000-word survey with
dozens of contributing institutions, and this reading covers its framing
sections and taxonomy rather than its full catalogue of open problems. Under
[ADR-025](../decisions.d/ADR-025.md) that is not enough to source a practice from, and this note has no
claims table. For a survey whose value is a taxonomy, the framing is the part
that matters, and the rest is a bibliography.

## Contribution

Defines federated learning as a field and organises its problems. The
definitional work is what other papers cite it for.

## Key insight

**Cross-device and cross-silo are different problems wearing one name.**

- **Cross-device**: very many unreliable clients (phones), each with little
  data, mostly unavailable, never individually addressable.
- **Cross-silo**: a small number of reliable organisational participants
  (hospitals, banks), each with a lot of data, always available, individually
  identifiable.

Almost every practical concern — client sampling, communication cost, dropout
handling, the threat model, whether a participant can be held to an agreement —
differs between them. The survey contrasts both against traditional
single-datacenter distributed learning, and states that it addresses cross-device
by default "though many of the problems apply to other FL settings".

The general form: **a name that spans two operating regimes with different
constraints will produce results that do not transfer, and splitting the name is
the fix.**

## Assumptions

Not established from this reading. The survey is descriptive and its scope is
2019–2020.

## Key results

*(From the framing sections read here.)*

- The **cross-device / cross-silo** taxonomy, and the contrast of both with
  single-datacenter distributed training.
- Deployment context: Apple using cross-device FL, medical-research
  applications, home-assistant work — the field described as already in
  production rather than prospective.
- A catalogue of open problems spanning privacy, security, system design,
  fairness and efficiency, which this reading does not cover in detail.

## Concepts

- **Cross-device vs cross-silo** — the taxonomy, and the reason this document
  is worth keeping.
- **Federated learning as distinct from distributed training** — the survey's
  own comparison, and the distinction the record's `distributed-optimization`
  practices implicitly assume away.

## Connections

The record's distributed practices — `SOTA-017`, `SOTA-018`, `SOTA-019`,
`LIT-065`'s 3D parallelism, `LIT-102`'s collectives — are all
single-datacenter, and all assume reliable, addressable, homogeneous workers on
a known interconnect. Every one of those assumptions is what federated learning
removes.

<!-- inactive-ok-block: SOTA-155 — Proposed, named as the record's one non-datacenter distributed practice rather than relied on -->
`SOTA-155` (train across poorly connected islands: many inner steps per worker,
an outer momentum optimizer over the deltas) is the record's one practice in the
adjacent direction, and `LIT-212` (DiLoCo) is its source. **That is the bridge:
DiLoCo-style training is the datacenter-adjacent end of the same axis this
survey defines the far end of.**

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**
Federated learning is not a line this anthology tracks, and a 2019 survey of a
different subfield is not going to become one.

What the reading is worth is the observation that the record's distributed
<!-- inactive-ok-block: SOTA-155 — Proposed, named as the record's one non-datacenter distributed practice rather than relied on -->
practices all quietly assume the datacenter, and that `SOTA-155` is the one
that does not. The cross-device/cross-silo distinction is the vocabulary for
saying which assumptions a distributed practice depends on, and the record has
no such vocabulary.

Marked `Skimmed` deliberately: the third use of that status in this record, and
here it is a judgement about proportion rather than about availability. Reading
66,000 words of open problems in a subfield the anthology does not track, to
correct four generic bullets on a document nothing cites, is not a good use of
the pass. The taxonomy is the part with reach and it is now recorded.

The document's takeaways — "comprehensive survey of federated learning",
"privacy and security challenges", "system design considerations", "open
research problems" — are a fair description of a survey and contain none of its
content. That is a lower bar to clear than most in this pass, and it does not
clear it.

## Limitations

Of this note: framing sections only, no claims table, and no coverage of the
open-problems catalogue that is most of the document.

## Open questions

- **Decide this document's standing rather than reading it further.** It is
  `Active` in an anthology that does not track its field, nothing cites it, and
  the one idea worth having from it is now in this note. `Rejected` with the
  reason "out of scope" would be defensible and cheaper than a full reading.
