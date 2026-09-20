---
number: 207
status: Skimmed
formerly:
- NOTE-tmpmg0fm
paper: LIT-459
title: 'Contextures: The Mechanism of Representation Learning'
version: 1
date: '2026-09-20'
summary: >-
  A representation is the association between the input and a context
  variable; capturing its maximum information is optimal on tasks compatible
  with that context. A context is most useful when the association is neither
  too strong nor too weak, and mixing contexts is offered as the cheap way to
  get there. Skimmed: a 313k-character dissertation, read at summary level.
---

# NOTE-207: Contextures: The Mechanism of Representation Learning
<!-- inactive-ok-file: SOTA-256 — Proposed, and named as the record's other account of where scaling stops paying -->

## What was read, and what was not

**This is a `Skimmed` note and the status is the first thing it should say.**
The source is a CMU dissertation of roughly 313,000 characters. What was read:
the abstract, the introduction, the stated implications, the conclusions, and
the sections naming the two objectives. What was not read: the theorems and
their proofs, the statistical learning bounds, and the semi-supervised
extension through spectrally transformed kernel regression.

Everything below is the dissertation's own statement of its results, not a
check of them. [ADR-025](../decisions.d/ADR-025.md) makes `Skimmed` respectable and explicitly not
enough to source a practice from alone; the practice drawn from this records
that in its conditions.

## Contribution

Proposes that the many pretraining objectives — supervised, self-supervised,
generative — are one mechanism with a varying part. The varying part is the
**context variable**: a representation is learned from the association
between the input and that variable, and an encoder capturing the maximum
information of the association is claimed optimal for the class of tasks
compatible with it. That converts "what is this representation good for" from
an empirical question into a statement about the context, and it yields a
criterion for a *good* context — neither too strong nor too weak an
association — plus a construction for making better ones by mixing.

## Key insight

**Scale aligns a representation to the top singular functions of an
association it did not choose.** If the context is what determines the
ceiling, then more parameters buy a closer approach to that ceiling and
nothing beyond it — which is a mechanism for diminishing returns that is not
about data volume or optimisation, and which predicts that the way out is to
change the context rather than the model. The sweet-spot criterion is the
part that makes it usable: a context whose association is too strong teaches
little because the answer is nearly determined, and one too weak teaches
little because there is nearly no signal, so the useful contexts sit in
between and that position is readable off the singular-value decay.

## Assumptions

- **The association between input and context is the object.** Everything
  rests on that framing being the right decomposition of pretraining.
- Optimality is **on the class of tasks compatible with the context** — a
  conditional claim, and the conditional is doing real work.
- The spectral criterion assumes the expectation operator's singular values
  are the right summary of association strength.
- The mixing construction assumes contexts combine in a way that moves the
  decay rate toward the middle.
- *(Unverified: the conditions on the theorems themselves were not read.)*

## Key results

*(As stated by the source; not checked against proofs.)*

- **Learning the contexture is optimal** on tasks compatible with the
  context.
- **A context is most useful when the association is neither too strong nor
  too weak**, i.e. the singular values of the expectation operator decay
  neither too fast nor too slowly.
- **Mixing contexts improves them**: several contexts whose associations are
  individually too strong or too weak combine into a better one, described as
  an effortless route to better contexts.
- **Scaling has a ceiling set by the context.** Scale brings the
  representation into alignment with the top singular functions; once
  alignment is high, further scaling gives diminishing returns.
- **Two general objectives**, SVME and KISE, for learning the contexture
  under different access assumptions.
- Many existing pretraining objectives are shown to learn the contexture.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Pretraining methods differ by context variable and are otherwise one mechanism | moderate | argued across method families; the unification is the dissertation's thesis |
| C2 | Capturing the association's maximum information is optimal on compatible tasks | moderate | stated as proved; proof not read |
| C3 | The best contexts have association neither too strong nor too weak | moderate | stated as shown; the spectral form makes it measurable |
| C4 | Mixing contexts produces better ones | weak | stated as a construction; no measurement read |
| C5 | Scaling alone yields diminishing returns because the context sets the ceiling | weak | an implication of C2 and C3 rather than an independent measurement |

## Method

*(Not read in enough detail to summarise responsibly.)* The framework is
spectral: the association between input and context is treated through an
expectation operator whose singular functions and singular values carry the
structure, with "learning the contexture" defined as capturing the top
singular functions. SVME and KISE are objectives for doing so under pair
access and under a weaker access model respectively.

## Concepts

- **Context variable** — the quantity a representation is learned in
  association with. Masking gives one, augmentation another, a label another.
- **Learning the contexture** — capturing the maximum information of the
  input-context association.
- **Compatible task** — a downstream task for which the context's
  association is sufficient; the class on which optimality is claimed.
- **Association strength** — operationalised as the decay rate of the
  expectation operator's singular values.

## Connections

Against the record's data-constrained cluster: [SOTA-256](../practices.d/SOTA-256.md) judges a scaling
recipe by its asymptote and [LIT-441](../literature.d/LIT-441.md) moves that asymptote with
regularisation and ensembling. This locates the asymptote in the *context*
and says no amount of scaling moves it — a stronger and more falsifiable
version of the same worry from a different direction, and nobody has put the
two together.

Against the record's objective practices — masked diffusion, fill-in-the-
middle, multi-token prediction, the augmentation families — which are filed
one at a time with no account of what they share. This proposes that they
differ in one variable with a measurable optimum.

## Recommendations

- **R1** — Choose a pretraining context whose association with the input is
  neither too strong nor too weak, judged by singular-value decay. *Topic:*
  objectives. *Status:* experimental. *Strength:* weak. *Applies when:* the
  spectrum is estimable, which is not addressed in what was read.
- **R2** — Mix contexts rather than searching for a single good one. *Topic:*
  objectives. *Status:* experimental. *Strength:* weak. *Applies when:* as
  above.
- **R3** — Do not expect model scaling to move a ceiling the context sets.
  *Topic:* scaling. *Status:* experimental. *Strength:* weak. *Applies when:*
  the framing holds, which is the whole question.

## Bearing on the record

- **Should produce one practice**, combining R1 and R2, filed `Proposed`, and
  recording in its conditions that the source is `Skimmed`. Filing two would
  overstate what a skim supports.
- **R3 should not be filed.** It is an implication of an unread proof, and
  the record already holds better-evidenced accounts of diminishing returns.
- **Gives the record a frame for objectives as a class**, which it has never
  had — every objective practice is filed on its own evidence with nothing
  saying what would make a new one good.
- **Should be re-read properly if anything comes to depend on it.** A
  `Skimmed` note under a `Proposed` practice is a thin foundation, and the
  honest move if the practice is ever promoted is to read the theorems first.

## Limitations

- **The reading is a skim**, which is the dominant limitation and is the
  reason most claims above are `weak`.
- A dissertation is one group and one framework; the unification is a
  proposal about how to see the field, and such proposals are hard to falsify.
- Optimality is conditional on task compatibility, and how to know in advance
  whether a task is compatible is not something the skim reached.
- No frontier-scale demonstration was found in what was read; the objectives
  are introduced but their empirical standing is unassessed here.
- The mixing construction is the most actionable claim and the one with least
  read evidence behind it.

## Open questions

- Can the singular-value decay of a real pretraining context be estimated
  cheaply? Without that, R1 is a criterion nobody can apply.
- Does the context ceiling and the [LIT-441](../literature.d/LIT-441.md) asymptote refer to the same
  quantity? Two accounts of where scaling stops paying, from different
  premises, never compared.
- What is the context of next-token prediction, in this framework, and where
  does its association sit on the too-strong/too-weak axis? That is the case
  the record most needs and the skim did not reach it.
