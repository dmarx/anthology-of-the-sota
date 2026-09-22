---
number: 276
status: Read
formerly:
- NOTE-tmp4ho8v
paper: LIT-536
title: 'Order-sensitivity refutes it, and the models everyone measured were trained for the task'
version: 1
date: '2026-09-22'
summary: >-
  Read as the challenge from outside the setup. It separates the hypothesis
  that pretrained models *do* in-context learning by gradient descent from the
  hypothesis that transformer weights *exist* which simulate it, and shows the
  literature had been testing only the second. Theorem 1 then gives a
  contradiction from order sensitivity alone, and LLaMA-7B disagrees with
  fine-tuning on three metrics across four datasets.
---

# NOTE-276: Order-sensitivity refutes it, and the models everyone measured were trained for the task

<!-- inactive-ok-file: THEORY-068 — Rejected, and cited as the rejected account itself: this document is part of the evidence that retired it, not a recommendation resting on it. -->
<!-- inactive-ok-file: SOTA-323 — Proposed, the sibling practice filed in this same contribution and named as its counterpart; it is new, not retired. -->

## Contribution

It names a distinction the field had been eliding, and then attacks the claim
on both a formal and an empirical front. The distinction: a statement about
*emergent* in-context learning in a model pretrained on natural data is not
the statement a construction or an ICL-objective experiment establishes. The
formal attack: any algorithm equivalent to ICL must share its order
sensitivity, and gradient descent does not have any. The empirical attack:
measured on LLaMA-7B, in-context learning and fine-tuning on the same
demonstrations move the output distribution differently.

## Key insight

**"There exist weights such that…" and "pretraining produces weights such
that…" are different claims, and only the first has been proved.** The
constructions are results about architectural expressivity. The experiments
that appear to confirm them train the model on the very task family they then
test, which selects for exactly the inductive bias in question. This is the
paper's Hypothesis 2 versus Hypothesis 1, and it is reusable well beyond
in-context learning.

## Assumptions

- `M` is the family of models arising from causal-language-modelling
  pretraining on natural data; `M̂` the family arising from the ICL objective.
  The relationship between them is, as the paper says, neither clear nor
  discussed in the work it criticizes.
- The empirical comparison fine-tunes on **label loss only**, to match the
  formalism it is testing.
- Sub-model gradient descent (`ĜD`) cannot be located exactly, so two
  **intuitive** subsets are used: `W_V` of one deep layer and `W_V` of one
  middle layer, chosen from the two earlier papers' own claims about where the
  implicit model sits. This is the paper's weakest step and it says so.
- Order sensitivity of ICL is taken from prior work and re-measured here.

## Key results

- **Theorem 1.** If `A` is equivalent to ICL — meaning
  `M_Θ0(S_1 ∘ … ∘ S_N ∘ x_t) = M_{Θ_S}(x_t)` for all inputs — then for two
  demonstration orderings, `M_Θ0(σ_A ∘ x_t) − M_Θ0(σ_B ∘ x_t) =
  M_{Θ_σA}(x_t) − M_{Θ_σB}(x_t)`. Gradient descent averages over the batch, so
  the right side is identically zero; ICL's left side is not. *The proof is one
  subtraction, which is the point: nothing about the architecture is needed.*
  Corollary 1 carries it to the implicit-sub-model version.
- **Measured order sensitivity** (LLaMA-7B, AGNews, standard deviation of the
  output distribution over 10 orderings of 8 demonstrations): ICL stays above
  GD, SGD and Adam across 175 epochs. The Akyürek construction updates one
  example at a time and so *can* be order-sensitive, which is why SGD and Adam
  are included — ICL is still more sensitive than either.
- **Sparsity mismatch.** Reproducing the [ARXIV-2212.07677](https://arxiv.org/abs/2212.07677) construction at
  LLaMA's `N_x = N_y = 4096` requires `> 99.99%` sparsity in `W_K` and `W_Q`
  and about `75%` in `W_V`. Measured sparsity in LLaMA, averaged over layers,
  is far below that at every threshold from `10⁻²` to `10⁻⁶`. Also: `P =
  (η/N)I` diverges at `N = 0`.
- **ICL is a property of a family of weights.** Across GPT-J checkpoints,
  in-context accuracy on AGNews is roughly flat while parameters change
  steadily. Equivalence exhibited at one point in weight space is not the claim.
- **The empirical gap.** LLaMA-7B on AGNews, CB, SST-2, RTE; `N ∈ {1,2,4,8}`;
  learning rates `{1e-3, 5e-3, 1e-4, 5e-4}`; 200 epochs; three metrics
  (accuracy over the whole vocabulary, top-10 **token overlap**, and **overlap
  cosine similarity**). All three show a gap between ICL and every GD and `ĜD`
  variant — and **ICL agrees more with itself under a different demonstration
  order than with any of them**, which is the comparison that makes the
  magnitude interpretable.

## Limitations

**The sub-model probe is a guess.** Identifying the implicit model inside a
real LLM is not feasible by search, so two plausible subsets stand in for it.
A negative result on two guesses is weaker than a negative result on the
thing itself, and the paper does not overclaim here.

**Order sensitivity refutes equivalence, not resemblance.** Theorem 1 kills the
strict functional-equivalence reading. A claim that the forward pass does
something *gradient-like* is not touched by it, and the paper's conclusion —
"remains an open hypothesis" — is the honest one.

**Vanilla GD only**, for the formal argument; the empirical section adds SGD
and Adam.

## Bearing on the record

It is the source of [SOTA-323](../practices.d/SOTA-323.md) — test a claim about what pretraining
produces on a model trained with the pretraining objective — which is the
transferable part and is not specific to in-context learning at all.

It is also the reason [THEORY-068](../theory.d/THEORY-068.md) is `Rejected` rather than left standing:
for real pretrained models the evidence is a contradiction plus a measured
gap, and for ICL-objective models [ARXIV-2310.17086](https://arxiv.org/abs/2310.17086) supplies a separation of
its own. What survives is [THEORY-067](../theory.d/THEORY-067.md), the expressivity claim, which this
paper explicitly leaves intact.

**[DP-007](../../docs/design-principles.md#dp-7).** The gradient-descent reading became consensus without anyone
having tested Hypothesis 1; agreement had no author.

## Open questions

- **Can the implicit sub-model be found rather than guessed?** The paper's
  weakest step is the only one in it that a better method could strengthen.
- **What would count as confirmation?** Neither this paper nor the ones it
  criticizes state a measurement on a naturally pretrained model that would
  settle Hypothesis 1 either way, and the record cannot find one elsewhere.
