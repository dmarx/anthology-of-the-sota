---
number: 316
status: Read
formerly:
- NOTE-tmpk15k0
paper: LIT-576
title: 'MEMIT'
version: 1
date: '2026-09-23'
summary: >-
  ROME's idea extended to thousands of facts by spreading updates across a
  range of MLP layers in one batched solve. 85.8 on 10,000 CounterFact edits
  on GPT-J, where ROME falls to 50.3. Main text read, appendices skimmed.
---

# NOTE-316: MEMIT

## Contribution

A weight editor that scales to 10,000 simultaneous facts on 6B and 20B
models.

## Key insight

**Spread the change.** Many small updates, each distributed over several
MLP layers and solved jointly against a covariance of existing keys,
interfere less than many rank-one updates stacked in one layer.

## Key results

- zsRE, 10,000 edits, GPT-J: efficacy 96.7, paraphrase 89.7, specificity
  26.6 (unedited 27.0)
- CounterFact, 10,000 edits: GPT-J 85.8 (NS 73.7 against 83.5 unedited),
  GPT-NeoX 82.0. ROME 50.3. Fine-tuning 67.6 with generation collapse
- ROME degrades from 32 edits, and MEND loses efficacy by 1,000

## Limitations

- **Neighborhood damage grows with the number of edits** (83.5 to 73.7)
- **Recall of the edited triple only.** Implications are not tested
- **Hours of compute** for 10,000 edits in the released implementation
- Fine-tuning's weight-decay hyperparameter was tuned only at n = 10,000
