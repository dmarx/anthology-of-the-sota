---
status: 'Active'
title: 'use RoPE for LLM (1D sequence) positional embeddings'
version: 3
history:
- version: 2
  date: '2026-09-07'
  note: >-
    Gained the two sections a one-line stub was missing: where the line goes
    (SOTA-151 rescales what this recommends) and what it does not cover. The
    recommendation is unchanged for a dense transformer; the addition is that
    a linear-attention hybrid may be better off with no positional encoding
    at all (LIT-207, LIT-133, LIT-131).
- version: 3
  date: '2026-09-07'
  note: >-
    The alternative now has a practice of its own (SOTA-153) and a
    correction. Version 2 said RoPE-or-not was not a parameter an existing
    model can be re-tuned on and left reversibility open; LIT-209
    answers it — conversion by continued pretraining, at parity on short
    benchmarks.
tags:
- model-architecture
date: '2026-08-24'
published: '2021-04-01'
source:
- LIT-045
summary: >-
  Su et al. (2021), [LIT-045](../literature.d/LIT-045.md) — [ARXIV-2104.09864](https://arxiv.org/abs/2104.09864).
compared_against:
- SOTA-153
corrected_by:
- SOTA-151
---

# SOTA-063: use RoPE for LLM (1D sequence) positional embeddings

## Source

Su et al. (2021), [LIT-045](../literature.d/LIT-045.md) — [ARXIV-2104.09864](https://arxiv.org/abs/2104.09864).

## Where the line goes from here

This is the head of a line rather than a standing answer on its own. A model
that uses RoPE and later needs a longer window than it was trained on takes
[SOTA-151](SOTA-151.md), which rescales the position indices instead of fine-tuning at the
longer length — the succession runs [LIT-045](../literature.d/LIT-045.md) → [LIT-192](../literature.d/LIT-192.md) → [LIT-193](../literature.d/LIT-193.md).

## The alternative

The recommendation is not uncontested, and the objection is not that rotation
is the wrong function. [LIT-207](../literature.d/LIT-207.md) trained five positional schemes from
scratch under identical hyperparameters and found rotary among the schemes
that do *not* generalize to unseen lengths, with the best result coming from
using no positional encoding at all — a decoder-only transformer can
represent both absolute and relative position without being told which to
use. Frontier practice has since split: Kimi Linear ([LIT-133](../literature.d/LIT-133.md)) and Kimi K3
([LIT-131](../literature.d/LIT-131.md)) drop positional encoding from their global-attention layers
entirely and let an interleaved recurrence carry position, which is what
lets K3 reach 1M tokens with no RoPE modification at all.

The alternative is filed as [SOTA-153](SOTA-153.md), and it is not marked as
contesting this one, because the two are not rival settings of one knob:
RoPE-or-not is an architectural choice, made before training and reversible
afterwards only at the cost of continued pretraining ([LIT-209](../literature.d/LIT-209.md) converted
an 8B model that way, at parity on short benchmarks). What a reader should
take from it: RoPE remains right for a dense transformer, and is not
automatically right for a hybrid whose cheap layers can carry position
themselves.
