---
status: Read
paper: LIT-052
title: 'Scale Efficiently'
version: 1
tags:
- model-architecture
date: '2026-09-09'
summary: >-
  Model shape, not only model size, determines downstream fine-tuning quality — and the widely adopted T5-Base and T5-Large configurations are Pareto-inefficient. Read in full for [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114) after its LIT note was found to describe a different paper.
---

# NOTE-tay: Scale Efficiently

## Contribution

Kaplan et al. established scaling laws for Transformers on **upstream
pretraining loss**, and found that shape — depth, width, head count — has
"minimal effects within a wide range" once parameter count is fixed. This
paper asks whether those findings survive the pretrain-finetune paradigm,
and finds that one of them does not: measured on **downstream fine-tuning
quality**, shape matters, and depth matters most. It converts that into a
scaling protocol (DeepNarrow) and shows the canonical T5 sizes are
Pareto-inefficient under it. Over 100 pretrained T5 configurations released.

## Key insight

The scaling law you fit depends on the quantity you measure, and upstream
loss is not the quantity anyone actually cares about. Two models with equal
parameter counts and equal pretraining loss can differ substantially after
fine-tuning, so a shape conclusion drawn from the loss curve does not
transfer to the task. Once you measure the thing you want, depth stops being
interchangeable with width — and the reason it stops is not statistical but
physical: depth is serial, so its advantage is bought with a parallelism
cost that the loss curve never showed you.

## Assumptions

Not a theoretical paper; there are no formal assumptions to discharge. The
empirical setting is the thing to carry, because it is narrower than the
conclusion sounds:

- **Encoder-decoder T5**, pretrained on C4, evaluated on GLUE, SuperGLUE and
  SQuAD. Not decoder-only, not a modern pretraining mix.
- **Fine-tuning is the downstream protocol.** Nothing here is measured
  through in-context learning or post-training, which is how the record's
  contemporary practices are evaluated.
- **A parallelism ceiling of 64 workers with model parallelism 32.** The
  paper states its protocol holds "within a certain hardware limit" and puts
  extreme width-parallel scaling explicitly out of scope.
- Vision Transformers on few-shot image recognition are the one cross-domain
  check.

## Key results

No theorems. The results are a Pareto frontier and a table, and the exact
figures are the useful part.

- **Model shape matters downstream.** Configurations with equal parameter
  counts and comparable upstream loss separate on downstream quality — the
  finding that contradicts the received reading of Kaplan et al.
- **Scaling protocols differ by compute region.** A strategy validated at
  small scale need not transfer upward, which the paper offers as a caution
  against its own generalisation.
- **DeepNarrow, Table 4.** Increase depth preferentially before any uniform
  scaling of other dimensions:

  | model | vs. baseline | params | FLOPs | outcome |
  |---|---|---|--:|--:|---|
  | Small 16L | T5-Base | 134M vs 223M | 63.1% | comparable quality, 40% faster |
  | Small 24L | T5-Base | — | 87% | — |
  | Base 36L | T5-Large | 16% saving | lower | outperforms |
  | Large 36L | T5-XL | 37% of params | — | outperforms on all three tasks |
  | XL 32L | T5-XXL | ~33% | ~44% | outperforms, ~3× faster |

- **The Pareto frontier tapers.** Depth-scaling a small model is
  Pareto-efficient until it is not; after that the base model takes over,
  then the large. The strategy has a range, not a limit.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Model shape affects downstream fine-tuning quality independently of model size | strong | the paper's central experimental program, across three benchmark suites |
| C2 | Depth is the shape axis with the largest effect on the Pareto frontier | strong | Table 4 and the frontier plots, at five size classes |
| C3 | T5-Base and T5-Large are Pareto-inefficient configurations | strong | direct comparison against DeepNarrow alternatives at lower cost |
| C4 | Scaling protocols behave differently in different compute regions | moderate | observed across their size range; offered as caution rather than measured law |
| C5 | DeepNarrow transfers outside language | weak | one cross-domain check, ViT few-shot image recognition, small models only |
| C6 | The protocol holds only within a hardware parallelism limit | moderate | argued from depth's seriality and their own 64-worker ceiling; the limit is not located |

## Concepts

- **DeepNarrow** — a scaling strategy that increases depth preferentially,
  before any uniform scaling across other dimensions. Named here; the
  authors' concurrent Charformer calls the same idea *Tall*.
- **Compute region** — a band of the compute budget within which one scaling
  protocol is Pareto-efficient. The paper's claim is that the bands have
  different protocols, not merely different constants.
- **Pareto-efficient (of a configuration)** — not dominated on *at least one*
  compute axis (parameters, FLOPs, steps/second) for *at least one*
  downstream task. Weaker than the usual reading, and the paper says so:
  which compute dimension matters is left to the practitioner.

## Connections

Directly a response to Kaplan et al. ([LIT-028](../literature.d/LIT-028.md)) — it takes that paper's
method and changes the measured quantity from upstream loss to downstream
task quality, and reverses its shape conclusion in doing so. It also cites
Hernandez et al. on transfer scaling as the other open thread.

The record's own second arrival at the same finding is Falcon-H1-Tiny's
90M ablation, from a different group and a different architecture family,
which chose 24–27 layers over both shallower and 50-layer options — and
rejected the deeper one on throughput, the same trade named here.

## Recommendations

- **R1** — When scaling a Transformer at a fixed parameter budget, increase
  depth before width. *Topic:* model shape. *Status:* experimental.
  *Strength:* moderate. *Applies when:* quality is measured downstream and
  the available parallelism is not the binding constraint.
- **R2** — Do not choose a configuration by upstream loss if you will judge
  the model downstream. *Topic:* evaluation. *Status:* standard.
  *Strength:* strong. *Applies when:* always, in the pretrain-finetune
  paradigm this paper studies.
- **R3** — Report parameters, FLOPs and wall-clock together. *Topic:*
  reporting. *Status:* standard. *Strength:* strong. *Applies when:* a
  design choice trades between them, which depth-versus-width always does.
- **R4** — Treat the canonical size names (base, large, XL) as conventions
  rather than efficient points. *Topic:* model shape. *Status:*
  experimental. *Strength:* moderate. *Applies when:* the family's shapes
  were inherited rather than swept.

## Bearing on the record

<!-- inactive-ok-block: SOTA-190, SOTA-125 — both Proposed; this paragraph is about what the reading produced and what it corroborates -->
**Produces [SOTA-190](../practices.d/SOTA-190.md)** (increase depth before any other dimension), filed from
R1, `Proposed`, `compared_against: SOTA-125`.

**Contradicted five practices that cited it.** [SOTA-064](../practices.d/SOTA-064.md), [SOTA-065](../practices.d/SOTA-065.md), [SOTA-066](../practices.d/SOTA-066.md) and
<!-- inactive-ok-block: SOTA-064, SOTA-065, SOTA-066, SOTA-067, SOTA-068 — all retired in #112; this paragraph is the record of why -->
[SOTA-067](../practices.d/SOTA-067.md) are `Rejected` and [SOTA-068](../practices.d/SOTA-068.md) `Superseded` as a result. They described
warmup length, layer-norm initialisation, gradient clipping and an early
instability window. This paper contains the strings `warmup`, `gradient
clip`, `layer norm` and `instabilit` **zero times each**. The
[LIT-052](../literature.d/LIT-052.md) takeaways they were written from belonged to some other paper.

<!-- inactive-ok: SOTA-190 — Proposed, and this paragraph says why -->
**C6 is the reason [SOTA-190](../practices.d/SOTA-190.md) is `Proposed` rather than `Active`.** The
promotion condition asks for a depth comparison at a scale where model
parallelism binds, reporting wall-clock — which is exactly the measurement
this paper declines to make.

## Limitations

- The parallelism ceiling is stated but never located. "Within a certain
  hardware limit" is the paper's own phrase, and it does not say where.
- Encoder-decoder T5 on fine-tuning benchmarks is two architectural
  generations from what the record's practices assume.
- C4 (compute regions differ) is asserted from observation across their own
  size range and is the claim most likely to be an artefact of that range.
- The ViT check is small-model only, so C5 is barely evidence.

## Open questions

<!-- inactive-ok-block: SOTA-190 — Proposed; named as the practice this open question would promote -->
- Where is the parallelism limit? A depth-versus-width comparison reporting
  wall-clock under model parallelism at frontier scale would settle both
  C6 and [SOTA-190](../practices.d/SOTA-190.md)'s promotion.
- Does the shape finding survive decoder-only pretraining evaluated by
  in-context learning rather than fine-tuning? Nothing in the record answers
  this.
- Falcon-H1-Tiny reached the same conclusion at 90M and rejected 50 layers on
  throughput. Whether the two are the same finding or two different ones
  that happen to agree is not established by either.
