---
status: Proposed
promote_when: >-
  The same swap run on a second corpus, or run in the direction this paper
  did not: a tokenizer fitted to the *baseline* corpus, which would say
  whether the gain is "fit the tokenizer to the corpus" or "this corpus
  tokenizes better". The authors name that arm themselves as the one they
  left out. What would not move it: another small-model report shipping a
  custom tokenizer, which is common and is not a controlled swap.
consensus: unreplicated
consensus_note: >-
  One group, one corpus, one swap — and the swap is clean, which is more
  than most of the neighbouring claims can say. Reduced vocabularies are
  widespread in small-model work (TinyStories itself truncated GPT-Neo's to
  10K) and the size of the effect when it is isolated has essentially not
  been reported.
title: 'Fit the tokenizer to the corpus when the corpus is deliberately narrow'
version: 1
tags:
- representation-and-encoding
- tiny-models
date: '2026-09-21'
source:
- LIT-tmpvjesi
introduced_by:
- LIT-tmpvjesi
implementations: []
summary: >-
  Finke et al. (2025), [LIT-tmpvjesi](../literature.d/LIT-tmpvjesi.md) — holding the dataset and the
  architecture fixed and changing only the tokenizer, a **4,096**-token
  WordPiece vocabulary seeded with English affixes beats GPT-2's **50,257**
  by **+26.7 coherence** and **+27.5 quality**. It is the one fully
  controlled comparison in a paper that is mostly about something else, and
  the effect is larger than the architecture change measured beside it.
---

# SOTA-tmpu9u55: Fit the tokenizer to the corpus when the corpus is deliberately narrow

## Source

Finke et al. (2025), [LIT-tmpvjesi](../literature.d/LIT-tmpvjesi.md) — [ARXIV-2504.09184](https://arxiv.org/abs/2504.09184) §3.5, read as
[NOTE-tmppb47z](../notes.d/NOTE-tmppb47z.md).

## What to do

When the training corpus is a restricted distribution on purpose — a model
organism, an interpretability corpus, a specialized domain — do not inherit a
general-purpose tokenizer. Build one over the corpus, and build it small:

- **A vocabulary sized to the corpus, not to the web.** 4,096 tokens against
  GPT-2's 50,257, a factor of twelve.
- **Seeded with the corpus's morphology.** The initial alphabet includes
  common English affixes recovered by analysing the corpus — prefixes like
  `un`, `re`, suffixes like `ed`, `ing`, `ly` — so that inflection is
  compositional rather than a separate entry per form.

## What it buys

Dataset held fixed, architecture held fixed, tokenizer varied: **+26.7
coherence** and **+27.5 quality** on a 0–100 judged scale, with originality
and grammar also up.

Two comparisons in the same figure say how large that is. Re-architecting the
baseline to Llama style, with its tokenizer left alone, improves it — and
leaves it behind the custom-tokenizer model on every metric. And the
vocabulary is most of the reason the model is small at all: the same
architecture with GPT-2's tokenizer is a 65M-parameter model, and with the
4,096-token one it is 35M. At this scale the embedding table is the model.

## Why this is about narrow corpora specifically

The argument is not that small vocabularies are better. It is that a
tokenizer is fitted to a distribution, and a general-purpose tokenizer is
fitted to the web. Point it at a corpus that uses a few thousand words and
most of its vocabulary is dead weight that you nonetheless pay for in
embedding parameters — parameters which, at these sizes, are more than half
the model.

That is also the boundary. Nothing here says anything about a model trained
on a broad corpus, where the general-purpose tokenizer is fitted to the right
distribution and [SOTA-007](SOTA-007.md) is the incumbent for good reasons.

## Conditions

**The swap is clean and the conclusion drawn from it is one step wider than
the swap.** What was varied is the tokenizer on *this* corpus. Whether the
gain is "fit the tokenizer to your corpus" or "this corpus happens to
tokenize well under a small vocabulary" is undetermined, because no custom
tokenizer was fitted to the baseline corpus. The authors state this as their
own limitation and name it as the missing arm.

**Two changes inside one swap.** The vocabulary shrank *and* it gained
morphological seeding, and these are separable interventions that were not
separated. The affix seeding is the more interesting half and is the less
evidenced one.

**No comparison against a like-for-like BPE.** The authors note they did not
train a BPE tokenizer at the same vocabulary size, so WordPiece-versus-BPE is
untested here and the result should not be read as favouring either
algorithm.

**Judged, not perplexity-matched.** The metric is a judge model scoring
generations. A smaller vocabulary changes what perplexity even means, so a
judged comparison is arguably the right call — and it is still a judge.

**One corpus, one architecture family, one language.**

## Known implementations

- The SimpleStories model suite, 1.25M–35M parameters, with the tokenizer and
  training code published
