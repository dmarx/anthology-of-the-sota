---
status: Active
title: 'The most citable sentence in a paper is often its least supported one'
version: 1
tags:
- evidence
date: '2026-09-21'
---

<!-- inactive-ok-file: SOTA-282 — Proposed, and named as the worked example of
     this principle's instruction about units. The principle is about how to file
     a claim, not about whether that practice should be adopted -->

# DP-tmpymzzl: The most citable sentence in a paper is often its least supported one

Papers are written to be read once. The sentence that survives that reading —
the one that ends up in an abstract, a talk, a survey, a `summary:` field —
is selected for memorability, and memorability is not correlated with
evidential weight. Often it is anti-correlated, because the claims that are
easiest to state are the ones a paper has had to hedge.

This is not an accusation of bad faith. In every case below the authors said
what they had done and what they had not, in the same document, usually within
a page of each other. The hedge is present and it does not travel.

## Four from one week

- **nGPT** (`LIT-472`). The abstract reports 4–20× fewer training steps.
  Footnote 3, same page as Figure 1, reports step time 80% higher at 4k
  context and 60% at 8k. The wall-clock figure is roughly half the headline,
  and the headline is the one in the unit that flatters.
- **The Coverage Principle** (`LIT-474`). Globally normalized SGD is
  proved to remove a sequence-length dependence. The next sentence says
  "somewhat speculatively, we believe that it may be possible" to extend this
  to Adam, and notes that Adam's per-coordinate normalization is a meaningful
  difference. One of those two sentences is a theorem.
- **Local volume** (`LIT-tmpk8scf`). Section 3.3 argues that adaptive
  optimizers generalize worse because they partly undo the architecture's
  parameter-to-function map. It is the best idea in the paper and no figure
  touches it.
- **Zero-shot chain of thought** (`LIT-469`). MultiArith 17.7 → 78.7 is the
  number everyone quotes. The sentence that decides the practice is in the
  body: it underperforms few-shot CoT and beats eight-shot standard prompting,
  which makes it a first move rather than a better method.

Four papers, four weeks apart in filing, one shape.

## Why it matters to a record rather than to a reader

A reader who quotes the wrong sentence is wrong once. A record that files it
is wrong for everyone who comes after, and the error is laundered: the
`summary:` field is read far more often than the document, and the document
far more often than the paper.

The failure is also invisible to the usual checks. Every citation resolves.
The paper says the thing. The lint is clean. Nothing in the record can tell
that the cited sentence is the one the authors were least sure of, because
that information lives in the hedge, and the hedge is what compression
removes first.

## What to do

**Find the hedge before writing the summary.** It is usually there: a
footnote, a "somewhat speculatively", a limitations paragraph, a sentence
beginning "we leave to future work". If a striking claim has no hedge anywhere
near it, that is worth a second look rather than a relief.

**State the unit, and prefer the one the reader decides on.** Tokens versus
wall clock, relative versus absolute, against which baseline. `SOTA-282`
says to quote the wall-clock figure for nGPT, and that instruction is the
whole practical content of this principle for that document.

**Put the unmeasured claim in the record as unmeasured, not out of it.**
Leaving it out is safe and lossy; the next reader hits the same sentence and
has to do the work again. Naming it, and saying no experiment touches it, is
what stops it entering as a finding later.

**And say which practice it does not move.** `SOTA-001` recommends Adam, and
two of the four papers above contain a sentence that looks like it bears on
that recommendation. Neither does. Writing that down costs a line and is the
only thing that prevents the inference being drawn silently in six months.

## Its relation to [DP-005](design-principles.md#dp-5)

[DP-005](design-principles.md#dp-5) says adoption is not evidence — that a practice being widespread
says nothing about whether it was ever tested. This is the same failure one
level down: a *sentence* being widespread says nothing about whether it was
ever supported. Both are about the gap between how well-travelled a claim is
and how well-founded, and both have the same remedy, which is to go and look.
