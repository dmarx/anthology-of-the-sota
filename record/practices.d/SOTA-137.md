---
status: Superseded
# inactive-ok: SOTA-136 — the successor, a Proposed practice; the retirement names it on purpose
superseded_by: SOTA-136
status_note: constraining the mixing to a doubly-stochastic manifold keeps the width and restores the identity mapping this gave up
title: 'Widen the residual stream into several streams with freely learned mixing (hyper-connections)'
version: 1
tags:
- model-architecture
date: '2026-09-05'
published: '2024-09-01'
# inactive-ok: LIT-141 — this practice's own source, retired with it
source:
- LIT-141
# inactive-ok: LIT-141 — the summary names the retired source on purpose
summary: >-
  Zhu et al. (2024), [LIT-141](../literature.d/LIT-141.md) — n parallel residual streams with learnable mixing; gains on dense and MoE pretraining, and an identity-mapping property lost that its successor restores.
extended_by:
- SOTA-136
---

# SOTA-137: Widen the residual stream into several streams with freely learned mixing (hyper-connections)

## Source

<!-- inactive-ok: LIT-141 — the superseded paper, named as the predecessor in the chain -->
Zhu et al. (2024), [LIT-141](../literature.d/LIT-141.md) — Hyper-Connections.

Replace the single residual stream with n parallel streams (n = 2 in most of
the paper's runs) and learn the mixing between them, so that the network
can tune connection strength across depth and exchange information
laterally between streams. The motivation is the seesaw between vanishing
gradients and representation collapse that fixed residual variants cannot
escape; the paper shows consistent pretraining gains on dense and MoE models.

## Why this is superseded

<!-- inactive-ok-block: SOTA-136 — the successor this retirement names -->
The free mixing discards the identity mapping a residual guarantees, and
the successor's authors report that this is what made hyper-connections
unstable and hard to scale. Constraining the mixing matrices ([SOTA-136](SOTA-136.md), [LIT-140](../literature.d/LIT-140.md))
keeps the width and the gains. Kept here so that the chain can be read from
the residual forward; the claim above was right about the seesaw and wrong
about what could be left free.
