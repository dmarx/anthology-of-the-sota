---
status: Active
title: 'Does Localization Inform Editing? Surprising Differences in Causality-Based Localization vs. Knowledge Editing in Language Models'
version: 1
tags:
- analysis-and-evaluation
- adaptation-and-tuning
date: '2026-09-23'
published: '2023-01-01'
arxiv: '2301.04213'
first_author: 'Hase'
keywords:
- 'causal-tracing'
- 'localization'
- 'knowledge-editing'
- 'rome'
- 'negative-result'
implementations: []
corrects:
- LIT-tmpvij69
summary: >-
  Hase, Bansal, Kim, Ghandeharioun (NeurIPS 2023), [ARXIV-2301.04213](https://arxiv.org/abs/2301.04213). On 652
  facts known to GPT-J, causal tracing often peaks outside the layers ROME
  and MEMIT edit. Yet editing at those layers works regardless. In a
  regression of ROME's rewrite score, the edit layer explains 94.7% of the
  variance, and adding the fact's tracing effect raises it to 94.8%.
  Robust across editing methods (ROME, MEMIT, fine-tuning), metrics, models
  and datasets. Localization, as causal tracing measures it, does not tell
  you where to edit.
---

# LIT-tmp6e8di: Does Localization Inform Editing? Surprising Differences in Causality-Based Localization vs. Knowledge Editing in Language Models

Hase, Bansal, Kim, Ghandeharioun, Google Research and UNC (NeurIPS 2023)
— [ARXIV-2301.04213](https://arxiv.org/abs/2301.04213)

## Key takeaways

- **Where tracing puts facts** (Figure 1): for 652 facts GPT-J knows, the
  tracing peak is spread across layers, many at 1–3 and 16–20, outside
  ROME's layer 6 and MEMIT's 4–9 (the figure counts from 1; MEMIT's paper
  gives 3–8 counting from 0)
- **Where editing works:** ROME reaches 99% rewrite score at layer 6 and
  above 96% at every layer except the last
- **The regression** (Table 1): per-fact tracing effect against per-fact
  edit success, correlation ρ = −0.13. With the edit layer as a predictor,
  R² = 94.7%. Adding the tracing effect gives 94.8%, so tracing explains
  0.1%
- **Rescue attempts** (§5): four variants of the editing problem, one of
  them (Fact Forcing) built to match tracing's own setup. Tracing relates
  to success only there, and even there the layer choice dominates
- **Robustness:** the same holds for MEMIT, constrained fine-tuning,
  paraphrase and neighborhood metrics, GPT-2 XL and zsRE

## Standing in the anthology

**Filed from `#163`** (LARQL). It `corrects` ROME ([LIT-tmpvij69](LIT-tmpvij69.md)), and it is
why the localization-to-editing account is filed `Rejected`
([THEORY-tmpde7eo](../theory.d/THEORY-tmpde7eo.md)).

**What it does not say.** It does not show that causal tracing is wrong
about where information is, or that editing mid-layer MLPs fails. It shows
that the two are unrelated. The authors conclude that "better mechanistic
understanding ... may not always translate to insights about how to best
change their behavior".

Read — [NOTE-tmpceyj8](../notes.d/NOTE-tmpceyj8.md).
<!-- inactive-ok-file: THEORY-tmpde7eo — Rejected on this paper's evidence, filed in this same contribution -->
