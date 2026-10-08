---
status: Active
title: 'Is Random Attention Sufficient for Sequence Modeling? Disentangling Trainable Components in the Transformer'
version: 1
tags:
- model-architecture
- attention-techniques
- analysis-and-evaluation
- model-stability
date: '2026-10-08'
published: '2025-06-01'
arxiv: '2506.01115'
first_author: 'Dong'
keywords:
- 'frozen-attention'
- 'random-transformer'
- 'induction-heads'
- 'mixit'
- 'rank-collapse'
- 'shaped-attention'
- 'memorization'
- 'ablation'
implementations:
- 'MixiT (princeton-pli)'
summary: >-
  Dong, Noci, Khodak and Li, Princeton and ETH Zurich (2025),
  [ARXIV-2506.01115](https://arxiv.org/abs/2506.01115). Freeze parts of a
  Llama-style transformer at initialization and see what still works. With
  query and key weights frozen at random, the model still forms induction
  heads (97.0% retrieval, 96.7% 5-layer 16-hop against 100% and 99.99%) and
  lands near the trained model on language modeling (log perplexity 3.07 against
  2.78 on Wikitext, 3.16 against 3.05 on Fineweb-edu). With attention replaced
  by a fixed, input-independent random mixing matrix (MixiT, shaped so signal
  propagation stays stable with depth), retrieval collapses to 11% and
  perplexity degrades to 3.73, yet decimal addition, Dyck-1, modular addition
  and Yelp sentiment are solved as well as by the trained model. Small models
  (at most 12 layers, hidden size 1024), grid-searched hyperparameters, no
  seeds or variance reported.
---

# LIT-tmpes9nd: Is Random Attention Sufficient for Sequence Modeling? Disentangling Trainable Components in the Transformer

Dong, Noci, Khodak and Li (2025) — [ARXIV-2506.01115](https://arxiv.org/abs/2506.01115). Read at v3 (3 September 2025),
main text and Appendices C and D; the proofs in the appendices were not checked.

## Key takeaways

- **Three ablations of a Llama-style decoder.** Frozen-QK keeps ordinary
  attention but freezes the query and key matrices at initialization, so only
  the value matrix learns. Frozen-MLP freezes the gated MLPs and leaves
  attention trainable. MixiT replaces attention with a fixed random mixing
  matrix that does not depend on the input: the identity plus a centred random
  matrix (so rows sum to one), scaled after Noci et al.'s shaped attention to
  keep signal propagation stable with depth (§2, Eq. 2.3).
- **Trainable query/key weights are not needed to form induction heads**
  (Table 1, Fig. 3). Frozen-QK gets 97.0% on needle-in-a-haystack retrieval
  (up to 30 key-value pairs) and 96.7% on 16-hop induction, against 100% and
  99.99% for the standard model. Frozen-MLP matches the standard model.
  MixiT gets 11.2% and 48.6%. Fig. 3 shows a two-layer Frozen-QK model
  implementing the previous-token head and the retrieval head. Retrieval
  accuracy falls off with the number of pairs faster for Frozen-QK than for the
  standard model (Fig. 2).
- **Language modeling is within reach of random attention, not of static
  attention** (Table 2, log perplexity): standard 2.78 / 3.05, Frozen-QK
  3.07 / 3.16, MixiT 3.73 / 4.08 on Wikitext-103 / Fineweb-edu. Appendix D adds
  that Frozen-QK trains 23.9% faster per sample than the standard model and
  MixiT 32.0% faster, with the quality gaps above.
- **Many algorithmic tasks do not need input-dependent attention** (Table 3).
  Decimal addition, Dyck-1, modular addition (p = 599), a pure-memorization
  task and Yelp polarity are solved by MixiT about as well as by the trained
  model (Yelp 92.56% against 90.55%). The authors propose MixiT's score on a
  task as a litmus test for whether the task needs in-context reasoning.
- **MLPs carry memorization, with help from attention** (Table 4, 2-layer
  models, bits per parameter): standard 2.98, Frozen-QK 2.25, MixiT 2.18,
  Frozen-MLP 1.13. Freezing the MLPs costs the most, but the gap from Frozen-QK
  to the trained model (2.25 to 2.98) exceeds what the parameter count explains.
- **An explanation for why random transformers fail with depth** (Tables 6
  and 7). Zhong and Andreas's random transformer drops from 100% to about 23%
  on decimal addition at 8 and 16 layers while MixiT stays at 100%, and the
  covariance between token representations rises with depth for the random
  transformer (0.0022 to 0.054 from 2 to 32 layers) and stays flat for MixiT.
  The authors read this as rank collapse and prove (Thm 2.1) that MixiT's
  covariance converges to an SDE in the infinite depth-and-width limit.
- **Theory for Frozen-QK** (Thm 5.1): one layer of multi-head attention plus
  MLP with random frozen query and key matrices approximates any continuous
  causal function with compact support. The same argument shows MixiT cannot,
  because its attention features are linear in the input.

## Standing in the anthology

An ablation study on small models, and read as that. It is the place in the
record where the question "which parts of the transformer have to be learned"
is answered with a controlled spectrum of models on tasks that separate
retrieval, memorization and bag-of-tokens judgements. Two results are likely to
be cited by other work: that frozen random query and key weights still form
induction heads, and that the memorization gap is mostly an MLP effect. The
MLP-and-attention collaboration reading agrees with the localization line that
[LIT-578](LIT-578.md) belongs to, and the paper says so, though it declines to
attribute facts to particular neurons.

No practice is drawn from it. The efficiency suggestion (drop the KV cache for
tasks that do not need in-context retrieval) is the authors' aside in the
related-work section and nothing in the paper tests it.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **Small models, tuned per task.** Language modeling uses 8 or 12 layers at
  hidden size 512 or 1024, trained for 40,000 steps at sequence length 256.
  Hyperparameters are grid-searched per architecture per task (Tables 8–9),
  and the retrieval and memorization comparisons deliberately fix width and
  depth to keep accuracy below saturation. Whether the Frozen-QK perplexity gap
  (0.11 to 0.29 log units) shrinks, holds or grows at scale is not tested.
- **One number per cell, no variance.** No table reports seeds, standard
  deviations or confidence intervals. The memorization split, for example,
  separates models by a few points of accuracy and the language-modeling
  margins by 0.1 to 0.3, which a reseed could plausibly move.
- **Text and tables disagree in two places.** The memorization paragraph
  assigns 1.13 bits per parameter to Frozen-QK and 2.25 to Frozen-MLP, while
  Table 4 and its caption say the reverse (and the trainable-parameter counts
  fit the table). The Fineweb-edu perplexity for Frozen-QK is 3.16 in Table 2 and
  3.15 in Appendix D. Neither changes a conclusion; both are reasons to quote
  the tables and not the prose.
- **"Attention mixing is all you need" is about these tasks.** The tasks where
  MixiT matches the trained model are ones where, by the authors' own
  litmus test, no in-context retrieval is needed, so the claim is partly
  circular. The head-count result (Table 5) is also mixed: decimal addition
  rises from 35% to 92% with 256 heads, while Yelp does not move.
- **Related-work claims are the authors' reading.** The note on Synthesizer,
  FNet and data-free static attention is positioning, not a reproduced
  comparison.
