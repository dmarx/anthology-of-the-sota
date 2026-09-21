---
number: 19
status: Active
formerly:
- THEORY-tmp1rmwn
title: 'A softmax head with nothing to attend to must place its mass somewhere, so models learn a positional sink'
version: 1
tags:
- attention-techniques
- numerics-and-precision
date: '2026-09-17'
source:
- LIT-191
- LIT-190
explains:
- SOTA-134
summary: >-
  Xiao et al. (2023), [LIT-191](../literature.d/LIT-191.md) — attention scores are normalized to sum to one,
  so a head with nothing it needs to attend to still has mass to shed, and it
  learns to dump it on the positions every query can see, which under causal
  masking are the first few tokens. The evidence that it is positional rather
  than semantic: replacing the first four tokens with linebreaks moves
  Llama-2-13B from 5.40 to 5.60 perplexity, while evicting them from the cache
  moves it to 5158. [LIT-190](../literature.d/LIT-190.md) finds the same concentration in the residual
  stream, and [SOTA-134](../practices.d/SOTA-134.md)'s gate removes sinks rather than relocating them, which
  is what the account predicts.
---


<!-- inactive-ok-file: SOTA-248 — Proposed, filed in this same change,
     and named here as one of the two remedies the source paper tested. Its
     own status says why it is not asserted: the evidence is at 109M and the
     phenomenon intensifies with scale. -->

# THEORY-019: A softmax head with nothing to attend to must place its mass somewhere, so models learn a positional sink

## Source

Xiao et al. (2023), [LIT-191](../literature.d/LIT-191.md) —
[ARXIV-2309.17453](https://arxiv.org/abs/2309.17453); with Sun et al. (2024),
[LIT-190](../literature.d/LIT-190.md).

## What was actually shown

**The mechanism is an accounting constraint, not a learned preference.**
Softmax normalizes its scores to sum to one. A head that has nothing it needs
to attend to at a given position cannot therefore assign zero everywhere — the
mass has to land somewhere. The only positions every query can see under
causal masking are the earliest ones, so that is where models learn to put it.
Xiao et al. name the role the **attention sink**.

**It is positional, and that is measured rather than assumed.** Beyond the
bottom two layers, every layer and head of Llama-2-7B attends heavily to the
first few tokens regardless of content. Substituting those first four tokens
with linebreaks moves perplexity from **5.40 to 5.60** — essentially nothing.
Whatever the sink is doing, it is not reading them.

**And it is load-bearing, which the same experiment shows by contrast.**
Evicting the initial tokens from the cache removes a large part of the softmax
denominator and shifts the entire attention distribution: Llama-2-13B goes
from **5.40 to 5158.07** perplexity. The failure is a cliff, not a slope. A
mechanism whose removal costs three orders of magnitude is not an artifact.

**Two independent confirmations.** [LIT-190](../literature.d/LIT-190.md) finds
the corresponding concentration on the activation side — massive activations
at particular positions in the residual stream — from a different group and a
different measurement. And [SOTA-134](../practices.d/SOTA-134.md)'s
head-specific output gate **eliminates** the sink pattern rather than moving
it elsewhere, which is exactly what this account predicts: give a head a way
to scale its whole output down and it has no surplus mass to shed, so no sink
is needed.

**What could have come out the other way.** If the sink were semantic, the
linebreak substitution would have hurt. If it were incidental, eviction would
have degraded gracefully. If the mechanism were something other than surplus
softmax mass, a gate on the output — which does not touch the attention
distribution's normalization — would have had no reason to remove it.

## What this explains

**Why keeping four initial tokens repairs streaming**, which is the practice
[LIT-191](../literature.d/LIT-191.md) is mostly cited for: window attention
drops exactly the entries the denominator depends on, so restoring them
restores the distribution, and it works without any finetuning because nothing
was broken except the cache.

**Why the gate in [SOTA-134](../practices.d/SOTA-134.md) both improves quality
and removes sinks**, which reads as two unrelated benefits until you have this
account. They are one effect: the practice and the streaming fix are answers
to the same pressure from opposite ends — one gives the surplus mass a
designated place to go, the other arranges for there not to be any.

## What this does not say

**It does not make sinks a defect.** In an ungated model the sink is
load-bearing, and the 5158 figure is what removing it costs. "Attention sinks
are an artifact to be eliminated" is the reading this document exists to
block: they are eliminable only by changing the architecture so the pressure
that creates them is gone.

**It does not explain why four.** One or two initial tokens are not enough,
four is, and more adds little. The account says mass must land on globally
visible positions; it does not predict the number, and nobody has derived it.

**It does not account for the models' failure to use long context.**
[LIT-191](../literature.d/LIT-191.md) volunteers that larger caches do not
monotonically lower perplexity — Llama-2-7B is better at 4+2044 than at
4+4092 — which is a separate phenomenon this account says nothing about.

**The account did not originate here, and the tested version of the fix is
older than the popular one.** [LIT-414](../literature.d/LIT-414.md)
(June 2023) reached the same mechanism from the quantization side — a head
approximating a no-op must drive its softmax input to extremes, producing the
activation outliers that break INT8 — and shipped **two** remedies with
experiments: clipped softmax ([SOTA-248](../practices.d/SOTA-248.md))
and gated attention, which is [SOTA-134](../practices.d/SOTA-134.md). That the
same account was reached independently from quantizability and from streaming
is the strongest support this document has.

**What remains untested is `softmax₁` specifically** — one added to the
denominator, [LIT-413](../literature.d/LIT-413.md), the version most
people have read. Its author reports no experiments and says so. The record
holds tested siblings and nothing on that exact formulation, which is worth
keeping visible: the popular version of an idea and the evidenced version are
not always the same version.
