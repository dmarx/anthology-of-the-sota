---
status: Proposed
promote_when: >-
  A second group reporting a controlled comparison of best-fit packing against
  concatenation, or a frontier pretraining report that names the packing
  method it used and why. Adoption alone will not do it: the two reports that
  cite this cite it in passing, and neither says whether it changed anything
  for them.
consensus: unreplicated
consensus_note: >-
  One group, one broad study. Two frontier reports cite it (LIT-130, LIT-139)
  without reporting a comparison of their own, which is where nearly every
  data-plumbing decision sits — done once, never measured again.
title: 'Pack training documents by best fit instead of concatenating and splitting'
version: 1
tags:
- data-pipeline
date: '2026-09-07'
published: '2024-04-01'
source:
- LIT-tmp66u4l
summary: >-
  Ding et al. (2024), [LIT-tmp66u4l](../literature.d/LIT-tmp66u4l.md) — concatenate-then-split truncates
  documents that would have fit, and the model then learns to continue text
  whose beginning it never saw. Treating the grouping as bin packing removes
  those truncations at the same efficiency, no padding added: +4.7% reading
  comprehension, +16.8% context following, +9.2% program synthesis, and up to
  58.3% less closed-domain hallucination.
---

# SOTA-tmpcsora: Pack training documents by best fit instead of concatenating and splitting

## Source

Ding et al. (2024), [LIT-tmp66u4l](../literature.d/LIT-tmp66u4l.md) — Fewer Truncations Improve Language Modeling.

The universal default is to concatenate documents and split the stream at the
sequence length. It wastes no tokens on padding, which is why everyone does
it, and it fragments documents that would have fitted whole. The fragments
are then trained on as if they were complete: the model repeatedly sees text
whose beginning it never saw, and learns to continue it.

Best-fit Packing treats the grouping as what it is — a bin-packing problem —
and solves it with a Best-Fit-Decreasing approximation, segmenting only
documents genuinely longer than the sequence length. Because it minimises the
number of sequences it introduces no padding, so **the efficiency argument
for concatenation is not being traded away**. That is what makes this cheap
rather than a quality-for-throughput exchange.

At 7B–13B, sequence lengths 2k–8k, on both natural-language and code corpora,
across 22 tasks: +4.7% relative on reading comprehension, +16.8% on context
following, +9.2% on program synthesis. And closed-domain hallucination falls
by up to **58.3%**, which is the number that explains the rest — truncation
removes the grounding a fact depends on, so a model trained on fragments
learns to assert things its context does not support.

Conditions: one group, and the comparison is theirs. The gains are relative
and concentrated in tasks that depend on complete context, so a workload
dominated by short documents has less to gain — the effect is a function of
how much of your corpus exceeds the sequence length. The cost is a packing
pass over the corpus, which is offline and one-off but not free at scale.

## Why `Proposed` rather than Active

The evidence is good and broad, and there is exactly one study. Olmo 3
([LIT-130](../literature.d/LIT-130.md)) and DeepSeek-V4 ([LIT-139](../literature.d/LIT-139.md)) both cite this work, which is adoption
rather than replication — neither reports what it did for them.

That is the ordinary condition of data-plumbing decisions, and the reason to
file this at all. The choice is made once in a dataloader, looks like an
implementation detail with an obviously correct answer, and is never measured
again. A practice that says "this one was measured, and the default lost" is
worth more here than in a corner of the field where people run ablations by
habit.
