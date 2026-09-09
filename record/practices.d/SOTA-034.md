---
number: 34
status: 'Active'
consensus: contested
consensus_note: >-
  Two independent groups, months apart, object to SwiGLU's unboundedness as a
  numerical liability in low-precision training and ship bounded replacements
  — LIT-131 at 2.8T, LIT-200 at 124B. Neither disputes its quality, and
  neither compares the two remedies, so the recommendation is qualified
  rather than replaced.
contested_by:
- LIT-131
- LIT-200
title: 'Use SwiGLU activation for transformers'
version: 3
history:
- version: 3
  date: '2026-09-09'
  note: >-
    Noam → Shazeer in the citation line. LIT-030's first_author held the
    author's given name rather than his surname, so every rendering read
    "Noam et al." The recommendation is unchanged.
- version: 2
  date: '2026-09-07'
  note: >-
    Gained the GLU origin it never had (LIT-199), the sibling to K3's
    SiTU-GLU (LIT-200), and `contested` on the strength of the two.
    The recommendation is unchanged at ordinary precision.
tags:
- model-architecture
date: '2026-08-24'
published: '2020-02-01'
source:
- LIT-030
summary: >-
  Shazeer et al. (2020), [LIT-030](../literature.d/LIT-030.md) — [ARXIV-2002.05202](https://arxiv.org/abs/2002.05202). Contested at frontier
  scale in low precision: two groups now ship bounded replacements, on the
  grounds that SwiGLU's unbounded factors produce activation outliers.
implementations:
- llama2
compared_against:
- SOTA-158
---

# SOTA-034: Use SwiGLU activation for transformers

## Source

Shazeer et al. (2020), [LIT-030](../literature.d/LIT-030.md) — [ARXIV-2002.05202](https://arxiv.org/abs/2002.05202).

## Where the gate came from

The record recommended SwiGLU without holding the GLU its name refers to.
[LIT-199](../literature.d/LIT-199.md) is that paper, and its argument is about **gradients rather than
expressivity**: an LSTM-style tanh gate puts a downscaling factor on both
branches, so the gradient shrinks multiplicatively with depth, while gating a
*linear* unit leaves a path with no downscaling — a multiplicative skip
connection. The gate is there to let depth work.

That matters for what follows. The linear, unbounded branch is the thing the
design was chosen for, and unboundedness is precisely what the two objections
below are about. Which is why both remedies **soft-cap** the branch rather
than removing it.

## Contested: the range, not the quality

Two independent groups, months apart, decided SwiGLU's unboundedness is a
numerical liability at frontier scale in low precision.

## Variations

**SiTU-GLU** ([LIT-131](../literature.d/LIT-131.md)), the first replacement in the record. The
objection is about range, not quality: both of SwiGLU's multiplicative
factors are unbounded, so coincident large coordinates produce activation
outliers and raise the overflow risk in low-precision arithmetic. The
original GLU's sigmoid gate is bounded but gives up the approximately linear
positive regime that Swish has. SiTU-GLU applies a scaled `tanh` soft cap to
the linear factor of the Swish gate and, independently, to the up branch —
near-linear at the origin, bounded far from it — with a different cap
constant per branch. Kimi K3 ships it at 2.8T.

One group, one model, no ablation: the report gives the motivation and the
functional form and does not measure SiTU-GLU against SwiGLU anywhere.

**PowLU** ([LIT-200](../literature.d/LIT-200.md)) is the other one, and it is the better-evidenced of
the pair. Same objection reached from a different angle: for large positive
inputs SwiGLU approximates x², and that quadratic amplification is what
enlarges the output range and produces the outliers. The remedy is a rational
power function — adaptive nonlinearity, bounded growth — with scaling-law
experiments across sizes and results on the Ling architecture at 7.9B and
124B against **SwiGLU-Clip as well as SwiGLU**. That control matters: hard
clipping is the obvious cheap fix, and a bounded-activation paper that skips
it has not isolated its own contribution.

## What this does and does not settle

The recommendation stands at ordinary precision. Neither paper claims SwiGLU
is worse; both object to its *range* when the arithmetic is narrow, which is
a condition rather than a refutation.

What is missing is the comparison nobody has run: the two remedies against
each other, and either against SwiGLU at a scale where the instability does
not appear. Until then this is `contested` rather than superseded — the
field's default is being replaced in two places for one stated reason, and
neither replacement has been checked against the other.

## Known implementations

- llama2; Kimi K3 (SiTU-GLU)
