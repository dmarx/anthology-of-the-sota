---
number: 139
status: Active
title: 'Extend the context length in stages during pretraining rather than training at the target length from the start'
version: 1
tags:
- training-optimization
- attention-techniques
date: '2026-09-05'
source:
# LIT-tmpkql17 (Shortformer) added in the correction pass: the only
# controlled comparison against training at the target length throughout.
# LIT-139 runs the schedule and does not ablate it (NOTE-361).
- LIT-139
- LIT-tmpkql17
introduced_by:
# Was LIT-139. DeepSeek-V4 runs the schedule and does not originate it.
# BERT (LIT-670, Oct 2018) trained at 128 tokens for 90% of steps and 512 for
# the rest, and Shortformer (LIT-tmpkql17) names BERT as where the routine
# was first applied before testing it.
- LIT-670
summary: >-
  DeepSeek-AI (2026), [LIT-139](../literature.d/LIT-139.md) — 4K, then 16K, 64K and 1M over 32–33T tokens, with sparse attention introduced at the 64K stage; Kimi K3 ([LIT-131](../literature.d/LIT-131.md)) reaches 1M the same way.
---

# SOTA-139: Extend the context length in stages during pretraining rather than training at the target length from the start

## Source

DeepSeek-AI (2026), [LIT-139](../literature.d/LIT-139.md) — DeepSeek-V4.

Press, Smith and Lewis (2020), LIT-tmpkql17 — Shortformer.

## The schedule

Start pretraining at a short sequence length and lengthen it in stages:
V4 trains at 4K, then 16K, 64K and finally 1M tokens, and schedules its
architectural switch — sparse attention on — at the 64K stage. Kimi K3
([LIT-131](../literature.d/LIT-131.md)) reports the same shape of schedule to its own 1M window, adding
synthetic tasks that can only be solved by attending across the whole
window. The short stages are where most tokens are cheapest to process; the
long stages teach the position-dependent behaviour the target length needs.

What [LIT-139](../literature.d/LIT-139.md) supplies is the schedule as run, not a test of it: §4.2.2 gives
4K → 16K → 64K → 1M over 32–33T tokens, with dense attention for the first
1T tokens on Flash (longer on Pro) and sparse attention switched on at 64K
after a short indexer warm-up, and the close reading ([NOTE-361](../notes.d/NOTE-361.md)) finds no
ablation of the staging. The outcome it reports is a working 1M window, with
MRCR 1M at 83.5 for V4-Pro-Max and MRCR stable to 128K and degrading beyond.

## Where it comes from, and the test the record holds

The schedule is older than either frontier report. BERT, LIT-670, is where
it was first run: pretraining at 128 tokens for 90% of the steps and 512 for
the rest, because "longer sequences are disproportionately expensive because
attention is quadratic to the sequence length", with the short final stage
there "to learn the positional embeddings". That is both halves of the
reasoning above, in 2018, and the record names BERT as the origin.

BERT used it only for speed. Shortformer, LIT-tmpkql17, is what tested it
against training at the target length throughout, crediting BERT for the
routine. On WikiText-103 with a 247M model and a final length of 3,072,
starting at 128 tokens for the first 50 of 205 epochs gave 17.52 dev
perplexity against 18.65 for the baseline, in 87% of its training time, and
every first stage of 1,024 tokens or less that switched by epoch 125 beat the
baseline by a large margin. More than two stages, up to six, did no better.

## Conditions

The frontier reports are not controlled comparisons against training at the
target length throughout, and neither publishes the token split per stage in
the material read here; the controlled comparison the record holds, Shortformer's, is at
3,072 tokens and 247M parameters, a long way from a million-token window and
from a sparse-attention switch partway. The practice is stated because the
small-scale test favours it and two independent laboratories converged on it
for million-token contexts; the stage boundaries and what to switch on at
each are the parts to tune.

## Known implementations

- DeepSeek-V4, Kimi K3
