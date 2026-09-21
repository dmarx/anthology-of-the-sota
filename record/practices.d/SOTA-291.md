---
number: 291
status: Proposed
formerly:
- SOTA-tmphxqsm
promote_when: >-
  A specific-affordance evaluation run at collective scale with the group-level
  outcome actually measured — the source notes two large platform studies that
  tested realistic ranking changes and assessed only individual outcomes, so
  the missing piece is small and nameable. A further argument that individual
  trials are inadequate is not it; that is the premise.
consensus: unreplicated
consensus_note: >-
  The negative half — that individual-level trials cannot identify collective
  effects when units interact — is not really in dispute once stated; SUTVA
  violation and path-dependence are structural. What is unreplicated is the
  positive programme, and its two sources share a first author, so the record
  holds one position argued twice rather than two groups agreeing.
title: 'Evaluate a specific intervention on a specific affordance rather than the net effect of the system, and never read an individual-level null as the absence of a collective effect'
version: 1
tags:
- deployment-and-society
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-482
introduced_by:
- LIT-482
implementations: []
explained_by:
- THEORY-048
---

# SOTA-291: Evaluate a specific intervention on a specific affordance rather than the net effect of the system, and never read an individual-level null as the absence of a collective effect

## Source

Bak-Coleman, Lewandowsky, Lorenz-Spreen, Narayanan, Orben and Oswald (2025),
[LIT-482](../literature.d/LIT-482.md) — read as [NOTE-230](../notes.d/NOTE-230.md).

## When this applies

You want to know what a deployed system does to a population, the population's
members interact, and the system adapts to their behaviour. That is every
recommender, ranking system and large-scale assistant, and the source's domain
is one instance of it rather than the scope.

## The negative half

**A null from an individual-level randomized trial is not evidence that the
system has no collective effect.** [THEORY-048](../theory.d/THEORY-048.md) gives four
separable reasons; two of them are structural and cannot be fixed with more
data:

- **Units interact, so the design violates SUTVA.** Assign someone a
  chronological feed and their neighbours still pass them algorithmically
  ranked content. The trial is not estimating what its design says.
- **Removal is not the inverse of addition.** This is the objection to every
  **withdrawal study** — deactivation, reduced use, feature removal — and it is
  worth stating on its own, because withdrawal designs are popular and their
  assumption is invisible until named. Stopping something for two weeks tells
  you about stopping it for two weeks.

The symmetry matters: this is equally not evidence that the effects are real.
The claim is that the design is uninformative about the collective question,
in both directions.

## The positive half

Ask about a **specific intervention on a specific affordance** — down-ranking
toxic content, bridging-based ranking, a cross-partisan prompt — rather than
about the net effect of the system's existence. Three advantages the source
gives:

1. **A coherent counterfactual**, so the estimand is meaningful. "What if this
   platform had never existed" has no usable counterfactual; "what if this
   ranking rule were changed" does.
2. **It can run long enough.** A small treatment can be left in place for far
   longer than a deactivation study can, which is what the time-dependence
   problem requires.
3. **It maps to a decision** somebody can actually take.

Two riders. Because effects depend on time and on the state of other
variables, **evaluate continuously** rather than once — which is what
operators already do for their own commercial metrics. And **triangulate**:
no modality here is a gold standard, so combine trials, observation and models
rather than looking for a better trial.

## Conditions

**Both halves are argument, not demonstration.** The source is a review with
no new data. The negative half is strong because two of its four mechanisms
are structural; the positive half is three stated advantages and a direction.

**The positive programme has not been run at the scale it asks for.** The
source notes that two large platform studies did test realistic ranking
interventions — and did not assess collective outcomes at the group level. So
the missing step is specific and small, and nobody has taken it.

**"Limited value" is a judgement, not a measurement.** How much an
individual-level trial still tells you is not quantified for any published
study. If your estimand genuinely is the short-run individual effect, none of
this binds.

**This does not license dismissing a literature.** The claim bounds what a
design can conclude. A reader who takes it as "those studies were wrong" has
taken more than it says — and the direction of the error is not determined.

**Read the surrounding literature with its funding visible.**
[LIT-481](../literature.d/LIT-481.md) finds industry ties in 49% of high-profile papers in
this field, mostly undisclosed, and **sparse in exactly the platform-dynamics
cluster** this practice points you toward. That is correlational and its
authors say so; it is still the context in which "the evidence is mixed" gets
said.

**Two sources, one first author.** This practice and the disclosure finding
share an author, which is why the consensus note says one position argued
twice rather than two groups agreeing.
