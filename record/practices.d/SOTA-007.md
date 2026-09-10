---
number: 7
status: 'Active'
title: 'BPE tokenization for open vocabulary tasks'
version: 1
tags:
- representation-and-encoding
date: '2026-08-24'
source:
- LIT-003
summary: >-
  Sennrich et al. (2015), [LIT-003](../literature.d/LIT-003.md) — [ARXIV-1508.07909](https://arxiv.org/abs/1508.07909).
implementations:
- llama2
---

# SOTA-007: BPE tokenization for open vocabulary tasks

## Source

Sennrich et al. (2015), [LIT-003](../literature.d/LIT-003.md) — [ARXIV-1508.07909](https://arxiv.org/abs/1508.07909).

## Known implementations

- llama2

## The problem it solved

A word-level vocabulary has to be closed, so anything outside it becomes an
unknown token and the model can neither read nor produce it — names, numbers,
morphology, code, any language with productive compounding. A character-level
vocabulary is open and pays for it in sequence length.

BPE takes the middle: start from characters, repeatedly merge the most
frequent adjacent pair, stop at a chosen vocabulary size. Frequent words end
up as single tokens, rare ones decompose into pieces, and **nothing is ever
out of vocabulary** because the character level is always available underneath.
That property — open vocabulary at a bounded size — is why every model in this
record tokenises this way.

## What the choice costs, which the title does not say

The vocabulary size is a real trade and it is set once, before training.
Larger means shorter sequences and so cheaper attention, and a larger
embedding and output layer whose cost is paid on every token. Smaller means
the reverse, plus worse handling of anything the merges did not reach.

The merges are also fit to a corpus, so a tokeniser trained on one
distribution is systematically inefficient on another — a language, a
programming language or a domain under-represented at fitting time spends
more tokens per unit of meaning, permanently, and no amount of later training
recovers it.

That last point is the reason this is worth a body rather than a line. The
tokeniser is one of the few decisions that cannot be revised without
retraining, and its failure mode is a quiet tax rather than an error.
