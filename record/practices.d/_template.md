---
# Don't copy this file by hand — run `luria new sota`, which assigns the
# number and fills in what a machine can compute.
#
# A practice is a claim about what you should do. State it as an instruction,
# not as a topic: "Keep sequence lengths a multiple of 128" rather than
# "sequence length considerations".

# Active | Proposed | Deferred | Superseded | Rejected, optionally " — note".
# What each one means here is in statuses.yaml, beside this file. When a
# practice stops being right, change the status and leave the body — the
# record is more useful for saying what it used to believe.
status: Proposed

# The claim. Repeat it as the body's `# SOTA-NNN:` heading; the lint checks
# that the two agree.
title: The thing you should do, in the imperative

version: 1

# Exactly one of the seven in tags.yaml, enforced by luria.toml. Secondary
# tags beyond that are unconstrained — add one when the practice genuinely
# belongs on a second page, not to be thorough.
tags:
- training-optimization

date: '2026-01-01'

# REQUIRED. The reading note for the paper this comes from — `LIT-000`. A
# recommendation with no paper behind it is an opinion, and the lint will
# say so. If the paper isn't in the record yet, `luria new lit` first.
source: LIT-000

# Optional. Models or codebases known to do this.
implementations: []

# What the index table shows. Provenance is the useful thing here, since the
# title already carries the claim: who said it, and where. Prose, so bare
# codes in it get linked by `luria link --fix`.
summary: >-
  Author et al. (YEAR), LIT-000 — [ARXIV-0000.00000](https://arxiv.org/abs/0000.00000).
---

<!-- unresolved-ok-file: LIT-000 — the placeholder a new practice replaces -->

# SOTA-NNN: The thing you should do, in the imperative

## Source

Author et al. (YEAR), LIT-000 — [ARXIV-0000.00000](https://arxiv.org/abs/0000.00000).

Anything the claim needs to be usable: the conditions it holds under, the
hardware or scale it assumes, the thing it trades away. A practice stated
without its conditions is the one people cargo-cult.

## Known implementations

- 
