---
number: 327
status: Proposed
formerly:
- SOTA-tmpclqxm
promote_when: >-
  A published measurement, by a group other than the MRL authors, of a
  text-embedding model trained with nested prefix losses, against separately
  trained models of the prefix widths, on retrieval benchmarks with graded
  relevance. It must report both the prefix accuracy and the full-width cost.
  A vendor exposing a `dimensions` parameter does not count, and neither does
  a comparison only against truncating an embedding trained without MRL.
title: 'Train retrieval embeddings with nested losses, so a prefix of the vector can shortlist and the full vector re-rank'
version: 1
tags:
- representation-and-encoding
- inference-optimization
date: '2026-09-22'
source:
- LIT-547
introduced_by:
- LIT-547
consensus: emerging
consensus_note: >-
  It has spread beyond the authors, though not only to independent groups.
  Google's EmbeddingGemma paper evaluates its model with truncated outputs,
  and Google is also the authors' organization. OpenAI's text-embedding-3
  models take a dimensions parameter, which third-party documentation
  (Weaviate, Supabase) credits to MRL. Vector databases document prefix
  shortlisting as a supported pattern. That is adoption, not evidence
  (DP-005). The status stays Proposed because the record holds no
  measurement of what people actually use it for, which is text retrieval,
  and the one measurement it does hold is the authors' own.
implementations:
- text-embedding-3
- EmbeddingGemma
summary: >-
  Kusupati, Bhatt, Rege et al. (2022), [LIT-547](../literature.d/LIT-547.md) — put the loss on
  log(d) nested prefixes of the embedding. Each prefix then matches a
  separately trained model of that width (ResNet50, ImageNet), and one
  database supports shortlisting on 16 dimensions and re-ranking on 2048:
  equal mAP@10, 14× faster. Measured on image retrieval. Widely shipped in
  text embedding models without an independent comparison in the record.
---

# SOTA-327: Train retrieval embeddings with nested losses, so a prefix of the vector can shortlist and the full vector re-rank

## Source

Kusupati, Bhatt, Rege et al. (2022), [LIT-547](../literature.d/LIT-547.md) — Matryoshka
Representation Learning. Read as [NOTE-291](../notes.d/NOTE-291.md).

## The practice

**When training an embedding model, add the loss at about `log₂ d` prefix
lengths**, halving from the full width down to a small bottleneck (8 or 12
dimensions in the paper), with a head per prefix or one tied head.
Normalize each prefix separately if the representation is normalized. That
is the only change.

**Then deploy one vector at several costs:**

- **Store one database of full-width embeddings.** Do not keep one per width
- **Shortlist on a prefix, re-rank on the full vector.** A 16-d shortlist
  of 200 and a 2048-d re-rank matched single-shot 2048-d retrieval at about
  14× lower wall-clock on ImageNet-1K. The harder ImageNet-4K needed a 64-d
  shortlist (6×). So the shortlist width is a per-corpus setting, not a
  constant
- **Truncate when storage or bandwidth is the constraint.** A prefix is at
  least as good as a separately trained model of that width, and far better
  than SVD or random dimensions below 256

## Conditions

- **Measured on image retrieval with class labels as relevance**
  (ImageNet-1K/4K), on ResNet50, ViT-B/16 (JFT, ALIGN), and BERT for masked
  LM only. **No text retrieval is measured in the source**
- **The full-width vector gives up a little.** On the web-scale models,
  0.15–0.25 top-1 k-NN points at full width. If you only ever use the full
  width, this is a small cost for nothing
- **Against separately trained narrow models, the evidence is ResNet50 on
  ImageNet.** At web scale the paper compares only against random subsets of
  the full model's features, which is a weak baseline
- **Measure the end task, not only the retrieval metric** ([SOTA-308](SOTA-308.md)). The
  paper's mAP@10 is label recall

## Known implementations

- OpenAI `text-embedding-3-small` / `-large` (`dimensions` parameter)
- EmbeddingGemma
