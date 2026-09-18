---
status: Active
title: 'From Tokens to Words: On the Inner Lexicon of LLMs'
version: 1
tags:
- representation-and-encoding
date: '2026-09-17'
published: '2024-10-01'
arxiv: '2410.05864'
first_author: 'Kaplan'
keywords:
- 'detokenization'
- 'inner-lexicon'
- 'vocabulary-expansion'
- 'subword-tokenization'
- 'interpretability'
implementations: []
summary: >-
  Kaplan et al. (2024), [ARXIV-2410.05864](https://arxiv.org/abs/2410.05864), ICLR 2025. LLMs recombine sub-word
  sequences into whole-word representations at the word's last token, mostly
  in early and middle layers, and the effect is robust to arbitrary splits,
  typos and words the tokenizer never had. The control is what makes it: a
  probe on the last token reaches 89% word-vs-nonword accuracy, the same probe
  on the penultimate token only 61%, so it is the completed word rather than
  token co-occurrence. Turned into a vocabulary-expansion method whose core
  parameters stay frozen.
---

# LIT-tmp8gq9j: From Tokens to Words: On the Inner Lexicon of LLMs

Kaplan et al. (2024) — [ARXIV-2410.05864](https://arxiv.org/abs/2410.05864), ICLR 2025

## Key takeaways

- **The claim.** Models perform an intrinsic *detokenization*: sub-word
  sequences are combined into coherent whole-word representations at the
  word's last token. So a model maintains a latent vocabulary beyond its
  tokenizer's.

- **The probe, and its three-stage shape.** 10,000 words from the Gutenberg
  corpus against nonwords built by shuffling tokens *while preserving
  positional roles* — `ing` extracted from word-final position stays
  word-final — so the nonwords match the real words' positional statistics.
  A k-NN classifier on Llama2-7B last-token hidden states is at chance in the
  first layers, separates from **layers 2-6**, is near-completely separated
  through **layers 6-20**, peaks at **89% at layer 13**, and falls off after
  layer 20.

- **The control is the reason to believe it.** The obvious deflation is that
  the probe detects frequent token sequences rather than words. Repeating it
  on the **penultimate** token of three-token-or-longer words — which
  co-occurs with the same prefixes just as often — reaches only **61%**. The
  signal is tied to the presence of a complete word, not to co-occurrence.

- **Robust to things a lookup table would not survive**: arbitrary splits
  (`cats` → `ca` + `ts`), typos, and out-of-vocabulary words. Feeding the last
  token's internal representation back in as input, the model "understands" it
  as the complete word despite never having seen such a representation as
  input during training.

- **The application, and its actual shape.** Three steps: extract the
  detokenized representation with PATCHSCOPES at the earliest layer that
  decodes to the full word; learn orthogonal-Procrustes maps from that layer
  into the embedding and unembedding spaces, fitted only on existing
  in-vocabulary tokens; then refine with two `d×d` matrices trained on **20M
  tokens with every other parameter frozen**. A word that never decodes at any
  layer is taken not to be in the inner lexicon and is not added.

- **What the expansion actually bought.** Llama2-7B, token-level top-1
  accuracy. On WikiText-103 overall accuracy is preserved — 0.519 against the
  original model's 0.522 — where the mean-embedding baseline degrades to
  0.473. The strongest case is **Arabic Wiki40B**: new-token accuracy 0.402
  against the baseline's 0.117, with overall accuracy 0.532 against 0.535.
  The motivation given is that multilingual tokenizers produce sequences up to
  13× longer for non-English text.

## Standing in the anthology

Filed to close a gap the record had named twice and could not fill. This is
the mechanism half of the question
[THEORY-tmprceog](../theory.d/THEORY-tmprceog.md) left open, and the paper
[LIT-tmpyn738](LIT-tmpyn738.md) imports its stage-1 reassembly claim from.

The paper's own framing is "finetuning-free", and the record's version of that
should be exact: **the core parameters are frozen, and two refinement matrices
are trained on 20M tokens.** That is much cheaper than retraining and it is
not nothing, which matters for the practice filed from it.
