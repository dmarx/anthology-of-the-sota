---
number: 217
status: Read
formerly:
- NOTE-tmpkw9rw
paper: LIT-468
title: 'Self-Consistency'
version: 1
date: '2026-09-21'
summary: >-
  Sample several chains, take the majority answer. Reading it: it is a
  decoding change rather than a prompt change, so it composes with everything
  else in the topic — and it counts answers, not reasoning, so it does not
  make the traces trustworthy.
---

# NOTE-217: Self-Consistency

## Contribution

Chain-of-thought prompting had been paired with greedy decoding, so one
sampled path determined the answer. This replaces that with
sample-and-marginalize: draw a diverse set of reasoning paths and take the
most consistent final answer. The prompt is untouched, which is what makes it
composable — it is a change to how the model is read, not to what it is
asked.

## Key insight

Agreement across independently sampled derivations is evidence, and a single
greedy path provides no such check. A hard problem admits several routes to
one correct answer while wrong answers tend to be reached idiosyncratically,
so the mode of the answer distribution is a better estimator than any one
sample. It is ensembling without an ensemble — one model, several draws.

## Assumptions

- **The task has a determinate, extractable final answer** that can be
  compared across samples. Arithmetic and multiple-choice qualify; open-ended
  generation does not, and the paper does not claim it.
- **Sampling with enough diversity** to produce genuinely different paths;
  the method degenerates to greedy decoding if it does not.
- **Chain-of-thought prompting is already in use.** This modifies it rather
  than replacing it.

## Key results

- **GSM8K +17.9, SVAMP +11.0, AQuA +12.2, StrategyQA +6.4, ARC-challenge
  +3.9**, over four model families at varying scale (UL2, GPT-3/Codex,
  LaMDA-137B, PaLM-540B).
- **Saturation is fast.** The authors' own guidance is that five or ten paths
  recover most of the gain, which is the whole cost story and is stated as a
  limitation rather than buried.
- **By-products**: uncertainty estimates and improved calibration, plus
  rationales worth collecting.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Marginalizing over sampled paths beats greedy decoding for CoT | strong | five benchmarks, four model families, consistent direction and large margins |
| C2 | Most of the gain arrives by ~5–10 samples | moderate | the saturation figure; a curve rather than a threshold |
| C3 | It improves calibration and supplies uncertainty estimates | moderate | reported, secondary to the accuracy result |
| C4 | The generated rationales could train a better single-pass model | weak | named as future work, not done here |

## Method

Prompt with chain of thought; sample `N` paths from the decoder rather than
decoding greedily; extract each path's final answer; return the most frequent.

## Concepts

- **Self-consistency** — the sample-and-marginalize decoding procedure.
- **Marginalizing out the reasoning path** — treating the path as a latent
  variable and taking the mode of the answer it induces.

## Connections

Extends [LIT-467](../literature.d/LIT-467.md), which it leaves untouched and decodes differently. It
composes with [LIT-469](../literature.d/LIT-469.md) — nothing about it requires the chains to
come from exemplars rather than from a trigger sentence, though that
combination is not what was measured here.

## Bearing on the record

- **It produces [SOTA-280](../practices.d/SOTA-280.md)**, with the sample count and the
  saturation guidance in its conditions, because the cost is the whole
  question a practitioner has.
- **It is filed under `inference-optimization` as well as
  `in-context-learning`**, because it is a sampling algorithm, which that
  topic's blurb names explicitly. This is the first document to use the new
  topic alongside an old one rather than in place of it.
- **It does not make traces trustworthy, and that matters for
  [SOTA-278](../practices.d/SOTA-278.md).** Marginalizing counts answers, not reasoning. The
  authors note models sometimes generate nonsensical paths, and
  [LIT-467](../literature.d/LIT-467.md)'s error analysis found correct answers reached through
  incorrect chains. An evaluation that reads the trace as an explanation is
  not rescued by this.

## Limitations

- **Compute cost**, stated by the authors as the one limitation, with the
  5–10 mitigation.
- **Needs an extractable final answer**, so it does not reach open-ended
  tasks.
- **Two of the four models are not public** (LaMDA-137B, PaLM-540B); the
  authors supply prompts and two public Codex engines for reproducibility.
- **Nonsensical reasoning paths are acknowledged and not fixed.**
- **No interaction with zero-shot CoT measured**, though nothing forbids it.

## Open questions

- Does the saturation point move with task difficulty? Five or ten is offered
  as a rule of thumb without a scaling story.
- Does it compose with a trigger sentence instead of exemplars, and at what
  cost?
- Is majority voting the right aggregator, or would weighting by path
  likelihood do better? The paper marginalizes uniformly.
