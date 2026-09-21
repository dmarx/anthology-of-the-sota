---
status: Read
paper: LIT-tmpwr4bz
title: 'PHi: prediction of hidden states'
version: 1
date: '2026-09-21'
summary: >-
  Read for the instrument. The diagnosis of next-token loss is clean and the
  boring/interesting separation is convincing on two architectures. The
  reasoning-selection result is weaker than the abstract implies, and the
  paper says so itself in a sentence most readers will pass over: picking by
  next-token loss alone already scores 71%.
---

<!-- inactive-ok-file: SOTA-101 — cited to mark a boundary rather than to
     lean on it: perplexity filtering ranks documents by typicality, which is
     a different job for the same number, and this paper's claim is bounded
     away from it. A citation that says "this does not disturb that" does not
     depend on that document's standing -->

# NOTE-tmpsw3lp: PHi: prediction of hidden states

## Contribution

A named failure of the field's default metric, and a replacement that does
not share it.

Next-token loss conflates two different things: how hard a sequence is to
predict, and how much computation predicting it requires. Uniform noise
maximizes the loss and requires nothing. Reciting a memorized licence
minimizes it and requires nothing. The interesting cases — inferring an
unfamiliar automaton, modelling unseen code — sit in the middle, where an
intermediate loss is indistinguishable from a mixture of easy and impossible
tokens.

What is true afterwards: there is a measurable quantity that separates them,
it is architecture-agnostic, it can be attached to a frozen pretrained model,
and it retains predictive power *after* next-token loss is controlled for.

## Key insight

**Ask what the model's own hidden states tell it that it did not already
know.**

The PHi layer is a variational bottleneck with one unusual feature: instead
of the standard fixed prior, the prior is a **learned autoregressive
predictor** over the latents' own history. The KL between posterior and prior
is then the nats of hidden-state information at this step that the past did
not predict — which is exactly the incremental description length of the
"in-context program" the model is building.

That framing is what makes the metric mean something rather than merely
correlate. A memorized routine has already been written down in the weights,
so it costs nothing to describe as the sequence proceeds. Noise supports no
program at all. Inferring a fresh automaton requires assembling a
description, and its cost is what the KL measures.

## Assumptions

- The model must have **at least two sequence layers** so the bottleneck can
  sit between them.
- Joint training combines the PHi loss with the ordinary next-token loss, so
  the bottleneck is under pressure to keep whatever the top layers need.
- For the LLM experiments the base weights are **frozen** and only the PHi
  layer trains — 10,000 steps on a reasoning-and-language mixture.
- Task "interestingness" is assigned **by the authors' judgement**, not
  measured independently, in the five-way LLM comparison. The automaton
  experiments are the ones with an external ground truth.
- The formal-language complexity is an analytic code length over the
  automaton, which is what makes §3.1.2 a genuine correlation rather than a
  vibe.

## Key results

- **Four-task separation:** only in-context learning of a fresh automaton
  gives high PHi loss; memorized subsequences, memorized automata and uniform
  noise are all low. Holds for a 12-layer Transformer *and* a 2-layer LSTM.
  Next-token loss instead orders them memorized < in-context < random.
- **Complexity beyond next-token loss:** binning by next-token loss and
  stratifying by automaton description length, higher complexity gives higher
  PHi loss within every bin; partial correlation significant.
- **Transplant into frozen Llama-3.2-3B** reproduces the separation — unseen
  literature and a private codebase high, trivial/licence/shuffled low —
  while next-token loss shows no consistent pattern over the same five.
- **Maths difficulty:** partial correlation between PHi loss on a step-by-step
  solution and MATH difficulty level is significant at every layer tested.
- **Posterior collapse is located:** early-layer insertion degrades
  next-token loss badly *and* drives PHi loss to near zero. Layers 18–24 are
  where the metric discriminates without disturbing the model.
- **Rationale selection:** on GSM-8K pairs, picking the higher-PHi-loss
  rationale beats chance, including on the adversarial subset where the
  lower-next-token-loss answer is wrong.

## Claims

**Well supported, and the reason to file this:** that next-token loss does
not measure computation, and that PHi loss separates the cases it conflates.
Two architectures, an analytic complexity ground truth, a frozen-LLM
replication, and partial correlations throughout rather than raw ones.

**Well supported and the most useful practical detail:** the posterior
collapse finding. It is a concrete placement rule with a measured basis, and
it is the thing that would otherwise waste a reader's first attempt.

**Weaker than the abstract implies, and the paper says so.** "Solutions with
high PHi loss have a significantly increased chance of being correct" is
true and is not the comparison that matters. Buried in §3.2.3: *choosing by
lower mean next-token loss alone already yields 71%*. The paper never claims
PHi loss beats that as a standalone selector, and reports no such number.
What is demonstrated is **incremental** value — partial correlation with
next-token loss controlled, plus the adversarially-constructed
counterintuitive subset where the next-token baseline is wrong by
construction. A reader who takes the abstract's sentence as "use PHi to pick
answers" has been handed the wrong instruction by a true sentence.

**Judgement, not measurement:** which of the five LLM text types count as
"interesting". The result is that the metric agrees with the authors'
intuition; the automaton experiments are what keep this from being circular.

**Tentative and labelled as such:** the easy/hard asymmetry on
counterintuitive questions, with a proposed story about oversimplified
rationales. One dataset split, no test.

## Method

Insert a variational bottleneck with a learned autoregressive prior mid-model;
define interestingness as the posterior-prior KL per step. Train from scratch
on a four-task mixture with Transformer and LSTM; correlate against analytic
automaton description length with next-token loss controlled; repeat with a
single layer trained into a frozen Llama-3.2-3B; sweep insertion depth; apply
to MATH difficulty and GSM-8K self-generated rationale pairs.

## Connections

- [SOTA-200](../practices.d/SOTA-200.md) — check whether an emergent capability is a metric
  artefact — is the same genre of finding: the field's default measurement
  answering a different question than the one being asked. That one is
  destructive, this one ships a replacement.
- [SOTA-270](../practices.d/SOTA-270.md) — do not read a smooth loss curve as evidence of smooth
  training — is the closest neighbour, and the complement: it says decompose
  the aggregate over *training*, this says the per-token quantity is the
  wrong quantity to begin with.
- [SOTA-101](../practices.d/SOTA-101.md) uses perplexity to filter training data. Not in tension:
  that ranks documents by typicality, which is a different job for the same
  number, and nothing here argues against it.
- [SOTA-280](../practices.d/SOTA-280.md) samples several reasoning paths and takes the majority.
  The GSM-8K experiment is a selection rule over sampled rationales and so is
  adjacent — but the practice this record files from it is the *measurement*,
  not the selector, precisely because the selector is not shown to beat its
  baseline.

## Bearing on the record

One practice: the measurement and its placement rule. The reasoning-selection
application is deliberately **not** filed as a practice, because the paper
does not establish it against the obvious baseline and the record should not
be the place where that gap closes silently.

## Limitations

**The metric requires modifying the model.** A bottleneck is inserted and
trained, so this is not an observational probe of an unmodified network —
and in the joint-training setting the model is shaped by the metric it is
being measured with.

**"Interesting" is defined by this construction.** The paper is careful
enough to give an external ground truth in the automaton setting, but the
LLM text taxonomy is the authors' own, and the headline figure rests on it.

**One LLM, 3B, one family.** Whether the discriminating band generalizes
beyond layers 18–24 of Llama-3.2-3B is untested, and the sweep is the only
guidance offered.

**Cost is unreported.** Training a PHi layer for 10,000 steps is cheap
relative to pretraining and the paper gives no wall-clock or comparison,
which matters for anyone considering this as routine instrumentation.

## Open questions

- Does PHi-based selection beat next-token-loss selection outright, on a
  full set rather than the counterintuitive subset? The paper supplies the
  71% baseline and not the comparison.
- Is there a placement rule better than "sweep and look"? The collapse
  boundary is presumably a function of where the residual stream's
  information becomes redundant, which would be predictable rather than
  discovered.
- Does the metric survive the model being *trained* against it at scale —
  that is, is it robust to becoming a target?
