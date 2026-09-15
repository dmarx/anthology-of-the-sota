---
number: 60
status: 'Active'
title: 'Initialize layer norms with smaller variance (0.02) for stability'
version: 2
history:
- version: 2
  date: '2026-09-13'
  note: >-
    The 1/sqrt(2N) factor this body names and did not cite is Child et al.
    (2019) §5.2, now carried in `introduced_by:` under ADR-029. The
    claim is unchanged and so is the confusion flagged below, which fixing
    would change what the practice asserts.
tags:
# Retagged from the report of unbound lineage. This is an initialization rule
# for stability, and `model-stability` names initialization in its blurb. It
# carried `distributed-optimization` because its source is a Megatron paper,
# which is where it was found rather than what it is about (ADR-026).
- model-stability
date: '2026-08-24'
source:
- LIT-043
# Megatron-LM is the evidence at scale; the factor itself is three years
# older and the body was naming it without a citation (ADR-029).
introduced_by:
- LIT-225
summary: >-
  Narayanan et al. (2021), [LIT-043](../literature.d/LIT-043.md) — [ARXIV-2104.04473](https://arxiv.org/abs/2104.04473).
compared_against:
- SOTA-051
---

<!-- inactive-ok-file: ADR-029 — Proposed. Every mention here names it as the decision that added `introduced_by:`, which is the field this document uses; the citation is to the reasoning, not a claim the decision is settled -->

# SOTA-060: Initialize layer norms with smaller variance (0.02) for stability

## Source

Narayanan et al. (2021), [LIT-043](../literature.d/LIT-043.md) — [ARXIV-2104.04473](https://arxiv.org/abs/2104.04473).

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

That factor has an author. Child et al. (2019), [LIT-225](../literature.d/LIT-225.md) §5.2, scales the
initialisation of the two residual-output projections by exactly `1/sqrt(2N)`,
and states the invariant it is protecting: **the ratio of input-embedding scale
to residual-block scale, held constant across values of `N`**. The `2` is the
two residual functions per block, which is why it is `2N` here and `N` in the
GPT-2 formulation this body reached for. Named in prose and cited nowhere until
[ADR-029](../decisions.d/ADR-029.md) gave the record a field for it.

## What the title gets wrong

It says "layer norms", and the initialisation that matters here is the
*output projections* of the attention and MLP blocks. LayerNorm's own
parameters are conventionally initialised to weight 1 and bias 0 — which is
what [SOTA-025](SOTA-025.md) and [SOTA-026](SOTA-026.md) say, and 0.02 is not that.

0.02 is also a familiar number for a different reason: it is the standard
deviation of the normal distribution GPT-2 and its descendants use to
initialise *all* weights, before the depth scaling is applied on top. Two
distinct conventions have been merged into one sentence.

Flagged rather than rewritten: fixing it means deciding which of the two the
practice is about, which changes what it claims.
