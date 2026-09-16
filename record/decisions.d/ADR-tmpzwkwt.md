---
status: Proposed
title: 'An unbound relation is one of four things, and only one of them is a retag'
version: 1
tags:
- record
- taxonomy
date: '2026-09-15'
summary: >-
  The unbound-lineage report had 38 relations and 16 lines. Reading all of
  them: 15 documents were plainly mis-filed and are retagged, two sibling
  links were analogies rather than comparisons and are removed, and the
  remaining 24 are two structural facts about the vocabulary — that
  `analysis-and-evaluation` is a kind rather than a subject and will unbind
  every lineage it touches, and that the record has no relation for "this is
  the domain-specific instance of that". Neither is fixed by retagging, and
  retagging to clear them is the move luria.yaml already warns against.
---

# ADR-tmpzwkwt: An unbound relation is one of four things, and only one of them is a retag

## Context

Both chains in this record assert an invariant on `primary_topic`: two
documents joined by succession or rivalry are about the same kind of thing,
and a topic in common is what says so. `docs/reports/unbound-lineage.md`
reports where the assertion was made and nothing says what it means. It had
**38 unbound relations and 16 unbound lines**, and had never been read
through.

The report's own preamble gives the prior — *"usually a sign the vocabulary is
short a word rather than that the relation is wrong"* — and `luria.yaml`
records the failure mode beside the `practice` chain: [#101](https://github.com/dmarx/anthology-of-the-sota/issues/101) bound the
[SOTA-085](../practices.d/SOTA-085.md) / [SOTA-161](../practices.d/SOTA-161.md) pair by giving both a `flash-attention` secondary tag,
which **satisfied the check rather than answering it**. Any pass over this
report has to be able to leave a finding standing.

Reading all 38: they are four different things.

## Decision

**1. Fifteen documents were mis-filed on their own terms. Retagged.**

Not to bind an edge — each is wrong read alone, and would still be wrong if
the relation did not exist.

- **Eight positional-encoding papers** — [LIT-045](../literature.d/LIT-045.md) (RoPE), [LIT-048](../literature.d/LIT-048.md) (ALiBi),
  [LIT-192](../literature.d/LIT-192.md) (Position Interpolation), [LIT-193](../literature.d/LIT-193.md) (YaRN), [LIT-207](../literature.d/LIT-207.md), [LIT-208](../literature.d/LIT-208.md),
  [LIT-209](../literature.d/LIT-209.md), [LIT-210](../literature.d/LIT-210.md) — split between `model-architecture` and
  `attention-techniques`, because when they were filed there was no third
  option. `representation-and-encoding` names *positional encoding* in its own
  blurb, and *"the frequency or basis choices that go with them"*, which is
  literally YaRN's subject and [LIT-210](../literature.d/LIT-210.md)'s. [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114) added that topic and nobody
  went back. All eight now carry it, and [NOTE-028](../notes.d/NOTE-028.md) follows its paper.
- **[LIT-211](../literature.d/LIT-211.md)**, *Evolution Strategies at Scale: LLM Fine-Tuning Beyond
  Reinforcement Learning*, carried `training-optimization`. It is about
  fine-tuning; [SOTA-154](../practices.d/SOTA-154.md), the practice it introduced, and five of its six
  descendants already carry `adaptation-and-tuning`.
- **[SOTA-092](../practices.d/SOTA-092.md), [SOTA-093](../practices.d/SOTA-093.md), [SOTA-094](../practices.d/SOTA-094.md)** — three claims about batch size from one
  model report, carrying `model-architecture` because a model report is where
  they were found rather than what they are about. `training-optimization`
  names batch size.
- **[SOTA-060](../practices.d/SOTA-060.md)**, an initialization rule for stability, carrying
  `distributed-optimization` because its source is a Megatron paper.
- **[SOTA-098](../practices.d/SOTA-098.md)** and **[SOTA-099](../practices.d/SOTA-099.md)**, both about detecting instability — [SOTA-099](../practices.d/SOTA-099.md)'s
  title says so — carrying `training-optimization` while the practices they
  are compared against, one of them from the same paper, carry
  `model-stability`.

This is the largest category and it is a *filing* error, not a vocabulary
one: eleven of the fifteen were filed under the topic of the **document they
were found in** rather than the topic of the **claim they make**, which is
exactly the distinction [ADR-026](ADR-026.md)'s filing rule draws.

**2. Two sibling links were analogies, not comparisons. Removed.**

[ADR-011](ADR-011.md) defines `compared_against:` as *this work evaluates itself against
that one*. Nobody compared [SOTA-045](../practices.d/SOTA-045.md) (profile the input pipeline separately)
with [SOTA-091](../practices.d/SOTA-091.md) (profile memory access patterns), or [SOTA-047](../practices.d/SOTA-047.md) (overlap
communication with the backward pass) with [SOTA-079](../practices.d/SOTA-079.md) (pre-fetch the next
batch). Different papers, different subsystems; the shared thing is a word in
the title and a shape of idea. Both links are removed, with the reason left in
the frontmatter of all four practices.

This is the case the report's preamble calls unusual, and it is worth naming
that it exists: an unbound relation is sometimes evidence that the relation
was asserted too cheaply.

**3. Seven relations cross because `analysis-and-evaluation` is a kind, not a
subject. Left standing.**

[LIT-127](../literature.d/LIT-127.md) and [LIT-211](../literature.d/LIT-211.md) against [LIT-230](../literature.d/LIT-230.md), [LIT-233](../literature.d/LIT-233.md) and [LIT-235](../literature.d/LIT-235.md); [LIT-235](../literature.d/LIT-235.md) against
[LIT-238](../literature.d/LIT-238.md). Every one joins a paper that *does* something to a paper that
*measures* it. They are about the same thing at different altitudes, which is
precisely what the relation asserts and what the invariant cannot see.

Twelve of the thirteen topics name a subject. `analysis-and-evaluation` names
a kind of work — *"how to find out whether something worked… theory,
interpretability and debugging belong here too"* — and it will unbind a
lineage every time a line grows an analysis paper. This is not a defect in
those six documents' tags: [LIT-230](../literature.d/LIT-230.md)'s body argues its own filing explicitly,
and the argument is right.

So the invariant is over-strong where one end is `analysis-and-evaluation`.
Fixing that is a change to what the chain asserts, not to a tag, and it
belongs to whoever next opens the chain declaration. **Nothing here is
retagged to hide it.**

**4. The remaining fifteen are real fault lines. Left standing, and named.**

Four shapes, and they recur:

- **A general practice and its domain-specific instance.** [SOTA-083](../practices.d/SOTA-083.md) (custom
  kernels for critical ops) against [SOTA-085](../practices.d/SOTA-085.md) and [SOTA-106](../practices.d/SOTA-106.md) (flash attention):
  in both pairs the second *is an instance of* the first. The record has no
  relation for that, so `compared_against` is standing in — which is why these
  read as comparisons nobody ran while not being spurious in the way category
  2 was. **A `specializes:` relation is the thing that would answer these**,
  and it is a scheme change, not a retag.
<!-- inactive-ok-block: SOTA-107 — Rejected, and this paragraph is about what
     an edge to a retired practice means; naming it is the point -->
- **One edge whose far end is in the attic.** [SOTA-089](../practices.d/SOTA-089.md) (align tensor
  dimensions to hardware boundaries) against [SOTA-107](../practices.d/SOTA-107.md), which is `Rejected`:
  its status note records that the 128 in it was traced to a head dimension
  and a block size, never a sequence length. That looks like the shape above
  and is not one. An unbound relation with a retired end is not a filing
  question — the comparison is the record of how the claim was checked, which
  is what the attic is for, and this report does not filter by status. Worth
  knowing when reading it: some share of any future finding here will be
  this, and this pass found one in twenty-four.
- **Rival fixes made at different layers.** [SOTA-032](../practices.d/SOTA-032.md) (pre-LN) against [SOTA-100](../practices.d/SOTA-100.md)
  (warmup proportional to model size) — an architectural fix and a schedule
  fix for one instability. [SOTA-131](../practices.d/SOTA-131.md) (rescale query and key weights under
  Muon) against [SOTA-192](../practices.d/SOTA-192.md) (normalize queries and keys) — an optimizer-specific
  fix and an architectural one. [SOTA-085](../practices.d/SOTA-085.md) against [SOTA-161](../practices.d/SOTA-161.md) — flash attention
  and the FP32 output its rounding requires. [LIT-030](../literature.d/LIT-030.md) against [LIT-200](../literature.d/LIT-200.md) — an
  activation function and the one that replaces it for stability. These cross
  because *the layer you fix something at is not the layer the problem is
  about*, and that is a true thing about the work.
- **Trunk papers whose contribution spans two topics.** [LIT-187](../literature.d/LIT-187.md) (GShard:
  conditional computation *and* automatic sharding) against the three MoE
  architecture papers around it. [LIT-137](../literature.d/LIT-137.md) against [LIT-162](../literature.d/LIT-162.md), where Mamba-2 is
  filed as a model family and the delta-rule papers as attention variants.
  [LIT-211](../literature.d/LIT-211.md) against [LIT-229](../literature.d/LIT-229.md) and [LIT-242](../literature.d/LIT-242.md), where an LLM fine-tuning method meets
  the optimizer papers it descends from; [LIT-127](../literature.d/LIT-127.md) against [LIT-241](../literature.d/LIT-241.md), GRPO
  against PPO. Splitting a trunk paper's topic would be filing it under half
  its contribution.

## Consequences

**The report is down from 38 relations and 16 lines to 24 and 10**, and the
part that remains is the part it is for. The positional-encoding line —
eight documents, six relations — is gone entirely, which is the shape of a
finding that was a missing retag rather than a missing word.

**The vocabulary is not short a word.** That was the report's prior and on
this reading it is wrong: not one of the 38 wanted a fourteenth topic. What
the record is short of is a **relation** (`specializes:`), and what the chain
is short of is a way to say that one end of an edge is an analysis of the
other.

**Eleven of fifteen mis-filings shared one cause**, and it is worth stating as
a filing habit rather than eleven corrections: a practice extracted from a
model report, a Megatron paper or a systems paper tends to inherit *that
document's* topic instead of its own. [ADR-026](ADR-026.md)'s rule already covers it — take
the topic of the claim, not of where it was found — and this is the first
measurement of how often it is missed.

**Two removed relations is not a licence to prune.** They were removed because
`compared_against` has a definition in [ADR-011](ADR-011.md) and they did not meet it, not
because they were unbound. The fifteen in category 4 are equally unbound and
all of them stay.

## Alternatives considered

**Bind the flash-attention cluster with a secondary tag.** Already tried, at
[#101](https://github.com/dmarx/anthology-of-the-sota/issues/101), and `luria.yaml` records why it was wrong: the invariant moved to
`primary_topic` partly to re-open that edge. Doing it again under a different
name would close the finding without answering it.

**Add a fourteenth topic for the analysis/subject split.** It would be a
second axis wearing the costume of a topic. `analysis-and-evaluation` is
already that second axis; adding another would not stop a lineage crossing
between them.

**Retag the Mamba papers to `attention-techniques` to bind their line.** The
record's practice here is inconsistent — Mamba, Mamba-2, Mamba-3 and RWKV-7
are `model-architecture` while Kimi Linear, Gated DeltaNet, GLA, DeltaNet,
Griffin and Monarch Mixer are `attention-techniques` — but there is a
defensible rule under the inconsistency: a *model family* takes
`model-architecture`, a *mechanism* takes `attention-techniques`, and Mamba
is both. Picking a side across six documents on one filer's judgement, to
bind one line, is the [#101](https://github.com/dmarx/anthology-of-the-sota/issues/101) move. It is named here so the next pass has
something to argue with.

**Loosen the invariant to `tags` rather than `primary_topic`.** That is the
declaration this record deliberately tightened, for a reason its own comment
states: any shared tag is too weak to carry the assertion.
