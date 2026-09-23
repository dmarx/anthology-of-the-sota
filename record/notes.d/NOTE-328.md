---
number: 328
status: 'Read'
formerly:
- NOTE-tmpsqg9c
paper: 'LIT-606'
title: 'Linear Representation Hypothesis (Park, Choe, Veitch)'
version: 1
date: '2026-09-23'
summary: >-
  Formalizes "concepts are directions" with counterfactual word pairs, proves
  that the unembedding direction is a probe and the embedding direction a
  steering vector, and shows the two coincide under a causal inner product.
  One such product is the inverse unembedding covariance. The experiments,
  on LLaMA-2 7B, are qualitative. Read in full, appendices included.
---

# NOTE-328: Linear Representation Hypothesis (Park, Choe, Veitch)

## Contribution

A definition precise enough to prove things about. Before it, "linear
representation" meant any of a shared offset, a probe or a steering vector,
and similarity between concept directions was measured with a Euclidean
cosine that training does not pin down. After it, the three are one object up
to a choice of inner product, and there is a principled way to choose one.

## Key insight

**Which inner product is right is a question about the model, not a
convention.** Softmax logits λᵀγ are unchanged by γ → Aγ, λ → A⁻ᵀλ for any
invertible A, so geometry in the representation space is identified only up
to that map. Requiring causally separable concepts to be orthogonal selects a
family of inner products, and under any member of it the probe direction and
the steering direction for a concept are the same vector.

## Assumptions

- Next-token probability is softmax(λ(x)ᵀγ(y)), and the concept's value is
  read deterministically off the output word
- Binary concepts, each specified by counterfactual output pairs
- Existence results assume d − 1 separable concepts completing a basis with
  the target
- Thm 3.4 assumes that, for a word drawn **uniformly from the vocabulary**
  (not from text), its values on two separable concepts are uncorrelated

## Main results

- **Thm 2.2 (measurement)**: logit P(Y = Y(1) | Y ∈ {Y(0), Y(1)}, λ) =
  α λᵀγ̄_W, with α > 0 depending on the pair. The unembedding direction is a
  probe, and it ignores off-target correlates a fitted probe would pick up.
- **Thm 2.5 (intervention)**: λ + cλ̄_W leaves every separable concept's
  pairwise probability constant and raises W's.
- **Thm 3.2 (unification)**: under a causal inner product, the Riesz map
  sends γ̄_W to λ̄_W.
- **Thm 3.4 (explicit form)**: M⁻¹ = GGᵀ and GᵀCov(γ)⁻¹G = D for diagonal
  D > 0. With D = I, M = Cov(γ)⁻¹.

## Key results

- 26 of 27 concepts show counterfactual differences aligned with their
  leave-one-out direction well beyond random pairs. thing⇒part does not.
- Under Cov(γ)⁻¹, separable concepts are near-orthogonal. Related concepts
  form visible blocks (verb forms, language pairs).
- On LLaMA-2 the Euclidean product is "somewhat" orthogonal too. On Gemma-2B
  it is not, and whitening fixes it.
- A concept's direction probes held-out Wikipedia contexts (French⇒Spanish)
  and steers the next token ("Long live the" → queen at α = 0.2).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | the three notions of linear representation are one object under a causal inner product | strong | Thms 2.2, 2.5, 3.2 |
| C2 | Euclidean similarity between concept directions is not identified by training | strong | the invariance in (3.1) |
| C3 | Cov(γ)⁻¹ is a causal inner product | moderate | Thm 3.4 under Assumption 3.3, with D = I chosen |
| C4 | LLaMA-2 concepts are linearly represented and separable ones orthogonal under it | weak | heatmaps on 27 hand-picked concepts, no null statistic |
| C5 | directions built from word pairs steer generation | weak | one table, four quadruples, generated contexts |

## Limitations

- Only the final unembedding and the last-layer context representation;
  intermediate layers are left open
- Single-token words only, so multi-token concepts are unmeasured
- D = I is unjustified, and separability is decided by the authors
- Two models, one 7B and one 2B, and orthogonality is judged by eye
