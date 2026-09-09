---
status: 'Active'
title: 'Orca: A Distributed Serving System for Transformer-Based Generative Models'
version: 1
tags:
- inference-optimization
date: '2026-09-09'
published: '2022-07-01'
# No arXiv preprint and no DOI USENIX exposes for it — OSDI proceedings are
# open access at this URL, which is the third preference under ADR-009 and
# the only one available.
url: 'https://www.usenix.org/conference/osdi22/presentation/yu'
first_author: 'Yu'
implementations:
- orca
keywords:
- 'inference-serving'
- 'scheduling'
- 'batching'
- 'throughput'
summary: >-
  Yu et al. (2022), OSDI '22. Introduces **iteration-level scheduling** — schedule at the granularity of one model iteration rather than one request — and **selective batching**. 36.9× throughput over FasterTransformer at equal latency on GPT-3 175B. The origin of what the field calls continuous batching.
---

# LIT-tmpe5an0: Orca: A Distributed Serving System for Transformer-Based Generative Models

Yu et al. (2022) — [OSDI '22](https://www.usenix.org/conference/osdi22/presentation/yu)

## Key takeaways

- **The problem is request-granularity scheduling.** Generation is
  multi-iteration: each forward pass emits one token per request. Existing
  servers fixed the batch for the whole request, so a request that finished
  early could not return to the client, and a newly arrived one waited for the
  entire batch to drain
- **Iteration-level scheduling** is the fix: the scheduler invokes the engine
  to run *a single iteration* on the batch, then re-decides. Finished
  requests leave, waiting requests join, every step
- **Selective batching** makes that compatible with a Transformer. Requests at
  different positions cannot be batched uniformly across every operation, so
  batching is applied only to the operations where it is valid
- **36.9× throughput improvement** over NVIDIA FasterTransformer at the same
  latency, on GPT-3 175B
- Designed for scale-out to models of hundreds of billions of parameters

## Standing in the anthology

The source of [SOTA-113](../practices.d/SOTA-113.md).

Filed in [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114) because it was missing. `SOTA-113` — use continuous batching for
inference — had been sourced to vLLM ([LIT-112](LIT-112.md)), which describes
iteration-level scheduling in its **background** section and cites this paper
for it. vLLM's contribution is PagedAttention; the batching this practice
recommends is Orca's.

"Continuous batching" is the name the field settled on and is not this
paper's term, which is why the citation drifted: the practice is filed under a
name that appears in neither paper.
