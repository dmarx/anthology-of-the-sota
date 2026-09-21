---
status: Active
title: 'Two more topics: one that had a trailing clause for a home, and one that had nothing'
version: 1
tags:
- record
- taxonomy
date: '2026-09-21'
summary: >-
  Eighteen topics, from sixteen. `multimodal-learning` takes nine documents
  that sat across six topics while `model-architecture`'s blurb carried
  "multi-modal designs" as a trailing clause — the same half-home shape
  `ADR-050` found for numerics. `deployment-and-society` names nothing in the
  record at all and twenty-four papers on the incoming list, led by its single
  highest-revisit entry. Rejected on counting: mechanistic interpretability,
  the physics of learning, safety, agents, graphs, federated learning, human-AI
  interaction and scientific domains.
---

<!-- inactive-ok-file: ADR-050 — Proposed, and the decision this one follows
     in method and cites for the half-home diagnosis and the counting test. Its
     unsettled status is not load-bearing: what is cited is a measurement it
     made and a rule it applied -->

<!-- inactive-ok-file: SOTA-262 — Proposed, named in the Consequences list of
     documents that gained a tag; a practice's standing is unaffected by which
     topic it files under -->

<!-- inactive-ok-file: SOTA-271 — see above -->

# ADR-tmpkp17k: Two more topics: one that had a trailing clause for a home, and one that had nothing

## Context

The papers-feed worklist is ranked by revisits, and the top of it had drifted
away from what the sixteen topics could express. Working down it meant
repeatedly skipping the most-read entries — including the single highest, at
22 revisits — and filing the in-scope items beneath them.

That is the pattern `DP-009` names and warns about. A document with a real
claim and no category has two readings: the claim is out of scope, or the
vocabulary is short a word. The first is cheaper, requires no work, and is
**self-confirming** — decline the document and the vocabulary keeps looking
complete, because the evidence that would have shown otherwise has just been
turned away.

Asked to extend the vocabulary, the question was which words, and the
instrument is `DP-009`'s: count, then read the hits.

## Decision

Two topics, taking the vocabulary from sixteen to eighteen.

### `multimodal-learning`

*What changes when one model has to take in more than one kind of signal —
joint architectures and fusion, contrastive image-text training, cross-modal
transfer, and what a second modality buys the first.*

This is a **naming gap**, and it has the exact shape `ADR-050` found for
numerics. `model-architecture`'s blurb ended with "multi-modal designs" — a
trailing clause on a topic about the shape of a network, doing duty for a
subject about how many kinds of signal go into it. Nine documents sat across
six topics, with `model-architecture` holding three of them.

Thirty-five more are queued on the incoming list, at 55 revisits between them,
and they are not the generative ones: text-to-image and text-to-video work
already has a home in `generative-modeling`, whose blurb names it. What is
left is vision-language encoders, multimodal foundation models, fusion
architectures, image-text datasets and cross-modal behaviour.

`model-architecture`'s blurb loses the clause, and now says what it is about:
how the network is shaped, not how many signals it takes in.

### `deployment-and-society`

*What a system does once it is running among people, and how anyone outside it
could find out — audits of deployed platforms and recommenders, information
ecosystems, moderation and governance, and the access problems and funding
pressures of studying any of it from the outside.*

This is a **scope extension**, and it is the only topic in the vocabulary that
named nothing on the day it was added. A probe across all 749 record documents
returned one hit and that hit was a homonym. The incoming list holds
twenty-four, led by the highest-revisit paper on it.

The blurb's last clause is deliberate. A quarter of those twenty-four are
methodological rather than substantive — how to do this research, what
happens when platform data access is withdrawn, who funds the high-profile
studies, what a benchmark for societal-impact work would have to look like.
Those are claims of a kind this record already files: recommendations about
how to measure. `ADR-026` is the rule that lets the rest in — a claim takes
its kind, not its domain.

Adding a topic that names nothing is the weakest move in this decision and it
is made deliberately, because the alternative is the self-confirming decline.
The first filing follows this contribution; if it does not, this term is the
one to reconsider.

## Alternatives considered

Six candidates were counted and rejected. Recording them matters more than
the two that passed, because the next pass should not re-measure them.

- **Mechanistic interpretability.** 19 apparent record documents, about ten
  real after reading — "circuit", "feature" and "interpretable" are used
  loosely across the corpus, and an evolution-strategies paper was among the
  hits. The survivors sit in `analysis-and-evaluation` and
  `representation-and-encoding`, and **both blurbs already name the work**:
  the first says "theory, interpretability and debugging belong here too".
  Two honest homes is not a half-home.
- **The physics of learning.** 28 record documents — and **17 of them already
  take `analysis-and-evaluation` as primary**, 61%. By the test `ADR-050` set,
  a subject the vocabulary can say lands mostly in one topic, and a subject it
  cannot scatters. This one lands. The instrument working in the negative
  direction is the reason to trust it in the positive one.
- **Safety.** 20 apparent, **about three real**. The rest matched "harmful"
  and "misuse" in passing — five of them inside the quantization cluster,
  which is the purest homonym this exercise produced. `ADR-050` already put
  "safety alignment" into `adaptation-and-tuning`'s blurb, and the three real
  documents are there. Three is not several.
- **Agents and tool use.** 15 on the incoming list, none above two revisits,
  and scattered across multi-agent reinforcement learning, agentic frameworks
  and model reports. No subject, no engagement.
- **Graphs and networks.** 16 incoming, and they split. The graph-neural-network
  half is architecture and `model-architecture` covers it; the community-detection
  and network-curvature half is network science, and makes no claim of a kind
  this record's schemes can express. The record holds two documents, one of
  which is a false positive.
- **Federated learning and privacy.** 9 incoming, none above two revisits, and
  six of the nine are federated learning — which is parallelism and
  communication, already `distributed-optimization`.
- **Human-AI interaction** (8 incoming, two or three real) and **scientific
  domains** (4 incoming). Both fail on count alone. `DP-009`: two is not
  several.

The other alternative was **doing nothing**, which is what the previous
eleven contributions did by working down past the top of the list. That has a
cost the ranking makes visible: the most-read paper on the worklist has been
skipped on every pass.

## Consequences

- **Eighteen topics, seventeen of them primary.** `tiny-models` remains
  secondary-only.
- **Nine documents retagged** — four to `multimodal-learning` as primary
  (`LIT-071`, `LIT-080`, `SOTA-262`, `SOTA-271`), five as a secondary. The
  primary moved only where the document's central claim is about crossing
  modalities: `SOTA-262` recommends giving each modality its own weights, and
  `LIT-072`'s open-vocabulary detection is vision work that happens to use
  text, so it keeps `vision-and-graphics` first.
- **`model-architecture` loses a clause and gains a boundary.** No document
  loses a tag.
- **Three stale counts corrected.** The vocabulary comment and blurb said
  "sixteen", which was right; a third comment said the primary group was "the
  thirteen above" when it had been fifteen for some time. That is the second
  count in this file to have drifted — `ADR-050` found "thirteen" where
  fourteen terms were declared — and suggests the number should not be written
  in prose at all.
- **`deployment-and-society` is on probation by construction.** It is the one
  term here justified entirely by what is queued rather than by what is held.
