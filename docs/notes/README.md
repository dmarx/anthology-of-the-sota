# NOTE documents

<!-- GENERATED below this line by `luria index` — edit README.stub instead. -->

**[Data-Pipeline](tags/data-pipeline.md)** (1):
[002](../../record/notes.d/NOTE-002.md)

**[Distributed-Optimization](tags/distributed-optimization.md)** (1):
[003](../../record/notes.d/NOTE-003.md)

**[Model-Architecture](tags/model-architecture.md)** (1):
[004](../../record/notes.d/NOTE-004.md)

**[Model-Stability](tags/model-stability.md)** (1):
[001](../../record/notes.d/NOTE-001.md)

**By status:** [Read](statuses/Read.md) (4) · [Skimmed](statuses/Skimmed.md) (0) · [Unread](statuses/Unread.md) (0) · [Re-read](statuses/Superseded.md) (0)

What the status column means in this scheme — the words are luria's, the meanings are this project's.

| Status | | Means |
|---|---|---|
| `Read` | Read | The full text, closely enough to state its assumptions and results exactly — the only status that licenses a claims table |
| `Skimmed` | Skimmed | Abstract, figures and selected sections; honest, useful, and explicitly not enough to source a practice from |
| `Unread` | Unread | The note exists to record that nobody has read this yet, which is a fact the record could not previously state |
| `Superseded` | Re-read | A later reading replaced this one, and names it |

| # | Title | Summary | Status |
|---|---|---|---|
| [NOTE-001](../../record/notes.d/NOTE-001.md) | Understanding and Improving Layer Normalization | LayerNorm's benefit is in the backward pass — the derivatives of the mean and variance re-center and re-scale the gradients — not in forward normalization. Its bias and gain increase overfitting risk and "do not work in most cases". | Read |
| [NOTE-002](../../record/notes.d/NOTE-002.md) | Efficient Online Data Mixing | An Exp3 bandit over data domains, rewarded by per-domain training loss on the batches the run is already taking, revising the mixture during training. 19% fewer iterations to the next best method's final perplexity, at negligible wall-clock cost. | Read |
| [NOTE-003](../../record/notes.d/NOTE-003.md) | PyTorch FSDP | Fully Sharded Data Parallel as an industry-grade PyTorch component: a sharding factor F generalising replication through full sharding, communication overlapped by backward prefetching, and a rate limiter over the CUDA caching allocator. The first cluster in [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114) whose practices its paper actually supports. | Read |
| [NOTE-004](../../record/notes.d/NOTE-004.md) | Scale Efficiently | Model shape, not only model size, determines downstream fine-tuning quality — and the widely adopted T5-Base and T5-Large configurations are Pareto-inefficient. Read in full for [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114) after its LIT note was found to describe a different paper. | Read |

