---
status: Active
consensus: converged
consensus_note: >-
  Verified in library code rather than inferred. `mlfoundations/open_clip`
  ships the paper's set verbatim as `OPENAI_IMAGENET_TEMPLATES` — 80 entries,
  exactly the count the paper reports ensembling — alongside a
  `SIMPLE_IMAGENET_TEMPLATES` of 7, and its zero-shot classifier builds the
  ensemble from them. Checked at `2d53460` on 2026-09-23. A five-year-old
  prompt list surviving unchanged as the default evaluation protocol is
  convergence; whether each adopter chose it deliberately is another
  question, which `DP-005` says is the right one to keep separate.
title: 'Build a zero-shot classifier from prompt templates and ensemble them in embedding space'
version: 1
tags:
- in-context-learning
- multimodal-learning
- analysis-and-evaluation
date: '2026-09-23'
source:
- LIT-tmpc8ymt
introduced_by:
- LIT-tmpc8ymt
implementations: []
---

# SOTA-tmp4xixm: Build a zero-shot classifier from prompt templates and ensemble them in embedding space

## Source

Radford et al. (2021), [LIT-tmpc8ymt](../literature.d/LIT-tmpc8ymt.md) — [ARXIV-2103.00020](https://arxiv.org/abs/2103.00020).

## The claim

When you build a classifier by embedding class names with a contrastively
trained text encoder, **do not embed the bare class name**. Put it in a
sentence, build several sentences, and average their embeddings — not their
probabilities — into one classifier.

The measurements, on ImageNet:

| step | gain |
| --- | --- |
| `"A photo of a {label}."` over the bare name | **+1.3%** |
| ensembling 80 context prompts on top of that | **+3.5%** |
| together, averaged over 36 datasets | **~+5%** |

The paper measures that ~5% as **equivalent to using 4× more compute** with
the contextless method.

## Why it is nearly free, which is the part that makes it a practice

Averaging happens in the **embedding space**, not over softmax outputs. So
the 80 prompts collapse into a single set of class vectors, computed once per
label set and cached. Amortised over a dataset, an 80-prompt ensemble costs
what one prompt costs. A probability-space ensemble would cost 80× and is the
obvious wrong way to do it.

## Why the bare class name loses

It is a distribution mismatch, not a semantic one. Almost nothing in a
web-scraped caption corpus is a single word; the text the encoder saw was
sentences. `"A photo of a {label}."` moves the query back into the
distribution the encoder was trained on. That also explains why the task
hints help — `", a type of pet"` on Oxford-IIIT Pets, `"a satellite photo
of"` on satellite imagery, quotes around the string for OCR: each names the
context the matching caption would have carried.

## Conditions

- **This is a property of the evaluation, not of the model.** Two papers
  reporting zero-shot numbers for the same checkpoint can differ by ~5% on
  prompting alone, which is larger than most claimed improvements. A
  zero-shot number without its prompt set is not comparable to another one.
- **The templates are dataset-specific and hand-written.** The paper's own
  list was tuned against the datasets it reports on, and the authors say
  their evaluation suite is "undeniably co-adapted" with CLIP. Carrying the
  ImageNet 80 to a new domain is a starting point, not a result.
- **It is a prompting practice for contrastive image-text classifiers.** The
  mechanism — put the query in the training distribution, ensemble cheaply
  where the geometry lets you — generalises further than the template list
  does.

## Known implementations

- `mlfoundations/open_clip` — `OPENAI_IMAGENET_TEMPLATES` (80) and
  `SIMPLE_IMAGENET_TEMPLATES` (7) in `src/open_clip/zero_shot_metadata.py`.
