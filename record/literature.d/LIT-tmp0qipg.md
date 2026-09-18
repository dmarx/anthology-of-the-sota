---
status: Active
title: 'Softpick: No Attention Sink, No Massive Activations with Rectified Softmax'
version: 1
tags:
- attention-techniques
date: '2026-09-18'
published: '2025-04-01'
arxiv: '2504.20966'
first_author: 'Zuhri'
keywords:
- 'attention-sink'
- 'massive-activations'
- 'softmax-alternatives'
- 'quantization'
- 'attention-sparsity'
implementations:
- 'https://github.com/zaydzuhri/softpick-attention'
summary: >-
  Zuhri et al. (2025), [ARXIV-2504.20966](https://arxiv.org/abs/2504.20966). Drops the sum-to-one constraint
  outright — `ReLU(e^x − 1)` over a sum of absolute values — and gets a **0.00%
  sink rate** at both 340M and 1.8B, kurtosis from 33511 to 341, and attention
  matrices that are 95-99% exact zeros. **That is the mechanism confirmed and
  the remedy failing**: at 340M it matches softmax, at 1.8B it is worse across
  every benchmark, and the paper's own contribution list includes
  investigating why. The most useful negative result the record holds on
  attention sinks.
---

# LIT-tmp0qipg: Softpick: No Attention Sink, No Massive Activations with Rectified Softmax

Zuhri et al. (2025) — [ARXIV-2504.20966](https://arxiv.org/abs/2504.20966)

## Key takeaways

- **The change, and it is the most direct test of the account available.**

      Softpick(x)ᵢ = ReLU(e^{xᵢ} − 1) / Σⱼ |e^{xⱼ} − 1|

  Rectified, and explicitly **not sum-to-one**. A head can now output all
  zeros. No extra parameters, no custom optimizer, and a FlashAttention-2
  compatible online form is given.

- **The design detail that earns its place.** A first attempt used a positive
  denominator and heads **died** — negative inputs receive no gradient because
  they contribute to neither numerator nor denominator, and the heads never
  recovered from outputting zeros. Taking the *absolute value* in the
  denominator lets negative scores contribute to the sum without changing the
  derivative's magnitude. The paper reports that the naive version also failed
  to remove sinks.

- **The phenomenon is removed, completely.** Sink rate **0.00%** at both
  scales, against 63.41% and 14.96% for softmax at `ε_s = 0.3`. Hidden-state
  kurtosis at 340M: **33510.81 → 340.96**; at 1.8B: **74456.81 → 2193.27**.
  Activation extremes shrink correspondingly. Attention matrices become
  **99.34% and 95.63% exact zeros**, against softmax's ~4.5% which arise only
  from numerical underflow.

- **And the model gets worse at the larger scale.** At 340M softpick matches
  or slightly beats softmax and the final training loss differs by 0.004. At
  1.8B the training-loss gap is **0.12**, and every downstream number moves
  the wrong way: ARC-Easy −5.17, LAMBADA −5.92 accuracy and +4.43 perplexity,
  PIQA −2.72, SciQ −6.00, WikiText +2.77 perplexity. Trained on 52B and 104B
  tokens respectively.

- **Quantization is where it wins, and the win narrows.** At 340M, quantized
  softpick models beat softmax consistently across HQQ, bitsandbytes and GPTQ,
  with the advantage growing as precision drops. At 1.8B the base-model gap
  dominates, though it closes at lower precision.

- **Two hypotheses for the scaling failure, both the authors' own.**
  *Underscoring*: as context grows and attention gets sparser, softpick's
  normalization shrinks the scores on the few relevant tokens, weakening the
  value signal — visible in retrieval heads. *Dead heads*: heads that stay
  dormant for long stretches of training, reducing effective capacity. A
  score-scaling fix borrowed from Scalable-Softmax made things worse.

- **Long-context retrieval did not improve** despite sharper, sparser
  attention maps. Passkey retrieval collapses at 4986 tokens for every method,
  which is out of the 4096 training range.

## Standing in the anthology

**Filed as the negative result, and that is its value.** The record holds four
answers to the softmax-mass pressure — the gate
([SOTA-134](../practices.d/SOTA-134.md)), clipped softmax, `softmax₁`, and
now this. This is the one that removes the constraint most completely and it
is also the one that demonstrably fails to scale under its authors' recipe.

For [THEORY-tmp1rmwn](../theory.d/THEORY-tmp1rmwn.md) it cuts both ways and
both are worth having. **It confirms the mechanism about as hard as it can be
confirmed**: remove the sum-to-one constraint and the sink goes to exactly
zero, at two scales, with the massive activations going with it. And it
separates that from the engineering question, because the model that has no
sinks is also the worse model at 1.8B. Sinks are not merely tolerable, as
[LIT-191](LIT-191.md) already showed by evicting them; a model built so the
pressure never arises pays somewhere else.

The authors are explicit that the failure is under **their recipe with
softmax's hyperparameters**, which is the obvious confound and is named in
their limitations rather than buried.
