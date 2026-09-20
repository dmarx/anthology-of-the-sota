---
status: Active
title: 'Diffusers: State-of-the-art diffusion models for image, video and audio generation'
version: 1
tags:
- generative-modeling
- systems-optimization
date: '2026-09-20'
published: '2022-07-01'
# No arXiv id and no DOI: this is a library, and the thing to cite is the
# repository. ADR-009's order of preference ends at `url:` for exactly this
# case, and ADR-032 is why a library is admissible at all.
url: 'https://github.com/huggingface/diffusers'
first_author: 'von Platen'
keywords:
- 'diffusion'
- 'inference'
- 'schedulers'
- 'reference-implementation'
implementations: []
summary: >-
  von Platen et al. (2022) — the reference implementation for diffusion
  sampling. Filed because the record named it as an implementation of
  [SOTA-203](../practices.d/SOTA-203.md) and held no document for it: of 142 names that field
  carried, this was the only one with no paper and no note, which is what
  typing the field to `LIT` turned up.
---

# LIT-tmpgpqc2: Diffusers: State-of-the-art diffusion models for image, video and audio generation

## Key takeaways

- **The library is where diffusion sampling is actually specified.** Papers
  give a sampler as equations; what practitioners run is a `scheduler` class,
  and the two are not always the same thing. Where the record recommends a
  sampler, this is usually what implements the recommendation.
- **It is infrastructure, filed as literature**, which [ADR-032](../decisions.d/ADR-032.md) decided:
  benchmarks, model reports and training or serving infrastructure are
  literature and the record files them, because 9 of the 27 most-cited
  artefacts were of those kinds and none had a home.
- **Cited by `url:` rather than by identifier.** [ADR-009](../decisions.d/ADR-009.md) prefers arXiv, then
  DOI, then URL, and says plainly that a URL is a string nothing can check.
  A library has no arXiv id; the repository is the citable thing, and this
  note is one of the cases that preference order exists to accommodate rather
  than to exclude.

## Standing in the anthology

**It is here because a schema change went looking for it.** `implementations:`
was an undeclared free-text field carrying 142 distinct names across 216
declarations. Typing it to `LIT` required every name to resolve to a
document — and 141 of them did, most to notes the record already held under a
different spelling. This was the one that did not.

That is the whole value of the exercise in one document: the record had been
asserting, in a structured field, that it knew of a system, and there was
nothing behind the assertion. Nothing in prose complained, because nothing in
prose was wrong.

No practice is sourced here and none should be. [SOTA-203](../practices.d/SOTA-203.md) recommends a
higher-order ODE solver on the weights you have, sourced to the papers that
measured it; this is what ships that recommendation, which is an adoption
fact and belongs where [DP-005](../principles.d/DP-005.md) sent adoption — to `implementations:` and to
`consensus:`, not to `source:`.

**Filed unread.** There is no `NOTE`, which under [ADR-025](../decisions.d/ADR-025.md) is the statement
that nobody has read it. What the record needs from it is that it exists, is
the reference implementation, and can be pointed at.
