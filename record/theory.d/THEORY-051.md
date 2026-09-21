---
number: 51
status: Proposed
formerly:
- THEORY-tmp8vfb1
promote_when: >-
  The inversion measured as the mechanism rather than inferred alongside it —
  the predictive validity of a feature tracked against that feature's
  dispersion in the population, so that the loss of signal is shown to follow
  the loss of variance rather than merely to co-occur with it. A second
  platform showing feature shift and outcome null together would not settle
  it: that is the observation this account is one explanation of, and reader
  suspicion and diminished author effort are the other two, both of which
  predict the same null.
title: 'A text feature predicts success partly by being uncommon, so a tool that gives it to everyone destroys its predictive value'
version: 2
history:
- version: 2
  date: '2026-09-21'
  note: >-
    No change to the account. Adds a section pointing at THEORY-tmp2lctc,
    which describes a text distribution narrowing by a different route — a
    model generating the tokens rather than a person accepting them — and
    says why the record has not joined the two. #234 asked whether they are
    one phenomenon; the answer filed is that nobody has measured it, and the
    two documents name each other so the next reader does not have to
    rediscover the question.
tags:
- deployment-and-society
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-487
explains:
- SOTA-298
summary: >-
  Corpus et al. (2025), [LIT-487](../literature.d/LIT-487.md) — length, readability and lexical
  variety predicted petition success, an AI drafting tool moved all three in
  the successful direction and raised rated quality, and success did not
  follow. Inter-petition similarity rose **23%** in the same window, and the
  features' predictive strength weakened or reversed.
---

<!-- inactive-ok-file: SOTA-298 — Proposed, filed in this same
     contribution; this theory declares `explains:` on it, so the citation is
     the relation itself -->

<!-- inactive-ok-file: THEORY-tmp2lctc — Proposed, filed in the same
     contribution as this v2. It is named in "A second narrowing", whose
     entire content is that the record has NOT joined the two accounts;
     citing a document in order to say the connection is unmeasured is the
     opposite of citing it as settled. -->

# THEORY-051: A text feature predicts success partly by being uncommon, so a tool that gives it to everyone destroys its predictive value

## Source

Corpus et al. (2025), [LIT-487](../literature.d/LIT-487.md) — read as [NOTE-236](../notes.d/NOTE-236.md).

## What it explains

| practice | what it says to do | what this says is going on |
|---|---|---|
| [SOTA-298](../practices.d/SOTA-298.md) | measure a writing assistant by the outcome, not by the text features that used to predict it | the features are not a cheaper measurement of the same thing; their correlation with the outcome was partly a fact about the population, and the tool changes the population |

## The account

A measured association between a text feature and an outcome has two possible
readings, and before an intervention they are indistinguishable.

The first is that the feature **causes** the outcome: longer, clearer, more
varied petitions persuade more readers, and if every petition became longer
and clearer, every petition would do better.

The second is that the feature **distinguishes**: in a population where most
petitions are short and plain, writing a long careful one marks you as the
kind of author who will also do the other things that make a petition
succeed — recruit signatories, contact local press, post it in the right
community. On this reading the feature is a signal, its value depends on its
scarcity, and handing it to everyone is not an improvement but an erasure of
information.

**Change.org ran the experiment.** The tool moved all three features
decisively toward the successful profile, independent raters confirmed the
text genuinely improved on quality and persuasiveness, and the outcomes did
not improve. Then the diagnostic: the predictive strength of those same
features on outcomes **weakened or reversed**. A causal feature does not stop
predicting when more people have it. A distinguishing one does.

**The visible trace is homogenization.** Mean pairwise similarity between
petitions rose 23% in the same window. That is what the loss of a
distinguishing feature looks like from outside: the distribution narrows, and
a narrow distribution cannot separate anything.

## A second narrowing, and why this document does not claim it is the same one

The record holds another account of a text distribution narrowing.
[THEORY-tmp2lctc](THEORY-tmp2lctc.md) describes corpora a model generates directly:
**59.38%** of TinyStories contains "once upon a time", and the proportion of
synthetic pretraining data correlates negatively with what gets trained on it.
Same destination — a narrower distribution of text — reached by a different
route. There the model emits the tokens; here a person accepts, edits and
posts what it suggested.

The two are not joined in this record, and the reasons are worth carrying
rather than settling:

- **The metrics are not the same measurement.** That account is built on
  n-gram over-concentration; this one on mean pairwise embedding similarity.
  The two move independently in general — paraphrase preserves one and
  destroys the other — and nobody has run both instruments on either corpus.
- **This path has a selection step the other lacks.** Writers accept, reject
  and rewrite, which could damp the narrowing or amplify it. [LIT-487](../literature.d/LIT-487.md)
  cannot distinguish them: its treatment is *access* to the tool, not use of
  it.
- **The harms differ in kind.** There the damage is to a model trained on the
  corpus. Here it is that a signal between people stopped carrying
  information — and this document's account of *why* that happens, scarcity,
  has no counterpart in the generated-corpus case at all. A pretraining
  corpus is not competing with itself for a rivalrous outcome.

That last point is the strongest reason to keep them apart. The two could
share a statistical signature entirely and still have different causes, and
the narrowing here is offered as the *visible trace* of the mechanism rather
than as the mechanism.

[#234](https://github.com/dmarx/anthology-of-the-sota/issues/234) is where this was argued out. The conclusion was to file both
accounts separately and have them name each other, rather than to assert a
connection neither source claims — [DP-009](../../docs/design-principles.md#dp-9).

## Why `Proposed`

**Two of the three mechanisms the authors propose also predict the null.**
Readers may have grown suspicious of AI-styled text, penalizing it directly.
Or authors who did not write their own petition may feel less ownership and
so promote it less off-platform, which is what actually drives signatures.
Neither is about scarcity, both produce flat-or-worse outcomes alongside
improved text, and neither has been tested. The reader-suspicion account in
particular also predicts the observed reversal, since a feature that becomes
a *marker of AI use* would acquire a negative coefficient for reasons that
have nothing to do with this theory.

**The inversion is reported, not investigated.** It appears in an appendix and
one discussion sentence. Nobody has plotted predictive validity against the
dispersion of the feature it rests on, which is the measurement that would
distinguish "the signal was diluted" from "the signal acquired a new meaning".

**One platform, one tool, eleven weeks.** And an unusual platform: petition
success depends heavily on off-platform promotion, which is precisely the
channel the ownership hypothesis runs through, so Change.org may be the case
where the rival explanation is strongest.

## What it does not say

**It does not say the writing did not improve.** It did, measurably, by human
judgement, with a large effect size. The claim is about what that improvement
was worth once everyone had it.

**It does not say features never cause outcomes.** Most real associations are
some of both. The claim is that the distinguishing component is invisible
until an intervention compresses the distribution, and that it can be large
enough to cancel the causal component entirely.

**It does not generalize to any deployed model automatically.** The account
needs a population whose members are *compared against each other* for a
scarce outcome — signatures, attention, a job, a grant. Where the outcome is
not rivalrous, giving everyone a better draft can simply make everyone better
off, and nothing here argues otherwise.
