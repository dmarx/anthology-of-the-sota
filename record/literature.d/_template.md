---
# Don't copy this file by hand — run `luria new lit`.
#
# A note records why a paper is worth keeping. It is not a summary of the
# paper; it is this project's reading of it.

# Active | Proposed | Deferred | Superseded | Rejected, optionally " — note".
# See statuses.yaml beside this file. `Rejected` is the attic: retire a paper
# by setting it, with the reason in the status note and the long version
# under "Standing in the anthology" below. Never by deleting the file —
# something cites it.
status: Active

# The paper's title, verbatim. Repeat it as the body's `# LIT-NNN:` heading.
title: 'The paper title, exactly as published'

version: 1

# Exactly one of the thirteen in tags.yaml, enforced by luria.toml — the same
# thirteen the practice registry uses (ADR-026).
tags:
- training-optimization

# When this note was filed. The record's own clock, not the paper's.
date: '2026-01-01'

# REQUIRED. When the PAPER appeared — the arXiv posting month, from the id:
# 2205.11487 → 2022-05. Distinct from `date:` above, which is when the record
# got round to it.
#
# This is the one place the date lives. A practice reads it from its primary
# source and a reading note from its paper, both by `derive`/`from` in
# luria.toml, so neither carries a copy that could drift (#119).
published: '2022-05-01'

# A SOURCE is required — at least one of these three, enforced (ADR-009).
# Prefer them in this order: an arXiv id or a DOI resolves through a remote
# and can be pinned; a URL is a string nothing can check. Bare id, no
# version suffix. Delete the lines you don't use.
arxiv: '0000.00000'
# doi: '10.0000/example'
# url: 'https://example.org/report'

first_author: 'Surname'

# The paper's own subject words, kept verbatim. Free-form on purpose — this
# is what the paper is about, whereas `tags:` is where the record files it.
keywords: []

# Optional. Models or codebases known to use this work.
implementations: []

# What the index table shows: the citation and the one finding that matters.
summary: >-
  Surname et al. (YEAR), [ARXIV-0000.00000](https://arxiv.org/abs/0000.00000). The single most useful thing this
  paper establishes.
---

<!-- unresolved-ok-file: LIT-000 — the placeholder a new note replaces -->

# LIT-000: The paper title, exactly as published

Surname et al. (YEAR) — [ARXIV-0000.00000](https://arxiv.org/abs/0000.00000)

## Key takeaways

- What it establishes, in claims rather than topics.

## Standing in the anthology

Why this is here — or, once it is `Rejected` or `Superseded`, why it isn't
any more, and what replaced it. Omit the section entirely while the answer is
just "it's good work", which is the usual case.
