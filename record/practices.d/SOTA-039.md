---
number: 39
status: Superseded
superseded_by: SOTA-140
status_note: warmup-stable-decay matches it and leaves the token budget open; every report since 2024 in the record uses a stable-then-decay schedule
title: 'single cycle of cosine decay is sufficient lr schedule'
version: 1
tags:
- model-architecture
date: '2026-08-24'
source:
- LIT-035
# CORRECTED. Was `introduced_by: LIT-035`, which passed only because it is
# also the source. GPT-3 reports a recipe and runs no schedule against it.
# The single cosine cycle is older: SGDR (Loshchilov and Hutter 2016) defined
# the cosine anneal and, in its own §4.2, found that one cycle over the whole
# 200-epoch budget (T_0 = 200, no restart) gave the best final test error of
# the schedules it ran, while restarts won only on anytime performance. Bag of
# Tricks (He et al. 2018, 1812.01187, not held) later recommends the
# single-cycle "simplified version" outright and credits it to SGDR.
# inactive-ok: LIT-042 — the origin, Superseded; the chain it opens is why it is kept
introduced_by:
- LIT-042
summary: >-
  Brown et al. (2020), [LIT-035](../literature.d/LIT-035.md) — [ARXIV-2005.14165](https://arxiv.org/abs/2005.14165).
---

# SOTA-039: single cycle of cosine decay is sufficient lr schedule

## Source

Brown et al. (2020), [LIT-035](../literature.d/LIT-035.md) — [ARXIV-2005.14165](https://arxiv.org/abs/2005.14165).

## Why this is superseded

<!-- inactive-ok: LIT-042 — the retired warm-restarts paper this practice itself retired -->
A single cosine cycle retired warm restarts ([LIT-042](../literature.d/LIT-042.md)) by showing they were not
needed at scale, and was the default from GPT-3 through 2023. It ties the
result to a token budget fixed in advance, so every duration is its own run
and no intermediate checkpoint is a finished model. Warmup-stable-decay
([SOTA-140](SOTA-140.md)) matches or beats it while removing that constraint, and by 2025
every frontier report in the record uses a stable-then-decay shape. The
claim here was right that one cycle beats several; what moved is the shape
of the one cycle.

What [LIT-035](../literature.d/LIT-035.md) reports is the recipe, not a comparison. All eight GPT-3 models,
125M to 175B, were trained with a linear warmup over the first 375 million
tokens and a single cosine decay to 10% of the peak rate over 260 billion
tokens, held at 10% for the rest of the 300 billion. No other schedule is run
against it, so the paper's evidence for "sufficient" is that the one cycle
trained every size; that it showed warm restarts unnecessary is the record's
reading, not a result in the paper.

<!-- inactive-ok: LIT-042 — the origin of the single cycle, Superseded as a recommendation of restarts -->
The single cycle comes from the paper it is usually set against. LIT-042
introduced cosine annealing as the schedule inside each restart cycle, and
on WRN-28-10 for CIFAR-10 and CIFAR-100 it also ran the case with no restart
at all, one cosine anneal over the full 200 epochs. That run "shows the best
results", which the authors read as the standard step schedule being
suboptimal; it also had the worst anytime performance until the last epochs,
and anytime performance is what the restarts were for. So the evidence that
one cycle suffices for the final model predates GPT-3 by four years and sits
in the warm-restarts paper itself; what GPT-3 added is that the one cycle
trained every model size up to 175B.
