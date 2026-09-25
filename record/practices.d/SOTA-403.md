---
number: 403
status: Proposed
formerly:
- SOTA-tmpgqcuy
consensus: unreplicated
consensus_note: >-
  One group, one result, and the group that proposed the technique. Nobody has
  run the ablation again, and nothing *shipped* at current scale shares layers
  at all, which is not a refutation. One research model does: LIT-683
  (3.5B) iterates a fully shared core block, feed-forward included, but it
  spends the saving on more depth and never splits attention from
  feed-forward, so it does not bear on this recommendation. The field went to spending parameters rather than
  saving them, so the question this ablation answers stopped being asked;
  `DP-005` says adoption is not evidence, and non-adoption is not evidence
  either. Read as of 2026-09.
promote_when: >-
  The attention-only/FFN-only split is run again on a decoder-only language
  model at a scale anyone currently trains, with the parameter saving spent
  somewhere — width, depth or data — so the comparison is at equal cost rather
  than equal shape. Re-running it on an encoder at BERT scale would confirm the
  2019 measurement without answering whether the asymmetry survives the
  architecture the field actually uses.
title: 'Share the attention parameters across layers if you need to cut parameters; do not share the feed-forward ones'
version: 3
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Consensus note corrected. "Nothing at current scale shares layers at all"
    was false once LIT-683 (Huginn, 3.5B, a fully shared core iterated
    up to 32 times) was filed. It is a research model, not a shipped one, and
    it tests a different question. The recommendation, status and consensus
    are unchanged.
- version: 3
  date: '2026-09-25'
  note: >-
    Records an outside test of cross-layer sharing and of the Universal
    Transformer. Narang et al. (LIT-tmpnc3oh) found all-shared,
    encoder-only and decoder-only sharing worse than no sharing. The
    Universal Transformer did not match a vanilla baseline even after 25
    tuning runs. Neither tests the attention/FFN split. The paragraph that
    cited the Universal Transformer's gain as pointing the other way now says
    the gain did not reproduce. Also notes that LIT-tmpbukux gives the
    mechanism paragraph deletion evidence. Recommendation, status and
    consensus are unchanged.
tags:
- model-architecture
- training-optimization
date: '2026-09-25'
source:
- LIT-668
# Same code as `source:`, and the interesting part is who it is NOT. Cross-layer
# sharing itself is Dehghani et al. 2018 (Universal Transformer), which this
# record does not yet hold — but Universal Transformer shares everything and
# reports a gain. The recommendation here is the SPLIT, which is Lan et al.'s
# ablation and nobody else's (ADR-030).
introduced_by:
- LIT-668
# Deliberately empty. ALBERT ships ALL-shared, which is the configuration this
# practice advises against — so listing it here would claim an adopter this
# recommendation does not have.
implementations: []
summary: >-
  Lan et al. (2019), [LIT-668](../literature.d/LIT-668.md). A transformer block has two halves and they
  are not equally compressible across depth. On an ALBERT-base configuration at
  `E = 128`, sharing every layer's attention parameters scores **81.7 average
  against 81.6 for no sharing** while removing 89M parameters to 64M; sharing
  the feed-forward parameters instead scores **80.2**. At `E = 768` the same
  split reads −0.7 against −2.8. One paper, 2019, encoder-only, and nobody has
  re-run it.
---

# SOTA-403: Share the attention parameters across layers if you need to cut parameters; do not share the feed-forward ones

<!-- inactive-ok-file: THEORY-103 — Proposed, and cited to say that its premise would supply a
     mechanism for this asymmetry and that no document claims it yet. Open is exactly what is being
     asserted about it. -->

## Source

Lan, Chen, Goodman, Gimpel, Sharma and Soricut (2019), [LIT-668](../literature.d/LIT-668.md) —
[ARXIV-1909.11942](https://arxiv.org/abs/1909.11942).

## What to do

If a parameter budget is the binding constraint, tie the `Q`, `K`, `V` and
output projections across every layer of the stack and leave each layer its own
feed-forward weights. The measurement, averaged over SQuAD 1.1/2.0, MNLI, SST-2
and RACE on an ALBERT-base configuration:

| | params | Avg | | params | Avg |
| --- | --- | --- | --- | --- | --- |
| **`E = 128`** | | | **`E = 768`** | | |
| not shared | 89M | 81.6 | not shared | 108M | 82.3 |
| attention shared | 64M | **81.7** | attention shared | 83M | 81.6 |
| FFN shared | 38M | 80.2 | FFN shared | 57M | 79.5 |
| all shared | 12M | 80.1 | all shared | 31M | 79.8 |

Sharing attention costs +0.1 and −0.7; sharing the FFN costs −1.4 and −2.8. If
you need more than the quarter of parameters that attention-sharing buys, the
next increment is grouped sharing rather than all-sharing — divide `L` layers
into groups of `M` and share within each, where the paper reports smaller `M` is
strictly better.

## Conditions, and what is not established

**The scale and the architecture are 2019 and encoder-only.** ALBERT-base is a
12-layer bidirectional encoder trained on Wikipedia and BookCorpus, evaluated by
fine-tuning on GLUE-era tasks. Nothing here says the split holds for a
decoder-only model at a scale anyone currently trains, and the `promote_when`
asks for exactly that rather than for a confirmation at the old one.

**Equal shape, not equal cost.** The table compares configurations with the same
width and depth and different parameter counts. It does not spend the saving,
which is what you would actually do — and when Lan et al. do spend it, on width,
the resulting ALBERT-xxlarge has fewer parameters than BERT-large and **3.17×
lower throughput**. A parameter saving from sharing is not a compute saving, and
this recommendation is about parameters.

**The asymmetry has no mechanism here, only a number.** An obvious candidate
sits in this record: if a layer's feed-forward block is where facts are stored,
sharing it removes per-layer storage, and [THEORY-103](../theory.d/THEORY-103.md) argues from
exactly that premise in the other direction — that the *absence* of a per-layer
store is what breaks out-of-distribution composition, and that sharing the two
halves of the stack **fixes** it. Same intervention, and the two papers price it
oppositely because they measure different things. That is a coincidence of
premise, not an explanation, and no document in this record claims the
mechanism yet.

**Cross-layer sharing per se is not this practice, and it points the other
way.** Dehghani et al. (2018) share everything and report a *gain* over a
standard transformer on language modelling and subject-verb agreement; Lan et al.
name the disagreement in their related work. The recommendation here survives it
because the two are compatible — the question of whether sharing helps overall
is open, and which half to share if you do is what got measured.

**The Universal Transformer's gain did not reproduce, and neither did sharing in
general.** Narang et al. ([LIT-tmpnc3oh](../literature.d/LIT-tmpnc3oh.md)) reimplemented both in a 223M T5
encoder-decoder with hyperparameters fixed. The Universal Transformer reached
early pre-training loss 2.40 against the vanilla 2.182, at about 4× the
FLOPs. A 25-configuration sweep brought it to 2.265 and "we were ultimately
unable to match the performance of the vanilla Transformer". ALBERT-style
all-block sharing scored 2.497, encoder-only sharing 2.298 and decoder-only
sharing 2.352, all worse. That weakens the counter-signal above, and it adds a
second measurement that sharing costs quality. It still does not test the
split. No configuration there shares attention alone, so the asymmetry
remains one group's result.

**On the mechanism, one causal data point.** [LIT-tmpbukux](../literature.d/LIT-tmpbukux.md) deletes the
feed-forward layers from a small decoder and moves the parameters into
attention depth. What is lost is almost entirely prediction on tokens the
context cannot help with, which the authors call parametric recall. That fits
the storage premise above. It deletes the FFN rather than sharing it, so it
does not measure what sharing the FFN costs.

## Known implementations

- **None.** ALBERT itself ships all-shared rather than attention-shared, which
  is worth noticing rather than glossing: the authors chose the configuration
  their own ablation scores **1.6 lower** at `E = 128` and 1.8 lower at
  `E = 768`, because the parameter saving was the point of the paper and the
  accuracy was the price they were willing to pay. This recommendation is
  therefore one nobody has shipped — including the group that measured it.
