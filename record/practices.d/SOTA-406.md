---
number: 406
status: Proposed
formerly:
- SOTA-tmpz04ck
consensus: unreplicated
consensus_note: >-
  One measurement against a convention adopted by almost every MLM after BERT —
  RoBERTa, SpanBERT, DeBERTa. The convention's own evidence is a single BERT
  appendix table whose two rows differ by 0.1 on MNLI, so what this practice
  contests is not a result but an inherited default. `unreplicated` because
  nobody has re-run the comparison, in either direction. Read as of 2026-09.
promote_when: >-
  A second group compares all-`[MASK]` against 80-10-10 at a matched masking
  rate and reports it, in either direction. What would *not* settle it is
  another model shipping 80-10-10, or shipping without it, since neither comes
  with the comparison — the whole problem with this rule is that it spread
  without one.
title: "Replace every masked token with [MASK]; drop BERT's 80-10-10 substitution rule"
version: 1
tags:
- representation-and-encoding
- training-optimization
date: '2026-09-25'
source:
- LIT-672
- LIT-670
# LIT-672 is the measurement. LIT-670 is the paper that introduced the
# rule this practice drops, and is listed as evidence because its own ablation
# is part of the case: the two rows differ by 0.1 on MNLI (ADR-030).
introduced_by:
- LIT-672
implementations: []
summary: >-
  Wettig et al. (2022), [LIT-672](../literature.d/LIT-672.md). BERT replaced 10% of selected positions
  with the original token and 10% with a random token, to reduce the
  pretrain/fine-tune mismatch caused by `[MASK]` never appearing downstream.
  Measured against an all-`[MASK]` baseline at a matched 40% rate, **80-10-10 is
  worse on everything but SST-2** — and the stated motivation does not bite,
  because "the model can adapt to full, uncorrupted sentences, regardless of the
  use of alternative corruption strategies in pre-training".
---

# SOTA-406: Replace every masked token with [MASK]; drop BERT's 80-10-10 substitution rule

## Source

Wettig, Gao, Zhong and Chen (2022), [LIT-672](../literature.d/LIT-672.md) —
[ARXIV-2202.08005](https://arxiv.org/abs/2202.08005), measuring against the rule
[LIT-670](../literature.d/LIT-670.md) introduced.

## What to do

When a position is selected for prediction, replace it with `[MASK]`. Do not
keep 10% of them unchanged and do not substitute a random token for another 10%.

## Why the rule existed, and why it does not hold

BERT's reasoning was a distribution mismatch: `[MASK]` never appears during
fine-tuning, so a model trained only on `[MASK]` inputs is being asked to
generalise to sentences it has never seen. The 80-10-10 mix was meant to keep
some uncorrupted and some differently-corrupted positions in the training
distribution. Almost every MLM since copied it.

Two things undercut it.

**The rule's own evidence was thin from the start.** BERT's only ablation of it
is Appendix C.2, whose table is headed "Masking Rates" and holds the selection
rate at 15% while varying the mix. The 80/10/10 row scores **84.2** on MNLI and
the 100/0/0 row scores **84.3** — the all-`[MASK]` condition is *already ahead*,
by an amount nobody should read either way. The paper kept the mix on the
argument rather than on the number.

**The mismatch does not materialise.** Wettig et al. measure it directly and
report that "the model can adapt to full, uncorrupted sentences, regardless of
the use of alternative corruption strategies in pre-training". Fine-tuning has
enough signal to close the gap the rule was insuring against.

**And the mix is worse.** Against a 40%-masking all-`[MASK]` baseline,
80-10-10 loses on every task except SST-2, where the same-token predictions do
help. Read through the corruption/prediction decomposition the same paper
builds, the reason is legible: same-token predictions "neither count towards the
corruption nor to the prediction" — they neither remove context nor teach much —
and the loss on randomly-substituted tokens is slightly *higher* than on
`[MASK]`, because the model must also work out whether a given input token is a
corruption at all.

## Conditions

**Encoder MLM, one group, one architecture family.** Everything above is
measured on masked language models between 51M and 354M parameters, on GLUE and
SQuAD. Denoising objectives with a different corruption vocabulary are not
covered.

**SST-2 is a real exception, not noise to wave away.** Same-token predictions
help there, in both this comparison and BERT's own C.2 feature-based column. If
a single sentence-classification target is what you are optimising, check it.

**This is a recommendation against an inherited default, which is a weaker
position than it sounds.** Nobody has published the comparison in the other
direction either. The `promote_when` asks for that comparison from a second
group and explicitly refuses to count another model merely shipping the rule, or
merely dropping it — that is how the rule spread in the first place.

## Known implementations

- **None to name for the recommendation.** For the rule it drops: BERT,
  RoBERTa, SpanBERT and DeBERTa all use 80-10-10, which is why the practice is
  worth stating.
