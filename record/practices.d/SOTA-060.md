---
number: 60
status: 'Active'
title: 'Initialize weights from N(0, 0.02) and scale the residual-output projections by 1/sqrt(2N)'
version: 4
history:
- version: 2
  date: '2026-09-13'
  note: >-
    The 1/sqrt(2N) factor this body names and did not cite is Child et al.
    (2019) §5.2, now carried in `introduced_by:` under ADR-029. The
    claim is unchanged and so is the confusion flagged below, which fixing
    would change what the practice asserts.
- version: 3
  date: '2026-10-01'
  note: >-
    Re-sourced from LIT-043, which says nothing about initialization, to the
    Megatron-LM paper that states the recipe (LIT-022). `introduced_by:`
    moved from Child et al. to GPT-2, which stated the depth scaling two
    months earlier. The claim, and the confusion flagged below, are
    unchanged.
- version: 4
  date: '2026-10-01'
  note: >-
    Retitled, resolving the confusion versions 2 and 3 flagged. The title
    said "layer norms with smaller variance (0.02)", merging two conventions
    and naming neither: LayerNorm's own parameters start at 1 and 0. The new
    source settles which the practice is about, because Megatron-LM states
    both as one recipe: every weight from N(0, 0.02), then the weights
    immediately before each residual scaled by 1/sqrt(2N). That recipe is
    now the title.
tags:
# Retagged from the report of unbound lineage. This is an initialization rule
# for stability, and `model-stability` names initialization in its blurb. It
# carried `distributed-optimization` because its source is a Megatron paper,
# which is where it was found rather than what it is about (ADR-026).
- model-stability
date: '2026-08-24'
# Was LIT-043 (Narayanan et al. 2021), which says nothing about
# initialization. The Megatron-LM paper that states this recipe is Shoeybi et
# al. (2019), LIT-022: N(0, 0.02) with 1/sqrt(2N) on the weights before each
# residual. It reports the recipe, not an ablation of it.
source:
- LIT-022
# Was LIT-225 (Child et al., April 2019). GPT-2 stated the same depth scaling
# two months earlier, as 1/sqrt(N) over N residual layers, in a model it
# says largely follows GPT, whose base initialization is N(0, 0.02)
# (ADR-029).
introduced_by:
- LIT-733
summary: >-
  Shoeybi et al. (2019), [LIT-022](../literature.d/LIT-022.md) — [ARXIV-1909.08053](https://arxiv.org/abs/1909.08053).
compared_against:
- SOTA-051
explained_by:
- THEORY-011
---

<!-- inactive-ok-file: ADR-029 — Proposed. Every mention here names it as the decision that added `introduced_by:`, which is the field this document uses; the citation is to the reasoning, not a claim the decision is settled -->

# SOTA-060: Initialize weights from N(0, 0.02) and scale the residual-output projections by 1/sqrt(2N)

## Source

Shoeybi et al. (2019), [LIT-022](../literature.d/LIT-022.md) — [ARXIV-1909.08053](https://arxiv.org/abs/1909.08053).

Megatron-LM, [LIT-022](../literature.d/LIT-022.md), states the recipe in exactly this form: weights drawn
from `N(0, 0.02)`, then the weights immediately before each residual scaled
by `1/sqrt(2N)`, `N` the number of transformer layers — and trains GPT-2-style
models to 8.3B parameters with it. That is a report of what was used, not a
measurement of what it buys; the paper runs no arm without it. Narayanan et
al. ([LIT-043](../literature.d/LIT-043.md)), cited here before, says nothing about initialization.

## What the smaller variance is protecting against

The residual stream accumulates the output of every layer, so its variance
grows with depth unless something holds it down. Initialising the output
projection of each block with a smaller standard deviation — scaled down by
the number of layers — keeps each block's contribution small relative to what
is already in the stream, so the signal at the top of a deep model is not
dominated by initialisation noise.

That is the same reasoning that puts a 1/√(2·n_layers) factor on the output
projections in GPT-2-style initialisations, and the same problem ReZero
([SOTA-051](SOTA-051.md)) attacks by starting the residual branch at literally zero.

That factor has an author, and it is GPT-2. Radford et al. (2019),
[LIT-733](../literature.d/LIT-733.md) §2.3, uses "a modified initialization which accounts for the
accumulation on the residual path with model depth", scaling the weights of
residual layers by `1/sqrt(N)` with `N` the number of residual layers — the
same quantity as `2·n_layers`, two residual layers per block. Child et al.
(2019), [LIT-225](../literature.d/LIT-225.md) §5.2, two months later, writes it as `1/sqrt(2N)` over
blocks and states the invariant it is protecting: **the ratio of
input-embedding scale to residual-block scale, held constant across values of
`N`**. Child's base initialisation is not 0.02. GPT-2 says it "largely
follows" GPT, whose report initialises every weight from `N(0, 0.02)`, and
Megatron-LM writes the two down together. Named in prose and cited nowhere
until [ADR-029](../decisions.d/ADR-029.md) gave the record a field for it, and attributed to Child until
the earlier report was checked.

## What the title used to get wrong

Until version 4 it said "layer norms with smaller variance (0.02)", and the
initialisation that matters here is the
*output projections* of the attention and MLP blocks. LayerNorm's own
parameters are conventionally initialised to weight 1 and bias 0 — which is
what [SOTA-025](SOTA-025.md) and [SOTA-026](SOTA-026.md) say, and 0.02 is not that.

0.02 is also a familiar number for a different reason: it is the standard
deviation of the normal distribution GPT-2 and its descendants use to
initialise *all* weights, before the depth scaling is applied on top. Two
distinct conventions have been merged into one sentence.

This was flagged rather than rewritten for two versions, because fixing it
meant deciding which of the two the practice is about. Megatron-LM
([LIT-022](../literature.d/LIT-022.md)) decides it: it states both together, as one recipe, so the title
now names both. Neither it nor GPT-2 ablates the recipe. The evidence for it
is that it is the setup large runs report using, not a measurement that it
beats an alternative.
