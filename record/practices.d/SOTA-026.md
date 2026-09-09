---
number: 26
status: 'Active'
title: 'Initialize LayerNorm bias to 0'
version: 2
history:
- version: 2
  date: '2026-09-09'
  note: >-
    Source moved from LIT-025 to LIT-005 (#114). LIT-025 does not
    recommend setting the bias; it argues the bias should be removed, and
    that argument is now its own practice. LIT-005 is where the bias is
    defined. The recommendation is unchanged.
tags:
- model-stability
date: '2026-08-24'
published: '2019-11-01'
source:
# LIT-005 defines the bias. LIT-025 was the source until #114 and argues
# the opposite — see the body.
- LIT-005
summary: >-
  Ba et al. (2016), [LIT-005](../literature.d/LIT-005.md) — [ARXIV-1607.06450](https://arxiv.org/abs/1607.06450). Zero is the identity; a convention rather than a published result, and moot in any model using RMSNorm.
---

# SOTA-026: Initialize LayerNorm bias to 0

## Source

Ba et al. (2016), [LIT-005](../literature.d/LIT-005.md) — [ARXIV-1607.06450](https://arxiv.org/abs/1607.06450), where the bias is
introduced.

## Zero is the identity here too

The bias is added after the normalised activation is scaled, so initialising
it to zero means the layer starts as pure normalisation-and-scale with no
offset. Any other starting value asserts a preferred direction in feature
space before training has said anything, which is the thing initialisation
schemes generally try to avoid.

There is no interesting trade here, which is worth stating plainly: this is a
convention with no live alternative, and the practice's value is as a
statement of what the default is rather than as advice between options.

## What the former source actually argues

This cited [LIT-025](../literature.d/LIT-025.md) until [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114). That paper's finding is that the bias and gain
*increase the risk of over-fitting and do not work in most cases*, and that
LayerNorm with both removed beats LayerNorm on four datasets. It is a case for
deleting the parameter this practice initialises, not for setting it, and it
<!-- inactive-ok: SOTA-191 — Proposed; named as where the former source's real argument now lives -->
is now filed as [SOTA-191](SOTA-191.md).

[LIT-005](../literature.d/LIT-005.md) introduces the bias and states no initialisation for it, so the
zero is a convention rather than a result — the same standing as [SOTA-025](SOTA-025.md)'s
gain, and said plainly for the same reason.

## Where it stops applying

RMSNorm has no bias at all. It normalises by root-mean-square without
centring, on the finding that the mean subtraction contributes little, and
drops both the centring and the offset — so in the models this record mostly
concerns itself with ([SOTA-006](SOTA-006.md)), there is no parameter for this practice to
initialise.

Kept rather than retired because BatchNorm and LayerNorm are both still in
use and the convention is real. But it is a practice about a component the
frontier has largely moved past, which the record should say rather than
leave the reader to infer from its absence elsewhere.
