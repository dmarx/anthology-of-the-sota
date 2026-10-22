---
status: Active
title: 'Graph Neural Networks Exponentially Lose Expressive Power for Node Classification'
version: 1
tags:
- graphs-and-networks
- analysis-and-evaluation
- model-stability
date: '2026-10-22'
published: '2019-05-27'
arxiv: '1905.10947'
first_author: 'Oono'
keywords:
- 'over-smoothing'
- 'expressive-power'
- 'gcn'
- 'dynamical-system'
- 'graph-spectrum'
- 'weight-scaling'
implementations:
- 'delta2323/gnn-asymptotics'
extends:
- LIT-tmp8uu4y
summary: >-
  Oono, Suzuki (ICLR 2020), [ARXIV-1905.10947](https://arxiv.org/abs/1905.10947). For a ReLU GCN, the distance
  of layer-l features from the subspace that carries only connected-component
  and degree information is at most (sλ)^l times its initial value. Here s
  bounds the weights' largest singular values, and λ < 1 is set by the
  augmented normalized Laplacian's spectrum. On dense Erdős–Rényi graphs
  most GCNs meet the condition. On real citation graphs the theorem says
  something only for 1 ≤ s < 1.0036 (Cora), so the experiments add random
  edges to raise the threshold to 1.11–1.17.
---

# LIT-tmpivepp: Graph Neural Networks Exponentially Lose Expressive Power for Node Classification

Oono and Suzuki, University of Tokyo, Preferred Networks and RIKEN AIP
(ICLR 2020) — [ARXIV-1905.10947](https://arxiv.org/abs/1905.10947)

## Key takeaways

- **The general result** (Theorem 1, Corollary 2): for layers
  X ↦ MLP(PX) with ReLU, symmetric P and a P-invariant subspace U with a
  non-negative orthonormal basis, d_M(X^(l)) = O((sλ)^l), where λ is P's
  operator norm on U⊥. ReLU never increases the distance, because it
  projects onto a cone that the non-negative basis respects
- **For GCN** (Proposition 1, Theorem 2): with P = D̃^{-1/2} Ã D̃^{-1/2},
  the invariant space is spanned by D̃^{1/2}·(component indicators), and
  λ < 1. If sλ < 1, the output approaches it exponentially, so two nodes in
  one component with equal degree become indistinguishable. Features can
  lose information even with s ≥ 1, provided s < λ^{-1}
- **Dense random graphs** (Theorem 3): on G(N, p) with log N/(Np) = o(1),
  any GCN whose weights' singular values are below a bound that grows like
  √(Np / log(N/ε)) meets the condition with probability at least 1 − ε
- **The threshold on real graphs** (Appendix H, Table 1): λ^{-1} is
  1 + 3.62×10⁻³ on Cora, 1 + 1.25×10⁻³ on CiteSeer and 1 + 9.57×10⁻³ on
  PubMed. Adding 2,495–24,993 random edges ("Noisy" versions, Table 2)
  raises it to 1.11–1.17
- **Weight scaling** (§6.3, Figure 3): on Noisy Cora, GCNs whose
  largest singular value is held above λ^{-1} beat those held below it in
  almost all depth settings, and s = 10 beats no normalization. Trained
  three-layer GCNs push s up and out of the region on their own. Accuracies
  are shown only as plots, with 3 trials per setting
- **The residual question is left open** (§7): the Markov-chain picture
  suggests residual links should not prevent the collapse. The authors note
  that 56-layer residual GCNs train well, and say the situation "could be
  more complicated than our intuitions"

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22).

**It extends Li et al.** ([LIT-tmp8uu4y](LIT-tmp8uu4y.md)), and says so: Li et al. proved
that repeated linear smoothing converges on each component, and this paper
proves the same subspace attracts a GCN with weights and ReLU, at a rate
set by the weights' scale and the graph's spectrum. Its key step, that
ReLU never moves features away from the subspace, needs non-negative
eigenvectors and does not carry over to other activations.

**The hedge is the threshold.** The abstract says GCNs "exponentially lose
expressive power". The theorem's condition, s < λ^{-1}, is a sliver on
sparse real graphs, so the paper's real-data evidence comes from citation
graphs densified by adding thousands of random edges. The result is a
condition under which depth cannot help. It does not show that the
condition holds where GCNs are actually trained. It bears on [LIT-582](LIT-582.md)'s
depth appendix only through that condition. The account is
[THEORY-tmpv5yfb](../theory.d/THEORY-tmpv5yfb.md).

Read — [NOTE-tmp36ez0](../notes.d/NOTE-tmp36ez0.md).
