---
number: 28
status: Read
formerly:
- NOTE-tmp3trot
paper: LIT-048
title: 'Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation'
version: 1
tags:
- model-architecture
date: '2026-09-09'
summary: >-
  Replaces position embeddings with a fixed linear penalty on attention scores proportional to query–key distance, one slope per head from a geometric sequence. Trains on short sequences and evaluates on longer ones. The paper's own Appendix B says the gain is "largely explained by" avoiding the early token curse rather than by better use of long history.
---

# NOTE-028: Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation

## Contribution

Asks a question the transformer literature had left open — *how does a model
handle sequences longer than it was trained on?* — and answers it by removing
position embeddings entirely.

**ALiBi** adds a static, non-learned bias to each attention score, linear in
the distance between query and key:

    softmax(q_i · k_j + m · −(i − j))

with `m` a per-head slope. Nothing is added to the token embeddings; there is
no position representation at all, only a recency penalty whose strength varies
by head.

## Key insight

The heads need *different* recency preferences, and the useful ones are all
gentle. The slopes are the geometric sequence `2^(-8/n)`, i.e. for 8 heads
`1/2¹, 1/2², …, 1/2⁸`; for 16 heads the same sequence with the geometric mean
of each consecutive pair interleaved. The authors are explicit that this came
from **"a brief manual exploration of around ten slope sets"**, and their
stated generalisation is:

> the slope sets that work best are those with slopes in the (0, 1) range,
> with the slopes' density increasing as we get closer to 0.

**Making the slopes trainable did not yield strong extrapolation** and slowed
training by 3%. A fixed, hand-found, non-learned constant beat learning it —
which is the interesting result and the one most summaries drop.

## Assumptions

- **Recency is the right inductive bias** for causal language modelling. The
  penalty is monotone in distance and unconditional on content.
- The slope set transfers: found on WikiText-103, applied unchanged to other
  corpora and model sizes, and reported to work.
- Decoder-only causal attention.

## Key results

- **Extrapolation works.** Sinusoidal models "cannot extrapolate at all" —
  performance degrades as soon as one token beyond `L` is added at evaluation,
  for both `L = 512` and `L = 1024`.
- **The T5 relative-position bias also extrapolates.** Raffel et al. proposed
  this and never tested it; this paper tests it and confirms it. ALiBi's
  novelty is therefore being *fixed and cheap*, not being the only thing that
  extrapolates.
- **At 1.3B on a 461 GB corpus**, ALiBi matches sinusoidal perplexity while
  **running faster and using less memory**, because it can be trained on
  shorter subsequences. That is the practical argument, and it is about
  training cost, not about long-context quality.
- **The deflationary finding, from the authors, in Appendix B:** ALiBi's edge
  over sinusoidal embeddings is **"largely explained by its improved avoidance
  of the early token curse"** — the difficulty of predicting tokens that have
  little context behind them. They add that future work "might achieve further
  gains by more efficiently exploiting longer histories", i.e. **ALiBi is not
  doing that.**

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Sinusoidal position embeddings do not extrapolate at all | strong | measured, immediately past `L` |
| C2 | A fixed linear distance penalty enables extrapolation | strong | the paper's core result, several corpora and sizes |
| C3 | The T5 bias also extrapolates | strong | tested here for the first time |
| C4 | The specific geometric slope set transfers unchanged across domains and sizes | moderate | asserted from ~10 hand-tried sets, then applied unmodified |
| C5 | Learned slopes are worse | moderate | tried, reported, 3% slower |
| C6 | **The perplexity gain is mostly early-token-curse avoidance, not better long-range use** | strong — the authors' own analysis | Appendix B |

## Method

Delete position embeddings. Add `m·−(i−j)` to every attention score before the
softmax, with per-head `m` from the geometric sequence starting at `2^(-8/n)`.
Train on short sequences; evaluate on long ones.

## Concepts

- **Position as a bias on scores rather than a signal in the representation** —
  the move, and the one RoPE makes differently.
- **Per-head recency slopes** — heads specialise by *how far back they look*,
  set rather than learned.
- **The early token curse** — the confound that makes "perplexity improves with
  longer evaluation context" a much weaker statement than it appears.

## Connections

Directly upstream of the long-context practice line, and the alternative to
<!-- inactive-ok-block: SOTA-179 — Proposed, named as the record's neighbourhood for this question rather than relied on -->
RoPE that lost. `SOTA-179` (truncate the rotary encoding's low frequencies
rather than rescaling its base) is the same problem — position representations
that do not survive length changes — approached from the RoPE side.

C6 is the connection worth having: **it is a methodological warning about every
long-context evaluation in the record.** A model that scores better when given
a longer evaluation window may simply be answering fewer hard early-token
questions, and this paper is where that confound is named and measured.

## Recommendations

- **R1** — When evaluating on longer sequences than training, separate the
  early-token effect from genuine long-range use before claiming the latter.
  *Topic:* analysis and evaluation. *Strength:* strong, and it is the authors'
  own caveat about their own headline.
- **R2** — Consider a fixed non-learned positional bias; learning it did not
  help and cost 3%. *Topic:* model architecture. *Strength:* moderate.
- **R3** — Give heads different recency scales in the (0,1) range with density
  increasing toward 0. *Strength:* weak — a hand-found constant from ~10 tries,
  reported as transferring.
- **R4** — The reason to train on short sequences is *training cost*, not
  quality. *Strength:* moderate.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.** RoPE
won; ALiBi is carried as a historical alternative.

The reading's value is C6, which the record should have and does not. Every
long-context claim in the corpus is a claim about a model doing better with
more context, and this paper — from the authors of the technique being praised
— says most of their own measured improvement was **not** that. The record has
no practice or note stating that confound, and it applies far beyond ALiBi.

The document's takeaway **"theoretical analysis" is false.** There is no
theoretical analysis in this paper. The slopes come from trying about ten sets
by hand, and the mechanism claim in Appendix B is empirical. That bullet
attributes to the paper the one kind of contribution it does not make.

## Limitations

- 1.3B maximum, 2021, decoder-only causal LM.
- C4 rests on a hand search of ~10 slope sets; there is no principle behind the
  geometric sequence.
- Recency is imposed unconditionally, so genuinely long-range dependencies are
  penalised by construction — which is consistent with C6 and never framed as
  the cost it is.
- No downstream task evaluation; perplexity throughout.

## Open questions

- If the gain is early-token-curse avoidance, what *does* buy better use of
  long history? The authors pose this and leave it.
- The slopes were never derived. Given how much the record's µP-adjacent
  practices care about principled scaling, a hand-tuned per-head constant that
  reportedly transfers across scales is an odd thing for nobody to have
  explained.
