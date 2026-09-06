---
status: Proposed
promote_when: >-
  A head-to-head of RLVR-on-base against SFT-then-RLVR from the same base
  and the same data, on a base whose pre-RL reasoning behaviour is reported.
  LIT-167 makes *which base* the live variable, so a result that does not
  control for it cannot settle this.
consensus: contested
consensus_note: >-
  LIT-167 finds the base model already exhibits the behaviour the track
  attributes to RLVR, and the source itself ships the SFT path for the
  models it releases.
title: 'Skip the reasoning SFT stage and run RL with verifiable rewards directly on the base model'
version: 1
tags:
- training-optimization
date: '2026-09-05'
published: '2025-12-01'
source:
- LIT-130
summary: >-
  Olmo Team (2025), [LIT-130](../literature.d/LIT-130.md) — the RL-Zero track: RLVR on the base model with
  no reasoning SFT in between, released as an open benchmark for studying RL
  rather than as the recommended recipe; a variation on [SOTA-129](SOTA-129.md) that the
  record keeps so the family of reasoning recipes can be traced.
---

# SOTA-130: Skip the reasoning SFT stage and run RL with verifiable rewards directly on the base model

## Source

Olmo Team (2025), [LIT-130](../literature.d/LIT-130.md) — the Olmo 3 RL-Zero track.

Take the pretrained base, skip the supervised stage on reasoning traces, and
run reinforcement learning with verifiable rewards straight away: a
rule-based verifier with reference answers for math, test cases for code, an
LLM judge for general chat. Olmo 3 releases four such 7B series with their
data and checkpoints so that RL algorithms, and the effect of pretraining
data on RL, can be studied from a clean start.

Why *Proposed*: the source itself calls the track experimental and positions
it as a benchmark, and the Think models Olmo 3 actually ships go through the
SFT stage ([SOTA-129](SOTA-129.md)). The idea predates Olmo 3: the "R1-Zero" style of training
is where the name comes from, and that work is now filed ([LIT-164](../literature.d/LIT-164.md)).
Olmo 3 remains the source because it is the open, reproducible statement of
the pathway.

A second reason to stay *Proposed* arrived with the literature.
[LIT-167](../literature.d/LIT-167.md) finds that DeepSeek-V3-Base already exhibits the "Aha moment"
before any RL, and that Qwen2.5 bases reason without a prompt template — so
how much of the result belongs to skipping SFT, and how much to what the
base model already carried, is unsettled. "Run RLVR directly on the base" is
a claim whose answer may depend on which base. [LIT-119](../literature.d/LIT-119.md) cites the pathway to
mark the other direction one can go from [SOTA-129](SOTA-129.md): it removes the middle
stage, where the anti-curriculum ([SOTA-123](SOTA-123.md)) merges the first two.
