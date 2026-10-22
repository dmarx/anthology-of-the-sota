---
status: Active
title: 'In a message-passing GNN, how much one node''s output can depend on another node''s input is bounded by the graph between them, so wider layers only rescale the bound, deeper ones trade it for vanishing gradients, and only changing the graph moves it'
version: 1
tags:
- graphs-and-networks
- analysis-and-evaluation
- model-architecture
date: '2026-10-22'
source:
- LIT-tmp0hkly
- LIT-tmpggqnq
- LIT-tmpt6hyo
explains:
- SOTA-tmps0jek
summary: >-
  Topping et al. (2021), [LIT-tmp0hkly](../literature.d/LIT-tmp0hkly.md), and Di Giovanni et al. (2023),
  [LIT-tmpggqnq](../literature.d/LIT-tmpggqnq.md), formalizing Alon and Yahav's over-squashing (2020),
  [LIT-tmpt6hyo](../literature.d/LIT-tmpt6hyo.md). The Jacobian between distant nodes is bounded by powers of
  the normalized adjacency. It is small across very negatively curved edges
  and between nodes of high commute time. Width multiplies every
  sensitivity by the same factor. The bounds are theorems, and their
  predictions hold on synthetic tasks. On real benchmarks, rewiring gains
  are mostly a few points or less.
---

<!-- inactive-ok-file: SOTA-tmps0jek — the practice this account explains, Proposed on one group's evidence -->

# THEORY-tmpk02h3: In a message-passing GNN, how much one node's output can depend on another node's input is bounded by the graph between them, so wider layers only rescale the bound, deeper ones trade it for vanishing gradients, and only changing the graph moves it

## Source

Topping et al. (2021), [LIT-tmp0hkly](../literature.d/LIT-tmp0hkly.md), read as [NOTE-tmp9fulo](../notes.d/NOTE-tmp9fulo.md). Di Giovanni et
al. (2023), [LIT-tmpggqnq](../literature.d/LIT-tmpggqnq.md), read as [NOTE-tmprhd2j](../notes.d/NOTE-tmprhd2j.md). Alon and Yahav (2020),
[LIT-tmpt6hyo](../literature.d/LIT-tmpt6hyo.md), read as [NOTE-tmp198gc](../notes.d/NOTE-tmp198gc.md).

## The account

Alon and Yahav ([LIT-tmpt6hyo](../literature.d/LIT-tmpt6hyo.md)) named the problem. A task that needs
information from r hops away needs r layers. By then, messages from a
receptive field exponential in r arrive through fixed-size vectors. On
their tree task every GNN stopped fitting the training set by depth 5, and
a hidden size of 512 fit depth 7 at most.

Topping et al. ([LIT-tmp0hkly](../literature.d/LIT-tmp0hkly.md)) made it a bound. With message and update
derivatives bounded by α and β, |∂h_i^(r+1)/∂x_s| ≤ (αβ)^{r+1}(Â^{r+1})_is,
so sensitivity is capped by how much walk mass the normalized adjacency
carries from s to i. They located where that mass is lost: across an edge
whose Balanced Forman curvature is close to −2, many two-hop neighbours
have an average Jacobian below (αβ)²δ^{1/4}.

Di Giovanni et al. ([LIT-tmpggqnq](../literature.d/LIT-tmpggqnq.md)) separated the model from the graph. The
bound is (c_σ·w·p)^m·(S^m)_vu: width p and weight scale w multiply every
pair's sensitivity alike, so the pairs the topology starves stay starved
relative to the rest. Depth near the distance gives decay like
(2c_σwp/d_min)^r. Much more depth makes the gradients vanish. Averaged over
layers, the obstruction between two nodes is bounded above and below by
their commute time, which is 2|E| times their effective resistance.

## What it explains

- **Why adding edges helps where adding width does not.** On QM9, Alon and
  Yahav's doubled width cut error 5.5% and a fully adjacent last layer cut
  it 42%. Adding edges lowers effective resistance, by Rayleigh
  monotonicity, and a fully adjacent layer makes every pair one hop apart.
  This is the reason behind [SOTA-tmps0jek](../practices.d/SOTA-tmps0jek.md)
- **Why topology, not distance, sets difficulty.** At equal source–target
  distance, GIN, SAGE, GCN and GAT fail first on CliquePath, then Ring,
  then CrossedRing, in order of their effective resistance
- **Why diffusion rewiring and curvature rewiring differ.** PPR rewiring
  cannot raise a bottleneck's Cheeger constant far (Topping et al.,
  Theorem 6), while adding edges around negatively curved edges targets it
- **Why attention helps a little.** GAT and GGNN fit one more level of the
  tree task than GCN and GIN, by ignoring the irrelevant half of the
  incoming messages. Di Giovanni et al.'s bounds exclude such models

## Where it stops

- **A bound, not a measurement of benchmark harm.** The tree and
  graph-transfer tasks are built to need distant information. On node
  classification, SDRF gains 0.3–6.7 points and trails other rewirings on
  five of nine datasets. Tönshoff et al. ([LIT-579](../literature.d/LIT-579.md), [SOTA-349](../practices.d/SOTA-349.md)) closed the
  long-range benchmark's message-passing gap on Peptides with tuning and
  an MLP head, without rewiring. How much of a real gap is over-squashing
  is not settled by these papers
- **Two hops for curvature.** The curvature theorem covers two-hop
  propagation. Commute time covers longer range, in expectation and under
  an assumption that all ReLU paths are equally likely to be active
- **Equal-weight aggregation.** Attention and gating are outside the
  bounds
- **Which rewiring to use is open**, as Di Giovanni et al. say
- **Not over-smoothing** ([THEORY-tmpv5yfb](THEORY-tmpv5yfb.md)). Alon and Yahav give a case of
  each without the other
