---
status: Active
title: 'implementations: names documents, not strings, and a systems scheme would compete with a decision already made'
version: 1
tags:
- record
date: '2026-09-20'
summary: >-
  `implementations:` was undeclared: 142 distinct spellings across 216
  declarations, naming things nothing could resolve. Typed to `LIT`. A
  separate systems scheme was considered and is not built — luria's `scheme:`
  is single-valued so a field cannot accept two, and [ADR-032](ADR-032.md) already routes
  benchmarks, model reports and infrastructure to `LIT`. 141 of the 142 names
  already had a note.
---

# ADR-tmpoe5gf: implementations: names documents, not strings, and a systems scheme would compete with a decision already made

## What was wrong

`implementations:` appeared on `SOTA` and `LIT` documents from the beginning
and was **never declared in `luria.yaml`**. It carried whatever anybody
typed.

What it had accumulated by 2026-09-20:

- **142 distinct names** across **216 declarations**.
- Duplicates differing only in case (`t5` / `T5`) and in size suffix
  (`SWAN-GPT-1B`, `SWAN-GPT-8B`, `SWAN-GPT (NVIDIA, 1B and 8B)`;
  `Kimi Linear` / `Kimi Linear 48B-A3B`; `RNoPE-SWA (Cohere)` /
  `RNoPE-SWA (Cohere, 8B)`).
- Entries that were not systems at all: `the 4-bit path in the major PEFT
  libraries`, and `Falcon-H1-Tiny (0.1 after the linear projections, for a
  repeated FIM corpus)` — a hyperparameter value parenthesised into a name.
- **141 of the 142 named a document the record already held.** `MMLU` is
  [LIT-390](../literature.d/LIT-390.md). `RETRO` is [LIT-060](../literature.d/LIT-060.md). `EDM` is [LIT-075](../literature.d/LIT-075.md). `Progressive
  Distillation` is the title of [LIT-067](../literature.d/LIT-067.md).

So the field was asserting, in a structured position, that the record knew
of a system — and the assertion resolved to nothing a reader or a tool could
follow, while in almost every case a document existed under a different
spelling.

Nothing in prose complained, because nothing in prose was wrong. This is the
structured-field class of gap that [#203](https://github.com/dmarx/anthology-of-the-sota/issues/203) is about, and it is the largest
instance of it in the record.

## The decision

**`implementations:` is a reference to `LIT`**, declared on both schemes,
`required: false`, `many: true`.

Every declaration is migrated to codes. A name that cannot be resolved to a
note can no longer be written, which is the point: the failure mode is not
made *detectable*, it is made **impossible to introduce**.

**No converse is written back.** `luria link --fix` writes converses for the
lineage relations and deliberately does not write one here. A paper's note
should not accumulate a list of every practice somebody used it for; that
list is the practice registry, read from the other end.

## Why there is no systems scheme

The obvious alternative was a `SYS` scheme — one document per model, dataset,
benchmark or library — with `implementations:` pointing at it. Two things
rule it out.

**luria's `scheme:` is single-valued.** A reference field names one scheme.
Declaring `scheme: [LIT, SYS]` is refused:

    schemes.SOTA.references.implementations names scheme "['LIT', 'SYS']",
    which is not declared (have: ADR, DP, LIT, NOTE, SOTA, THEORY)

So `implementations:` could point at `SYS` or at `LIT`, not both. Pointing it
at `SYS` would require **142 `SYS` documents, 141 of which would proxy a
`LIT` note that already exists** — two documents for one object, which is
what [DP-002](../principles.d/DP-002.md) is about.

**And the categories are already routed.** [ADR-032](ADR-032.md) decided that
benchmarks, model reports and training or serving infrastructure are
literature and the record files them. Every kind of thing a `SYS` scheme
would hold — `MMLU`, `Llama 3`, `verl`, `TVM`, `The Pile` — is a kind
[ADR-032](ADR-032.md) already sends to `LIT`, and the record has notes for all of them.

A second scheme would not have been a new home. It would have been a
competing one.

## What this costs

**Variants collapse.** `DiffuGPT` and `DiffuLLaMA` both become [LIT-381](../literature.d/LIT-381.md);
`SWAN-GPT-1B` and `SWAN-GPT-8B` both become [LIT-209](../literature.d/LIT-209.md). The field can no
longer distinguish two models reported in one paper.

That is accepted, and the mitigation is the one [ADR-017](ADR-017.md) already uses for
`source:`: **the field is typed and the prose is argument.** Every practice
affected carries a `## Known implementations` section naming the specific
systems, and those sections are unchanged. A reader who needs to know it was
the 8B and not the 1B reads the sentence; a tool that needs to follow the
citation reads the code.

**Three entries were dropped rather than mapped**, because they name nothing
the record holds:

- `Nemotron-3 Super` and `Nemotron-3 Ultra` on [SOTA-180](../practices.d/SOTA-180.md) — NVIDIA models the
  record knows of only because [LIT-196](../literature.d/LIT-196.md) mentions them as adopters. There is
  no report for either. Mapping them to [LIT-196](../literature.d/LIT-196.md) would have been wrong twice
  over: that note is the *method's* paper, and it is already [SOTA-180](../practices.d/SOTA-180.md)'s
  `source:`, so the field would have claimed a practice is implemented by its
  own evidence.
- `the 4-bit path in the major PEFT libraries` on [SOTA-230](../practices.d/SOTA-230.md) — a description,
  not a system.

All three remain in the body at their citing site, so nothing is lost but the
false precision of a structured field.

**That residue is the honest answer to "are there systems with no paper".**
There are, and there were two of them, and they are adopters known only by
somebody else's mention. That is a small enough class to carry in prose, and
[ADR-043](ADR-043.md)'s provisional-carry rule is what says prose is enough until it is
not.

## What it buys

One thing, and it is worth the migration: **the record can no longer name a
system it holds nothing for.** Before this, `Stable Diffusion 3` sat in
[SOTA-188](../practices.d/SOTA-188.md)'s `implementations:` for a month with no paper in the record,
and it was found by a paper wandering past rather than by anything looking.

It also makes the adoption side of [DP-005](../principles.d/DP-005.md) followable. That principle
separated adoption from evidence and sent adoption here and to `consensus:`.
Adoption stated as an unresolvable string was separated from evidence and
from everything else as well.
