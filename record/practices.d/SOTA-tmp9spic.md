---
status: Proposed
promote_when: >-
  A second group fitting the parallel–parameter exchange rate, at a different
  architecture family or past `P = 8`, and reporting inference cost in memory
  and latency rather than FLOPs. What would not move it: a model that uses
  several parallel passes and reports better benchmarks — parallel sampling
  is everywhere and the content here is the *exchange rate* against
  parameters, which needs a fit and a matched-performance cost comparison to
  be a claim at all.
consensus: unreplicated
consensus_note: >-
  One group, one architecture family, and an unusually large amount of
  compute spent on the one question — six model sizes, two corpora, a 1T
  token run and 67 released checkpoints. Nobody outside Qwen has fitted the
  exchange rate, and the ingredients are old enough (prefix tuning, learned
  ensembling) that adoption would not be evidence for it.
title: 'Scale parallel computation with learnable input transforms, not parameters, when inference memory is the binding constraint'
version: 1
tags:
- inference-optimization
- model-architecture
- training-optimization
date: '2026-09-21'
source:
- LIT-tmpitbks
introduced_by:
- LIT-tmpitbks
implementations: []
explained_by:
- THEORY-tmprktkw
summary: >-
  Chen et al. (2025), [LIT-tmpitbks](../literature.d/LIT-tmpitbks.md) — run the same weights over `P`
  learnably-prefixed copies of the input and learn the aggregation. Loss falls
  as if the parameters had grown by `O(log P)`; a 1.6B model at `P = 8`
  matches a 4.4B one on code. At batch size 1 that costs **22× less added
  memory and 6× less added latency** than the parameter scaling it replaces —
  and `P`× the training FLOPs.
---

<!-- inactive-ok-file: THEORY-tmprktkw — Proposed, filed in this same
     contribution and named as `Proposed` in the sentence that cites it. The
     practice rests on the measured asymmetry, not on the account of it -->

<!-- inactive-ok-file: SOTA-tmp91kxm — Proposed, filed in this same
     contribution; it is the mitigation for this practice's training cost and
     is cited as such, which is a fact about what it recommends -->

# SOTA-tmp9spic: Scale parallel computation with learnable input transforms, not parameters, when inference memory is the binding constraint

## Source

Chen et al. (2025), [LIT-tmpitbks](../literature.d/LIT-tmpitbks.md) — [ARXIV-2505.10475](https://arxiv.org/abs/2505.10475) — read as
[NOTE-tmp5l9o0](../notes.d/NOTE-tmp5l9o0.md).

## What to do

Prepend `P` different **learned prefixes** to the input — equivalently, keep
`P` distinct KV-caches — run the backbone on all `P` in parallel, and combine
the `P` output distributions with a **learned** dynamic weighted average from
a small MLP. Train with the streams switched on; serve with them switched on.

Roughly **0.2% additional parameters per stream**. Nothing about the
backbone, the objective, the data or the tokenizer changes.

**Do not over-design the transformation.** The paper's pivot experiments try
several input transformations and aggregation rules — including LoRA-style
factorizations — and find they "minimally affect model performance; the
significant factor is the number of computations". Pick a cheap one and spend
the effort on choosing `P`.

## What it buys, and the exchange rate

Fitted across 0.5B–4.4B non-embedding parameters and `P = 1…8` on 42B tokens:
**`P` streams behave like `O(log P)` more parameters**, with the fitted
coefficient **0.39** on Stack-V2-Python and **0.33** on the Pile. Larger
models gain more — the loss contours flatten as parameters grow.

Downstream, and the asymmetry is the interesting part: a 1.6B model at
`P = 8` matches the **4.4B** baseline on coding (39.1 against 39.2) and only
the **2.8B** baseline on general tasks (55.7 against 55.2).
[THEORY-tmprktkw](../theory.d/THEORY-tmprktkw.md) is the account of why, and is `Proposed`.

## Why "when inference memory is the binding constraint" is in the title

Because that is the condition under which this wins, and the paper measures
where it stops winning rather than quoting its best number alone.

At **batch size 1**, a 1.6B model at `P = 8` costs **22× less added memory**
and **6× less added latency** than the parameter scaling that reaches the same
performance. The memory result is structural: the extra parameters are
negligible and the only real growth is the KV cache, which is `P`× a quantity
that is already far smaller than the weights. The latency result is
conditional: decoding at small batch size is memory-bound, so the added
arithmetic is close to free — and **as batch size rises, decoding becomes
compute-bound and the advantage narrows**. It survives to batch size 8 and the
paper does not claim beyond that.

So the target is small-batch, memory-constrained serving — the paper says
edge devices explicitly — and a high-throughput server batching hundreds of
requests is the case where this reasoning does not apply.

**A methodological note worth taking on its own.** The cost analysis
deliberately uses memory and latency rather than FLOPs, on the grounds that
decode is memory-bound and FLOPs mis-rank it — flash attention spends more
FLOPs for less latency. Any comparison of this kind that is denominated in
FLOPs is measuring the wrong thing; this one would have looked much worse and
been much less true.

## Conditions

**`P`× the training FLOPs.** This is the cost and it is not small. The
mitigation is [SOTA-tmp91kxm](SOTA-tmp91kxm.md) — add the streams in a short final stage —
and it is a mitigation rather than an answer.

**The law is fitted, not derived.** The theoretical result says the parameter
multiplier depends on the *diversity* between streams; `log P` was chosen
because the measured gains from 1→2, 2→4 and 4→8 were about equal, and the
diversity term is never measured. The theory permits anything from logarithmic
to a power law depending on that term. What is established is a fit over the
range tested.

**`P = 8` is where the evidence stops**, and the fitted shape is the one that
most flatters an extrapolation nobody ran. Whether there is a ceiling is
named as open by the authors.

**One group, one architecture family.** Qwen-2.5 dense throughout. The claim
of applicability to "any model structure" is a claim, not a result — the
mixture-of-experts combination the paper calls promising is untested, and the
record's [SOTA-150](SOTA-150.md) is the opposite trade (parameter-heavy,
latency-friendly) rather than an independent confirmation.

**Inference cost is modelled rather than timed**, with the `llm-analysis`
framework.

**The data axis is held fixed** at 42B tokens without repetition for the fit.
A footnote reports that `P` appeared to reduce overfitting under data
repetition, with no experiment behind it.

## Known implementations

- 67 released checkpoints and training code from the authors. No third-party
  adoption known to this record.
