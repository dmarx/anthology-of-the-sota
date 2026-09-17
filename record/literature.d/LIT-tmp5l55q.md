---
status: Active
title: 'The English phrase-as-lemma construction: When a phrase masquerades as a word, people play along'
version: 1
tags:
- representation-and-encoding
date: '2026-09-17'
published: '2025-06-01'
doi: '10.1353/lan.2025.a962899'
first_author: 'Goldberg'
keywords:
- 'phrasal compounds'
- 'constructions'
- 'grammatical categories'
- 'family of constructions'
- 'quotes'
implementations: []
summary: >-
  Goldberg and Shirtz (2025), Language 101(2):291-320. English has a
  construction — `a don't-mess-with-me driver` — in which a unit with the
  internal syntax of a phrase, up to a whole sentence, occupies a slot
  reserved for a word, and speakers treat it as a word: four preregistered
  surveys (N = 685 plus 70) find such sentences judged to presuppose more
  shared common knowledge, and to be wittier and more sarcastic, than normed
  near-paraphrases. The effect survives restricting to high-frequency phrases
  and shows no frequency dependence. **No model was run and the paper makes
  no recommendation** — it is filed as evidence about where a lexical unit
  ends, which is the question tokenization answers and which the record holds
  nothing else on. See [ADR-tmps5go3](../decisions.d/ADR-tmps5go3.md) for the scope call it forced.
---

<!-- inactive-ok-file: ADR-tmps5go3 — Proposed, filed in this same change,
     and named in both places AS the open question this note forced rather
     than as a settled rule. Proposed is where it should stay until a second
     case arrives; see its own consequences section. -->

# LIT-tmp5l55q: The English phrase-as-lemma construction: When a phrase masquerades as a word, people play along

Goldberg and Shirtz (2025) — Language 101(2):291-320, <https://doi.org/10.1353/lan.2025.a962899>

## Key takeaways

- **The phenomenon is a unit with the internal syntax of a phrase in a slot
  reserved for a word**, and it goes up to whole sentences: `a trickle-down
  policy`, `a must-do task`, `an 'I'm not a witch' moment`, `a 'take music for
  granted' attitude`. All attested in COCA.

- **It resists every familiar category, and the argument is distributional
  rather than theoretical.** Against a compound analysis: `very` and `more`
  modify PALs (`a very 'I'm white and right' way`, `a much more 'I'm
  compassionate too' campaign`), which modify adjectives rather than compound
  nouns; and PAL + Noun cannot scope over a distinct head noun, which NN and
  AN compounds can. For one: PALs take compound stress (`an 'I'm not a WITCH'
  moment`, not `a nonwitchy MOMent`) and bind tightly enough that adjectives
  resist intervening. The authors' conclusion is that the construction needs
  its own representation — external syntax of a word, internal syntax of a
  phrase — rather than assimilation to Noun or Adjective.

- **Speakers act on the word-slot, and that is the measured part.** Four
  preregistered surveys on Prolific, against 100 sentence pairs normed for
  semantic similarity (target pairs at M = 90.4, statistically
  indistinguishable from near-synonymous fillers at 93.0). 700 recruited, 685
  after two catch trials:
  - **shared common knowledge** — PAL chosen 77.3% (β = 1.69, p < 0.0001); a
    separate 'shared background' wording, 74.3%
  - **wittiness** — 82.2% (β = 2.58, p < 0.001)
  - **sarcasm** — 84.5% (β = 2.71, p < 0.001)

- **No frequency effect, and Study 4 is the reason that matters.** Estimated
  log COCA frequency of each PAL phrase predicted nothing. A fourth survey (70
  new participants) restricted to high-frequency phrases — `anything goes`,
  `all you can eat`, `do it yourself`, `wait and see`, `trickle-down` —
  reproduced every effect at roughly the same size (common knowledge 72.9%,
  wittiness 79.8%, sarcasm 84.5%). **So the effect is not memorization of
  particular strings.** It is carried by the construction, which is what makes
  it a claim about structure rather than about a list.

- **The mechanism proposed is lemma-like meaning.** A word-slot implies a
  lemma; a lemma presupposes familiarity with the semantic frame it names
  (Fillmore); so putting a phrase there asserts that the situation it
  describes is one the listener already recognizes — the linguistic analogue
  of observational humor. The form's peculiarity and its function are claimed
  to be the same fact, which is why the paper predicts comparable
  constructions in unrelated languages (Hebrew and Brazilian Portuguese are
  observed).

- **Stated limitations.** English only, with cross-linguistic comparison left
  to future work and flagged as hard because reference grammars omit
  infrequent constructions. The analysis is restricted to phrases containing
  a verb; other phrase types, non-English quotes and noises (`kids are
  'doo-doo-doo-doo'-ing the day away`) are expected to assimilate but were not
  tested.

## Standing in the anthology

**This note sources no practice and no theory, deliberately, and the reason is
not the paper's quality.** It is a preregistered study with normed stimuli, a
replication under the one condition that would have explained the effect away,
and a null result the authors went looking for. What it does not contain is
anything about a machine: no model was run, no representation was learned,
nothing here was measured on a system this anthology gives advice about. Under
[DP-006](../../docs/design-principles.md#dp-6) the entry question is whether the work contains an instruction, and for
this record it does not.

It is here because of what it is evidence *about*. The record's
`representation-and-encoding` topic covers "how the signal is encoded before
the expensive network sees it — tokenizers and learned latents", and every
practice filed under it takes for granted that there is a defensible answer to
*where a unit of meaning ends*. This paper is a measurement of a case where
English says the answer is "a whole sentence, used as one word", and where
speakers demonstrably act on that. That is the empirical situation
multi-word-expression and phrase-level tokenization work is built on, and the
record holds nothing else on it.

**The tag is the closest available and it does not fit cleanly**, which is a
finding about the vocabulary rather than about the paper — [DP-009](../../docs/design-principles.md#dp-9) — and
saying so here rather than absorbing it quietly is what [DP-008](../../docs/design-principles.md#dp-8)'s corollary
requires. [ADR-tmps5go3](../decisions.d/ADR-tmps5go3.md) is where that question is put.
