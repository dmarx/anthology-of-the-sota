---
status: Active
consensus: emerging
consensus_note: >-
  The specific measurement is one group on one benchmark family, but it is a
  measurement of *other people's* systems by authors proposing a system in
  the same family, and it cites two independent benchmarks that had already
  found GraphRAG underperforming naive RAG. The shape is also not new to the
  record: `SOTA-210` reports the same failure with a different pair of
  metrics in a different field, which is why this is `emerging` rather than
  `unreplicated` — what recurs is the pattern, not the numbers.
title: 'When a retrieval change raises recall, measure relevance and the end-task metric before calling it an improvement'
version: 1
tags:
- in-context-learning
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-tmpghnyd
introduced_by:
- LIT-tmpghnyd
implementations: []
summary: >-
  Wu et al. (2026), [LIT-tmpghnyd](../literature.d/LIT-tmpghnyd.md) — across three published
  GraphRAG pipelines on G-Medical, graph expansion raises retrieval recall
  (GFM-RAG **84.3%** against vanilla RAG's 71.8%) and drops context relevance
  (**38.5%** against 62.9%). The wider context is noisier, and generation
  accuracy falls with it — a system that retrieves more of the right thing and
  much more of the wrong thing answers worse.
---

# SOTA-tmp7wp0k: When a retrieval change raises recall, measure relevance and the end-task metric before calling it an improvement

## Source

Wu, Xiang, Tang, Chen, Zhang and Su (2026),
[LIT-tmpghnyd](../literature.d/LIT-tmpghnyd.md) — read as [NOTE-tmp73iuw](../notes.d/NOTE-tmp73iuw.md).

## When this applies

You are changing what goes into a model's context — a retriever, an index, a
reranker, a graph expansion, a longer top-`k` — and you have a coverage
metric that went up.

## Do this

**Report the precision side and the end-task number in the same table as the
recall.** Retrieval quality is a pair, and improving one member is not
improving the pair. The specific measurement that motivates this, on
G-Medical:

| | evidence recall | context relevance |
|---|---|---|
| vanilla RAG | 71.8% | **62.9%** |
| GFM-RAG | **84.3%** | 38.5% |

Twelve and a half points of recall bought at twenty-four points of relevance,
and downstream QA accuracy falls. A context that contains the answer *and* a
great deal else is not a better context; the generator has to find the answer
in it.

**Treat "we retrieve more of the relevant material" as a hypothesis about the
end task, not a result.** The source's framing is that the field's graph
pipelines "expand the retrieval coverage at the cost of introducing excessive
irrelevant information, which ultimately harms the QA performance" — and it
cites two independent benchmarks that had already found advanced GraphRAG
underperforming naive RAG on real-world QA.

**Check how much of your index is doing nothing.** The same paper filters
extracted triples by schema frequency and drops the lowest 40%: accuracy goes
from 64.85% to 65.28%. The honest reading of that number is not that filtering
helps — 0.43 points is inside anyone's noise — but that **40% of the
constructed graph could be deleted at no cost**, which is a statement about
what the construction step is producing.

## Why `Active`

Because the measurement is against the authors' own interest. They are
proposing a GraphRAG system; the pilot study establishes that GraphRAG
systems, as a family, trade relevance for recall and lose end-task accuracy
doing it. Evidence that runs against the presenter's thesis is worth more than
evidence for it, and the two benchmark papers they cite got there
independently.

The instruction is also close to free: the relevance number is computed by the
same evaluation harness as the recall number.

## Conditions

**One benchmark family, one domain for the headline numbers.** G-Medical, with
three GraphRAG systems. The trade-off's *existence* has independent support in
the cited benchmarks; its size is this measurement.

**Relevance is itself a model-scored metric.** Context relevance here is
semantic alignment between question and retrieved passages, and evidence
recall is judged for whether the retrieved content contains what is needed.
Both are estimates, and a practice that says "measure relevance" inherits
whatever that estimator gets wrong.

**This does not say graph retrieval is a bad idea.** It says coverage is not
the objective. The source's own system claims to hold both — recall 90.42 and
relevance 82.64 on complex reasoning — and whether it does is a separate
question this practice does not rest on.

**Nothing here sets a threshold.** There is no "relevance must exceed `x`".
The instruction is to report the pair and the end-task number, so that a
reader can see a trade when one has been made.

## Related

[SOTA-210](../practices.d/SOTA-210.md) says to report pass@k as well as pass@1 after
post-training, because reinforcement learning raises one and lowers the other.
That is the same failure with a different pair of metrics in a different
field: an intervention moves two coupled measures in opposite directions, and
the literature reports the favourable one. Neither practice is evidence for
the other, and the recurrence is worth noticing — filed as an observation
here rather than as a general principle, because two instances are two
instances (`DP-009`).

[SOTA-269](../practices.d/SOTA-269.md) recommends keeping a knowledge base outside the weights.
This is about evaluating the thing you keep there, and is the record's first
document on that question.
