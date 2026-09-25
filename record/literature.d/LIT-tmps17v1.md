---
status: Deferred
status_note: seeded from the abstract and a skim on 2026-09-25; not read in full
title: 'Topos and Stacks of Deep Neural Networks'
version: 1
tags:
- model-architecture
- concept-geometry
date: '2026-09-25'
published: '2021-06-01'
arxiv: '2106.14587'
first_author: 'Belfiore'
keywords:
- 'topos theory'
- 'stacks'
- 'deep neural networks'
- 'semantic information'
- 'homotopy theory'
implementations: []
summary: >-
  Belfiore et al. (2021), [ARXIV-2106.14587](https://arxiv.org/abs/2106.14587). The authors claim that every DNN architecture defines a Grothendieck topos of sheaves over a site built from its graph, that backpropagation is a flow of morphisms in that topos, and that layer invariances (CNN translations, LSTM structure) are stacks, and they conjecture that these stacks explain generalization and support a homological notion of "semantic information".
---

# LIT-tmps17v1: Topos and Stacks of Deep Neural Networks

Jean-Claude Belfiore, Daniel Bennequin (2021), *arXiv preprint* — [ARXIV-2106.14587](https://arxiv.org/abs/2106.14587)

## Key takeaways

- The authors claim that every DNN architecture defines a Grothendieck topos of sheaves over a site built from its graph, that backpropagation is a flow of morphisms in that topos, and that layer invariances (CNN translations, LSTM structure) are stacks, and they conjecture that these stacks explain generalization and support a homological notion of "semantic information".

*Seeded from the abstract and a skim, not a reading. What follows is what the work says about itself.*

The paper holds that each artificial deep neural network corresponds to an object in a canonical Grothendieck topos, with learning dynamics as a flow of morphisms there. Invariance structures in layers, as in CNNs or LSTMs, are modelled as Giraud stacks, which the authors suppose are responsible for generalization. The fibres carry pre-semantic categories (after Culioli and Thom) over which artificial languages with intuitionist, classical or linear internal logics are defined, and a network's semantic functioning is its ability to express theories in such languages. Semantic information is defined by analogy with the Baudot-Bennequin homological reading of Shannon entropy, generalizing Carnap and Bar-Hillel. These structures are classified by fibrant objects in a Quillen closed model category, organised by Martin-Löf type theory and analysed with Grothendieck derivators.

## Standing in the record

Filed by the reading-time triage of 2026-09-25: 665 seconds of active reading over 2 sessions in the papers-feed tracker. `Deferred` because nobody has read it closely here yet, not on merit.

It was one of the triage's out-of-scope works, and it is filed here rather than in the catchall record, nucleation, because it sits on the boundary and the rule for the boundary is to keep it in the anthology. It is a mathematical account of what a network architecture lets information and semantics do, which no anthology document yet holds.

**Priority for a deeper reading: medium — the only ML-facing work in this batch and connected to item 75, but it is 152 pages of largely conjectural category theory; read Ch. 1 and the §3.4 definitions of semantic information, and skip the rest unless those deliver a checkable claim (t=665 s).**

What a deeper reading should check:

- The strongest, least-supported claim is that stack invariances are "supposed to be responsible" for generalization. The skim found no empirical test, so check whether any theorem connects the structures to generalization bounds or observed behaviour.
- Check whether Thms 1.1-1.2 say anything beyond "a DAG gives a poset site, and presheaves on it form a topos", i.e. whether the formalism constrains or predicts anything about trained networks.
- ML link: explicit, but foundational rather than practical. It is a candidate theory-of-why for equivariance, and nothing in it tells a practitioner what to do.

Access when seeded: arXiv abs page and full PDF (152 pp.) retrieved; read abstract, contents, Preface/Introduction (pp. 4-5, including the list of main results) and the start of §1.4 (backpropagation as a flow in the topos). A Crossref search found no journal version of this text; the same authors have a related 2025 book chapter "Toward a Theory of Semantic Information" (DOI 10.1002/9781394247912.ch3) that was not examined. Theorems and proofs were not checked.
