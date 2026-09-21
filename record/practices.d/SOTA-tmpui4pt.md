---
status: Proposed
promote_when: >-
  A second group measuring hidden-state predictability against an
  **external** complexity ground truth — an analytic description length, a
  known program size, a task whose difficulty is fixed independently of
  anyone's judgement — with next-token loss controlled for, on a model family
  that is not Llama. The external ground truth is the part to insist on:
  the LLM half of this paper shows the metric agreeing with the authors'
  taxonomy of which texts are interesting, which is suggestive and circular,
  and the automaton half is what stops it being only that. What would not
  move it: another information-bottleneck probe reporting that its quantity
  correlates with something, without the next-token-loss control.
consensus: unreplicated
consensus_note: >-
  One group, one paper. The ingredients are old — variational bottlenecks,
  self-predictive representations, the observation that next-token loss is
  not complexity — and the assembly is new, so adoption of any of the parts
  would not be evidence for this. Nothing else in the record measures what a
  model is computing as distinct from how well it predicts.
title: 'To tell whether a model is doing non-trivial in-context computation, measure how well it predicts its own hidden states, not its next-token loss'
version: 1
tags:
- analysis-and-evaluation
- in-context-learning
date: '2026-09-21'
source:
- LIT-tmpwr4bz
introduced_by:
- LIT-tmpwr4bz
implementations: []
summary: >-
  Herrmann et al. (2025), [LIT-tmpwr4bz](../literature.d/LIT-tmpwr4bz.md) — uniform noise maximizes
  next-token loss and requires no computation; reciting a memorized licence
  minimizes it and requires none either. Insert a variational bottleneck with
  a **learned autoregressive prior** and measure the posterior-prior KL: only
  the genuinely in-context task scores high, on a Transformer and an LSTM,
  and the signal survives controlling for next-token loss.
---

# SOTA-tmpui4pt: To tell whether a model is doing non-trivial in-context computation, measure how well it predicts its own hidden states, not its next-token loss

## Source

Herrmann, Csordás and Schmidhuber (2025), [LIT-tmpwr4bz](../literature.d/LIT-tmpwr4bz.md) —
[ARXIV-2503.13431](https://arxiv.org/abs/2503.13431) — read as [NOTE-tmpsw3lp](../notes.d/NOTE-tmpsw3lp.md).

## The problem with the obvious metric

Next-token loss conflates *difficulty* with *computation*, and it does so at
both ends:

- **Uniform random tokens** give the highest possible loss and require the
  model to do nothing, because nothing it computes can help.
- **A memorized licence** gives near-zero loss and also requires nothing, the
  program having been written into the weights already.

So both extremes are uninteresting, the interesting cases land in the middle,
and an intermediate loss is indistinguishable from a mixture of trivial and
impossible tokens. Reaching for perplexity to answer "is the model doing
something here" returns an answer to a different question.

## What to do instead

Split the model between two sequence layers and insert a **PHi layer**:

1. A posterior encoder mapping the hidden state to a latent.
2. A decoder reconstructing the hidden state from that latent.
3. **A learned autoregressive prior** predicting the latent from its own
   past. This is the part that distinguishes it from an ordinary variational
   bottleneck, and it is what makes the quantity mean something.

The metric is `KL(posterior ‖ prior)` per step — the nats of hidden-state
information the past did not predict, which is the incremental description
length of the in-context program. Average it over a sequence to score the
sequence.

Train it jointly with the ordinary next-token loss so the bottleneck stays
under pressure to keep what the upper layers need, **or** freeze a pretrained
model and train only the PHi layer.

**Put it in the upper layers.** Inserting the bottleneck early causes
posterior collapse — next-token loss degrades badly and the metric goes to
nearly zero, which reads as "no computation" and means "instrument broken".
In a 3B Llama the usable band was layers **18–24**. Sweep and check
next-token loss is undisturbed before trusting any number.

## What it buys

- **The separation next-token loss cannot make.** Across memorized
  subsequences, memorized automata, fresh in-context automaton learning and
  uniform noise: only the in-context task scores high, on a 12-layer
  Transformer *and* a 2-layer LSTM.
- **Complexity tracking with the confound controlled.** Binning tokens by
  next-token loss and stratifying by the *analytically computed* description
  length of the generating automaton, higher complexity gives higher PHi loss
  in every bin. This is the result the practice rests on, because the
  complexity axis is external rather than judged.
- **It transplants.** A single layer trained into a frozen Llama-3.2-3B
  reproduces the separation, while next-token loss shows no consistent
  pattern across the same texts.
- **Maths difficulty** correlates with PHi loss on step-by-step solutions,
  partial correlation significant at every layer tested.

## Conditions

**This measures, it does not select.** The paper's most quotable downstream
result — higher-PHi-loss rationales are likelier to be correct — is reported
without the comparison that would make it actionable. Choosing by **lower
next-token loss alone already scores 71%** on the same GSM-8K pairs, the
paper says so, and no number is given for PHi as a standalone selector. What
is shown is incremental value under partial correlation, plus performance on
an adversarial subset where the next-token baseline is wrong by
construction. Use this to ask what a model is doing; do not reach for it as a
verifier on this evidence.

**You have to modify the model.** A bottleneck is inserted and trained. In
the joint-training setting the model is also *shaped* by the metric, so it is
not an observational probe of a network you already have.

**Half the evidence rests on the authors' taxonomy.** Which of trivial
tasks, licences, shuffled tokens, unseen literature and unseen code count as
"interesting" is their judgement, and the metric agreeing with it is
suggestive rather than probative. The automaton experiments, where
complexity is a formula, are what keep the claim from being circular — and
they are the smaller-scale half.

**One model family for the LLM results**, and the usable layer band is
reported for that model only, discovered by sweeping.

**Cost is unreported.** 10,000 training steps for the layer, no wall-clock
and no comparison, which matters if you were considering this as standing
instrumentation rather than a one-off study.
