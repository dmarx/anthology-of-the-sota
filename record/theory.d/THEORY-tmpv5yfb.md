---
status: Active
title: 'Stacked GCN propagation drives node features exponentially toward a subspace that keeps only connected-component membership and degree, at a rate set by the weights'' scale against the graph''s spectrum'
version: 1
tags:
- graphs-and-networks
- analysis-and-evaluation
- model-stability
date: '2026-10-22'
source:
- LIT-tmpivepp
- LIT-tmp8uu4y
- LIT-tmp44ov9
explains: []
summary: >-
  Oono and Suzuki (2019), [LIT-tmpivepp](../literature.d/LIT-tmpivepp.md), extending Li et al. (2018),
  [LIT-tmp8uu4y](../literature.d/LIT-tmp8uu4y.md) — over-smoothing. With largest weight singular value s and
  spectral factor λ < 1, a ReLU GCN's distance from the subspace is at most
  (sλ)^l times its start. It is a theorem. What it does not establish is
  that this is why deep GCNs lose accuracy. On sparse citation graphs the
  condition sλ < 1 is a sliver, and Rusch et al., [LIT-tmp44ov9](../literature.d/LIT-tmp44ov9.md), show a deep
  GCN that avoids over-smoothing and degrades just as much.
---

# THEORY-tmpv5yfb: Stacked GCN propagation drives node features exponentially toward a subspace that keeps only connected-component membership and degree, at a rate set by the weights' scale against the graph's spectrum

## Source

Oono and Suzuki (2019), [LIT-tmpivepp](../literature.d/LIT-tmpivepp.md). Read as [NOTE-tmp36ez0](../notes.d/NOTE-tmp36ez0.md). Li et al.
(2018), [LIT-tmp8uu4y](../literature.d/LIT-tmp8uu4y.md), read as [NOTE-tmphp27d](../notes.d/NOTE-tmphp27d.md). Rusch et al. (2023),
[LIT-tmp44ov9](../literature.d/LIT-tmp44ov9.md), read as [NOTE-tmpgkme7](../notes.d/NOTE-tmpgkme7.md).

## The account

A GCN layer multiplies the features by P = D̃^{-1/2} Ã D̃^{-1/2}, which is
Laplacian smoothing. Li et al. ([LIT-tmp8uu4y](../literature.d/LIT-tmp8uu4y.md)) proved that repeated
smoothing alone converges on each connected component to a vector
proportional to √degree, so nodes of equal degree in one component become
identical. They named this over-smoothing.

Oono and Suzuki ([LIT-tmpivepp](../literature.d/LIT-tmpivepp.md)) proved the same subspace attracts the full
network. P's eigenvalue 1 has an eigenspace spanned by D̃^{1/2} times the
component indicators, and every other eigenvalue has modulus at most
λ < 1. The weights stretch distances by at most s, their largest singular
value, and ReLU never increases the distance from this subspace. So the
distance shrinks by at least a factor sλ per layer. When sλ < 1 the
features lose everything except component and degree, exponentially fast.
Dense graphs have small λ, so on large dense Erdős–Rényi graphs almost
any GCN meets the condition.

Rusch et al. ([LIT-tmp44ov9](../literature.d/LIT-tmp44ov9.md)) turn this into a measurable definition:
exponential decay with depth of a measure such as the Dirichlet energy.
GCN, GAT and GraphSAGE show that decay on three real graphs with random
inputs. DropEdge and a residual GCN still show it, and PairNorm, GCNII,
GraphCON and G² do not.

## What it explains

- Why one or two smoothing steps help and many do not: on Cora one step
  takes a linear classifier from 53.1% to 70.8%, and the limit is
  uninformative (Li et al., Table 1)
- Why denser graphs are more exposed: λ^{-1} grows as the graph
  densifies (1.0036 on Cora, 1.11 and 1.15 with 2,495 and 4,988 random
  edges added), so a wider range of weights falls in the information-loss
  region. On the densified graphs, GCNs held below the threshold do worse
  than those held above it in almost all depth settings
- Why trained GCNs push their weights up: three-layer GCNs on Noisy Cora
  raise s during training and stay out of the information-loss region

## Where it stops

- **It is not shown to be why deep GCNs lose accuracy.** Li et al.
  attribute their own deeper GCNs' drop to overfitting. On Cora the
  threshold λ^{-1} is 1.0036, so Oono and Suzuki added 2,495–4,988 random
  edges to test it. Rusch et al.'s GCN with a bias keeps a constant
  Dirichlet energy and loses accuracy with depth as much as the plain GCN
  does. [LIT-582](../literature.d/LIT-582.md)'s difficulty past about seven layers is not explained by
  this account until someone separates over-smoothing from trainability
  there
- **Necessary, not sufficient.** In Rusch et al. avoiding the collapse
  does not by itself make depth help. Of the methods tested, only G² did
- **ReLU, node classification, no readout.** The proof needs ReLU's
  projection onto the non-negative cone
- **Residual connections are open.** Oono and Suzuki's Markov-chain
  intuition says they should not stop the collapse, and they note 56-layer
  residual GCNs that train well. Rusch et al. find a residual GCN's
  Dirichlet energy still decays exponentially
- **Distinct from over-squashing** ([THEORY-tmpk02h3](THEORY-tmpk02h3.md)), which can occur
  without it
