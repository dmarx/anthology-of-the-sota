---
number: 103
status: Proposed
formerly:
- THEORY-tmp6pl9b
promote_when: >-
  The layer asymmetry is measured on a model trained on natural text — the
  second-hop fact recoverable from the upper layers for compositions the model
  was trained on and absent for facts it only ever saw atomically — or the
  cross-layer-sharing fix is reported with numbers on a task that is not
  synthetic. Corroboration that frontier models do the first hop and not the
  second is not enough: that pattern is what this account predicts, and it was
  already observed before the account existed.
title: 'A transformer stores a fact where it needed it, so two-hop composition generalizes only to facts it already saw as a second hop'
version: 1
tags:
- model-architecture
- analysis-and-evaluation
- capability-thresholds
date: '2026-09-25'
source:
- LIT-667
summary: >-
  Wang et al. (2024), [LIT-667](../literature.d/LIT-667.md). Composition and comparison are both
  two-fact tasks that both arrive by grokking, and only one of them
  generalizes to facts held out of the training compositions. The difference
  is where the circuit keeps the facts: composition's is **sequential** and
  ends up with a second copy of the atomic facts in the upper layers,
  containing only those that appeared as a second hop; comparison's is
  **parallel** and keeps one copy downstairs. So the failure is not an
  inability to compose — the first hop works on held-out facts — but a
  missing copy, and tying the two halves of the stack together unlocks it.
---

# THEORY-103: A transformer stores a fact where it needed it, so two-hop composition generalizes only to facts it already saw as a second hop

## Source

Wang, Yue, Su and Sun (2024), [LIT-667](../literature.d/LIT-667.md).

## The account

Train a transformer on a mixture of atomic facts and the facts a latent rule
deduces from pairs of them, and it learns to apply the rule — after grokking.
Whether it then applies the rule to atomic facts it *only ever saw atomically*
depends on the shape of the circuit it built, and the shape depends on the
rule.

**Two-hop composition builds a sequential circuit.** `(h, r₁, b)` has to be
resolved before `(b, r₂, t)` can be looked up, so the lower half of the stack
retrieves the first hop and parks the bridge entity, and the upper half
retrieves the second. The second retrieval is a lookup into knowledge that has
to be *in the upper layers*, so the network ends up holding a second copy of
the atomic facts up there. Which facts? Gradient descent has no reason to put a
fact upstairs that was never queried upstairs — so the copy contains exactly
those atomic facts that appeared as a second hop in some training composition,
and nothing else.

**Comparison builds a parallel circuit.** Both operands are independent
lookups, so both happen in the lower layers, and the upper layers only compare
two values and select a label. There is no second copy, so there is nothing for
a held-out fact to be missing from.

That is the whole account, and the consequence is the interesting part: the
out-of-distribution failure on composition is **not** a failure to have learned
the rule, and not a failure of retrieval. It is one absent copy of one fact in
the wrong half of the network.

## What was actually shown

The circuits are traced, not assumed: causal tracing by same-type token
replacement across checkpoints, with logit lens on the individual states. For
composition the surviving graph is layers 0, 5 and 8, with the bridge entity
readable at `S[5, r₁]` and the delayed second relation at `S[5, r₂]`. Two
connection strengths grow during grokking — `S[5, r₁]` to the prediction, and
the `r₂` component of `S[5, r₂]` — which is the second hop forming upstairs.

The prediction that distinguishes this from "the model just cannot compose OOD"
was checked: **in the out-of-distribution setting, `S[5, r₁]` and `S[5, r₂]`
still carry `b` and `r₂` exactly as in distribution.** The first hop works on
facts the model never composed. So whatever is broken is downstream of the
bridge, which is where this account puts it.

And the fix derived from it was run. Tying layers 0–3 to 4–7, after Universal
Transformer, gives the upper layers access to what the lower layers stored —
and **OOD composition goes from flat zero at two million optimization steps to
generalizing**, slowly. A story about where facts are stored predicted that
sharing storage would fix it, and sharing storage fixed it.

## What this does not say

**It is not a claim about depth or capacity.** Scaling the model changed
nothing in these experiments beyond convergence speed. The missing copy is not
missing for want of room.

**It does not explain the frontier-model observations it is consistent with.**
The paper notes that its account would explain why large models show evidence
of performing the first hop of a composition and not the second. That
observation predates the account and was not made under it, so it corroborates
nothing on its own — which is why the `promote_when` rules it out explicitly.

**The evidence is entirely synthetic**, on random knowledge graphs with a
unique token per entity and an 8-layer model. The mechanism is stated in terms
of what gradient descent has an incentive to store, which is general; that
mechanism has so far only been watched in a setting where the experimenter
controls which facts appear in which role.

**The parallel/sequential distinction is a property of the rule, not of the
task name.** Comparison generalizes here because its two lookups are
independent. Nothing in this says a task that *looks* like comparison inherits
that, and nothing says every sequential rule fails — only that a sequential
rule creates a second store, and that the second store is populated by what
training queried from it.

**It is adjacent to, and not the same as, [THEORY-038](THEORY-038.md)**, which says a decoder
cannot compose over a long *context* in few layers because each position
forgets what it forwarded. That is an expressivity bound on in-context
composition. This is an incentive argument about parametric composition: the
circuit exists and works, on the facts it was trained to work on.
