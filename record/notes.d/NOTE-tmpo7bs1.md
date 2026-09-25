---
status: Skimmed
paper: LIT-tmps17v1
title: 'Topos and Stacks of Deep Neural Networks'
version: 1
date: '2026-09-25'
summary: >-
  The authors claim that every DNN architecture defines a Grothendieck topos of sheaves over a site built from its graph, that backpropagation is a flow of morphisms in that topos, and that layer invariances (CNN translations, LSTM structure) are stacks, and they conjecture that these stacks explain generalization and support a homological notion of "semantic information".
---

<!-- inactive-ok-file: LIT-tmps17v1 — Deferred: this is the seeded skim of the paper, filed with it on 2026-09-25 -->

# NOTE-tmpo7bs1: Topos and Stacks of Deep Neural Networks

## Contribution

The paper holds that each artificial deep neural network corresponds to an object in a canonical Grothendieck topos, with learning dynamics as a flow of morphisms there. Invariance structures in layers, as in CNNs or LSTMs, are modelled as Giraud stacks, which the authors suppose are responsible for generalization. The fibres carry pre-semantic categories (after Culioli and Thom) over which artificial languages with intuitionist, classical or linear internal logics are defined, and a network's semantic functioning is its ability to express theories in such languages. Semantic information is defined by analogy with the Baudot-Bennequin homological reading of Shannon entropy, generalizing Carnap and Bar-Hillel. These structures are classified by fibrant objects in a Quillen closed model category, organised by Martin-Löf type theory and analysed with Grothendieck derivators.

## Skim

*Abstract, figures and selected sections, read when the work was seeded. Not enough to state its assumptions or results exactly; a `Read` note replaces this one.*

- The authors describe the text as "a mixture of an analysis of the functioning networks, and of a conjectural frame", so its programme is partly speculative by their own account (Preface/Introduction, p. 4).
- Main results they list: Thms 1.1-1.2 characterise the topos of a DNN; Thm 2.1 gives a geometric sufficient condition for "fluid circulation of semantics"; Thms 2.2-2.3 characterise fibrations and fibrant objects in the model category of stacks over a fixed architecture; semantic information is tentatively defined (§3.4-3.5); Thm 4.1 covers the generic structure and dynamics of LSTMs (Introduction, p. 5).
- Construction: the site comes from the network graph with added fork points A*, A for multi-input layers; weights form a sheaf W, and the functioning network is a crossed product X over W, an object of the topos (§1.3).
- Supervised learning is framed as minimising the mean of an energy over weights, with backpropagation as a natural (stochastic) flow of the tangent objects T(X), T(W) (§1.4).
- Related work placed alongside: Fong-Spivak, Shiebler-Gavranović-Wilson's ML-category-theory survey, Manin-Marcolli, sheaf and cosheaf approaches (Ghrist, Curry, Robinson), and Abramsky-Brandenburger (item 75) (Introduction, p. 4).
- Later chapters cover RNN/LSTM/GRU "memories and braids", attention as "moduli" and a 3-category of networks (§4-5).

## Open questions

- The strongest, least-supported claim is that stack invariances are "supposed to be responsible" for generalization. The skim found no empirical test, so check whether any theorem connects the structures to generalization bounds or observed behaviour.
- Check whether Thms 1.1-1.2 say anything beyond "a DAG gives a poset site, and presheaves on it form a topos", i.e. whether the formalism constrains or predicts anything about trained networks.
- ML link: explicit, but foundational rather than practical. It is a candidate theory-of-why for equivariance, and nothing in it tells a practitioner what to do.
