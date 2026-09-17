---
status: Proposed
promote_when: >-
  An independent group adding multi-token vocabulary this way on a model
  family other than Llama and reporting both halves — that the frozen model
  actually emits the new tokens, and that accuracy on existing tokens is
  unchanged — or a serving report that measures the end-to-end latency and
  throughput the shorter sequences are supposed to buy. What would NOT satisfy
  this: another paper showing a model has detokenized internal
  representations, which is the finding this method is built on rather than
  evidence that the method works; or an accuracy-preserved result with no
  measurement of whether the new tokens get used.
consensus: unreplicated
consensus_note: >-
  One group, one paper, one model. The technique it is measured against —
  mean-embedding initialization — degrades the model, so the comparison is
  against a baseline rather than against a field position. Nobody has
  disagreed because nobody has tried it.
title: "Add a multi-token word to a frozen model's vocabulary from the model's own detokenized representation of it"
version: 1
tags:
- representation-and-encoding
date: '2026-09-17'
source:
- LIT-tmp8gq9j
introduced_by:
- LIT-tmp8gq9j
implementations: []
summary: >-
  Kaplan et al. (2024), [LIT-tmp8gq9j](../literature.d/LIT-tmp8gq9j.md) — a model already computes a whole-word
  representation for a word its tokenizer splits, so initialize the new
  embedding and unembedding from *that* rather than from an average of the
  word's token embeddings. On Llama2-7B the frozen model then uses the new
  tokens while keeping its accuracy on existing ones (0.519 against 0.522 on
  WikiText-103), where mean-embedding initialization both fails to use them
  and degrades the model. The gain is largest where the tokenizer is worst:
  Arabic Wiki40B, 0.402 new-token accuracy against 0.117.
explained_by:
- THEORY-tmpkh59b
---

# SOTA-tmp5b7vv: Add a multi-token word to a frozen model's vocabulary from the model's own detokenized representation of it

## Source

Kaplan et al. (2024), [LIT-tmp8gq9j](../literature.d/LIT-tmp8gq9j.md) —
[ARXIV-2410.05864](https://arxiv.org/abs/2410.05864), ICLR 2025.

The reason it works is [THEORY-tmpkh59b](../theory.d/THEORY-tmpkh59b.md): the
model has already built a single representation for the word, so the thing you
need to put in the embedding matrix exists inside the network and can be read
out rather than guessed at.

## The procedure

1. **Extract.** Pass the word in, apply PATCHSCOPES to the last token's hidden
   states at every layer, and take the representation at the **earliest layer
   that decodes to the full word**. If no layer decodes it, the word is not in
   the model's inner lexicon — **do not add it**. That test is part of the
   method, not a caveat.
2. **Project.** Fit orthogonal-Procrustes maps from that layer into the
   embedding and unembedding spaces, using **only the existing in-vocabulary
   tokens**, so the projection does not depend on which words you are adding.
3. **Refine.** Two `d×d` matrices, trained on 20M tokens with every other
   parameter frozen.

## What it costs, which the phrase "finetuning-free" understates

The core parameters are frozen and **step 3 is still training** — 20M tokens
of continued pretraining for the refinement matrices. That is cheap against
retraining a tokenizer and it is not free, and the distinction matters when
the alternative being considered is doing nothing.

## What was measured

Llama2-7B, token-level top-1 accuracy, against the unmodified model and
against mean-embedding initialization:

| | new tokens used | all tokens (orig. → ours) |
|---|--:|--:|
| WikiText-103 | 0.171 vs 0.071 baseline | 0.522 → 0.519 |
| PubMed | 0.180 vs 0.123 | 0.517 → 0.511 |
| Wiki40B Arabic | **0.402 vs 0.117** | 0.535 → 0.532 |

Two things at once, and both are needed: the frozen model **uses** the new
entries, and it does not get worse on the old ones. Mean-embedding
initialization fails both — it struggles to use the new tokens and degrades
overall performance, badly on Arabic (0.211).

**Where to expect it to pay.** The motivation is that multilingual tokenizers
produce sequences up to 13× longer for non-English text, and the Arabic result
is where the method is most clearly worth it. On English the accuracy is
preserved rather than improved, so what you are buying is shorter sequences,
not better predictions.

## What this does not claim

**The speed benefit is argued, not measured here.** Shorter sequences mean
fewer inference iterations, and the paper motivates the work that way, but
what it reports is accuracy. No end-to-end latency or throughput number
appears in the results above, which is why `promote_when` asks for one.

**Perplexity is not the metric and cannot be.** Expanding the vocabulary
changes what perplexity is computed over, so the paper uses token-level
accuracy instead. Comparisons against perplexity-reported baselines elsewhere
are not like-for-like.

**One model.** Llama2-7B. The `Proposed` status is about that and about the
missing serving measurement, not about doubt over the mechanism, which
[THEORY-tmpkh59b](../theory.d/THEORY-tmpkh59b.md) holds `Active` on three
independent lines of evidence.

## Known implementations

- None known outside the paper.
