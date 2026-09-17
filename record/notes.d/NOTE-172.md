---
number: 172
status: Read
formerly:
- NOTE-tmpfvfhu
paper: LIT-386
title: 'SuperGlue: Learning Feature Matching with Graph Neural Networks'
version: 1
date: '2026-09-17'
summary: >-
  Learn the matcher instead of hand-designing it: a GNN predicts assignment
  costs, differentiable optimal transport solves them, and correspondence and
  rejection happen jointly. Filed for the line rather than for a practice —
  its surviving assumption, that a detector ran first, is what the next paper
  identifies as the binding constraint.
---

# NOTE-172: SuperGlue: Learning Feature Matching with Graph Neural Networks

Read from [LIT-386](../literature.d/LIT-386.md) — [ARXIV-1911.11763](https://arxiv.org/abs/1911.11763).

## What it replaced

The paper is precise about its target: "traditional, hand-designed heuristics".
In matching, that means the ratio test and the filtering conventions built
around it — rules that decide whether a putative correspondence is real using
local evidence and a threshold somebody tuned.

SuperGlue replaces them with "priors over geometric transformations and
regularities of the 3D world" learned end to end from image pairs. The
mechanism is worth stating because it explains why the result is more than an
accuracy delta: a graph neural network predicts assignment costs, and a
**differentiable optimal transport** step solves the assignment — so finding
correspondences and rejecting unmatchable points are one operation rather than
a match followed by a filter.

Attention supplies the context: an assignment is made in view of the other
assignments and the 3D structure they imply, which a per-pair threshold cannot
do.

## The assumption it does not question

It "matches two sets of local features". The detector runs first, upstream,
untouched — and the paper positions itself as something you drop into an
existing SfM or SLAM system, which is exactly the framing that keeps the
preceding stage in place.

That is not a criticism of the paper, which is excellent at what it set out to
do. It is the observation that makes the next one legible: having made
matching learned and strong, the remaining weakness has to be somewhere else,
and [LIT-387](../literature.d/LIT-387.md) locates it in the detector.

## Why it is filed with no practice

Its recommendation — learn the matcher rather than hand-designing it — was
overtaken twice within eighteen months: first by removing the detector, then
by removing matching as a separate stage. Filing it as a live practice would
recommend a middle step of a line whose end the record now holds at
[SOTA-236](../practices.d/SOTA-236.md).

But filing nothing would leave that endpoint as a conclusion without an
argument. The record gains the step where this stage was shown to be learnable
at all, and the constraint it left behind, which is what the next result is
about.
