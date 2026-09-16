---
status: Proposed
title: 'An algorithm-local tuning constant belongs in the reading of the paper that measured it, not in the practice registry'
version: 1
tags:
- record
- taxonomy
date: '2026-09-16'
issue: '#139'
summary: >-
  A number fitted to one algorithm on one workload is a finding about that
  paper, not a recommendation to a reader who may not be running that
  algorithm. It stays in the note's `## Recommendations` section, where it is
  already visible and already attributed, and it does not become a `SOTA`
  document. The test: strip the algorithm's name from the sentence and see
  whether anything is left to do.
---

<!-- inactive-ok-file: SOTA-tmpwgbmj, SOTA-tmpboy96 — Proposed practices,
     cited here as the two worked examples of this decision being applied:
     each names a constant from its own source and declines it. The
     decision does not rest on either. -->

# ADR-tmpl8z39: An algorithm-local tuning constant belongs in the reading of the paper that measured it, not in the practice registry

## Context

The import behind [#139](https://github.com/dmarx/anthology-of-the-sota/issues/139) brought 187 recommendations out of 70 readings, and the
single largest class in what remained after the obvious filings was constants:

- *"Set `alpha = 2/(m+2)` for EASGD"*
- *"Use rank 2 for CNNs and rank 4 for LSTMs"* (PowerSGD)
- *"Set `tau = 48` for SGP and `tau = 12` for local SGD"* (SlowMo)
- *"Set Moshpit grid dimensions so `M^d` approximates the worker count"*
- *"Use `alpha = 0.6` and anchor momentum `beta = 0.7`"* (Overlap Local-SGD)

Every one is correct, measured, and useful. None of them has been filed, and
the reason each was passed over has been re-derived by hand each time rather
than decided once. That is the thing this closes: not the question of whether
they are worth having — they are, and they are already in the record — but the
question of *where*, so that the next contributor meeting the twentieth one
does not have to think about it.

The pull toward filing them is real and worth naming. They are the most
concrete, most actionable sentences in any of these papers. A practice
registry that holds "prefer decentralized SGD below 1 Gbps" and not "use rank
4 for LSTMs" can look like it is holding the vague half.

## Decision

**A recommendation whose subject is a named algorithm's own hyperparameter
stays in the reading. It does not become a practice.**

The test, which is mechanical enough to apply without judgement: **remove the
algorithm's name from the sentence.** If what remains is an instruction, it is
a practice. If what remains is nothing — *"set alpha to 2/(m+2)"* — then the
sentence was a fact about that algorithm and its home is the note on the paper
that measured it.

Two consequences that follow and are the point:

**The note already holds it, findably.** `## Recommendations` in a `NOTE` is a
rendered section with the strength and the conditions the reading recorded.
Nothing is lost by not promoting it; a reader who has decided to run PowerSGD
reaches the PowerSGD note, which is where the rank is.

**A practice may still cite the constant in prose.** [SOTA-tmpwgbmj](../practices.d/SOTA-tmpwgbmj.md) names
[LIT-254](../literature.d/LIT-254.md)'s 30-epoch densification schedule and declines it; [SOTA-tmpboy96](../practices.d/SOTA-tmpboy96.md) names
[LIT-323](../literature.d/LIT-323.md)'s anchor-momentum pair and declines it. Declining to give a number its
own document is not declining to mention it, and saying why in the practice
that neighbours it is how a reader learns the boundary.

## What this does not cover

**A constant that transfers is not algorithm-local.** `beta2 = 0.999` is in
this record as [SOTA-002](../practices.d/SOTA-002.md) because it is what people set on a family of
optimizers across a decade of workloads, not because Adam's paper reported it.
The distinction is whether the number outlived the paper, and that is a
judgement, not a test.

**A threshold about the world is not a tuning constant.** [SOTA-tmpjynpv](../practices.d/SOTA-tmpjynpv.md)
carries "below about 1 Gbps or above about 5 ms", which is a number, is
dated, and is filed anyway — because it is a fact about when one *regime*
beats another, and the reader it addresses has not yet chosen an algorithm.
The line is between a number that configures a thing you have chosen and a
number that helps you choose.

**This is not a claim that the class is empty.** Some of the 157 will turn out
to be practices wearing a constant's clothes, and the test above is what
catches them. It is a claim that the default is "no", stated once.

## Alternatives considered

- **File each as a `Deferred` practice** with a `promote_when` naming a second
  workload. This is what [DP-006](../../docs/design-principles.md#dp-6) would suggest for a claim with weak-but-honest
  evidence, and it is the wrong reading of [DP-006](../../docs/design-principles.md#dp-6) here: the evidence is not
  weak, the *scope* is narrow. `Deferred` says "probably right, not yet worth
  asserting", and *"use rank 4 for LSTMs"* is not something the record is
  hesitating about. It is something the record is not addressed to.
- **Add a scheme for them.** A `CONST` or `PARAM` family alongside `SOTA`,
  `LIT`, `THEORY` and `NOTE`. Rejected because the `NOTE` scheme already is
  it: one document per reading, with a recommendations section, which is
  exactly where a paper's own settings belong. A fifth scheme would move them
  without changing what they are.
- **Decide per paper, as now.** What produced the [#139](https://github.com/dmarx/anthology-of-the-sota/issues/139) backlog, and the cost
  is not the thinking — it is that the thinking leaves no trace, so the
  hundredth constant costs what the first did.
