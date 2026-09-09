---
# Don't copy this file by hand — run `luria new note`, which assigns the
# code and fills in what a machine can compute.
#
# A NOTE is a READING of a paper: what it contains, what it assumes, what it
# proves, and how strongly. It is not the paper's standing in the anthology
# — that is the LIT note's job, and the two are allowed to disagree
# (ADR-tmp2q9cv).

# Read | Skimmed | Unread | Superseded, from statuses.yaml beside this file.
# This says HOW DEEPLY THE PAPER WAS READ, not whether it is any good.
# Be honest here. `Skimmed` is a useful, respectable status and is
# deliberately not in force: it is not enough to source a practice from,
# and the whole scheme exists because the record could not previously tell
# a read paper from an unread one.
status: Skimmed

# REQUIRED. The LIT code this is a reading of. The bibliography — title,
# authors, year, arxiv — lives there and is NOT repeated here.
paper: LIT-000

# Repeat the paper's short name as the body's `# NOTE-xxx:` heading; the
# lint checks that the two agree.
title: ''

version: 1

# Exactly one primary topic from tags.yaml — the paper's topic, over LIT's
# wider vocabulary, not the practice registry's narrower one.
tags:
- training-optimization

date: ''

# What the index table shows. One or two sentences: the finding, not the
# subject area. Prose, so bare codes get linked by `luria link --fix`.
summary: >-
  The single thing this paper established.
---

<!-- unresolved-ok-file: LIT-000 — the placeholder a new note replaces -->

# NOTE-xxx: <paper short name>

## Contribution

Two to four sentences. What did this add that did not exist before? Not what
field it is in — what is true after it that was not true before.

## Key insight

One paragraph. The single mental model this paper installs: the thing to
remember if everything else is forgotten.

## Assumptions

The formal conditions the main results require. State them as conditions,
with the expressions where they have them.

- `L`-smooth gradients: ‖∇f(x) − ∇f(y)‖ ≤ L‖x − y‖
- Bounded stochastic variance: E[‖g − ∇f‖²] ≤ σ²
- IID data across workers, or the heterogeneity bound if not

Where a paper's setting differs from the one this record's practices assume
— dense decoder-only transformers, large batch, homogeneous cluster — say so
here rather than letting a reader assume it transfers.

## Key results

Theorem-level, with the **exact expressions**. `O(1/√(nK))` is more useful
than "converges at the same rate as centralized". Give the regime each holds
in.

- **Theorem 1** — statement. *Holds when:* the parameter regime.

## Claims

Only a `Read` note may fill this in. `strength` is about the *support*, not
about how much you believe it.

| id | claim | strength | support |
|---|---|---|---|
| C1 | plain English | strong / moderate / weak | Theorem 2 / experiment in §5 / informal argument |

## Method

*(Omit this section entirely for empirical or survey papers.)*

The algorithm, its steps, and its components.

## Concepts

Terms as *this paper* defines them, which is not always as the field uses
them.

- **term** — precise definition as used here.

## Connections

How this builds on prior work, in prose. Machine-readable lineage —
`extends:`, `corrects:`, `compared_against:` — is declared on the LIT and
must not be duplicated here.

## Recommendations

Practitioner-facing advice derived from the paper, useful beyond this
record. These are candidate practices; a `SOTA` document is where one
becomes a recommendation this anthology makes.

- **R1** — the recommendation. *Topic:* short label. *Status:* standard or
  experimental. *Strength:* strong / moderate / weak. *Applies when:* the
  conditions.

## Bearing on the record

Which `SOTA` practices this reading confirms, contradicts, or should
produce. Name the codes. If a practice cites this paper for something the
paper does not say, this is where that gets written down.

## Limitations

What the paper does not establish, including what its own authors say it
does not.

## Open questions

What it leaves open, and what result would close it.
