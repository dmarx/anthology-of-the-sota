---
status: Proposed
consensus: contested
consensus_note: >-
  One source recommends it, on qualitative evidence from two models. The one
  independent test, LIT-526, measured whitening by this covariance for
  cross-lingual concept transport in 17 models and found no benefit over
  spectral regularization alone (p = 0.95). That tests one use at
  intermediate layers, not the output-space comparison the source makes, so
  it qualifies the practice without refuting it.
contested_by:
- LIT-526
promote_when: >-
  A measured comparison, against a null, showing that whitened similarity
  between concept directions tracks some independent ground truth (which
  concepts are separable, or which interventions interfere) better than
  cosine does, on more than one model family and at the layers where probes
  and steering vectors are actually taken.
title: 'Compare, project and orthogonalize a language model''s concept directions after whitening by the unembedding covariance, not by raw cosine'
version: 1
tags:
- concept-geometry
- analysis-and-evaluation
date: '2026-09-23'
source:
- LIT-tmpoa14o
introduced_by:
- LIT-tmpoa14o
summary: >-
  Park, Choe and Veitch (2024), [LIT-tmpoa14o](../literature.d/LIT-tmpoa14o.md) — training fixes a model's
  representation only up to an invertible linear map, so Euclidean cosine
  between concept directions is not meaningful. Use ⟨u, v⟩ = uᵀ Cov(γ)⁻¹ v,
  with Cov(γ) the covariance of the unembedding rows, or equivalently
  transform by Cov(γ)^(−1/2) and then use Euclidean tools. Shown on LLaMA-2
  7B and Gemma-2B by heatmap. Contested by a null for cross-lingual transport
  in 17 models.
implementations: []
explained_by:
- THEORY-tmpsbx36
---

# SOTA-tmpb5sn6: Compare, project and orthogonalize a language model's concept directions after whitening by the unembedding covariance, not by raw cosine

## Source

Park, Choe and Veitch (2024), [LIT-tmpoa14o](../literature.d/LIT-tmpoa14o.md) — [ARXIV-2311.03658](https://arxiv.org/abs/2311.03658), §3.2 and
App D.2. The account is [THEORY-tmpsbx36](../theory.d/THEORY-tmpsbx36.md).

## The claim

Before measuring the similarity of two concept directions, projecting one out
of another, or orthogonalizing a set, change the inner product:

    ⟨u, v⟩_C = uᵀ Cov(γ)⁻¹ v

where Cov(γ) is the covariance of the model's unembedding rows over the
vocabulary. Equivalently, map every direction by Cov(γ)^(−1/2) and use
ordinary cosine and projection afterwards. The steering direction matching an
unembedding direction γ̄ is Cov(γ)⁻¹γ̄.

**Why:** training leaves the representation defined only up to an
invertible linear map, so a Euclidean cosine reports a coordinate system.
Under this product, concepts that can vary independently are orthogonal,
and each concept's probe and steering directions coincide.

## Evidence

- **LLaMA-2 7B, 27 concepts** (Fig 3, Fig 8). Whitened, separable concepts
  are near-orthogonal with interpretable blocks. Euclidean is "somewhat"
  orthogonal as well. The visible gains are frequent⇒infrequent, whose
  spurious Euclidean overlaps disappear, and language pairs sharing French,
  whose real overlap appears.
- **Gemma-2B** (Fig 9). Euclidean does not capture semantics and whitening
  does. The authors attribute this to tied embeddings.
- All of it is heatmaps read by eye, with no statistic.

## Why `Proposed`, and why contested

- **One source, qualitative, output space only.** Intermediate layers,
  where directions are usually taken, are untested in the source.
- **[LIT-526](../literature.d/LIT-526.md) tested the obvious use and found nothing**: for cross-lingual
  concept transport, whitening adds nothing over spectral regularization
  across 17 models and four language pairs. It also finds contextual concept
  directions concentrated in the low-variance tail of this very covariance,
  where whitening amplifies them most ([THEORY-063](../theory.d/THEORY-063.md)). Whether that helps or
  hurts is not known.
- **The covariance is one choice** among the causal inner products the
  theorem allows.

## Conditions

- Applies to directions in the unembedding or final-layer space. Anywhere
  else it is an extrapolation.
- Cov(γ) over the whole vocabulary, not over word frequencies in text: the
  assumption behind it is about words drawn uniformly from the vocabulary.
- Cheap: one d×d covariance and its inverse, once per model.

## Known implementations

- `github.com/KihoPark/linear_rep_geometry` (the authors' code)

<!-- inactive-ok-file: THEORY-tmpsbx36 — Proposed, filed in this same contribution as this practice's account -->

<!-- inactive-ok-file: THEORY-063 — Proposed, named as the placement result whose bearing on whitening is unknown -->
