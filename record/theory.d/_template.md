---
# Don't copy this file by hand — run `luria new theory`, which assigns the
# code and fills in what a machine can compute.
#
# A theory is a claim about WHY something happens, or about what is true of
# these systems. State it as a finding, not as an instruction: "Batch
# normalization helps by smoothing the optimization landscape" rather than
# "Use batch normalization". If what you are about to write tells the reader
# what to do, it is a practice — `luria new sota` (ADR-tmpvv7zp).

# Active | Proposed | Deferred | Superseded | Rejected, optionally " — note".
# What each one means here is in luria.yaml, and it is NOT what the same word
# means on a practice: this status says whether the record believes the
# ACCOUNT, and an explanation can be `Rejected` while the thing it explained
# goes on working exactly as well as it ever did.
status: Proposed

# REQUIRED while the status is Proposed or Deferred; delete it when the
# explanation goes Active. What would settle it — a KIND of result, not a
# quantity of them (ADR-014). An explanation that cannot say what would show
# it wrong is a story, and this field is where that shows up.
promote_when: >-
  The kind of result that would settle this, stated so that the wrong kind
  of result cannot satisfy it.

# The claim. Repeat it as the body's `# THEORY-NNN:` heading; the lint checks
# that the two agree.
title: What is true, stated as a finding

version: 1

# Exactly one of the thirteen, from the same table the practices and the
# reading list use (ADR-026). Most explanations land in
# `analysis-and-evaluation`, whose blurb already says theory belongs there —
# but a claim about WHY a normalization works is `model-stability`, the same
# topic as the practice it explains, and taking the topic of what you are
# explaining is usually right.
tags:
- analysis-and-evaluation

date: '2026-01-01'

# There is deliberately no `published:` line. It is DERIVED from the first
# entry in `source:` below, and writing it down is a lint violation, because
# the value has one home and this is not it.

# REQUIRED, and a LIST. The papers this account rests on, primary first. An
# explanation with no paper behind it is a hunch, and the lint will say so.
source:
- LIT-000

# Optional. The practices this explains — which is the whole point of the
# scheme, and is optional anyway, because a finding that underwrites nothing
# YET is still a finding. `luria link --fix` writes `explained_by:` back onto
# each practice named here; never write that side by hand.
explains: []

# What the index table shows. The title already carries the claim, so spend
# this on provenance and on the sharp edge: who said it, and what it does not
# say. Prose, so bare codes in it get linked by `luria link --fix`.
summary: >-
  Author et al. (YEAR), LIT-000 — what was shown, and the reading of it that
  the evidence does not support.
---

<!-- unresolved-ok-file: LIT-000 — the placeholder a new document replaces -->

# THEORY-NNN: What is true, stated as a finding

## Source

Author et al. (YEAR), LIT-000.

## What was actually shown

The experiment or argument, and its conditions. An explanation is only as
good as what would have falsified it, so say what the paper did that could
have come out the other way.

## What this does not say

The reading the result invites and does not support. This section is the one
that earns the document — a finding filed without it becomes the stronger
claim nobody checked, which is how "sharpness correlates with test error"
gets cited as "flatten the minimum and it generalizes".
