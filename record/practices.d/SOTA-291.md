---
number: 291
status: Active
formerly:
- SOTA-tmphxqsm
consensus: emerging
consensus_note: >-
  The negative half — that individual-level trials cannot identify collective
  effects when units interact — is not really in dispute once stated; SUTVA
  violation and path-dependence are structural. The positive programme now has
  one execution as well as its argument, by a different group on a different
  platform, which is why this is `emerging` rather than `unreplicated`. It is
  not `converged`: one worked example is not a method the field runs, and the
  two documents arguing for the programme still share a first author.
title: 'Evaluate a specific intervention on a specific affordance rather than the net effect of the system, and never read an individual-level null as the absence of a collective effect'
version: 2
history:
- version: 2
  date: '2026-09-21'
  note: >-
    Proposed -> Active. The promotion condition asked for a specific-affordance
    evaluation run at collective scale with the group-level outcome actually
    measured, and named the gap as small and nameable. LIT-487 is that
    evaluation: one affordance (an AI drafting tool in one writing flow), a
    coherent counterfactual (a staggered rollout that reached three countries
    eleven weeks before a fourth), an eleven-week window against a 65-week
    pre-period, and outcomes measured at the platform level rather than the
    user level. The authors arrive at the design from this practice's own
    reasoning independently — they decline individual-level estimates because
    an interconnected platform biases them — which is stronger than following
    the source would have been. The recommendation is unchanged; what changes
    is that the positive half has been done rather than only argued.
tags:
- deployment-and-society
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-482
- LIT-487
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

**The positive programme has now been run once.** [LIT-487](../literature.d/LIT-487.md) takes
one affordance — Change.org's in-platform AI drafting tool — across a
staggered rollout, and measures platform-level outcomes: the share of
petitions clearing a signature threshold, inter-petition homogeneity, and
total participation. It finds the text transformed and the outcomes flat or
worse. That is the missing step, taken, and the practice moves to `Active` on
it.

It is one execution, on a platform with four country-level clusters and an
eleven-week window, and it should be read as proof that the design is
available rather than as evidence that it is easy. The source's original
observation still stands for the ranking literature specifically: the two
large platform studies it named tested realistic interventions and assessed
only individual outcomes.

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
