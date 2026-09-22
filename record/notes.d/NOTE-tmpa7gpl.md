---
status: Read
paper: LIT-tmpu3ldd
title: 'ReFT'
version: 1
date: '2026-09-22'
summary: >-
  A learned low-rank edit to the residual stream at a few prompt positions,
  with the model frozen. Up to 65× fewer parameters than LoRA. It leads on
  commonsense QA and on GPT-4-judged instruction following, is level on
  GLUE, and loses on arithmetic chain of thought. All baselines are copied
  from earlier papers. Read §1–6 and Appendix D; the other appendices
  were not read.
---

<!-- inactive-ok-file: SOTA-tmpx0l6h — Proposed, filed in this same contribution from this paper; new, not retired, and cited as the practice this document sources -->

# NOTE-tmpa7gpl: ReFT

## Contribution

A PEFT family that trains interventions on activations, not deltas to
weights, and one instance (LoReFT) that is very small and competitive on
short-output tasks. It also brings interpretability's intervention tools
into fine-tuning.

## Key insight

**If a concept lives in a linear subspace of the residual stream, steering
that subspace is a cheaper handle than changing the weights that produce
it.** LoReFT is the distributed interchange intervention of causal
abstraction, with the counterfactual source replaced by a learned linear
map of the current state.

## Assumptions

- **A frozen base model**, loaded in bf16, one GPU per run
- **Intervention sites** are the first `p` and last `s` prompt positions at
  chosen layers. Generated tokens are not intervened on
- **Hyperparameters** are tuned on development sets (GSM8K-derived for the
  reasoning suites, Alpaca-52K for instructions), then reused
- **Models:** LLaMA-1 7B/13B, Llama-2 7B, Llama-3 8B, RoBERTa base/large

## Key results

- **Commonsense170K, 8 tasks (Table 1):** LoReFT averages 80.2 / 83.3 /
  81.8 / 86.6 on LLaMA-7B / LLaMA-13B / Llama-2 7B / Llama-3 8B. LoRA
  averages 74.7 / 80.5 / 77.6 / 80.8, and DoRA 78.1 / 81.5 / 79.7 / 85.2. That
  is at 0.03% of parameters against LoRA's 0.7–0.8%
- **Math10K, 4 tasks (Table 2):** LoReFT 42.6 / 49.6 against LoRA 46.9 /
  51.1 (7B / 13B). The GSM8K gap is largest: 26.0 against 37.5 at 7B
- **Instruction following (Table 3):** LoReFT 85.60 win rate, LoRA 81.48,
  full FT 80.93, RED 81.69. With 1K examples, 81.91
- **GLUE (Table 4):** RoBERTa-large LoReFT 88.2, LoRA 88.1, full FT 88.6.
  At base size DiReFT is worse than most PEFTs

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | LoReFT beats weight-based PEFTs on short-answer commonsense QA at a fraction of the parameters | moderate | 4 models, 3 seeds, but the baselines are copied from other papers |
| C2 | It is worse than LoRA on multi-step arithmetic with chain of thought | moderate | Table 2, stated by the authors |
| C3 | It beats full fine-tuning at instruction following | weak | one model, GPT-4 judge, AlpacaEval v1, baselines copied |
| C4 | It is as good as other PEFTs on small encoders | moderate | GLUE, 5 seeds |
| C5 | Editing representations is more powerful than editing weights | weak | the paper's framing; the results are mixed by task |

## Method

`Φ(h) = h + Rᵀ(Wh + b − Rh)`, where `R ∈ ℝ^{r×d}` has orthonormal rows and
`W ∈ ℝ^{r×d}`, `b ∈ ℝ^r`. It is applied at layer `l`, positions `P`, and
changes everything downstream. The loss is ordinary cross-entropy on the
outputs, with a classification head for GLUE.

## Concepts

- **Intervention** — a triple of function, positions and layer, applied in
  the forward pass
- **DII** (distributed interchange intervention) — `b + Rᵀ(Rs − Rb)`, which
  sets a subspace of one run's state to its value in another run

## Connections

It generalizes activation steering (fixed steering vectors) and RED
(learned scaling and bias on representations) by learning a subspace edit.
DiReFT is LoRA's form applied to activations. It compares against LoRA
([LIT-046](../literature.d/LIT-046.md)) and DoRA using those papers' numbers.

## Recommendations

- **R1** — For classification and short-answer tasks, try LoReFT before a
  weight adapter when trainable parameters or adapter storage are the
  constraint. *Strength:* weak to moderate. Filed as [SOTA-tmpx0l6h](../practices.d/SOTA-tmpx0l6h.md)
- **R2** — Do not use prompt-position interventions for long chain-of-thought
  generation. *Strength:* moderate. Part of [SOTA-tmpx0l6h](../practices.d/SOTA-tmpx0l6h.md)

## Bearing on the record

- **[SOTA-184](../practices.d/SOTA-184.md)** (LoRA) is not overturned. On the tasks where LoRA is used
  hardest, reasoning and long generation, this paper's own numbers favour
  LoRA
- **[SOTA-231](../practices.d/SOTA-231.md)** (adapters on every linear layer) is about where weight
  adapters go, and this paper does not test it

## Limitations

- **Cross-paper baselines**, which the authors partly justify by the
  baselines' own tuning practices
- **LLaMA-family decoders and RoBERTa only**, at 13B at most
- **A large search space** (positions, layers, tying), which the authors
  list as a limitation
- **The GPT-4-judged instruction result** is the least robust kind of
  evaluation in the paper

## Open questions

- Whether intervening on generated positions as well closes the
  chain-of-thought gap, or whether the gap is intrinsic
- A head-to-head against LoRA and DoRA under one tuning protocol
