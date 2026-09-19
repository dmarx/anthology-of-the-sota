---
number: 252
status: Active
formerly:
- SOTA-tmprcin9
consensus: unreplicated
consensus_note: >-
  One paper, one setting. Nobody in this record has agreed or disagreed, and
  the claim is about a design pattern rather than a measured quantity, which
  makes it easy to believe and hard to check. Filed for the argument, which
  is unusually clean, rather than for a number.
title: 'Make the full-resolution path affordable instead of upsampling, when the shortcut is what breaks correctness'
version: 1
tags:
- vision-and-graphics
- systems-optimization
date: '2026-09-19'
source:
- LIT-113
introduced_by:
- LIT-113
implementations:
- Gaussian Shell Maps
summary: >-
  Abdal et al. (2023), [LIT-113](../literature.d/LIT-113.md) — [ARXIV-2311.17857](https://arxiv.org/abs/2311.17857). Prior 3D GANs render
  small and upsample in 2D because volume rendering is too slow at training
  resolution — but a 2D upsampler is multi-view inconsistent by construction.
  Efficient Gaussian rendering makes native 512x512 affordable, and the
  inconsistency leaves with the upsampler rather than being mitigated.
---

# SOTA-252: Make the full-resolution path affordable instead of upsampling, when the shortcut is what breaks correctness

## Source

Abdal et al. (2023), [LIT-113](../literature.d/LIT-113.md) — [ARXIV-2311.17857](https://arxiv.org/abs/2311.17857).

## The rule

When a system is too slow to run at full resolution and the workaround is to
run it small and upsample, **check what the upsampler costs in correctness
before treating the speed problem as the problem.**

In the case this comes from, the cost is categorical rather than incremental:
a 2D upsampler is **multi-view inconsistent by construction**. It works on
one rendered view at a time and has no way to know what the neighbouring view
will contain. No amount of training fixes that, because it is a property of
where the operator sits.

So the fix is not a better upsampler. Making the native path affordable —
here, Gaussians on articulable shells instead of volume rendering — removes
the defect by removing the stage that caused it.

## Why this is a rule and not an anecdote

The shape recurs whenever a resolution or precision shortcut is introduced to
buy throughput:

1. The system cannot afford the honest path
2. A cheaper stage is inserted
3. That stage has a defect the honest path does not have
4. Effort goes into mitigating the defect

The recommendation is to ask at step 4 whether step 1 is still true. Hardware
and representation both move; a shortcut adopted when the honest path cost 10x
is worth re-examining when it costs 1.2x.

## Conditions

- **The defect must be structural, not statistical.** This is the part that
  makes the rule usable: "the upsampler is multi-view inconsistent by
  construction" is a statement about what it *can* see. A stage that is merely
  worse on average does not qualify — that is an ordinary quality trade
- **The native path has to actually become affordable.** The paper earns this
  with a representation change, not with patience
- **One paper, one setting.** See `consensus_note`. The 512x512 figure is
  3D human generation from single-view data

## Where else the record has this shape without naming it

[SOTA-249](SOTA-249.md) is the mirror image and worth reading beside this one: there,
recomputation *is* the right answer because the trade buys memory the system
genuinely does not have. The distinction is step 3 — recomputation has no
correctness defect, and a 2D upsampler does.
