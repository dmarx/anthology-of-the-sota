---
status: Active
title: 'On the Statistical Query Complexity of Learning Semiautomata: a Random Walk Approach'
version: 1
tags:
- analysis-and-evaluation
- model-architecture
- training-optimization
date: '2026-09-21'
published: '2025-10-05'
arxiv: '2510.04115'
first_author: 'Giapitzakis'
keywords:
- 'statistical-query-hardness'
- 'semiautomata'
- 'state-tracking'
- 'sq-dimension'
- 'random-walks-on-groups'
- 'representation-theory'
implementations: []
summary: >-
  Giapitzakis, Fountoulakis, Nichani and Lee (2025), [ARXIV-2510.04115](https://arxiv.org/abs/2510.04115). The first Statistical
  Query hardness result for semiautomata, and the first where the hardness
  comes from the **transition structure alone** rather than from a hard
  language embedded in the machine. Two distinct machines in the constructed
  family agree at chance after `O(N² ln N)` random symbols, so the signal
  separating them vanishes exponentially in sequence length. The regime it
  needs is unusual and belongs beside the result: an alphabet of size
  `Ω(N³ ln N)`.
---

<!-- inactive-ok-file: THEORY-tmp38xax — Proposed, filed in this same
     contribution as this paper's account, with its unsettledness argued in
     the theory's own "why Proposed" -->

<!-- inactive-ok-file: SOTA-178 — Proposed, and cited precisely to say this
     paper is about a DIFFERENT axis from it. A contrast between two open
     claims does not wait on either being settled -->

# LIT-tmpzynnf: On the Statistical Query Complexity of Learning Semiautomata: a Random Walk Approach

Giapitzakis, Fountoulakis, Nichani and Lee (2025) —
[ARXIV-2510.04115](https://arxiv.org/abs/2510.04115), read as [NOTE-tmpi0371](../notes.d/NOTE-tmpi0371.md).

## Key takeaways

- **Structural, not language-based hardness.** Every prior SQ hardness result
  for finite automata works by embedding something hard — usually parity —
  into the language the machine accepts, often under an adversarial input
  distribution. A semiautomaton has no accepting states, so there is no
  language to hide anything in. The hardness here comes only from the
  transition functions, under the **uniform** distribution over input words
  and initial states.
- **The mechanism is a mixing argument.** Reading a random word drives a
  random walk on `S_N × S_N`; the probability two machines land in the same
  state is `1/N + error`, with `|error| ≤ (1 − 1/2N)^T`. So distinct machines
  become indistinguishable **exponentially fast in word length**. A single
  irreducible representation, `std ⊗ std`, controls the whole thing, which is
  what makes the calculation tractable.
- **`N!` nearly-uncorrelated machines gives SQ dimension `N!`**, and therefore
  the lower bound: any SQ learner must make super-polynomially many queries or
  use super-polynomially small tolerance.
- **The bridge to practice is cited, not proved here.** Abbe et al. (2021)
  showed SGD is equivalent in power to SQ learning **with large mini-batches
  or low-precision gradients** — which is the regime almost all current
  training is in. The paper states this in one sentence of related work and
  builds nothing on it.
- **The construction needs an alphabet of `Ω(N³ ln N)`** and words of
  `Ω(N² ln N)`. At `N = 100` that is an alphabet of roughly 4.6 million
  symbols for a hundred-state machine. This is stated plainly in the
  contributions and is the single most important thing to carry when citing
  the result.
- **The mixing bound is tight**, `T = Ω(N² ln N)`, proved as a byproduct.

## Standing in the anthology

Kept for the mental model rather than the theorem, which is
[THEORY-tmp38xax](../theory.d/THEORY-tmp38xax.md): longer random sequences carry *less*
information about a hidden transition structure, not more. That is the
opposite of the usual intuition about context length and it is where the
record had nothing.

**No practice is filed.** The result is a proof about one constructed family
in a regime nobody trains in, with no experiments, and the step from SQ to
gradient descent is somebody else's theorem quoted once. What a practice would
need is in the reading's open questions.

It sits beside the record's existing limits cluster and is a different axis
from it. [SOTA-178](../practices.d/SOTA-178.md) and [THEORY-038](../theory.d/THEORY-038.md) are about
**expressivity** — what an architecture can represent at all. This is about
**learnability** — whether gradient descent finds it. A model that provably
can represent a machine can still be unable to learn it, and the record did
not previously distinguish the two.

**Worth recording:** the paper's AI-use statement says the randomized
construction in §5 was initially suggested by Gemini 2.5 Pro, which prompted
the authors to draw the random-walk connection. Second paper read today with
an explicit statement of that kind, filed as an observation and not as a
finding.
