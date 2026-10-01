---
status: Active
title: 'agents-and-environments, graphs-and-networks, physical-sciences, human-ai-interaction'
version: 1
tags:
- taxonomy
- record
date: '2026-10-01'
summary: >-
  Four topics, taking the vocabulary from twenty-two to twenty-six:
  `agents-and-environments`, `graphs-and-networks`, `physical-sciences` and
  `human-ai-interaction`. Filing the reading feed's revisit list ([#180](https://github.com/dmarx/anthology-of-the-sota/issues/180))
  declined three papers because no topic held them and filed four more under
  the nearest wrong word, each saying so; under [ADR-059](ADR-059.md) that is the axis
  being short. Existing documents whose subject the new words name take
  them, first where it is their main subject and as a secondary tag
  otherwise. Rejected: a separate `collective-intelligence`, which
  `agents-and-environments` covers, and leaving the papers unfiled, which
  [ADR-059](ADR-059.md) rules out.
---
<!-- inactive-ok-file: LIT-697, LIT-715, LIT-717, SOTA-298, SOTA-303, SOTA-309, THEORY-091 — Deferred or Proposed; named because this decision retags them or cites them as the evidence-quality warnings it relies on, not as settled claims -->

# ADR-tmp56fu3: agents-and-environments, graphs-and-networks, physical-sciences, human-ai-interaction

## Context

The [#180](https://github.com/dmarx/anthology-of-the-sota/issues/180) pass filed papers the owner returned to on three or more days. Its
readers hit the edge of the vocabulary seven times, and each one said so
rather than forcing a tag:

- *The Work Capacity of Channels with Memory* and *The Computational
  Foundations of Collective Intelligence* were declined: one is about the
  work a finite-state agent can extract in a percept–action loop, the other
  about animal collectives, and no topic is about agents or what acting does.
- *Community Detection on Networks with Ricci Flow* was declined: no topic is
  about graphs, though the record already holds the GNN expressivity and
  evaluation papers ([LIT-580](../literature.d/LIT-580.md), [LIT-581](../literature.d/LIT-581.md)) and a practice and a theory drawn from
  them ([SOTA-350](../practices.d/SOTA-350.md), [SOTA-351](../practices.d/SOTA-351.md), [THEORY-083](../theory.d/THEORY-083.md)), all filed under
  `model-architecture` and `analysis-and-evaluation`.
- *From monoliths to modules* ([LIT-tmpsv8zc](../literature.d/LIT-tmpsv8zc.md)), a paper about world models, was
  filed under `model-architecture` and said its primary subject had no word.
- *Erwin* ([LIT-tmpv26b7](../literature.d/LIT-tmpv26b7.md)) evaluates only on cosmology, molecular dynamics,
  PDEs and airflow, and its note said the domain was unplaceable.
- *Textoshop* ([LIT-tmp5cmgx](../literature.d/LIT-tmp5cmgx.md)) was filed under `deployment-and-society`, a
  topic about deployed systems among people, with a note that the fit was
  loose; [LIT-503](../literature.d/LIT-503.md) had been filed the same way.

The owner approved the four words the readers proposed.

## Decision

Four topics, each with a label and blurb in `luria.yaml`:

- **`agents-and-environments`** — systems that perceive, act and are changed
  by the consequences: percept–action loops, world models and training
  environments, multi-agent and collective behaviour.
- **`graphs-and-networks`** — graph-structured data and the models that run
  on it: message passing, how GNNs are evaluated, curvature, rewiring,
  community structure.
- **`physical-sciences`** — models whose data is the physical world: learned
  simulation surrogates and foundation models for physical observation. It
  sits beside `biomolecular-modeling` ([ADR-059](ADR-059.md)), which keeps molecules.
- **`human-ai-interaction`** — how people work with a model through an
  interface, how such interfaces are scored, and what lab studies of them can
  show. `deployment-and-society` keeps what a deployed system does among
  people at scale.

The filing rule stays [ADR-026](ADR-026.md)'s and [ADR-059](ADR-059.md)'s: a document *about* the subject
takes the topic first; a general method found there takes its kind first and
this topic as well.

**Retagged.** First tag:

- `graphs-and-networks`: [LIT-579](../literature.d/LIT-579.md), [LIT-580](../literature.d/LIT-580.md), [LIT-581](../literature.d/LIT-581.md), [LIT-582](../literature.d/LIT-582.md), [THEORY-083](../theory.d/THEORY-083.md),
  [SOTA-350](../practices.d/SOTA-350.md), [SOTA-351](../practices.d/SOTA-351.md);
- `agents-and-environments`: [LIT-tmpsv8zc](../literature.d/LIT-tmpsv8zc.md);
- `physical-sciences`: [LIT-715](../literature.d/LIT-715.md) (Surya, a heliophysics foundation model);
- `human-ai-interaction`: [LIT-tmp5cmgx](../literature.d/LIT-tmp5cmgx.md), [LIT-503](../literature.d/LIT-503.md), [THEORY-091](../theory.d/THEORY-091.md), [SOTA-309](../practices.d/SOTA-309.md).

Secondary tag: SuperGlue ([LIT-386](../literature.d/LIT-386.md)) takes `graphs-and-networks`; AgentSociety
([LIT-697](../literature.d/LIT-697.md)) and MemGraphRAG ([LIT-502](../literature.d/LIT-502.md)) take `agents-and-environments`; Erwin
takes `physical-sciences`; [LIT-717](../literature.d/LIT-717.md) takes `human-ai-interaction`.

Every document keeps its existing tags, so no relation's `invariant: tags`
loses a shared value.

## Alternatives considered

- **A separate `collective-intelligence`.** Its reader offered it as the
  alternative if `agents-and-environments` were kept to machine agents. The
  blurb includes collective behaviour instead: a group that perceives and
  acts is an agent system, and splitting it would leave one paper alone under
  a topic.
- **Leaving the three papers out.** They are already held in nucleation.
  [ADR-059](ADR-059.md) is explicit that the topics are an axis, not a scope, and the owner
  asked for them to be held in both.
- **Widening `deployment-and-society` for interface studies.** Its subject is
  a system's effect on people at scale, and its blurb is about audits and
  information ecosystems; a twelve-person lab study of an editor is a
  different kind of evidence, and the record's warnings about it ([SOTA-298](../practices.d/SOTA-298.md),
  [SOTA-303](../practices.d/SOTA-303.md)) are about exactly that difference.

## Consequences

- The vocabulary has twenty-six topics; `CLAUDE.md` and the vocabulary's own
  header say so.
- The three declined papers are filed in the same contribution.
- The GNN material now shares a topic, so a reader can find the expressivity
  bound, the evaluation pitfalls and the practices drawn from them together.
