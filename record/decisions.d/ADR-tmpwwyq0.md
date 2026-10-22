---
status: Active
title: 'representation-learning'
version: 1
tags:
- taxonomy
- record
date: '2026-10-22'
summary: >-
  A twenty-ninth topic, primary-eligible: how learned systems come to
  represent their data. Seventy-seven documents take it, forty as primary
  where `representation-and-encoding` stood first and was the misfit. That
  topic's subject is the input before the network sees it, and it had been
  carrying contrastive, self-supervised, masked-prediction and embedding
  work besides. Rejected: widening `representation-and-encoding`, and
  tagging the graph benchmarks to silence a lineage warning.
---

<!-- inactive-ok-file: THEORY-058 — Proposed, named as a document this decision retags, not cited as an established account -->

# ADR-tmpwwyq0: representation-learning

## Context

The graph pass ([ADR-tmp7rjjv](ADR-tmp7rjjv.md)) filed DeepWalk, LINE, node2vec, NetMF, Deep
Graph Infomax, GraphCL, TransE and RotatE. NetMF `extends` Levy and
Goldberg's word-embedding analysis ([LIT-612](../literature.d/LIT-612.md)), and the lint then reported
that the joined graph and word-embedding line shares no tag across every
member. The owner asked for a tag that fits.

Looking for one showed what the two sides do share: both are filed under
`representation-and-encoding`, whose blurb is "how the signal is encoded
before the expensive network sees it — tokenizers and learned latents,
positional encoding". So is SimCLR ([LIT-591](../literature.d/LIT-591.md)), MoCo ([LIT-590](../literature.d/LIT-590.md)), BYOL
([LIT-594](../literature.d/LIT-594.md)), DINO ([LIT-664](../literature.d/LIT-664.md)), MAE ([LIT-601](../literature.d/LIT-601.md)), CPC ([LIT-589](../literature.d/LIT-589.md)), BERT ([LIT-670](../literature.d/LIT-670.md)),
GloVe ([LIT-602](../literature.d/LIT-602.md)), word2vec ([LIT-603](../literature.d/LIT-603.md)) and the practices and theories drawn
from them. None of those is about encoding the input. Each is about an
objective that makes a network learn a representation, and what that
representation then holds. It is the shape [ADR-060](ADR-060.md) found for concept
geometry: a subject filed under the nearest wrong word, which under
[ADR-059](ADR-059.md) means the axis is short.

## Decision

**A twenty-ninth topic, primary-eligible:**

> `representation-learning` — how learned systems come to represent their
> data: self-supervised, contrastive and masked-prediction objectives,
> word, node and knowledge-graph embeddings learned from co-occurrence,
> what the learned representations keep and compress, and whether they
> converge across models.

**Primary for forty documents** whose first tag was
`representation-and-encoding` and whose subject is this: the contrastive
and self-supervised papers ([LIT-589](../literature.d/LIT-589.md) to [LIT-598](../literature.d/LIT-598.md), [LIT-601](../literature.d/LIT-601.md), [LIT-663](../literature.d/LIT-663.md), [LIT-664](../literature.d/LIT-664.md)),
the word-embedding papers ([LIT-602](../literature.d/LIT-602.md) to [LIT-604](../literature.d/LIT-604.md), [LIT-609](../literature.d/LIT-609.md), [LIT-610](../literature.d/LIT-610.md), [LIT-612](../literature.d/LIT-612.md),
[LIT-613](../literature.d/LIT-613.md)), BERT and its masking rate ([LIT-670](../literature.d/LIT-670.md), [LIT-672](../literature.d/LIT-672.md)), Matryoshka
([LIT-547](../literature.d/LIT-547.md)), E5 ([LIT-744](../literature.d/LIT-744.md)), the Platonic and Contextures papers ([LIT-458](../literature.d/LIT-458.md),
[LIT-459](../literature.d/LIT-459.md)), and the practices and theories drawn from them. They keep
`representation-and-encoding` second, as [ADR-060](ADR-060.md)'s documents kept their
other tags.

**Secondary for thirty-seven**, inserted after the first tag so their
primaries stand. These are the graph and knowledge-graph embeddings
(primary `graphs-and-networks`), I-JEPA and DINOv2 (vision, data), the
protein and RNA language models (biomolecular), the information-bottleneck
papers and [THEORY-058](../theory.d/THEORY-058.md) (analysis), ALBERT, RoBERTa and SigLIP 2, Levy et
al. and Baroni et al. (analysis), and the practices on augmentation, data
curation, view counts, frequent-token subsampling and negative sampling.

The test is [ADR-046](ADR-046.md)'s: would someone browsing representation learning
expect it?

## Not retagged

- **Learned latents for generation** (VQ-VAE, VQGAN, the image and video
  tokenizers). They encode the input for a generator, which is
  `representation-and-encoding`'s subject as written.
- **Topic models and their evaluation** ([LIT-592](../literature.d/LIT-592.md), [LIT-597](../literature.d/LIT-597.md), [LIT-600](../literature.d/LIT-600.md), and the
  practices on coherence and interpretability). They are representations,
  but nothing in them is learned by the objectives this word names, and
  their readers come for evaluation.
- **Concept geometry** ([LIT-460](../literature.d/LIT-460.md), [LIT-526](../literature.d/LIT-526.md), [THEORY-034](../theory.d/THEORY-034.md), [THEORY-063](../theory.d/THEORY-063.md)).
  `concept-geometry` is about how concepts are laid out once learned, and
  the documents that are about both already carry both.
- **The graph neural networks themselves.** GIN, GCN, the graph
  transformers and the benchmarks are about architectures and evaluation.
  The pass tags only the embedding and self-supervised graph papers.

## Alternatives considered

- **Widen `representation-and-encoding`.** Rejected for [ADR-060](ADR-060.md)'s reason:
  one word for what happens to the signal before the network and for what
  the network builds from it makes the tokenizer papers and the contrastive
  papers impossible to browse apart.
- **Tag the graph benchmarks and GNN papers too, so the lineage warning
  clears.** The joined line runs from GloVe through NetMF and DeepWalk to
  GIN, GCN, LRGB and Errica et al.'s evaluation protocol. A browser of
  representation learning would not expect a benchmark audit, and adding
  the word to bind a check is the move [DP-008](../../docs/design-principles.md#dp-8)'s corollary forbids. The
  warning is the lint's "weaker signal" (each step shares a tag; no tag
  spans the line), and two such lines are already on `main`.
- **Drop NetMF's `extends: LIT-612`.** The relation is true. NetMF builds
  directly on Levy and Goldberg's shifted-PMI result.

## Consequences

- Twenty-nine topics. `CLAUDE.md` and `luria.yaml` change their counts.
- The NetMF step binds on the new word as well as the old. The
  whole-line lineage warning stays, for the reason above.
- `representation-and-encoding` keeps its blurb. Once the retagged
  documents have the new word first, what remains with the old one first
  is tokenizers, positional encodings and latents, which is what its blurb
  says.
