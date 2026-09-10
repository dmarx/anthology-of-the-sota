---
number: 60
paper: LIT-060
status: Read
formerly:
- NOTE-tmpqqz7s
title: 'Improving Language Models by Retrieving from Trillions of Tokens'
version: 1
tags:
- model-architecture
date: '2026-09-09'
published: '2021-12-01'
summary: >-
  Matches GPT-3 on the Pile with 25× fewer parameters by cross-attending to chunks retrieved from a 2-trillion-token database, using a frozen BERT retriever that never needs training. The gain is constant from 150M to 7B, and the model improves at *evaluation* time by enlarging the database — capability added after training ends.
---

# NOTE-060: Improving Language Models by Retrieving from Trillions of Tokens

## Contribution

Retrieval at a scale nobody had tried: a **2-trillion-token** database, cross-
attended by an autoregressive language model, giving performance **comparable to
GPT-3 and Jurassic-1 on the Pile with 25× fewer parameters.**

Three specific choices make it work:

- **A frozen, pretrained BERT retriever.** No retriever training, no periodic
  re-indexing as the model changes. The paper's claim is that this "works at
  scale", removing the moving part that retrieval-augmented systems usually
  break on.
- **Chunked cross-attention**, with time complexity **linear in the amount of
  retrieved data** — so retrieving more is affordable.
- **A leakage-aware evaluation** that accounts for proximity between test
  documents and the training set.

## Key insight

**Parameters and a database are substitutable, and they are not the same
resource.** 25× fewer parameters for comparable quality is an allocation
statement, and it introduces a third axis alongside the parameter/token
trade the record carries from the Chinchilla line.

The consequence that makes it different in kind: **Retro "can be improved at
evaluation time by increasing the database size and the number of retrieved
neighbours."** Capability that increases after training has finished, with no
gradient step. Nothing else in the record does that.

And the gain is **constant from 150M to 7B**, so retrieval is not a small-model
crutch that scale absorbs — it is an additive benefit across the range tested.

## Assumptions

- **A frozen retriever is good enough.** The load-bearing engineering claim, and
  the one that makes the system operable.
- The database is available at inference and its cost is acceptable — 2T tokens
  of storage and nearest-neighbour search is not free, and the paper's parameter
  comparison does not price it.
- Retrieved chunks are usable without the model having been trained to compose
  them from scratch.

## Key results

- **Comparable to GPT-3 and Jurassic-1 on the Pile with 25× fewer parameters**,
  from a 2T-token database.
- **Constant gain from 150M to 7B parameters.**
- **Improvable at evaluation time** by enlarging the database or retrieving more
  neighbours.
- State of the art on a range of downstream sets including WikiText-103 and the
  Pile; fine-tunable to competitive question answering.
- **A proposed evaluation aware of test-document proximity to the training set**,
  which the authors note "is relevant for all language models, and especially for
  retrieval-enhanced models since they have direct access to the training dataset
  during evaluation."

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | A 2T-token database substitutes for 25× the parameters | strong | measured on the Pile against two baselines |
| C2 | A frozen BERT retriever suffices at this scale | strong | the system works without retriever training |
| C3 | The gain is constant across 150M–7B | strong | measured across the range |
| C4 | Capability increases at evaluation time with database size | strong | measured |
| C5 | Leakage-aware evaluation is necessary for retrieval models | strong | argued, and the paper builds one |

## Method

Chunk the corpus. Embed with a frozen BERT. At training and inference, retrieve
nearest-neighbour chunks per input chunk and incorporate them by chunked
cross-attention. Evaluate with test/train proximity accounted for.

## Concepts

- **Database as a substitute for parameters** — the allocation claim, and a
  third axis beside model size and token count.
- **Post-training capability growth** — C4, and the property that makes
  retrieval structurally different from scaling.
- **Freezing the retriever** — removing the co-adaptation problem by declining to
  co-adapt.
- **Proximity-aware evaluation** — C5, which the paper says applies to *all*
  language models.

## Connections

Sits directly against the record's allocation line — `LIT-028` and `LIT-040`
(sub-linear), Chinchilla (1:1), `LIT-099` (1:1 confirmed). All of those trade
parameters against **tokens seen during training**. This trades parameters
against **tokens available at inference**, which none of them models.

C5 is the fourth instance in this pass of evaluation being the problem:
`LIT-077` ships a contamination probe, `LIT-073` builds DrawBench because COCO
could not resolve its comparison, `LIT-072` finds two metrics with opposite
optima, and this proposes proximity-aware evaluation.

## Recommendations

- **R1** — Treat an inference-time database as a third allocation axis beside
  parameters and training tokens. *Topic:* model architecture. *Strength:*
  moderate — measured to 7B on 2021 baselines.
- **R2** — Freeze the retriever. *Strength:* strong; it removes the
  co-adaptation and re-indexing problem, and it worked at trillion-token scale.
- **R3** — Evaluate with test/train proximity accounted for, especially but not
  only for retrieval models. *Topic:* analysis and evaluation. *Strength:*
  strong.
- **R4** — Report the database's cost when claiming a parameter reduction.
  *Strength:* strong — this paper does not, and the 25× is the headline.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**
Retrieval-augmented pretraining is not a line the anthology tracks, and the
record's inference practices are about serving a parametric model.

<!-- inactive-ok-block: SOTA-160 — Proposed, named as an allocation practice this bears on rather than relied on -->
R1 is the finding worth recording. Every allocation practice in the record —
the Chinchilla line, `SOTA-160`'s joint token-budget-and-quantization decision —
assumes capability is fixed at the end of training and the only question is how
to spend the training budget. **C4 is a direct counterexample: a system whose
capability rises after training with no gradient step.** Whether that changes
anything the record recommends is a registry question; that the record has no
place to put it is a fact.

The document's takeaways get two things wrong. **"Efficient similarity search"**
is not a contribution — the retriever is a frozen off-the-shelf BERT, and the
paper's point is that it did *not* need to build one. And **"memory-efficient
architecture"** is backwards: the architecture trades a 25× parameter reduction
for a two-trillion-token database, which is the opposite of memory-efficient
unless you count only the weights.

## Limitations

- 2021, up to 7B, against GPT-3-era baselines.
- The 25× parameter claim omits the database's storage and search cost entirely.
- C2 is an engineering result at one retriever and one scale.
- Whether the retrieved-chunk mechanism composes reasoning or only supplies
  facts is not examined.

## Open questions

- What is the exchange rate? C1 gives one point — 25× at 2T tokens — and the
  curve relating database size to parameter savings is exactly what an
  allocation practice would need.
