---
number: 391
status: Read
formerly:
- NOTE-tmp9fulo
paper: 'LIT-803'
title: 'Over-squashing via curvature'
version: 1
date: '2026-10-22'
summary: >-
  Over-squashing measured as a Jacobian bounded by powers of the normalized
  adjacency. Balanced Forman curvature lower-bounds Ollivier curvature, and
  very negative edges starve two-hop neighbours of sensitivity. SDRF adds
  edges around them. Small gains on node classification, largest on
  heterophilic graphs. Main text read, appendix definitions and
  experimental details skimmed.
---

# NOTE-391: Over-squashing via curvature

## Contribution

The first formal treatment of over-squashing. It gives a sensitivity
measure, a local cause in the graph, and a rewiring aimed at that cause.

## Key insight

**A bottleneck is an edge whose two ends share no triangles or squares.**
Messages between the two sides have one road, and every node beyond it
receives a vanishing share of what was sent. Curvature measures how many
alternative roads an edge has, so raising it locally relieves the
bottleneck.

## Key results

- Lemma 1: |∂h_i^(r+1)/∂x_s| ≤ (αβ)^{r+1}·(Â^{r+1})_is
- Theorem 2: Ollivier κ(i, j) ≥ Balanced Forman Ric(i, j), at lower cost
- Corollary 3 and Proposition 5: Ric ≥ k > 0 on every edge bounds the
  diameter from above and the Cheeger constant, hence the spectral gap,
  from below
- Theorem 4: Ric(i, j) ≤ −2 + δ implies more than 1/δ two-hop nodes with
  average Jacobian below (αβ)²·δ^{1/4}
- Theorem 6: PPR rewiring cannot raise the Cheeger constant arbitrarily
- Table 2: SDRF over no rewiring, by dataset: Cornell +1.9, Texas +3.3,
  Wisconsin +0.9, Chameleon +1.4, Squirrel +6.7, Actor +4.6, Cora +0.9,
  Citeseer +0.3, Pubmed +0.9 (accuracy points)
- Table 3: SDRF changes 0.2–33% of edges, and DIGL adds 73–8,331%

## Limitations

- **Two-hop theory.** Theorem 4 does not reach long-range dependencies
  directly
- **Short-range benchmarks.** Node classification on small or homophilic
  graphs, with a GCN only, and no long-range task
- **Topology only.** Curvature and SDRF ignore node features and labels,
  as the authors note, and the theory does not extend to multigraphs
- **Gains are small** except on Squirrel and Actor. Plain SDRF trails
  DIGL or +FA on five of nine datasets (Cornell, Texas, Cora, Citeseer,
  Pubmed), though SDRF on the undirected graph is best on Texas
