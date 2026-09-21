---
number: 293
status: Proposed
formerly:
- SOTA-tmph3t1d
promote_when: >-
  A second group stating the convention and applying it — a tiny-model report
  that gives both counts, or a venue or benchmark that requires the all-in
  figure. What would not move it: a report that happens to include embeddings
  without saying which convention it used, since the entire problem is that
  the two counts are indistinguishable once printed.
consensus: unassessed
consensus_note: >-
  Nobody has surveyed which convention tiny-model reports use, and the
  reason to suspect it matters is that the two papers this record holds on
  the subject use opposite ones without either being wrong. `unassessed` is
  the honest value: this is a recommendation about reporting that one paper
  has argued for and nobody has counted.
title: "Count embedding parameters when you report a tiny model's size"
version: 1
tags:
- tiny-models
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-485
introduced_by:
- LIT-485
implementations: []
summary: >-
  Finke et al. (2025), [LIT-485](../literature.d/LIT-485.md) — at these sizes the embedding
  table is not a rounding error, it is most of the model: TinyStories-33M is
  **68M** parameters all-in, and an 8M model in the same paper is "more than
  half embeddings". Two papers can each claim the smaller model and both be
  telling the truth. Print the all-in figure.
---

# SOTA-293: Count embedding parameters when you report a tiny model's size

## Source

Finke et al. (2025), [LIT-485](../literature.d/LIT-485.md) — [ARXIV-2504.09184](https://arxiv.org/abs/2504.09184) §3.5, read as
[NOTE-234](../notes.d/NOTE-234.md).

## What to do

State the parameter count including the embedding and unembedding tables, and
say that you have. If you also want the non-embedding figure, give both.

## Why it is not pedantry at this size

The convention of quoting non-embedding parameters is inherited from
large-model work, where the embedding table is a few percent of the total and
excluding it makes the number more comparable across tokenizers. At a million
to thirty million parameters that reasoning inverts:

- **TinyStories-33M is 68M parameters all-in** — the name is the
  non-embedding count, and the model is twice that.
- An 8M-parameter model in the same paper is **more than half embeddings**.
- The same architecture on the same data is a 65M model under GPT-2's
  50,257-token vocabulary and a 35M model under a 4,096-token one — the
  *architecture did not change*. The parameter count moved by a factor of
  nearly two because the tokenizer did.

So the number that gets printed is a joint claim about the network and the
tokenizer, and dropping the embeddings hides the half that is easiest to move.

**This has already caused a specific misreading**, which is the paper's own
reason for raising it: it cites a documented case and recommends that anyone
competing for "the smallest model that outputs grammatical English" count
every parameter. A leaderboard where one entry excludes embeddings and
another does not is not a leaderboard.

<!-- inactive-ok-block: SOTA-125 — Proposed, and cited for the fact that it
     states a parameter budget at a tiny scale, which is true of the document
     whatever its standing; nothing here depends on the trade it recommends
     being right -->

The record has a standing reason to care: [SOTA-125](SOTA-125.md) is a parameter-budget
trade at a tiny scale, and a budget is only a budget if everyone is counting
the same things into it.

## Conditions

**This is a reporting convention argued from one case, not a measurement.**
There is no experiment here and there could not be one; what there is, is an
arithmetic fact about where the parameters sit at this scale and one
documented instance of the ambiguity misleading a reader. Filed as `Proposed`
for that reason rather than because the argument is doubtful.

**It says nothing about which count is the right one for analysis.**
Non-embedding parameters remain the more comparable figure for scaling work
across tokenizers, which is why the convention exists. The recommendation is
to be explicit and to lead with the all-in number when the claim is about
smallness, not to abolish the other count.

**Nobody has surveyed the field.** The evidence that this is a live problem
is two papers in this record using opposite conventions, and one citation.
That is enough to recommend the fix and not enough to say how often it bites.
