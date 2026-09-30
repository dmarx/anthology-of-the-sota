---
number: 295
status: Proposed
formerly:
- SOTA-tmpvc466
promote_when: >-
  A second group measuring corpus-level diversity before and after moving the
  constraint above the lexical level, on a synthetic corpus that is not a
  children's-story corpus — or an ablation separating the opening constraint
  from the prompt parameterization, which arrive together here and are not
  the same intervention. What would not move it: another synthetic dataset
  that happens to use structured prompts and reports downstream scores.
  Structured prompting is common; the content here is the measurement that
  lexical sampling alone does not work, and downstream scores do not isolate
  the generation procedure.
consensus: unreplicated
consensus_note: >-
  One group, one corpus pair, one language of the two it generated. The
  measurement is unusually thorough for a claim of this size — five
  diversity instruments agreeing — and it is still a comparison between one
  procedure and one alternative.
title: 'Parameterize the generating prompt above the word list, and constrain how each sample opens'
version: 1
tags:
- data-pipeline
- tiny-models
date: '2026-09-21'
source:
- LIT-485
introduced_by:
- LIT-485
implementations:
- 'SimpleStories'
summary: >-
  Finke et al. (2025), [LIT-485](../literature.d/LIT-485.md) — requiring a story to contain three
  words drawn from a vocabulary constrains the lexicon and leaves the frame
  alone, and the frame is where a generator repeats itself: **59.38%** of
  TinyStories begins "once upon a time". Name a theme, a topic, a style and a
  narrative feature per sample, and require the sample to open with a given
  part of speech and letter. Five diversity metrics move; measured simplicity
  does not.
explained_by:
- THEORY-057
---

<!-- inactive-ok-file: SOTA-172 — Proposed, and the whole Conditions passage
     citing it is about where the two practices apply and where they agree.
     Its unsettled status is load-bearing in the right direction: this
     practice does not rest on it, it is bounded against it, and the boundary
     is drawn from the measurement `SOTA-172` reports rather than from its
     standing -->

# SOTA-295: Parameterize the generating prompt above the word list, and constrain how each sample opens

## Source

Finke et al. (2025), [LIT-485](../literature.d/LIT-485.md) — [ARXIV-2504.09184](https://arxiv.org/abs/2504.09184) — read as
[NOTE-234](../notes.d/NOTE-234.md).

The procedure it replaces is [LIT-484](../literature.d/LIT-484.md)'s, which is the reason this
is a practice and not an observation: TinyStories was not careless about
diversity. It identified the problem — a commercial model prompted for
stories repeats itself however high the temperature — and built a mechanism
against it. The mechanism was lexical, and this is the measurement of how far
that got.

## What to do

**Parameterize above the lexicon.** Draw, per sample, from lists that name
what the sample is *about* and how it is *told*: a theme, a topic, a writing
style, a narrative feature, and on some fraction of samples a grammar feature
and an author persona. SimpleStories uses 63, 48, 23, 26, 31 and 23 options
respectively, with the grammar feature on half the samples and the persona on
a third.

**Constrain the opening separately.** Require each sample to begin with a
given part of speech and a given initial letter, with letter frequencies
drawn from a reference corpus. This is a small, local constraint and it
targets the specific failure: the repetition the diagnosis found was
**near-identical first sentences**, and an opening constraint disambiguates
the generation from the first token onwards.

**Then you can sample sharply.** The authors run nucleus sampling at
temperature 1 and argue it is safe *because* the parameterization is supplying
the entropy temperature would otherwise have to — so constraint adherence
improves and diversity does not suffer for it.

**Keep the parameters.** They were chosen rather than inferred, so every
sample arrives labelled at no extra cost, and a judge model can recover the
labels above chance.

## What it buys

Against the lexical-sampling procedure, on the corpus itself rather than on
anything trained from it:

- **Top 4-gram frequency 59.38% → 7.49%.** The next three in TinyStories are
  28.24%, 16.52% and 11.55%; SimpleStories has nothing above 5%.
- Lower compression ratio and lower Self-BLEU self-homogenization, both at
  p < 0.001.
- Higher n-gram diversity score for n = 1…10, the gap widening with n.
- POS-template rate **88.9 against 100** — every TinyStories sample contains
  one of the hundred commonest part-of-speech sequences — and
  template-per-token 0.016 against 0.026.
- Judged content and style diversity much higher, with **no significant
  difference in judged simplicity**. That null is the load-bearing one: the
  whole difficulty is that diversity and simplicity trade against each other,
  and the claim is only interesting if simplicity held.

The artefacts are also measurable downstream in a literal sense: in a
single-layer model trained on TinyStories, `[bos, 'once']` is the strongest
bigram outlier in the weights.

## Conditions

**This is for corpora generated from scratch, and that is a narrower case
than it sounds.** [SOTA-172](SOTA-172.md) argues that synthetic pretraining data should be
made by editing human text rather than generated from a prompt at all, on
evidence that the proportion of generated data correlates *negatively* with
performance. The two are not in conflict and neither refutes the other: this
practice applies where generating from scratch is the point — model
organisms, interpretability corpora, deliberately restricted distributions —
and `SOTA-172` applies where the goal is a pretraining corpus that stands in
for real text. Reading either as general advice about synthetic data gets
both wrong.

**They agree about the disease.** `SOTA-172`'s mechanism for why generated
corpora hurt is *over-concentration of n-gram features*, and the measurement
here is n-gram over-concentration in a generated corpus, arrived at
independently and on a different corpus. What they disagree about is the
remedy. That agreement is worth more than it looks, because it is the same
finding from two directions.

**The two interventions arrive together.** Prompt parameterization and the
opening constraint are never ablated apart, and the opening constraint is far
the cheaper of the two. Nobody knows how much of the gain it carries alone.

**Four years of generator sit inside the comparison.** GPT-4o-mini here
against GPT-3.5 and GPT-4 there, uncontrolled. Some of the improvement is
plausibly a better instruction-follower rather than a better prompt.

**Diversity metrics are the claim, and they are proxies.** Five of them
agree, which is the right way to handle that, and the authors still recommend
reading random samples by hand. The one thing measured about a *model* rather
than the data — that a model trained on the more diverse corpus is better —
is confounded three ways in this paper and is not what this practice rests on.

**One language of the two.** The Japanese half of the dataset is unevaluated,
for the stated reason that no fair comparison exists.

## Known implementations

- SimpleStories — 2M samples per language in English and Japanese, with the
  generation code and parameter lists published
