---
status: Proposed
promote_when: >-
  The effect measured outside the construction that proves it: agreement
  between distinct state machines tracked against sequence length at an
  alphabet size and state count somebody would actually use — not the cubic
  alphabet the theorem needs — and, separately, a trained sequence model shown
  to do *worse* at recovering a transition structure from longer uniformly
  random inputs than from shorter ones. What would not move it: another
  hardness theorem for another automaton class, which would add a second proof
  about a constructed family and still say nothing about the regime.
title: 'Distinct state machines agree at chance on long random inputs, so a learner that reads only statistics loses the signal as the sequences get longer'
version: 1
tags:
- analysis-and-evaluation
- model-architecture
date: '2026-09-21'
source:
- LIT-tmpzynnf
summary: >-
  Giapitzakis, Fountoulakis, Nichani and Lee (2025), [LIT-tmpzynnf](../literature.d/LIT-tmpzynnf.md) —
  reading a uniformly random word drives a random walk on `S_N × S_N`, and the
  probability two distinct semiautomata land in the same state is
  `1/N + error` with `|error| ≤ (1 − 1/2N)^T`. The quantity that identifies
  which machine you are looking at decays **exponentially in sequence
  length**, so more data of this kind is less evidence, not more.
---

<!-- inactive-ok-file: SOTA-178 — Proposed, cited in "what this does not say"
     to keep an expressivity claim and a learnability claim apart. That is a
     statement about what the two are about, not a reliance on either -->

# THEORY-tmp38xax: Distinct state machines agree at chance on long random inputs, so a learner that reads only statistics loses the signal as the sequences get longer

## Source

Giapitzakis, Fountoulakis, Nichani and Lee (2025),
[LIT-tmpzynnf](../literature.d/LIT-tmpzynnf.md) — read as [NOTE-tmpi0371](../notes.d/NOTE-tmpi0371.md).

## The account

Take two different state machines over the same `N` states, start both in the
same state, and feed both the same uniformly random string of symbols. Early
on they mostly agree — they have not had time to diverge. Late on they agree
`1/N` of the time, which is what two unrelated machines do. The interesting
part is the middle, and specifically how fast the middle ends.

Reading a random symbol is applying a random permutation, so reading a word is
a random walk on pairs of permutations — the group `S_N × S_N`. Whether the
two machines can still be told apart is a question about how far that walk has
mixed, and mixing is governed by a spectral gap. Here the gap is `1/(2N)`, so
the excess agreement above chance is bounded by `(1 − 1/(2N))^T` after `T`
symbols: it decays geometrically, and after about `N² ln N` symbols it is
gone.

**The consequence is what makes this worth filing.** A learner that sees only
statistics of the data — expectations, averages, correlations — is reading
exactly the quantity that is decaying. Longer sequences do not give it a
longer look at the machine; they give it a *more thoroughly stirred* look.
Past the mixing time, every machine in the family looks the same, and the
information was not lost in the model or the optimizer. It was destroyed by
the data.

This runs against the ordinary intuition that a longer context is more
evidence. For a structure that mixes, more of the same random input is
strictly worse, and the crossover is computable from the spectral gap.

The hardness theorem follows: build `N!` machines that are pairwise
indistinguishable in this sense and the statistical dimension is `N!`, so no
Statistical Query learner can separate them with polynomially many queries at
reasonable tolerance. Since SGD with large mini-batches or low-precision
gradients is SQ-equivalent (Abbe et al., 2021, cited by the source and not
proved in it), the shadow this casts over gradient training is real and
unquantified.

## Why `Proposed`

Because the mechanism is proved only where it is convenient. The construction
needs an alphabet of `Ω(N³ ln N)` — millions of symbols for a hundred-state
machine — and transitions drawn as random transpositions, which is the
generating set that makes the Fourier analysis tractable. The mixing argument
itself is sound and general; whether the *rate* is anything like this at an
alphabet of 2 or 256 is not addressed, and that is the only regime anyone
trains in.

The status is about the reach, not the algebra. Every theorem in the source is
proved and one of them is proved tight.

## What this does not say

**It does not say transformers cannot learn state machines.** There are
architectures that track state well and tasks where they do. The claim is
about a constructed family under a uniform input distribution, and the source
is careful to present it as an existence result.

**It does not say long contexts are bad.** It says that for a mixing
structure, longer *uniformly random* inputs carry less identifying
information. Real training data is not uniformly random, and the extent to
which natural sequences mix like this is exactly what nobody has measured.

**It is not an expressivity claim, and confusing the two is the mistake it
exists to prevent.** [SOTA-178](../practices.d/SOTA-178.md) and [THEORY-038](../theory.d/THEORY-038.md) are about
what an architecture can represent. This is about whether gradient descent
finds it. A model can provably represent a machine and provably fail to learn
it, and the record should not read a learnability result as an architecture
verdict or the reverse.

**And the step to gradient descent is borrowed.** SQ hardness becomes SGD
hardness through somebody else's equivalence, which holds with large
mini-batches or low-precision gradients and whose tightness in practice is not
examined here or anywhere the record holds.
