---
number: 414
status: Read
formerly:
- NOTE-tmpstzo8
paper: 'LIT-766'
title: 'Community detection with Ricci flow'
version: 1
date: '2026-10-22'
summary: >-
  Ollivier–Ricci curvature is negative on edges that carry traffic between
  communities, and a flow that stretches those edges, then cuts them,
  recovers planted communities on SBM and LFR graphs. The cutoff and the
  iteration count are chosen per network, and the theorem covers a
  parameter setting the experiments do not use. Main text read in full,
  supplementary theory skimmed.
---

# NOTE-414: Community detection with Ricci flow

## Contribution

A community-detection algorithm built on a graph analogue of Ricci flow,
with nothing learned. Curvature is computed per edge by optimal transport
between the endpoints' neighbourhood measures. The flow re-weights edges
by their curvature, and cutting the heaviest edges leaves the communities.

## Key insight

**An edge between communities is a bottleneck, and optimal transport sees
it as negative curvature.** If x and y share few neighbours, the cheapest
way to move x's neighbourhood mass onto y's is across the edge xy itself,
so W(m_x, m_y) exceeds d(x, y) and κ = 1 − W/d is negative. Inside a
community, shared neighbours and shortcuts make W small and κ positive.
The same quantity reappears in the over-squashing literature as a
diagnostic for message passing, though that work mostly uses other
discretizations of curvature.

## Key results

- **SBM, 500 nodes, two equal communities (Fig. 5a, ARI averaged over 10
  graphs):** near 1.0 up to p_inter/p_intra = 0.5, near 0 by 0.55. Most
  baselines also succeed below 0.5. Label propagation and Infomap do not
- **LFR, 500 nodes, average degree 20 (Fig. 5b):** Ricci flow and
  Spinglass lead. Spinglass reaches about 95% and Ricci flow is "nearly
  perfect for most of the values of µ"
- **One LFR graph, 1000 nodes, 30 communities, µ = 0.4 (Fig. 6a):** any
  final cutoff between 1 and 0.47 gives ARI 1.0. Modularity peaks at
  cutoff 0.275, which yields 290 communities, so modularity and ground
  truth disagree on where to cut
- **Real graphs (Fig. 5c):** "competitive or better" on Karate, Football,
  Polbooks and Polblogs. The figure also shows FB-Ego and Email-EU-core,
  where the text makes no claim
- **Surgery (supplement D.4, Fig. S14):** cutting the top 5% of edge
  weights every 5 iterations raises ARI from 0.3 to 0.8 on a 1000-node LFR
  graph at µ = 0.6
- **Density (Fig. 8):** both Ricci flow and Spinglass improve as average
  degree rises from 20 to 40

## Limitations

- **The knobs are tuned per network.** The iteration count (50 or 20) and
  the cutoff are chosen per graph, which the paper defends by analogy with
  surgery timing in Hamilton–Perelman. Without labels it suggests cutting
  where modularity first plateaus. The supplement (D.2, Figs. S10–S11)
  sweeps the measure's power p and exponential base, each on 1000-node LFR
  graphs, and finds p = 2 or 3 and base e best at high mixing. α, the
  iteration count and the surgery schedule are not swept
- **The theorem is for a setting the experiments do not use.** The
  separation result (supplement, Theorem 4.1) is for α = 0, p = 0 on a
  symmetric clique family. The experiments mostly use α = ½, p = 2
- **Small real graphs, results shown only as bars.** No numbers are
  tabulated for the real-network comparison, and four of the six graphs
  have under 1,300 nodes
- **Forman curvature was tried and dropped** as "less satisfying", with no
  result shown
- **A setup inconsistency.** §4.2.3 says p_inter was fixed at 0.15. The
  Fig. 5a caption says p_intra = 0.15, which is the reading consistent with
  the ratio on its x-axis
- **Cost.** Each curvature is a transport problem per edge, recomputed
  each iteration. The only timing is in the supplement (Fig. S12): on a
  300-node LFR graph a flow iteration takes 6.4 s with exact transport and
  1.6 s with Sinkhorn, at similar ARI, on a 20-process Xeon
