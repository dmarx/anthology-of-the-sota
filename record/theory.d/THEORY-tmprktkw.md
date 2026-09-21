---
status: Proposed
promote_when: >-
  The split measured on a third corpus chosen to separate the two skills
  rather than to contrast two off-the-shelf datasets — or, better, a
  within-corpus test: hold the training data fixed and show the
  parameter-versus-computation exchange rate differing between memorization-
  heavy and reasoning-heavy *evaluations* of that one model. The present
  evidence cannot tell "computation buys reasoning" apart from "Stack-V2 is a
  narrower distribution than the Pile". What would not settle it: another
  paper reporting that a parallel or inference-time method helps more on
  maths and code, which is the observation rather than the explanation.
title: 'Parameters carry memorization and parallel computation carries reasoning'
version: 1
tags:
- analysis-and-evaluation
- model-architecture
date: '2026-09-21'
source:
- LIT-tmpitbks
explains:
- SOTA-tmp9spic
summary: >-
  Chen et al. (2025), [LIT-tmpitbks](../literature.d/LIT-tmpitbks.md) — the exchange rate between parallel
  streams and parameters is fitted **higher on code (0.39) than on general
  text (0.33)**, and downstream a 1.6B model at `P = 8` matches a 4.4B model
  on coding but only a 2.8B one on general tasks. Two independent
  measurements pointing the same way, and an account the authors themselves
  call a conjecture.
---

<!-- inactive-ok-file: SOTA-tmp9spic — Proposed, filed in this same
     contribution; this theory declares `explains:` on it, so the citation is
     the relation itself and cannot wait on the practice being settled -->

# THEORY-tmprktkw: Parameters carry memorization and parallel computation carries reasoning

## Source

Chen et al. (2025), [LIT-tmpitbks](../literature.d/LIT-tmpitbks.md) §3.2 and §3.3 — read as
[NOTE-tmp5l9o0](../notes.d/NOTE-tmp5l9o0.md).

## What it explains

| practice | what it says to do | what this says is going on |
|---|---|---|
| [SOTA-tmp9spic](../practices.d/SOTA-tmp9spic.md) | scale parallel computation instead of parameters when inference memory binds | you are buying one of the two things parameters buy, and not the other — which is why the practice's benefit is uneven across tasks rather than uniform, and why the decision is task-dependent rather than purely an efficiency calculation |

## The account

A model's parameters do two jobs that scaling has never had to separate:
they **store** things, and they **compute** with them. Parallel scaling moves
one of those independently of the other — the parameter count is nearly
fixed and the computation multiplies — so for the first time the two can be
priced apart.

The claim is that what extra computation buys is **reasoning**, and what
extra parameters buy is **memorization**.

**Two measurements, arrived at differently, agree.** The fitted exchange rate
between streams and parameters is **0.39** on Stack-V2-Python and **0.33** on
the Pile — a corpus built around code comprehension and one built around
general knowledge. Separately, at the downstream level, a 1.6B model at
`P = 8` reaches the **4.4B** baseline on coding tasks and only the **2.8B**
baseline on general ones. A fitted constant and a benchmark table are
different instruments, and they rank the two corpora the same way.

**It also explains the thing the paper started from.** Classifier-free
guidance's second forward pass carries *less* information than the first, and
the two-pass result is better. If computation were merely a way of retrieving
more of what the weights already store, a degraded input could not help. If
computation is its own resource, it can.

## Why `Proposed`

**Because two corpora are not a variable.** Stack-V2-Python and the Pile
differ in more ways than memorization-versus-reasoning: one is far narrower,
more repetitive, more structured, and lower in entropy per token. Any of
those could produce a higher return on ensemble-like diversity without a word
of it being about reasoning. The experiment that distinguishes them has not
been run, and the promotion condition asks for it.

**Because the authors label it a conjecture** — "an intuitive conjecture" is
their phrase — and the record's job is to carry that label rather than to
quietly upgrade it. This is the sentence in the paper most likely to be cited
as a finding, which is [DP-010](../principles.d/DP-010.md)'s shape exactly.

**Because "reasoning" is doing unexamined work.** The evidence is coding and
maths benchmarks. Whether those measure reasoning, or measure the kinds of
task where a narrow training distribution and a verifiable answer make
ensembling pay, is the whole question and is assumed.

**Because the mechanism is absent.** There is no account of *how* parallel
computation would produce reasoning specifically. The formal result in the
paper says the benefit of `P` streams depends on the **diversity** between
them, and diversity is never measured — so even the paper's own theory does
not connect to this claim. A story about what computation is for sits on top
of a fit that is agnostic about it.

## What it does not say

**It does not say parameters are useless for reasoning**, or computation
useless for recall. The measurements are of *marginal* returns at the margin
tested: the exchange rate differs by corpus, both coefficients are positive,
and general tasks improve under `P` too — just less.

**It does not license reading the two corpora as pure.** The Pile contains
code and Stack-V2 contains memorizable idiom. The 0.39/0.33 gap is the
difference between two impure mixtures, and its size should be read with that
in mind: it is a real difference and it is not a large one.

**It says nothing about inference-time scaling**, though the authors note the
alignment with work on latent-space reasoning. Serial and parallel
computation are different resources and this measured one of them.
