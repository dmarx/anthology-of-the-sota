---
number: 234
status: Read
formerly:
- NOTE-tmppb47z
paper: LIT-485
title: 'SimpleStories'
version: 1
date: '2026-09-21'
summary: >-
  Read to see what, if anything, it establishes that its trunk did not. The
  dataset comparison is direct and well instrumented; the model comparison is
  confounded three ways and the authors say so. The practice this record takes
  from it is about the generation procedure, which was measured.
---

# NOTE-234: SimpleStories

## Contribution

`LIT-484` needed a diverse synthetic corpus, described a mechanism for
getting one, and did not check. This checks: **59.38% of TinyStories contains
"once upon a time" verbatim**. Then it diagnoses why — the constraint was
lexical, and repetition lives in the frame, not the word list — and builds a
generator that constrains the frame instead.

What is true afterwards that was not before: sampling content words into a
prompt is a weak diversity mechanism at scale, and there is a measured
alternative with the numbers to compare against.

## Key insight

**Constrain the story, not the words in it.** Every generation names a theme,
a topic, a writing style and a narrative feature, and sometimes a grammar
feature and an author persona, drawn from lists of 63, 48, 23, 26, 31 and 23.
Separately and importantly, each story must **begin with a given part of
speech and initial letter**, with letter frequencies from a reference corpus.

That last constraint is doing specific work. The identified failure was
near-identical *first sentences*; an opening constraint "disambiguates
generations from the first token onwards", which is why the fix can be small
and local and still move a corpus-level statistic.

A by-product falls out for free: because the parameters were chosen rather
than inferred, every story arrives **labelled**.

## Assumptions

- Generated with **GPT-4o-mini**, against TinyStories' GPT-3.5/GPT-4. Some of
  the difference is four years of generator, not the procedure.
- **Nucleus sampling at temperature 1**, which the authors argue is safe here
  *because* the parameterization supplies the entropy that temperature
  otherwise has to.
- Evaluation is English-only; the Japanese half is unevaluated for lack of a
  fair comparison.
- Model-as-a-judge is GPT-4o-mini, with chain-of-thought elicited before
  grading.

## Key results

**On the data — direct, and the reason this is filed:**

- Top 4-gram frequency **59.38% → 7.49%**. "there was a little" 28.24%, "a
  little girl named" 16.52%, none with a counterpart above 5%.
- Lower compression ratio and lower Self-BLEU self-homogenization, both at
  p < 0.001; higher n-gram diversity score for n = 1…10, the gap widening
  with n.
- POS-template rate **88.9 vs 100**; template-per-token **0.016 vs 0.026**.
- Model-as-a-judge: much greater content and style diversity, **no significant
  difference in simplicity** — the trade that would have invalidated the
  result did not happen.
- Labels are recoverable by a judge above chance for every field, `topic`
  strongly, `theme`/`style`/`narrative feature` weakly, with no elicitation.

**On the models — one clean arm and one confounded one:**

- **Clean:** holding dataset and architecture fixed and varying only the
  tokenizer, a 4,096-token WordPiece vocabulary seeded with English affixes
  beats GPT-2's 50,257 by **+26.7 coherence** and **+27.5 quality**.
- **Confounded:** SimpleStories models beat TinyStories-33M on originality,
  coherence, grammar and quality — across a different dataset, a different
  tokenizer and a different architecture at once.
- A Llama-architecture TinyStories-33M improves on the original but stays
  behind, which separates architecture from the rest of the bundle and leaves
  dataset and tokenizer entangled with each other.
- TinyStories-33M's **grammar score nearly matches the best model** while its
  other scores do not — the authors read this as its training having
  emphasized grammatical correctness.
- Single-layer bilinear-MLP models: `[bos, 'once']` is the TinyStories model's
  strongest bigram outlier, and **6–10% of its outliers are non-ASCII**
  characters from encoding errors in the corpus.

## Claims

**Well supported:** that the TinyStories generation procedure produced a
formulaic corpus, and that parameterizing the prompt above the lexical level
plus constraining the opening produces a less formulaic one at comparable
simplicity. Five instruments, agreeing, on the artefact itself.

**Well supported and about something else:** the tokenizer result. It is the
only fully controlled comparison in the paper and it is large.

**Not supported by the experiment offered:** that the *dataset* improves
downstream model quality. Three things vary at once. The abstract's "improved
sample efficiency" rests on this comparison.

**Stated as a limitation by the authors, which is why this reading trusts the
rest:** no custom tokenizer was trained on TinyStories, so tokenization and
corpus are never separated. They name the missing arm precisely.

**A recommendation, not a result:** count embedding parameters when reporting
a small model's size. Argued from a documented case of the ambiguity causing
a misreading, not measured.

## Method

Generate 2M stories per language under a parameterized prompt; measure
diversity against TinyStories five ways; train a suite from 1.25M to 35M
parameters with a custom tokenizer; grade generations with a judge; ablate
the tokenizer; probe the labels; compare bigram-outlier structure in
single-layer models on each corpus.

## Connections

- [LIT-484](../literature.d/LIT-484.md) is the trunk. Declared as `extends` — this modifies the
  generation procedure rather than disputing the finding.
- [SOTA-127](../practices.d/SOTA-127.md) filters chain-of-thought traces out of a tiny model's
  training data. Same family of move: at this size the corpus is the
  specification, and what you leave in shows up in the weights — which the
  bigram-outlier comparison here demonstrates literally.
- The tokenizer finding belongs beside the record's `representation-and-encoding`
  work rather than beside its data work, which is why it is filed as its own
  practice.

## Bearing on the record

Two practices, and they come from different halves of the paper — one from
the part that was measured directly, one from the part that was ablated
cleanly. A third, about how to report a small model's parameter count, is a
convention the paper argues for rather than a result.

It also closes a question `NOTE-233` left open: the trunk assumed its
diversity mechanism worked and this is the measurement.

## Limitations

**The headline is the confounded comparison.** A reader taking the abstract's
"improved sample efficiency compared to the TinyStories dataset" at face value
is taking a three-way difference as a one-way one.

**Four years of generator sit inside the comparison.** GPT-4o-mini versus
GPT-3.5/GPT-4, uncontrolled. Some of the diversity gain is likely a better
instruction-follower, not a better prompt.

**Simplicity is judged, not measured** — Flesch-Kincaid is reported for both
but the "no significant difference in simplicity" result is the judge's.

**English only** for every evaluation, on a two-language dataset.

## Open questions

- How much of the downstream gain is the dataset? The authors name the
  experiment that would answer it — a custom tokenizer on TinyStories — and
  did not run it.
- Does the opening constraint alone recover most of the diversity gain? It is
  the cheapest component and is never ablated separately from the
  parameterization.
- What is the smallest model that outputs grammatical English under an honest
  parameter count? The paper raises the question, recommends the convention,
  and explicitly declines to answer it.
