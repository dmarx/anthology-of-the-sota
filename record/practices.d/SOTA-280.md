---
number: 280
status: Active
formerly:
- SOTA-tmp9d9au
consensus: emerging
consensus_note: >-
  One group, one paper, but across four model families and five benchmarks,
  and the technique is widely reimplemented under this name. Not `converged`:
  no production report in the record trains or serves under it, and the
  compute cost means plenty of deployments reasonably decline it.
title: 'Sample several reasoning paths and take the majority answer rather than decoding one greedily'
version: 1
tags:
- in-context-learning
- inference-optimization
date: '2026-09-21'
source:
- LIT-468
introduced_by:
- LIT-468
extends:
- SOTA-279
implementations: []
summary: >-
  Wang et al. (2022), [LIT-468](../literature.d/LIT-468.md) — replace greedy decoding with
  sample-and-marginalize: GSM8K +17.9, SVAMP +11.0, AQuA +12.2. Five or ten
  paths recover most of it, which is the whole cost question.
---

# SOTA-280: Sample several reasoning paths and take the majority answer rather than decoding one greedily

## Source

Wang et al. (2022), [LIT-468](../literature.d/LIT-468.md) — [ARXIV-2203.11171](https://arxiv.org/abs/2203.11171),
read as [NOTE-217](../notes.d/NOTE-217.md).

## What to do

Keep the chain-of-thought prompt exactly as it is. Change the decoding:
sample several reasoning paths instead of taking the greedy one, extract each
path's final answer, and return the most frequent.

**Start at five or ten paths.** That is the authors' own guidance and it is
the practical content — performance saturates quickly, so the marginal path
stops paying well before the budget does.

## Why it works, and what that implies

A hard problem admits several routes to one correct answer, while wrong
answers tend to be reached idiosyncratically. Agreement between independent
derivations is therefore evidence, and a single greedy path offers no such
check — it is exposed both to local optimality and to the luck of one sample.
It is ensembling without an ensemble.

The implication worth carrying: **it counts answers, not reasoning.** The
by-products the authors report — calibration and an uncertainty estimate —
come from the answer distribution, not from the traces being any better.

## Conditions

- **The task needs a determinate, extractable final answer** to compare
  across samples. Arithmetic and multiple choice qualify; open-ended
  generation does not, and the paper does not claim it.
- **Cost is linear in paths** and is the one limitation the authors name.
  Five or ten is a rule of thumb without a scaling story — whether the
  saturation point moves with task difficulty is not measured.
- **Sampling must be diverse enough** to produce genuinely different paths,
  or this degenerates to greedy decoding at `N` times the price.
- **It does not make the traces trustworthy.** The authors note models
  sometimes generate nonsensical reasoning paths, and [LIT-467](../literature.d/LIT-467.md)'s error
  analysis found correct answers reached through incorrect chains. An
  evaluation that reads a trace as an explanation is not rescued by this —
  see [SOTA-278](../practices.d/SOTA-278.md).
- **Two of the four models are not public**, so part of the evidence is not
  directly reproducible; the authors supply prompts and two public Codex
  engines.

## Relation to the neighbours

Extends [SOTA-279](../practices.d/SOTA-279.md) by changing how its output is read rather than what
it is asked. Being a sampling algorithm, it also files under
`inference-optimization`, whose blurb names them.

It composes with [SOTA-281](../practices.d/SOTA-281.md) in principle — nothing requires the
sampled chains to come from exemplars rather than a trigger sentence — but
that pairing is not what either paper measured, and the record should not
imply it was.
