---
status: Active
title: 'Understanding AI from the Inside: The State of Mechanistic Interpretability for AI Safety'
version: 1
tags:
- analysis-and-evaluation
- concept-geometry
- adaptation-and-tuning
date: '2026-11-26'
published: '2026-11-05'
arxiv: '2611.08438'
first_author: 'Barez'
keywords:
- 'mechanistic-interpretability'
- 'ai-safety'
- 'survey'
- 'sparse-autoencoder'
- 'transcoder'
- 'circuit-discovery'
- 'probing'
- 'steering'
- 'training-data-attribution'
- 'evaluation-framework'
implementations: []
summary: >-
  Barez, Wu and 25 others (2026), [ARXIV-2611.08438](https://arxiv.org/abs/2611.08438). A survey of
  mechanistic interpretability for transformers, organised around the
  question whether understanding a model makes it safer. It calls that
  assumption "largely untested" and, being a survey, does not test it. It
  proposes a five-dimension evaluation framework without applying it, and
  concludes that interpretability is one layer of a defence-in-depth
  strategy, not a guarantee. Its SAE checklist (§6.5.6) agrees with
  [SOTA-310](../practices.d/SOTA-310.md) and [SOTA-345](../practices.d/SOTA-345.md) and adds no new evidence for either.
---

# LIT-tmpilnw1: Understanding AI from the Inside: The State of Mechanistic Interpretability for AI Safety

Barez, Wu, Batra, Dominici, Draye, Elazar, Fornasiere, García, Harrasse,
Harris, Hooker, Lan, Li, Maiwald, Oozeer, Saphra, Shafran, Simhi, Trager,
Upadhyay, Yao, Zhao, Cohen, Geva, Bengio, Biderman, Sajjad; Oxford, Martian,
Tel Aviv, Mila, EleutherAI and others (2026) — [ARXIV-2611.08438](https://arxiv.org/abs/2611.08438)

## Key takeaways

- **Scope** (§1.2): two criteria make an analysis mechanistic. It works on
  model internals, and it makes causal claims through interventions such as
  ablation, patching and steering. A probe is correlational until the
  direction it finds is used to intervene. Training-data attribution meets
  neither criterion and is included because workflows now chain it with
  mechanistic analysis
- **Why behaviour is not enough** (§2): contamination and saturation,
  models that reach a score by the wrong mechanism, evaluation awareness,
  and no handle for fine-grained edits. The worked case is sleeper agents,
  where safety SFT, RLHF and adversarial training left the backdoor in
  place. A linear probe still detected the trigger at over 99% AUROC
  (MacDiarmid et al., 2024), so detecting a mechanism and removing it are
  different problems
- **Where mechanism is needed** (§3.6): finding intents hidden from
  outputs, verifying that a capability is absent, and guarantees beyond the
  evaluated distribution. Behavioural tests can only show that something is
  present. The authors set the cost against this and call mechanistic
  methods a complement to behavioural evaluation, not a replacement
- **Explanation is not control** (§3.7): explanations are often
  incomplete, scale poorly, and a validated mechanism need not give a
  reliable intervention. This cites Hase et al. ([LIT-574](LIT-574.md)) and the hydra
  effect. The authors call these "not fundamental barriers" and give no
  argument for that
- **SAE checklist** (§6.5.6): report dead features, duplication and
  cross-seed stability next to reconstruction loss, since often fewer than
  half of features recur across seeds (Paulo & Belrose, 2026). Validate
  features by intervention. Compare with baselines and across SAE variants.
  Treat a dictionary as one valid decomposition, not the true one. Use
  supervised probes or DAS when the concept is known in advance
- **Evaluation framework** (§7.5): five dimensions (attribution
  faithfulness, completeness, stability, causal validity, human
  interpretability), each with metrics and a protocol. It is proposed and
  not applied to any method. §7.5.4 says the metrics are "not uniquely
  correct", the thresholds need calibration, and the full protocol may cost
  too much for large studies
- **Safety applications** (§13): concept erasure, ROME-style editing,
  steering vectors and circuit monitors, each with a worked pipeline.
  Steering vectors often degrade on related tasks (Tan et al., 2024), so
  the survey treats them as a complement and not a standalone safety tool.
  Its overall verdict (§13.7.5, §15.1) is that interpretability is "one
  component of a defence-in-depth safety strategy rather than a standalone
  guarantee of safety"

## Standing in the anthology

**Filed as a map of the field, not as evidence.** It reports no
experiments. Every number in it comes from a cited paper, so nothing in
the record should be sourced to it where the primary work can be filed
instead. It is the broadest current account of mechanistic interpretability
in the reading list, and its section structure works as a gap list for the
`concept-geometry` topic.

**The title question is not answered.** The abstract asks whether
understanding how a model works makes it safer. The introduction and the
conclusion both say the assumption is "largely untested". The conclusion
then asks the question again (§15.2). What the survey shows is narrower and
still useful: which safety tasks have a mechanistic method with a result
behind it, and where the gap between explanation and control is documented.
Read the verdict as a judgement from the literature, not as a finding.

**Unsupported sentences that should not travel** ([DP-010](../principles.d/DP-010.md)). In §7.3 a
circuit "typically explains 60–80% of behavioural variance", with no
citation and no definition of the variance. §14.1 says safety training has
made backdoors harder for adversaries to implant, also uncited. The five
evaluation dimensions are a proposal, and §7.5.4 says so.

**What it does not move.** Two of its SAE recommendations repeat practices
the record already holds on primary evidence. Treating a dictionary as one
valid decomposition among several is [SOTA-310](../practices.d/SOTA-310.md), from Méloux et al.
([LIT-504](LIT-504.md)), whose enumeration found no small network with a unique circuit
explanation. Preferring supervised probes for known concepts is [SOTA-345](../practices.d/SOTA-345.md),
from Kantamneni et al. ([LIT-568](LIT-568.md)), where SAE probes added nothing over
logistic regression across 113 datasets. The survey cites Méloux et al. but
not Kantamneni et al.; its probing claim rests on Wu et al. (2025b).
Agreement from a survey is adoption, not a second test ([DP-005](../principles.d/DP-005.md)), and neither
practice's sources or consensus change.

**Candidate follow-ups.** The cross-seed instability of SAE features
("Sparse autoencoders trained on the same data learn different features",
Paulo & Belrose, ICLR 2026) supports a reporting practice the record lacks.
That paper, not this survey, is what to file first.

<!-- inactive-ok: NOTE-tmpovz7x — Skimmed, and cited to say so: the method chapters of this survey have no reading in force -->
Skimmed — [NOTE-tmpovz7x](../notes.d/NOTE-tmpovz7x.md).
