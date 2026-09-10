---
number: 70
# inactive-ok: LIT-092 — Rejected, and this document is the reading that says why the paper is in the attic and what survives it
paper: LIT-092
status: Read
formerly:
- NOTE-tmpwrx2y
title: 'Understanding Contrastive Learning Requires Incorporating Inductive Biases'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-09'
published: '2022-02-01'
summary: >-
  Shows that theoretical guarantees for contrastive learning that depend only on the augmentations and the loss value cannot explain why it works, and are provably vacuous in some settings. Different function classes and algorithms behave very differently downstream given identical augmentations and identical contrastive loss.
---

# NOTE-070: Understanding Contrastive Learning Requires Incorporating Inductive Biases

## Contribution

A negative result about a class of theory. Several analyses of contrastive
learning prove downstream guarantees as a function of two things: properties of
the augmentation distribution, and the value of the contrastive loss achieved.
This paper shows that framing **cannot be right** — and in some settings the
guarantees it produces are **vacuous**.

The demonstration is empirical as well as formal: across image and text
domains, "different function classes and algorithms behave very differently on
downstream tasks, despite having the same augmentations and contrastive losses."

## Key insight

If two setups agree on every quantity a bound depends on and disagree on the
outcome the bound is about, the bound is not explaining the outcome. That is the
whole argument, and it is decisive.

The paper formalises prior analyses through an abstraction it calls a **transfer
function `T`**, which maps contrastive-loss performance to downstream
performance, and shows that any such function — one taking only loss and
augmentations as input — must be loose enough to be uninformative, because the
real dependence is on the function class and the optimisation algorithm.

The positive half: for **linear representations**, incorporating the function
class's inductive bias lets contrastive learning be shown to work under **less
stringent conditions** than the augmentation-only analyses require. So the fix is
not to abandon theory but to admit the inductive bias into it.

## Assumptions

- Prior analyses are fairly captured by the transfer-function abstraction — the
  paper's own framing of Arora et al., Tosh et al. and HaoChen et al.
- The positive result is for linear representations, which is where the analysis
  is tractable and not where contrastive learning is used.

## Key results

- **Augmentation-and-loss-only guarantees are vacuous in some settings**, shown
  formally.
- **Extensive experiments across image and text** with matched augmentations and
  matched contrastive loss, and diverging downstream performance — the ubiquity
  claim.
- **For linear representations**, incorporating inductive bias yields guarantees
  under weaker conditions than prior analyses.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Guarantees depending only on augmentations and loss cannot explain contrastive learning's success | strong | formal, plus matched-setup experiments |
| C2 | Such guarantees are provably vacuous in some settings | strong | shown |
| C3 | The problem is ubiquitous across function classes and algorithms | strong | image and text, several classes |
| C4 | Including inductive bias gives better conditions, at least for linear representations | moderate | proved in a tractable case |

## Method

Abstract prior analyses as a transfer function from contrastive loss to
downstream performance. Construct settings where it must be vacuous. Empirically
match augmentations and contrastive loss across function classes and algorithms
and measure downstream divergence. Prove a bias-aware result for linear
representations.

## Concepts

- **The matched-setup falsification** — hold constant everything a theory
  depends on, vary what it ignores, and see whether the outcome moves. A general
  and cheap way to test whether an explanation is doing work.
- **Transfer function** — a useful abstraction for "what does this bound
  actually take as input".
- **Inductive bias as a required term**, not a nuisance.

## Connections

The record's `LIT-018` (`On the Convergence of Adam and Beyond`), read in batch
A, is the same genre from the other direction: there a proof was *wrong*, here a
whole class of proofs is *insufficient*. Both are cases of a formal result not
settling the empirical question, and both are worth carrying for that.

<!-- inactive-ok-block: LIT-057, LIT-044 — Rejected, and named as a paper this one argues with; each has its own reading saying why it is in the attic -->
`LIT-057` and `LIT-044`, read in the same batch, are exactly the kind of work
this paper's argument bears on — both reason about augmentation design and the
contrastive objective, and this says that reasoning cannot by itself predict the
downstream outcome.

## Recommendations

- **R1** — To test whether an explanation explains, hold fixed everything it
  depends on and vary what it ignores. *Topic:* analysis and evaluation.
  *Strength:* strong, and the most portable thing here.
- **R2** — Distrust a guarantee that does not mention the function class or the
  optimiser. *Strength:* strong for this literature; the general form is a good
  prior.
- **R3** — When a bound is loose, check whether it is *vacuous* before treating
  it as conservative. *Strength:* moderate.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice**, and the
document is `Rejected`. The reading does not argue with that: contrastive
representation learning is not a line this anthology tracks, and the positive
result is for linear models.

R1 is why it is still worth having read. The record contains many claims of the
form "X works because of Y", and this paper demonstrates the cheapest available
test of such a claim — **match everything Y covers, vary what it does not, and
see whether the outcome follows Y**. That is a method, not a result, and it
transfers to any explanation the anthology carries.

The document's takeaways — "role of inductive biases", "theoretical analysis",
"augmentation strategies", "performance bounds" — name the paper's ingredients
without its conclusion, which is that a class of existing bounds **does not
work**. A reader would take from those bullets that the paper is *about*
performance bounds rather than *against* a family of them.

## Limitations

- Contrastive learning specifically; the general claim is by analogy.
- C4 is for linear representations, which is a tractability choice.
- The paper diagnoses and does not supply a usable bias-aware theory for
  realistic function classes.

## Open questions

- What would a guarantee that includes the optimiser even look like? The paper
  establishes it is necessary and gets one only in the linear case.
