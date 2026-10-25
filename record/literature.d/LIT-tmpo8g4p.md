---
status: Active
title: 'Improving Graph Neural Network Expressivity via Subgraph Isomorphism Counting'
version: 1
tags:
- graphs-and-networks
- model-architecture
- representation-and-encoding
date: '2026-10-22'
published: '2020-06-16'
arxiv: '2006.09252'
doi: '10.1109/TPAMI.2022.3154319'
first_author: 'Bouritsas'
keywords:
- 'gsn'
- 'substructure-counting'
- 'structural-encoding'
- 'expressive-power'
- 'weisfeiler-lehman'
- 'molecular-graphs'
implementations:
- graph-substructure-networks
compared_against:
- LIT-580
- LIT-tmp6ppm0
summary: >-
  Bouritsas, Frasca, Zafeiriou, Bronstein (TPAMI 2023), [ARXIV-2006.09252](https://arxiv.org/abs/2006.09252).
  Counts small substructures (cycles, paths, cliques) around each node or
  edge in preprocessing and feeds the counts into message passing. This is
  strictly more expressive than 1-WL for any substructure other than a star,
  and stays linear in edges at training time. ZINC test MAE 0.140 without
  edge features against 0.254 for the same MPNN. Training error tracks how
  uniquely the counts identify nodes; test error does not, and cycles
  generalize best on molecules.
---

<!-- inactive-ok-file: NOTE-tmpy4wqs — Skimmed, and cited precisely to record that the reading covers the main text only (ADR-025) -->

# LIT-tmpo8g4p: Improving Graph Neural Network Expressivity via Subgraph Isomorphism Counting

Bouritsas, Frasca, Zafeiriou, Bronstein, Imperial College London and Twitter
(TPAMI 2023) — [ARXIV-2006.09252](https://arxiv.org/abs/2006.09252)

## Key takeaways

- **Structural features:** for a chosen set of small graphs, count for each
  node how often it sits in each automorphism orbit of each one (GSN-v), or
  do the same for edges (GSN-e). The counts enter the message function. They
  are permutation invariant, so the network stays invariant
- **Expressivity** (Theorem 3.1): strictly more powerful than 1-WL when the
  counted graph is anything but a star (non-induced counting), or anything
  but a single node or edge (induced counting). Edge counts are at least as
  expressive as node counts (Theorem 3.3). 4-clique counts separate the Rook
  and Shrikhande graphs, which 2-FWL cannot (Figure 2)
- **Strongly regular graphs** (Figure 4): with random weights, cycles or
  paths up to size 6 separate every same-size pair in the collection.
  1-WL- and 2-FWL-equivalent models fail on all of them
- **ZINC** (Table 2, about 100k parameters): MAE 0.140 without edge
  features and 0.115 with them, against 0.254 and 0.209 for the base MPNN.
  An MPNN with random node features scores 0.322 and 0.279, worse than the
  plain MPNN
- **Fit and generalization part ways** (Figure 5, left): as k grows, training
  error tracks how uniquely the counts identify nodes. Test error does not.
  Paths and trees disambiguate more and generalize about as well as the base
  MPNN; cycles disambiguate less and generalize much better, with a jump at
  k ≥ 6. GSN trained on 20% of ZINC reaches about the test error the MPNN
  reaches on all of it (Figure 5, right)
- **The counts alone go a long way** (Table 4): DeepSets, a model that
  ignores the edges, given the same counts ties or beats GSN on MUTAG (93.3
  vs 92.8), PROTEINS (77.8 both) and PTC (66.4 vs 68.2, within deviation).
  Message passing adds most on ZINC (0.288 vs 0.108)

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22). It is `compared_against` GIN ([LIT-580](LIT-580.md)): GIN is the base
architecture on the TUD benchmarks, and the better GSN variant beats GIN's
reported number on all seven datasets, mostly by less than one standard
deviation. The clearest TUD gain is COLLAB (85.5 vs 80.2). GSN's proof that
it is at least as expressive as 1-WL reuses GIN's Theorem 3.

**What the expressivity theorem buys and what it does not.** The paper says
so itself in §3.4: "none of the above claims can guarantee good
generalisation". Its own Figure 5 is the evidence. Substructures that
separate more nodes fit training better and do not test better, and the
substructure that helps on molecules (rings) is chosen from domain
knowledge, then tuned per dataset as a hyperparameter. This bears on the
"Where it stops" section of [THEORY-083](../theory.d/THEORY-083.md).

**Matched without ring counts.** Bevilacqua et al. ([LIT-tmp6ppm0](LIT-tmp6ppm0.md)) quote
GSN's ZINC result against their subgraph-bag model, which uses no
substructure counts: 0.102 for their best configuration, under a 100k
budget, against 0.108 for GSN. That GSN figure matches GSN's own Table 4
entry, which lists 385k parameters; at about 100k, GSN reports 0.115.

**The TUD protocol** is GIN's: the epoch with the best accuracy averaged
over the ten folds, and the substructure family and size are also selected
that way. Treat the TUD row as optimistic.

Skimmed — [NOTE-tmpy4wqs](../notes.d/NOTE-tmpy4wqs.md) (main text read in full, appendices not).
