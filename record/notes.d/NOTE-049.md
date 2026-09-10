---
number: 49
paper: LIT-049
status: Read
formerly:
- NOTE-tmpj96x3
title: 'Learning to Prompt for Vision-Language Models'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-09'
published: '2021-09-01'
summary: >-
  Replaces hand-written CLIP prompts with continuous context vectors learned end-to-end while every pretrained parameter stays frozen. One or two shots beat prompt engineering; sixteen shots average about 15% gain, over 45% at the best. The paper also reports where it overfits and names the cause as noisy labels.
---

# NOTE-049: Learning to Prompt for Vision-Language Models

## Contribution

Identifies **prompt engineering as the deployment bottleneck** for CLIP-style
models — "a slight change in wording could have a huge impact on performance" —
and removes it. **CoOp** models a prompt's context words as **learnable
continuous vectors**, optimised end-to-end from a few labelled examples, with
the entire pretrained model frozen.

Two variants: **unified context** (one context shared across classes) and
**class-specific context**.

## Key insight

A prompt is a point in embedding space that someone is searching by typing. Once
that is said, the search should be gradient descent, and the discreteness of
words is an obstacle rather than a feature. Nothing about the model changes; the
optimisation happens entirely in the input.

This is the same move as `LIT-078`'s textual inversion — optimise in the frozen
model's input embedding space — arriving from the other direction. There the
goal was to *name a new concept*; here it is to *find better words for a known
one*. Same intervention point, same reason it is safe.

## Assumptions

- The context that works is expressible in continuous embedding space and
  reachable by gradient descent from a reasonable initialisation.
- A handful of labelled examples per class is available — this is few-shot
  learning, not zero-shot, despite operating on a zero-shot model.
- 11 image recognition datasets, CLIP-family models, 2021.

## Key results

- **One or two shots beat hand-crafted prompts by a decent margin.**
- **16 shots: ~15% average gain, highest over 45%** across 11 datasets.
- **Strong domain generalisation** compared to the zero-shot model with
  hand-crafted prompts — notable, because a learned prompt should be the thing
  that fails to generalise.
- **Reported negative results, with a diagnosis:** on Food101, CoOp and linear
  probing both underperform, and the authors attribute it to training data with
  "intense colors and sometimes wrong labels". The learning curves show a loss
  of momentum with more shots — "seemingly an overfitting problem" — and they
  suggest **higher weight decay** as a remedy without claiming to have solved it.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Prompt engineering is a real and costly bottleneck | strong | the premise, widely corroborated |
| C2 | Learned continuous context beats hand-written prompts | strong | 11 datasets, large margins |
| C3 | One or two shots suffice to beat prompt engineering | strong | measured |
| C4 | Learned prompts still generalise across domains | moderate | measured against the zero-shot baseline |
| C5 | Failures are caused by label noise | **moderate — an attribution** | consistent with the cited dataset description, not isolated |

## Method

Freeze CLIP. Represent the context tokens of the prompt as learnable vectors.
Optimise them on a few labelled examples per class with the classification loss.
Optionally learn a separate context per class.

## Concepts

- **Prompting as continuous optimisation** — the reframing.
- **Input-space adaptation** — changing nothing but what goes in, the same
  intervention point as textual inversion and as soft prompting in language
  models.
- **Reporting the failure and naming the suspect** — C5, and the paper does not
  overclaim the diagnosis.

## Connections

Sibling to `LIT-078` (textual inversion), same intervention point, different
goal. Both sit at the cheap end of the adaptation spectrum whose expensive end
is `LIT-079`'s full fine-tune.

C4 is in tension with the general expectation that a learned prompt overfits its
training distribution, and is a data point the record's adaptation
neighbourhood does not have.

## Recommendations

- **R1** — If a discrete artefact is being tuned by hand, check whether its
  continuous relaxation can be optimised instead. *Topic:* adaptation and
  tuning. *Strength:* strong.
- **R2** — Adapt in the input space before adapting weights. *Strength:*
  strong.
- **R3** — When a method underperforms, report the dataset property you suspect
  and say you have not isolated it. *Topic:* analysis and evaluation.
  *Strength:* strong.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**
Retagged from `model-architecture` — nothing architectural happens — to
`adaptation-and-tuning`.

R1 is the transferable statement and the record does not have it. Prompt
optimisation, textual inversion and soft prompting are three instances of the
same move, in two modalities, and the general form — **replace hand search over
a discrete artefact with gradient descent over its continuous relaxation** —
covers all three and is stated nowhere.

The document's takeaway **"zero-shot capabilities" is misleading.** CoOp is
few-shot: it needs labelled examples. What it preserves is the *zero-shot
model's* generality, which is a different claim and the one C4 is about.

## Limitations

- 11 image classification datasets, CLIP-family, 2021.
- Few-shot, so it needs labels the zero-shot setting does not.
- C5 is an attribution the authors offer without isolating it.
- Learned contexts are not interpretable, which the paper does not dwell on and
  which matters for the "prompt engineering is hard" framing — the fix removes
  the artefact people were reasoning about.

## Open questions

- Does the domain generalisation in C4 survive a larger distribution shift? A
  learned prompt generalising better than a written one is surprising enough to
  want more evidence.
