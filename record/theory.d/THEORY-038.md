---
number: 38
status: Active
formerly:
- THEORY-tmpahhzk
title: 'A decoder cannot compose over a long context in few layers, because each position forgets what it forwarded'
version: 1
tags:
- model-architecture
- analysis-and-evaluation
- in-context-learning
date: '2026-09-21'
source:
- LIT-464
explains:
- SOTA-277
summary: >-
  Chen et al. (2024), [LIT-464](../literature.d/LIT-464.md) — causal masking makes a decoder a
  line of forgetful communicating players, one epoch per layer, and sequential
  composition needs more epochs than a constant-depth model has. An
  unconditional bound on what can be expressed, not on what can be learned.
---

# THEORY-038: A decoder cannot compose over a long context in few layers, because each position forgets what it forwarded

## Source

Chen et al. (2024), [LIT-464](../literature.d/LIT-464.md) — read as [NOTE-214](../notes.d/NOTE-214.md).

## The account

Causal masking is usually described as a training convenience: it is what
makes next-token prediction well-posed. This says it is also a computational
constraint with a price, and names the price.

Model a decoder as players standing on a line, one per chunk of the prompt.
A player may send messages only rightwards. One round of everyone messaging
is one attention layer. The feature that makes the model bind is that the
players are **forgetful**: a player does not retain what it sent. Its own
state is only what it has received.

Sequential composition — apply `f_1` to the query, then `f_2` to that, and so
on — is hard in this game for a reason that survives translation back. To
evaluate `f_2` you must know the output of `f_1`, which lives at a position
that has already spoken. Getting it to where it is needed costs an epoch, and
`k` compositions cost `k` epochs, unless a position carries enough bits to
shortcut — which is what the parameter count buys. So depth and width trade
against each other, and the trade is exponential.

Three things follow, and they are the same fact seen from three sides. Add
layers and you get epochs, so `log k` layers suffice where a constant number
does not. Remove the mask and the bottleneck disappears, so an encoder does
it exponentially smaller. Or let the model write its intermediate results
into the context and read them back, which is what chain of thought is — and
one layer plus `k` such steps suffices.

## What was actually shown

An unconditional lower bound, which is the part that could not have been
assumed. Every prior limitation result for a transformer of more than one
layer rested on a complexity conjecture, and there was a published argument
that this was necessary — that an unconditional bound against an *encoder*
would imply breakthrough circuit lower bounds. That argument is not refuted
here; it is sidestepped, because the proof uses the one thing an encoder does
not have. The bound is a theorem about decoders specifically, and the reason
it exists is the reason encoders escape it.

## What this does not say

**It does not say a trained model fails at composition.** This is a bound on
what a parameter setting can express. Whether gradient descent finds a
composing solution when one exists, and whether a model below the bound fails
on inputs anyone uses, are different questions with no answer here. The paper
offers itself as "theoretical justification" for measured compositional
failure, and that step — asymptotic non-representability to observed error
rate — is one nobody has argued.

**It does not tell you a context length or a parameter count.** The
statement is asymptotic in prompt length. No constant in it is small enough
to bear on a concrete model.

**The hard task is built to be hard.** `k`-sequential function composition
was constructed against this model class. That it is hard is a real fact
about decoders; that anything people train on is hard for the same reason is
not established.

**And it licenses no chain-of-thought recommendation.** Corollary 1.4 says a
one-layer decoder *with* chain of thought can express the composition. It
does not say a model asked to think step by step will do so, nor that
emitting steps helps on any measured task. The record holds no practice
recommending chain of thought at all — [SOTA-127](../practices.d/SOTA-127.md), which says to filter
such traces out of tiny models' training data, is the whole of it — and this
is not the paper to fill that gap with. The gap is named here rather than
filled badly.

## Why `Active`

Because it is a theorem, and because the modelling step it rests on —
simulating a decoder by the communication protocol — is proved rather than
asserted. What is uncertain is its reach into practice, and that uncertainty
is marked above rather than carried in the status: the account of *why*
decoders are constrained is not in doubt; what follows for a model you are
training is.
