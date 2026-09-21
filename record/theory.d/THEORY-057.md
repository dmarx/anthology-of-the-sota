---
number: 57
status: Proposed
formerly:
- THEORY-tmp2lctc
promote_when: >-
  One corpus, two generators, one measurement: the same lexical or semantic
  seed distribution run through models of materially different capability or
  sampling temperature, with n-gram concentration measured on the outputs and
  the seed distribution's own concentration reported as the floor. That would
  separate "the model concentrates" from "the prompt distribution was narrow",
  which no source here does. What would NOT meet it: another corpus shown to
  be formulaic. That is the observation this is an account of, and the record
  already holds two.
title: 'A corpus a model generates is narrower than the distribution it imitates, and the narrowing shows up as n-gram over-concentration'
version: 1
tags:
- data-pipeline
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-205
- LIT-485
explains:
- SOTA-172
- SOTA-295
summary: >-
  Zhu et al. (2024), [LIT-205](../literature.d/LIT-205.md), and Finke et al. (2025),
  [LIT-485](../literature.d/LIT-485.md) — two groups, different corpora, no citation between them,
  both locating the damage in the same statistic. Generated text concentrates
  on the generator's high-probability continuations, so the corpus is narrower
  than what it imitates; **59.38%** of TinyStories contains "once upon a time",
  and the proportion of synthetic pretraining data correlates *negatively*
  with downstream performance.
---

<!-- inactive-ok-file: SOTA-172 SOTA-295 THEORY-051 SOTA-298 — all Proposed.
     The first two are declared `explains:` on this theory, so the citation is
     the relation itself. THEORY-051 and SOTA-298 are named in "A second
     narrowing, and why this document does not claim it is the same one",
     whose whole content is that the connection is NOT established — citing a
     document in order to say the record has not joined them to this one is
     the opposite of citing it as settled. -->

# THEORY-057: A corpus a model generates is narrower than the distribution it imitates, and the narrowing shows up as n-gram over-concentration

## Source

Zhu et al. (2024), [LIT-205](../literature.d/LIT-205.md), and Finke et al. (2025),
[LIT-485](../literature.d/LIT-485.md) — read as [NOTE-234](../notes.d/NOTE-234.md). Two groups, two
corpora, two instruments, no citation in either direction.

## What it explains

| practice | what it says to do | what this says is going on |
|---|---|---|
| [SOTA-172](../practices.d/SOTA-172.md) | build synthetic pretraining data by editing human text at the token level, not by generating from scratch | editing keeps the corpus anchored to a distribution that was never passed through a generator, so there is nothing to concentrate |
| [SOTA-295](../practices.d/SOTA-295.md) | parameterize the generating prompt above the word list, and constrain how each sample opens | if you must generate, the entropy has to be supplied from outside the model, because the model will not supply it itself |

The two practices disagree about the remedy and agree about the disease. That
agreement is what this document is for: it was stated in prose in
[SOTA-295](../practices.d/SOTA-295.md)'s conditions and had no page of its own.

## The account

Sampling from a model is sampling from a distribution the model learned, and
that distribution is not the distribution it was trained on. It is sharper.
Whatever the training data contained, the model puts more mass on the
continuations it is most confident about, and every sample is a draw from the
sharpened version. Generate a corpus this way and the corpus inherits the
sharpening; train on that corpus and the next model sharpens what was already
sharp.

**The statistic where this becomes visible is n-gram frequency**, and both
sources land on it independently.

[LIT-205](../literature.d/LIT-205.md) pretrains across varying proportions of synthetic data and
finds the proportion correlates **negatively** with performance, then
attributes it statistically to distributional shift and **over-concentration
of n-gram features**. The remedy follows from the diagnosis rather than from
intuition: edit human text at the token level, and the test error is bounded
above by construction because the result never leaves the neighbourhood of a
real distribution.

[LIT-485](../literature.d/LIT-485.md) measures a corpus rather than a model trained on one, and finds
the same concentration with a battery of instruments. **59.38%** of
TinyStories contains "once upon a time"; the next three 4-grams are 28.24%,
16.52% and 11.55%. Every sample contains one of the hundred commonest
part-of-speech sequences — a POS-template rate of **100**. Compression ratio
and Self-BLEU both say the same thing at `p < 0.001`.

**What makes the second source more than a repetition is what it rules out.**
TinyStories was not careless. It had already identified this failure and built
a mechanism against it: sample a lexicon per story so the prompt differs every
time. That mechanism was lexical, and lexical variation turns out to be the
wrong level — the openings stayed near-identical because the *shape* of the
request never changed. So the narrowing is not merely "the prompt was the
same". A prompt distribution designed to be diverse still produced a corpus
whose top 4-gram covers three fifths of it.

The trace reaches into a model trained on it: in a single-layer model trained
on TinyStories, `[bos, 'once']` is the strongest bigram outlier in the
weights.

## A second narrowing, and why this document does not claim it is the same one

The record holds another account of a text distribution narrowing.
[THEORY-051](THEORY-051.md) describes Change.org's AI drafting tool raising mean pairwise
similarity between petitions by **23%**, with the text features that had
predicted success ceasing to predict it. Same destination — a narrower
distribution of text — reached by a different route: there a human accepts,
edits and posts what a model suggested, where here the model emits the tokens
directly.

It is tempting to call these one phenomenon, and this record declines to, for
reasons it can state:

- **The metrics are not the same measurement.** N-gram over-concentration and
  mean pairwise embedding similarity move independently in general —
  paraphrase preserves one and destroys the other — and nobody has run both
  instruments on either corpus.
- **The human-in-the-loop path has a selection step this one lacks.** Writers
  accept, reject and rewrite. That could damp the narrowing or amplify it, and
  [LIT-487](../literature.d/LIT-487.md) cannot tell: its treatment is *access* to the tool, not use
  of it.
- **The harms are different in kind.** Here the damage is to a model trained
  on the corpus. There the damage is that a signal between people stopped
  carrying information. Two things with the same statistics need not have the
  same remedy.

What would settle it is a measurement, not a reading: run both instruments
across both boundaries — the AI-access boundary on Change.org and the
synthetic/human boundary in TinyStories and SimpleStories. If n-gram
concentration and embedding homogenization track each other, that is one
phenomenon with two metrics. If they dissociate, these are two things that
share a word. [#234](https://github.com/dmarx/anthology-of-the-sota/issues/234) is where that was argued out, and the conclusion was
to file the two accounts separately and point them at each other rather than
to assert a connection neither source claims. [DP-009](../../docs/design-principles.md#dp-9): two is not several,
and it is certainly not a mechanism.

## Why `Proposed`

**Neither source isolates the model's contribution.** A generated corpus is
narrow, and the narrowness has at least two possible owners: the model's
sharpened output distribution, and the prompt distribution that was fed to it.
[LIT-485](../literature.d/LIT-485.md) rules out the *lexical* part of the second by construction —
TinyStories varied the lexicon and stayed formulaic — but nothing measures the
concentration of the seed distribution itself as a floor. Until somebody runs
one seed distribution through two generators, "the model concentrates" is the
plausible reading rather than the measured one.

**The mechanism is stated rather than derived, in both.** [LIT-205](../literature.d/LIT-205.md)
attributes the effect to n-gram over-concentration by statistical analysis of
outcomes; it does not show the sharpening step happening. [LIT-485](../literature.d/LIT-485.md)
measures the result and does not model its cause at all.

**Two corpora, both narrow, both English, both short-form.** TinyStories is a
deliberately restricted distribution of children's stories. Whether the same
concentration appears in generated code, generated mathematics, or generated
long-form text is untested here — and generated mathematics is exactly where
the field currently generates most heavily.

## What it does not say

**It does not say generated data is useless.** [SOTA-295](../practices.d/SOTA-295.md) exists because
a generated corpus with the entropy supplied from outside is a good corpus,
and it beats its predecessor on every diversity instrument with **no
significant difference in judged simplicity**. The claim is about where the
entropy has to come from, not about whether generation works.

**It does not say the two remedies are in competition.** They apply to
different jobs — [SOTA-172](../practices.d/SOTA-172.md) where the goal is a pretraining corpus standing
in for real text, [SOTA-295](../practices.d/SOTA-295.md) where generating from scratch is the point.
Reading either as general advice about synthetic data gets both wrong.

**It does not predict a rate.** Nothing here says how much narrowing per
generation, or after how many rounds it matters. The negative correlation in
[LIT-205](../literature.d/LIT-205.md) is measured at that paper's scale, and the recipes in this record
that rephrase at frontier scale are not covered by it.
