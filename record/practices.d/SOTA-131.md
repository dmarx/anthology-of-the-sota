---
number: 131
status: Active
title: 'When training with Muon at scale, rescale query and key weights whenever attention logits exceed a threshold (QK-Clip)'
version: 3
history:
- version: 2
  date: '2026-09-07'
  note: >-
    Sourced to LIT-155 and LIT-119 as well as LIT-132. The mechanism the
    practice argues from is LIT-155's, and the scope qualifier in its own
    title rests on LIT-119's small-scale runs without clipping. K3 keeping
    the optimizer at 2.8T is adoption, so it stays consensus evidence under
    ADR-017. The recommendation is unchanged.
- version: 3
  date: '2026-09-10'
  note: >-
    Enriched from the #123 readings. The recommendation is unchanged;
    the source list, the numbers or the neighbourhood are.
tags:
- training-optimization
date: '2026-09-05'
source:
# LIT-132 is where QK-Clip is introduced. LIT-155 established attention-logit
# growth as a distinct instability and is the mechanism the practice argues
# from; LIT-119 trained 90M and 0.6B with Muon and no clipping and reports
# stable runs, which is the evidence for the "at scale" in the title. LIT-159,
# LIT-122 and LIT-131 are the line and its adopter, and LIT-139 is the
# variation that does without — all body (ADR-017).
- LIT-132
- LIT-155
- LIT-119
# Corrective succession (ADR-017). QK-Clip is added on top of Muon with
# decoupled weight decay and RMS-matched updates, on the defect it names: at
# trillion scale Muon drives the maximum attention logit past 1000, which
# brings loss spikes and occasional divergence. The Sequence section below
# still spells the same order out in prose; that duplication predates this.
corrects:
- SOTA-121
summary: >-
  Kimi Team (2025), [LIT-132](../literature.d/LIT-132.md) — MuonClip carried a 1T/32B MoE through 15.5T tokens with zero loss spikes where plain Muon let attention logits pass 1000; confirmed at 2.8T in [LIT-131](../literature.d/LIT-131.md).
compared_against:
- SOTA-192
---

# SOTA-131: When training with Muon at scale, rescale query and key weights whenever attention logits exceed a threshold (QK-Clip)

## Source

Kimi Team (2025), [LIT-132](../literature.d/LIT-132.md) — the Kimi K2 report.

Muon with weight decay and RMS-matched updates ([SOTA-121](SOTA-121.md)) is enough at small
scale. At a trillion parameters the K2 team found it drives the maximum
attention logit past 1000 early in training, and logits of that size bring
loss spikes and occasional divergence. QK-Clip is the addition: after each
step, for any head whose maximum logit exceeds a threshold, rescale that
head's query and key projection weights so it does not. The clip acts on
weights, so the served model is unchanged, and it fires only where needed.
With it, K2 trained on 15.5T tokens without a single loss spike; K3
([LIT-131](../literature.d/LIT-131.md)) keeps the same optimizer at 2.8T.

Conditions: the failure this prevents is a large-scale one. [LIT-119](../literature.d/LIT-119.md) trained
90M and 0.6B models with Muon and no clipping and reports stable runs, so
the clip is insurance whose premium is a per-head max-logit check per step —
cheap, but not free, and unnecessary until the logits say otherwise. The
threshold is a hyperparameter; the report's value is tuned for its model.

## Variations

DeepSeek-V4 ([LIT-139](../literature.d/LIT-139.md)) pretrains 1.6T and 284B MoE models with Muon and
without QK-Clip, and the report says so in as many words: "The attention
architecture of DeepSeek-V4 series allows us to directly apply RMSNorm on
the attention queries and KV entries, which effectively prevents attention
logits from exploding. Consequently, we do not employ the QK-Clip technique
in our Muon optimizer." So the clip is one of two ways to the same
invariant, and QK-normalisation is the other — not a reading of secondary
coverage but the primary source's own account, under the heading "Avoiding
Exploding Attention Logits".

**The other way now has its own practice and its own source.**
[SOTA-192](SOTA-192.md) files QK-normalisation against [LIT-088](../literature.d/LIT-088.md), which diagnoses the
mechanism this practice's threshold is defending against: logits grow with the
weights until the softmax is almost one-hot with near-zero entropy, at which
point the gradient vanishes and the run diverges. ViT-22B observed it at ~8B
parameters and shows a before/after.

The two are `compared_against` and **nobody has actually compared them.** The
open question is whether the clip is only necessary when the normalisation is
absent — DeepSeek-V4's report is consistent with that and does not establish
it.

## Sequence

Muon ([LIT-159](../literature.d/LIT-159.md)) → weight decay and RMS matching
so AdamW's hyperparameters transfer ([LIT-122](../literature.d/LIT-122.md), [SOTA-121](SOTA-121.md)) → QK-Clip so the
attention logits stay bounded at scale (this practice) → [LIT-131](../literature.d/LIT-131.md) adds Per-Head
Muon on top, orthogonalizing each attention head's momentum block separately
so that heads with larger gradients stop dominating the shared update.
Each step keeps the one before.

## Mechanism

The failure QK-Clip answers is attention-logit growth, which
[LIT-155](../literature.d/LIT-155.md) established as a distinct instability with a normalization
remedy, and — the useful part — reproducible in small models at high
learning rate rather than only at the scale where it first cost someone a
run. That is also why [LIT-139](../literature.d/LIT-139.md) can decline QK-Clip: an RMSNorm on the queries
and compressed KV entries bounds the same quantity, so the choice is between
normalizing the input to the logit and clipping the weights after the fact.

## Known implementations

- Kimi K2, Kimi K3 (QK-Clip); DeepSeek-V4 (Muon with QK-norm, no clip)
