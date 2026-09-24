---
status: Active
title: 'Scaling Language Models: Methods, Analysis & Insights from Training Gopher'
version: 1
tags:
- analysis-and-evaluation
- training-optimization
- capability-thresholds
date: '2026-09-24'
published: '2021-12-01'
arxiv: '2112.11446'
first_author: 'Rae'
keywords:
- 'gopher'
- 'scale-analysis'
- 'nonuniform-scaling'
- 'inverse-scaling'
- 'stochastic-rounding'
implementations:
- gopher
compared_against:
- LIT-068
summary: >-
  Rae et al. (2021), [ARXIV-2112.11446](https://arxiv.org/abs/2112.11446). Six models on one dataset at one token
  budget, 44M to 280B, evaluated on 152 tasks — a controlled study of
  parameter scale. **The gains are nonuniform**: 51.2% of tasks improve by
  over 25%, 10.5% not at all, and Gopher is *worse* than its own smaller
  models on Abstract Algebra, Temporal Sequences and High School Mathematics.
  Also the allocation [LIT-068](LIT-068.md) corrects: 280B parameters on 300B tokens is
  **1.07 tokens per parameter** against Chinchilla's 20.
---

# LIT-tmpkxt2i: Scaling Language Models: Methods, Analysis & Insights from Training Gopher

Rae et al. (2021), DeepMind — [ARXIV-2112.11446](https://arxiv.org/abs/2112.11446)

## Key takeaways

- **It is a controlled study of parameter scale, and says so.** Six models
  from 44M to 280B, **all trained on the same dataset for the same 300B
  tokens** — "this allows us to isolate the effect of scaling parameters and
  training compute for each task". That property is what makes the scale
  analysis worth more than a model report, and it is rarer than it sounds.

- **The headline is the nonuniformity, quantified.** Gopher against the best
  of the family up to 7.1B, over 152 tasks:

  | relative improvement | tasks | share |
  | --- | --: | --: |
  | over 25% | 79 | 51.2% |
  | up to 25% | 57 | 37.5% |
  | zero or none | 16 | 10.5% |

  Largest gains in Medicine, Science, Technology, Social Sciences and the
  Humanities. The extreme case is BIG-bench Figure of Speech Detection:
  **16.8% → 52.7%, a 314% relative increase**.

- **Scale made three tasks worse, and they are named.** Abstract Algebra and
  Temporal Sequences from BIG-bench, and High School Mathematics from MMLU —
  Gopher below its own smaller models. Measured inverse scaling inside a
  controlled family, which is a stronger form of the observation than a
  cross-model comparison can give.

- **Maths, logical reasoning and common sense benefit least**, and the
  authors distinguish the two reasons: for maths and logic *"it is unlikely
  that scale alone will lead to performance breakthroughs"*, whereas the
  modest common-sense gains are because the small models were already strong
  and there was little headroom. Language modelling shows the smallest
  average improvement for a third reason — it is scored in BPB, which limits
  relative movement. **Three different causes behind one small number**, and
  the paper separates them rather than reporting "diminishing returns".

- **TruthfulQA goes the other way from other families.** Performance improves
  from 1.4B to 280B here, *"despite scale appearing to hurt performance for
  several other model families such as GPT-J, GPT-2, T5, GPT-3"*, and 280B is
  the first model significantly beyond random guessing on the multiple-choice
  formulation.

- **Two numerics findings, one of them negative.** Gradient norm clipped at
  1.0, **reduced to 0.25 for the 7.1B and 280B models for stability**.
  And bfloat16 parameters were updated with stochastic rounding, after which:
  *"**We subsequently found that stochastic rounding does not fully recover
  mixed precision training performance.**"*

- **Architecture and schedule, for the record.** RMSNorm rather than
  LayerNorm; Transformer-XL relative position encodings rather than absolute,
  chosen so evaluation can exceed the training length; SentencePiece at 32k
  with byte-level backoff; Adam, 1500-step warm-up from `10⁻⁷`, cosine decay
  by 10×; maximum learning rate falling from `6×10⁻⁴` at 44M to `4×10⁻⁵` at
  280B; Gopher's batch size **raised from 3M to 6M tokens during training**.

## Standing in the anthology

Unit 1 of `#326`, and the record's dependence here is on the paper this one
loses to. **48 files say "Chinchilla"**, `LIT-068` holds it, and twelve
practices and theories cite it — `SOTA-096` is the `20 × params` ratio
itself. Gopher is the allocation that ratio was derived against, and the
arithmetic is the point: **280B parameters on 300B tokens is 1.07 tokens per
parameter, roughly nineteen times under-trained by the rule the record now
recommends.**

Unit E's shape, at the scale where it costs most: the record held the winner
of a named comparison, the rule that comparison produced, and twelve
documents downstream of the rule, and not the run that made the rule worth
publishing. `SOTA-096` attributes the superseded practice to `LIT-028`
(Kaplan et al.), which is correct about the *prescription* — this is the
280-billion-parameter instance of following it.

**`compared_against: LIT-068` rather than `corrected_by:`,** deliberately.
Chinchilla ran the comparison, which is what `ADR-011` requires of the
field, and that is verifiable. What Chinchilla corrects is Kaplan's
allocation rule; Gopher is the instance rather than the claim, and filing
the relation as a correction would overstate what this paper asserted.

**The compression conjecture is recorded here and not filed as a theory.**
The conclusion offers an account of the nonuniformity — *"it is hard to
compress mathematics and easier to learn many associative facts about the
world"* — and immediately names its own alternative, that reasoning may
emerge beyond this scale. It is adjacent to `THEORY-050`, which holds that
parameters carry memorization and parallel computation carries reasoning, and
it does **not** meet that theory's `promote_when`: a conjecture in a
discussion section is not the within-corpus exchange-rate measurement being
asked for. Filed as a reading, not as evidence.

Primary topic `analysis-and-evaluation` rather than `model-architecture`:
what the record needs is the 152-task scale analysis, not the architecture
(`ADR-046`).
