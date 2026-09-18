---
number: 22
status: Active
formerly:
- THEORY-tmprceog
title: 'A phrase placed in a word slot is read as a lemma, and the reading comes from the construction rather than the phrase''s frequency'
version: 1
tags:
- representation-and-encoding
date: '2026-09-17'
source:
- LIT-410
explains: []
summary: >-
  Goldberg and Shirtz (2025), [LIT-410](../literature.d/LIT-410.md) — English has a productive
  construction in which a unit with the internal syntax of a phrase, up to a
  whole sentence, occupies a slot reserved for a word, and comprehenders give
  it the kind of meaning a word has: it evokes a semantic frame presumed to be
  shared. Four preregistered surveys measure the reading, and the fourth
  removes the obvious deflation — the effect is the same size on
  high-frequency phrases, and estimated corpus frequency predicts nothing. So
  **the lexical unit is delimited by construction, not by how often the string
  has been seen**, which is the assumption a frequency-merge tokenizer makes.
---


# THEORY-022: A phrase placed in a word slot is read as a lemma, and the reading comes from the construction rather than the phrase's frequency

## Source

Goldberg and Shirtz (2025), [LIT-410](../literature.d/LIT-410.md) —
*Language* 101(2):291-320.

## What was actually shown

**The form.** A unit with the internal syntax of a phrase — up to a complete
sentence — appears in a slot reserved for a word: `a trickle-down policy`, `an
'I'm not a witch' moment`, `a 'take music for granted' attitude`. All attested
in COCA, all productive rather than listed.

**That it is a category of its own, argued distributionally.** `very` and
`more` modify these units (`a very 'I'm white and right' way`), which modify
adjectives rather than compound nouns; but they take compound stress and bind
tightly enough that adjectives resist intervening; and unlike compounds, the
phrase + Noun combination cannot scope over a distinct head noun. No familiar
category covers the distribution, which is why the authors argue for
representing the external syntax of a word over the internal syntax of a
phrase directly.

**That comprehenders act on the word slot.** Four preregistered Prolific
surveys, 100 sentence pairs normed for semantic similarity — targets at
M = 90.4, statistically indistinguishable from near-synonymous fillers at
93.0 — 685 participants after catch trials. Against those paraphrases the
phrase-in-a-word-slot version was judged to imply more shared common
knowledge (77.3%, β = 1.69, p < 0.0001; a separate 'shared background'
wording, 74.3%), wittier (82.2%, β = 2.58) and more sarcastic (84.5%,
β = 2.71).

**And the part that makes it a claim about structure.** The deflationary
reading is that these are memorized strings and the effect is familiarity. The
authors tested it directly: estimated log COCA frequency of each phrase
predicted nothing in the main analyses, and Study 4 re-ran the whole design on
70 new participants using **only** high-frequency phrases — `anything goes`,
`all you can eat`, `do it yourself`, `wait and see`, `trickle-down` — where
every effect reproduced at roughly the same size (72.9%, 79.8%, 84.5%). The
reading survives when the string is maximally familiar, so it is not carried
by the string.

**What could have come out the other way.** Study 4 is a preregistered attempt
to kill the authors' own account, and the frequency nulls are reported rather
than buried. That is the shape of evidence this record counts: a prediction
that had a way to fail.

## Why this is filed here, and what it bears on

The claim is about **where a lexical unit ends**, which is the question
[SOTA-007](../practices.d/SOTA-007.md) answers and the one every practice under
`representation-and-encoding` presupposes. That practice's own body reasons in
exactly these terms — a tokenizer that spends "more tokens per unit of
meaning" is paying a permanent tax — and BPE's answer is that the unit is
whatever adjacent-pair frequency merged, bounded above by roughly a word.

This finding says that in the data, a lexical unit can be an arbitrary-length
phrase, and **that which units get the reading is fixed by construction rather
than by frequency**. Those are the two properties a frequency-merge vocabulary
cannot represent: it is bounded, and it is frequency-driven. The paper is not
an argument against BPE and does not mention it. What it is, is a measurement
of the thing BPE approximates, which the record held nothing on.

## What this does not say

**It is not about a model, and nothing here was measured on one.** The
subjects are people. Reading this as a result about transformers is the
overreach this section exists to mark — the finding is about the signal, not
about anything trained on it.

**It does not show that a model fails to recover these units.** The natural
next claim is that a tokenizer splitting a construction forces the network to
reassemble it. The record now holds the mechanism side of that:
[THEORY-021](THEORY-021.md) — models rebuild multi-token units into
single representations in early layers, and the units include
**non-compositional multi-word expressions**, which is this document's subject
approached from inside a model.

That overlap is narrower and better than "both concern tokenization", and it
is still not one claim. **Nobody has run the experiment**: whether the units a
model's implicit vocabulary contains are the ones a language delimits by
construction, and what becomes of the ones it does not. Reading the pair as
"the network repairs what the tokenizer broke" would be the anthology
asserting a result nobody has produced.

**It does not license a tokenization practice.** No recommendation follows
without the missing half above: knowing that the data contains
construction-delimited units says nothing about whether a vocabulary should
try to hold them, which is a cost question nobody in this record has measured.
`explains:` is deliberately empty.

**English, and phrases containing a verb.** The authors observe comparable
constructions in Hebrew and Brazilian Portuguese and predict them generally,
but did not test them; and the analysis excludes non-verbal phrases,
non-English quotes and noises, which are expected to assimilate and were not
checked. A cross-linguistic result is what would turn the prediction into a
finding.

**Status `Active` is about this claim, not about its reach.** The account is
preregistered, replicated under the condition that would have explained it
away, and the best the record holds for why these units are read as they are.
It is `Active` in a record that holds no other evidence on the question, which
is a weak kind of best.
