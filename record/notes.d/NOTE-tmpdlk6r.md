---
status: Read
paper: LIT-tmpu3hfw
title: 'QLoRA: Efficient Finetuning of Quantized LLMs'
version: 1
date: '2026-09-17'
summary: >-
  Store the frozen base in 4 bits, compute in 16, and train only LoRA
  adapters: 65B fine-tuning goes from >780GB to <48GB with no measured loss
  against a 16-bit fully fine-tuned baseline. The quantization is the
  headline; the more useful result for anyone already using LoRA is that the
  standard query/value placement does not reach full fine-tuning at scale,
  and that the adapter count rather than the rank is what closes the gap.
---

# NOTE-tmpdlk6r: QLoRA: Efficient Finetuning of Quantized LLMs

Read from [LIT-tmpu3hfw](../literature.d/LIT-tmpu3hfw.md) — [ARXIV-2305.14314](https://arxiv.org/abs/2305.14314).

## What the method actually is

Two data types, and keeping them straight is what makes the paper read
clearly. There is **one storage type**, normally 4-bit NormalFloat, and **one
computation type**, BFloat16. Whenever a weight tensor is used it is
dequantized to BFloat16 and the matrix multiply happens in 16 bits. Gradients
flow back through that dequantized base but are only *computed* for the LoRA
parameters, which are themselves BFloat16.

So nothing is ever multiplied in 4 bits. The quantization buys resident
memory for the frozen weights and nothing else, which is precisely why it
costs no accuracy: the arithmetic is unchanged from 16-bit LoRA.

Three components, in decreasing order of how interesting they are:

1. **NF4**, a data type whose quantiles are placed for a normal distribution
   rather than uniformly. The paper's claim of information-theoretic
   optimality is for normally distributed data, and it checks empirically
   rather than resting on the theory — Int4 **34.34**, Float4 (E2M1)
   **31.07**, Float4 (E3M0) **29.48**, NF4 + double quantization **27.41**
   mean Pile Common Crawl perplexity, over 125M–13B OPT, BLOOM, LLaMA and
   Pythia.
2. **Double quantization** — quantize the per-block quantization constants
   too. About **0.37 bits per parameter**, roughly 3GB on a 65B model. Small,
   and the kind of saving that decides whether a model fits.
3. **Paged optimizers** — optimizer state paged between GPU and CPU on
   unified memory, to survive gradient-checkpointing spikes. An engineering
   answer to an OOM, not a claim about learning.

Headline: **>780GB → <48GB** to fine-tune 65B, "without degrading the runtime
or predictive performance compared to a 16-bit fully fine-tuned baseline".

## The result that is not about quantization

Buried under the memory headline, and the reason this paper is worth reading
if you already use LoRA and never intend to quantize anything:

> When using the standard practice of applying LoRA to query and value
> attention projection matrices, we are not able to replicate full finetuning
> performance for large base models. […] the most critical LoRA hyperparameter
> is how many LoRA adapters are used in total and that LoRA on all linear
> transformer block layers are required to match full finetuning performance.
> Other LoRA hyperparameters, such as the projection dimension `r`, do not
> affect performance.

Two things follow, and they point in opposite directions from the usual
advice. **The knob people tune is inert** — `r` does not matter across their
sweep. **The knob people leave at its default is the one that decides whether
the method works at all** — which matrices carry adapters.

It is also a methodological point worth noticing: they found this because they
also re-tuned the *baseline*. The paper says the default hyperparameters for
fully fine-tuned baselines are undertuned, and searches learning rate 1e-6 to
5e-5 and batch size 8 to 128 to get a fair one. A weaker baseline would have
let the default Q/V placement look adequate.

## What this does to the record

Sources two practices, and they are separable claims: the quantized-base
method, and the placement rule. Neither depends on the other — you can apply
the placement finding to ordinary 16-bit LoRA and get the benefit without
quantizing anything.

The placement result **qualifies [SOTA-184](../practices.d/SOTA-184.md)** rather than contesting it.
That practice already says rank does well small on the LoRA paper's tasks;
this adds a second observation agreeing about `r`, and supplies the variable
that was missing. Nothing in [SOTA-184](../practices.d/SOTA-184.md) is wrong; it was silent where a
reader needed a number, and the silence read as "the default is fine".

Not filed from this paper: the Guanaco results and the chatbot evaluation.
The paper's own limitations section says current chatbot benchmarks are not
trustworthy, and it argues GPT-4 evaluation is a cheap proxy while showing
where it disagrees with humans — an argument about evaluation methodology
that belongs to whoever files the evaluation practices, not here.
