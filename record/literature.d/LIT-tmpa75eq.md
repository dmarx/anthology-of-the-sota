---
status: Active
title: 'Cramming: Training a Language Model on a Single GPU in One Day'
version: 1
tags:
- training-optimization
- tiny-models
- model-architecture
- data-pipeline
- model-stability
- analysis-and-evaluation
date: '2026-09-25'
published: '2022-12-28'
arxiv: '2212.14034'
first_author: 'Geiping'
keywords:
- 'compute-constrained-pretraining'
- 'masked-language-modeling'
- 'scaling-laws'
- 'throughput'
- 'data-filtering'
- 'negative-results'
implementations:
- 'cramming (github.com/JonasGeiping/cramming)'
compared_against:
- LIT-670
- LIT-672
- LIT-052
summary: >-
  Geiping and Goldstein (ICML 2023), [ARXIV-2212.14034](https://arxiv.org/abs/2212.14034). A BERT-style MLM
  trained from scratch for 24 hours on one consumer GPU, which reaches 79.2–80.4
  GLUE against BERT-base's 80.9. The transferable finding is negative: **model
  shape does not beat the scaling law at this budget**. Every reshape it tried
  lands near the same final loss, because a smaller model's extra throughput
  cancels its slower learning. So the only architectural lever is to cut step
  time at constant parameter count. Its data result is the cheapest filter in
  the record: drop text the tokenizer compresses badly.
---

<!-- inactive-ok-file: SOTA-tmpkawow SOTA-tmphcbvi — Proposed, and named as the two practices
     this paper sources; they are filed with it at Proposed because one study is
     what stands behind each -->

<!-- inactive-ok-file: SOTA-405 — Proposed; named to say this paper does NOT meet
     its promote_when, which is the point of the sentence -->

# LIT-tmpa75eq: Cramming: Training a Language Model on a Single GPU in One Day

Geiping and Goldstein (2022; ICML 2023) — [ARXIV-2212.14034](https://arxiv.org/abs/2212.14034)

**Read in the ICML version (PMLR 202), not arXiv v1.** The two differ in
numbers and in one decision. v1's headline table has crammed BERT at
**78.6** GLUE on an A6000. The ICML table has it at **80.4**, after a change
of dataset (the Pile, filtered and sorted), a batch size of 8192 rather than
4096, and a 25% masking rate. Quote the ICML numbers.

## Key takeaways

**The rules.** An MLM transformer trained from scratch, with no pretrained
model anywhere in the pipeline. That excludes distillation and model-based
data filtering. Any raw text, and preprocessing is not counted against the
budget. **24 hours on one GPU**: an RTX 2080 Ti, an A4000 or an A6000,
which is 5, 8 and 13 exaFLOP of peak compute. Against that, Table 1 puts
the original BERT at 680. Fine-tuning is capped at 5 epochs, with one set
of hyperparameters for every GLUE task.

**Shape does not escape the scaling law.** This is the result the paper is
built on, and it is a controlled one. Many variants (depth 4 to 24,
deep-narrow, width 512 to 1024, funnel, FFN every 2–4 blocks, ALBERT-style
recurrence, heads from 1 to 24) are trained with the same budget and recipe.
Figure 1 shows the loss curves "differ by only a multiplicative constant" after
the first billion tokens, and "this constant depends almost entirely on the
model size, not model shape, so that all choices reach a MLM loss around 1.9".
Smaller models learn less per token and ingest more tokens, and the two
cancel. Table 11, all on an A4000:

| variant | MLM loss | MNLI-m | tokens/s |
| --- | --- | --- | --- |
| 4 layers | 1.94 | 79.13 | 161,034 |
| 8 layers | 1.84 | 81.22 | 88,652 |
| 12 layers | 1.85 | 81.68 | 59,346 |
| 24 layers | 1.97 | 80.81 | 30,455 |
| Recurrent (4-3) | 1.91 | 81.43 | 61,596 |
| BERT-Large variant | 2.12 | 79.50 | 17,688 |

From 4 layers to 24, throughput falls more than **5x** while the final loss stays
between 1.84 and 1.97 and MNLI-m between 79.1 and 81.7. The paper does find an optimal size "at a budget of around 4B
tokens", but "gains from model size optimization are small at this compute
scale".

**So the lever is step time at constant size.** "Because per-gradient
efficiency remains nearly constant for all models of the same size, we can
exploit scaling laws by searching for architectural choices that speed up
computation while keeping model size roughly constant." In practice that means
removing QKV and linear-layer biases and the decoder bias, predicting only the
masked tokens, and using a pre-norm layer structure, which enables the larger
learning rate. Each change is small, and the paper says so ("marginal but
worthwhile/free gains").

**The architecture half cannot be separated from the training half.** Table 5
resets one group at a time to the original BERT. With the original
architecture training **fails outright**, and with the original training
recipe the model is "close to random performance" (50.5 GLUE). The paper's
attribution — "about two percentage points gained in average GLUE score
through either architectural changes, data changes, or training
modifications" — comes from the rows with *minimal* modifications, 78.0 and
78.3 against 80.4. A reader should not take those two points per group as
independent effects, because the groups only work together.

**The data result: filter by the tokenizer's compression ratio.** Drop every
entry whose token count exceeds `t` times its character count (`t = 0.25`),
which removes "hard-to-compress HTML" and similar text. No model is involved.
Table 2, GLUE, one pretraining run per cell:

| source | none | filtered | filtered + sorted |
| --- | --- | --- | --- |
| bookcorpus-wikipedia | 78.1 | 78.7 | 78.8 |
| C4 | 75.9 | **79.3** | 79.0 |
| OSCAR | 79.1 | 79.2 | 79.2 |
| Pile | 78.2 | 79.3 | 80.1 |
| Pile (natural sources) | 79.2 | 79.8 | 80.1 |

The filter is worth the most where the source is dirtiest, as expected: C4
gains **3.4**, while already-clean bookcorpus-wikipedia gains 0.6.
Deduplication (exact substring, length 75) does "not reliably help". The best
sort order is short sentences first. That was chosen over sorting by unigram
prevalence, which v1 had used. Its gain is within the size of the other
cells' differences.

**Two findings about what to measure.** The batch size that minimizes
pretraining loss is about **2048**, and the one that maximizes MNLI is about
**8192** (Figure 3). Selecting on pretraining loss would have picked the
wrong one. The paper says it chose "not to make this a focus". And v1's data
section compared data changes by downstream score only: "changes in
pretraining loss [are] not very meaningful" across different corpora and
tokenizers.

**Dropout is off in pretraining and back on for fine-tuning.** The argument
is that a single epoch cannot overfit, and dropout "effectively reduces the
number of gradient updates seen by each parameter". There is one measured
row: "With Dropout activated", 80.95 MNLI-m against 81.79 without (Table 12).
The *argument* about updates per parameter is not measured. The *outcome* is,
once.

**Negative results carry most of the value, and they get a whole appendix.**
None of these helped at this budget: funnel transformers, dropping FFN
layers, recurrent layers (even with BPTT), deep-narrow rescaling, FLASH
attention, Fourier attention, rotary embeddings (a gain in loss but a loss
in speed), softmax replacements, RMSNorm instead of LayerNorm, factorized or
untied embeddings, Adafactor, higher-order optimizers, length curricula,
token dropping, adaptive batch rules, and MSE or L1 in place of cross-entropy.
Each is a single run at one budget, and none is a claim about scale.

## Traps

**The 25% masking rate is a throughput choice, and the paper's own sweep does
not support it as a quality one.** The ICML main text says it trains "with a
masking rate of 25%" and that "the increased masking rate provides benefits
at almost no extra cost, as the original 15% results in inopportune tensor
shapes, whereas 25% of micro-batch size and sequence length neatly falls on
the next power of 2". With sparse prediction over sequences of 128 tokens,
25% is 32 predicted tokens and 15% is 19.2. The benefit is kernel shape.
Meanwhile Appendix C.3, carried over unchanged from v1, still reads "We see
no improvement from masking at larger rates, e.g. at 40% as proposed in
(Wettig et al., 2022)". The only rate table (Table 12, A4000,
bookcorpus-wikipedia, batch 4096) has **no 25% row**:

| rate | MLM loss | MNLI-m | MNLI-mm |
| --- | --- | --- | --- |
| 15% (the adopted recipe's row; the table does not label its rate) | 1.84 | 81.79 | 82.14 |
| 20% | 2.06 | 80.76 | 81.48 |
| 40% | 2.70 | 81.11 | 81.30 |
| 60% | 3.41 | 80.62 | 80.88 |

MLM loss is not comparable across rates, so only the MNLI columns count. They
put **15% at or near the top, and the order is not monotone**: 20% is below
40%. With one pretraining run per row, a one-point difference here is inside
the noise. So a reader who takes "Cramming uses 25%" as evidence about the
optimal rate is reading a tensor-shape decision as a measurement. This is
the second masking rate in two days to turn out declared rather than swept,
after [LIT-670](LIT-670.md)'s 15%.

**"Close to BERT" is on GLUE with a global hyperparameter set, and CoLA is
where it is not close.** Crammed BERT on an A6000 scores 51.8 CoLA against
BERT-base's 56.5 under the same protocol. The paper offers three hypotheses
and tests none of them. On SuperGLUE, with the same untuned protocol, the
average is 54.2 against 56.6.

**It is a BERT-base-sized model, not a tiny one.** The paper never states a
parameter count. The model is BERT-base-shaped, and the ICML text reports
"minimal gains by increasing the number of layers to 16". What is
small is the *budget*, not the model. It is tagged `tiny-models` because it
is a controlled study at the small-compute end. Its central finding is that
the ordinary scaling behaviour *does* hold there, which is the opposite of
what that topic usually collects.

## Standing in the anthology

Filed as substrate from the reading-time triage of 2026-09-25. It is the
controlled study the record's masked-language-modelling neighbourhood was
missing, and the paper the record held BERT, RoBERTa and Wettig et al.
without.

- **It sources two practices.** `SOTA-tmpkawow`: under a fixed budget,
  change the architecture only where it cuts step time at constant parameter
  count. `SOTA-tmphcbvi`: filter pretraining text by its tokenizer compression
  ratio.
- **It joins [SOTA-240](../practices.d/SOTA-240.md)'s evidence** as a second
  language-model confirmation of the right edge. A single-epoch run cannot
  memorize, and turning dropout on costs 0.8 MNLI in the one row that measures
  it.
- **It is one size's worth of data for [SOTA-405](../practices.d/SOTA-405.md), and
  does not meet that practice's `promote_when`**, which asks for a sweep at
  more than one size. At roughly BERT-base size and a one-GPU-day budget, 15% is
  at or near the top of a four-point sweep whose differences are within
  single-run noise. That is consistent with a flat optimum at this capacity.
  It says nothing about the optimum *moving*. What it adds is a warning
  about citation. The paper that ships 25% is not evidence for 25%.
- **Its recurrent-layer rows bear on two later filings.** ALBERT-style
  recurrence "(4-3)" reaches 81.43 MNLI against 81.68 for 12 unshared layers,
  at about the same throughput. The same first author later built a
  recurrent-depth model (`2502.05171`). That is a different claim, about
  test-time compute, which this paper did not test.
