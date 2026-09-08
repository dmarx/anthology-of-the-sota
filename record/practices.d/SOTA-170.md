---
status: Active
formerly:
- SOTA-tmp2n6i4
consensus: unreplicated
consensus_note: >-
  One group, one dataset, and the strongest single piece of evidence in the
  record's data material — an 8B model at 15T tokens beating Llama 3.1 8B.
  Nobody has replicated it and nobody has argued against it; the practice it
  argues against (aggressive model-based filtering, LIT-184 and DCLM) is what
  the field was doing when this was published.
title: 'Choose filtering aggressiveness by the token horizon: at long horizons rephrase what a filter would discard'
version: 1
tags:
- data-pipeline
date: '2026-09-08'
published: '2024-12-01'
source:
# The paper that ran both horizons and reported the crossover. LIT-184 is
# the position it argues against and stays in the body — contrast is not
# support (ADR-010).
- LIT-178
implementations: []
summary: >-
  Su et al. (2024), [LIT-178](../literature.d/LIT-178.md) — aggressive model-based filtering wins at 1T
  tokens and loses at 15T, because removing 90% of the data optimises mean
  quality and mean quality is not what binds when the corpus runs out.
  Ensemble the classifiers, rephrase text synthetically instead of discarding
  it, and lean less on heuristics.
---

# SOTA-170: Choose filtering aggressiveness by the token horizon: at long horizons rephrase what a filter would discard

## Source

Su et al. (2024), [LIT-178](../literature.d/LIT-178.md) — [ARXIV-2412.02595](https://arxiv.org/abs/2412.02595).

FineWeb-Edu and DCLM won benchmark gains through aggressive model-based
filtering, **at the cost of removing 90% of the data**. The critique is not
that this is wrong; it is that it is a trade whose sign depends on how many
tokens you intend to train on. Good at a short horizon. Bad at 15T, where you
run out of corpus.

What to do instead, and it is three things together:

- **Ensemble the classifiers** rather than trusting one quality model.
- **Rephrase text synthetically** instead of discarding it — the borderline
  document becomes usable rather than absent.
- **Lean less on heuristic filters.**

## The crossover, which is the whole argument

- **Short horizon.** A high-quality subset improves MMLU by **5.6 over DCLM**
  when training 8B models for 1T tokens. Aggressive filtering wins here, and
  the paper does not dispute it.
- **Long horizon.** The full 6.3T-token dataset **matches** DCLM on MMLU
  while containing **four times more unique real tokens**. An 8B model
  trained for 15T tokens, 7.2T of them from this dataset, beats Llama 3.1 8B
  by +5 MMLU, +3.1 ARC-Challenge and +0.5 averaged over ten tasks.

Matching on quality while holding four times the unique data is the result:
what filtering optimises is mean quality, and mean quality stops being the
binding constraint once the corpus does.

## The other side, and why it is not `contested_by`

[LIT-184](../literature.d/LIT-184.md) — FineWeb — is the position this argues against, and it is a
careful one: its contribution is an ablation methodology showing that
filtering and deduplication choices are worth measuring individually rather
than adopted as a bundle. The two do not contradict each other. FineWeb
measured filters at the horizon it measured them at; this says the answer
moves with the horizon. Naming it `contested_by` would assert a disagreement
neither paper makes.

## Where it sits among the record's other answers to "the corpus is finite"

<!-- inactive-ok-block: SOTA-124 — Proposed, named as one of the three
     answers to the same underlying problem -->
Three practices now answer that question from different directions, and none
of their sources cites the others. [SOTA-124](SOTA-124.md) asks when high-quality data may
be *repeated*. The four-epoch practice drawn from [LIT-166](../literature.d/LIT-166.md) prices repetition
against unique tokens. This asks how much data stays high-quality if you
filter less. A reader out of corpus has three levers, and the record can now
say so.

## Known implementations

- Nemotron-CC itself, and the 8B model trained on it.
