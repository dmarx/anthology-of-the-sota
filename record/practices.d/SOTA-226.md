---
number: 226
status: Active
formerly:
- SOTA-tmpwgbmj
consensus: unreplicated
consensus_note: >-
  One paper in this record, but the load-bearing part is a property of the
  graph rather than a measurement: a directed exponential graph reaches exact
  consensus in log2(n) rounds, and that is checkable rather than reported.
title: 'If the gossip topology is static, make it a directed exponential graph, not a ring'
version: 1
tags:
- distributed-optimization
date: '2026-09-16'
source:
- LIT-254
introduced_by:
- LIT-254
extends:
- SOTA-225
compared_against:
- SOTA-223
implementations: []
summary: >-
  Assran et al. (2018), [LIT-254](../literature.d/LIT-254.md). Having chosen gossip over a parameter server,
  the next choice is the graph, and it is not a detail: a ring's consensus
  rate degrades with the node count badly enough that the speedup regime
  recedes out of reach. A directed exponential graph — each node sends to
  peers at distance 1, 2, 4, 8, ... in rotation — reaches exact consensus in
  log2(n) rounds with constant out-degree per round, and spreads the load
  evenly.
---

<!-- inactive-ok-file: SOTA-223 — Proposed, and cited as the practice
     that argues against this one. Filing a disagreement is what the pair
     is for; neither supports the other. -->
<!-- inactive-ok-file: SOTA-222, ADR-041 — Proposed: a
     neighbouring practice from a different paper, and the decision under
     which this document declines LIT-254's densification schedule. -->

# SOTA-226: If the gossip topology is static, make it a directed exponential graph, not a ring

## What to do

In a gossip scheme with a fixed communication graph, use a **directed
exponential graph**: node `i` sends to node `i + 2^k mod n`, cycling `k`
through `0, 1, 2, ...` on successive rounds. Each node sends to one peer per
round, and after `log2(n)` rounds every node's value has reached every other.

Do not use a ring, which is the easy default and the one this replaces.

## Why

**The graph decides how fast disagreement decays**, and a ring decides it
badly. Information crosses a ring at one hop per round, so consensus takes
`O(n)` rounds; [LIT-302](../literature.d/LIT-302.md) puts the resulting requirement for the linear-speedup
regime at `K = Omega(n^13)`, which is a way of saying the regime does not
arrive. The exponential graph gets there in `log2(n)`.

**It is directed on purpose.** Each node sends to exactly one peer per round
and receives from exactly one, so out-degree and in-degree are both constant
and the communication load is balanced. An undirected graph with the same
diameter costs more per round.

**And the consensus is exact rather than asymptotic.** [LIT-254](../literature.d/LIT-254.md) shows that
after `k = floor(log2(n-1))` iterations of cycling deterministically through
the neighbours, the second eigenvalue of the accumulated mixing matrix is
exactly zero — every node holds the true average. For 32 nodes that is five
rounds. Cycling through the edges of the *complete* graph instead leaves
`lambda_2 ~= 0.6` after the same five.

**[LIT-254](../literature.d/LIT-254.md) evaluated randomization and rejected it, which is the part this
record needs on the table.** Sampling one destination uniformly from the
exponential graph's neighbours gives `E[lambda_2] ~= 0.4`; sampling uniformly
from all `n-1` nodes gives `~= 0.2`. Both are worse than zero, and the paper
adds that a randomized scheme loses the guarantee that every node receives the
same number of messages, so the load stops being balanced.

## Conditions

**[SOTA-223](SOTA-223.md) argues against static answers, and the two papers are not
quite arguing about the same thing.** [LIT-315](../literature.d/LIT-315.md) claims a fresh random
neighbourhood each round beats every static topology, improving the
transient-iteration bound by `s^2`. [LIT-254](../literature.d/LIT-254.md)'s rejection of randomization,
above, is at **out-degree one** — each node sends to a single random peer per
round. [LIT-315](../literature.d/LIT-315.md) samples `s ~= log2(n)` peers per round and compares at equal
*communication volume*, so it is spending the same bytes in fewer, fatter
rounds.

That is not a refutation in either direction, and it is why neither practice
supersedes the other. What it means is that the open question is narrower than
"random or static": it is whether the advantage [LIT-315](../literature.d/LIT-315.md) measures survives when
the static baseline is a directed exponential graph rather than an
unspecified 7-regular one. Nobody has run that.

**The exactness needs `n` a power of two.** Otherwise the guarantee degrades to
approximate consensus and the argument becomes the ordinary spectral one.

**The rest of [LIT-254](../literature.d/LIT-254.md)'s recommendations are not filed here.** Overlapping the
gossip with computation is [SOTA-222](SOTA-222.md)'s subject from a different paper, and
its suggestion to run a denser topology for the first 30 epochs and then
sparsify is an algorithm-local schedule of the kind [ADR-041](../decisions.d/ADR-041.md) declines.

## Known implementations

None recorded.
