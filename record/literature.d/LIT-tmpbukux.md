---
status: Active
title: 'A Controlled Study of Attention-Only Transformers'
version: 1
tags:
- model-architecture
- analysis-and-evaluation
- attention-techniques
- model-stability
- training-optimization
date: '2026-09-25'
published: '2026-07-20'
arxiv: '2607.18363'
first_author: 'Ndubuaku'
keywords:
- 'attention-only'
- 'feed-forward-ablation'
- 'parametric-memory'
- 'qk-normalization'
- 'residual-gating'
- 'weight-spectra'
- 'muon'
implementations: []
summary: >-
  Ndubuaku et al. (2026), [ARXIV-2607.18363](https://arxiv.org/abs/2607.18363). Removing every feed-forward layer from a
  decoder costs 0.47 nats at matched depth and 0.26 at matched training FLOPs,
  but only **0.0055 nats (0.27% of loss) at matched parameters** once the freed
  budget goes into attention depth: 20 attention-only layers against 4
  standard blocks, 24M parameters, 105B tokens of a synthetic reasoning
  corpus, with a separate learning-rate sweep for each arm. The remaining gap sits on
  low-context tokens, where the answer must come from the weights. A
  pre-registered test on fineweb-edu predicted 0.02–0.05 nats and measured
  0.040. Removing QK-norm made the attention-only stack diverge; residual
  gates and ReZero changed nothing. Everything is at or below 87M parameters.
compared_against:
- LIT-047
- LIT-640
---

<!-- inactive-ok-file: SOTA-403 — Proposed; named as a practice this paper bears on without settling, and its status is not relied on -->

# LIT-tmpbukux: A Controlled Study of Attention-Only Transformers

Ndubuaku, Mosoyan, Mroz, Cylich, Kumar, Sandhu, Shemet and Lee (2026) —
[ARXIV-2607.18363](https://arxiv.org/abs/2607.18363)

## Key takeaways

**Three matchings, because no single one is fair.** Deleting the FFN changes
parameters, FLOPs and depth at once, so the attention-only model (a "SAN", 20
layers at `d = 512`, 24.13M parameters) is compared against three standard
transformers, each matched on one axis:

| control | config | params | Δ val loss vs SAN @105B |
| --- | --- | --- | --- |
| iso-depth | 20L, SwiGLU `d_ff = 4d` | 87.06M | FFN ahead by **0.470** |
| iso-FLOP | 9L | 43M | FFN ahead by **0.263** |
| iso-param | 4L | 24.12M | FFN ahead by **+0.0055, +0.0054** on two clean seed pairs |

The third seed pair reverses sign, and it is excluded as a documented
terminal-phase instability in the FFN run. The same-seed noise floor,
calibrated with an optimizer-equivalent normalization pair, is 0.0015 nats.
Every arm and optimizer cell had its own learning-rate sweep (17 cells), and
the locked rates are interior minima. The optimal Muon rate differs by 2×
between the arms.

**It closes with tokens and stays flat with size.** At matched parameters the
gap is 0.046 at 5B tokens, 0.019 at 30B and 0.0055 at 105B, each separately
trained. Across five size pairs at 31.5B tokens it sits near 0.02 nats from 16M
to 57M non-embedding parameters. Token convergence was measured at one size
only, and size-flatness at one budget only.

**Where the gap is: parametric recall.** The deficit is on query tokens, where
the context gives little to route from. At 31B tokens their per-token deficit
is five times the aggregate. By 105B the SAN leads on every answer region of
the decomposition sample, and that sample was seen in training. On benchmarks,
lambada favours the FFN arm and sciq (answer in a supplied passage) favours
the SAN, by a growing margin. The rest are at chance. The pre-registered
fineweb-edu prediction of 0.02–0.05 nats measured 0.0398.

**Components (Table 6, 20-layer SAN, one run each).** With QK-norm removed,
the model **diverges** at the tuned rate, and it is the only divergence in
the study. The claim is scoped to that rate. Sandwich norm gains −0.0092, and
it is the only variant that beats the baseline. A standard residual scores
−0.0013 and a ReZero residual +0.0032 against the gated baseline, both inside
a few noise floors, so the gates are neutral at 8–48 layers and in the FFN
arm too. With no residual at all, loss rises by +0.75. At matched parameters,
depth is U-shaped with the optimum at 20 layers, and 48 layers train without
incident.

**Mechanism (weight spectra).** Q/K stable rank stops moving within the
first quarter of training. The matrices that write content into the residual
stream keep accumulating rank through the stable phase: the FFN
down-projection in a standard model, and `W_o` once the FFN is gone.

## Standing in the anthology

Filed as `#290`'s promotion [#14](https://github.com/dmarx/anthology-of-the-sota/issues/14): "a controlled study, the evidence form [DP-009](../../docs/design-principles.md#dp-9)
asks for". It is controlled in the ways that usually go missing. There are
three matchings rather than one, a separate learning-rate sweep per arm, a
calibrated noise floor, and a numerical prediction registered before its run,
and the authors report that two of their eight registered predictions failed.

What it is **not** is a recommendation to drop the feed-forward layer. The
authors say "we claim regime, not superiority". At matched parameters the SAN
costs about 2× the FLOPs per token at 2048 context, and every result is at 87M
parameters or below on one synthetic corpus plus one web-text pair. Its
bearing on the record is narrower:

- **[SOTA-192](../practices.d/SOTA-192.md)** gains a data point from outside the language-model line it was
  filed from. QK-norm is what keeps a 20-layer attention-only stack from
  diverging, in one ablation run at one learning rate.
- **[SOTA-051](../practices.d/SOTA-051.md)**. The ReZero residual is neutral here, alongside the Narang
  et al. result ([LIT-tmpnc3oh](LIT-tmpnc3oh.md)) that ReZero *replacing* normalization is worse.
  The two do not conflict, because here normalization is kept.
- **[SOTA-403](../practices.d/SOTA-403.md)**'s unexplained asymmetry. This paper is causal evidence, by
  deletion, that FFN capacity tends toward parametric recall. It deletes and
  does not share, so it does not test that practice's split.
