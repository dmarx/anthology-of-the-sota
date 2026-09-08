---
status: Proposed
formerly:
- SOTA-tmpa81q9
promote_when: >-
  A frontier report that says its token budget was chosen with the
  quantization plan in view, or an independent group refitting the
  precision-aware law above 1.7B and reporting whether the
  data-makes-quantization-worse effect survives at the scale where FP4
  actually ships. What would not move it: another paper quantizing a
  heavily-trained model and finding it degrades, which is the observation
  rather than the law.
consensus: unreplicated
consensus_note: >-
  One group, one functional form, fit on 465 pretraining runs but validated
  only to 1.7B and 26B tokens. Nobody has disputed it and nobody has refit
  it; the two frontier reports in this record that quantize say nothing about
  having priced it into their token budget.
title: 'Treat the pretraining token budget and the post-training quantization plan as one decision, not two'
version: 1
tags:
- training-optimization
date: '2026-09-08'
published: '2024-11-01'
source:
- LIT-186
implementations: []
summary: >-
  Kumar et al. (2024), [LIT-186](../literature.d/LIT-186.md) — degradation from post-training quantization
  *increases* with how much data the model was trained on, to the point where
  additional pretraining data becomes actively harmful if the model will be
  quantized afterwards. Fit over 465 runs into one precision-aware scaling
  law covering both pre- and post-training quantization.
---

# SOTA-160: Treat the pretraining token budget and the post-training quantization plan as one decision, not two

## Source

Kumar et al. (2024), [LIT-186](../literature.d/LIT-186.md) — [ARXIV-2411.04330](https://arxiv.org/abs/2411.04330).

Standard scaling laws are silent about numerical precision, which is strange
given that precision decides both training cost and serving cost. This fits
precision-aware laws for both sides.

**The training side** is the tidy half: low precision reduces the model's
*effective parameter count*, which makes the extra loss from training in low
precision predictable rather than empirical, and lets the law price parts of
a model held at different precisions. A practical suggestion falls out —
training larger models in lower precision may be compute-optimal.

**The inference side is the counter-intuitive one, and it is the
recommendation.** Degradation from post-training quantization *increases*
with how much data the model was trained on. Past a point the law can locate,
additional pretraining data becomes **actively harmful** if the model will be
quantized afterwards. More training makes a model less robust to being
compressed.

## Why that is a recommendation and not a curiosity

The usual instinct — train on more data, it can only help — is wrong for any
model that will be served quantized, which is most of them. And the decision
it breaks is one normally made by different people at different times: the
pretraining budget is set months before anyone picks a serving format.

The practice is therefore about *sequencing* rather than about a number: if
the serving plan is FP4, that fact belongs in the room when the token budget
is chosen, and the law is what lets it be priced instead of argued.

## Conditions, and why this is Proposed

Both halves are unified into a single functional form, fit on **over 465
pretraining runs** — which is a lot of evidence for the shape — and validated
up to **1.7B parameters and 26B tokens**, which is far below everything that
ships FP4 today. That gap is the whole reason for the status: the effect is
well measured where it was measured, and the regime it matters most in is not
that regime.

Read with [SOTA-163](SOTA-163.md), which says what each quantization width can bear.
That practice answers "what will this format survive"; this one answers "does
my pretraining choice make the answer worse". Two frontier reports in the
record quantize — DeepSeek-V4 and Kimi K3 — and neither says whether it
priced this in.

## Known implementations

- None reported. The two frontier reports that quantize are silent on the
  coupling.
