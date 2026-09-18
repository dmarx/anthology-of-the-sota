---
number: 21
status: Active
formerly:
- THEORY-tmpkh59b
title: "A model builds a latent vocabulary in its early layers whose units are not the tokenizer's"
version: 1
tags:
- representation-and-encoding
date: '2026-09-17'
source:
- LIT-412
- LIT-409
- LIT-417
explains:
- SOTA-247
summary: >-
  Kaplan et al. (2024), [LIT-412](../literature.d/LIT-412.md), with [LIT-409](../literature.d/LIT-409.md) and [LIT-417](../literature.d/LIT-417.md) —
  sub-word sequences are recombined into whole-unit representations at a
  unit's last token, in early and middle layers, and the units include things
  the tokenizer has no entry for: arbitrary splits, typos, out-of-vocabulary
  words, named entities and non-compositional multi-word expressions. Three
  groups, three methods — a probe with a co-occurrence control, an erasure
  signature, and layer ablation — reaching the same place. The tokenizer's
  vocabulary is the model's input format, not its inventory of units.
---


<!-- inactive-ok-file: SOTA-247, THEORY-023 — both Proposed and
     both filed in this same change. The practice is named as what this
     account makes possible, with its own status saying why it is not
     asserted; the four-stage framework is named as the WEAKER framing
     that this evidence supports one stage of and does not promote. -->

# THEORY-021: A model builds a latent vocabulary in its early layers whose units are not the tokenizer's

## Source

Kaplan et al. (2024), [LIT-412](../literature.d/LIT-412.md), primary;
with Feucht et al. (2024), [LIT-409](../literature.d/LIT-409.md), and
Lad et al. (2024), [LIT-417](../literature.d/LIT-417.md).

## What was actually shown

**Three groups, three methods, one place.** This is the reason the record
holds the claim rather than the papers' individual confidence.

- **A probe, with the control that matters.** A k-NN classifier on Llama2-7B
  last-token states separates real words from positionally-matched nonwords at
  **89%** by layer 13, rising from chance across layers 2-6. Run on the
  **penultimate** token — which co-occurs with the same prefixes just as often
  — it reaches only **61%**. So the signal tracks a completed unit, not a
  frequent token sequence ([LIT-412](../literature.d/LIT-412.md)).
- **An erasure signature.** Probes that recover neighbouring and current token
  identity everywhere else **fail at the last token of a multi-token word or
  named entity**, in early layers, on Llama-2-7b and Llama-3-8b across ~12,000
  correctly-answered COUNTERFACT and Wikidata prompts. Non-final subject
  tokens do not show it ([LIT-409](../literature.d/LIT-409.md)).
- **An ablation.** The layers whose removal a model cannot absorb are the
  first ones, and the stage immediately after the first layer is the one Lad
  et al. name detokenization ([LIT-417](../literature.d/LIT-417.md)).

**The units exceed the vocabulary, which is the substantive half.** The
reassembly survives **arbitrary splits** (`cats` → `ca` + `ts`), typos, and
**out-of-vocabulary words**; feeding a last-token representation back in as
input, the model reads it as the whole word although no such representation
ever appeared as input during training. And the units are not only words:
[LIT-409](../literature.d/LIT-409.md) counts named entities and
**non-compositional multi-word expressions** — `break a leg`, whose meaning is
no more predictable from `break` and `leg` than `patrolling`'s is from `pat`
and `rolling`.

**What could have come out the other way.** If reassembly were memorization of
frequent token sequences, the penultimate-token probe would have matched the
last-token probe, and out-of-vocabulary words and arbitrary splits would have
broken it. Both checks were run and both went the other way.

**And it is constructive.** The representations support a vocabulary-expansion
method that preserves the model's accuracy —
[SOTA-247](../practices.d/SOTA-247.md) — which is a stronger test of
the account than any probe: a representation you can put back into the
embedding matrix and have the frozen model use is one that was really there.

## What this does not say

**It does not say the tokenizer's choice is free.** The latent vocabulary is
recovered *despite* the split, which says reassembly happens, not that it is
costless. Nobody in this line measures what the reassembly spends — in layers,
in parameters, or in accuracy on units it fails to rebuild — and the obvious
practice, *stop worrying about tokenizer quality*, does not follow and is not
filed.

**The erasure instrument has no ground truth**, and its authors say so: a high
lexicality score cannot be told apart from an error in the method, and the
comparison set of multi-token words and spaCy entities "likely does not cover
all cases".

**Llama, and English.** [LIT-409](../literature.d/LIT-409.md) is
Llama-2-7b and Llama-3-8b only, and English only, by its own limitations
section; [LIT-412](../literature.d/LIT-412.md)'s probes are Llama2-7B,
with the vocabulary-expansion result reaching Arabic. The layer-ablation
evidence is GPT-2 and Pythia. No result here is at the scale the practice
registry mostly advises on.

**It does not confirm the four-stage framework**, though it supports one
stage of it. [THEORY-023](THEORY-023.md) remains `Proposed` for
reasons this evidence does not touch: its boundaries are approximate and its
middle stages are interpolations.

**And it does not close the bridge to the signal side.**
[THEORY-022](THEORY-022.md) says English delimits lexical units by
construction rather than by frequency; this says models rebuild units their
tokenizer split. The two now overlap on **non-compositional multi-word
units**, which is a much narrower coincidence than "both concern
tokenization" — and it is still a coincidence of subject matter. **Nobody has
run the experiment**: whether the units a model's implicit vocabulary contains
are the ones a language delimits by construction, and what happens to the ones
it does not.
