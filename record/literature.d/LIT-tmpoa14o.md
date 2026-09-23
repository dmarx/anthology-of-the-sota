---
status: Active
title: 'The Linear Representation Hypothesis and the Geometry of Large Language Models'
version: 1
tags:
- concept-geometry
- analysis-and-evaluation
date: '2026-09-23'
published: '2023-11-01'
arxiv: '2311.03658'
first_author: 'Park'
keywords:
- 'linear-representation-hypothesis'
- 'causal-inner-product'
- 'unembedding'
- 'linear-probe'
- 'steering-vector'
- 'counterfactual-pairs'
implementations: []
summary: >-
  Park, Choe and Veitch (ICML 2024), [ARXIV-2311.03658](https://arxiv.org/abs/2311.03658). "Concepts are
  directions" has three readings: a shared difference between word pairs, a
  linear probe, and a steering vector. The paper formalizes the first with
  counterfactual pairs in the unembedding and embedding spaces, and proves
  the first is a probe and the second a steering vector. Training identifies
  the representation only up to an invertible linear map, so Euclidean cosine
  has no special meaning. An inner product under which causally separable
  concepts are orthogonal unifies the two spaces, and one such product is the
  inverse covariance of the unembedding rows. Evidence is 27 concepts on
  LLaMA-2 7B, with a Gemma-2B comparison in the appendix.
compared_against:
- LIT-526
extended_by:
- LIT-460
---

# LIT-tmpoa14o: The Linear Representation Hypothesis and the Geometry of Large Language Models

Park, Choe and Veitch, University of Chicago (ICML 2024) — [ARXIV-2311.03658](https://arxiv.org/abs/2311.03658).
Code: `github.com/KihoPark/linear_rep_geometry`.

## Key takeaways

- **Three things go by the one name** (§1). *Subspace*: queen − king and
  woman − man share a direction. *Measurement*: a linear probe reads the
  concept off the representation. *Intervention*: adding a vector changes the
  concept and nothing else. Before this paper nothing said how the three
  relate.
- **Concepts are defined causally** (§2.1). A concept is a latent variable
  the context causes and the output depends on, specified by counterfactual
  output pairs (king/queen, roi/reine). Two concepts are *causally separable*
  when they can vary freely of each other: English⇒French and male⇒female
  are, English⇒French and English⇒Russian are not.
- **Two spaces, two theorems.** In the unembedding (output word) space, a
  concept's direction is the one all its counterfactual pair differences lie
  along, and it is exactly a logit-linear probe for the concept (Thm 2.2). In
  the embedding (context) space, the direction is exactly a steering vector
  that moves the concept and leaves every separable concept's probability
  unchanged (Thm 2.5).
- **The inner product is not identified by training** (§3). The softmax is
  unchanged if unembeddings are multiplied by any invertible A and embeddings
  by A⁻ᵀ, so any fixed inner product, the Euclidean one included, can be made
  to say anything about similarity.
- **Pick the inner product under which separable concepts are orthogonal**
  (Def 3.1). Such a *causal inner product* maps each concept's unembedding
  direction onto its embedding direction (Thm 3.2), so probes and steering
  vectors become one object. If a randomly drawn *vocabulary word's* values on
  two separable concepts are uncorrelated, the causal inner products are
  exactly those with M⁻¹ = GGᵀ, and choosing D = I gives
  ⟨γ̄, γ̄′⟩ = γ̄ᵀ Cov(γ)⁻¹ γ̄′ (Thm 3.4).
- **Experiments on LLaMA-2 7B.** 22 BATS relations, four language pairs and
  frequent⇒infrequent, restricted to single-token words. Counterfactual
  differences project onto their leave-one-out concept direction far more
  than random pairs do, for 26 of 27 concepts. thing⇒part is the exception
  (Fig 2, App D.1). Under the whitened product the 27 directions are nearly
  orthogonal, apart from blocks of related concepts (Fig 3). The
  French⇒Spanish direction separates French from Spanish Wikipedia contexts
  (Fig 4). Adding Cov(γ)⁻¹γ̄ for male⇒female to "Long live the" moves "queen"
  to the top of the next-token distribution by α = 0.2 (Table 1).

## Standing in the anthology

**This is the trunk the record's concept-geometry filings kept pointing at.**
[LIT-460](LIT-460.md) (the lattice hypothesis) and [THEORY-034](../theory.d/THEORY-034.md) build half-spaces on these
directions. [LIT-458](LIT-458.md) (the Platonic hypothesis) and [LIT-526](LIT-526.md) cite it, and
[LIT-526](LIT-526.md) began as a test of its inner product. All four were filed before it.

[THEORY-tmpsbx36](../theory.d/THEORY-tmpsbx36.md) holds the account: the three
notions coincide under a causal inner product. [SOTA-tmpb5sn6](../practices.d/SOTA-tmpb5sn6.md) holds the one
instruction that follows: compare concept directions after whitening by the
unembedding covariance, not by raw cosine. It is `Proposed` and contested,
for reasons given under the practice. **Building steering vectors from
counterfactual word pairs is described here and is not filed.** One
illustrated example (Table 1) and four quadruples (Fig 5, App D.4), on
contexts ChatGPT-4 wrote, do not yet support a recommendation over other
ways of building a steering vector.

The paper names word2vec and GloVe ([LIT-603](LIT-603.md), [LIT-602](LIT-602.md)) as where the subspace
notion was first observed. [THEORY-089](../theory.d/THEORY-089.md) is the record's account of why it
appears there, as log co-occurrence ratios becoming offsets. This paper
asks what the subspace notion means and does not rely on that mechanism.

## What it does not establish

- **The evidence is qualitative.** Orthogonality is shown as a heatmap, with
  no statistic against a null and no count of how many pairs meet a
  threshold.
- **The Euclidean product "somewhat works" on LLaMA-2** (App D.2, the
  authors' words): most separable concepts are already near-orthogonal under
  plain cosine. The whitened product helps visibly on frequent⇒infrequent and
  on language pairs sharing French. On Gemma-2B, which ties embeddings and
  unembeddings, Euclidean fails and whitening works. That is two models, both
  read by eye.
- **D = I is a choice, not a result.** The theorem leaves d degrees of
  freedom and "we do not have a principle for picking out a unique choice".
- **Only the output and input spaces are studied.** Intermediate layers,
  where most probing and steering happen, are named as future work. [LIT-526](LIT-526.md)
  is the record's test of that extension, and for cross-lingual concept
  transport it finds whitening adds nothing over spectral regularization
  (p = 0.95, 17 models).
- **Causal separability is assumed, not tested.** Which concepts count as
  separable is the authors' call, and the orthogonality check uses the same
  judgement.

<!-- inactive-ok-file: THEORY-tmpsbx36, SOTA-tmpb5sn6 — Proposed, filed in this same contribution from this paper -->
<!-- inactive-ok-file: THEORY-034, THEORY-089 — Proposed, named as the accounts that build on or sit beside this one, not cited as established -->
