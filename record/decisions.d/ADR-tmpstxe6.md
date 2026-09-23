---
status: Active
title: 'biomolecular-modeling, and the topics as an axis rather than a scope'
version: 1
tags:
- taxonomy
- record
date: '2026-09-23'
issue: '#163'
summary: >-
  A twentieth topic, `biomolecular-modeling`, for models whose data is
  molecules: protein and nucleic-acid structure prediction, biological
  sequence language models, docking and molecular property prediction. It
  also records the rule the gap exposed. The topics organize what the
  anthology holds, they do not decide what it may hold, so content the axis
  cannot place is a finding about the axis. Rejected: declining AlphaFold as
  "outside the topics", which is what happened first, and a
  `protein-structure-prediction` word too narrow for AlphaFold 3 or for
  the RNA paper already in the record.
---

# ADR-tmpstxe6: biomolecular-modeling, and the topics as an axis rather than a scope

## Context

Issue `#163` listed AlphaFold among things to file. Working through the
issue, the filer left it unfiled and reported it as a scope question
because "protein structure prediction is outside the eighteen topics" (the
count at the time, before `capability-thresholds`). The owner's answer is
the rule this decision writes down:

> the topic set is not a constraint, it is just an axis around which to
> organize content. if the axis is insufficient to represent content we're
> interested in: that should be interpreted as a signal about the
> inadequacy of the axis rather than the non-relevance of the content.

The record already said most of this. The `topics` alert says the
vocabulary is closed "NOT because the list is finished". [ADR-026](ADR-026.md) says the
bias toward language-model training is "a bias, not a boundary", and
[DP-009](../../docs/design-principles.md#dp-9) is written beside `deployment-and-society` in `luria.yaml`:
"declining a document because no category fits is the self-confirming
reading". The slip happened anyway, because the sentence a filer reads
first, in `CLAUDE.md`, said work "qualif[ies] if the recommendation is one
the nineteen topics can express". Read literally, that sentence is a gate.

A sweep found the cost was already being paid:

- `LIT-505` (ESM-1b, a protein language model trained on 250 million
  sequences) and `LIT-506` (RNA-FM, an RNA foundation model for structure
  and function) are filed with `representation-and-encoding` as their
  primary topic. That is the nearest wrong word the `topics` alert warns
  about. Their subject is models of biological molecules, and a reader
  browsing for that had nowhere to look.
- AlphaFold 2 and 3, which the issue asked for, had no topic at all.

## Decision

**A twentieth topic, primary-eligible:**

> `biomolecular-modeling` — models whose data is molecules: protein and
> nucleic-acid structure prediction, biological sequence language models,
> docking and molecular property prediction. What they get right, what
> their benchmarks can show, and which of their methods travel to other
> domains.

**The filing rule stays [ADR-026](ADR-026.md)'s.** A document *about* biomolecules takes
this topic, first. A practice that was discovered in AlphaFold but is
about something general, such as self-distillation on confident
predictions, takes its kind first and this topic as well, so someone
browsing either finds it.

**The scope rule, stated where filers read it.** `CLAUDE.md` now says the
topics are an axis, not a scope, and that content the axis cannot place
means the axis gains a topic. The document is not declined. The `topics`
blurb in `luria.yaml` says the same, so it renders in the views.

**Retagged:** `LIT-505` and `LIT-506` take `biomolecular-modeling` as their
primary topic and keep their other tags. Their subject is protein and RNA
models, and their representation and adaptation lessons stay findable
under the old words.

## Rejected alternatives

- **Leave AlphaFold unfiled until a transferable lesson is identified.**
  This is what the filer proposed, and it inverts the relation between
  content and axis. It also misjudged the content: AlphaFold's
  self-distillation and confidence heads are general methods, and would
  have been filed under their kinds anyway.
- **`protein-structure-prediction`.** It names the issue's item exactly and
  nothing else. AlphaFold 3 predicts nucleic acids, ligands and their
  complexes, and RNA-FM is about RNA. A word that fits its first document
  and not its second would need replacing on the next filing.
- **A general `scientific-applications` word.** It is broader than anything
  in hand, and a topic nobody can blurb precisely is one nobody can tag
  consistently. Physics, climate and materials models can each get their
  own word when the record holds them.

## Consequences

- Twenty topics, eighteen primary-eligible. `tiny-models` and
  `capability-thresholds` stay where their decisions put them.
- `LIT-579` (Where did the gap go?) uses molecular benchmarks but is about
  evaluation practice. It is not retagged, because someone browsing
  biomolecular models would not expect it.
- The next document the axis cannot place follows the same path: a word, a
  blurb, a decision. It does not wait for permission.
