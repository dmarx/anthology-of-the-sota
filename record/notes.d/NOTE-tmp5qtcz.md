---
status: Skimmed
paper: LIT-tmp0lkmx
title: 'Language Design as Information Renormalization'
version: 1
date: '2026-09-25'
summary: >-
  The paper models Chomsky's MERGE as a coarse-graining tensor, so that sentence probabilities form mostly loop-free stochastic tensor networks. It argues from this that tree-like syntax gives polynomially decaying (long-range) correlations. It then concludes that tree-structured networks (it names deep CNNs, as Tree Tensor Networks) fit language, while MPS-like models (RNNs, HMMs) with exponentially decaying correlations do not.
---

<!-- inactive-ok-file: LIT-tmp0lkmx — Deferred: this is the seeded skim of the paper, filed with it on 2026-09-25 -->

# NOTE-tmp5qtcz: Language Design as Information Renormalization

## Contribution

The authors read syntax through physics and argue that MERGE, the operation that combines two syntactic objects into one, is an information coarse-graining, which makes it a renormalization step across time scales. Formalized in a language-model setting, MERGE becomes a probability tensor similar to a probabilistic context-free grammar. The probability vectors of well-formed sentences are then stochastic tensor networks of diagonal tensors, mostly loop-free (tree tensor networks, matrix product states), and so efficient to manipulate. They derive the observed power-law correlations in language from this, argue for certain neural-network types, and use language-model quantum states that a quantum computer could prepare to bound perplexity.

## Skim

*Abstract, figures and selected sections, read when the work was seeded. Not enough to state its assumptions or results exactly; a `Read` note replaces this one.*

- Structure: introduction; the basic MERGE↔renormalization analogy (§II, Figs. 1–4); tensor networks and language (§III: MERGE tensor, syntactic TNs, properties, refinement levels); long-range correlations (§IV); language-model quantum states (§V); perplexity from entanglement (§VI); arbitrary grammars (§VII); implications (§VIII).
- §IV: correlations decay exponentially with *syntactic* distance. Because most syntactic structures are trees, the average syntactic distance grows like log₂|j−i|, so the average correlation decays polynomially with linear distance.
- §VI: an entanglement-based lower bound on perplexity (Eq. 39). The authors stress it is a classical result, and it roughly implies P ≳ (1/p_max)^(n−1): perplexity grows exponentially with sentence length and shrinks as MERGE probabilities sharpen.
- §VIII.A: the "good versus bad" neural-network claim. Deep CNNs are said to be TTNs with the right renormalization structure; RNNs and HMMs are said to be MPS with exponentially decaying correlations and so "bad" at language.

## Open questions

- The strongest ML claim, that RNNs cannot capture language's long-range correlations and tree-structured networks can, is an argument from correlation decay in idealized TN classes. Check whether it applies to real gated RNNs (LSTMs have been shown empirically to capture power-law mutual information, e.g. Lin & Tegmark 2017). The paper predates the dominance of transformers, which it does not address.
- The link between the power law and tree structure is the load-bearing result. Check the averaging assumption behind "d ≈ log₂|j−i|" and whether it is derived or asserted.
- It belongs to the physics-inspired "language as renormalization / tensor network language models" line, relevant to theory-of-why claims in the anthology (a THEORY rather than a practice, if filed).
