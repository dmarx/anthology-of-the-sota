---
status: Proposed
consensus: unreplicated
consensus_note: >-
  One group, one result, and the group is the one that proposed the knob.
  Nobody has agreed or disagreed — the field's stated position is still the
  one this paper corrects, that the transition is indexed by training-set
  size, and it is held by people who had no occasion to look at a ratio
  because their setting does not have one. So there is no dispute to report,
  which is `unreplicated` and not `contested`. Read as of 2026-09.
promote_when: >-
  The ratio is varied on a model trained on natural text — derived or
  multi-step statements up-sampled against the atomic facts they follow from,
  with held-out multi-step accuracy measured, and with a control that separates
  the ratio from the extra tokens it brings. A second synthetic result adds
  nothing: the effect is already clean there, and the open question is whether
  a real corpus has a ratio you can move.
title: 'To teach a model to reason over facts it holds, spend added data on facts derived from other facts rather than on more atomic facts'
version: 1
tags:
- data-pipeline
- capability-thresholds
- training-optimization
date: '2026-09-25'
source:
- LIT-tmppwagl
# Same code as `source:`. Wang et al. both measured the effect and drew the
# recommendation from it — "our findings guide data and training setup to
# better induce implicit reasoning" — so there is no earlier statement to
# credit (ADR-030).
introduced_by:
- LIT-tmppwagl
implementations: []
summary: >-
  Wang et al. (2024), [LIT-tmppwagl](../literature.d/LIT-tmppwagl.md). Two sweeps that separate what is normally
  varied together: with the inferred/atomic ratio `φ` fixed, scaling the
  training set changes nothing about how a transformer acquires a two-fact
  inference rule; with the size effect thus accounted for, raising `φ` moves
  the acquisition monotonically, and at `φ = 18.0` the delay is gone — 96.7%
  before training accuracy has even saturated. Synthetic knowledge graphs
  only, and it buys rule application on facts already seen in compositions,
  not systematicity.
explained_by:
- THEORY-071
---

# SOTA-tmpvsnuz: To teach a model to reason over facts it holds, spend added data on facts derived from other facts rather than on more atomic facts

<!-- inactive-ok-file: THEORY-071 THEORY-tmp6pl9b — Proposed, and both named as the explanations of
     this practice rather than as evidence for it: one says why the ratio is the variable, the
     other says why the practice cannot buy systematicity. That they are open is the point being
     made where each is cited. -->

## Source

Wang, Yue, Su and Sun (2024), [LIT-tmppwagl](../literature.d/LIT-tmppwagl.md) — [ARXIV-2405.15071](https://arxiv.org/abs/2405.15071).

The setting is a transformer trained from scratch on a mixture of *atomic
facts* — `(subject, relation, object)` edges of a random knowledge graph — and
*inferred facts*, which a latent rule deduces from pairs of atomic ones. The
quantity the recommendation is about is

    φ = |inferred facts in training| / |atomic facts|

and the model's ability to complete inferred facts it has not seen arrives by
grokking: training accuracy saturates above 99% long before test accuracy
leaves single digits.

**What the two sweeps establish, and why it takes two.** Raising `φ` also
raises the total amount of training data, so on its own the `φ` sweep would not
say which of the two did the work. The second sweep is what settles it: hold
`φ = 9.0` and vary the number of entities — and therefore the training-set
size, which scales linearly with it — and **nothing qualitatively changes**,
not the gap between the train and test curves, not the level of generalization
reached. Then the `φ` sweep at fixed size moves grokking speed monotonically,
and at **`φ = 18.0` the model reaches 96.7% before training accuracy has
saturated** — the delay the phenomenon is named for is simply gone.

So the operational form of this is not "add data" and not "add less data". It
is: **when you have a budget of additional examples and a model that already
holds the facts, spend the budget on statements derived from those facts.**
Another million atomic facts buys the acquisition of the rule nothing.

## Conditions, and what it does not buy

**It buys in-distribution rule application, not systematicity.** Across every
`φ` the authors tried, out-of-distribution composition — applying the rule to
atomic facts that appeared in training only in atomic form — stayed at **zero,
out to two million optimization steps**. Whatever this knob is for, it is not
for getting a model to compose facts it has only ever seen stated alone. That
limit has its own explanation in [THEORY-tmp6pl9b](../theory.d/THEORY-tmp6pl9b.md), and the fix
there is architectural, not a data ratio.

**It assumes you can tell derived from atomic.** The whole effect is indexed on
a partition of the training data that a synthetic generator hands you for free
and a natural corpus does not. On real text the analogous quantity — how much
of the corpus states a consequence of something else it states — is not
something anybody has measured, let alone moved deliberately. The
`promote_when` is about exactly that gap.

**Weight decay is part of the setup.** The source trains with AdamW at weight
decay 0.1 and reports that raising it accelerates grokking further. The account
that explains the ratio effect ([THEORY-071](../theory.d/THEORY-071.md)) needs the
regularizer, so a run with the regularization turned off is outside what has
been measured here.

**Everything is synthetic**, with a unique token per entity and an 8-layer
GPT-2. The authors argue in their limitations that the control this buys is
worth the distance from practice, and the record agrees — while pricing the
distance in, which is what the status is for.

## Known implementations

- None known. The source is a controlled study, not a training report.
