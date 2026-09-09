---
number: 111
status: 'Active'
title: "Use Monarch Mixer where attention's quadratic cost is what bottlenecks training"
version: 3
history:
- version: 3
  date: '2026-09-09'
  note: >-
    Bhardwaj → Fu in the citation line, with LIT-115's correction. The
    recommendation is unchanged.
- version: 1
  note: >-
    Titled "Use for tasks where attention bottlenecks training" — which never names its
    subject. All three practices from this source share the defect: they were
    bullets under a heading that supplied the subject, promoted one-to-one
    without it, so each reads as an instruction with no object.
- version: 2
  note: >-
    Subject restored to the title. The claim is unchanged; the source is
    LIT-115 and has always been Monarch Mixer.
tags:
- attention-techniques
date: '2026-08-24'
published: '2023-10-01'
source:
- LIT-115
summary: >-
  Fu et al. (2023), [LIT-115](../literature.d/LIT-115.md) — [ARXIV-2310.12109](https://arxiv.org/abs/2310.12109).
---

# SOTA-111: Use Monarch Mixer where attention's quadratic cost is what bottlenecks training

## Source

Fu et al. (2023), [LIT-115](../literature.d/LIT-115.md) — [ARXIV-2310.12109](https://arxiv.org/abs/2310.12109).

## The condition the whole cluster turns on

Attention's cost is quadratic in sequence length; Monarch Mixer replaces the
mixing with structured Monarch matrices, which are products of block-diagonal
factors and give sub-quadratic scaling while staying expressible as dense
matrix multiplies — so the hardware still sees GEMMs rather than a sparse
kernel it handles badly.

That last part is the reason this is a serious proposal rather than one more
sub-quadratic scheme. Most alternatives to attention lose in practice because
their theoretical FLOP saving lands on operations the accelerator runs slowly;
keeping the work as GEMMs is what makes the asymptotic win reachable.

## When the condition is not met

At the sequence lengths most language models train on, attention is not the
bottleneck — the MLPs are, and a fused exact-attention kernel ([SOTA-085](SOTA-085.md),
[SOTA-106](SOTA-106.md)) has already removed the memory cost that made attention look worse
than it is. Substituting a sub-quadratic mixer there gives up exactness for
nothing.

So the practice is genuinely conditional, and the title now says on what. Its
two siblings state the other faces of the same condition: [SOTA-110](SOTA-110.md) is the
regime where the condition is met by default, and [SOTA-112](SOTA-112.md) is what to do when
it is met only in part.

The record has no measurement of where the crossover sits, which is the honest
limit — [LIT-115](../literature.d/LIT-115.md) reports the architecture and its scaling, and nobody here has
established the sequence length at which the substitution starts paying for a
transformer of a given size.
