---
number: 242
status: Proposed
formerly:
- SOTA-tmp4fwxw
promote_when: >-
  A pretraining report that states its selection target as a sample of the
  text it wants rather than as a quality rubric or a classifier's label, or
  an evaluation that runs a distribution-matched selection against a
  quality-classifier selection on the same corpus and token budget and says
  which won and at what breadth of target. What would not move it: another
  quality classifier beating a heuristic, which is the opposing frame getting
  better at its own game and says nothing about whether the frame is right.
title: 'Select pretraining data by matching a target distribution you can sample from, not by scoring it for quality'
version: 1
consensus: unreplicated
consensus_note: >-
  One group, 2023, and the record's own filtering practices take the other
  frame — SOTA-170 and the DCLM line score documents for quality and discard
  the low scorers. Nobody has disputed distribution matching and nobody has
  staged the comparison; the two frames coexist in the literature without
  having been made to argue.
tags:
- data-pipeline
date: '2026-09-17'
source:
- LIT-087
introduced_by:
- LIT-087
implementations:
- LIT-087
summary: >-
  Xie et al. (2023), [LIT-087](../literature.d/LIT-087.md) — data selection needs a description of what you
  want, not a criterion for what is good. Supply a small sample of the target
  text and resample the raw corpus to match it. The target is an artifact you
  can produce; a quality rubric is an argument you have to win.
---

# SOTA-242: Select pretraining data by matching a target distribution you can sample from, not by scoring it for quality

## Source

Xie et al. (2023), [LIT-087](../literature.d/LIT-087.md) — [ARXIV-2302.03169](https://arxiv.org/abs/2302.03169).

## The two frames

Almost everything the record holds about choosing pretraining data is
**quality-shaped**: score each document for how good it is, keep the good
ones. `SOTA-170` is the record's central filtering practice and the thing it
tunes is *how aggressive a quality classifier to run*; the FineWeb-Edu and
DCLM work it argues with differs on the setting, not on the question. The
question is always *is this document good enough*.

DSIR asks a different one. Given a small sample of the text you actually
want — the target — and a large raw corpus, select a subset **distributed
like the target**. That is classical importance resampling, and the paper
makes it tractable by estimating the weights in a reduced feature space
rather than over text.

## Why the frame is the recommendation and the method is not

A quality criterion is a claim about documents in the abstract, and it has to
be defended: whose definition of quality, good for what, measured how. Every
argument about filtering aggressiveness is an argument about that criterion,
and it is unfalsifiable until somebody trains on it.

**A target distribution is an artifact.** You produce it by pointing at text
you want more of. It is not a claim that the target is *good*, only that it
is what you are aiming at, so the argument moves from a rubric nobody can
settle to a sample anybody can inspect. The specification is also reusable:
the same target admits any selection method, which is what makes selections
comparable at all — and is the precondition for the proxy filed alongside
this one.

The method is incidental to that. Hashed n-grams are 2023's tractable
estimator and will not be the last one; the instruction here is about what
you supply as input, not about how the weights get computed.

## Conditions

**The target has to exist, and it has to be sampleable.** This is the real
cost, and it is where the frame can simply fail to apply. If what you want is
"generally capable", there is no sample to point at, and the quality frame is
not being lazy — it is answering the only question anyone has stated.

**Breadth changes which frame wins.** The paper's own qualification: for
domain-specific targets, plain top-`k` heuristic classification is
competitive, and the authors reason that "diversity may be less important
than in the general-domain setting". DSIR's margin over heuristic
classification is **0.9%**, and its advantage is attributed to selecting the
most diverse source distribution. So the frame buys most where the target is
broad enough that a scorer collapses it, and least where the target is narrow
enough that a scorer captures it.

**Selecting for the wrong target costs about 1.7 points.** Within-domain F1
82.9% against cross-domain 81.2% — small, and the right order of magnitude to
know before reusing somebody else's target.

**Hashed n-grams cannot express structure, reasoning or correctness.** "Match
the target" is only as good as the target, and nothing in the mechanism will
warn you that the target was badly chosen.

## Why Proposed

The evidence is a 0.9% margin from 2023, at a scale well below where the
record's other data practices operate, and the correlational result it rests
on has not been re-run since. That is a reason not to mark it `Active` and
not a reason for the record to be silent on the frame — `DP-006`. What the
condition above is waiting for is somebody stating a selection target as a
sample, or running the two frames against each other; neither has happened in
the literature this record holds.

## Known implementations

- **DSIR** — the paper's own release, selecting from the Pile.
