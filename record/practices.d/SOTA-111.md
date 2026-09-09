---
number: 111
status: 'Active'
title: "Use Monarch Mixer where attention's quadratic cost is what bottlenecks training"
version: 4
history:
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
- version: 3
  date: '2026-09-09'
  note: >-
    Bhardwaj → Fu in the citation line, with LIT-115's correction. The
    recommendation is unchanged.
- version: 4
  date: '2026-09-09'
  note: >-
    Gained the half of the source it was leaving out (#114). M2 is
    sub-quadratic along the model dimension as well as the sequence
    length, using one primitive for both, and that is what separates it
    from the efficient-attention literature. The recommendation is
    unchanged.
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


## The other axis, which this practice was leaving out

Transformers scale quadratically along **two** axes — sequence length and
model dimension — and almost all efficient-attention work addresses only the
first, because it replaces the sequence mixer and leaves the MLP alone.

[LIT-115](../literature.d/LIT-115.md)'s contribution is one primitive that is sub-quadratic along **both**,
serving as sequence mixer and dimension mixer alike. That is what separates it
from the long-convolution line it builds on, and it is the reason to reach for
it: if the model dimension is as much of a constraint as the context, nothing
in the efficient-attention literature helps and this does.

The measured form: BERT-base and BERT-large quality on GLUE with up to **27%
fewer parameters** and up to **9.1× throughput at 4K**; ViT-b beaten by 1% at
**half the parameters**.

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

So the practice is genuinely conditional, and the title now says on what.
[SOTA-110](SOTA-110.md) states the other face of the same condition: the regime where it is
met by default.

<!-- inactive-ok-block: SOTA-112 — Rejected in #114; named here because this paragraph used to point at it as live guidance -->
The third sibling, [SOTA-112](SOTA-112.md), used to be named here as "what to do when the
condition is met only in part" — interleave M2 with attention. It is retired:
[LIT-115](../literature.d/LIT-115.md) is an attention-free architecture and argues for replacement, so
there is no partial case it describes. If one exists it needs a source.

The record has no measurement of where the crossover sits, which is the honest
limit — [LIT-115](../literature.d/LIT-115.md) reports the architecture and its scaling, and nobody here has
established the sequence length at which the substitution starts paying for a
transformer of a given size.
