---
number: 162
status: Active
formerly:
- SOTA-tmpekps6
consensus: emerging
consensus_note: >-
  Three labs ship it — DeepSeek-V3 and V4, Kimi K3, Qwen3-Next and Qwen3.8 —
  and each report names it as settled rather than arguing for it. Not
  `converged`: Olmo 3, Llama 3 and the Falcon line do not carry an MTP head,
  and no adopter ablates it, so what the record has is wide adoption without
  a second measurement.
title: 'Train with auxiliary multi-token-prediction heads alongside next-token prediction'
version: 1
tags:
- training-optimization
date: '2026-09-08'
published: '2024-04-01'
source:
# The paper that measured it. The five model reports that ship an MTP head
# name it as settled and none of them ablates it, so they are adoption and
# live in consensus_note (ADR-017).
- LIT-163
implementations: []
summary: >-
  Gloeckle et al. (2024), [LIT-163](../literature.d/LIT-163.md) — predict the next n tokens through n
  independent heads on a shared trunk, as an auxiliary task rather than a
  replacement. No training-time overhead, the benefit grows with model size
  and survives multi-epoch training, and the extra heads are a draft model
  you already trained.
---

# SOTA-162: Train with auxiliary multi-token-prediction heads alongside next-token prediction

## Source

Gloeckle et al., Meta (2024), [LIT-163](../literature.d/LIT-163.md) — [ARXIV-2404.19737](https://arxiv.org/abs/2404.19737).

At each position, ask the model to predict the following **n** tokens through
n independent output heads on a shared trunk. It is an *auxiliary* objective,
not a replacement: next-token prediction stays, and the extra heads are
supervision on top of it. That framing is what keeps the change cheap.

## Why this is a design choice and not a trick

Two properties, and both are the kind that usually fail:

- **The benefit grows with model size.** Most auxiliary objectives help small
  models and wash out; this does the opposite.
- **It survives multi-epoch training**, which is where auxiliary supervision
  normally stops paying.

Reported at no overhead in training time, for code and natural language
alike; strongest on generative benchmarks, with 13B models solving 12% more
HumanEval and 17% more MBPP than comparable next-token models. Small
algorithmic tasks suggest the mechanism: multi-token prediction favours
induction heads.

## The double motive, which nobody has separated

It is sold as a *training* objective that improves the model and pays for
itself, and adopted as an *inference* mechanism — models trained with 4-token
prediction run up to **3× faster** at decode, because the extra heads are a
draft model for speculative decoding you did not have to train separately.

Which of the two is doing the work at frontier scale is not something any
adopting report isolates. That matters for reading this practice: if you want
only the training benefit, the evidence for it is this one paper; if you want
the draft heads, the adoption is overwhelming and the training claim comes
along for free either way.

## Filed late, and the reason is the same as the deduplication one

Five model reports in this record ship an MTP head and each mentions it as
settled. A step everyone agrees on generates no argument, so nothing prompted
a practice — the registry was missing nodes at the too-obvious end as well as
the too-new end.

## Known implementations

- DeepSeek-V3 and V4, Kimi K3 (fine-tuned into an EAGLE-3-style single-layer
  draft model), Qwen3-Next, Qwen3.8-27B.
- Against, by silence: Olmo 3, Llama 3, the Falcon line.
