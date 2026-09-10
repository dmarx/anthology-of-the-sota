---
number: 76
status: Rejected
status_note: >-
  a cluster-scheduling claim rather than a training one: it is the
  scheduler's decision, expressed as a placement-group request, not
  something in a training run. ADR-026 (superseding ADR-020) scopes
  this record by the kind of claim, and this is a different kind
title: 'Place replicas to minimize cross-rack traffic'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
source:
- LIT-051
summary: >-
  Jiang et al. (2020), [LIT-051](../literature.d/LIT-051.md) — https://www.usenix.org/conference/osdi20/presentation/jiang.
---

<!-- inactive-ok-file: ADR-020 — Superseded by ADR-026, which carries its decision forward; every mention here names it as the superseded document, deliberately -->

# SOTA-076: Place replicas to minimize cross-rack traffic

## Source

Jiang et al. (2020), [LIT-051](../literature.d/LIT-051.md) — https://www.usenix.org/conference/osdi20/presentation/jiang.

## A scheduling claim in a training registry

Placing the workers of a job so that its collectives stay inside a rack is
sound and is what topology-aware schedulers do. It is also not a decision the
person training the model usually makes: it belongs to the cluster scheduler,
and on managed infrastructure it is expressed as a placement-group request
rather than as anything in the training code.

That makes it a different *kind* of recommendation from the rest of this
record, which is about what to do inside a training run. Worth keeping only
if the anthology intends to hold cluster-scheduling practice, and worth
saying so explicitly if it does — a scope question rather than a citation
one, and the kind [ADR-026](../decisions.d/ADR-026.md) is about.

## The citation, separately

[LIT-051](../literature.d/LIT-051.md) does not argue for it. BytePS's setting is a heterogeneous cluster
whose spare CPU and network capacity it exploits; its contribution is the
unified communication framework and the Summation Service split ([SOTA-047](SOTA-047.md)).
Placement is assumed as part of the environment, not recommended.
