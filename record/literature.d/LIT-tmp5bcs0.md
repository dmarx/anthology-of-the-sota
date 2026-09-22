---
status: Active
title: 'Gemma 3n model overview'
version: 1
tags:
- model-architecture
- inference-optimization
- representation-and-encoding
date: '2026-09-22'
published: '2025-06-01'
url: 'https://ai.google.dev/gemma/docs/gemma-3n'
first_author: 'Google DeepMind'
keywords:
- 'per-layer-embeddings'
- 'on-device'
- 'matformer'
- 'parameter-offloading'
- 'embedding-memory'
implementations:
- Gemma 3n
- Gemma 4 E2B
- Gemma 4 E4B
summary: >-
  Google DeepMind (2025), model documentation with no accompanying paper. The
  origin of Per-Layer Embeddings (PLE): each token id looks up a small vector
  for every layer, and each layer gates it into the residual stream. The
  table is about 2.35B parameters in E2B and is kept off the accelerator. A
  design disclosure and not evidence: Google published no ablation. Cited by
  the Qwen3.8-Flash-Next report ([LIT-152](LIT-152.md)) as the precedent for embedding
  tables held in host memory.
---

<!-- inactive-ok-file: SOTA-tmp0fz4e — Proposed, filed in this same contribution from this paper's own ablations; new, not retired, and cited as the practice this document feeds -->

# LIT-tmp5bcs0: Gemma 3n model overview

Google DeepMind (2025) — https://ai.google.dev/gemma/docs/gemma-3n

## Key takeaways

- **Per-Layer Embeddings.** Besides the usual input embedding, each token id
  indexes a second table holding one small vector *per layer*. The public
  implementation uses 256 dimensions per layer, 35 layers and a 262,144-token
  vocabulary, which comes to roughly 2.35B parameters. At each layer the
  hidden state is projected down, passed through the activation, multiplied
  elementwise with that layer's vector, projected back to model width,
  normalized and added to the residual. The lookup is keyed on the token
  alone, not on its context
- **The point is where the parameters live.** The table is addressed by
  token id, so which rows a sequence needs is known before any layer runs.
  That lets the table sit in CPU memory or fast storage and be fetched ahead.
  The documentation gives E2B as "over 5 billion parameters" with "an
  effective memory load of approximately 1.91 billion". The developer guide
  says only about 2B (E2B) and 4B (E4B) "core transformer weights" need to be
  on the accelerator
- **The quality claim is asserted, not measured.** The developer guide says
  PLE "dramatically improves model quality without increasing the high-speed
  memory footprint". Neither page gives a number, a baseline or an ablation
- **Carried forward**: the Gemma 4 technical report ([ARXIV-2607.02770](https://arxiv.org/abs/2607.02770)) says
  its E2B and E4B models "use per-layer embeddings as in Gemma 3n", 2.3B and
  4.5B effective out of 5B and 8B total

## Standing in the anthology

**Filed because a paper in the record cites it and the record could not
follow the reference.** [LIT-152](LIT-152.md)'s n-gram embedding section cites "Google
DeepMind. Gemma 3n model overview, 2025" twice. First it names embedding-based
memory as a way to add capacity. Second, and the more specific claim, it
says deterministic addressing allows host-memory offloading and
asynchronous prefetching.

**It is not the source of the n-gram embedding.** `#163` called PLE the
source for Qwen3.8-Flash-Next's n-gram embedding. The Qwen report is more
careful than that. It cites Gemma 3n among six sources for *unigram* lookup
memory, and a separate list for the *n-gram* generalization: N-Grammer,
Over-Tokenized Transformer, and Cheng et al.'s *Conditional memory via
scalable lookup*. The two designs also differ in shape. PLE reads a small
table at *every* layer, while Qwen reads one large n-gram table at *one*
layer. None of the n-gram papers is in the record yet.

**Carries no practice, and could not.** It has no measurements, so it is
adoption and not evidence ([DP-005](../../docs/design-principles.md#dp-5)). Its place in the record is on the
consensus side of [SOTA-tmp0fz4e](../practices.d/SOTA-tmp0fz4e.md), as one of the groups that shipped
embedding memory held off the accelerator.

Read — [NOTE-tmpsgjrr](../notes.d/NOTE-tmpsgjrr.md).
