---
status: Active
title: 'Learning to summarize from human feedback'
version: 1
tags:
- adaptation-and-tuning
- analysis-and-evaluation
date: '2026-09-19'
published: '2020-09-02'
arxiv: '2009.01325'
first_author: 'Stiennon'
keywords:
- 'rlhf'
- 'reward-model'
- 'summarization'
- 'rouge'
- 'human-preferences'
extends:
- LIT-tmpqljj7
implementations: []
summary: >-
  Stiennon et al. (2020), [ARXIV-2009.01325](https://arxiv.org/abs/2009.01325). The step where the preference loop
  crosses into language: human comparisons between summaries, a reward model
  fit to them, PPO against that reward. The summaries beat the human reference
  summaries, and beat much larger models fine-tuned supervised — which is the
  result that made the loop look like a general answer rather than a control
  technique.
extended_by:
- LIT-377
---

# LIT-tmp7x0k6: Learning to summarize from human feedback

Stiennon et al. (2020) — [ARXIV-2009.01325](https://arxiv.org/abs/2009.01325)

## Key takeaways

- **The loop, on text.** Collect human comparisons between candidate
  summaries, fit a reward model to predict the preferred one, fine-tune the
  policy against it with reinforcement learning. Structurally
  `LIT-tmpqljj7`'s construction with a language model as the policy
- **The models beat the human reference summaries**, on a version of the
  TL;DR Reddit dataset — and beat much larger models fine-tuned with
  supervised learning alone, which is the size-versus-post-training comparison
  `LIT-377` later ran on general instructions
- **It transfers without task-specific tuning.** The TL;DR-trained models
  produce CNN/DM news summaries nearly as good as the human reference with no
  news-specific fine-tuning, so what the reward model learned is not the
  dataset
- **Optimizing the reward model beats optimizing ROUGE, judged by humans.**
  This is the methodological half and the paper leads with it: the training
  loss and the metric are both proxies, and the paper's closing ask is that
  researchers "pay closer attention to how their training loss affects the
  model behavior they actually want"
- **The reward model generalises to datasets it was not fit on**, stated as a
  measured result rather than assumed — which is the property PPO is spending
  when it optimizes against a fixed reward model

## Standing in the anthology

**The bridge, and the reason the lineage is a lineage rather than a
resemblance.** `LIT-377` names this paper as the second half of its
methodological inheritance — Christiano introduced learning from human
preferences, and this "applied it to summarization". The author lists make
the continuity literal rather than reconstructed: Ouyang, Christiano, Lowe
and Amodei appear on both this paper and InstructGPT.

Filed with `LIT-tmpqljj7` because a two-step lineage with the middle missing
is not a lineage. This is where the loop stops being an RL control result and
becomes a language-model result, and the record's post-training documents all
sit downstream of *that* transition rather than of the original construction.

**The evaluation claim is the half the record was weakest on.** Its second
tag is not decoration: the argument that a widely-used automatic metric
disagrees with the thing it stands in for is a claim about measurement, made
by running the comparison, and it predates by years the record's own
benchmark-scepticism documents.

Unread — no `NOTE`.
