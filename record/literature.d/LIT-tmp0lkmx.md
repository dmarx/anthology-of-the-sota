---
status: Deferred
status_note: seeded from the abstract and a skim on 2026-09-25; not read in full
title: 'Language Design as Information Renormalization'
version: 1
tags:
- signal-structure
date: '2026-09-25'
published: '2017-08-01'
arxiv: '1708.01525'
doi: '10.1007/s42979-021-01002-y'
first_author: 'Gallego'
keywords:
- 'MERGE'
- 'renormalization'
- 'tensor networks'
- 'language models'
- 'perplexity'
implementations: []
summary: >-
  Gallego et al. (2022), [ARXIV-1708.01525](https://arxiv.org/abs/1708.01525). The paper models Chomsky's MERGE as a coarse-graining tensor, so that sentence probabilities form mostly loop-free stochastic tensor networks. It argues from this that tree-like syntax gives polynomially decaying (long-range) correlations. It then concludes that tree-structured networks (it names deep CNNs, as Tree Tensor Networks) fit language, while MPS-like models (RNNs, HMMs) with exponentially decaying correlations do not.
---

# LIT-tmp0lkmx: Language Design as Information Renormalization

Angel J. Gallego, Román Orús (2022), *SN Computer Science (vol. 3, art. 140)* — [ARXIV-1708.01525](https://arxiv.org/abs/1708.01525)

## Key takeaways

- The paper models Chomsky's MERGE as a coarse-graining tensor, so that sentence probabilities form mostly loop-free stochastic tensor networks. It argues from this that tree-like syntax gives polynomially decaying (long-range) correlations. It then concludes that tree-structured networks (it names deep CNNs, as Tree Tensor Networks) fit language, while MPS-like models (RNNs, HMMs) with exponentially decaying correlations do not.

*Seeded from the abstract and a skim, not a reading. What follows is what the work says about itself.*

The authors read syntax through physics and argue that MERGE, the operation that combines two syntactic objects into one, is an information coarse-graining, which makes it a renormalization step across time scales. Formalized in a language-model setting, MERGE becomes a probability tensor similar to a probabilistic context-free grammar. The probability vectors of well-formed sentences are then stochastic tensor networks of diagonal tensors, mostly loop-free (tree tensor networks, matrix product states), and so efficient to manipulate. They derive the observed power-law correlations in language from this, argue for certain neural-network types, and use language-model quantum states that a quantum computer could prepare to bound perplexity.

## Standing in the record

Filed by the reading-time triage of 2026-09-25: 625 seconds of active reading over 2 sessions in the papers-feed tracker. `Deferred` because nobody has read it closely here yet, not on merit.

It was one of the triage's out-of-scope works, and it is filed here rather than in the catchall record, nucleation, because it sits on the boundary and the rule for the boundary is to keep it in the anthology. It argues from the correlation structure of language to which architectures can carry it, which is a claim about the signal before it is a claim about any model.

**Priority for a deeper reading: medium — It is the one ML-adjacent item in this batch and makes a strong, checkable architectural claim. t = 625 s is modest, and the skim gives the argument but not the rigour of §III–§VI.**

What a deeper reading should check:

- The strongest ML claim, that RNNs cannot capture language's long-range correlations and tree-structured networks can, is an argument from correlation decay in idealized TN classes. Check whether it applies to real gated RNNs (LSTMs have been shown empirically to capture power-law mutual information, e.g. Lin & Tegmark 2017). The paper predates the dominance of transformers, which it does not address.
- The link between the power law and tree structure is the load-bearing result. Check the averaging assumption behind "d ≈ log₂|j−i|" and whether it is derived or asserted.
- It belongs to the physics-inspired "language as renormalization / tensor network language models" line, relevant to theory-of-why claims in the anthology (a THEORY rather than a practice, if filed).

Access when seeded: The arXiv abs page and the full PDF of the final arXiv version (25 pp.) were both reachable. arXiv's journal-ref is "SN Comput. Sci. 3, 140 (2022)", and Crossref confirms the DOI (published 2022-01-21). I read the abstract, the section heads, §IV (long-range correlations), §VI (perplexity bound) and §VIII.A (implications for neural networks). arXiv subjects are cs.CL, cond-mat.str-el, physics.hist-ph and quant-ph. The keywords above are mine.
