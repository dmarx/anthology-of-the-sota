---
number: 33
status: 'Active'
title: 'continued pre-training for fine tuning'
version: 1
tags:
- model-architecture
date: '2026-08-24'
published: '2020-04-01'
source:
- LIT-034
summary: >-
  Gururangan et al. (2020), [LIT-034](../literature.d/LIT-034.md) — [ARXIV-2004.10964](https://arxiv.org/abs/2004.10964).
---

# SOTA-033: continued pre-training for fine tuning

## Source

Gururangan et al. (2020), [LIT-034](../literature.d/LIT-034.md) — [ARXIV-2004.10964](https://arxiv.org/abs/2004.10964).

## The finding, more precisely than the title

[LIT-034](../literature.d/LIT-034.md)'s result is that continuing to pretrain on unlabelled text before
fine-tuning helps, and that it helps on two distinguishable axes: **domain**
adaptive pretraining on a large corpus from the target domain, and **task**
adaptive pretraining on the (much smaller) unlabelled text of the task itself.

Both help, they are complementary rather than alternatives, and the second is
the surprise — a few thousand unlabelled task examples are worth a further
pretraining stage even when the domain corpus has already been used.

## Where this sits now

The practice predates instruction tuning and post-training with verifiable
rewards, and the record should say so rather than leave a reader to assume
this is current adaptation advice. The modern pipeline's stages are different
in kind: the question is no longer "more pretraining before fine-tuning" but
what mixture of supervised and reinforcement stages follows pretraining
<!-- inactive-ok: SOTA-130 — Proposed; cited as the line the modern question runs along, not as advice -->
([SOTA-130](SOTA-130.md)'s line).

What survives, and is still worth knowing, is the underlying claim: **the
pretraining distribution matters more than the fine-tuning one for a task far
from it**, and unlabelled in-domain text is the cheapest lever on that. That
is why domain-specialised models are still built this way, and why the record
keeps the practice Active while its surrounding pipeline has been replaced.
