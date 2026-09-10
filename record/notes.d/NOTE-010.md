---
number: 10
status: Read
formerly:
- NOTE-tmp74997
paper: LIT-003
title: 'Neural Machine Translation of Rare Words with Subword Units'
version: 1
tags:
- representation-and-encoding
date: '2026-09-09'
published: '2015-08-01'
summary: >-
  Translation was open-vocabulary and NMT models were not, backing off to a dictionary for unknown words. Encoding rare and unknown words as subword units — byte pair encoding adapted to segmentation — makes the model open-vocabulary itself.
---

# NOTE-010: Neural Machine Translation of Rare Words with Subword Units

## Contribution

Neural translation models operated with a **fixed vocabulary** while
translation is an **open-vocabulary problem** — names, compounds, morphology
and loanwords are unbounded. The standard workaround was to back off to a
dictionary for out-of-vocabulary words, which handles them outside the model.
This paper makes the model itself open-vocabulary by encoding rare and unknown
words as **sequences of subword units**, adapting **byte pair encoding** from
compression into a segmentation algorithm.

## Key insight

An unknown word is not unanalysable — it is usually built from pieces the
model has seen. If the vocabulary is a set of *segments* rather than a set of
words, then "nothing is out of vocabulary" becomes a structural property
rather than a fallback path, because the segmentation can always descend to
characters.

The choice of BPE as the mechanism is what makes it practical: it is a
frequency-driven merge process, so common words survive as single units and
only rare ones fragment. The vocabulary size becomes a **dial** between
sequence length and coverage, set once by how many merges you run.

## Assumptions

- **Neural machine translation** of the period, on WMT tasks; encoder-decoder
  RNNs, not Transformers.
- The merge table is **fit to a corpus**, so the segmentation is only as
  appropriate as that corpus is representative — a property the paper's setting
  does not stress but every later use does.
- Vocabulary size is chosen in advance and fixed for the model's life.

## Key results

- **Subword segmentation makes NMT open-vocabulary** without a back-off
  dictionary, which is the structural claim.
- **Byte pair encoding adapted to word segmentation**: start from characters,
  repeatedly merge the most frequent adjacent pair, stop at a chosen number
  of merges.
- Frequent words remain single units; rare words decompose; **the character
  level is always available underneath**, so nothing is unrepresentable.
- Improvements on rare-word translation specifically, which is the case the
  method targets.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Translation is open-vocabulary and a fixed word vocabulary is the wrong shape for it | strong | the paper's premise, and uncontroversial |
| C2 | Subword units make the model open-vocabulary without a back-off mechanism | strong | structural — the character level is always reachable |
| C3 | BPE is a suitable segmentation algorithm for this | strong | demonstrated; the field's adoption is the stronger evidence |
| C4 | Rare-word translation improves specifically | moderate | measured on the tasks of the period |

## Method

Represent the corpus as characters. Count adjacent symbol pairs, merge the
most frequent, repeat for a chosen number of merges. The merge table defines
the segmentation; applying it to new text yields subword units, descending to
characters wherever the merges do not reach.

## Concepts

- **Open-vocabulary** — the model can read and produce any string, as opposed
  to having a closed word list plus an escape hatch.
- **Subword unit** — a segment between a character and a word. The
  representation this paper argues for.
- **Byte pair encoding** — a compression algorithm, here repurposed: the
  merges are fit once and used as a segmentation.

## Connections

Replaces the back-off-dictionary approach to unknown words. Its descendants
are every tokenizer in this record; the vocabulary-size trade it introduces
is still a live pretraining decision.

## Recommendations

- **R1** — Use subword segmentation rather than a word vocabulary with a
  back-off. *Topic:* tokenization. *Status:* standard. *Strength:* strong.
  *Applies when:* any open-vocabulary task, which is all of them.
- **R2** — Treat vocabulary size as a real trade, not a default. *Topic:*
  tokenization. *Status:* standard. *Strength:* moderate. *Applies when:*
  larger means shorter sequences and a bigger embedding and output layer paid
  on every token; smaller means the reverse.
- **R3** — Fit the merges on a corpus representative of what you will run on.
  *Topic:* tokenization. *Status:* standard. *Strength:* moderate.
  *Applies when:* always — a distribution under-represented at fitting time
  pays more tokens per unit of meaning permanently.

## Bearing on the record

**The one practice sourced to this note is confirmed.**

| practice | disposition |
|---|---|
| [SOTA-007](../practices.d/SOTA-007.md) BPE tokenization for open vocabulary tasks | confirmed — C1 through C3 |

`SOTA-007`'s body already carries the vocabulary-size trade and the
corpus-fitting tax, and both hold. The reading adds one framing worth having:
the paper's contribution is **open-vocabulary modelling**, and BPE is the
mechanism it reaches for. Stated the other way round — as a recommendation for
BPE — the practice makes the algorithm the point, when the point is that the
vocabulary should not be closed. That matters because the field has since
replaced the algorithm repeatedly while keeping the property.

## Limitations

- 2015 NMT; RNN encoder-decoders on WMT.
- Nothing here addresses the tokenizer's interaction with model scale, which
  is where the modern trade lives.
- The corpus-fitting bias is a consequence the paper does not examine;
  it becomes visible only at multilingual scale.

## Open questions

- If the durable claim is *open vocabulary* rather than *BPE*, should the
  record's practice be stated at that altitude, with BPE as one
  implementation? Byte-level and learned-segmentation alternatives all keep
  C2 and discard C3.
- The merge table is fit once and frozen for the model's life. Nothing in
  this record asks whether that is necessary.
