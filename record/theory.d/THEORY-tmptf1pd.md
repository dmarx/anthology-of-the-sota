---
status: Active
title: 'A causal mask implicitly encodes absolute position, because a token can count how many predecessors it may attend to'
version: 1
tags:
- representation-and-encoding
- model-architecture
date: '2026-09-25'
source:
- LIT-tmpbi5gf
summary: >-
  Haviv et al. (2022), [LIT-tmpbi5gf](../literature.d/LIT-tmpbi5gf.md). A decoder-only transformer given no
  positional encoding recovers absolute position within four layers, and the
  reason is the mask: a token that can count its attendable predecessors knows
  its index. The account's prediction is that removing the mask removes the
  mechanism, and a bidirectional MLM without an encoding does not merely
  degrade — it fails, at **147.18 perplexity against 4.00**.
---

# THEORY-tmptf1pd: A causal mask implicitly encodes absolute position, because a token can count how many predecessors it may attend to

## Source

Haviv, Ram, Press, Izsak and Levy (2022), `LIT-tmpbi5gf`.

## The claim

Self-attention is permutation-equivariant, so the received account is that a
transformer needs position injected — absolute embeddings, a relative bias,
rotation. For a **causal** transformer that account is incomplete.

A causal mask gives each position a different number of tokens it may attend
to: the first sees one, the second two, the `n`-th sees `n`. If the network can
estimate that count, it has the absolute index at that precision. Nothing needs
to be added, because the constraint is already positional information —
**the mask is an encoding that nobody wrote down as one.**

The paper's phrasing: *"the causal attention… allows them to predict the number
of attendable tokens at each position."*

## What it explains

**That NoPos models work at all**, which is otherwise surprising: gaps of 0.05
perplexity from learned embeddings at 1.3B on the Pile.

**Where the position appears.** Absent at layer 1, on par with a random
baseline — correctly, since nothing was supplied. Recovered **within four
layers**, and by the middle layer as accurate as a model with learned
embeddings. That is the shape a *computed* quantity has and not the shape an
*injected* one has, which would be present at layer 1 and decay.

**That the recovered position matters.** Shuffling the suffix moves average
token-level loss from ~4 to ~11.

## Why it is `Active`

Because the account predicted a failure and the failure was produced.

The mechanism is the mask, so it should not survive removing the mask. A
bidirectional encoder trained on masked language modelling has no such
constraint. RoBERTa-large architecture, the Pile, 128 tokens:

| encoding | MLM perplexity |
| --- | --: |
| Learned | 4.06 |
| Sinusoidal | 4.07 |
| ALiBi | 4.00 |
| **NoPos** | **147.18** |

**Thirty-six times worse.** Not a degradation — a failure to train. The
conjecture's one falsifiable consequence was tested in the same paper and came
out as the account requires, and Sinha et al. (2021) had independently seen the
MLM degradation.

The record has decided a status on one source this way before
(`THEORY-101`), and the standard is the same: **a successful intervention
derived from the hypothesis, not a correlation consistent with it.**

## What it does not settle

**The counting mechanism is not localised.** Nobody has shown a head or a
circuit doing the counting. The evidence is that position is recoverable by a
probe and that it disappears when the mask does; the intermediate step —
*this* is the computation — is a conjecture, and the paper calls it one.

**It does not say the encoding is redundant.** NoPos is *"always slightly
worse"* by the authors' own summary, and smaller models benefit measurably from
fixed non-parametric encodings with the gap closing as scale grows. The
mechanism supplies position; it does not supply the inductive bias an explicit
encoding also carries.

**It says nothing about relative position**, which is what rotary and ALiBi
encode and what most of the record's cluster is about. `LIT-207` reports that a
NoPos decoder represents relative position too; that is a separate finding and
this account does not reach it.

**Precision is unquantified.** "Counting predecessors" would give exact
indices; a probe recovering position "about as well as learned embeddings" is
not the same statement, and no error bound is given for what the mask can
resolve at long range.

## What rests on it

`SOTA-153` drops positional encoding from the global-attention layers of a
hybrid. This account is why that is possible at all, and it also draws the
boundary: the mechanism is causal, so it is available to a decoder and not to
an encoder, and it is recovered over the first few layers rather than present
at the input.

The second half matters for a layout decision. A hybrid choosing which layers
may go without an encoding is choosing among layers that differ in how much
implicit position has accumulated by the time they run — and no document in
this record, including this one, says what that does.
