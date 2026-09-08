---
status: Proposed
title: 'The recommendations are scoped by kind of claim, and domain is a separate axis'
version: 1
tags:
- ontology
date: '2026-09-08'
---

# ADR-tmpqq6xc: The recommendations are scoped by kind of claim, and domain is a separate axis

## Context

[ADR-003](ADR-003.md) gave the `SOTA` scheme seven topics and the `LIT` scheme those seven
plus five more, on the ground that "the reading list covers ground the
practice registry does not." [DP-008](../../docs/design-principles.md#dp-8) then read that arrangement back as a scope
statement: **the recommendations are scoped to language-model training by
construction**, so a vision paper can be a note and cannot be a
recommendation — "not on judgement, not on evidence, but because there is no
category for it to take."

Three things have since gone wrong with that.

**The record already contradicts it.** [SOTA-113](../practices.d/SOTA-113.md) (continuous batching) and
[SOTA-115](../practices.d/SOTA-115.md) (prefill/decode overlap) are `Active` recommendations about
*serving*, filed under `systems-optimization`. So are the record's
quantization practices. "Scoped to language-model training" was never true of
the practices the record actually holds; it was true of the sentence in
[DP-008](../../docs/design-principles.md#dp-8).

**The bundling was wrong in the other direction too.** [ADR-003](ADR-003.md) justified all
five extra `LIT` topics with one sentence, and it holds for
`generative-modeling` and `vision-and-graphics` but not for
`adaptation-and-tuning` or `inference-optimization` — the record files
fine-tuning, preference-training and quantization practices under the seven,
several of each. LoRA sat in this corpus for a year sourcing nothing because
its tag looked like a scope boundary and was not one.

**And the cost is the thing the anthology exists to avoid.** A scope drawn by
domain makes the record blind to work whose *transferable* content is exactly
the kind of claim it collects. EDM's contribution is a preconditioning scheme,
a noise-level sampling distribution and a loss weighting. Segment Anything's
is a model-in-the-loop annotation bootstrap. Those are a
`training-optimization` claim and a `data-pipeline` claim that happen to have
been discovered in image models. Declining them keeps the record ignorant of
its own subject.

## Decision

**Scope the recommendations by the kind of claim, not by the domain it was
discovered in.** A practice belongs here if it is an instruction about how to
build, train, adapt or serve a model that one of the seven topics can express.
Where the work came from is not the test.

The seven topics stay exactly as [ADR-003](ADR-003.md) set them. They are kinds of claim,
and they were never the problem.

**Add an orthogonal `domain:` axis** — a scheme-owned vocabulary in
`record/practices.d/domain.yaml`, declared on the `SOTA` scheme, saying what
the practice is known to apply to.

    unassessed | domain-general | language-modeling | vision |
    generative-modeling | multimodal

**Many-valued**, where `consensus:` is single, because the two facts have
different shapes. Consensus is a scalar: one position on one axis. A domain
reading is a *set* — where the practice has been shown to hold — and it
accumulates as evidence arrives, which is `source:`'s shape under [ADR-010](ADR-010.md)
rather than `consensus:`'s. Forcing one value makes the interesting cases
unstatable: LoRA is established in language modelling *and* in diffusion, and
naming either underclaims while `domain-general` overclaims.

`domain-general` is the load-bearing value and the one of a different kind
from the rest. The others report where evidence exists; this one says the
mechanism does not depend on modality at all, which is not the union of the
list and cannot be reached by enumerating it — nobody tested Adam in six
fields, it simply does not care what produced the gradients. It is listed
alone, as is `unassessed`, and the lint cannot check either: both are
coherence rules about what a set of values would mean together, and luria's
vocabularies have no mutual-exclusion mechanism. Written in `domain.yaml`
where the values are, as a rule for a reader rather than a guard.

`unassessed` is the default and most of the corpus will carry it, honestly —
a domain reading is a judgement and it needs grounds.

[DP-008](../../docs/design-principles.md#dp-8)'s principle stands unchanged; its worked example is amended, because
the example described a scope this decision replaces.

## Alternatives considered

- **Widen `primary_topic` — add `generative-modeling` and
  `vision-and-graphics` to the practice seven.** The obvious move, and it
  defeats the purpose. `primary_topic` is `exactly-one` and it is the
  browsing axis: a diffusion preconditioning practice tagged
  `generative-modeling` renders on the generative page and *not* beside the
  LLM normalization practices it is a sibling of. Widening the topic list
  gives cross-domain work its own page, which is the opposite of
  cross-pollination — a topic spent naming the domain is a topic not spent
  naming the claim. Under the decision above, the same practice is
  `training-optimization` + `domain: generative-modeling`, and it lands
  exactly where someone would trip over it.
- **Merge the two vocabularies.** [ADR-003](ADR-003.md) rejected this and was right: it
  "puts a diffusion sampler paper under `training-optimization` or
  `model-architecture` and makes both pages worse." Nothing here disturbs
  that. The `LIT` scheme keeps its twelve topics; what changes is that a
  note's topic no longer implies anything about whether a practice can be
  drawn from it.
- **Add a `phase:` axis too — pretraining, post-training, inference.**
  Deferred, on [DP-008](../../docs/design-principles.md#dp-8)'s own corollary that "a category added to admit a
  single document is how a scope stops being one." Inference practices
  already have somewhere to go: [SOTA-113](../practices.d/SOTA-113.md) and [SOTA-115](../practices.d/SOTA-115.md) have been sitting
  comfortably under `systems-optimization`. If a claim arrives that is
  inference-shaped and genuinely homeless — a sampler schedule is the likely
  first — that is the moment to decide, with two documents in hand instead
  of none.
- **Say nothing and let practice drift.** What has been happening. Two
  serving practices already sit outside the written scope and nobody
  noticed, which is precisely [DP-008](../../docs/design-principles.md#dp-8)'s warning about vocabularies working in
  the dark.

## When one practice has different consensus in different domains

The axis makes this askable for the first time, so it needs an answer.

Most of the time it does not arise, because **`domain:` scopes the
consensus**. `consensus: universal` with `domain: [language-modeling]` reads
"universal within language modelling", which is what is meant. A practice
established in one domain and untested elsewhere names one domain, and the
consensus value is about that domain. Nothing further is needed.

It bites only when a practice lists two domains and the field has converged
in one and not the other. The test then is whether **the recommendation
differs, or only its uptake**:

- **The recommendation differs** — different conditions, different
  parameters, a different trade — then these were always two practices and
  should be split into separate codes, linked with `compared_against` or
  `extends`. That is the ordinary reason to split anything, it holds
  regardless of consensus, and each code then carries its own coherent
  status, consensus and domain.
- **Only the uptake differs** — the instruction is word-for-word the same
  and one community has adopted it and another has not — then **do not
  split**. One claim across two documents is the failure this record has
  already paid for twice:
  <!-- inactive-ok-block: LIT-006, LIT-042, LIT-029 — the retired duplicates, named as the evidence for this rule; being retired is the fact being cited -->
  [LIT-006](../literature.d/LIT-006.md) and [LIT-042](../literature.d/LIT-042.md) held one paper as both `Active`
  and `Superseded`, and [LIT-029](../literature.d/LIT-029.md) and [LIT-114](../literature.d/LIT-114.md) held one paper with two readings,
  one of them fabricated, which fed a conflated practice for a year. Bodies
  that say the same thing drift, and nothing notices. `status:` would have to
  duplicate too, and that one is plainly wrong: whether *this record*
  believes a practice works is an editorial position and does not vary by
  domain.

For that residual case the correct fix is for `consensus:` itself to become
per-domain —

    consensus:
      language-modeling: universal
      generative-modeling: emerging

— which is a luria feature (a map-valued vocabulary field; the field
mechanism holds scalars and lists today) and not something to approximate
with duplicate documents. Deferred until the record holds an actual instance,
on [DP-008](../../docs/design-principles.md#dp-8)'s corollary: build the category when there is a document that needs
it, not in anticipation. Until then a practice whose consensus genuinely
splits says so in its body, and the axis carries the reading for the domains
it lists.

## Consequences

The bar for a new practice is now a question about the claim — *is this an
instruction one of the seven can express?* — rather than a question about the
paper's field. That is a wider gate, deliberately.

The `domain:` backfill is a judgement per practice and will be partial for a
long time. That is the same trade `consensus:` made and it is the honest one:
a column filled by inference is worse than a column that admits what has not
been looked at.

Issue [#85](https://github.com/dmarx/anthology-of-the-sota/issues/85)'s remaining surface changes shape. Twenty-three inherited notes were
set aside as out of scope by construction; they are now ordinary unread notes,
and the ones with a transferable claim — EDM, Segment Anything, Latent
Diffusion, the distillation pair — are the most interesting reading left in
the corpus rather than the least.

The risk this accepts: the record can become a directionless list of
everything. The guard is that the seven topics did not move. A claim still has
to be an instruction about building, training, adapting or serving a model,
and still has to take exactly one of seven categories, and still has to name a
paper that produced evidence about it.
