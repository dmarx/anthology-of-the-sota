---
number: 158
status: Proposed
formerly:
- SOTA-tmp0cmo2
promote_when: >-
  A comparison between the two remedies — a bounded-growth activation against
  a soft-capped GLU — at a scale where the instability actually bites; or a
  third group independently reaching a bounded activation for the same
  numerical reason. What would not move it: another paper proposing a fourth
  bounded activation without measuring against SwiGLU-Clip, which is the
  cheap fix any such paper has to beat.
consensus: emerging
consensus_note: >-
  Two groups, months apart, independently decided the field's default
  activation is a numerical liability at frontier scale and shipped bounded
  replacements — LIT-200 at 124B, Kimi K3 at 2.8T. Neither disputes SwiGLU's
  quality; both object to its range. Not `converged`, because the two
  remedies differ and nobody has compared them.
title: "Bound the activation's output range when training in low precision"
version: 1
tags:
- model-architecture
date: '2026-09-08'
source:
# LIT-200 is the one with the evidence: scaling-law experiments, 7.9B and
# 124B, and a comparison against SwiGLU-Clip. Kimi K3's SiTU-GLU is the
# second group reaching the same conclusion, but its report ships the design
# rather than testing the trade, so it is consensus data (ADR-017).
- LIT-200
compared_against:
- SOTA-034
implementations: []
summary: >-
  Jiang et al. (2026), [LIT-200](../literature.d/LIT-200.md) — SwiGLU approximates x² for large positive
  inputs, which is where its expressive capacity comes from *and* what
  enlarges the output range and exacerbates outliers. Two groups independently
  concluded that is intolerable in low precision. What they agree on is the
  constraint; the functions they chose differ.
---

# SOTA-158: Bound the activation's output range when training in low precision

## Source

Jiang et al. (2026), [LIT-200](../literature.d/LIT-200.md) — [ARXIV-2605.25704](https://arxiv.org/abs/2605.25704), for PowLU and the
evidence; Kimi K3 for the second, independent instance.

The diagnosis is precise and it is about the same property twice. SwiGLU
approximates **x²** for large positive inputs. That is where its expressive
capacity comes from, and it is also what enlarges the output range and
exacerbates outliers — harmless at ordinary precision, and not harmless when
the arithmetic is FP8 or narrower.

Two groups reached that conclusion independently, months apart, by different
routes:

- **PowLU** ([LIT-200](../literature.d/LIT-200.md)) identifies the quadratic regime specifically and
  answers with a rational power function: adaptive nonlinearity with
  **bounded growth**, with theory for the properties rather than only curves.
- **SiTU-GLU** (Kimi K3) objects that "both multiplicative factors in SwiGLU
  are unbounded, so coincident large coordinates can produce activation
  outliers and increase overflow risk in low-precision arithmetic", and
  soft-caps both branches with a scaled tanh.

**Neither disputes SwiGLU's quality. Both object to its range.** That
agreement is this practice; the two functions are not.

## Why this is the trunk and not either function

The record cannot recommend PowLU over SiTU-GLU or the reverse, because
nobody has compared them — and it should not have to in order to say the
thing both groups established, which is that an unbounded activation is a
liability once the arithmetic narrows. Filing the constraint separately is
what lets a reader act on the agreement without picking a side of the
disagreement.

It also puts the objection in the same family as [SOTA-161](SOTA-161.md)'s rounding
bias: both are cases where an operation that is fine in FP32 stops being fine
when the format narrows, and where the fix is to bound or correct the
numerics rather than to retune the model.

## Against [SOTA-034](SOTA-034.md), which it qualifies rather than replaces

[SOTA-034](SOTA-034.md) recommends SwiGLU and is already `contested` on exactly these
grounds. This is the positive statement of what the two objections agree on,
and the relation is `compared_against` because [LIT-200](../literature.d/LIT-200.md) ran the comparison:
PowLU against SwiGLU **and against SwiGLU-Clip**. That second arm is what
makes the paper's contribution isolable — hard clipping is the obvious cheap
fix, and a bounded-activation paper that skips it has not shown its function
is doing anything a clamp would not.

The evidence is unusually complete for an activation paper: scaling-law
experiments confirming consistency across model sizes, then the Ling
architecture at 7.9B and 124B total parameters.

## Conditions, and why this is Proposed

What is missing is the comparison *between* the remedies, and any measurement
against SwiGLU at a scale where the instability does not bite — so the size
of what bounding costs, if anything, at ordinary precision is unknown. At
ordinary precision [SOTA-034](SOTA-034.md)'s recommendation stands unqualified.

## Known implementations

- Ling at 7.9B and 124B (PowLU); Kimi K3 at 2.8T (SiTU-GLU).
