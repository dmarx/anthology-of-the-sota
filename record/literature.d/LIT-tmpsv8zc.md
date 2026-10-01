---
status: Active
title: 'From monoliths to modules: Decomposing transducers for efficient world modelling'
version: 1
# Filed first under model-architecture because no topic named its subject;
# agents-and-environments was added for it and its neighbours (ADR-tmp56fu3).
tags:
- agents-and-environments
- model-architecture
- analysis-and-evaluation
- concept-geometry
date: '2026-10-01'
# v2 (2026-05-20), the version read, adds Fernando E. Rosas as fifth author.
published: '2025-12-01'
arxiv: '2512.02193'
first_author: 'Boyd'
keywords:
- 'world-models'
- 'transducers'
- 'POMDPs'
- 'computational-mechanics'
- 'epsilon-transducers'
- 'causal-states'
- 'modularity'
- 'coarse-graining'
- 'AI-safety'
summary: >-
  Boyd et al. (2025), [ARXIV-2512.02193](https://arxiv.org/abs/2512.02193) — a formal paper with no experiments.
  A world model is a transducer (a stochastic input-output machine with
  latent memory, generalizing POMDPs), and composing transducers is a
  Kronecker product of their operators. The paper inverts this. Two
  information measures, Intransducibility (with latents) and Acausality
  (observables only), are zero exactly when one block of variables can be a
  causal module driven by the rest. Peeling such modules off factors a
  monolithic model into a DAG of sub-transducers that can be learned and
  inferred separately. Minimal predictive models (ε-transducers) are closed
  under composition.
---
<!-- inactive-ok-file: LIT-031 — Superseded, named as the record's existing modularity work and marked superseded where cited -->

# LIT-tmpsv8zc: From monoliths to modules: Decomposing transducers for efficient world modelling

Boyd, Nowak, Hyland, Baltieri and Rosas (2025) — [ARXIV-2512.02193](https://arxiv.org/abs/2512.02193).

## Key takeaways

- **Transducers as the common language.** An interface is a family of
  conditional distributions `Pr(Y₀:t | X₀:t)`. It is causal
  (non-anticipatory) when past outputs do not depend on future inputs.
  Theorem 1: an interface is causal iff some time-invariant transducer, a
  kernel `Pr(Yₜ, Rₜ₊₁ | Xₜ, Rₜ)` over a latent memory `R`, presents it.
  MDPs, POMDPs, factored and decentralized POMDPs and reward machines are
  special cases.
- **Composition is a Kronecker product.** Feeding `T`'s input and output into
  `U` yields a transducer whose operator is `T̂ ⊗ Û`. That product is
  associative but not commutative. Series, parallel ("divergent") and
  convergent wiring are restrictions of it, and the cascade products of
  automata theory embed in it.
- **Decomposition with latents: Intransducibility.** A conditional
  mutual-information sum, Eq. 14, is zero iff `X` can be transduced to `Y`
  through `R` (Lemma 1). Algorithm 1 repeatedly finds a smallest block that is
  a valid module downstream of the rest and peels it off, like factoring an
  integer. The result is an ordered set of "prime" modules, which gives a
  causal ordering of the processes.
- **Decomposition without latents: Acausality.**
  `AC[X⇛Y] = Σₜ I[past Y; future X | past X]` is zero iff a transducer from
  `X` to `Y` exists (Lemma 2), so the same peeling works on observables alone
  (Algorithm 2). Each resulting module `I[X(n) | X(0:n)]` can then be fitted
  independently, and in parallel.
- **Coarse-graining.** Nodes strictly downstream of a block of interest can
  be marginalized out, and a block with no incoming edges can be conditioned
  on, without changing the remaining interface. This extends lumpability from
  Markov chains to transducer networks. A Mars-rover example shows the goal
  deciding which modules can go.
- **Minimality composes (Theorem 2).** The ε-transducer, or causal-state
  model, of a composite interface is the composition of its parts'
  ε-transducers. The authors read this as saying that the belief states of an
  AI system may decompose into interacting belief subspaces rather than one
  monolithic latent.
- **Limits, stated by the authors.** Both measures need joint distributions
  over long histories and can be intractable to estimate. Only feedforward,
  stationary networks are treated: no feedback, no adaptation. And "we have
  focused on formal properties and did not include empirical case studies";
  nothing is run on a trained world model or a neural network.

## Standing in the anthology

Nothing in the record connects to it directly, so it is a seed and not
evidence for anything held. The nearest document is [LIT-215](LIT-215.md) (V-JEPA 2),
whose action-conditioned world model is exactly the monolithic, single-latent
kind this paper proposes to factor. The paper says nothing about learned
latents of that sort and tests nothing on one. The modularity work in the
record is about trained networks' weights ([LIT-031](LIT-031.md), superseded), not about
the environments they model.

Its one claim about neural networks is in §6, and it is borrowed. The
claim rests on work by Shai et al. showing transformers represent the belief
states of a data-generating process in their residual stream. None of that
work is in the record, and filing it would be what turns §6 into something
the concept-geometry shelf could use. That is the reason for the
concept-geometry tag, and it is the weakest of the three.

**Its primary topic is `agents-and-environments`**, added for it and its
neighbours by [ADR-tmp56fu3](../decisions.d/ADR-tmp56fu3.md): when it was filed the vocabulary had no word for
world models and the environments agents act in, and it sat under
`model-architecture`, which stays as a secondary tag because the paper's
claim is about how a world model should be structured.

Unread — no NOTE.
