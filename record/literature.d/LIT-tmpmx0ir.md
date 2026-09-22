---
status: Active
title: 'The emergence of clusters in self-attention dynamics'
version: 1
tags:
- attention-techniques
- model-architecture
- analysis-and-evaluation
date: '2026-09-22'
published: '2023-05-09'
arxiv: '2305.05465'
first_author: 'Geshkovski'
keywords:
- 'interacting particle systems'
- 'clustering'
- 'self-attention dynamics'
- 'value matrix spectrum'
- 'low-rank attention'
implementations: []
summary: >-
  Geshkovski, Letrouit, Polyanskiy and Rigollet (2023), [ARXIV-2305.05465](https://arxiv.org/abs/2305.05465) —
  treat tokens as interacting particles and self-attention as their dynamics.
  Tokens cluster, and **the spectrum of the value matrix decides the limiting
  geometry**: `V = I` gives the vertices of a convex polytope, a simple
  positive leading eigenvalue gives at most three parallel hyperplanes,
  `V = −I` gives one cluster at the origin. In one dimension the attention
  matrix provably converges to a low-rank Boolean matrix. Read as
  [NOTE-tmp582ca](../notes.d/NOTE-tmp582ca.md).
---

# LIT-tmpmx0ir: The emergence of clusters in self-attention dynamics

Geshkovski, Letrouit, Polyanskiy and Rigollet (2023) —
[ARXIV-2305.05465](https://arxiv.org/abs/2305.05465), NeurIPS 2023. Read as
[NOTE-tmp582ca](../notes.d/NOTE-tmp582ca.md).

## Key takeaways

- **A taxonomy indexed by the spectrum of `V`.** Four regimes, proved:

| value matrix | key/query condition | limiting geometry |
|---|---|---|
| `V = I_d` | `Qᵀ K ≻ 0` | vertices of a convex polytope |
| `λ₁(V) > 0`, simple | `⟨Qφ₁, Kφ₁⟩ > 0` | at most **three** parallel hyperplanes |
| `V` paranormal | `Qᵀ K ≻ 0` | polytope × subspaces |
| `V = −I_d` | `Qᵀ K = I_d` | a single cluster at the origin |

- **The attention matrix goes low-rank, provably.** For `d = 1` with `V > 0`
  and `QK > 0`, `P(t)` converges — doubly exponentially — to a Boolean matrix
  that is generically rank 1 or 2. At most three tokens capture the attention
  of all but at most one of the others.
- **The assumptions are checked on a real model.** ALBERT-xlarge-v2, 16 heads,
  `n = 256`, `d = 128`: heads 5 and 14 satisfy both conditions of the good-triple
  definition, with `⟨Qφ₁, Kφ₁⟩` equal to **1.3060** and **0.6719**. The paper
  also says plainly that not all sixteen heads do.
- **Discrete time is not a gap.** The forward-Euler analogue is written out and
  the proofs are stated to carry through with straightforward modifications.
- **It sharpens rank collapse rather than repeating it.** Dong et al. showed
  that *without* skip connections the dynamics trivialize into one tight
  cluster; this shows that *with* them a rich cluster structure emerges.

## Standing in the anthology

**It is the trunk for a mechanism this record already uses as a premise.**
[NOTE-105](../notes.d/NOTE-105.md) treats rank collapse in transformer projection matrices as an
established fact, and the record holds neither Dong et al. nor this. Filing
this puts the refinement in, along with the reason the naive picture is wrong
in the presence of residual connections.

**It is the theoretical root of the low-rank attention assumption two
practices rest on.** The paper's own framing: the near-low-rank structure of
`P` is the empirical observation behind Linformer and behind LoRA, and in both
"the low-rank structure is imposed rather than extracted from `P` itself."
Theorem 2.1 extracts it. [SOTA-184](../practices.d/SOTA-184.md) and
[SOTA-147](../practices.d/SOTA-147.md) are downstream of that assumption.

**And it belongs beside the spectral cluster filed this week.** Every document
in that cluster asks what the spectrum of a weight matrix does to training;
this asks what the spectrum of the value matrix does to the *representations*,
and answers with a classification. Same object, different question, and no
citation in either direction.

**Filed after being declined once.** The first pass rejected it as an
idealization too far from a trained model. That reading was wrong on the
record's own terms — see [NOTE-tmp582ca](../notes.d/NOTE-tmp582ca.md).
