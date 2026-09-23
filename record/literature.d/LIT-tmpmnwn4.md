---
status: Active
title: 'Mass-Editing Memory in a Transformer'
version: 1
tags:
- adaptation-and-tuning
- analysis-and-evaluation
date: '2026-09-23'
published: '2022-10-01'
arxiv: '2210.07229'
first_author: 'Meng'
keywords:
- 'memit'
- 'knowledge-editing'
- 'mass-editing'
- 'counterfact'
- 'zsre'
implementations:
- memit
extends:
- LIT-tmpvij69
summary: >-
  Meng, Sen Sharma, Andonian, Belinkov, Bau (2023), [ARXIV-2210.07229](https://arxiv.org/abs/2210.07229). MEMIT
  writes thousands of facts at once by spreading each update over a range
  of mid-layer MLPs (layers 3–8 in GPT-J) in one batched least-squares
  solve. At 10,000 CounterFact edits it scores 85.8 on GPT-J (ROME 50.3,
  fine-tuning 67.6 with generation collapse). Neighborhood success falls
  from 83.5 to 73.7.
compared_against:
- LIT-tmprhke9
---

# LIT-tmpmnwn4: Mass-Editing Memory in a Transformer

Meng, Sen Sharma, Andonian, Belinkov, Bau, MIT, Northeastern and Technion
(2023) — [ARXIV-2210.07229](https://arxiv.org/abs/2210.07229)

## Key takeaways

- **The method** (§4): compute a target hidden state for each fact at the
  last critical layer. Distribute the needed change across the range of
  critical MLP layers, R = {3…8} for GPT-J, chosen where severing MLPs cuts
  the causal effect. Solve for each layer's update with a least-squares
  objective that also preserves a covariance of existing keys
- **zsRE, 10,000 real facts on GPT-J** (Table 1): efficacy 96.7, paraphrase
  89.7, specificity 26.6 (unedited 27.0). ROME collapses to 2.6 overall.
  Plain fine-tuning (42.1) beats both ROME and MEND at this scale
- **CounterFact, 10,000 counterfactuals** (Table 2): MEMIT 85.8 on GPT-J
  (ES 98.9, PS 88.6, NS 73.7, against 83.5 unedited) and 82.0 on GPT-NeoX-20B.
  ROME 50.3. Fine-tuning scores 67.6, with fluency collapsing (generation
  entropy 294 against 622)
- **Scaling curve** (Figure 5): ROME is fine to about 10 edits and degrades
  from 32. MEND loses efficacy by 1,000. At small n, ROME generalizes
  slightly better than MEMIT
- **Cost:** 7.4 hours for 10,000 edits on GPT-J, done serially in the
  released code

## Standing in the anthology

**Filed from `#163`** (LARQL). It `extends` ROME and sources [SOTA-tmp2nfwy](../practices.d/SOTA-tmp2nfwy.md),
which RippleEdits ([LIT-tmprhke9](LIT-tmprhke9.md)) contests.

**What "10,000 memories" means here.** The test is recall of the edited
triple, its paraphrases and unrelated neighbors. Whether the edited facts
propagate to their implications is not tested, and when it later was,
MEMIT did not ([LIT-tmprhke9](LIT-tmprhke9.md)).

Read — [NOTE-tmpk15k0](../notes.d/NOTE-tmpk15k0.md).
<!-- inactive-ok-file: SOTA-tmp2nfwy — Proposed and contested, filed in this same contribution from this paper -->
