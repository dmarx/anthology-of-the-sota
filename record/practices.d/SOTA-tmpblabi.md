---
status: Proposed
promote_when: >-
  A second group compares a bidirectional teacher against a causal teacher
  for the same causal few-step student, with the two teachers matched in
  quality before distillation, and reports a video metric or human
  preference. CausVid's own comparison cannot separate "causal" from
  "weaker", because its causal teacher is also the worse model.
consensus: unreplicated
consensus_note: >-
  One controlled comparison, CausVid (LIT-631, Table 4). Self Forcing
  (LIT-629) adopts the arrangement: a bidirectional Wan2.1-14B serves as the
  distribution-matching teacher for a causal 1.3B student. That is adoption
  and not a second test. Read as of 2026-09.
title: 'When distilling a causal few-step video generator, take the teacher bidirectional, not causal'
version: 1
tags:
- generative-modeling
- inference-optimization
- vision-and-graphics
date: '2026-09-24'
source:
- LIT-631
introduced_by:
- LIT-631
implementations:
- 'CausVid'
- 'Self Forcing'
summary: >-
  Yin et al. (2024), [LIT-631](../literature.d/LIT-631.md). A block-causal 4-step student distilled from a
  bidirectional teacher beats one distilled from a causal teacher, at the same
  initialization, data and step count (Table 4). The causal teacher is also
  the weaker model before distillation, so the result shows the arrangement
  works and does not isolate why.
---

# SOTA-tmpblabi: When distilling a causal few-step video generator, take the teacher bidirectional, not causal

## Source

Yin et al. (2024), [LIT-631](../literature.d/LIT-631.md) — CausVid, Table 4.

## The claim

A streaming video generator has to be causal: each chunk is generated from
the ones before it, with a KV cache. It does not follow that its teacher has
to be causal. **Distil the causal student from a bidirectional teacher**,
which sees the whole clip and generates it well, rather than first making
the teacher causal.

CausVid compares the two at the same ODE-regression initialization,
architecture, data and 4 sampling steps (Table 4), scored as temporal
quality / frame quality / text alignment:

| Teacher | Student score |
|---|---|
| Bidirectional | 94.7 / 64.4 / 30.1 |
| Causal | 91.9 / 61.7 / 28.2 |

The same table shows the student initialized by ODE regression beats one
without it: 94.7 / 64.4 / 30.1 against 93.4 / 60.6 / 29.4.

## Conditions

- **The result does not isolate causality.** The causal teacher is also the
  weaker model before any distillation: 92.4 / 60.1 / 28.5 against the
  bidirectional teacher's 94.6 / 62.7 / 29.6 at 100 steps (Table 4). The
  authors attribute the gap to the causal teacher's error accumulation
  passing into its student (Fig. 8). That is an explanation, and the
  ablation cannot tell it apart from "the better teacher makes the better
  student".
- **One run per arm** and no confidence intervals.
- **The student is worse than its teacher on two axes.** It "performs worse
  in temporal flickering and output diversity" (§5.2), and the diversity loss
  is "characteristic of reverse KL" (§6). The practice picks the teacher. It
  does not make distillation free.
- **Distribution matching is the distillation method throughout.** The record
  does not hold DMD or DMD2. Whether the result carries to other distillation
  objectives is untested.
