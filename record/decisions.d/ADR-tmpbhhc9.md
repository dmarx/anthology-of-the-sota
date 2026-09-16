---
status: Proposed
title: 'Advice on how to prove a theorem is out of scope; advice on how to find out whether a technique worked is not'
version: 1
tags:
- record
- taxonomy
date: '2026-09-16'
issue: '#139'
summary: >-
  Six recommendations in the [#139](https://github.com/dmarx/anthology-of-the-sota/issues/139) import tell a reader how to construct a
  proof — use the bounded-Lipschitz metric, check a log-Sobolev inequality,
  work in a rigged Hilbert space. They were struck by one filer without a
  decision, and `analysis-and-evaluation` is broad enough that the cut was not
  obviously right. It is right, and the reason is the scope test in [ADR-026](ADR-026.md):
  the reader this anthology addresses is training a model. A proof technique
  is advice to someone writing a paper about training, which is a different
  person.
---

# ADR-tmpbhhc9: Advice on how to prove a theorem is out of scope; advice on how to find out whether a technique worked is not

## Context

The import behind [#139](https://github.com/dmarx/anthology-of-the-sota/issues/139) struck six recommendations as *"not filed — advice on
proof technique, not on training"*. Three of them:

- use the bounded-Lipschitz metric and Neunzert-style empirical-measure
  coupling
- check whether the `N`-particle Gibbs measure satisfies a log-Sobolev
  inequality uniformly in `N`
- work in a rigged Hilbert space and analytically continue the resolvent

The cut was made by one filer, in the course of doing something else, and
[#139](https://github.com/dmarx/anthology-of-the-sota/issues/139) is right that it wants deciding in writing — because the vocabulary does
not obviously exclude it. `analysis-and-evaluation` is blurbed as *"how to
find out whether something worked… theory, interpretability and debugging
belong here too"*. Theory belongs there. A proof is theory. Nothing in the
tag list says no.

[DP-009](../../docs/design-principles.md#dp-9) is the reason this cannot be left as a shrug. *A claim the categories
cannot express is evidence about the categories until someone shows
otherwise*, and the cheap reading — "out of scope" — is self-confirming,
because declining the documents leaves the vocabulary looking complete. Six
documents declined for the same missing category would be a missing category.

## Decision

**Advice whose reader is constructing a proof is out of scope. Advice whose
reader is finding out whether a technique worked is in scope, and is what
`analysis-and-evaluation` is for.**

The test is the one [ADR-026](ADR-026.md) already uses, applied to the *audience* rather
than the domain: **who does the sentence tell what to do?**

- *"Measure the gradient noise scale instead of sweeping batch size"* — the
  reader is running a training job. In scope. It is [SOTA-198](../practices.d/SOTA-198.md).
- *"Check whether the `N`-particle Gibbs measure satisfies a log-Sobolev
  inequality uniformly in `N`"* — the reader is writing the convergence
  section of a paper. Out of scope.

Both are about theory. Only one is addressed to somebody training a model,
and [ADR-026](ADR-026.md) scopes this record by the kind of claim, which is a claim about
what the reader does next.

**The paper stays, the reading stays, the recommendation stays struck in
place.** This decides nothing about admitting mean-field or particle-system
papers as `LIT` documents; [THEORY-009](../theory.d/THEORY-009.md) is a wide two-layer network's gradient
flow and is filed, correctly. What is out of scope is one *kind of sentence*
inside such a paper, and the `## Recommendations` section of the note keeps it
with a strikethrough and the reason, which is how the cut stays auditable.

## Why this is not the vocabulary being short a category

Applying [DP-009](../../docs/design-principles.md#dp-9)'s own two tests:

**Would you decline this claim if it arrived with excellent evidence and a
familiar author?** Yes — and this is the test that settles it. A beautifully
evidenced result that the bounded-Lipschitz metric is the right one for
coupling empirical measures is still not something a reader of this anthology
does. The objection was never about the strength of the work.

**Are the claims already in the record on this subject filed coherently?** Yes.
Twelve `THEORY` documents, all of them accounts of *why a technique behaves as
it does*, none of them about how to establish such an account. The subject
exists in the corpus with one consistent shape, and proof technique is not
scattered across four ill-fitting categories — it is absent, which under
[DP-009](../../docs/design-principles.md#dp-9) is the state that needs explaining, and this is the explanation.

## What this does not decide

**It does not narrow `analysis-and-evaluation`.** Debugging, interpretability,
evaluation methodology and the accounts in `THEORY` all stay exactly where
they are. This removes one class the blurb could be read as admitting, and the
blurb is not changed, because the boundary is about audience and a topic tag
cannot express that.

**It does not say a proof technique can never become in scope.** If a
particular argument became the standard way practitioners verify a training
claim — the way a scaling-law fit did — the sentence would then be addressed
to a practitioner and would pass the test. The decision is about what the
sentence does, not about which field it came from.

**It does not decide the reverse case**: a training recommendation that only
exists inside a theory paper. Those are in scope on this test and always
were; [#139](https://github.com/dmarx/anthology-of-the-sota/issues/139)'s six are not that.

## Alternatives considered

- **Admit them under `analysis-and-evaluation`.** The tag's blurb allows it on
  a literal reading. Rejected because it would make the registry hold advice
  two different professions act on, and a reader filtering to that tag for
  "how do I tell whether my run worked" would get resolvent continuation.
- **Add a `proof-technique` topic.** This is the [DP-009](../../docs/design-principles.md#dp-9)-shaped move and it
  fails its own first test: the category would be added so that a decision
  would not have to be, which is exactly what [DP-008](../../docs/design-principles.md#dp-8)'s corollary forbids.
- **Leave it undecided and cut case by case.** The status quo, and what [#139](https://github.com/dmarx/anthology-of-the-sota/issues/139)
  filed the objection against. The cost is a filer re-deriving the same
  judgement at every mean-field paper, with nothing pointing at the last
  time it was made.
