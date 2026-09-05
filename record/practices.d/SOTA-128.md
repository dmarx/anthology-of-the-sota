---
status: Active
title: 'Train fill-in-the-middle data without masking the loss on non-FIM tokens'
version: 1
tags:
- data-pipeline
- tiny-models
date: '2026-09-05'
published: '2026-01-15'
source: LIT-119
summary: >-
  Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost. At 80 GT and 90M, computing the loss on every token beat masking the prefix and suffix; matches what the reference FIM recipes appear to do.
---

# SOTA-128: Train fill-in-the-middle data without masking the loss on non-FIM tokens

## Source

Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost.

Whether to mask the loss on the prefix and suffix of a FIM sample, as one
would mask a prompt in SFT, is left unstated in [ARXIV-2207.14255](https://arxiv.org/abs/2207.14255) and only
implicit in [ARXIV-2409.12186](https://arxiv.org/abs/2409.12186). Two 90M runs on the same mix (80% FIM, 10%
code, 10% web and math), 80 GT with 20 GT of decay, one masking the
non-middle tokens and one not: the unmasked run was clearly better across
the coding benchmarks. The authors note the unmasked run simply trains on
more tokens for the same budget, and conclude that for a fixed token and
compute budget the unmasked data is the more efficient use of it — FIM
samples serve both the infilling objective and next-token prediction.

Two further details from the same work, worth carrying with the practice:
use PSM format with dedicated `<|prefix|>`, `<|suffix|>`, `<|middle|>`
tokens; and construct samples in which the model must produce the
indentation after the prefix itself, since HumanEval-FIM prompts do not
include it and a model that never had to predict indentation starts a new
function instead.

## Known implementations

- Falcon-H1-Tiny-Coder-90M
