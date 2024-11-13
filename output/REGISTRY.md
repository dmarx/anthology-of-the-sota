# ML Training Recommendations Registry

Last updated: 2024-11-13

## Experimental Recommendations


## Standard Recommendations

### MoE

- [MLR-2021-Fedus001-0001] Use largest batch that maintains >80% sample efficiency
  - Source: Fedus et al. (2021)

- [MLR-2021-Fedus001-0002] Scale batch size with model size but sub-linearly
  - Source: Fedus et al. (2021)

### attention

- [MLR-2022-Dao002-0001] Use flash attention for all attention computations when hardware supports it
  - Source: Dao et al. (2022)

- [MLR-2022-Dao002-0002] Tiling size should match hardware SRAM size
  - Source: Dao et al. (2022)

- [MLR-2022-Dao002-0003] Recompute attention during backward pass instead of storing it
  - Source: Dao et al. (2022)

- [MLR-2023-Kwon001-0001] PagedAttention to accelerate batch inference for LLM sampling
  - Source: Kwon et al. (2023)

- [MLR-2023-Dao003-0001] Use flash-attention-2 over original flash-attention when available
  - Source: Dao et al. (2023)

- [MLR-2023-Dao003-0002] Keep sequence lengths multiple of 128 for best performance
  - Source: Dao et al. (2023)

- [MLR-2023-Dao003-0003] Pad attention masks to block boundaries for better hardware utilization
  - Source: Dao et al. (2023)

- [MLR-2023-Yang001-0001] Prefer GQA to MQA or MHA
  - Source: Yang et al. (2023)
  - Implementations: llama2

### attention-alternatives

- [MLR-2023-Bhardwaj001-0001] Consider for very long sequence tasks
  - Source: Bhardwaj et al. (2023)

- [MLR-2023-Bhardwaj001-0002] Use for tasks where attention bottlenecks training
  - Source: Bhardwaj et al. (2023)

- [MLR-2023-Bhardwaj001-0003] Combine with standard attention for hybrid approaches
  - Source: Bhardwaj et al. (2023)

### checkpointing

- [MLR-2021-Li003-0001] Checkpoint frequency should increase with training time
  - Source: Li et al. (2021)

- [MLR-2021-Li003-0002] Save optimizer state every N epochs (N ~ sqrt(total_epochs))
  - Source: Li et al. (2021)

- [MLR-2021-Li003-0003] Use async I/O for checkpoint writing
  - Source: Li et al. (2021)

- [MLR-2021-Li003-0004] Implement multi-level checkpoint strategy
  - Source: Li et al. (2021)

### compilation

- [MLR-2022-Anderson001-0001] Use operator fusion for small operations
  - Source: Anderson et al. (2022)

- [MLR-2022-Anderson001-0002] Optimize memory layout for hardware
  - Source: Anderson et al. (2022)

- [MLR-2022-Anderson001-0003] Implement custom kernels for critical ops
  - Source: Anderson et al. (2022)

- [MLR-2022-Anderson001-0004] Profile-guided optimization for hot paths
  - Source: Anderson et al. (2022)

### data-loading

- [MLR-2021-Johnson001-0001] Memory-map large datasets
  - Source: Johnson et al. (2021)

- [MLR-2021-Johnson001-0002] Use mixed precision during data loading
  - Source: Johnson et al. (2021)

- [MLR-2021-Johnson001-0003] Pin memory for CPU-GPU transfers
  - Source: Johnson et al. (2021)

- [MLR-2021-Johnson001-0004] Profile data loading separate from training
  - Source: Johnson et al. (2021)

- [MLR-2021-Amodei001-0001] Use tar archives for dataset storage
  - Source: Amodei et al. (2021)

- [MLR-2021-Amodei001-0002] Buffer size should be 2-3x batch size
  - Source: Amodei et al. (2021)

- [MLR-2021-Amodei001-0003] Pre-fetch next batch during compute
  - Source: Amodei et al. (2021)

- [MLR-2021-Amodei001-0004] Use multiple worker processes (num_workers = 4 * num_gpus)
  - Source: Amodei et al. (2021)

### data-quality

- [MLR-2023-Albalak001-0001] Use perplexity-based filtering for quality assessment
  - Source: Albalak et al. (2023)

- [MLR-2023-Albalak001-0002] Implement dynamic temperature scaling for mixing
  - Source: Albalak et al. (2023)

- [MLR-2023-Albalak001-0003] Adjust mixing ratios based on validation performance
  - Source: Albalak et al. (2023)

- [MLR-2023-Albalak001-0004] Monitor domain coverage during training
  - Source: Albalak et al. (2023)

### distributed-training

- [MLR-2018-Huang001-0001] Use micro-batch splitting for pipeline parallelism
  - Source: Huang et al. (2018)

- [MLR-2018-Huang001-0002] Balance pipeline stages to minimize bubble overhead
  - Source: Huang et al. (2018)

- [MLR-2018-Huang001-0003] Choose pipeline chunks based on memory vs. compute trade-off
  - Source: Huang et al. (2018)

- [MLR-2021-Jiang001-0001] Use hierarchical allreduce for tensors > 1MB
  - Source: Jiang et al. (2021)

- [MLR-2021-Jiang001-0002] Overlap communication with backward pass
  - Source: Jiang et al. (2021)

- [MLR-2021-Jiang001-0003] Group small tensors before communication
  - Source: Jiang et al. (2021)

- [MLR-2021-Jiang001-0004] Set buffer size to network bandwidth-delay product
  - Source: Jiang et al. (2021)

- [MLR-2021-Narayanan001-0001] Use sequence parallelism for attention layers
  - Source: Narayanan et al. (2021)

- [MLR-2021-Narayanan001-0002] Overlap communication with computation when possible
  - Source: Narayanan et al. (2021)

- [MLR-2021-Narayanan001-0003] Initialize layer norms with smaller variance (0.02) for stability
  - Source: Narayanan et al. (2021)

- [MLR-2021-Zhang001-0001] Monitor network utilization during training
  - Source: Zhang et al. (2021)

- [MLR-2021-Zhang001-0002] Adapt buffer sizes to network conditions
  - Source: Zhang et al. (2021)

- [MLR-2021-Zhang001-0003] Use gradient compression for slow networks
  - Source: Zhang et al. (2021)

- [MLR-2021-Zhang001-0004] Place replicas to minimize cross-rack traffic
  - Source: Zhang et al. (2021)

- [MLR-2023-Zhao001-0001] Use FSDP over DDP when model size exceeds single GPU memory
  - Source: Zhao et al. (2023)

- [MLR-2023-Zhao001-0002] Overlap communication with computation using backward prefetch
  - Source: Zhao et al. (2023)

- [MLR-2023-Zhao001-0003] Employ mixed precision to reduce memory usage
  - Source: Zhao et al. (2023)

- [MLR-2023-Zhao001-0004] Choose sharding factor based on model and GPU memory size
  - Source: Zhao et al. (2023)

### hardware-optimization

- [MLR-2022-Wang001-0001] Fuse small operations into larger kernels
  - Source: Wang et al. (2022)

- [MLR-2022-Wang001-0002] Align tensor dimensions to hardware boundaries
  - Source: Wang et al. (2022)

- [MLR-2022-Wang001-0003] Use hardware-specific memory layouts
  - Source: Wang et al. (2022)

- [MLR-2022-Wang001-0004] Profile and optimize memory access patterns
  - Source: Wang et al. (2022)

### initialization

- [MLR-2021-Kumar001-0001] Scale attention weights by 1/sqrt(head_dim)
  - Source: Kumar et al. (2021)

- [MLR-2021-Kumar001-0002] Initialize final layer weights near zero
  - Source: Kumar et al. (2021)

- [MLR-2021-Kumar001-0003] Use smaller variance for deep networks
  - Source: Kumar et al. (2021)

- [MLR-2021-Kumar001-0004] Special handling for gated architectures
  - Source: Kumar et al. (2021)

### language-models

- [MLR-2020-Gururangan001-0001] continued pre-training for fine tuning
  - Source: Gururangan et al. (2020)

- [MLR-2020-Brown001-0001] gpt training recipe
  - Source: Brown et al. (2020)

- [MLR-2020-Brown001-0002] LM in-context learning emerges at scale
  - Source: Brown et al. (2020)

- [MLR-2020-Brown001-0003] ICL permits few-shot task adaptability
  - Source: Brown et al. (2020)

- [MLR-2020-Brown001-0004] single cycle of cosine decay is sufficient lr schedule
  - Source: Brown et al. (2020)

- [MLR-2022-Chowdhery001-0001] smaller batch sizes are more sample efficient (i.e., better loss as a function of tokens seen) earlier in training
  - Source: Chowdhery et al. (2022)
  - Implementations: PaLM

- [MLR-2022-Chowdhery001-0002] larger batch sizes are beneficial later in training due to better gradient estimates
  - Source: Chowdhery et al. (2022)
  - Implementations: PaLM

- [MLR-2022-Chowdhery001-0003] throughput (energy efficiency) wins out over theoretically optimal sample efficiency
  - Source: Chowdhery et al. (2022)
  - Implementations: PaLM

- [MLR-2022-Chowdhery001-0004] consider rewinding to earlier checkpoint and skipping a few batches to mitigate unusual loss spikes
  - Source: Chowdhery et al. (2022)
  - Implementations: PaLM

### large-batch-training

- [MLR-2017-You001-0001] linear warmup of LR stabilizes early training with large batch size.
  - Source: You et al. (2017)

### memory-efficiency

- [MLR-2020-Rajbhandari001-0001] Stage optimizer states across data parallel ranks (ZeRO-1)
  - Source: Rajbhandari et al. (2020)

- [MLR-2020-Rajbhandari001-0002] Partition gradients and optimizer states (ZeRO-2) for larger models
  - Source: Rajbhandari et al. (2020)

- [MLR-2020-Rajbhandari001-0003] Use ZeRO-3 only when other strategies insufficient
  - Source: Rajbhandari et al. (2020)

- [MLR-2020-Rajbhandari001-0004] Keep micro-batch size per GPU as large as memory allows
  - Source: Rajbhandari et al. (2020)

### nlp

- [MLR-2015-Sennrich001-0001] BPE tokenization for open vocabulary tasks
  - Source: Sennrich et al. (2015)
  - Implementations: llama2

### normalization

- [MLR-2015-Ioffe001-0001] Place BatchNorm after linear/conv layers but before activation functions
  - Source: Ioffe et al. (2015)

- [MLR-2015-Ioffe001-0002] Use running statistics for inference
  - Source: Ioffe et al. (2015)

- [MLR-2015-Ioffe001-0003] Consider alternatives like LayerNorm for transformers
  - Source: Ioffe et al. (2015)

- [MLR-2018-Santurkar001-0001] Use larger learning rates with batch normalization
  - Source: Santurkar et al. (2018)

- [MLR-2018-Santurkar001-0002] Monitor loss landscape smoothness during training
  - Source: Santurkar et al. (2018)

- [MLR-2018-Santurkar001-0003] Place BN after linear/conv layers but before activation functions
  - Source: Santurkar et al. (2018)

- [MLR-2019-Xu001-0001] Initialize LayerNorm weight close to 1 (0.97-1.0)
  - Source: Xu et al. (2019)

- [MLR-2019-Xu001-0002] Initialize LayerNorm bias to 0
  - Source: Xu et al. (2019)

- [MLR-2019-Xu001-0003] Use a smaller learning rate for LayerNorm parameters
  - Source: Xu et al. (2019)

### optimization

- [MLR-2014-Kingma001-0001] Default choice for neural network training
  - Source: Kingma et al. (2014)

- [MLR-2014-Kingma001-0002] Common hyperparameters: β₁=0.9, β₂=0.999, ε=1e-8
  - Source: Kingma et al. (2014)

- [MLR-2014-Kingma001-0003] Learning rate typically 1e-4 to 1e-3 for most tasks
  - Source: Kingma et al. (2014)

- [MLR-2017-Smith001-0001] warmup to a large early lr, anneal throughout training to small final lr
  - Source: Smith et al. (2017)

- [MLR-2017-Li001-0001] skip connections promote training stability by smoothing out the loss landscape
  - Source: Li et al. (2017)

- [MLR-2017-Li001-0002] visualizing eigenvalues of hessian (ratio of largest to smallest) over training can be useful diagnostics
  - Source: Li et al. (2017)

- [MLR-2017-Li001-0003] sharpness in loss landscape corerlates with test error
  - Source: Li et al. (2017)

- [MLR-2020-Li002-0001] use gradient clipping
  - Source: Li et al. (2020)

### scaling-laws

- [MLR-2020-Kaplan001-0001] larger models are more sample efficient
  - Source: Kaplan et al. (2020)

- [MLR-2020-Kaplan001-0002] lr tuning less important for larger models
  - Source: Kaplan et al. (2020)

- [MLR-2022-Hoffmann001-0001] `num_tokens ~ 20 * num_params`
  - Source: Hoffmann et al. (2022)
  - Implementations: chinchilla, llama2

- [MLR-2022-Hoffmann001-0002] Optimal batch size scales approximately with compute budget - `B ∝ C^(1/4)`
  - Source: Hoffmann et al. (2022)
  - Implementations: chinchilla, llama2

### systems

- [MLR-2023-Chen002-0001] Use continuous batching for inference
  - Source: Chen et al. (2023)

- [MLR-2023-Chen002-0002] Fuse attention operations where possible
  - Source: Chen et al. (2023)

- [MLR-2023-Chen002-0003] Overlap prefill and decode compute
  - Source: Chen et al. (2023)

### training-dynamics

- [MLR-2021-Tay001-0001] Warmup needed scales sub-linearly with model size
  - Source: Tay et al. (2021)
  - Implementations: vision_transformer, bert

- [MLR-2021-Tay001-0002] Initialize layer norm weights closer to 1 for larger models
  - Source: Tay et al. (2021)
  - Implementations: vision_transformer, bert

- [MLR-2021-Tay001-0003] Can use shorter warmup periods for wider models
  - Source: Tay et al. (2021)
  - Implementations: vision_transformer, bert

- [MLR-2021-Tay001-0004] Monitor loss specifically during first ~5000 steps for instabilities
  - Source: Tay et al. (2021)
  - Implementations: vision_transformer, bert

- [MLR-2021-Tay001-0005] Use gradient clipping during early training phase
  - Source: Tay et al. (2021)
  - Implementations: vision_transformer, bert

- [MLR-2023-Luo001-0001] Monitor validation loss for unexpected spikes during training
  - Source: Luo et al. (2023)

- [MLR-2023-Luo001-0002] Track gradient norm statistics to detect training instabilities
  - Source: Luo et al. (2023)

- [MLR-2023-Luo001-0003] Use learning rate warmup proportional to model size
  - Source: Luo et al. (2023)

### training-efficiency

- [MLR-2017-Micikevicius001-0001] Use dynamic loss scaling that doubles every 2000 successful steps
  - Source: Micikevicius et al. (2017)

- [MLR-2017-Micikevicius001-0002] Maintain master weights in FP32
  - Source: Micikevicius et al. (2017)

- [MLR-2017-Micikevicius001-0003] Store optimizer states in FP32
  - Source: Micikevicius et al. (2017)

- [MLR-2017-Micikevicius001-0004] Perform forward/backward passes in FP16
  - Source: Micikevicius et al. (2017)

### training-stability

- [MLR-2020-Xiong001-0001] Use pre-norm (RMSNorm) for transformer layers
  - Source: Xiong et al. (2020)
  - Implementations: llama2

- [MLR-2021-Chen001-0001] Monitor exp(loss) for stability
  - Source: Chen et al. (2021)

- [MLR-2021-Chen001-0002] Track gradient norm ratios between layers
  - Source: Chen et al. (2021)

- [MLR-2021-Chen001-0003] Use gradient clipping with dynamic threshold
  - Source: Chen et al. (2021)

- [MLR-2021-Chen001-0004] Implement early warning system for NaNs
  - Source: Chen et al. (2021)

### transformers

- [MLR-2019-Dao001-0001] Use multi-query attention for decoder-only models to reduce memory bandwidth
  - Source: Dao et al. (2019)

- [MLR-2019-Dao001-0002] Keep key/value projections shared across heads while query projections remain separate
  - Source: Dao et al. (2019)

- [MLR-2020-Noam001-0001] Use SwiGLU activation for transformers
  - Source: Noam et al. (2020)
  - Implementations: llama2

- [MLR-2021-Su001-0001] use RoPE for LLM (1D sequence) positional embeddings
  - Source: Su et al. (2021)


## Deprecated Recommendations


## Statistics

### MoE

- Total recommendations: 2
- By status:
  - Experimental: 0
  - Standard: 2
  - Deprecated: 0
- Year range: 2021 - 2021

### attention

- Total recommendations: 8
- By status:
  - Experimental: 0
  - Standard: 8
  - Deprecated: 0
- Year range: 2022 - 2023

### attention-alternatives

- Total recommendations: 3
- By status:
  - Experimental: 0
  - Standard: 3
  - Deprecated: 0
- Year range: 2023 - 2023

### checkpointing

- Total recommendations: 4
- By status:
  - Experimental: 0
  - Standard: 4
  - Deprecated: 0
- Year range: 2021 - 2021

### compilation

- Total recommendations: 4
- By status:
  - Experimental: 0
  - Standard: 4
  - Deprecated: 0
- Year range: 2022 - 2022

### data-loading

- Total recommendations: 8
- By status:
  - Experimental: 0
  - Standard: 8
  - Deprecated: 0
- Year range: 2021 - 2021

### data-quality

- Total recommendations: 4
- By status:
  - Experimental: 0
  - Standard: 4
  - Deprecated: 0
- Year range: 2023 - 2023

### distributed-training

- Total recommendations: 18
- By status:
  - Experimental: 0
  - Standard: 18
  - Deprecated: 0
- Year range: 2018 - 2023

### hardware-optimization

- Total recommendations: 4
- By status:
  - Experimental: 0
  - Standard: 4
  - Deprecated: 0
- Year range: 2022 - 2022

### initialization

- Total recommendations: 4
- By status:
  - Experimental: 0
  - Standard: 4
  - Deprecated: 0
- Year range: 2021 - 2021

### language-models

- Total recommendations: 9
- By status:
  - Experimental: 0
  - Standard: 9
  - Deprecated: 0
- Year range: 2020 - 2022

### large-batch-training

- Total recommendations: 1
- By status:
  - Experimental: 0
  - Standard: 1
  - Deprecated: 0
- Year range: 2017 - 2017

### memory-efficiency

- Total recommendations: 4
- By status:
  - Experimental: 0
  - Standard: 4
  - Deprecated: 0
- Year range: 2020 - 2020

### nlp

- Total recommendations: 1
- By status:
  - Experimental: 0
  - Standard: 1
  - Deprecated: 0
- Year range: 2015 - 2015

### normalization

- Total recommendations: 9
- By status:
  - Experimental: 0
  - Standard: 9
  - Deprecated: 0
- Year range: 2015 - 2019

### optimization

- Total recommendations: 8
- By status:
  - Experimental: 0
  - Standard: 8
  - Deprecated: 0
- Year range: 2014 - 2020

### scaling-laws

- Total recommendations: 4
- By status:
  - Experimental: 0
  - Standard: 4
  - Deprecated: 0
- Year range: 2020 - 2022

### systems

- Total recommendations: 3
- By status:
  - Experimental: 0
  - Standard: 3
  - Deprecated: 0
- Year range: 2023 - 2023

### training-dynamics

- Total recommendations: 8
- By status:
  - Experimental: 0
  - Standard: 8
  - Deprecated: 0
- Year range: 2021 - 2023

### training-efficiency

- Total recommendations: 4
- By status:
  - Experimental: 0
  - Standard: 4
  - Deprecated: 0
- Year range: 2017 - 2017

### training-stability

- Total recommendations: 5
- By status:
  - Experimental: 0
  - Standard: 5
  - Deprecated: 0
- Year range: 2020 - 2021

### transformers

- Total recommendations: 4
- By status:
  - Experimental: 0
  - Standard: 4
  - Deprecated: 0
- Year range: 2019 - 2021

