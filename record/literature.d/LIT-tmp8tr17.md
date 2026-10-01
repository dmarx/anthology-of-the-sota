---
status: Active
title: 'SepLLM: Accelerate Large Language Models by Compressing One Segment into One Separator'
version: 1
tags:
- attention-techniques
- inference-optimization
- model-architecture
date: '2026-10-01'
published: '2024-12-16'
arxiv: '2412.12094'
first_author: 'Chen'
# StreamingLLM's cache (initial sink tokens plus a rolling window, positions
# assigned within the cache) is SepLLM's cache minus the separators, and the
# paper runs it as the baseline at matched KV budget throughout.
extends:
- LIT-191
compared_against:
- LIT-191
keywords:
- 'separator-tokens'
- 'sparse-attention'
- 'kv-cache-compression'
- 'attention-sinks'
- 'streaming'
- 'training-free'
- 'flexattention'
implementations:
- 'sepllm.github.io'
summary: >-
  Chen et al. (2024), [ARXIV-2412.12094](https://arxiv.org/abs/2412.12094) — SepLLM. Let each token attend only
  to a few initial tokens, the previous n tokens, and every earlier separator
  token (punctuation and whitespace), on the hypothesis that a segment's
  content is condensed into the separator that ends it. Training-free on
  Llama-3-8B-Instruct it keeps GSM8K-CoT at 77.18 against 77.79 with 47% of
  the KV cache, where StreamingLLM at the same budget gets 70.89. Trained
  that way from scratch at 160M it reaches lower loss than full attention at
  equal FLOPs.
---
<!-- inactive-ok-file: THEORY-tmp7q4tl — Proposed, named as the theory filed from this paper, which sets out both readings -->

# LIT-tmp8tr17: SepLLM: Accelerate Large Language Models by Compressing One Segment into One Separator

Chen et al., Huawei Noah's Ark Lab and The University of Hong Kong (2024) — [ARXIV-2412.12094](https://arxiv.org/abs/2412.12094)

## Key takeaways

- **The observation.** Visualised attention in Llama-3-8B-Instruct on a
  GSM8K problem puts disproportionate weight on separators such as "," and
  "." rather than on content words. The paper reads this as segment
  information being compressed into the separator, and builds on it.
- **The mask.** Each query sees a initial tokens (attention sinks, kept as in
  StreamingLLM), all preceding separator tokens, and the n nearest tokens; all
  others are masked, in every head. The separator set used everywhere is
  `. , ? ! ; :`, space, tab and newline. The mask is data-dependent, and a
  FlexAttention-based kernel (Sep-Attention) makes it trainable.
- **Training-free (Table 1, Llama-3-8B-Instruct).** GSM8K-CoT 8-shot: full
  attention 77.79, SepLLM (n=256) 77.18 with 47.36% of the KV, StreamingLLM
  (n=380) 70.89 at the same 47.5%. MMLU 5-shot: 65.72, 64.68 at 44.61% KV,
  and 63.39 for StreamingLLM at 52.5%. Against H2O, SnapKV and PyramidKV at
  47.54% KV on GSM8K-CoT (Table 15) it is ahead on both metrics (strict match
  77.18 against 75.06, 73.62 and 72.02), with no importance scoring.
- **Training from scratch (Pythia-160M, 300B Pile tokens, Tables 2–3).**
  SepLLM's mask cuts FLOPs to about 72% of full attention and per-iteration
  time from 2524 to 1648 ms. At equal FLOPs its loss is lower than the
  full-attention model's (Fig. 5b); at equal steps downstream scores are
  roughly on par (n=128: LAMBADA ppl 30.16 against 34.83, ARC-c 19.97
  against 20.14). Making the first layer, or the first and last, full
  attention helps further: LAMBADA ppl 40.08 → 36.54 → 33.41 at n=64. A
  StreamingLLM mask trained the same way is clearly worse (44.03).
- **Post-training.** A 1.4B Pythia checkpoint at step 93,000 converts to the
  SepLLM mask by continued training, faster with a larger n and a restarted
  learning-rate schedule. Loss curves only; no downstream table.
- **Streaming (PG19, Llama-3-8B).** At a fixed 324-entry cache, perplexity
  is lower than StreamingLLM's at every length from 1M to 4M tokens (e.g.
  34.5 against 36.1 at 4M with s=32). At c=800 generating 64K tokens: 33.4
  ppl in 1049.7 s, against 37.9 in 1096.0 s for StreamingLLM and 1090.8 ppl
  for full attention, which is out of its trained length.
- **What is ablated.** Initial tokens matter for both methods (Table 8).
  Position shifting within the cache, taken from StreamingLLM, matters more:
  without it StreamingLLM goes to about 400–560 perplexity and SepLLM to about
  175–265. FixLLM, which keeps one token at fixed intervals instead of
  separators, is significantly worse (Appendix I), which is the paper's
  evidence that it is the separators and not merely the sparsity. A naive
  mix of sliding-window and full heads at the same KV does poorly (Table 9).
  Larger separator caches and windows lower perplexity a little.
- **What is not shown.** The separator hypothesis is inferred from
  attention maps and from what masking costs; there is no probe of what a
  separator's representation contains. The from-scratch evidence is at 160M,
  and the post-training at 1.4B is shown as loss curves.

## Standing in the anthology

SepLLM extends StreamingLLM ([LIT-191](LIT-191.md)) by one cache. StreamingLLM keeps a
handful of initial tokens, because evicting the attention sink breaks the
model, plus a rolling window, with positions assigned within the cache.
SepLLM keeps all of that and adds the KV of every separator that has scrolled
out of the window. StreamingLLM is also the baseline in every experiment at a
matched cache budget, and the comparison is consistently in SepLLM's favour:
seven points on GSM8K-CoT at the same 47% of KV, lower perplexity at every
streaming length to 4M, and a needle-in-a-haystack test StreamingLLM fails
outright (Appendix F). The streaming ablation also reproduces [LIT-191](LIT-191.md)'s own
finding that the initial tokens cannot be dropped.

It bears on [THEORY-019](../theory.d/THEORY-019.md) in a way the record should register. That theory
explains the sink as a softmax with nothing to attend to dumping its mass on
the positions every query can see. [LIT-414](LIT-414.md) extends the same diagnosis to
content: heads learning a no-op land it on `[SEP]`, periods and commas. So the
attention on separators that SepLLM starts from has a reading in the record
already, and it is that the attention is a no-op, not a summary. SepLLM's
matched-budget comparisons do not decide between the two. Its seven GSM8K
points over StreamingLLM and its win over fixed-interval selection are what
the no-op reading predicts too: [LIT-414](LIT-414.md)'s heads park on punctuation
specifically, so the initial tokens cannot stand in for them, and evicting
the positions a head parks on disturbs its softmax whichever reading is
right. The account is filed as a Proposed theory, [THEORY-tmp7q4tl](../theory.d/THEORY-tmp7q4tl.md), which sets
out both readings; keeping the separators' keys while dropping their values,
or probing their states, would decide it.

For practice, it sits beside [SOTA-138](../practices.d/SOTA-138.md), which recommends sparse attention
learned with an indexer. SepLLM's sparsity is fixed by the tokenizer, not
learned, and needs no indexer. It also gains from keeping a full-attention
first and last layer, the hybrid instinct of [SOTA-132](../practices.d/SOTA-132.md) in a different form.
No practice in the record recommends separator-based KV retention, and this
single paper, with from-scratch evidence only at 160M, is not enough to
file one.

Unread — no NOTE.
