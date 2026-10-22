---
status: Active
title: 'Let Your Graph Do the Talking: Encoding Structured Data for LLMs'
version: 1
tags:
- graphs-and-networks
- representation-and-encoding
- adaptation-and-tuning
- multimodal-learning
date: '2026-10-22'
published: '2024-02-08'
arxiv: '2402.05862'
first_author: 'Perozzi'
keywords:
- 'graphtoken'
- 'soft-prompt'
- 'graph-encoder'
- 'frozen-llm'
- 'graphqa'
- 'equivariance'
implementations: []
compared_against:
- LIT-tmp3l6xc
summary: >-
  Perozzi, Fatemi, Zelle, Tsitsulin, Kazemi, Al-Rfou, Halcrow (2024),
  ARXIV-2402.05862. GraphToken trains a small GNN, separately for each
  task, whose pooled output is projected into soft tokens and prepended to
  the prompt of a frozen Flan-PaLM 2 S. On GraphQA it reaches 0.996 on node
  count, 0.962 on node degree and 0.956 on cycle check, but only 0.264 on
  connected nodes. Its prompting baselines match, to the digit, Talk like a
  Graph's PaLM 62B averages over all nine text encodings, a different and
  larger model. So "up to 73 points" sets a trained encoder against prompts
  averaged over good and bad encodings. The one same-model trained
  baseline, a soft prompt with no access to the graph, scores at the
  majority rate.
---

# LIT-tmpdsg6j: Let Your Graph Do the Talking: Encoding Structured Data for LLMs

Perozzi, Fatemi, Zelle, Tsitsulin, Kazemi, Al-Rfou, Halcrow, Google Research
and Waymo (2024) — ARXIV-2402.05862

## Key takeaways

- **The method** (§3): a GNN reads the graph, with Laplacian or learned
  node-identity features. Its output is pooled per graph, per node or per
  node pair, then projected by a dense layer into a fixed number of LLM
  input embeddings placed before the question. Only the encoder is trained,
  on the answer's log-likelihood under the frozen LLM, with Lion at learning
  rate 0.05. The encoder body has 17k–199k parameters. The projection head
  has about 11M (Table 3)
- **Main result** (Table 1, GraphQA test set): node count 0.996, edge count
  0.426, cycle check 0.956, triangle counting 0.348, node degree 0.962,
  connected nodes 0.264, reachability 0.932, edge existence 0.738, shortest
  path 0.638. Each entry is the best of seven encoder architectures for that
  task, chosen on the 1,000-graph training split
- **No single encoder wins** (Table 2): MPNN is best or near-best on
  counting and degree, and MHA on edge existence. Linear set-pooling models
  win the task they directly sum: NodeSet on node count (0.996), EdgeSet on
  edge count (0.426)
- **Breaking equivariance helps** (Figure 3): learned per-node identity
  features beat Laplacian positional encodings for most encoders and tasks.
  This is shown only as differences from the soft-prompt baseline
- **Transfer of the representation** (Table 4): a kNN probe on all 11,117
  connected 8-node graphs detects bipartiteness at 95.03 from HGT trained on
  triangle counting and at 87.00 from MHA trained on cycle check. Most other
  encoder–task pairs score 50–70

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own review, 2026-10-22).
The GNN encoders it compares include GCN (LIT-582) and GIN (LIT-580). In its
Table 2, GIN is the best encoder on no task. GCN is best on connected nodes
(0.264) and ties EdgeSet on cycle check (0.964).

**Compared against Talk like a Graph** (LIT-tmp3l6xc), whose GraphQA
benchmark and prompting methods are its baselines. The zero-shot, few-shot
and CoT rows of Table 1 are identical, column for column, to the "Overall"
rows of LIT-tmp3l6xc's Table 1 (v1). Those are PaLM 62B accuracies averaged
over all nine text encodings, including the named-entity ones that fail on
counting. GraphToken itself runs on Flan-PaLM 2 S. The paper does not say
the baselines come from another model. That paper's appendix gives a closer
comparison: plain PaLM 2 S with the best text encoding per task (its Table
10). Against those numbers, GraphToken is still ahead on node count (0.996
against 89.0%), degree (0.962 against 78.4%), cycle check (0.956 against
83.6%), edge existence (0.738 against 69.4%) and edge count (0.426 against
26.6%). It is far behind on connected nodes, 0.264 against 81.6% for the
incident encoding. Those text numbers are the best of many configurations
read off the test table, so they flatter prompting, and the checkpoints
differ (plain against Flan). It is the comparison the paper needed and did
not run.

**What the headline omits.** One trained encoder per task, so it is a
supervised adapter, and the comparison to untrained prompting is not like
for like. Tasks are on small synthetic graphs. The generalization claim
rests on probes of frozen representations (§5.1), not on an LLM answering
an unseen task.

Read — NOTE-tmpasyzx.
