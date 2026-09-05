---
status: Active
title: 'For tiny specialized models, pretrain from scratch on the target SFT or reasoning data instead of pretrain-then-finetune'
version: 1
tags:
- data-pipeline
- tiny-models
date: '2026-09-05'
published: '2026-01-15'
source: LIT-119
summary: >-
  Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost. At 90M, 25% SFT data in the pretraining mix beat a separate SFT stage by 10 IFEval points and yields one checkpoint that is both base and instruct.
---

# SOTA-123: For tiny specialized models, pretrain from scratch on the target SFT or reasoning data instead of pretrain-then-finetune

## Source

Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost.

The authors' *anti-curriculum*, a departure from the three-stage recipe
([SOTA-129](SOTA-129.md)) that Olmo 3 states in the open and that its Zero-RL track varies
<!-- inactive-ok: SOTA-130 — a Proposed variation, named as the sibling -->
from the other end ([SOTA-130](SOTA-130.md)). The argument: a model's memorization window
<!-- inactive-ok: SOTA-124 — the hypothesis this recipe rests on, filed as Proposed on purpose -->
([SOTA-124](SOTA-124.md)) scales with its size, and at 90M it is about 5 GT — no larger
than an SFT mix — so the constraint that forces SFT into a short final stage
disappears, and the high-quality data can be present from the first token.

Evidence at 90M, 800 GT:

- Instruction following: a mix with 25% SFT data, trained from scratch,
  against the same base recipe followed by a tuned 10 GT SFT stage. IFEval
  50.1 vs 40.8 before DPO, 66.1 vs 53.5 after; other benchmarks within
  noise. The SFT-25% checkpoint scored as well as SFT-0% *without* the chat
  template, so it serves as both base and instruct model. An extra SFT stage
  on top of it gave no measurable gain. Mixes above 50% SFT were worse
  overall — pretraining data is still needed to develop instruction
  following.
- Reasoning: pretraining on reasoning traces alone against pretrain-then-
  reasoning-SFT. AIME24 pass@16 6/30 vs 3/30, AIME25 9/30 vs 2/30, MATH500
  0.4 vs 0.2; the from-scratch run scaled better with budget throughout.

Conditions and the cases where it did not hold: the 100M multilingual model
tied between the two strategies, which the authors attribute to SFT data
quality and to capacity; tool calling tied as well, and looked bounded by
what a 90M model can represent rather than by when it saw the data. The
recommendation is for the regime where the target data fits inside the
memorization window — tiny models, or large models with very large SFT
corpora — not a replacement for post-training in general.

## Known implementations

- Falcon-H1-Tiny-90M-Instruct, Falcon-H1-Tiny-R-0.6B, Falcon-H1-Tiny-R-90M
