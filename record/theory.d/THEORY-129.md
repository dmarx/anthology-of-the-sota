---
number: 129
status: Proposed
formerly:
- THEORY-tmpszvjk
promote_when: >-
  Two kinds of result. One is an independent check of the separation proofs
  (Olmo Hybrid, App. B): the positive constructions and the two negative
  lemmas, the circuit-complexity one for transformers and the
  communication-complexity one for bounded-state recurrences. The other is a
  synthetic test that could separate expressivity from learnability: a
  transformer arm that solves state-based recall at small n and fails only
  as n grows, beside a hybrid that does not fail. A further hybrid winning
  where the transformer already fails at n = 4 would not count, because
  depth is not the binding limit at four swaps.
title: 'Interleaving attention with a negative-eigenvalue delta-rule recurrence expresses problems neither layer type can express alone, because state tracking and recall come from different layers and one alternation composes them'
version: 1
tags:
- model-architecture
- attention-techniques
- analysis-and-evaluation
date: '2026-10-06'
source:
- LIT-799
explains:
- SOTA-132
summary: >-
  Merrill et al. (2026), [LIT-799](../literature.d/LIT-799.md), §3.3–3.4 and App. B. Fixed-depth
  transformers lie in TC⁰ and cannot track state (if TC⁰ ≠ NC¹).
  Bounded-state recurrences cannot recall from a long context. A Gated
  DeltaNet with negative eigenvalues tracks state, and attention recalls.
  One alternation of the two solves state-based recall, which neither can
  alone, and with padding a hybrid recognizes all of NC¹. The proofs are
  conditional on a complexity conjecture. The synthetic evidence does not
  separate expressivity from learnability, and the account does not say the
  expressive gap is what makes hybrids better language models.
---

<!-- inactive-ok-file: THEORY-126, SOTA-178 — Proposed, named as the
     separate scaling account and the neighbouring practice, not relied on -->

# THEORY-129: Interleaving attention with a negative-eigenvalue delta-rule recurrence expresses problems neither layer type can express alone, because state tracking and recall come from different layers and one alternation composes them

## Source

Merrill, Li, Romero, Svete, Costello et al. (2026), [LIT-799](../literature.d/LIT-799.md) — Olmo
Hybrid, §3.1–3.5, Theorems 1 and 3, Corollary 3.1, App. B and C.

## The account

**Each parent has a hole the other fills.** A fixed-depth transformer used as
a next-token predictor computes only functions in TC⁰. Hard state tracking,
such as composing swaps over five objects, is NC¹-complete. So, if TC⁰ ≠ NC¹,
no transformer of fixed depth tracks state over arbitrary lengths. A linear
recurrence with a non-diagonal, input-dependent transition can track state.
Gated DeltaNet can do it once its transition I − 2βkkᵀ is allowed an
eigenvalue of −1, which makes a swap expressible. But a recurrence with a
bounded state cannot recall an arbitrary bit from a long array: that needs
memory growing with the array, a communication-complexity argument.

**Composing them is more than having both.** State-based recall tracks five
pointers through n swaps and then reads the bit one of them points to.
Theorem 1 gives two hybrid solutions, each with one alternation of layer
types. GDN can compose the swaps and attention then retrieve the bit, or
attention can retrieve the five candidate bits and GDN then permute them.
Neither parent alone can do both halves, so the hybrid expresses something
neither does.

**With padding, the gap is a whole complexity class.** Barrington's theorem
reduces any NC¹ problem, by a first-order formula, to composing permutations
of five elements. Padded attention can compute the reduction, and GDN can
compose the permutations. So padded hybrids recognize all of FO-uniform NC¹,
while padded transformers recognize exactly TC⁰ (Theorem 3). Boolean formula
evaluation is the named example.

## What was measured

- **Synthetic tasks** (§3.5, Tables 15–17). Olmo Hybrid ([LIT-799](../literature.d/LIT-799.md))
  trained 4-layer models, best run of a
  sweep. Here "hybrid" means three GDN layers followed by one attention
  layer. State tracking at n = 128: transformer 0.23, GDN 1.00, hybrid 1.00.
  Recall at m = 128: transformer 0.96, GDN 0.68, hybrid 1.00. State-based
  recall at n = m = 128: transformer 0.54, GDN 0.64, hybrid 1.00.
- **Negative eigenvalues are what the recurrent half needs.** Without them,
  pure GDN falls to 0.22 on state tracking at n = 64, and the hybrid falls to
  0.36 at n = 128 and to 0.57 on state-based recall. Recall is unaffected.
  That matches which half of the account depends on the eigenvalue.

## What this does not say

- **Not that the result is unconditional.** The transformer half rests on
  TC⁰ ≠ NC¹. That is the standard conjecture, but it is unproved.
- **Not that the synthetic curves measure expressivity.** The transformer
  scores 0.51 at n = 4 and 0.28 at n = 8 on state tracking. Four swaps are
  well within what a 4-layer transformer can express, so those failures are
  about learning under this curriculum, not about depth. The separation at
  large n is consistent with the account. It is not a test of it.
- **Not that this is why hybrids are better language models.** That further
  step is the paper's scaling argument, filed separately
  ([THEORY-126](THEORY-126.md)). Its own ablations weaken it: a hybrid without negative
  eigenvalues, which cannot track state, scales about as well.
- **Not that interleaving many times beats alternating once.** One
  alternation suffices for both theorems. The authors leave open whether
  more alternations add expressive power. The placement ablation that
  favours interleaving is a language-modelling result, by 0.003 BPB at 1B,
  and it is not evidence for this account.

## What it explains

Why the hybrid layout in [SOTA-132](../practices.d/SOTA-132.md) keeps global attention in the minority
layers, not local attention: recall over the whole context is the half a
bounded-state recurrence lacks. It also explains why the recurrent layer's
transition matters. A decay-only layer such as Mamba-2's, with nonnegative
real eigenvalues, cannot supply the state-tracking half, and Olmo Hybrid's
Mamba-2 hybrid was the weakest hybrid it trained. This is the record's
first formal account of what the two layer types contribute. [SOTA-178](../practices.d/SOTA-178.md), from
the RWKV-7 side, makes the same kind of claim: that a recurrence with richer
gating can track state that a softmax layer provably cannot.
