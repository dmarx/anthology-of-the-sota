---
status: Active
title: 'ReFT: Representation Finetuning for Language Models'
version: 1
tags:
- adaptation-and-tuning
- analysis-and-evaluation
date: '2026-09-22'
published: '2024-04-01'
arxiv: '2404.03592'
first_author: 'Wu'
keywords:
- 'representation-finetuning'
- 'parameter-efficient-finetuning'
- 'interventions'
- 'causal-abstraction'
- 'loreft'
implementations:
- pyreft
compared_against:
- LIT-046
summary: >-
  Wu, Arora et al. (2024), [ARXIV-2404.03592](https://arxiv.org/abs/2404.03592). Freeze the model and train a
  low-rank edit to the hidden state at a few prompt positions:
  `h + Rᵀ(Wh + b − Rh)`, with `R` having orthonormal rows. It uses 15–65×
  fewer parameters than LoRA. It leads on commonsense QA (LLaMA-7B, 80.2
  against LoRA's 74.7), leads on GPT-4-judged instruction following, and is
  level on GLUE. It loses on arithmetic chain of thought (GSM8K 26.0 against
  37.5). Baseline numbers are copied from earlier papers.
---

<!-- inactive-ok-file: SOTA-tmpx0l6h — Proposed, filed in this same contribution from this paper; new, not retired, and cited as the practice this document sources -->

# LIT-tmpu3ldd: ReFT: Representation Finetuning for Language Models

Wu, Arora, Wang, Geiger, Jurafsky, Manning, Potts, Stanford (2024) —
[ARXIV-2404.03592](https://arxiv.org/abs/2404.03592)

## Key takeaways

- **Edit representations, not weights.** An intervention applies a learned
  function to the residual stream at chosen layers and positions. LoReFT's
  function, `h + Rᵀ(Wh + b − Rh)`, sets the projection of `h` onto an
  `r`-dimensional subspace (rows of `R`, kept orthonormal) to a learned
  linear function of `h`. DiReFT drops the orthogonality and the
  difference: `h + W₂ᵀ(W₁h + b)`, which is LoRA applied to a hidden state
- **Where it is applied is a hyperparameter:** the first `p` and last `s`
  prompt positions, a set of layers, and whether positions share
  parameters. Generated tokens are not intervened on, so the added
  inference cost does not grow with prompt length
- **Results, three seeds for ReFT, baselines from earlier papers:**
  - commonsense (8 tasks): LoReFT leads at every size, e.g. LLaMA-7B 80.2
    against DoRA 78.1 and LoRA 74.7. HellaSwag alone is 93.1 against 78.1
  - arithmetic CoT (4 tasks): **LoReFT trails LoRA**, 42.6 against 46.9 at
    7B and 49.6 against 51.1 at 13B. GSM8K is 26.0 against 37.5 at 7B
  - instruction following (Llama-2 7B, AlpacaEval v1 judged by GPT-4):
    85.60 win rate against LoRA 81.48 and full fine-tuning 80.93
  - GLUE (RoBERTa): level with the other PEFTs, not ahead
- **ReFT was tuned on development sets.** The authors say much PEFT work
  tunes on test sets, which, if true of the copied baselines, would favour
  them

## Standing in the anthology

**An alternative to [SOTA-184](../practices.d/SOTA-184.md)'s weight update, filed from `#163`.** The
record's LoRA practice is `Active` and `universal`, and this paper is a
prominent claim that editing hidden states beats editing weights on
parameter count. It sources [SOTA-tmpx0l6h](../practices.d/SOTA-tmpx0l6h.md), which is scoped to where the
evidence points: short outputs, not long reasoning.

**The comparison is not controlled.** Every baseline number is taken from
Hu et al. 2023, Liu et al. 2024 (DoRA) or Wu et al. 2024 (RED). None was
re-run under ReFT's protocol. The paper states its protocol clearly and
criticizes others' test-set tuning, but a cross-paper table cannot settle a
ranking. The authors' own explanation for the arithmetic loss is that
longer generations dilute an intervention made only on prompt positions,
and that points at a structural limit, not a tuning gap.

**Its interpretability roots are why it carries `analysis-and-evaluation`.**
LoReFT is distributed interchange intervention with a learned source, from
the causal-abstraction line of work.

Read — [NOTE-tmpa7gpl](../notes.d/NOTE-tmpa7gpl.md).
