---
status: Active
title: 'Git-Theta: A Git Extension for Collaborative Development of Machine Learning Models'
version: 1
tags:
- adaptation-and-tuning
- distributed-optimization
date: '2026-10-01'
published: '2023-06-07'
arxiv: '2306.04529'
first_author: 'Kandpal'
keywords:
- 'version-control'
- 'git'
- 'model-checkpoint'
- 'collaborative-development'
- 'communication-efficient-updates'
- 'model-merging'
- 'locality-sensitive-hashing'
implementations:
- 'r-three/git-theta'
summary: >-
  Kandpal et al. (2023), [ARXIV-2306.04529](https://arxiv.org/abs/2306.04529) — Git-Theta, a Git extension that
  versions a checkpoint per parameter group rather than as one blob. Unchanged
  groups (detected with a locality-sensitive hash) are stored as references;
  changed groups are stored as typed updates (dense, sparse, low-rank, (IA)³)
  that are reconstructed by walking back through history. In one T0-3B
  workflow it stored 41.5 GB against Git LFS's 57.0 GB, the saving coming
  almost entirely from a LoRA commit (0.27 GB against 11.4); dense fine-tunes
  were stored nearly in full, and every add was slower than Git LFS.
---
<!-- inactive-ok-file: SOTA-tmpcasx3 — Proposed; named to say this paper is a precedent for half of it, not its origin -->

# LIT-tmpumvqf: Git-Theta: A Git Extension for Collaborative Development of Machine Learning Models

Kandpal, Lester, Muqeeth, Mascarenhas, Evans, Baskaran, Huang, Liu and
Raffel, UNC Chapel Hill (2023) — [ARXIV-2306.04529](https://arxiv.org/abs/2306.04529)

## Key takeaways

- **The unit of versioning is the parameter group, not the file.** Git's
  clean filter loads the checkpoint (PyTorch, TensorFlow or Flax), compares
  each weight matrix or bias against the previous commit, and stores only
  what changed, through Git LFS. Unchanged groups become references to the
  version that last changed them. Git then tracks a small text metadata file
  instead of the checkpoint.
- **Changes are stored as typed updates, and some are deltas.** An `Update`
  plug-in keeps "the smallest amount of information needed to describe how
  the parameter group was modified": the new values for a dense update, the
  indices and values of the non-zero difference for a sparse one, the factors
  for a low-rank one. Updates that depend on earlier values are restored by
  recursively loading previous versions until a full value is reached. There
  is no periodic full base and no bound on that chain in the paper.
- **Change detection is approximate on purpose.** A Euclidean
  locality-sensitive hash decides whether a group changed, so that
  floating-point noise across machines does not register as an edit, with
  `np.allclose` as a check near the threshold. The authors note this bounds
  parameter drift, not drift in the model's predictions.
- **Merges and diffs are per group.** `git merge` offers a menu: keep ours,
  keep theirs, keep the ancestor, or average the parameters. `git diff`
  lists which groups were added, removed or modified.
- **One benchmark workflow, against Git LFS only (Table 1).** T0-3B, then
  LoRA on CB, a fine-tune on RTE on a branch and on ANLI on main, a merge by
  averaging, and removal of the sentinel embeddings. Totals: 41.5 GB against
  57.0 GB. The LoRA commit took 0.27 GB against 11.4 GB. The dense
  fine-tunes took 10.4–10.62 GB against 11.4, and the first commit 9.6 GB;
  the authors credit that saving to TensorStore's compression and to T0-3B
  being trained in bfloat16 but shipped as float32. Git-Theta's `add` was
  3m 41s–15m 51s against Git LFS's steady 2m 22s–2m 25s, and every checkout
  was slower too. Transfer time is not measured; on-disk size stands in for it.
  One CPU machine, one workflow, no repeated runs.

## Standing in the anthology

Filed because ZipNN ([LIT-tmpbjxkg](LIT-tmpbjxkg.md)) cites it for the idea it uses for its
checkpoint half: "save a base model and for the rest of the models only store
the differences from this base model". Read against [SOTA-tmpcasx3](../practices.d/SOTA-tmpcasx3.md), Git-Theta
is the precedent for storing a model version as its difference from an
earlier one, but not the origin of the delta step that practice recommends.
Its deltas are structured: they pay off when training touched few parameters
or a low-rank subspace, and a dense fine-tune is stored almost whole, which
is the case ZipNN's XOR-and-entropy-code delta exists for. Git-Theta has no
periodic base either; it walks the whole history to restore.

Its saving rests on parameter-efficient adaptation. LoRA ([LIT-046](LIT-046.md)) is the
update type behind the one large number in Table 1. Its averaging merge is
the operation of model soups ([LIT-675](LIT-675.md)), which [SOTA-407](../practices.d/SOTA-407.md) applies between a
zero-shot and a fine-tuned model; Git-Theta supplies the plumbing for it and
measures no accuracy effect beyond one RTE figure. The record otherwise
holds nothing on versioning models or on lossless storage of them, beyond
ZipNN; [SOTA-054](../practices.d/SOTA-054.md) is about when to checkpoint, not how to store one.

Unread — no NOTE.
