---
number: 24
status: Proposed
formerly:
- THEORY-tmpm3lav
title: 'Orthogonalising the update is dualising it, and muP and Shampoo are two partial approximations of the same duality map'
version: 2
history:
- version: 2
  date: '2026-09-20'
  note: >-
    Demoted from `Active` to `Proposed`. This document closed by saying all
    three of its sources share authors and that it was `Active` "not because
    anyone outside has confirmed the frame." Shumaylov et al. (LIT-456)
    are the first outside group to test the frame, and they come back
    negative on its explanatory force: an optimizer that replaces the
    gradient's singular values with chaotic noise matches Muon. The
    derivation is untouched and no text has been removed; a section records
    what the test reaches and `promote_when` says what would restore the
    status.
promote_when: >-
  An outside replication of the Kaon control at a scale where the record's
  Muon practices are evidenced — a billion parameters or more — in which
  the geometry-free optimizer does NOT match Muon. That is the result the
  duality frame predicts and the small-scale control denies, and it is the
  one that would put this back to `Active`. What would not settle it:
  another derivation showing some further optimizer is a steepest-descent
    step under some norm. The contested claim is that the geometry is what
  pays, and reformulating the geometry does not test it.
tags:
- training-optimization
date: '2026-09-19'
source:
- LIT-438
- LIT-436
- LIT-437
explains:
- SOTA-121
- SOTA-143
- SOTA-168
summary: >-
  Bernstein and Newhouse (2024), [LIT-438](../literature.d/LIT-438.md) — gradients are dual vectors
  and weights are primal, so the subtraction in gradient descent needs a
  duality map. Build it recursively from per-layer operator norms and the
  Linear case is a Newton-Schulz iteration, which is what Muon does. The same
  construction shows muP and Shampoo are partial approximations of one map.
---

<!-- inactive-ok-file: SOTA-168 SOTA-121 SOTA-143 — the three practices this account explains; SOTA-168 is Proposed and is cited as one of the two approximations, not as a settled recommendation -->
<!-- inactive-ok-file: THEORY-033 THEORY-032 ADR-034 — the two rival accounts and the decision that keeps all three off the practices, all Proposed, all named in the v2 section rather than leaned on -->

# THEORY-024: Orthogonalising the update is dualising it, and muP and Shampoo are two partial approximations of the same duality map

## What it explains

Three practices the record recommends and could not account for:

| practice | what it says to do | what this says it is |
|---|---|---|
| [SOTA-121](../practices.d/SOTA-121.md) | use Muon — orthogonalise the update | applying the duality map for the spectral norm |
| [SOTA-143](../practices.d/SOTA-143.md) | parameterize with muP | a partial approximation of that map |
| [SOTA-168](../practices.d/SOTA-168.md) | run Adam in Shampoo's eigenbasis | the other partial approximation of it |

## The account

Gradients are **dual vectors** and weights are **primal**. Subtracting one
from the other — which is what `weight -= LR * grad` does — is a type error
that only looks harmless because the Euclidean norm makes the two spaces
identifiable. Choose a different norm and the identification fails, and the
correct update is `weight - LR * dualize(grad)`.

**Modular dualization** builds that map for a whole architecture in three
steps: assign each layer an operator norm *from its input-output semantics*,
derive that layer's duality map from the norm, then recurse over the
architecture. For `Linear` and `Conv2D` layers the map is computed by a
rectangular Newton-Schulz iteration — which is precisely the operation Muon
performs on the update.

So the sequence of the record's optimizer cluster inverts. Muon is not a trick
that turned out to work and later acquired a rationalisation; it is the
duality map for a particular norm, and the blog post that introduced it
([LIT-159](../literature.d/LIT-159.md)) came out of the same group's work on this theory.

## Why the unification is the load-bearing part

[LIT-438](../literature.d/LIT-438.md) §4.1 shows that **maximal update parametrization and Shampoo
both emerge as partial approximations to a single duality map** — the one
induced by the RMS–RMS operator norm. The paper's own framing is that these
are "important and seemingly disparate" methods, one aimed at scalable
training and the other at fast training.

The record recommends both, in `SOTA-143` and `SOTA-168`, filed from different
literatures at different times, with nothing connecting them. That they are
one object seen from two sides is the kind of claim `THEORY` exists to hold:
it changes nothing about either recommendation and changes what a reader
understands when they meet the second one.

## The supporting line

- [LIT-437](../literature.d/LIT-437.md) — feature learning follows from scaling the **spectral**
  norm of weights and updates like `sqrt(fan-out/fan-in)`, not from Frobenius
  or entry-size heuristics, and muP falls out of it elementarily. This is why
  the spectral norm is the quantity in play at all
- [LIT-436](../literature.d/LIT-436.md) — the **modular norm**, defined recursively alongside the
  architecture, against which the dualization is performed. Normalising any
  base optimizer's updates in it makes the learning rate transferable across
  width *and* depth

## What it does not explain

**The constants.** `SOTA-121`'s decoupled weight decay and AdamW-matched
update RMS, and `SOTA-131`'s QK-Clip for attention-logit growth at a trillion
parameters, are engineering this theory does not reach. It says the *shape* of
the update is right; it does not say what to set.

**Nor does it settle whether the norm assignment is correct.** Choosing an
operator norm from a layer's semantics is the paper's substantive modelling
move, argued rather than derived. A different assignment yields a different
optimizer, and the theory tells you what follows from a choice rather than
fixing the choice.

**And it is one group.** All three papers share authors, and `ADR-010`'s
neighbouring caution applies: a line agreeing with itself is not replication.
It was `Active` because the argument is checkable and the practices it
explains are independently evidenced, not because anyone outside had
confirmed the frame. At v2 somebody did, and the section below is what they
found.

## What an outside test found, and what it reaches

*(Added at v2.)* The paragraph above rests the `Active` status on the
argument being checkable and the practices being independently evidenced —
not on anyone outside having confirmed the frame. Shumaylov et al.,
[LIT-456](../literature.d/LIT-456.md), are the first outside group to look, and what they
built is the control this frame never had.

`Kaon` replaces the gradient's singular values with noise from a chaotic
recurrence. It computes no linear minimization oracle, dualizes nothing, and
targets no norm — and on NanoGPT it matches Muon. Two smaller results point
the same way: `TruncatedSGD` shows that suppressing the large singular values
is necessary and not sufficient, and the best exponent in the Schatten family
on GPT-2 sits strictly in the quasi-norm regime, where Theorem 2.1 of that
paper says no update can be steepest descent for any unitarily invariant
norm.

**What this reaches and what it does not.** The derivation here is
mathematics: that Muon's Newton–Schulz step *is* the duality map for the
spectral norm, and that muP and Shampoo fall out of one construction, are not
claims an experiment can touch. What the experiment reaches is the sentence a
reader takes away — that being the duality map is *why* Muon works. An
account that cannot distinguish its object from a randomized control is not,
on that evidence, doing the explanatory work. Hence `Proposed` rather than
`Rejected`: the frame may still be right, and it has stopped being the thing
the record can point to.

The counter-evidence is NanoGPT and WikiText-2 at 118M tokens against
practices demonstrated from 90M to 1.6T parameters, and that asymmetry is
why the demotion stops where it does. [THEORY-033](../theory.d/THEORY-033.md) holds the
account the controls leave standing; [THEORY-032](../theory.d/THEORY-032.md) holds a third,
from an unrelated group, that reaches the same practices through rank
structure rather than geometry. None of the three touches
[SOTA-121](../practices.d/SOTA-121.md), [SOTA-143](../practices.d/SOTA-143.md) or [SOTA-168](../practices.d/SOTA-168.md), which is
[ADR-034](../decisions.d/ADR-034.md)'s point exactly.
