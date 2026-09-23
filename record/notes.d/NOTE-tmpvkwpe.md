---
status: Read
paper: LIT-tmp95aa1
title: 'GIN'
version: 1
date: '2026-09-23'
summary: >-
  Message passing is bounded by 1-WL, and sum aggregation with an MLP
  reaches the bound where mean and max do not. The theory predicts the
  training-fit ordering. Test accuracy separates the aggregators decisively
  only on featureless graphs. Main text read, proofs skimmed.
---

# NOTE-tmpvkwpe: GIN

## Contribution

A precise statement of what message-passing GNNs can distinguish, and the
simplest architecture that reaches it.

## Key insight

**An aggregator that forgets how many neighbors there are cannot tell
apart graphs that differ only in counts.** Mean keeps proportions and max
keeps the set. Only sum, followed by an MLP, keeps the multiset.

## Key results

- Training accuracy ranks sum–MLP > sum–1-layer > mean/max variants, as
  predicted (Figure 4)
- REDDIT-BINARY and MULTI-5K, with no node features: GIN-0 92.4 and 57.5,
  mean variants 50.0 and 20.0 (chance). With degree features, mean gets 71.2
  and 41.3
- The other seven datasets: GIN is best or tied, and most gaps are within
  one standard deviation. Mean–MLP beats GIN on PTC
- GIN-0 (ε fixed at 0) generalizes slightly better than learned ε

## Limitations

- **Distinguishing power is not accuracy.** The theorem bounds what can be
  separated, not what will generalize
- **Small graph-classification benchmarks** with large variance
- **Node features blunt the difference.** Where features are informative,
  the aggregator matters much less
