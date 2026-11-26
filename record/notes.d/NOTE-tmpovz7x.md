---
status: Skimmed
paper: LIT-tmpilnw1
title: 'Understanding AI from the Inside'
version: 1
date: '2026-11-26'
summary: >-
  A survey of mechanistic interpretability for transformers that asks whether
  understanding makes models safer, calls the assumption untested, and does
  not test it. Read at v2: introduction, the behavioural-evaluation case,
  limitations, the SAE checklist, the evaluation framework's own caveats,
  the safety verdicts and the conclusion. The method chapters were skimmed.
---

# NOTE-tmpovz7x: Understanding AI from the Inside

**This note is `Skimmed`, not `Read`.** The v2 HTML is about 5,300 lines of
body before the references. These parts were read verbatim: the abstract,
§1 and §1.2 (scope), §2, §3.6–3.7, §6.5.4–6.5.6, §6.9.4, §7.3, §7.5.4,
§13.1.2, §13.3, §13.7.5, §14.1–14.2 and §15. §4–§7 were covered unevenly,
partly through a model-extracted summary. §8–§12, most of §13 and the
appendices were not read beyond their headings. Nothing should be sourced
from this note. It is a survey in any case, and the record sources
practices from primary work.

## Contribution

A survey of mechanistic interpretability (MI) for transformers, framed
around one question: does understanding how models work make them safer?
It covers foundations (features, polysemanticity, circuits), core hypotheses
(linear representation, superposition, privileged access, universality),
feature extraction (SAEs and their variants, transcoders, cross-layer
transcoders, crosscoders), circuit discovery and causal verification,
natural-language decoding of representations, learning dynamics and
training-data attribution. Beyond the review it offers two things of its
own: a five-dimension evaluation framework (§7.5) and a taxonomy of six
research orientations (§12).

## Key insight

**Mechanistic evidence and behavioural evidence answer different
questions, and neither replaces the other.** Behavioural testing can show
that a behaviour is present on the inputs tried. It cannot show that a
capability is absent, that the mechanism is the intended one, or that the
result holds off-distribution. Mechanistic analysis can address those, but
it costs more, it is usually incomplete, and finding a mechanism does not
by itself give control over it. The survey's verdict is that
interpretability is one layer of defence in depth.

## Assumptions

Scope assumptions rather than formal ones (§1.2):

- An analysis counts as mechanistic only if it works on internals and
  makes a causal claim through intervention
- Transformers are the main object. §14.7 marks transfer to other
  architectures as open
- Behavioural evaluation, input attribution, concept-bottleneck models and
  causal abstraction are discussed but not covered in depth

## Key results

None of its own. The numbers it reports come from cited work. These are
the ones the reading checked:

- Linear probes detect a sleeper-agent trigger at over 99% AUROC, while
  SFT, RLHF and adversarial training fail to remove the backdoor
  (MacDiarmid et al., 2024; Hubinger et al., 2024) (§2)
- Often fewer than 50% of SAE features recur across seeds (Paulo & Belrose,
  2026) (§6.5.4)
- With labels available, supervised methods often beat SAEs at concept
  detection and steering (Wu et al., 2025b and others) (§6.9.4)
- Steering vectors frequently degrade under distribution shift (Tan et al.,
  2024) (§13.3.1)

## Concepts

- **Mechanistic** — internals plus causal claims through intervention
  (§1.2). A probe becomes mechanistic only when its direction is used to
  intervene
- **Feature** (§4.3) — a geometric structure in activation space that
  predicts a concept and is causally relevant to it
- **Interpretability gap** (§1) — the distance between what a model can do
  and what is understood about how it does it
- **Five evaluation dimensions** (§7.5.2) — attribution faithfulness,
  completeness, stability, causal validity, human interpretability

## Connections

It builds on earlier surveys it names (Bereska & Gavves 2024, Ferrando et
al. 2024 and others) and differs from them in asking what interpretability
buys for safety. In the record it overlaps with Méloux et al. ([LIT-504](../literature.d/LIT-504.md)),
whose identifiability result it cites in §6.5.5. It also overlaps with
Hase et al. ([LIT-574](../literature.d/LIT-574.md)), cited in §3.7 for localisation not informing
editing, and with ROME ([LIT-578](../literature.d/LIT-578.md)), the §13.2.2 case study. It does not
cite Kantamneni et al. ([LIT-568](../literature.d/LIT-568.md)), the record's source for probes over
SAEs.

## Recommendations

From §6.5.6, as the survey states them. They are candidates, and the
evidence for each belongs to the cited primary work:

- **R1** — Report dead-feature rate, duplication and cross-seed stability
  next to SAE reconstruction loss. *Topic:* concept-geometry. *Strength:*
  moderate, resting on Paulo & Belrose (2026), which is not in the record
- **R2** — Validate a feature's necessity, sufficiency and specificity by
  intervention before making claims about it. *Strength:* moderate
- **R3** — Treat a dictionary as one valid decomposition, not the true
  features. Already [SOTA-310](../practices.d/SOTA-310.md)
- **R4** — Use supervised probes or DAS when the concept is known in
  advance. Already [SOTA-345](../practices.d/SOTA-345.md)

## Bearing on the record

This reading confirms [SOTA-310](../practices.d/SOTA-310.md) and [SOTA-345](../practices.d/SOTA-345.md) and changes neither. A
survey's agreement is adoption, not a second test. R1 is the one candidate
the record lacks. It should be filed from Paulo & Belrose (2026) after a
reading of that paper, not from this survey.

## Limitations

- The title question goes unanswered. The paper says the assumption that
  understanding makes systems safer is "largely untested" (§1.1, §15.1).
  It does not test it, and it ends by asking the question again (§15.2)
- §7.3 says a circuit "typically explains 60–80% of behavioural variance",
  with no citation and no definition of the variance
- §14.1 says safety training has made backdoors harder to implant, also
  without a citation
- §3.7 calls MI's limitations "not fundamental barriers" without an
  argument
- The evaluation framework is not applied to any method. §7.5.4 says its
  metrics are "not uniquely correct" and its thresholds uncalibrated, and
  that the full protocol may cost too much to run
- Of this note: the method chapters were not read closely enough to check
  the survey's characterisation of the work it cites

## Open questions

- Whether any safety task can be done better with mechanistic methods than
  with a matched black-box baseline, on the same budget. The survey asks
  this (§1.1) and does not settle it
- Whether the five-dimension framework, once applied, ranks methods
  differently from the single metrics each method reports now
