---
status: Active
title: 'DataComp-LM: In search of the next generation of training sets for language models'
version: 1
tags:
- data-pipeline
- analysis-and-evaluation
date: '2026-09-17'
published: '2024-06-17'
arxiv: '2406.11794'
first_author: 'Li'
keywords:
- 'data-curation'
- 'benchmark'
- 'model-based-filtering'
- 'pretraining-corpus'
implementations:
- 'DCLM-Baseline'
summary: >-
  Li et al. (2024), [ARXIV-2406.11794](https://arxiv.org/abs/2406.11794). A controlled testbed for data curation — a
  fixed 240T-token corpus, fixed training recipes at 412M–7B, and 53
  evaluations — whose baseline finding is that model-based filtering is what
  makes a high-quality training set. The position two documents in this record
  already argue with.
---

# LIT-tmpwhgmr: DataComp-LM: In search of the next generation of training sets for language models

Li et al. (2024) — [ARXIV-2406.11794](https://arxiv.org/abs/2406.11794)

## Key takeaways

- **A benchmark whose unit of submission is a dataset, not a model.** The
  corpus (240T tokens from Common Crawl), the training recipe (OpenLM) and
  the 53 downstream evaluations are held fixed at scales from 412M to 7B, so
  deduplication, filtering and mixing strategies can be compared to each other
  rather than to whatever else changed in somebody's training run
- **The baseline result is the influential claim: model-based filtering is
  key.** DCLM-Baseline trains a 7B model to **64% 5-shot MMLU on 2.6T
  tokens** — 6.6 points over MAP-Neo with 40% less compute, and comparable to
  Mistral-7B-v0.3 and Llama 3 8B on MMLU with 6.6× less compute than the
  latter
- What that established, and what it did not: the experiment is controlled
  for everything *except* the token horizon, which it fixes at 2.6T

## Standing in the anthology

**Carries no practice, deliberately.** Filed under [ADR-032](../decisions.d/ADR-032.md), which admits
benchmarks and dataset reports for what they establish rather than what they
recommend. There is a recommendation in here — filter aggressively with a
learned classifier — and this record already holds it in its qualified form
as [SOTA-170](../practices.d/SOTA-170.md), which says the sign of that trade depends on the token horizon
and reports the crossover between 1T and 15T.

That practice cites DCLM as **the position it argues against**, which under
[ADR-010](../decisions.d/ADR-010.md) keeps it in the body rather than in `source:`; contrast is not
support. Until now the record made that argument against a paper it did not
hold, which is the gap this filing closes. [LIT-184](LIT-184.md) (FineWeb) is filed in the
same role.

Unread — no NOTE. Filed from the abstract and the benchmark's stated design,
which is what an argued-against position needs to be checkable; [ADR-025](../decisions.d/ADR-025.md) makes
the absence of a note mean exactly that, and claiming a reading here would be
false.
