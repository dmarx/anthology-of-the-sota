---
number: 25
status: 'Active'
title: 'Initialize the LayerNorm gain to 1'
version: 2
history:
- version: 2
  date: '2026-09-09'
  note: >-
    Two corrections from reading the source (#114). The title's "0.97-1.0"
    is gone: the range appears nowhere in LIT-025, which contains the
    string "0.97" zero times, and the body had already flagged it as a
    constant nobody had grounds for. And the source moved from LIT-025 to
    LIT-005, because LIT-025 does not recommend setting the gain — it
    argues the gain should be removed, and that argument is now filed as
    its own practice. LIT-005 is where the gain is defined.
tags:
- model-stability
date: '2026-08-24'
source:
# LIT-005 defines the gain; identity is the initialisation its formulation
# implies. LIT-025 was the source until #114 and argues the opposite —
# see the body.
- LIT-005
summary: >-
  Ba et al. (2016), [LIT-005](../literature.d/LIT-005.md) — [ARXIV-1607.06450](https://arxiv.org/abs/1607.06450). Identity at initialisation: the normalised signal passes through unchanged. A convention rather than a published result, and the record says so.
compared_against:
- SOTA-051
---

# SOTA-025: Initialize the LayerNorm gain to 1

## Source

Ba et al. (2016), [LIT-005](../literature.d/LIT-005.md) — [ARXIV-1607.06450](https://arxiv.org/abs/1607.06450), where the gain is
introduced.

## What the initialisation controls

LayerNorm's learned gain multiplies the normalised activation, so its initial
value sets how much of the block's output reaches the residual stream at step
one. Starting at 1 is the identity: the normalised signal passes through
unchanged, and the network begins as the architecture without the learned
adjustment rather than with an arbitrary one.

## It is a convention, not a result

No paper in the record argues for it, including this one. [LIT-005](../literature.d/LIT-005.md) introduces
the gain and bias — "each neuron its own adaptive bias and gain" — and states
no initialisation; the string "set to 1" does not appear in it. Every
framework initialises the gain to 1 because identity is the obvious default,
and nobody published that.

The record files it anyway, because a reader who does not know it is a
convention will go looking for the paper that established it, and the useful
thing to say is that there isn't one.

## What the former source actually argues

This practice cited [LIT-025](../literature.d/LIT-025.md) until [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114), and its title carried a range —
"0.97–1.0" — attributed there. That paper contains the string "0.97" **zero
times**. What it argues is that the gain and bias *increase the risk of
over-fitting and do not work in most cases*, and that removing them
outperforms keeping them on four datasets. It is a case for deleting the
<!-- inactive-ok: SOTA-191 — Proposed; named as where the former source's real argument now lives -->
parameter this practice initialises, and it is now filed as [SOTA-191](SOTA-191.md).

So the record briefly held a recommendation about how to set a parameter,
sourced to the paper arguing that parameter should not exist. The range was
the tell — the body already called it a constant nobody had grounds for,
alongside [SOTA-078](SOTA-078.md)'s buffer and [SOTA-089](SOTA-089.md)'s alignment — but flagging an unsourced
number is not the same as checking whether the source says anything at all.

## Where it stands now

RMSNorm ([SOTA-182](SOTA-182.md)) is the current default and keeps this gain while dropping
the centering and the bias, so the practice applies to it unchanged and
[SOTA-026](SOTA-026.md) does not.

The shrink-below-identity idea the old range gestured at is real and lives
elsewhere with sources: [SOTA-060](SOTA-060.md)'s scaled output projections and [SOTA-051](SOTA-051.md)'s
near-zero final layer both damp the residual branch at initialisation. That
is the instinct the 0.97 was reaching for, and those are the practices that
carry it.
