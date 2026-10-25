---
number: 395
status: Skimmed
formerly:
- NOTE-tmpbwjql
paper: 'LIT-836'
title: 'Graph foundation models are already here'
version: 1
date: '2026-10-22'
summary: >-
  A position paper: graph foundation models transfer when they share a
  "graph vocabulary" of structural units, and the paper organizes existing
  principles and models under that idea. No experiments. Main text read.
  Appendices A–E (dataset and model lists, feature alignment, further
  discussion) not read.
---

# NOTE-395: Graph foundation models are already here

## Contribution

A taxonomy of existing graph foundation models (task-specific,
domain-specific, primitive), and a reading of their successes as cases of
a suitable shared vocabulary. It sorts transferability principles by task
and lists open problems in scaling.

## Key insight

**Transfer needs units that mean the same thing in every graph.** In
language the units are tokens. In graphs the paper proposes structures that
an expressive enough model never merges and that new graphs can be mapped
onto, as ULTRA's graph of relations does for unseen relation types.

## Key results

- No measurements. Its claims are arguments from cited work: ULTRA's
  zero-shot knowledge-graph completion, OFA's joint training, and the
  absence of positive scaling for a larger GAT on graph regression

## Limitations

- **The vocabulary is a metaphor here**, not a construction. No experiment
  tests whether a model with a "better vocabulary" transfers better
- **"Actionable steps" are proposals**, each resting on one or two cited
  papers
- **The title outruns the text**, which says no current model transfers
  across all tasks and domains
