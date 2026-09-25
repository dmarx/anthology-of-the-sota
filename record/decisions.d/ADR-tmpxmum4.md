---
status: Active
title: 'published: is the exact date of first appearance where a source gives one'
version: 1
tags:
- record
date: '2026-09-25'
summary: >-
  A LIT's `published:` records the day a work first appeared — the arXiv v1
  submission date, else the earliest full date Crossref reports, else the date
  the document itself carries — and falls back to the first of the month only
  when no source gives a day. The month-only convention recorded a date nobody
  meant and discarded one every source states.
---

# ADR-tmpxmum4: published: is the exact date of first appearance where a source gives one

## Context

The LIT template said `published:` is "the arXiv posting month, from the id:
2205.11487 → 2022-05", written as the first of that month. So a paper posted
on 23 October was recorded as posted on 1 October: not a coarser truth but a
false date that looks exact, and one that practices and theories then inherit
through `derive: '{published}'`. Every arXiv abstract page states the v1 day.
The owner's ruling, when a reading surfaced it in the sibling record
nucleation: "that's a stupid convention, use exact dates where we have them."
Nucleation adopted it as its [ADR-002](ADR-002.md); this is the same decision here.

## Decision

`published:` is the exact date of first appearance:

- **arXiv:** the v1 "Submitted on" date from the abstract page — even when it
  falls in the month before the id's (the id is the announcement month).
- **DOI without arXiv:** the earliest full year-month-day date Crossref
  reports among posted, published-online, published-print and issued.
- **Neither:** the date the document itself carries.
- **No day anywhere:** the first of the month, as before.

Two guards, because an automated source can be wrong in a way that looks
exact: a Crossref date is used only when it falls in the year already
recorded (Crossref's earliest full date for an old work is often the date the
publisher digitised it — a 1991 volume came back as 2006), and an arXiv v1
more than a year after the recorded date is treated as a late posting of an
older work, not its first appearance. Both are flagged for a human rather
than applied.

## Rejected alternatives

- **Keep the month convention** — it records a date nobody meant.
- **Trust Crossref's earliest date unconditionally** — it would move five
  works by years, including a 2024 preprint to its 2026 journal date.
- **A `published_precision:` field** — nearly every LIT has a day, so it
  would be a field almost every record shares ([DP-002](../../docs/design-principles.md#dp-2)).

## Consequences

Backfilled on 2026-09-25 by script (arXiv abstract pages, then Crossref, both
cached): **420 LITs changed, 229 already exact or without a day-level source.**
Four moved month, all arXiv v1 dates earlier than their id month ([LIT-126](../literature.d/LIT-126.md),
[LIT-139](../literature.d/LIT-139.md), [LIT-154](../literature.d/LIT-154.md), [LIT-515](../literature.d/LIT-515.md)); [LIT-139](../literature.d/LIT-139.md)'s arXiv page gives 26 April for id
2606.19348, which is what arXiv states and is recorded as such. Five were
flagged and left alone: [LIT-248](../literature.d/LIT-248.md) and [LIT-296](../literature.d/LIT-296.md) (digitisation dates), [LIT-410](../literature.d/LIT-410.md) and
[LIT-509](../literature.d/LIT-509.md) (a journal issue date a year after the recorded date), and [LIT-696](../literature.d/LIT-696.md)
(the 2026 Nature date of a 2024 preprint). Every practice and theory that
derives `published` from its source moved with it. The template's comment
now states the rule.
