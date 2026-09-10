---
number: 194
status: Active
formerly:
- SOTA-tmpdl6gb
consensus: emerging
consensus_note: >-
  Stated as a discipline by papers careful enough to notice the confound in
  their own results; not a named methodological norm anywhere.
title: 'When an objective arrives with its own dataset, state the composition before crediting the objective'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-10'
source:
- LIT-080
- LIT-099
implementations: []
---

# SOTA-194: When an objective arrives with its own dataset, state the composition before crediting the objective

## Source

Chen et al. (2022), [LIT-080](../literature.d/LIT-080.md) — PaLI, whose ablation section is the worked
example.

Anil et al. (2023), [LIT-099](../literature.d/LIT-099.md) — PaLM 2, which ranks the data mixture above
architecture for final quality.

## The claim

A new objective is almost never added alone. It arrives with the dataset it is
trained on, and that dataset has a composition. **Any result attributed to the
objective is confounded with the composition until someone says otherwise.**

`LIT-080` is the clean instance, and the paper does the right thing in prose
even though its experiment does not separate the two:

> the captioning objective on CC3M-35L helps on COCO; on XM-3600, its positive
> contribution for non-EN languages and the slight degradation for English is a
> reflection of CC3M-35L having a much higher non-EN example ratio (34/35)
> compared to WebLI alt-text (60% English)

An objective helped some languages and hurt one. The explanation is arithmetic
about the data, not a property of the objective, and the numbers are given so a
reader can check.

`LIT-099` is the reason this matters beyond one ablation: at frontier scale the
mixture is ranked **above architecture** for final quality, and translation
pairs that were "a minor part of the mixture" were enough to reach production
translation quality. If the mixture is that determining, an unstated composition
is an unstated cause.

## The minimum

Not a controlled experiment — that is often unaffordable. The minimum is
**stating the composition alongside the result**, which costs a sentence and
lets a reader do what `LIT-080`'s authors did for themselves.

## Conditions

This is a reporting discipline, not a finding, and the sources support it by
demonstration rather than by measurement. `LIT-080`'s attribution is itself
unisolated — the paper describes the confound instead of testing it, which is
the point and also its limit.

<!-- inactive-ok-block: SOTA-166 — Proposed, named as the record's adjacent data practice rather than relied on -->
The record's data practices ([SOTA-166](SOTA-166.md), [SOTA-103](SOTA-103.md), [SOTA-170](SOTA-170.md)) are about *choosing*
a mixture. This is about *reading* a result that a mixture produced, which is
the other half.

## Known implementations

- `LIT-080`'s CC3M-35L ablation, which states the ratio it is confounded with
