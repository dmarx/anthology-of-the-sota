---
number: 223
status: Proposed
formerly:
- SOTA-tmpf0z9t
promote_when: >-
  The comparison redrawn at a second scale or on a second workload, by anyone,
  against a directed exponential graph specifically rather than an unspecified
  s-regular one. What would not satisfy it: another paper reporting that
  randomized gossip converges well, which is the claim's premise rather than
  its content — the content is that it beats the best static graph at equal
  communication.
consensus: unreplicated
consensus_note: >-
  One group, one workload, 96 nodes. Nothing in the record disputes it; the
  static-topology literature it would displace largely predates it and has
  not answered.
title: 'Do not keep the gossip topology static: sample a fresh random neighbourhood every round'
version: 1
tags:
- distributed-optimization
date: '2026-09-16'
source:
- LIT-315
introduced_by:
- LIT-315
extends:
- SOTA-225
compared_against:
- SOTA-226
implementations: []
summary: >-
  de Vos et al. (2023), [LIT-315](../literature.d/LIT-315.md). Decentralized training has spent years
  choosing good fixed graphs. Epidemic Learning does not choose one: each
  round, every node sends its update to `s` peers picked at random. The
  transient-iteration count falls from the best-known O(n^3) to O(n^3/s^2),
  and at 96 nodes on CIFAR-10 it converges 1.7x faster and 2.2% more
  accurately than a static 7-regular graph at equal communication volume.
---

# SOTA-223: Do not keep the gossip topology static: sample a fresh random neighbourhood every round

## What to do

Each round, have every node independently sample `s` peers uniformly at random
and send its model update to those. Do not fix a graph and reuse it.

`s ~ log2(n)` is the paper's practical default, trading communication volume
against convergence; raise it where bandwidth is plentiful.

Sample **locally** — each node picks its own peers with no coordination. The
paper's other variant coordinates the draw so that the round's graph is
exactly `s`-regular, and reports the difference as negligible in both theory
and experiment, so the coordination is not worth its cost.

## Why

**Changing the graph is the mechanism, not an implementation convenience.**
The convergence argument turns on the *sequence* of topologies mixing faster
than any one of them does. Formally, the transient iterations — the rounds
before asymptotic linear speedup arrives — go from the best-known `O(n^3)` for
static and semi-dynamic topologies to `O(n^3/s^2)`. That is a statement about
the whole class, and the paper's Table 1 places the known static results
inside it.

**The empirical claim is at equal communication volume**, which is the
comparison that matters: 1.7× faster to a target and 2.2% higher final
accuracy than a static 7-regular topology, at 96 nodes on CIFAR-10, over five
seeds with confidence intervals.

## What this does not settle

**It is one workload at one scale.** CIFAR-10, 96 nodes. Nothing here is a
language model, and nothing here is at a node count where the `n^3` in either
bound is doing visible work.

**The baseline is a 7-regular graph, not the graph [SOTA-226](SOTA-226.md)
recommends.** The theoretical claim covers directed exponential graphs by
covering the static class; the measured 1.7× does not, because that comparison
was not run. This is why the two practices are filed as a pair with neither
superseding the other, and why `promote_when` asks for exactly that
comparison.

**And [LIT-254](../literature.d/LIT-254.md) had already looked at randomization and rejected it** — five
years earlier, on a different metric, at a different degree. It reports that
sampling one random destination per round leaves `E[lambda_2] ~= 0.4` against
exactly zero for deterministic cycling through the exponential graph, and that
random schemes unbalance the message load. That is a comparison at out-degree
one, and this practice samples `s ~= log2(n)` peers; the two results are
about different operating points and neither has met the other. A reader
should know both exist before choosing.

**Resampling has to be possible.** A node needs a peer list or a peer-sampling
service, and the round's communication pattern cannot be baked into a fabric
or a job launcher. Where it is — which is most datacentre training — the
static answer is the only available one.

**`s ~ H^2/sigma^2` for skewed data is the paper's own weakest
recommendation** and is not filed. It requires a measurable heterogeneity
term, and the paper marks it as such.

## Known implementations

None recorded.
