---
number: 314
status: Read
formerly:
- NOTE-tmpi3p60
paper: LIT-577
title: 'RippleEdits'
version: 1
date: '2026-09-23'
summary: >-
  Knowledge-editing benchmarks test the edited fact and leave its
  consequences untested. On six ripple criteria, weight editors average
  38–66, and prompting with the new fact beats them. Main text read.
---

# NOTE-314: RippleEdits

## Contribution

An evaluation of what an edit should change besides the edited fact, and
a benchmark that measures it.

## Key insight

**A fact is not an isolated triple.** Changing "Jack Depp's father" should
change his siblings, and "the country of X's capital" should hop through
it. An edit that updates only the queried string has not updated the
model's knowledge.

## Key results

- Parameter editors (ROME, MEMIT, MEND) average 38–66 across subsets and
  models
- Logical generalization on POPULAR, GPT-2 and GPT-J: 5.5–7.0. Subject
  aliasing: 86–100
- ICE averages 81–83 on LLaMA-7B against ROME's 49–61

## Limitations

- **Test queries are generated from Wikidata rules and templates.** Queries
  the model could not answer before editing are filtered out, and the
  surviving sets are small for GPT-2 and GPT-J
- **ICE is not evaluated on GPT-2 or GPT-J** for that reason
- **Generation-based scoring** by alias match within 20 tokens
