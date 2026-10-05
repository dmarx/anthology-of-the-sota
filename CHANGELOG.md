# Changelog

Assembled from `record/changelog.d/` fragments on a weekly cadence — never
hand-edited ([ADR-002](record/decisions.d/ADR-002.md)). Each contribution files a fragment; the `collect` job
in `.github/workflows/docs.yml` moves them here.

<!-- luria-insert-here -->

## 2026-10-05

### Fixed

- **[LIT-251](record/literature.d/LIT-251.md) and [NOTE-131](record/notes.d/NOTE-131.md) (Entezari et al.) misstated the paper.** The
  "no dead neurons" condition does not exist. The only theorem (3.1) is
  for one hidden layer at random initialization, and it bounds the output
  gap, not a loss barrier. The paper's own search did not lower barriers
  for VGG or ResNet. Barriers rise and then fall with width. About ten
  further claims had no basis in the text.
- **[LIT-333](record/literature.d/LIT-333.md) and [NOTE-116](record/notes.d/NOTE-116.md) (Git Re-Basin) misstated the paper.** Weight
  matching is coordinate descent over all layers, not greedy single-pass
  matching, which Appendix A.7 argues against. Merging many models uses
  MergeMany, with no anchoring. Zero barrier needs width: none at 1×
  width, and a barrier remains on ImageNet. Activation matching is the
  slower method and needs data. Several quoted figures were not in the
  paper.
- **[SOTA-217](record/practices.d/SOTA-217.md) and [THEORY-010](record/theory.d/THEORY-010.md)** repeated the activation-matching error and
  read [LIT-251](record/literature.d/LIT-251.md)'s conjecture as a finding. Both now state the width
  condition. [THEORY-010](record/theory.d/THEORY-010.md)'s promote_when now asks for the 1×-width and
  ImageNet residual to be explained.
- **[ADR-066](record/decisions.d/ADR-066.md)** kept its temporary `number:` beside the concretized one, a
  duplicate key that failed the lint on `main`.

### Added

- **Two subtopics**, `flows-and-transport` and `few-step-generation`
  ([ADR-066](record/decisions.d/ADR-066.md)). They are secondary-only words worn beside
  `generative-modeling` or `inference-optimization` and never placed first,
  so no primary topic moved. Twenty-seven existing documents were retagged.
- **Twenty flow-methods papers.** All twenty were read in full and all carry
  the new subtopics.
  - Recipes and couplings: InstaFlow ([LIT-796](record/literature.d/LIT-796.md)), Lee, Lin & Fanti's
    improved reflow ([LIT-791](record/literature.d/LIT-791.md)), minibatch-OT flow matching
    ([LIT-798](record/literature.d/LIT-798.md)), Multisample Flow Matching ([LIT-789](record/literature.d/LIT-789.md)), the Flow
    Matching Guide ([LIT-777](record/literature.d/LIT-777.md)) and Discrete Flow Matching ([LIT-792](record/literature.d/LIT-792.md)).
  - Normalizing flows and neural ODEs: RealNVP ([LIT-781](record/literature.d/LIT-781.md)), Glow
    ([LIT-771](record/literature.d/LIT-771.md)), Neural ODEs ([LIT-772](record/literature.d/LIT-772.md)), FFJORD ([LIT-780](record/literature.d/LIT-780.md)),
    TarFlow ([LIT-794](record/literature.d/LIT-794.md)) and STARFlow ([LIT-785](record/literature.d/LIT-785.md)).
  - RL post-training of flows: Flow-GRPO ([LIT-779](record/literature.d/LIT-779.md)).
  - Few-step: Shortcut Models ([LIT-787](record/literature.d/LIT-787.md)), MeanFlow ([LIT-784](record/literature.d/LIT-784.md)), Flow
    Map Matching ([LIT-793](record/literature.d/LIT-793.md)), Inductive Moment Matching ([LIT-775](record/literature.d/LIT-775.md)),
    sCM ([LIT-790](record/literature.d/LIT-790.md)), rCM ([LIT-783](record/literature.d/LIT-783.md)) and iCT ([LIT-786](record/literature.d/LIT-786.md)).
  - The older papers they extend or compare against now explain those
    relations in prose.

- **Six proposed practices from the batch.** All six are `Proposed`.
  - Robust loss for consistency and MeanFlow training ([SOTA-443](record/practices.d/SOTA-443.md),
    emerging).
  - Minibatch-OT pairing for flows sampled with a coarse solver
    ([SOTA-444](record/practices.d/SOTA-444.md), emerging).
  - Stop-gradient rather than EMA consistency targets ([SOTA-446](record/practices.d/SOTA-446.md)).
    Unreplicated: only iCT tests it.
  - Flow-GRPO's SDE rollout with a per-step KL anchor ([SOTA-442](record/practices.d/SOTA-442.md),
    unreplicated).
  - MeanFlow for teacher-free one-step generation ([SOTA-448](record/practices.d/SOTA-448.md),
    unreplicated).
  - A DMD term added to continuous-time consistency distillation
    ([SOTA-447](record/practices.d/SOTA-447.md), unreplicated).
- **DDPO** ([LIT-776](record/literature.d/LIT-776.md)) and **Diffusion-DPO** ([LIT-774](record/literature.d/LIT-774.md)), the roots of
  RL and preference tuning for diffusion models, both read in full.
  - Flow-GRPO's DPO baseline is now recorded as compared against
    Diffusion-DPO, the form it actually ran, rather than against DPO
    ([LIT-169](record/literature.d/LIT-169.md)).
  - [SOTA-145](record/practices.d/SOTA-145.md) and [SOTA-302](record/practices.d/SOTA-302.md) cite them as the earlier multi-step cases.

- **Seven theories from the batch.** Three are `Active`, where the claim
  is derived. Four are `Proposed`, where it is only illustrated.
  - [THEORY-123](record/theory.d/THEORY-123.md) (Active): a flow's ODE curves because its training
    pairs cross. A non-crossing coupling straightens it. Extends [THEORY-106](record/theory.d/THEORY-106.md).
  - [THEORY-119](record/theory.d/THEORY-119.md) (Active): consistency, shortcut, MeanFlow and progressive
    distillation all estimate the two-time flow map, and differ in which
    identity they train on.
  - [THEORY-124](record/theory.d/THEORY-124.md) (Proposed): consistency training is a bootstrapped
    fixed-point iteration, so a lagging EMA target swamps the data signal.
  - [THEORY-118](record/theory.d/THEORY-118.md) (Proposed): continuous-time consistency is unstable
    through its tangent's time derivative, which tangent normalization
    (MeanFlow's adaptive weight) controls.
  - [THEORY-121](record/theory.d/THEORY-121.md) (Proposed): distribution-matching distillation loses
    coverage through a reverse divergence on the student's own samples.
  - [THEORY-122](record/theory.d/THEORY-122.md) (Active): policy-gradient RL needs a stochastic sampler
    with a tractable per-step density. A same-marginal SDE supplies one.
  - [THEORY-120](record/theory.d/THEORY-120.md) (Proposed): a likelihood-trained normalizing flow
    samples well only with training noise well above the quantization
    width.

- **Six more reward- and preference-tuning papers**, all read in full:
  - Lee et al.'s reward-weighted alignment ([LIT-797](record/literature.d/LIT-797.md)).
  - DPOK ([LIT-778](record/literature.d/LIT-778.md)).
  - ImageReward and ReFL ([LIT-788](record/literature.d/LIT-788.md)).
  - Pick-a-Pic and PickScore ([LIT-782](record/literature.d/LIT-782.md)).
  - The Flow-DPO video paper ([LIT-773](record/literature.d/LIT-773.md)), which finds Diffusion-DPO's
    loss carried over exactly lets text alignment fall, and a constant β
    fixes it.
  - Gao et al. on reward-model over-optimization ([LIT-795](record/literature.d/LIT-795.md)), whose KL
    penalty acted like early stopping. Flow-GRPO argues against that
    without citing it, and the two now meet in its note, in [SOTA-302](record/practices.d/SOTA-302.md) and
    in [SOTA-442](record/practices.d/SOTA-442.md).
- **[THEORY-125](record/theory.d/THEORY-125.md)** (Proposed): one affine autoregressive flow block
  cannot be universal. STARFlow proves that half. Its "two or three
  blocks are enough" half is a sketch.
- **Two proposed practices from DDPO and Diffusion-DPO**, both
  unreplicated:
  - Train the guided prediction at a fixed weight when reward-tuning a
    classifier-free-guided model ([SOTA-449](record/practices.d/SOTA-449.md)).
  - Prefer Diffusion-DPO over fine-tuning on the winners when the base
    model beats the data's generators ([SOTA-445](record/practices.d/SOTA-445.md)).

### Changed

- [SOTA-206](record/practices.d/SOTA-206.md) moved from emerging to converged consensus, on the owner's
  decision. Three groups outside the source's line now serve one model at
  several step counts.

- [SOTA-392](record/practices.d/SOTA-392.md) (distil rather than reflow) is now `contested` by InstaFlow. At
  Stable Diffusion scale with a curved teacher and an LPIPS distiller,
  reflow then distillation beats distilling directly. The Conditions narrow
  the practice to a teacher that is already a rectified flow.
- [SOTA-204](record/practices.d/SOTA-204.md) (doubling discretisation curriculum) is now `contested` by sCM.
  sCM's continuous-time model removes the step count instead of scheduling
  it.
- New evidence or narrower conditions, with no change to recommendation or
  status:
  - [SOTA-266](record/practices.d/SOTA-266.md): straight path ahead of VP from a non-source group; the
    logit-normal half does not carry to reflow.
  - [SOTA-265](record/practices.d/SOTA-265.md) and [SOTA-145](record/practices.d/SOTA-145.md): Flow-GRPO tunes the SDE coefficient and runs
    GRPO's group baseline on an image model.
  - [SOTA-187](record/practices.d/SOTA-187.md): STARFlow puts a normalizing flow in latent space.
  - [SOTA-206](record/practices.d/SOTA-206.md): five new step-count-flexible models.
  - [SOTA-289](record/practices.d/SOTA-289.md), [SOTA-302](record/practices.d/SOTA-302.md) and [SOTA-394](record/practices.d/SOTA-394.md): their mechanisms or diversity
    conditions are refined.
- Rectified Flow ([LIT-636](record/literature.d/LIT-636.md)) no longer lists InstaFlow among its
  implementations. InstaFlow now `extends` it.

### Fixed

- sCM's Fig. 7 was described as comparing one-step VSD only with two-step
  sCD, with guidance as a confound. The figure also plots one-step sCD. At
  guidance 1.0 its recall is about 0.70 against VSD's 0.65, and the
  summed-loss arm tracks VSD. [LIT-790](record/literature.d/LIT-790.md), [LIT-643](record/literature.d/LIT-643.md), [SOTA-394](record/practices.d/SOTA-394.md) and
  [SOTA-447](record/practices.d/SOTA-447.md) now say so.
- sCM's takeaway said tangent warmup improves FID. Fig. 5a shows that
  normalization and clipping do, and the paper's "does not affect sample
  quality" sentence is read as being about warmup.
- Step-Video ([LIT-624](record/literature.d/LIT-624.md)) and [NOTE-338](record/notes.d/NOTE-338.md) now cite Diffusion-DPO by code, and
  Step-Video `extends` it.

### Added

- **DMAD** ([LIT-770](record/literature.d/LIT-770.md)), "Distribution Matching as Adversarial
  Distillation" (2026), read in full. It extends DMD ([LIT-643](record/literature.d/LIT-643.md)) by
  estimating the distribution-matching gradient from discriminator logits
  instead of a fitted fake score, and is compared against DMD2 ([LIT-646](record/literature.d/LIT-646.md))
  and its EDM, SDXL and Wan2.1 teachers. The equivalence proof holds only at
  the discriminator optimum, the real-data head carries most of the gain,
  and several headline comparisons use copied rows or longer budgets.
  EDM, Consistency Models, SDXL, Wan2.1 and DMD2 now say in prose how DMAD
  uses them.

### Changed

- [SOTA-337](record/practices.d/SOTA-337.md) v4, [SOTA-338](record/practices.d/SOTA-338.md) v2 and [SOTA-392](record/practices.d/SOTA-392.md) v2 note DMAD as adoption, not
  evidence: its best ImageNet-64 FID comes from an ImageNet-pretrained
  projected discriminator and is reported in FID alone ([SOTA-337](record/practices.d/SOTA-337.md), [SOTA-338](record/practices.d/SOTA-338.md)),
  and it distils the rectified-flow Wan2.1 without reflow ([SOTA-392](record/practices.d/SOTA-392.md)).
  Recommendations, statuses and consensus are unchanged.

### Added

- **A theory can be contested** ([ADR-065](record/decisions.d/ADR-065.md)). THEORY gains `contested_by`
  (a paper whose evidence disputes the account, as on SOTA) and `rivals` (a
  competing account of the same phenomenon, symmetric). [THEORY-070](record/theory.d/THEORY-070.md)'s
  `corrects` on the two weight-norm grokking accounts becomes `rivals`, as its
  own `promote_when` already said; [THEORY-071](record/theory.d/THEORY-071.md) and [THEORY-072](record/theory.d/THEORY-072.md) are contested by
  [LIT-537](record/literature.d/LIT-537.md), [THEORY-024](record/theory.d/THEORY-024.md) by [LIT-456](record/literature.d/LIT-456.md) and rivalled by [THEORY-033](record/theory.d/THEORY-033.md), and the separator
  theory is contested by [LIT-414](record/literature.d/LIT-414.md).
- **Six origin papers** behind the practices filed from the [#180](https://github.com/dmarx/anthology-of-the-sota/issues/180) papers:
  Promptagator, Net2Net, bert2BERT, the Set Transformer, Git-Theta and
  Wonderland. Promptagator ran the self-consistency filter before E5, so
  [SOTA-441](record/practices.d/SOTA-441.md)'s `introduced_by` now names it. The other five are lineage
  and precedent, not origin, and each practice now says why in its body.
  Scaling Smart now `extends` Net2Net and bert2BERT, and Lyra is
  `compared_against` Wonderland.

### Fixed

- **[SOTA-011](record/practices.d/SOTA-011.md) understated what a Hessian-vector product costs.** It said
  "roughly a forward-backward pass"; [LIT-746](record/literature.d/LIT-746.md) measured 4.5–5.5 gradients
  of time and 3–4.5× the memory in PyTorch. Corrected at version 3; the
  practice's conclusion, a diagnostic run at intervals, stands.
- **Promptagator is now a source of the self-consistency filter practice**,
  not only its origin: its with-and-without comparison is the evidence that
  the filter helps on average and hurts on the smallest datasets.

### Added

- **Four topics: `agents-and-environments`, `graphs-and-networks`,
  `physical-sciences` and `human-ai-interaction`** ([ADR-064](record/decisions.d/ADR-064.md)). The [#180](https://github.com/dmarx/anthology-of-the-sota/issues/180)
  pass declined three papers and filed four under the nearest wrong word,
  each naming the gap. The vocabulary goes from twenty-two to twenty-six,
  existing GNN, interface and physical-science documents take the new words,
  and the three declined papers are filed.
- **Six Proposed practices and two Proposed theories** from the [#180](https://github.com/dmarx/anthology-of-the-sota/issues/180) papers,
  each sourced to its paper with the limits stated and a `promote_when`
  naming the evidence that would settle it: E5's self-consistency filter,
  symmetric width expansion from a smaller pretrained model, lossless
  exponent-stream checkpoint compression, latent-bottleneck cross-attention,
  testing a KFAC implementation against its exact cases, and supervising a 3D
  reconstructor with a video model's renderings; low rank rather than small
  norm as gradient descent's implicit bias, and separators as summaries of
  their segment, set against the record's no-op reading.
- **Not filed: the role-play superposition reading.** Its paper runs no
  experiment and declines the representational claim, and nothing in the
  record evidences it.

### Added

- **Twenty-one papers from the reading feed's revisit list ([#180](https://github.com/dmarx/anthology-of-the-sota/issues/180)).** The
  worklist was recomputed from the papers-feed snapshot of 30 September:
  papers opened on three or more separate days and absent from the record.
  Each was read, and each note says how it bears on what the record holds.
  Among them: KFAC from scratch, curvature operators, dynamical mean-field
  theory for SGD and SGD's preference for flat minima; notions of rank, the
  Semanticist tokenizer, and two formal papers (synaptic field theory,
  decomposing transducers); the Perceiver, Erwin, SepLLM and Lyra; small-model
  initialization, ZipNN, Parallel Evoformer and SigLIP 2; E5, role-play with
  LLMs, Textoshop, the influencers position paper, and the scaffold-flow
  account of generalization.
- **ZipNN and the context-content paper are also held in nucleation**, each
  read there for a question of its own; the two records' notes name each
  other once both have permanent codes.
- **Converse comparisons explained** on [LIT-191](record/literature.d/LIT-191.md), [LIT-496](record/literature.d/LIT-496.md), [LIT-497](record/literature.d/LIT-497.md), [LIT-583](record/literature.d/LIT-583.md),
  [LIT-587](record/literature.d/LIT-587.md), [LIT-590](record/literature.d/LIT-590.md) and [LIT-605](record/literature.d/LIT-605.md), where the new notes ran them as baselines.

### Fixed

- **Relations the reading found wrong are corrected, from the papers.** The
  [#395](https://github.com/dmarx/anthology-of-the-sota/issues/395) pass left 39 relations unexplained because, on reading, they were
  false. Each was checked against the paper and fixed:
  - **`compared_against` removed where nobody ran the comparison**: 19 pairs,
    both sides of each, including sibling readings of one paper, analogies,
    and clauses of one PaLM sentence. The field records a measurement.
  - **Wrong sources replaced**: sequence parallelism, communication overlap
    and the 0.02 / `1/sqrt(2N)` initialisation are no longer sourced to a
    paper that never mentions them; pinned memory now rests on a
    measurement; the batch-size rules rest on McCandlish, Kaplan and
    Shallue rather than a paper that borrowed GPT-3's settings.
  - **Wrong origins repointed or emptied under [ADR-053](record/decisions.d/ADR-053.md)**, among them
    LayerNorm to Ba et al., single-cycle cosine to SGDR, the batch ramp to
    McCandlish, the SFT-free RL path to R1-Zero, and staged context length
    to BERT, with Shortformer as its controlled test.
  - **Two practices said more than their source.** [SOTA-094](record/practices.d/SOTA-094.md) no longer
    claims PaLM ranks throughput over sample efficiency, and [SOTA-098](record/practices.d/SOTA-098.md)
    watches the training loss PaLM reports rather than a validation loss
    it never mentions.

- **Claims in notes that disagreed with their papers are corrected.** These
  include SWAN's converted-model scores (swapped), xPos's ALiBi-versus-RoPE
  gap (its prose contradicts its own table), SmoothQuant's 52B result,
  MAE's mask-ratio sweep, the Olfati-Saber–Murray theorems, PowLU's
  SwiGLU-Clip arm (7.9B only), mHC's overhead (27B only), FSDP's two
  ablations, and which activations compress in Saxe et al.'s averages.

- **Seven papers filed** because a correction needed them: Korthikanti et
  al. 2022, CoCoNet, GPT-2, Shortformer, the TensorFlow white paper, 10Cache,
  and Ziegler et al. 2019.

### Changed

- **915 relations explained from reading.** Of the 954 relations that
  [ADR-063](record/decisions.d/ADR-063.md) v2 reported unexplained, 915 now have a passage in the holding
  document saying what the paper showed, measured or contributed: the
  numbers behind a practice, the experiment behind a theory, the result of a
  comparison, what an extension took and what it added. Each was written
  from the paper's note, its close reading where there is one, and the
  paper itself where neither said enough.

- **39 relations were read and judged wrong, and are left unexplained.**
  The prose was not written because the relation is the defect: sources
  that never make the claim (sequence parallelism, overlap and
  initialisation attributed to the PTD-P paper; pinned memory to CoorDL;
  validation-loss monitoring to PaLM), origins credited to a paper that
  cites an earlier one, and `compared_against` links between documents
  nobody ever measured against each other. 29 of them still warn. The other
  10 are `introduced_by` fields whose paper is also the `source`, so the new
  source passage clears the check, and the field still needs correcting.

### Changed

- **Luria 0.33.2 → 0.33.3: the `## Source` line no longer counts as an
  explanation.** A reference entry (`Kingma et al. (2014), LIT-001 —
  ARXIV-1412.6980.`) names a paper and says nothing about it. Half the
  evidence relations had been satisfied by it alone. They are now reported:
  590 relations, each naming the entry's line ([ADR-063](record/decisions.d/ADR-063.md) v2).

- **`compared_against` and `LIT.extends` must be explained in prose too.**
  What a comparison showed and what an extension added are what a reader
  cannot get from frontmatter. 364 relations are reported.

  The 954 warnings in total are a backlog to work down while reading, not a
  build failure.

### Fixed

- **Zucchet et al. 2025 ([LIT-450](record/literature.d/LIT-450.md), [NOTE-199](record/notes.d/NOTE-199.md)), corrected against the paper.**
  A re-reading done for the sibling nucleation record found these errors:
  - The "optimal imbalance exponent between 1 and 2" is not in the paper.
    The sweep covers α ∈ [0, 1]. The plateau-minimising α is 0.6–0.8 at every
    population size; the final-loss-minimising α grows with population.
  - The tested curriculum is a uniform warm-up on a subset of individuals,
    not a flattening imbalance schedule.
  - The most/least-common frequency effects are the paper's argument, not
    measurements.
  - Plateau growth is sublinear (0.43·N^0.81).
  - Only Fig. 2 is multi-seed.
  - Fine-tuning corrupts memories only for new individuals; rare individuals
    already seen in pre-training improve.
- **[SOTA-267](record/practices.d/SOTA-267.md), which rests on it, now recommends what was tested:** warm up
  on a subset of the entities before training on all of them. It stays
  `Proposed`, now stated as single-seed. [THEORY-028](record/theory.d/THEORY-028.md)'s "near-linear" plateau
  is corrected.
- **Saxe et al. 2018 ([LIT-509](record/literature.d/LIT-509.md), [NOTE-253](record/notes.d/NOTE-253.md)), corrected against the paper.**
  - There is an open route: co-author Kolchinsky's page links both PDFs.
  - `published:` is 2018-02-15, not the conference start.
  - The "three independent estimators" claim is qualified: Kraskov measures
    H(T) only, and MNIST is a single run.
  - "Exact" linear mutual information holds only given the imposed noise.
  - Fig. 15's small tanh layers compress late.
  - App. I's explanation of the gradient-SNR transition is added, with the
    transition's earlier names.
  - How the JSTAT version differs from the ICLR one is recorded.
  - [SOTA-312](record/practices.d/SOTA-312.md)'s machine-precision row is corrected to match.

### Fixed

- **184 broken links in the curation journal and one changelog fragment.**
  These were written relative to the source file (`../../../../literature.d/LIT-019.md`),
  but journal entries render into `docs/curation/2026-09.md`, and from there
  every one of those paths pointed above the repository. `luria link --fix`
  leaves a hand-written link alone. So each became a bare code again, and the
  fixer spelled it for the frame where it renders.

- **The weekly changelog collection runs again.** `CHANGELOG.md` never
  existed, so `luria collect` died on the missing file at every scheduled
  run, and 363 fragments piled up in `record/changelog.d/`. The file now
  exists with its insert marker. The next collection assembles the backlog;
  a trial run on a copy produced a changelog that passes the lint.

- **`LIT-181` passes the source check again.** arXiv's v2 retitled the paper
  "Spectral-Sphere-Constrained Hyper-Connections", dropping v1's "Beyond the
  Birkhoff Polytope:" prefix, which the record carries. That failed
  `source-mismatch` on every branch. It is acknowledged with `source-ok:`,
  which is the documented case for a title changed between versions.

### Changed

- **Luria 0.31.0 → 0.33.2.** `luria lint` now lists every site of a retired
  or unresolved citation under its row, so `docs/reports/reference-status.md`
  is no longer the only place to find them.

- **Ten relations must now be explained in the prose that holds them**
  ([ADR-063](record/decisions.d/ADR-063.md)). These are a practice's and a theory's evidence, a practice's
  origin, a theory's `explains`, every `corrects`, `contested_by`, and
  `extends` on practices and theories. Each code these fields hold must be
  cited somewhere in the body (`explain: cited`); a code the prose never
  mentions is reported. 23 citations that had been written as backticked
  mentions became real ones.

### Added

- **Prose for 58 relations the bodies never mentioned.** These are sources a
  practice named and never discussed, theories that never said which practice
  they explain, and corrections that never said what was wrong.

### Fixed

- **`LIT-655` passes the source check again.** arXiv now returns its title
  with the bound in TeX (`$O(n^2)$`), which no longer matches the record's
  rendered `O(n²)`, and `source-mismatch` fails the build. It is the same
  title, so it is acknowledged with `source-ok:` rather than rewritten.

### Added

- **Grad-CAM: Visual Explanations from Deep Networks via Gradient-based
  Localization** — `LIT-732`. Selvaraju, Cogswell, Das, Vedantam, Parikh
  and Batra (2016; ICCV 2017, IJCV 2019), `1610.02391`. **Eight live documents
  cited it before the record held it** — `LIT-563`, `LIT-713`, `LIT-724`,
  `LIT-727`, `LIT-729`, `NOTE-365`, `SOTA-430` and `THEORY-113` — and it is the
  referent behind *both* halves of `SOTA-430`'s verdict table.

  **GradCAM and Guided GradCAM are one paper, and the second is a product of
  the first with guided backpropagation** (§3.2, element-wise, after bilinear
  upsampling from 14×14). So the row `SOTA-430` reports as passing the
  parameter-randomization test and the row it reports as failing differ by one
  factor, and all the fine structure a reader sees in a Guided GradCAM image
  comes from the failing one.

  Also carried: Grad-CAM's definition and the proof that it generalizes CAM
  without CAM's architecture change (which costs 2.98 points of top-1
  classification); ILSVRC-15 top-1 localization error 56.51 for VGG-16 with
  classification untouched; PASCAL VOC 2012 weakly-supervised segmentation IoU
  44.6 → 49.6 when Grad-CAM replaces CAM as SEC's seed; the ablation table in
  which the deconvnet's ReLU rule costs 24 points of localization error inside
  Grad-CAM (83.95 against 59.65); and the doctor-versus-nurse case where a map
  diagnosed a gender-stereotyped classifier and rebalancing took test accuracy
  from 82% to 90%.

### Changed

- **`SOTA-430` v8 — both verdict rows have a subject, and the negative half has
  a number older than the practice.** Its source's human study — 90
  image-category pairs, 9 ratings each — asked which of two annotated classes a
  visualization depicts: Guided Backpropagation **44.44%**, Deconvolution
  53.33%, Deconvolution Grad-CAM 60.37%, Guided Grad-CAM 61.23%. **The method
  everyone found most convincing to look at is last.** Those four numbers are in
  arXiv v1, 7 October 2016; the sentence reading them — that Deconvolution is
  "more class-discriminative … although Guided Backpropagation is more
  aesthetically pleasing" — is in v4, 3 December 2019, fourteen months after
  `LIT-713` made the point another way. The practice also gains the figures
  behind its own "passing is not a certificate": GradCAM passes both tests and
  agrees with occlusion maps at rank correlation 0.254, with human attention on
  VQA at 0.136. Recommendation, status and consensus unchanged.

- **`NOTE-365` v3 — three of the four referents it named as missing are held,
  in two documents.** GradCAM and Guided GradCAM being one paper is why its
  claims C1 and C2 sit one factor apart rather than being independent findings.
  Only the plain gradient (`1312.6034`) is still unheld. The reading also now
  records that its own paper's bibliography cites the November 2016 workshop
  note `1611.07450` for GradCAM, not `1610.02391`.

- **`LIT-727` v4 and `LIT-728` v2 — the guided-backprop and deconvnet notes gain
  a third-party measurement of their rules.** Grad-CAM's Table 3 substitutes
  each into its own backward pass: guided ReLU is roughly neutral for
  localization (59.14 against 59.65) while costing class-discriminativeness;
  deconv ReLU loses 24 points. `LIT-728` also gains one of the three things its
  limitations section said its occlusion validation lacked — Grad-CAM turned its
  grey-square occlusion test into a rank-correlation reference over 2510 images,
  in 2016 and in the accepting direction. Still no threshold, and still no
  baseline for what an unfaithful map would score.

- **`LIT-563`** now names the document behind "a Grad-CAM adaptation", so the
  instrument it uses to say what FID looks at resolves.

### Measured, not closed

**No practice and no theory, deliberately.** The composition point — that a map
passing the randomization test, multiplied by one that fails, yields a failing
map whose visible structure is the failing factor's — is a consequence of a
definition and two verdicts, and **nobody published it**. `LIT-713` states the
construction in a subordinate clause and draws nothing from it; Grad-CAM's
authors state it as a rendering improvement. A `THEORY` needs a `source:`, and
filing this one would mean filing the record's own reading as a paper's
argument. It is stated in `SOTA-430`'s prose instead, marked as a derivation.

Grad-CAM's own rankings are also not `ADR-011` comparisons for recommending
Grad-CAM: the authors are comparing their method against alternatives. Two of
its results survive that discount because they cut across the authors' interest
— Deconvolution beating Guided Backprop, neither being theirs, and Grad-CAM's
own agreement figures being low in absolute terms.

### Changed

- **`SOTA-430` v7 — its summary, which the six amendments above never read.**
  "The evidence is image classifiers only" was true at v1 and **false from v2**,
  when `LIT-724` supplied a BERT text classifier and the practice gained a
  Condition saying the verdict does not transfer from image to text. The same
  field credited one source where `source:` has named two since that
  amendment.

  The index renders `summary:`, which makes it the most-read line in a
  document and the only one an amendment never touches.

- **Its negative half now rests on three groups and a mechanism** rather than on
  one paper's phrasing. Guided Backprop surviving randomization above the lowest
  layers is measured by `LIT-713` (Inception, MNIST), `LIT-724` (Inception,
  BERT) and `LIT-729` (VGG-16, ResNet-50), each by a similarity curve. And the
  edge-detector comparison has `THEORY-115` behind it: partial image recovery is
  what an edge detector approximates.

  The reading caveat is stated where a reader of the practice will see it rather
  than only in `LIT-713`: that paper's published Figure 2 for Guided Backprop is
  wrong, `LIT-729`'s authors confirmed the implementation bug, and footnote 5
  withdrew the stronger "entirely invariant" claim.

### Measured, not closed

**A correction of my own reporting, not of the practice.** Three earlier units
described this example as "leaning on a figure both Adebayo and Sixt amended" and
called it the practice's oldest outstanding defect. Re-reading shows the practice
was correctly scoped throughout — summary, verdict table and negative half all
state the narrowed *above the lowest layers* claim, never the withdrawn one.
**The defect was smaller than three reports of it said**, and each report was
written from memory of the document rather than from it. Same shape as the three
paper-content errors this week, with the sign reversed: a flaw asserted about a
document that did not have it.

**The sweep that found the real one.** Twelve documents were amended today; their
summaries were read against their bodies, and **one was stale**. That is the
yield, and it is worth recording as a rate rather than as a failure: an
amendment leaves the summary alone about one time in twelve, and when it does the
consequence lands in the index.

Filed as luria `LU-#326`: warn when a `history:` entry is added and `summary:` is
byte-identical. The document changed enough to earn a version and its most-read
line was not looked at. Cheap, mechanical, and the same shape as `LU-#325` —
move a check the prose asks a human to remember into the tool.

### Added

- **SmoothGrad: removing noise by adding noise** — `LIT-731`. Smilkov,
  Thorat, Kim, Viégas and Wattenberg (2017), `1706.03825`. **Eight held
  documents named it and none held it.**

  **The method and its numbers.** Average the vanilla gradient over `n` copies of
  the input perturbed with `N(0, σ²)`. **10–20%** noise, expressed as
  `σ/(x_max − x_min)`, and **`n ≈ 50`**, past which "there was little apparent
  change". Inception on ImageNet, with MNIST in the appendix, and the caveat that
  "the ideal noise level depends on the input".

  **Its evidence is entirely qualitative and it says so:** "since quantitative
  evaluation of a map remains an unsolved problem, we again focus on qualitative
  evaluation." Both assessments — visual coherence and discriminativity — are
  judged by eye.

  **It asked a question the record answered yesterday.** "It remains an open
  question to understand … why Guided BackProp seems to show the weakest
  discriminativity." `LIT-730` answers it: guided backprop is doing partial image
  recovery, which is class-insensitive by construction. Question and answer filed
  in consecutive units, in reverse order.

### Changed

- **`THEORY-113` v4 — the account has a 2017 antecedent, in a section about
  colour scales.** Its history in the record ran: `LIT-713` (2018) suspects the
  input multiplier and says it does not measure it; `LIT-725` (2021) measures it.
  §3.1 of the new note says it informally first — multiplying by the input "does
  tend to produce visually simpler and sharper images, although it can be unclear
  how much of this can be attributed to sharpness in the original image itself …
  a black/white edge in the input can lead to an edge-like structure on the final
  visualization **even if the underlying sensitivity map has no edges**."

  Filed as advice about heatmap rendering rather than as a claim about
  faithfulness, which is why nobody cites it for mechanism and why the record
  rebuilt the account from the 2021 measurement. The account is unchanged; who
  first wrote it down is not.

  It also adds a structural objection the record had from nobody: under
  gradient⊙input "pixels with values of 0 will never show up", so a correctly
  classified black ball on white is never highlighted if black encodes zero.

- **`SOTA-435` v2 — step 3's smoothing gains its parameters and their
  provenance**, which is the weakest thing in the step and now says so. The
  10–20% and `n ≈ 50` were chosen by looking at pictures. **This step's case for
  smoothing rests on `LIT-725`'s Theorem 4.1 and its measured improvement in
  infidelity and max-sensitivity, not on those figures** — so the recommendation
  survives its own technique's source being qualitative. Recommendation, status
  and consensus unchanged.

### Measured, not closed

**The one method in this cluster that nothing faults is the one with the least
evidence behind it.** SmoothGrad passes both randomization tests (`LIT-713`),
carries no input multiplier (`THEORY-113`), does not converge to rank 1
(`THEORY-114`), and is not doing image recovery (`LIT-730`). Its own paper reports
no quantitative result at all.

That is not a contradiction in the record, and the reason is worth stating: the
practice that recommends smoothing is sourced to the paper that supplied
**numbers** two years later rather than to the paper that supplied the
**method**. The right way round, and not deliberate.

**§3.1's other lesson is unheld and worth a line.** Cap gradients at the 99th
percentile, because a few far-above-average pixels "have the potential to throw
off color scales completely" and without it "maps may end up almost entirely
black". A display artefact that can be mistaken for a finding, and the record
holds nothing on it.

**No practice and no theory.** The parameters belong on `SOTA-435`, which already
recommends the smoothing, rather than in a second practice about one technique —
the call `LIT-728` got for occlusion sensitivity. And the paper offers no
mechanism for why averaging over noise sharpens a map.

Three `#290` reversals remain — Grad-CAM, InputXGradient, plain-gradient
saliency — and all three are now plainly referent gaps: every verdict about them
is stated correctly from `LIT-713`, and all three sit inside accounts the record
now holds.

### Added

- **A Theoretical Explanation for Perplexing Behaviors of
  Backpropagation-based Visualizations** — `LIT-730`. Nie, Zhang and Patel
  (2018), `1805.07039`, ICML 2018. The attribution cluster's last mechanism gap,
  named by identifier in five held documents.

  **Theorem 1.** In a **random** three-layer CNN with enough filters,
  `s_k^GBP(x) ≈ x` — guided backpropagation recovers the input, with untrained
  i.i.d. Gaussian weights and regardless of the class label. **Theorem 2:** the
  saliency map and DeconvNet in the same network are `N(0, I)`. So neither the
  plain gradient nor the backward ReLU alone produces a recognisable map; the
  combination in GBP does.

  **The second cause is structural and quantified.** Filters needed scale as
  `Õ(p/ε²)` in the filter size `p`, so a 3×3×3 filter needs at most `O(10³)` for
  error under 0.1. Small filters are what local connectivity means, and small
  filters are what make the recovery cheap.

  **In a trained network the weights do something, and it is not class
  selection:** they "control which image patch could form an active path to the
  class logit. More importantly, this filtering process is not class sensitive
  (e.g. the edge detector)."

- **`THEORY-115`**, **`Active`** — guided backprop and DeconvNet do
  **partial image recovery**, not attribution. Four arms, two of them
  architectural surgery and one running opposite to every randomization test in
  the cluster:

  | arm | prediction | result |
  | --- | --- | --- |
  | random CNN | GBP recovers; saliency and DeconvNet do not | Theorems 1–2, Figure 4 |
  | **remove local connections** | GBP fails too | all noise in an FCN; `N_h = 70000`, "definitely unrealistic", still under a CNN with `N = 64` |
  | **add max-pooling** | only DeconvNet moves | GBP and saliency unaffected; DeconvNet noise → interpretable |
  | **adversarial attack** (FGSM panda → "busby", VGG-16) | class-sensitive maps change, recovery maps do not | saliency "changes significantly"; GBP and DeconvNet "remain almost unchanged" |

  The adversarial arm is the mirror of a randomization test — hold the input and
  destroy the weights, or hold the weights and flip the class — and the account
  survives both.

### Changed

Five documents each carried a partition row reading "not held — `1805.07039`".
All five are updated.

- **`SOTA-430` v6 — the partition completes and the practice's own negative half
  gets its mechanism.** Its headline failure is guided backprop's maps surviving
  weight randomization; the map was never about the weights. And its
  do-not-validate-by-eye argument rests on "an untrained edge detector produces
  maps strikingly similar to several methods'" — partial image recovery is what
  an edge detector approximates, so that comparison was the mechanism all along.
  Recommendation, status and consensus unchanged.

- **`LIT-727` v3 — the question it declined to answer, answered in the direction
  it declined to assert.** v1 quoted Springenberg's "the bottom-up signal in form
  of the pattern of bottom ReLU activations substitutes the switches" and refused
  to conclude the map's structure comes from the input, because bottom ReLU
  activations are themselves computed by the network. **Theorem 1 removes that
  objection by making the network random.** The restraint was right about the
  argument; the conclusion is true for a reason that sentence does not contain.

- **`THEORY-113` v3, `THEORY-114` v2, `LIT-729` v2** — one table cell each, plus
  the note that this account is as far from the other two as they are from each
  other: guided backprop recovers the input in a *random* CNN, where a
  converging non-negative chain would need trained weights to have collapsed at
  all.

- **`LIT-729` also records a clash that is not one.** It says class insensitivity
  "is not caused by missing ReLU masks and Pooling switches"; the new paper finds
  max-pooling switches are exactly what turn DeconvNet's output from noise into a
  recognisable image. Checked rather than assumed: the first rejects Gu et al.'s
  account for the `z⁺` family, and the second's switches produce *recovery*,
  which is why DeconvNet is insensitive rather than a rival cause of it.

### Measured, not closed

**A "not held" row copied into four documents in one unit went stale in the
next.** Yesterday's partition table was written into `SOTA-430`, `LIT-729`,
`THEORY-113` and `THEORY-114` to make the boundary legible from every document in
the cluster. It was legible, and it was also four copies of a gap sentence — the
shape this journal has recorded having roughly a one-unit half-life, now observed
at scale. Nothing reports a stale table cell; `luria lint` checks relations
between documents, and "not held" is a claim about the absence of one.

### Added

- **When Explanations Lie: Why Many Modified BP Attributions Fail** —
  `LIT-729`. Sixt, Granz and Landgraf (2019), `1912.09818`, ICML 2020.

  **Theorem 1.** A backpropagation rule that keeps only non-negative relevance —
  the `z⁺`-rule behind Deep Taylor Decomposition, LRP-α1β0 and Excitation BP —
  gives a product of non-negative matrices, and such a product converges to a
  **rank-1** matrix. Write it `C = c γᵀ`; then `C v = c γᵀ v = λ c` for every
  `v`. The relevance vector set at the output, which is what carries the class
  being explained, survives only as a scalar and can at most flip the map's
  sign.

  **So class-insensitivity and independence of the later layers' weights are one
  mechanism, not two coincidences.** Random logit: converging methods give
  "almost identical saliency maps, independently of the output logit (SSIM very
  close to 1)" against 0.4–0.8 for the rest. Cascading randomization: the same
  clustering. Cosine similarity convergence, a new metric that traces the
  collapse layer by layer, puts every analysed method except LRP z and DeepLIFT
  past **0.99** on VGG-16 and ResNet-50.

  Also: **ROAR does not separate converging from non-converging methods** —
  Integrated Gradients and Guided Backprop are "equally bad, worse than a random
  baseline". And the intuitive story is refuted by name: "Other than argued in
  (Gu et al. 2018), the class insensitivity is **not** caused by missing ReLU
  masks and Pooling switches."

- **`THEORY-114`**, **`Active`** — that account. `Active` rather than
  `Proposed` because it is a theorem about matrix products *and* because the
  paper supplies the arms in both directions: DeepLIFT is a published method
  that does not converge, for the reason the account gives (its linear rule
  intermixes positive and negative contributions), and **DeepLIFT Ablation** is
  a variant the authors build to order, removing the intermixing so the chains
  decouple — "as predicted by the theory, it converges". A prediction made in
  advance about something that did not previously exist.

### Changed

- **`SOTA-430` v5 and `LIT-727` v2 — a false sentence written hours earlier,
  corrected.** Both said `1912.09818` "is the paper that argues" why guided
  backprop fails a randomization test. **It is not.** It measures guided
  backprop and explicitly hands the explanation on: "As a ReLU operation is
  applied to the gradient, the backpropagation is no longer a linear function.
  The ReLU also results in a *different failure* than before. (Nie et al. 2018)
  provides a theoretical analysis for GuidedBP." That paper is Nie, Zhang and
  Patel, *A Theoretical Explanation for Perplexing Behaviors of
  Backpropagation-based Visualizations*, `1805.07039`, identifier resolved
  against arXiv and unheld.

  The error came from reading `LIT-725`'s citation — "Guided BackProp and Guided
  GradCAM ... do not pass randomization tests for different reasons (Sixt et al.
  2020)" — as an attribution of the *argument* rather than of the *observation*.
  **A citation tells you who reported something, not who explained it.**

- **`THEORY-113` v2 — the boundary, now that a second account exists.** The
  cluster's failures partition three ways and each document says which part it
  owns:

  | family | mechanism | held as |
  | --- | --- | --- |
  | IG, InputXGradient, DeepLIFT, Gradient SHAP | the input multiplier | `THEORY-113` |
  | DTD, LRP-α1β0, Excitation BP, PatternAttribution | rank-1 convergence | `THEORY-114` |
  | Guided Backprop, Deconv, RectGrad | a third mechanism | **not held** — `1805.07039` |

  The new paper also supports `THEORY-113` from outside its own subject: methods
  that rely on the gradient directly "[do] not converge", so Integrated
  Gradients' behaviour is not the rank-1 mechanism, which leaves the multiplier.

  **DeepLIFT is in the first row and outside the second, and that is not a
  contradiction** — it carries an input multiplier *and* keeps negative
  contributions, so it has one failure mode and escapes the other.

### Measured, not closed

**`SOTA-430`'s headline failure is now the one remaining unexplained row**, and
the paper that explains it is named with a verified identifier. That is a better
position than an hour ago, when the record had a masking rule, a measurement, and
a wrong claim about which paper joined them.

**Sixt is in this record three times and was unheld until now.** `LIT-713`'s
acknowledgements credit him with the bug report that made Adebayo et al.
withdraw "entirely invariant"; `LIT-725` cites him for the different-reasons
sentence; and here he states the bug confirmation from his own side, reporting
maps that differ from that paper's Figure 2. The **verdict** survives — this
paper lists Guided BP among the methods independent of later layers'
parameters — but `SOTA-430`'s headline example rests on a figure its own author
and its bug-reporter both amended.

### Added

- **Chu & Raginsky, *Talagrand Meets Talagrand*** (`LIT-726`, with a
  `Read` NOTE), moved from the catchall record nucleation at the owner's
  request. It is a probability paper with no ML claim. What it offers here is
  exact Gaussian-score relations between softmax sharpness, entropy and score
  scale, the Gaussian counterpart of `THEORY-098`'s dispersion argument.

### Added

- **Visualizing and Understanding Convolutional Networks** — `LIT-728`.
  Zeiler and Fergus (2013), `1311.2901`. Two attribution families begin here
  and the record leans on both.

  **The deconvnet**, which needs max-pooling "switches" from a forward pass and
  is therefore "conditioned on an image and does not directly visualize learned
  features" — the approach guided backpropagation is defined as a variant of.

  **Occlusion sensitivity** — slide a grey square, watch the class probability
  and the top feature map's activity — which `LIT-725` names as the origin of
  perturbation-based attribution, and whose quantitative descendant is
  `LIT-725`'s infidelity. The record acquired that metric yesterday and did not
  hold the method it descends from.

  Also: the paper validates one attribution with the other. "When the occluder
  covers the image region that appears in the visualization, we see a strong
  drop in activity in the feature map. This shows that the visualization
  genuinely corresponds to the image structure that stimulates that feature
  map." Three examples, qualitative — but it is the positive-evidence move
  `SOTA-430`, a rejection rule, explicitly cannot make.

- **Striving for Simplicity: The All Convolutional Net** — `LIT-727`.
  Springenberg, Dosovitskiy, Brox and Riedmiller (2014), `1412.6806`, ICLR
  2015 workshop. **Guided backpropagation's defining paper**, and so the
  referent for `SOTA-430`'s headline failure case.

  **The rule, in one sentence (§4.2).** At each ReLU, zero the gradient
  wherever *either* the top gradient or the bottom activation is negative.
  Plain backprop masks on the second; the deconvnet masks on the first;
  guided backprop applies both. The stated reason is to "prevent backward flow
  of negative gradients, corresponding to the neurons which decrease the
  activation of the higher layer unit we aim to visualize".

  **The property later found to be its defect is presented here as its
  advantage.** The method exists because this paper's architecture has no
  max-pooling and so no switches: "unlike the 'deconvnet', guided
  backpropagation works remarkably well without switches", while the deconvnet
  "fails completely in the absence of switches". The explanation offered —
  "the bottom-up signal in form of the pattern of bottom ReLU activations
  substitutes the switches" — is four years before anyone measured that its
  maps survive destroying the weights.

### Changed

- **`SOTA-430` v4 — the failing row's two methods get their defining papers**,
  so its headline example can be followed to a masking rule instead of stopping
  at a name. Verdict, recommendation and status unchanged. Third amendment
  today; each was driven by a source arriving rather than by a rereading, and
  the history entry says which.

### Measured, not closed

**The record now holds the rule and the measurement and still cannot join
them.** Guided backprop's masking is here; that its maps survive randomization
is `LIT-713`; that it fails "for different reasons" from the
multiplier-carrying methods is `LIT-725`'s sentence, and `THEORY-113` covers
only the multiplier side.

Joining them from what is held would be an over-reach, and it is worth naming
why, because the temptation is specific: the bottom ReLU activation pattern
still depends on the weights, so "the structure comes from the input" is not
what Springenberg's sentence says. **No theory is filed, and the paper that
argues it is named rather than gestured at** — Sixt, Granz and Landgraf (2020),
*When Explanations Lie: Why Many Modified BP Attributions Fail*, `1912.09818`,
identifier verified. Next read in this cluster.

**No practice for occlusion sensitivity.** The positive-validation move is
already held in quantitative form as `LIT-725`'s infidelity, under `SOTA-435`.
Filing the 2013 qualitative version separately would be filing on antecedence
rather than on a defect — the call `LIT-722` got two units ago. What the note
adds is the lineage.

**Zeiler and Fergus's ablation is out of scope and worth recording.** Removing
the fully connected layers "only gives a slight increase in error ... surprising,
given that they contain the majority of model parameters", while removing them
*and* two middle conv layers is "dramatically worse". A 2013
depth-against-parameters result in a record with a large scaling cluster, cited
by nothing in it.

### Added

- **On the (In)fidelity and Sensitivity for Explanations** — `LIT-725`.
  Yeh, Hsieh, Suggala, Inouye and Ravikumar (2019), `1901.09392`, NeurIPS 2019.
  The definitions behind two numbers this record started quoting yesterday.

  **Max-sensitivity is minimised by a constant explanation.** The paper's own
  words: the optimum "is simply a constant explanation that just outputs a
  (potentially nonsensical) constant value for all possible test inputs". An
  attribution that ignores the input wins the measure outright.

  **Infidelity is defined relative to a perturbation distribution you choose**,
  and Propositions 2.2–2.5 show several published explanations are each the
  optimum for some choice — demonstrated by giving SHAP the lowest infidelity
  under SHAP's own perturbation. An infidelity number without its perturbation
  is not comparable to anyone else's.

  Also carried: kernel smoothing lowers max-sensitivity provably (Thm 4.1) and
  infidelity empirically ("for all base explanations across all datasets"); and
  a planted-feature human study where infidelity tracks whether people can
  infer which half of the image the model actually used — 0.55/0.38/0.35/0.00
  infidelity against 0.47/0.50/0.53/0.88 accuracy.

- **`SOTA-435`**, `Active`/`unreplicated` — report infidelity and
  sensitivity together, never either alone, and name the perturbation
  distribution. `Active` on one paper because most of it is not the kind of
  claim replication tests: the degenerate optimum falls out of the definition
  and the perturbation dependence is proved. Following it costs a sentence and
  a column.

### Changed

- **`SOTA-430` v3 — step 3 gets a third independent source, and the
  `promote_when` gets sharper.** Three groups on three model families now agree
  that the similarity metric flips the verdict: `LIT-713` on Inception and
  MNIST, `LIT-724` on Inception and BERT, and `LIT-725` on ResNet-50, where
  signed rank correlation runs **0.10–0.18** across five explanations and the
  absolute-value correlation on the same explanations runs **0.57–0.62**. Step 3
  is now the best-supported thing in a practice whose headline is still
  `Proposed`.

  **The `promote_when` asks for the randomization tests run where the
  input–output dependence is known by construction. `LIT-725` builds
  exactly that setting and points it at a different question.** Its planted
  feature — a caption in one half of the image, one model verified to use it
  and one verified not to — validates infidelity against human judgement; its
  randomization test runs on ImageNet with no ground truth. The two are
  different experiments in the same paper. The bar is not met, and now the
  reason is specific: **the experiment is a table-join away inside published
  work.**

- **`LIT-724` v2** — its two metrics have a definition at last, and one needs a
  caveat the note reported around. "Max-sensitivity remains almost unchanged"
  is weaker than it reads when a constant explanation is the measure's optimum.
  Its infidelity figures are unaffected: it named its perturbations, which is
  step 2 done correctly.

### Measured, not closed

**`#290`'s fourteen captum declines, re-read: eight reverse, six confirm.** They
were declined *behind* `1703.01365` and `1810.03292` with the trigger "file the
openers first and revisit the rest" — a condition that went false when the
openers landed and that nothing reports.

Named in held documents, and so now candidates: `1412.6806` (Guided Backprop, 7
documents — `SOTA-430`'s headline failure case), `1610.02391` (Grad-CAM, 6),
`1704.02685` (DeepLIFT, 6), `1312.6034` (plain-gradient saliency, 5),
`1605.01713` (InputXGradient, 5), `1311.2901` (Zeiler and Fergus, 3),
`1706.03825` (SmoothGrad, 3), `1901.09392` — filed here.

Named nowhere, and declined again with a measured reason rather than an
inherited one: `1712.01312`, `1802.03788`, `1805.05492`, `1805.12233`,
`1807.09946`, `1810.04247`. **Zero mentions each**, and four of the six are
layer- or neuron-level attribution, which is a cluster the record has not
opened and which nothing in it depends on.

**No theory.** Proposition 2.1's "the infidelity optimum is smoothed Integrated
Gradients" is a derivation from the definition, not a contested explanation of
why anything works — the same call made about the conditional-score
decomposition in `LIT-722`.

### Added

- **Investigating Sanity Checks for Saliency Maps with Image and Text
  Classification** — `LIT-724`. Kokhlikyan, Miglani, Alsallakh, Martin and
  Reblitz-Richardson (2021), `2106.07475`. The paper three documents named and
  none held: `SOTA-430` twice (`promote_when` — "`2106.07475` is the first to
  read" — and `consensus_note` — "The record holds none of it and has not read
  it"), `NOTE-365` twice, `LIT-713` once. Five sites, one bare arXiv id.

  **The failure has a named cause and it is not the attribution method.**
  Global Integrated Gradients multiplies a model-dependent path integral by
  `(x − x₀)`, which does not depend on the model. Drop it and, on Inception
  under cascading randomization, the maps change — SSIM for the local variant
  is about half the global variant's.

  **The verdict does not survive the change of modality.** On BERT/SST-2, both
  local and global IG are parameter-sensitive: global IG **fails the test on
  images and passes it on text**, because token scores are summed over
  embedding dimensions and the multiplier's structure does not survive the sum.

  **SSIM and Spearman disagree about the same experiment**, in the paper's own
  Appendix A. And randomization degrades the integral approximation badly
  enough to move a faithfulness metric on its own: infidelity **2.84 →
  1.27 × 10⁷** down the Inception stack.

- **`THEORY-113`**, `Proposed` — the input-multiplier account. What makes
  this an account rather than a relabelling is that it has two discriminating
  arms pointing opposite ways: remove the multiplier and the map becomes
  parameter-sensitive; destroy the multiplier's *structure* without removing
  it, as the text summation does, and the same thing happens to the global
  variant. An explanation that only covered the image result would be
  indistinguishable from the word "multiplier"; this one predicts a sign change
  across modality and gets it.

  `LIT-713` named the multiplier as the likely cause and said plainly that it
  "do[es] not measure input multiplier's quantitative impact". This is that
  measurement.

### Changed

- **`SOTA-430` v2 — a fourth step, two conditions, and a consensus that can
  now be judged.** The new step: *if a method fails, re-run it without the
  input multiplier before concluding anything about the method.* The
  conditions: the verdict does not transfer across modality, and part of what
  the test moves is quadrature error rather than explanation.

  Consensus goes `unassessed` → **`contested`**, which is the honest reading of
  a clean fork. Both groups run the tests and neither validates a map by eye,
  so the trunk is agreed. `LIT-713` reads a failure as evidence that
  gradient-based methods are "inadequate tools for model explanation";
  `LIT-724` reads the same failure as an artefact of a factor you can
  switch off. Recommendation and status unchanged.

  Its step 3 already warned that SSIM and signed rank correlation can hand you
  either verdict, on `LIT-713`'s data. **A second group reproduces that split
  on a different model** — which is the strongest corroboration any part of
  this practice has, and it corroborates the caveat rather than the headline.

- **`NOTE-365` v2 and `LIT-713` v2** now name the code behind the paper they
  called unread. `NOTE-365`'s open question — "Do the verdicts hold for
  transformers and for token attributions?" — is struck through and answered:
  no.

### Measured, not closed

**`#342`'s Tier C was filed a day before this unit, by two contributions
working a different queue, and nothing noticed.** All seven items are held and
`Active`: `1703.01365` (`LIT-712`), `1810.03292` (`LIT-713`), `2102.11972`
(`LIT-711`), `2607.18363` (`LIT-708`), `2212.14034` (`LIT-681`), `2303.09556`
(`LIT-710`), `2109.08668` (`LIT-709`). Six came in with `#375` and one with
`#366`, both journal-backlog units. The issue body says Tier C is "untouched,
as intended", and so does a comment posted hours *after* six of the seven
landed.

That comment is mine, it is a day old, and it re-measured Tiers A and B against
`main` in the same breath. **Measuring two of three tiers and reporting the
third from the issue body is the `#379` defect exactly** — a claim read off a
stale artefact instead of a tree — one day after writing that the fix is to
re-measure immediately before committing.

**No practice for the smoothing result.** Replacing ReLU with Softplus and
MaxPool with LSE for better infidelity is a recommendation to change the model
in order to explain it, on one figure, one metric, one architecture. Whether
the explanation then describes the model you ship is the question, and the
paper does not ask it.

### Added

- **Swin Transformer: Hierarchical Vision Transformer using Shifted Windows** —
  `LIT-723`. Liu, Lin, Cao, Hu et al. (2021), `2103.14030`. The last
  unfiled Tier A/B item on `#342`, and the one that kept getting ranked last
  because all nine documents that mention it use it as somebody else's
  experimental backbone.

  **What it is.** Self-attention confined to non-overlapping `7×7` windows,
  which takes the cost from `2(hw)²C` to `2M²hwC`, plus 2×2 token merging
  between stages so the backbone emits `H/4, H/8, H/16, H/32` feature maps
  instead of one. The partition is shifted by `(⌊M/2⌋, ⌊M/2⌋)` in alternate
  blocks to connect the windows.

  **Why it is worth holding: the ablation is run on three tasks.** Swin-T, one
  recipe, ImageNet-1K / COCO / ADE20K, Table 4:

  | variant | ImageNet top-1 | COCO AP_box | ADE20K mIoU |
  |---|---|---|---|
  | no position encoding | 80.1 | 49.2 | 43.8 |
  | absolute only | 80.5 | 49.0 | 43.2 |
  | absolute + relative | 81.3 | 50.2 | 44.0 |
  | **relative only** | **81.3** | **50.5** | **46.1** |

  The absolute term is worth **+0.4** top-1 and **−0.2** box AP and **−0.6**
  mIoU. **One design choice, scored on three tasks, with the classification
  score pointing the wrong way.**

  Also carried: shifted windows are a *speed* result, not a modelling one —
  Table 6 gives sliding and shifted windows the same accuracy to within noise
  (81.4/50.2/45.8 against 81.3/50.5/46.1) and Table 5 gives shifted windows a
  4.1×/1.5× speed-up, because all queries in a window share one key set.

- **`SOTA-434`**, `Proposed`/`unreplicated` — carry position with a
  relative bias inside the attention window, and do not add an absolute
  position embedding on top. Stacking absolute on relative leaves ImageNet
  unchanged at 81.3 and costs **2.1 mIoU**.

  The recommendation is about the **sign**, not the size: top-1, box AP and
  mIoU are not commensurable quantities, so nothing here supports "the effect
  is larger on dense tasks". The direction needs no commensurability.

### Changed

- **`SOTA-388` v2 — the task scope of its position item.** Every number in it
  is ImageNet-1k top-1, and fixed 2D sin-cos positions are the smallest of its
  five changes at 0.4 points. That is the same 0.4 the new note measures for an
  absolute position term on classification, alongside negative numbers on both
  dense tasks. Different architecture, different encoding, so it refutes
  nothing — it marks the row to re-measure if the baseline is being used as a
  backbone rather than as the classification baseline it is scoped to be.
  Recommendation, status and consensus unchanged.

- **`SOTA-358` v3 — the threshold is per-task.** The practice states the trade
  on one axis, prior against data volume, with the downstream task held fixed
  at classification and never named as a variable. The new note varies it
  inside one model and the invariance prior's value changes sign. The
  amendment says explicitly what this does *not* show: not a data-scale sweep,
  not convolution, and **not** Swin-beating-ViT, which varies everything at
  once. What it shows is that "sweep pre-training set size and find the
  crossover" is incomplete — the crossover you find belongs to the task you
  scored.

### Measured, not closed

**No theory.** The paper attributes the sign flip to translation invariance
mattering more for dense prediction and runs no experiment isolating it, so the
account and the measurement are one observation told twice. The standard this
record applied to autoguidance three days ago — a mechanism claim earns its
status when the experiment includes an arm the mechanism says must fail — is
not met, and the sign flip stays measured and unexplained.

**`SOTA-320` and `THEORY-062` are left alone.** They rest on "ViT, Swin and GPT
all train without warmup", which is a strong sweep precisely because Swin is
architecturally far from ViT, and neither document says so. That is a weakness
in how the generality is argued rather than an error, and the note now supplies
the referent for a reader who wants to check it.

### Added

- **Score-Based Generative Modeling through Stochastic Differential Equations** —
  `LIT-722`. Song, Sohl-Dickstein, Kingma, Kumar, Ermon and Poole (2020),
  `2011.13456`. The framework the record's diffusion vocabulary rests on, cited as
  an authority three times and held by nothing.

  **Classifier guidance is §5, Eq. 14, in November 2020** — six months before ADM:

      dx = {f(x,t) − g(t)²[∇ₓ log pₜ(x) + ∇ₓ log pₜ(y|x)]}dt + g(t)dw̄

  plus the recipe for the noise-conditioned classifier that supplies the second
  term: sample `(x(0), y)`, noise it through the tractable forward SDE, train with
  "a mixture of cross-entropy losses over different time steps". `LIT-699` credits
  it in its own words, as a "score-based conditioning trick adapted from Song et
  al." and as prior work that "uses a classifier to generate class-conditional
  CIFAR-10 images with a diffusion model".

  Also carried: the unification of SMLD and DDPM as discretizations of one
  reverse-time SDE; the probability flow ODE with exact likelihoods and unique
  encoding; predictor-corrector sampling; CIFAR-10 IS **9.89** / FID **2.20** /
  2.99 bits/dim; the first 1024×1024 samples from a score model; and the
  limitation it names — that access to score functions "introduces a number of
  hyper-parameters" whose tuning is future work, which is most of what this
  record's sampler practices have been doing since.

### Changed

- **`SOTA-397` v2 — the rejection now names what it rejects, and why it fails.**
  v1 argued against **replacement** as though it were folklore. It is
  `LIT-722` §I.2, and that paper writes down the step where it breaks: it
  wants `pₜ(z(t) | Ω(x(0)) = y)`, calls it "in general intractable", and
  approximates it by dropping the conditioning on the *exact* known values and
  keeping only the *noised* known dimensions. The discarded term is exactly the
  requirement that new content agree with the real frames rather than a noisy copy
  of them — so the 136-against-451 FVD gap is the size of a named approximation
  error, not a mysterious fact about splicing. Recommendation, status and
  consensus unchanged.

- **`NOTE-358`, `NOTE-347` and `NOTE-067`** now name the code behind "Song et
  al.", so three citations that resolved to nothing resolve to a document.
  `NOTE-067`'s case is the useful one: it exists because a reading had confused
  DDIM with this paper, and the distinction it draws is now checkable against both
  documents instead of one.

### Measured, not closed

**No new practice or theory, deliberately.** The conditional-score decomposition
is a derivation rather than a contested explanation, so a `THEORY` for it would be
filing on novelty — the same call made about EDM2's magnitude-preserving layers.
Predictor-corrector sampling is a real recommendation, but the record's sampler
practices (`SOTA-203`, `SOTA-410`, `SOTA-416`) are about the deterministic branch
and this paper runs no controlled comparison against them. Filing the substrate is
the whole contribution.

### Added

- **Guiding a Diffusion Model with a Bad Version of Itself** — `LIT-721`.
  Karras, Aittala, Kynkäänniemi, Lehtinen, Aila and Laine (2024), `2406.02507`.
  Added to `#342` by request and filed the same day; Tier A on measurement, because
  28 documents name classifier-free guidance or the guidance scale and seven
  practices turn on the unconditional model specifically.

  **CFG's quality gain is not the class emphasis.** Guidance adds a force along
  `∇ₓ log[p₁/p₀]`, and the reference `p₀` is a *worse fit* — a harder task on a
  smaller slice of the training budget — so it falls off more slowly away from the
  data, the ratio's gradient points inward, and samples concentrate on the manifold.
  EDM2-S on ImageNet-512 is FID **2.56** conditional against **11.67**
  unconditional: that is the size of the asymmetry every CFG deployment exploits,
  and the paper notes the unconditional number "is hardly ever reported".

  **The mechanism is tested with a negative control**, which is the rare part.
  Post-hoc corruptions of one base model: dropout 5%/10% autoguides back to
  **2.55** against the undamaged 2.56, input noise +10%/+20% to **2.56** — and
  dropout against input noise, *incompatibly degraded*, gives **no improvement at
  any weight**. A worse reference is not sufficient; it has to be worse in the same
  direction.

- **`THEORY-112`**, `Proposed` — the account above. The record held
  `THEORY-104` (what a large guidance scale does to a solver) and `THEORY-109` (a
  suspicion about the metrics) and **nothing about why guidance works**. The
  `promote_when` asks for precision and recall on autoguided against CFG-guided
  samples at matched FID — the account's distinctive prediction is that the two
  split on *coverage*, and every number in the source is a Fréchet distance that
  mixes coverage with fidelity.

- **`SOTA-433`**, `Proposed`/`unreplicated` — guide with a smaller,
  less-trained copy of the same model. For EDM2-S: an XS guiding model at 1/16 of
  the training iterations, with **independent** EMA lengths for the two models
  (forcing them equal costs FID 1.34 → 1.53, which makes `SOTA-428` a
  precondition). ImageNet-512 **2.56 → 1.34** (S) and **1.25** (XXL),
  ImageNet-64 **1.01**, unconditional **11.67 → 3.86**.

  `Proposed` rather than `Active` on the authors' own objection: an early snapshot
  of a smaller model is "easy to satisfy in principle, but these are not available
  for current large-scale image generators in practice".

### Changed

- **`SOTA-424` v3 — two Conditions bounded to the recipe they belong to.**
  "Conditional generation only" and "diversity is what is being spent" were written
  as properties of guidance; they are properties of *CFG's choice of reference
  model*. An unconditional model can be guided, and the diversity loss travels with
  the class emphasis rather than with the guidance. Recommendation, status and
  consensus unchanged — this is still how you get a CFG model.

### Measured, not closed

**The paper's own future work names the instrument the record already holds** and
does not run it: "alternative metrics, such as precision and recall, Human
Preference Score, or PickScore". That is `SOTA-425`'s recommendation and part of
`THEORY-109`'s `promote_when`. Two papers in this cluster have now asked for a
coverage measurement on guided samples and neither has taken it.

**Contrastive decoding** is named as a conceptual sibling in language models, and
the record holds nothing on it.

### Added

- **Five works filed `Deferred`, each with a `Skimmed` NOTE.** They are the
  boundary cases of the survey of work this record set aside as out of scope,
  and they are filed here under the rule that a work in doubt belongs in the
  anthology:
  - Burrell
  - *Your Brain on ChatGPT*
  - Møller et al.
  - *Surya*
  - the tiny-RNN cognitive-strategies paper

### Changed

- **`published:` is the exact date of first appearance** where a source gives
  one (arXiv v1, else Crossref within the recorded year), not the first of the
  posting month. 420 LITs backfilled; five left alone and named in the ADR where
  the only available date was a digitisation or journal-issue date years off.
  Practices and theories follow through `derive`.

### Added

- **Twelve papers from the skipped-readings worklist, each read in full:**
  - Integrated Gradients and Sanity Checks for Saliency Maps
  - EDM2 and FLIP
  - Min-SNR and Primer
  - Narang et al. and the attention-only controlled study
  - Li et al., Gal & Ghahramani and Hara et al. on dropout
- **Five `Proposed` practices:**
  - Dropout after the last batch-norm layer.
  - Post-hoc EMA length.
  - Magnitude-preserving diffusion layers.
  - Patch masking in CLIP-style training.
  - Randomization tests before trusting an attribution map.

### Changed

- **`SOTA-034` (SwiGLU) is `contested_by` Primer.** It also gains Narang et
  al. as a corroborating source that is not a transfer test.
- **Six more architecture practices record what Narang et al. and the
  attention-only study found for them:** `SOTA-182`, `SOTA-150`, `SOTA-051`,
  `SOTA-403`, `SOTA-190` and `SOTA-192`.
- **`SOTA-195`, `SOTA-188` and `SOTA-424` record** what Min-SNR and EDM2
  measured.
- **`LIT-020`, `LIT-023` and `LIT-047` gain `model-architecture`.**
  **`LIT-605` and `SOTA-372` gain a tag each.**

### Changed

- **`SOTA-415` v2–v3 — qualifies one of its two reasons for uniform averaging.**
  "It has no hyperparameter" described uniform averaging as a *scheme*, not the
  choice: the practice's own next bullet is a heuristic for tuning a window, with
  a measured 4.6-point penalty for getting it wrong early. `LIT-714` shows the
  averaging length can be reconstructed after the run, so the hyperparameter is
  avoidable rather than unaffordable, and `SOTA-428` is how. Recommendation,
  status and consensus unchanged.

- **`SOTA-408` v2–v3** — its "the extra epochs are real compute" objection is a
  property of its method, not of weight averaging: `SOTA-428` accumulates its
  averages inside the run and pays storage. Different settings, never compared,
  and the charge still applies to what `SOTA-408` asks for.

### Retired

- **`LIT-720`, `SOTA-432` and `THEORY-111` — a duplicate filing of
  `2312.02696`, retired the day they were filed.** The paper was already held as
  `LIT-714` and its recommendation as `SOTA-428`, filed hours earlier in `#375`
  and merged while this unit was being written. `LIT-714` is the fuller reading
  and `SOTA-428` the better practice — it carries the architecture,
  learning-rate, guidance and metric dependences where the duplicate had two —
  and `THEORY-111`'s claim is already a `SOTA-428` Conditions bullet in the
  source's own words.

  The duplicate broke the trunk: `arxiv` is declared unique on `LIT`, so two notes
  holding `2312.02696` failed the lint on `main`. Retired rather than deleted, per
  the lint's own remedy and so the mistake stays visible.

  What survives is only the two amendments above, which touch practices
  `SOTA-428` does not mention.

### Added

- **Improved Precision and Recall Metric for Assessing Generative Models** —
  `LIT-703`. Kynkäänniemi, Karras, Laine, Lehtinen and Aila (2019),
  `1904.06991`. The definitions `SOTA-425` rests on, filed because that practice
  made them load-bearing in the unit before this one and said in its own Source
  section that the 2026-09-23 decline had expired.

  **The method.** Embed 50 000 real and 50 000 generated images, surround each
  feature vector with a hypersphere reaching its `k`th nearest neighbour, and ask
  binary membership. Precision is the fraction of generated samples inside the
  real manifold; recall the fraction of real samples inside the generated one.
  Two manifolds estimated separately, never mixed — which is why it survives
  truncation where the predecessor does not.

  **The demonstration, which is better than the one `SOTA-425` had.** Four
  StyleGAN setups on FFHQ: **B at FID 16.9** produces good samples at lower
  variety, **D at FID 16.7** is "practically all images broken", and **C at FID
  4.5** is the FID-optimised configuration with visible facial distortion. Two
  setups 0.2 FID apart and perceptually opposite.

  Also carried: `k = 3` and the fact that both metrics rise with `k`; the Pareto
  frontier as the answer to two-objective model selection; FID varying "by up to
  **±14%** between consecutive training iterations"; the realism score and why
  its estimator has to discard the largest half of the hyperspheres; and 2.4% of
  500 000 interpolation paths leaving the real manifold.

- **`THEORY-110`**, `Proposed` — FID is not neutral between fidelity and
  coverage; it weights coverage more, so optimizing it walks toward variety at
  the cost of per-sample quality.

  Measured on six StyleGAN configurations: "FID favors configurations with high
  recall over the ones with high precision", and the best-recall configuration
  set a new state-of-the-art FID. The mechanism is stated rather than inferred —
  FID is a Wasserstein-2 distance in feature space, so "low intrinsic variation
  implies low FID even when much of that variation is missed". `LIT-699` is an
  independent instance in another family: ADM-G beats BigGAN-deep on FID at three
  resolutions while losing precision at all three. Different groups, neither
  citing the other for this. The `promote_when` asks for the magnitude, which
  nobody has measured.

### Changed

- **`SOTA-425` v2 — corrects a false claim about the instrument it
  recommends.** v1 said precision and recall are "computed with the same ImageNet
  network FID uses". They are not: **VGG-16 activations after the second fully
  connected layer**, against FID's Inception-v3. The conclusion survives and is
  arguably sharper — two *different* ImageNet classifiers whose own paper reports
  they give "substantially similar" results is not a cross-check — but the reason
  was wrong. Adds two conditions v1 lacked: fix `k` and the sample count, and
  treat model selection as multi-objective (report the Pareto frontier).

- **`SOTA-337` v3** — the same wrong sentence in the Conditions bullet v2 added
  hours earlier.

- **`SOTA-307` v5** — the one case in this record of its own "port the protocol,
  measure your own floor" instruction being followed: ±14% for StyleGAN on FFHQ
  against the 1–2% calibrated for SiT on ImageNet. Different family, different
  dataset, and a ±range over consecutive snapshots rather than a coefficient of
  variation over seeds, so it prices the warning rather than correcting the
  number. Also notes that a second metric turns the error bar into a frontier.

### Measured, not closed

**Sajjadi et al. (2018), `1806.00035`, is unheld**, and everything the record now
knows about it comes from the paper that replaces it — the same one-sided
position `THEORY-109` holds with respect to classifier guidance. Deliberate, and
named in `LIT-703`'s Standing section rather than left implicit.

**`LIT-699` never states which feature network its precision and recall use**, as
it does for FID. The values `SOTA-425` argues from are therefore internally
consistent and of unstated comparability with anyone else's.

### Added

- **Three papers the journal had named and not filed**, each read in full:
  - MDLM (`LIT-702`)
  - SEDD (`LIT-701`)
  - Islamov et al. (`LIT-700`)
- **Read NOTEs for DeepSeek-V4** (`LIT-139`) **and Dhariwal & Nichol** (`LIT-699`, filed by [#369](https://github.com/dmarx/anthology-of-the-sota/issues/369)), with [LIT-699](record/literature.d/LIT-699.md)'s lineage relations.
- **ReLoRA's restart rule** as a `Proposed` practice.

### Changed

- **`SOTA-157` is scoped to what its sources show:** masked over other discrete
  diffusion, not diffusion over autoregression.
- **`THEORY-035` distinguishes the update's norm from the Euclidean
  sharpness.**
- **`LIT-104` (ReLoRA) → `Active`**, and `ADR-042`'s status note no longer says
  ReLoRA is unfiled.

### Fixed

- **`LIT-185`, `SOTA-227`, `SOTA-162` and `LIT-163` no longer say DeepSeek-V4
  ships EAGLE-style speculative drafting.** The V4 report describes MTP as a
  training objective only.
- **The classifier scale of 8.0 is described as a stress test**, not a setting,
  in `LIT-676`, `SOTA-203` and `SOTA-410`. `THEORY-109` names the right
  classifier.

### Changed

- **Posani et al. read in full** (`LIT-696`, `NOTE-353`). It is now `Active`
  with a `Read` NOTE. The reading qualifies the paper's headline: "maximally
  separable" rests on an above-chance test over 16 regions, not 43. It also
  gives a check the record's probing documents lack. A linear probe that
  works is weak evidence in a high-dimensional code unless it is compared
  against random groupings of the same inputs. The reading bears on
  `THEORY-034` and `THEORY-090`.

### Fixed

- **The boundary-works curation entry no longer says *Topos and Stacks*
  builds on Abramsky & Brandenburger.** It cites that paper once, in a
  related-work list.

### Changed

- **`CLAUDE.md` documents the branch-point hazard that temporary codes create.**
  `luria concretize` runs only on `main`, so a PR branch carrying `LIT-tmpxxxxx`
  is correct — and the consequence, which was written nowhere, is that `main`'s
  tip is briefly inconsistent: the merge commit still holds the temp codes and
  the bot's next commit renames them. On `#367` that window was 62 seconds.

  The check to run before `git checkout -B`, and the reason it must name the
  remote ref rather than the local checkout, are now in the "Working" section.
  `LU-#325` asks the CLI to own the check so that the configured temp shape and
  the set of merge-allocated schemes are what gets tested, rather than the
  substring `tmp`; the paragraph says to delete its grep when that ships.

### Added

- **Five boundary works from the reading-time triage's out-of-scope set**,
  filed `Deferred` with `Skimmed` notes under the owner's rule that a work in
  doubt belongs here: the cortical-representations paper, *Language Design as
  Information Renormalization*, *Topos and Stacks of Deep Neural Networks*,
  AgentSociety, and *Rigor with Machine Learning from Field Theory to the
  Poincaré Conjecture*. The other 29 went to the catchall record,
  nucleation.

### Added

- **Diffusion Models Beat GANs on Image Synthesis** — `LIT-699`. Dhariwal
  and Nichol (2021), `2105.05233`. The record's most-cited unread paper, used
  four times as an instrument or an authority, and the antecedent
  `LIT-693` is named against.

  **The title claim is metric-dependent, and the paper's own main table says so.**
  ADM-G beats BigGAN-deep on FID and recall at ImageNet 128, 256 and 512 — and
  loses precision at all three:

  | ImageNet | model | FID ↓ | Prec ↑ | Rec ↑ |
  | --- | --- | --- | --- | --- |
  | 128 | BigGAN-deep | 6.02 | **0.86** | 0.35 |
  | 128 | ADM-G | **2.97** | 0.78 | **0.59** |
  | 256 | BigGAN-deep | 6.95 | **0.87** | 0.28 |
  | 256 | ADM-G | **4.59** | 0.82 | **0.52** |
  | 512 | BigGAN-deep | 8.43 | **0.88** | 0.29 |
  | 512 | ADM-G | **7.72** | 0.87 | **0.42** |

  The paper states the exception plainly: guidance "is only a better choice up
  until a certain precision threshold, after which point it cannot achieve
  better precision".

  **The adversarial question was asserted away here, not answered here.** The
  introduction says the gradient scale can be raised "by an order of magnitude
  without obtaining adversarial examples". The word *adversarial* appears
  nowhere else in the paper — no test, no held-out classifier, no non-Inception
  distance. The nearest check, App. C on memorization, is run in InceptionV3
  feature space.

  Also carried: the architecture ablation (`AdaGN` 13.06 against 15.08; combined
  changes −3.14 FID), the one change that made FID **worse** (rescaling residual
  connections by `1/√2`, which everyone else had adopted), and **two settings
  that are not the ablation's winners** — depth and 64 channels per head, both
  chosen for wall-clock time and both stated as such.

- **`SOTA-425`**, `Active`/`emerging` — report precision and recall beside
  FID whenever the generator has a fidelity/diversity knob. FID mixes the two,
  so on such a knob its optimum is interior and a single FID cannot say which
  side of the trade a model is on. The paper's own headline comparison is the
  demonstration.

  The metric's defining paper (`1904.06991`) is **not** held here, and was
  declined in the 2026-09-23 metric-definition sweep as "not load-bearing on
  anything". This practice is what makes it load-bearing, so that decline has
  expired. Said in the practice rather than papered over.

### Changed

- **`SOTA-337` v2 — the title widens to the scope its source already had.**
  Kynkäänniemi et al. suspected classifiers "placed in the sampling loop" as
  well as pretrained discriminators, and the body had said so since v1, but the
  title said "take part in **training** a generator". That excluded classifier
  guidance: a procedure that maximises an ImageNet classifier's log-probability
  on every sampling step, evaluated with an ImageNet classifier. Recommendation,
  status and consensus unchanged; provenance is now explicitly not the point —
  a classifier trained from scratch on ImageNet labels has the same feature
  space as a downloaded one.

- **`THEORY-109` v2 — its `promote_when` now names the instrument the
  record already owned.** Filed this morning asking for "a feature distance from
  a self-supervised encoder", it did not notice that `SOTA-337` recommends
  exactly that, names CLIP and SwAV, and lists the sampling loop among the cases
  it suspects. The condition is now a specific experiment: a CLIP or SwAV
  Fréchet distance on guided against unguided samples at matched FID. Status
  stays `Proposed`, and the account gains the antecedent's non-measurement.

- **`LIT-693` v2** and **`LIT-676` v3** — both said `2105.05233` was still
  unheld. Both were true when written and false hours later. `LIT-676`'s is the
  second such correction to the same note in one day.

### Measured, not closed

**Three notes in three consecutive units have had a "the record does not hold X"
sentence falsified by the next unit.** `LIT-676` (twice) and `LIT-693`. The
sentences are useful — two of these filings happened *because* a note named the
gap — but nothing checks them, and a bare arXiv id in prose that the record has
since acquired is mechanically detectable. That is a lint rule nobody has asked
`luria` for yet.

### Added

- **Four origins the record had been citing second-hand, each read in full.**
  - Porian et al. 2024 (`LIT-690`).
  - Lin et al. 2023 (`LIT-689`).
  - Marigold (`LIT-691`).
  - Kingma and Gao 2023 (`LIT-692`).
- **Three practices, all `Proposed`.**
  - The scaling-law fitting protocol (`SOTA-421`).
  - Zero terminal SNR with v-prediction (`SOTA-422`).
  - Guidance rescale (`SOTA-423`).
- **Two theories.**
  - Kaplan and Chinchilla differ through counting, warmup and tuning, not the
    decay (`THEORY-108`, `Proposed`).
  - A monotone weighting makes the diffusion loss maximum likelihood on
    noise-augmented data (`THEORY-107`, `Active`).

### Changed

- **`SOTA-416` → `Active`** on its `promote_when`. Its attribution is corrected:
  Lin states the rule, credits the discretization to DPM-Solver, and never says
  "slight".
- **`SOTA-413` → `Active`** on the second clause of its `promote_when`.
- `SOTA-096` gains Porian et al. as a source for the exponent, not for the ratio
  of 20.

### Fixed

- **"Chinchilla identified the schedule" is corrected in `NOTE-017` and
  `NOTE-072`, and refined in `LIT-028`.** Only the warmup half of the schedule is
  a cause. `NOTE-072`'s open question is answered for language.
- **`LIT-688`'s description of Porian's steps is fixed.** It read as a chain
  through the decay row.
- **`THEORY-106`'s weighting identity is scoped to the unshifted cosine.** Its
  schedule-invariance step is re-cited to Kingma and Gao §3.2.
- **Smaller corrections.**
  - `SOTA-264`'s "nobody has run the comparison" is no longer true.
  - `SOTA-263`, `NOTE-351` and `LIT-687` name Lin as the origin where due.
  - `LIT-678` points at the now-held derivation.

### Added

- **Classifier-Free Diffusion Guidance** — `LIT-693`. Ho and Salimans (2022),
  `2207.12598`. The technique three practices turn on and nineteen other
  documents name, which this record had never held. Two of those practices
  acquired the dependency earlier today.

  **The method is a training change.** Replace the conditioning with a null token
  with probability `p_uncond`, so one network learns the conditional and
  unconditional scores together; at sampling, extrapolate away from the
  unconditional estimate. No classifier, no second model, and no classifier that
  has to be trained on noisy data.

  **`p_uncond = 0.1`** is the measured best — best achievable FID 1.55 at 0.1
  against 1.62 at 0.2 and 1.91 at 0.5.

  **The trade, with the numbers, because the paper's own wording inverts the
  sign.** ImageNet 64×64 at `p_uncond = 0.1`:

  | `w` | FID ↓ | IS ↑ |
  | --- | --- | --- |
  | 0.0 | 1.80 | 53.71 |
  | **0.1** | **1.55** | 66.11 |
  | 1.0 | 12.60 | 170.1 |
  | **4.0** | 26.22 | **260.2** |

  FID degrades about **seventeen-fold** while IS nearly quintuples. The paper
  writes this as "FID monotonically decreasing", meaning the FID *quality*
  decreasing — the number rising. Read that sentence without the table and you
  get the direction backwards.

- **`SOTA-424`**, `Active`/`universal` — the recipe, and the rule for
  choosing `w`: by which metric you are prepared to lose. **Never compare two
  models at different weights**, because a sweep can produce almost any FID or IS
  from one checkpoint.

- **`THEORY-109`**, `Proposed` — classifier guidance may flatter
  classifier-based metrics because it steps along a classifier gradient, and
  guidance without a classifier is the control.

  The paper raises it about its own predecessor: classifier-guided sampling "can
  be interpreted as attempting to confuse an image classifier with a
  gradient-based adversarial attack", and FID and IS are both computed with an
  Inception classifier. The trade surviving the classifier's removal is evidence
  it is real. What is *not* settled is the predecessor's magnitude, because the
  comparison is still scored with the same classifier — beating a suspect
  measurement at its own game says nothing about whether it was suspect. The
  `promote_when` asks for a metric with no classifier in it.

### Changed

- **`SOTA-307` v4 — its guidance items get their source**, with recommendation,
  status and consensus unchanged.

  It told a reader to search the classifier-free guidance scale per cell and
  quantified the noise ±0.05 on the scale injects, while the record held no paper
  for the technique. The new source supplies a much stronger argument than the one
  the document made: against a seventeen-fold FID swing from one checkpoint, a
  seed-noise floor is a rounding error, so fixing the weight is **prior to** any
  seed question rather than a refinement of it.

### Measured, not closed

`2105.05233` — Dhariwal & Nichol, the paper classifier-free guidance is named
against — remains unheld, and this record cites it four times as an instrument or
an authority: `LIT-448` says they "ablated" a design choice, `NOTE-340` uses their
U-Net, `LIT-630`'s controlled path comparison uses the same U-Net, and
`LIT-676`'s entire ImageNet table is run on their model. It is
deliberately not in this unit, on the same reasoning that kept Wettig out of the
BERT unit: filing both together would let the sourcing of one rest on the other.

### Added

- **Eleven papers from the reading-time triage, each read in full.**
  - Cramming (`LIT-681`).
  - Diffusion Meets Flow Matching (`LIT-678`).
  - ScheduleFree+ (`LIT-682`).
  - MuLAN (`LIT-677`).
  - The Marigold fine-tuning paper (`LIT-687`).
  - Hinton et al.'s distillation paper (`LIT-680`).
  - Fromage (`LIT-686`).
  - Sub-Scaling Laws / its ACL version (`LIT-685`).
  - Reconciling Kaplan and Chinchilla (`LIT-688`).
  - Model Merging in Pre-training (`LIT-684`).
  - Huginn (`LIT-683`).
  - H-Net (`LIT-679`).
- **Ten practices, all `Proposed`.**
  - Cut step time at constant parameter count under a fixed budget.
  - Filter text by tokenizer compression ratio.
  - A latent-conditioned per-dimension noise schedule, for likelihood.
  - Trailing timestep spacing for few-step sampling.
  - One-step end-to-end fine-tuning for dense geometry.
  - The soft-target distillation recipe.
  - Count the output head in scaling studies and fit with an offset.
  - Estimate the annealed score from a stable-phase checkpoint average.
  - A depth-recurrent core trained on random iteration counts.
  - Two-stage learned chunking for tokenizer-free models.
- **Two theories.**
  - Gaussian flow matching is a diffusion model, differing in weighting, output
    and schedule (`Active`).
  - Soft targets carry wrong-class similarity structure (`Proposed`).

### Fixed

- **`LIT-285` (Jadbabaie, Lin & Morse 2003) rewritten from a full reading.** The
  imported text gave the wrong condition (directed spanning tree, where the
  paper uses undirected joint connectivity), invented a corollary, and claimed a
  Vicsek result the paper declines to prove. `NOTE-136` and `NOTE-092` carry
  marked corrections.
- **Six sentences the new filings made false.**
  - `SOTA-140`: "nobody has run the two against each other".
  - `SOTA-156`: "no additional hyperparameter".
  - `SOTA-007`: "every model in this record tokenises this way".
  - `SOTA-403`: "nothing at current scale shares layers".
  - `LIT-028`: Chinchilla "identified" the schedule as the cause.
  - `THEORY-027`: now scoped to scalar schedules.

### Changed

- `SOTA-240` and `SOTA-257` gain second sources, and `SOTA-190` records an
  outside test.
- `LIT-052` gains `analysis-and-evaluation`.

### Documentation

- **The triage was wrong about four of the thirteen.** Jadbabaie was already
  held, as `LIT-285`. Marigold's fix does not make one step match fifty. Merging
  does not replace annealing. Fromage is not Muon's ancestor. Three of those
  errors came from adopting the paper's own framing, and one from a held-check
  keyed on a URL hash.
- **Universal sentences about the record's own contents go stale.** Four of the
  six fixes had the same shape, and a cheap sweep for them is proposed.

### Added

- **DPM-Solver++** — `LIT-676`. Lu et al. (2022), `2211.01095`. Re-measured
  from **last** among the remaining `#342` Tier B items to **first**, because the
  count was never the right question: `SOTA-203` is `Active` with
  `consensus: universal` and mentions guidance nowhere.

  ImageNet 256×256, classifier guidance 8.0, no thresholding, FID:

  | sampler | 10 NFE | 15 | 20 | 25 | 250 |
  | --- | --- | --- | --- | --- | --- |
  | DDIM — order 1 | **13.04** | 11.27 | 10.21 | 9.87 | 9.37 |
  | DPM-Solver-2 | 114.62 | 44.05 | 20.33 | 9.84 | — |
  | DPM-Solver-3 | 164.74 | 91.59 | 64.11 | 29.40 | — |
  | DPM-Solver++(2M) | 14.44 | **9.46** | **9.10** | **9.11** | — |

  **Monotone in the wrong direction** at 10 evaluations — 13.04, 114.62, 164.74
  for orders 1, 2, 3 — with PNDM and DEIS failing the same way, so it is a
  property of order under guidance rather than of one implementation. And the fix
  is cheap: 9.10 at 20 evaluations beats DDIM at 250.

- **`THEORY-104`**, `Proposed` — a large guidance scale amplifies the
  model's derivatives, which narrows a high-order solver's convergence radius.

  A `k`-th order method is built from `k`-th order derivatives and is therefore
  the most sensitive to the amplification, so the ordering **inverts** rather
  than flattening. `Proposed` because the paper says "intuitively" and "may" and
  never reports the derivative magnitudes: the FID inversion is measured, the
  reason is argued. The `promote_when` asks for a step-size-against-guidance
  sweep.

- **`SOTA-410`**, `Active`/`converged` — for guided sampling, use a
  second-order multistep solver on the data-prediction parameterization.

  Order 2 is the ceiling the authors accept ("high-order solvers may be
  unsuitable for large guidance scales"). The parameterization is not a detail:
  it is what makes `SOTA-202`'s per-step clamp available at all.

### Fixed

- **`SOTA-203` v2 — a `universal` recommendation bounded to the regime it was
  measured in.** Status and consensus unchanged; the claim was never wrong and
  its scope was never written.

  Its own rhetorical point was that "DDIM is exactly DPM-Solver-1 — the
  *first-order* case, the least accurate member of the family". Under guidance
  that **inverts**: DDIM becomes the most accurate of them at a small budget. The
  sentence now carries the qualifier and the document carries the table.

  **Why the gap survived.** Its `implementations` line reads "default or
  selectable sampler in essentially every diffusion serving stack" — which is
  exactly where guidance is on by default. A practice can name its deployment
  setting and still not have checked that setting's own defaults.

### Changed

- **`SOTA-202` v2 gains the precondition it never stated**, with recommendation,
  status and consensus unchanged.

  It says clamp `x̂₀` at every step. That assumes there *is* an `x̂₀` to clamp, and
  a high-order solver written on the noise prediction has intermediate stages
  where there is not — so the one fix this record already recommends is
  unavailable precisely at the large guidance weights that made it necessary.

  Two documents in this record now hold the same boundedness mechanism, reached
  from opposite directions: Imagen found it because high guidance was destroying
  images, and `LIT-676` found it because it broke an ODE solve. That
  convergence is the strongest support either of them has.

### Added

- **Model soups** — `LIT-675`. Wortsman et al. (2022), `2203.05482`. The
  paper `SOTA-407`'s consensus note named as unheld, in a sentence written
  earlier the same day.

  A hyperparameter sweep ends by discarding every model but one. Average them
  instead. **Uniform** averaging can come out *worse* than the best individual
  model — one ingredient from a different basin drags it down. The **greedy**
  recipe sorts by held-out accuracy and adds each model only if held-out accuracy
  improves, which makes it *"no worse than the best individual model on the
  held-out validation set"* **by construction**. `O(1)` at inference against an
  ensemble's `O(k)`.

  **+0.7 pp** on CLIP and **+0.5 pp** on ALIGN over the best sweep member. ViT-G
  on ImageNet: 90.78 → **90.94**, and 84.68 → **85.02** under distribution shift.

  Two things to read carefully. The state-of-the-art claim is 90.94 against
  CoAtNet-7's 90.88 — **0.06 pp** — while the same sentence reports **25% fewer
  inference FLOPs**; the second number is the durable one. And the NLP extension
  the abstract advertises is labelled "preliminary" in §3.3.3, where BERT greedy
  soups on four GLUE tasks gain **+0.0, +0.7, +0.0 and +0.5** — two of four gain
  nothing.

- **`SOTA-409`**, `Active`/`emerging` — average the fine-tuned models from
  your sweep instead of keeping only the best, adding each in validation order
  and only if it helps. `Active` on the guarantee rather than on the gains: the
  downside is bounded at zero on the selection metric by construction.

  Conditions worth having: the soup is free **given** a sweep, not free; the
  held-out set gets consumed by the greedy selection, so budget a third split;
  and every ingredient must come from one pretrained checkpoint.

### Changed

- **`SOTA-407` v2 — the dependency its own note named is resolved, and
  resolving it changes nothing.** Recommendation, status and consensus unchanged.

  The note wanted an adopter outside the authors' line of work. `LIT-675`
  shares a first author with this practice's source, so `DP-005` counts the two
  as one line of work rather than as a result and its replication. Consensus
  stays `emerging`; what changes is that the note now says why instead of leaving
  a paper unread.

  The image-classification limit is nuanced rather than lifted: the *family* has
  a non-vision data point, which its authors call preliminary and on which half
  the tasks gain nothing.

- **`SOTA-217` v3 — a third shared-trajectory case, and the boundary turns out to
  be a spectrum.**

  A shared initialization is **not sufficient**. The greedy soup recipe exists to
  "avoid adding in models which may lie in a different basin of the error
  landscape", which the paper says can happen "if, for example, models are
  fine-tuned with high learning rates". So: a shared start makes averaging
  usually safe, a per-ingredient check makes it reliably safe, and this
  practice's permutation alignment is what is left for networks that share
  nothing. Three points on a line, not two sides of one.

- **`LIT-478` v3** — model soups comes off the list of what the family is missing.
  Snapshot ensembles and Polyak averaging remain. Keeping the list current is the
  point of having written it.

### Added

- **`src/scripts/audit/reading_time.py`**, which ranks the papers-feed
  tracker by cumulative active reading time and prints the works no LIT
  note holds. It merges the several keys the feed files one paper under, which
  are an arXiv id, an `arxiv.`-prefixed id, a URL hash and a bare title. It
  does not key on the Cloudflare "Just a moment..." title, which 169 unrelated
  sessions share. Tested in `tests/test_reading_time.py`.

### Documentation

- **Reading time, triaged as a candidate queue.** 87 unheld works have ten
  minutes or more of reading. 14 rows (13 works) are promoted under the
  substrate, trunk and claim reasons, 16 are held back, and 57 are declined
  with a code on each. Nothing was filed. The two strongest substrate finds
  are **Cramming**, which the feed holds only under a PDF hash, and **Hinton
  et al.'s distillation paper**, which is missing although 110 documents
  mention distillation.
- **The two rankings disagree in the one-to-four-session band.** The revisit
  worklist has exhausted its high-session tail. Eight of the promoted rows sit
  below 150th by revisits.
- **47% of the band's reading time goes to subjects no topic holds**:
  quantum foundations, network science, complex systems, and law and
  politics. This is recorded as a scope question for the owner under
  `ADR-059`. `ADR-052`'s rejection of those topics stands until someone
  decides otherwise.

### Added

- **Averaging Weights Leads to Wider Optima and Better Generalization** —
  `LIT-673`. Izmailov et al. (2018), `1803.05407`. The paper `LIT-478` named
  as the first thing missing here, and the baseline `SOTA-288`'s promotion
  condition asks for by name — a condition the record could not have checked,
  because the baseline was not in it.

  ImageNet top-1 from pretrained torchvision checkpoints, ten further epochs
  under one shared cyclical schedule, mean of three runs: ResNet-50 **76.15 →
  76.97 ± 0.05**, ResNet-152 **78.31 → 78.94 ± 0.07**. Better than +1.3% on
  CIFAR-100 and +0.4% on CIFAR-10. At one model's inference cost — the paper's
  framing is that it "approximates Fast Geometric Ensembling with a single
  model".

  And the part people skip: with batch normalization the stored running
  statistics belong to the visited weights, not their average, so **one extra
  pass over the data** is required. Omitting it breaks the model rather than
  costing a fraction of a point.

- **Robust fine-tuning of zero-shot models** — `LIT-674`. Wortsman et al.
  (2021), `2109.01903`. Tier B of `#342`, promoted within the tier once
  `LIT-478`'s claim was checked.

  Ship `(1 − α)·θ_zero-shot + α·θ_fine-tuned`. At **α = 0.5**, accuracy under six
  distribution shifts rises by **3.5, 6.2, 1.7, 2.1, 9.0 and 23.2 pp** against
  the fine-tuned model while reference accuracy falls **by at most 0.3 pp** and
  often improves. Not a trade-off dial: intermediate `α` beats **both**
  endpoints on **both** axes, at no cost in training or inference.

  It also states the precondition the record most needed, in one sentence:
  averaging all layers of unrelated networks "typically fails, achieving no
  better accuracy than a randomly initialized neural network" — this works
  because the fine-tuned weights came *from* the zero-shot ones.

- **`SOTA-407`**, `Active`/`emerging` — interpolate the zero-shot and
  fine-tuned weights at about half way rather than shipping the fine-tuned model.
  `Active` because the recommendation is free and the downside is bounded at
  0.3 pp.

- **`SOTA-408`**, `Proposed`/`converged` — average the weights along the
  tail of training under a cyclical or high constant learning rate, then
  re-estimate the normalization statistics.

  The `ADR-015` corner used deliberately. SWA ships in
  `torch.optim.swa_utils` and appears across this record as a baseline, so not
  doing it is not what needs justifying; and every measurement the record holds
  is 2018 convolutional vision against SGD. The `promote_when` asks for a
  transformer and a modern optimizer, and explicitly refuses to count a model
  report that lists SWA without an ablation.

### Fixed

- **`LIT-478` v2 — a claim about the record's own contents that was false the
  day it was written.**

  Its "Why it's here" read: *"The record has nothing on weight-space ensembling.
  No stochastic weight averaging, no model soups, no snapshot ensembles, no
  Polyak averaging."* On 2026-09-21, when that was written, the record held
  `SOTA-217`, `THEORY-010`, `LIT-333` and `LIT-251` — the permutation-alignment
  half of weight averaging, all filed 2026-09-15.

  What was actually missing is the **shared-trajectory** half, where no alignment
  is needed, and that is what this unit files. Model soups, snapshot ensembles
  and Polyak averaging remain absent. The wrong sentence is quoted rather than
  deleted: a note explaining why a paper was filed should show what the reasoning
  was.

### Changed

- **`SOTA-217` v2 gains the scope line it was missing** — when the alignment step
  is *unnecessary* — with recommendation, status and consensus unchanged.

  It tells you to align hidden-unit permutations before averaging weights from
  separately trained networks. It never said what "separately" was doing, and
  two practices filed today average weights with no alignment at all. The test
  before averaging is not whether two networks share an architecture or a task
  but **whether one of the weight vectors came from the other**. `LIT-674`'s
  sentence about unrelated networks scoring no better than random initialization
  is now quoted there, because it is simultaneously the bound on this practice
  and the sharpest argument for it.

### Added

- **Should You Mask 15% in Masked Language Modeling?** — `LIT-672`. Wettig,
  Gao, Zhong and Chen (2022), `2202.08005`. The sweep BERT never ran, taken as
  the ranked follow-up to the previous unit rather than folded into it.

  **The optimum tracks capacity, not the signal**: 40% at 354M parameters, 20%
  at 124M, 15% at 51M, under an efficient pre-training recipe. At 354M, 40% beats
  15% on seven of nine GLUE-plus-SQuAD tasks — SQuAD +1.8, RTE +2.0 — and loses
  SST-2 by 0.2 and CoLA by 1.1. The efficiency framing is stronger than the
  accuracy one: **on QNLI and QQP, 40% reaches the 15% model's score in half the
  training time.** The authors also report the advantage shrinking under longer
  and more expensive recipes, which is in the note.

  **80% masking still works, and that is the result with teeth.** Validation
  perplexity above **1,000** — nothing can be reconstructed — while **95% of
  fine-tuning performance** and **90% of BLiMP probing accuracy** survive against
  the 15% baseline.

  **The decomposition.** A masking rate sets a corruption rate and a prediction
  rate at once, and they are **antagonistic**: untied, lowering corruption at
  fixed prediction improves monotonically, and raising prediction at fixed
  corruption helps.

- **`SOTA-405`**, `Proposed`/`unreplicated` — scale the masking rate with
  model size rather than holding it at 15%. `implementations: []`, because 15%
  is still the default everywhere, which is inertia and not evidence (`DP-005`).

- **`SOTA-406`**, `Proposed`/`unreplicated` — replace every masked token
  with `[MASK]`; drop BERT's 80-10-10 rule.

  Against a 40% all-`[MASK]` baseline, 80-10-10 is worse on everything but
  SST-2, and its stated motivation does not bite: "the model can adapt to full,
  uncorrupted sentences, regardless of the use of alternative corruption
  strategies in pre-training". The rule's own evidence was always thin —
  BERT's Appendix C.2 scores 80/10/10 at **84.2** on MNLI against **84.3** for
  all-`[MASK]`, so the condition being dropped was already behind.

### Fixed

- **`THEORY-088` v2 — the account lost a term, and its promotion condition was
  confounded.**

  It claims the masking optimum is a property of the signal's information
  density. Within one signal, the optimum moves **by capacity** (a factor of
  nearly three across 51M–354M) and **by masking strategy** (uniform admits a
  higher rate than span or PMI masking). Neither is a property of text.

  And the mechanism's link to reconstruction is severed: redundancy governs
  whether hidden content can be recovered, and at 80% masking nothing can be
  recovered while 95% of fine-tuning performance survives.

  The `promote_when` asked for a cross-modality correlation against a measured
  redundancy statistic. It now also requires **one capacity and one masking
  strategy**, because a correlation drawn from models of different sizes measures
  capacity as much as redundancy.

- **`LIT-668` v2 — a statement about the record's own contents that this
  session falsified.**

  Its "gap this reading measured" paragraph said BERT and RoBERTa were in the
  record in no scheme. Both were filed the same day. The paragraph is updated
  rather than deleted, because the finding was that note's and the measurement
  is what made the next unit obvious. Changelog fragments and curation entries
  from the same day are deliberately **not** touched: they are dated statements
  about a moment, and a reading note's standing section is a live statement about
  now.

### Changed

- **`SOTA-373` v3 — the question v2 left open is answered**, with
  recommendation, status and consensus unchanged for the third version running.

  v2 said this practice's text anchor was "an unexamined default rather than a
  rival datum" and named the paper that would settle it. It arrives: the text
  optimum is higher than 15% and depends on the model, so the five-fold gap this
  practice was explaining is nearer two-fold once both sides are measured.

  **Do not inherit the number** is stronger advice now, not weaker — the
  inherited number was wrong in its own modality. What the document no longer
  claims is that the 75%-against-15% gap is explained by the signals.

- **`SOTA-404` v2 — a third source, and the first constructive one.**

  The other two tripped over the confound. This one names it, builds the
  corruption/prediction decomposition, and uses it. The word worth keeping is
  **antagonistic**: where the other cases had two quantities pushing the same
  way and hiding an attribution, here they push opposite ways, so the confound
  can hide an effect entirely — a sweep that finds nothing may be watching two
  real effects cancel. Status unchanged, because this is a third reversal and the
  `promote_when` asks for a conclusion that survives.

### Added

- **Lines of explanation** (`docs/theory-lines.md`, [ADR-061](record/decisions.d/ADR-061.md)). A third
  chain walks `extends:` and `corrects:` between theories, as `lineage` does
  for papers and `practice` for recommendations. It shows which account
  refined another and which replaced one whose reasoning broke. There are 11
  lines on the record as filed, all bound by a shared topic, and seven of the
  theories on them correct an earlier account. Listed in `docs/README.md`.

### Added

- **BERT: Pre-training of Deep Bidirectional Transformers for Language
  Understanding** — `LIT-670`. Devlin et al. (2018), `1810.04805`. The gap
  the previous unit measured and left open: **89 files in this record said
  "BERT"**, 51 of them reading notes, practices or explanations, and the record
  held no BERT.

  Two things it is cited for here are not in it.

  **The 15% was never swept.** *"In all of our experiments, we mask 15% of all
  WordPiece tokens in each sequence at random."* The one appendix table on
  masking is headed **"Masking Rates"** and is a trap: its columns are
  `Mask / Same / Rnd` and every row fixes the selection rate at 15% while
  varying the 80/10/10 substitution mix — which barely matters, 84.2 against
  84.3 on MNLI for 80/10/10 against 100/0/0.

  **The NSP ablation removes a loss and keeps its input format.** `No NSP` is
  described only as MLM "without the next sentence prediction task", and the
  paired-segment construction stays. Of the three drops the paper calls
  significant, one carries it: QNLI **−3.5**, against MNLI −0.5 and SQuAD −0.6.

  What is solid is the bidirectionality comparison, which changes one thing:
  `LTR & No NSP` falls to 77.5 on MRPC and 77.8 on SQuAD from 86.5 and 87.9.

- **RoBERTa: A Robustly Optimized BERT Pretraining Approach** —
  `LIT-671`. Liu et al. (2019), `1907.11692`. Filed beside BERT because
  either alone misleads.

  It names the confound: *"It is possible that the original BERT implementation
  may only have removed the loss term while still retaining the segment-pair
  input format."* Split into four conditions, the attribution inverts — keeping
  the loss and shortening inputs to single sentences **hurts**, while dropping
  the loss and packing contiguous text **matches or slightly improves**.

  **BERT was undertrained**: same architecture, objective and 16GB corpus at
  100K steps gives SQuAD 1.1/2.0 **94.0/87.7** against **90.9/81.8**, MNLI-m
  **89.3** against **86.6**. Read with care — that row already carries four
  recipe changes and a much larger batch, so it is the recipe *and* the compute.

  And two of its own results are smaller than their adoption: dynamic masking
  is "comparable or slightly better" (**78.3 → 78.7** SQuAD 2.0, **84.3 →
  84.0** MNLI-m — one goes the wrong way), and byte-level BPE is adopted having
  been found *"slightly worse end-task performance on some tasks"*. It ships
  `full-sentences` though `doc-sentences` scores higher.

- **`SOTA-404`**, `Proposed`/`unassessed` — when you ablate an auxiliary
  loss, ablate the input construction that came with it, or the result is about
  both.

  Two sources in two literatures. RoBERTa on NSP, and `LIT-667` on grokking,
  where four papers varied the training fraction of a fixed universe and so
  could not separate dataset size from dataset composition. Neither drew the
  general lesson. The `promote_when` asks for the case the record is missing —
  a re-run where the original conclusion **survives** — because a record that
  only collects reversals will overstate the rate.

### Fixed

- **`SOTA-373` v2 — a consensus note that made a false claim about the record's
  own contents, and an anchor that was never measured.** Recommendation,
  status and consensus unchanged.

  The note called BERT one of "the two masked-prediction documents it holds".
  The record held one. That is the second time a consensus note has asserted
  something structural about unfiled papers — `SOTA-365` was the first, yesterday —
  and it is now true rather than merely repaired.

  The substantive half: the practice contrasts MAE's swept 75% against "BERT's
  15%", and **only one of those is a measurement**. Neither BERT nor RoBERTa
  ever varied the rate. So "the ratio that worked on text" names a number that
  was declared in 2018 and inherited since — which *strengthens* the half of
  the recommendation that says do not inherit the number, and removes the
  reading where 15% and 75% are two measured optima whose gap needs explaining.

  Ranked as the follow-up: Wettig et al. (2022), `2202.08005`, which sweeps the
  text side and reports a higher optimum.

### Added

- **`LIT-669`, Kanerva's *Sparse Distributed Memory and Related Models*
  (RIACS TR 92.10, 1992; published 1993 in Hassoun (ed.), *Associative Neural
  Memories*).** Read in full from NASA's Technical Reports Server. It restates
  SDM as a matrix memory, with recall `z(YYᵀW)` weighted by activation
  overlaps. It gives the signal-to-noise optimum `p = (2MT)^(-1/3)` and a
  capacity of about 10% of the number of locations. It relates SDM to
  correlation-matrix memories, feed-forward nets and the cerebellum.
  `LIT-669` extends `LIT-666`, and `LIT-641` now extends both.

### Changed

- **`LIT-666` v2 corrects which optimal radius is the book's.** `LIT-641` §1
  cites all three of the radii it fits β against to the review. The review has
  the signal-to-noise and capacity analyses but no critical distance, which
  `LIT-641`'s own Appendix B.5 reproduces from the book's Figure 7.3.
  `LIT-666` had followed §1. It now credits critical distance to the book,
  and answers one of its two open questions from `LIT-641` Appendix B.1.
- `THEORY-097` names the source of each of the three optima.

### Added

- **ALBERT: A Lite BERT for Self-supervised Learning of Language
  Representations** — `LIT-668`. Lan et al. (2019), `1909.11942`. Tier B
  unit 3 of `#342`, ranked on **17 documents saying "ALBERT" against zero
  practices** and moved to the front of the tier by the previous unit, which
  made cross-layer parameter sharing load-bearing here.

  The sharp result is an **asymmetry**. On an ALBERT-base configuration,
  averaged over SQuAD 1.1/2.0, MNLI, SST-2 and RACE:

  | sharing | params (`E=128`) | Avg | params (`E=768`) | Avg |
  | --- | --- | --- | --- | --- |
  | not shared | 89M | 81.6 | 108M | 82.3 |
  | attention only | 64M | **81.7** | 83M | 81.6 |
  | FFN only | 38M | 80.2 | 57M | 79.5 |
  | all shared | 12M | 80.1 | 31M | 79.8 |

  Sharing every attention block is free; sharing the feed-forward blocks costs
  −1.4 and −2.8.

  Three further things the record wanted. **Sentence order prediction against
  next sentence prediction**, with the mechanism in the intrinsic numbers: an
  NSP-trained model scores **52.0% on SOP**, which is chance, while an
  SOP-trained model scores **78.9% on NSP** — NSP is solvable from topic
  overlap. **Fewer parameters is not less compute**: ALBERT-xxlarge has fewer
  parameters than BERT-large and **3.17× lower throughput**, which the
  discussion concedes in its first sentence — and the equal-wall-clock
  comparison, which is the one that settles it, still favours ALBERT by **+1.5
  average and +5.2 on RACE**. And **dropout hurting a large transformer**,
  claimed as a first and bounded in the same paragraph.

- **`SOTA-403`**, `Proposed`/`unreplicated` — share the attention
  parameters across layers if you need to cut parameters; do not share the
  feed-forward ones.

  Filed as a practice rather than an explanation because the asymmetry has a
  number and no mechanism. `implementations:` is deliberately empty: ALBERT
  itself ships all-shared, the configuration its own ablation scores **1.6
  lower**, because the parameter saving was the point of the paper. This is a
  recommendation nobody has shipped, including the group that measured it.

### Changed

- **`THEORY-103` v2 — the fix it endorses is priced.**

  That account's strongest evidence is an intervention: tying the two halves of
  the stack takes out-of-distribution composition from flat zero at two million
  steps to generalizing. ALBERT ran the same change on natural text for a
  different reason and found the **feed-forward half is the expensive one** —
  which is the half the account needs shared, because the per-layer store it is
  about *is* the feed-forward block. The fix is not free, and it is not free for
  the reason the account gives.

  That yields an untested implication, filed as one: if the cost of sharing the
  FFN is the loss of per-layer storage, it should fall hardest on whatever the
  upper layers were storing separately.

  **And the sign is contested.** Universal Transformer, whose scheme the source
  borrowed, reports sharing as a *gain*; ALBERT reports it as a loss and names
  the disagreement — *"Different from our observations"*. The record holds
  neither that paper nor a reconciliation.

- **`SOTA-240` v3 — this document's own admission becomes a reported result**,
  with recommendation, status and consensus unchanged.

  v2 said that where the sweet-spot curve leaves large-scale pretraining "is an
  inference, not a reported result", and that the record had not confirmed why
  current recipes set dropout to zero. ALBERT is one confirmation, from 2019 and
  in the same terms: the model does not overfit after 1M steps, so dropout came
  out, and **90.4 → 90.7 average** with every task improving.

  Still not a statement about current recipes — one 2019 encoder with an unusual
  architecture, and 0.3 points is a confirmation rather than a large effect. The
  caution in v2 stays.

### Fixed

- Nothing. This unit found no defect, which is worth recording after four units
  that each found one — and the reason is that the gap here was an **absence**
  rather than a wrong attribution.

  Measured and left open: neither `1810.04805` nor `1907.11692` — BERT and
  RoBERTa — is in this record in any scheme, while **89 files say "BERT"**, 51 of
  them reading notes, practices or explanations. `THEORY-066` and `LIT-530`
  measure rank collapse on it, `LIT-303` and `LIT-316` use "ALBERT-style layer
  sharing" as an instrument, and this unit's own subject is a *lite* one. The
  record has been reasoning about a model it does not hold. Filed as a finding;
  it wants its own unit.

### Added

- **`LIT-666`, Kanerva's *Sparse Distributed Memory* (MIT Press,
  1988).** The associative memory that `LIT-641` shows attention
  approximates. The record held that account as `THEORY-097` without holding
  its subject. `LIT-641` now `extends` it, and `THEORY-097` cites it where
  it describes the memory.

  Filed from secondary accounts. The book is not openly available, so the
  note rests on OSTI's catalogue abstract and `LIT-641`'s review of the model,
  and says which takeaway rests on which. The optimal-radius criteria that
  `LIT-641` fits β against come from Kanerva's 1993 review, which is not held,
  so they are not attributed to the book. The source is the publisher's URL:
  the book has no DOI in Crossref, and ACM's `10.5555/534853` does not resolve.

### Added

- **Grokked Transformers are Implicit Reasoners** — `LIT-667`. Wang, Yue,
  Su and Sun (2024), `2405.15071`. Tier B unit 2 of `#342`, ranked on **41
  documents saying "grokking" against one practice**. The count was the wrong
  reason: the grokking cluster was already eight notes and six explanations
  deep. The right reason is that the paper **contradicts a claim two of those
  explanations make**.

  Grokking on knowledge-based reasoning, which nobody had reported. An 8-layer
  GPT-2 on a synthetic knowledge graph reaches **>99% training accuracy at ~14K
  steps**, with in-distribution test accuracy **no higher than 9.2% at any
  point before then**, and near-perfect test accuracy after roughly **50× the
  steps it took to fit**.

  Two sweeps that separate what the algorithmic literature moves with one knob:
  hold the inferred/atomic ratio `φ` and scale the data — **nothing changes**;
  hold the size and raise `φ` — grokking accelerates monotonically, and at
  **`φ = 18.0` it is gone** (96.7% before training accuracy saturates). The
  paper names the hypothesis it corrects, *critical data size*, and proposes
  **critical data distribution**.

  And the out-of-distribution split: composition **never** generalizes, out to
  **2 million steps**; comparison does.

- **`THEORY-103`**, `Proposed` — a transformer stores a fact where it
  needed it, so two-hop composition generalizes only to facts it already saw as
  a second hop.

  Causal tracing gives two circuits. Composition's is **sequential**: the lower
  layers resolve hop one and park the bridge entity, the upper layers look up
  hop two — which requires a **second copy of the atomic facts upstairs**,
  containing only those that appeared as a second hop in training. Comparison's
  is **parallel**: both lookups happen downstairs, one copy, nothing missing.

  The failure is localized, not diffuse: **in the OOD setting the bridge entity
  and the second relation are still correctly encoded** at layer 5. The first
  hop works on facts the model never composed. And the fix derived from the
  account was run — tying layers 0–3 to 4–7 after Universal Transformer takes
  OOD composition from flat zero to generalizing, slowly.

  `Proposed` and not `Active`, against `THEORY-101` and `THEORY-102`: the
  intervention succeeded, but it is reported as a figure with no number, and
  every measurement is on a synthetic knowledge graph.

- **`SOTA-402`**, `Proposed`/`unreplicated` — to teach a model to reason
  over facts it holds, spend added data on facts **derived from** other facts
  rather than on more atomic facts.

  It takes both sweeps to say this. Raising `φ` also raises the data volume, so
  the `φ` sweep alone would not attribute the effect; the size sweep at fixed
  `φ` is what shows the volume is inert.

  What it does not buy: **systematicity**. Across every `φ`, out-of-distribution
  composition stayed at zero.

### Fixed

- **`THEORY-071` v2 — "at a critical dataset size" was wrong, and the
  `promote_when` asked for a quantity that does not exist.**

  The title now reads *"...which one wins flips when the data makes memorising
  more expensive"*. The circuit-efficiency crossover survives; what it is
  indexed on does not. `C_mem` must store the inferred facts as well as the
  atomic ones while `C_gen` stores the atomic facts twice at most, so the
  *ratio* is what the regularizer sees, and **dataset size was a proxy for it**
  in a setting where every example is an inferred fact.

  The previous condition asked for *"a measured `D_crit` ... outside algorithmic
  data"*. The paper that went outside algorithmic data reported there is no
  `D_crit` there to measure. **A promotion condition can be met in spirit and
  refuted in letter at the same time**; the condition is rewritten rather than
  read as satisfied, and now asks for the efficiency ordering to be *measured*
  on networks that actually grok — which is what was never done, in either
  setting.

  The reverse inference is explicitly withheld: modular addition has no
  atomic/inferred split, so nothing here says the algorithmic size dependence
  was secretly a distribution effect. Only that those experiments could not have
  told.

### Changed

- **`THEORY-069` v2 — the first of its three knobs is qualified, and it keeps
  `Active`.**

  Every measurement behind "training-set size" varies the training *fraction* of
  a fixed universe, which moves size and composition together. The knob is real;
  **what it is a knob on is open.** The heading now says so.

  The unanimity argument is corrected with it: "a dataset-size condition appears
  in all four papers" was the document's reason for holding this above the
  mechanisms that disagree, and agreement among four papers that could not
  separate size from composition is not evidence about which it was.

  Not counted as a fourth knob, deliberately — on `THEORY-071`'s amended
  reading the ratio is the first knob seen properly, and counting it twice would
  claim an independence nobody has shown.

  What *has* narrowed is the document's own "what would change this": grokking
  here arrives at a **standard initialization, in a standard optimizer, with
  nothing inflated or constrained**. The remaining gap is no longer the
  initialization. It is that every setting anyone has watched grokking in has a
  data distribution somebody chose.

- **`SOTA-279` v2 gains the first measured counter-case it has held**, with
  recommendation, status and consensus unchanged.

  Its consensus note already said the evidence was one 2022 paper plus
  everything built on it since. Here is a 2024 measurement: on a deduction task
  over 28.2K in-context facts, against **33.3% for chance**, Gemini-1.5-Pro
  scores **28.7% direct against 11.3% verbalized**, and **37.3% against 12.0%**
  with retrieval. GPT-4-Turbo is at chance either way. The failure is legible —
  **70.7% of the verbalized responses conclude the answer cannot be decided**
  when it can.

  And the existing condition on rationale correctness gets much worse. Wei et
  al.'s own error analysis found two of fifty correct answers reached by
  incorrect reasoning; here, on a task where the proofs are mechanically
  checkable, **most** of the rationales behind correct answers are wrong. That
  one is from inspection with no count, and is recorded as a reason to score the
  rationale rather than as a rate.

  The paper does not say how it elicited the verbalization, so this bounds a
  regime rather than singling out exemplars, and lands on `SOTA-280` and
  `SOTA-281` equally.

### Changed

- `LIT-640` (QK-norm) is tagged `model-architecture` as well. QKNorm changes
  the attention block itself, and the tag binds the lineage it sits in with
  `LIT-641` and `LIT-651`, which both carry it — clearing the one unbound
  line the lint reported since luria 0.30.0.

### Added

- **Transformer Language Models without Positional Encodings Still Learn
  Positional Information** — `LIT-665`. Haviv et al. (2022),
  `2203.16634`. Tier B unit 1 of `#342`, `#290`'s promotion [#15](https://github.com/dmarx/anthology-of-the-sota/issues/15), ranked on **45
  documents saying "positional encoding", 23 saying "NoPE" and 8 practices**.

  Causal LMs with **no positional information at all** are competitive: 0.05
  perplexity from learned embeddings at 1.3B on the Pile, 0.55 on
  WikiText-103 — where five seeds of the sinusoidal baseline span up to 0.9, so
  that gap sits inside seed noise.

  Probing says where the position comes from: **absent at layer 1** (random
  baseline), position-aware **within four layers**, as accurate as learned
  embeddings by mid-network. Shuffling the suffix moves token-level loss from
  ~4 to ~11, so it is load-bearing.

- **`THEORY-102`**, `Active` — the causal mask is itself a positional
  encoding, because a token that can count its attendable predecessors knows
  its index.

  `Active` on one source for the reason `THEORY-101` is: **the account
  predicted a failure and the failure was produced.** Remove the mask and the
  mechanism should vanish — a bidirectional MLM without an encoding does not
  degrade, it **fails**, at **147.18 perplexity against 4.00** for
  position-aware baselines. Thirty-six times worse, in the same paper, with
  Sinha et al. (2021) having independently seen the effect.

### Fixed

- **`LIT-207` v2 and `SOTA-153` v3 — the record had attached a result to the
  paper that used it.**

  `SOTA-153`'s source comment read: *"`LIT-207` is not a hybrid paper — it is
  the result the other three rest on — but it is the source of the claim that
  the global layers lose nothing by dropping the encoding."* `LIT-207` is
  Kazemnejad et al., **2023**, and its summary here read *"A decoder-only
  transformer without positional encoding is shown to represent both absolute
  and relative position anyway."*

  **The absolute half of that is Haviv et al., 2022**, with the probing and the
  mechanism. `LIT-207`'s own contribution is the length-generalization
  comparison — five schemes under identical hyperparameters, and the one that
  extrapolates is none at all — plus the relative-position half. Both documents
  now say which is which.

### Changed

- **`SOTA-153` gains the account and two bounds**, with recommendation, status
  and consensus unchanged.

  **Why a layer can go without an encoding at all** was not in any of the
  hybrid papers this practice cites. It is now, with the mechanism.

  **The mechanism is causal, so it is available to a decoder and to nothing
  else** — the MLM control is the evidence, and nothing about this layout
  transfers to an encoder.

  **Position accumulates over depth rather than arriving at the input.** A
  hybrid is choosing among layers that differ in how much implicit position has
  built up by the time they run, and **no document in this record says what
  that does** — including the new ones. That is the obvious open question the
  layout raises.

  **"Lose nothing" was too strong.** Haviv et al.'s own limitations section
  says NoPos is *"always slightly worse"*, and their scale sweep shows smaller
  models benefiting from fixed non-parametric encodings with the gap closing as
  scale grows. What NoPE *wins* is extrapolation past the training length —
  `LIT-207`'s result, not this one's. The practice stands on the extrapolation,
  not on parity.

### Added

- **Emerging Properties in Self-Supervised Vision Transformers** —
  `LIT-664`. Caron et al. (2021), `2104.14294`. **The origin of the DINO
  line**, which 31 documents here reference and 12 practices touch.

  Self-supervised ViT features carry explicit semantic segmentation that
  supervised ViTs and convnets do not show as clearly, and reach **78.3%
  ImageNet top-1 with a bare k-NN** — no finetuning, no linear classifier, no
  augmentation. DINO is self-distillation with no labels: a student predicting
  a momentum-encoder teacher through cross-entropy.

  The immediate reason to file it is a number this record printed yesterday.
  The registers note reports DINOv2 at 35.3 corloc on VOC 2007 against **DINO's
  61.9** — its headline evidence — cited against a paper the record did not
  hold.

- **DINOv3** — `LIT-663`. Siméoni et al. (2025), `2508.10104`. The finding
  is not the model:

  **Train a self-supervised ViT long enough and its dense features rot while
  its global metrics keep improving.** ImageNet linear-probe top-1 rises
  monotonically for ViT-g and ViT-7B; Pascal VOC segmentation mIoU **declines
  after ~200k iterations** and for the 7B *"fall[s] below its early levels."*
  The authors name the consequence: *"a relative independence between learning
  strong discriminative features and maintaining local consistency."*

  What degrades is **locality** — the similarity map from a reference patch goes
  from *"smooth and well-localized"* at 200k to *"substantially"* degraded by
  600k, while CLS-to-patch similarity climbs throughout.

  **And it is not the defect registers fixed**, which they say outright:
  *"These patch-level irregularities differ from the high-norm patch outliers
  described in Darcet et al. 2024… with the integration of register tokens,
  patch norms remain stable throughout training."* Same group, confirming their
  own earlier fix worked and did not cover this.

- **`SOTA-401`**, `Proposed`/`unreplicated` — Gram anchoring. Keep an
  early EMA teacher and pull the student's patch **similarity structure**
  toward it: `L_Gram = ‖X_S·X_Sᵀ − X_G·X_Gᵀ‖²_F` on `L2`-normalized patch
  features, global crops only, teacher refreshed every 10k iterations.

  The design point is theirs: *"By operating on the Gram matrix rather than the
  features themselves, the local features are free to move, provided the
  structure of similarities remains the same."* Can be started late — after 1M
  iterations — and *"still manages to 'repair' very degraded local features"*,
  with gains inside 10k iterations.

  The condition worth carrying past the loss term: **the trigger is a dense
  metric, not a global one.** If you are not tracking a patch-level benchmark
  through training you cannot tell whether this applies to you.

### Fixed

- **`SOTA-365` v2 — a factual claim about a paper the record did not hold.**

  Its consensus note said the unfiled `#304` units, *"DINO and DINOv2 — carry
  the same structure"*: predictor plus stop-gradient. **They do not.** DINO
  avoids collapse with *"only a centering and sharpening of the teacher
  output"*, and has no predictor on either branch.

  So the asymmetric-predictor family is one route to learning without negatives
  and the DINO line is a **second**. The recommendation is unchanged and
  `converged` is kept, with its grounds narrowed: it describes the predictor
  family, not negative-free learning in general.

### Changed

- **`LIT-599` v3 — placed in its lineage, both ends of which the record now
  holds.** Two dense-feature defects in this recipe, both characterized
  afterwards by the same group, on different axes:

  | defect | axis | remedy |
  | --- | --- | --- |
  | high-norm token artifacts | model **size** (ViT-L+) | registers |
  | loss of patch locality | training **duration** (~200k iters) | Gram anchoring |

  DINOv3 reports the second as present *"to a lesser extent, during the training
  of DINOv2"*. This note's thesis — curation plus scale gives general-purpose
  features — holds on the evaluations run, and **both things that went wrong
  were invisible to them.**

### Added

These are the remaining open items of `#331`.

- **simple diffusion** (`LIT-660`, 2301.11093) and **On the
  Importance of Noise Scheduling for Diffusion Models** (`LIT-659`,
  2301.10972). They are concurrent January 2023 papers and together
  originate the resolution-dependent noise-schedule shift, with controlled
  measurements. On ImageNet 256, FID goes from 7.65 to 3.76 (simple
  diffusion Table 2) and from 7.21 to 3.52 (Chen Table 4).
- **W.A.L.T** (`LIT-661`, 2312.06662). It is the only ablation found
  that switches a separate image corpus on and off for video diffusion: FVD
  598.8 → 344.5 at 419M, with compute not stated. Separately, windowed
  hybrid attention matches full 3D attention on UCF-101 at 1.7× the speed.
- **FiT** (`LIT-658`, 2402.12376). The one generative measurement of
  aspect-preserving training. At a square 256² output, FID moves
  44.83 → 43.34 with a worse sFID. The large non-square gains are against a
  baseline that never trained on those shapes.

### Changed

- **`SOTA-263` v3 is now `Active`,** and its consensus is `emerging`.
  `promote_when` asked for an ablation of what the shift is worth, and
  simple diffusion published one 14 months before the practice was filed.
  `introduced_by` moves from SD3 to the two 2023 papers, since SD3 credits
  Hoogeboom et al. for the log-SNR shift. The practice now says that the
  direction is measured, while the magnitude is tuned in every source and
  never taken from the formula. SD3 derives α = 4 and uses 3.0.
- **`LIT-449` v2 (SD3)** no longer calls the shift new. It now records the
  Fig. 6 preference sweep that `SOTA-263` had called qualitative.
- **`SOTA-305` v2 and `SOTA-307` v3** add cases from the video line's
  readings. `SOTA-305` gains:
  - MAGVIT-v2's vocabulary step, a rate increase at fixed token count.
  - Step-Video's "8 times" compression, which is 2× in information.
  - LTX-Video's token-ratio comparison.
  - Open-Sora 2.0's equal-rate Table 1, which follows the rule.

  `SOTA-307` gains MAGVIT-v2's 1.78 against 1.79, which falls inside the
  floor.
- **`SOTA-386` v4** adds W.A.L.T as a source and stays `Proposed`, because
  compute is not stated.
- **`SOTA-390` v3** adds W.A.L.T's window-attention result as a condition
  that points the other way, at 128px and 17 frames.
- **`SOTA-398` v2** adds FiT as the one measured generative case.
- Eight `inactive-ok` directives that vouched for `SOTA-263` as
  `Proposed` were removed or narrowed, now that it is `Active`.

### Added

- **Vision Transformers Need Registers** — `LIT-662`. Darcet, Oquab,
  Mairal and Bojanowski (2023), `2309.16588`. Unit 6 of `#342` and the last of
  its Tier A. `#290`'s promotion [#12](https://github.com/dmarx/anthology-of-the-sota/issues/12), ranked on **107 documents naming ViT**
  with the defect-and-fix unheld.

  The characterization, measured from four directions. Patch-token norms are
  bimodal; above 150 is an outlier and **2.37% of DINOv2 ViT-g's tokens are
  one**. They sit on patches with high cosine similarity to their neighbours
  *at the patch embedding*, before any attention. They have lost their local
  content — position probe **22.8** top-1 against 41.7, reconstruction L2
  **25.23** against 18.38 — and gained global content: one high-norm token
  taken at random as the whole image representation classifies much better than
  one normal token.

  And it reads like emergence: around **layer 15 of 40**, only after **a third
  of training**, only at **ViT-Large and above**.

- **`THEORY-101`**, `Active` — the model has no scratch space, so it takes
  patches it can afford to lose and overwrites them with global state. The
  artifacts are that, seen from outside.

  `Active` on one paper because **the account made a prediction and the
  prediction was tested**: supply dedicated scratch space and the high-norm
  patch tokens should vanish. They do, entirely, in supervised, image-text and
  self-supervised training alike. A successful intervention derived from the
  hypothesis is stronger than any number of correlations consistent with it.

- **`SOTA-400`**, `Active`/`emerging` — append a few learned tokens that
  do not come from the image, carry them through, discard them at the output.
  One removes the artifacts; a few more help dense tasks slightly.

  Nothing degrades and DINOv2 improves on all three probes (ImageNet 84.3 →
  84.8, ADE20k 46.6 → 47.9, NYUd 0.378 → 0.366). The benefit is not in
  classification but in anything reading the feature map **spatially**: LOST
  object discovery on DINOv2 goes **35.3 → 55.4 corloc** on VOC 2007, and
  DeiT-III more than doubles.

  The `emerging` note says the grounds are the evidence and not adoption: the
  only adopter the record can name is the source group's own DINOv2 register
  checkpoints, which `DP-005` counts as adoption rather than a second
  measurement.

### Changed

- **`LIT-599` v2 — DINOv2's features have a characterized defect, and it broke
  a task family.**

  This note recommends DINOv2 as a frozen feature extractor and that is what
  the record reaches for it for. Beyond the 2.37%: *"we observed that DINOv2 is
  surprisingly incompatible with LOST."*

  Unsupervised object discovery was built on DINO and had *"significantly
  surpassed the previous state of the art"* with it. DINOv2 is the stronger
  model on dense prediction and scores **35.3 corloc on VOC 2007 against
  DINO's 61.9** — a generational regression of nearly half, on a task family
  nobody in the comparison was running.

  What that does to the note's thesis is the reason it is carried:
  curation-plus-scale produces general-purpose features **on the evaluations
  run**.

### Documentation

- Three qualifications carried into the documents rather than dropped, each
  cutting against the tidy version:

  **OpenCLIP object discovery is slightly worse with registers** — the one
  evaluation where the intervention does not help, unexplained by the paper or
  the account.

  **Registers do not close the gap.** DINOv2+reg reaches 55.4 corloc where DINO
  reaches 61.9. If artifacts were the whole difference the gap would have gone.
  Something else about DINOv2 also costs object discovery and nobody has named
  it.

  **"Redundant" is operationalised as similarity to four neighbours**, a proxy
  for what the model can afford to lose rather than a measurement of it.

- **What this unit shares with unit 5, and where the parallel stops.** Unit 5
  filed `THEORY-100`: activation outliers in language models were called
  emergent at scale and track optimization choices instead. This unit has the
  same **shape of inference** in its setup and a different resolution — the
  outliers are the model solving a problem it has no machinery for, and the fix
  is to give it the machinery.

  Both are recorded as supporting a **question, not a conclusion**: when an
  activation pathology appears above a size threshold, what else changed at the
  same time? They are different modalities, quantities, causes and remedies,
  and they should not be read as corroborating each other. The record can see
  the pair only because it files by kind of claim rather than domain
  (`ADR-026`).

### Added

- **Intriguing Properties of Quantization at Scale** — `LIT-656`.
  Ahmadian et al. (2023), `2305.19268`. Unit 5 of `#342`, `#290`'s promotion
  [#19](https://github.com/dmarx/anthology-of-the-sota/issues/19), ranked on the record's **largest cluster: 127 documents naming
  quantization and 18 practices.**

  Post-training quantization was reported to fail sharply above ~6B and the
  failure was called **emergent**. The motivating puzzle was already in the
  field: OPT-175B is badly sensitive to INT8 and BLOOM-176B is relatively
  robust, at the same scale and the same decoder-only shape.

  Same architecture, one axis varied at a time, every variant trained from
  random initialization, 410M → 52B — and, the control that makes it a study,
  **comparable pre-quantization quality across variants**:

  | choice | INT8 degradation |
  | --- | --: |
  | weight decay 0.1 | **0.09%** |
  | weight decay 0.001 | 1.36% |
  | weight decay 0.01 + fp16 | 1.73% |

  Dropout monotonically worse; gradient clipping helps and offsets a low
  weight decay; bf16 over fp16. At 52B with all four, plain INT8 **gains
  0.08%** on the eight-task zero-shot average, against **~42% degradation
  reported for OPT-66B**.

- **`THEORY-100`**, `Proposed` — activation outliers are a product of
  pre-training optimization choices, not an emergent property of scale. The
  proposed mechanism is the LayerNorm gain, whose spread sets the activation
  spread entering the projections and which is **2× wider under fp16 than
  bf16**.

  `Proposed`: one group, one architecture family, and the mechanism is a
  correlate — nobody has intervened on the gain distribution while holding the
  optimizer fixed.

- **`SOTA-399`**, `Proposed`/`unreplicated` — choose weight decay,
  dropout, clipping and precision for the quantization you intend to ship.

  Why it is worth stating: every other quantization practice here repairs the
  problem after the fact — isolate the outliers (`SOTA-355`), scale the salient
  channels (`SOTA-356`), absorb them into a high-precision branch
  (`SOTA-314`) — and each costs kernel complexity or rank. This costs a
  hyperparameter you were setting anyway. The awkward part is stated too:
  **the cost is paid at pre-training and the benefit months later at serving.**

### Fixed

- **`LIT-586` v2 — the record bet on which half of LLM.int8() would survive,
  and picked the wrong one.**

  Its Standing section said: *"The emergent-outlier characterization is the
  part that has been independently built on; the no-degradation headline is
  the part a later, harder evaluation could move."*

  The no-degradation headline has held. What moved is **emergent**. And the
  detection recipe did not travel: the same group reports the published
  threshold of 6.0 *"too high to classify a feature dimension as an outlier
  for all the variants we consider"*, with no adaptation correlating with
  quantization sensitivity **even after correspondence with the original
  authors**.

  The note keeps the original sentence and records that it was wrong, with the
  reason: *"independently built on"* was measuring **adoption, not
  replication**. Several papers took the framing; one group tried to reproduce
  the criterion and could not. `DP-005`'s distinction, applied to a
  characterization rather than a recommendation.

### Changed

- **`SOTA-355` v2 — two conditions, recommendation and status unchanged.**

  *"Emergent"* in its title is contested, and the practice says so while
  keeping the word, because it is the source's and the technique is known by
  it. And **step 2 — detect the outlier dimensions — has failed the only
  independent replication the record holds.** That does not make the practice
  wrong; the shipped implementations have detectors that work. It means a
  reader implementing step 2 from the paper should know one group could not,
  and that the threshold may be specific to how the model was trained.

### Added

- **Self-attention Does Not Need O(n²) Memory** — `LIT-655`. Rabe and
  Staats (2021), `2112.05682`. Unit 4 of `#342`, `#290`'s promotion #4, ranked
  on **61 documents naming FlashAttention and 5 practices recommending it**
  with the antecedent unheld.

  Six months before FlashAttention: move the softmax denominator to the end by
  the distributive law, carry a running vector and scalar, and attention needs
  **`O(1)` memory per query** — `O(log n)` for self-attention, `O(√n)` in the
  practical chunked form. Exact, not approximate: 100K training steps reach
  62.69 evaluation accuracy against 62.59 standard. **59× less memory overhead
  at sequence length 16,384**, 32× during differentiation.

### Changed

- **`SOTA-085` v4 — the memory saving and the speedup are different claims.**

  This practice carried them together. The antecedent separates them, and on
  **hardware class** rather than kernel availability: the same algorithm on
  TPU is *"within a few percent of the runtime of the standard
  implementation"*, because *"standard self-attention already balances the
  available FLOPs and memory bandwidth of TPUs."*

  | | depends on | holds where |
  | --- | --- | --- |
  | less memory | the algorithm | anywhere it runs |
  | more speed | HBM traffic being the bottleneck | GPUs; near zero on TPU |

  `LIT-074`'s 3× on GPT-2 is a GPU number and its Theorem 2 is explicitly a
  claim about a memory hierarchy. Both still hold. What does not follow, and
  what this practice implied, is that the speedup travels with the algorithm.

  **Recommendation and status unchanged.** The condition in the title now
  covers hardware class as well as whether a compiled kernel exists.

- **`LIT-074` v3 — names what came before it.** It had said it was the source
  of four confirmed practices and named no antecedent. There are two:
  `LIT-655` six months earlier, and **Jang et al. (2019)**, unheld, whose
  "lazy softmax" Rabe and Staats say in as many words their own Equation 1 is
  *"a rediscovery"* of.

  What this paper contributes is unchanged and is the **systems half** —
  IO-awareness, the HBM-access bound, IO-optimality, derived block sizes, a
  CUDA kernel.

### Documentation

- **`#342`'s prediction for this unit was wrong, and the issue said to check.**
  It ranked this fourth expecting a repeat of `SOTA-192`'s origin defect —
  `introduced_by: LIT-074`, dated May 2022, against a December 2021 paper —
  and added *"same shape as `#338`; verify before asserting."*

  It is a different shape. `SOTA-192`'s title was a generic technique credited
  to an adopter. `SOTA-085`'s title names an **artifact**: *flash attention*
  is Dao et al.'s system, and the recommendation to run that kernel was first
  made by them. **`introduced_by` is deliberately unchanged**, with the
  argument written into the practice's Source section so the next pass does
  not re-open it.

  What the practice was missing was not an origin but a condition.

- **Jang et al. (2019)** is a third link in this chain, unheld, and not in
  `#290`'s queue — so `#342` has not ranked it. By Rabe and Staats' account it
  discusses neither memory complexity, numerical stability, nor
  backpropagation, and has no public implementation, which is why it is
  recorded rather than promoted.

### Added

- **Patch n' Pack: NaViT** — `LIT-657`. Dehghani, Mustafa et al.
  (2023), `2307.06304`. It is the follow-up `#331` named after filing Sora:
  no practice covered training at native size instead of fixed crops, and
  Sora's reference 18 was not held.

  Patches from several images are packed into fixed-length sequences, with
  per-example masks. The ViT then trains on aspect-preserved images at a
  sampled resolution. It leads ViT at each of 12 compute-matched budgets
  and matches the best ViT with 4x less compute. **The paper credits
  seeing about 5x more images as "the chief contributor."** Pretraining
  samples the area (r ~ U(64, 256)) rather than using true native size.

- **`SOTA-398`** (`Proposed`, `unreplicated`) — pretrain a vision
  transformer on packed, aspect-preserved images at sampled resolutions,
  not on fixed square crops. The practice includes a table of what each
  part rests on:
  - The package: compute-matched, but its parts are not separated.
  - Variable resolution: isolated (Fig. 5).
  - Aspect ratio: isolated only in a linear fairness probe (p = 0.02).
  - Throughput: most of the gain.

  `promote_when` asks for an independent compute-matched replication or a
  pretraining run that isolates aspect ratio. Adoption by Sora or SD3 does
  not count. No generative model is measured.

### Changed

- **`LIT-652` (Sora) v2.** Its note that NaViT was not held now points to
  the filing and the practice.

### Fixed

- **The published site titles every page again** ([#271](https://github.com/dmarx/anthology-of-the-sota/issues/271)). luria 0.31.0 in all
  ten pins, from 0.28.2. Quartz 5 reads frontmatter only through a plugin the
  generated config had left out, so every page was untitled: search results
  listed as blank cards, graph nodes were labelled with their paths, the
  explorer showed filenames, and each page's YAML rendered as a paragraph
  above the record table. Pages are now titled `CODE: title` — `SOTA-255: Tune
  weight decay upward…` — and a generated view by its heading.

### Changed

- The record table under each title is replaced by Quartz's properties panel,
  which shows the same facts — status, consensus, tags, source, and the typed
  edges both ways, each code followed by its title — and whose links now also
  feed the graph and backlinks. The filing date is no longer repeated in it:
  Quartz shows it under the title ([LU-#322](https://github.com/dmarx/luria/issues/322)).
- The lint now reports one unbound line — `LIT-640`, `LIT-641`, `LIT-651`
  share no `tags` across the whole lineage. It was already in
  `docs/reports/unbound-lineage.md`; 0.30.0 made the unbound findings lint
  classes. A warning, not a failure: it is not in `lint.fail_on`.

### Added

- **Muon Outperforms Adam in Tail-End Associative Memory Learning** —
  `LIT-654`. Wang et al. (2025), `2509.26030`. Unit 3 of `#342` and
  `#290`'s promotion #2. **94 documents here name Muon, 17 practices name it,
  and five theories mention it without accounting for it.**

  The ablation is the part the record had been waiting for. Muon on some
  blocks, Adam on the rest, everything else matched: **VO + FFN nearly
  recovers the full-Muon trajectory, and query-key contributes little.**
  Applying Muon to `W_V` alone or `W_O` alone already beats applying it to all
  of QK. Within the effective set, `W_O` over `W_V` and `W_out` over `W_in`.

  Not a parameter-count effect, and they say so: **QK and VO are the same
  size.** They also check it is not the MoE logit explosion others report.

- **`THEORY-099`**, `Proposed` — the account. A linear associative memory
  is a sum of outer products; orthogonalising the update allocates the same
  step to every stored direction regardless of how much gradient signal it
  carries. Gradient signal tracks frequency, corpora are heavy-tailed, so the
  directions Adam under-serves are the rare ones. Measured: Muon matches Adam
  on head classes and substantially beats it on tail classes. Proved on a
  one-layer associative memory — for **any** embeddings satisfying their
  assumption, one-step Muon gives `ϱ ≥ 1 − ε(1 + O(log K/K))`, where plain
  gradient descent gives `O(ε^{−r}K^{r−1})` with `r < 1`.

  `Proposed`, with the strongest counter-observation stated in the document:
  the source **also** reports Muon learning more isotropic QK weights, and QK
  is the block that contributes little. So isotropy is general and the benefit
  is not, which means isotropy alone cannot be the whole mechanism.

### Changed

- **`THEORY-032` v3 — `promote_when` sharpened into a discriminating
  measurement.** The account is unchanged.

  It had asked for *"an ablation that uses the condition as a decision rule…
  and trains faster than applying spectral updates everywhere."* Wang et al.
  ran that ablation under a **different** rule — associative-memory role, not
  incoming-activation stable rank — and got *nearly recovers* rather than
  *faster*.

  So the condition is not met, and what it establishes is the half that was in
  doubt: **a per-block split is nearly costless**, so a decision rule over
  blocks is a real object. The new `promote_when` names the cheap experiment —
  measure the stable rank of incoming activations for QK, VO and FFN
  separately and check whether this account's condition orders them the way
  the measured gains do — and says what failure means: if it does not, this is
  a quantity correlating with the regime rather than the mechanism, and **the
  status should fall rather than rise.**

- **`SOTA-121` v3 — which parameters the gain is paid on.** This practice
  recommended an optimizer without saying where its advantage sits. It sits on
  VO and the FFN.

  **Recommendation unchanged**, for two stated reasons: the recovery is
  architecture-sensitive (VO + `W_out` nearly recovers full Muon ungated and
  falls short gated), and VO+FFN *nearly recovers* rather than beats, so this
  is not an argument for running a hybrid. It is an answer to what you are
  buying, and a note on where to spend first if a deployment cannot afford
  Muon everywhere — from one group at small scale with a 0.7B check, and not
  yet a practice.

### Documentation

- **A `Proposed` account became load-bearing without becoming better
  evidenced.** The mechanism above assumes the associative-memory reading of
  FFN layers — `THEORY-081`, `Proposed`, from 160 hand-annotated keys of one
  16-layer model. An optimizer result now rests on it, which raises the cost
  of its being wrong and is not evidence that it is right. Recorded in both
  new documents; `THEORY-081` is deliberately **not** amended, because a
  downstream user is not the replication its `promote_when` asks for.

### Added

- **Video generation models as world simulators** — `LIT-652`. Brooks,
  Peebles et al., OpenAI (2024), the Sora technical report. It closes unit
  7 of `#331`, which was blocked because openai.com refuses the build
  environment. It was read in full through the r.jina.ai reader rendering
  of the canonical URL, since web.archive.org and archive.ph refuse the
  connection too. `url:` is the canonical page.

  Sora is a latent diffusion transformer over spacetime patches. It trains
  on native sizes and uses DALL-E 3 recaptioning with prompt upsampling.
  The report withholds model details and contains no measurement. The
  scaling comparison (base, 4x, 32x compute) and the square-crop ablation
  are shown as videos only. It `extends` DiT and DALL-E 3, and is
  `compared_against` Movie Gen and Wan, which benchmark against it.

### Fixed

- **`NOTE-350` v2 — Sora's "separate upsampler" is not in Sora's report.**
  The LTX-Video reading said Movie Gen and Sora pay for high-frequency
  detail with a separate upsampler. The Sora half came from LTX-Video §2,
  which cites the report as proposing a pixel-space upsampler conditioned
  on base-model latents. The report says nothing about an upsampler. The
  note now presents this as LTX's attribution.

### Added

- **Softmax is not Enough (for Sharp Size Generalisation)** — `LIT-653`.
  Veličković, Perivolaropoulos, Barbero and Pascanu (2024), `2410.01104`.
  Unit 2 of `#342` and `#290`'s promotion [#17](https://github.com/dmarx/anthology-of-the-sota/issues/17). **106 documents in this record
  name the softmax, 23 practices name it, and no note held it.**

  The result, in two steps. For `n` logits with spread `δ` and temperature
  `θ > 0`, no softmax coefficient can exceed `(1/n)·exp(δ/θ)` — and over a
  **finite vocabulary** the logits are bounded in every attention layer, since
  the embeddings sit in a compact set, feedforward layers are continuous, and
  self-attention outputs convex combinations. So the premise is not an
  assumption about a model; it follows from tokenisation plus global
  attention.

  What that costs: a function depending on any fixed number of inputs — `max`,
  `min`, a lookup — cannot be computed robustly as `n` grows. Measured on
  single-head max retrieval trained at 16 items, **98.6% at 16 falls to 12.4%
  at 16,384**, one model read at eleven input sizes.

- **`THEORY-098`**, `Active` — the account. `Active` because it is a
  proof with stated, checkable assumptions, explaining a phenomenon others had
  already reported without being able to account for it (Yan et al. 2020;
  Ebrahimi et al. 2024).

  The limits are written into the document: it is a bound and not a rate, so
  it does not say dispersion has happened yet at the length you are running;
  local attention is outside it; and three families escape it — unnormalised
  attention (linear, sigmoidal, stick-breaking), selective attention, and
  possibly *not* the Differential Transformer, whose subtraction happens after
  each softmax and cannot undo dispersion inside them.

### Changed

- **`SOTA-192` v7 — what bounding the logits also does.**

  This practice bounds attention logits to stop entropy collapsing during
  training. Proposition 3.1 of the new source names the intervention by
  description — *"layer normalisation… which clamps `‖x_i‖` and `‖y‖` if
  applied right before the query-key mechanism, accentuating the impact of Q
  and K's singular values"* — and shows `δ ≤ 2·σ_max(Q)·σ_max(K)·‖y‖·max‖x‖`.

  So sharpness in a Transformer is only reachable by growing weights, which is
  the growth this practice treats as the failure; and the spread it shrinks is
  the same `δ` that sets the dispersion cap.

  **Recommendation, status and consensus unchanged.** The two failures live at
  different input sizes — entropy collapse is a training pathology at the
  length you train on, dispersion an out-of-distribution one — and nobody has
  measured whether QK-normalised models disperse sooner. Recorded as a
  consequence of two bounds, not as a cost anyone has paid.

### Documentation

- **Adaptive temperature recorded and not filed as a practice.** The source's
  mitigation — read the coefficients' Shannon entropy, map it through a fitted
  degree-4 polynomial to a temperature, re-softmax, never raising entropy — is
  streamable and composes with FlashAttention-style attention. The gains are
  statistically significant from 64 items up and largest at +3.9 points.

  They are also a rounding error against the failure: 98.6% → 12.4% becomes
  98.6% → 14.0%. The authors call it *"an ad-hoc technique"* that *"warrants
  further investigation"*. A practice here would recommend a 1.6-point patch
  on an 86-point collapse. It would become one if the correction held accuracy
  roughly flat across a decade of `n`.

- **A gap this note opens rather than fills.** The record holds **zero**
  documents naming the Differential Transformer, selective attention, sigmoid
  attention or stick-breaking attention — the families the theorem exempts.
  The linear-attention line (`#161`) is filed here as an efficiency story, and
  this is an argument for the same family on *expressivity* grounds.

### Added

- **Transformers without Tears** — `LIT-651`. Nguyen and Salazar (2019),
  `1910.05895`. Unit 1 of `#342`, and `#290`'s promotion [#23](https://github.com/dmarx/anthology-of-the-sota/issues/23). The first
  systematic evaluation of pre-norm in the base Transformer regime, and it
  carries a result the record's `universal` pre-norm practice did not have.

  **On high-resource WMT'14 English-German, post-norm wins**: PostNorm +
  LayerNorm 27.58, PreNorm + LayerNorm 26.83. The paper flags it as surprising
  and reports Wang et al. (2019) observing the same. Its own summary: *"while
  PostNorm performs better for high-resource NMT in the original base
  Transformer regime, PreNorm is both more stable and more competent in
  low-resource settings."*

  It also introduces **ScaleNorm** — `ℓ₂` normalization to a single learned
  length `g` — which is what `LIT-640`'s QK-norm applies to queries and keys.

### Fixed

- **`SOTA-032` v5 — `introduced_by` is now empty, and the emptiness is the
  finding.**

  The practice named `LIT-114` (Xiong et al., **February 2020**) as the work
  that first made the recommendation. This paper is **October 2019**, so the
  field was wrong — but the repair is not to repoint it here, because
  **`LIT-651` disowns the origin in its own introduction**, crediting Chen
  et al. (2018) and Wang et al. (2019) and noting pre-norm was *"already
  implemented in popular toolkits (Vaswani et al. 2018; Ott et al. 2019;
  Hieber et al. 2018), though not necessarily used by their default recipes."*

  So no document this record can name *first made this recommendation*. The
  origin is code. `introduced_by: []` under `ADR-053`, with a frontmatter
  comment naming exactly what was searched — which is how a reader refutes it.
  Second use of that decision, argued on its own terms as its Scope section
  requires.

- **`LIT-640` v2 — what the +0.928 BLEU was measured against.**

  The note said "against state-of-the-art bilingual benchmarks", the paper's
  own abstract phrasing, which reads as though QK-norm had been isolated. The
  baseline row is **Nguyen and Salazar's own system**, whose repository this
  work starts from, and the comparison **changes two things at once**:
  ScaleNorm becomes vanilla LayerNorm, and scaled dot-product attention becomes
  QKNorm. The number is *QKNorm + LayerNorm* against *ScaleNorm + `1/√d`*, not
  QK-norm against a plain Transformer. Per-pair figures added.

### Changed

- **`SOTA-032` gains the two qualifications its motivation was missing**, with
  the recommendation, the status and the `universal` value all unchanged.

  **The regime where post-norm wins** — the table above — so `universal` is now
  stated as a claim about the scales this record files for rather than about
  transformers in general.

  **How much of the instability is initialization.** On low-resource en→vi,
  post-norm with default Xavier initialization fails to converge at 4k and 8k
  warm-up and reaches 5.76 BLEU at 16k. Reduce the attention layers'
  initialization and the same post-norm model reaches **28.17** at 4k, against
  pre-norm's 28.52. The dramatic form of this practice's motivation is **partly
  an initialization artefact**; the paper's own phrasing is that smaller
  initialization *"partly reclaims PostNorm's stability"* and pre-norm is
  *"less sensitive to this magnitude"*.

  What survives unchanged is depth without warm-up, where the difference stays
  categorical: at five and six layers with no warm-up, post-norm **fails** and
  pre-norm sits at 28.13 and 28.32.

  Also recorded: the paper's speculation about *why* post-norm wins at high
  resource — identity residual networks acting like shallow ensembles and
  *"undermining the learning of the longest path"* — is **not** the
  representation-collapse account `THEORY-096` holds. Two accounts of the same
  cost, neither adjudicated.

### Documentation

- Two antecedents this paper names are unheld and are not in `#290`'s queue,
  so they are unranked: **Chen et al. (2018)**, `1804.09849`, credited with
  finding pre-norm instrumental, and **Wang et al. (2019)**, `1906.01787`, who
  first compared the placements at depth and report the same high-resource
  result.

### Fixed

- **`NOTE-197` v2 (the SiT reading).** It said R3, "tune the stochastic
  sampler's diffusion coefficient after training", was something "the record
  has nothing resembling". That was left in place when `#339` filed the
  stochastic-interpolants framework (2303.08797), which states the result
  first and is now `introduced_by` on `SOTA-265`. The note now credits R3
  to the framework and names this paper as where it is measured. The
  Connections section also names the framework, whose proofs SiT reuses
  ("Most proofs are derived from [2]"), and 2209.15571, whose
  `cos(πt/2)`/`sin(πt/2)` path is SiT's GVP interpolant.

### Added

Eight substrate papers the video line (`#331`) cited and did not hold. Each
was read in full for its filing.

- **DMD** (`LIT-643`, 2311.18828) and **DMD2** (`LIT-646`,
  2405.14867) — distribution-matching distillation, the method CausVid and
  Self Forcing carry to causal video. DMD2 drops DMD's regression loss and
  adds a GAN term; its student is less diverse than its SDXL teacher (0.61
  against 0.64) and the paper gives no cause for it.
- **Building Normalizing Flows with Stochastic Interpolants**
  (`LIT-644`, 2209.15571) and **Stochastic Interpolants: A Unifying
  Framework** (`LIT-645`, 2303.08797). The second is the framework SiT
  instantiates, and SiT now `extends` it.
- **Improving Image Generation with Better Captions** (`LIT-648`, the
  DALL-E 3 paper; OpenAI PDF, no arXiv id). Its controlled evidence is CLIP
  score only.
- **Scheduled Sampling** (`LIT-649`, 1506.03099), **MIXER**
  (`LIT-647`, 1511.06732) and **Professor Forcing** (`LIT-642`,
  1610.09038) — the RNN papers on the train/test mismatch that
  autoregressive video now calls exposure bias.

FLUX.1 is not filed. It has no technical report, and FLUX.1 Kontext
(`LIT-573`) §2 describes the base model.

### Fixed

- **The straight path had two origins, not three.** `LIT-630`, `LIT-636`
  and `SOTA-266` named stochastic interpolants as a third concurrent origin
  of the straight data-to-noise path. 2209.15571 uses a trigonometric
  interpolant. The linear path appears only in a remark that credits Liu et
  al., and its related work says Liu and Lipman "focus on straight
  interpolants". It is now cited for what it did originate, the
  simulation-free interpolant objective.
- **`SOTA-265` v2: `introduced_by` moved from SiT to the interpolants
  framework.** The v1 abstract of 2303.08797 already says the noise strength
  "can be tuned as model hyper-parameter after training". SiT shares three
  of its authors and takes the KL bound from it. SiT stays in `source:` for
  the ImageNet measurement.
- **`LIT-629`: "exposure bias" was attributed to the wrong papers.** Only
  MIXER uses the term, 11 times. Scheduled Sampling and Professor Forcing
  never use it.
- **`SOTA-333` v4: an unsourced condition now has sources.** "For discrete
  tokens, teacher forcing does not diverge in the same way" now cites the
  three RNN papers. They show measurable but modest gains, confounded in
  MIXER's case by optimizing the test metric, and no measured divergence.

### Changed

- `LIT-447` (SiT) v2, `LIT-631` (CausVid) v3, `NOTE-343`, `SOTA-394` and
  `SOTA-389`. Sentences saying DMD, DMD2, the DALL-E 3 paper or anything
  like the diffusion-coefficient result was not held now cite the filed
  documents. CausVid now `extends` DMD and DMD2.

### Added

- **Competition-Level Code Generation with AlphaCode** — `LIT-650`. Li
  et al. (2022), `2203.07814`. Unit 6 of `#326` and the last of its worklist.
  Top 54.3% over ten Codeforces contests; 34.2% of held-out CodeContests
  problems within ten submissions. The system samples enormously, filters on
  the example tests, clusters the survivors by program behaviour, and submits
  ten.

  `#326` ranked it last because **0 files said "AlphaCode"** and the argument
  was about `SOTA-210`'s subject rather than the record's dependence on the
  paper. Right about the paper's standing, wrong about the unit: the
  dependence is on `LIT-388`, which **25 documents name and six practices
  use**, and this is the work that measured what its tests certify.

### Changed

- **`LIT-388` v2 — HumanEval's false-positive rate, measured by hand at 30%.**

  The note listed what the benchmark is insensitive to and did not carry the
  hardest number of the set. Li et al. took fifty problems their model solved
  on HumanEval and examined one passing solution for each manually: **30% were
  programs that pass every test and are not correct**, at **7.77 tests per
  problem**. APPS came out at 60% on 20.99 tests; the dataset they built to
  avoid the problem, at 4% on 203.7.

  The cause is general — *"input/output examples are an under-specification of
  program behavior"* — so test count is the binding constraint and 7.77 is a
  small number.

  Three qualifications carried across with it, because the number travels
  badly. Fifty problems, checked once, in 2022, against one 1B model's
  outputs. The comparison was run **unfavourably to their own dataset** — 200
  samples per HumanEval problem against a million per CodeContests problem,
  and fewer samples on simpler problems both push the rate down. And 30% of
  *solved* problems being false positives is **not** a claim that published
  scores are 30% too high; it says the benchmark's ceiling is lower than its
  tests suggest, by an amount nobody has bounded tightly.

- **`SOTA-210` v3 — `pass@k` is an upper bound, and the practice now says so.**

  Li et al. define `n@k` — solved with `n` submissions from `k` samples — and
  state the relation: **`pass@k = k@k`, an upper bound for using `k` samples**,
  because it scores a system allowed to submit everything it draws. So
  `pass@k` measures whether a correct sample *exists*, not whether the system
  can *find* it. In their setting, filtering on the problem's own example
  tests removes **about 99% of samples**, and on roughly **10% of problems
  nothing survives the filter at all**.

  The finding this practice rests on is unaffected — base against tuned on the
  same metric in both arms, so a bound applied to both still shows the two
  numbers moving apart. What changes is the reading. The practice's own
  conditions say the coverage matters *"where test-time sampling is the
  deployment — verifiable domains, agentic retries, best-of-n, majority
  voting, search over candidate solutions"*, and **every one of those has a
  selection step**. Coverage you cannot select from is not coverage you can
  spend.

  Added recommendation: where the deployment has a submission or verification
  budget, report `n@k` at that budget beside `pass@k`. The gap is the part of
  the problem that is yours rather than the model's.

### Documentation

- Recorded in `LIT-650` and deliberately **not** filed as practices,
  with the reason in each case:

  **Test-time compute allocation.** Solve rate scales approximately
  log-linearly in the sample budget on both `10@k` and `pass@k`, and
  log-linearly in training compute and in sampling compute separately; larger
  models have higher slopes, so model quality buys exponentially fewer
  samples. One system, one task family, 2022, and the record has no
  test-time-compute cluster for this to join or correct. Promotes with a
  second measurement of the training-versus-sampling trade-off elsewhere.

  **A controlled comparison of multi-query attention.** 4.74 samples/TPU·sec
  against 0.37 for standard multi-head at matched training compute and equal
  solve rate — **12.8×** — with a decoder-only baseline at 1.23 and the *best*
  solve rate. `SOTA-023` and `SOTA-024` are `Superseded` by `SOTA-109`, so
  this is history; recorded because a 12.8× number attached to a retired
  practice is worth being able to find.

  **Validation loss diverging from the target metric.** Validation loss rises
  early in fine-tuning while `10@1024` keeps improving past 50k steps. That is
  `SOTA-284`'s premise, reported three years before its source, and that
  practice's `promote_when` rules it out by name — *"a further demonstration
  that cross-entropy predicts downstream performance poorly is not it."* What
  it adds is that the premise is older than the record's citation for it.

### Added

- **Query-Key Normalization for Transformers** — `LIT-640`. Henry,
  Dachapally, Pawar and Chen (2020), `2010.04245`. **The origin of QK-norm.**
  `ℓ₂`-normalize each query and key along the head dimension before the dot
  product, then **scale by a learnable parameter instead of dividing by
  `1/√d`** — so the softmax temperature becomes a trained quantity. Motivated
  by softmax saturation costing expressivity, not by divergence at scale.
  +0.928 BLEU averaged over five low-resource pairs.

  Thirty documents in this record name QK-norm and the origin was not held.
  `#290` promoted this identifier as candidate #7 with the diagnosis stated
  exactly — *"named origin of QK-norm; `LIT-088` uses it with no source for
  the technique"* — and the promoted queue has not been worked: **21 of
  `#290`'s 25 promotions are still unfiled**, this one included until now.

  The turn worth noticing is that this unit reached it through the re-read of
  `#290`'s *declines*, not through its promotions. The defect was named a day
  earlier, in the same issue, in the list of things to do next.

- **Attention Approximates Sparse Distributed Memory** — `LIT-641`.
  Bricken and Pehlevan (2021), `2111.05498`. Unit 5 of `#326`, which ranked
  it fifth and called it the weakest reversal. That assessment of the theory
  holds; what it could not anticipate is that reading the paper is what
  surfaced the defect above.

  Attention's update rule is Kanerva's SDM read given two conditions — `L²`
  normalized vectors and a fitted `β`. The retrodiction is the interesting
  part: *"In requiring that Attention vectors be `L²` normalized and β fitted,
  SDM predicted Query-Key Norm."* Trained QK-norm heads learn **β ∈ [10, 25]**
  (from the QK-norm authors in private correspondence), interpolating between
  SDM's critical-distance, SNR and memory-capacity optima.

- **`THEORY-097`**, `Proposed` — attention as an SDM approximation. The
  record holds five accounts of what self-attention *does* (clustering,
  collapse, entropy, spectral concentration, circuit formation) and this is
  the only one about what the operation **is**. Its nearest neighbour is
  `THEORY-081`, feed-forward layers as key-value memories, which is better
  evidenced: direct measurement rather than a correspondence plus a
  temperature check.

  `promote_when` asks for a point prediction that could have come out wrong,
  and rules out two things explicitly: the β range (a band spanning three
  optimality criteria was wide before anything was measured, and the authors
  say the reference values "are only a weak reference") and further components
  reinterpreted in SDM terms, which extends the mapping without testing it.

### Fixed

- **`SOTA-192` v6 — `introduced_by` repointed from the adopter to the
  origin.** The practice named `LIT-088` (ViT-22B, 2023) as the work that
  first made the recommendation. It was first made by Henry et al. in 2020.

  The sharp part: **`LIT-088`'s own note had refused this claim.** It says
  *"nothing in the record reads a source establishing QK-norm. This is one of
  the earliest at scale"* — a correctly hedged adoption claim. The practice
  built on it asserted what the note declined to. A hedge in one document does
  not travel to the document that cites it, and no check compares them.

  `LIT-088` stays in `source:`, because the 8B divergence and the entropy
  diagnosis this practice is built on are entirely its; the origin joins it
  there, having run a controlled comparison of its own. The recommendation,
  the status and the `converged` reading are unchanged.

  One substantive difference now recorded: Henry et al. **replace** `1/√d`
  with a learnable scalar; `LIT-088` and the record's later usage keep it.
  Both bound the logits, only one makes the temperature a trained parameter —
  and that parameter is what `LIT-641` measures.

### Changed

- **`LIT-088` v3.** The hole this note identified is filled. The Standing
  section records what the hedge was doing rather than deleting it: the
  diagnosis was correct, it named the right gap, and it is what produced the
  repair.

### Added

- **ResiDual** — `LIT-639`. Unit 4 of `#326`. Unlike units 1–3 this was
  **not** a heading leak: the paper genuinely is an architecture variant, and
  the decline was the rule itself. **The variant is the contribution and the
  analysis is what the record needed.**

  `SOTA-032` recommends Pre-LN, is `Active` and `universal`, and states the
  cost in its own prose — *"deep pre-norm models can see later blocks
  contributing proportionally less — the representation collapse argument"* —
  **with no citation.** Nineteen files discuss Pre-LN and ten discuss
  Post-LN; the cost of the recommended choice was stated everywhere and
  sourced nowhere.

  Xie et al. give it a rate. Assuming block outputs are independent, the
  per-layer change in the normalised hidden state is `O(1/√k)`, and adding a
  block to an `N−1` block model moves the output `O(1/√N)`.

  They also credit the observation to **Liu et al. (2020)**, whom the record
  does not hold either — recorded rather than filed, since this unit is one
  paper.

- **`THEORY-096`**, `Proposed` — the account. The shape worth carrying:
  **the benefit and the cost are one mechanism described twice.** The residual
  path being unrenormalised is what lets gradients reach the early blocks, and
  what lets the stream outgrow any single block's contribution. That is why
  the fixes are rearrangements rather than removals.

  `Proposed`, with the limits stated: the independence assumption is doing the
  work and a trained network does not satisfy it; the derivation describes
  initialisation, not training; and **`O(1/√k)` is slow** — at 24 layers the
  per-layer change is about a fifth of its first-layer value, not a
  thousandth. "Collapse" names the direction and overstates the speed.

### Changed

- **`SOTA-032` v4**, three things, recommendation unchanged.

  **The collapse argument gains its source and rate**, via
  `THEORY-096`, with both qualifications carried across rather than
  just the headline.

  **The no-warm-up consequence gains a measurement.** The practice said
  Xiong et al.'s result is that "the warmup stage can be removed entirely",
  with no number. On IWSLT: Pre-LN with warm-up 35.12 / 35.18, **without
  32.28 / 31.82** — a cost of 2.84 and 3.36 BLEU. Pre-LN trains without
  warm-up, which is what Xiong et al. claimed; it does not train *as well*,
  which nobody had measured here. That narrows the `SOTA-100` tension this
  practice flags and does not resolve: **what pre-norm removed is the
  requirement, not the benefit.**

  **The `universal` reading gains the note it never had** — one of `#294`'s
  eight practices asserting a non-default consensus on no stated grounds. The
  grounds are adoption, said as adoption; the new evidence for it not being
  merely inherited is that post-norm *fails outright* at twelve encoder and
  twelve decoder layers even with warm-up.

  One reading worth keeping from the source: **Xie et al.'s prose is looser
  than their own table.** They write that Pre-LN "can train effectively
  without" warm-up, in the paragraph beneath the three-point drop. Anyone
  citing the sentence rather than the table carries the received view forward
  unqualified — which is how this practice came to state it.

### Added

- **Six single-source practices from the video line ([#331](https://github.com/dmarx/anthology-of-the-sota/issues/331)).** All are
  `Proposed`, each with a `promote_when`:
  - `SOTA-394`: distil a causal few-step video generator from a
    bidirectional teacher, not a causal one (CausVid, [LIT-631](record/literature.d/LIT-631.md)).
  - `SOTA-395`: post-train an autoregressive video generator on its own
    rollouts and score the whole rollout (Self Forcing, [LIT-629](record/literature.d/LIT-629.md)).
  - `SOTA-393`: freeze the image model's spatial layers when checkpoint
    compatibility matters, and do not expect a quality gain (Emu Video,
    [LIT-635](record/literature.d/LIT-635.md)).
  - `SOTA-397`: condition an unconditionally trained diffusion model on
    known frames with reconstruction guidance, not replacement (VDM,
    [LIT-627](record/literature.d/LIT-627.md)).
  - `SOTA-396`: fine-tune a reused image decoder and upsampler on video
    (Video LDM, [LIT-621](record/literature.d/LIT-621.md)).
  - `SOTA-392`: for a one-step rectified flow, distil first; reflow is
    an optional extra pass that costs many-step quality (Rectified Flow,
    [LIT-636](record/literature.d/LIT-636.md)).

### Added

- **Unit 6 of [#331](https://github.com/dmarx/anthology-of-the-sota/issues/331): reading notes for the video line.** Eighteen new `NOTE`s,
  all `Read`, one for every video paper filed in [#330](https://github.com/dmarx/anthology-of-the-sota/issues/330) and [#332](https://github.com/dmarx/anthology-of-the-sota/issues/332). Wan's
  `NOTE-333` goes from `Skimmed` to `Read` (v2), adding §5.2–5.7 and the
  benchmark tables.

### Changed

- **Nineteen LIT notes corrected to v2** against the full readings. About 55
  corrections in all. Among them:
  - HunyuanVideo's image scaling fit favours parameters, not data.
  - AnimateDiff does not lead the user study.
  - Rectified Flow's distilled one-step FID without reflow is 6.18, not 378.
  - Open-Sora 2.0's $200k run does not depend on its DC-AE.
  - Step-Video's 16×16×8 VAE measures below HunyuanVideo's on Open-Sora's
    benchmark.
  - CogVideoX's attention ablation is FVD "in early steps" only.
- **`SOTA-386` v3: `Active` → `Proposed`.** None of its three controlled
  sources separates images from compute, and none uses a separate image
  corpus. A `promote_when` names the missing comparison.
- **`SOTA-389` v2.** CogVideoX is removed as an adopter: its reported model
  trained on frame-caption summaries. SVD's contrary captioner result is
  added. Movie Gen's motion breakdown is prose, and says "most".
- **`SOTA-390` v2.** Restated to what CogVideoX reports: early-training FVD,
  factorized instability, and a cost of 1.08×–2.30× by resolution. Adds
  AnimateDiff's plug-in compatibility as a reason to factorize.
- **`SOTA-266` v3.** Four video reports state the logit-normal, not one.
  Rectified Flow's comparison is partly controlled.
- **`SOTA-333` v3.** Self Forcing's Table 2 is two matched pairs. Its
  clean-context inference is stated, not inferred.

### Added

- **XPos / LeX Transformer** — `LIT-638`. Unit 3 of `#326`, reversed from
  `#290`'s `D-variant` declines where it sat under the heading "Rotary
  Positional Embeddings" — a heading naming a different paper.

  **What the record was missing was a measure, not a method.** Four practices
  concern rotary encoding — `SOTA-063` recommends it, `SOTA-151` rescales it,
  `SOTA-179` truncates its low frequencies, `SOTA-153` drops it from a
  hybrid's global layers — and `SOTA-151` was already built on RoPE not
  extrapolating. The phenomenon was held. The number was not.

  Average attention resolution per layer, at the 1024 training length and at
  2048:

  | variant | 1024 | 2048 |
  | --- | --: | --: |
  | RoPE | **0.91** | **0.08** |
  | absolute sinusoidal | 0.87 | 0.28 |
  | ALiBi | 0.81 | **0.88** |
  | xPos + blockwise causal attention | 0.98 | 1.08 |
  | xPos alone | 0.98 | 0.54 |

  **RoPE is the best incumbent inside the training length and the worst
  outside it by an order of magnitude.** Two further things the paper reports
  rather than hides: half its own extrapolation comes from an inference-time
  masking change and not the encoding (0.54 → 1.08), and ALiBi's stability
  "comes from explicit decay, but it prevents the model from learning position
  dependency itself."

- **`SOTA-391`**, `Proposed` — estimate attention resolution before
  training, and measure it at two lengths rather than one. `unreplicated`, and
  the `promote_when` asks for the specific missing thing: the metric reported
  by someone who is *not* proposing an encoding, against a downstream
  long-context measurement. As it stands the paper shows its own method
  scoring highest and performing best, which is one coincident point rather
  than a correlation.

### Changed

- **`LIT-048` v4 — the ALiBi note was right about adoption and incomplete
  about the measurement.** Its standing section read *"RoPE won, and ALiBi is
  carried as the alternative that did not."* On the one axis ALiBi was built
  for, it is the **only incumbent that works** — and the trade has a price,
  0.2–0.3 perplexity above RoPE, attributed to the same mechanism that buys
  the stability.

  **A paper can lose on adoption while being right about the thing it
  measured.** The field preferred the perplexity and recovered extrapolation
  by other means, which is what `SOTA-151` and `SOTA-179` are.

- **`SOTA-151` v3 — the recommendation is unchanged and what it is evidence
  *for* is narrower than it looked.** Every result behind it is perplexity at
  the extended length, and `LIT-638` separates that from the thing wanted:
  "the perplexity does not explode but does not decrease at the same time. The
  ideal situation is to use the long context in the right way."

  This cuts both ways and the practice now says so. It **strengthens the
  motivation** — the defect it names has a number now, 0.91 → 0.08, and the
  number is not marginal. It **narrows the claim** — nobody in this record has
  measured whether a rescaled model recognises position at the target length,
  and the one available instrument says the unrescaled pattern barely does.
  Not degrading and working are different claims; only the first is
  established.

### Added

- **Units 1–5 of [#331](https://github.com/dmarx/anthology-of-the-sota/issues/331): the video generation line, continued.**
  - **Flow matching** (`LIT-630`) and **Rectified Flow**
    (`LIT-636`). These are the originating papers of the objective.
    Thirteen files named it and none held the source. SD3 now `extends`
    Rectified Flow, and Movie Gen `extends` Flow Matching.
  - **Imagen Video** (`LIT-637`), **Make-A-Video** (`LIT-632`) and
    **Emu Video** (`LIT-635`). Emu Video is the recipe Movie Gen builds
    on, and it has controlled ablations of factorization, zero terminal SNR,
    low-then-high resolution and freezing.
  - **CausVid** (`LIT-631`) and **Self Forcing** (`LIT-629`), the
    causal and streaming branch. Self Forcing is the record's first document
    on exposure bias.
  - **Open-Sora 2.0** (`LIT-634`), the only video report that states a
    training cost, and **AnimateDiff** (`LIT-633`).
  - **`SOTA-390`**: attend over space and time jointly in a video DiT,
    and budget for the 2.3× cost. `Proposed`, `converged`.
  - **`SOTA-389`**: caption training video with a video-native
    captioner. `Proposed`, `converged`.

### Changed

- **`SOTA-266` v2.**
  - `introduced_by` now names the 2022 originating papers, not SiT (2024).
  - Movie Gen's 5B flow-matching-against-diffusion ablation is added as
    video evidence.
  - The claim that uniform-timestep rectified flow "does not win" is scoped
    to SD3's setting. Both originating papers win with uniform timesteps in
    controlled comparisons.
- **`SOTA-333` v2.** Consensus moves from `unassessed` to `contested`, with
  `contested_by` Self Forcing. That paper argues against noised-history
  rollout without testing it. Its controlled test of the training half is
  split. Status is unchanged.
- **`SOTA-386` v2.** Five more reports were checked and none tests it. The
  separate image corpus is traced to Imagen Video, where it is asserted.
  Freezing is added as an untested alternative to the "alongside" clause.

### Added

- **Wan** (`LIT-619`, reading `NOTE-333`, `Skimmed`). This is
  Alibaba's open Wan2.1 text-to-video and image-to-video report, and the
  first video generation model in the record. It `extends` DiT (`LIT-448`)
  and the rectified-flow transformer (`LIT-449`). It is tagged under six
  existing topics and needed no new one. The abstract claims "scaling laws"
  that no curve in the body shows, and the text-encoder ablation it uses to
  choose umT5 has the rejected encoder marginally ahead on FID. Both are
  recorded as hedges.
- **The video generation line behind Wan**: nine LIT notes. The roots are
  VDM (`LIT-627`), Video LDM (`LIT-621`) and Stable Video
  Diffusion (`LIT-625`). The tokenizer is MAGVIT-v2 (`LIT-623`).
  The open and industrial reports are CogVideoX (`LIT-622`), Movie Gen
  (`LIT-626`), HunyuanVideo (`LIT-620`), Step-Video-T2V
  (`LIT-624`) and LTX-Video (`LIT-618`). They are joined by
  `extends` and `compared_against`, and every one records the hedge in its
  abstract.
- **`SOTA-386`, "Show a video diffusion model images before and
  alongside video"**, `Active`, `converged`. It is sourced from the three
  small controlled studies, with the large reports as adoption.

### Added

- **Better plain ViT baselines** — `LIT-628`. Unit 2 of `#326`, reversed
  from `#290`'s `D-variant` declines where it was filed as a variant called
  "SimpleViT". **It is not a variant** — it changes no architecture. It is a
  negative result about a belief concerning the incumbent, which is the class
  `#290` promoted `2102.11972` for on exactly that reasoning.

  Four pages, one ablation, ViT-S/16 on ImageNet-1k:

  | setting | 90ep | 150ep | 300ep |
  | --- | --: | --: | --: |
  | five changes | **76.5** | **78.5** | **80.0** |
  | − RandAugment + Mixup | 73.6 | 73.7 | **73.7** |
  | **original recipe** | **66.8** | **67.2** | **67.1** |

  **The original recipe does not improve with training.** 66.8 → 67.2 → 67.1:
  done by 90 epochs and slightly worse by 300. And the flat row shows what
  augmentation is actually for — the four structural changes set the level,
  augmentation sets whether a longer schedule means anything.

  None of the five changes is novel and **none is a regulariser**. One of them
  makes no difference and they say so.

- **`SOTA-388`** — the recipe, with each change's worth from the
  ablation. Filed with the warning that matters: adopt the structural changes
  and skip the augmentation and you get a model that is done at 90 epochs and
  a conclusion that longer training does not help.

- **`SOTA-387`**, `Proposed` — hold out a slice of *train* for model
  selection rather than selecting on the validation split. Beyer et al. keep
  1% of ImageNet-1k as a minival "to encourage the community to stop selecting
  design choices on the validation (de-facto test) set."

  Filed because **no document in this record had raised it**, and because the
  failure is invisible by construction: selection against a public split is
  distributed across a literature rather than happening inside one study, so
  no single methods section looks wrong. `Proposed` because nobody has
  measured what it costs, including this paper, which asserts the convention
  in one sentence.

### Changed

- **`SOTA-358` v2 — the load moved off one measurement and onto another.** Its
  first bullet had ViT-Large losing to ViT-Base on ImageNet-1k *"despite tuned
  regularisation"*. That configuration is the one Beyer et al. measured at
  **13.2 points below reachable**, and which had stopped learning by 90
  epochs.

  **This does not refute the crossover** — Beyer et al. ran ViT-S/16 only, and
  whether the ViT-L/ViT-B ordering flips under their recipe is untested. What
  it does is shift the practice onto its *second* measurement: the JFT
  9M/30M/90M/300M sweep with hyperparameters held fixed, which never depended
  on anyone tuning ImageNet-1k well. Status unchanged; the condition now comes
  from the bullet that can carry it.

### Added

- **Gopher** — `LIT-617`. Unit 1 of `#326`, reversed from `#290`'s
  `D-variant` declines where it had been recorded under the heading "Root
  Mean Square Layer Normalization".

  **48 files say "Chinchilla"**, `LIT-068` holds it, and twelve practices and
  theories cite it — `SOTA-096` is the `20 × params` ratio itself. Gopher is
  the allocation that ratio was derived against, and the arithmetic is the
  finding: **280B parameters on 300B tokens is 1.07 tokens per parameter,
  about nineteen times under-trained by the rule the record recommends.**

  Reading it supplies more than the substrate:

  - **A controlled study of parameter scale.** Six models, 44M to 280B, *same
    dataset and same 300B tokens* — which is what lets the 152-task analysis
    isolate scale rather than confound it.
  - **The gains are nonuniform, and quantified**: 79 tasks (51.2%) improve by
    over 25%, 57 (37.5%) by less, **16 (10.5%) not at all**. Largest single
    gain is BIG-bench Figure of Speech Detection at **+314%** (16.8% → 52.7%).
  - **Scale made three tasks worse**, named: Abstract Algebra, Temporal
    Sequences, High School Mathematics. Inverse scaling *inside* a controlled
    family, which is stronger than the cross-model version.
  - **Three different causes behind the small numbers**, separated rather than
    lumped: maths and logic where "scale alone" is unlikely to break through,
    common sense where the small models left no headroom, and language
    modelling where BPB limits relative movement.
  - **A negative numerics result**: *"we subsequently found that stochastic
    rounding does not fully recover mixed precision training performance."*

### Changed

- **`SOTA-015` v2.** Its closing hedge said stochastic rounding "recover[s]
  most of the memory while holding accuracy on many workloads" — stated with
  no scale attached. Gopher used it for bfloat16 parameters at 7.1B and 280B
  while its smaller models used float32 parameters, and reported afterwards
  that it does not fully recover mixed-precision performance. **A memory
  optimization verified at one size is not verified at twenty times that
  size**, and the record can now point at the case.

### Added

- **`SOTA-385`**, `Proposed` — tighten the gradient-norm clip as the
  model grows. Gopher clipped at 1.0 up to 1.4B and at **0.25 for 7.1B and
  280B**, "for improved stability".

  Filed because **three held practices say to clip and none names a value**:
  `SOTA-035` says to clip, `SOTA-071` says to use a dynamic threshold, and a
  reader following them picks a framework default tuned for a much smaller
  model. `Proposed` and `unreplicated` because the value is *reported, not
  ablated* — the paper does not show the 1.0 run failing — and the clip moved
  together with the learning rate across the same family, which the paper does
  not separate.

### Fixed

- **`#290`'s `D-variant` decline rule ranked papers by their contribution
  rather than by what they say about the incumbent.** Re-read as `#326`:
  **6 of 27 reverse**, 2 reclassify to `D-cluster`, 19 stand.

  The rule was *"catalogue variant; nothing held depends on it and the
  incumbent is filed"* — a question about the paper. `1801.01401` was declined
  on four record mentions of KID, and what the paper carries is a proof that
  **no unbiased estimator of FID exists**, plus a construction where 50,000
  samples return the wrong ordering in all 100 trials. Filed as `LIT-615` in
  the metric sweep.

  **A mention count inherits the error.** For a paper whose contribution is a
  correction, "what the paper made" and "what the record depends on" come
  apart completely.

  Highest-value reversal: **Gopher** (`2112.11446`), declined under the
  heading "Root Mean Square Layer Normalization". **48 files say
  "Chinchilla"**, Chinchilla is held, and Gopher is the compute allocation
  Chinchilla corrects — the winner of a named comparison without the loser.
  Four more heading leaks sit in the same list, including AlphaCode recorded
  under the title of a different paper.

  Not recorded as a defect in `#290`'s execution. Its triggers were right and
  still are; the **question** behind the disposition was the wrong one, and
  the write-up did not say which question it had asked.

### Fixed

- **`SOTA-382` retired to `SOTA-374`.** `#323` fixed the `arxiv` uniqueness
  violation by retiring the duplicate *notes*, which cleared the lint. It did
  not catch that the **practices had collided too**: `SOTA-374` and
  `SOTA-382` both said to subsample frequent tokens, from Mikolov et al.
  §2.3, and both were `Active`.

  Nothing could have caught it. Uniqueness is declared on `arxiv`, and there
  is no equivalent for a recommendation — two practices can say the same
  thing in different words and no check can tell.

  They disagreed about the evidence:

  | | `SOTA-382` | `SOTA-374` |
  |---|---|---|
  | consensus | `emerging` | `contested` |
  | the accuracy claim | "it improves the rare ones" | helps similarity, **costs 4.4–5.4 on analogies** |
  | the discard rule | described | stated, `1 − √(t/f)` at `t ≈ 10⁻⁵` |

  `SOTA-374` is right, because `LIT-607` ran the ablation. The direction of
  retirement is decided by that measurement, and it is the opposite of what
  incoming-link counts would have chosen.

### Changed

- **`SOTA-374` v4** absorbs what `SOTA-382` had that it lacked — the argument
  for **why speed and accuracy move together**, and the falsifier that comes
  with it. An update spent on a very frequent token is nearly redundant with
  the last thousand, so dropping it costs almost no signal and the freed
  budget goes where each occurrence still carries information.

  **That is a claim about the data, not the model**, so it should fail on a
  near-uniform unit distribution — the test to run before assuming the
  practice transfers off text. It is now stated *against* `LIT-607`'s
  ablation rather than beside it: the mechanism predicts a gain concentrated
  in rare items, the ablation finds it on similarity and a loss on analogies,
  and those are compatible without the argument being evidence for the
  analogy case.

- **`LIT-603` v3** absorbs the two readings `LIT-609` held and it did not:

  - **Negative sampling is a deliberate degradation and the paper says so.**
    NEG descends from NCE, which "approximately maximize[s] the log
    probability of the softmax", and the authors drop that on purpose: *"we
    are only concerned with learning high-quality vector representations, so
    we are free to simplify NCE as long as the vector representations retain
    their quality."* **NEG is not an estimator of anything.**
  - **`k` falls from 5–20 to 2–5 as data grows** — the earliest of four
    arguments that the negative count is not a quality dial, alongside
    `THEORY-085`'s `log N` ceiling, `LIT-591`'s closing batch-size gaps and
    `SOTA-377`'s saturation at 32k. Whether it is the same phenomenon is left
    open, because the objectives differ and nobody has connected them.

### Added

- **KID, and the case against comparing FID numbers** — `LIT-615`.
  Bińkowski et al. (2018), *Demystifying MMD GANs*. The sweep's largest
  finding, and it is not about KID.

  The record held three documents on FID — `LIT-611` for the definition,
  `LIT-501` on its ≈1.3% seed floor, `LIT-563` on its ImageNet-class
  dependence — and **not one of them mentions that the estimator is biased,
  or that two FID values are comparable only at equal `n`.** Those are the
  oldest published objections of the three and the only ones with a proof.

  - Estimating a distance whose true value is 0 (CIFAR-10 train vs test),
    FID still reads about **8.1 at n=10,000**, the entire CIFAR test set,
    and is still falling. KID is essentially 0 by n=2000.
  - At `d=2048` on ReLU-censored normals, `FID(P₁,Q) ≈ 1123.0 > 1114.8 ≈
    FID(P₂,Q)` while the 50,000-sample estimates come out **reversed in all
    100 trials**, with standard deviations of 0.2 and 0.5. **The variance is
    smallest exactly where it misleads.**
  - And it is not a bad formula: Appendix D.3 shows **no unbiased estimator
    of FID exists** on any class containing two-component Gaussian mixtures.

  `#290` had declined this paper as a `D-variant` on four record mentions.
  That was wrong, and instructively so: **the mentions counted KID, and the
  paper's load is about FID.**

- **Post-hoc calibration** — `LIT-616`. Guo et al. (2017), *On
  Calibration of Modern Neural Networks*. `LIT-514` describes itself as "the
  record's first document on probability calibration"; it was also the only
  one, so the record entered this literature at a 2025 refinement and never
  held the 2017 paper the refinement is built on.

  Modern networks are miscalibrated where a 1998 LeNet is not, at a typical
  **4–10% ECE**, and depth, width, BatchNorm and *less* weight decay each
  make it worse while improving accuracy. The mechanism is an overfitting
  the error rate hides: on CIFAR-100 test error falls 29% → 27% **inside the
  region where NLL is already rising**.

- **The Inception Score** — `LIT-614`. Salimans et al. (2016). Unit E's
  shape again: the record held the winner of a named comparison (`LIT-611`
  states its advantage as being over the Inception Score) and the re-run
  (`LIT-615`, which finds the *opposite* answer on monotonicity) and
  not the incumbent. Filed on weak substrate and the note says so.

  Two things worth having from it. The metric was introduced as an automatic
  stand-in for a Mechanical Turk panel, on **50k samples** because part of
  what it measures is diversity — a sample-size requirement as old as the
  measure. And the human baseline it was validated against is itself
  unstable: "results change drastically when we give annotators feedback
  about their mistakes."

- **`SOTA-383`** — fix `n` before comparing FID values, and settle a
  close call with an unbiased estimator rather than a tighter error bar.
  `extends` `SOTA-307`, because the two error terms add and only one of them
  shrinks when you average runs.

- **`SOTA-384`** — calibrate with a single temperature fitted on
  held-out data. It cannot move the argmax, so accuracy is unchanged by
  construction, and it beats vector scaling, matrix scaling and all three
  binning methods — **including the two that strictly contain it**, which is
  the informative part: miscalibration is intrinsically low dimensional.

- **`THEORY-095`** — why no amount of averaging fixes it. `Active`
  rather than `Proposed`: the non-existence half is proved, not proposed.

### Changed

- **`SOTA-307` v2.** A `Conditions` bullet naming the second error term. This
  practice asks for an error bar around the FID estimator's own mean; the
  estimator is biased, the offset is shared by every seed, and averaging runs
  does not touch it.

- **`SOTA-315` v2 — a correction.** Its `consensus_note` said nobody else had
  reported "the separation **or the remedy**". The remedy is temperature
  scaling, Guo et al. 2017, nine years older than the practice and the
  field's standard post-hoc calibrator. What is new in `LIT-514` is applying
  it inside model selection rather than after it. The record had not held
  the paper, which is how a claim about the field came to be made about the
  record.

### Added

- Arora, Li, Liang, Ma and Risteski (2016), *A Latent Variable Model
  Approach to PMI-based Word Embeddings* ([LIT-613](record/literature.d/LIT-613.md)), read in full
  ([NOTE-332](record/notes.d/NOTE-332.md)).
- [THEORY-094](record/theory.d/THEORY-094.md) (`Proposed`): a random-walk discourse model over isotropic
  word vectors gives PMI ≈ ⟨v, v'⟩/d in low dimensions, and isotropy denoises
  relation offsets. It `extends` [THEORY-093](record/theory.d/THEORY-093.md) and [THEORY-089](record/theory.d/THEORY-089.md).

### Fixed

- `main` failed the lint after [#317](https://github.com/dmarx/anthology-of-the-sota/issues/317): word2vec's two papers were each filed
  twice ([LIT-603](record/literature.d/LIT-603.md) and [LIT-609](record/literature.d/LIT-609.md), [LIT-604](record/literature.d/LIT-604.md) and [LIT-610](record/literature.d/LIT-610.md)), and `arxiv` is unique.
  [LIT-609](record/literature.d/LIT-609.md) and [LIT-610](record/literature.d/LIT-610.md) are `Superseded` by the entries that merged first, and
  [SOTA-381](record/practices.d/SOTA-381.md) and [SOTA-382](record/practices.d/SOTA-382.md) now cite [LIT-603](record/literature.d/LIT-603.md). Five backticked references in the
  pre-concretization spelling are updated.

### Added

- Levy and Goldberg (2014), *Neural Word Embedding as Implicit Matrix
  Factorization* ([LIT-612](record/literature.d/LIT-612.md)), read in full ([NOTE-331](record/notes.d/NOTE-331.md)).
- [THEORY-093](record/theory.d/THEORY-093.md) (`Active`): skip-gram with negative sampling is a weighted
  factorization of the PMI matrix shifted by log k.

### Changed

- [LIT-607](record/literature.d/LIT-607.md) `extends` the paper. [THEORY-089](record/theory.d/THEORY-089.md) and [THEORY-092](record/theory.d/THEORY-092.md) `extend` the theory,
  whose result both had assumed without a document behind it.

### Added

- Baroni, Dinu and Kruszewski (2014), *Don't count, predict!*
  ([LIT-608](record/literature.d/LIT-608.md)), read in full ([NOTE-330](record/notes.d/NOTE-330.md)). It is the "predict beats
  count" result that [LIT-607](record/literature.d/LIT-607.md) reversed, and [LIT-607](record/literature.d/LIT-607.md) now `corrects` it.
- [SOTA-380](record/practices.d/SOTA-380.md), filed `Rejected`: its recommendation to prefer
  prediction-based over count-based word vectors. [SOTA-379](record/practices.d/SOTA-379.md) `corrects` it.

### Changed

- [SOTA-374](record/practices.d/SOTA-374.md) (subsampling) records Baroni et al.'s supporting evidence
  beside [LIT-607](record/literature.d/LIT-607.md)'s contrary ablation. It stays contested.

### Added

- **FID** — `LIT-611`. Unit H of `#304`, and the largest substrate
  defect the audit found: **68 documents in this record mention FID and none
  held the paper.** For scale, `LIT-587` (ViT) had 47 and `LIT-588` (CLIP)
  45.

  The dependency was not background. The record already held **two papers
  about this metric's failure modes and two `Active` practices for surviving
  them** — `LIT-563` (FID can be moved without improving images), `LIT-501`
  (its ≈1.3% seed-noise floor), `SOTA-337` (when its gains cannot be
  trusted), `SOTA-307` (report it as an error bar) — plus `SOTA-338` turning
  on it. **Four documents deep into the critique, and no note for the thing
  being criticised.**

  Reading it supplies the two things every one of those documents assumes
  without restating:

  - **The Gaussian fit is an assumption, stated once.** "We assume the coding
    units to follow a multidimensional Gaussian", after which the Fréchet —
    Wasserstein-2 — distance between the two fitted Gaussians is
    `‖m − m_w‖²₂ + Tr(C + C_w − 2(C·C_w)^{1/2})`.
  - **The validation was ordering deliberately degraded distributions.**
    Figure 3 shows FID rising monotonically under Gaussian noise, blur,
    implanted black rectangles, swirls, salt-and-pepper, and CelebA
    contaminated with ImageNet. That is the evidence offered. It is not
    evidence that small gaps between two competent models mean anything, and
    the paper does not claim it is — which is precisely the gap `LIT-501`
    later measured at ≈1.3%.

  And the provenance is `DP-010` in one line: **the field's default
  generative metric is a subsection of a paper about two time-scale update
  rules and Nash equilibria.** Its stated advantage is over the Inception
  Score — one comparison against one incumbent.

  `extended_by: LIT-501, LIT-563`, which is the lineage the record already
  had and could not express.

### Added

- Levy, Goldberg and Dagan (2015), *Improving Distributional Similarity with
  Lessons Learned from Word Embeddings* ([LIT-607](record/literature.d/LIT-607.md)), read in full
  ([NOTE-329](record/notes.d/NOTE-329.md)). Tuned alike, count-based and prediction-based word vectors
  show no consistent winner, and SGNS beats GloVe on every task. The paper
  `corrects` [LIT-602](record/literature.d/LIT-602.md) on that claim.
- [SOTA-379](record/practices.d/SOTA-379.md) (`Active`): give count-based baselines the same design
  choices and tuning before crediting an embedding method.
- [THEORY-092](record/theory.d/THEORY-092.md) (`Proposed`): 3/4-power context smoothing helps because PMI
  overweights rare contexts.

### Changed

- [SOTA-375](record/practices.d/SOTA-375.md) (3/4-power negatives) gains its first measurement and stays
  `Proposed`: two exponents compared, a small gain for SGNS.
- [SOTA-374](record/practices.d/SOTA-374.md) (subsampling) is now `contested`: it helps similarity and costs
  4–12 points on analogies.
- [THEORY-089](record/theory.d/THEORY-089.md) adds the paper as a source. [LIT-602](record/literature.d/LIT-602.md) and [LIT-603](record/literature.d/LIT-603.md) point to it.

### Added

- [THEORY-091](record/theory.d/THEORY-091.md) (`Proposed`), from [LIT-503](record/literature.d/LIT-503.md): command-to-outcome mutual
  information scores an interface because it measures how reliably the
  operator's input determines the outcome at the chosen horizon. That rewards
  a learnable channel, not an intuitive one. It explains [SOTA-309](record/practices.d/SOTA-309.md), the
  bimodal convergence to inversion, and the sign flip under shared autonomy.
  The paper's own explanation, by intuitiveness, predicts neither.

### Added

- `concept-geometry`, a twenty-second topic, for how concepts are laid out
  in a model's representation space ([ADR-060](record/decisions.d/ADR-060.md)). [LIT-460](record/literature.d/LIT-460.md), [THEORY-034](record/theory.d/THEORY-034.md),
  [LIT-526](record/literature.d/LIT-526.md) and [THEORY-063](record/theory.d/THEORY-063.md) take it as primary; twelve more documents on
  superposition, sparse autoencoders, probing, word-vector offsets and
  representational convergence add it.
- Park, Choe and Veitch, *The Linear Representation Hypothesis and the
  Geometry of Large Language Models* ([LIT-606](record/literature.d/LIT-606.md)), read in full
  ([NOTE-328](record/notes.d/NOTE-328.md)): the trunk [LIT-460](record/literature.d/LIT-460.md), [LIT-458](record/literature.d/LIT-458.md) and [THEORY-034](record/theory.d/THEORY-034.md) had each said
  was missing. Its account is [THEORY-090](record/theory.d/THEORY-090.md) (`Proposed`): a concept's
  word-pair direction, probe and steering vector are one object under an
  inner product that makes separable concepts orthogonal. One practice,
  [SOTA-378](record/practices.d/SOTA-378.md) (`Proposed`, contested by [LIT-526](record/literature.d/LIT-526.md)): compare concept
  directions after whitening by the unembedding covariance.

### Documentation

- [LIT-460](record/literature.d/LIT-460.md), [LIT-458](record/literature.d/LIT-458.md) and [THEORY-034](record/theory.d/THEORY-034.md) no longer say the Linear Representation
  Hypothesis is absent from the record. [LIT-460](record/literature.d/LIT-460.md) `extends` the new paper,
  [LIT-526](record/literature.d/LIT-526.md) is `compared_against` it, and [THEORY-034](record/theory.d/THEORY-034.md) `extends` its account.

### Added

- **word2vec, both papers** — `LIT-610`, `LIT-609` and two
  practices. Unit G of `#304`, the last on its worklist, filed with the
  audit's qualification intact: **weak substrate**. Three record documents
  mention word2vec and all three use it as a benchmark task inside the µP
  cluster.

  **`LIT-610`** — CBOW and Skip-gram, whose contribution is
  computational: delete the non-linear hidden layer and word vectors become
  cheap enough for 1.6B words in under a day, with hierarchical softmax over
  a Huffman tree cutting the output cost from `V` to about `log₂(V)`. The
  `King − Man + Woman ≈ Queen` result is here, and so is the part worth
  keeping — they **built a test set** rather than leaving it an anecdote.

  **`SOTA-381` — sample negatives, and let `k` fall as data grows.**
  Where negative sampling comes from, with the sentence that licenses it:
  NEG descends from NCE, which approximately maximises the softmax log
  probability, and the paper drops that property on purpose — *"we are free
  to simplify NCE as long as the vector representations retain their
  quality"*. **Negative sampling is not an estimator of anything**; it is a
  task chosen because its by-product is good. Also carried: the noise
  distribution is the unigram to the **3/4** power, a measured constant with
  no derivation, inherited by everyone since.

  **`SOTA-382` — subsample frequent tokens.** "Significant speedup"
  *and* better representations of rare words, both at once, because an update
  spent on a very frequent token is nearly redundant with the last thousand.
  A claim about the signal, not the model: it should hold for any
  heavy-tailed unit distribution and fail for a uniform one.

  **The finding that made the unit worth doing:** `k` in **5–20** for small
  datasets, **2–5** for large ones. The number of negatives that helps
  *decreases* with data. That is a **fourth** independent argument that the
  negative count is not a quality dial — after `THEORY-085`'s `log N`
  ceiling, `LIT-591`'s vanishing batch-size gaps, and `SOTA-377`'s
  measured saturation at 32k — from a different literature, **ten years
  earlier**, and pointing further.

### Added

- **word2vec**, both papers, filed on request:
  - "Efficient Estimation of Word Representations in Vector Space"
    ([LIT-604](record/literature.d/LIT-604.md), read as [NOTE-325](record/notes.d/NOTE-325.md)) introduces skip-gram, CBOW and the
    analogy test.
  - "Distributed Representations of Words and Phrases and their
    Compositionality" ([LIT-603](record/literature.d/LIT-603.md), read as [NOTE-326](record/notes.d/NOTE-326.md)) `extends` it
    with negative sampling, subsampling and phrases.
  - **[SOTA-374](record/practices.d/SOTA-374.md), `Active`**: subsample frequent tokens with discard
    probability 1 − √(t/f).
  - **[SOTA-375](record/practices.d/SOTA-375.md), `Proposed`**: draw negatives from unigram^(3/4). The
    paper asserts this without numbers.
- **GloVe** ([LIT-602](record/literature.d/LIT-602.md), read as [NOTE-327](record/notes.d/NOTE-327.md)), `compared_against` the
  second word2vec paper.
- **[THEORY-089](record/theory.d/THEORY-089.md), `Proposed`**, from GloVe and word2vec: word vectors are
  linear because they encode log co-occurrence statistics.
- GloVe and the second word2vec paper also carry `signal-structure`.
  GloVe's argument is about which statistic of text carries meaning.
  word2vec's subsampling and phrase detection rest on word frequency and on
  multi-word units.

### Documentation

- **GloVe's win over word2vec is on word2vec's defaults.** Training time was
  proxied by negative samples, which the authors acknowledge should be
  relaxed, and the margin is 2.6 points.
- **word2vec's headline comparison is not controlled**, since it compares
  public vectors across very different data sizes and dimensions.
- **The 3/4 exponent carries no numbers in its source.**

### Added

- **SigLIP** — `LIT-605`, `SOTA-376` and `SOTA-377`. Unit F of
  `#304`, and rank 20 of `#290`'s tier B.

  **`SOTA-376` — score each pair with a sigmoid.** Keep CLIP's
  supervision (`SOTA-359`) and change only the normalization: a softmax term
  cannot be computed until every pairwise similarity exists, a sigmoid term
  can be computed from one pair, so **the loss stops needing a global view**.
  The distributed implementation then collapses — negatives swapped between
  devices in a ring, **no all-gathers**, only a `b×b` per-device block ever
  materialised, where the usual implementation holds `|B|×|B|`. It is also
  better below 16k batch "by a large margin", which is exactly the regime a
  small lab operates in and the one least represented in the consensus.
  84.5% ImageNet zero-shot in two days on **four TPUv4 chips**.

  With the one line a reimplementation drops: `|B|²−|B|` negatives against
  `|B|` positives means the imbalance "dominates the loss" at initialisation,
  so a **learnable bias** sits beside the temperature, initialised `b = −10`
  and `t' = log 10`. Same shape as CLIP's clipped temperature.

  **`SOTA-377` — the batch ceiling, and it is lower than the belief.**
  Trained from 512 to **one million**, performance **saturates around 32k** —
  for the **softmax** loss as well as the sigmoid, so it is a property of the
  objective family. The paper says why nobody had seen it: existing studies
  "stop at 64k". The ceiling sits just below where everyone stopped looking.

  Filed `unreplicated` rather than `emerging`: the measurement is the only
  one of its kind, and what is missing is a second group going as far
  (`DP-005`).

  It joins two arguments the record already holds, and **none of the three is
  downstream of the others** — `THEORY-085`'s `log N` cap on the InfoNCE
  certificate, `LIT-591`'s finding that batch-size gaps "decrease or
  disappear" with longer training, and this direct measurement. Three
  independent reasons the negative count is not a quality dial.

### Added

- **MAE** — `LIT-601`, two practices and one theory. Unit E of `#304`,
  and filed because the record had been **arguing against it without holding
  it**: `SOTA-250` ("predict representations of masked regions, not their
  pixels") names MAE as the competitor it beats on compute.

  **`SOTA-372` — the asymmetric encoder-decoder.** Give the encoder only
  the visible tokens; introduce mask tokens afterwards, to a small decoder
  you discard. **3× or more** faster pretraining and less memory, "without
  any specialized sparse operations". The encoder also never trains on an
  input distribution that does not occur at inference.

  **`SOTA-373` — set the masking ratio by redundancy, not by BERT.**
  BERT masks 15% of tokens; MAE masks **75%** of image patches, which the
  paper calls "surprisingly high" and justifies from the signal rather than
  from a sweep: images have heavy spatial redundancy, so a low ratio leaves a
  task solvable "by extrapolation from neighboring patches". The transferable
  part is the question — **can a competent interpolator solve my masked
  task?** — and cheap proxies for it beat a pretraining sweep.

  **`THEORY-088` (`Proposed`) — information density is why the ratio
  differs.** The account: the same objective specifies different tasks on
  different signals, so 15% on a dense one demands comprehension while 15% on
  a redundant one demands interpolation. Directionally useful and resting on
  **two points from two literatures**, chosen by groups with different
  architectures, protocols and compute, with redundancy invoked qualitatively
  and never measured. `promote_when` asks for three modalities under one
  recipe, correlated against an independent redundancy statistic — and says a
  fourth data point would not do, because the claim is that the optimum
  *tracks* density.

  **What this unit deliberately does not do is relitigate `SOTA-250`.** Its
  position stands. The two practices filed here are the parts of MAE
  orthogonal to the target choice: an encoder that skips mask tokens and a
  ratio set by redundancy are needed whether you reconstruct pixels or
  predict representations, which is why they outlived the argument they
  arrived in. `SOTA-250`'s own architecture has the same asymmetry.

### Changed

- **`LIT-216` v3 — `compared_against: LIT-601`.** I-JEPA is the paper
  that ran the MAE comparison `SOTA-250` quotes, and the record held the
  winner of a named comparison without the loser.
  `representation-and-encoding` added alongside, on the document's own merit
  — its whole claim is about what the representation is trained to be — and
  so the relation binds.

### Added

- **Automatic Evaluation of Topic Coherence** (Newman et al., NAACL 2010),
  [LIT-600](record/literature.d/LIT-600.md), read as [NOTE-324](record/notes.d/NOTE-324.md). It `extends` Reading Tea Leaves
  ([LIT-597](record/literature.d/LIT-597.md)) and is sourced by URL. **[SOTA-371](record/practices.d/SOTA-371.md), `Proposed`**: score
  topic coherence as the average PMI of the top-word pairs over a large
  external corpus, as a validated proxy for the human task in [SOTA-368](record/practices.d/SOTA-368.md). It
  stays Proposed because the validation covers LDA topics only.

### Documentation

- **"At or nearing inter-annotator agreement" is not like-for-like.** The
  ceiling compares one annotator with the mean of the other eight. The
  method is compared with the mean of all nine. The corpora were also chosen
  for varied topic quality, which raises rank correlations.

### Fixed

- **Two recorded titles failed the source check** when arXiv answered, and
  `source-mismatch` fails the build. [LIT-463](record/literature.d/LIT-463.md)'s title was truncated and now
  gives the full title. [LIT-462](record/literature.d/LIT-462.md) now spells "μP" as the paper does, not
  "muP". Neither was part of this filing. Both surfaced because this run of
  the lint reached arXiv.

### Added

- **SwAV** — `LIT-598` and `SOTA-370`. Unit D of `#304`. Predict
  one view's *cluster code* from another view's representation instead of
  comparing features pairwise, with an **equipartition constraint** — the
  batch is equally divided across prototypes via Sinkhorn-Knopp — doing the
  anti-collapse work. No pairwise comparisons, so large and small batches
  both work. 75.3% ImageNet linear with a standard ResNet-50.

  **`SOTA-370` files multi-crop**, which is the separable half: two
  standard crops plus several small ones, so view count rises while compute
  does not. Unusually well evidenced for a component — the introducing paper
  transplanted it into **SimCLR, DeepCluster and DeepCluster-v2** and gained
  **2–4 points top-1 in every one**. What it implies is worth keeping: if
  view *count* is what helps and view *resolution* is what costs, the loss is
  learning from the number of independent comparisons rather than the
  fidelity of each.

- **DINOv2** — `LIT-599` and `SOTA-369`. The thesis is about data,
  not objectives: existing self-supervised methods already give
  general-purpose features "if trained on enough curated data from diverse
  sources".

  **`SOTA-369` files curation by retrieval** — use the curated datasets
  you already have as queries and pull their nearest neighbours (typically 4;
  more "leads to more collisions") out of the uncurated pool, deduplicate,
  train. It is an index job: Faiss, 20 nodes, under two days for 142M images.
  The comparison that makes it a practice is **142M curated against 142M
  randomly sampled from the same source**, which controls volume, source and
  crawl and leaves selection as the only difference. Against ImageNet-22k it
  *matches* on ImageNet-1k while significantly outperforming it elsewhere —
  curation aimed at generality buys the tail, not the seed distribution, so a
  pipeline evaluated only on its seeds would have reported no gain.

### Changed

- **[THEORY-087](record/theory.d/THEORY-087.md) v2 — a fifth account, and a group declining to
  choose.** SwAV's equipartition constraint is on the *assignment*, not the
  embedding and not the architecture, so neither existing family covers it.
  It also carries the sharpest reminder that these mechanisms are not clean:
  SwAV's entropy regularisation `ε` must be kept low because "a strong
  entropy regularization generally leads to a trivial solution where all
  samples collapse" — **a mechanism introduced to prevent collapse has a
  setting at which it causes it.**

  DINOv2 then joins as a sixth source by *stacking* mechanisms rather than
  selecting: a KoLeo regulariser spreading features within a batch, plus
  Sinkhorn-Knopp centering borrowed from SwAV, on top of DINO's
  teacher-student asymmetry — three ablation rows, no account. A group with
  the compute to settle the question assembled the answers additively
  instead, which is the most informative datum the document has and is
  evidence for none of them.

### Added

- **Reading Tea Leaves** (Chang et al., NIPS 2009), [LIT-597](record/literature.d/LIT-597.md), read as
  [NOTE-323](record/notes.d/NOTE-323.md). It is `compared_against` LDA ([LIT-592](record/literature.d/LIT-592.md)) and sourced by URL,
  since the paper has no arXiv version or DOI. **[SOTA-368](record/practices.d/SOTA-368.md), `Active`**:
  when a latent space is meant to be read by people, measure its
  interpretability with a word- or topic-intrusion task, not by held-out
  likelihood.

### Changed

- **[NOTE-322](record/notes.d/NOTE-322.md) and [THEORY-086](record/theory.d/THEORY-086.md)** (LDA) now point to it. It is the human
  evaluation the LDA note said the record lacked, and the theory adds that
  people and model agree least on documents that span several subjects.

### Documentation

- **"Likelihood is negatively correlated with interpretability" is stronger
  than the data.** It rests on 18 fitted models, and the trend is carried
  mostly by one, CTM. Within LDA and pLSI the human scores barely move. The
  practice states the weaker claim the data supports.

### Added

- **Latent Dirichlet Allocation** (Blei, Ng and Jordan 2003), [LIT-592](record/literature.d/LIT-592.md),
  read as [NOTE-322](record/notes.d/NOTE-322.md), filed on request after the phrase-as-lemma
  discussion. Its source is the JMLR page, since the paper's old MIT Press
  DOI is listed as deleted. It is tagged `signal-structure` first, with
  `representation-and-encoding` and `generative-modeling`.
  **[THEORY-086](record/theory.d/THEORY-086.md), `Proposed`**: a document is better modelled as a
  mixture of topics than as one. The support is held-out perplexity, and the
  multi-topic claim is confounded with LDA's Dirichlet prior. No practice
  is filed.

### Documentation

- **Two caveats on the paper are recorded in its note.** Its pLSI baseline
  uses folding-in, which the authors say favours pLSI, so LDA's win is
  conservative. Its classification features were fit on all documents,
  test documents included.

### Changed

- **[LIT-409](record/literature.d/LIT-409.md) appends `signal-structure`** (implicit vocabulary, Feucht et al.).
  The first sweep left it out because its evidence is model-internal. Its
  framing, though, is a claim about language: lexical items are
  non-compositional units of meaning. That is the property [THEORY-022](record/theory.d/THEORY-022.md)
  measures from the language side, and the note already pairs the two.

### Added

- **The collapse-avoidance cluster** — four notes (`LIT-594` BYOL,
  `LIT-593` SimSiam, `LIT-596` Barlow Twins, `LIT-595`
  VICReg), three practices and one theory. Unit C of `#304`, and the unit
  where the record's existing `representation collapse` prose finally gets
  its sources.

  **`SOTA-365` — break the symmetry.** Drop negatives entirely and match
  two views, provided the branches are not the same function: a prediction
  MLP on one, a stop-gradient on the other. Removing the stop-gradient sends
  the loss to its floor of −1 in a few steps; removing the predictor gives an
  unsupervised Mean Teacher, which collapses. The EMA target is *optional* —
  BYOL drops it and still gets 52.5% with a closed-form predictor or 66.5%
  by raising only the predictor's learning rate, but ≈25% if the projector's
  rate rises too. The shared content: **the branch being predicted must not
  be chasing the branch predicting it.**

  **`SOTA-367` — or put the constraint in the loss.** A hinge keeping
  each dimension's standard deviation above `γ`, plus a decorrelation term.
  The two fail differently and both are needed: the floor stops the embedding
  becoming a point, the decorrelation stops it becoming a line. Buys the
  whole list VICReg names as unnecessary — weight sharing, batch norm,
  feature-wise normalisation, output quantisation, stop-gradient, memory
  banks. The variance term is the one component here with evidence of working
  *outside* its own method.

  **`SOTA-366` — the three-line collapse detector.** Log the per-channel
  standard deviation of the ℓ2-normalised embedding. **0** is collapsed;
  **1/√d** is scattered on the unit hypersphere, and `1/√d` is computable
  from the embedding width alone, so one run can be judged without a
  baseline. Filed `unassessed` — the derivation is arithmetic but whether
  people run it has not been measured here, and an invented consensus value
  would be worse than the admission.

  **`THEORY-087` (`Proposed`) — nobody knows why any of this works.**
  Four methods, four incompatible accounts, all landing within a couple of
  points (74.3 / 67.7 / 73.2 / 73.2). The sharpest contradiction is
  numerical: **BYOL reports 0.3% when its momentum encoder is removed, and
  SimSiam — which *is* that removal — reports 67.7%.** Two careful groups,
  the same ablation, three orders of magnitude apart.

  `promote_when` asks for the experiment none of the four ran: one codebase,
  one recipe, the candidate mechanisms varied independently. Every result in
  hand is a paper removing components of its own method under its own
  learning rate, weight decay and augmentation set — and BYOL's own note that
  removing weight decay makes both BYOL and SimCLR diverge is a reminder of
  how much of a recipe is load-bearing for reasons unrelated to collapse.

### Added

- **SimCLR** — `LIT-591`, plus `SOTA-361` and `SOTA-362`.
  Unit B of `#304`. Augment, encode, project, NT-Xent — no memory bank, no
  special architecture — with every piece ablated.

  **The augmentation set is the task specification**, and the tell is that
  the model can "almost perfectly identify the positive pairs" while learning
  a poor representation: solving the pretext task and learning the
  representation are different events. Crop alone fails because crops of one
  image share a colour histogram, so colour identifies the image; crop **with**
  colour distortion works because the second augmentation destroys the
  statistic the first left intact. And the policy does not port across
  objectives — over colour-distortion strength 1/8 → 1 the contrastive probe
  rises 59.6 → 64.5 while the supervised model falls 77.0 → 75.4, and
  AutoAugment (searched under supervision) is best for supervised and worse
  than plain crop+colour for contrastive.

  **The projection head is a sacrificial layer.** Nonlinear beats linear by
  ~3 points and no head by >10, yet the layer *before* it is >10 points
  better than the layer after. Verified rather than conjectured: recovering
  the applied transformation from `h` gives rotation 67.6% (chance 25) and
  original-vs-corrupted 99.5%, against 25.6% and 59.6% from `g(h)`. The head
  absorbs the invariance the loss demands so the representation does not
  have to.

- **MoCo** — `LIT-590` and `SOTA-363`. Contrastive learning as
  dictionary look-up, wanting a dictionary both **large** and **consistent**:
  a queue buys size independently of the batch, an EMA-updated key encoder
  buys consistency.

  The momentum ablation is the result that propagated — `m` = 0 (copy the
  query encoder each step, which is what anyone writes first) **fails to
  train**; 0.9 → 55.2, 0.99 → 57.8, 0.999 → 59.0. At equal `K` a memory bank
  is 2.6% worse because its keys were written across a whole past epoch. Size
  without consistency underperforms. Filed `emerging` with the split stated:
  the slow encoder converged and became the EMA teacher, the queue did not —
  SimCLR dropped it for a large batch and CLIP uses in-batch negatives at
  32,768.

- **The batch-norm leak** — `SOTA-364`, sourced to **both** papers.
  BN makes a sample's activations depend on its batch-mates, and in a
  contrastive objective the batch-mates are the answer. MoCo's appendix names
  the mechanism: per-device BN statistics act as a signature telling the model
  which sub-batch the positive is in, so it never compares content. Two
  independent fixes three months apart — shuffle the batch across devices for
  the key encoder (MoCo), or aggregate BN statistics globally (SimCLR).

  Filed separately because **the failure is silent in the only place people
  look**: training loss drops *faster* with the bug, and pretext-task accuracy
  — the natural thing to monitor — moves in the wrong direction, so the metric
  that should catch it endorses it instead.

### Changed

- **`signal-structure` swept across the record.** Every LIT, THEORY and
  SOTA document was checked, 969 in all. The test was whether someone
  browsing the topic would be right to expect the document, which means a
  property of the data has to be load-bearing, not incidental. 17 documents
  append the topic after their existing ones. Each carries a history entry
  naming the property:
  - **Zipfian tokens and activation rank:** [THEORY-032](record/theory.d/THEORY-032.md), [SOTA-274](record/practices.d/SOTA-274.md) and [LIT-457](record/literature.d/LIT-457.md).
  - **Data spectra:** [LIT-555](record/literature.d/LIT-555.md) (the 1/f² image spectrum) and [LIT-328](record/literature.d/LIT-328.md) (the
    data eigenspectrum sets the learning-curve exponent).
  - **Frequency distributions of facts:** [LIT-450](record/literature.d/LIT-450.md) and [SOTA-267](record/practices.d/SOTA-267.md).
  - **Image redundancy and imperceptible bits:** [SOTA-263](record/practices.d/SOTA-263.md), [SOTA-187](record/practices.d/SOTA-187.md) and
    [LIT-062](record/literature.d/LIT-062.md).
  - **Corpus statistics:** [SOTA-243](record/practices.d/SOTA-243.md) (the scaling exponent as a measure of
    redundancy), [SOTA-238](record/practices.d/SOTA-238.md) (irreducible entropy per domain), and [THEORY-057](record/theory.d/THEORY-057.md),
    [SOTA-172](record/practices.d/SOTA-172.md) and [LIT-205](record/literature.d/LIT-205.md) (generated text is narrower).
  - **What the signal carries:** [THEORY-056](record/theory.d/THEORY-056.md) and [LIT-484](record/literature.d/LIT-484.md).
  - None takes it as primary. Candidates left out because the data property
    was model-internal, assumed rather than claimed, or incidental: [LIT-003](record/literature.d/LIT-003.md),
    [LIT-036](record/literature.d/LIT-036.md), [LIT-126](record/literature.d/LIT-126.md), [LIT-409](record/literature.d/LIT-409.md), [LIT-440](record/literature.d/LIT-440.md), [LIT-449](record/literature.d/LIT-449.md), [LIT-489](record/literature.d/LIT-489.md), [LIT-518](record/literature.d/LIT-518.md),
    [THEORY-025](record/theory.d/THEORY-025.md), [THEORY-053](record/theory.d/THEORY-053.md), [SOTA-175](record/practices.d/SOTA-175.md), [SOTA-205](record/practices.d/SOTA-205.md), [SOTA-269](record/practices.d/SOTA-269.md) and [SOTA-360](record/practices.d/SOTA-360.md).

### Added

- **CPC / InfoNCE** — `LIT-589`, `SOTA-360` and `THEORY-085`.
  Unit A of `#304`. Predict in latent space and score the prediction as a
  **density ratio** `f(x,c) ∝ p(x|c)/p(x)` against sampled negatives, rather
  than reconstructing the observation.

  The justification is a budget argument with a number in it: a generative
  loss on `p(x|c)` must account for every detail of the observation, and
  *"images may contain thousands of bits of information while the high-level
  latent variables such as the class label contain much less (10 bits for
  1,024 categories)"*. Reconstruction spends capacity in proportion to the
  data's entropy; the density ratio spends it in proportion to what the
  context and target share — which is why one mechanism with a deliberately
  plain encoder gives a 48.7% ImageNet linear probe (+9 absolute over the
  best prior pretext task), 64.6% LibriSpeech phone classification against
  39.7 for MFCCs, skip-thought-level sentence vectors without a word-level
  decoder, and a gain on 4 of 5 DeepMind Lab tasks as an auxiliary loss.

  **`THEORY-085` files the part the folklore drops.** The paper derives
  `I ≥ log(N) − L_N` and says the bound tightens with `N`. Since `L_N` is a
  cross-entropy and so non-negative, the same inequality **caps the bound at
  `log N`** — about 10.4 nats at CLIP's batch of 32,768, however much the
  pair actually shares. Two sentences get conflated downstream: the
  estimator's optimum is *independent* of `N` (the paper proves this), while
  the MI *certificate* is bounded *by* `N`. "More negatives is better" is a
  claim about the certificate, and it saturates.

### Changed

- **`SOTA-359` v2 — CLIP's caption practice now declares `extends:
  SOTA-360`**, which is what `LIT-588` itself says: CLIP cites Oord et
  al. by name for its loss, and its recipe is the image-text instance of the
  general recommendation. `training-optimization` added alongside, on the
  document's own merit — a practice justified entirely by a training-
  efficiency measurement belongs on that page — with the reasoning recorded
  in its history rather than left as a silent retag (`ADR-049`).

### Added

- **ViT** — `LIT-587` and `SOTA-358`. Cut the image into fixed
  patches, linearly embed them, add learned 1D position embeddings and run an
  unmodified transformer encoder. The only 2D prior injected by hand is the
  patch grid, plus interpolating the position embeddings when fine-tuning at
  higher resolution.

  The practice states the **threshold**, not the architecture, because the
  threshold is the half that gets dropped. Pre-trained on ImageNet-1k,
  ViT-Large is *worse* than ViT-Base; on ImageNet-21k they draw level; only
  on JFT-300M does the larger model pay. With hyperparameters held fixed on
  random JFT subsets, ViT-B/32 is much worse than a comparable ResNet-50 at
  9M images and better at 90M+. A domain prior is a substitute for data, and
  below the crossover it is still the better bet — which is the opposite of
  what "transformers beat CNNs" tells a practitioner with 50k images.

  Also worth keeping: the paper's own self-supervised attempt (masked patch
  prediction, 79.9%) landed **4 points behind supervised pre-training**. The
  paper that opened the modern vision backbone did not solve its own
  pre-training objective.

- **CLIP** — `LIT-588`, `SOTA-359` and `SOTA-357`. Train an
  image encoder and a text encoder to match 400M (image, text) pairs
  contrastively, then build a classifier for any label set by embedding its
  class names.

  `SOTA-359` files the objective **with the efficiency argument that
  justifies it**, because the argument is what transfers. Predicting the
  caption's words learns 3× slower than predicting a bag-of-words encoding
  of the same text; swapping predictive for contrastive gives a further 4×.
  The claim is not that contrastive representations are better in the
  abstract — it is that the exact-words target is an expensive way to buy
  supervision the matching target buys cheaply. The simplifications are part
  of the method: a linear projection rather than a non-linear head, a random
  square crop as the only augmentation, nothing initialised from pre-trained
  weights, and a learned temperature **clipped at logit scale 100, which the
  paper says was necessary to prevent divergence**.

  `SOTA-357` files prompt templating and embedding-space ensembling:
  `"A photo of a {label}."` is +1.3% on ImageNet over the bare class name,
  80 ensembled contexts add +3.5% more, and together ~+5% across 36 datasets
  — which the paper measures as equivalent to **4× more compute**, and which
  is free once amortised because the ensemble averages into one cached
  classifier. Filed because it means two papers can report zero-shot numbers
  for the same checkpoint that differ by more than most claimed
  improvements.

### Changed

- **`SOTA-196` v2 — the zero-shot/in-distribution conflict has two
  measurements, and the earlier one is larger.** The practice said one clean
  measurement (`LIT-072`, OWL-ViT, 2022). CLIP had made it in 2021: a
  supervised linear classifier fitted on ImageNet raises ImageNet accuracy by
  **9.2%**, "roughly 3 years of improvement in SOTA", and produces **no
  average improvement across seven natural distribution shifts** — the gain
  concentrates on ImageNetV2 while accuracy falls 4.7% on ImageNet-R, 3.8% on
  ObjectNet, 2.8% on Sketch and 1.9% on ImageNet-A.

  CLIP also supplies the continuum OWL-ViT does not: effective robustness
  decays monotonically from 0-shot through 128-shot to fully supervised, and
  zero-shot is more robust than a few-shot model at *equal* ImageNet
  accuracy. So the trade is not a property of one hyperparameter's setting
  but of how much distribution-specific supervision the model has seen.

  The old `consensus_note` said one measurement, which was true of the record
  and not of the literature. That is the failure mode a consensus reading has
  when the record is the only thing it counts.

### Changed

- **The catalogue manifest reads `k-diffusion` and `captum`, and deliberately
  does not read `open_clip`.** `#290` triaged the four catalogue repositories
  by hand: **128 distinct arXiv identifiers, 22 already held, 106 missing, of
  which 25 were promoted and 81 declined.**

  `captum` is kept as a `catalogue` rather than reclassified as an `adoption`
  index, although it is Meta's production library. Its README links
  `1810.03292` and `2106.07475`, both of which examine methods it ships
  anyway — a list that carries its own critiques is enumerating a literature,
  not reporting a convergence.

  `open_clip` is dropped and the manifest header says why: nine of its
  fifteen missing identifiers are checkpoint rows or dataset cards and two
  more are its own papers, so the `arxiv` extractor reads a model roster
  rather than a feature index. That is a third kind of index, and not one
  `#183` has a reading for.

### Documentation

- **The triage's headline finding, recorded in the curation log.** The
  catalogues' strongest yield was not practice candidates but **substrate the
  record leans on and never filed**: `2010.11929` (ViT) is cited by no held
  document though 47 say "ViT", and `2103.00020` (CLIP) by none though 45 say
  "CLIP". Three more of the same shape — the Muon analysis `2509.26030` (59
  documents say "Muon"), ALBERT `1909.11942` (12), Swin `2103.14030` (9).

  This class is invisible to both previous audits by construction: `#202`
  looks for practices filed under a topic no source holds, `#289` for
  techniques several libraries ship, and a substrate paper supports no
  practice of its own and is shipped by nothing.

  Also recorded: a heading in a catalogue names the feature a citation
  supports, not the paper, and ranking on headings mis-ranked 4 of 23; and
  arXiv's HTTP 406 is rate limiting rather than a difference between luria's
  client and curl, which the previous entry had half-right.

### Added

- **AWQ** — `LIT-585` and `SOTA-356`. Weight-only low-bit
  quantization that protects the ~1% of channels whose **activations** are
  largest, by scaling them up before rounding rather than keeping them in
  higher precision.

  Two choices carry it, and both are easy to get backwards. Salience is read
  from activations, not weight magnitude — weight magnitude is a poor proxy
  and choosing by it is a different, worse method. And the protection is a
  *scaling*, not a mixed-precision carve-out: keeping 1% of channels in 16
  bits makes the kernel irregular and costs more than the quantization saves.

  Filed `compared_against: SOTA-185` because the paper runs that comparison
  itself (`ADR-011`). The distinguishing claim against GPTQ is
  **generalization**, not accuracy at a bit width: GPTQ fits a calibration
  objective and AWQ deliberately does not. The record holds no independent
  test of that claim, and the practice says so.

- **`LLM.int8()`** — `LIT-586` and `SOTA-355`. Int8 inference for
  the projections, at no measured quality cost up to 175B, by pulling the
  systematically emergent outlier feature dimensions into a separate 16-bit
  multiplication and quantizing the other 99.9% vector-wise.

  The decomposition is the whole method. Naive int8 works on small
  transformers and breaks on large ones, which had read as "quantization gets
  harder with scale"; the paper's contribution is the diagnosis that a few
  feature dimensions emerge with very large magnitudes and dominate
  prediction, so one scale cannot cover two distributions.

  What it buys is **memory, not speed** — the payoff is 175B on one server of
  consumer GPUs. Reports of int8 being slower than 16-bit at small batch are
  consistent with this method rather than evidence against it.

### Documentation

- **Both close `#289`'s worklist**, which came from the library sweep: AWQ was
  one of three items in 91 that two independent adoption indexes both carried,
  and `LLM.int8()` surfaced because `bitsandbytes` turned out to be a library
  name covering two techniques — NF4, which the record held as `SOTA-230`,
  and this one, which it did not.

- **Both practices carry a `consensus_note` naming what was checked and
  when**, which is what `ADR-058` asks for. Both are `converged` on adoption
  grounds and both notes say that is adoption and not evidence (`DP-005`).

- **The "no performance degradation" headline is flagged rather than
  repeated.** It means *no degradation the authors measured, on their suite,
  up to 175B* — an absence-of-evidence claim of the shape `DP-010` names. The
  emergent-outlier characterization is the part later work built on.

### Added

- **`signal-structure`, a twenty-first topic,** for what the data itself is
  like, independent of any model. That covers the statistics and structure
  of language, images and other signals: spectra, heavy-tailed distributions
  and what counts as a unit. It comes from **[ADR-045](record/decisions.d/ADR-045.md) v3**. That decision admitted a
  finding about language measured on people as a THEORY, then rejected adding
  a topic for it. [ADR-059](record/decisions.d/ADR-059.md) has since made the topics an axis rather than a
  scope, which overturns that rejection. [THEORY-022](record/theory.d/THEORY-022.md) and [LIT-410](record/literature.d/LIT-410.md) take it as
  their primary topic, and [THEORY-080](record/theory.d/THEORY-080.md), whose account rests on natural-image
  spectra, adds it second. [ADR-045](record/decisions.d/ADR-045.md) itself stays `Proposed`, because its
  promotion condition, a second such finding, is unmet.

### Fixed

- **[SOTA-161](record/practices.d/SOTA-161.md) and [LIT-198](record/literature.d/LIT-198.md) described [SOTA-085](record/practices.d/SOTA-085.md) as a bodyless stub** that says
  nothing about precision. It has since been written up and points to
  [SOTA-161](record/practices.d/SOTA-161.md) for the one numerical change it names, so both passages are
  corrected and no longer cite [ADR-012](record/decisions.d/ADR-012.md).

### Documentation

- **`#289`'s adoption sweep, as far as it goes mechanically.** Three
  repositories enumerated at pinned commits — `vllm` (feature matrix),
  `diffusers` (scheduler exports), `transformers` (quantization backends) —
  giving 91 distinct items.

  **Only three of the seven repositories can be enumerated at all.**
  `sglang`, `Megatron-LM` and `pytorch-lightning` put what they implement in
  prose; their README headings are *News*, *About*, *Getting Started*. That is
  reading, not extraction, and the issue had assumed seven comparable sweeps.

  **The adoption/catalogue split turns out to be per index, not per
  repository.** `transformers` is an adoption repository whose quantization
  table lists 22 backends the record holds none of — `AQLM`, `EETQ`, `HIGGS`,
  `SINQ`, `SpQR`, `VPTQ` and so on. Those are integrations somebody
  contributed, not techniques the field adopted, which is precisely what
  `#290` was warned about for x-transformers. Same repository, different
  index, different kind.

  **The signal that survives is the cross-repository intersection** — an item
  two independent indexes both carry. Three of 91: `AWQ`, `bitsandbytes` and
  `GGUF`. That ratio is the result: presence in one index is nearly
  worthless.

  Judged apart, only one of the three is a technique gap. `AWQ` is genuinely
  absent while GPTQ is held three times. `bitsandbytes` is a library name
  covering two techniques, one of which the record already holds (`SOTA-230`,
  NF4) and one of which it does not (`LLM.int8()`) — so the row was a false
  positive and a true one at once. `GGUF` is a container format and is
  declined.

  Neither gap is filed here: the network cannot reach arXiv from this session
  (`luria lint` reports 140 unverified identifiers), and filing papers whose
  metadata cannot be checked is how a wrong identifier enters the record
  (`ADR-009`).

### Changed

- **Decision statuses brought up to date.** 22 decisions were still
  `Proposed`, and most of them had been in force for days. Each was audited
  against the config and the record, and the owner ruled on the rest.
  - **Now `Active` (18):** [ADR-028](record/decisions.d/ADR-028.md), [ADR-030](record/decisions.d/ADR-030.md), [ADR-031](record/decisions.d/ADR-031.md), [ADR-033](record/decisions.d/ADR-033.md), [ADR-034](record/decisions.d/ADR-034.md),
    [ADR-037](record/decisions.d/ADR-037.md), [ADR-038](record/decisions.d/ADR-038.md), [ADR-039](record/decisions.d/ADR-039.md), [ADR-040](record/decisions.d/ADR-040.md), [ADR-041](record/decisions.d/ADR-041.md), [ADR-042](record/decisions.d/ADR-042.md), [ADR-043](record/decisions.d/ADR-043.md), [ADR-050](record/decisions.d/ADR-050.md),
    [ADR-053](record/decisions.d/ADR-053.md), [ADR-054](record/decisions.d/ADR-054.md), [ADR-055](record/decisions.d/ADR-055.md), [ADR-056](record/decisions.d/ADR-056.md) and [ADR-057](record/decisions.d/ADR-057.md).
  - **[ADR-031](record/decisions.d/ADR-031.md)** was promoted by the owner without the event its promotion
    condition named. **[ADR-042](record/decisions.d/ADR-042.md)** is promoted as a standing permission before
    its first use. Both status notes say so.
  - **[ADR-030](record/decisions.d/ADR-030.md)** carries a note that [ADR-053](record/decisions.d/ADR-053.md) amends it. **[ADR-038](record/decisions.d/ADR-038.md)** records
    that [ADR-055](record/decisions.d/ADR-055.md) reversed its "no cross-scheme invariants" clause.
    **[ADR-037](record/decisions.d/ADR-037.md)** records that its upstream blocker was fixed.
  - **[ADR-024](record/decisions.d/ADR-024.md) is `Superseded` by [ADR-049](record/decisions.d/ADR-049.md).** It was an options paper, each
    of its options was taken by a later decision, and [ADR-049](record/decisions.d/ADR-049.md) reversed its
    premise.
  - **[ADR-012](record/decisions.d/ADR-012.md) is `Deferred`.** Its `kind:` field was never adopted, and half
    of its motivation is gone.
  - **Still `Proposed`:** [ADR-045](record/decisions.d/ADR-045.md), which waits on a second case (its heading
    is corrected), and [ADR-058](record/decisions.d/ADR-058.md), which waits on `LU-#319`, `#294` and `#291`.
- **Acknowledgement directives updated to match.** 30 that vouched only for
  now-Active decisions are removed. About 20 mixed ones drop the promoted
  codes and keep the rest. Those naming [ADR-024](record/decisions.d/ADR-024.md) or [ADR-012](record/decisions.d/ADR-012.md) now give their
  current status. Changelog fragments are left as written.
- **[ADR-054](record/decisions.d/ADR-054.md)'s Decision text** now lists `link --fix` in `make ready`, which
  the Makefile already ran.

### Added

- **`src/scripts/repo_features`** — what the big libraries implement, read at
  a named commit and diffed against the record (`#291`).

  ```
  python -m src.scripts.repo_features
  ```

  Four modules: `refs` resolves a repository to a SHA and reads a file at it,
  `extract` pulls a list out of what was read, `corpus` indexes the record,
  `run` diffs against the previous run's lockfile. The manifest
  (`repos.yaml`) says which files to read and how.

  **Pinning works after all.** The GitHub API is 403 through the session
  proxy, which is what made an exact ref look unavailable, and `git ls-remote`
  is plain git over HTTPS and answers with the SHA directly. `ADR-058` requires
  the observation to name what it read; the `#287` pilot could not, having
  fetched from `main`.

  **The `gone` column is the point.** A technique leaving a library is a
  signal nothing else in this project can produce, and per `ADR-058` it means
  read this again, never lower the consensus.

### Changed

- **The record's matching is two answers, not one** — measured, and the
  reason this harness is worth more than a grep.

  `#287` found that matching a practice's **body** over-matches: µP looks like
  an FP8 practice because it mentions FP8 once. Restricting to **titles and
  summaries** has the opposite failure and it is just as bad — `speculative
  decoding` finds nothing, though `SOTA-227` is *"Decode with a draft model
  and an accept-reject rule"* and is exactly that.

  So a body hit is a **candidate** and a subject hit is a **confirmation**, and
  the report prints both. Collapsing them hides whichever error the choice
  made, and the point of generating this rather than grepping is that the
  discarding becomes an artifact somebody can look at twice.

- **`pyproject.toml` declares the dependencies it was already using.** `fire`
  and `loguru` have been imported by `audit/verify_arxiv.py` since it was
  written and were declared nowhere; the description still called the package
  the frozen migration, which stopped being true when the audit script landed.

### Documentation

- **Three defects the live run found that the tests did not**, each now a
  regression test. The fixtures were idealised and the real files are not:
  `diffusers` puts several exports on one line inside a lazy-import table, so
  an anchored pattern read it as exporting nothing; vLLM's quantization page
  holds an API reference as well as a hardware matrix, so reading every table
  put `get_name()` in a list of techniques; and a table's header is whatever
  that table calls its first column, so dropping the literal word *Feature*
  left `Implementation` behind.

### Added

- **`biomolecular-modeling`, a twentieth topic** ([ADR-059](record/decisions.d/ADR-059.md)), for models
  whose data is molecules. The decision also records the rule the gap
  exposed: the topics organize the anthology, they do not bound it. Content
  the axis cannot place is a finding about the axis. `CLAUDE.md` said work
  qualified "if the recommendation is one the nineteen topics can express",
  and it now says the opposite. ESM-1b ([LIT-505](record/literature.d/LIT-505.md)) and RNA-FM ([LIT-506](record/literature.d/LIT-506.md)) had
  been filed under the nearest wrong word, and they take the new topic as
  their primary.
- **AlphaFold 2** (`#163`), [LIT-583](record/literature.d/LIT-583.md), read as [NOTE-321](record/notes.d/NOTE-321.md).
  - **[SOTA-354](record/practices.d/SOTA-354.md), `Proposed`**: self-distill on confident predictions for
    unlabeled inputs.
  - **[SOTA-353](record/practices.d/SOTA-353.md), `Proposed`**: train a head that predicts the model's
    own accuracy, and use it to rank and filter.
  - **[THEORY-084](record/theory.d/THEORY-084.md), `Proposed`**: the alignment places the coarse fold
    and refinement does not need it.
- **AlphaFold 3** (`#163`), [LIT-584](record/literature.d/LIT-584.md), read as [NOTE-320](record/notes.d/NOTE-320.md), `extends`
  AlphaFold 2. It is a second source for [SOTA-353](record/practices.d/SOTA-353.md).
  **[SOTA-352](record/practices.d/SOTA-352.md), `Proposed`**: when a structure predictor goes
  generative, distill from a regression model so disorder is not
  hallucinated as structure.

### Documentation

- **AlphaFold's ablations and AF3's benchmark success rates exist only as
  figures.** The record cites their direction and the stated significance
  tests, not magnitudes read off plots.
- **AF3's PoseBusters comparison favors the baseline.** Vina is given the
  solved pocket and AF3 is not.

### Added

- **Where library evidence goes** ([ADR-058](record/decisions.d/ADR-058.md), `#288`). A repository that
  implements a technique is evidence about **`consensus`** and about nothing
  else — not `status`, which is this record's own editorial position, and not
  whether the practice is any good.

  `DP-005` says adoption is not evidence. What makes `consensus` the exception
  is that its vocabulary is about adoption by construction: *"converged: the
  field agrees and dissent is marginal, whether or not each adopter made the
  choice deliberately"*.

  **The judgement goes in `consensus_note`, naming what was checked and when.**
  "Widely adopted" cannot be disagreed with; "implemented in vLLM, SGLang and
  TensorRT-LLM as of 2026-09" can be, by somebody who looks.

  **The observation goes in a generated report** (`#291`), fetched at a pinned
  ref rather than `main` — the same split the record already runs on, where a
  source holds what a person concluded and a view holds what a machine derived
  ([ADR-004](record/decisions.d/ADR-004.md)). The pilot demonstrated the hazard by fetching from `main` and
  being unable to say afterwards which `main`.

  **Removal is a prompt, not a verdict.** A technique leaving a library means
  read this again, never lower the consensus — a library can narrow its scope.

  A library does **not** become a `LIT` note: a note names a source that
  resolves and holds still, and `README.md` on `main` does neither. Where the
  repository has a paper, the paper is already the note — vLLM's is `LIT-112`,
  Megatron's `LIT-043`.

### Documentation

- **Three defects found by trying to write that decision down**, none of them
  visible from the pilot:

  - **`implementations:` means four different things** (`#293`) — 85 distinct
    values across 84 practices, mixing models (`llama2`, `PaLM`), *methods*
    that are not implementations at all (`NeRF`, `CycleGAN`, `Progressive
    Distillation`), libraries (`vLLM`, `diffusers`) and prose that escaped
    into a list field. Declared in no scheme. This is why the decision routes
    around it: a fifth meaning would end any chance of it being readable.
  - **Eight practices assert a non-default `consensus` on no stated grounds**
    (`#294`) — four of them `universal`, which is the strongest claim the axis
    makes. 183 of 191 already carry a note, so the honest declaration of
    `consensus_note` is 8 documents away.
  - **luria cannot declare a field it is not also checking** (`LU-#319`) — a
    field's type comes from its constraint, so an optional prose field's
    `blurb` is unreachable. `consensus_note` stays undeclared for now despite
    this decision making it load-bearing.

### Documentation

- **`#183` pilot: vLLM, one repository worked end to end** (`#287`), to
  establish a method before thirteen repositories are swept.

  Twenty-one features enumerated from vLLM's compatibility matrix and its
  quantization backend table, matched against 351 practices. **Fourteen
  matched, seven did not.**

  **The seven gaps are real.** None of AWQ, prefix caching, RadixAttention,
  expert parallelism, CUDA graph capture or GGUF appears anywhere in the
  practices *or* the literature. AWQ is the sharpest: GPTQ is in the record
  three times and its direct competitor zero times, which is a hole that looks
  like a judgement nobody made.

  **The fourteen matches are mostly false positives**, and that is the
  methodological result. Eighteen matched practices carry weak consensus, but
  the rows do not survive reading: µP matched *FP8* because its body mentions
  FP8, a masked-diffusion practice matched *speculative decoding* because it
  discusses draft models. A practice body mentions a technique for many
  reasons and only one of them is being about it. The grep is a candidate
  generator with poor precision and useful recall — the gaps are what it is
  for.

  **`SOTA-105` (PagedAttention) and `SOTA-113` (continuous batching) carry no
  `consensus` field at all** — the two most universally adopted serving
  techniques in the field, unassessed. Not moved here: one repository is thin
  evidence for a claim about what the field does, and `#289` checks seven
  more. `consensus` is absent or unassessed on 160 of 351 practices.

  No practice changed in this contribution. The output is the worklist, the
  method, and the negative result about matching.

### Removed

- **`SOTA-037` and `SOTA-038` no longer `extends` `SOTA-036`**, and
  `SOTA-038` drops the `model-architecture` tag that was added to bind that
  edge ([ADR-057](record/decisions.d/ADR-057.md)).

  `extends` means *"the earlier practice this one builds on and could not
  stand without."* `SOTA-036` is a specific recipe — decoder-only, a broad web
  corpus, a fixed context, a single next-token objective. "ICL permits
  few-shot task adaptability" does not depend on any of those particulars; it
  depends on the class of model. Change the corpus and it still stands, which
  is the test the relation sets and the edge fails.

  What is real was already written down. All three practices name
  `source: LIT-035` and `introduced_by: LIT-035` — three recommendations drawn
  from one paper, siblings by provenance. `extends` was saying "same paper" a
  second time, in a vocabulary that means something else, and the `practice`
  chain read that second saying as a lineage of refinement.

  `SOTA-279 extends SOTA-038` stays: chain-of-thought exemplars genuinely
  could not stand without few-shot prompting.

### Changed

- **`SOTA-038` → v3.** Its v2 note justified the **relation** rather than the
  document: *"In-context learning is a capability of the decoder-only-at-scale
  family [SOTA-036](record/practices.d/SOTA-036.md) describes, which is what the relation between them
  asserts."* The tag test is the document's — would someone browsing
  `model-architecture` be right to expect "ICL permits few-shot task
  adaptability"? They would not. With the relation gone the tag has no
  argument left.

  `SOTA-037` keeps `model-architecture` deliberately. It was original tagging
  rather than a tag added to bind an edge, so removing it is a different
  judgement on different evidence.

- **`docs/practice-lines.md` loses a line and gains two singletons.** The
  narrative — GPT-3's recipe, then in-context learning, then chain of thought
  — is real and is not a *line of practice*. It is readable from `LIT-035`'s
  page, which lists all three practices sourced to it.

  The chain's one unbound line goes to zero as a consequence, not as the
  reason. Had the relations survived the "could not stand without" test, the
  right outcome would have been to leave the row standing and say so.

### Added

- **Graph neural networks** (`#163`, "graph representation / gnn"). A small
  set chosen for what it lets the record recommend. None needed a new
  topic, because the claims are architectural and evaluative:
  - GCN, [LIT-582](record/literature.d/LIT-582.md), skimmed, with no note. The reference baseline,
    with no practice of its own.
  - GIN, [LIT-580](record/literature.d/LIT-580.md), read as [NOTE-319](record/notes.d/NOTE-319.md). **[THEORY-083](record/theory.d/THEORY-083.md), `Active`**:
    the 1-WL bound, reached only by injective aggregation. **[SOTA-351](record/practices.d/SOTA-351.md),
    `Active`**: sum aggregation with an MLP when structure carries the signal.
  - Pitfalls of GNN evaluation, [LIT-581](record/literature.d/LIT-581.md), read as [NOTE-318](record/notes.d/NOTE-318.md).
    **[SOTA-350](record/practices.d/SOTA-350.md), `Active`**: many splits and seeds, and one shared
    protocol.
  - Where did the gap go?, [LIT-579](record/literature.d/LIT-579.md), read as [NOTE-317](record/notes.d/NOTE-317.md).
    **[SOTA-349](record/practices.d/SOTA-349.md), `Active`**: retune message-passing baselines before
    crediting graph transformers.

### Documentation

- **GIN's test-set advantage is decisive only on featureless graphs.** On
  seven of nine benchmarks most gaps are within a standard deviation, and
  mean–MLP beats GIN on PTC.
- **"The gap vanished" holds on the Peptides datasets only.** On
  PascalVOC-SP and COCO-SP, tuned GPS still leads by 5.6 and 9.6 F1.

### Added

- **The techniques behind LARQL** (`#163`, "use SQL to query and modify the
  information in your network"). The tool (github.com/chrishayuk/larql) is
  software without an evaluation, so the papers it rests on are filed
  instead:
  - FFN layers as key-value memories, [LIT-575](record/literature.d/LIT-575.md), read as [NOTE-312](record/notes.d/NOTE-312.md).
    **[THEORY-081](record/theory.d/THEORY-081.md), `Proposed`.**
  - ROME, [LIT-578](record/literature.d/LIT-578.md), read as [NOTE-315](record/notes.d/NOTE-315.md). Its account is
    **[THEORY-082](record/theory.d/THEORY-082.md), `Rejected` at filing**: causal tracing shows where
    to edit.
  - "Does Localization Inform Editing?", [LIT-574](record/literature.d/LIT-574.md), read as
    [NOTE-313](record/notes.d/NOTE-313.md), `corrects` ROME. On GPT-J, per-fact tracing explains
    0.1% of the variance in edit success, and the edit layer explains 94.7%.
  - MEMIT, [LIT-576](record/literature.d/LIT-576.md), read as [NOTE-316](record/notes.d/NOTE-316.md). **[SOTA-347](record/practices.d/SOTA-347.md),
    `Proposed`, contested**: batch many edits over a range of MLP layers,
    choosing the range by measured edit success.
  - RippleEdits, [LIT-577](record/literature.d/LIT-577.md), read as [NOTE-314](record/notes.d/NOTE-314.md), contests it. **[SOTA-348](record/practices.d/SOTA-348.md),
    `Active`**: evaluate an edit on its implications. Weight editors
    average 38–66, and in-context editing does better.

### Documentation

- **LARQL's `INSERT` is not the weight edit it is described as.** Its
  default `MODE KNN` records a retrieval override. That is closer to what
  RippleEdits favors than to ROME or MEMIT.
- **Geva et al.'s key-value reading is weaker than its title.** Value-key
  agreement is at most 3.5%, on 160 keys of one small model, and outputs
  are mostly compositions.

### Added

- **FLUX.1 Kontext** (`#163`, "flux1"), [LIT-573](record/literature.d/LIT-573.md), read as [NOTE-310](record/notes.d/NOTE-310.md),
  `extends` SD3 ([LIT-449](record/literature.d/LIT-449.md)). It is the only paper describing FLUX.1. No
  practice is filed, because no design choice in it is ablated.
- **The FLUX.2 latent-space report** (`#163`, "flux2"), [LIT-572](record/literature.d/LIT-572.md), read as
  [NOTE-311](record/notes.d/NOTE-311.md), `extends` Kontext. FLUX.2 has no paper, and this BFL
  technical report (`url:`) is its technical account. **[SOTA-346](record/practices.d/SOTA-346.md),
  `Proposed`**: retune the training timestep shift for each autoencoder
  latent, and never rank latents under one schedule. The shift alone moves
  FID by 61–86%, and the RAE vs FLUX.2 ranking flips without it.

### Documentation

- **The FLUX.2 report's √(m/n) shift rule is partly a grid-edge effect.**
  RAE's predicted α = 6.93 is the top of the searched grid, and the report
  says the optimum may lie above it. FLUX.2's optimum (4.63) misses its
  prediction (2.82). Recorded on the paper's entry. It is not filed as a
  practice.
- **FLUX.1's wider VAE is less learnable than SD's** (gFID 10.1 against 7.7)
  despite far better reconstruction. That is the trade-off the FLUX.2 VAE
  was built to escape.

### Added

- **A nineteenth topic: `capability-thresholds`** — *a capability that arrives
  abruptly rather than smoothly: emergence at scale, grokking after long
  training, phase transitions in learning; which axis it turns on, and whether
  the discontinuity is real or an artefact of how it was measured*
  ([ADR-056](record/decisions.d/ADR-056.md)).

  **Nineteen documents across all three schemes carried
  `analysis-and-evaluation`, and for most it was the primary** — the emergence
  debate (`LIT-470`, `LIT-471`, `THEORY-040`, `SOTA-200`), the grokking line
  (`LIT-085`, `LIT-537` through `LIT-540`, `THEORY-069` through `THEORY-072`)
  and the singular-learning-theory account of stagewise development
  (`LIT-543`, `LIT-544`, `THEORY-073`, `THEORY-074`). One topic had absorbed
  an entire subject.

  Its blurb is "how to find out whether something worked", which is a word for
  **methods**. "A capability appears above 100B parameters" and "a network
  generalises long after it has memorised" are claims about **what happens**.
  Filing the phenomenon and the argument about the phenomenon under one word
  makes the disagreement invisible.

  One word rather than three, though the axes differ — scale, training time,
  dataset size. In every case the claim is that a curve has a knee and the
  argument is whether the knee is in the phenomenon or in the plot, and
  `THEORY-074` exists precisely to say a Bayesian and a dynamical transition
  are *different events* — a distinction that is unstatable if each axis has
  its own topic.

  Not `emergence`, which smuggles in the answer: the whole dispute is whether
  the word describes the model or the metric.

### Changed

- **Four primary topics moved** — `LIT-470` (*Emergent Abilities*), `LIT-471`
  (*Are Emergent Abilities a Mirage?*), `LIT-538` (Power et al., which named
  grokking) and `THEORY-069` (the one `Active` grokking explanation). Each is
  this claim and nothing else. The other fifteen documents **appended** the
  tag, because `primary_topic` derives `{tags[0]}` and a prepend silently
  refiles a document ([ADR-055](record/decisions.d/ADR-055.md)).

  No document left `analysis-and-evaluation`. The methodological reading is
  real and additional.

- **The topic count is nineteen** in `luria.yaml`'s header comment, in the
  vocabulary's own `blurb` and in the two sentences in `CLAUDE.md` that state
  it. Dated records keep their number: they were true when written.

### Added

- **Logit lens and tuned lens** (`#163`, "LogitLens"). The logit lens is
  filed as [LIT-570](record/literature.d/LIT-570.md), the original LessWrong post (`url:`). The tuned
  lens is [LIT-569](record/literature.d/LIT-569.md), read as [NOTE-308](record/notes.d/NOTE-308.md), which `extends` it.
  **[SOTA-343](record/practices.d/SOTA-343.md), `Proposed`**: read intermediate predictions through a
  tuned lens, not the raw logit lens, which fails on BLOOM, OPT and GPT-Neo
  and is biased where it works.
- **Sparse autoencoders** (`#163`, "SAE"). Gao et al., [LIT-571](record/literature.d/LIT-571.md), read as
  [NOTE-307](record/notes.d/NOTE-307.md), source two `Proposed` practices. **[SOTA-344](record/practices.d/SOTA-344.md)**: train
  with TopK, transposed-decoder initialization and an auxiliary dead-latent
  loss. **[SOTA-342](record/practices.d/SOTA-342.md)**: report fidelity as downstream loss in
  compute-equivalent terms, not as fraction recovered against zero ablation.
- **The case against SAE probes.** Kantamneni et al., [LIT-568](record/literature.d/LIT-568.md), read as
  [NOTE-309](record/notes.d/NOTE-309.md), is `compared_against` [LIT-571](record/literature.d/LIT-571.md). **[SOTA-345](record/practices.d/SOTA-345.md),
  `Active`**: probe with logistic regression on raw activations. On 113
  datasets, adding SAE probes changes AUC by −0.003, and it does not help
  in any hard regime.

### Documentation

- **"98.2% of loss recovered" corresponds to 10% of GPT-4's compute.** Gao et
  al.'s own footnote shows zero-ablation normalization flatters an SAE.
  This is the basis of [SOTA-342](record/practices.d/SOTA-342.md).
- **The tuned lens's prompt-injection result has no win against its
  baseline.** Its AUROC is near 1 on five of nine tasks, but a one-layer
  Mahalanobis detector matches or beats it on eight. The paper's version 6
  also says every lens in it was undertrained. Both are recorded on the note.
- **Not filed:** Bricken et al. and Cunningham et al., the 2023 SAE papers.
  The practices rest on the later work, which compares against them.

### Added

- **MARLIN** (`#163`, "marlin format"), [LIT-567](record/literature.d/LIT-567.md), read as [NOTE-305](record/notes.d/NOTE-305.md).
  It `extends` GPTQ ([LIT-081](record/literature.d/LIT-081.md)). **[SOTA-340](record/practices.d/SOTA-340.md), `Proposed`**: weight-only
  4-bit quantization speeds serving up only while the batch keeps the matmul
  memory-bound. End-to-end in vLLM that is 2.3–3.2× single-GPU at batch 16
  or below, and 1.1–1.2× at 128, on four GPU classes (Table 2).
- **SDXL** (`#163`), [LIT-566](record/literature.d/LIT-566.md), read as [NOTE-306](record/notes.d/NOTE-306.md). It `extends` LDM
  ([LIT-062](record/literature.d/LIT-062.md)). **[SOTA-341](record/practices.d/SOTA-341.md), `Proposed`**: condition on each training
  image's original size, instead of discarding or upsampling small images.
  The evidence is one class-conditional ImageNet run per arm (FID-5k 43.84
  discarding, 39.76 keeping, 36.53 keeping with conditioning).
- **FLUX-Reason-6M & PRISM-Bench** (`#163`), [LIT-565](record/literature.d/LIT-565.md), skimmed. There is
  no note and no practice. Supra2-IMG, the model the issue pairs with it, is
  not filed because it has no paper.

### Documentation

- **MARLIN's "2.8×" is a latency figure** from one serving benchmark
  (Llama-2-7B, A6000). The speed-up shrinks with sharding (1.38× at batch 1
  for Llama-2-70B on eight A100s). Its INT4 + 2:4 model scores above the FP16
  baseline only because it was further distilled on synthetic data. These
  are recorded on the note.
- **Most of SDXL's measured size-conditioning gain comes from keeping the
  data.** Keeping small images accounts for 4.1 FID-5k, and the conditioning
  for 3.2. The practice states it that way.

### Added

- **CycleGAN** (`#163`), [LIT-564](record/literature.d/LIT-564.md), read as [NOTE-302](record/notes.d/NOTE-302.md).
  **[SOTA-339](record/practices.d/SOTA-339.md), `Proposed`**: cycle consistency for unpaired appearance
  translation. It is scoped away from geometric change, where the authors
  report failure. The paper's own labels → photo ablation has a
  one-directional cycle beating the bidirectional one, and the practice says
  so.
- **Projected GAN** (`#163`), [LIT-562](record/literature.d/LIT-562.md), read as [NOTE-303](record/notes.d/NOTE-303.md).
  **[SOTA-338](record/practices.d/SOTA-338.md), `Proposed`, `contested`**: discriminate on frozen
  multi-scale pretrained features with fixed random mixing. It reaches
  StyleGAN2's best Church FID after 1.1M images instead of 88M. The speed-up
  is measured in FID, and the contest is over whether it is quality.
- **The Role of ImageNet Classes in FID**, [LIT-563](record/literature.d/LIT-563.md), read as
  [NOTE-304](record/notes.d/NOTE-304.md). It is the `contested_by` of [SOTA-338](record/practices.d/SOTA-338.md). With a fixed
  generator, resampling to match ImageNet-class statistics cuts FFHQ FID
  5.30 → 1.78 while CLIP-space FD moves 2.76 → 2.64. At equal FID, Projected
  FastGAN loses to StyleGAN2 in CLIP space and with human raters.
  **[SOTA-337](record/practices.d/SOTA-337.md), `Active`**: when ImageNet-pretrained networks take part
  in training, confirm FID gains in a non-ImageNet feature space.

### Documentation

- **Found while filing Projected GAN, not listed on `#163`.** The FID
  paper was pulled in because a practice cannot be filed honestly without
  the measurement that contests it. It complements [SOTA-307](record/practices.d/SOTA-307.md) (FID variance)
  with a practice about FID bias.

### Added

- **StyleGAN, StyleGAN2, StyleGAN3** (`#163`), [LIT-561](record/literature.d/LIT-561.md), [LIT-560](record/literature.d/LIT-560.md)
  and [LIT-559](record/literature.d/LIT-559.md), an `extends` chain. StyleGAN2 was read ([NOTE-301](record/notes.d/NOTE-301.md)),
  StyleGAN3 read (§1–3.2, [NOTE-300](record/notes.d/NOTE-300.md)), StyleGAN skimmed with no NOTE.
- **[SOTA-336](record/practices.d/SOTA-336.md), `Proposed`: no progressive growing** (`#163`'s
  "progressive training"). A fixed output-skip generator and residual
  discriminator keep the coarse-to-fine emphasis without phase artifacts.
  FFHQ FID 4.34 → 3.31. The best pair is dataset-dependent.
- **[SOTA-334](record/practices.d/SOTA-334.md), `Proposed`: weight demodulation instead of instance
  normalization** in style-modulated generators. It removes the droplet
  artifact at unchanged FID.
- **[SOTA-335](record/practices.d/SOTA-335.md), `Proposed`: alias-free generators when content must
  move** (`#163`'s "equivariant representation"). Filtered nonlinearities,
  Fourier input and no noise give EQ-T 63 dB and EQ-R 40 dB at StyleGAN2's
  FID.

### Documentation

- **[SOTA-336](record/practices.d/SOTA-336.md) records StyleGAN3's partial reversal.** StyleGAN3 keeps
  the fixed topology but drops StyleGAN2's output skips, attributing their
  benefit to gradient-magnitude dynamics. The practice's claim is *no
  growing*, not the particular skip wiring.
- **Lazy regularization and path-length regularization are not filed.**
  The first rests on one configuration with one regularizer. The second
  trades FID for a smoothness metric the same group introduced, and worsens
  FID on LSUN Car.

### Added

- **Tensor Programs I, II and III** (`#163`), [LIT-558](record/literature.d/LIT-558.md), [LIT-557](record/literature.d/LIT-557.md) and
  [LIT-556](record/literature.d/LIT-556.md). They complete the series under TP-IV ([LIT-548](record/literature.d/LIT-548.md)) and TP-V
  ([LIT-148](record/literature.d/LIT-148.md)) as an `extends` chain TP-I → TP-II → TP-III → TP-IV. TP-II also
  `extends` the NTK paper ([LIT-360](record/literature.d/LIT-360.md)). These are theory machinery with no
  practice: GP behaviour at initialization for every standard architecture
  (I), the NTK limit for every architecture (II), and free independence of
  weights and activations, which justifies the dynamical-isometry Jacobian
  calculations (III).

### Changed

- **[LIT-360](record/literature.d/LIT-360.md) (NTK) to v2, now also tagged `training-optimization`.** The
  paper is about the dynamics of gradient-descent training. Attaching the
  Tensor Programs chain had left the µP lineage with no topic common to all
  twelve members, and this was the true topic that was missing, not a label
  added to pass the check. The three new Tensor Programs notes carry it
  for the same reason: they are the width-scaling theory whose payoff is µP.

### Documentation

- **Skimmed, and marked so.** Each note says it was filed from the abstract,
  introduction and contribution statements, with no NOTE and the proofs not
  checked. None of them sources anything, so none needs more.

### Added

- **Cold Diffusion** (`#163`, "[theory] cold diffusion"), [LIT-553](record/literature.d/LIT-553.md),
  read as [NOTE-299](record/notes.d/NOTE-299.md). Its account is filed as **[THEORY-079](record/theory.d/THEORY-079.md),
  `Rejected` at filing**: "diffusion does not depend on the noise" is
  contradicted by its own Table 5 (noiseless blur generation FID 97.00 on
  CelebA against 23.11 with noise, halved by σ = 0.002 of added noise).
  What survives is the sampler, exact for degradations linear in severity.
- **Warm Diffusion** (`#163`, "[theory] warm diffusion"), [LIT-555](record/literature.d/LIT-555.md),
  read as [NOTE-297](record/notes.d/NOTE-297.md). It `extends` Cold Diffusion and is
  `compared_against` EDM ([LIT-075](record/literature.d/LIT-075.md)). **[THEORY-080](record/theory.d/THEORY-080.md), `Proposed`,
  `corrects` [THEORY-079](record/theory.d/THEORY-079.md)**: noise keeps intermediate states on the data
  manifold, and blur helps only once noise dominates the bands it removes.
  The blur-to-noise sweep fits (FID 1.85 at 0.5 to 11.97 at 10). The
  manifold departure is not measured, and `promote_when` asks for that.
- **Diffusion Forcing** (`#163`), [LIT-554](record/literature.d/LIT-554.md), read as [NOTE-298](record/notes.d/NOTE-298.md).
  **[SOTA-333](record/practices.d/SOTA-333.md), `Proposed`**: train continuous-token sequence models with
  per-token noise and condition rollouts on slightly noised history. The
  long-rollout stability it is known for is qualitative in the source.

### Documentation

- **Warm Diffusion's Table 1 misattributes a Cold Diffusion number.** It
  lists 80.08 FID for Cold Diffusion's unconditional CIFAR-10 generation,
  but that is Cold Diffusion's CIFAR-10 *deblurring* FID. Cold Diffusion
  reports unconditional generation only on CelebA and AFHQ. Recorded on the
  Warm Diffusion note.
- **No practice filed for Warm Diffusion.** Its gain over EDM is 0.12 FID,
  reported as the best of three sampling rounds.

### Added

- **Fourier features** (`#163`, "[theory] fourier features"), [LIT-550](record/literature.d/LIT-550.md),
  read as [NOTE-296](record/notes.d/NOTE-296.md). It `extends` NeRF ([LIT-435](record/literature.d/LIT-435.md)), whose positional
  encoding it explains and generalizes.
- **[THEORY-077](record/theory.d/THEORY-077.md), `Active`: why coordinate MLPs need a sinusoidal input
  encoding.** Their NTK spectrum falls off fast with frequency, so detail is
  learned too slowly to matter. Sinusoids of the input make the composed
  kernel stationary, with a bandwidth the frequencies set. The NTK linear
  model's loss predictions matched trained 4×1024 networks. It is scoped as
  a lazy-regime account of an input encoding, with [THEORY-076](record/theory.d/THEORY-076.md) cited for why
  that is not an account of feature learning.
- **[SOTA-331](record/practices.d/SOTA-331.md), `Active`, `converged`: encode low-dimensional coordinates
  with sampled sinusoids and tune only the frequency scale.** Gaussian
  features beat no mapping and NeRF-style positional encoding on all seven
  tasks. Four sampling distributions fall on one error curve against scale.
- **SIREN** (`#163`), [LIT-551](record/literature.d/LIT-551.md), read as [NOTE-295](record/notes.d/NOTE-295.md). It is
  `compared_against` NeRF ([LIT-435](record/literature.d/LIT-435.md)), whose positional encoding is its
  baseline. Image-GS ([LIT-511](record/literature.d/LIT-511.md)) now declares the same-size comparison it ran
  against SIREN and Fourier features.
- **[THEORY-078](record/theory.d/THEORY-078.md), `Proposed`: the answer to `#163`'s question of why
  periodic activations struggled.** Initialization that keeps
  pre-activations near N(0,1) makes each sine layer arcsine-distributed
  with slow frequency growth. That is verified at initialization for 6 and
  50 layers. That earlier periodic networks failed for lack of it is not
  tested, since the paper has no training ablation over initializations,
  and `promote_when` asks for exactly that.
- **[SOTA-332](record/practices.d/SOTA-332.md), `Proposed`: use SIREN when the representation is
  supervised through its derivatives.** It is scoped away from value
  fitting, where [SOTA-205](record/practices.d/SOTA-205.md) and Image-GS's benchmark point elsewhere, and it
  records that SIREN was never compared with Fourier features.
- **XGrammar** (`#163`, "sampling structured outputs"), [LIT-552](record/literature.d/LIT-552.md), read
  as [NOTE-294](record/notes.d/NOTE-294.md). It is the record's first document on constrained
  decoding.
- **[SOTA-330](record/practices.d/SOTA-330.md), `Active`, `emerging`: enforce structure with a grammar
  mask whose per-node verdicts are precomputed and built on the CPU during
  the forward pass.** Each optimization is ablated (65.8 → 0.018 ms per
  token) and end-to-end overhead is 0.1–0.2 ms per token. The paper's
  "accuracy" gains (62% → 100%) are syntactic validity, guaranteed by
  construction. The practice says that task correctness under the
  constraint is not measured.

### Documentation

- **YaRN's "RoPE is close to a Fourier feature" is recorded as analogy, not
  evidence.** The theory is not listed as explaining [SOTA-151](record/practices.d/SOTA-151.md) or [SOTA-179](record/practices.d/SOTA-179.md).
  The paper is about MLPs on 1–3-dimensional coordinates.

### Added

- **Tensor Programs IV** (`#163`), [LIT-548](record/literature.d/LIT-548.md), read end to end as
  [NOTE-292](record/notes.d/NOTE-292.md). This is the paper where µP is introduced. [SOTA-143](record/practices.d/SOTA-143.md) tells
  the reader to parametrize with µP and was sourced only to TP-V ([LIT-148](record/literature.d/LIT-148.md)),
  the transfer paper that builds on it.
- **[THEORY-076](record/theory.d/THEORY-076.md), `Active`: why the standard parametrization's learning
  rate has to move with width.** A rate large enough to move the features
  blows up the logits, and one small enough to be stable (`O(1/width)`)
  leaves the wide network a kernel machine. µP is the parametrization where
  a width-independent rate is stable and every layer updates maximally.
  `explains` [SOTA-143](record/practices.d/SOTA-143.md), which until now had one explanation, [THEORY-024](record/theory.d/THEORY-024.md)'s
  duality account, and that is `Proposed`.
- **Lineage:** [LIT-148](record/literature.d/LIT-148.md) (TP-V) and [LIT-437](record/literature.d/LIT-437.md) (spectral condition) now
  `extends` the TP-IV note, and [THEORY-037](record/theory.d/THEORY-037.md) (depth scaling) `extends` the new
  theory. [THEORY-037](record/theory.d/THEORY-037.md) already relied on the maximal-update principle, which is
  Definition 5.2 of this paper.

- **Gemma 3n** (`#163`), [LIT-545](record/literature.d/LIT-545.md), read as [NOTE-293](record/notes.d/NOTE-293.md) from the
  model overview, the developer guide and the `transformers` implementation.
  There is no paper. This is the origin of Per-Layer Embeddings: a
  token-keyed table holding one 256-d vector per layer, about 2.35B
  parameters in E2B, kept off the accelerator. [LIT-152](record/literature.d/LIT-152.md) cites it and the
  record could not follow the reference. Filed as adoption, not evidence,
  because Google published no ablation.
- **[SOTA-326](record/practices.d/SOTA-326.md), `Proposed`, `unreplicated`: add n-gram embedding memory
  as one table read early, on top of the expert budget rather than in place
  of experts.** Sourced to [LIT-152](record/literature.d/LIT-152.md)'s §2.3 ablations. One table at layer 2
  lifts the benchmark average from 45.44 to 47.94. A second layer buys
  nothing, and no depth clearly wins: placement is worth under a point, and
  layer 2 is chosen so the prefetch overlaps layer 1. Funding the table with
  experts moves no downstream benchmark. Growing it lowers loss after MMLU
  has flattened and while GSM8K falls.
- **MatFormer** (`#163`), [LIT-546](record/literature.d/LIT-546.md), read as [NOTE-289](record/notes.d/NOTE-289.md): nested FFN
  widths trained one per step, with per-layer width selection at inference.
  The Gemma 3n note now `extends` it, which is the architecture Gemma 3n
  ships.
- **[SOTA-328](record/practices.d/SOTA-328.md), `Proposed`, `unreplicated`: train one nested model
  instead of a family of separately trained sizes.** At the compute of
  training four sizes separately (78M–850M), the largest granularity
  *matches* its baseline, and the smaller ones beat theirs because shared
  weights see up to 4× the tokens. The practice says it pays only if you
  were going to train the family. The paper's "extremely similar" scaling
  fits (`b` −0.13 vs −0.10, `c` 1.33 vs 0.89) are recorded as they are.
- **Matryoshka Representation Learning** (`#163`), [LIT-547](record/literature.d/LIT-547.md), read as
  [NOTE-291](record/notes.d/NOTE-291.md). MatFormer's note now `extends` it.
- **[SOTA-327](record/practices.d/SOTA-327.md), `Proposed`, `emerging`: train retrieval embeddings with
  nested losses, then shortlist on a prefix and re-rank on the full
  vector.** Each prefix matches a separately trained model of that width on
  ResNet50 and ImageNet, and a 16-d shortlist with a 2048-d re-rank is 14×
  faster at equal mAP@10. `Proposed` because the only measurement is the
  authors' own and it is image retrieval. The text-embedding adoption that
  makes it `emerging` is not evidence. The full-width cost (0.15–0.25 top-1
  at web scale) and the random-feature web-scale baseline are recorded.
- **ReFT** (`#163`), [LIT-549](record/literature.d/LIT-549.md), read as [NOTE-290](record/notes.d/NOTE-290.md). The note is
  `compared_against` LoRA ([LIT-046](record/literature.d/LIT-046.md)).
- **[SOTA-329](record/practices.d/SOTA-329.md), `Proposed`, `unreplicated`: for short-output tasks,
  adapt with a low-rank residual-stream intervention instead of a weight
  adapter, and not for long chain of thought.** It uses 0.03% of
  parameters against LoRA's 0.8%. It leads on commonsense QA, is level on
  GLUE, and trails LoRA on arithmetic chain of thought (GSM8K 26.0 against
  37.5 at 7B). Every baseline number is copied from other papers, and the
  practice says so. `compared_against` [SOTA-184](record/practices.d/SOTA-184.md), which stays the default.

### Fixed

- **The 2026-09-19 claim that the "add TP-IV for muP" item was already
  satisfied.** That entry and its fragment said [LIT-148](record/literature.d/LIT-148.md) "*is* the µP paper".
  It is not. TP-V is µTransfer, and µP, with the theorem saying why SP
  fails at width, is TP-IV. The old entries stay as written, and this is the
  correction.

### Changed

- **Consensus prose goes in `consensus_note:`**, which is where 180 of the
  192 practices with a `consensus:` value keep it. The three practices
  filed earlier in this contribution had it in a body section, and it was
  moved before merge.

- **[LIT-152](record/literature.d/LIT-152.md) to v2.** Adds the n-gram embedding ablations, which v1 reduced to
  one clause, and says the note now sources [SOTA-326](record/practices.d/SOTA-326.md).

### Documentation

- **What the theory claims is limited to what the theorem covers.** It
  covers the *maximum stable* learning rate for SGD on MLPs. That the
  *optimum* transfers, and that it does so under Adam, is TP-V's empirical
  claim, and the theory's "What this does not say" section keeps the two
  apart.
- **`#163` re-measured before starting.** GPTQ ([LIT-081](record/literature.d/LIT-081.md)), SiT ([LIT-447](record/literature.d/LIT-447.md)) and
  SD 1.x ([LIT-062](record/literature.d/LIT-062.md), the latent diffusion paper) were already in the record and
  are now ticked in the issue.
- **`#163`'s premise for the Gemma 3n item was too strong.** The issue calls
  PLE the source of Qwen3.8-Flash-Next's n-gram embedding. The report cites
  Gemma 3n among six sources for *unigram* lookup memory and for host-memory
  offloading, and cites N-Grammer, the Over-Tokenized Transformer and Cheng
  et al.'s conditional-memory lookup for the n-gram form. None of those three
  is in the record. PLE also has a different shape: a small table at every
  layer, not one large table at one layer.

### Fixed

- **A false claim about concretization, written into `luria.yaml` yesterday and
  corrected today.** `ADR-055`'s config comment said a temporary code written
  into `luria.yaml` "would go stale with no mechanism to fix it", citing
  `ADR-039`. It is not true. `luria concretize` rewrites every occurrence of a
  renamed code in every file matching `code.globs`, and `ADR-039` put
  `luria.yaml` in that list.
- **`ADR-039` to v3.** The decision stands and bought more than it claimed:
  adding the glob turned on the lint **and** made concretization repair the
  config. The Context — "nothing was rewriting the config" — is accurate
  history of the state *before* the decision; the Consequences never recorded
  that the decision ended it, which is how a later reader took the Context for
  the current state.

### Documentation

- **Measured rather than argued.** A scratch decision was minted on a throwaway
  branch, its temporary code written into `luria.yaml` both bare and inside
  backticks and into a changelog fragment bare, backticked and lower-cased, and
  `luria concretize` was run. Every one of the six came back as the numbered
  code. The probe was then discarded.
- **The backtick theory is half wrong, and the record has been repeating it
  since 2026-09-21.** Concretization *does* reach inside backticks —
  `_rewrite_files` is a plain string replace over whole file contents. What
  cannot is `luria link --fix`, which upgrades a **bare** already-concretized
  code and leaves two shapes untouched: the same code inside backticks, and a
  hand-written markdown link whose text and target are both the old spelling.
  Also measured.
- **So the citations hand-fixed on 21 and 22 September were a different defect
  from the one the record named.** They were codes another branch had already
  concretized, so there was no pending rename for `luria concretize` to apply
  — `#211`, which is open and which this contribution now carries evidence
  for. The backtick blind spot is real but belongs to `link --fix` alone, and
  it is why those citations survived the second pass.
- **A third gap, new here: `luria link --fix` does not repair a hand-written
  link whose target is an old spelling.** A markdown link whose text and target
  are both a code that has since been concretized is reported by the lint and
  left alone by the fixer. That is the shape the
  `LIT-489` fragment's advice — "backticking a code keeps it out of the
  relative-link warning class and also keeps it out of the fixer's reach" —
  half-anticipated without measuring.
- **The prompt for all of this was a challenge, not a check.** Nothing in the
  lint would have caught a wrong sentence in a config comment. It was caught by
  being asked whether the claim was still true, and the honest answer required
  reading `luria/concretize.py` and running the probe rather than re-reading
  `ADR-039`.

### Changed

- **`schemes.SOTA.references.source` declares `invariant: tags`.** A practice
  and every paper behind it must now share at least one topic. Recorded as
  `ADR-055`, closing `#202`.
- **49 documents retagged.** 21 literature notes and 28 practices gained one
  topic each; one practice was retagged outright.

### Documentation

- **The pass came first and the declaration second, which is the whole
  decision.** `#202` named the reason: there is no acknowledgement directive
  for an unbound row — `inactive-ok:` covers citations, `target-ok:` link
  targets, `unresolved-ok:` codes, and nothing covers "deliberately unbound".
  Declaring over a standing backlog would have made
  `docs/reports/unbound-lineage.md` read 60 with no way to retire a row that
  had been looked at, and that report's all-clear is most of its value.
- **60 rows, reproduced fresh.** The issue counted 59 two days ago; the record
  has grown. 44 sat on `Active` practices and 51 had both sides in force.
- **The distribution was not what the issue expected**, and that is the
  finding. **57 of 60 were under-tagging** — a topic that was true and
  missing. *Attention Is All You Need* did not carry `attention-techniques`.
  FlashAttention did not carry `systems-optimization`. CheckFreq did not carry
  `distributed-optimization`, whose own blurb names checkpointing. Twelve
  diffusion practices did not carry `generative-modeling`. **One** was a
  mis-tagged practice: `SOTA-033`, continued pre-training, was
  `model-architecture` and is `adaptation-and-tuning`. **None** was the RETRO
  class the issue flagged as the one worth the pass — `#201` had already
  closed it. **None** needed a word the vocabulary does not have.
- **Tags were appended, never reordered.** `primary_topic` derives `{tags[0]}`,
  so a prepend silently refiles a document. Verified mechanically across all 49
  changed files: exactly one primary topic moved, and it moved on purpose.
- **Each row was judged against `CLAUDE.md`'s test** — would someone browsing
  that topic be right to expect this document? — and not against whether the
  row went away. One topic per row, each with a stated reason, so the batch is
  auditable.
- **The weakest row is named in the decision rather than buried.** `SOTA-060`
  (layer-norm init variance 0.02) sources `LIT-043` (Megatron-LM 3D
  parallelism), and `model-stability` was added to a parallelism paper. It is
  also a symptom: `LIT-043`'s entire note is the sentence "3D parallel training
  strategy", and a note that thin cannot say what it is about. That row is as
  much a reading backlog as a tagging one.

### Fixed

- **Two invented references, caught before they shipped.** The config comment
  first read "Declared by `ADR-055`" — a decision number that does not exist —
  and cited `LU-#288` for the missing `unbound-ok:` directive, an upstream
  issue number with no basis. Both removed. The config now cites `#202`, which
  is stable, and `ADR-039` is why: concretization rewrites the record and not
  this file, so a temporary code written into `luria.yaml` would go stale with
  no mechanism to fix it.

### Added

- **`LIT-541`** — *Deep Learning is Singular, and That's Good* (Murfet,
  Wei, Gong, Li, Gell-Redman and Quella, 2020), read as `NOTE-286`.
- **`LIT-542`** — *The Local Learning Coefficient: A Singularity-Aware
  Complexity Measure* (Lau, Furman, Wang, Murfet and Wei, 2023), read as
  `NOTE-285`.
- **`LIT-543`** — *Loss Landscape Degeneracy and Stagewise Development in
  Transformers* (Hoogland, Wang, Farrugia-Roberts, Carroll, Wei and Murfet,
  2024; TMLR 2025), read as `NOTE-287`.
- **`LIT-544`** — *Dynamical versus Bayesian Phase Transitions in a Toy
  Model of Superposition* (Chen, Lau, Mendel, Wei and Murfet, 2023), read as
  `NOTE-288`.
- **`THEORY-075`** — neural networks are singular, so effective complexity
  is a volume-scaling exponent and not a curvature. `Active`.
- **`THEORY-073`** — training passes through stages marked by changes in
  loss-landscape degeneracy. `Proposed`.
- **`THEORY-074`** — a Bayesian phase transition and a training-trajectory
  transition are different events, and only the first is well defined.
  `Proposed`.
- **`SOTA-325`** — when the training loss has saturated and runs still
  differ, measure loss-landscape degeneracy rather than curvature. `Proposed`.

### Changed

- **`SOTA-012` to v3**, a condition rather than a correction. The correlation
  between sharpness and test error stands and the advice stands. What is added
  is that filter normalisation answers the *rescaling* objection and not a
  deeper one: in a singular model the theorems contain the **exponent** of the
  volume law and curvature is its prefactor, appearing in neither the
  model-selection criterion `n L_n(w_0) + λ log n` nor the Bayes generalisation
  rate `λ/n`.
- **Two citations that pointed at nothing now resolve.** `LIT-476` compared its
  own local-volume power law against "Local Learning Coefficient results where
  `d/2` is a strict upper bound not seen in practice", and `NOTE-225` named the
  LLC as "the singular-learning-theory neighbour". Both now name
  `LIT-542`.

### Documentation

- **The record was citing this school's findings and holding none of its
  papers.** Zero hits for Watanabe, RLCT, WBIC or algebraic geometry; three
  mentions of singular learning theory, all pointing outward.
- **The vocabulary question was already settled and did not need reopening.**
  The curation entry of 21 September ran `ADR-050`'s test on "the physics of
  learning" — 28 documents mentioning mean-field analysis, free energy, singular
  learning theory, random matrix theory and phase transitions — and found 61%
  already primary-tagged `analysis-and-evaluation`. That is the test returning
  "no gap". These four documents take the same primary topic and no new tag was
  proposed.
- **What the trunk actually claims.** A model is regular iff the
  parameter-to-function map is one-to-one **and** the Fisher information is
  positive definite. Networks are neither, so the set of optima is a real
  analytic variety, the loss is not locally quadratic, and BIC's `d/2 log n` —
  which comes from the Laplace approximation — does not apply. The replacement
  is `λ`, the exponent in `V(ε) ∝ ε^λ`: the model-selection criterion becomes
  `n L_n(w_0) + λ log n`, and the Bayes generalisation error is `λ/n` against
  `C/n` for MAP and MLE, with `C = λ = d/2` only in the regular case.
- **`2λ` need not be an integer**, and in the minimally singular case `λ = d′/2`
  where `d − d′` directions leave the function unchanged. The curvature
  constants do not enter.
- **The instrument, and why it is believable.**
  `λ̂(w*) = n β* [E_{w|w*,β*,γ} L_n(w) − L_n(w*)]` at `β* = 1/log n`, by SGLD.
  It reproduces Aoyagi (2024)'s theoretical learning coefficients on deep linear
  networks **up to 100M parameters**, including at an SGD-found minimum, and is
  proved invariant to local diffeomorphism.
- **The result that made it a practice rather than a finding.** ResNet18 on
  CIFAR10: stronger implicit regularization — higher learning rate, lower batch
  size, higher momentum — gives lower `λ̂` and higher test accuracy, **while
  every training loss has collapsed to zero**. `Proposed`, because the sweeps
  are one-dimensional and by the measure's own authors.
- **A rival to `LIT-085`, named by its authors as one.** `SOTA-200` records
  that `LIT-085`'s progress measures are computed by projecting onto five
  frequencies the network was reverse-engineered to be using. Degeneracy is
  described by `LIT-543` as a "setting-agnostic, unsupervised alternative"
  that detects change without a mechanistic hypothesis in advance — and returns
  a boundary rather than a mechanism, which is less.
- **The stage findings, and the one that reaches today's other unit.** The
  language model's five stages land on bigrams, n-grams, previous-token heads
  and the induction circuit. The in-context regression transformer acquires
  in-context learning in LR2 and then **loses it** across LR3 and LR4 while
  specializing to its pre-training distribution — with the loss falling
  throughout. Every paper in `THEORY-067`'s cluster measures a trained
  model at an unstated point in that trajectory.
- **The distinction the record most needed.** Every grokking mechanism it
  holds — `THEORY-072`, `THEORY-071`, `THEORY-070` — is a claim
  about a trajectory indexed by step. Everything singular learning theory proves
  is about a posterior indexed by sample size. `LIT-544` says out loud that
  "there is no necessary relation between these two kinds of transitions", and
  demonstrates it: its `5 → 6` Bayesian transition is predicted at `n_cr ≈ 600`,
  observed at `600 ≤ n ≤ 700`, and **has not been observed as a dynamical
  transition at all**. The bridge — the Bayesian Antecedent Hypothesis — is
  labelled a conjecture by its authors and has two inconclusive cases in its own
  model.
- **`ARXIV-2310.03789` read and not filed.** Rubin, Seroussi and Ringel treat
  grokking as a first-order phase transition via the adaptive-kernel approach.
  It is a genuine result and it belongs to statistical mechanics rather than
  singular learning theory — a different framework answering a related
  question. Filing it here would have made one unit carry two theoretical
  machineries. It is named as its own unit, and its observation that grokking
  occurs as a function of sample size as well as time would be a fourth
  independent arrival at `THEORY-069`'s regime claim.
- **No `compared_against` between `SOTA-325` and `SOTA-012`.** `ADR-011`:
  that relation means somebody ran the comparison. Nobody has run
  filter-normalised sharpness against the local learning coefficient as
  predictors of test error on the same models. The argument that the exponent
  is the right quantity is theoretical, and both documents say so.

### Fixed

- **`ADR-054` to v2: the decision stands and one of its reasons was
  wrong.** v1, written an hour earlier, said `luria repair` is a superset of
  `luria link --fix` and removed `link --fix` from the documented sequence. It
  is not a superset. `link --fix` writes the converse of a declared relation
  and `repair` does not. **This unit is what caught it**: two `extends`
  relations were declared, `repair` reported nothing to do, the lint reported
  "2 declared relation(s) are held by one side only", and `luria link --fix`
  then wrote both. `CLAUDE.md`, the `Makefile` and the decision body are
  corrected; the sequence is `new` → `repair` → `link --fix` → `index` →
  `lint`.
- **And the other defect the same ADR named as upstream work arrived on
  schedule.** This contribution's prose cited five temporary codes minted by
  the two units merged earlier today — `THEORY-067`, `THEORY-069`,
  `THEORY-070`, `THEORY-071`, `THEORY-072` by their old spellings. The lint
  reported all sixteen sites with the mapping; because every one was inside
  backticks, neither concretization nor the fixer could reach them and they
  were rewritten by hand. A first attempt applied the mapping across all of
  `record/` and silently overwrote the `formerly:` field of the five
  concretized documents, destroying exactly the provenance those fields exist
  to hold; caught by reading the diff, and reverted. The lesson is narrow and
  worth keeping: a code rewrite must skip the document the code now names.
- **`make views-reset` now unstages before restoring.** The `pre-commit` hook
  made its first real catch on this contribution — views staged by a careless
  `git add -A` — and that exposed the gap: at the moment the hook fires the
  unwanted copies are *in the index*, so `git checkout -- docs/` restores them
  from exactly the wrong place. A `git reset -q HEAD -- docs/` goes first. The
  guard found a bug in its own remedy, which is the best argument for it.
- **And the hook needed an exemption for merges.** Merging `main` into a branch
  necessarily brings main's regenerated views with it; refusing that is not
  enforcing `ADR-018`, it is making the branch unmergeable. The hook now exits
  early when `MERGE_HEAD` exists — incorporation is not authorship. Found when
  a conflict resolution against `main` could not be committed.

### Added

- **`ADR-054`** — the four commands are five, and two of them are
  invariants a hook can hold. `Proposed`.
- **A `Makefile`.** `make ready` runs `luria repair`, `luria index` and
  `luria lint` and then discards the regenerated views — the whole pre-commit
  sequence in one target. `make hooks` installs the hook directory;
  `make views-reset` is the discard on its own.
- **`.githooks/pre-commit`.** Refuses staged paths under `docs/` on any branch
  but `main`, naming the offending files and the two ways past it. Tracked, so
  it is reviewable; installed by `make hooks` via `core.hooksPath`, since a
  file in `.git/hooks/` is neither.

### Changed

- **`CLAUDE.md`'s working sequence names `luria repair`, not
  `luria link --fix`.** `repair` is a superset: it links bare references *and*
  populates a journal entry's `created:` from the path `luria new` chose,
  retires a stale configuration reference, and moves a note out of `status:`.

### Documentation

- **Four filing units in one day ran `link --fix` and none ran `repair`,
  because the map said there were four commands.** `CLAUDE.md` describes
  itself as "a map, not a copy" and says that when it disagrees with
  `luria --help`, this file is wrong. That rule is right and it did not help:
  nobody reads `luria repair --help` for a command they do not know exists.
- **The cost was a violation fixed by hand.**
  `record/curation.d/2026/09/22/031952.md` carried a `created:` timestamp
  written from the changelog fragment's clock rather than from its own path,
  and the lint reported the disagreement. `luria repair` populates that field
  from the path. It was in the toolbox the whole time.
- **`ADR-018` was held by a sentence, and sentences are what failed that
  day.** The discard step held four times out of four — and the same session
  shipped a stale acknowledgement directive, a citation to another
  contribution's temporary code, and a directive naming a code that does not
  exist, each governed by a sentence somebody was supposed to remember. The
  hook checks the **branch**, not the content, because `main` has to be able to
  commit views: that is where CI commits them.
- **Three more defects from that session cannot be fixed here**, and the
  decision names them as upstream work rather than leaving them implied: a
  lint baseline, so seven standing warnings and 184 standing link targets stop
  living in a contributor's memory; an `ack` command writing acknowledgement
  directives from `docs/reports/reference-status.md` instead of from recall,
  which structurally cannot name a code that does not exist; and a branch-side
  check for citations to temporary codes a contribution does not itself mint.

### Added

- **`LIT-538`** — *Grokking: Generalization Beyond Overfitting on Small
  Algorithmic Datasets* (Power, Burda, Edwards, Babuschkin and Misra, 2022),
  read as `NOTE-281`.
- **`LIT-540`** — *Omnigrok: Grokking Beyond Algorithmic Data* (Liu,
  Michaud and Tegmark, 2022; ICLR 2023), read as `NOTE-282`.
- **`LIT-539`** — *Explaining grokking through circuit efficiency*
  (Varma, Shah, Kenton, Kramár and Kumar, 2023), read as `NOTE-283`.
- **`LIT-537`** — *Grokking as the Transition from Lazy to Rich Training
  Dynamics* (Kumar, Bordelon, Gershman and Pehlevan, 2023; ICLR 2024), read as
  `NOTE-284`.
- **`THEORY-069`** — grokking is a regime rather than a property of
  algorithmic data, and at least three knobs move it. `Active`.
- **`THEORY-072`** — the LU mechanism: training and test loss disagree as
  functions of weight norm. `Proposed`.
- **`THEORY-071`** — circuit efficiency and the critical dataset size.
  `Proposed`.
- **`THEORY-070`** — grokking is the transition from lazy to rich
  dynamics. `Proposed`, `corrects` the other two.

### Changed

- **`SOTA-200` to v3.** Its third check — *is the discontinuity a property of
  the regime?* — said grokking is "a data-starved-regime phenomenon, not a
  fundamental one", on `LIT-085`'s 60% figure alone. The check now says **move
  the regime and see whether the discontinuity moves with it**, names three
  axes rather than one, and points at ungrokking as the sharpest instance.
  Sources and `explained_by` extended; a Conditions paragraph added about how
  narrow the grokking evidence is.

### Documentation

- **The record had one grokking paper and a practice resting on it.**
  `LIT-085` (Nanda et al.) was the whole line — filed, `Rejected`, then
  promoted to `Active` on 2026-09-10 precisely because `SOTA-200` needed it —
  and the paper that named the phenomenon was absent, along with every
  mechanistic account. The same shape as the last four units, and sharper here
  because the practice is `Active` and makes a claim.
- **The founding paper reported the regime dependence itself.** `LIT-538`
  measures that converged accuracy is flat across a range of training fractions
  while time-to-generalize explodes as the fraction falls — near 25–30% on
  `S₅`, removing 1% of the data raises median steps-to-generalize by 40–50%,
  while steps-to-fit stay at `10³`–`10⁴`. So `LIT-085` sharpened an existing
  measurement into a threshold; it did not arrive from outside and deflate the
  phenomenon, which is how `SOTA-200` read.
- **`DP-010` in one figure.** Figure 1's left panel — the thousand-fold gap on
  division mod 97 — is what travelled. The centre panel of the same figure is
  the data-fraction curve.
- **Data fraction is one axis of three.** `LIT-540` induces grokking on
  **MNIST** (1k examples, Kaiming weights scaled by `α > 1`), **IMDb** with an
  LSTM at `α = 6` and **QM9** with a GCNN at `α = 3` — and reports none at
  standard initialization in any of the three — then eliminates it on
  algorithmic data by constraining the weight norm. `LIT-537` adds initial
  neural-tangent-kernel alignment, measurable on any task as centered kernel
  alignment. That is `THEORY-069`, and it is `Active` because it is the
  one claim all four papers support.
- **Three mechanisms, none of them settled, filed separately.** The LU
  mismatch (`THEORY-072`), circuit efficiency (`THEORY-071`) and
  lazy-to-rich (`THEORY-070`). All `Proposed`. `Active` on this scheme
  means "the best explanation the record holds", and with a published
  counterexample to two of them and two unexplained phenomena against the
  third, no single account earns it.
- **The counterexample is why the unit is four papers rather than two.**
  `LIT-537` §3: modular arithmetic, two-layer MLP, **no weight decay**,
  parameter norm **rising** through the transition. Both weight-norm accounts
  explain grokking by a late decrease in norm, so neither can produce that run.
  `THEORY-070` declares `corrects` on both.
- **And the correction does not finish the job, which the record says rather
  than smoothing over.** `THEORY-071` derived **ungrokking** — a grokked
  network regressing to near-random test accuracy when trained below a critical
  dataset size, sharply, with an endpoint independent of weight decay — and
  **semi-grokking**, and then observed both. Nothing in the lazy-to-rich
  picture addresses either. A correction that cannot reproduce what it corrects
  has narrowed its predecessor rather than replaced it, and that is in
  `THEORY-070`'s `promote_when`.
- **The record's existing grokking paper turns out to be an antecedent.**
  `LIT-539` names `LIT-085`'s Appendix E as the explanation genre it makes
  precise and cites its Figures 1 and 7. So `LIT-085` was holding a position in
  a lineage whose trunk and whose descendant were both missing.

### Added

- **`LIT-534`** — *What Can Transformers Learn In-Context? A Case Study
  of Simple Function Classes* (Garg, Tsipras, Liang and Valiant, 2022;
  NeurIPS 2022), read as `NOTE-279`.
- **`LIT-533`** — *Transformers learn in-context by gradient descent*
  (von Oswald et al., 2022; ICML 2023), read as `NOTE-280`.
- **`LIT-532`** — *What learning algorithm is in-context learning?
  Investigations with linear models* (Akyürek, Schuurmans, Andreas, Ma and
  Zhou, 2022; ICLR 2023), read as `NOTE-277`.
- **`LIT-535`** — *Transformers Learn to Achieve Second-Order Convergence
  Rates for In-Context Linear Regression* (Fu, Chen, Jia and Sharan, 2023;
  NeurIPS 2024), read as `NOTE-278`.
- **`LIT-536`** — *Do pretrained Transformers Learn In-Context by Gradient
  Descent?* (Shen, Mishra and Khashabi, 2023; ICML 2024), read as
  `NOTE-276`.
- **`THEORY-067`** — a transformer can run a learning algorithm on a model
  held in its activations, and the architecture admits several, so a
  construction identifies none. `Active`.
- **`THEORY-068`** — in-context learning is gradient descent on an
  implicit model. `Rejected`, and kept.
- **`SOTA-323`** — test a claim about what pretraining produces on a model
  trained with the pretraining objective, not one trained on the task family
  you are testing. `Proposed`.
- **`SOTA-324`** — separate rival accounts of an internal algorithm by
  convergence rate and conditioning, not by how well each fits the output.
  `Proposed`.

### Documentation

- **The record said in-context learning emerges and adapts, and held nothing
  about what the forward pass does.** `SOTA-037` and `SOTA-038` come from
  Brown et al.; `THEORY-038` is a limit on what a decoder can compose in few
  layers; the chain-of-thought practices are downstream. None of the five
  papers this contribution files was here, and `ARXIV-2212.07677` sits at four
  distinct reading days on the refreshed `#180` worklist.
- **The cluster is a dispute, not a finding, and that is why all five are
  filed together.** Filing `ARXIV-2212.07677` alone would have put a claim in
  the record that two later papers contest and that its own §3 qualifies.
- **The word "gradient descent" is doing two jobs, and the two documents
  separate them.** `THEORY-067` keeps the frame: activations carry a
  model, layers carry updates to it. That has been made precise three times,
  for three different algorithms — one gradient step per linear-self-attention
  layer, a Sherman–Morrison ridge update in `O(d²)` width, and `k` Iterative
  Newton steps in `k + 8` layers. Its second clause is the consequence: the
  architecture expresses first-order, closed-form and second-order solvers
  alike, so no construction of this kind can identify the algorithm.
  `THEORY-068` is the identification, and it is `Rejected`.
- **Three refutations, at three depths, and the first is the source paper's
  own.** Beyond one layer, `LIT-533`'s trained models match GD++ —
  gradient descent on data transformed by `I − γXXᵀ`, with a learning rate and
  a `γ` fitted per layer — not gradient descent. `LIT-535` matches layers
  to steps and finds a linear correspondence with Iterative Newton (about 3
  iterations per middle layer) against an exponential one with GD, and at
  condition number 100 the transformer is unchanged while GD needs about 2,000
  steps a twelve-layer model cannot hold. `LIT-536`'s Theorem 1 needs no
  weights at all: an algorithm equivalent to in-context learning must share its
  order sensitivity, batch gradient descent has none, and on LLaMA-7B ICL is
  more order-sensitive than GD, SGD and Adam.
- **`ADR-031` doing the work it was added for.** The explanation is rejected
  and the phenomenon is untouched — transformers do solve regression from
  context, do improve monotonically with depth, and do reach the optimal
  estimator.
- **`LIT-536`'s Hypothesis 1 / Hypothesis 2 split is the transferable
  part**, and is filed as `SOTA-323` because it is not about in-context
  learning. "There exist weights such that" and "pretraining produces weights
  such that" are different claims; training a model on the task family you are
  about to test collapses them, and the second is the one a reader takes away.
  `Proposed`: the argument is clean and has been applied once.
- **`LIT-535`'s method is filed separately from its finding**, as
  `SOTA-324`. Output similarity cannot separate algorithms that converge
  to the same answer — the paper reports gradient descent fitting well at later
  layers while being the wrong description. A rate can, and so can a regime
  where the rivals must differ. Its `promote_when` asks for the measurement to
  be run on a model pretrained on a general objective, which is the experiment
  neither side of this dispute has done.
- **`DP-010` twice over.** `LIT-533`'s title is the most-quoted sentence
  in the cluster and its own §3 supplies the qualification the title omits;
  `LIT-532`'s title asks which algorithm and its strongest result —
  matching the minimum-Bayes-risk ridge predictor at every noise level — is a
  statement about *what* is computed rather than *how*, with the
  gradient-descent phase belonging to its shallowest models.
- **`DP-007`.** The identification became the standard answer without anybody
  having tested it on a model pretrained on natural data. Agreement had no
  author.
- **`ARXIV-2111.02080` was read for its abstract and deliberately not filed.**
  Xie et al.'s implicit-Bayesian-inference account answers a different question
  — why in-context learning emerges from pretraining, rather than what the
  forward pass computes — and belongs to a unit with its own descendants, not
  to this one.

### Added

- **`LIT-531`** — *Deep Learning and the Information Bottleneck
  Principle* (Tishby and Zaslavsky, 2015; ITW 2015), read as
  `NOTE-275`.

### Fixed

- **Three citations in a concretized code's old spelling**, in the curation
  entry that was itself about that trap. `luria link --fix` cannot reach
  inside backticks, so they were rewritten by hand — which is exactly what
  the `LIT-489` fragment recorded a day earlier, with the words "worth
  knowing before the next fragment".

### Documentation

- **[#180](https://github.com/dmarx/anthology-of-the-sota/issues/180)'s published worklist is exhausted, and the ranking has been
  recomputed.** Every one of the fourteen entries in the issue's top tier is
  now filed. Re-mining `dmarx/papers-feed`'s snapshot — 12,301 objects, 4,542
  interaction records, snapshot dated 2026-09-22 — gives **2,169**
  arXiv-resolvable papers with reading sessions, of which **299** have ≥2
  distinct reading days, **83** have ≥3 and **31** have ≥4. Against the 428
  arXiv ids the record holds, **33 are absent at ≥3 days**. That list is the
  refreshed worklist and is posted to the issue.
- **A correction to the method, worth recording because it changes the
  numbers.** A first pass matched only bare `NNNN.NNNNN` ids and found 139
  resolvable papers against the issue's reported 2,196. The snapshot's keys
  are mostly `arxiv.NNNN.NNNNN`, with `arxiv:` and bare forms alongside and
  `openreview.`, `nature.`, `pnas.` and `url.` prefixes for the rest. Matching
  the three arXiv shapes gives 2,169 — close to the issue's figure and
  reproducible.
- **The top of the refreshed list contained a gap this session created.**
  `ARXIV-1503.02406` — Tishby and Zaslavsky, the paper the whole
  information-bottleneck line descends from — was absent, while the record
  held `LIT-507`, `LIT-508` and `LIT-509` arguing about it, plus `THEORY-058`
  and `SOTA-312` filed from that argument.
- **Reading it reassigns part of the blame in that dispute.** `SOTA-312` says
  to state the noise or binning assumption behind any mutual information
  reported for a deterministic network, and `THEORY-058` exists because
  `I(h;X)` is infinite for a deterministic map. That objection is fatal to the
  2017 measurement — and it is not one the founding paper failed to
  anticipate. It says, in one sentence, that "getting closer to the optimal
  limit requires **stochastic mapping between the layers**". The condition was
  named at the start and dropped by the work that tried to observe the
  picture. The two-phase claim stays refuted; what moves is where the defect
  sits.
- **The famous figure is labelled a hypothesis by its own caption.** Figure 2
  is "a **qualitative** information plane, with a **hypothesized** path of the
  layers in a typical DNN". The green path later papers went looking for is
  drawn, not measured, and says so.
- **And two claims nobody has examined.** The paper also claims the optimal
  architecture — number of layers, features per layer — is set by the
  **bifurcation points** of the IB tradeoff, and that hierarchical
  representations are **structural phase transitions** on the information
  curve. Those are checkable architecture claims. The 2017 measurement, the
  2018 rebuttal and the 2019 counter-rebuttal all argue about compression and
  none of them touches either. `DP-004`: the dispute's query was shaped like
  the information plane, so the architecture claims were never in anyone's
  field of view — including this record's when it filed the dispute.
- **Neural collapse assessed and not filed.** The previous unit deferred it
  saying it "gets a unit or it gets nothing". Tested against the record: the
  only mentions of simplex or equiangular geometry are the two documents filed
  yesterday that name it as a resemblance, and nothing here touches
  terminal-phase training or class-mean geometry. It would be a trunk with no
  descendants, and "famous and adjacent" is the `DP-005` trap. Not filed, and
  the test is recorded so the next pass does not redo it.

### Added

- **`LIT-530`** — *Attention is not all you need: pure attention loses
  rank doubly exponentially with depth* (Dong, Cordonnier and Loukas, 2021;
  ICML 2021), read as `NOTE-274`.
- **`LIT-529`** — *Linformer: Self-Attention with Linear Complexity*
  (Wang, Li, Khabsa, Fang and Ma, 2020), read as `NOTE-273`.
- **`THEORY-066`** — pure self-attention collapses every token onto one,
  and skip connections prevent it by keeping short paths alive. `Proposed`.

### Documentation

- **Two trunks the record was leaning on without holding.** Four documents use
  "rank collapse" as an established premise and none held its source;
  `SOTA-184` and `SOTA-147` both rest on attention having usable low-rank
  structure and neither had a source for that either.
- **"Rank collapse" names two different phenomena in this record, and the
  conflation is the field's rather than ours.** Dong et al.'s rank collapse is
  *token representations converging to rank 1 through depth in one forward
  pass*, prevented by skip connections. `LIT-350` — in its own words, "as
  training progresses, weight matrices exhibit rank collapse, converging to
  low-rank subspaces" — means *weight matrices over training time*, which is
  what `LIT-516` measures too. Different objects, different axes, different
  remedies. `NOTE-105` reports its source faithfully and needs no correction;
  `NOTE-274` carries the table separating them.
- **The path decomposition is the machinery and it earns its own mention.** A
  depth-`L`, `H`-head network's output is a sum over paths, one head per
  layer. With skip connections the count of length-`l` paths becomes
  `C(L,l)·H^l`, so short paths dominate — and one path skips every layer. Read
  through it, a deep transformer looks like an **ensemble of shallow
  single-head networks**, because the long paths have had their residual
  destroyed and the short ones have not.
- **The rate is cubic, not linear, and the reason is a cascade.** An attention
  matrix formed from a low-rank input mixes tokens faster, so each layer's
  collapse accelerates the next. The authors' calibration: three orders of
  magnitude takes a linear rate about a dozen steps and a cubic rate two or
  three.
- **Layer normalization provably cannot help, in two lines.** `LN(SA(X))`
  rewrites as `Σ_h P_h X W̃_h + 1b̃ᵀ` with `W̃_h = W_h D_LN^{-1}`, so it is a
  right multiplication plus a rank-1 shift — and right multiplication cannot
  increase rank. The record holds a large normalization cluster and this is a
  clean statement of one thing normalization is not for.
- **A second, independent reason for skip connections.** `THEORY-011` holds
  they smooth the loss landscape — the account `SOTA-010` was superseded into.
  This holds they preserve rank, and the source says explicitly that this
  effect was "previously unknown … beyond facilitating optimization". Two
  mechanisms, one component, no relation declared because neither refines the
  other.
- **The record has held the rebuttal since this morning with nothing to
  rebut.** `LIT-521` names rank collapse of activations as the wrong locus,
  arguing the cause sits in the weight matrix. Both sides are now present and
  nobody has adjudicated them.
- **`Proposed`, and the reason is the source's own open problem.** What is
  proved about skip connections is that *some* parameterization preserves the
  residual, because one path skips every layer. What the paper is cited for is
  that skip connections prevent collapse in real transformers. The authors
  call their upper bound "vacuously large" and pose the tight lower bound as an
  open challenge; that challenge is the promotion condition.
- **Linformer is filed for its measurement, and the record's existing verdict
  on its method stands.** `NOTE-005` has FlashAttention undermining this
  literature's premise "by showing the cost model was wrong". That is about
  `O(n)` being the right target. The spectrum measurement — SVD of `P` across
  every layer and head of RoBERTa-base and RoBERTa-large, `n = 512`, 10k
  sentences, Wiki103 and IMDB, long-tailed everywhere and more skewed in higher
  layers — is untouched by it. `Active`, because the record retires a document
  when its claim stops holding, and this claim did not.
- **Theorem 1 is narrower than its own section heading.** "Self-attention is
  low rank" is the heading; what is proved is that for each column there exists
  a rank-`Θ(log n)` matrix approximating that column's image with high
  probability. The empirical spectrum is doing more work than the theorem.
- **The two papers read the same fact in opposite directions and neither
  notices.** Linformer measures `P` as low rank and calls it an opportunity;
  Dong et al. proves `P` driving representations to rank 1 is the pathology
  skip connections exist to prevent. The difference is whether you are
  compressing the matrix or passing information through it. Recorded, not
  joined.
- **And one trade nobody has framed as a trade.** MLPs counteract rank collapse
  in proportion to their Lipschitz constant, and the source states that larger
  Lipschitz constants make a model less robust and more sensitive to input
  perturbations. `THEORY-064` holds that transformers' robustness is made of
  their bias toward low-sensitivity functions. Three years apart, no citation
  in either direction, and neither paper says the two pull against each other.
- **Neural collapse deferred, with a reason.** `LIT-528` names it as a
  resemblance and the record holds nothing on it. It is a different subject —
  the geometry of the classification layer at the end of training — nothing
  filed here leans on it, and it deserves a unit rather than a paragraph at the
  end of this one.

### Added

- **`LIT-528`** — *The emergence of clusters in self-attention dynamics*
  (Geshkovski, Letrouit, Polyanskiy and Rigollet, 2023; NeurIPS 2023), read as
  `NOTE-272`.
- **`THEORY-065`** — self-attention drives tokens into a few clusters,
  and the spectrum of the value matrix decides the geometry they land in.
  `Proposed`.

### Fixed

- **A decline reversed.** The previous contribution declined this paper on the
  grounds that its `t → ∞` frozen-weights idealization put it too far from a
  trained model to be evidence about one, and that it underwrites no practice
  the record holds. Both halves were wrong, and the second was wrong against
  this project's own schema, which makes `explains` optional on a theory
  because "a finding that underwrites nothing YET is still a finding, and
  requiring this would mean filing it nowhere — which is the state this scheme
  exists to end."

### Documentation

- **The classification is the contribution, and it is indexed by the value
  matrix.** `V = I_d` sends tokens to the vertices of a convex polytope,
  generically far fewer than `n` of them; a real, positive, simple leading
  eigenvalue sends them to at most **three** parallel hyperplanes
  perpendicular to the leading eigenvector; a paranormal `V` gives a polytope
  in one subspace and a linear subspace in the rest; `V = −I_d` collapses
  everything to the origin. Four theorems, four regimes.
- **The assumptions on `Q` and `K` are soft and the assumptions on `V` are
  not.** Numerically the clustering survives violating `Qᵀ K ≻ 0`; nothing
  survives the leading eigenvalue of `V` going negative or complex. `Q` and
  `K` decide which tokens attract which; `V` decides what kind of object they
  are attracted to.
- **The low-rank theorem is the part that touches practice.** At `d = 1` with
  `V > 0` and `QK > 0`, the attention matrix converges doubly exponentially to
  a Boolean matrix of rank 1 or 2 — a handful of tokens capture the attention
  of almost all the rest. The paper's own remark is the sharp one: the
  near-low-rank structure of `P` is the empirical premise behind Linformer and
  LoRA, and in both "the low-rank structure is imposed rather than extracted
  from `P` itself". `SOTA-184` and `SOTA-147` inherit that premise and now
  have a source for it, with conditions.
- **It refines rank collapse rather than repeating it.** Dong et al. showed
  pure attention *without* skip connections trivializes into one tight
  cluster. With residual connections the structure is a classification instead.
  `NOTE-105` already treats rank collapse as an established fact and the record
  held no source for it; this supplies the refinement and the reason the
  unqualified version is wrong about the architecture people train.
- **The idealization partly closes its own gap, which the first pass did not
  read far enough to find.** Time-independent weights are ALBERT's actual
  architecture, not only an analytic convenience. The discrete-time
  forward-Euler analogue is written out with the proofs stated to carry
  through. Clustering is reported to arrive "after few layers". And the
  hypotheses are checked on ALBERT-xlarge-v2: heads 5 and 14 satisfy both
  conditions with `⟨Qφ₁, Kφ₁⟩` = **1.3060** and **0.6719** — with the paper
  saying in the same breath that not all sixteen heads do.
- **Genericity is quantified, against the paper's own interest.** The
  leading-eigenvalue condition holds for about **14%** of real Ginibre
  matrices at `d = 128`, a fraction the authors say vanishes as `d → ∞`,
  slowly.
- **And the limits are stated by the source, not inferred.** Theorem 2.1 is
  one-dimensional, and Remark 7.9 gives a `d = 2` counterexample where two
  tokens form one cluster while `P` converges to the identity — so the rank of
  the limit is not the cluster count in general. Multi-head and feed-forward
  variants are open problems with numerics attached.
- **`Proposed` for one group and one missing measurement, not for being
  idealized.** The record already holds `THEORY-009` — a mean-field
  infinite-width limit — at `Active`. What stands between this and promotion
  is a forward pass: token trajectories tracked layer by layer in a trained
  model, cluster counts plotted against each head's value-matrix spectrum,
  including the heads that violate the condition. It requires no training.

### Added

- **`LIT-527`** — *Leaner Transformers: More Heads, Less Depth*
  (Saratchandran, Teney and Lucey, 2025), read as `NOTE-269`.
- **`LIT-525`** — *Transformers Learn Low Sensitivity Functions*
  (Vasudeva et al., 2024), read as `NOTE-271`.
- **`LIT-524`** — *Ghost in the Transformer* (Wang et al., 2025), read as
  `NOTE-268`.
- **`LIT-526`** — *Concepts Whisper* (Acharya, Rimal and Dhakal, 2026),
  read as `NOTE-270`.
- **`SOTA-322`** — trade attention heads for depth. `Proposed`,
  `unreplicated`.
- **`SOTA-321`** — verify a model's lineage from the singular spectra of
  its attention products. `Proposed`, `unassessed`.
- **`THEORY-064`** — transformers are biased toward low-sensitivity
  functions, and that bias is what their robustness is made of. `Proposed`.
- **`THEORY-063`** — contextual concept directions sit in the
  low-variance tail of the unembedding spectrum while vocabulary contrasts sit
  at the top. `Proposed`.

### Documentation

- **Heads for depth, isolated from the confound.** Six of the source's twelve
  configurations also shrink the MLP width, so their parameter savings are not
  evidence for the trade its title names. The five that hold the MLP fixed
  are: XCiT-M 84.4M → 59.0M at 81.4 → 81.7; TNT-B 65.4M → **30.9M** at 82.3 →
  82.3; DaViT-B 88.0M → 62.0M at 83.3 → 83.5; XCiT-L 189.1M → 103.8M at 82.1
  → 82.4; DaViT-L 196.8M → 140.0M at 83.6 → 83.6. Five for five hold or
  improve at 29–53% fewer parameters. Crammed BERT matches the original GLUE
  average of 78.6 at 84M against 119M.
- **It pulls against `SOTA-190` and no relation is declared.** That practice
  says increase depth before any other dimension. This removes depth and buys
  it back with head count. The axes differ — depth-against-width there,
  depth-against-heads here — neither paper cites the other, and nobody ran the
  comparison (`ADR-011`). Recorded in prose on both sides.
- **The mechanism is conditioning, which the record was already circling.**
  More heads lower the attention block's condition number, proved. `THEORY-041`
  says unconstrained matrices drift badly conditioned and is `Proposed`
  because nothing intervenes on conditioning alone. This intervenes on it by
  head count — not the experiment that account asks for, and the nearest thing
  the record holds.
- **A scalar that separates transformers from every other architecture.**
  Sensitivity to token-wise random input perturbation is lower for
  transformers than for MLPs, CNNs, ConvMixers and LSTMs, on vision and
  language, at matched training accuracy. It relates to polynomial degree and
  decision-tree size on Boolean inputs, so low sensitivity is simplicity bias
  in established senses; low sensitivity is proved to imply robustness in that
  setting; and it is the record's first architecture-comparable inductive-bias
  measure defined on the learned *function* rather than on weights.
- **Its grokking result is named beside `SOTA-200` and not folded into it.**
  Sensitivity falls during the modular-addition plateau while the training
  loss does not, which makes it a progress measure needing no reverse
  engineering. `SOTA-200` asks whether an apparent jump is a metric artefact
  and would be better off with such an instrument — on more than one synthetic
  task.
- **The record held no document about model provenance at all.** Grepping the
  practices for watermarking, fingerprinting or provenance returned nothing:
  three hundred recommendations about building and serving models and none
  about establishing where one came from. `DP-004` — an absence produces no
  unresolved code and no unbound relation.
- **And the fingerprint is built on the same matrix the stability cluster is
  about.** `W_q W_k^T` is the product whose spectral energy concentration
  predicts a training crash and whose spectral norm bounds attention entropy.
  Here its spectrum is a serial number, because the products absorb the
  permutation and rescaling that change weights without changing the function.
  F1 0.9867 over 55 model pairs against 0.9610 for the best prior method.
  Neither literature cites the other; recorded as an observation.
- **The provenance practice is `Proposed` for a specific missing
  measurement.** Every result is about correctly detecting derivation. Nothing
  measures the false-positive case — two models similar because trained alike
  and not derived — which is the case that decides whether this can support a
  claim about anyone. Its conditions say so, and say the difference between
  evidence and proof.
- **A paper that grades its own claims.** `LIT-526` reports concept
  directions anti-concentrating in the low-variance tail of the unembedding
  covariance — 17 of 17 models, three independent extraction methods — with
  static vocabulary contrasts concentrating at the other end. It also reports a
  robust **null** against the hypothesis it set out to test (`p = 0.95`), and
  a table labelling two of its six claims *partial*. Filed partly for the
  finding and partly for that.
- **Third instance of one shape, counted and not joined.** The small end of a
  spectrum carrying more than its magnitude suggests now appears in weight
  matrices (`LIT-517`), in the residual a low-rank branch hands its
  quantizer (`SOTA-314`), and in the unembedding covariance here. Three
  matrices, three literatures, no mechanism that survives being written down.
  `DP-009`.
- **Two papers from the batch were read and declined, with reasons.**
  *The emergence of clusters in self-attention dynamics* (`ARXIV-2305.05465`)
  is rigorous mathematics about an idealization — weights frozen, no training,
  behaviour as `t → ∞` — and while the eighteen topics can express its claim,
  it supports no recommendation and explains no practice the record holds. It
  is a candidate trunk if the record ever files rank collapse.
  *Fine-tuning CLIP in spectral space* (`10.1007/s40747-026-02280-w`) proposes
  perturbing the principal singular subspaces instead of adding a low-rank
  matrix, evaluated on three multimodal-sentiment benchmarks against an
  incumbent the record already holds (`SOTA-184`). The evaluation is too
  narrow to carry a recommendation stated at the breadth this record would
  have to state it. `DP-005`.

### Added

- **`LIT-523`** — *Stabilizing Transformer Training by Preventing
  Attention Entropy Collapse* (Zhai et al., 2023), read as `NOTE-265`.
- **`LIT-521`** — *Taming Transformer Without Using Learning Rate Warmup*
  (Qi et al., 2025), read as `NOTE-266`.
- **`LIT-522`** — *Pion: A Spectrum-Preserving Optimizer* (Shi et al.,
  2026), read as `NOTE-267`.
- **`SOTA-319`** — reparameterize every linear layer by its spectral norm
  with a learned scalar. `Proposed`, `unreplicated`.
- **`SOTA-320`** — bound the learning rate by the ratio of the update's
  spectral norm to the weight's, and drop warmup. `Proposed`, `unreplicated`.
- **`THEORY-061`** — attention entropy is bounded below by a quantity
  falling exponentially in the spectral norm of the query-key product.
  `Proposed`.
- **`THEORY-062`** — what crashes a transformer is spectral energy
  concentration, not low attention entropy as such. `Proposed`, and it
  `corrects` the one above.

### Changed

- **`SOTA-192` → v5.** A condition about diagnosis. The recommendation, the
  status and the `converged` consensus are unchanged.

### Documentation

- **The record held a failure and two remedies for it, and was missing the
  inequality that makes the failure inevitable.** `SOTA-192` (QK-norm) and
  `SOTA-131` (QK-clip) both rest on the observation that attention logits grow
  until the softmax saturates. Theorem 3.1 of `LIT-523` bounds attention
  entropy below by a quantity behaving like `Ω(Tσe^{−σ})` in
  `σ = ‖W_K W_Q^T‖₂·‖XX^T‖₂`, and the bound is tight. Saturation is forced,
  not unlucky.
- **And a reason the spectral norm grows at all.** Under Adam's idealized
  update `Δ = E[g]/√E[g²]`, the update's own spectral norm is bounded below by
  something growing like `√w` in the matrix width. That is the shape of an
  instability absent in small models and fatal in large ones.
- **The learned scalar in σReparam is the method, not a detail.** ViT-B:
  σReparam 82.2%, plain spectral normalization **69.81%**, WeightNorm 77.51%.
  A twelve-point gap between constraining the spectral norm and rescaling by
  it while learning the scale back.
- **A published account is contradicted by a published counterexample, and
  the record now carries both sides.** `LIT-521` reports attention maps
  that are sparse but not low-rank — near-identity, near-zero entropy — in
  runs that train fine, and says in those words that this is a counterexample
  to entropy collapse. The cause it offers instead is spectral energy
  concentration in `W_q^T W_k`, which collapses into fewer than ten directions
  in crashed runs. `corrects`, not `extends`: the bound survives, the step
  from low entropy to instability does not.
- **Three papers, three places to intervene, no comparison.** σReparam
  rescales the weight each step; the Weyl rule caps how fast the weight's
  largest singular value may grow; Pion forbids the spectrum from moving at
  all by updating through orthogonal equivalence transformations. Each beats a
  plain baseline. None is tested against the others, or against QK-norm or
  QK-clip.
- **All three remove a crutch, and the synthesis is deliberately not filed.**
  σReparam trains without pre-LN, warmup, weight decay or an adaptive
  optimizer; the Weyl rule replaces 60-epoch, 20-epoch and 2000-step warmups
  with nothing; Pion trains a 60M model with every normalization layer
  removed. "Warmup is a workaround for uncontrolled spectral growth" is the
  obvious reading and no paper here claims it, so it is recorded in prose in
  all three documents rather than filed as a theory sourced to papers that do
  not make its claim. `DP-010`.
- **The warmup-free result contradicts two `Active` practices, and the scales
  do not meet.** `SOTA-008` and `SOTA-100` both recommend warmup. The
  counter-evidence runs at 50M–307M — below where those were established and
  far below where warmup is expensive to get wrong. Recorded in the new
  practice's conditions; neither side is moved.
- **No practice was filed from Pion, on purpose.** Its recommendable claim —
  that spectrum-preserving updates can substitute for normalization layers —
  rests on one 60M model and one run. Its 200-layer stability number is 0.0892
  against Muon's 0.0927, which is not a result. Its 1.3B pretraining run wins
  the benchmark average and *loses* the validation loss to Muon, which the
  paper reports and this record repeats.
- **Pion sits against a measurement filed hours earlier and neither knows.**
  `LIT-520` finds the trace-normalized spectrum stops moving early in
  ordinary pretraining; Pion forbids it from moving from step zero. Whether
  the early spectral motion Pion forbids is the part that was doing the work
  is asked by nobody. Recorded as a juxtaposition, not a relation — nobody ran
  the comparison (`ADR-011`).

### Added

- **`LIT-517`** — *Small Singular Values Matter: A Random Matrix Analysis
  of Transformer Models* (Staats, Thamm and Rosenow, 2024), read as
  `NOTE-263`.
- **`LIT-516`** — *From Low Rank Gradient Subspace Stabilization to
  Low-Rank Weights* (Jaiswal et al., 2024), read as `NOTE-264`.
- **`LIT-519`** — *Complexity-Guided Component-wise Initialization for
  Language Model Pretraining* (Garbers and Oh, 2026), read as
  `NOTE-262`.
- **`LIT-520`** — *The Stability of Singular Distribution* (Zhang et al.,
  2026), read as `NOTE-261`.
- **`LIT-518`** — *The Truth is in There* (Sharma, Ash and Misra, 2023),
  filed on a partial reading for the debate it anchors.
- **`SOTA-318`** — choose the rank per matrix when compressing a
  transformer. `Active`, `unreplicated`.
- **`SOTA-317`** — do not rank singular directions by magnitude when
  deciding what to discard; check the small end, and after fine-tuning.
  `Active`, `unreplicated`.

### Changed

- **`THEORY-059` → v2.** Half its promotion condition is met. Weight-spectrum
  steepness outside diffusion transformers is measured; the condition is
  narrowed to the half nobody has touched, the spectrum of `W − Q(W)`.
  `Proposed` unchanged.
- **`SOTA-314` → v2.** Two conditions added, recommendation and status
  unchanged.

### Documentation

- **The question was `THEORY-059`'s and the answer is yes-with-a-
  qualification.** That account holds that a low-rank branch corrects
  quantization because weight spectra are steep and quantization-error spectra
  are flat, and it was `Proposed` because the steep half was plotted only on
  diffusion transformers. It is now plotted on BERT, Pythia-410M,
  Llama-3.1-8B, LLaMA-2 7B and 13B, Mistral-7B and eleven GPT-2-style
  checkpoints across six languages.
- **The steep case turns out to have a name, and so does the flat one.** A
  trained transformer's spectrum is a Marchenko-Pastur bulk plus outliers —
  exact agreement with MP at initialization, departures after training. MP is
  the law for a matrix with i.i.d. entries, which is exactly the hypothesis
  `THEORY-059` invokes for the quantization error. So the account's two cases
  are "MP plus outliers" and "MP" — sharper than the account said, and still
  not a measurement, because nobody plots the residual's spectrum.
- **Steepness is strongly non-uniform, which the account did not say.** Query,
  Key and MLP Gate converge to low rank; MLP Up, MLP Down and Value do not.
  Middle blocks resist, the first and last few give way. At 50% effective-rank
  reduction on LLaMA-2 7B, `q_proj` and `k_proj` take over 90% compression.
- **And that is a practice the record did not hold in any form.** Choosing the
  rank per matrix beats one global rank by ~6.4× in perplexity at 30%
  reduction (LLaMA-2 7B) and ~47× at 40% (13B). On LLaMA-7B at 25%
  compression, factoid QA is 79.02 for the full model, **34.63** uniform,
  71.89 per-matrix. Against *tuned* baselines the margin is ordinary — 71.89
  against SVD-LLM's 71.95 is a tie — and the practice says to quote it that
  way.
- **The premise has three instruments and they disagree about two cells.**
  Hessian gaps and heavy tails, activation-covariance overlap plus perplexity
  ablation, and effective-rank entropy across eleven checkpoints all find
  non-uniformity; they place Value and Gate differently. That disagreement is
  the argument for the practice being *measure yours* rather than *use this
  list*.
- **Magnitude order is not importance order, and that is the second
  practice.** In non-square transformer matrices the smallest singular
  directions overlap the activation covariance at 3σ and their removal is
  catastrophic: Llama-3 8B on GSM8K falls from 43.2% to **2.0%** when the
  smallest decile of the Down-Projection goes, against 40.0% for the same
  decile of the square Attention-Output. On RULER at 8192 context, removing
  the smallest decile scores 0.0 on all five tasks — the same as removing the
  largest.
- **It reconciles two published results that contradicted each other.** One
  group found small singular values essential; another found removing them
  improved reasoning (GPT-J on CounterFact, 13.3% → 24.1%, `LIT-518`).
  Varying only whether pruning happens before or after fine-tuning reproduces
  both. Fine-tuning writes into the small directions — so a pruning result
  measured on a base model does not transfer to an aligned one, and removing
  those directions can raise a task metric and remove the alignment together.
- **What the answer cost `THEORY-059`.** The account leaned on an unstated
  assumption: that once the dominant directions are peeled off, the remainder
  is undifferentiated. The remainder is where the bottom outliers live. That
  is flagged in both `THEORY-059` and `SOTA-314` and claimed in neither,
  because zeroing a direction is not quantizing it and nobody has drawn the
  damage curve against bit-width.
- **Nine of the fourteen candidate papers were not filed.** Four are about
  spectral norm, attention entropy or token dynamics rather than the shape of
  a weight spectrum; one is a fine-tuning method that uses SVD rather than a
  measurement of one; the rest are adjacent without bearing on the question.
  Recorded here so the next pass does not re-triage them.

### Added

- **`LIT-515`** — *Exploiting Block Coordinate Descent for Cost-Effective
  LLM Model Training* (Liu et al., 2025), read as `NOTE-260`.
- **`SOTA-316`** — when memory binds rather than time, train every
  parameter one block at a time, cutting the blocks on layer boundaries.
  `Proposed`, `unreplicated`.

### Documentation

- **The practice fills a hole between two the record already held.**
  `SOTA-184` trains a low-rank update, which is cheap and explicitly not
  full-parameter. `SOTA-155` distributes across poorly connected workers,
  which assumes workers. Neither answers "every parameter, one small GPU", and
  grepping the practices for block coordinate descent, layer freezing and
  memory-efficient full-parameter training returned nothing.
- **The partition rule is the contribution, and it is close to a priori.**
  Block coordinate descent puts no mathematical constraint on how the
  parameters are split, so the choice is free and should be made for the
  kernels: most operators live entirely inside a layer, so freezing whole
  layers keeps the optimized paths. A finer cut keeps the same parameter
  count and loses the kernel.
- **Three times the iterations, from the paper's own Table 2.** GPT-2 2B:
  9,968 → 28,870 on wiki, 9,652 → 25,898 on alpaca, 9,550 → 28,707 on
  slimpajama, for perplexity that is comparable or better (97.96 vs 96.69,
  27.85 vs 28.30, 58.82 vs 69.28). LLaMA 2B on alpaca is the exception at
  1.08× — 20,076 against 18,579, PPL 21.04 against 21.06 — and the paper does
  not remark on why.
- **Two cost figures that are not the same kind of claim.** 33% on A100/A800
  at 7B isolates the method: same device on both arms. The abstract's 2.6% on
  RTX 4090 does not, because the paper states the 4090's hourly cost is about
  a quarter of an A100's — that number is the method and the hardware
  substitution multiplied together.
- **Quality and cost are measured at different scales.** The perplexity
  comparison tops out at 2B; the 7B appears only in the economic experiments,
  and 1.6B, 5.4B and 10B are estimated from measured single-round speeds
  rather than trained. The practice being recommended is "train a big model on
  a small machine", and whether the big model comes out the same is the one
  thing not shown at the big size. That is what `promote_when` asks for.
- **The trade is memory for time, and the practice says so in its
  conditions.** Nothing here claims BCD reaches a given loss in less compute;
  it claims a given loss is reachable on less hardware. Three times the
  iterations on a cheaper machine can still be slower in wall-clock, so if a
  deadline binds this is the wrong answer.
- **Counted, and it does not extend the count.** Earlier units this session
  found reported numbers sensitive to a choice the report did not state. This
  is not that: the iteration column and the 4090 pricing are both in the body.
  It is the Gemini shape — complete disclosure with a flattering headline —
  recorded in the practice's conditions rather than promoted to a finding.
  `DP-009`, `DP-010`.

### Added

- **`LIT-514`** — *Rethinking Early Stopping: Refine, Then Calibrate*
  (Berta, Holzmüller, Jordan and Bach, 2025), read as `NOTE-259`.
- **`SOTA-315`** — early-stop and tune on validation loss after
  temperature scaling, then calibrate post hoc. `Active`, `unreplicated`.
- **`THEORY-060`** — calibration error and refinement error have separate
  minimizers during training, so the loss minimum is optimal for neither.
  `Proposed`.

### Documentation

- **The record had no calibration document at all.** Grepping the practices
  returns quantization scales, data-mixing temperature (`SOTA-102`, and
  `Superseded`) and incidental uses of "confidence". Eighty practices touch
  training and none asked whether the probabilities mean anything. The gap was
  a subject, not a paper.
- **The decomposition is classical; the observation about its minimizers is
  not.** A proper loss is calibration error plus refinement error. Minimizing
  it minimizes a *sum*, and the two terms do not bottom out at the same epoch
  — so the validation-loss minimizer carries non-zero calibration error and is
  not at the best refinement either. It is a compromise point nobody chose.
- **Why temperature scaling is the right instrument.** It rescales logits by
  one scalar, so it cannot reorder predictions: accuracy and refinement are
  untouched and only confidence moves. Validation loss measured after fitting
  it therefore estimates refinement alone, and one parameter barely overfits
  the validation set.
- **The instruction is a line in a training loop.** Fit a temperature on the
  validation set each time you would have read the loss, read the loss after
  it, stop there — then keep the temperature, because the selected model is
  deliberately one that was not penalised for over-confidence.
- **The proposed mechanism.** As the training set becomes well separated the
  model must make confident predictions to keep *training* calibration error
  small; across a generalization gap that confidence does not transfer, so it
  is over-confident on held-out data while refinement may still improve. This
  also reframes an observation the field treated as standalone — that modern
  networks are poorly calibrated after training — as the expected endpoint of
  minimizing a sum with one term still being traded away.
- **The scale is unusual for this corpus.** 196 tabular classification
  datasets across XGBoost, an MLP and RealMLP, 30 hyperparameter
  configurations per split; separately a vision benchmark with **ten runs per
  dataset** and about 300 GPU hours. Most of what this record holds is a
  single run.
- **Stopping on accuracy is the obvious alternative and it loses.** Accuracy
  is the intuitive refinement proxy; it is less consistent than TS-refinement
  on vision, and on tabular data often yields poor log-loss even after
  calibration. TS-refinement also frequently gives better accuracy and AUC
  than stopping on log-loss.
- **A side contribution that is itself a practice.** The loss is convex in the
  inverse temperature, so bisection on its derivative finds the fit — faster
  and lower-test-loss than the implementations in Guo et al.,
  TorchUncertainty and AutoGluon. Released as `probmetrics`.
- **Conditions the source states against itself.** Results are "more noisy and
  unclear" on small or easy datasets, and the headline tabular figure is
  restricted to ≥10K samples. The learning-rate schedule and regularization
  strength change how far apart the minima are, so the practice predicts the
  direction and not the magnitude.
- **`THEORY-060` is `Proposed` because the only party to have plotted the
  separation is the one proposing the remedy.** The `promote_when` asks for
  the two curves from a run set up for some other purpose — one figure, on any
  model with a validation set.
- **Counted, not generalized.** `SOTA-196` says report zero-shot and
  in-distribution performance separately because one hyperparameter moves them
  in opposite directions. This is the same shape one level down — two
  components of a single loss, moved oppositely by one knob, averaged into a
  number that hides it. Different mechanisms; `DP-009`.

### Added

- **`LIT-513`** — *mHC-lite: You Don't Need 20 Sinkhorn-Knopp
  Iterations* (Yang, 2026), read as `NOTE-258`.

### Changed

- **`SOTA-136`** → v3. Gains `LIT-513` as a source and one instruction:
  if you adopt the doubly-stochastic constraint, construct it exactly rather
  than approximating it. Status, consensus and recommendation unchanged.

### Documentation

- **Not a fourth constraint, and that matters for where it lands.**
  `SOTA-169`'s promotion condition says in as many words that another paper
  proposing a fourth constraint would not move the trunk. This keeps the
  doubly-stochastic constraint exactly as `LIT-140` states it and changes how
  the matrix is built, so the exclusion does not apply — and the trunk stays
  put anyway, because nothing here isolates width or ships in a released
  model.
- **The approximation gap is measured in training, not constructed.** The
  worked example uses a near-degenerate input (`α = 10⁻¹³`) where 20
  Sinkhorn-Knopp iterations leave column sums of **1.92, 0.59, 0.59**. On its
  own that would be adversarial; it is not, because Figure 4 measures the
  distribution of `log(1/ν)` over real SK inputs and finds **≈ 27.9%** at
  `1/ν ≥ 10¹³`.
- **And it accumulates with depth.** A single residual matrix's column sum can
  be off by **100%**; the layer-wise product `∏_l H^res_l` by **220%** at 24
  layers.
- **The replacement is exact and cheap.** Birkhoff-von Neumann: every doubly
  stochastic matrix is a convex combination of permutation matrices, so a
  softmax over permutation weights is doubly stochastic by construction. No
  iteration, no gap, no fused CUDA kernel.
- **This is the third document to look like it should settle the Birkhoff
  objection and not.** `LIT-139` was the production report at depth and
  measured no stream statistic; `LIT-152` was the independent evaluation that
  did not test the constraint; this repairs the implementation and also
  measures no stream statistic. Searching it for homogenization, diversity,
  distinctness or collapse returns nothing.
- **It is also the sharpest of the three misses, and the reason is worth
  keeping.** Under Sinkhorn-Knopp mHC the matrices are not actually doubly
  stochastic, so `LIT-151`'s objection has an escape hatch — whatever keeps
  the streams distinct might be surviving through the approximation gap.
  Exact construction closes it, which makes this the cleanest available test
  of whether the doubly-stochastic set homogenizes the streams. The objection
  predicts it should homogenize *more*. Nothing was measured either way. One
  histogram, on a model already trained, with public code.
- **The scale is small and the paper says so.** nanoGPT at S (6 layers, ~45M),
  M (12 layers, ~0.12B) and L (24 layers, ~0.36B), `n = 4`, for **10,000 steps
  ≈ 1.3B tokens total**, against a technique that ships at 1.6T. No seeds: the
  gradient-norm bands are within-window variation across steps, not across
  runs.
- **A methodological choice worth crediting.** Statistics are computed
  per-token over 64 sequences of length 1024 rather than averaged, explicitly
  because "averaging across tokens can hide potential instability" — the same
  discipline `SOTA-307` argues for elsewhere.

### Added

- **`LIT-512`** — *SVDQuant: Absorbing Outliers by Low-Rank Components
  for 4-Bit Diffusion Models* (Li et al., 2024), read as `NOTE-257`.
- **`SOTA-314`** — absorb quantization outliers into a high-precision
  low-rank branch taken from the weights, and fuse its kernels into the
  low-bit ones. `Active`, `unreplicated`.
- **`THEORY-059`** — a low-rank branch corrects quantization because
  weight spectra are steep and quantization-error spectra are flat.
  `Proposed`.

### Documentation

- **The idea that travels is an ordering, not an ingredient.** Decompose the
  weights and quantize the residual; do not quantize and then patch the error.
  The control is a published method that does it the other way round — LoRC
  puts its low-rank branch on `W − Q(W)` — and it underperforms.
- **The reason is proved, which is why the practice is `Active` on one
  source.** Proposition 4.1 bounds a layer's output error by four quantities:
  the rounding errors of weights and activations **and their magnitudes**.
  Proposition 4.2 bounds a matrix's rounding error by its own magnitude. So
  shrinking what you hand the quantizer shrinks both terms, and Eckart-Young
  makes the truncated SVD the optimal rank-`r` way to shrink it.
- **That makes the question spectral.** Subtracting a rank-`r` matrix removes
  exactly the magnitude held in the first `r` singular values, so the move
  pays on a steep spectrum and not on a flat one. Figure 5 shows `W`'s
  singular values are highly imbalanced and that the first 32 of the smoothed
  `Ŵ` drop steeply. A quantization error, being near-independent across
  entries, has no preferred directions.
- **The systems half is not optional, and the paper quantifies it.** A rank-32
  branch run independently costs **57%** latency from 16-bit reads and writes
  around the projections. Fused — Down Projection with Quantize because they
  share an input, Up Projection with the 4-bit compute because they share an
  output — it reaches 3.0× over W4A16 on a 16GB laptop 4090 and 3.1× on an
  RTX 5090 with NVFP4, at 3.5× memory reduction on 12B FLUX.1. The practice
  states both halves as one instruction because a reader who takes the
  decomposition and leaves the fusion has built something slower than where
  they started.
- **Proposition 4.1 is also a map of the record's quantization cluster.**
  `SOTA-185` compensates rounding error into not-yet-quantized columns;
  `SOTA-163` shrinks a scale's blast radius; this removes magnitude before
  quantizing. Different terms of one bound, composing rather than competing —
  which is why the source runs GPTQ on its own residual weights.
- **Superficially `SOTA-230`, and opposite in purpose.** QLoRA also puts a
  16-bit low-rank side beside a 4-bit base. There the branch carries new task
  information into a frozen base; here it carries existing weight magnitude
  away from the quantizer and learns nothing. The source draws the distinction
  itself.
- **One result recorded sceptically.** On FLUX.1-dev the 4-bit model exceeds
  the original BF16 model on Image Reward, which the source reads as
  "suggesting stronger human preference". A 4-bit model preferred over the
  model it approximates is more cheaply explained by Image Reward being a
  learned preference model with its own biases, and PSNR and LPIPS do not
  invert.
- **`THEORY-059` is `Proposed` for a specific gap.** The steep half is
  plotted; the flat half — that `W − Q(W)` has well-spread singular values —
  is asserted and used rather than measured, and it is the load-bearing reason
  the control fails. One line of code away, and the `promote_when` asks for
  both spectra outside diffusion.

### Added

- **`LIT-511`** — *Image-GS: Content-Adaptive Image Representation via 2D
  Gaussians* (Zhang et al., 2024), read as `NOTE-256`.

### Changed

- **`SOTA-205`** → v2. Gains `LIT-511` as a fifth source and its first
  outside 3D, with the decode-cost number the practice wanted. No change to
  the recommendation.

### Documentation

- **The practice was `converged` on four radiance-field papers and evidenced
  in one setting.** Image-GS carries the same claim to single-image
  representation, which is close to the weakest case for an explicit
  structure: no viewpoint, no occlusion, no geometry to exploit. It wins
  anyway, against six implicit baselines held at matched model size.
- **The decode number is the one the practice wanted.** The 3D sources argue
  from rendering speed, which entangles the representation with a rasterizer.
  This gives **0.3K multiply-accumulates per pixel** against C3's **3K MACs at
  0.31 bpp** — an order of magnitude, in the units the claim is about.
- **The comparison is run the way this record keeps asking for.** Six neural
  representations at 2K×2K with model sizes of **164, 166, 161, 154, 159, 164
  and 160 KB**, baselines' official implementations with only size changed,
  bitrate on the axis in bpp and bppc throughout. Beats all six across the
  range and passes JPEG below **0.244 bpp** — and says in the same sentence
  that JPEG and GI use entropy coding while Image-GS does not, which is what
  its random-access claim costs it.
- **The ablation inverts the headline, and the paper prints it plainly.**
  Against a full model at 31.77 dB: removing content-adaptive initialization
  entirely costs **2.23**, while removing the `1/s` reparameterization costs
  **2.66** and removing top-K normalization costs **2.42**. The two
  unglamorous optimizer choices each outweigh the content-adaptive allocation
  the paper is named for.
- **Second instance of that shape, counted not promoted.** `SOTA-304` records
  the first: in Genesys, removing the symbolic checker costs 62 points of
  validity against 19 for the clever unit-wise decomposition. Two instances
  from unrelated fields is a count; what would make it more is a mechanism,
  and "papers name themselves after the interesting half" is a sociological
  observation rather than one. `DP-009`.
- **The constructive counterpart to `LIT-494`.** GaussianToken landed two
  units earlier with comparisons matched on token *count* while each token
  carried an index plus five continuous floats, and `NOTE-243` recorded that
  nothing ruled out the rival explanation that it simply had more channel.
  Image-GS is the same primitives in the same year with bits per pixel on the
  axis. **No relation is declared** between them — nobody ran that comparison
  and `ADR-011` means what it says — but holding both is what makes the
  criticism of the first precise rather than general.
- **`extends: LIT-108` is earned.** The paper says it "is inspired by the
  recent success of Gaussian Splatting", defines its primitives "similar to
  the Gaussian primitives in 3D Gaussian Splatting", and states what it drops:
  no spherical harmonics, "as an image essentially shows a single view".
- **No new practice, and the reason is the fourth standing reminder.**
  Content-adaptive densification is what `LIT-108` already does in 3D and what
  `SOTA-205` already covers; a 2D instance adds a source, not a
  recommendation. The `1/s` reparameterization is the most surprising number
  in the paper and rests on one sentence about one parameter — filed as an
  open question rather than promoted.

### Added

- **`LIT-510`** — *Gemini: A Family of Highly Capable Multimodal Models*
  (Gemini Team, Google, 2023), read as `NOTE-255`. Filed for its
  evaluation appendices, not its models.
- **`SOTA-313`** — treat the inference-time decision procedure as part of
  what you are comparing, and report the ordering under each one. `Active`,
  `unassessed`.

### Changed

- **`SOTA-197`** → v2. Gains `LIT-510` as a third source and, with it,
  the practice's first number. No change to the recommendation.

### Documentation

- **The MMLU ordering flips twice inside the report's own appendix.** Greedy
  sampling: Gemini Ultra 84.0%, GPT-4 84.2%. Chain-of-thought at 32 samples:
  85.0% against 87.3%. Uncertainty-routed CoT at 32 samples: **90.0%** against
  87.3%. Human-expert performance is 89.8%, so exactly one of the three
  procedures crosses it. The main table reports the same shape — Ultra at
  **83.7%** 5-shot, the protocol every other model in that table is scored on,
  against GPT-4's 86.4%.
- **The mechanism, which is the part worth keeping.** The procedure is worth
  **6.0** points to Gemini Ultra and **3.1** to GPT-4, and the two gains have
  different sources: GPT-4 gets all of its from plain chain-of-thought with
  the routing rule adding nothing, while Gemini Ultra gets almost none from
  plain CoT and nearly all of it from the routing. So running the same
  procedure on both models is necessary and **not sufficient** — a procedure
  that is a no-op for one model and a six-point lift for another is a
  component of one of the systems, not a harness around both.
- **The routing threshold is a fitted parameter inside an evaluation
  protocol.** It is optimized per model on that model's own validation split,
  with no held-out confirmation reported.
- **Contamination, priced from the inside.** An additional **hundred
  fine-tuning steps** on web extracts corresponding to the HellaSwag training
  set take Gemini Pro to **89.6%** and Ultra to **96.0%** at 1-shot, against
  GPT-4's measured 92.3%. A hundred steps is nothing against any pretraining
  budget, so the gap between a contaminated and an uncontaminated number is
  smaller than the gap between two frontier models and costs a rounding error
  of compute. This is what `SOTA-197` was missing: its `consensus_note` said
  almost nobody states their exposure, and here is a frontier lab doing it
  against its own interest — dropping LAMBADA after leak analysis, reporting
  HellaSwag decontaminated at 10-shot only, and building Natural2Code from
  non-web sources.
- **A held-out control nobody asked for.** On FLEURS the report volunteers
  that its large gain comes from having trained on the FLEURS training set,
  then reports retraining without it: WER **15.8**, still ahead of Whisper.
- **Credit where it is due on the comparison itself.** The uncertainty-routed
  procedure was run on GPT-4 via API rather than quoting OpenAI's published
  number against Google's best, and rows mixing a quoted number with a
  measured one are labelled as such.
- **Sixth instance of the session's running shape, and the one that breaks
  it.** `SOTA-305`, `SOTA-307`, `SOTA-308`, `SOTA-309` and `SOTA-312` are all
  "a reported number is sensitive to a choice the report does not state". Here
  the report states everything — both protocols in the main table, the full
  sweep in the appendix, the contamination price, the FLEURS control — and the
  headline is still the flattering row. The remedy therefore cannot be
  "disclose more", so the count does not extend: this is `DP-010`, not the
  shape the other five share. `DP-009`.
- **A trunk gap closed on the way past.** `LIT-383` evidences `SOTA-233` on
  Gemini 1.0 Pro and 1.5 Flash, and the report describing those models was
  absent — the same gap `#243` was opened about.
- **Nothing filed about the models.** No architecture ablation, no data
  mixture, no scaling detail, no training compute. Nothing in this record
  should cite the report as a source on any of them.

### Added

- **`LIT-508`** — *Opening the Black Box of Deep Neural Networks via
  Information* (Shwartz-Ziv and Tishby, 2017), the claim.
- **`LIT-509`** — *On the Information Bottleneck Theory of Deep Learning*
  (Saxe et al., 2018), the rebuttal, read as `NOTE-253`.
- **`LIT-507`** — *Adaptive Estimators Show Information Compression in
  Deep Neural Networks* (Chelombiev, Houghton and O'Donnell, 2019), read as
  `NOTE-254`.
- **`SOTA-312`** — state the noise or binning assumption behind any
  mutual information you report for a deterministic network, and show the
  conclusion survives changing it. `Active`, `emerging`.
- **`THEORY-058`** — apparent compression in the information plane is
  saturating activations collapsing into extreme bins. `Proposed`.

### Documentation

- **`#220` is unblocked and the reading changed its framing.** The issue
  proposed this as a third instance of "the finding was in the measurement",
  alongside emergence and grokking under `SOTA-200`. That is too weak. In the
  emergence case the underlying quantity is real and a thresholding metric
  makes a smooth thing look sharp. Here the underlying quantity is
  **infinite**: for a deterministic map `H(h|X) = -∞`, so `I(h;X)` is
  unbounded and every finite number on an information plane is a property of a
  noise model the analyst imposed and the network never had.
- **The sensitivity is demonstrated twice, in opposite directions, by papers
  arguing against each other.** `LIT-509` re-bins the same `tanh` run
  evenly in *net input* instead of evenly in *activity* and the compression
  phase disappears; at full machine precision the information sits pinned at
  `log₂(P)`. `LIT-507` re-bins ReLU adaptively per layer and epoch and
  compression appears. Neither states this as its conclusion; it is visible
  only from holding both.
- **The three IB claims do not have the same status, and saying "the dispute
  is unresolved" would be wrong.** The two-phase claim is estimator-dependent
  and genuinely contested. The claim that compression causes generalization is
  refuted by `LIT-509`'s four-cell dissociation — compress-and-generalize,
  compress-and-overfit, neither, both — and independently by `LIT-507`,
  which set out to defend the theory and found no significant correlation in
  hidden layers. The claim that compression comes from SGD's diffusion is
  refuted by full-batch gradient descent compressing just as much, and by the
  gradient SNR transition appearing in ReLU networks that never compress and
  in a 1-1-1 linear network where compression is impossible.
- **What the rebuttal leaves standing.** The original's fourth claim — that
  depth dramatically reduces the epochs needed for good generalization, so the
  main benefit of hidden layers is computational — is examined by neither
  later paper. Recorded as an open question rather than as refuted.
- **Two consequences of the noise assumption that almost nobody quotes.** The
  data processing inequality does not apply to these estimates, because the
  noise is added per layer for analysis and does not propagate. And the
  estimate is **not** invariant to invertible reparameterization: scaling one
  linear layer by `c` and the next by `1/c` computes an identical function and
  generalizes identically, yet changes the reported mutual information. The
  promise of a "common currency" for comparing architectures fails on
  architectures that compute the same function.
- **`LIT-507`'s abstract is not supported by its own protocol.** It says
  saturation is not required for compression; its Figure 6, averaged over the
  50 initializations the original study used, shows a ReLU network with no
  distinct phase at all, fitting and compression "mostly cancel out". The
  showcased compression is one initialization, and Figure 5 shows
  initialization alone sends hidden layers on vastly different trajectories.
  `DP-010`, unusually clean.
- **The theory is `Proposed`, not `Active`, and the reason is the entanglement
  rather than the disagreement.** The saturation account says a fixed binning
  cannot resolve the saturation region — which is also why a differently
  placed binning removes the effect. Separating "saturation caused this" from
  "the bins were in the wrong place" needs a control neither paper ran, and
  the `promote_when` asks for it.
- **A pass-over recorded inside the practice.** `SOTA-200` is named to be
  distinguished from, not relied on. Two arrivals at "the measurement produced
  the finding" by different mechanisms is a count, not a generalization —
  `DP-009`.
- **Access.** Saxe et al. is not openly readable from this environment:
  OpenReview returns 403 to `/pdf` and to its API, and the JSTAT page resolves
  but serves no article text. The ICLR 2018 version was supplied by the
  record's owner; the DOI filed is the JSTAT one, per `ADR-009`, and the
  literature document says which version the numbers come from.

### Added

- **`LIT-505`** — *Biological structure and function emerge from scaling
  unsupervised learning to 250 million protein sequences* (Rives et al.,
  2021). Filed unread, as the trunk.
- **`LIT-506`** — *Interpretable RNA Foundation Model from Unannotated
  Data* (Chen et al., 2022), read as `NOTE-252`.

### Documentation

- **The record now holds a biological-sequence trunk, which it did not.**
  Before this, the corpus contained no protein, RNA or genomic sequence model
  at all. The protein ancestor is filed unread and says so, so that the RNA
  descendant can declare what it extends — the lesson `#243` taught when
  GaussianToken landed on an empty tokenizer trunk and could name none of its
  four baselines. The `extends:` relation is not a family resemblance: RNA-FM
  cites ESM-1b as reference 66 and takes its downstream ResNet32 from it
  verbatim.
- **The structural results are large.** F1 **0.941** on ArchiveII600 and
  **0.704** on bpRNA TS0 against twelve published methods; a single model on
  RNA-FM embeddings exceeds a 100-model ensemble by 30% on long-range top
  precision.
- **The one clean control is the weakest result in the paper.** Table 5 swaps
  the input of Paul et al.'s published UTR CNN and holds everything else
  fixed. On Human7600 — the real-human generalization set — one-hot sequence
  gives `R²` 0.814 and the 640-dimensional pretrained embedding gives
  **0.816**, while a 16-dimensional *predicted secondary structure* gives
  **0.820**. Three times the gain from a representation forty times smaller.
- **One row goes the wrong way and is not mentioned.** `Seq + SS + RNA-FM` on
  Human7600 scores 0.811 against `Seq` alone at 0.814, with the worst MSE in
  the table at 0.287. The surrounding text says accuracy "is indeed further
  improved" and that gains are "consistent across all the lengths and
  contexts".
- **Nothing checks the pretraining corpus against the test sets.** The
  pretraining set is named **RNAcentral100** — the 100 is the cd-hit-est
  cut-off, so identical sequences were collapsed and nothing else removed.
  RNAcentral aggregates 47 databases and the paper describes it as
  representing all ncRNA types; the secondary-structure benchmarks come from
  that same universe. bpRNA-1m's 80% identity filter is internal and says
  nothing about the relationship to pretraining. This is the standard protocol
  for the model family and is not misconduct, but the margin over methods that
  never saw the sequences is not only a margin in representation quality.
- **The paper is honest in the two places it counts most.** Its abstract
  volunteers that the margin drops from ~30% to 4–7.5% on the low-redundancy
  dataset, and its Discussion volunteers that "the improvement brought by
  RNA-FM in the functional tasks seems more slight compared with the gain in
  the structural tasks". Neither sentence is in the title.
- **No practice, for two reasons.** The recommendation the paper argues for —
  pretrain self-supervised on the unlabelled pool when labels are scarce — is
  already carried implicitly across every practice in this record that touches
  pretraining, so a new domain adds an instance rather than evidence
  (`DP-005`). And the narrower recommendation it *could* have supported — keep
  the published task model, swap its one-hot input for embeddings — is exactly
  Table 5, where the controlled effect is 0.002 `R²`.

### Added

- **`THEORY-057`** — a corpus a model generates is narrower than the
  distribution it imitates, and the narrowing shows up as n-gram
  over-concentration. `Proposed`, explaining `SOTA-172` and `SOTA-295`.

### Changed

- **`THEORY-051`** → v2. No change to the account; adds a section naming
  `THEORY-057` and saying why the record has not joined the two.

### Documentation

- **Two narrowings, filed separately and pointed at each other.** `#234` asked
  whether generated-corpus collapse and tool-assisted human collapse are one
  phenomenon. The record declines to answer, and the two documents now name
  each other so the next reader inherits the question rather than
  rediscovering it.
- **Why they are kept apart.** The metrics are not the same measurement —
  n-gram over-concentration and mean pairwise embedding similarity move
  independently, and paraphrase preserves one while destroying the other. The
  human-in-the-loop path has a selection step the generated path lacks, and
  `LIT-487`'s treatment is *access* to the tool rather than use of it, so it
  cannot say whether accepting damps the narrowing or amplifies it. And the
  harms differ in kind: a model trained on a narrow corpus is damaged
  differently from a signal between people that stopped carrying information.
- **The strongest reason is in `THEORY-051`'s account, not in the
  statistics.** Its mechanism is scarcity — a feature predicts partly by being
  uncommon — and scarcity has no counterpart in the generated-corpus case,
  because a pretraining corpus is not competing with itself for a rivalrous
  outcome. Two things can share a statistical signature entirely and have
  different causes.
- **What the new theory adds beyond restating its two practices.** `SOTA-172`
  and `SOTA-295` disagree about the remedy — edit human text, versus supply
  the entropy from outside the prompt — and agree about the disease. That
  agreement was stated in prose in `SOTA-295`'s conditions and had no page of
  its own. Two groups, two corpora, two instruments, no citation in either
  direction.
- **What `LIT-485` rules out, which makes it more than a repetition.**
  TinyStories had already identified this failure and built a lexical
  mechanism against it: a fresh word list per story. The corpus stayed
  formulaic, because the *shape* of the request never changed. So the
  narrowing is not merely "the prompt was the same" — a prompt distribution
  designed to be diverse still produced a corpus whose top 4-gram covers three
  fifths of it.
- **`Proposed`, and the missing control is named.** Neither source isolates
  the model's contribution: a generated corpus is narrow, and the narrowness
  has at least two possible owners — the model's sharpened output distribution
  and the prompt distribution fed to it. Nothing measures the seed
  distribution's own concentration as a floor. The `promote_when` asks for one
  seed distribution through two generators, and explicitly refuses another
  formulaic corpus, which is the observation rather than the account.
- **Two corpora, both English, both short-form.** Whether the same
  concentration appears in generated code or generated mathematics is untested
  here — and mathematics is where the field currently generates most heavily.

### Added

- **`SOTA-311`** — evaluate a search on tasks held out of its own fitness
  function, and report the gap against the tasks it selected on. `Active`,
  `unassessed`, and the record's first practice with an empty
  `introduced_by:`.
- **`ADR-053`** — a practice may state that it has no identifiable
  origin, by leaving `introduced_by:` empty. Amends `ADR-030`.

### Changed

- **`luria.yaml`**: `schemes.SOTA.references.introduced_by.required` is now
  `false`. The comment beside it says why, and that the convention is narrower
  than the schema.

### Documentation

- **The practice has no source that argues for it, and says so in its first
  paragraph.** `LIT-493` is cited as the instance that made the gap visible —
  a search that did not hold anything out — not as evidence for the
  recommendation. The recommendation rests on a fact about maximization: the
  maximum of many noisy estimates is a biased estimate of the maximum of the
  underlying quantities, and the bias grows with how many candidates were
  maximized over. What nobody has measured is how large it gets here.
- **Two selection steps share a metric with the report, and the second is the
  unusual one.** Genesys selects designs by fitness — average downstream
  accuracy — and then selects the nine reported benchmarks from the same pool
  by *largest standard deviation across the search population*. A benchmark
  chosen because designs differ on it is, by construction, one where the best
  of 1,062 sits far above the middle.
- **What the paper's own tables show.** Best discovered design 61.81 against
  best seed 61.78 — a margin of **0.03** — and the five discovered designs
  average **60.17** against the seeds' **60.77**.
- **`Active` with no evidence behind it, deliberately.** A practice is
  `Proposed` here when the record does not know whether the recommendation is
  right; the direction of this one follows from what selection is. What is
  unknown is the magnitude, which is what `consensus: unassessed` and the
  conditions carry. The general argument is standard in statistics and well
  known in the NAS and AutoML literature; the record simply holds no paper
  that quantifies it, which is a gap in the corpus rather than a reason to
  leave the shelf empty.
- **The order-of-magnitude check is labelled as this record's arithmetic.**
  Under assumptions the practice states and then says overstate the effect,
  the expected best of 1,062 draws sits about 3.7 standard deviations above
  the population mean — around five points on a benchmark whose design-to-
  design spread is 0.0138, against reported margins of half a point to two and
  a half. The point is the order, not the number.
- **Why `introduced_by:` is empty rather than filled with `source[0]`.**
  Writing `LIT-493` there would assert in a machine-readable field that
  Genesys first recommended holding tasks out, which it did not. `ADR-030`
  made the field required because absence was ambiguous between "the origin is
  the primary source" and "nobody checked"; this is a third case that decision
  did not anticipate — the record looked, and can name no such document.
- **The cost is stated rather than minimised.** With `required: false` the
  lint can no longer catch a practice that forgot the field, and the
  replacement is a convention, which decays. What would buy the guarantee back
  is an upstream distinction luria does not currently draw: a `required:`
  satisfied by an explicitly empty list but not by an absent key. `luria lint`
  reports both as "no `introduced_by:` in frontmatter".
- **Genesys is not being accused of anything.** Table 16 is published, the
  selection standard is stated in the paper, and the checkpoints are online.
  The gap was nameable only because the paper hands a reader the instrument to
  check it — `DP-004`, since the query that found it was shaped like the
  paper's own appendix.

### Added

- **`LIT-504`** — *Everything, Everywhere, All at Once: Is Mechanistic
  Interpretability Identifiable?* (Méloux, Maniu, Portet and Peyrard, 2025),
  read as `NOTE-251`.
- **`SOTA-310`** — treat a mechanistic explanation that passes circuit
  error or causal alignment as one of many, and report what you did to rule
  the others out. `Active`, `unreplicated`.

### Documentation

- **Circuit error and IIA are satisfiability tests, not selection rules.**
  They establish that an explanation is admissible and say nothing about how
  many others are equally admissible. Nobody had counted, because counting
  needs a model small enough to enumerate exhaustively.
- **The counts, by exhaustive enumeration.** Median computational abstractions
  rise from **38 to 910,000** (circuit-first) and **8 to 3,700**
  (algorithm-first) as width goes 2 → 5. Under **2%** of trained networks have
  exactly one valid minimal mapping; **no network** has exactly one circuit
  interpretation. Both figures are lower bounds by construction — the
  enumeration is capped at sparsity above 0.3 and to two-input/one-output
  circuits — so any error runs in the direction that makes it worse.
- **`Active` on one paper, and the reason is the method.** Exhaustive
  enumeration over a space small enough to exhaust cannot be underpowered, and
  the recommendation costs a sentence: say what you did not rule out.
- **Sparsity is considered as a tiebreak and rejected**, in a line worth
  keeping: "Should we dismiss an entirely different candidate explanation
  simply because it involves one additional node than another?"
- **One lever, and it is thin.** Training on more tasks significantly reduces
  the number of valid abstractions (`p = 0.05`) up to four tasks, then
  plateaus. Not filed as a practice: acting on it means changing how a model
  is trained in order to make it easier to explain, which is a larger decision
  than `p = 0.05` at one width carries.
- **The scale question is left where the paper leaves it.** One partial
  demonstration — 3,209 valid circuits in the enumerable tail of an MNIST
  network — plus a burden-shifting argument that if the problem vanishes at
  scale, somebody must show why. The practice records this as an argument
  about burden rather than as evidence about large models.
- **What the paper does not claim.** It does not say mechanistic
  interpretability is wrong. §5.1 treats the pragmatic position — that
  predictivity and manipulability may be all an explanation is owed — as live,
  and the authors' constructive recommendation is to state which epistemic
  goal an explanation serves. The practice asks for the count and the stated
  goal, not for the count to be one.
- **Completes a set.** `SOTA-278` (rule out the evaluation before reporting a
  model cannot do something) and `SOTA-286` (measure how much of parameter
  space behaves like your sample) are the other two. This is the same
  discipline at the explanation end, and the sharpest of the three because the
  criterion is *passed* — nothing looks wrong.

### Added

- **`LIT-503`** — *First Contact: Unsupervised Human-Machine Co-Adaptation
  via Mutual Information Maximization* (Reddy, Levine and Dragan, 2022), read
  as `NOTE-250`.
- **`SOTA-309`** — score a control interface by the mutual information
  between the operator's command and the state change it induces, and choose
  the horizon of that state change deliberately. `Proposed`, `unreplicated`.

### Documentation

- **The idea is one sentence and a good one.** Whatever the operator is trying
  to do, an interface they can use produces commands that explain what
  happens, so `I(x_t, (s_t, s_{t+Δ}))` scores the interface with no labels, no
  reward and no task list. Spearman **ρ = 0.43** against ground-truth task
  completion across 540K examples, and maximizing it directly learns a usable
  interface from scratch in under 30 minutes with 12 participants.
- **The horizon is in the practice's title because the sign depends on it.**
  In the shared-autonomy Lunar Lander data the assistant helps by *overriding*
  the user to prevent crashes — which is precisely what lowers one-step mutual
  information, while *raising* their influence over later states because they
  have not crashed. At `Δ = 1` the correlation with true reward was **strongly
  negative**; at episode length it is positive. A one-step influence metric
  punishes an assistant for assisting.
- **The fix reintroduces what the method removed, and the authors say so.**
  Choosing `Δ` "requires prior knowledge of the timescale of the user's
  desired influence over the system... This is the primary limitation on the
  generality of our method." The abstract's "completely unsupervised" is
  unsupervised *given a hyperparameter that encodes what the user is trying to
  do* — still a large reduction in what must be known, and not nothing.
- **Four domains of five, and the abstract says "a variety".** The ρ = 0.43
  average is over the four that worked; the fifth is the one that inverted.
- **What the objective rewards is a usable channel, not an intuitive one.**
  Across 12 users the learned perturbation angle converges to two modes: no
  perturbation and **exact inversion**. Both are consistent mappings a person
  can learn. The motivating sentence is about intuitiveness; the measured
  quantity is reliability of the command-to-outcome relation.
- **Scale is small and stated:** the largest interface has 8 parameters,
  limited by user-study duration and the data efficiency of the
  Bayesian-optimization RL.
- **Fourth measurement trap of the day, and the sharpest.** Beside
  `SOTA-305` (reconstruction FID needs its rate), `SOTA-307` (generation FID
  needs seeds) and `SOTA-308` (recall bought with relevance), this one flips
  the **sign** of a correlation rather than shifting its size — and flips it
  exactly when the system under test is working. Four instances from four
  unrelated fields of "the reported number is sensitive to a choice the report
  does not state". Counted, not generalized: `DP-009`, and four things are not
  obviously one mechanism.

### Added

- **`LIT-502`** — *MemGraphRAG: Memory-based Multi-Agent System for Graph
  Retrieval-Augmented Generation* (Wu et al., 2026, KDD), read as
  `NOTE-249`.
- **`SOTA-308`** — when a retrieval change raises recall, measure
  relevance and the end-task metric before calling it an improvement.
  `Active`, `emerging`.

### Documentation

- **The practice comes from the pilot study, not the system.** On G-Medical,
  three published GraphRAG pipelines beat vanilla RAG on evidence recall
  (GFM-RAG **84.3%** against 71.8%) and lose on context relevance (**38.5%**
  against 62.9%), and end-task accuracy falls with it. Twelve points of
  coverage bought at twenty-four points of precision.
- **The evidence runs against its presenters' interest**, which is why the
  practice is `Active` on one benchmark family. The authors are proposing a
  GraphRAG system and their §3 establishes that GraphRAG as a family trades
  relevance for recall at a net loss; they also cite two independent
  benchmarks that had already found advanced GraphRAG underperforming naive
  RAG.
- **Forty per cent of the graph is free to delete**, and the record states
  that more strongly than the source does. Filtering the lowest-frequency 40%
  of extracted triples moves accuracy 64.85% → 65.28%. The paper reads that as
  evidence of thematic noise; 0.43 points is inside anyone's noise, and the
  result the number actually supports is that a 40% reduction costs nothing.
- **`emerging` rather than `unreplicated`, and the reason is a shape rather
  than a number.** `SOTA-210` reports the same failure with a different pair
  of metrics in a different field — reinforcement learning raises pass@k and
  lowers pass@1, and the literature reports the favourable one. Two instances
  in two fields with no shared mechanism established: recorded as an
  observation in both documents and promoted to nothing, per `DP-009`.
- **No practice rests on MemGraphRAG itself.** Single runs, no seeds, the
  authors' own system against baselines they ran — and a transferability
  section whose verbs outrun its numbers: HippoRAG 51.07 → **51.78** and
  MS-GraphRAG 43.75 → **44.21**, one run each, described as "consistent
  improvement" that "substantially strengthens the effectiveness of existing
  retrievers". Having filed `SOTA-307` an hour earlier on what several
  hundred training runs say sub-point deltas are worth, the record is not in
  a position to accept that framing. The underlying claim may still be true.
- **The record's first GraphRAG document.** `SOTA-269` says keep a knowledge
  base outside the weights; nothing until now said how to tell whether the one
  you built is any good. This arrives as a caution rather than a method.
- **One control the source does not run, named in the reading.** The 40%
  result says a large part of the graph is disposable; it does not show that
  the frequency ordering identifies *which* part. Deleting 40% at random is
  the missing arm.

### Added

- **`LIT-501`** — *The FID Lottery: Quantifying Hidden Randomness in
  Generative-Model Evaluation* (Dufour, Efros and Pérez, 2026), read as
  `NOTE-248`.
- **`SOTA-307`** — report generative FID as an error bar over several
  training seeds, and treat any gap below about 2% of the mean as
  inconclusive. `Active`, `unreplicated`.

### Changed

- **`SOTA-143` to v2.** The µP practice already hedged that transferred values
  are "a starting point that production recipes then adjust". That hedge now
  has a number on one family: the optimum transfers as a **1.7×-wide window**,
  not a point, because seed variance blurs it into a flat region.

### Documentation

- **The finding is not that FID is noisy but which noise dominates.**
  Everyone knows a single FID has error bars; almost everyone estimates them
  by resampling a fixed model, which measures the small term. On a converged
  SiT-B/2 panel of 25 training seeds × 10 sampling seeds,
  `σ_between = 0.438` against `σ_within = 0.137` — **3.2×** — and ten times
  the sampling budget shrinks the within-seed jitter by `√10` while leaving
  the 0.44-wide between-seed envelope exactly where it was. The source's own
  observation: that envelope "is already larger than the headline gain claimed
  in many recent papers".
- **The control is what makes it a measurement rather than an anecdote.** 24
  retrains with initialisation, data order and training noise all fixed,
  leaving only multi-GPU floating-point reduction order. The EMA weights end
  **5–6% of their norm apart** — genuinely different networks — and
  `σ_between` falls to 0.047, *below* the within-seed floor of 0.119,
  inverting the ratio to 0.4×. The lottery is in the draws the recipe intends,
  not in numerical noise.
- **Initialisation is not the largest source.** Varying one generator at a
  time: flow-matching loss noise **0.336** (77% of the full 0.438), init
  **0.294** (67%), data order **0.221** (51%). The folk version in which
  "different seeds mean different inits" has it second. And the three combine
  **sub-additively** — quadrature predicts 0.50 against an observed 0.44 — so
  one-at-a-time ablations overstate what fixing any single source buys.
- **Scale does not tighten the floor.** CoV stays inside `[0.74%, 2.06%]`
  across all 76 cells of a four-size, ten-checkpoint panel, median **1.30%**,
  and is non-monotonic in size. "Reproducibility is a property of the metric
  and the loss, not of compute or scale."
- **The compute framing is the one to quote.** Anchored to the FID the
  unluckiest of ~20 seeds reaches at 2M steps, the luckiest gets there
  **1.25× faster on S/B, 1.82× on L, 2.0× on XL** — so a single-seed paper
  claiming a ~1.3× speedup on this architecture is competing with what the
  seed lottery delivers for free.
- **`unreplicated`, and the reason is the authors'.** One combination — SiT,
  flow matching, class-conditional ImageNet `256×256`, Inception-V3 — which
  they describe as "a calibration target for that combination, not a universal
  constant". What generalizes is the shape and the protocol. The practice
  says port the protocol and measure your own floor, and records that **recall
  is the outlier** among the metrics replicated in the appendix.
- **Beside `SOTA-305`, not on top of it.** That practice wants the token count
  stated beside a *reconstruction* FID; this wants an error bar over training
  seeds beside a *generation* FID. Derived independently from different
  papers, on different halves of the same metric family — two ways to publish
  a Fréchet distance that does not mean what it looks like.
- **Taken ahead of its dwell rank, deliberately.** All the remaining [#180](https://github.com/dmarx/anthology-of-the-sota/issues/180)
  candidates sit at six revisits, and the ordering below that is a tiebreak
  this session invented rather than anything the task specified. Within a tie,
  adjacency to a practice filed an hour earlier is a better reason than
  seconds-on-page.

### Added

- **`LIT-500`** — *Vector-quantized Image Modeling with Improved VQGAN*
  (Yu et al., 2021), read as `NOTE-247`. ViT-VQGAN: the origin of the
  codebook design `SOTA-306` rests on.

### Changed

- **`SOTA-306` to v2, retitled, and `emerging` → `converged`.** Filing the
  origin corrected the practice in three places, which is the argument for
  filing origins rather than only the papers that cite them.
- **`LIT-497` declares a second ancestor.** LlamaGen credits Yu et al. for the
  codebook design; now that the paper is in the record the `extends` is
  declared, and the note says what reading the origin revealed — LlamaGen
  *reimplements* the idea rather than reproducing it.

### Documentation

- **The instruction was wrong, or at least not the mechanism.** `SOTA-306` v1
  said "make the code vectors low-dimensional". The origin's instruction is to
  **factorize**: project the encoder output down to a low-dimensional *lookup*
  space, match there, then project the winner back up to a high-dimensional
  embedding — "decoupling code lookup and code embedding", in its own words.
  Nearest-neighbour search wants low dimension because distances concentrate;
  the embedding wants high dimension because that is where the capacity is.
  Both framings produce the effect and only one names why.
- **`ℓ₂`-normalization was carried as an unablated detail and is the largest
  effect in the table.** v1 said it was "reported as part of the same design
  and is not separately ablated in either paper here", which was true of the
  two descendants and false of the origin. Removing it at lookup dimension 32
  takes codebook usage to **2%** and FID to **5.44** — worse than leaving the
  lookup at 256 dimensions.
- **Utilization is necessary and not sufficient, which v1 got wrong.** It
  called utilization "the mechanism". The origin's dimension-4 row reports
  **96% usage — the best in the table — with 3.68 FID**, tied for worst among
  the normalized rows. Every code gets used and none of them can say enough.
- **Three points on the optimum, and no account of it.** Best lookup dimension
  is **16** in ViT-VQGAN, **8** in LlamaGen, **3** in GaussianToken, on three
  architectures. The practice still says sweep, and now says so with three
  data points rather than two.
- **`converged` rather than `emerging`, and the reason is specific.** Two
  measurements of somebody else's recommendation is corroboration; a
  recommendation plus two independent confirmations — one of which cites
  nobody — is the field having settled. The consensus note says which of the
  two the record is claiming.
- **The causal claim the descendants dropped.** ViT-VQGAN states that VQGAN
  relied on top-`k` and top-`p` sampling heuristics *because* its codebook was
  mostly dead, and samples at temperature 1.0 with neither at codebook size
  8192. That is a diagnostic worth having — check how many codes are alive
  before reaching for sampling heuristics — and it is **not filed**, because
  the paper demonstrates one half of it and never runs the comparison that
  would separate "unnecessary" from "not tried". The reading carries it as a
  candidate with a cheap experiment attached.
- **`β = 0.25` passes through a third paper untested.** VQ-VAE reported it
  insensitive over 0.1–2.0 at `K = 512` in 2017; ViT-VQGAN uses it "in all our
  experiments" at `K = 8192`. `NOTE-245` asked whether that survives at modern
  codebook sizes, and this filing makes the question sharper rather than
  answering it.

### Added

- **`LIT-499`** — *Neural Discrete Representation Learning* (van den
  Oord, Vinyals and Kavukcuoglu, 2017), read as `NOTE-245`. VQ-VAE: the
  root of the discrete tokenizer line.
- **`LIT-496`** — *Taming Transformers for High-Resolution Image
  Synthesis* (Esser, Rombach and Ommer, 2020), read as `NOTE-246`.
  VQGAN: the loss that made `f = 16` survivable.
- **`LIT-498`** — *MaskGIT* (Chang et al., 2022). Bidirectional masked
  decoding: 8 steps instead of 256, FID 6.18 vs 15.78.
- **`LIT-497`** — *Autoregressive Model Beats Diffusion* (Sun et al.,
  2024). LlamaGen, and the codebook and token-count ablations both new
  practices rest on.
- **`SOTA-306`** — make the codebook's code vectors low-dimensional and
  the codebook large, and report utilization alongside reconstruction quality.
  `Active`, `emerging`.
- **`SOTA-305`** — state the token count and input resolution beside any
  reconstruction FID, and compare tokenizers only at equal rate. `Active`.

### Changed

- **`LIT-494` to v2.** GaussianToken was filed two hours ago with no
  relations, because none of its baselines existed in the record. It now
  declares `extends` VQGAN — it is implemented as a module inside one — and
  `compared_against` VQ-VAE, MaskGIT and LlamaGen. The Standing paragraph
  asserting the trunk's absence is replaced by what closing it settled.

### Documentation

- **Closing [#243](https://github.com/dmarx/anthology-of-the-sota/issues/243) produced two practices, which is what the issue
  predicted and not a foregone conclusion.** Both come from LlamaGen's
  ablations, and both are corroborated by GaussianToken's — independently,
  on a different architecture and dataset.
- **The codebook practice has a mechanism and an interior optimum.** Dropping
  the code vector dimension from 256 to 8 takes utilization from **0.29% to
  97%** and rFID from 9.21 to 2.19: in 256 dimensions nearly every encoder
  output has the same nearest neighbour, so the codebook is decoration. But
  dimension 4 scores **9.88**, worse than 256. GaussianToken's independent
  sweep has the same shape with its optimum at 3 rather than 8. So the rule is
  "shrink it and sweep", and the practice says so rather than naming a number.
- **Both sources state the monotone half in their captions and leave the
  reversal in the table.** LlamaGen's reads "Lower vector dimension (from 256
  to 8) improves both", bounded exactly to exclude the row that reverses it;
  its codebook-size caption is bounded the same way. GaussianToken, to its
  credit, describes its own curve as rising then falling.
- **The reporting practice comes from one table and is the sharper of the
  two.** The *same* LlamaGen tokenizer scores rFID **2.19 / 0.94 / 0.70** on
  256 / 576 / 1024 tokens, every reconstruction resized to `256×256` before
  scoring. A three-fold range from a knob that is not the tokenizer — and
  LlamaGen's abstract quotes the 576-token row as "downsample ratio of 16,
  reconstruction quality of 0.94 rFID", which a reader maps to `256×256` and
  256 tokens, where the number is 2.19. §4's prose gives the same pair as 2.43
  and 0.99. Three versions of one comparison.
- **GaussianToken quotes the correct row**, which is worth recording now that
  both documents are in the record: it cites LlamaGen at 2.19, matched on
  token count. Its own rate mismatch runs the other way, through the five
  continuous parameters each of its tokens carries, and is a different error
  from its source's.
- **Neither VQ-VAE nor VQGAN yields a practice, and the readings say why.**
  Straight-through plus a codebook loss, `β = 0.25`, the perceptual-plus-
  adversarial objective and the adaptive `λ` are the substrate of the line
  rather than live choices, and none is measured against its alternative
  anywhere this record holds. Two candidates are named instead: whether `β`'s
  reported 0.1–2.0 insensitivity survives at `K = 16384` when it was found at
  `K = 512`, and whether the adaptive `λ` beats a tuned constant — an ablation
  nobody appears to have published while everybody copies the formula.
- **The next gap in this line is named rather than filled.** LlamaGen credits
  the low-dimension, `ℓ₂`-normalized, large-codebook design to ViT-VQGAN (Yu
  et al., 2021), which the record still does not hold. Both new practices are
  therefore two independent measurements of somebody else's recommendation
  rather than two independent discoveries, and the consensus note says so.

### Added

- **`LIT-495`** — *On the Statistical Query Complexity of Learning
  Semiautomata: a Random Walk Approach* (Giapitzakis, Fountoulakis, Nichani
  and Lee, 2025), read as `NOTE-244`.
- **`THEORY-056`** — distinct state machines agree at chance on long
  random inputs, so a learner that reads only statistics loses the signal as
  the sequences get longer. `Proposed`.

### Documentation

- **The mental model is the reason this is filed, and it inverts a common
  intuition.** Reading a uniformly random symbol applies a random permutation,
  so reading a word is a random walk on `S_N × S_N`. The probability two
  distinct machines land in the same state is `1/N + error` with
  `|error| ≤ (1 − 1/2N)^T`. The quantity that identifies which machine you are
  looking at decays **exponentially in sequence length**. Past the mixing time
  every machine in the family looks alike, and the information was not lost by
  the model or the optimizer — it was destroyed by the data. More of this kind
  of context is less evidence.
- **The hardness is structural, which is the paper's own claim to novelty.**
  Every prior SQ lower bound for finite automata embeds a hard language —
  usually parity — into what the machine accepts, often under an adversarial
  input distribution. A semiautomaton has no accepting states, so there is
  nowhere to hide one. This is hardness from the transition functions alone,
  under the **uniform** distribution.
- **The regime belongs beside the theorem.** The construction needs an
  alphabet of `Ω(N³ ln N)` and words of `Ω(N² ln N)` — roughly 4.6 million
  symbols for a hundred-state machine. That is not a shape any real sequence
  task has, and it is the first thing a citing reader will drop.
- **A new axis for the limits cluster.** `SOTA-178` and `THEORY-038` are
  **expressivity** claims — what an architecture can represent. This is a
  **learnability** claim — whether gradient descent finds it. The two can
  disagree in the direction that matters: a model that provably represents a
  machine can still be unable to learn it. `SOTA-278` covers a third reason a
  capability looks absent, measurement. The record now names all three and
  says they are different.
- **No practice.** The result is a proof about one constructed family in a
  regime nobody trains in, with no experiments, and the step from SQ hardness
  to gradient-descent hardness is a cited equivalence (Abbe et al., 2021,
  holding with large mini-batches or low precision) quoted once in related
  work and built on nowhere. The reading names the two measurements that would
  produce a practice — both cheap, neither run.
- **`ARXIV-2204.00300` passed over with a reason.** RNA-FM ranked next by
  dwell time. Unlike `2504.06209`, the eighteen topics *can* express its
  general claim — self-supervised pretraining on a large unannotated corpus
  transfers when labels are scarce — and that is exactly the problem: the
  claim is foundational, the record already carries it across 80 practices
  that touch pretraining, and this would add an instance rather than evidence
  (`DP-005`). Its actual trunk is also absent: the corpus holds no protein or
  biological sequence models at all, so filing the RNA descendant would repeat
  the mistake [#243](https://github.com/dmarx/anthology-of-the-sota/issues/243) was just opened about. Whether this record wants a
  biological-sequence trunk is a scope question for its owner, not one to
  settle by filing.

### Added

- **`LIT-494`** — *GaussianToken: An Effective Image Tokenizer with 2D
  Gaussian Splatting* (Dong et al., 2025), read as `NOTE-243`. Replaces
  the fixed grid of a VQ tokenizer with `K` 2D Gaussians that learn their own
  position, rotation and scale. **No practice filed.**

### Documentation

- **The idea is good and the evidence cannot isolate it.** Only the feature
  coefficient is quantized; position, rotation and scale stay continuous and
  ride alongside the index. So each token is roughly 10 bits of codebook plus
  five floats — another 80 bits at fp16 — where every baseline's token is the
  index alone. The comparisons are matched on token **count**, which the paper
  states plainly, and bits per image is computed nowhere for either side. How
  much of rFID 1.61 against LlamaGen's 2.19 is the moving support and how much
  is the side-channel is not identifiable from what is reported, and that is
  the whole reason no recommendation follows.
- **The motivation is not met by the artifact.** The opening argument is that
  images need *discrete* tokens to align with text for autoregressive models.
  What comes out is, in §3.4's own word, **semi-discrete** — and a token that
  is an index plus five floats is not something a language model consumes.
  That word does not reach the abstract.
- **What is measured and what is argued are cleanly separated, to the paper's
  credit.** There are no generation experiments, no multimodal experiments and
  no downstream task, and the paper says so in §3.4 and again under
  Limitations. The §3.4 argument that the representation is better for
  generation is therefore argument — and its combinatorics is written
  backwards: an `h × w` index matrix over an `N`-entry codebook has `N^(h×w)`
  states, not `(h × w)^N`.
- **Three internal inconsistencies on the headline, recorded for the next
  reader.** §4.2 fixes the CIFAR embedding dimension at 4 and the ImageNet
  codebook at 2048, where Table 1 shows **3** and **1024**; §4.3 reports the
  ImageNet result as **1.67** where Table 1 says **1.61**; and §4.3's "14.01
  rFID better than VQGAN at dimension 4" matches neither Table 1's 14.06 at
  dimension 3 nor Table 2's dimension-4 row at 13.11.
- **The most useful thing the reading found is an absence.** Table 1's
  baselines — VQ-VAE, VQGAN, MaskGIT, LlamaGen — are none of them in this
  record. `SOTA-187` is the nearest practice and its latent is continuous, so
  the corpus holds nothing about discrete image tokenization for a descendant
  to attach to. The `LIT` note wants `compared_against` on three papers and
  can declare none. Filed as [#243](https://github.com/dmarx/anthology-of-the-sota/issues/243); same shape as the TinyStories gap,
  and invisible to every instrument for the same reason (`DP-004`).

### Added

- **`LIT-493`** — *Language Modeling by Language Models* (Cheng, Clark
  and Richardson, 2025), read as `NOTE-242`. The largest automated
  architecture-discovery experiment published: 1,062 designs verified by real
  pretraining at 14M–350M parameters, every artifact public.
- **`SOTA-304`** — generate a long program unit by unit, freezing each
  unit that passes an execution-based check, instead of regenerating the whole
  artifact on failure. `Proposed`.

### Documentation

- **The filed practice is not the paper's headline.** On 100 held-out
  proposals, the same model produced valid implementations **92%** of the time
  generating unit-by-unit against an execution-based checker and **6%** of the
  time one-shot with retries — and the one-shot outputs were trivial besides,
  49 lines of function body against 181, where the human reference library
  averages 220. The mechanism is stated and is not about architectures:
  one-shot needs `E[calls] = 1/p` for the whole artifact to be simultaneously
  valid, and freezing validated units turns one joint probability into a
  product of local ones.
- **The internal ordering is the useful part.** Removing the symbolic checker
  costs **62 points** of validity; removing the unit-wise decomposition costs
  **19**. The decomposition is the interesting idea and the checker is the
  boring one, and the boring one is the bigger lever. Two of the loop's agents
  — planner and observer — moved the measured quantity by one and three points
  respectively, which is recorded as a condition rather than omitted.
- **What the record declines to file is the discovery result.** "Outperform
  GPT2, Mamba2, etc., on 6/9 common benchmarks" is true as worded and is a
  maximum over the five best of 1,062 designs. On the average column the best
  discovered design beats the best seed by **0.03 points**, and the five
  discovered designs average **60.17** against their seeds' **60.77** — they
  are, on aggregate, slightly worse than the architectures they were bred
  from. The `LIT` note carries this; no practice rests on it.
- **The paper supplies the instrument that checks its own headline.** Table 16
  publishes the per-benchmark standard deviation across every verified design
  — 0.0138 on CoLA and SST2 — against Table 5 margins of half a point to two
  and a half. It also states that the nine evaluation benchmarks were selected
  from that same table by largest spread and by the best design beating random
  by over 5%, which means the final comparison is not held out of the fitness
  function. All of that is the paper's own reporting, and the record's reading
  uses it rather than disputing it.
- **`ARXIV-2504.06209` passed over with a reason.** *The Work Capacity of
  Channels with Memory* ranks next on revisits (8 sessions) and is an
  information-thermodynamic result about percept-action loops — bounds on
  extractable work, and a trade-off between prediction and forgetting. Under
  [ADR-026](record/decisions.d/ADR-026.md) the test is whether the eighteen topics can express the claim, and
  none of them can. Same disposition as `2510.20520`.

### Added

- **`LIT-492`** — *The unintended consequences of large language models
  as a labor-augmenting technology in science* (Duede, Gross, Crockett and
  Bergstrom, 2026), read as `NOTE-241`. Charnov's marginal value theorem
  applied to research effort, with the acceleration split into three phases.
- **`SOTA-303`** — name the phase a time-saving tool accelerates before
  predicting what it will do to the quality of what people produce with it.
  `Proposed`.
- **`THEORY-055`** — a producer's own rate of return is the price of
  their time, so making them faster raises the bar on every marginal hour of
  improvement. `Proposed`.

### Documentation

- **A mechanism for something the record had only observed.** `THEORY-051`
  named three candidate explanations for `LIT-487`'s finding that an AI
  drafting tool improved petition text on every feature while outcomes stayed
  flat or fell. One of them — diminished author effort — had no account behind
  it. This supplies one, and supplies it without needing the tool to be bad:
  the model stipulates a *perfect* assistant, faster with no added error and
  no cost, and derives the consequence from speed alone.
- **The result is a sign that depends on the phase, not a direction.**
  Accelerating the work done *before* an item's value is known makes producers
  **more** selective and each item less developed. Accelerating the fixed
  minimum needed to ship makes them **less** selective and each item less
  developed — opposite signs on the first quantity, from the same tool acting
  one step later. Accelerating discretionary improvement itself raises
  thoroughness. That third case is what makes the account worth filing rather
  than replacing with "tools make people sloppy".
- **Both new documents are `Proposed`, and the reason is the same one.** There
  are no measurements in the source. Every proposition is proved and none is
  tested, and the propositions concern a stylized producer maximizing a
  long-run rate with static institutions and independently-valued projects.
  The `promote_when` on the practice asks for two deployments with different
  phases whose selectivity moves in opposite directions, because that is the
  prediction no rival story makes; the theory's asks specifically for a case
  where thoroughness goes **up**.
- **No relation was declared between this paper and `LIT-487`.** The
  connection is real and is stated in prose in three places, but
  `compared_against` means somebody ran the comparison and `extends` means one
  work builds on the other, and neither happened — the two papers were written
  independently and do not cite each other. The mapping of a petition drafting
  tool onto this model's minimum-to-ship phase is this record's reading, and
  it is labelled as one.
- **The paper's most quotable sentence is the one its own proof contradicts.**
  "Impelling us to do more, less well" closes the discussion and is echoed
  unqualified in the abstract; Proposition 12 proves the opposite for one of
  the three channels, and §3 says so plainly. `DP-010` in both directions
  inside a single paper, which is what its v2 instruction was added to catch.

### Fixed

- **Two stale temp codes in the `LIT-489` fragments.** The changelog and
  curation entries written with that filing named it by the temporary
  code it carried on the branch, and CI's concretization does not reach
  inside backticks. The lint reports these as "citations in a concretized
  code's old spelling" and `luria link --fix` cannot upgrade them for the
  same reason, so they were rewritten by hand. Backticking a code keeps it
  out of the relative-link warning class and also keeps it out of the
  fixer's reach; worth knowing before the next fragment.

### Added

- **`LIT-491`** — Noise Hypernetworks (Eyring et al., 2025), read as
  `NOTE-240`. Train a LoRA hypernetwork once to predict an improved
  initial noise for a frozen step-distilled generator, instead of running
  reward-guided noise optimization per sample.
- **`SOTA-302`** — steer a distilled generator by modulating its input
  noise, not by fine-tuning its weights. `Proposed`.
- **`THEORY-054`** — the regularizer that is intractable in data space is
  tractable in noise space, and bounds the data-space divergence.
  `Proposed`.

### Documentation

- **The record can now state a trade from both sides.** `SOTA-301` was filed
  earlier today as the inference-time route — steer the sampler with a
  correctly-ordered gradient step, no training, cost on every sample. This is
  the amortized route: one training run, **0.1 s** of added latency, about
  **half** the gain. Neither dominates, and a corpus holding only one of them
  can state a practice but not a decision. Declared `compared_against`.
- **The load-bearing evidence is a control, not the headline.** Direct LoRA
  reward fine-tuning of the same model against the same reward does not
  merely underperform — it **degrades the base model**: GenEval 0.70 → 0.67
  at one step, 0.72 → 0.66 at two, **0.73 → 0.62** at four, and 0.59 at
  adapter rank 8. Noise modulation on the same budget gives 0.75 / 0.76 /
  0.77. That comparison is what makes this a recommendation about *where*
  adaptation belongs rather than one more alignment method, and the
  `promote_when` asks for it specifically because it is the half most likely
  to be dropped.
- **Why weight-space fails has a stated mechanism.** Aligning to a reward
  means learning a tilted distribution, and the term that keeps it near the
  base model is a KL requiring a Jacobian determinant through the generator —
  intractable for a distilled model. So weight-space fine-tuning optimizes the
  reward with a broken anchor. Posed over the input noise the same KL becomes
  an `L2` penalty, and the data processing inequality makes it an upper bound
  on the divergence that was wanted.
- **`THEORY-054` is `Proposed` because an upper bound is not a
  measurement of what it bounds.** The DPI gives the direction and nothing
  about tightness; a sharply contracting one-step generator could make the
  noise-space KL large while the data-space KL is near zero. And the Lipschitz
  condition the approximation needs is *engineered* — zero initialization
  makes it true at step 0 — rather than verified during training.
- **The paper's restraint is worth recording.** Its own summary is "about half
  of the performance gains achieved by ReNO", which matches the arithmetic
  (0.05 of 0.11 on SANA-Sprint). One phrase runs ahead of its table — "nearly
  recovers most of the improvements" for SD-Turbo, where 0.57 against a
  0.49→0.63 range is about 57% — and the note says so.

### Added

- **`LIT-490`** — Denoising as Projection (Zhang et al., 2026), read as
  `NOTE-239`. Standard gradient guidance adds the objective gradient
  *after* the denoising step; apply it *before* and the denoiser acts as an
  approximate projection, making the reverse process an inexact
  projected-gradient method.
- **`SOTA-301`** — apply the objective gradient before the denoiser, not
  after it, when guiding diffusion toward a task objective. `Proposed`.
- **`THEORY-053`** — the Stein posterior-mean denoiser acts as an
  approximate projection onto the learned data geometry. `Proposed`.

### Documentation

- **The record's diffusion line gains its missing case.** `SOTA-266` covers
  the interpolant and timestep distribution, `SOTA-203` the solver,
  `SOTA-187` the latent — all training or plain sampling. None covered
  steering a pretrained sampler toward an external objective, which is where
  diffusion meets planning and control.
- **The benefit is not "better objective values", and saying so straight is
  the point of the practice.** In trajectory tracking, the standard ordering
  produces plans that follow the reference closely and **loses much of that
  advantage once the controls are executed through the true dynamics**. The
  new ordering's planned and executed trajectories nearly coincide. A
  practitioner comparing the two on planned cost — the obvious comparison —
  would pick the worse method.
- **That is the third paper in this session whose real finding is that the
  metric measured the wrong object**, after `LIT-487` (text features stopped
  predicting petition outcomes) and `LIT-489` (next-token loss is not
  computation). Different subfields, no shared authors, same shape.
- **`THEORY-053` is `Proposed` despite having proofs.** The theorems
  assume an *exact* Stein posterior-mean denoiser and a learned support that
  faithfully represents the feasible set; what anyone runs is a trained
  approximation on a model that may put mass off the feasible set. The
  authors name misspecification as future work, and that gap is the whole
  distance between the theorem and the deployment. The setting is also narrow
  — deterministic DDIM, variance-exploding, exponentially decaying schedule.
- **The most citable arm is the weakest.** D4RL/MuJoCo gives "slightly
  higher" normalized returns — the authors' word — on three tasks against one
  baseline. The unicycle study is the better evidence and will travel less
  far, so the practice says which is which.
- **Effect sizes were not verified in this reading.** The comparison tables
  did not survive text extraction from the HTML rendering, so the note and
  practice quote directions and the authors' own qualifiers, and say so
  rather than implying magnitudes that were not read.

### Added

- **`LIT-489`** — Measuring In-Context Computation Complexity via Hidden
  State Prediction (Herrmann, Csordás and Schmidhuber, 2025), read as
  `NOTE-238`. Insert a variational bottleneck with a **learned
  autoregressive prior** mid-network; the posterior-prior KL is the nats of
  hidden-state information the past did not predict.
- **`SOTA-300`** — to tell whether a model is doing non-trivial
  in-context computation, measure how well it predicts its own hidden states,
  not its next-token loss. `Proposed`.

### Documentation

- **The diagnosis is the contribution and it is exact.** Next-token loss
  conflates difficulty with computation at *both* ends: uniform noise
  maximizes it and requires nothing, a memorized licence minimizes it and
  requires nothing either. The interesting cases land in the middle, where an
  intermediate loss is indistinguishable from a mixture of trivial and
  impossible tokens.
- **The practice rests on the automaton half, not the LLM half.** Which of
  five text types counts as "interesting" is the authors' judgement, so the
  metric agreeing with it is suggestive and close to circular. The
  probative result is §3.1.2: bin tokens by next-token loss, stratify by the
  **analytically computed** description length of the generating automaton,
  and higher complexity gives higher PHi loss in every bin. The promotion
  condition asks for an external complexity ground truth for that reason.
- **The reasoning-selection result is deliberately not filed as a practice.**
  "Solutions with high PHi loss have a significantly increased chance of
  being correct" is the quotable sentence and it is true. In §3.2.3 the paper
  states that **choosing by lower next-token loss alone already scores 71%**
  on the same GSM-8K pairs, and gives no standalone number for PHi. What is
  demonstrated is incremental value under partial correlation plus an
  adversarial subset where the baseline is wrong by construction. The
  practice carries this as a condition — *this measures, it does not select*
  — rather than the record closing the gap silently.
- **Posterior collapse is located and is the detail that saves a first
  attempt.** Early-layer insertion degrades next-token loss badly and drives
  the metric to nearly zero, which reads as "no computation" and means
  "instrument broken". Layers 18–24 of a 3B Llama are the usable band, found
  by sweeping.
- **No tension with `SOTA-101`.** Perplexity filtering ranks documents by
  typicality, which is a different job for the same number. The claim here is
  bounded to asking what computation a model is doing.

### Added

- **`LIT-488`** — gen2seg (Khangaonkar and Pirsiavash, 2025), read as
  `NOTE-237`. Finetune Stable Diffusion or MAE end-to-end — encoder
  *and* decoder — for category-agnostic instance segmentation on **indoor
  furnishings and cars only**, and the model segments people, animals, x-rays
  and impressionist paintings. Declared `compared_against: LIT-096` (SAM).
- **`SOTA-299`** — finetune the whole generative model, encoder and
  decoder, for a dense perception task instead of attaching a head to a
  backbone. `Proposed`.
- **`THEORY-052`** — synthesis requires equivariant representations and
  discriminative pretraining rewards invariant ones. `Proposed`.

### Documentation

- **The controls are the practice, not the headline.** "Narrow finetuning
  generalizes broadly" would be one more transfer result; what makes it a
  recommendation is `SimpleClick` — the **same MAE-B backbone**, the **same
  finetuning data**, a conventional promptable-segmenter head — scoring
  **1.4–2.4 mIoU on every one of seven splits**. That is not degradation, it
  is absence, and it isolates the freshly-initialized head as the component
  that cannot generalize. A second control narrows it: discriminative
  features under the generative decoder (DINO-B + frozen SD VAE) reach 14.9
  against MAE-B's 21.6, so the decoder recovers part of the gap and the
  encoder's prior is the rest.
- **Three ablations remove three rival explanations.** Pretraining scale:
  MAE on **unlabeled ImageNet-1K alone** generalizes to art and x-rays.
  Category diversity: ten Hypersim classes match the full thirty-three.
  Label cleanliness: finetuning on COCO's coarse polygonal masks loses
  **under 5 edge-AP points** — a model trained on polygons does not predict
  polygons.
- **"Approaches SAM" is an aggregate that hides a failure mode.** COCO-Large
  57.6 vs 57.0 and iShape **51.4 vs 16.8**, but COCO-Small **8.5 vs 56.9**.
  The practice carries the small-object loss in its Conditions rather than
  the headline, and notes the authors offer two causes for it — pretraining
  bias and a quarter of SAM's finetuning resolution — and separate neither.
- **`SOTA-186` now has a counterweight rather than a rival.** SAM's answer to
  category-agnostic segmentation is to bootstrap 1.1B masks with a data
  engine; this reaches most of the same place on **3.7M masks and four GPUs**
  and loses on small objects. Neither refutes the other, and the trade now
  has numbers on both sides, which is what makes it a decision somebody can
  take.
- **`THEORY-052` is `Proposed` because at least three rival accounts
  predict the same ranking.** Low-level detail retention, output resolution
  and capacity each order the models identically to the
  equivariance/invariance story, and nothing in the paper measures
  equivariance directly. The authors write "we hypothesize" twice in a
  paragraph; the promotion condition asks for a representation-level test.

### Changed

- **`DP-010` v2 — four more instances, counted separately and chosen for
  unrelated reasons.** The principle was filed on four papers from one week.
  These are the next four read end to end off the `#180` revisit ranking, and
  every one has the shape: `LIT-483` (55.8% of the FLOPs, FLOP-matched and not
  memory-matched), `LIT-485` ("improved sample efficiency" from a three-way
  confounded comparison, while the one clean arm is about tokenizers),
  `LIT-486` (a scaling *law* whose exponent was fitted after looking at the
  curve, over a term the paper never measures), `LIT-487` (the inverse case).
  Eight papers across two independently-chosen batches is the difference
  between a pattern and four anecdotes, which is `DP-009`'s test applied to
  `DP-010` itself.
- **`DP-010` gains an instruction, because `LIT-487` is the case the first
  version could not have caught.** There the load-bearing sentence is real,
  checked, and given one line in an appendix — the finding that the text
  features stopped predicting outcomes, which is the whole reason the paper's
  null means anything. A reading that only guards against overclaiming files
  the abstract and loses it. So: **look for the underreported sentence too**,
  and ask which sentence is doing the work rather than whether the headline is
  supported.
- **The principle's diagnosis is sharpened.** The failure is not that authors
  overclaim — in all eight cases the hedge is present and the authors are
  honest. It is that **compression is not selective for evidence in either
  direction**: it promotes the memorable unsupported sentence and demotes the
  unmemorable load-bearing one.

### Removed

- **A stale acknowledgement directive on `THEORY-048`.** It vouched for citing
  `SOTA-291` while `Proposed`; `#233` made that practice `Active`, so the
  directive stopped governing anything and became a finding on the same
  report it was filed to quiet. The report notices both directions, which is
  the design working.

### Documentation

- **`#234` filed rather than answered.** The record now holds two descriptions
  of a text distribution narrowing — `SOTA-172` and `SOTA-295` on generated
  corpora, diagnosed by n-gram over-concentration, and `SOTA-298`/`THEORY-051`
  on text people wrote holding a tool, diagnosed by embedding similarity.
  Whether these are one phenomenon or two is a measurement nobody has run
  (both instruments on both corpora), and writing the `THEORY` now would be
  precisely the `DP-010` failure this session spent four units documenting in
  other people's work. The question is recorded; the answer is not asserted.

### Added

- **`LIT-487`** — Introducing AI to an Online Petition Platform Changed
  Outputs but not Outcomes (Corpus et al., 2025), read as `NOTE-236`.
  Change.org's "write with AI" tool reached three countries eleven weeks
  before a fourth; across 1.5M petitions, access made petitions **49% longer**,
  more lexically varied, 1.5 reading grades harder, and rated higher by human
  judges on quality (d = 0.96) and persuasiveness (d = 0.86) — while the share
  reaching ten signatures fell **5.33 points** and inter-petition similarity
  rose **23%**.
- **`SOTA-298`** — measure a writing assistant by the outcome it was
  deployed to improve, not by the text features that used to predict it.
  `Proposed`.
- **`THEORY-051`** — a text feature predicts success partly by being
  uncommon, so a tool that gives it to everyone destroys its predictive value.
  `Proposed`.

### Changed

- **`SOTA-291` promoted to `Active`, v2** — "evaluate a specific intervention
  on a specific affordance rather than the net effect of the system". Its
  condition asked for a specific-affordance evaluation run at collective scale
  **with the group-level outcome actually measured**, and called the gap small
  and nameable. `LIT-487` is that evaluation, by a different group on a
  different platform, and the authors reach the design from this practice's own
  reasoning independently — they decline individual-level estimates because an
  interconnected platform biases them. `consensus` `unreplicated` → `emerging`,
  not `converged`: one worked example is not a method the field runs, and the
  two documents *arguing* for the programme still share a first author.

### Documentation

- **The finding with the longest reach is in an appendix.** The three lexical
  features were chosen *because* they predicted petition outcomes before the
  tool existed; afterwards, their predictive strength — and that of rated
  quality and persuasiveness — **weakened or reversed**. That single
  reported-once sentence is what makes this a general lesson rather than a
  fact about petitions, and it is not in the abstract and was not
  preregistered.
- **The result is not "AI writing is bad".** Independent raters scored the
  AI-access petitions markedly better on quality and persuasiveness. Without
  that arm, the outcome null would be explained by the tool being poor. The
  text improved and it did not help, which is stranger and more useful.
- **Three mechanisms, none tested, and two of them predict the same null.**
  Thin substance; reader suspicion of AI-styled text; diminished author
  ownership reducing the off-platform promotion that actually drives petition
  success. `THEORY-051` is `Proposed` for exactly this reason, and
  `SOTA-298` is written not to depend on which is right.
- **The within-writer analysis reads stronger than it is.** Repeat writers'
  second petitions did worse in every cohort, and the *largest* decline
  (OR = 0.662) was among writers who had AI access for **both** petitions —
  so "gaining access" is not the variable, the three confidence intervals
  overlap heavily, and the authors' own regression-to-the-mean caveat covers
  it. Recorded as a consistency check that failed to contradict the main
  result, not as individual-level confirmation.
- **Treatment defined as access, not use**, because AI detection is
  unreliable — an intention-to-treat design that needs no detector to be
  valid, at the cost of dilution by the adoption rate (their classifier puts
  it above half). Carried into `SOTA-298` as the corollary about how to
  test your own tool.
- **`SOTA-292` applied rather than cited.** The industry-ties check was run
  against this paper and comes out clean: academic authors, publicly
  accessible data, launch dates confirmed with platform staff, and a
  conclusion unflattering to the platform.
- **A human-in-the-loop case beside the synthetic-data line.** `SOTA-172` and
  `SOTA-295` concern generated corpora collapsing toward themselves, measured
  by n-gram over-concentration. This is the same collapse measured by
  embedding similarity, in text written by **people holding a tool** — a
  different causal path to the same statistical place.

### Added

- **`LIT-486`** — Parallel Scaling Law for Language Models (Chen et al.,
  2025), read as `NOTE-235`. Run the same weights over `P`
  learnably-prefixed copies of the input and learn the aggregation: loss falls
  as if parameters had grown by `O(log P)`, fitted across 0.5B–4.4B and
  `P = 1…8` on two corpora.
- **`SOTA-297`** — scale parallel computation with learnable input
  transforms, not parameters, when inference memory is the binding
  constraint. `Proposed`. At batch size 1 a 1.6B model at `P = 8` costs
  **22× less added memory and 6× less added latency** than the parameter
  scaling that matches it.
- **`SOTA-296`** — add the parallel streams in a short final training
  stage, not from the start. `Proposed`. 1T tokens plain, then **20B (2%)**
  with streams on; the stage-2 loss spike recovers within 0.0002T tokens.
  This is what makes the first practice affordable, since parallel scaling
  costs `P`× the training FLOPs.
- **`THEORY-050`** — parameters carry memorization and parallel
  computation carries reasoning. `Proposed`.

### Documentation

- **The condition is in the practice's title on purpose.** This wins when
  decoding is memory-bound, which is small-batch and edge serving; as batch
  size rises decoding becomes compute-bound and the advantage narrows. The
  paper sweeps batch sizes 1–8 and shows where it stops, rather than quoting
  the best case alone, and the practice carries that boundary rather than the
  headline.
- **The cost analysis is denominated in memory and latency rather than
  FLOPs**, on the argument that decode is memory-bound and FLOPs mis-rank it
  — flash attention spends more FLOPs for less latency. Recorded inside
  `SOTA-297` rather than as its own practice: the argument is good and
  no experiment in the paper isolates it.
- **A scaling *law* that is a fit.** The theoretical result says the
  parameter multiplier depends on the diversity between streams; `log P` was
  chosen because the measured gains from 1→2, 2→4 and 4→8 were about equal,
  and diversity is never measured. The theory permits anything from
  logarithmic to a power law. What is established is a fit over `P ≤ 8`, and
  a logarithm is the shape that most flatters the extrapolation nobody ran.
- **The load-bearing ablation is in an appendix.** Several input
  transformations and aggregation rules "minimally affect model performance;
  the significant factor is the number of computations". Without that, this
  is a paper about prefix tuning; with it, it is a paper about computation.
- **`THEORY-050` is `Proposed` for a reason worth stating.** Two
  independent measurements agree — the fitted coefficient (0.39 on
  Stack-V2-Python, 0.33 on the Pile) and the downstream asymmetry (1.6B at
  `P = 8` matches 4.4B on code, 2.8B on general tasks) — and two corpora are
  not a variable. Stack-V2 is also narrower, more repetitive and more
  structured, any of which could raise the return on ensemble diversity with
  nothing to do with reasoning. The authors call it "an intuitive conjecture";
  it is the sentence most likely to be cited as a finding, which is `DP-010`'s
  shape.

### Added

- **`LIT-484`** — TinyStories (Eldan and Li, 2023), read as
  `NOTE-233`. The trunk the record was eight `tiny-models` practices
  deep into without holding. Its result is a separation, not a record: hold
  the architecture, shrink the corpus's breadth, and models **below 10M
  parameters** — or with a **single transformer block** — produce fluent
  English. What stopped them was what they were asked to learn.
- **`LIT-485`** — SimpleStories (Finke et al., 2025), read as
  `NOTE-234`. `extends` the trunk. **59.38%** of TinyStories contains
  "once upon a time" verbatim; the diversity mechanism was lexical and the
  repetition is in the frame.
- **`SOTA-295`** — parameterize the generating prompt above the word
  list, and constrain how each sample opens. `Proposed`. Five diversity
  instruments agree and judged simplicity does not move, which is the null
  that makes the rest mean anything.
- **`SOTA-294`** — fit the tokenizer to the corpus when the corpus is
  deliberately narrow. `Proposed`. A 4,096-token vocabulary seeded with
  English affixes beats GPT-2's 50,257 by **+26.7 coherence** and **+27.5
  quality** with data and architecture held — the one fully controlled
  comparison in a paper that is mostly about something else.
- **`SOTA-293`** — count embedding parameters when you report a tiny
  model's size. `Proposed`, `consensus: unassessed`. TinyStories-33M is 68M
  all-in, and the same architecture on the same data is 65M or 35M depending
  only on the tokenizer.

### Changed

- **`LIT-483` gains `generative-modeling`.** Mixture-of-Transformers'
  Transfusion arm trains images by diffusion and its headline small-model
  result is an image-generation one. The tag was missing and its absence is
  what left the `LIT-447 → LIT-448 → LIT-449 → LIT-483` lineage line unbound
  when `#230` extended it. `ADR-049`'s intended answer, taken: the relation
  was right and the vocabulary entry was true and unwritten.

### Documentation

- **ar5iv serves v1 and the arXiv API serves the latest.** SimpleStories' v1
  says "we seek to train a suite of small language models" in the future
  tense; v3 has the suite, the ablations and a different author list. A
  reading built from the rendered HTML and an abstract fetched separately
  would have attributed v3's claims to v1's evidence. Read the version you
  quote.
- **The headline comparison in `LIT-485` is confounded three ways and
  the practices filed from it avoid it.** Dataset, tokenizer and architecture
  all differ between the SimpleStories models and TinyStories-33M, so
  "improved sample efficiency compared to the TinyStories dataset" is not a
  measurement of the dataset. `SOTA-295` rests on the corpus metrics,
  which are direct; `SOTA-294` rests on the tokenizer ablation, which is
  clean. Neither rests on the abstract.
- **`SOTA-172` and `SOTA-295` agree about the disease and disagree about
  the cure**, and that is recorded rather than resolved. `SOTA-172`'s
  mechanism for why generated corpora hurt is over-concentration of n-gram
  features; this is a measurement of n-gram over-concentration in a generated
  corpus, on a different corpus by a different group. The remedies point
  opposite ways because they address different jobs — standing in for real
  text, versus deliberately excluding it — and `SOTA-172`'s own
  `promote_when` already says a better generator would not move it.
- **TinyStories does not satisfy `SOTA-125`'s promotion condition**, which is
  worth saying because the words match and the measurements do not. That
  practice trades depth against MLP width in a hybrid at 90M; this sweeps
  depth against embedding dimension in pure-attention GPT-Neo at 1–35M, with
  no SSM state to trade against.

### Added

- **`LIT-483`** — Mixture-of-Transformers (Liang et al., 2024). Untie
  every non-embedding parameter by modality and keep self-attention global.
  Dense-baseline performance at **55.8% of the FLOPs** in the Chameleon
  setting, **37.2%** with speech, about a third in the Transfusion setting,
  and a 760M model beating a 1.4B dense one. Read as `NOTE-232`.
- **`THEORY-049`** — modalities compete for the same feed-forward
  parameters, the competition is not symmetric between them, and that is
  where separating by modality pays. `Proposed`: the contention is inferred
  from the benefit of relieving it, never measured.

### Changed

- **`SOTA-262` promoted to `Active`, v2** — "give each modality its own
  weights and let the streams attend jointly". Its `promote_when` asked for a
  second group reporting per-modality weights against a shared-weight backbone
  at matched compute; this is a different lab, a different family of model,
  and FLOPs held identical to the dense baseline across three settings and two
  baselines. `consensus` goes `unreplicated` → `emerging`.
- **The practice now says *which* weights to untie, and in what order** —
  feed-forward first, `Q`/`K`/`V` and output projections second, layer norms
  not at all. That ordering is what the second source adds beyond the
  replication, and the one-source version of the practice could not state it.
- **`LIT-449` gains `multimodal-learning`.** MMDiT is where the record's
  multimodal-architecture line starts and the tag postdates the note.

### Removed

- **Two acknowledgement directives for `SOTA-262`**, on `LIT-449` and
  `ADR-052`. Both vouched for citing it while `Proposed`; it no longer is.

### Documentation

- **The promotion condition had two satisfiers and only one is met.** No arm
  of either paper varies the attention — every variant attends globally — so
  what two independent groups now agree on is a *bundle* nobody has taken
  apart. Recorded in the practice's Conditions as a standing gap rather than
  as grounds for withholding it, and the distinction is the reason the
  `history:` entry says so explicitly.
- **FLOP-matched is not memory-matched.** A sparse architecture at identical
  FLOPs holds more total parameters than the dense baseline it matches. The
  second source's headline ratio is a compute claim and the practice's
  Conditions now separate the two budgets.
- **"Layer norms do not matter" is the short and wrong version.** The
  negligible result is about untying layer norms *given* the other two
  untyings; the authors say plainly it establishes nothing about untying them
  alone, and both the practice and the theory carry the caveat.

### Added

- **Moving towards informative and actionable social media research**
  (`LIT-482` / `NOTE-230`), Bak-Coleman, Lewandowsky,
  Lorenz-Spreen, Narayanan, Orben and Oswald (2025).
- **Industry Influence in High-Profile Social Media Research**
  (`LIT-481` / `NOTE-231`), Bak-Coleman, West, O'Connor and
  Bergstrom (2026).
- **`THEORY-048`** — randomizing individuals estimates an individual
  quantity, and when the units interact the collective effect is not the sum
  of it. `Active`.
- **`SOTA-291`** — evaluate a specific intervention on a specific
  affordance rather than the net effect, and never read an individual-level
  null as the absence of a collective effect. `Proposed`.
- **`SOTA-292`** — check industry ties yourself; disclosure is unreliable
  and the ties are mechanically detectable. `Proposed`.

### Documentation

- **The argument is not about social media and the record should not file it
  as though it were.** It concerns randomizing interacting units and asking
  about an aggregate, which is the shape of every deployed recommender,
  ranking system and assistant at population scale.
- **The power grid, run twice, is the whole case.** Randomize substations to
  demand spikes: treat a small share and the grid absorbs it, no difference
  between arms; treat a large enough share and the grid fails, blacking out
  **the controls too**, again no difference. The same null appears from either
  side of a real effect, because the estimated quantity was never the
  estimand.
- **Four separable reasons, and two of them are structural.** Non-linearity
  across scale; **hysteresis**, which is the objection to *every withdrawal
  design* because removal is not the inverse of addition; feedback in time,
  under which two-week smoking cessation would establish smoking as a way to
  lose weight; and **SUTVA violation**, since assigning someone a chronological
  feed still leaves their neighbours passing them ranked content. Escaping the
  last needs whole subnetworks randomized, and **no trial in the literature
  does**. Neither of those two is fixable with a larger sample.
- **The symmetry matters.** A null from this design is equally *not* evidence
  that the effects are real. The claim bounds what the design can conclude,
  in both directions, and a reader who takes it as "those studies were wrong"
  has taken more than it says.
- **The positive half is argued, not demonstrated**, and the missing step is
  small and nameable: the source notes two large platform studies that tested
  realistic ranking interventions and **did not assess collective outcomes at
  the group level**.
- **49% of high-profile papers in this field have an industry tie and most go
  undisclosed** — but the number that reframes it is **21% of authors**. Half
  the output, a fifth of the people: a small group with durable relationships,
  not a field broadly engaged, and a different problem with a different fix.
  The same detection finds undisclosed ties among **editors and reviewers**.
- **The two halves fit, and share a first author.** Ties are over-abundant in
  the cluster about *what users share* and **sparse in the platform-dynamics
  cluster** — which is exactly where the methodology paper says the effects
  live. Correlational, and its authors say so. Filed as one position argued
  twice rather than two groups agreeing, and both consensus notes say so.
- **The 49% is a floor, not an estimate.** Detection requires a public trace,
  so undetected ties push it down. A headline number that is the conservative
  one is rare enough to be worth naming.
- **`DP-005` read in the direction it is least often used.** The corpus reaches
  745 policy documents at 180 citations a paper. Being well-adopted is what
  makes a body of work worth auditing, not a reason to trust it.
- **And this record has not run the check on itself.** The method is
  mechanical and the corpus construction reusable; `SOTA-292`'s promotion
  condition asks for the measurement somewhere other than social media, and
  the anthology's own sources are the obvious corpus.

### Added

- **Auditing Political Exposure Bias** (`LIT-480` / `NOTE-229`), Ye,
  Luceri and Ferrara (2024). 120 sock-puppet accounts, six weeks, 9.79M tweets
  from Twitter/X's "For You" timeline during the 2024 US presidential
  election. **The first document filed under `deployment-and-society`**, and
  the paper `ADR-052` was measured against.
- **`SOTA-290`** — to measure what a deployed recommender does, use
  sock-puppets that never interact, follow sets curated to your question, and
  exposure weighted by rank. `Proposed`, `unreplicated`.
- **`THEORY-047`** — personalizing a feed concentrates what it shows
  rather than broadening it, and a handful of moderate signals is enough to
  start. `Proposed`.

### Documentation

- **`ADR-052`'s falsifier is answered.** That decision added a topic naming
  nothing and wrote the condition down: *if the first filing produces a
  literature note and nothing actionable, the topic is a shelf rather than a
  category.* It produced a practice and an account. The topic is a category.
- **The durable content is the method, not the finding.** The finding is about
  one platform in a six-week window around one election and will date. The
  design is about measuring any ranking system whose operator will not help
  you, which is the normal case and increasingly so as research APIs are
  withdrawn.
- **The load-bearing decision is that the puppets never interact** — against
  the practice in radicalization studies, and for three stated reasons:
  interaction creates feedback loops so the system's prior cannot be separated
  from what your own behaviour taught it; different arms would engage
  differently, so cross-arm comparison stops being clean; and the question is
  what the system does *before* a user teaches it anything. The cost is
  ecological validity and the source says so.
- **Follow sets are curated to the question rather than to realism**, also
  against prior practice. Real users follow diverse things unrelated to what
  you are measuring, and every one of them is a confound.
- **A raw appearance count is not exposure.** Weight by rank — here an
  exponential decay calibrated so the top 20% of a timeline carries ~70% of
  attention. That calibration is **borrowed from TikTok and YouTube studies**
  and transplanted, every exposure number inherits it, and **no sensitivity
  analysis over the decay is reported**. The practice says to run one.
- **The control arm carries the finding.** Accounts following *nobody* receive
  the **most diverse** recommendations of any group; right-leaning accounts the
  least. Gini above 0.45 in every arm, all pairwise differences at p < 0.001,
  and comparable to published figures of 0.6–0.7 for exposure to one's own
  friends. So on this measurement personalization is a narrowing operation.
- **And the amount of signal required is small**: ten media outlets, seven of
  them moderate, plus four political accounts, with no interaction and no
  history, is enough to amplify aligned voices more than 50% above the
  balanced baseline.
- **Three things the account deliberately does not carry.** It does not claim
  personalization *causes* the concentration — following a set of accounts
  changes both the signal and the candidate pool, and the arm that would
  separate them was not run. It does not say concentration is harmful. And it
  does not rest on the partisan asymmetries, which depend on hand-assigned
  political leanings the authors describe as possibly inaccurate or stale.
- **The baseline arm is not clean, and the source says so about its own
  design**: accounts following nobody still receive trending topics and
  platform defaults, so the arm anchoring the ordering has a known confound.

### Added

- **Two topics, taking the vocabulary from sixteen to eighteen**
  (`ADR-052`). The instrument is `DP-009`'s and the method is
  `ADR-050`'s: count, then read the hits.
- **`multimodal-learning`** — what changes when one model has to take in more
  than one kind of signal: joint architectures and fusion, contrastive
  image-text training, cross-modal transfer, and what a second modality buys
  the first. A **naming gap**, and the same shape `ADR-050` found for
  numerics: `model-architecture`'s blurb ended with "multi-modal designs", a
  trailing clause on a topic about the shape of a network doing duty for a
  subject about how many signals go into it. 9 documents in the record across
  6 topics; 35 more queued at 55 revisits.
- **`deployment-and-society`** — what a system does once it is running among
  people, and how anyone outside it could find out: audits of deployed
  platforms and recommenders, information ecosystems, moderation and
  governance, and the access problems and funding pressures of studying any of
  it from the outside. A **scope extension**, and the only term in the
  vocabulary that named nothing on the day it was added.

### Changed

- **`model-architecture` loses "multi-modal designs"** and gains a boundary:
  "how the network is shaped, not how many signals it takes in." No document
  loses a tag.
- **9 documents retagged**, 4 to `multimodal-learning` as primary (`LIT-071`,
  `LIT-080`, `SOTA-262`, `SOTA-271`) and 5 as a secondary. The primary moved
  only where the document's central claim is about crossing modalities:
  `LIT-072`'s open-vocabulary detection is vision work that happens to use
  text, so it keeps `vision-and-graphics` first.
- **Three stale counts corrected** in `luria.yaml` and `CLAUDE.md`. One of
  them said the primary group was "the thirteen above" when it had been
  fifteen for some time — the second count in that file to have drifted after
  `ADR-050` found "thirteen" where fourteen terms were declared.

### Documentation

- **Six candidates were counted and rejected, and recording them is the point
  of this entry** — the next pass should not re-measure them.
  - **Mechanistic interpretability**: 19 apparent record documents, ~10 real
    after reading ("circuit" and "feature" are used loosely; an
    evolution-strategies paper was among the hits). The survivors sit in
    `analysis-and-evaluation` and `representation-and-encoding`, and **both
    blurbs already name the work**. Two honest homes is not a half-home.
  - **The physics of learning**: 28 record documents, **17 of them already
    primary in `analysis-and-evaluation`** — 61%. By `ADR-050`'s own test, a
    subject the vocabulary can say lands mostly in one topic. This one lands,
    and the instrument working in the negative direction is the reason to
    trust it in the positive.
  - **Safety**: 20 apparent, **about three real** — and five of the false
    positives were inside the quantization cluster, matching "harmful" and
    "misuse" in passing. The purest homonym this exercise produced.
    `ADR-050` already put "safety alignment" into `adaptation-and-tuning`.
  - **Agents and tool use**: 15 incoming, none above two revisits, scattered
    across multi-agent RL, agentic frameworks and model reports.
  - **Graphs and networks**: 16 incoming, and they split — the
    graph-neural-network half is `model-architecture`, and the
    community-detection half makes no claim of a kind this record can express.
  - **Federated learning and privacy** (9 incoming, six of them federated
    learning, which is `distributed-optimization`), **human-AI interaction**
    (8, two or three real) and **scientific domains** (4). All fail on count.
- **Why a topic that names nothing was added anyway.** `DP-009`: a document
  with a real claim and no category has two readings, and declining it is the
  cheaper one, requires no work, and is **self-confirming** — the vocabulary
  keeps looking complete because the evidence that would show otherwise has
  been turned away. The previous eleven contributions each worked down past
  the top of the ranking. `deployment-and-society` is on probation by
  construction, and its first filing follows.

### Added

- **The Diffusion Duality** (`LIT-479` / `NOTE-228`), Sahoo,
  Deschenaux, Gokaslan, Wang, Chiu and Kuleshov (2025). Uniform-state discrete
  diffusion is the `argmax` of a Gaussian diffusion, which makes Gaussian
  training and sampling technique portable to it.
- **`THEORY-046`** — the duality, and why it exists for uniform-state
  diffusion and **not** for masked diffusion. `Active`: both halves are
  derived and one is checked numerically.
- **`SOTA-289`** — when the sampling budget is small, prefer uniform-state
  diffusion with consistency distillation. `Proposed`, `unreplicated`.

### Documentation

- **This does not contest `SOTA-157` or `SOTA-254`.** Masked diffusion is
  ahead on likelihood in the source's own tables — MDLM wins 6 of 7 zero-shot
  datasets and both training corpora. What the paper adds is a **crossover**:
  below roughly 32 function evaluations, distilled uniform-state diffusion
  generates better text than distilled masked diffusion; above it, masked
  diffusion wins. The record previously had no way to say that, because it
  held only one of the two discrete families.
- **The reason the ordering flips is structural.** Masked diffusion unmasks
  many tokens independently and **cannot revise one once emitted**; at a small
  step count that means committing with little context and living with it.
  Uniform-state diffusion is self-correcting. That should survive tuning in a
  way a tuned number would not.
- **The theorem earns under half the headline.** The ablation splits Duo's
  three-point perplexity gain over the previous uniform-state model roughly
  evenly between a Rao-Blackwellized ELBO (~1.7 points) — which has nothing to
  do with the Gaussian connection — and the duality-derived curriculum (~1.3).
  The paper prints this.
- **The training loss is not a valid NELBO** except in the limit, because the
  denoising model consumes a continuous latent while the bound is defined for
  a discrete process. The source says so and evaluates with the proper
  discrete bound. So the theorem justifies the *shape* of the procedure, not
  its status as a likelihood bound.
- **Measure generative perplexity in float64 and report entropy beside it.**
  Masked diffusion models can show misleading Gen PPL with low diversity under
  low-precision sampling — a known artefact the source cites and guards
  against by running every sampling experiment in double precision. It also
  reports entropy: MDLM distilled with SDTT matches an autoregressive model's
  Gen PPL at 5.4 entropy against 5.6. The practice says a comparison run
  without both is not evidence.
- **Use the denoising model, not an EMA copy, as the distillation teacher** —
  against standard practice in consistency models, and ablated.
- **"Beats autoregressive on 3 of 7" is not the headline to carry.** It is
  true, and the comparison is conservative because diffusion perplexities are
  upper bounds. It is also 3 of 7 against a transformer that wins the other
  four by wide margins — 82.05 against 89.35 on PTB, 25.75 against 33.57 on
  Wikitext.
- **MDLM and SEDD are still not in the record**, and arrive here as table
  entries. That is the **third** family this session to enter as somebody
  else's baselines, after backprop-free local learning (via NoProp) and
  weight-space ensembling (via late-phase weights).

### Added

- **Neural networks with late-phase weights** (`LIT-478` /
  `NOTE-227`), von Oswald, Kobayashi, Meulemans, Henning, Grewe and
  Sacramento (2020). An ensemble you never pay for at inference: replicate a
  *small* subset of the weights late in training, share everything else, and
  average the subset back into one model at the end.
- **`SOTA-288`** — the recipe. `Proposed`, `unreplicated`.

### Documentation

- **The record holds nothing on weight-space ensembling** — no Polyak
  averaging, no stochastic weight averaging, no snapshot ensembles, no model
  soups. Several of those appear in this paper only as baselines. This is an
  entry point to the family rather than a summary of it, and **SWA in
  particular is simpler, stronger in places, and still absent**.
- **Three ablations constrain the recommendation more than the headline
  does, and the authors ran all three.**
  - **"Late" is load-bearing.** Running the same procedure from `T₀ = 0`
    *fails to reach the base model* on both CIFAR-10 and CIFAR-100. The copies
    have to stay in one basin for the final average to mean anything;
    perturbing early gives the mode coverage an ordinary ensemble wants and
    this method cannot use.
  - **Replicate a small subset, not everything.** A late-phase *full* deep
    ensemble lands between the base model and the low-dimensional version.
  - **The general version is the one that fails.** Hypernetwork weight
    embeddings score 81.55 on CIFAR-100 against BatchNorm's 82.87 — and under
    SWA reach 82.01 against a base of **82.46**, worse than not doing it.
- **Compare against SWA, and expect the answer to depend on the problem.** On
  CIFAR the two stack: +0.33 and +0.60 points on top of SWA. On the enwik8
  LSTM they mostly overlap — 1.626 BPC for base-plus-SWA against 1.615 for
  late-phase-plus-SWA, where the no-SWA gap was 0.062. Try SWA first.
- **Half the LSTM gain is not the ensemble at all**: adding the rank-1
  multiplicative parameters with no replication moves 1.695 → 1.663;
  late-phase takes it to 1.633.
- **Deep ensembles remain better at `K` times the cost** — 96.91 vs 96.81 on
  CIFAR-10, 84.09 vs 83.06 on CIFAR-100 — and the source uses them as an
  explicit upper baseline rather than a comparison.
- **Dropout loses to doing nothing here** (96.02 vs 96.16, CIFAR-10 WRN
  28-10), which is consistent with `SOTA-240`'s conditional rather than
  against it: a WRN on augmented CIFAR-10 is not obviously in the regime where
  dropout pays.
- **The flat-basin assumption is relied on, not measured.** The perturbative
  initialization is justified by the dense-cluster, low-curvature picture of
  SGD solutions — `SOTA-012`'s subject approached from the constructive side.
  Nothing confirms the copies stayed in one mode; the `T₀ = 0` failure is
  evidence that the assumption matters, not that it holds.

### Added

- **NoProp** (`LIT-477` / `NOTE-226`), Li, Teh and Pascanu (2025).
  Train each block independently to denoise a noisy **label** embedding given
  the raw input — diffusion machinery pointed at a classifier. No forward or
  backward pass across the network at training time.
- **`SOTA-287`** — if you need to train without backpropagation, this is
  the method. `Proposed`, `unreplicated`, and deliberately titled as an answer
  to "which backprop-free method" rather than to "should I use one".

### Documentation

- **The record had no entry in this family at all.** `SOTA-154` (evolution
  strategies) was its only answer to "what if not backpropagation", and that
  is a different family: perturbation-based and black-box where this is local
  and analytic. Forward-forward, target propagation and forward gradients are
  still absent; this is the entry point by revisit count.
- **The interesting number is in the train column and nobody discusses it.**
  NoProp matches backprop on *test* accuracy — MNIST 99.54 vs 99.46, CIFAR-10
  80.54 vs 79.92 — while sitting **8 to 15 points behind on train**: CIFAR-10
  95.0–97.2 against 99.98, CIFAR-100 83.3–90.7 against 98.6–99.2. On these
  datasets backprop is at ceiling on the training set and test scores are set
  by generalization, so the gap is free. Anywhere fitting the training data is
  the binding constraint — which is essentially every setting this record
  covers — it is the whole question. The source raises it nowhere; it is
  recoverable only from the tables.
- **The margin over prior backprop-free methods is not close**: CIFAR-10 test
  accuracy about 80 against 69.32 (local greedy forward gradients) and 50.71
  (difference target propagation); MNIST 99.54 against forward-forward's
  98.63. Memory roughly halves against backprop, and falls four- to
  thirteen-fold against adjoint sensitivity.
- **Use the discrete-time variant.** Continuous-time diffusion is several
  points worse, and **flow matching with one-hot embeddings fails outright on
  CIFAR-100 at 6.38 ± 4.9**. Learned embeddings rescue it to 31.14, still
  well short. "NoProp works" is a claim about one of three variants.
- **The parity claim rests on a structure-matched baseline, which cuts both
  ways.** Building the backprop arm to share NoProp's forward structure is the
  right comparison to have run, and that structure includes a direct
  connection from the input into **every block** — which a conventional stack
  does not have. The authors state the structural difference in §2.1 and note
  that it also makes the comparison against other backprop-free methods
  "challenging", since those do not condition layers on the input.
- **Depth may not be doing what depth usually does.** Every block seeing the
  raw input is what makes independent training possible, and it means the
  layer-wise refinement that motivates deep networks is not obviously
  happening. The paper does not investigate what intermediate blocks
  represent.
- **No limitations section.** The conclusion is a page of positive summary.
  Every caveat above came from the tables or from one sentence in §2.1, which
  is `DP-010`'s shape again and is why the practice carries them explicitly.

### Added

- **Estimating the Probability of Sampling a Trained Neural Network at
  Random** (`LIT-476` / `NOTE-225`), Scherlis and Belrose (2025).
  An estimator for the measure, under the *initialization distribution*, of
  the region around a trained network whose behaviour matches it.
- **`THEORY-045`** — how much of parameter space behaves like your
  trained network is a description length, and the better-generalizing
  network occupies more of it. `Proposed`.
- **`SOTA-286`** — to find a model that generalizes badly where its
  outputs look fine, measure that region. `Proposed`, `unreplicated`.

- **`DP-010`** — the most citable sentence in a paper is often its least
  supported one. `Active`, and filed on four counted instances rather than an
  impression: nGPT's 4–20× with the step-time footnote attached, the coverage
  principle's "somewhat speculatively" about Adam sitting next to a theorem,
  this paper's §3.3, and zero-shot CoT's 17.7 → 78.7 against the wrong
  baseline. `DP-009` says counting is the antidote; this is four.

### Documentation

- **Two choices make this more than rescaled flatness.** Measuring under the
  prior rather than Lebesgue, because some real neighbourhoods turn out to
  have **infinite Lebesgue volume** — so the classical quantity is not always
  defined — and defining the region by *behaviour* (a KL ball on held-out
  inputs, no labels) rather than by loss, which is zero at the anchor and
  compact enough to estimate. The bits-back argument then makes `−log` volume
  a description length outright, rather than a proxy for one.
- **The demonstration is an audit, and it is the part with a clean
  experiment.** A ConvNeXt trained to fail on a held-out poison set while
  keeping training loss low has a measurably smaller local volume than its
  clean twin — detected **on clean held-out data**, where the two behave
  alike, in a small number of forward passes. No poison set, no labels.
- **Measure a converged model, not a run in progress**, and the source's own
  figure is why. The poisoned network has the *larger* volume for most of
  training, crossing below the clean one around 30,000 steps — where
  validation and poison losses diverge. A mid-training reading would have
  pointed the wrong way. So small volume is a property of a badly-generalizing
  *converged model*, not of a badly-generalizing *run*.
- **Do not reach for the Fisher matrix.** Adam's second moment, K-FAC and
  HesScale all precondition the estimator well and similarly; the full Hessian
  of the KL — the theoretically natural choice — does no better than none.
  The authors report this as surprising and cannot explain why axis-aligned
  approximations beat the thing they approximate.
- **Two numerical failure modes, both identified by the authors.** At high KL
  cutoffs the Adam preconditioner returns *smaller* estimates than no
  preconditioning; at very low cutoffs a volume collapse turned out to be
  floating-point failure in the radius-finding binary search rather than a
  finding. Credit for chasing the second down instead of plotting it.
- **The estimator's accuracy against ground truth is unknown**, stated in the
  source's own conclusion, and the aggregate sits close to the largest
  individual sample — the signature of a lower bound of unestablished
  tightness. Comparisons between two models measured the same way are on
  firmer ground than any single number.
- **The adaptive-optimizer argument is not filed as evidence.** §3.3 proposes
  that Adam and Adagrad generalize worse because, as approximations of natural
  gradient descent, they partly undo the architecture's nonuniform
  parameter-to-function map and give up the overrepresentation of simple
  functions — making natural gradient descent a theoretical extreme rather
  than an ideal, with sharpness-aware minimization at the other end. **No
  experiment in the paper touches it.** It is the most quotable idea in a
  paper whose other claims come with figures, and `SOTA-001` gains nothing
  from it.
- **It does not settle `SOTA-012`** (sharpness correlates with test error),
  and is not a restatement of it: volume under a prior and curvature at a
  point are different quantities, and this source itself cites the known
  counterexamples to flat minima generalizing better.
- **Scale.** 4810 parameters, 3.4M, and 31M for the language model — three
  orders below where the record's practices are mostly argued, and the
  estimator's cost at those sizes is not reported.

### Added

- **Dropout Reduces Underfitting** (`LIT-475` / `NOTE-224`), Liu,
  Xu, Jin, Shen and Darrell (2023). Dropout applied only for the first stretch
  of training and then switched off **lowers training loss** and raises test
  accuracy on models too small to overfit — the regime where standard dropout
  costs ViT-T six points of ImageNet top-1.
- **`SOTA-285`** — put dropout at the start if the model underfits and at
  the end if it overfits; the schedule decides the sign, not the rate.
  `Proposed`, `unreplicated`.
- **`THEORY-044`** — early dropout buys a *biased* gradient estimate with
  much less directional variance, and the trade is favourable until it is not.
  `Proposed`.

### Changed

- **`SOTA-240` to version 2**, bounding its negative half. The recommendation
  is unchanged and its evidence is strengthened: the six-point drop on ViT-T
  is now the clearest measurement in the record of the cost that practice
  warns about. What is added is that the verdict is about dropout applied
  **throughout** training — a reader taking "not where it cannot [memorize]"
  as "never" would miss the prefix case.

### Documentation

- **The persuasive number is the training loss, not the accuracy.** ViT-T:
  3.443 baseline, **3.885** with standard dropout, **3.394** with early
  dropout. A regularizer raises training loss by construction, so the same
  operator is doing two opposite things depending only on when it runs. The
  practice says that if you try this and training loss does not fall, you have
  not reproduced the effect whatever the accuracy did.
- **The mechanism starts from a contradiction.** With dropout, gradient norms
  are *smaller* and the model ends up *farther* from initialization. The
  resolution is that the steps agree with each other: dropout lowers the
  pairwise angular spread of mini-batch gradients and, more importantly,
  lowers their angle to the **whole-dataset** gradient — for about the first
  thousand iterations, after which it rises.
- **Bias for variance, stated exactly.** Without dropout a mini-batch gradient
  is unbiased. With dropout it is biased, because each batch runs through a
  different sub-network. Variance falls by more than bias costs, so total
  angular error falls — early, when the model is changing fast and variance
  dominates. Later there is no variance left to remove and only the bias
  remains, which is why the effect is temporary and why the curves cross.
- **What is replicated and what is one model.** The variance and error
  reduction appears across five model/optimizer pairs (AdamW −13.60%, SGD
  −9.30%, momentum SGD −6.67%, Swin-F −17.41%, ConvNeXt-F s.d. −7.62%). The
  **crossing point** — the thing that would tell you where to switch — is
  ViT-T on ImageNet only. `THEORY-044` is `Proposed` for exactly that
  reason: if the crossing predicts the switch point the metric is a tool, and
  if it does not then the practice's wide robustness range is doing the work.
- **This paper reports its variance, and it changes the reading.** Three seeds,
  average standard deviation 0.142%. So +0.4 to +0.9 is real and ConvNeXt-F's
  +0.2 is not. Worth saying plainly after the previous contribution, where an
  approximation beating its own oracle had to stand in for error bars nobody
  reported.
- **The gains survive a stronger baseline and shrink.** Doubling epochs and
  weakening mixup and cutmix put ViT-T at 76.3, past published numbers, and
  early dropout still added 0.4.
- **All the evidence is vision**, and the underfitting regime it targets is a
  5–20M-parameter model on a fixed 1.2M-image set — not obviously the same
  object as a large model under-trained on a large corpus, which is the
  underfitting a reader of this record is likely to have. `ADR-026` is why it
  is filed; it does not make the evidence wider, and the promotion condition
  asks for a language-model run rather than another vision one.
- **An untested overlap worth naming.** `SOTA-008` and `SOTA-009` recommend
  learning-rate warmup, the record's other early-training intervention
  justified by gradient behaviour. Nobody has asked whether early dropout and
  warmup are doing one job twice — and the gradient-direction-error metric is
  exactly the instrument that would answer it.

### Added

- **The Coverage Principle** (`LIT-474` / `NOTE-223`), Chen, Huang,
  Golowich, Malladi, Block, Ash, Krishnamurthy and Foster (2025). Names the
  quantity cross-entropy is a bad proxy for — the **coverage profile**, the
  mass a model puts on rare high-quality responses — and proves it is
  necessary and sufficient for Best-of-N to succeed.
- **`THEORY-043`** — cross-entropy pays an unbounded price for mass a
  learner never had, and that price grows with sequence length. `Proposed`.
- **`SOTA-284`** — choose the checkpoint you post-train from by coverage,
  not validation cross-entropy. `Proposed`, `unreplicated`.

### Documentation

- **The whole argument fits in a two-outcome model.** Let `π*(1) = ε`. With
  constant probability a small sample contains no `1`, maximum likelihood
  assigns it zero, and **expected KL is infinite** — while the coverage
  profile stays fine, because it can write the missing mass off instead of
  paying `log(1/π̂)` for it. Nothing went wrong with the learner. KL's penalty
  for an under-assigned outcome simply has no upper bound, and coverage's
  does.
- **The two metrics diverge in the direction everything is moving.** Over `H`
  tokens the missed-tail opportunities multiply, so sequence-level KL grows
  **linearly in `H`** — proved as a lower bound for any proper estimator on
  autoregressive linear models, and reproduced empirically — while coverage at
  convergence shows no `H` dependence at all. Pushed through the KL-to-coverage
  bound this predicts test-time compute exponential in sequence length, which
  is the wrong shape, and that mismatch is what motivates the paper.
- **Within a single run, KL improves monotonically while coverage degrades.**
  Figure 1. At large `N` coverage is the better predictor of Best-of-N
  performance and cross-entropy can be anti-correlated with it.
- **`SOTA-210` now has its theory.** "Report pass@k as well as pass@1, because
  RL raises one and lowers the other" is, in this language, RL trading
  coverage for mode — and pass@k at `k = N` is an estimator of the quantity
  that gates post-training. Two independent groups found the effect; this says
  what they found.
- **The Adam sentence is speculation and is labelled as such in the source.**
  What is proved is that *globally* normalized SGD removes the sequence-length
  dependence on autoregressive linear models. The text then says "somewhat
  speculatively" that Adam may inherit the benefit, and notes that Adam
  normalizes per coordinate — a difference the authors themselves call
  important for deep models. `SOTA-001` gains nothing from this, and all three
  new documents say so, because it is the line most likely to be cited as a
  result.
- **Necessity is proved for Best-of-N, not for RL.** The source states
  directly that the minimal conditions for RL are unknown; the bridge is a
  cited empirical regularity that BoN predicts post-RL performance.
- **Why `Proposed` rather than `Active`, with the theorems not in doubt.** The
  distance between the setting and a language model is large and the authors
  list it themselves: a prompt/response formulation they call "closer in
  spirit to supervised fine-tuning", realizability for the main theorem,
  autoregressive linear models for the optimizer results, and one synthetic
  graph-reasoning task as the entire empirical content. A proof about a model
  class the record's practices are not about is an account offered rather than
  established.
- **The recommended quantity is not observable**, which the source concedes in
  a footnote. What is computable is an empirical coverage statistic on a
  labelled downstream set — cheap compared to a training run, expensive
  compared to reading a validation loss, and the practice says so.
- **Not "ignore cross-entropy".** It upper-bounds coverage and it is the thing
  you can see. The narrower claim is where the bound goes slack: at missing
  mass, increasingly with sequence length.

### Added

- **Quantized Evolution Strategies** (`LIT-473` / `NOTE-222`), Xu,
  Miikkulainen and Qiu (2026). Fine-tuning that happens *inside* a quantized
  model rather than around it: bank the part of each ES update that is
  smaller than the lattice spacing until it crosses a grid point, and
  rematerialize the accumulator from stored seeds instead of holding it.
  Joins `numerics-and-precision` to the `SOTA-154` line at a point neither
  had reached.
- **`SOTA-283`** — the recipe, `Proposed` and `unreplicated`, `extends`
  `SOTA-154` because it only makes sense if you are already fine-tuning with
  evolution strategies.
- **`THEORY-042`** — an update smaller than the lattice spacing is not
  merely rounded away, it is **cancelled exactly**. `Active`, because it is a
  derivation rather than a conjecture.

### Documentation

- **The failure is stronger than "rounding loses small updates".** Decompose
  the quantizer as identity plus error and expand the trajectory: when every
  step falls short of the grid, the accumulated quantization loss annihilates
  the accumulated ideal update term for term and `w_T = w_0`. No drift, no
  eventual threshold crossing — the optimizer is stationary. Round
  stochastically instead and you get an unbiased estimator whose *application*
  random-walks with variance growing in `T`. Carrying the remainder converts
  both into a bound: the physical weights stay within `Δ/2` of the
  high-precision trajectory for every `T`.
- **The memory trick is the contribution, not the error feedback.** Error
  feedback is 1-bit SGD's device and the paper credits it. What is new is
  that the accumulator **does not have to exist** — it is a deterministic
  function of seeds and scalar rewards already being kept. Without that
  inversion the method needs an FP16 buffer larger than the quantized weights,
  which is a memory method that does not fit in memory.
- **The reported variance is larger than the reported effects.** QES beats its
  own full-residual *oracle* at INT8 on both model sizes (26.35 vs 22.10;
  37.40 vs 33.30) and loses to it by 10 points at W8A8 on 3B (21.35 vs
  31.70). An approximation cannot beat what it approximates, so these are
  run-to-run noise — and no repeats or error bars appear anywhere. The
  caption's "only slightly lower than with full residuals" does not describe
  the W8A8 row. Every margin in the source is filed as provisional, the
  favourable ones included.
- **The source's prose disagrees with its own table twice in §4.2**: it gives
  QES "18.00%" on INT4/1.5B where the table has QES at 16.00 and the oracle at
  18.05, and it calls 14.25 → 31.85 a doubling of "the base model" where 14.25
  is QuZO's number and the base is 2.80. The record takes the table.
- **This is not an independent result in the ES line.** Its corresponding
  author is `LIT-211`'s first author. `SOTA-154`'s consensus note keeps an
  explicit count of which results come from inside that line, and this belongs
  on that side — so the practice's consensus does not move.
- **And it is the misuse `THEORY-006` named in advance.** That account's
  `promote_when` says what would *not* satisfy it: "a further post-training
  method that works and is read back as evidence for the account". This is
  one. All three new documents say so rather than leaving a reader to notice.
- **Working settings, from the ablation.** Decay `γ = 0.90` with a replay
  window between 10 and 50 — accuracy is flat across that range. Do **not**
  scale the decay down with the window: `W` = 10 at `γ` = 0.58 collapses to
  4.55%, and the ablation shows it is the aggressive decay rather than the
  short history.
- **The account says nothing ES-specific**, which is the obvious test it
  invites. The cancellation is about rounding an update, not about how the
  update was estimated, so the same argument covers a first-order optimizer
  on a quantized lattice. The record holds no result either way.

### Added

- **nGPT** (`LIT-472` / `NOTE-221`), Loshchilov et al. (2024). The
  normalized Transformer: every matrix and hidden state on one unit
  hypersphere, every normalization layer deleted, weight decay and
  learning-rate warmup set to zero, and each block's residual contribution
  made a learned per-dimension step size. 8 revisits on the papers-feed
  ranking and **zero mentions in the record** before this.
- **`SOTA-282`** — the recipe, `Proposed` and `unreplicated`. 4× / 10× /
  20× fewer tokens to a given validation loss at 1k / 4k / 8k context, 0.5B
  and 1B on OpenWebText, matched parameter count, learning rate tuned for
  both arms.
- **`THEORY-041`** — left unconstrained, a transformer's matrices drift
  into a badly conditioned, rank-deficient shape, and the norms are the part
  nothing was managing. `Proposed`: the evidence is correlational, and the
  document says what would settle it.

### Documentation

- **The headline is in tokens and the decision is in time.** Step time is
  **80% higher at 4k context and 60% higher at 8k** — six normalizations per
  layer instead of two, unfused. So 10× in tokens is about **5.5× in wall
  clock** as measured, and 20× is about 12.5×. Still large; not the number on
  the abstract. The practice says to quote the wall-clock figure, and the
  paper's expectation that kernel work will close the gap is recorded as a
  prediction rather than a result.
- **Two hyperparameters out, one in.** At the largest configuration tested —
  1B at 8k — Adam's `ε` on the learned step sizes had to be raised from its
  default to 0.1 to keep the learning-rate curve smooth. That is the direction
  of scaling, so "removes weight decay and warmup" is filed as an even trade
  until somebody shows otherwise.
- **The recipe bundles two separable ideas and nothing separates them.** The
  sphere constraint and the learned per-dimension residual step size are
  independent — the step size could be added to an ordinary pre-norm
  transformer tomorrow — and no ablation tells you which carries the gain. If
  it is the step size, this is far cheaper than it looks.
- **It collides with three practices the record holds, and the collision is a
  gap in their conditions.** `SOTA-008` and `SOTA-009` recommend warmup;
  `SOTA-120` recommends decoupled weight decay. All three are argued on
  architectures where the quantity they manage is free to drift. Worth noting
  that `SOTA-008`'s claim is specifically about **large batch size**, and
  global batch 512 at 1B is not that regime — so the warmup removal is
  untested against the case warmup exists for. No status changed.
- **Two groups reached one diagnosis independently and neither cites the
  other.** `SOTA-122` (learnable per-row and per-column multipliers) and this
  practice both hold that a weight matrix's norm should be managed
  deliberately rather than left as a residue of the learning rate and weight
  decay. Different remedies, both `Proposed`, both `unreplicated`. Two
  independent arrivals at a diagnosis is worth more than either remedy's
  evidence, and the record can say so without promoting either.
- **The variable-metric reading is a frame, not a finding.** The paper's
  interpretation — blocks supply gradients, the learned step sizes are a
  diagonal variable metric, normalization is a Riemannian retraction — earns
  the parameters their names and carries no evidence that it is why training
  is faster. `THEORY-041` records the conditioning observation instead,
  which at least has measurements, and says plainly that those are
  correlational.

### Added

- **The emergence dispute, both sides** (`LIT-470` / `NOTE-219`,
  `LIT-471` / `NOTE-220`). Wei et al. (2022), which named and
  defined emergent abilities, and Schaeffer et al. (2023), which argues they
  are a metric artefact. `SOTA-200` has recommended checking emergence claims
  for metric artefacts since 2026-09-10 while the record held **neither the
  claim nor its rebuttal** — a gap in the citation graph rather than a
  disagreement.
- **`THEORY-040`** — a metric that composes or thresholds per-token
  error turns a smooth capability curve into a sharp one, with nothing
  happening in the model. If per-token accuracy `p` rises smoothly, a metric
  demanding all `L` tokens goes as `p^L`, which is flat-then-sharp on a
  log axis by construction; a thresholded metric does it by a step instead.
  `Active`. Second account explaining `SOTA-200`, independent of
  `THEORY-039` — that one is about what the task asks of the model, this one
  about the scoring function applied afterwards.

### Changed

- **`SOTA-200` to version 2**, and the substantive edit is a reversal of its
  own advice. It said finding the continuous measure underneath was expensive,
  generalising from `LIT-085`'s progress measures, which needed the network
  reverse-engineered first. Usually it is cheap: **rescore the fixed outputs**
  under a linear metric or a proper scoring rule. Schaeffer et al. turned
  GPT-3's emergent arithmetic curve smooth without regenerating anything, and
  BIG-bench already computes Brier Score alongside Multiple Choice Grade.
- **A third check, which the first two missed.** `SOTA-200` asked whether the
  metric is all-or-nothing over multiple steps and whether the discontinuity
  is a regime property. Neither catches Multiple Choice Grade, which is a step
  function with no long target and no compounding — and **>92%** of
  hand-annotated BIG-Bench emergent abilities sit under it or Exact String
  Match. The practice now asks about discontinuity separately.
- **`SOTA-200`'s `consensus_note` corrected.** It said nobody had put a number
  on what share of emergence is artefactual. A number now exists and is not
  that number: >92% counts which *metrics* the claims sit under, not how many
  survive rescoring. Consensus stays `emerging` rather than `converged` — the
  bump was considered and declined, because the grounds available are one
  award and a citation count, and a consensus reading is a judgement about a
  community that needs better.

### Documentation

- **The popular framing of this dispute is wrong, and reading the primary
  source is what shows it.** "Wei said emergence, Schaeffer said metrics"
  is not what happened. `LIT-470` §5.1 raises the metric explanation
  itself, runs its own cross-entropy analysis, confirms that cross-entropy
  improves smoothly while downstream metrics sit at chance, and then declines
  the explanation for two stated reasons.
- **One of those two reasons was answered and the other was not.** Wei et al.
  argued the metric story could not cover "many classification tasks" — which
  assumed the problem was denying partial credit on long strings. Multiple
  Choice Grade is discontinuous rather than partial-credit-denying, so
  classification tasks are inside the explanation; the >92% figure is exactly
  that reply. **The intermediate-step objection is still open**: if final
  answer accuracy is a metric artefact, why does the quality of intermediate
  reasoning steps also jump? Nobody has answered it, and `SOTA-278` gives this
  record independent reasons to distrust reading traces as evidence — so it is
  open on both sides at once.
- **What `LIT-471` does not claim, in its own words**: "nothing in this
  paper should be interpreted as claiming that large language models cannot
  display emergent abilities". Manufacturing emergence in CIFAR-100
  autoencoders and Omniglot transformers proves a metric is *sufficient* to
  produce a sharp curve, not that every published curve was produced that way.
  Caballero et al. and Michaud et al. both hold some emergence is real and
  neither is refuted.
- **Why the vision experiments are the strongest evidence**, rather than the
  GPT-3 rescoring everyone quotes. Dissolving one instance leaves open whether
  that instance was special; running the mechanism forwards in two
  architectures and a domain with no prior emergence claims shows the metric
  alone is enough.

### Fixed

- **`Pages` could have published a branch over the site.** `deploy`'s
  condition was `github.event_name != 'pull_request'` — a deny-list with one
  entry — and `workflow_dispatch` takes no branch filter, so a manual dispatch
  from any branch ran it. The environment's branch policy used to refuse that;
  it has since been widened to admit `claude/*`, which turned a job that
  failed loudly into one that would have succeeded quietly. `deploy` now
  names the branch: a `workflow_run` whose `head_branch` is `main`, or a
  `workflow_dispatch` on `refs/heads/main`, and nothing else. The two events
  are checked separately because `workflow_run` reports the triggering
  branch in `head_branch`, not in `github.ref` (`ADR-051`).

### Removed

- **The `pull_request` trigger on `Pages`.** Pull requests no longer build the
  site. `docs-check` still lints the sources on every pull request, so nothing
  about record correctness moves; what is lost is the automatic proof that
  `luria site` still builds. `build` is deliberately left ungated, so a
  `workflow_dispatch` from a branch is that check on demand — a worse check
  than one that runs itself, and the honest cost. Restoring it is one line.

### Documentation

- **A decision for a permission that is granted and unused** (`ADR-051`).
  The `github-pages` environment admits `claude/*` deployments and the
  workflow declines to use them. That state invites tidying from both
  directions — revoke a policy somebody wanted, or spend it because it is
  there — so the reason is written down rather than left to be inferred from a
  condition.

### Added

- **The two chain-of-thought descendants** (`#180`), both named as uncovered
  by `SOTA-279` when the trunk was filed, and both landing in
  `in-context-learning` — the topic `ADR-050` added hours earlier.
- `LIT-469` / `NOTE-218` — Kojima et al., *Large Language Models are
  Zero-Shot Reasoners* (`ARXIV-2205.11916`). Read. `extends: LIT-467`.
- `LIT-468` / `NOTE-217` — Wang et al., *Self-Consistency Improves
  Chain of Thought Reasoning* (`ARXIV-2203.11171`). Read. `extends: LIT-467`,
  tagged `inference-optimization` as well.
- `SOTA-281` — try the single step-by-step instruction before writing
  exemplars. `Active`, `consensus: universal`. Extends `SOTA-279`.
- `SOTA-280` — sample several reasoning paths and take the majority
  answer. `Active`, `consensus: emerging`. Extends `SOTA-279`.

### Documentation

- **The ordering is the practice, not the number.** Zero-shot chain of
  thought takes MultiArith from 17.7% to 78.7% — against *zero-shot*
  prompting. It **underperforms** hand-written few-shot chains and
  **outperforms** eight-shot standard prompting, and the paper says both. So
  the recommendation is about what to try first, which is all those two facts
  together license.
- **`SOTA-279`'s conditions are sharpened rather than contradicted.** That
  practice says to write worked steps into the exemplars; this says measure
  the free version before paying for them.
- **Self-consistency counts answers, not reasoning.** Its calibration and
  uncertainty by-products come from the answer distribution. The authors note
  models sometimes generate nonsensical paths, and `LIT-467`'s own error
  analysis found correct answers reached through incorrect chains — so an
  evaluation that reads a trace as an explanation is not rescued by it, which
  `SOTA-278` is the practice about.
- **The cost is in the conditions, not the prose.** Zero-shot CoT is two
  generation calls per question, not one. Self-consistency is linear in
  paths, and the authors' own five-to-ten guidance is a rule of thumb with no
  scaling story behind it.
- **Composition is noted and not claimed.** Nothing requires self-consistency's
  sampled chains to come from exemplars rather than a trigger sentence, but
  neither paper measured that pairing and the record does not imply it was.
- **The "single prompt" framing is slightly stronger than the method**, since
  the answer-extraction stage is format-dependent. Recorded in the practice's
  conditions.

### Added

- **Two topics, taking the vocabulary from fourteen to sixteen**
  (`ADR-050`, `#213`). `ADR-024` listed adding a topic as one of four
  options and decided none of them; two of the other three have been taken
  since and this takes the first.
- **`numerics-and-precision`** — how many bits, where, and what that costs:
  number formats, training precision and the failures it causes,
  post-training quantization, and the interaction between them. 18 documents
  take it as primary, 11 more as a secondary.
- **`in-context-learning`** — getting behaviour out of a fixed model by what
  you put in the context: few-shot exemplars, chain of thought, prompting
  strategy, and what the context can and cannot buy. 6 primary, 6 secondary.

### Changed

- **`systems-optimization` loses "numerical precision" from its blurb** and
  **`inference-optimization` loses "quantization"**. The subject had two
  half-homes, each carrying it as a trailing item in a topic that is about
  something else. No document loses a tag.
- **41 documents retagged**, 24 to a new primary and 17 to a new secondary.
  The primary moved only where the document's central claim is the new topic:
  `SOTA-016` (do the forward pass in FP16) takes it, `SOTA-159` (a
  parameterization that happens to make FP8 work) keeps
  `training-optimization` first and takes it second.
- **`adaptation-and-tuning`'s blurb says "safety alignment" rather than
  "alignment".** The bare word is a homonym and this pass proved it the
  expensive way: a probe returned 42 documents that read as a safety-shaped
  gap, and two of them were about safety. A blurb item that matches the wrong
  sense of its own word sends documents to the wrong place and hides it
  afterwards. This adds no topic — two documents is not several, the same
  test retrieval failed.
- **The config said "thirteen" while declaring fourteen terms.** `tiny-models`
  was added without updating the comment or the axis blurb. Both now say
  sixteen.

### Documentation

- **The instrument changed, because the old one stopped reporting.**
  `ADR-024` found its seams in the unbound-lineage report; `ADR-049` has since
  driven that to zero by liberal tagging, which is correct and leaves the
  report unable to show a *missing* word — a subject with no name produces no
  unbound edge, it produces documents filed under whatever was nearest. This
  pass used `DP-009`'s test instead: count the documents on a candidate
  subject and measure how concentrated their primary topics are.
- **Why one numerics topic and not two.** The train/serve split is real and is
  not where the work is: `SOTA-160`, `LIT-186`, `SOTA-234` and `LIT-380` are
  about the interaction, and splitting there would re-create the seam one
  level down — `ADR-024`'s own warning about dividing a subject by provenance.
- **Why the name is precision rather than quantization.** `LIT-363` and
  `LIT-341` are *vector* quantization, which is representation work.
- **A third candidate was rejected on counting.** Retrieval measured 12
  documents at 33%; inspected, it is two — `SOTA-269` and `LIT-060`. The rest
  are a homonym: "retrieval" in the linear-attention papers means the
  in-context recall benchmark. `DP-009` asks for several and two is not
  several.
- **Three probes in this pass were inflated by homonyms**, each caught only by
  reading the hits: "alignment" (gradient alignment, not safety — 42 apparent
  documents, 2 real), "retrieval", and "quantization". A keyword probe over
  this corpus generates candidates and settles nothing.
- **One unbound line survives, with both of `ADR-049`'s readings tested and
  both failing.** No true tag binds `SOTA-036 → 037 → 038 → SOTA-279`, and
  the edges hold against `extends`'s own blurb — "a rule that only exists
  because the earlier one is followed" covers a capability claim about models
  trained under a recipe. Left open for the record's owner rather than closed
  by asserting a tag nobody believes.

### Changed

- **`CLAUDE.md`'s rule on second topics is corrected.** It read "add a second
  topic when it is genuinely true, and never to bind a relation". The second
  clause forbids a *motivation* rather than a falsehood, and read on its own
  it rules out the workflow `docs/reports/unbound-lineage.md` exists to
  support — noticing, from the report, that a document is not saying what it
  is about, and adding the topic that is true of it. The rule now states the
  truth test and says what `ADR-035` actually rules out.
- **`ADR-035` gains a section pointing at what narrowed it** (v2). No decision
  changes. §3 already called a shared tag binding a relation "the point and
  the risk" and §4 identified the risk as a *free-form label* invented to
  satisfy the check; §5 then closed the vocabulary on `SOTA`, `LIT` and
  `THEORY`, which makes that failure structurally unavailable there. `ADR-046`
  and `ADR-049` have since narrowed it explicitly, and the new section sends
  the reader to them rather than restating the rule a third time.
- **`LIT-035`'s v2 history note is rewritten.** It justified the added tag
  against the misread rule, arguing that the tag was added "because it is
  true … and not because it binds an edge, which `CLAUDE.md` forbids". The
  reasoning was sound and the frame was wrong: acting on the report is the
  intended response, not something needing a defence. The note now says the
  plain thing.

### Documentation

- **What `ADR-035` rules out, exactly.** Not "a tag that binds an edge" —
  that is what a relation asserting a shared subject is *for*. The failure is
  "a tag that is not a topic, added because it binds", which is the `#101`
  move with `flash-attention`, removed in §4.
- **`CLAUDE.md` now states what actually governs tagging**, which is `ADR-046`
  (tag the subject, liberally; the test is *justifiably appropriate*) and
  `ADR-049` (an unbound relation has two readings and never a third). Neither
  was cited in the rule before, and `ADR-035` alone is the wrong place to read
  it from.
- **One open finding, and it is open rather than settled.** The
  `SOTA-036 → 037 → 038 → SOTA-279` line has no tag common to every member.
  Under `ADR-049` that is a defect with two readings and this contribution
  answers neither: `adaptation-and-tuning` is not justifiably appropriate for
  `SOTA-036`, which is a pretraining recipe, and no edge in the line looks
  wrong. What the line shares is *in-context learning*, which the vocabulary
  cannot say. Adding a topic is `CLAUDE.md`'s named move for that and wants
  its own decision rather than a drive-by.
- **`ADR-035` is still `Proposed`**, and its own text says why: it reads
  `exactly-one` as never having been load-bearing for a document having one
  subject, and asks for "that reading … checked by someone who was there".
  Unchanged here; this contribution corrects a gloss, not the decision.

### Added

- **The chain-of-thought trunk** (`#180`). Filling the gap named one
  contribution earlier: the record held no practice recommending chain of
  thought, in 278.
- `LIT-467` / `NOTE-216` — Wei et al., *Chain-of-Thought Prompting
  Elicits Reasoning in Large Language Models* (`ARXIV-2201.11903`). Read.
  Declares `extends: LIT-035`.
- `SOTA-279` — put worked reasoning steps in the few-shot exemplars when
  the task needs more than one step, and only once the model is large enough.
  `Active`, `consensus: universal`. Extends `SOTA-038`.

### Changed

- **`LIT-035` gains `adaptation-and-tuning`** (v2). The GPT-3 paper is titled
  "Language Models are Few-Shot Learners" and its central claim is reaching a
  new task from in-context examples with no gradient update — which is what
  that topic's blurb describes. `SOTA-038`, sourced to it, already carried
  the tag, so the paper was the one document in the chain not saying what it
  was about. Surfaced by the unbound-lineage report and recorded that way on
  purpose: added because it is true, which is the test, and not because it
  binds an edge, which `CLAUDE.md` forbids.
- **`SOTA-277` cited a temp code that no longer existed.** It referenced the
  temporary code that had already become `SOTA-275` in the preceding
  contribution; concretization rewrote that document's own codes but not this
  cross-reference to an earlier branch's, leaving a dangling link and a
  directive that excused nothing. Repointed to `SOTA-275`.

### Documentation

- **The ablations are the reason this is the trunk.** Three rival accounts
  were built and knocked down: not the equation (equation-only prompting does
  not help on GSM8K), not the extra tokens (a row of dots as long as the
  needed equation performs at baseline), and not knowledge activation (the
  chain placed *after* the answer performs at baseline).
- **The regime is carried, not dropped.** Below roughly 100B parameters the
  effect is absent and often negative — small models produce chains the paper
  calls "fluent but illogical" — and on single-step problems the gain is
  negative or negligible. `SOTA-127`, which says to filter such traces out of
  a tiny specialist's training data, now has the paper explaining why sitting
  beside it.
- **The dots ablation and the theory result do not conflict.**
  `THEORY-038` holds that chain of thought gives a shallow decoder extra
  computation space. This paper shows that extra tokens carrying *no
  information* buy nothing. Both are true: the room only helps if
  intermediate results go in it. Stated in the reading note because a fast
  reading makes them look opposed.
- **The emergence claim is flagged against `SOTA-200`.** It is measured as
  exact-match over multi-step answers, which is almost word for word the case
  BIG-bench (`LIT-077`) names as producing breakthrough curves. The *gains*
  at 540B survive three ablations and are not in doubt; the *discontinuity*
  has not been re-measured against a continuous score. Schaeffer et al.
  (`ARXIV-2304.15004`) argues this directly and the record does not hold it.
- **`consensus: universal` with one source, and `DP-005` is why those are
  separate columns.** The field stopped arguing about this years ago and
  models are post-trained to produce traces unprompted; the evidence column
  still holds one paper about models nobody serves any more.
- **One unbound line, left unbound.** `SOTA-036 → 037 → 038 → SOTA-279`
  now has no tag common to every member: the first two are
  `model-architecture`, the last is `adaptation-and-tuning`. That is the line
  genuinely changing subject — from what the architecture does at scale to
  how to prompt it — rather than a missing word. Forcing `model-architecture`
  onto a prompting practice to close it would be the move `ADR-035` forbids.

### Added

- **The capability-limits cluster** (`#180`). Four papers on the difference
  between a limit a model has and a limit an evaluation produced. The record
  held nothing on either.
- `LIT-464` / `NOTE-214` — Chen et al., *Theoretical limitations of
  multi-layer Transformer* (`ARXIV-2412.02975`). The first unconditional lower
  bound for a decoder-only transformer of more than one layer.
- `LIT-466` / `NOTE-212` — Shojaee et al., *The Illusion of
  Thinking* (`ARXIV-2506.06941`), NeurIPS 2025.
- `LIT-463` / `NOTE-213` — Lawsen, *Comment on The Illusion of
  Thinking* (`ARXIV-2506.09250`). Declares `corrects: LIT-466`.
- `LIT-465` / `NOTE-215` — Hu and Frank, *Auxiliary task demands
  mask the capabilities of smaller language models* (`ARXIV-2404.02418`),
  COLM 2024.
- `THEORY-038` — a decoder cannot compose over a long context in few
  layers, because each position forgets what it forwarded. `Active`.
- `THEORY-039` — a measured capability is the capability minus what the
  evaluation demands, and the gap is widest for the weakest model. `Active`.
  Explains `SOTA-200` as well as the new practice.
- `SOTA-277` — for a task that is a sequential composition, buy depth
  rather than width. `Proposed`.
- `SOTA-278` — before reporting that a model cannot do something, rule
  out the evaluation. `Active`, `emerging`.

### Documentation

- **The record's first lower bound.** Everything in it until now says what to
  do or why something works. A claim about what is unavailable at any amount
  of tuning is a different shape, and `THEORY-038` is the first.
- **The chain-of-thought gap is named, not filled.** The record holds no
  practice recommending chain of thought; `SOTA-127`, which says to filter
  such traces *out* of tiny models' training data, is the whole of it.
  Corollary 1.4 of `LIT-464` proves a one-layer decoder with chain of
  thought can express a composition that a constant-depth one cannot — a
  representability result, and not grounds for a recommendation about
  inference (`ADR-017`).
- **A dispute held open rather than decided.** `LIT-466` is NeurIPS
  2025, camera-ready, revised in November 2025 — five months after the comment
  against it appeared. `LIT-463` is a single-author preprint whose
  central experiment is underpowered by its author's own statement, which has
  been publicly corrected once, and whose bibliography miscites the paper it
  comments on. Its unsolvable-instance claim is a checkable mathematical fact
  and stands on its own. Both notes say which claims are which.
- **The two papers agree on the fact they are arguing about.** Both report
  that the accuracy collapse happens *below* the token limit. They differ on
  what that means: a scaling limitation of thinking, or a model poorly
  calibrated about its own remaining budget.
- **`SOTA-200` now has its mirror.** That practice checks whether a capability
  appearing with scale is a metric artefact; `SOTA-278` checks whether a
  limit appearing at small scale is a demand artefact. Independent
  literatures, opposite signs, one instrument problem — and `THEORY-039`
  explains both.

### Added

- **The width-depth muP unit** (`#180`). The paper that had been sitting at
  the top of the revisit ranking, unread because arXiv serves no HTML for it.
  A second download of the PDF came back complete where the first was
  truncated, and it extracted cleanly.
- `LIT-462` / `NOTE-211` — Zheng et al., *Spectral Condition for
  muP under Width-Depth Scaling* (`ARXIV-2603.00541`). Read. Declares
  `extends: LIT-437` (the width-scaling spectral condition) and
  `extends: LIT-150` (CompleteP).
- `THEORY-037` — residual-branch depth sets the depth scaling rule,
  because a branch with two transformations has a second-order update term a
  branch with one does not. `Active`. Explains `SOTA-144`, `SOTA-275`
  and `SOTA-276`.
- `SOTA-275` — pick the depth parameterization from the residual branch;
  a Transformer branch holds more than one transformation, so it needs
  CompleteP's `1/L` and not Depth-muP's `1/√L`. `Proposed`. Extends
  `SOTA-144`.
- `SOTA-276` — for a normalized or preconditioned optimizer, width-depth
  muP is width muP plus a hidden residual multiplier of order `1/L`; SGD is
  the exception. `Proposed`.

### Changed

- **`SOTA-144` consensus `unreplicated` → `emerging`** (v2), with
  `promote_when` rewritten. It asked for "an independent group training under
  CompleteP itself and reporting depth transfer". Zheng et al. are
  independent — Renmin University and ByteDance Seed, no overlap with the
  CompleteP authors — derive the same depth scaling from their own spectral
  framework, and report learning-rate transfer to 256 layers across four
  optimizers. Status stays `Proposed`: `promote_when` now asks for the thing
  that is actually missing, which is a run at a realistic token budget.

### Documentation

- **The old `promote_when` is recorded as not literally met, and a section
  says why.** Zheng et al. train Muon-Kimi-AdamW, Muon-AdamW, Shampoo-AdamW
  and Sophia — explicitly not AdamW, the optimizer CompleteP was defined for
  — under a condition the paper says "recovers CompleteP-style results". The
  hedge is the paper's own word. The record counts this as corroboration of
  the route by a wider set of optimizers rather than as the literal test, and
  writes the difference down instead of treating the field as discharged.
- **Two depth parameterizations turn out to be one.** The record carried
  Depth-muP and CompleteP as separate things with nothing connecting them.
  They are `k = 1` and `k ≥ 2` of a single spectral condition, and the whole
  difference is one term in a product expansion — the case where both weights
  in a residual branch move in the same step.
- **The record recommends Muon and matrix preconditioning and never said how
  to muP either.** `SOTA-276` is the answer, and it is short: a
  preconditioned update's norm does not depend on the residual multiplier, so
  the optimizer-specific rule is unchanged from the width-only case.
- **A confound the authors flag themselves.** For Muon-Kimi-AdamW, standard
  parameterization appears to transfer across depth in their Figure 1(d).
  They attribute it to moderate depths and to LayerNorm and QKNorm masking
  the pathology, and removing LayerNorm breaks it. Carried into
  `SOTA-275`'s conditions and `THEORY-037`, because it means the
  practical margin at realistic depth is smaller than the asymptotic
  argument.

### Added

- **The update-geometry cluster** (`#180`). Three papers on why spectral
  optimizers work and one on the regime underneath them, all
  `training-optimization`.
- `THEORY-035` — gradient descent raises the sharpness until its own
  step size cannot tolerate more, then trains there. `Active`. Sources
  `LIT-461` (Cohen et al., `ARXIV-2103.00065`), read in `NOTE-205`.
  Explains `SOTA-272`.
- `THEORY-033` — what a spectral optimizer buys is a step size that
  stays optimal, not adherence to a target geometry. `Proposed`. Sources
  `LIT-456` (Shumaylov et al., `ARXIV-2605.11181`), read in
  `NOTE-208`.
- `THEORY-032` — a spectral update wins where the incoming activations
  are low stable rank and the gradient spectrum is spread out. `Proposed`.
  Sources `LIT-457` (Davis and Drusvyatskiy, `ARXIV-2512.04299`), read
  in `NOTE-209`. Explains `SOTA-165` and `SOTA-274`.
- `SOTA-272` — expect the loss to be non-monotone at the step size that
  trains fastest, and do not set the step size from a curvature bound.
  `Proposed`.
- `SOTA-274` — before adopting a spectral optimizer, measure the stable
  rank of each block's incoming activations against its gradient's nuclear
  rank. `Proposed`.

### Changed

- **`THEORY-024` demoted from `Active` to `Proposed`** (v2). It closed by
  saying all three of its sources share authors and that it was `Active`
  "not because anyone outside has confirmed the frame." Shumaylov et al.
  are the first outside group to test the frame and come back negative on
  its explanatory force: `Kaon`, which replaces the gradient's singular
  values with chaotic noise and dualizes nothing, matches Muon. The
  derivation is untouched, no text was removed, and a new section records
  what the test reaches. `promote_when` names the result that would restore
  the status.
- **`LIT-453` declares `extends: LIT-461`** (v2). The edge existed in
  the argument from the day it was filed — a central flow is a model of the
  edge of stability, by the same first author — and the record did not hold
  the antecedent, so the relation could not be written.
- Acknowledgement directives at the five pre-existing sites that cite
  `THEORY-024` (`LIT-438`, `LIT-453`, `NOTE-189`, `NOTE-203`, `THEORY-030`),
  written from the lint's own report after the demotion made them
  unacknowledged.

### Documentation

- **A premise the record asserted and did not hold.** `THEORY-030`'s
  `promote_when` says of the edge of stability that it "is established and
  is the premise rather than the claim" — true of the literature, and not of
  the record, which held no paper for it. `LIT-461` is that paper, five
  years old and cited by the document that stood on it.
- **No practice was filed from `LIT-456`, and `NOTE-208` says
  why.** Its actionable residue — retune the learning rate per optimizer
  rather than transferring it — is already `SOTA-165`'s, from `LIT-156`, at
  four scales rather than one. `Kaon` is a control and not a
  recommendation.
- **Three accounts of one practice, held as three.** `THEORY-024`,
  `THEORY-033` and `THEORY-032` all bear on matrix
  preconditioning; the second denies the first's explanatory force and the
  third reaches the same practices through rank structure. Neither of the
  two new papers cites the other. They are filed separately because
  collapsing them would assert an answer nobody has.
- **None of it touches `SOTA-121`, `SOTA-143`, `SOTA-165` or `SOTA-168`.**
  What is contested is the account, not the technique — `ADR-031`'s
  separation and `ADR-034`'s restatement of it.

### Added

- **The representation-convergence cluster** (`#180`). The
  `representation-and-encoding` topic held **fourteen** `LIT` notes and every
  one was tokenisation or positional encoding — subword units, RoPE, ALiBi,
  context extension, the inner lexicon. Nothing on what a representation *is*
  or what it converges to.
- `THEORY-036` — representations converge across architectures,
  objectives and modalities, and the endpoint is conjectured to be a model of
  what generated the data. Explains `SOTA-271`. Sources `LIT-458`
  (Huh et al., `ARXIV-2405.07987`), read in `NOTE-206`.
- `THEORY-034` — concepts sit in embedding space as intersections of
  half-spaces, so inclusion, intersection and union are geometric meet and
  join. `explains:` is empty and says why. Sources `LIT-460` (Xiong,
  `ARXIV-2603.01227`), read in `NOTE-210`.
- `SOTA-271` — train on a second modality even when the target is
  single-modality. The vision direction is already standard practice; the
  language direction is the claim.
- `SOTA-273` — choose a pretraining context whose association with the
  input is neither too strong nor too weak, and mix contexts to get there.
  Sources `LIT-459` (Zhai, `ARXIV-2504.19792`), read in `NOTE-207`.

### Documentation

- **A `Skimmed` reading, marked as one.** `LIT-459` is a
  313,000-character dissertation. `NOTE-207` records what was read —
  abstract, introduction, implications, conclusions, the two objectives — and
  what was not: the theorems, the statistical learning bounds, the
  semi-supervised extension. `ADR-025` makes `Skimmed` respectable and says
  it is not enough to source a practice from alone; `SOTA-273` carries
  that debt in its conditions rather than discharging it, and is
  `consensus: unassessed` for the same reason.
- **A trunk named rather than filled.** Both new theory documents stand on
  the **Linear Representation Hypothesis** — that features and concepts are
  directions in embedding space — and the record holds no document for it,
  nor for steering vectors, nor for concept geometry. Filing two
  elaborations of an absent foundation is backwards, and closing it properly
  is a unit of its own.
- **Two claims kept apart that a summary would merge.** That representations
  are converging is measured. That the endpoint is a model of the world is
  conjectured, with a proof holding only for bijective observations. The
  theory document separates them, which is why it is `Proposed` despite its
  first half being well supported.
- **The friendliest test is not a severe one.** `LIT-460`'s evidence is
  WordNet — a hand-built ontology with exactly the hierarchical structure the
  hypothesis predicts. Recovering a lattice from concepts somebody
  constructed as a lattice is weak evidence that the lattice is in the
  embeddings. The severe test is cheap and is named in `promote_when:`.

### Added

- **The loss-curve cluster** (`#180`) — three papers, four years apart, none
  citing the others, each measuring a different thing the aggregate loss
  curve throws away.
- `THEORY-031` (`Active`) — **the aggregate loss curve is a lossy
  projection of training, in at least three measured ways.** It time-averages
  oscillation the optimizer is actually doing; it sums over transitions that
  are individually abrupt and differently timed; and it reads flat while the
  weights keep travelling. No one paper states this — the record does, from
  holding all three, which is the `DP-007` shape given an arrival event.
- `SOTA-270` (`Active`) — do not read a smooth loss curve as evidence of
  smooth training; decompose it when the answer matters. The caution is free;
  the instrument is not.
- `THEORY-030` — adaptive optimizers work by **shaping** the curvature
  they adapt to, and oscillation is how a first-order method sees curvature
  at all. At the edge of stability sharpness sets the step size and the
  learning rate modulates an implicit curvature penalty. Explains `SOTA-001`,
  which the record has recommended without an account of what adaptivity
  buys.
- `LIT-453` / `NOTE-203` — Cohen et al., *Central Flows*
  (`ARXIV-2410.24206`). `LIT-455` / `NOTE-204` — Kangaslahti et
  al., *Hidden Breakthroughs* (`ARXIV-2506.15872`). `LIT-454` /
  `NOTE-202` — Kunin et al., *The Limiting Dynamics of SGD*
  (`ARXIV-2107.09133`).

### Documentation

- **The record's only prior account of optimizer dynamics is one it does not
  believe.** `THEORY-013` is `Rejected` — the SGD noise scale selecting
  minima that generalise, retired because a 35-workload sweep found the
  effect vanishes once metaparameters are retuned. Edge of stability, among
  the most-replicated findings about neural optimization of the last five
  years, had no document at all.
- **Guilt by association is the available mistake here, and three passages
  are written to prevent it.** `LIT-454` shares its SDE machinery with
  `THEORY-013`. What was rejected is a claim about *test accuracy*, which
  Kunin et al. do not make. `ADR-034`'s rule is the guard: `Rejected` on a
  theory retires the reason, not everything built with the same tools.
- **Smoothness is what many breakthroughs look like added up.** The negative
  control is what makes this more than a story — clustering exact per-example
  loss curves recovers digit position and misses carrying at chance (0.514);
  decomposing per example *and* along a curvature-derived basis recovers
  both.
- **Two accounts of one puzzle, neither citing the other.** `THEORY-024` says
  orthogonalising the update is dualising it; `THEORY-030` says
  first-order methods already pick up second-order information by
  oscillating. Whether those are two descriptions of one mechanism is the
  question the record can now pose from holding both.
- **The full-batch boundary is stated rather than blurred.** Every Central
  Flows result is deterministic training and every recipe this record holds
  is stochastic. No practice is filed from it for that reason, and
  `promote_when:` asks for the bridge.

### Added

- **The knowledge-acquisition cluster** (`#180`) — three papers on how
  factual knowledge is acquired and stored, all bearing on `THEORY-025`,
  which shipped two days ago with `explains:` empty.
- `SOTA-268` — **do not transfer a data mixing ratio across model
  scales.** Below a critical model size, or a critical mixing ratio, a model
  acquires almost nothing from a knowledge-dense domain however long it
  trains; past the threshold accuracy jumps to over 60%. The critical ratio
  follows a power law in model size. Sources `LIT-451` (Gu et al.,
  `ARXIV-2505.18091`), read in `NOTE-201`.
- `SOTA-269` (`Active`) — keep a knowledge base outside the weights.
  All of Wikidata would want ~1000B non-embedding parameters at 100 epochs,
  and derivable facts cost full price. Sources `LIT-452` (Lu et al.,
  `ARXIV-2406.15720`, read in `NOTE-200`) and `LIT-060`.
- `SOTA-267` — start the training distribution imbalanced and flatten
  it. Plateau length is set by the *most* frequent entities and acquisition
  speed by the *least*, so no fixed distribution is right. Sources
  `LIT-450` (Zucchet et al., `ARXIV-2503.21676`), read in `NOTE-199`.
- `THEORY-029` — a model of bounded capacity allocates it across
  datasets like a knapsack, so the optimum jumps rather than sliding.
  Explains `SOTA-268`.
- `THEORY-028` (`Active`) — **the plateau before factual recall is the
  formation of the attention circuit that recall needs.** Established by
  intervention: patching a reference model's attention patterns in removes
  the plateau. Explains `SOTA-267`.

### Changed

- **`SOTA-166` v2 and `SOTA-238` v3 are both `contested`**, by
  `LIT-451`. Both set data proportions from small runs — one by fitting
  a mixing law and extrapolating, the other with a small proxy under group
  DRO — and both assume the fitted quantity moves continuously with scale.
  Neither is refuted; both now name the way that assumption can fail.
- `THEORY-025` v2 — corroborated and bounded in the same contribution.
  `LIT-452` measures fact capacity on Wikidata and finds it linear in
  model size, which is this account's linear claim through a different
  instrument and different units. `LIT-451` bounds it: the
  fixed-budget picture is the single-claimant case.

### Documentation

- **A scaling law measured on one dataset is a statement about a model with
  one claimant on its capacity.** The linear law for knowledge acquisition
  was measured by training on biographies alone. Add a second dataset and the
  model is solving an allocation problem, which has a discrete answer, and a
  discrete answer moves discontinuously. The smoothness everyone assumed came
  from never having more than one claimant.
- **A flat loss can be a prerequisite under construction.** Until the
  extraction circuit exists, the error at the attribute token does not reach
  the name tokens, so the key-value store in the MLPs gets no usable signal.
  The model is not stuck; it is making the only progress available, on a
  component whose value is invisible in the loss until it is finished.
- **The record held RETRO and never recommended retrieval.** `LIT-060` has
  been filed since early on, and the only practice drawn from it was
  `SOTA-197`, about contamination in evaluation. An absence no query would
  have found, because nothing was complaining about it.

### Added

- **The flow and interpolant trunk** (`#180`) — the record held DDPM, DDIM,
  latent diffusion, EDM and the distillation line, and nothing at all on
  rectified flow, flow matching or continuous-time diffusion. Four papers,
  three of them read in full.
- `SOTA-266` (`Active`) — **connect data and noise on a straight line,
  and sample the training timesteps from a logit-normal rather than
  uniformly.** Both halves are the practice: rectified flow with *uniform*
  timesteps does not win the 61-way comparison, and with a logit-normal it
  does. Sources `LIT-449` (Esser et al., `ARXIV-2403.03206`, read in
  `NOTE-196`) and `LIT-447` (Ma et al., `ARXIV-2401.08740`, read in
  `NOTE-197`).
- `SOTA-265` (`Active`) — tune the stochastic sampler's diffusion
  coefficient after training. It affects neither the velocity nor the score,
  so it was never downstream of training; the claim rests on an identity
  rather than a sweep.
- `SOTA-263` — shift the timestep schedule when the resolution changes.
  `SOTA-262` — give each modality its own weights and let the streams
  attend jointly (MMDiT).
- `SOTA-264` — fix the noise schedule's endpoints against the bound and
  choose its shape to minimise the loss estimator's variance. Sources
  `LIT-446` (Kingma et al., `ARXIV-2107.00630`), read in `NOTE-198`.
- `THEORY-027` (`Active`) — **in continuous time the diffusion bound
  depends on the noise schedule only through its endpoints.** Integrate over
  signal-to-noise ratio instead of time and the schedule leaves the
  integrand. Variance-preserving and variance-exploding specifications are
  the same model up to a rescaling. Explains `SOTA-188` and `SOTA-264`.
- `LIT-448` — DiT (Peebles and Xie, `ARXIV-2212.09748`), filed as
  context and **filed unread**, which per `ADR-025` is what the absent `NOTE`
  says. It is the backbone the other two hold fixed.

### Changed

- `SOTA-188` v4 — the implementation it already listed now has its paper.
  Stable Diffusion 3's logit-normal over timesteps is this practice's
  log-normal over noise levels in rectified-flow coordinates, confirmed at
  8B in a formulation EDM did not test. And the objection the practice never
  answered — *if you change where you sample, have you changed the model?* —
  now has `THEORY-027` as a qualified no.
- `SOTA-192` v4 — records an independent arrival. QK-norm reaches an 8B
  diffusion transformer through the discriminative ViT literature's
  attention-entropy diagnosis, after mixed-precision training diverged at
  high resolution. Neither that line nor the language-model line this
  practice was filed from cites the other.

### Documentation

- **A summary would have dropped the half that matters.** Rectified flow had
  two years of equivocal empirics because the literature wrote it with
  uniform timestep sampling. The path and the distribution over where you
  train along it are separate decisions, and conflating them made a real
  advantage look absent.
- **A change of variables can tell you which of your design choices were
  choices.** Noise schedules looked like modelling because the loss was
  written as an integral over time. Written over signal-to-noise ratio, the
  schedule appears only in the limits — so years of schedule proposals were
  an argument about an optimisation convenience conducted in the vocabulary
  of a model class.
- **`DP-007` has an interesting variant here.** Agreement has no author and
  so no arrival event; QK-norm has *two* arrival events, in two literatures,
  from two different failure modes, with no citation in either direction.
  The record can see both only because `ADR-026` files by the kind of claim
  rather than the domain it was found in.

### Added

- **The hyperparameter-scaling cluster** (`#180`) — three papers from the
  reading feed on the constants everybody copies: weight decay, batch size,
  and Adam's decay rates.
- `SOTA-261` — set weight decay by targeting a normalized AdamW
  timescale, which follows a power law in tokens-per-parameter with exponent
  about −0.52 over three orders of magnitude of compute. Sources
  `LIT-443` (Bergsma et al., `ARXIV-2505.13738`), read in `NOTE-193`.
- `SOTA-258` (`Active`) — **scale batch size with the token budget, not
  with compute or model size.** Sources `LIT-445` (Zhang et al.,
  `ARXIV-2410.21676`, read in `NOTE-195`) and `LIT-443`.
- `SOTA-260` — use the smallest batch that still saturates the device,
  and do not gradient-accumulate to avoid it. `SOTA-259` — hold Adam's
  second-moment half-life fixed in tokens when the batch changes, not
  `beta_2`. Both from `LIT-444` (Marek et al., `ARXIV-2507.07101`), read
  in `NOTE-194`.
- `THEORY-026` — critical batch size is set by how much data has been
  seen, not by how large the model is. Explains `SOTA-258`.

### Changed

- **`SOTA-097` is `Superseded`.** `B ∝ C^0.24`, from Kaplan's equation 1.7,
  has been carried since the record's first month, and its own body said the
  exponent "has not been re-derived by anyone since … a reason to hold it
  loosely". It has now been re-derived twice, by groups who did not
  coordinate, and the scaling variable is the token budget rather than
  compute.
- **`SOTA-062` is `Superseded`**, and retagged. Zhang et al. ran the
  decoupling experiment its body invited — hold the token budget fixed, vary
  model size — and the dependence very nearly vanishes.
- `SOTA-061` v2 — retagged `model-architecture` → `training-optimization`,
  the same mis-filing `SOTA-062` carried, from the same source paper.
- `SOTA-198` v2 — the disagreement it recorded with `SOTA-097` is resolved,
  and resolved in a way that vindicates its instrument: a gradient noise
  scale rising through a run is what growth in tokens seen looks like from
  inside the run.
- `SOTA-255` v2 — the gap its conditions named now has a candidate law, and
  the candidate is fitted in a disjoint regime. The record holds both and
  composes neither.
- `LIT-028` v3 — `corrected_by` the two new notes on the batch-size exponent.
  The paper stays `Active`; this is one exponent, not the work.

### Documentation

- **Two papers, two hyperparameters, one diagnosis.** `beta_2 = 0.95` is a
  decay per optimizer step and an optimizer step is not a fixed amount of
  data; `lambda = 0.1` is meaningless without the learning rate and the step
  count it multiplies. Both are ratios whose denominators were left out of
  the recipe, and both papers make the same move — name the denominator, and
  the constant becomes transferable.
- **What a confounded fit looks like from the outside.** Kaplan's batch
  exponent is not bad arithmetic. Along the Chinchilla line `C = 6ND` moves
  with `D`, so a power law in either describes the data. The tell is only
  visible with runs off that line: plot `B` against `C` and points at equal
  `D` fall on parallel lines rather than one. That is the same failure mode
  Chinchilla found in the allocation exponent, in a different coordinate.
- **Every batch-size practice the record held assumed bigger was the goal.**
  `SOTA-097`, `SOTA-062`, `SOTA-093`, `SOTA-198`, `SOTA-061` all ask how large
  a batch may usefully be. `SOTA-260` argues the target is the smallest
  that saturates the device. With `SOTA-258`'s ceiling the record now
  has a range with a reason at each end, which it did not have before.

### Added

- **The data-constrained cluster** (`#180`) — three papers that all answer
  one question the record had been arguing about without resolution: what to
  do when data, not compute, is the binding constraint.
- `SOTA-254` — train as masked diffusion when the corpus is fixed and
  the compute is not. `extends` `SOTA-157`, adding the condition that one
  lacked. Sources `LIT-442` (Prabhudesai et al., `ARXIV-2507.15857`),
  read in `NOTE-192`.
- `SOTA-255` — tune weight decay upward over a repeated corpus rather
  than inheriting 0.1. `SOTA-257` — ensemble independently seeded models
  and distil, rather than scaling one. `SOTA-256` — judge a monotone
  scaling recipe by its asymptote. All three from `LIT-441` (Kim et al.,
  `ARXIV-2509.14786`), read in `NOTE-191`.
- `THEORY-025` — a transformer holds about 3.6 bits per parameter, and
  generalization begins where the data outgrows that budget. Sources
  `LIT-440` (Morris et al., `ARXIV-2505.24832`), read in `NOTE-190`.
  `explains:` is empty on purpose.

### Changed

- `SOTA-171` v2 — the four-epoch bound was **reproduced independently** and
  relocated. Prabhudesai et al. re-ran the study with the objective swapped
  and recovered `R* = 31.93` for autoregressive training against `512.85` for
  masked diffusion. The number holds; it is a fact about the objective, not
  about repetition.
- `SOTA-173` v2 — the augmentation claim was **tested from outside its own
  source and the result points the other way**. Two of its three families,
  applied to an autoregressive arm in exactly the setting it describes, did
  not close the overfitting gap. Not a refutation — the claim is delay, not
  removal — and recorded as such.
- `SOTA-124` v4 — its linear-in-parameters conjecture is now half-checked.
  Capacity is measured linear in parameter count across three orders of
  magnitude; the *window*, a token count, still is not. `promote_when:`
  stands.
- `SOTA-157` v2 — gained a second line of evidence and a specialization.

### Documentation

- **The repetition dispute had a variable nobody was controlling.**
  `SOTA-124`, `SOTA-171` and `SOTA-173` all ask how far a corpus may be
  repeated, and between them report one setting of weight decay. Kim et al.
  find the optimum is roughly thirty times it, and that with it the loss curve
  stops turning up. None of the three measurements is wrong; they may all be
  measurements of the under-regularized case.
- **Three papers, three different remedies, one diagnosis.** `SOTA-173` said
  the overfitting belongs to the objective rather than to repetition. Both new
  sources agree with the diagnosis and neither adopts its remedy: one changes
  the objective, the other raises the regularization. That is the shape of a
  reframing outliving the recipe it arrived with.
- **`explains:` left empty on a theory, deliberately.** `THEORY-025`
  supplies the common unit the repetition dispute lacks — bits of data against
  bits of capacity — and the experiment that would connect it to multi-epoch
  overfitting has not been run by anyone. A finding that underwrites nothing
  yet is still a finding, and saying which is the honest version.

### Added

- **The theory under the record's optimizer cluster** (`#180`).
  `THEORY-024` — orthogonalising the update is *dualising* it, and muP
  and Shampoo are two partial approximations of the same duality map. Explains
  `SOTA-121`, `SOTA-143` and `SOTA-168`, none of which had an account.
- **Three `LIT` notes forming the line**: `LIT-437` (a spectral condition
  for feature learning), `LIT-436` (scalable optimization in the modular
  norm, `extends` it), `LIT-438` (modular duality, `extends` that).
  `NOTE-189` reads the last.

### Documentation

- **Ten practices mentioned Muon and the only source was a blog post.**
  `LIT-159`'s own standing called it "the clearest case yet for `ADR-009` —
  three laboratories pretrain frontier models with this and there is no paper
  to cite." The paper existed; it was the theory paper, and the record held
  neither it nor its two predecessors.
- **muP and Shampoo were filed from different literatures and are one
  object.** `LIT-438` §4.1 derives both as partial approximations to the
  duality map induced by the RMS–RMS operator norm. The record recommends both
  and had nothing connecting them — which is the shape `THEORY` exists for: it
  changes neither recommendation and changes what a reader understands on
  meeting the second.
- **Found from outside the record, which is new.** The trunk detector works by
  reading the record's own complaints about absences. Nothing here mentioned
  modular duality, the modular norm or the spectral condition — there was no
  complaint to find. The signal came from `#180`'s reading feed, where these
  three sit at 8 distinct days and 14 sessions each, near the top of 4,076
  papers. `DP-007` says agreement has no author and so no arrival event; here
  the arrival event was external.

### Added

- **`LIT-439`, the founding diffusion paper** (`#180`).
  Sohl-Dickstein et al. (2015), `extended_by` `LIT-036` (DDPM). The record
  held 62 documents mentioning diffusion and four practices about it, and not
  the paper the construction comes from. Carries no practice: the practices
  rest on what came later, and `SOTA-188` is sourced to EDM, which derives
  what this paper set by hand. What it supplies is the framing every later
  argument about schedules and samplers is conducted inside.

- **Two practices extracted from notes already read** (`#154` item 1).
  `SOTA-252` from `LIT-113` — make the full-resolution path affordable
  instead of upsampling, when the shortcut is what breaks correctness.
  `SOTA-253` from `LIT-111` — add a new instance by reconstructing it,
  not by training on it.

### Changed

- **`LIT-107` records its determination.** MiDaS v3.1's transferable claim is
  real — classification accuracy does not by itself pick a backbone for dense
  prediction — but what a practitioner does with it is run their own sweep,
  which the paper already says. Its durable contribution is the process for
  integrating a new backbone, which is infrastructure under `ADR-032`.

### Documentation

- **`#154`'s item 1 was the cheap half and it paid.** Three notes were read
  and unsourced in one neighbourhood; two carried recommendations nobody had
  extracted. That is the signature `#121` used to produce `SOTA-205`, run once
  more on the residue it left.
- **The upsampler rule turns on a distinction worth keeping.** A 2D upsampler
  is multi-view inconsistent *by construction* — a statement about what the
  operator can see, not about its average quality. `SOTA-249` is the mirror
  image: recomputation is the right shortcut precisely because it has no
  correctness defect. Step 3 of the pattern is what separates them.
- **`#180` mined; the ordering finding stands, the conclusion does not.**
  `dmarx/papers` does not exist; `dmarx/papers-feed` does, with 187 papers and
  **no revisit count** — the only engagement field is
  `total_reading_time_seconds`, whose median is 10 seconds and which is zero
  for 63 entries.
- **I ranked its candidates against `#137`'s criterion, and that was wrong.**
  That criterion — *something in the record has to be answerable from it* —
  belongs to `#137`, which was re-ranking papers proposed **as things the
  record needed**. A reading feed is an **input**: its papers are absent
  because they have not been filed yet, which is the premise rather than a
  disqualification. `ARXIV-1503.03585`, the founding diffusion paper, stays a
  live candidate rather than struck.
- **The error to avoid is importing a criterion past the boundary it was
  written for.** `#137`'s test was stated in `#137` and justified by `#137`'s
  framing. It is not a house rule; it became one in my hands because it had
  worked twice.

### Added

- **NeRF** (`#163`), `LIT-435` and its reading `NOTE-188`. The
  coordinate network `SOTA-205` exists to replace: that practice says to
  "replace a large coordinate network with a compact explicit structure and a
  small decoder", and all four of its sources — Instant-NGP, K-Planes, 3D
  Gaussian Splatting, NeuS2 — are responses to this paper. Two of them named
  it and the record could not follow the reference.

### Documentation

- **Carries no practice, deliberately.** The record's position on coordinate
  networks is `SOTA-205`'s and it is a recommendation *against* this design.
  Same shape as `LIT-428`, where `SOTA-167` holds the record's position on
  linear attention and the trunk note carries none of its own.
- **`#163`'s list measured against the record, same criterion as `#137`'s.**
  Fifteen items; NeRF is the only one with load-bearing dependents:

  | item | documents mentioning it |
  |---|--:|
  | NeRF | **4**, two of them `SOTA-205` sources |
  | Tensor Programs (TP-IV for muP) | 2 — but `SOTA-143` already sources TP-V, which *is* the muP paper |
  | interpolant / SiT | 3 |
  | Fourier features | 1 |
  | SIREN, StyleGAN, CycleGAN, Projected GAN, cold diffusion, diffusion forcing, SAE/logit lens, ReFT, structured-output sampling | **0 each** |

  The same shape `#137` ended in: the top of the list is load-bearing and the
  tail has no dependents at all. The issue's "at very least add TP-IV for
  muP" is already satisfied one paper along — `LIT-148` is TP-V and
  `SOTA-143` parameterizes with µP from it.

### Added

- **The record's first statement about how a visual encoder gets pretrained**
  (`#85`, `#154`). `SOTA-250` — predict the representations of masked
  regions, not their pixels — sourced to `LIT-216` (I-JEPA). Twenty-one `LIT`
  notes carried `vision-and-graphics` and all three practices that did were
  downstream of an encoder: scene representation (`SOTA-205`) and geometry
  estimation (`SOTA-236`, `SOTA-237`).
- **`SOTA-251`, `Proposed`** — train at low resolution and raise it only
  during the decay phase of a warmup-stable-decay schedule, `extends`
  `SOTA-140`. Up to 8x less pretraining compute in `LIT-215`'s measurement.
- **Three readings**: `NOTE-185` (`LIT-216`), `NOTE-186`
  (`LIT-215`), `NOTE-187` (`LIT-218`).

### Documentation

- **The transferable rule in a video paper turned out to be about
  schedules.** `LIT-215`'s progressive-resolution result belongs to
  `training-optimization`, not to vision, and it only makes sense against a
  schedule with a distinct decay phase — which is why it `extends` `SOTA-140`
  rather than standing alone. `ADR-026`'s filing rule in its purest form: the
  claim takes its kind, not the domain it was discovered in.
- **The record now holds both live bets on general visual understanding.**
  `LIT-216` and `LIT-215` predict representations and refuse to generate;
  `LIT-218` generates and gets representations as a side effect. `LIT-216`'s
  own Figure 2 taxonomy names the distinction years before the generative side
  looked like it was winning.
- **`LIT-218` carries no practice and is not close.** One proprietary model,
  no recipe, no ablation — `DP-005` puts that in the adoption column. What it
  is for is that a corpus holding only the joint-embedding line would read as
  though the question were settled.
- **One lab, twice, is not two groups agreeing.** `LIT-215` scales `LIT-216`'s
  construction and shares authors with it, so it is named in
  `SOTA-250`'s `consensus_note` rather than its `source:` — `ADR-017`,
  since the recommendation survives losing it.

### Added

- **Three readings, which is the work `#85`'s audit existed to identify**
  (`#85`). `NOTE-184` for `LIT-004` (gradient checkpointing),
  `NOTE-182` for `LIT-055` (P-Tuning v2) and `NOTE-183` for
  `LIT-095` (LPIPS). All three were the residue after the audit half closed:
  unsourced, unread, and in force.

### Changed

- **`LIT-004` v4, `LIT-055` v3, `LIT-095` v3** — each now names its reading
  and says what the reading changed.

### Documentation

- **Two PEFT families reached the same conclusion four years apart, and the
  record can now say so.** P-Tuning v2 finds that prompt *depth* closes the
  gap to fine-tuning while reparameterization — the knob prior work tuned —
  is inconsistent across datasets. QLoRA (`SOTA-231`) finds that the *number
  of adapted matrices* closes it while the rank `r` — the knob people tune —
  has no effect across its sweep. Coverage decides; the tuned knob does not.
- **Not recorded as replication, deliberately.** Different mechanism,
  different setting, four years apart. `ADR-010` says contrast is not
  support; the cousin is that structural agreement is not measurement either,
  so `SOTA-231` stays `unreplicated`.
- **Every reading confirmed the determination its note already carried.**
  None of the three produced a practice, and all three now say *why* more
  precisely — `LIT-095`'s most transferable claim turns out to be a negative
  one (the effect survives losing VGG, ImageNet and supervision, and does not
  survive losing training), and `LIT-004`'s allocation half is framework work
  rather than a decision a person makes.
- **`LIT-040` was a false positive in the bare-note query**, not a gap. It
  has carried a full determination and a reading (`NOTE-072`) since
  2026-09-10; the query's regex missed "nothing is filed from this reading".

### Added

- **`SOTA-249`: recompute activations from a `sqrt(n)` subset of
  checkpoints when activation memory is the binding constraint** (`#85`),
  sourced to `LIT-004`. `consensus: universal`. The record recommended
  recomputation only for attention (`SOTA-087`), while the memory accounting
  underneath `SOTA-017`, `SOTA-019` and `SOTA-031` assumed activations were
  recomputed with nothing saying so.

### Changed

- **`LIT-004` v3.** Its four category-naming bullets — "introduces gradient
  checkpointing", "trade-off between memory and computation" — are replaced
  by the method and its numbers: `O(sqrt(n))` memory for one extra forward
  pass per minibatch, `O(log n)` for `O(n log n)`, and a 1,000-layer ResNet
  at 48G → 7G for 30% more running time.
- **`SOTA-087` v4** gains `extends: SOTA-249`. Its v3 note said it was
  tagged `systems-optimization` because "trading recomputation for stored
  activations is a memory-access decision, and it is what its line holds in
  common" — that line now has its earliest member. The recommendation, the
  source and the `ADR-029` attribution split are unchanged.

### Documentation

- **`#85`'s audit half is done and the issue's own numbers are stale.**
  Re-measured over `LIT-001..118`: 79 of 118 source a practice or theory,
  39 are unsourced, 12 of those are retired, and **1** is bare with no
  written determination. The issue was filed at 53 bare.
- **Three inherited notes remain both unsourced and unread**: `LIT-004`
  (now filed from), `LIT-055` (P-Tuning v2) and `LIT-095` (LPIPS). `LIT-185`
  (EAGLE-3), which the issue singled out, is now both sourced and read.
- **Filing from an abstract is not the failure `#121` declined to commit.**
  That pass refused to file from four bullets *describing a category*, which
  was right. The input changed rather than the judgement: the paper's own
  abstract states the algorithm, both asymptotics and a measured
  before-and-after. `LIT-004` stays `Unread` and says so.

### Documentation

- **Every declared relation is now checked in both directions** (`#84`). Ten
  inverse queries over `extends`/`extended_by`, `compared_against`,
  `corrects`/`corrected_by`, `explains`/`explained_by`, `contested_by`,
  `introduced_by` and `NOTE.paper`. Seven return zero, and structurally:
  `luria link --fix` derives each converse from whichever end declares it, so
  the symmetry class is the tool's guarantee rather than the contributors'.
- **Three of the queries had the wrong premise, which is `DP-004` turned on
  itself.** `corrects` does not imply the corrected document is retired —
  fourteen instances, every one already annotated `Corrective succession
  (ADR-017)`, because the corrector is conditional on the corrected. And
  `introduced_by` is *designed* not to be a subset of `source:`; that
  separation is `ADR-029`. A pass finds only defects its query is shaped
  like, and the inverse pass can be mis-shaped in the inverse direction.
- **A query over prose that looks for codes asks whether a document was
  linked, not whether it was discussed.** Eleven of fourteen
  `compared_against` pairs with "no trace in either body" narrate the
  comparison by paper name — `LIT-230`, `LIT-233` and `LIT-235` mention
  DeepSeekMath or GRPO eight to twelve times each.
- **Three `compared_against` groups joining practices drawn from one paper**
  are left standing and raised rather than fixed: `SOTA-040`/`041`,
  `SOTA-061`/`062`, and `SOTA-010`/`011`/`012`, whose own comment calls it a
  record that "three readings of one figure were filed together". `ADR-011`
  says the field means somebody ran the comparison; shared `source:` already
  carries the sibling fact. Whether the record wants a sibling relation is a
  decision, not a sweep.

### Fixed

- **`LIT-180` v2 said Qwen3 was unfiled; `LIT-182` is the Qwen3 technical
  report and was filed the same day**, two numbers along in the same batch.
  Wrong when written rather than aged into wrongness — a claim about the
  record's own contents, made while the batch making it false was still
  landing.
- **`LIT-181` v2 asked for a practice the record already carries.** Its
  Standing section said the agreement across the hyper-connections papers was
  "probably the practice the record should eventually carry"; `SOTA-169` is
  that practice, filed three days later and sourcing this note. The request
  stood for eleven days after it was answered.

### Documentation

- **`#86`'s second query, the exegesis detector, is run and found nothing to
  act on.** Fifteen Standing sections explain another document's decision;
  ten have a practice or theory sourced to them, and every one of the
  remaining five states in its own body why it carries none — `LIT-101`
  (unproven, and the absence is the information), `LIT-161` (successor
  already carried), `LIT-199` (origin of a unit the record recommends a
  variant of), `LIT-406` and `LIT-428`. The `#40` reference pass had already
  converted this class into `SOTA-153`, `SOTA-161` and `SOTA-163`.
- **Both fixes above are the same defect as the one `#86`'s first query
  found**, and it is not about papers. A claim about the record's own
  contents — "X is not filed", "the record should carry Y" — has no code,
  resolves to nothing, and is therefore invisible to every check luria runs.
  The lint can see a citation pointing at a retired document. It cannot see a
  paragraph that is wrong about what the record holds.

### Added

- **The RLHF lineage `LIT-377` named as open** (`#86`). Three `LIT` notes
  carrying no practice under `ADR-032`: Christiano et al. 2017
  (`ARXIV-1706.03741`, learning from human preferences), Stiennon et al. 2020
  (`ARXIV-2009.01325`, the same loop on summarization) and Wei et al. 2021
  (`ARXIV-2109.01652`, FLAN). The reading list now renders preference
  learning → summarization → general instruction following, with FLAN
  alongside as the arm InstructGPT measured itself against.

### Changed

- **`LIT-377` v2** gains `extends: LIT-433` and
  `compared_against: LIT-432`, and its closing paragraph now says what
  closed rather than what is missing.

### Documentation

- **Five documents depended on a construction none of them could name.**
  `LIT-169` is a claim about what InstructGPT's reward model secretly is,
  `LIT-082` replaces its human labels with model-written ones, `SOTA-183` is
  that replacement as a practice, `SOTA-126` tunes the schedule of the method
  that removed the explicit reward model — and the loop they all assume was
  introduced on Atari and simulated locomotion, with no language model in it.
- **The gap was found by running `#86`'s trunk detector**, not by anyone
  noticing. `LIT-377` had written the three papers down as open in its own
  Standing section three days earlier. A request in prose carries no code and
  resolves to nothing, so no check could raise it — `DP-004` about the
  record's own prose rather than about a search.
- **`compared_against` rather than `extends` for FLAN**, under `ADR-011`:
  somebody ran that comparison, and InstructGPT is not built on it. The
  record already held the result — FLAN at 29.8 ± 2% against InstructGPT's
  73.4 ± 2% — and `NOTE-161` already held the assumption that makes it
  narrower than it reads, that the prompts were the API's rather than
  academic task types. What was missing was the arm that lost.

### Added

- **The RWKV lineage, and the linear-attention trunk under it** (`#161`).
  Four `LIT` notes carrying no practice under `ADR-032`: Katharopoulos et al.
  2020 (`ARXIV-2006.16236`, linear attention), Zhai et al. 2021
  (`ARXIV-2105.14103`, AFT), Peng et al. 2023 (`ARXIV-2305.13048`, RWKV-4)
  and Peng et al. 2024 (`ARXIV-2404.05892`, Eagle and Finch). With `LIT-173`
  at its head the reading list now renders a five-step line from linear
  attention to RWKV-7.

### Documentation

- **The record argued about linear attention in twelve documents and could
  not cite its source.** `LIT-194` ("no decay term, so it cannot forget"),
  `LIT-176` ("compromises recall over long contexts"), `LIT-195` ("lacks
  precise associative recall"), `SOTA-132`, `SOTA-153` and `LIT-165` are all
  claims about what one 2020 construction gives up. `DP-007` — agreement has
  no author — and the sharpest instance of it the record has filed.
- **`SOTA-178`'s evidence base is now legible.** Its conditions section reads
  "RWKV-7 'Goose', 0.19B to 2.9B. Nothing else in the record", which is a
  different claim depending on whether that architecture is a one-off or the
  current member of a line scaled and re-derived four times. It is the
  second. `SOTA-135`'s "independently and a year earlier" and `LIT-194`'s
  timing claim are also about papers the record did not hold.

### Changed

- **The unbound-lineage report is empty: 0 relations and 0 lines**, from 22
  and 10. Twenty-one documents gained a topic they were already about, in
  seven groups — the evolution-strategies line, the SSM/delta-rule line,
  early-training instability, batch size, the flash-attention kernels, and
  the query/key interventions. Every addition passed `ADR-046`'s test; the
  relation is what pointed at it.
- **`groups.primary_topic` removed from all three schemes.** It listed
  thirteen of fourteen topics under `require: any`, which luria documents as
  *"the group is a label, not an axis"* — it constrained nothing. Its comment
  still claimed *"the topic consolidation, enforced"*, true before `ADR-035`
  relaxed it from `exactly-one`, and once inert its membership drifted:
  `tiny-models` was added to the vocabulary and never to the list, so the
  config quietly said a document about small models has no primary topic.

### Documentation

- **`ADR-049` supersedes `ADR-048`**: unbound is never the resting state.
  A relation asserts a commonality, so if a chain exists the commonality
  exists — which makes an unbound relation one of exactly two defects, *the
  invariant is missing* or *the relation is wrong*, and never a third where
  the answer is to note that somebody looked.
- `SOTA-085`'s standing request is answered. Its frontmatter recorded a tag
  removed for binding its edge to `SOTA-083`, asking that the crossing *"keep
  showing up until someone answers it."* Flash attention is a custom kernel;
  the tag was missing, not forbidden.

### Fixed

- **`ADR-018` v3 and `ADR-044` v2 stop quoting the lockfile's size as a
  number.** Both said `remotes.lock.json` held **305 `titles` entries**, and
  `ADR-044` added **921 lines**. The entry count was wrong when written —
  measured on a branch carrying two entries `main` did not have — and both
  figures have drifted since, to 319 and 963 as of this contribution.

  Neither argument ever needed the figures. What they are about is that the
  file is **one file holding one entry per cited identifier, rewritten by
  every contribution that files a paper**, which is true at any size. The
  numbers survive only in the `history:` notes, where a superseded figure
  belongs.

### Added

- **Every relation now says what it means.** All twenty-one references across
  `SOTA`, `THEORY`, `LIT` and `NOTE` carry a `label:` and a `blurb:`
  (`ADR-047`). They render on the generated contract page, which until
  now glossed `status`, `consensus` and `tags` while showing every relation
  as a bare type declaration. luria has supported these keys since `LU-#254`
  and no record had used them.

### Changed

- **`SOTA-085` and `SOTA-106` now `extend` `SOTA-083`** rather than being
  `compared_against` it. Flash attention is an instance of *implement custom
  kernels for critical ops*; nobody ran a comparison between them, which is
  what `ADR-011` says that field asserts. The practice line now reads: custom
  kernels → flash attention → flash-attention-2, with the FP32 rule beside
  it. `SOTA-106`'s direct edge to `SOTA-083` is dropped as transitive.
- The unbound-lineage report goes from 16 relations to **15**.

### Documentation

- **`extends` is not split, and `specializes:` is not added.** Writing the
  blurb answered it: a later version, a narrower case and a rule that only
  exists because the earlier one is followed are one assertion — *B carries
  A's claim further and does not stand without A* — and the line reads
  oldest-first in all three. `ADR-036` and `ADR-048` both asked for the
  new relation; that request is withdrawn.

### Changed

- **Six documents gain a topic they always warranted**, closing six unbound
  relations. `LIT-187` (GShard) gains `model-architecture`; `LIT-162`
  (Mamba-2) gains `attention-techniques`; `LIT-137` (Gated Delta Networks)
  gains `model-architecture`; `LIT-127` (DeepSeekMath) gains
  `training-optimization` and `data-pipeline`; `LIT-200` (PowLU) gains
  `model-architecture`; `SOTA-032` (pre-LN) gains `model-architecture`. No
  primary topic moves — every addition is second or later.
- The unbound-lineage report goes from **22 relations and 10 lines** to
  **16 and 8**.

### Documentation

- **`ADR-036` is superseded by `ADR-048`**, in one category of four. Its
  classification, its fifteen retags and its two removed sibling links all
  stand. What changed is its verdict on **trunk papers whose contribution
  spans two topics**, left standing because *"splitting a trunk paper's topic
  would be filing it under half its contribution"* — true, and an argument
  against splitting rather than against tagging. `ADR-046` made splitting
  unnecessary: a paper that does two things carries two topics.
- The successor records what it **declined** to retag, because a pass that
  reports only its additions is not auditable. The seven
  `analysis-and-evaluation` crossings stay unbound — `ADR-036` decided that
  and the fix belongs to the chain declaration. The flash-attention edges stay
  unbound because `SOTA-085`'s own frontmatter records a tag *removed* for
  binding them, with the note that the edge *"should keep showing up until
  someone answers it"*. And `SOTA-031` keeps one tag because its claim is
  about memory per device, not training dynamics.
- **A `specializes:` relation is the highest-value scheme change the report is
  asking for**, and it asks twice. `ADR-036` named it first; liberal tagging
  did not make it go away.

### Added

- **SmolLM2** (Ben Allal et al. 2025, `ARXIV-2502.02737`) — the model report
  behind SmolLM2-135M-Instruct, which is the base `LIT-129`'s whole
  experiment runs on. `LIT` carrying no practice, `ADR-032`. The last entry
  on `#137`'s list that meets that issue's own filing criterion.

### Changed

- The luria pin moves to **0.28.2** across `docs.yml` and `pages.yml` — ten
  action refs and pip specs. Picks up two fixes: a 406 from a metadata remote
  now classifies as a throttle rather than an outage, so a refusing host is
  asked once per run instead of once per identifier; and luria now sends
  `luria/<version>` rather than `Python-urllib/3.11`. The `0.28.0` at
  `docs.yml:110` is a statement about history and stays as it is.

### Documentation

- **`#137` is finished, and nine of its remaining ten entries are struck
  rather than filed.** PRM800K, MATH-Beyond, DeepSeek LLM, Meyerson et al.,
  MiniPile, Brax, Craftax, NAVIX and JaxMARL have **zero** mentions in this
  record, which is exactly what that issue's stated criterion excludes: *a
  benchmark nothing here is argued on has no standing to record.* The issue
  anticipated this for the four RL environments; it turns out to be true of
  five more.

### Changed

- **`LIT-425` v2** (T5/C4) gains `model-architecture` and
  `adaptation-and-tuning`. It was filed a contribution ago with
  `data-pipeline` alone, on the reasoning that the record holds the paper for
  its corpus. That confused the record's motive with the document's subject:
  the text-to-text framework and the transfer-learning ablation are most of
  the paper, and a reader browsing either topic had no way to find it.
- **`LIT-426` v2** (The Pile) gains `analysis-and-evaluation`. The paper
  argues diversity improves downstream performance and measures it across
  held-out components, which is an evaluation claim as much as a corpus
  description.

### Documentation

- **`ADR-046`** — tag for what a document is about, liberally, rather
  than for why the record went and got it. `ADR-035` stands: the first tag is
  still primary, and adding one *in order to bind a relation* is still
  forbidden. What is new is that the forbidden case is narrow — an invariant
  binds an edge only where a relation is declared, and neither of the notes
  above declares one — so that warning should not have been read as a general
  brake on second tags. The costs are asymmetric: an extra true tag adds an
  index row, a missing one makes a document unfindable with nothing in any
  report to say so.

### Added

- **C4**, via the T5 paper that introduced it (Raffel et al. 2019,
  `ARXIV-1910.10683`). Forty-six documents here train on C4 and the paper was
  absent from the record entirely. `LIT` carrying no practice, `ADR-032`.
- **The Pile** (Gao et al. 2020, `ARXIV-2101.00027`). Only five documents cite
  it, well below where this record usually draws the line — filed for what
  those five do with it, which is measure the whole data-mixing line against
  its default weights.

### Changed

- `SOTA-164` v2 names C4 and adds the point that gives its two-granularity
  argument its force: C4 shipped already deduplicated by its own authors, and
  `LIT-202` found a 61-word sentence repeated thousands of times in it
  anyway. Recommendation unchanged.
- `SOTA-238` v2 reads its own denominator. The **+6.5 points** is measured
  over The Pile's default weights — a judgement its authors made and never
  claimed was optimal — so the gain is partly a property of the baseline.
  Recommendation and consensus unchanged.

### Documentation

- C4 plays two roles here and they want different caveats. As **a corpus with
  a known defect** it is load-bearing: `SOTA-164`'s evidence is a fact about
  C4 specifically. As **a standard workload** for distributed and
  communication-efficient results (`SOTA-155`, `LIT-212`, `LIT-252`,
  `LIT-276`, `THEORY-014`) nothing depends on it being C4 — it is there
  because everyone else used it, which is `DP-007`.

### Added

- The four datasets most of this record's optimizer, compression and
  distributed-training evidence is measured on, none of which it held. All
  four are `LIT` carrying no practice under `ADR-032`.
  **ImageNet** the database (Deng et al. 2009, `DOI-10.1109/CVPR.2009.5206848`)
  and **ILSVRC** the challenge (Russakovsky et al. 2014, `ARXIV-1409.0575`)
  are filed separately, because they are separate things and the record's
  seventy-four "ImageNet" mentions run across both plus ImageNet-64.
  **CIFAR-10/100** (Krizhevsky 2009, technical report) and **MNIST** (LeCun
  et al. 1998, `DOI-10.1109/5.726791`) complete the set.

### Changed

- `SOTA-221` v2 names ILSVRC as the instrument behind its ImageNet/ResNet-50
  comparison at 16K, rather than leaving "ImageNet" to mean one of three
  things. Recommendation and evidence unchanged.
- `SOTA-222` v2 points its existing CIFAR-10-versus-ImageNet caveat at the
  CIFAR note. The practice already recorded that the paper's experiments are
  CIFAR-10 while the claim is pitched at ImageNet scale; that gap now has a
  document behind it.

### Documentation

- **"ImageNet" names three instruments in this record and now says which.**
  A classification top-1 number is ILSVRC's thousand-class challenge;
  ImageNet-64 is a downsampled generative set scored on FID; TinyImageNet is
  a third thing. Ten documents use the last two. Third instance of one name
  over several instruments, after ARC-AGI/AI2 ARC and BBH/BIG-bench.
- The MNIST note records what MNIST is actually *for* in this record: not a
  performance claim — nothing here cites an MNIST accuracy as evidence a
  method is good — but the scale at which leave-one-out retraining and
  exhaustive subsampling are affordable. `LIT-058`'s MNIST-and-ImageNet
  subsampling is what put `THEORY-013` in the attic, and is what `SOTA-218`
  rests on.

### Added

- Three references from `#137`'s backlog, all filed as `LIT` carrying no
  practice under `ADR-032`. **BBH** (Suzgun et al. 2022, `ARXIV-2210.09261`) —
  the 23 BIG-bench tasks where models had not yet beaten the average human
  rater, and the instrument `SOTA-235`'s central argument turns on.
  **OlympiadBench** (He et al. 2024, `ARXIV-2402.14008`) — the benchmark
  `ADR-032` named as its worked example of a bound the record had nowhere to
  write down. **HybridFlow / verl** (Sheng et al. 2024,
  `ARXIV-2409.19256`) — one of the four references `ADR-032` put at the top of
  the queue it opened.

### Changed

- `SOTA-235` v3 names the BBH instrument rather than asserting what it is, and
  carries the qualifier the new note adds: a BBH number is unusually
  prompt-sensitive, and the comparison this practice draws holds because both
  of its conditions are 10-shot.
- `SOTA-154` v4 gains a third caveat on its 32B evidence. Two were already
  there — published checkpoints rather than budget-matched runs, and a single
  lab. The third is the benchmark's own dynamic range: the best model at
  OlympiadBench's publication scored 17.97%, so a separation measured there is
  measured near the bottom of the scale.

### Documentation

- **BBH is not BIG-bench**, and the record now says so. `LIT-077` is the
  204-task suite that `SOTA-200` and `SOTA-197` are argued from; the new note
  is the 23-task hard split that seven other documents report numbers on. The
  same subset-versus-suite confusion `LIT-405` and `LIT-407` were filed to
  settle for ARC.

### Added

The benchmark tier of [#137](https://github.com/dmarx/anthology-of-the-sota/issues/137), finished. All three carry no practice and no
reading, per `ADR-032` and `ADR-025`.

- `LIT-415` — **Stream of Search**, filed for its *task*. Countdown is
  what twenty-three documents here report on; the method is cited zero times.
  Its note records what Countdown buys (a reward computable by evaluating the
  answer), what it costs (bounded symbolic search and nothing else), and that
  this record's own evidence says it behaves unlike its neighbours —
  `NOTE-082` has ES peaking quickly on every task *except* Countdown.
- `LIT-411` — **MATH**. Every problem ships a worked solution, so the
  dataset is a training signal as well as a benchmark and a number quoted
  without saying which is ambiguous. `MATH-500` is a later convention, not
  this paper's split.
- `LIT-416` — **GPQA**. Two bounds worth having: domain experts reach
  **65%**, so the ceiling is not 100%; and 448 items make one question worth
  0.22 points, so a one-point difference is below the instrument's
  granularity.

### Changed

- Pinned to `luria==0.28.1` and the action refs to `@0.28.1`, which brings
  **grouped chain pages**: `docs/practice-lines.md` and `docs/lineage.md` now
  section by the `invariant: tags` each chain already declared, instead of
  rendering in the order the component walk produced. 11 sections on the
  practice lines, 7 on the reading list.
- Nothing in this record changes — both chains have declared `invariant: tags`
  since they were written. The declaration was checked and unused by the view;
  now the view uses it (`LU-ADR-113`).
- The `Sharing no \`tags\`` section is the part worth reading. On the reading
  list it holds four lines, and they are **the ones this record's own config
  predicted** — Mamba, the MoE line, the RoPE papers — written there as "the
  ordinary state of a lineage that crosses a fault line in the vocabulary".
  That prediction is now visible on the page rather than only in a comment.

### Added

Five from [#137](https://github.com/dmarx/anthology-of-the-sota/issues/137)'s worklist, re-ranked against the whole corpus rather than the
twelve evolution-strategies papers the issue's counts came from. All carry no
practice and no reading, per `ADR-032` and `ADR-025`.

- `LIT-406` — **Qwen2.5 Technical Report**. Named in forty-five documents
  here, the most-cited thing the record did not hold. The record already had
  Qwen3, Qwen3.8 and Qwen2.5-Coder: the successors and a sibling, not the base
  everyone measures against.
- `LIT-405` — **Chollet, On the Measure of Intelligence**, which
  introduces ARC-AGI.
- `LIT-407` — **Clark et al., the AI2 Reasoning Challenge**, which is a
  different benchmark with the same acronym.
- `LIT-404` — **HellaSwag**, whose distractors are adversarially filtered
  against 2019's models, so its difficulty is relative to them.
- `LIT-408` — **MBPP**, the other half of the code-generation pair whose
  first half (`LIT-388`, HumanEval) was already filed.

### Changed

- `SOTA-235` v2 and `LIT-379` v2 — **ARC disambiguated to ARC-AGI.** The
  record used one acronym for two unrelated benchmarks: ten documents mean the
  AI2 Reasoning Challenge, and this practice's headline — 53.0%, up to 6×
  fine-tuned baselines — is on Chollet's puzzle set. A result is only as
  legible as what it was measured on.

### Changed

- **The identifier lockfile is written on `main`, not on branches.**
  `docs-generate` now passes `resolve: "true"` beside `concretize` and the
  views, so `luria remotes --resolve` records what upstream says each cited
  identifier is at the serialization point. Until luria 0.28.0 the *lint*
  wrote `remotes.lock.json`, and the lint runs everywhere — so every
  paper-filing branch carried a diff on a 305-entry file and two such branches
  conflicted over nothing. See `ADR-044`, and `LU-DP-002` for the rule.
- The lint still **asks** on a pull request, so `source-mismatch` still fails
  before a merge. Only the write moved.
- Pins to `luria==0.28.0` and the three action refs to `@0.28.0`. The `lint`
  and `site` actions are byte-identical between 0.25.0 and 0.28.0; the bump
  buys one version to reason about.

### Changed

- `ADR-018` v2 — names the principle it is an instance of. It was filed
  citing `LU-ADR-068` as a shape to adopt, which is precedent rather than a
  rule, so when the same problem arrived on a second artifact — the
  identifier lockfile — it was argued from scratch instead of recognised.
  `LU-DP-002` v3 now states it: **one artifact, one writer, and the writer is
  wherever merges serialize.** The decision itself is unchanged.

### Added

- `LIT-403` (Koh and Liang 2017, read in `NOTE-181`),
  `LIT-400` (TracIn, `NOTE-180`), `LIT-401` (Grosse et al.
  2023, `NOTE-178`) and `LIT-402` (Bae et al. 2022,
  `NOTE-179`) — training-data attribution, which the record held nothing
  on. The origin, the checkpoint-based alternative, the version that reaches
  52B parameters, and the paper that says what any of them measure.
- `THEORY-017` (`Rejected`) and `THEORY-018` (`Active`) — the
  account influence functions were derived from, that the estimate predicts
  the effect of removing a point and retraining, and its replacement: on
  neural networks the estimate tracks the proximal Bregman response function.
  Three of the five terms in the discrepancy are not error, they are a
  different question.
- `SOTA-246` (`Proposed`) — find mislabelled training data by
  self-influence rather than by training loss. Survives the correction above,
  because it needs an ordering over training points and never needed the
  counterfactual; `LIT-402` says so explicitly, which is why it is in
  `source:`.
- `SOTA-245` (`Proposed`) — state a relation in both orders in the
  corpus if you want it usable in both directions. A training sequence
  influences a completion only when the prompt-related phrase comes first;
  identical content reversed scores barely above an unrelated baseline.

### Added

- `LIT-399` (Sorscher et al. 2022, read in `NOTE-176`) and
  `SOTA-243` (`Proposed`) — power-law scaling in dataset size is a
  measurement of redundancy, and given a difficulty ranking it can be beaten
  toward exponential. Which end of the ranking to discard **inverts** with
  data abundance: keep hard examples when data is plentiful, easy ones when
  it is scarce, where keeping the hardest does worse than random pruning.
- `LIT-397` (Paul et al. 2021, read in `NOTE-177`) and
  `SOTA-244` (`Proposed`) — the importance ranking is available from a
  single early checkpoint averaged over several initializations, not only
  from a finished run, and it transfers across architectures.
- `LIT-398` (DCLM) — carries no practice, deliberately. The position
  `SOTA-170` argues against, which the record had been arguing against
  without holding.

### Changed

- `SOTA-170` v2 — DCLM named by code now that the record holds it. It stays
  out of `source:` under `ADR-010`: contrast is not support.

### Added

- `THEORY-022` — a phrase placed in a word slot is read as a lemma, and
  the reading comes from the construction rather than the phrase's frequency.
  Four preregistered surveys measure the reading; the fourth removes the
  obvious deflation, reproducing every effect on high-frequency phrases only,
  with estimated corpus frequency predicting nothing. So the lexical unit is
  delimited by construction, not by how often the string has been seen —
  which is the assumption `SOTA-007`'s frequency-merge vocabulary makes.
  `explains:` is empty and the document says why.
- `LIT-410` — Goldberg and Shirtz (2025), the English phrase-as-lemma
  construction (`a don't-mess-with-me driver`). Sources the theory above and
  no practice: knowing the data contains construction-delimited units says
  nothing about whether a vocabulary should hold them, which is a cost
  question nobody here has measured.
- `ADR-045` — the scope question filing it forced, `Proposed`. A document
  is filed by the kind of claim it makes, not by the instrument that produced
  it, so a finding about the signal is a `THEORY` whether it was measured on a
  GPU or on 755 people. The record already held physics, control theory and
  pure mathematics, so "outside CS" was never the boundary; what changed is
  that the apparatus stopped being treated as the question. Rejected, and
  recorded because it looked right: admitting it as a note that sources
  nothing, on a special rule.
- `LIT-417` — Lad et al. (2024), the layer deletion and swap study.
  Deleting a layer outright, or swapping two adjacent ones, at inference and
  without fine-tuning, leaves 72-95% of top-1 predictions unchanged — but the
  damage is localized: the first and last layers are fragile, the middle is
  not, and swapping hurts less than dropping. It sources two theories rather
  than one, because the paper's measurement and the framework it proposes do
  not have the same evidence behind them, and the paper says so with a
  question mark in its own title.
- `THEORY-020` (`Active`) — layer importance is not uniform with depth.
  The measurement: every layer intervened on in turn across four GPT-2 and
  four Pythia models, scored by KL divergence and prediction agreement, and
  confirmed on HellaSwag, ARC-Easy and LAMBADA. Robustness grows with depth,
  so it is not small-model slack. `explains:` is empty and the document says
  why: measuring sensitivity by deleting a layer and shipping a model without
  one are different claims.
- `THEORY-023` (`Proposed`) — the four stages, of which detokenization is
  the first. Filed at the weaker status because it is one measurement, one
  experiment, one structural argument and two interpolations; `promote_when`
  asks for a stage boundary predicted *before* it is tested, since a framework
  with approximate boundaries and co-occurring stages is otherwise hard to
  falsify.
- `LIT-412` and `LIT-409` — the inner-lexicon line, which the two
  preceding theory documents both named as the gap standing between the record
  and a claim it wanted to make. Kaplan et al. (2024) show models recombine
  sub-word sequences into whole-word representations at a unit's last token,
  with the control that settles it: a probe on the last token separates words
  from positionally-matched nonwords at 89%, the same probe on the penultimate
  token at 61%. Feucht et al. (2024) find the erasure signature of the same
  mechanism, and count named entities and non-compositional multi-word
  expressions as lexical items.
- `THEORY-021` (`Active`) — a model builds a latent vocabulary in its
  early layers whose units are not the tokenizer's. Three groups, three
  methods: a probe with a co-occurrence control, an erasure signature, and
  layer ablation. The units survive arbitrary splits, typos and
  out-of-vocabulary words, so the tokenizer's vocabulary is the input format
  rather than the inventory.
- `SOTA-247` (`Proposed`, `unreplicated`) — add a multi-token word to a
  frozen model's vocabulary from the model's own detokenized representation of
  it. The frozen model uses the new entries and keeps its accuracy on the old
  ones (0.519 against 0.522 on WikiText-103), where mean-embedding
  initialization does neither. Largest gain where the tokenizer is worst:
  Arabic, 0.402 new-token accuracy against 0.117. The practice states what the
  paper's "finetuning-free" understates — the core parameters are frozen and
  two refinement matrices are still trained on 20M tokens — and `promote_when`
  asks for the serving measurement nobody has reported.
- `THEORY-019` (`Active`) — a softmax head with nothing to attend to must
  place its mass somewhere, so models learn a positional sink. Filed from
  `LIT-191`, which the record had held for ten days while advising people to
  remove the phenomenon it describes. It `explains: SOTA-134`: the gate and
  the streaming fix are answers to the same pressure from opposite ends, which
  is why the gate removes sinks rather than relocating them.

### Changed

- `SOTA-134` gains `explained_by:`, written by `luria link --fix`. The
  practice's body already argued the mechanism in prose; it now points at the
  document that holds it.
- `LIT-414` — Bondarenko et al. (2023), the quantization-side diagnosis
  of the same mechanism: a head approximating a no-op must drive its softmax
  input to extremes, which is what makes the activation outliers that break
  INT8. Two remedies, both measured. BERT-base W8A8 perplexity 1294 → 4.55 and
  max infinity-norm 735 → 20, with the FP16 model slightly *better*.
- `LIT-413` — Miller (2023), "Attention Is Off By One". The version most
  people have read, filed for provenance and reach rather than evidence: it
  reports no experiments and says so.
- `SOTA-248` (`Proposed`, `unreplicated`) — stretch and clip the softmax
  so a head can output exact zeros. Architectural, has to be pre-trained in,
  and evidenced only at 109M/125M/22M, which is why it is `Proposed`.

### Changed

- **`SOTA-134`'s origin is corrected.** It was filed with
  `introduced_by: LIT-138` (Qiu et al. 2025). Bondarenko et al. (2023)
  equation 5 is the same gate, per-head, two years earlier — and Qiu et al.
  say so: "The work most closely related to ours is Quantizable Transformers
  ... Building on these insights, we scale up gated attention models."
  `introduced_by:` now names the 2023 paper; `source:` keeps Qiu et al. first
  and gains Bondarenko et al., which measured the gate as well as proposing
  it. The recommendation is unchanged, and so is its `Active` status.

  It also relocates the claim: the gate was introduced to let a head do
  nothing so it would stop breaking quantization, and the quality gain is a
  later discovery about it.
- `SOTA-134` gains `explained_by:`, written by `luria link --fix`.

### Added

- `ADR-043` (`Proposed`) — doubt about whether an item is worth carrying
  is not a reason to leave it out, and not a third kind of provisional.
  `DP-006` covers a claim you doubt; this covers a claim you believe but are
  unsure the record wants. Writing the `promote_when:` dissolves the second
  into the first, and where no condition can be written the item was an
  observation for a note rather than a practice.
- `SOTA-242` (`Proposed`) — select pretraining data by matching a target
  distribution you can sample from, not by scoring it for quality. The record
  holds no other practice that takes the distribution-matching frame; every
  selection practice it has is quality-shaped.
- `SOTA-241` (`Proposed`) — rank candidate data selections with a
  model-free distributional proxy before spending a training run. Cheap enough
  to sit in front of `SOTA-166` and `SOTA-238`, both of which cost runs to
  decide which candidates deserve one.

### Changed

- `LIT-087` v5 and `NOTE-031` v2 — sourced at last. The [#121](https://github.com/dmarx/anthology-of-the-sota/issues/121) audit named both
  recommendations and filed neither, deferring a registry decision `DP-006`
  had already answered. The caveat it recorded is now the `promote_when:` on
  each practice, where evidence can come due against it.

### Fixed

- `LIT-087`'s v4 history note, which had been truncated at write time to the
  single word `The`. Restored from the commit that made the edit.

### Added

- Dropout, which the record did not hold at all. `SOTA-240` is the practice,
  stated conditionally because both its sources state it conditionally: apply
  it where the model can memorize what it is shown, and not where it cannot.
  `LIT-394` (Hinton et al. 2012) is the origin and `LIT-395` (Srivastava et
  al. 2014, JMLR) the evidence, so the practice's `introduced_by:` and
  `source:` name different papers.
- Two explanations, filed separately because they answer different questions.
  `THEORY-016` is why one forward pass with scaled weights stands in for the
  ensemble — exact for logistic units, and the logistic and constant functions
  are the only ones with that property. `THEORY-015` is what dropout does to
  the objective: a data-dependent penalty rather than an isotropic one.
  `LIT-393` (Baldi and Sadowski 2013) and `LIT-396` (Wager et al. 2013) are
  the sources. Both theory documents record that the two accounts are *not*
  independent — the second is derived using the first, in the same paper.

### Added

- `LIT-391` (DoReMi, read in `NOTE-175`) and `SOTA-238` — set
  domain weights with a small proxy under group DRO, then transfer them. The
  design point is the objective: worst-case **excess** loss against a reference
  model, because worst-case raw loss upweights whichever domain is noisiest.
  The record held `SOTA-166`, the 2024 method, and not the 2023 one that
  literature measures itself against.
- `LIT-392` (Skill-it) and `SOTA-239` (`Proposed`) — order training
  data by skill prerequisite. Twenty-six `data-pipeline` practices answered
  what to include and in what proportion; none answered in what order.

### Added

- The three benchmarks the record leans on hardest, filed under `ADR-032`
  ([#137](https://github.com/dmarx/anthology-of-the-sota/issues/137)): `LIT-389` (GSM8K), `LIT-390` (MMLU) and `LIT-388`
  (HumanEval). Each records what it measures and what it is known to be
  insensitive to, which is what a practice resting on its numbers could not
  previously bound.
- `NOTE-174` reads the HumanEval paper for its metric rather than its
  benchmark. GSM8K and MMLU are filed on their abstracts and carry no reading
  note, which `ADR-025` makes the honest signal.

### Changed

- `SOTA-210` names the source of the estimator it recommends. It called it
  "the standard one" and cited the paper that uses it rather than the one that
  defines it — `pass@k` and the unbiased form `1 − C(n−c,k)/C(n,k)` are both
  introduced in `LIT-388`. The recommendation is unchanged.

### Added

- The matching line, which completes the geometry lineage [#154](https://github.com/dmarx/anthology-of-the-sota/issues/154) said was
  missing. `LIT-386` (SuperGlue) and `LIT-387` (LoFTR), both read,
  and `SOTA-237`: match densely without a keypoint detector, because the
  detector sets the pipeline's ceiling and fails in low-texture regions where
  it cannot emit repeatable points — so no downstream matcher can recover a
  correspondence that was never proposed.
- SuperGlue is filed carrying no practice, deliberately. Its recommendation —
  learn the matcher rather than hand-designing the heuristics — was overtaken
  twice within eighteen months, and filing it live would recommend the middle
  step of a line whose end the record already holds at `SOTA-236`. It is
  filed because the endpoint reads as a conclusion without an argument
  otherwise.

### Added

- The geometry half of 3D vision, which the record did not hold at all ([#154](https://github.com/dmarx/anthology-of-the-sota/issues/154)).
  `LIT-385` (DUSt3R) and `LIT-384` (VGGT), read in `NOTE-171`
  and `NOTE-170`, sourcing `SOTA-236`: given uncalibrated, unposed
  images, regress the 3D structure and let camera parameters and pixel matches
  fall out of it, rather than estimating calibration and pose first so that
  triangulation becomes possible.
- The practice is `emerging` rather than `converged`. The classical pipeline is
  decades of tooling and still what most production reconstruction runs on, and
  a triangulated point has a geometric justification and an inspectable
  residual where a regressed pointmap has neither — which is the whole question
  wherever a reconstruction must be certified rather than used.

### Added

- The last two topics from [#87](https://github.com/dmarx/anthology-of-the-sota/issues/87)'s list, which turned out to be the same
  question asked of two different artifacts.
  - `LIT-381` (read in `NOTE-166`) and `SOTA-232` — convert an
    autoregressive model into a diffusion model by continual pretraining under
    200B tokens, rather than training one from scratch. The counterpart to
    `SOTA-157`, and both stay `Proposed`: the record holds the choice and
    recommends neither side.
  - `LIT-379` (read in `NOTE-167`) and `SOTA-235` — build a
    loss from the test instance's own in-context examples, take gradient steps
    at inference, discard the update. Up to 6x a fine-tuned baseline on ARC
    and +7.3 points on BIG-Bench Hard at 10-shot. Both documents record that
    `ARXIV-2407.04620` shares the name "TTT" and is a different claim — a
    sequence architecture, not an inference-time method.

### Added

- The self-correction pair, which is a negative result and its resolution
  rather than a disagreement. `LIT-382` (Huang et al.) defines
  *intrinsic* self-correction — no oracle, no verifier, no second model — and
  finds that under it, models do not reliably improve on reasoning and
  sometimes degrade. `LIT-383` (Kumar et al., SCoRe) concedes that and
  changes the intervention from prompting to training: multi-turn online RL
  on entirely self-generated traces, +15.6% on MATH and +9.1% on HumanEval.
- `SOTA-233` — treat self-correction as a capability to train rather than
  a behaviour to request. Carries the two named reasons supervised
  fine-tuning on correction traces fails (distribution mismatch, behaviour
  collapse), which is the half that transfers past self-correction.

### Added

- BitNet b1.58 (`LIT-380`, read in `NOTE-168`) and `SOTA-234`,
  the record's first practice about choosing the *training* format rather than
  compressing a finished model: constrain the weights during training and
  never hold a high-precision checkpoint. Ternary weights trained from scratch
  match FP16 at equal size and tokens from 3B upward — and below 3B they do
  not, which the practice states as a condition rather than a caveat. Filed
  `Proposed`: one group, one architecture, nothing at the frontier ships it.
  The measured saving (memory, bandwidth, throughput) is separated in the body
  from the argued one (integer-addition arithmetic), because the second
  assumes hardware built for the format.

### Added

- QLoRA (`LIT-378`, read in `NOTE-164`) and the two practices it
  supports, which are separable claims that happen to share a paper:
  `SOTA-230` — store the frozen base in 4-bit NormalFloat and dequantize
  to BFloat16 per multiply, training only 16-bit adapters, which takes 65B
  fine-tuning from >780GB to <48GB with no measured loss; and
  `SOTA-231` — put an adapter on every linear layer rather than the
  attention query and value projections alone, because the adapter count is
  what reaches full fine-tuning at scale and the projection rank is flat.

### Changed

- `SOTA-051` retitled from "Initialize final layer weights near zero" to state
  the claim its body actually argues: exactly zero, not near zero. The body
  had been naming the defect in its own title since it was written. Its
  truncated `version: 3` history note (the single word "The") and its bare
  citation `summary:` are repaired in the same pass.
- `SOTA-184` gains the placement condition it was silent about, with the
  measurement filed beside it. The recommendation is unchanged.

### Added

- A decision that the record may file a practice whose recommendation is
  negative — a technique that was published, adopted and did not hold, filed
  as `Rejected` to say *do not do this* ([ADR-042](record/decisions.d/ADR-042.md), closing [#88](https://github.com/dmarx/anthology-of-the-sota/issues/88)). The entry
  test is the one every practice already passes, plus one addition: the
  failure needs a citation exactly as a recommendation does, so a negative
  practice usually names two sources. `Superseded` still wins wherever a
  successor exists, because the chain carries more than a rejection does.

### Changed

- Pin moved to `luria==0.27.0`, and the `source` field group on `LIT` now
  declares `unique: true` — no two notes may name the same paper. The two move
  together because 0.26.0 ignores the key silently: declaring it against the
  old pin would have left the record carrying a constraint nothing checked.
  The three duplicate pairs the record already holds ([LIT-006](record/literature.d/LIT-006.md)/[LIT-042](record/literature.d/LIT-042.md),
  [LIT-029](record/literature.d/LIT-029.md)/[LIT-114](record/literature.d/LIT-114.md), [LIT-090](record/literature.d/LIT-090.md)/[LIT-105](record/literature.d/LIT-105.md)) pass without an acknowledgement, because a
  duplicate retired naming its survivor is the resolution rather than the
  finding.

### Added

- **`SOTA-228`** — pick the inference partitioning from where the
  bottleneck is, and expect it to move between prefill and decode. From
  `LIT-110` (Pope et al. 2022), read as `NOTE-162`. The analysis three
  serving practices here were already standing on: prefill parallelises and
  decode does not, the binding cost moves from weights to KV cache as batch
  and context grow, and at 500B with multihead attention that cache reaches
  3 TB — three times the parameters.
- **`SOTA-229`** — scale the draft model's training data, once nothing
  constrains it to predict the target's features. From `LIT-185` (EAGLE-3),
  read as `NOTE-163`. `Proposed`: one target, one benchmark, a data range
  that is not large.

### Fixed

- **`SOTA-227` said the record held no measurement of where speculative
  decoding stops paying on throughput. It did.** `LIT-185` reports +40%
  throughput at batch size 64 in SGLang, explicitly against the expectation
  that speculation is latency-only — and it was sitting unread in the record
  when that sentence was written this morning. The conditions now say to
  measure the crossover rather than assume its sign.
- **`LIT-039` was tagged `inference-optimization`.** It is an analysis of
  gradient flow in sparse networks whose only citer is `THEORY-004`, a
  lottery-ticket account. Retagged `analysis-and-evaluation`.

### Changed

- `LIT-110`'s standing section, which said *"Nothing in the record cites this
  note"* and then explained precisely why something should. `LIT-185`'s, which
  had recorded it as unsourced and unread since `#121`.

### Added

- **InstructGPT** — `LIT-377` (Ouyang et al. 2022, `ARXIV-2203.02155`)
  with a full reading, `NOTE-161`. The paper that made
  SFT → reward model → RL the default shape of post-training, and it was
  absent from this record in every form while four documents here —
  `LIT-169` (DPO), `LIT-082` (Constitutional AI), `SOTA-183`, `SOTA-126` —
  were defined by their relationship to it.

  The reading carries the three steps, the 1.3B-preferred-to-175B result, the
  85 ± 3% and 73.4 ± 2% win rates, the per-token KL penalty, the single 6B
  reward model, and the **alignment tax** with the four datasets it shows up
  on and the PPO-ptx fix the paper supplies for it.

  **No practice is filed from it**, deliberately: three of its five
  recommendations are now universal enough that documenting them would
  manufacture entries for agreement, and the one live candidate — mixing
  pretraining gradients into the alignment objective — overlaps `SOTA-199`
  closely enough that deciding needs `SOTA-199`'s source read first. Stated
  in the note rather than guessed.

### Added

- **Speculative decoding, the practice** — `SOTA-227`. Draft `gamma`
  tokens with a cheap model, score all `gamma + 1` positions in one target
  pass, keep a prefix under an accept-reject rule built so the output
  distribution is the target's **exactly**. 2x-3x at 11B, 2-2.5x at 70B, no
  retraining and nothing traded away. `Active`, `converged`.
- **Its two sources, with readings.** `LIT-376` (Leviathan et al. 2022,
  `ARXIV-2211.17192`) and `LIT-375` (Chen et al. 2023,
  `ARXIV-2302.01318`) — the same algorithm derived independently two months
  apart, at 11B and at 70B. Both `Read`.

### Changed

- `LIT-185` (EAGLE-3) and `SOTA-162` (multi-token prediction) now point at the
  thing they refine. `SOTA-162` claimed a 3x decode speedup because "the extra
  heads are a draft model for speculative decoding you did not have to train
  separately" — a sentence that rested on no document in this record until
  now.

### Fixed

- `SOTA-227` records a discrepancy found while counting adopters:
  `LIT-185`'s standing section says `LIT-139` ships a draft head, and
  `LIT-139`'s own note says only that multi-token prediction was carried over.
  Left as found rather than repaired from the same distance that produced it.

### Added

- **Five practices from the import backlog**, all `distributed-optimization`:
  ramp the sparsity ratio rather than starting at target (`LIT-056`); drop the
  parameter server once the network is the bottleneck (`LIT-302`); a directed
  exponential graph if the gossip topology is static (`LIT-254`); a fresh
  random neighbourhood every round if it need not be (`LIT-315`); and overlap
  the synchronisation with one or two local steps (`LIT-323`). The last two
  are `Proposed`; the middle two disagree with each other and are filed as a
  pair.
- **`THEORY-014` — the outer optimizer is what buys the inner step
  count.** Three papers prescribe synchronisation intervals differing by
  thirty times, and the two with small intervals have no outer optimizer.
  `LIT-212`'s own ablation reports that plain averaging at `H = 500` performs
  poorly.
- **`THEORY-013` — the SGD noise scale sets generalization, so the
  optimal batch size grows with the training set.** Filed `Rejected` and kept:
  `LIT-017` and `LIT-058` both contradict the dataset-size half, and `LIT-017`
  does it by name.
- **Two decisions closing classes rather than cases.** `ADR-041`: an
  algorithm-local tuning constant stays in the reading, with a test — strip
  the algorithm's name and see whether an instruction is left. `ADR-040`:
  advice on proof technique is out of scope, advice on finding out whether a
  technique worked is not.

### Fixed

- **`SOTA-216` and `SOTA-155` no longer declare an unreconciled conflict.**
  `LIT-212` cites `LIT-373` as the source of its own outer optimizer, and
  `LIT-373` is now a source on `SOTA-155` — whose `consensus_note` said
  nothing corroborated it.
- **`SOTA-198` and `LIT-305` no longer imply that two different quantities are
  one statistic.** `g = eps*N/B` is set; `B_simple` is measured.
- **A "~1 Gbps" threshold that is not in the paper it cited.** `LIT-302`'s
  low-bandwidth configuration is **10 Mbps** — a hundred times lower — and the
  crossover is a sweep rather than a number. The practice built on the
  reading has been rewritten; the reading's `5 ms` is the paper's and stands.
- **An ImageNet result `LIT-323` does not have.** Its experiments are
  CIFAR-10, and its anchor model is the method rather than a variant for
  skewed data.

### Changed

- `SOTA-218`, `SOTA-198`, `SOTA-216`, `SOTA-155`, `LIT-305`, `LIT-058` and
  `NOTE-132` all gain or lose text where the reconciliations touched them.

### Added

- `SOTA-221` — to train past the batch size where your optimizer stalls,
  change the optimizer's conditioning rather than the scaling rule. From
  `LIT-265` (LAMB), with `LIT-058` corroborating.
- `THEORY-012` — how far a batch-size scaling heuristic transfers is a
  property of the optimizer, not of the heuristic. `Proposed`. It explains
  `SOTA-218` and `SOTA-221`, which is what lets both stand.

### Fixed

- `SOTA-218` cited four figures the paper does not contain: 71 million training
  runs (the real count is 168,160 models; 71,638,836 is the number of loss
  measurements), seven workloads (35), four optimizers (three), and one
  batch-size range where the paper reports two different transitions. All
  corrected against `ARXIV-1811.03600`.
- `LIT-058` understated the same scale and transposed its model-family and
  data-set counts — six model families and seven data sets, not the reverse.
  Its standing section still said nothing in the record cited it, six weeks
  after `SOTA-218` did.

### Changed

- `SOTA-218` no longer ends by declaring an unresolved conflict with LAMB.
  `LIT-265` cites `LIT-058` approvingly as its own motivation and labels its
  large-batch tables *untuned*; the two papers were never in dispute.
- `NOTE-132`'s "Bearing on the record", which is where the supposed
  contradiction was actually written, and which refused a practice on those
  grounds.

### Added

- **Every vocabulary describes itself.** All nine carry a `label` and a
  `blurb` saying what the set is; the seven a closed field names also carry an
  `alert`, printed under the violation. `adr-tags` and `dp-tags` get no alert
  because the fields naming them are open, where an alert would be inert.

  The prose was already written — it sat in YAML comments above each table,
  where no view could reach it and no violation could quote it. What moved is
  the part that answers *what is this set?*; what stayed a comment is the part
  that is about this file's history rather than about the vocabulary.

  The distinctions the record most needs a reader to hold are the ones now
  printed at the point of failure. A bad `note-statuses` value says *the value
  you want may be no note at all*. A bad `consensus` value says *`unassessed`
  is a real answer rather than a gap*. A bad `lit-statuses` value says *if you
  mean the advice has moved on, that is a status on the practice*.

- **The `topics` vocabulary describes itself.** It carries a `label`, a
  `blurb` saying what the axis is — the thirteen kinds of claim, and
  [ADR-026](record/decisions.d/ADR-026.md)'s filing rule — and an `alert` printed with any closed-set
  violation:

  > Closed so that every tag is one somebody chose and blurbed, NOT because
  > the list is finished. If your document wants a word this vocabulary
  > cannot say, add it — with a label, a blurb and a decision saying why,
  > exactly as `representation-and-encoding` and `analysis-and-evaluation`
  > were added.

  That sentence was the point of asking for the feature: `closed: true` is an
  enforcement mechanism whose risk is discouraging the growth it exists to
  channel, and CLAUDE.md has said so in prose that no violation ever showed
  anyone. All three declarations live on the set, so one of each reaches
  SOTA, LIT and THEORY rather than three copies free to drift.

### Changed

- Pinned to luria 0.26.0 — `alert` is [LU-#273](https://github.com/dmarx/luria/issues/273), `label`/`blurb` on a
  vocabulary are [LU-#279](https://github.com/dmarx/luria/issues/279), and the two composing is
  [LU-#281](https://github.com/dmarx/luria/issues/281). A nested vocabulary's values live under `terms:`, not
  `values:`.

### Changed

- The file-wide acknowledgements in `luria.yaml` and on [ADR-039](record/decisions.d/ADR-039.md) are **two
  each, split by the reason** — Superseded and named as history, or Proposed
  and merely unmoved — rather than one line carrying every code. [LU-#278](https://github.com/dmarx/luria/issues/278) was
  closed upstream: a continuation line is not worth supporting, and a
  file-wide acknowledgement is not position-sensitive, so several directives
  cost nothing. They also read better than the line they replace, which is
  the grouping the prose already wanted.
- [ADR-039](record/decisions.d/ADR-039.md) is at version 2. The choice is unchanged — the config is scanned —
  but its consequence was written as a workaround for a bug that turned out
  to be intended behaviour, so the reason is corrected in place.

<!-- inactive-ok-file: ADR-035, ADR-038 — both Proposed, named as the decisions whose stale citations this change repaired. -->

### Added

- `luria.yaml` and `.github/workflows/*.yml` are scanned for references, which
  is the pair luria scans for itself. The config carries 87 code citations
  across 38 documents — the densest commentary in the repository, and every
  one of them a reason the schema is shaped the way it is — and nothing was
  checking them. The workflows carry six, all remote, and add no findings:
  covering a file before it rots costs a line.
  [ADR-039](record/decisions.d/ADR-039.md) has the measurement.

### Fixed

- **Sixteen dead citations in the configuration**, invisible until the file
  was scanned. Fifteen named decisions by temporary codes that had since been
  numbered — ten of them [ADR-035](record/decisions.d/ADR-035.md) alone, dead since [#140](https://github.com/dmarx/anthology-of-the-sota/issues/140) merged — and two named
  a luria decision by a temporary code numbered upstream as [LU-ADR-084](https://github.com/dmarx/luria/blob/main/record/decisions.d/ADR-084.md).
- One citation in `record/decisions.d/ADR-038.md` named luria's decision on
  derived fields without the `LU-` prefix, so this record read it as a local
  document that does not exist. Now spelled the way [ADR-022](record/decisions.d/ADR-022.md) already spelled
  the same citation.
- Four stale temp codes in a September changelog fragment.

<!-- inactive-ok-file: ADR-036 — Proposed. Named as the decision whose four
     categories the cross-scheme measurement is read against, not as a rule in
     force. -->

### Changed

- **A reading is filed under its paper's topics, not its own.** `NOTE.tags`
  and `NOTE.primary_topic` derive from `paper`, the way `NOTE.published`
  already did. A note and its paper are the same paper, so a second copy of
  the subject was a second copy free to disagree — and four of the 158 were.
  To change what a reading is filed under, retag the paper.
  [ADR-038](record/decisions.d/ADR-038.md) has the decision, and the survey of all six cross-scheme
  relations showing why none of them asserts an invariant instead.
- Pinned to luria 0.24.0, which is what lets a derivation hold a list
  ([LU-#276](https://github.com/dmarx/luria/issues/276)). Without it the derived field reads as no values at all and every
  `docs/notes/tags/*.md` page silently stops being written — this record is
  the case that was found on.

### Fixed

- Four papers retagged from their own readings, which had been disagreeing
  with them: [LIT-014](record/literature.d/LIT-014.md) gains `model-stability`, [LIT-096](record/literature.d/LIT-096.md) gains `data-pipeline`,
  [LIT-024](record/literature.d/LIT-024.md) makes `attention-techniques` primary and [LIT-112](record/literature.d/LIT-112.md) makes
  `inference-optimization` primary. Every old topic is kept as a secondary;
  each added one was chosen independently by that paper's reader.

### Removed

- `tags:` from all 158 notes and from `record/notes.d/_template.md`. Writing
  one is now a lint violation, like `published:`.

### Changed

- **`lint.fail_on` is no longer empty.** It gains `source-mismatch`, and only
  that — the check that verifies a document is about the paper it names, at
  zero today, and the one that would have failed the import in [#138](https://github.com/dmarx/anthology-of-the-sota/issues/138), which
  filed three readings against identifiers belonging to other papers while the
  lint printed a clean run. It reads the committed lockfile, so it fails only
  on a disagreement that is in the diff.

- **`source-unchecked` is deliberately not promoted**, though it is the
  natural companion. Its only failure mode is an upstream outage, which a
  contributor who did nothing wrong cannot act on. A check earns enforcement
  by failing on something somebody can fix.

### Added

- **`ADR-037` — fail the build on `source-mismatch`, and take the source
  invariant upstream.** `Proposed`.

### Documentation

- **"A claim inherits the topic of the document it was extracted from" does
  not survive measurement, and the sentence is withdrawn.** It was the summary
  the unbound-lineage pass put on eleven of its fifteen findings. Measured:
  **167 of 220 practices — 76% — already share their source's topic**, which
  is the ordinary correct case, and of the six practices that pass retagged,
  four had inherited their source's topic while two were wrong in the opposite
  direction. The sentence described four documents.

- **That is not an argument against an invariant on `source:`, and this
  decision's first draft treated it as one.** A relation asserts that its
  documents have something in common and the invariant is the record saying
  what — as true of a practice and its evidence as of two practices. The 73
  crossings the check reports were dismissed on a topic-pair histogram; read
  individually they are four kinds, and only one of them is settled. **16** are
  multi-topic sources, which `ADR-032` admitted deliberately. **14** are
  practices resting on `analysis-and-evaluation` papers, the kind-not-subject
  fact the lineage pass documents. Roughly **10** are `ADR-026`'s filing rule
  working — the practice takes its kind, the paper takes the domain it was
  discovered in. The remaining **~33** include candidates worth a reading:
  `LIT-112`, *Efficient Memory Management for LLM **Serving***, filed
  `attention-techniques` while all four practices under it are
  `inference-optimization`; and `LIT-059` (CheckFreq) filed
  `systems-optimization` while its four checkpointing practices are
  `distributed-optimization`, the topic whose blurb names checkpointing.

- **The invariant cannot be declared in config today.** A chain over a
  cross-scheme relation raises `KeyError` in `luria index`:
  `chains.lines_of` indexes only documents in the chain's declared scheme, and
  `source:` crosses `SOTA` to `LIT`. Filed as `LU-#272` with the measurement
  rather than recorded here as a decision against it.

- **Two luria docstrings state a reason for the default that is this record's
  old state.** `invariants.py` and `config.py`'s `Chain.invariant` both
  explain the unset default with *"`source:` joins a practice to its paper
  across two vocabularies that were separated on purpose"*. `ADR-026` merged
  them. The default may still be right; the stated reason is stale, and a
  general-purpose library reasoning about one consumer's schema is worth
  flagging on its own. Both go in `LU-#272`.

- **`LU-#165` is the duplicate-identifier gap, already filed upstream.** Two
  documents claiming one identifier — the defect [#138](https://github.com/dmarx/anthology-of-the-sota/issues/138) shipped 67 times — is
  not in luria's finding vocabulary and no config setting produces it. The
  upstream issue asks for a `duplicate-source` finding and a `luria merge`,
  and `luria.yaml` now names it beside the dial.

### Fixed

- **Sixty-seven duplicate literature notes removed.** PR [#138](https://github.com/dmarx/anthology-of-the-sota/issues/138)'s first commit
  filed 68 papers as `Deferred`; its second commit replaced that decision and
  filed them again with readings, without deleting the first set — the
  regeneration between the two used `git clean -fd`, which removes untracked
  files, and the first set was tracked. Nothing cited them, none carried a
  `NOTE`. The literature count goes from 376 to 310 and the undecided-document
  count from 121 to 54.

- **The topic group moves from `exactly-one` to `any` on all four schemes**
  (`ADR-035`). A document is often about two of the thirteen — a
  positional-encoding scheme is also an attention technique — and under
  `exactly-one` recording the second meant deleting the first.
  `primary_topic` still derives `{tags[0]}`, so the primary is still exactly
  one value and every chain invariant still compares one against one:
  `docs/reports/unbound-lineage.md` is byte-identical at 24 relations and 10
  lines before and after. The cost is that tag order is now load-bearing
  where it was conventional.

- **The chain invariant moves from `primary_topic` to `tags`** (same
  decision). What a relation asserts is that its members share a subject, not
  that they share their *first* subject. Measured: 24 unbound relations become
  21, and the three that bind are the argument in miniature — `LIT-211` binds
  to `LIT-229` and `LIT-242` on `training-optimization` and should, while
  `SOTA-085` binds to `SOTA-161` on a `flash-attention` label that [#101](https://github.com/dmarx/anthology-of-the-sota/issues/101) added
  for exactly this purpose. **Both `flash-attention` tags are removed**, which
  re-opens that edge and settles the count at 22 relations and 10 lines.

- **The `topics` vocabulary gains `tiny-models`, and `tags` is closed on
  `SOTA`, `LIT` and `THEORY`.** Ten documents carried `tiny-models` as an
  undeclared string; it now has a label and a blurb. Closing follows from the
  invariant move — if any tag can bind a relation, a word typed once can
  quietly assert two documents share a subject. `NOTE.tags` declares no
  vocabulary, so it is not covered.

- **`CLAUDE.md` says the closure is an invitation**, because the lint's own
  message does not. *"is not in the `topics` vocabulary — the values are …"*
  sets up "pick the nearest of these fourteen", which is the failure this
  whole pass repaired. `LU-#273` asks luria to let a rule carry its own note
  so the remedy prints where the failure is.

- **Eleven of the retags below get their old topic back as a secondary**,
  plus `NOTE-028` following its paper. The first pass replaced where it
  should have added, and the old tag was still true in each case: the eight
  positional-encoding papers keep `attention-techniques` or
  `model-architecture`, `LIT-211` keeps `training-optimization`, and
  `SOTA-098`/`SOTA-099` keep `training-optimization`. Four stay replacements
  because the old tag named where the claim was *found* rather than what it
  is about — `SOTA-060` under `distributed-optimization` because its source
  is a Megatron paper, and `SOTA-092`/`SOTA-093`/`SOTA-094` under
  `model-architecture` because theirs is a model report.

- **Fifteen documents retagged, from reading the unbound-lineage report.**
  Eight positional-encoding papers — `LIT-045` (RoPE), `LIT-048` (ALiBi),
  `LIT-192` (Position Interpolation), `LIT-193` (YaRN), `LIT-207`, `LIT-208`,
  `LIT-209`, `LIT-210` — move to `representation-and-encoding`, the topic [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114)
  added for exactly this and which nobody applied retrospectively; `NOTE-028`
  follows its paper. `LIT-211`, which has *LLM Fine-Tuning* in its title, moves
  to `adaptation-and-tuning`, where the practice it introduced and five of its
  six descendants already were. `SOTA-092`, `SOTA-093` and `SOTA-094` — three
  batch-size claims from one model report — move to `training-optimization`.
  `SOTA-060` moves to `model-stability`. `SOTA-098` and `SOTA-099` move to
  `model-stability`, joining the practices they are compared against.

- **Two sibling relations removed as analogies rather than comparisons.**
  `SOTA-045` ↔ `SOTA-091` and `SOTA-047` ↔ `SOTA-079`. `ADR-011` defines
  `compared_against:` as the work evaluating itself against the other, and
  neither pair was ever compared — different papers, different subsystems, a
  shared shape of idea. The reason is left in all four frontmatters.

### Added

- **`ADR-036` — an unbound relation is one of four things, and only one
  of them is a retag.** `Proposed`. The report is down from 38 relations and 16
  lines to 24 and 10, and what remains is named rather than cleared: seven
  relations cross because `analysis-and-evaluation` is a *kind* rather than a
  subject and will unbind any lineage that grows an analysis paper, and
  fifteen are real fault lines — a general practice against its
  domain-specific instance, rival fixes made at different layers, and trunk
  papers whose contribution spans two topics.

### Documentation

- **The report's own prior turned out to be wrong for this record.** It reads
  an unbound relation as *"usually a sign the vocabulary is short a word"*.
  None of the 38 wanted a fourteenth topic. What is missing is a **relation** —
  `specializes:`, for the four edges where one practice is the
  domain-specific instance of another and `compared_against` is standing in.

- **Eleven of the fifteen mis-filings had one cause**, worth stating as a
  habit rather than as eleven corrections: a claim extracted from a model
  report, a Megatron paper or a systems paper inherits *that document's* topic
  instead of its own. `ADR-026`'s filing rule already forbids it; this is the
  first measurement of how often it is missed.

### Changed

- **`SOTA-010` is `Superseded` and its claim now lives in the `THEORY`
  scheme.** *Skip connections promote training stability by smoothing out the
  loss landscape* states what is true rather than what to do. `ADR-031` listed
  it as one of eight practices in that shape, called it one of the two
  clearest candidates to move, and deliberately left it — the move needed a
  decision about what a vacated code says. The new theory carries the claim,
  the figure's limits, and `explains:` the five practices that rest on it
  (`SOTA-032`, `SOTA-051`, `SOTA-060`, `SOTA-136`, `SOTA-169`); the vacated
  code keeps its lineage and becomes a redirect. **No practice is filed
  alongside it**: the instruction it would imply is *use skip connections*,
  which `DP-007` keeps unfiled as trunk.

- **`ADR-034` — a document that changes scheme is `Superseded` where it
  leaves, and names its successor across the boundary.** `Proposed`.
  `Superseded` rather than `Rejected` because `Rejected` on a practice means
  *do not do this*, and no reader should take `SOTA-010` as advice against
  skip connections. The successor is carried by `superseded_by:`, which
  already crosses schemes — the draft of the decision asserted no such field
  existed and the lint corrected it on the first run.

### Added

- **Seventy `NOTE` documents and sixty-seven `LIT` notes: the decentralized
  training literature, read.** Ported from readings made for another project.
  The local-update line (Local SGD, post-local SGD, Cooperative SGD,
  Overlap Local-SGD, SlowMo, OpenDiLoCo, GPA), the decentralized line (D-PSGD,
  Stochastic Gradient Push, Epidemic Learning, Moshpit SGD), compression
  (signSGD, PowerSGD, 1-bit Adam, Subspace Networks), Byzantine-robust
  aggregation (Krum, coordinate-wise trimmed mean and median), federated
  learning (FedAvg, Async-HFL, FedHSA), volunteer-scale training
  (Learning@home, DeDLOC, SWARM), the mean-field account of wide networks
  (Mei–Montanari–Nguyen, Rotskoff–Vanden-Eijnden, Sirignano–Spiliopoulos,
  Chizat–Bach, NTK, MFLD), the teacher–student line (Saad–Solla, Goldt,
  Refinetti), permutation symmetry (Entezari et al., Git Re-Basin), and the
  consensus and flocking results the gossip literature rests on (Wolfowitz
  1963, Tsitsiklis–Bertsekas–Athans 1986, Jadbabaie et al.,
  Olfati-Saber–Murray, Tahbaz-Salehi–Jadbabaie, Cucker–Smale, Kuramoto). Four
  papers the record already held — DGC, Shallue et al., ZeRO and DiLoCo — had
  no reading and now have one.

- **Seven practices.** Pair any compressor with error feedback and correct the
  momentum under it (`Active`; PowerSGD, DGC and 1-bit Adam each report the
  failure without it). Retune learning rate, momentum and schedule at every
  batch size rather than transferring by a scaling heuristic (`Active`;
  Shallue et al., 71 million runs). Freeze Adam's variance term before
  compressing its update (`Proposed`). Align the hidden-unit permutation
  before averaging separately trained networks (`Proposed`). Switch from
  minibatch to local SGD at the first learning-rate decay (`Proposed`).
  Aggregate coordinate-wise by median when workers may be faulty
  (`Proposed`). Leave the inner optimizer state unsynchronised in
  local-update training (`Active`; extends the DiLoCo practice, and is where
  two thirds of its saving comes from).

- **Two theory documents.** That a wide two-layer network's dynamics are a
  gradient flow on the distribution of its neurons, and that the flow is
  convex — `Active`, four groups by four routes within about a year, and the
  reason the `1/N` versus `1/sqrt(N)` output scaling is a choice about whether
  features move at all. And that most of the loss barrier between two
  independently trained networks is permutation rather than disagreement —
  `Proposed`, and the account under the alignment practice.

- **`ADR-033` — readings made in another context port; their agenda does
  not.** `Proposed`. Eleven of the incoming schema's twelve fields are this
  record's NOTE sections under other names. The twelfth answers five questions
  from another project's agenda and is rewritten rather than transcribed.

### Fixed

- **Three readings were bound to the wrong identifier, and two rebind.**
  `1805.01361` is a second reading of `1804.06561` filed against a stranger's
  id — the two are merged into one note. `1906.08632`'s reading is of the
  paper its id names; only the title came from a different Goldt paper.
  `2102.11742` binds to nothing, so the paper is filed `Deferred` with no
  note. Wolfowitz (1963) was given a journal, volume, pages and a DOI that
  returns 404; every identifier in the port now comes from arXiv or CrossRef
  and none from the reading.

- **Twenty-three of the 187 recommendations are marked, in place, as not
  filed.** Seventeen name another project's own system and experiments despite
  the schema calling the field project-agnostic; six are advice on proof
  technique rather than on training. Struck rather than deleted, so the cut is
  auditable.

### Documentation

- **`## Bearing on the record` is seventy fresh paragraphs, not a
  transcription.** The source field answered another project's questions.
  Each replacement answers this one's: what a practice here could rest on, and
  whether one exists. Most of them say no practice does — which is the point
  of writing them rather than copying.

### Added

- **`LIT-242` / `NOTE-087` — Evolution Strategies as a Scalable
  Alternative to Reinforcement Learning** (Salimans, Ho, Chen, Sidor and
  Sutskever, 2017). `extended_by:` `LIT-211`. The trunk of this record's ES
  line, cited by ten of the twelve papers in it and absent until the
  bibliography sweep found it. Its contribution is a communication scheme:
  synchronize random seeds and every worker can reconstruct every other's
  perturbation, so an update costs one scalar per worker instead of a
  gradient. 3D humanoid walking in 10 minutes on 1,440 cores with linear
  speedup, against ~11 hours on 18. Data efficiency is **worse** — 3–10× more
  data than A3C — and the paper leads with that; its argument is that
  parallelism converts the deficit into wall clock.

- **`LIT-241` / `NOTE-088` — Proximal Policy Optimization
  Algorithms** (Schulman, Wolski, Dhariwal, Radford and Klimov, 2017).
  `extended_by:` `LIT-127`. Cited by six of the twelve. The clip is not what
  does the work — taking the **minimum** of the clipped and unclipped
  surrogate makes the objective a pessimistic lower bound, which is what
  licenses several epochs of minibatch SGD on one batch of on-policy data.

- **`ADR-032` — benchmarks, model reports and infrastructure are
  literature, and the record files them.** `Active`. The sweep found them to
  be 9 of the 27 most-cited missing references, with GSM8K alone cited by 9 of
  12, and no pass had ever written down that it was declining them. The
  argument is the scheme's own: a `LIT` note records a paper's **standing**,
  and a benchmark the record's practices are argued on has standing. The
  trigger for filing stays narrow — something in the record cites it — and no
  vocabulary changes.

### Documentation

- **Salimans §3.2 states `THEORY-007`'s claim in 2017.** That account holds
  that what governs ES's scalability is not the ambient parameter count but a
  low-dimensional effective structure. The 2017 paper says: "this does not
  mean that larger neural networks will perform worse than smaller networks
  when optimized using ES: what matters is the difficulty, or intrinsic
  dimension, of the optimization problem", gives the concatenated-features
  argument for it, and reports larger networks doing slightly better. What
  `LIT-236` adds — a mechanism, a measurement across scales, the link to
  rise-then-decay — is real and is less than filing the two side by side
  would have suggested. Both documents now say so.

- **Three practices in the record modify PPO and none could cite it.**
  `SOTA-145` removes its critic, `SOTA-146` corrects an objective descended
  from its clipped ratio, `SOTA-129` makes the family a recipe stage. One
  detail the parent supplies: the ES line grid-searches PPO's KL coefficient
  `β`, and §4 of the PPO paper reports the KL-penalized variant as the
  *worse* of the two its authors tested.

- **`SOTA-154`'s `introduced_by:` is unchanged, deliberately.** Salimans et
  al. recommends ES over policy gradients for control tasks trained from
  scratch; that practice recommends it for LLM fine-tuning, which this paper
  does not attempt and which the field doubted until `LIT-211`. Same
  sentence, different claim — and the field's doubt is the evidence that they
  are different.

### Added

- **`LIT-236` / `NOTE-084` — The Blessing of Dimensionality in LLM
  Fine-tuning: A Variance–Curvature Perspective** (Liang et al., 2026).
  `extended_by:` `LIT-233`. One geometric property accounts for two puzzles:
  fine-tuning landscapes are low-dimensional in curvature, so a handful of
  stiff directions carry improvement amid a near-zero bulk.

- **`THEORY-007` — fine-tuning landscapes are low-dimensional in
  curvature, and improving directions are degenerate rather than unique.**
  `Proposed`. Because improvement depends only on a perturbation's projection
  onto a `k`-dimensional curvature-active subspace, every useful projection
  has a `(d−k)`-dimensional preimage — so the ambient dimension drops out and
  a fixed population of about thirty keeps working from 0.5B to 7B, with **no
  systematic rightward shift** in the best-of-`N` knee. The same spectral
  heterogeneity produces **rise-then-decay** under fixed hyperparameters, in
  GRPO as well as ES.

### Changed

- **`SOTA-154` version 3: a correction, not a change of position.** Version 2
  promoted this practice on `LIT-233`, described there and in the practice as
  "an independent group" with "no stake in the result". **It is not. Yulu
  Gan, that paper's first author, is the second author of `LIT-211`**, and the
  paper cites it as prior work. The promotion condition excluded "further
  results from the same group".

  The practice stays `Active`, on evidence identified after the fact:
  `LIT-235` at 4B with both arms swept and ES highest on all four tasks,
  plus `LIT-230`, `LIT-229` and `LIT-240` — none sharing an author with
  `LIT-211`. The consensus note is now tallied **by authorship rather than by
  institution**, which moves four of the eight positive results inside the
  line they were being counted as independent of.

- **The scale-boundary table gains a competing reading.** It reads every
  negative ES result at ≤1.5B as a density threshold. `LIT-236` reports
  improvement accessible at 0.5B with a population of thirty **provided the
  perturbation scale is small enough** — so the failures below 1.5B may be a
  `σ` tuned for larger models rather than a density that is absent. `LIT-233`
  holds `σ` fixed at 1e-3 across every scale; `LIT-236` chooses a viable
  `σ` per model. Both practice and theory now say so.

- **`SOTA-213` separates two stopping questions it had run together.**
  Prior-task accuracy dips and recovers, so do not stop early to protect it.
  The *target* reward rises, peaks and decays, so stop near its peak. Two
  curves, two answers, and the rule that satisfies both is to watch the curve
  you are optimizing. It also gains `LIT-236` as a third arrival at the
  population knob, and two interventions it does not yet carry because nobody
  has run them end to end — noise scheduling and adaptive step sizes.

### Documentation

- **`LIT-233` and `NOTE-078` carry the correction where a reader meets them.**
  The reading note now records that it got this wrong twice: first calling the
  baseline result "the weaker of the two", then over-correcting to "an
  independent replication". Both versions are kept.

- **`THEORY-006` and `THEORY-007` are complementary, by `LIT-233`'s own
  construction.** That paper cites `LIT-236` and reads the thicket as
  "the intersection of (a) a broad loss basin induced by pretraining and
  overparameterization, and (b) a set of task-relevant directions that are
  effectively low-dimensional... but embedded within the full parameter
  space". One account is about the basin, the other about the directions in
  it. Filed side by side without that note they would read as rivals.

  They do disagree about scale, and it is methodological: fixed-`σ` density
  rising 0% → 64% across 0.5B–32B against best-`σ` accessibility flat across
  0.5B–7B. Different quantities. Nobody has run one protocol measuring both.

### Added

- **`LIT-238` / `NOTE-081` — Overcoming Forgetting in LLM Fine-Tuning
  with Evolution Strategies** (Schweighofer et al., 2026). `corrects:`
  `LIT-237`, `extends:` `LIT-235`. Three findings that between them
  reframe the forgetting result: the degradation is **transient** — HellaSwag
  falls 8% over 300 iterations and returns to baseline by the end, with
  MMLU-Pro and ARC-Challenge doing the same and ProofWriter the mirror image —
  it is **not specific to ES**, since GRPO forgets considerably with
  ProofWriter as the target, and it is **controllable**. Anchored Weight
  Decay, an `L1` or `L2` pull toward the initial weights applied in the update
  rule rather than through a loss, buys a population-128 reduction in drift at
  population 30 for 1–2% runtime.

### Changed

- **`THEORY-008` is `Active`.** Its condition asked for the `σ²dT/N`
  scaling measured by an independent group on a transformer at a different
  scale, with the population-size dependence tested directly by raising `N`
  and observing drift fall at fixed `T`. `LIT-238` is that: no shared
  authors with `LIT-235`, Qwen2.5-3B rather than Qwen3-4B, and population
  30 → 128 halving the update norm with prior-task degradation falling
  monotonically across 30, 128 and 256.

  One refinement arrived with the confirmation and sharpens the account: even
  at population 256 or under an anchor penalty, ES update norms stay an order
  of magnitude above GRPO's while the prior-task *distributional* shift becomes
  comparable. Displacement is what scales; what a displacement costs depends on
  whether anything constrained its direction.

- **`SOTA-213` is rewritten, and its title changed.** It was filed in this
  same pull request as *"stop evolution-strategies post-training when the
  target task converges, and buy accuracy with population size rather than
  more steps"*, drawn from `LIT-237`'s single run in which averaged
  prior-task accuracy fell throughout training. **If the dip recovers, a
  stopping rule fitted to that average stops at the worst point on the curve.**
  It is now *"control evolution-strategies drift with a larger population or an
  anchor penalty, not by stopping training early"*, with the population half of
  the original claim confirmed and AWD as its cheaper form.

- **`SOTA-154`'s drift caveat is qualified.** The cost is real and smaller than
  it first looked: transient rather than permanent, not specific to ES, and
  avoidable at 1–2% runtime. `LIT-237`'s failed replication on *accuracy*
  is untouched by any of that and is what still makes the practice
  `contested`.

### Documentation

- **`NOTE-082` keeps its wrong guess.** That reading asked, as an open
  question, whether the forgetting would appear at all if training stopped at
  convergence, and answered that the paper's own data suggested not. It is
  struck through rather than deleted, with the correction beside it — the
  guess and its refutation are more useful than either alone, and per
  [DP-003](docs/design-principles.md#dp-3) the abandoned position is most of the content.

- **Averaging was the whole disagreement, or most of it.** `LIT-237`
  reported mean prior-task accuracy declining through training; `LIT-238`
  reports the same experiment per task and finds recoveries. Neither
  measurement is wrong. `NOTE-081` files "report prior-task curves per
  task, not averaged" as a candidate recommendation rather than a practice,
  because the paper demonstrates it without recommending it.

### Added

- **Four papers closing the evolution-strategies line**, each with a `Read`
  reading note:
  - `LIT-237` / `NOTE-082` — *Evolutionary Strategies lead to
    Catastrophic Forgetting in LLMs* (Abdi et al., 2026). `corrects:`
    `LIT-211`. The first independent replication attempt, which fails, and the
    first measurement of what ES costs a capability nobody is training.
  - `LIT-235` / `NOTE-083` — *Matching Accuracy, Different Geometry*
    (Hoy et al., 2026). The mechanism the line was missing.
  - `LIT-240` / `NOTE-086` — *ESSAM* (Sun et al., 2026). `extends:`
    `LIT-211`. Sharpness-aware minimization transposed into zeroth order.
  - `LIT-239` / `NOTE-085` — *ESSA* (Korotyshova et al., 2025). The
    earliest paper in the line and the last one filed.

- **`THEORY-008` — an ES update is mostly a loss-invariant random walk
  whose size grows with steps and shrinks with population.** `Proposed`. The
  off-manifold component's squared norm grows as `σ²dT/N`, and in a landscape
  with many flat directions it dominates. One decomposition accounts for four
  separate observations: the enormous update norm, the near-orthogonality of
  ES and GRPO directions, the flat curvature along the ES displacement, and
  the linear mode connectivity between two solutions that look nothing alike.

  It `explains:` `SOTA-154` in a different place from `THEORY-006`. That
  account says why there is anything worth finding near the pretrained
  weights; this says what the search does with the rest of the space while it
  looks.

- **`SOTA-213` — stop ES post-training when the target task converges,
  and buy accuracy with population size rather than more steps.** `Proposed`,
  `emerging`. Countdown peaks at about 200 iterations; `LIT-237` ran to
  500 and held-out HellaSwag declined across the whole stretch that bought no
  task performance. Since drift is linear in `T` and inverse in `N`, the knob
  is available — and `LIT-235`'s continual result is explicitly
  conditioned on "when its iteration budget is controlled".

### Changed

- **`SOTA-154` gains a second `contested_by:` and a scale boundary.**
  `LIT-237` is the independent replication attempt that did not reproduce
  the ordering — GRPO ahead on three of four settings, at 1B and 1.5B. It also
  gains `LIT-235` as a source: a fourth independent group, at 4B, both
  arms swept, ES highest on all four tasks.

- **The scale boundary is now tabulated in `SOTA-154` and `THEORY-006`.**
  Across eight papers, **every negative result sits at 1.5B or below and every
  positive at 1.5B or above**. Six groups, none of them testing `THEORY-006`
  and most not citing it, recovered the threshold that account names. The
  practice's scale condition is now sharp rather than hedged.

- **`SOTA-154` states the drift cost.** ES moves orders of magnitude further
  from the base model than GRPO — roughly 1000× after 500 iterations, 87–107×
  across four sequential tasks — and a held-out capability degrades with it.
  Neither that nor the scale floor retires the practice; both are conditions
  on running it.

- **`THEORY-006` stays `Proposed` for the third time, and says so.** The
  condition has now been approached by a confirmed prediction, by a mechanism,
  and by this boundary, and met by none of them. The document flags that two
  readings are available — the account is genuinely unconfirmed, or the
  condition asks for a measurement nobody has reason to repeat — takes the
  first, and leaves the second for someone other than the author who wants it
  met.

### Documentation

- **The record held a reply before it held the claim.** `LIT-230`'s entire RQ2
  is an answer to `LIT-237`, and the record filed the answer first,
  because the citation graph was followed forward from a 2026 paper and never
  backward. `LIT-239` is the same error at the other end of the line: the
  earliest paper in it, filed last. Both are `DP-004` — a pass finds only what
  its query is shaped like, and "papers this one cites" and "papers that cite
  this one" are different queries.

- **Three papers were arguing about one quantity without knowing it.**
  `LIT-237` read ES's drift as the cause of forgetting, `LIT-230` read it
  as functionally sparse and harmless, `LIT-231` read it as proof the search
  finds nothing. `THEORY-008` says all three are describing a
  loss-invariant random walk, and that whether it hurts is a question about
  what else you measure and for how long.

### Added

- **Three papers completing the evolution-strategies line**, each with a
  `Read` reading note:
  - `LIT-230` / `NOTE-076` — *Understanding Evolution Strategies for
    LLM Reasoning* (Ba et al., 2026). The first paper in the line to ask what
    ES **does** rather than whether it wins.
  - `LIT-234` / `NOTE-077` — *Beyond the Best Guess* (Hayes et al.,
    2026). Carries the comparison to 32B against published RL checkpoints, and
    locates coverage collapse in the accuracy histogram.
  - `LIT-232` / `NOTE-079` — *EGGROLL, Unrolled* (Kaya and Hashemi,
    2026). `corrects:` `LIT-229`. Works out what the low-rank update
    converges to and halves the estimator's evaluation cost.

- **`SOTA-210` — report pass@k as well as pass@1 after post-training.**
  `Active`, `emerging`. GRPO finishes below its own base model on both pass@16
  and pass@32 in **15 of 18 comparisons** while improving pass@1; across
  Qwen2.5, Qwen3 and published RL checkpoints up to 32B, the base model
  eventually overtakes the RL checkpoint. The mechanism is countable: RL
  increases the number of prompts solved in *none* of `k` samples, which is a
  ceiling no further sampling can lift. Two groups with no authors in common,
  a fortnight apart.

- **`SOTA-211` — spend one fitness evaluation per ES direction, not an
  antithetic pair.** `Proposed`, `emerging`. The antithetic pair's variance
  reduction depends on both evaluations sharing randomness, and autoregressive
  regeneration breaks that: `LIT-230` measures the reduction on SST-2 and
  not on regenerated GSM8K rewards, while `LIT-232` derives a
  leave-one-out baseline — free, from the population mean score centering
  already computes — that preserves the expected field at half the cost. Two
  groups, two arguments, one instruction.

- **`NOTE-080` and `NOTE-075`** — `Read` readings of EGGROLL and
  Hyper-ES, filed after reading the theory sections the first pass skipped and
  declared skipped. Both papers previously had `LIT` notes and no reading.

### Changed

- **`SOTA-154` gains the coverage argument and a scale envelope of 32B.** Two
  sources added. What the practice is *for* has changed with them: the case is
  strongest where test-time sampling is the deployment, because that is where
  RLVR's narrowing is paid for. Two caveats travel with the 32B number and
  both are stated — those comparisons are against published checkpoints rather
  than budget-matched RL runs, and they come from `LIT-211`'s own lab. **The
  independent evidence still stops at 8B.**

- **`THEORY-006` gains a corroborating source and stays `Proposed`.**
  `LIT-230` cites the account by name and confirms a *prediction* of it —
  that fewer search directions suffice as scale grows, measured at 0.5B, 1.5B
  and 3B — and supplies a candidate mechanism the account lacked: ES's gains
  survive zeroing every update below a single-step magnitude threshold, so
  they live in a sparse coordinate subset, and larger models plausibly hold
  more such subsets. This is **not** what the promotion condition asks for: not
  the density measurement, same model family, and no mechanism predicting
  where the transition sits. The condition stands as written and the document
  says so.

### Documentation

- **Hayes et al. is not an independent replication and the record says so in
  the note itself.** Same lab as `LIT-211` — Cognizant AI Lab, Qiu on both —
  running that paper's own method. `SOTA-154`'s promotion condition excluded
  "further results from the same group" for exactly this case. What it adds is
  scale and a different kind of claim; what it is not is a second group.

- **The dissent and the characterization disagree about the same
  measurement.** `LIT-231`'s Lemma 1 concerns the angle between a random
  perturbation and a single useful *direction*, and concludes ES cannot find
  anything at LLM scale. `LIT-230` measures the same 40× parameter drift,
  agrees on its magnitude, and finds the gains concentrated in a sparse
  identifiable *subspace* — LayerNorm weights and attention projections. A
  random direction's projection onto a `k`-dimensional subspace is not its
  projection onto a line. Both notes now carry that, as the open question it
  is rather than as a resolution.

### Changed

- **`SOTA-154` is `Active`** — fine-tune with evolution strategies instead of
  policy-gradient reinforcement learning. Its own promotion condition asked
  for "an independent group running evolution strategies against a
  policy-gradient baseline that got the same tuning budget, on a task outside
  Countdown and the conciseness objective", and `LIT-233` is that: six
  further tasks, three model families at 0.5B–8B, all arms matched on
  training FLOPs, with PPO and GRPO grid-searched over learning rate and
  batch or group size while ES ran one fixed configuration. ES came out ahead
  in most cells.

  That evidence arrived as a *baseline* in a paper arguing for something
  else, and this record's first pass discounted it for that. **It was wrong
  to.** A group tuning the rival harder than the method, with no stake in the
  outcome, is the stronger form of the evidence the condition asked for, not
  the weaker. The half of the condition still unmet is the other one — no
  released model's post-training recipe uses it.

- **`SOTA-154`'s consensus moved from `unreplicated` to `contested`**, with
  `contested_by: LIT-231`. Both halves of that are new in the same edit
  and it is not a hedge: what makes it contested is a fourth group arriving
  with a counter-argument, which could not have been recorded while the axis
  still said nobody had replied.

- **`SOTA-212` is `introduced_by: LIT-211`, not by its own source.** The
  paper it rests on measures the method and declines to recommend it — "our
  goal is not to promote RandOpt as superior to alternative methods. Rather,
  we use it as a probe." The work that first stated the instruction is Qiu et
  al., and this is that instruction with the iteration count set to one and
  an ensemble on the end. It now `extends:` `SOTA-154` rather than being
  recorded only as a rival measured against it.

### Added

- **`LIT-229` — Evolution Strategies at the Hyperscale** (Sarkar et al.,
  2025), EGGROLL. `extends:` `LIT-211`. Replaces each worker's full-rank
  Gaussian perturbation with a rank-`r` product, cutting auxiliary memory per
  layer from `O(mn)` to `O(r(m+n))` and raising arithmetic intensity enough
  for a hundredfold throughput gain at billion scale — at up to 91% of pure
  batch-inference throughput, which is the number that says the optimizer has
  stopped being the bottleneck. The population average stays high-rank, and
  the low-rank update converges to the full-rank one at `O(1/r)`. Its LLM
  results are on RWKV-7 rather than transformers, which the note says.

- **`LIT-231` — Hyper-ES** (Gu et al., 2026). `corrects:` `LIT-211`, by
  [ADR-017](record/decisions.d/ADR-017.md)'s test: its motivating sentence names a defect in the parent
  rather than refining it — "directly applying ES to billion-parameter LLMs
  is highly ineffective", because almost all random perturbations in such a
  space are near-orthogonal to a useful descent direction. Its fix changes
  the search space rather than the search: cheap GRPO runs supply LoRA
  descent directions and CMA-ES searches merging coefficients over their
  span, which makes it gradient-seeded rather than gradient-free.

### Documentation

- **The record now offers a reading of its own dispute.** Hyper-ES tests only
  models at 1.5B and below, and `THEORY-006` holds that the density of
  task-improving perturbations rises with scale, with gains appearing sharply
  from about 1.5B and absent beneath it. So the dissent is measured exactly
  where this record's account predicts a negative result, and its lemma about
  near-orthogonal perturbations is the needle-in-a-haystack regime under
  another name. Neither paper cites the other; the reconciliation is this
  record's and is labelled as such, in both `SOTA-154` and `LIT-231`.

- **Hyper-ES never runs the method it says does not work.** Its ES baseline is
  CMA-ES over LoRA, not full-parameter ES at the scale `LIT-211` reports. The
  case against direct ES is two lemmas and a figure, which is a legitimate
  argument and not a failed reproduction — a distinction `SOTA-154` now
  states rather than averaging the two into "mixed evidence".

### Added

- **`LIT-233` — Neural Thickets: Diverse Task Experts Are Dense Around
  Pretrained Weights** (Gan and Isola, 2026), with `NOTE-078` as its
  reading. The paper measures the Gaussian neighbourhood of a pretrained
  weight vector and finds it dense with task-improving perturbations, with
  the density rising monotonically with model scale — 0% of perturbations
  match base accuracy on GSM8K at 0.5B against 64% at 32B — and finds those
  perturbations to be task specialists rather than uniform improvements.
  Filed under `analysis-and-evaluation`: the method it proposes is, in the
  authors' own words, a probe for the measurement.

- **`THEORY-006` — task-improving weight perturbations are dense around
  pretrained weights, and denser the larger the model.** It `explains:`
  `SOTA-154`, which is the first time the record carries an argument for
  *why* a gradient-free method can find anything in a billion dimensions, as
  distinct from the observation that it does. It also predicts where the
  property runs out — below roughly 1.5B parameters, and from an untrained
  initialization — and the paper tests that side.

  Filed `Proposed`. One group, one model family for the density curve. The
  promotion condition asks for the measurement repeated by someone
  unconnected to the authors, and explicitly refuses the evidence it is most
  likely to be offered: another post-training method that works, read back
  as confirmation.

- **`SOTA-212` — post-train by scoring many random weight perturbations
  in one parallel pass and majority-voting the best of them.** `Proposed`,
  `unreplicated`. The claim that carries it is wall-clock and parallelism
  rather than accuracy: one training step against 200 for GRPO and 600 for
  PPO, and OLMo3-7B to 70% on Countdown in 3.2 minutes across 200 GH200s.
  Recorded as `compared_against:` both `SOTA-154` and `SOTA-145` — the two
  comparisons the paper actually ran.

### Changed

- **`SOTA-154` has an explanation and a first outside evaluation.** Both
  arrive from the same paper, and they are different things. The explanation
  is `THEORY-006`. The evaluation is that this paper runs evolution
  strategies as one of its own baselines and finds it strong — which is
  corroboration from a group with no stake in it, and arrives as a *baseline
  result* rather than as the replication `promote_when` asks for. The
  practice's status is unchanged.

### Documentation

- **The record now says what an ensembled comparison is worth.** The new
  practice's headline result gives the method a 50-way ensemble and the RL
  baselines one sample, which the paper discloses and then corrects in its
  own appendix: evolution strategies plus the same 50-way vote takes the best
  or runner-up cell in about half the table. `SOTA-212` states the tie
  rather than the headline, and `NOTE-078` files the general form —
  match test-time sample budgets across compared arms — as a candidate
  recommendation rather than a practice, because the paper demonstrates it
  without recommending it.

### Added

- **Three papers on mixture-of-experts structure**, none of which was in the
  record: `LIT-226` (MoEfication, 2021), `LIT-228` (Emergent
  Modularity in Pre-trained Transformers, 2023) and `LIT-227` (Sparse
  Upcycling, 2022).

- **`THEORY-005` — dense feed-forward layers are already mixtures of
  experts, and pre-training settles the partition before the neurons.** It
  `explains:` `SOTA-150` and `SOTA-149`, which is the first time the registry
  carries an argument for why making the FFN sparse *works*, as distinct from
  why you would want it to: the architecture declares a structure dense
  training arrives at on its own, and the structure is at neuron granularity,
  which is what `SOTA-149`'s fine segmentation is matching.

  Filed `Proposed`. Both findings come from one group's line of work, and the
  promotion condition asks for the partition measured by someone unconnected
  to them, or measured inside a trained MoE rather than a dense model.

- **`SOTA-209` — initialize a mixture-of-experts model from a dense
  checkpoint rather than training it from scratch.** `Proposed`. The claim
  rests on Sparse Upcycling's *second* comparison, not its headline: upcycled
  models beat sparse models trained from scratch at the same total budget,
  which is a recommendation about how to start rather than about what to
  build. The scales are T5 and ViT in 2022, and nobody has reported where the
  advantage goes as the post-upcycling budget grows — which is what the
  promotion condition asks for.

### Documentation

- **The lottery-ticket documents are no longer isolated.** `THEORY-005`
  says what they share with the mixture-of-experts line — the dense run is
  what produces the sparse structure, in both — and where the analogy breaks:
  a ticket is static weight-level sparsity that needs a rewind, an MoE is
  conditional activation-level sparsity in which no parameter is removed.

  That difference resolves an apparent contradiction the record was carrying
  without noticing. `THEORY-004` explains sparse-from-scratch failure by
  poor gradient flow at initialization, and mixtures of experts train from
  scratch and work. They are not sparse in the sense that argument is about:
  every expert is dense internally and receives full gradients on its routed
  tokens, and `SOTA-148` exists to keep any from going unused. What is sparse
  is FLOPs per token, not parameters.

### Added

- **A third scheme, `THEORY`, for claims about why something works.** A
  practice tells you what to do; a theory says what is true, and the record
  had nowhere to put the second. [ADR-031](record/decisions.d/ADR-031.md) is the decision.

  It showed up from both ends. Eight of 208 practices state a behaviour
  rather than an instruction — `SOTA-012` "sharpness in the loss landscape
  correlates with test error" is not something you can do — and 48 of 225
  notes are cited by no practice at all, half of them in
  `analysis-and-evaluation`. Two of those notes already said so in their own
  words: `LIT-019` and `LIT-039` each carry a section headed "Carries no
  practice, deliberately."

  A `THEORY` names its `source:` like a practice does, and `explains:` the
  practices it underwrites; `luria link --fix` writes `explained_by:` back
  onto each of them. The field is optional, because a finding that
  underwrites nothing yet is still a finding.

- **Four documents, filed with the scheme.** The batch-normalization pair is
  the case it was shaped around: `THEORY-001`, the internal-covariate-shift
  account the technique was published with, is `Rejected`, and
  `THEORY-003` corrects it — while the practices remain `Active` and
  `LIT-002` remains worth reading. Three facts that needed three statuses,
  where there were only two places to put them. The lottery-ticket pair
  (`THEORY-002`, corrected by `THEORY-004`) is the other half of
  the argument: an explanation that underwrites no practice at all.

  `LIT-223` can now be cited. It was filed weeks ago saying "the practices
  that turn on the *mechanism* — why BN permits what it permits — belong
  here", and until now nothing in the record could point at it.

### Changed

- **Practices gain an `explained_by:` field**, written by `luria link --fix`
  from the theory side. Two carry one today, `SOTA-006` and `SOTA-020`, and
  in both cases what it adds is a correction: the reason in the practice's
  own source is not the reason the record believes.

- **A stale comment in `luria.yaml` corrected.** `contested_by:` was
  documented as having no converse because luria required one to be
  same-scheme. That has not been true since `LU-ADR-097`; the field still has
  no converse, but now by choice, and the comment says which.

<!-- inactive-ok-file: ADR-030 — Proposed. Named as the decision this
     contribution files; the citation is to its reasoning, not a claim it is
     settled. -->

### Changed

- **`introduced_by:` is required on every practice**, and all 208 carry it.
  [ADR-030](record/decisions.d/ADR-030.md) supersedes [ADR-029](record/decisions.d/ADR-029.md), which had made the field optional.

  [ADR-029](record/decisions.d/ADR-029.md) set a condition for promoting it: a pass over the practices should
  find origins that differ from the primary source often enough for the
  second field to carry information rather than duplicate the first. That
  pass has now run, and it is worth recording that **it did not find those
  numbers** — 168 practices cite exactly one source at all, and across all
  208 exactly three have an origin that is not `source[0]`.

  The field is required anyway, for a reason the condition did not test. An
  absent `introduced_by:` was ambiguous between *the origin is the primary
  source* and *nobody checked*, and those are different claims. Every
  practice now asserts an origin, which is a thing a reader can find wrong —
  `SOTA-087` spent years dating a 2019 recommendation to 2022 precisely
  because nothing had been asserted for anyone to check.

- **The practice scaffold carries the field**, with a note that the usual
  case is the same code as `source:` and that a difference is worth a
  comment. The lint caught its absence from the form as a violation the
  moment the field became required, which is the mechanism working.

### Fixed

- **`SOTA-121` now names its own origin in a field.** Its source block had
  been carrying "[LIT-159](record/literature.d/LIT-159.md) is the origin" in prose that no field could hold.

### Changed

- **The luria pin is `0.22.0`**, from `0.20.4`. Nothing about this record
  changes; the lint stops doing the same work repeatedly.

  `luria lint` over this record goes **128.2s → 12.9s**, measured here on
  both versions. The releases in between cache a scheme's directory
  listing, route every document read through one cache, cache the directive
  scans, render the view tree once per lint, and compile each scheme's code
  regexes once — all of it work this record was paying for on every CI run.

  Verified before pinning rather than after, and worth doing carefully
  because 0.22.0 changes lint *semantics* as well as speed: it adds a
  `mention-ok:` directive and fixes a bug where one stale code in a shared
  acknowledgement disabled the whole acknowledgement. Neither changes
  anything here — lint output is byte-identical, all 87 generated views
  hash identically, and `luria site` stages 633 pages with no links
  redirected to the repository.

<!-- inactive-ok-file: ADR-028 — Proposed. Named as the decision this
     contribution files; the citation is to its reasoning, not a claim it is
     settled. -->

### Changed

- **The configuration is one `luria.yaml`.** `luria.toml` and the ten
  vocabulary files beside the records are gone; everything they held is in
  one file, and every one of their 369 comment lines came with it.

- **One `topics` vocabulary, shared by the practice registry and the reading
  list — glosses included.** [ADR-026](record/decisions.d/ADR-026.md) made the two lists the same thirteen
  words and recorded that "the two vocabularies become identical". The keys
  did; each scheme kept its own copy of the blurbs, ten of the thirteen
  diverged, and the reading list's header still described a vocabulary of
  twelve. [ADR-028](record/decisions.d/ADR-028.md) folds them and says why [ADR-027](record/decisions.d/ADR-027.md)'s deliberate
  narrowing of `analysis-and-evaluation` does not survive the fold.

- **Per-status pages move** from `docs/<scheme>/statuses/` to
  `docs/<scheme>/status/`, because the directory is named for the field and
  the field is `status`. Four directories. Nothing in the record links to
  the old paths — every such link is generated — so no internal link breaks;
  inbound links from elsewhere will.

- **The luria pin is `0.20.4`**, from `0.15.0`.

### Fixed

- **Four links to the principles document reached nothing.** They were
  written zero-padded (`#dp-009`); the page emits `#dp-9`. The newer lint
  reports an anchor that resolves to no heading and no `id`, which is how
  these surfaced after five months.

- **Stale configuration prose, now that it is somewhere a reader passes.**
  The practice group's comment said "Seven categories" when there have been
  thirteen since [ADR-026](record/decisions.d/ADR-026.md); two comments still named the temporary
  codes two of those decisions carried before they were numbered, which
  `luria link --fix` does not reach inside a configuration file; and
  `docs/README.md` said the record page is generated from `luria.toml`.

### Added

- **`LIT-225` — Child et al. (2019), *Generating Long Sequences with
  Sparse Transformers* (`ARXIV-1904.10509`).** The origin of the sliding
  window the record uses in seven other notes and five practices, and had no
  document for: causal attention factorized into a local window of the
  previous `l` positions and a second head that escapes it, `l ≈ sqrt(n)`.

- **`SOTA-208` — that factorization, filed `Superseded`** (by
  `SOTA-138`, sparsity that is learned rather than fixed). Being superseded
  is not a reason to omit a recommendation; it is the reason to record what
  the record stopped believing (`DP-003`). Its enwik8 result is the
  strongest evidence in the corpus for the practice that replaced it:
  strided attention 1.13 bpb where dense gets 1.00, the fixed pattern 0.99,
  the same strided pattern winning on CIFAR-10. The escape's shape has to
  match the data's structure, and choosing it by hand is how you lose to
  dense attention outright.

- **`ADR-029` (`Proposed`) and `introduced_by:` on the `SOTA` scheme.**
  `source:` was one ordered list doing two jobs — naming the work that
  produced evidence about a claim, and naming the work the claim came from.
  `ADR-017`'s retraction test picks the first by construction, so the record
  read as though every practice began with the paper it cites.

      introduced_by:
        scheme: LIT
        required: false
        many: true

  `source:` is unchanged: still ordered, still primary-first, `published:`
  still derived from it. `many: true` because parallel invention is real
  (`LIT-208` and `LIT-209` arrive at one layout three months apart);
  optional because for most practices the origin *is* the primary source,
  and a field every record shares is `DP-002`'s failure.

### Fixed

- **`SOTA-087` was dating a 2019 recommendation to 2022.** *Recompute
  attention during the backward pass instead of storing it* is Child et al.
  §5.4 — *"we recompute the attention and feed-forward blocks during the
  backwards pass"* — and what FlashAttention changed is the **price**, not
  the instruction. `LIT-074` stays primary, because the body's argument is
  Dao's and would not survive its retraction; the origin now has a field.

- **`SOTA-060` named its own origin and cited nothing.** Its body reached for
  *"the 1/√(2·n_layers) factor on the output projections in GPT-2-style
  initialisations"* — that factor is Child et al. §5.2, `1/sqrt(2N)`, with
  the invariant it protects stated: the ratio of input-embedding scale to
  residual-block scale, held constant in depth. An uncited claim inside a
  practice, in a record whose first design principle is that the citation is
  structural.

- **`SOTA-138`'s `Sequence` began at February 2025.** The line it describes —
  sparse attention, and how to choose the pattern — starts at the fixed
  patterns of 2019 it is the answer to. Second instance of `SOTA-132`'s
  "describing a line from its middle", and found the same way: by following
  a citation backwards.

### Changed

- **`LIT-033` (Longformer) declares `compared_against: LIT-225`.**
  Longformer calls it *"the model with the most similar attention pattern to
  ours"* and reports matching its enwik8 result; the comparison is declared
  on the note whose paper ran it (`ADR-011`).

### Changed

- **`published:` is derived, not stored (`#119`, luria 0.15.0).** A practice
  takes the publication date of its **primary** source; a reading note takes
  its paper's. Neither carries a copy.

      [luria.schemes.SOTA.fields.published]
      derive = "{published}"
      from   = "source[0]"

      [luria.schemes.NOTE.fields.published]
      derive = "{published}"
      from   = "paper"

  **183 stored copies deleted.** The date lives in one place — the `LIT` note
  about the paper — and is read from there. Writing it anywhere else is a lint
  violation, not something a checker notices afterwards.

  `source[0]` is the primary source because `ADR-010` makes the list ordered
  and `ADR-017` makes the first entry the one that would force a rewrite if it
  were retracted. That was already the convention: **175 of the 183 practices
  that carried the field by hand used exactly this.** It had never been written
  down, which is why eight had drifted to the date of a source they no longer
  cited — `SOTA-048`'s came from a paper absent from its `source:` list
  entirely. Those eight are not corrected here. They are **unrepresentable**.

- **`LIT` declares `published:` required.** It was convention: load-bearing for
  the scheme's `alias` template and never declared. A followed template checks
  its names against the target scheme, so the declaration is what makes
  `{published}` resolve rather than silently yield nothing on every practice.

- **luria is 0.15.0 everywhere** — the four `pip-spec`/`pip install` pins and
  the five `dmarx/luria/actions/*@` refs, which were still on `0.12.0`. The
  action tree is byte-identical between the two tags, so the ref bump changes
  no behaviour; it removes a mixed-version signal a reader would have to check.

  One `pip-spec: ""` stays, in the pull-request lint: it reuses the install the
  `generate` step made in the same job, and pinning it twice would be two
  places to keep in step.

### Fixed

- **The published site was building on an unpinned luria.** `pages.yml` called
  the `site` action with no `pip-spec`, so it took the action's default — bare
  `luria` — and installed whatever release was newest while every other job was
  pinned. Nothing had gone wrong yet, and nothing would have said so: the site
  builds from its own workflow, and a version only it uses is a version nobody
  compares against anything.

- **The `LIT` template did not scaffold `published:`**, so a note copied from
  the form started in violation of the contract the field now has. Found by the
  scaffold check the moment the declaration landed.

- **The template's `date:` comment described a different field.** It read *"the
  arXiv posting month, from the id"* — that is `published:`. `date:` is when the
  record filed the note. One explanation, two fields, and it explained the one
  that did not exist yet.

- **"Exactly one of the twelve in `tags.yaml`"** in the same template.
  Thirteen since `ADR-026`.

### Found

- **`concretize` rewrites references, not values**, and the lint had no rule
  relating one document's field to another's — which is why a copied field
  could disagree with its original indefinitely with every mechanical check
  green. The gap is closed upstream rather than papered over here: this record's
  own bespoke checker became the evidence for `LU-#233`, and was superseded by
  it before merging.

- **Verified against the corpus, not fixtures:** 207/207 practices and 74/74
  reading notes resolve with nothing stored, and all eight formerly-stale
  practices compute the right value. Reinstating `SOTA-150`'s historical
  `2024-01-01` makes `luria lint` exit 1 and name the derivation; removing it
  returns to 0.

### Fixed

- **`record/practices.d/tags.yaml` contradicted itself about its own
  vocabulary.** Its header said:

  > What stays LIT-only is generative-modeling and vision-and-graphics, which
  > name a domain rather than a kind of claim (`ADR-020`).

  Both are declared sixty lines further down the same file. A contributor
  reading it top to bottom was told the two domain topics do not exist here,
  then shown them. The header now records how all thirteen arrived — seven
  transcribed, then `ADR-021`, `#114`, `ADR-027`, `ADR-026` — and states the
  invariant `ADR-026` established: **the two lists are the same thirteen, and
  nothing here is LIT-only.**

- **Nine stale temporary codes in configuration comments**, none of which any
  tool would have caught: `ADR-021` → `ADR-021`, `ADR-027` →
  `ADR-027`, `ADR-026` → `ADR-026` (four sites), `ADR-025` →
  `ADR-025` (two sites), and `LU-ADR-tmphedn4` → `LU-ADR-084`, a cross-repo
  reference whose target concretized in luria's own record.

  Files: `record/practices.d/tags.yaml`, `record/notes.d/statuses.yaml`,
  `luria.toml`.

  `LIT-tmp3kf9x` in `ADR-013` is **deliberate** — it illustrates the shape of a
  minted code and carries an `unresolved-ok-block` saying so. Left alone.

### Found

- **`luria concretize` does not reach comments in `.yaml` and `.toml` files.**
  It renumbers documents and rewrites references in markdown prose and
  frontmatter, which is where codes normally live. Configuration comments are
  neither, so a temp code written into one survives the merge that numbered its
  document — silently, and for as long as nobody reads that file.

  This is the fifth time in a week a change has left prose stale in a way no
  check can see, after `SOTA-120`'s promotion (8 directives), `LIT-085`'s (7),
  five topic counts found in a merge, and six notes saying nothing was sourced
  to them. The previous four were all markdown. **This one is worse, because
  the stale text was in the file that defines the rule** rather than in a
  document describing it.

  The sweep that found it is cheap and worth keeping: grep the whole repository
  for `-tmp[a-z0-9]+` outside a `formerly:` block, and expect exactly one hit —
  `ADR-013`'s illustration.

### Added

- **Five practices, from the audit of notes that source nothing (`#121`).**

  **Diffusion sampling**, which the record had no holding of at all. Its four
  diffusion practices — `SOTA-187`, `SOTA-188`, `SOTA-195`, `SOTA-202` — are
  every one of them about training or parametrization, while the three
  unsourced generative papers in the corpus are every one of them about
  sampling. The record said how to train a diffusion model and nothing about
  how to sample from one, while holding the three papers that decided how
  everyone samples.

  - Sample with a **higher-order ODE solver** on weights you already trained
    (`LIT-076` primary, `LIT-038` corroborating). The diffusion ODE is
    semi-linear: solve the analytic part exactly and approximate only the
    neural integral. 10-20 NFE, training-free. Stated as *higher-order* rather
    than by product name because **DDIM is exactly the first-order case**.
  - Use the **deterministic sampler** when the noise input has to mean
    something (`LIT-038`). Inversion and interpolation are structural
    consequences of zero injected noise. Qualified by `LIT-075`: stochasticity
    corrects accumulated error, so this is not a blanket recommendation.
  - **Keep a multi-step option** in a few-step model (`LIT-093`). The property
    worth having is that the step count is a knob.
  - **Anneal a discretisation** from coarse to fine (`LIT-093`), `Proposed` —
    the mechanism is general and the evidence is one paper in one setting.

  **And a convergence the readings had already found.** Four papers, three
  mechanically unrelated structures — a hash grid, planar factorisations,
  anisotropic Gaussians — reaching one conclusion inside eighteen months:
  replace a large coordinate network with a compact explicit structure and a
  small decoder (`LIT-064`, `LIT-108`, `LIT-086`, `LIT-109`). Filed as one
  practice with four sources, because what converged is the **decision** and
  not the mechanism.

### Changed

- **Every unsourced note now states its standing.** Twenty-five did already;
  twenty-four had a Standing section silent on the question, and now say what
  the audit concluded and what remains a candidate. Twelve are retired or
  tombstoned, where the status is itself the reason.

- **`SOTA-051` gained `LIT-089`.** It had been arguing from ControlNet's zero
  convolutions for its sharpest content — *zero is not "near zero"* — without
  naming the paper in `source:`. Under `ADR-017`'s retraction test that section
  does not survive the paper's removal.

- **Six documents that said nothing was sourced to them** were corrected in the
  same commit as the filing that made them wrong: `LIT-038`, `LIT-076`,
  `LIT-093` and their three readings. The readings are annotated rather than
  rewritten — a reading is a dated observation.

### Found

- **`ADR-017` already contained the audit's criterion.** *If this paper were
  retracted tomorrow, would the practice need rewriting?* — written to settle
  whether adopters belong in `source:`, and it answers this question too. The
  audit did not need a new rule, which matters because `ADR-017` is itself the
  record of what an invented mid-pass rule cost.

- **A deliberate deferral must say it is one.** All three sampling readings end
  *"Nothing is sourced to this paper and this reading files no practice"* — a
  pass policy that reads, a year later, as a judgement about the paper.
  "Nothing is filed" and "nothing should be filed" are different claims and
  were written the same way.

- **A note that sources nothing is fine; one that does not say why is not.**
  `DP-008`'s mechanism exactly: nobody re-reads an absence, so silence is
  indistinguishable from nobody having got round to it and every future audit
  pays the same cost again. Counting unsourced notes measures nothing.

- **The link can exist in prose and not in data, as well as the reverse.** The
  last three contributions kept finding prose left stale by a data change.
  `SOTA-051`/`LIT-089` is the inverse, and equally invisible to the lint.

- **`LIT-004` is a generic-bullet note the bullet-signature pass missed** —
  that pass selected on a signature, and a document can be equally empty
  without matching it. It is the gradient checkpointing paper, and it sits on a
  gap: the record recommends recomputation only for attention (`SOTA-087`) and
  holds no general activation-memory practice among twenty-nine
  `distributed-optimization` entries. **Nothing was filed from it** — filing
  from four bullets naming the category is the failure two passes have been
  spent correcting, and the fix is a reading.

- **Seven notes are unsourced because nobody has read them**, three of them a
  coherent joint-embedding cluster. Different from a paper read and declined,
  and the determinations say so rather than implying an assessment that never
  happened.

### Changed

- **The practice registry and the reading list now share one topic vocabulary
  — the same thirteen.** `ADR-026` adds `generative-modeling` and
  `vision-and-graphics`, and supersedes `ADR-020`.

  `ADR-020`'s **decision** is carried forward unchanged: recommendations are
  scoped by the kind of claim, not by the domain the work came from. What is
  superseded is the **alternative it rejected** — it declined to add these two
  topics on a browsing argument, and that paragraph had started being cited as
  a scope boundary, which is the exact thing `ADR-020` was written to remove.
  A widening decision containing a narrowing argument is a document that gets
  misread, and editing the paragraph leaves the shape.

  **The evidence against the browsing argument:** eight in-force practices are
  sourced to generative-modeling or vision-and-graphics papers, **none uses
  either word as a secondary tag** (so nothing is displaced), and **all eight
  already took a kind-of-claim topic** unprompted. The objection was an
  argument against mis-tagging, and `ADR-003`'s one-primary rule already
  answers that: making a word available does not make it the right answer.

  **The filing rule**, so the objection does not materialise: *take a domain
  topic when the claim is about the domain as such; a claim merely discovered
  in a domain still takes its kind.* If in doubt, ask what the practice would
  still be true of if the domain changed.

  This is **not** the merge `ADR-003` rejected. That was merging *downward* —
  forcing `LIT` documents into a narrow practice vocabulary. This merges
  *upward*: nothing is forced anywhere and both schemes gain range. The two
  schemes now differ in what a document **is**, not in what it may be
  **about**.

  **The cost, stated:** a topic in an `exactly-one` group cannot also be a free
  secondary tag, so `generative-modeling` can no longer be a secondary marker
  alongside another primary. No document does that today.

  **Nothing is retagged**, and the two candidates that looked plausible did not
  survive a look — `SOTA-187` argues for its own kind-of-claim filing in its own
  body, and `SOTA-157` is a claim about building a language model. The two new
  topics are available and currently unused, which is the expected outcome: a
  word that is available and correctly unused is doing its job.

- **`ADR-020` retired to `Superseded`**, and the seven prose sites that cited it
  as the live rule now point at the successor: `CLAUDE.md`, `luria.toml`,
  `DP-008`, `SOTA-076`, `LIT-096`, the literature `README.stub`, and
  `ADR-027` — whose own aside from the previous day had repeated the
  misreading and is amended to say so.

- **`SOTA-187`'s body named a topic it no longer carries.** It argued it was
  filed `model-architecture`; it has been `representation-and-encoding` since an
  earlier retag, and that topic — "how the signal is encoded before the
  expensive network sees it … tokenizers and learned latents" — is the better
  fit. The argument is unchanged; the prose had not followed the tag.

### Found

- **Five vocabulary decisions have converged on "the list the other scheme
  always had".** Seven → ten (`ADR-021`) → eleven with
  `representation-and-encoding` (`#114`) → twelve with
  `analysis-and-evaluation` (`ADR-027`) → thirteen here. Each was
  discovered separately, by something needing to be filed. **The vocabulary was
  not short of words; it was short of the words the other half of the record
  already used.**

### Added

- **`analysis-and-evaluation` joins the practice vocabulary**, making eleven —
  `ADR-027`. It was the one topic the literature vocabulary had and the
  practice vocabulary lacked that is a **kind of claim** rather than a domain;
  `generative-modeling` and `vision-and-graphics` are still absent on purpose
  per `ADR-020`. Orthogonal to `ADR-024`, whose seams are all *between* topics
  that exist.

- **Ten practices from the [#123](https://github.com/dmarx/anthology-of-the-sota/issues/123) readings.**

  | practice | source | what it says |
  |---|---|---|
  | `SOTA-200` | `LIT-077`, `LIT-085` | Check whether an emergent capability is a metric artefact |
  | `SOTA-196` | `LIT-072` | Report zero-shot and in-distribution separately — one dial moves them opposite ways |
  | `SOTA-197` | `LIT-060`, `LIT-077` | Grade evaluation by test/train proximity; state your contamination exposure |
  | `SOTA-194` | `LIT-080`, `LIT-099` | State the dataset composition before crediting the objective it arrived with |
  | `SOTA-192` | `LIT-088` | Normalize queries and keys before the attention dot product |
  | `SOTA-198` | `LIT-017`, `LIT-065` | Measure the gradient noise scale; expect it to grow and ramp the batch |
  | `SOTA-193` | `LIT-065` | Lower β₂ when the loss spikes, before the learning rate |
  | `SOTA-201` | `LIT-072` | Per-component learning rates; both corners are wrong |
  | `SOTA-199` | `LIT-079` | Regularize a narrow fine-tune against the pre-update model's own samples |
  | `SOTA-195` | `LIT-067` | Predict `v` when the model will be evaluated at low SNR |
  | `SOTA-202` | `LIT-073` | Clamp the prediction to the training range at every sampling step |

### Changed

- **`LIT-085` promoted `Rejected` → `Active`.** Its own reading recorded the
  data-fraction result as something any claim about delayed generalization needs
  to know, and in the same breath declined to argue with the status. Filing
  `SOTA-200`, which needs it, made that untenable. `ADR-002` permits an
  attic paper to source a live practice, and that permission is for a paper
  whose *standing* moved while its *result* held — nothing about this result
  moved. **A small setting is a limitation to state, not a reason to retire.**

- **Seven practices enriched**, recommendations unchanged:

  - `SOTA-188` gains `LIT-067` as a second source — the same requirement stated
    empirically four months before EDM derived it — and points at `v`-prediction
    as what people actually type.
  - `SOTA-187` gains `LIT-036`, which **measures** the premise it rests on two
    years before its own source assumed it.
  - `SOTA-097` gains `LIT-017`, where critical batch size is defined. The record
    carried the exponent without its origin.
  - `SOTA-002` records that MT-NLG trained at **β₂ = 0.95** and why. 0.999 is
    Adam's default and not what large runs use, and the practice now says so.
  - `SOTA-051` gains the adapter case: ControlNet's zero convolutions and LoRA's
    zero-initialized `B` are the same instrument applied to a branch attached to
    an *already trained* model, where **zero is not "near zero"** — one is
    probably harmless, the other is provably the identity.
  - `SOTA-131` names `SOTA-192` as the other route to its invariant, now
    with a source. Still uncompared.
  - `SOTA-191` gains a second 22B data point on the *other* side, plus the
    qualification that ViT-22B keeps its MLP biases while dropping the rest —
    so bias removal is not uniform even inside one model.

### Found

- **Three instruments for protecting a pretrained component now sit together**
  and none has been compared against the others: turn the learning rate down
  (`SOTA-201`), regularize toward the old model (`SOTA-199`), or do
  not touch the weights (`SOTA-184`).

- **Three instances of one instrument** — bound a quantity fed back into the
  process that produced it: gradients (`SOTA-035`), activations in low precision
  (`SOTA-158`), predictions in sampling (`SOTA-202`). The record says
  nothing about the other two places this structure appears, autoregressive
  decoding and agent loops.

### Changed

- **The generic-bullet `LIT` corpus is read out.** 49 papers read against their
  sources, with takeaways replaced by the papers' own mechanisms, numbers and
  scope — **47 `Read`, 2 `Skimmed`**. The fiftieth, `LIT-116`, has no paper to
  read and got a repair instead (below).

  Every reading files a `NOTE`, so the record no longer holds documents that
  look read and are not. Re-running the census that opened this: **0 of 224
  `LIT` documents now carry the generic-bullet signature with no reading**, down
  from 52.

### Fixed

- **Nine takeaways stated something the paper does not contain**, and six of
  those state its inverse or its subject:

  | document | said | is |
  |---|---|---|
  | [LIT-038](record/literature.d/LIT-038.md) (DDIM) | "continuous-time formulation", "connection to SDE theory" | **a different paper** — Song et al.'s SDE paper. DDIM is discrete-time and non-Markovian |
  | [LIT-111](record/literature.d/LIT-111.md) (OnePose) | "category-level pose estimation" | the paradigm it exists to avoid — it needs **no** category-specific training |
  | [LIT-108](record/literature.d/LIT-108.md) (3D Gaussian Splatting) | "dynamic scene optimization" | **static** scenes; the optimisation is density control during fitting |
  | [LIT-070](record/literature.d/LIT-070.md) (unCLIP) | "improved composition ability" | its own Figure 15 shows composition *failing* — attribute binding is lost |
  | [LIT-089](record/literature.d/LIT-089.md) (ControlNet) | "zero-shot conditioning" | zero-**initialized** convolutions; the adapter is trained per condition |
  | [LIT-091](record/literature.d/LIT-091.md) (T2I-Adapter) | "zero-shot control" | trained adapters that *transfer* to fine-tunes of the same base |
  | [LIT-031](record/literature.d/LIT-031.md) | "feature disentanglement", "impact on generalization" | measures connectivity; contains no generalization claim |
  | [LIT-048](record/literature.d/LIT-048.md) (ALiBi) | "theoretical analysis" | none exists — the slopes come from trying about ten sets by hand |
  | [LIT-101](record/literature.d/LIT-101.md) (AdaNorm) | "large-scale model optimization" | a title ending "for CNNs"; largest dataset TinyImageNet |

- **`LIT-116` stopped citing the paper it disavows.** Its Standing section said
  the recorded arXiv identifier belongs to an unrelated physics preprint; the
  summary and body byline went on rendering that identifier as its source. A
  document contradicting itself in prose is one thing, and one that keeps
  *rendering* the citation it disavows is a live link to the wrong paper.

### Found

- **Twelve findings the record holds narrowly or not at all**, each recorded in
  its note's Bearing section rather than filed as practice:

  - **`LIT-067` is `SOTA-188`'s antecedent.** Four months before EDM it states
    the problem — the implied `x̂` must stay stable as log-SNR varies — and
    gives three solutions, one of which is **v-prediction**, which the record
    mentions nowhere.
  - **`LIT-017`'s critical batch size is why 3D parallelism exists.** `LIT-065`
    says data parallelism caps out because batch size does; the record carries
    both legs and not the joint.
  - **`LIT-036` §4.3 measures the premise `SOTA-187` rests on** — that most
    capacity goes to imperceptible detail — which its own source treats as an
    assumption.
  - **`SOTA-131`'s alternative has no reading.** The record carries QK-Clip and
    calls QK-norm the other route to the same invariant; `LIT-088` is an early
    demonstration of it, with the mechanism diagnosed.
  - **Four independent arguments that the measurement produced the surprise** —
    `LIT-077` (brittle metrics), `LIT-085` (grokking vanishes above 60% data),
    `LIT-073` (DrawBench), `LIT-072` (two metrics, opposite optima).
  - **Three instruments for protecting a pretrained component**, none stated:
    `LIT-079`'s prior preservation, `LIT-072`'s 100× learning-rate asymmetry,
    `LIT-089`'s zero-initialized branch.
  - **`LIT-060` trades parameters against inference-time tokens**, a third
    allocation axis, and its capability rises *after* training ends.
  - **`LIT-073`'s dynamic thresholding** is a third instance of `SOTA-035` and
    `SOTA-158`'s instrument — bound what compounds — in a third place.
  - **`LIT-065` lowers β₂ to suppress loss spikes**, a stability lever the
    record names nowhere.
  - **`LIT-102` counts quantization *events*** along a path; the record's
    low-precision practices reason only about bit width.
  - **`LIT-087`'s KL reduction** ranks data selections without training, next to
    `SOTA-166`'s mixing law which costs training runs.
  - **`LIT-040` and `LIT-099` complete an arc** the record held only the middle
    of: sub-linear (2020) → 1:1 (2022) → 1:1 independently confirmed (2023).

- **`LIT-057` and `LIT-092` are both `Rejected` and argue with each other.**
  InfoMin is an augmentation-and-objective account of contrastive learning;
  `LIT-092` shows that genre of account cannot explain downstream performance
  and is provably vacuous in places. Recording the disagreement is worth more
  than either alone.

### Changed

- **`SOTA-120` promoted, `Deferred` → `Active`.** Its `promote_when:` asked for
  "a survey or a frontier training report that states which of the two it
  uses, rather than leaving the choice implicit in a config", and the record
  has since acquired both without anyone going looking. [LIT-156](record/literature.d/LIT-156.md) is that
  survey exactly — ten optimizers, four scales, each separately tuned, all
  measured against **a well-tuned AdamW**. [LIT-122](record/literature.d/LIT-122.md) is the stronger case,
  because there decoupling is a *stated design decision*: two changes carried
  Muon from small-scale results to a 3B/16B model on 5.7T tokens, and applying
  weight decay was one of them.

  The deferral rested on a doubt carried verbatim from the old `sota_maybe`
  field — *"I feel like everyone still uses vanilla Adam though"* — and the
  frontier reports answer it by name. This is the case the pending-decisions
  report describes as **a decision the codebase already made and never wrote
  down**; `consensus: converged` had been saying so on the other axis the
  whole time.

- **`LIT-101` (AdaNorm) and `LIT-104` (ReLoRA) read** — [NOTE-025](record/notes.d/NOTE-025.md) and
  [NOTE-024](record/notes.d/NOTE-024.md). Both were the oldest entries on the pending-decisions
  report, both carried the generic-bullet signature [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114) identified, and
  both were wrong about their papers:

  - `LIT-104` said **"rank-based layer stacking"**. ReLoRA stacks nothing;
    it restarts a LoRA adapter on a fixed architecture so that a sequence of
    low-rank updates sums to a high-rank one. It was tagged
    `model-architecture` on the strength of that bullet, and is now
    `training-optimization`, which is what a training procedure is.
  - `LIT-101` said **"large-scale model optimization"** about a paper whose
    title ends *"for CNNs"* and whose largest dataset is TinyImageNet, and
    **"scale-invariant updates"**, a property the paper never claims.

  Both stay `Proposed` — and for the first time carry what that status
  requires, a stated condition that would settle them.

- **Eight `inactive-ok` directives removed**, and the prose beside each one
  rewritten. Promoting `SOTA-120` invalidated every acknowledgement that had
  cited it as not-in-force, across `ADR-014`, `LIT-012`, `NOTE-015` and
  `SOTA-001`. `ADR-014` gains the better example in the exchange: it argued
  that a *social* promotion condition is well-formed, and the one it cited has
  now been collected by other people's work, which is the outcome it was
  betting on.

### Found

- **`#114`'s worklist was the complete at-risk set.** 52 `LIT` documents still
  carry the generic-bullet signature with no reading — and **none of them is
  the source of any in-force practice.** Verified by two independent
  traversals (paper→practice and practice→paper, 150 source edges, 78 cited
  papers), because a clean zero in this repository has been a broken detector
  before.

  So the 52 are decorative rather than dangerous, and reading them would
  correct no recommendation. Recorded in the curation journal, mostly to say
  that the obvious next move after `#114` is the wrong one.

### Changed

- **The one `Skimmed` reading is now `Read`, and `SOTA-188` is confirmed.**
  `ar5iv` has no rendering for `arXiv:2206.00364`, so `NOTE-019` (EDM)
  was written from the abstract and said so, and the practice it sources was
  left visibly unverified. dmarx supplied the full text; the note is rewritten
  from the paper, with the claims table it was not entitled to before.

  This is the round trip `Skimmed` exists for. The gap was recorded where the
  next reader would find it, and it was the note's own open question that
  closed it.

- **`SOTA-188` corrected at v2.** It said the noise-dependent scalings were
  "chosen so the effective training target has unit variance at every level",
  which reads as though all four came from that requirement. Appendix B.6 says
  otherwise: `c_in` and `c_out` are derived from unit variance, `c_skip` from
  minimising the amplification of the network's own error, the loss weight
  `λ(σ)` from flattening each level's contribution, and `c_noise` is a curve
  fit the paper itself calls empirical. **One of the four coefficients in a
  section titled as a principled analysis has no derivation**, and a practice
  that implies otherwise oversells the principle.

  The recommendation is unchanged. What changed is how much of the recipe it
  claims to cover — and that the log-normal's parameters (`ln σ ~ N(−1.2,
  1.2²)`) are tuned per dataset, not derived.

- `LIT-075`'s takeaways come from the full text rather than the abstract, and
  its Standing no longer says the practice is unverified.

### Added

- The last four readings, all confirming: `NOTE-011` (*Attention Is All
  You Need* → `SOTA-050`), `NOTE-020` (*Don't Stop Pretraining* →
  `SOTA-033`), `NOTE-009` (*Latent Diffusion* → `SOTA-187`),
  `NOTE-018` (*Segment Anything* → `SOTA-186`).

  **`#114` is complete: 23 of 23 notes, 45 of 45 practices.** 22 `Read`, one
  `Skimmed`.

Each supplies the thing its practice states without:

- **`SOTA-050`** gives the formula `1/√d_k` and not the reason. The paper's
  footnote is the whole justification — with `q` and `k` components
  independent, mean 0, variance 1, then `q·k` has **variance `d_k`**, so an
  unscaled score grows with the dimension and saturates the softmax. A reader
  who knows only the formula cannot tell whether it generalises. Worth noting
  the paper hedges this as *"we suspect"*, weaker than the record's flat
  statement.
- **`SOTA-033`** is two findings — `DAPT` and `TAPT` — and its title carries
  neither, least of all the second: a few thousand unlabelled task examples
  are worth their own pretraining stage *even after* the domain corpus.
- **`SOTA-187`** needs the condition that the latent be **perceptually
  equivalent**. What the autoencoder discards is a hard ceiling the diffusion
  model cannot see past, not a quality margin.
- **`SOTA-186`** needs its two preconditions: the model must be **useful
  before the dataset exists**, and **confidence must be informative** enough
  to route work. A task failing either never starts the loop. And the note
  names what the record relies on and the paper does not test — that the
  engine generalises past segmentation, where masks are unusually cheap to
  verify.

### Fixed

- **`ADR-021` amended, and `representation-and-encoding` added to the `LIT`
  vocabulary.** That decision added three topics to the *practice* vocabulary
  and observed, in the same paragraph, that the first two "are already the
  `LIT` scheme's, which is the point: where the two vocabularies name the same
  *kind of claim*, they should use the same word." It then did not act on that
  for the third.

  So from `ADR-021` until now, the two vocabularies named the same kind of
  claim with a word only one of them had. It surfaced the way these do: a
  `NOTE` on a tokenization paper had no topic to take, because `NOTE` inherits
  `LIT`'s vocabulary. `LIT-003` — the BPE paper — had been filed under
  `model-architecture` for want of anything better, and is retagged.

### Added

- `NOTE-013` (DeepNet → `SOTA-052`), `NOTE-010` (BPE → `SOTA-007`),
  both confirming, and **`NOTE-019` (EDM → `SOTA-188`), the first
  `Skimmed` reading.**

  ar5iv has no rendering for `arXiv:2206.00364`, so that note is written from
  the abstract alone. Under `ADR-025` that is not enough to source a practice
  from, so **`SOTA-188` is left unverified — deliberately and visibly** — and
  the note says so instead of implying it was checked. The lint then flagged
  the note's own citation as not-in-force, which is the design working: a
  `Skimmed` reading is not in force, and citing one is a thing worth
  acknowledging.

  `SOTA-052` is confirmed and far vaguer than its source. "Use smaller
  variance for deep networks" describes `β` and states neither the exponent
  (`(8M)^(−1/4)` for a decoder), nor that `α` grows as the same root, nor that
  **query and key projections are excluded from the downscaling** — the last
  being what a reader would most plausibly get wrong.

### Changed

- **`inert-status` and `acknowledged-uniformity` muted**, via `[luria.lint]
  mute` — the global switch added in luria 0.14.0 (`LU-#232`).

  `uniform_ok` on the `NOTE` scheme stays and carries the reason, because the
  *why* is worth recording even when the line is not printed: the scheme is
  uniform by design (`ADR-025`), since a note is written when someone
  finishes a paper and the absence of one is how this record says "unread".
  The mute is the answer to the separate question of whether the finding is
  worth reading every run here. It is not.

- CI's luria pin bumped `0.13.0 → 0.14.0` in the four `pip-spec` sites, which
  is what the `mute` key needs. The `dmarx/luria/actions/*@0.12.0` refs are
  left alone: they pin the *action definition*, the pip-spec pins the
  *package*, and the lint runs from the package. Verified against the real
  released 0.14.0 rather than the working tree.

### Changed

- **`ADR-025` amended: the absence of a `NOTE` means the paper is unread.**
  No `Unread` stubs are filed. `Unread` stays in the vocabulary for what
  absence cannot express — a deliberate human judgement that a paper was
  looked at and set aside. "Nobody has got to this yet" is silence; "I opened
  this and decided not to read it" is a fact.

  So luria's inert-status check will keep reporting `NOTE: n/n Read` while
  every filed note is a finished reading, and that is the honest shape of the
  field rather than a defect to engineer around.

- `SOTA-008` (linear warmup for large batch) **re-sourced** to `LIT-007`
  (Goyal et al.), where warmup comes from. `LIT-009` (LARS) cites it as prior
  art — *"Linear scaling of LR with a warm-up is the state-of-the-art
  recipe"* — and then argues against its sufficiency: the recipe **"is not
  general enough and training may diverge"**. The record had the practice
  sourced to the paper that found its **limit**. LARS is retained beside it
  for exactly that reason.

  **Second instance of this shape**, after `SOTA-113`/Orca: the citation
  landed on the more famous later paper, which described the technique in its
  background while contributing something else.

### Added

- Four readings, all **confirming** their practices:
  `NOTE-022` (RMSNorm → `SOTA-182`), `NOTE-015` (AdamW →
  `SOTA-120`), `NOTE-012` (LARS → `SOTA-008`), `NOTE-021` (GQA →
  `SOTA-109`).

Three things the readings surfaced that the record did not hold:

- **RMSNorm states its claim as a hypothesis** — "we hypothesize that
  re-centering invariance in LayerNorm is dispensable" — and never measures
  what re-centering does. `SOTA-182` is right that centered LayerNorm now
  needs justifying; that is the field's verdict, not this paper's proof.
- **GQA's second contribution, uptraining**, is absent from the practice
  registry: an existing multi-head checkpoint converts for **5% of original
  pretraining compute**, which says an inference-side architectural property
  need not be committed to before pretraining.
- **AdamW has a live tension with `LIT-153`**, which argues that *constant*
  decoupled decay pins a layer's equilibrium norm by hyperparameters rather
  than by data — a consequence of the very mechanism AdamW introduced. Both
  hold.

### Added

- `NOTE-017` — the reading of `LIT-028` (Kaplan et al., *Scaling Laws for
  Neural Language Models*). Seven claims with strengths, every exponent, and
  the methodological point its successor turned on: **the learning-rate
  schedule was held fixed across runs of different length**, which is what
  Chinchilla identified as the source of the wrong allocation exponent.

### Changed

- `SOTA-041` (*lr tuning less important for larger models*) **`Rejected` — it
  states the reverse of its source.** Kaplan, Appendix D.6:

  > We found that **larger models require a smaller learning rate to prevent
  > divergence**, while smaller models can tolerate a larger learning rate.

  And carries an explicit size-dependent rule used for most runs,
  `LR(N) ≈ 0.003239 − 0.0001395·log(N)` (Eq. D.1), which it notes "breaks down
  for `N > 10¹⁰` parameters". A paper that computes the learning rate *from*
  the parameter count is not claiming the rate matters less as that count
  grows. `insensitive` does not occur in it.

  Two conflations produced the practice. **Schedule for rate**: what Kaplan
  calls "mostly irrelevant" is the decay *shape* given warmup and a final
  decay, measured on a **3M-parameter** model with run-to-run noise at 0.05
  loss. And **direction**: larger models have *less* headroom, not more.

- `SOTA-003` rewritten where it asserted `SOTA-041`'s claim as fact. The
  reason a 2020-era learning-rate range survives is not that the choice
  stopped mattering — it is that nobody re-fit it.

`SOTA-040` and `SOTA-097` are confirmed; `SOTA-097` was already re-sourced
here from Chinchilla in `#113`, and Eq. 1.7 gives its exponent as
`α_C/α_B = 0.050/0.21 = 0.24`.

### Fixed

- `LIT-028`'s key takeaways replaced with the paper's own power laws.
- `record/notes.d/statuses.yaml` gains a note answering luria's inert-status
  check, which now reports **`NOTE: 12/12 at Read`**. The check is right: the
  workflow only produces a note when someone finishes a paper, so `Skimmed`
  and `Unread` are declared and unused, and a predictable field is one the
  citation checks cannot fire on. The fix is to file `Unread` notes for the
  papers nobody has read — a migration and a decision, so proposed rather than
  done.

### Added

- `LIT-224` — **Orca** (Yu et al., OSDI '22), which was missing from the
  record entirely. It introduced **iteration-level scheduling** — invoke the
  engine for a single model iteration rather than a whole request, then
  re-decide the batch — plus **selective batching**, for 36.9× throughput over
  FasterTransformer at equal latency on GPT-3 175B. No arXiv preprint, so it
  is filed under `url:` (`ADR-009`'s third preference).
- `NOTE-023` (vLLM / PagedAttention) and `NOTE-016` (multi-query
  attention).

### Changed

- `SOTA-113` (use continuous batching for inference) **re-sourced** to Orca at
  version 2, with `LIT-112` retained as the production system that carried the
  technique. vLLM describes iteration-level scheduling in its **background**
  section and cites Orca for it; vLLM's contribution is PagedAttention.

  **A fourth distinct failure mode for `#114`**: not an invented claim, not a
  transposed constant, not an inference standing in for a citation — a
  technique filed under a name **its own literature does not use**.
  "Continuous batching" appears in *neither* paper. Orca says *iteration-level
  scheduling*; vLLM inherits that term. Nothing tied the practice to its
  origin.

### Fixed

- `LIT-112`'s key takeaways replaced at version 2, now recording that
  iteration-level scheduling is background there rather than a contribution.
- `LIT-024`'s key takeaways replaced at version 2. **Both practices sourced to
  it are confirmed**, and both remain `Superseded` by GQA — worth recording
  that a superseded practice can still be checked and still be right, which is
  the benign case `ADR-002`'s two-scheme split exists for.

`SOTA-105` (PagedAttention) is confirmed.

### Added

- `NOTE-014` — the reading of `LIT-115` (Monarch Mixer).
- `src/scripts/audit/bump_version.py` — bumps `version:` and **appends** a
  `history:` entry. Doing that by hand went wrong three times in one session,
  always the same way: the naive edit inserts a fresh `history:` block above
  the existing one, producing a duplicate key or descending entries. Fired on
  both code paths (a document with four entries, and one with none) before
  being trusted.

### Changed

- `SOTA-112` (combine Monarch Mixer with standard attention) **`Rejected`** —
  **the fourth inversion in `#114`, and the most direct.** `LIT-115` is an
  **attention-free** architecture: `hybrid` occurs **zero times**, it
  *replaces* attention throughout, and its own reading of the causal result is
  that "radically different architectures than Transformers may be performant
  on causal language modeling". The practice recommends what the source argues
  against.

  The hybrid argument in its body is sound and belongs to the attention/SSM
  line elsewhere in the record, not here. Kept and reattributed rather than
  deleted.
- `SOTA-111` gains the half of its source it was leaving out: M2 is
  sub-quadratic along **model dimension as well as sequence length**, using
  one primitive for both, which is what separates it from the entire
  efficient-attention literature. It had named only the sequence axis.
- `SOTA-111`'s closing paragraph rewritten — it pointed at `SOTA-112` as live
  guidance for "when the condition is met only in part", and there is no
  partial case the source describes.

### Fixed

- `LIT-115`'s key takeaways replaced with the paper's own results and scope.

### Added

- `NOTE-006` — the reading of `LIT-016` (GPipe). **The fourth confirming
  cluster in `#114`**: all three practices sourced to it are supported, and
  all three gain a number where they had an adjective.

### Changed

- `SOTA-017` gains the threshold. Bubble overhead is `O((K−1)/(M + K−1))` for
  `K` partitions over `M` micro-batches, and the paper reports it **negligible
  once `M ≥ 4 × K`** — with the competing constraint, that `M` micro-batches
  means each is `1/M` the size, now stated as why `4K` is a floor rather than
  a target.
- `SOTA-018` gains the expression, and the reason balance is a **precondition
  rather than an optimisation**: the paper's bubble analysis explicitly
  assumes evenly balanced partitions, so with unequal stages the formula no
  longer describes the loss at all. Balancing makes the bubble the only thing
  left to minimise.
- `SOTA-019` gains the trade in closed form: peak activation memory is
  `O(N + (L/K)(N/M))` with re-materialization and partitioning, against
  `O(N × L)` with neither — which turns "choose based on the memory vs.
  compute trade-off" from a description of the problem into something
  solvable.

### Fixed

- `LIT-016`'s key takeaways replaced with the paper's own formulas at version
  2, including the scope condition it opens with: any model expressible as a
  **sequence of layers**.

This is the pattern across every confirming cluster so far. The practices were
right and stated at a level nobody could act on — which is what a note nobody
read against its paper produces even when nothing in it is wrong.

### Added

- `NOTE-008` — the reading of `LIT-014` (Li et al., *Visualizing the Loss
  Landscape of Neural Nets*). **The third confirming cluster in `#114`**: all
  three practices sourced to it are supported.

  Six claims, and the methodological point that makes the paper citable at
  all: sharpness comparisons are meaningless without normalising for the
  rescaling symmetries a network has, because rescaling changes apparent
  curvature without changing the function. Filter normalization is the answer
  to the objection Dinh et al. and Neyshabur et al. had raised.

### Changed

- `SOTA-011` retitled to *Map the Hessian ratio `|λ_min/λ_max|` to find where
  the loss surface is non-convex*, at version 2, and its body re-founded on
  what the source computes.

  The paper's quantity is `|λ_min/λ_max|` — **smallest over largest** — and it
  is interesting because `λ_min` is *negative*, making it a **non-convexity**
  measure. The title had it the other way up, which reads as a **condition
  number**: a real and useful diagnostic that answers a different question
  (*how hard is this to optimise* rather than *is this even locally convex*)
  and that this paper does not compute.

  The conditioning material is kept and signposted as unsourced rather than
  deleted. It is the same failure as `SOTA-107`'s — correct reasoning written
  where a citation belongs — and this is the third instance, so the record
  should expect it.

  It also gains the method that makes it affordable: an **implicitly restarted
  Lanczos** over Hessian-vector products, no explicit Hessian. The record kept
  this practice while retiring `SOTA-021` on the grounds that the eigenvalue
  ratio is at least computable; that judgement now has the method behind it.

### Fixed

- `LIT-014`'s key takeaways replaced with the paper's own results at version 2,
  including the `|λ_min/λ_max|` map, the under-1%-negative-curvature figure for
  ResNet-56, and the convex-to-chaotic transition in its own words.

### Added

- `NOTE-007` — the reading of `LIT-106` (FlashAttention-2). Five claims,
  the diagnosis (FlashAttention reaches only **25–40% of peak FLOPs/s**, and
  the cause is work partitioning between thread blocks and warps, not the
  algorithm), and the three changes that recover ~2× to **50–73% of peak**.

### Changed

- `SOTA-107` (keep sequence lengths a multiple of 128) **`Rejected`**. The
  constant is traced and belongs to a different quantity: `128` occurs
  fifteen times in the paper and **every one is a head dimension or a block
  size**, never a sequence length. `multiple of` and `divisible` occur zero
  times.
- `SOTA-108` (pad attention masks to block boundaries) **`Rejected`**.
  `padding`, `padded`, `pad`, `block boundar` and `divisible` occur **zero
  times** each.

  Both bodies contained correct reasoning about how blocked kernels behave —
  a partial block costs a full block; fully masked blocks can be skipped.
  That reasoning is sound and it is *mine*, not the source's. A new failure
  mode for the `#114` tally: not a takeaway describing another paper, but a
  plausible inference written where a citation belongs.

- `SOTA-089` sharpened: its comparison to `SOTA-107`'s constant now records
  that the comparison was checked and the other constant turned out to be a
  head dimension restated as a sequence length — which is the failure
  `SOTA-089` should be checked for next.

### Fixed

- `SOTA-086` **qualified at version 3, correcting an overstatement from
  version 2.** That version said the tile is "derived, not tuned" from
  `LIT-074`'s `B_c = ⌈M/4d⌉`. The successor kernel `LIT-106` says *"we
  manually tune for each head dimension since there are essentially only 4
  choices"*. Both papers agree on the constraint and disagree on how to
  satisfy it, and the record should not claim the size is derived without
  saying the current kernel picks it by hand.
- `LIT-106`'s key takeaways replaced with the paper's own diagnosis and
  numbers, at version 2.

### Added

- `NOTE-005` — the reading of `LIT-074` (FlashAttention). **The second
  confirming cluster in `#114`**: all four practices sourced to it are
  supported by it.

  Six claims, all three formal results with exact expressions — Theorem 1
  (`O(N²d)` FLOPs, `O(N)` extra memory), Theorem 2 (`Θ(N²d²M⁻¹)` HBM accesses
  against standard attention's `Θ(Nd + N²)`), and Proposition 3, the lower
  bound proving no exact attention algorithm does asymptotically better
  across all SRAM sizes.

### Fixed

- `LIT-074`'s key takeaways replaced at version 2. The originals — "IO-aware
  attention implementation", "memory efficiency improvements" — were correct
  and carried none of the theorems, the bound, or the block-size formula.

### Changed

- `SOTA-086` gains the formula its title only gestured at, at version 2. Step
  1 of Algorithm 1 sets `B_c = ⌈M/4d⌉` and `B_r = min(⌈M/4d⌉, d)`, so the tile
  is **derived** from SRAM size rather than tuned. "Match the SRAM size" is a
  real constraint with a stated relationship, and Theorem 2's bound is what
  respecting it buys.

  `SOTA-085` also gains its actual justification in the note: "use it when
  the hardware supports it" reads like a performance tip, and the reason it
  is unconditional is Proposition 3 — this is IO-optimal for *exact*
  attention, so unlike every approximate method there is no quality question
  to ask.

### Added

- `NOTE-003` — the reading of `LIT-083` (PyTorch FSDP), and **the first
  cluster in `#114` that confirms rather than corrects.** All four practices
  sourced to it are supported by it.

  That result matters as much as the failures. Three clusters read before it
  each inverted their source, and three for three would suggest the remaining
  eighteen notes are all wrong. They are not: the generic bullet shape is a
  signal that a note was never read, not evidence that it is wrong.

  `SOTA-119` gains most from the reading. Its title says "choose sharding
  factor based on model and GPU memory size" and states no rule; the paper
  gives the axis its endpoints — `F=1` is DDP, `F=W` is full sharding,
  between them is hybrid — which is what makes the choice describable.

### Fixed

- `LIT-083`'s key takeaways replaced with the paper's own terms at version 2,
  and a Standing section added. The originals were directionally correct but
  stated at a level that could not distinguish a read note from an unread one
  — which is the whole problem `#114` is about.

### Fixed

- `LIT-117` (Albalak et al., *Efficient Online Data Mixing*) at version 2.
  All four key takeaways replaced. The paper contains the strings `filter`,
  `temperature`, `domain coverage` and `validation performance` **zero times
  each**. Its method is an Exp3 multi-armed bandit over data domains whose
  reward is the **per-domain training loss** on the batch already drawn.

### Changed

- `SOTA-103` retitled to *Adjust data mixing proportions online from
  per-domain training loss* at version 2 — the loop was right and the signal
  was wrong. Avoiding a validation pass is not an optimisation of the method,
  it is the method.
- `SOTA-102` **`Superseded by SOTA-103`**, and its body's central argument
  corrected. It had claimed a temperature and a bandit are different kinds of
  thing; Exp3's policy is a Gibbs distribution whose exploration rate `ℰₜ`
  multiplies the reward inside the exponent, which is what an inverse
  temperature does. It named a real component imprecisely rather than naming
  something absent.
- `SOTA-101` (perplexity-based filtering) and `SOTA-104` (monitor domain
  coverage) `Rejected`. ODM reweights, it does not filter; and under it the
  sampling distribution is *supposed* to leave uniform coverage.
- `SOTA-186` no longer cites `SOTA-101` as a live sibling practice.

### Added

- `NOTE-002` — the reading of `LIT-117`. Five claims, the Exp3 policy in
  full, and the concept the cluster turned on: the exploration rate does two
  jobs, mixing in the uniform distribution *and* acting as an inverse
  temperature, which is the one an earlier reading missed.

### Added

- `NOTE-001` — the reading of `LIT-025` (Xu et al., *Understanding and
  Improving Layer Normalization*), the second paper read in full for `#114`.

  Six claims with strengths, all three theorems with their exact gradient
  identities (`d̄ = 0`, `D_c = D_g/σ²` under attached derivatives), and the
  concept the record was missing a name for: **detaching**, computing `μ` and
  `σ` in the forward pass and treating them as constants in the backward one,
  which is the instrument that makes the paper's central claim testable at
  all.

  Its Connections section records the thing neither note said before: this
  paper and RMSNorm (`LIT-023`) were published the same year, both conclude
  part of LayerNorm is unnecessary, and **they pick different parts**.
  RMSNorm drops the re-centering and keeps the gain; this drops the gain and
  bias and keeps the normalization whole. The field adopted RMSNorm's.

### Added

- **A third scheme, `NOTE`** (`ADR-025`), in `record/notes.d`. One
  document per paper someone has actually read, linked to its `LIT` by a
  required `paper:` reference. Sections: contribution, key insight,
  assumptions, theorem-level results with exact expressions, a claims table
  with strength and support, method, concepts, connections, recommendations,
  bearing on the record, limitations, open questions.

  A `LIT` note says what a paper's **standing** is here. It never said what
  the paper **contains**, and `LIT-052` and `LIT-025` are what that cost —
  eight practices built on takeaways that were not about their papers, both
  passing every mechanical check there is.

- **The status is the depth of the reading**: `Read`, `Skimmed`, `Unread`,
  `Superseded`. `active = "Read"`, so a `Skimmed` note is deliberately not in
  force — a practice sourced to a paper nobody finished is a finding the
  record can now state. This is the field it most needed and did not have:
  a read paper and an unread one were indistinguishable, which is how both
  failures survived.

- `NOTE-004` — the first reading, of `LIT-052` (*Scale Efficiently*),
  the paper that prompted the scheme. Six claims with strengths, the
  DeepNarrow table with its exact figures, and a Bearing section recording
  that five practices citing this paper were retired because it contains
  none of what they claimed.

Three departures from the supplied schema, all in `ADR-025`:
`research_implications`' `Q1`–`Q5` name another project's research agenda and
become **Bearing on the record**, naming `SOTA` codes; `related_in_library`
is not duplicated, because `LIT` already carries `extends:`/`corrects:`/
`compared_against:` with converses the fixer maintains; and the bibliography
is not repeated, because this record has already paid for a fact stored twice.

### Fixed

- `LIT-025` (Xu et al., *Understanding and Improving Layer Normalization*) at
  version 2. All four key takeaways replaced. The paper's findings are that
  LayerNorm's benefit comes from the derivatives of the mean and variance
  rather than forward normalization, and that **the bias and gain increase
  overfitting risk and do not work in most cases** — LayerNorm-simple, with
  both removed, beats LayerNorm on four datasets.

  All three practices sourced to it recommended how to *set* those two
  parameters. The paper argues they should be deleted. It contains the string
  "0.97" zero times and "smaller learning rate" zero times.

### Changed

- `SOTA-025` retitled from "Initialize LayerNorm weight close to 1
  (0.97-1.0)" to "Initialize the LayerNorm gain to 1" at version 2, and
  re-sourced to `LIT-005`, where the gain is defined. The range was invented.
- `SOTA-026` re-sourced to `LIT-005` at version 2; recommendation unchanged.
- `SOTA-027` (smaller learning rate for LayerNorm parameters) `Rejected` at
  version 2. Its body already said "the record cannot support the rate half";
  the paper turns out not to mention learning rates at all.

  Neither `LIT-005` nor `LIT-025` states an initialisation for the gain or
  bias — identity is a framework convention nobody published, and `SOTA-025`
  and `SOTA-026` now say so rather than implying a citation exists.

### Added

- `SOTA-191`: consider removing LayerNorm's learnable gain and bias
  rather than tuning them — what `LIT-025` actually argues. `Proposed` and
  `contested_by: LIT-023`, because RMSNorm keeps the gain and drops the
  centering, which is the opposite half from the one this paper calls
  expendable.

### Fixed

- Five literature notes declared a `first_author:` who is not an author of
  the paper at their `arxiv:` id, each corrected at version 2:
  `LIT-030` (`Noam` → Shazeer, a given name in a surname field), `LIT-086`
  (`Nerfstudio` → Fridovich-Keil, a software project rather than a person),
  `LIT-087` (`Liu` → Xie), `LIT-107` (`Ranftl` → Birkl — Ranftl leads the
  original MiDaS papers, but `arXiv:2307.14460` is MiDaS v3.1) and `LIT-115`
  (`Bhardwaj` → Fu).
- `LIT-115`'s wrong name had been rendered into the prose of `SOTA-110`,
  `SOTA-111` and `SOTA-112`, and `LIT-030`'s into `SOTA-034`. All four
  corrected at version 3; no recommendation changes.

### Added

- `src/scripts/audit/verify_arxiv.py` — checks every note's declared author,
  title and id against the arXiv API, and reports notes sharing an id. Fired
  against three deliberately re-introduced defects before being trusted.

  What it cannot catch is the point of running it: `LIT-052`, whose six
  takeaways belonged to another paper entirely, passes every check here.
  Its id, title, author and year were correct and mutually consistent. A
  clean run is not a clean bill of health, and the script's docstring says so.

### Changed

- Section headings on the last ten practices whose argument ran as loose prose
  under `## Source`: `SOTA-122`, `SOTA-123`, `SOTA-127`, `SOTA-128`,
  `SOTA-139`, `SOTA-142`, `SOTA-182`, `SOTA-183`, `SOTA-184` and `SOTA-185`.
  No claim changed; the arguments were already written and were unfindable by
  anyone scanning for what a practice claims or what conditions it holds
  under.

  With these, all 190 practices have both a body and a heading over it. The
  gap was two distinct defects that one bad detector conflated — a practice
  with nothing under Source but a citation line, and a practice with three
  paragraphs of argument and no way to see them in an outline. The first
  count was the one `#107` tracked; the second was invisible until the first
  reached zero.

### Fixed

- `LIT-052` at version 2. All six key takeaways replaced. They described
  warmup length, layer-norm initialisation, gradient clipping and an early
  instability window; the paper at `arXiv:2109.10686` contains the strings
  "warmup", "gradient clip", "layer norm" and "instabilit" **zero times each**.
  Its actual subject is model shape for downstream fine-tuning, and the
  DeepNarrow strategy. Title, arXiv id, author and year were all correct —
  only the content was another paper's.
- `SOTA-097` at version 2: source corrected from `LIT-068` (Chinchilla) to
  `LIT-028` (Kaplan). Chinchilla derives no batch-size exponent; Kaplan's
  equation 1.7 does, and it is 0.24 = α_C/α_B = 0.050/0.21, which the title
  rounds to C^(1/4).

### Changed

- The five practices built on `LIT-052`'s replaced takeaways are retired.
  `SOTA-064` (warmup sub-linear in size), `SOTA-065` (layer-norm init closer
  to 1), `SOTA-066` (shorter warmup for wider models) and `SOTA-067` (monitor
  the first ~5000 steps) are `Rejected` — nothing in the record supports any
  of them, and `SOTA-065` names an operation that cannot be performed, since
  LayerNorm's gain initialises to exactly 1 at every scale. `SOTA-068` (clip
  during early training) is `Superseded by SOTA-035`: clipping is real and
  correctly sourced there, and the "early training" qualifier read as an
  instruction to turn the guard off.

### Added

- `SOTA-190`: increase depth before any other dimension when scaling a
  transformer — the DeepNarrow strategy, which is what `LIT-052` actually
  says. `Proposed`, and `compared_against: SOTA-125`, which reaches the same
  conclusion at 90M from another group and stops at the same wall: depth wins
  on quality per parameter and loses on throughput.
- A body for `SOTA-096` (`num_tokens ~ 20 * num_params`), which is genuinely
  Chinchilla's and was the only one of that pair correctly attributed.

### Added

- Bodies for `SOTA-007` (BPE), `SOTA-033` (continued pretraining), `SOTA-075`
  (gradient compression) and `SOTA-115` (chunked prefill) — the last four
  practices in the `#107` backlog with nothing under the Source heading.
- Section headings on `SOTA-124`, `SOTA-125`, `SOTA-130`, `SOTA-141` and
  `SOTA-144`. These five had full arguments all along, written as loose prose
  under `## Source`; the argument was there and unfindable. This closes `#107`
  at zero.

### Changed

- `SOTA-130` retagged from `training-optimization` to `adaptation-and-tuning`
  at version 3, and `compared_against: SOTA-129` declared. It is a
  post-training pathway and its two siblings already carried that topic. The
  mis-tag is why the relation had never been declared: the practice chain
  holds `invariant = "primary_topic"`, so a wrong tag keeps an edge silently
  out of the lineage rather than flagging it.
- Two more relations declared from what the new bodies argue:
  `SOTA-115 extends SOTA-113` (chunked prefill is a decision inside the
  scheduler continuous batching introduced) and
  `SOTA-075 compared_against SOTA-155` (volume against frequency, for the same
  slow interconnect).
- `ADR-024` gains the `SOTA-130` case and refreshed counts. An edge that
  would bind once a mis-tag is fixed never appears in the unbound-lineage
  report at all, so the twenty-five it lists are a floor.

### Changed

- All three `LIT-115` practices retitled at version 2. `SOTA-110`, `SOTA-111`
  and `SOTA-112` read "Consider for…", "Use for…", "Combine with…" — none
  named its subject, because all three were bullets under a heading that
  supplied it and were promoted one-to-one without it. Monarch Mixer is now in
  each title.

### Added

- `ADR-024`: the fourth vocabulary decision `ADR-021` predicted, filed as
  four options and no decision. Four topic seams account for eighteen of the
  twenty-five unbound relations.
- Bodies for `SOTA-008`, `SOTA-009`, `SOTA-035`, `SOTA-041`, `SOTA-050`,
  `SOTA-052`, `SOTA-110`, `SOTA-111` and `SOTA-112`.

### Added

- A second relation pass over the practices whose bodies had already landed:
  14 more declarations, `luria link --fix` writing 18 back-references.
  Practices declaring a relation go from **36 of 189 to 98**;
  `docs/practice-lines.md` from **13 lines to 32**.

### Fixed

- The unbound edges the new relations produce are not scattered. Three pairs
  of topics account for eight of them: `systems-optimization` ↔
  `attention-techniques` (a fused attention kernel is both, and which one it
  gets depends on whether its source was a compiler paper or an attention
  paper), `model-stability` ↔ `training-optimization` (a monitoring practice
  splits by whether it is about the model or the run), and
  `distributed-optimization` ↔ `model-architecture`. Repeated failures at the
  same seam are evidence about the vocabulary rather than about the relations
  — `DP-009`'s argument, one level up.

### Added

- 26 relation declarations across the practices whose bodies were already
  arguing them in prose — the ZeRO stages, the FSDP knobs, the mixed-precision
  family, the FlashAttention kernels, the batch-size curve, the fusion
  principle, the quiet-residual-branch instinct, and the GPT-3 frame with the
  findings that build on it. `luria link --fix` wrote 29 back-references.

  `docs/practice-lines.md` goes from **13 lines to 28**. The bodies had been
  cross-referencing in prose, which renders as a link and not as an edge, so
  the chain pages could not move.

### Fixed

- Three new unbound edges follow, all real cross-topic joins the invariant
  exists to surface: `SOTA-032` ↔ `SOTA-100` (pre-norm against the warmup it
  removed the need for), `SOTA-036` ↔ `SOTA-038` (the pretraining frame against
  what the model it produces can do), and `SOTA-051` ↔ `SOTA-060`.

### Fixed

- `LIT-061` was attributed to "Fedus et al." `ARXIV-2112.10684` is Artetxe,
  Bhosale, Goyal, Mihaylov, Ott et al. — Fedus is Switch Transformer's first
  author, a different paper. Its summary also carried a malformed dict from the
  migration, rendering as `{'Analysis of compute/memory trade-offs': None}`.
  Corrected at version 2 with the history recorded.
- `SOTA-040` records that the planning advice taken from `LIT-028` did not
  survive Chinchilla's re-derivation, and that the record holds no source for
  that correction — so read alone the practice still points at the
  pre-Chinchilla allocation.

### Added

- Bodies for `SOTA-040`, `SOTA-051`, `SOTA-053`, `SOTA-061`, `SOTA-062`,
  `SOTA-100`, `SOTA-105` and `SOTA-113`.

### Changed

- `SOTA-036` retitled from *"gpt training recipe"* — which named an artefact
  and recommended nothing — to the four choices it stands for: a decoder-only
  transformer, a broad web corpus, a fixed context, and a single next-token
  objective. Version 2, history recorded.
- `SOTA-012`'s title had a typo in the claim itself ("corerlates"), carried
  since the migration. Corrected at version 2, recorded because a title is what
  citations resolve against.

### Added

- Bodies for the `LIT-014` cluster (`SOTA-010`–`SOTA-012`) and the `LIT-035`
  cluster (`SOTA-036`–`SOTA-038`).

### Fixed

- `SOTA-012` records that `LIT-014` establishes a *correlation* between
  sharpness and test error, not that flattening a minimum causes
  generalisation — and that the filter normalisation is what makes the
  comparison meaningful at all, since rescaling weights changes apparent
  sharpness without changing the function.
- `SOTA-037` records that the "emergence" reading is contested: several
  apparently emergent curves flatten when the metric is continuous rather than
  thresholded. The record holds no source for that critique, which is flagged
  rather than left implicit.

### Added

- `LIT-222`, CoreWeave's training benchmark report, for the quantity the
  record had no source for: a per-GPU failure rate fitted by right-censored
  survival model, and the identity that expected work lost to a failure is
  half the inter-checkpoint interval.
- `SOTA-189`, an alternative to `SOTA-054`: set the checkpoint interval
  from the job's measured time-to-failure, which falls linearly with GPU count
  — so an interval right for 256 GPUs is four times too long for the same work
  at 1,024. Filed `Proposed`, since it rests on one operator's self-published
  figures.
- Bodies for `SOTA-025`–`SOTA-027` (LayerNorm initialisation) and `SOTA-032`
  (pre-norm placement).

### Changed

- `SOTA-001` retitled to *"Use Adam as the default optimizer absent a reason to
  choose otherwise"*, at version 2 with the history recorded. The old title
  never named its subject, so neither `SOTA-121`'s disagreement at scale nor
  `SOTA-120`'s on weight decay could attach to it.
- `SOTA-054` gains the `history:` its restatement should have carried.

### Fixed

- `LIT-015` held one paper's author and takeaways under another paper's title
  and arXiv id. `ARXIV-1806.02375` is Bjorck, Gomes, Selman and Weinberger,
  *Understanding Batch Normalization*, whose claim is that BN's central benefit
  is permitting much larger learning rates. The internal-covariate-shift
  challenge, the landscape smoothing and the Lipschitzness result are Santurkar
  et al., `ARXIV-1805.11604`, now filed separately. Corrected at version 2 with
  the history recorded.
- `SOTA-022` is superseded by `SOTA-004`: the same placement rule, imported
  twice from different notes, with `SOTA-004` carrying the originating source.
- `SOTA-021` retired — no signal, no threshold, no response, and the mechanism
  it invokes belongs to the paper `LIT-015` had been conflated with.

### Added

- The Santurkar note, and bodies for `SOTA-001`–`SOTA-003` (Adam),
  `SOTA-004`–`SOTA-006` (batch normalization) and `SOTA-020`–`SOTA-022`.
- `SOTA-001`'s body records that its title never names its subject, which is
  why the practice cannot be cited or contested — `SOTA-121` argues Muon beats
  the default at scale and `SOTA-120` holds the AdamW half, and neither can
  attach to a title that says "default choice" without saying of what.

### Added

- Bodies for the `LIT-066` cluster (`SOTA-088`–`SOTA-091`, data movement) and
  the `LIT-117` cluster (`SOTA-101`–`SOTA-104`, online data mixing).

### Fixed

- `SOTA-101` records that perplexity measures *learnability*, not quality:
  a high-perplexity document can be noise or it can be rare and valuable, and
  the defensible practice is weighting a domain rather than filtering it.
- `SOTA-102` records that `LIT-117`'s mechanism is a multi-armed bandit, not
  temperature scaling — a temperature reshapes a distribution somebody chose,
  a bandit discovers it.
- `SOTA-103` records that ODM's reward comes from perplexity on the training
  batches, not from validation; a validation-driven loop is the cost the
  method exists to avoid.
- `SOTA-104` records that under ODM the sampling distribution is *supposed* to
  move away from uniform coverage. The real failure mode is a bandit starving
  a domain, and the guard is an exploration floor rather than a dashboard.

### Added

- Bodies for the `LIT-053` cluster (`SOTA-077`–`SOTA-080`, sharded tar storage)
  and the `LIT-063` cluster (`SOTA-081`–`SOTA-084`, TVM).

### Fixed

- `SOTA-078`'s "2-3x batch size" shuffle buffer is not `LIT-053`'s and is
  stated against the wrong quantity: what matters is the buffer against a
  shard's internal correlation, not against batch size.
- `SOTA-080`'s "num_workers = 4 * num_gpus" has no owner the record can find,
  and encodes one workload's CPU/GPU ratio as arithmetic.
- `SOTA-083` records that `LIT-063` argues *against* hand-written kernels —
  the paper exists to replace manual per-target optimisation with a compiler
  and a search. A narrow version survives as a fallback; the general
  recommendation inverts its own source.

### Added

- Bodies for the `LIT-054` cluster (`SOTA-069`–`SOTA-072`, `SOTA-099`, GLM-130B
  stability) and the `LIT-069` cluster (`SOTA-092`–`SOTA-095`, `SOTA-098`,
  PaLM batch size and recovery).

### Fixed

- `SOTA-071` records that its adaptive clipping threshold has no ceiling in
  either the practice or its source, and that an adaptive threshold rises with
  the gradient norms it exists to catch — a silent failure, because the clip
  rate stays where it always was.
- `SOTA-099` states its overlap with `SOTA-070` rather than presenting the two
  as independent findings: they are one paper's stability section split into
  bullets.

### Added

- `LIT-220` (Horovod) and `LIT-219` (PyTorch DistributedDataParallel),
  filed to give two correct practices their actual sources.

### Changed

- `SOTA-047` is sourced to the PyTorch DDP paper, which names overlapping
  communication with computation as one of its three techniques, rather than
  to `LIT-051`, which assumes it.
- `SOTA-048` is sourced to Horovod, whose Tensor Fusion section is where the
  practice comes from — with the buffer size the record had been guessing at:
  **64 MB**, Horovod's documented default.
- `SOTA-054` is restated as what `LIT-059` actually recommends — derive the
  checkpoint interval from online profiling and adapt it at runtime against an
  overhead bound — instead of the heuristic it carried.

### Removed

- Six practices retired as `Rejected`, each with a `status_note:` saying why:
  `SOTA-046` (a crossover constant with no owner), `SOTA-049` (two different
  buffers collapsed into one unfollowable sentence), `SOTA-055` (the practice
  its own source exists to replace), `SOTA-073` and `SOTA-074` (no signal,
  threshold or action), `SOTA-076` (cluster scheduling, not training —
  `ADR-020`).

### Added

- Bodies for the `LIT-016` cluster (`SOTA-017`–`SOTA-019`, GPipe) and the
  `LIT-043` cluster (`SOTA-058`–`SOTA-060`, Megatron-LM).

### Fixed

- `SOTA-060` records that its title merges two different conventions: the
  0.02 standard deviation GPT-2 uses to initialise *all* weights, and the
  depth-scaled initialisation of a block's *output projections* that actually
  controls residual-stream growth. LayerNorm's own parameters are weight 1
  and bias 0, which is `SOTA-025` and `SOTA-026`, not this.

### Fixed

- The seven practices credited to `LIT-051` (BytePS) now record that the paper
  does not support them. Its contribution is a unified all-reduce/parameter-
  server framework and the Summation Service split; the cluster contains
  generic distributed-training folklore instead. `SOTA-047` and `SOTA-048` are
  correct practices with the wrong citation; `SOTA-046`, `SOTA-049`,
  `SOTA-073`, `SOTA-074` and `SOTA-076` need restatement or retirement.

### Added

- Bodies for all seven, saying which of those two positions each is in and
  what would fix it.

### Added

- Bodies for the `LIT-083` cluster (`SOTA-116`–`SOTA-119`, FSDP) and the
  `LIT-106` cluster (`SOTA-106`–`SOTA-108`, FlashAttention-2).

### Fixed

- `SOTA-107` and `SOTA-108` record that the 128-token alignment is a property
  of blocked kernel implementations rather than something `LIT-106` states,
  and that at the sequence lengths language models actually train on the
  practice is worth very little — it bites on variable-length batches and
  short-input inference, not on ordinary training.

### Added

- `LIT-221`: NVIDIA's *Train With Mixed Precision* guide, filed under a
  `url:` because it is not a paper. It is where dynamic loss scaling's
  constants come from — "we successfully trained networks with N = 2000,
  increasing scaling factor by 2, decreasing scaling factor by 0.5" — and the
  record had been crediting them to `LIT-011`, which prescribes no schedule.
- Bodies for the `LIT-074` cluster: `SOTA-085`, `SOTA-086`, `SOTA-087` and
  `SOTA-114`.

### Fixed

- `SOTA-013` now cites both sources and says what each supplies: `LIT-011` the
  mechanism, `LIT-221` the constants. Its body also carries the guide's
  own qualifier — "many other settings are valid as well" — so 2000 stands as
  *tested once and adopted everywhere*, not as a measured optimum.

### Added

- Bodies for the eight practices drawn from `LIT-050` (data stalls) and
  `LIT-059` (CheckFreq): `SOTA-042`–`SOTA-045` and `SOTA-054`–`SOTA-057`.

### Fixed

- Three of those eight now record that their source does not support them.
  `SOTA-055` ("save optimizer state every N epochs, N ~ sqrt(total_epochs)")
  is the practice `LIT-059` exists to replace — that paper's argument is
  against epoch granularity and against hand-tuned intervals, both.
  `SOTA-043` and `SOTA-057` are plausible recommendations their cited paper
  does not make.
- `SOTA-054` records that CheckFreq derives the checkpoint interval from
  online profiling rather than ramping it with training time.

### Added

- Bodies for the eight practices drawn from `LIT-011` (mixed precision) and
  `LIT-027` (ZeRO): `SOTA-013`–`SOTA-016` and `SOTA-028`–`SOTA-031`. Each says
  when the recommendation holds, what it costs, and what it is chosen over —
  the first eight boxes of [#107](https://github.com/dmarx/anthology-of-the-sota/issues/107).

### Fixed

- `SOTA-013`'s body records that "doubles every 2000 successful steps" is the
  Apex/PyTorch AMP scaler's default growth interval, not something `LIT-011`
  prescribes. The mechanism is the paper's; the constants are an
  implementation's.

### Fixed

- `render_svg.yaml` pushes to the ref it ran on and declared no serialization,
  which is the hazard `ADR-019` exists to forbid. It now carries a
  `concurrency:` group per ref, and states its `contents: write` rather than
  pushing on the default token's implicit grant.

### Changed

- `ADR-019` is Active, at version 2. Its audit method changes from "list the
  jobs holding `contents: write`" to "list the jobs that push" — the first
  reads declarations, which is exactly how it missed the workflow above.

### Changed

- `ADR-016` (`contested_by`), `ADR-020` (scoped by kind of claim) and
  `ADR-021` (the ten-topic practice vocabulary) are Active. Each describes
  something the record already does; `Proposed` was claiming an open question
  that had been settled in the configuration and not written back.

### Removed

- Eight `inactive-ok:` acknowledgements that existed only because those two
  decisions were `Proposed`. An acknowledgement of an Active document is
  itself a finding, so they come out in the same edit.

### Fixed

- `CLAUDE.md` said the practice vocabulary has seven topics. `ADR-021` took
  it to ten, and `record/practices.d/tags.yaml` has had ten since.

### Added

- `primary_topic` is a real field on both schemes, derived from the first
  tag. The tag group still guarantees exactly one topic per document; the
  derivation names which one it is, so the topic can be compared, faceted and
  read rather than inferred by intersecting a list against a vocabulary.
  Nothing is stored: 406 documents gain the field and none of them changes.

### Changed

- Both chains assert `invariant = "primary_topic"` instead of
  `invariant = "tags"` — a line of work stays within one topic, rather than
  merely sharing some label. This re-opens one edge, `SOTA-085` / `SOTA-161`,
  which [#101](https://github.com/dmarx/anthology-of-the-sota/issues/101) had bound with a shared secondary tag; it belongs on [#85](https://github.com/dmarx/anthology-of-the-sota/issues/85)'s
  worklist with the twelve in the reading list.

### Added

- Every literature note answers to a readable second name:
  `LIT-Kingma-2014-001` resolves wherever `LIT-001` does. Rendered from the
  note's own `first_author:` and `published:` fields on every read, so it
  cannot drift from the note. All 218 render one; none collide.

### Changed

- Every document in the record carries `number:` in its frontmatter. The
  filename is unchanged and still holds the code; the number is now also a
  field, which is what lets a template read it.
- CI pins `luria==0.13.0`.

### Added

- Both chains declare `invariant = "tags"` (luria 0.12.0). A relation asserts
  that two documents have something in common; the invariant field is what
  says *what*, and `docs/reports/unbound-lineage.md` now names the relations
  and the lines where no topic survives. On the reading list it reports five
  such lines, each a fault line in the twelve-topic vocabulary rather than a
  mis-drawn relation — the RoPE papers split across `model-architecture` and
  `attention-techniques`, Mamba split the same way, GShard filed apart from
  the MoE papers it shards.

### Changed

- `SOTA-085` and `SOTA-161` carry a `flash-attention` secondary tag. Use flash
  attention, and keep its output in FP32 *because* flash attention: an
  `extends:` relation between an attention technique and a stability claim,
  with nothing in either document naming what they share. The check above
  found it; the tag is the answer it was asking for.

### Changed

- The latent-diffusion practice moved to `representation-and-encoding`. A
  learned latent autoencoder and a tokenizer are the same move — fit a cheap
  encoder, train the expensive model on what comes out — and the topic's
  description now says so.

### Added

- Three topics a practice can carry: inference-optimization,
  adaptation-and-tuning and representation-and-encoding. All three words are
  the reading list's, which has had two of them since [ADR-003](record/decisions.d/ADR-003.md).
- A design principle: where a claim has no category to take, that is a finding
  about the vocabulary rather than a verdict on the claim.

### Changed

- Twenty-one practices retagged. Serving was scattered across four topics,
  adaptation across four more, and positional encoding across three.

### Added

- Three practices from work the record could not previously recommend:
  preconditioning a noise-conditioned network so its target has unit variance
  at every level, bootstrapping an annotation set with the model being
  trained, and training a generative model in a learned compressed latent.

### Changed

- Nine notes in the vision and radiance-field corpus now say what they carry,
  rather than sitting bare because the old scope made them unreadable. Eight
  carry no practice and say why; one sources the annotation-loop practice.

### Fixed

- The literature index still told the reader that the generative and vision
  corpus is declined by construction — the scope [ADR-020](record/decisions.d/ADR-020.md) replaces. Two
  contributions landed within a minute of each other and `main` carried both
  claims at once for the interval between them.

### Changed

- The recommendations are no longer scoped to language-model training. A
  practice belongs in the record if it is an instruction one of the seven
  topics can express; where the work was discovered is not the test. Vision,
  generative and inference work all qualify, and the bias toward language
  models is now a bias rather than a boundary.
- [DP-008](docs/design-principles.md#dp-8)'s worked example described the old scope as a fact. Amended to
  describe it as a decision that was replaced, and why it was wrong in both
  directions at once — two `Active` serving practices were already outside it,
  and it declined work whose transferable content is exactly what the seven
  topics collect.

### Added

- A practice for error-compensating post-training quantization, from GPTQ —
  another note that had sat in the corpus for a year sourcing nothing.

### Fixed

- [LIT-039](record/literature.d/LIT-039.md) was attributed to Frankle. The Semantic Scholar record for
  2010.03533 lists Evci first of four. It is a lottery-ticket paper and
  Frankle wrote *the* lottery-ticket paper, which appears to be how the
  migration guessed.

### Changed

- Three notes that will never carry a practice now say why, instead of
  looking like an oversight: P-Tuning v2 (the record recommends low-rank
  adaptation for the same job), the lottery-ticket hypothesis (the procedure
  costs a full dense run before it yields anything), and its companion
  analysis.

### Added

- Two practices the record had been missing for a year, both from notes that
  were sitting in the corpus unfiled: low-rank adaptation, and generating
  harmlessness preference labels from a written set of principles.

### Fixed

- [LIT-082](record/literature.d/LIT-082.md) was attributed to the wrong first author. The arXiv record for
  2212.08073 lists Bai first, of fifty-one; Askell is among them.

### Documentation

- The literature index now separates the two reasons a note sources no
  practice. For the generative and vision corpus it is a decision [ADR-003](record/decisions.d/ADR-003.md) made
  and [DP-008](docs/design-principles.md#dp-8) states — the recommendations are scoped to language-model
  training by construction. For `adaptation-and-tuning` and
  `inference-optimization` it is not: [ADR-003](record/decisions.d/ADR-003.md) justified all five extra topics
  with one sentence, and that sentence is only true of three of them.

### Fixed

- Three literature notes in the inherited corpus were duplicates — two pairs
  that had never been noticed. [LIT-006](record/literature.d/LIT-006.md) and [LIT-029](record/literature.d/LIT-029.md) are retired against the
  copies that carry the reading ([LIT-042](record/literature.d/LIT-042.md) and [LIT-114](record/literature.d/LIT-114.md)). The [LIT-006](record/literature.d/LIT-006.md) pair had
  the record calling one paper `Active` and `Superseded` at the same time.

### Changed

- [SOTA-032](record/practices.d/SOTA-032.md) was two recommendations in one document — where the normalization
  sits, and what statistic it computes — sourced to a single paper that
  argues only the first. It is now the placement claim, sourced to Xiong et
  al.; the statistic is its own practice, sourced to Zhang and Sennrich, whose
  paper the record already held.

### Removed

- The legacy Python tooling and the workflows that ran it: the local README
  generator and its Jinja templates under `docs/readme/` and
  `docs/readme_llm/`, the directory summariser, the package-lock helper, the
  test suite that covered them, and the `llamero` dependency all three shared
  (issue [#41](https://github.com/dmarx/anthology-of-the-sota/issues/41)). What is left under `src/` is the frozen migration that produced
  `record/` from the YAML in `data/`, kept re-runnable by [ADR-008](record/decisions.d/ADR-008.md).

### Changed

- `README.md` and `README_LLM.md` are ordinary files now, written and edited
  in place rather than assembled from templates at build time.

### Added

- **`ADR-019`, `Proposed`: an automation that writes to shared state
  names its serialization, and a pacing failure is swept as a class.**

  Two CI failures in one evening, neither about the content being written.
  Views regenerated on branches, so two branches with disjoint sources
  conflicted on nineteen shared pages. Then four merges in forty seconds,
  where three push runs rebased their own regeneration commit onto the
  winner's and conflicted on the files both had just rewritten — losing a
  concretization that had already run correctly.

  Both are the same thing: **an assumption about pacing, never written down,
  true only because a person was doing the work.** Merging one pull request
  and reading the result before the next is a serialization supplied by the
  operator, invisible in the configuration, and removed the moment the
  operator is not a person.

  The decision has three parts: a job that writes where others write declares
  a `concurrency:` group or says why it needs none; the first pacing failure
  is answered by an audit of every writer rather than a patch to the one that
  broke; and the shared locations are inventoried explicitly, because the
  audit is only as good as the list of places two writers can meet.

  The case for the second part is that it already failed twice. `ADR-018`
  fixed the branch-level conflict and left the run-level one in the same
  file; `ADR-002` had reasoned the hazard out correctly for a *third* job in
  that file two months earlier and never generalised it.

### Fixed

- `generate_summaries.yaml` gains a concurrency group. The audit the ADR
  proposes found it in one command: `contents: write`, a tool whose default
  is to commit and push, and no serialization. It is dispatch-only so nothing
  has raced it — which is the observation the decision exists to distrust.

### Added

Last cluster of the [#73](https://github.com/dmarx/anthology-of-the-sota/issues/73) sweep.

- **Keep the routed experts' weights in a down-projected latent space**,
  `Active`, `emerging`, `extends` `SOTA-150`, from `LIT-196`. Judge a sparse
  design on accuracy per *parameter* as well as per FLOP, because at
  latency-critical batch sizes expert computation is bandwidth-bound and
  adding FLOPs there is free while moving weights is not. This is what makes
  896 routed experts with 16 active affordable at 2.8T.
- **Shard the sequence across devices in a ring**, `Active`, `emerging`, from
  `LIT-206`. Exact attention, no approximation, sequences scaling with device
  count. Filed mostly to separate it from the record's three other answers to
  long context, which operate at different layers and cost different things.
- **Truncate the rotary encoding's low frequencies**, `Proposed`,
  `unreplicated`, from `LIT-210`. RoPE's high frequencies build positional
  heads; its low frequencies carry semantics that provably cannot stay robust
  over long context. p=1 is RoPE and p=0 is NoPE, so this is the dial between
  two practices the record already holds — and it explains the base-rescaling
  trick everyone copies as a blunt version of the same move.

### Changed

- Six notes state why they keep no practice: `LIT-135`, `LIT-136`, `LIT-182`
  and `LIT-183` on `ADR-017` (a model report is adoption, not evidence);
  `LIT-154` on altitude (a stability *bundle* nobody has taken apart, despite
  released checkpoints that would allow it); `LIT-199` as the origin of a
  unit `SOTA-034` already recommends a variant of.

### The sweep closes

Every post-migration note carrying a practice-eligible topic now either
sources a practice or says, in its own Standing section, why it does not.
Twenty-eight practices were added across six clusters. The record went from
157 practices to **181**, and from three design principles to eight.

### Added

Fifth cluster of the [#73](https://github.com/dmarx/anthology-of-the-sota/issues/73) sweep: the state-space and linear-attention notes.
Eight candidates, three practices — the lowest yield of any cluster, and the
right one.

- **Hybridise inside the layer**, `Proposed`, from `LIT-176`. Long-term
  key-value slots updated by a linear RNN, short-term context from a sliding
  window, and a *single* softmax over both, so the weighting is per-token and
  content-dependent with no fusion parameters. Every layer stays identical
  and the window size slides from purely linear to full attention.
- **Decouple the erase address from the write address**, `Proposed`,
  `extends` `SOTA-135`, from `LIT-177`. The delta rule corrects what sits at
  the *write* address, so stale content elsewhere can only decay passively.
  Best at 2.5B dense and 25B-A2.8B MoE, and the gain survives 80B tokens of
  long-context midtraining.
- **Vector-valued gating with in-context learning rates**, `Proposed`, from
  `LIT-173`. A 2.9B model at the 3B state of the art on far fewer tokens —
  and an expressivity claim that cuts against the record's own hybrid
  reasoning: the recurrence can recognise all regular languages, which under
  standard conjectures a softmax stack cannot.

### Changed

- **`SOTA-132`'s `Sequence` now starts where the interleave actually starts.**
  Griffin (`LIT-204`, 2024) is two steps earlier than the practice's sources,
  and the delta-rule work says so outright. The fork is stated with it:
  Griffin puts *local* attention in the minority layers and this practice
  puts *global* attention there, which is the difference between preserving
  exact retrieval at arbitrary distance and not.
- `SOTA-132`'s note on the intra-layer layout points at the filed practice
  rather than saying no practice moves.
- `SOTA-135`'s `Sequence` distinguishes its descendant from its parallel:
  the decoupled erase extends it, RWKV-7 does not — that line reached
  per-channel gating from the recurrent-network tradition independently, and
  treating it as a step here would make two data points look like one.
- `LIT-161`, `LIT-162`, `LIT-194` and `LIT-204` say why they keep no
  practice, and the four reasons differ: a superseded recommendation, a
  premise rather than an instruction, parallel invention, and a fork the
  record took the other side of.
- A redundant acknowledgement removed from `SOTA-171`, where a file-scope
  directive already covered the citation. The lint reported it as no longer
  applying — which is the guard catching a vouch that was never needed rather
  than one that expired.

### Fixed

- **`docs.yml` serializes its runs per ref.** Four pull requests merged
  within forty seconds started four `main` push runs, each regenerating the
  same views and pushing them to the same branch. The three that lost the
  race pulled, rebased their own regeneration commit onto the winner's, and
  conflicted on the files both had just rewritten — so three runs failed, and
  the concretization one of them had already performed was lost with it,
  leaving five temporary codes on `main` that the trunk guard exists to
  forbid.

  `concurrency:` with `cancel-in-progress: false` queues them instead. The
  last run in a burst regenerates from the final source state and concretizes
  everything outstanding, which is the only outcome that has to be correct.

  The proximate cause was a merge cadence, not a workflow bug — but a
  workflow that only works when merges are spaced out is one that will fail
  again, and `ADR-002` already made this argument for the changelog
  collector: a per-merge bot commit races in-flight rebases. This is the same
  hazard reaching `docs-generate`.

### Added

- **A pass finds only the defects its query is shaped like — a clean run is
  evidence about the query, not about the record.** From `ADR-015` and
  `ADR-017`. The method principle held back from the scope four, filed
  separately because it is about how this record is audited rather than about
  what belongs in it.

  Three ways it goes wrong, all observed in one week. **Direction:** a query
  over a relation picks one end, so a pass whose candidates were "codes cited
  in the body that `source:` does not name" could only ever *add* sources and
  never remove one. **Recency:** a pass keyed to what changed cannot see a
  document whose *surroundings* changed — which is how `SOTA-124` kept
  "nobody has contradicted it either" while its own body argued with two
  papers that do. **Evidence of absence:** a refusal leaves a sentence to
  grep for, an omission leaves nothing at all.

  The corollary is cheap and is the point: after a pass over a relation, run
  it once in the other direction.

### Added

Four design principles, all about **what belongs in the record and why** —
the question this week's work kept answering ad hoc. Each is drawn from a
mistake that was made and corrected, and cites the decisions that produced
it.

- **Filing is not endorsement — the bar for having a document is lower than
  the bar for believing it.** From `ADR-014` and `ADR-015`. A refusal
  withholds the endorsement correctly and loses three other things: the
  condition that would reverse it, the node a consensus reading attaches to,
  and the provisional statuses themselves, which decay into nothing if only
  finished claims are filed.
- **What everyone agrees on has no author, so nothing prompts anyone to write
  it down.** From `ADR-011` and `ADR-017`. The filing habit runs on arrivals,
  and agreement has none — which is why the record held two rival constraints
  on a mechanism whose trunk had no entry, and a footnote about a training
  sample four months before the practice of constructing one.
- **Adoption is not evidence — who does a thing and whether it works are
  different questions.** From `ADR-010`, `ADR-015`, `ADR-017`. Both facts
  bear on a recommendation, which is why recording both is right and
  recording them in one field is not.
- **A vocabulary is a scope decision — a subject with no category is one you
  declined to hold.** From `ADR-002` and `ADR-003`. `tags.yaml` gives the
  recommendations seven topics and none is a vision category, so the
  practice scheme is scoped to language-model training *by construction* —
  a fact nobody had written down, and a better reason to decline a vision
  paper than any judgement about its evidence.

### Added

Fourth cluster of the [#73](https://github.com/dmarx/anthology-of-the-sota/issues/73) sweep: corpora and synthetic data.

- **Choose filtering aggressiveness by the token horizon: at long horizons
  rephrase what a filter would discard.** `Active`, `unreplicated`, from
  `LIT-178`. Aggressive model-based filtering removes 90% of the data and
  wins at 1T tokens; at 15T it loses, because what it optimises is mean
  quality and mean quality stops binding once the corpus does. The full
  6.3T-token dataset matches DCLM on MMLU while holding four times more
  unique real tokens.
- **Build synthetic pretraining data by editing human text at the token
  level, not by generating from scratch.** `Proposed`, `unreplicated`, from
  `LIT-205`. Pretraining across proportions of synthetic data shows a
  *negative* correlation with performance — distributional shift and
  over-concentration of n-gram features — and the remedy inverts the usual
  move: anchor to a real distribution and the test error is provably bounded.

### Changed

- `LIT-184` (FineWeb) and `LIT-125` (Qwen2.5-Coder) now state why they keep
  no practice. FineWeb on **scope**: a dataset is not a technique, and its
  transferable content is an ablation methodology. Qwen2.5-Coder on
  **`ADR-017`**: a model report describes a recipe in full and isolates none
  of it, so it supplies adoption rather than evidence about a claim.

### Added

Third cluster of the [#73](https://github.com/dmarx/anthology-of-the-sota/issues/73) sweep: repetition and fill-in-the-middle.

- **Train autoregressive models with fill-in-the-middle by default.**
  `Active`, `converged`, `extended_by` `SOTA-128`, from `LIT-124`. The
  FIM-for-free result: transforming a large fraction of the training data
  harms neither left-to-right perplexity nor sampling quality, so infilling
  is an added capability rather than a trade.
- **Mask whole syntactic units for code FIM, not random character spans.**
  `Proposed`, `unreplicated`, from `LIT-126`. Up to 5 points over
  random-character FIM at 1B and 8B, on a benchmark built from 30,000 real
  GitHub commits rather than synthetic holes.
- **Repeat a data-constrained corpus for up to about four epochs.**
  `Active`, `contested`, `contested_by` `LIT-119` and `LIT-175`, from
  `LIT-166`. 400 runs up to 900B tokens and 9B parameters. Both halves are
  the practice: repetition is close to free up to four epochs, and past that
  the value of adding compute decays toward zero.
- **Augment the objective to make multi-epoch pretraining productive.**
  `Proposed`, `unreplicated`, from `LIT-175`. Standard AR pretraining
  overfits *severely* on a fixed corpus; three orthogonal augmentation
  families each delay it.

### Changed

- **`SOTA-124` moves from `unreplicated` to `contested`**, with
  `contested_by` naming `LIT-166` and `LIT-175`. Its note said "nobody has
  contradicted it either" while its own body had been arguing with both
  papers for a month — the field moved and the axis did not. Version 3; the
  recommendation is unchanged.
- `SOTA-128` gains `extends:` the FIM practice as the fixer-written converse.
  The record had carried the *footnote* — whether to mask the loss on the
  prefix and suffix — since before it carried the practice being footnoted.

### Changed

- **Generated views are committed on `main` only; a pull request writes
  none** (`ADR-018`, adopting luria's `LU-ADR-068`). `docs.yml` splits
  by event: `docs-generate` + `docs-lint` on push, and a new `docs-check` on
  pull requests that runs the generate action with `views: "false"` and the
  lint action in the same job.

  A view is a file *every* branch rewrites, so two branches always collide on
  it — batch A and batch B of [#56](https://github.com/dmarx/anthology-of-the-sota/issues/56) touched disjoint sources and conflicted
  on nineteen generated pages, then conflicted again after each merge. A
  source repair is the opposite: it touches only what the branch authored, so
  it stays on the branch where the review reads it.

- `CLAUDE.md`'s Working section says to run `luria index` locally and then
  discard what it wrote — the reports are how you read what the lint is about
  to flag, and the views are not the branch's to carry. It also now says to
  write `inactive-ok:` acknowledgements *from the lint's report, after
  running it*, which is the mistake that cost six lint cycles across three
  branches today.

### Added

Second cluster of the [#73](https://github.com/dmarx/anthology-of-the-sota/issues/73) sweep: the precision and stability notes no
practice sourced. All four papers were already load-bearing — three of them
are what the record's frontier reports cite for decisions the record records
without explaining.

- **Keep the attention output in FP32 during training.** `Active`,
  `unreplicated`, `extends` `SOTA-085`, from `LIT-198`. Flash attention in
  BF16 alongside an FP8 FFN sometimes explodes, and the cause is two things
  at once: attention's low-rank updates repeat across steps and tokens, and
  low-precision addition rounds with a *bias*, so the error rides the
  repeated update instead of averaging out. Kimi K3 ships the FP32 output at
  2.8T for exactly this reason.
- **Quantize with block-scaled microscaling formats rather than one scale per
  tensor.** `Active`, `emerging`, from `LIT-197`. 32-element blocks, an E8M0
  shared scale so applying it is an exponent adjustment. Carries the regime
  table, including that 6-bit MX trains to FP32 accuracy *with no recipe
  change* — which the paper states as a result, not an aside. This is what
  "FP4" and "MXFP4" mean in the DeepSeek-V4 and Kimi K3 notes.
- **Treat the pretraining token budget and the post-training quantization
  plan as one decision.** `Proposed`, `unreplicated`, from `LIT-186`.
  Quantization damage *increases* with how much data the model was trained
  on, so past a point more pretraining data is actively harmful if the model
  will be quantized. `Proposed` because the fits stop at 1.7B and 26B tokens.
- **Bound the activation's output range when training in low precision.**
  `Proposed`, `emerging`, `compared_against` `SOTA-034`, from `LIT-200`.
  Another trunk: two groups independently concluded SwiGLU's unbounded range
  is a numerical liability at frontier scale, and chose *different* remedies
  that nobody has compared. The agreement is the practice; PowLU and SiTU-GLU
  are not.

### Changed

- `LIT-186`, `LIT-197`, `LIT-198` and `LIT-200` now say where their
  recommendation went.
- `SOTA-085` gains `extended_by:` as the fixer-written converse. Its
  recommendation is unchanged — and it is one of the bodyless migration stubs
  `ADR-012` is about, which is why the precision configuration that fails was
  never something it ruled out.

### Added

First cluster of the [#73](https://github.com/dmarx/anthology-of-the-sota/issues/73) sweep: the optimizer notes no practice sourced.

- **Precondition the gradient with matrices rather than entrywise scaling.**
  `Active`, `emerging`, `extended_by` `SOTA-121`. The trunk of the optimizer
  material, sourced to the fair comparison (`LIT-156`), the equivalence that
  makes the class a real object (`LIT-157`), and the distribution result that
  makes the overhead affordable (`LIT-158`). Two notes had been arguing in
  prose that the win belongs to the *class* rather than the algorithm; this
  is that argument as a document.
- **Combine µP with unit scaling so the hyperparameters decouple and FP8
  needs no loss scaling.** `Proposed`, `unreplicated`, `extends` `SOTA-143`,
  from `LIT-149`. Filed because `SOTA-144` — the other one-group extension of
  the same parent, on the same evidence profile — was already filed and this
  was not.
- **Run Adam in Shampoo's eigenbasis (SOAP) instead of Shampoo itself.**
  `Proposed`, `unreplicated`, `compared_against` `SOTA-121`, from `LIT-157`
  and `LIT-156`.

### Changed

- `LIT-149`, `LIT-157` and `LIT-158` now say where their recommendation went.
  `LIT-158` keeps no practice of its own and says why in terms of altitude
  rather than adoption: its transferable content — that sharding a
  preconditioner's blocks holds the per-step penalty to 10% — is a *condition*
  on a recommendation, and is stated in the trunk practice where a reader
  choosing an optimizer would look for it.
- `SOTA-121` gains `extends:` the trunk as the fixer-written converse. The
  recommendation is unchanged.

### Added

Five practices the record already held the evidence for. Three were refused
in writing for lack of frontier adoption — the `Active` bar applied to
whether the document should exist — and two were never considered at all.

- **Widen the residual stream into several streams and constrain the mixing
  between them.** `Proposed`, `emerging`. The trunk of the
  hyper-connections line, `extended_by` `SOTA-136` (doubly-stochastic) and
  `SOTA-137` (free mixing). `ADR-015` declined to file it on the grounds
  that "converting a hedge into an assertion is an editorial act" — but
  `Proposed` is the hedge. Both branches were filed and the trunk was not,
  so the disputed part of the design had a node and the agreed part did not.
- **Set the pretraining data proportions by fitting a mixing law on small
  runs, not by argument.** `Proposed`, `unreplicated`, from `LIT-201`. The
  same move `SOTA-142` makes for the peak learning rate.
- **Build linear-attention layers from the state-space view.** `Proposed`,
  `unreplicated`, from `LIT-165` — expressive discretisation, complex-valued
  state, MIMO readout; +1.8 at 1.5B over Gated DeltaNet, which is the module
  `SOTA-132` assumes.
- **Deduplicate the pretraining corpus at both substring and document
  granularity.** `Active`, `universal`, from `LIT-202`. Never refused, never
  considered: every pipeline in the record does it and none argues for it.
  Three separate wins usually conflated into one — tenfold less verbatim
  emission, fewer steps to equal accuracy, and evaluation that is not
  contaminated.
- **Train with auxiliary multi-token-prediction heads.** `Active`,
  `emerging`, from `LIT-163`. Five model reports ship an MTP head and each
  names it as settled; none ablates it, so the adoption is wide and the
  measurement is one paper's. Filed with the double motive stated, because
  the training claim and the speculative-decoding claim have never been
  separated at frontier scale.

### Changed

- `SOTA-136` and `SOTA-137` gain `extends:` the new trunk practice, written
  by the fixer as the converse of its `extended_by:`. Neither
  recommendation changes.

### Added

- Four literature notes and one `Proposed` practice, closing the [#56](https://github.com/dmarx/anthology-of-the-sota/issues/56)
  backlog. Three of the notes carry no practice, and each says why.
  - **Video models are zero-shot learners and reasoners** (`2509.20328`) —
    Veo 3 solving segmentation, edge detection, affordance recognition, tool
    use and early visual reasoning it was never trained on, offered as
    evidence that video is on the trajectory language took. A capability
    report on a closed model; no training recommendation in it.
  - **I-JEPA** (`2301.08243`) — predict the *representations* of masked
    blocks, not the pixels and not an augmentation invariance. Filed for its
    successor's sake: a line whose origin is missing cannot be checked.
  - **V-JEPA 2** (`2506.09985`) — `extends:` I-JEPA. The same objective on
    over 1M hours of video, then an action-conditioned world model from under
    62 hours of unlabelled robot video, planning zero-shot on Franka arms in
    labs that contributed no data.
  - **LLaDA** (`2502.09992`) — an 8B language model trained under the
    ordinary pretrain-then-SFT paradigm with the autoregressive factorization
    replaced by masked diffusion. Competitive with LLaMA3 8B on in-context
    learning, and past GPT-4o on reversal poem completion.
- A practice from LLaDA: **train the language model as a masked diffusion
  model rather than autoregressively**, `Proposed`, `consensus: unreplicated`.
  It promotes on a released model above 8B trained this way, or a
  matched-compute comparison with both arms swept, from a second group.
- What filing it exposed, recorded in the practice rather than only in the
  devlog: every practice in this registry is advice about training an
  autoregressive transformer and none of them says so. Some carry over
  untouched (AdamW, µP, WSD, MoE routing, packing) and some are load-bearing
  on the factorization (FIM, multi-token prediction, speculative decoding,
  KV-cache compression, RoPE rescaling). It sits under the new practice's
  "what adopting this would cost" heading, because a recommendation whose
  adoption cost is unknown should say so where it recommends.
- The two notes that stay literature-only now say why in terms that hold:
  the Veo 3 note contains no instruction to file, and the JEPA line has no
  primary topic to take — `tags.yaml` gives `SOTA` seven categories and none
  is a vision one, so the practice scheme is scoped to language-model
  training by construction.

### Added

- Four literature notes and three `Proposed` practices, from the [#56](https://github.com/dmarx/anthology-of-the-sota/issues/56)
  backlog.
  - **The Road Less Scheduled** (`2405.15682`) — a third answer to the
    schedule question: do not schedule. Scheduling and iterate averaging are
    the same mechanism, and the averaged form needs no stopping time T. Won
    the MLCommons 2024 AlgoPerf Self-Tuning track.
  - **DiLoCo** (`2311.08105`) — many inner AdamW steps per worker, Nesterov
    momentum as the outer optimizer, synchronised rarely; 500× less
    communication at matched quality on C4 with 8 workers. It fills a hole:
    the record's distributed material is all pre-migration and all assumes
    one tightly coupled cluster.
  - **Streaming DiLoCo** (`2501.18512`) — `corrects:` its parent. DiLoCo made
    synchronisation rare and left its size alone, so peak bandwidth was
    unchanged; streaming, overlapping and quantisation drop it two orders of
    magnitude at billion scale.
  - **Evolution Strategies at Scale** (`2509.24372`) — full-parameter-space
    ES on billion-scale LLMs, which the field had assumed impossible.
    `compared_against` `LIT-127`: +36.4% over base against GRPO's +21.3% and
    PPO's +17.9%, with ES on one fixed hyperparameter set and RL tuned per
    experiment.
- Three practices at `Proposed`, one per recommendation the above contain:
  train without a schedule; train across poorly connected islands; fine-tune
  with evolution strategies instead of policy-gradient RL. Each carries a
  `promote_when:` naming the kind of result that would move it, and
  `consensus: unreplicated`. None is `Active` — no frontier report in this
  record trains under any of them.

### Changed

- `SOTA-140`'s Sequence names the schedule-free practice as the third answer
  to the question the chain is about. The recommendation is unchanged, and
  the two are deliberately *not* `compared_against` each other: nobody has
  run that comparison.
- `SOTA-145` gains a `compared_against:` to the evolution-strategies
  practice — a rival somebody measured, rather than one asserted — and a
  third limit in "What this does not say": the practice does not say
  policy-gradient RL is the right *family*. The recommendation is unchanged.

### Changed

- The consensus values, re-read against the source lists [#58](https://github.com/dmarx/anthology-of-the-sota/issues/58) corrected.
  Twenty-two practices carry one; four move.
  - `SOTA-141` goes from `emerging` to `unreplicated`. Its own note ended
    "the field has not moved", which is the opposite of what `emerging`
    means. The value was set before `LIT-145` entered the source list and was
    never re-read after.
  - `SOTA-125`'s note said "at one scale" while its sources span 90M and
    1.5B. Corrected; the value holds, because two scales from one group is
    still one group.
  - `SOTA-147`, `SOTA-150` and `SOTA-153` had adopters **in** `source:`.
    `SOTA-147` is the clearest: its own Evidence section calls the four
    DeepSeek and Kimi generations "four generations of adoption rather than
    one result", and all four were listed as support. Only `LIT-174`, which
    ran MLA against the same team's dense 67B, remains. Nothing is lost —
    every removed code was already named in the practice's `consensus_note`.
- `SOTA-122` re-checked and correct: its "one team" reading is confirmed by
  `LIT-121`'s own Standing section, which calls `LIT-119` the authors' own
  first application at a released model's scale.
- No status and no recommendation changed.

### Changed

- The last of [#58](https://github.com/dmarx/anthology-of-the-sota/issues/58). Ten practices examined, three changed, seven correct as
  they stand.
  - `SOTA-121` names `LIT-153`, which argues Muon's shrinking advantage is an
    artefact of how the comparison held weight decay and recovers 20–30% by
    pinning the norms — a result about the size of this practice's own claim,
    from outside the group making it.
  - `SOTA-145` names `LIT-167`. Its body enumerates four works that run or
    rework GRPO and observes that all four keep the group baseline; three
    were in the field and the fourth was not, so the count the practice
    argues from could not be checked against it.
  - `SOTA-148` names `LIT-131`, which is not an adopter here: it reports the
    expert count at which the fixed-step bias update stops being effective,
    which is a measurement of where the claim stops holding.
- `SOTA-034`, `SOTA-063`, `SOTA-109`, `SOTA-149`, `SOTA-150`, `SOTA-151` and
  `SOTA-152` examined and correct. `SOTA-151` is the one to read: it already
  says, in its own body, that `LIT-210` explains why the problem exists and
  "does not evidence that rescaling is the answer, and the sources of a
  practice are what its recommendation rests on" — [ADR-017](record/decisions.d/ADR-017.md)'s rule, written
  before [ADR-017](record/decisions.d/ADR-017.md). `SOTA-152` says the other half: two reports "both cite this
  work, which is adoption rather than replication".

Closes [#58](https://github.com/dmarx/anthology-of-the-sota/issues/58). Thirty-two practices examined, seventeen changed, fifteen
confirmed correct.

### Changed

- The architecture cluster's sources, third batch of [#58](https://github.com/dmarx/anthology-of-the-sota/issues/58) and the first run
  under [ADR-017](record/decisions.d/ADR-017.md) rather than under a rule invented mid-pass. Nine practices
  examined, five changed.
  - `SOTA-132` is the one [#58](https://github.com/dmarx/anthology-of-the-sota/issues/58) flagged. Four adopters come **out** of
    `source:` — `LIT-131`, `LIT-135`, `LIT-136`, `LIT-183` ship the 3:1 ratio
    without reporting the alternative — and `LIT-195` goes in, the second
    independent comparison the body already said existed. What remains is
    three works that ran the experiment. The adopters move to a
    `consensus_note` the practice did not have: it read as unassessed while
    its source list carried four production lines, which is exactly the
    countability [ADR-010](record/decisions.d/ADR-010.md) wanted. `consensus: emerging`.
  - `SOTA-131` names `LIT-155`, the mechanism it argues from, and `LIT-119`,
    whose small-scale runs without clipping are the evidence for the "at
    scale" in its own title.
  - `SOTA-134` names `LIT-191` and `LIT-190` — what the gate is claimed to
    remove, which the record could not describe when the practice was filed.
  - `SOTA-138` names `LIT-143`, whose from-scratch result the Conditions
    section already counted as evidence.
  - `SOTA-136` names `LIT-152`, the independent evaluation its own
    `promote_when` says arrived.
- `SOTA-133`, `SOTA-135`, `SOTA-137` and `SOTA-139` examined and correct as
  they stand — every body-only code in them is an adopter, an alternative, or
  a successor with a practice of its own.
- No recommendation changed; `history:` entries per [ADR-019](record/decisions.d/ADR-019.md).

### Added

- `corrects:` / `corrected_by:` on both schemes, and both chains walk a signed
  spine — `relation = ["extends", "corrects"]`. [ADR-017](record/decisions.d/ADR-017.md)'s second half becomes
  the record's shape rather than a decision about it. `extends:` says a work
  builds on its parent; `corrects:` says it exists because the parent is
  broken, and the test is the child's own text: does it name a defect in the
  parent as its motivation?

### Changed

- Eleven edges move onto `corrects:`. Literature: `LIT-140`→`LIT-141`,
  `LIT-151`→`LIT-140`, `LIT-181`→`LIT-140`, `LIT-192`→`LIT-045`,
  `LIT-193`→`LIT-192`, `LIT-200`→`LIT-030`, `LIT-210`→`LIT-045`. Practice:
  `SOTA-131`→`SOTA-121`, `SOTA-136`→`SOTA-137`, `SOTA-146`→`SOTA-145`,
  `SOTA-151`→`SOTA-063`. Every one names the defect it corrects at the
  declaration.
- The trunk documents can now read their own corrections. `LIT-140` carries
  `corrected_by: [LIT-151, LIT-181]` and `SOTA-121` carries
  `corrected_by: [SOTA-131]` — the branched-conflict shape `luria.toml`
  already said it wanted readable from the trunk, and the reason this was
  filed as a second relation rather than a per-entry attribute.
- [ADR-017](record/decisions.d/ADR-017.md) is `Active`. It was filed `Proposed` on the argument that a proposal
  nothing implements belongs in the pending report; this contribution
  implements it, so the argument expires. Nothing in the decision changed.

### Fixed

- Two findings this record shipped in [#64](https://github.com/dmarx/anthology-of-the-sota/issues/64) and nobody saw, because the lint
  output was being read through `tail`. `ADR-017` cited `LU-ADR-076` without
  the foreign-code prefix, so it reported as a local code resolving to
  nothing; and its table of rejected checks names `SOTA-122`, a `Proposed`
  practice, as the example one of them fires on. The first is corrected, the
  second acknowledged with block scope — a directive inside a markdown table
  would break the table.

### Changed

- Pinned luria 0.11.0. It carries dmarx/luria#212, which lets a chain's spine
  walk more than one relation — the upstream change [ADR-017](record/decisions.d/ADR-017.md)'s second half
  is waiting on, so this record can spell succession with a sign rather than
  leaving it in prose. Nothing in this contribution uses it yet.
- Also in the release: dmarx/luria#207, a design principle about rewriting
  stale record prose rather than acknowledging it, which this record acted on
  under [#54](https://github.com/dmarx/anthology-of-the-sota/issues/54) before it was written down upstream.

### Added

- A decision settling what `source:` holds, `Proposed`. [ADR-010](record/decisions.d/ADR-010.md) made the field
  a list without saying what fills it, so the corpus grew two conventions —
  `SOTA-132` counts adopters as support, `SOTA-150` counts them as consensus
  data — and neither is checkable while both are live. The rule: `source:`
  holds work that produced *evidence about the claim*, and adoption without a
  test is consensus data. `consensus.yaml` already implied it, by admitting
  adopters "whether or not each adopter made the choice deliberately".
- With it, the one check the corpus supports: every declared source must be
  discussed in the body. Measured at 150 of 153 before adoption, and all three
  exceptions were real defects.

- The same decision says where the work it excludes goes. Defining `source:`
  narrowly evicts the literature that set up the problem, and the record
  already holds that relation without being able to say it: seven of the
  nineteen `extends:` edges mean "exists because the parent is broken" and
  state the defect only in prose. Succession gains a sign — corrective when
  the child names a defect in its parent as its motivation, cumulative
  otherwise — carried as a second relation rather than a document facet.
  dmarx/luria#211 shipped the one upstream change it needed in 0.11.0.

### Fixed

- `SOTA-109`, `SOTA-121` and `SOTA-150` each declared a source their body
  never mentioned — the GQA paper under "prefer GQA", Muon itself under "use
  Muon", and DeepSeek-V3 under the MoE practice. All three now say what the
  source contributes.
- `SOTA-142` loses `LIT-119` again. It gained it earlier the same day on the
  strength of its own sentence — Falcon-H1-Tiny's adoption "is what moves this
  from one group's result to a practice" — and the decision draws the line at
  whether the adopter *tested* the claim. Falcon-H1-Tiny used the power law
  without reporting a comparison, so the adoption moves the consensus reading
  and not the evidence base. The recommendation is unchanged.

### Fixed

- Three practices in the schedule and µP cluster now name every paper they
  rest on. Second batch of [#58](https://github.com/dmarx/anthology-of-the-sota/issues/58): six examined, three changed.
  - `SOTA-140` names `LIT-145`. Its Source section had said "Hägele et al.
    (2024), [LIT-145](record/literature.d/LIT-145.md), for the comparison against cosine" since it was filed;
    the frontmatter named only MiniCPM. The controlled comparison is what
    makes this practice evidenced rather than reported, and it was the half
    the field is now contesting.
  - `SOTA-141` names `LIT-145`. Its `consensus_note` already read "with
    [LIT-145](record/literature.d/LIT-145.md)'s cooldown pointing the same way", so the consensus value rested
    on a paper the source list did not name — exactly the disconnect [ADR-010](record/decisions.d/ADR-010.md)
    describes. The paper corroborates the endpoint, not the per-schedule
    comparison `promote_when` asks for, so the status does not move.
  - `SOTA-142` names `LIT-119`, the adoption its own body calls "what moves
    this from one group's result to a practice".
- No recommendation changed; `history:` entries per [ADR-019](record/decisions.d/ADR-019.md).
- `SOTA-039`, `SOTA-143` and `SOTA-144` were examined and are correct as they
  stand. `SOTA-144` is the instructive one: it cites `LIT-153` at length
  precisely to say the result *does not count*, and adding it to `source:`
  would invert what the practice says.

### Fixed

- Six practices in the Falcon-H1-Tiny and Olmo 3 cluster now name every paper
  they rest on, not just the report they were read from. First batch of [#58](https://github.com/dmarx/anthology-of-the-sota/issues/58).
  - `SOTA-122` names `LIT-121`, where the weight-decay-equilibrium claim and
    the multiplier remedy actually are — it had named only the blogpost that
    validated them at 90M, which is the case [ADR-010](record/decisions.d/ADR-010.md) itself argues from.
  - `SOTA-124` and `SOTA-125` name `LIT-120`: the memorization-window
    measurement one turns on is Figure 9 of the Falcon-H1 report, and the
    depth finding in the other is corroborated by the authors' 1.5B-Deep
    result.
  - `SOTA-127` names `LIT-123`, whose mechanism the source follows explicitly.
  - `SOTA-129` names `LIT-172` and `LIT-128`. Naming only Olmo 3 attributed a
    two-lab result to the lab that wrote it down last: Tulu 3 is where RLVR
    was named and published in full, and it is this practice's third stage.
  - `SOTA-130` names `LIT-164`. Its body already said Olmo 3 "remains the
    source" — correct, and written when a practice could name only one.
- No recommendation changed. All six carry a `history:` entry per [ADR-019](record/decisions.d/ADR-019.md).
- `SOTA-128` was examined and is correct as it stands: `LIT-124` and `LIT-125`
  are cited for *not* settling the masking question, which is what makes the
  source's two 90M runs worth reporting.

### Added

- A note for Barbero et al. (2024), *Round and Round We Go!* — the paper that
  opens a trained model to ask what RoPE is doing, rather than reasoning from
  the encoding's definition. It is the missing middle of the positional line:
  the high frequencies build positional attention heads, the low ones carry
  semantics in channels that provably fail at length, and truncating the low
  ones gives `p`-RoPE, a dial whose ends are exactly RoPE (`p`=1) and NoPE
  (`p`=0). Filed as extending `LIT-045` and compared against `LIT-207`.
  Closes [#59](https://github.com/dmarx/anthology-of-the-sota/issues/59).

### Changed

- `SOTA-151` gains the mechanism it had been reasoning around. Theorem 6.1 is
  why RoPE's frequencies do not survive a longer context, and it identifies
  the same distinction `LIT-193` reached from the other side. Deliberately
  not added to `source:` — the work explains why the problem exists, not that
  rescaling is the answer.

### Fixed

- `LIT-045` had four migrated bullets and two of them were contradicted by
  the line this note now roots. "Better extrapolation capability" is not a
  RoPE property — `SOTA-151` exists precisely because it does not extrapolate
  — and the long-range-decay justification, RoPE's own, is what the new note
  argues against. Both are corrected in place rather than deleted, since they
  are still what most readers believe.

### Added

- A practice for dropping positional encoding from the global-attention
  layers of a hybrid, `Active` at `emerging`. Three laboratories, three
  different local mechanisms and the same one-global-per-three-local layout
  within ten months, none replicating another's setup: Cohere's RNoPE-SWA at
  8B/5T, NVIDIA's SWAN-GPT at 1B and 8B, and Kimi Linear at 48B, shipped at
  2.8T in Kimi K3. Filed separately from `SOTA-132` because two of the three
  have no linear attention in them at all.
- Notes for the two papers that were missing: Yang et al.'s *Rope to Nope and
  Back Again*, which measures what each layer type is for — NoPE layers
  retrieve, RoPE layers attend locally — and Puvvada et al.'s SWAN-GPT. Both
  cite `LIT-207` and both were found in Kimi Linear's bibliography.

### Fixed

- `SOTA-151` said a model that already exists cannot take the NoPE option, and
  `SOTA-063` said reversibility was an open question. SWAN-GPT answers it:
  an 8B RoPE model pretrained on 15T tokens was converted by continued
  pretraining and came back at parity on short benchmarks. Neither practice's
  recommendation changes; the reason they are not filed as contesting each
  other is now cost rather than impossibility.
- `LIT-207` no longer says nobody has connected NoPE's `<bos>`-anchored
  position construction to the attention sink. Yang et al. measure both in one
  model and report that it is the NoPE layers that develop the sink.

### Added

- A note for Kazemnejad et al. (2023), the source under NoPE. The record had
  been discussing "no positional encoding" in four documents and two
  changelog fragments without holding the paper that established it — always
  as a thing Kimi models do, rather than as a controlled comparison of five
  positional schemes with a theorem behind it.

### Changed

- The positional-encoding line is declared rather than implied. `LIT-192`
  extends `LIT-045` — Position Interpolation is a rescaling of RoPE's indices
  and says so in its own first sentence — so the chain roots at RoFormer
  instead of at the interpolation. NoPE and ALiBi render alongside it, which
  is what two notes had been saying in prose. On the practice side,
  `SOTA-151` extends `SOTA-063`: rescaling RoPE is what a model that used
  RoPE does next.
- `LIT-133` records the half of Kimi Linear the note omitted. Its paper gives
  NoPE a design section, an ablation against a RoPE version of the same 48B
  configuration, and the citation the rest of this rests on; the note had
  been written about KDA alone, which is why every later document attributed
  NoPE to the K3 model report rather than to the method paper already in the
  record.
- `SOTA-063` says what it does not cover. Frontier practice has split, and a
  reader landing on "use RoPE" should learn that a linear-attention hybrid
  may be better off without it. Not marked `contested`: RoPE-or-not is
  settled at pretraining, so it is not a knob an existing model can turn.
- `SOTA-132` and `SOTA-151` cite the new note where they had been describing
  NoPE with nothing behind it.

### Fixed

- The 2026-09-07 curation entry's account of what merge-allocation hid stated
  two luria behaviours in the present tense that dmarx/luria#205 has since
  changed, and named the concretized practice by the temporary code it no
  longer answers to. Both halves are now stated as the past they are, with the
  fix and the version that carries it. This clears the record's last
  `legacy-spellings` finding — by rewriting the sentence rather than
  acknowledging it, which is the resolution dmarx/luria#201 settled on.

### Changed

- Pinned to luria 0.10.4, which carries two things this record needs.

  **[LU-#206](https://github.com/dmarx/luria/issues/206)** fixes the chain page's nesting: a step now renders under the
  parent it extends rather than under whichever step at that depth happened
  to precede it. Required before the lineage declarations in [#52](https://github.com/dmarx/anthology-of-the-sota/issues/52), which make
  the first real DAG in any luria record and would otherwise have the page
  assert that Kimi Linear descends from Mamba-3.

  **[LU-#205](https://github.com/dmarx/luria/issues/205)** gives merge-allocated documents standing with the reference
  checker, which means a temporary code is now scanned as a citation site.
  [ADR-013](record/decisions.d/ADR-013.md) spells `LIT-tmp3kf9x` out as an illustration of the shape, so it
  gains an `unresolved-ok` acknowledgement here — filed **with** the bump,
  because on 0.10.3 the code was not scanned and the directive would have
  been reported as applying to nothing.

### Added

- Thirteen `extends:` declarations, mined from the record's own prose. The
  practice page goes from 4 lines to 7 and the literature page from 2 to 6.

  Seven practices carried a `## Sequence` section that **narrated** a chain
  in paragraphs, and one of them declared it. That is the gap [ADR-011](record/decisions.d/ADR-011.md) was
  written to close — "so the fork this record already argues about is
  structure rather than paragraphs" — and it had reopened by accretion.

  Practices: QK-Clip extends Muon-with-decay ([SOTA-131](record/practices.d/SOTA-131.md) → [SOTA-121](record/practices.d/SOTA-121.md));
  decay-to-zero and the power-law peak both extend WSD ([SOTA-141](record/practices.d/SOTA-141.md), [SOTA-142](record/practices.d/SOTA-142.md) →
  [SOTA-140](record/practices.d/SOTA-140.md)); CompleteP extends µP ([SOTA-144](record/practices.d/SOTA-144.md) → [SOTA-143](record/practices.d/SOTA-143.md)).

  Literature: the SSM line (Mamba → Mamba-2 → Mamba-3, and → Gated DeltaNet
  → Kimi Linear, with Gated DeltaNet also extending the delta-rule paper);
  the µP line (u-µP and CompleteP from Tensor Programs V); the activation
  line (GLU → GLU Variants → PowLU); and YaRN from position interpolation.

### Fixed

- [LIT-194](record/literature.d/LIT-194.md) claimed GLA was one of Gated DeltaNet's two parents — "the delta
  rule of [LIT-195](record/literature.d/LIT-195.md) plus the data-dependent gate introduced here". It is not.
  Gated DeltaNet's abstract names the two mechanisms it combines as
  **Mamba2's** gate and DeltaNet's update rule, and its title is *Improving
  Mamba2 with Delta Rule*. The gating lineage runs through [LIT-162](record/literature.d/LIT-162.md).

  Declaring the edge is what caught it: writing `extends:` forces the
  question "which document, exactly", and prose had been able to gesture.
  GLA's real standing — an independent, earlier data-dependent gate for
  linear attention, plus the FlashLinearAttention kernels the whole line
  ships in — is what the note says now.

### Added

- Three notes closing the data-side gaps from the [#40](https://github.com/dmarx/anthology-of-the-sota/issues/40) reference pass.

  - **Deduplication** (Lee et al. 2021), the foundation under a step every
    pipeline in this record performs and none of them sourced. Three separate
    wins, usually conflated: memorised text emitted **ten times** less often,
    the same accuracy in fewer steps, and honest evaluation — train-test
    overlap contaminates a large share of standard validation sets. Only the
    middle one is an efficiency argument.

  - **Data mixing laws** (Ye et al. 2024). Mixture proportions are set by
    heuristic because tuning them looked like it needed a run per candidate.
    It doesn't: performance is a fittable function of the proportions, and
    nesting that with the scaling laws for steps and size lets small runs
    predict large ones. A 1B model over 100B RedPajama tokens matched the
    default mixture trained **48% longer**.

  - **Model collapse in synthetic data** (Zhu et al. 2024). A negative
    correlation between synthetic proportion and performance, with
    distributional shift and n-gram over-concentration as the signature. The
    remedy inverts the usual move: edit *human* text at the token level
    rather than generating better synthetic text, which bounds the test error
    by construction. DeepSeek-V4 cites it for the other end — filtering
    templated auto-generated content out of the crawl.

### Added

- The three remaining works each cited independently by two of this record's
  own model reports.

  - **Fewer Truncations Improve Language Modeling** (Ding et al. 2024), plus
    a practice. Concatenate-then-split fragments documents that would have
    fitted whole, and the model then learns to continue text whose beginning
    it never saw. Best-fit packing removes those truncations **at the same
    efficiency** — it minimises the number of sequences, so no padding is
    added and the reason everyone concatenates is not being traded away.
    58.3% less closed-domain hallucination is the number that explains the
    rest: truncation removes the grounding a fact depends on.

  - **Griffin** (De et al. 2024), where the interleaving pattern [SOTA-132](record/practices.d/SOTA-132.md)
    recommends actually starts — the delta-rule paper says its hybrid
    "follows Griffin and Samba". It also marks a fork the record had not
    named: Griffin's minority layers do **local** attention, while the
    layouts this record recommends keep **global** attention, and only the
    second preserves exact retrieval at arbitrary distance.

  - **Ring Attention** (Liu et al. 2023), the mechanism under a capability
    the record keeps citing without explaining. Blockwise attention
    distributed around a ring of devices with KV-block communication
    overlapped against computation, giving sequences device-count times
    longer with no approximation and no extra communication cost. Filed as
    vocabulary rather than practice: a distribution strategy dictated by
    cluster shape.

### Added

- **The GLU origin** (Dauphin et al. 2016). The record recommended SwiGLU
  without holding the GLU its name refers to, so the *shape* of the
  recommendation had no source. The paper's argument is about gradients, not
  expressivity: an LSTM-style tanh gate downscales both branches so the
  gradient shrinks multiplicatively with depth, while gating a **linear**
  unit leaves a path with no downscaling — a multiplicative skip connection.
  The gate is there to let depth work.

- **PowLU** (Jiang et al. 2026), the sibling to Kimi K3's SiTU-GLU and the
  better-evidenced of the two. Same objection from a different angle: for
  large positive inputs SwiGLU approximates x², and that quadratic
  amplification is what enlarges the output range and produces outliers. Its
  evidence includes a **SwiGLU-Clip** control, which matters — hard clipping
  is the obvious cheap fix, and a bounded-activation paper that skips it has
  not isolated its own contribution.

### Changed

- [SOTA-034](record/practices.d/SOTA-034.md) is `consensus: contested`, `contested_by` both, at `version: 2`.
  Two independent groups, months apart, decided the field's default
  activation is a numerical liability at frontier scale in low precision, and
  shipped bounded replacements at 2.8T and 124B.

  The practice says what that does and does not settle. **The recommendation
  stands at ordinary precision** — neither paper claims SwiGLU is worse, both
  object to its *range* when the arithmetic is narrow, which is a condition
  rather than a refutation. And the comparison nobody has run is named: the
  two remedies against each other, and either against SwiGLU where the
  instability does not appear.

  Reading the origin alongside them sharpens it: the linear, unbounded branch
  is the property the design was chosen for, which is why both remedies
  soft-cap it rather than removing it.

### Added

- Two notes for the numerics under the frontier reports, both cited by the
  reports and neither described in the record.

  - **Microscaling data formats** (Rouhani et al. 2023). What "FP4" and
    "MXFP4" actually mean in [LIT-139](record/literature.d/LIT-139.md) and [LIT-131](record/literature.d/LIT-131.md): a block of 32 elements
    sharing one E8M0 scale — eight exponent bits, no mantissa, so applying it
    is an exponent adjustment. Block scaling contains outliers locally
    instead of letting a few large values cost every small one its precision.
    8-bit does direct-cast inference on FP32 checkpoints with no calibration;
    6-bit trains weights, activations *and* gradients to FP32 accuracy with
    no recipe change; 4-bit weights cost a minor drop.

  - **Why low-precision transformer training fails** (Qiu et al. 2025). Kimi
    K3's stated reason for keeping the attention output in FP32. The failure
    needs two things at once: attention representations that are low-rank and
    similar across steps and tokens, and rounding error in BF16 addition that
    is *biased* rather than symmetric. The bias acts as a coefficient on the
    repeated low-rank update, so errors compound into a systematic gradient
    bias instead of cancelling, and the spectral norm runs away. De-biasing
    the rounding in flash attention stops it — which is what makes the
    account causal rather than correlational.

### Added

- **LatentMoE** (Elango et al., NVIDIA 2026), the architecture Kimi K3's
  expert layer is, which the record described twice without naming.

  Its objection is to how MoEs get designed: from high-level sparsity
  arguments, optimised for offline throughput. A roofline analysis of serving
  Qwen3-235B-A22B shows that at latency-critical batch sizes the per-expert
  token count is small, arithmetic intensity is low, and expert computation is
  **bandwidth-bound rather than compute-bound** — so accuracy per FLOP is the
  wrong objective and accuracy *per parameter* is what binds.

  The architecture follows: down-project tokens into a narrow latent space
  before the routed experts and keep those experts' weights there, while
  routing and the shared experts stay at full width. Dispatch volume and
  weight-loading bandwidth both fall by the width ratio, and the saving buys
  *more* experts rather than a smaller model.

### Changed

- [SOTA-150](record/practices.d/SOTA-150.md) gains a section on where the width should go once you have decided
  to make the layers sparse. Not filed as its own practice: one originating
  lab with one outside adopter (Kimi K3), and no independent comparison
  against a conventional MoE at matched serving conditions.

### Added

- The two parents of Gated DeltaNet, which the record has held ([LIT-137](record/literature.d/LIT-137.md))
  without either. Its title names both: the **delta rule**, and the
  **data-dependent gate**.

  - **Gated Linear Attention** (Yang et al. 2023) supplies the gate, and
    starts from a systems point being mistaken for an architectural one:
    linear attention was slower in wall-clock than a good softmax kernel
    because nobody had made it I/O-aware. FlashLinearAttention beats
    FlashAttention-2 as a standalone layer even at 1K, where the asymptotic
    argument has not begun to pay. The gate itself makes the forget term
    data-dependent and per-channel instead of RetNet's global constant.
  - **Parallelizing Linear Transformers with the Delta Rule** (Yang et al.
    2024) supplies the delta rule, and explains why it had not scaled: the
    original update is sequential over the sequence. A Householder-product
    reparameterization makes it chunkwise.

### Changed

- [SOTA-132](record/practices.d/SOTA-132.md) said "the controlled comparison is one group's at one mid scale".
  **It is not.** The DeltaNet paper ran the experiment in 2024 — two years
  before the reports that made the layout visible here — with two hybrid
  variants against a strong Transformer++ baseline at 1.3B, and both won.
  Different group, different linear module, different ratios, same
  conclusion.

  It also supplies a mechanism the source report does not: linear attention
  is content-addressed and specifically bad at precise local
  shift-and-compare, which a minority of softmax layers restores. That is a
  better reason to keep the global layers than "retrieval degrades", and it
  predicts the right ratio depends on how much local comparison the task
  needs rather than on a constant.

### Added

- A practice for extending a **finished** model's context: rescale the RoPE
  position indices so the longest relative distance the model is asked about
  is one pretraining already showed it, then fine-tune briefly. Sourced to two
  independent groups.

  The motivating fact is not that a longer window is expensive to train, but
  that training it directly barely works: fine-tuning a pretrained LLaMA at
  the longer length moved its *effective* window from 2048 to 2560 after more
  than 10000 batches. Rescaling reaches 32768 in under 1000 steps.

  Two notes behind it. **Position Interpolation** (Chen et al. 2023) makes the
  argument — a learned attention-score function is bounded between the grid
  points pretraining enforced and unbounded outside them, which is why
  interpolating is safe and extrapolating explodes. **YaRN** (Peng et al.
  2023) corrects the method: uniform stretching destroys RoPE's
  high-frequency components and stalls near a scale factor of 8, so scale by
  wavelength instead, leaving the dimensions that never complete a rotation —
  and therefore still carry *absolute* position — untouched. Its attention
  temperature folds into the rotary tables, so it costs nothing at run time.

  Filed `converged`: the mechanism ships in production, and Qwen3.8-27B's own
  serving configuration is the record's first-party evidence — `rope_type:
  yarn` at `factor: 4.0` over a 262144 native window.

  The practice also records the alternative rather than pretending there
  isn't one. Kimi K3 reaches 1M tokens with no positional encoding on its
  global-attention layers and says it therefore needs no rescaling at all.
  That is a pretraining-time choice, not a competing technique, which is why
  this is not filed as contested: a model that already exists cannot take it.

### Fixed

- `luria lint`'s source-mismatch check caught a real discrepancy on the first
  of those notes: arXiv registers the title as "via **Positional**
  Interpolation" while the paper's own title page reads "via **Position**
  Interpolation". The record follows the registry, with the reconciliation
  written into the note.

### Added

- Two notes for the phenomenon [SOTA-134](record/practices.d/SOTA-134.md) recommends removing and the record
  never described — the gap the [#40](https://github.com/dmarx/anthology-of-the-sota/issues/40) reference pass turned up.

  - **Attention sinks** (Xiao et al. 2023). A softmax cannot output zeros, so
    a head with nothing to attend to must still put its mass somewhere, and
    models learn to dump it on whatever every query can see. Replacing the
    first four tokens with linebreaks barely moves perplexity: it is the
    position doing the work, not the content.
  - **Massive activations** (Sun et al. 2024). How that gets implemented — a
    handful of scalars at ~100,000× the median, at fixed feature dimensions,
    behaving as constants rather than features, imposing an implicit bias on
    an attention mechanism that has no bias term. Distinct from outlier
    features, which the paper checks and finds do not overlap.

### Changed

- [SOTA-134](record/practices.d/SOTA-134.md) gains a section explaining what it is removing, and the reading
  changes: **the sink is load-bearing in an ungated model.** Evict those
  four KV entries and Llama-2-13B goes from 5.40 perplexity to 5158. The
  gate is not deleting a defect; it is removing the pressure that creates
  one, because a head that can scale its own output down has no surplus mass
  to shed.

  With that, three findings line up as one: an explicit learnable attention
  bias, a learnable sink token, and this output gate all eliminate the same
  phenomenon, and all three work by giving the model a way to *not attend*
  that softmax alone does not provide. Two cost nothing in quality; this one
  improves it.

  The practical corollary is now written down: a model **without** the gate
  needs its sinks protected, so anything that evicts early tokens — window
  attention, a rolling KV cache, aggressive trimming — has to keep the first
  few entries or retrain with a sink token.

### Changed

- [SOTA-148](record/practices.d/SOTA-148.md) (auxiliary-loss-free load balancing) moves from
  `consensus: unreplicated` to `emerging`, at `version: 2`. Its note said
  "no group outside it has published a result either way"; Kimi K3 is an
  outside group that adopted the method at 2.8T with 896 experts, found the
  fixed-step update rule outside the regime where it behaves, and published
  a replacement. The recommendation is unchanged and the promotion condition
  — balance *and* quality against an auxiliary-loss control — is still
  unmet, because K3 runs no such control.

  The practice also records **Quantile Balancing**, which keeps everything
  this practice turns on (bias excluded from the mixture weights, update
  applied only on the next step) and swaps the fixed step for a bias read
  off the router-score quantile matching each expert's target load,
  estimated from a per-expert histogram of margins.

  And it records the qualification DeepSeek-V4 makes to its own lab's
  result: auxiliary-loss-free bias at speed 0.001 *plus* "a slight
  sequence-wise balance loss" at weight 0.0001. The bias regulates load
  across a batch and cannot reach imbalance inside one sequence, so the
  practice's claim survives and the stronger reading of it does not.

### Added

- [SOTA-034](record/practices.d/SOTA-034.md) (SwiGLU) gains a *Variations* section for **SiTU-GLU**, the first
  replacement in the record. The objection is range, not quality: SwiGLU's
  two multiplicative factors are both unbounded, so coincident large
  coordinates give activation outliers and overflow risk in low precision.
  SiTU-GLU soft-caps the Swish gate's linear factor and the up branch
  independently with a scaled `tanh`. One group, one model, no ablation.

- [LIT-131](record/literature.d/LIT-131.md) gains the Stable LatentMoE stack — Normalized LatentMoE, SiTU-GLU,
  Quantile Balancing — and Table 1's K2-to-K3 comparison, which is the
  report's one quantitative account of what changed.

- [LIT-139](record/literature.d/LIT-139.md) gains the load-balancing detail above and the change of
  affinity-score activation from DeepSeek-V3's.

<!-- One fragment per contribution, named for its filing moment — `luria new
     changelog` stamps it, the way the devlog stamps entries. Keep
     only the headings that apply; delete the rest. Collected into CHANGELOG.md
     on a cadence, never on every merge (ADR-002).

     No user-facing changes? Replace everything with a single HTML comment
     saying why. A stub collects to nothing, which keeps "every contribution
     files a fragment" enforceable without inventing an entry. -->

### Added

-

### Fixed

-

### Changed

-

### Removed

-

### Documentation

-

### Fixed

- [SOTA-122](record/practices.d/SOTA-122.md) quoted the Falcon-H1-Tiny blogpost's "up to a 20% relative gain
  on MMLU, BBH and GSM8K" without its qualifier, which is "from random
  values". At 90M those three sit near chance, so the qualifier is most of
  the claim. Restored.

### Changed

- [SOTA-141](record/practices.d/SOTA-141.md) records what the newest frontier recipe actually does with the
  decay: DeepSeek-V4 ends at exactly 10% of peak (2.7e-4 → 2.7e-5 for Flash,
  2.0e-4 → 2.0e-5 for Pro), which is the customary floor this practice's
  source names and argues against, at 1.6T over 33T tokens.

  It also records why Kimi K3 does *not* satisfy the second half of the
  promotion condition despite being a schedule comparison with the
  hyperparameters retuned per schedule: that comparison runs "under a fixed
  minimum learning rate", which holds this practice's own variable constant.

- [SOTA-136](record/practices.d/SOTA-136.md) records that DeepSeek-V4 — the production report at depth its
  promotion condition asks for — does not answer the objection. Its case for
  the doubly-stochastic constraint is numerical stability, not stream
  distinctness; it reports no stream statistic, and the words *homogenize*,
  *diversity* and *distinct* appear nowhere in it.

<!-- The Falcon-H1-Tiny spot-check #18 asked for found no misalignment, so
     there is no user-facing change to report from it. The verification is
     recorded in the curation journal. -->

### Changed

- [SOTA-140](record/practices.d/SOTA-140.md) (warmup-stable-decay) is `consensus: contested`, with
  `contested_by: LIT-131`. Kimi K3 ran the same comparison the practice
  rests on, with the fairness correction that comparison already applies —
  hyperparameters retuned per schedule — and got the opposite answer at
  2.8T: cosine decay consistently lower final loss, and K3 adopts it. The
  recommendation is unchanged; what changed is the record's claim about how
  settled it is.

- Two claims in [SOTA-140](record/practices.d/SOTA-140.md) were wrong and are corrected:

  - "the schedule of every 2025–2026 report in the record" — false once K3
    was read.
  - "Final quality matches **or beats** a cosine schedule of the same
    length" — [LIT-145](record/literature.d/LIT-145.md)'s own result, with the peak learning rate swept for
    both arms, is "an almost perfect match", with the cooldown slightly
    ahead only at 10–20% of steps and the margin shrinking as training
    lengthens. A match plus the practical advantages, not a quality win
    with advantages on top.

- [SOTA-140](record/practices.d/SOTA-140.md)'s known-implementations line separates two things a report can
  mean by "cosine": DeepSeek-V4 ([LIT-139](record/literature.d/LIT-139.md)) holds its peak for most of
  training and decays near the end with a cosine-shaped cooldown, which is
  this practice; K3 runs cosine over the whole schedule, which is not.

### Changed

- The five claims [#18](https://github.com/dmarx/anthology-of-the-sota/issues/18) marked as *reported rather than read* are read claims
  now, checked against the primary sources. All five hold; the record's
  wording was accurate throughout, and what changes is the provenance and
  the precision, not the substance.

  - [LIT-131](record/literature.d/LIT-131.md) — Per-Head Muon is the report's own section (§2.5), and the
    51,219,741 sandboxes across 1,505,678 images figure is verbatim. The
    term *MuonClip* appears nowhere in the report, as the note said.
  - [LIT-139](record/literature.d/LIT-139.md), [SOTA-131](record/practices.d/SOTA-131.md) — DeepSeek-V4 declines QK-Clip and says why, under a
    heading called "Avoiding Exploding Attention Logits". [SOTA-131](record/practices.d/SOTA-131.md)'s
    variation paragraph now quotes it instead of hedging on coverage.
  - [LIT-139](record/literature.d/LIT-139.md) — the FP4 quantisation-aware training covers "MoE expert
    weights and the indexer QK path" and sits in post-training, both
    verbatim.
  - [LIT-138](record/literature.d/LIT-138.md), [SOTA-134](record/practices.d/SOTA-134.md) — Kimi K3's gated MLA gate is "input-dependent,
    channel-wise full-rank" against this paper's head-specific sigmoid. The
    relationship is stated rather than guessed at.
  - [LIT-135](record/literature.d/LIT-135.md) — the Qwen3.8-27B and Qwen3.6-27B `config.json` files were
    fetched and compared directly. They differ in exactly one key,
    `transformers_version`; every architectural field is identical.

### Fixed

- [LIT-131](record/literature.d/LIT-131.md) claimed its own ablation tables were "still unmined". The report
  has no component ablations at all — five tables, none of them an ablation
  — so the 2.5× scaling-efficiency figure cannot be apportioned between the
  changes it is credited to. The note says that now.

### Fixed

- The published site was always one merge behind. Pages and Docs both
  triggered on `push: [main]`, so they ran in parallel and Pages won: it built
  the merge commit's tree, and Docs then regenerated views and concretized
  merge-allocated codes on top of it. Harmless for a view whose content did
  not change; not harmless for a concretization, which *renames* record files.
  Five documents merged in [#33](https://github.com/dmarx/anthology-of-the-sota/issues/33) were missing from the site until an unrelated
  push happened to trigger Pages again.

  Pages now runs on `workflow_run` after Docs completes, which is what luria's
  own template has shipped all along — this repository's copy had drifted.

### Added

- Two practices for mixture-of-experts, answering the open question issue [#17](https://github.com/dmarx/anthology-of-the-sota/issues/17)
  poses and [LIT-170](record/literature.d/LIT-170.md) declined to settle: make the feed-forward layers sparse
  once the model is compute-bound (`Active`, `converged`), and build the sparse
  layers from many small experts plus an always-on shared one (`Active`,
  `emerging`).
- [SOTA-148](record/practices.d/SOTA-148.md) now `extends` the first of those, so the record's MoE material
  reads as one family rather than three unrelated documents: make it sparse,
  cut it up finely, keep it balanced.

### Changed

- The premise stops being unstated. [SOTA-146](record/practices.d/SOTA-146.md) already carried a caveat about RL
  being unstable on mixture-of-experts specifically, qualifying an
  architecture the record had never recommended.
- The three originating MoE papers the corpus was missing: the sparsely-gated
  layer (Shazeer et al., 2017), GShard (Lepikhin et al., 2020) and Switch
  Transformers (Fedus et al., 2021). The trunk practice is now sourced to the
  paper that introduced the change, as issue [#17](https://github.com/dmarx/anthology-of-the-sota/issues/17) asks, rather than to the one
  that measured it.

### Added

- A practice for auxiliary-loss-free load balancing: add a per-expert bias to
  the routing scores and update it from recent load, instead of penalising
  imbalance with an auxiliary loss whose gradients interfere with the
  objective. `Proposed`, `unreplicated` — the method and the 671B model that
  adopted it are both DeepSeek-AI, and nobody outside has published a result
  either way.

  [LIT-171](record/literature.d/LIT-171.md) had flagged itself as "a candidate practice the record has not
  drawn", worrying it would arrive without MoE context. It arrives without
  needing it: whether to build a sparse model is an editorial judgement, and
  how to keep its experts evenly loaded once you have is a technique. The
  record still carries no practice recommending a mixture of experts.

### Added

- A practice for Multi-head Latent Attention: compress the KV cache into one
  shared latent instead of sharing key and value heads. `Active`, `emerging` —
  four models across two labs, and no third adopter. [LIT-174](record/literature.d/LIT-174.md) had said filing it
  "closes the largest single hole the architecture half of the record had", and
  then no practice was drawn from it.

### Fixed

- [SOTA-023](record/practices.d/SOTA-023.md) and [SOTA-024](record/practices.d/SOTA-024.md) recommended multi-query attention and sat `Active`
  beside [SOTA-109](record/practices.d/SOTA-109.md)'s "prefer GQA to MQA or MHA". The record advised both at
  once. Both are `Superseded` by [SOTA-109](record/practices.d/SOTA-109.md) now; the bodies stay.
- [SOTA-109](record/practices.d/SOTA-109.md) was a migration stub — one line naming a source, no body, and the
  wrong authors. It now says what grouped-query attention is and why it is
  still the default, and names MLA as the other live answer rather than
  standing as the end of the line.
- Two attributions, verified against arXiv rather than corrected from memory:
  [LIT-024](record/literature.d/LIT-024.md) is Shazeer (2019), not "Dao et al."; [LIT-100](record/literature.d/LIT-100.md) is Ainslie et al.
  (2023), not "Yang et al."

### Added

- Two practices for the RL algorithm, a question the registry had never
  answered. [SOTA-129](record/practices.d/SOTA-129.md) and [SOTA-130](record/practices.d/SOTA-130.md) both say *when* to run RL with verifiable
  rewards; neither said which algorithm, while GRPO was cited by five notes
  and run by every reasoning recipe in the record.
- The settled half — drop the critic, take the baseline from a group of
  samples for the same prompt — is `Active`, `converged`. All four papers here
  that run or rework GRPO keep it, including the three that attack the rest of
  the objective.
- The unsettled half extends it and stays `Proposed`, `emerging`: three
  independent groups published a correction to the objective within seventeen
  months, each locating the defect somewhere else, and nothing compares them.

### Changed

- luria 0.10.3 in all six pins. The site's record line now names each cited
  document as well as citing it — `LIT-140 — mHC: Manifold-Constrained
  Hyper-Connections` rather than `LIT-140`, which asked a reader to already
  know the corpus — and a field with several values gets one bulleted line per
  value instead of center dots.

### Fixed

- The site's record line said things twice on every page. `status:` was
  rendered once by the status machinery and again by the generic vocabulary
  loop it joined when this record declared it; and every relation with a
  declared converse appeared both as itself and as a backlink under its raw
  field name — [LIT-140](record/literature.d/LIT-140.md) named [LIT-141](record/literature.d/LIT-141.md) three times. Both are luria 0.10.1.

### Changed

- luria 0.10.2 in all six pins. It also turns the record line from one
  center-dot-separated line into a two-column table, which is what the
  eleven-fact pages needed.
- The README links the published site from a `<!-- luria:site -->` region
  rather than not at all. Derived from the config, so it cannot drift from
  where `luria site` actually deploys.

### Added

- `contested_by:` on practices — a list of LIT codes, required exactly when
  `consensus: contested`. Of the six values on the axis, contested is the only
  one that asserts a specific other document exists, so it is now held to the
  same standard as `source:`: the evidence for was already checked, and the
  evidence against was prose ([ADR-016](record/decisions.d/ADR-016.md)).
- The two contested practices name their opposition as data rather than only
  in body prose: [SOTA-130](record/practices.d/SOTA-130.md) → [LIT-167](record/literature.d/LIT-167.md), [SOTA-136](record/practices.d/SOTA-136.md) → [LIT-151](record/literature.d/LIT-151.md) and [LIT-181](record/literature.d/LIT-181.md).

### Documentation

- The record page now states the rule — *`contested_by` — required when
  `consensus` is `contested`* — beside the fields it already listed.

### Fixed

- Two references to luria issues pointed at this repository's issue tracker
  instead. `LU-#173` in [ADR-015](record/decisions.d/ADR-015.md) linked to *our* [#173](https://github.com/dmarx/anthology-of-the-sota/issues/173), not luria's: a remote
  prefix scopes a document code but not an issue number, and `luria link --fix`
  quietly resolved the bare `#173` locally. Both are explicit URLs now, and the
  silent mislink is filed upstream as
  [dmarx/luria#194](https://github.com/dmarx/luria/issues/194).

### Added

- `extends:` now declares `extended_by:` as its converse, on both SOTA and
  LIT, and the back-references are written. The fork in a line is legible
  from the **trunk** and not only from the branches: [LIT-140](record/literature.d/LIT-140.md) says
  `extended_by: [LIT-151, LIT-181]`, which is the branched-conflict shape
  this record argues about, readable without opening four other notes or
  the chain page.

### Changed

- `compared_against:` now declares itself as its `converse` on both schemes.
  Upstream made the declaration the thing that licenses `luria link --fix`
  to write the other side of a symmetric relation, so without it the guard
  and the fixer both go quiet — silently, which is why this is here.
  Behaviour is unchanged: a one-sided comparison is a finding, and the fixer
  satisfies it.

### Notes

- Storing `extended_by:` is redundant with the forward declaration, which is
  the cost. It is paid deliberately: the fixer keeps both sides in agreement
  in either direction, including when a relation is *withdrawn*, so the
  redundancy cannot drift the way a hand-maintained back-reference would.

### Added

- A `consensus:` axis on practices — `unassessed | unreplicated | contested |
  emerging | converged | universal` — orthogonal to `status:`. `status` is
  this record's editorial position and could not say "shipped in production at
  one lab, disputed by two others"; mHC was exactly that ([ADR-015](record/decisions.d/ADR-015.md)).
- `extends:` and `compared_against:` on practices, and a
  [lines-of-practice page](docs/practice-lines.md), so an agreed trunk and the
  forks contending off it stop rendering identically.
- Ten practices assessed, each with a `consensus_note:` citing the grounds.
  The other 134 are `unassessed`, which is true and countable.

### Changed

- [ADR-014](record/decisions.d/ADR-014.md) amended to version 2: a threshold of *adoption* is a kind of result.
  The phrasing rule was narrower than the mechanism — two of the eight
  conditions written under it were already social.

### Added

- `promote_when:` on all eight provisional practices, plus the one Deferred
  one: what would settle each, stated as a kind of result rather than a
  quantity of them. Required by the lint at those statuses ([ADR-014](record/decisions.d/ADR-014.md),
  luria#170).
- Lineage as fields — `extends:` and `compared_against:` on LIT — with the
  residual chain migrated as the first line and rendered to
  [docs/lineage.md](docs/lineage.md). [ADR-011](record/decisions.d/ADR-011.md) promoted to Active on the
  strength of the trial.

### Changed

- The practice template scaffolds `source:` as a list and prompts for
  `promote_when:`. It had said `source: LIT-000` since before the field went
  plural, which is why 140 of 144 practices were single-sourced.
- Four notes in the residual chain lost the paragraphs that recited the
  chain. Every one was a roll call; the arguments stayed where they were.

### Added

- [ADR-014](record/decisions.d/ADR-014.md): a practice at a provisional status must state what would
  change it, in a `promote_when:` field, phrased as a kind of result rather
  than a count of them. Filed after two practices with near-identical prose
  conditions were both satisfied by the same paper on the same day and only
  one promoted.

### Changed

- **[SOTA-133](record/practices.d/SOTA-133.md) is Active.** Its condition — "one group, one paper, one
  production model; promote when an independent result lands" — is met.
  [LIT-152](record/literature.d/LIT-152.md) is a different laboratory implementing Attention Residuals in its
  own harness and measuring against its own competing design: 1.762 training
  loss at 28 layers against 1.789 for the pre-norm baseline, level with
  Qwen's Gated Residual. The practice gains conditions saying what that does
  *not* establish — three designs measure the same, so what pays is replacing
  fixed accumulation with something learned, and which learned thing is open.
- **[SOTA-136](record/practices.d/SOTA-136.md)'s condition is met and deliberately not applied**, which is now
  written into the practice rather than left as a silent non-decision. The
  same [LIT-152](record/literature.d/LIT-152.md) evaluation found mHC comparable, so "promote on an independent
  result" is satisfied — but [LIT-151](record/literature.d/LIT-151.md) and [LIT-181](record/literature.d/LIT-181.md) both attack the
  doubly-stochastic constraint the practice specifically recommends, from
  opposite directions. The claim has independent support and the mechanism
  has independent opposition; a condition phrased as "an independent result"
  cannot tell those apart, and was the wrong condition.
- **[SOTA-122](record/practices.d/SOTA-122.md)'s condition is sharpened.** "An independent reproduction *or* a
  result above 1B" was half-met by [LIT-153](record/literature.d/LIT-153.md): an independent group at 1.2B
  confirming the weight-decay-equilibrium diagnosis and adopting the opposite
  remedy. Confirming the mechanism while declining the fix is not a
  promotion; the condition now asks for gains from learned per-row and
  per-column multipliers specifically.
- **[SOTA-144](record/practices.d/SOTA-144.md)** notes the same paper's depth-transfer result as related but
  not a reproduction — two routes to one property is evidence the property is
  reachable, not that this route works.

### Fixed

- Two claims [#18](https://github.com/dmarx/anthology-of-the-sota/issues/18) flagged as reported rather than read are now checked against
  the primary sources:
  - DeepSeek-V4's FP4 quantization-aware training covers "MoE expert weights
    and the indexer QK path", and the report places it in **post-training**,
    not pretraining — which [LIT-139](record/literature.d/LIT-139.md) had not distinguished.
  - Kimi K3's gated MLA is *not* quite the head-specific gate [SOTA-134](record/practices.d/SOTA-134.md)
    records. The report says "an input-dependent, channel-wise full-rank
    output gate" — same position in the block, same justification, finer
    granularity. [LIT-138](record/literature.d/LIT-138.md)'s "appears to be the same idea" is replaced with
    what the report says.

### Added

- [LIT-131](record/literature.d/LIT-131.md) is read from the report rather than its abstract, and gains what
  that turned up: **no positional encoding on any MLA layer**, with the
  interleaved KDA layers supplying position sensitivity instead; the
  channel-wise gate above; the MTP-to-draft-model lineage; and the RL
  sandbox scale (51,219,741 sandboxes across 1,505,678 images).
- [SOTA-132](record/practices.d/SOTA-132.md) gains the consequence of that NoPE finding, which is a second
  argument for the hybrid the practice was filed without: with no positional
  parameter in the global layers, extending the context no longer requires
  retuning a RoPE base or applying YaRN, so the hybrid makes [SOTA-139](record/practices.d/SOTA-139.md)'s
  staged extension a smaller operation.

### Added

- Groups 3, 4 and 5 of the literature backlog ([#17](https://github.com/dmarx/anthology-of-the-sota/issues/17)) — 27 notes, all written
  from the papers.

  **Architecture (16).** The DeepSeek line the record's frontier half
  descends from and had never held: DeepSeekMoE, MLA from DeepSeek-V2,
  DeepSeek-V3, and auxiliary-loss-free load balancing. The state-space line
  from its root: Mamba, the SSM/attention duality and Mamba-2, Mamba-3, and
  RWKV-7 as the other expressive recurrence. Multi-token prediction and
  EAGLE-3, which explain the MTP-head-into-draft-model arrangement three
  frontier models ship fully formed. Llama 3 and Qwen3 as the period's
  dense and thinking-mode recipes. And four recent papers: Native Hybrid
  Attention, Erase-then-Delta Attention, Nemotron 3 Nano, and
  Spectral-Sphere-Constrained Hyper-Connections.

  **Data (5).** Scaling Data-Constrained Language Models, FineWeb,
  Nemotron-CC, Scaling Laws for Precision, and the training-time
  augmentation study.

  **Post-training (6).** DPO, Tulu 3, DeepSeek-R1, and the three GRPO
  variations — Dr. GRPO, DAPO and GSPO.

### Changed

- **[SOTA-126](record/practices.d/SOTA-126.md) cites DPO.** The practice recommended the algorithm and had
  never named the paper, which is the exact failure [DP-001](docs/design-principles.md#dp-1) exists to
  prevent; it survived because the practice's own finding is about DPO's
  behaviour at 90M rather than about DPO. A new section explains what DPO is
  and why it predicts the failure the practice guards against — a rising
  implicit reward is not an improving policy.
- **[SOTA-130](record/practices.d/SOTA-130.md) cites DeepSeek-R1**, which it had been calling "the R1-Zero
  style ... not in the record". It also gains a second reason to stay
  *Proposed*: Dr. GRPO finds DeepSeek-V3-Base already exhibits the "Aha
  moment" before any RL, so how much of the result belongs to skipping SFT
  and how much to the base model is unsettled.
- **[SOTA-124](record/practices.d/SOTA-124.md)'s "on the order of 400 times"** is corrected to 100 or more —
  the same misreading fixed in [LIT-119](record/literature.d/LIT-119.md) earlier and missed here. Its
  disagreement with the four-epoch result is now written out with both
  papers named, including why they may not be measuring the same thing.
- **[SOTA-132](record/practices.d/SOTA-132.md) gains a third independent adopter** — Nemotron 3 Nano, a MoE
  hybrid Mamba-Transformer from a third laboratory — which widens the claim
  from "the 3:1 interleave works" toward "a hybrid of a fixed-state mixer
  with periodic global attention works". Native Hybrid Attention is recorded
  as a third *layout*, keeping layers uniform and making the ratio a
  continuous knob.
- **[SOTA-135](record/practices.d/SOTA-135.md) gains a "Where it is incomplete" section**: the delta rule's
  correction is active and targeted while its decay is passive and global,
  so stale content at another address can only decay. Erase-then-Delta
  decouples the two.

### Documentation

- The residual chain now has two independent critiques of the constraint
  [SOTA-136](record/practices.d/SOTA-136.md) recommends. oHC says the doubly-stochastic set is bounded above
  but not below; sHC says it is degenerate near the identity and cannot
  subtract. Different arguments, same verdict, opposite remedies — and what
  all four papers agree on, that widening the stream and constraining the
  mixing helps, is untouched. That agreement is probably the practice to
  carry eventually.

### Added

- Group 2 of the literature backlog ([#17](https://github.com/dmarx/anthology-of-the-sota/issues/17)) — optimizers and stability, seven
  notes, written from the papers rather than from abstracts:
  - **Fantastic Pretraining Optimizers and Where to Find Them** — ten
    optimizers, 0.1B–1.2B, each tuned rather than handed the baseline's
    hyperparameters, and judged at the end of training. The controlled
    comparison the Muon practices lacked.
  - **Fantastic Pretraining Optimizers II: Hyperball** — the follow-up that
    blames the shrinking advantage on constant decoupled weight decay fixing
    the equilibrium weight norm.
  - **Small-scale proxies for large-scale Transformer training
    instabilities** — attention-logit growth reproduced at small scale, and
    the mechanism under QK-Clip.
  - **2 OLMo 2 Furious** — a documented stability recipe at 7B–32B with the
    checkpoints to check it.
  - **SOAP** and **Distributed Shampoo** — the second-order line Muon is
    contrasted with.
  - **Muon (Jordan et al., 2024)** — the blog post three frontier labs
    pretrain with, named as "not in the corpus" by [LIT-122](record/literature.d/LIT-122.md), [SOTA-121](record/practices.d/SOTA-121.md) and
    [SOTA-131](record/practices.d/SOTA-131.md) and now filed with a `url:` under [ADR-009](record/decisions.d/ADR-009.md).

### Changed

- **[SOTA-121](record/practices.d/SOTA-121.md) no longer quotes 2×.** [LIT-122](record/literature.d/LIT-122.md)'s scaling-law runs put Muon at
  roughly twice AdamW's compute efficiency; an outside comparison that tunes
  both optimizers separately and measures at the end of training gets 1.4× at
  0.1B falling to **1.1× at 1.2B**, and finds that ranking optimizers on
  intermediate checkpoints can reverse the answer. The practice stands — the
  gain is free, and every frontier adopter in the record trains far above the
  largest scale tested — but a new "How much it buys" section gives the range
  and says which number not to repeat.
- [SOTA-121](record/practices.d/SOTA-121.md)'s `source:` names four notes rather than one, the first use of
  [ADR-010](record/decisions.d/ADR-010.md) on a practice whose evidence was already plural in its body.
- [SOTA-131](record/practices.d/SOTA-131.md) gains a "Mechanism" section pointing at the instability paper, and
  both it and [LIT-122](record/literature.d/LIT-122.md) now link the Muon blog post instead of describing it as
  absent.

### Added

- The arXiv remote declares how to ask what an identifier is — `uris.title`
  and `title_re` — and `remotes.lock.json` now carries the resolved title for
  all 143 identifiers in the record. `luria lint` compares each against the
  title its note claims, offline, and reports a disagreement as
  `source-mismatch` (LU-[#166](https://github.com/dmarx/anthology-of-the-sota/issues/166)).

  This is the check that would have caught the 53 bad identifiers repaired
  earlier today, two years earlier. Reintroducing one of them —
  [LIT-099](record/literature.d/LIT-099.md) pointed back at `2305.10755` — now produces:

      [LIT-099](record/literature.d/LIT-099.md).md:9: `arxiv: 2305.10755` resolves to "Measurement-Device-
      Independent Quantum Secret Sharing", not "PaLM 2 Technical Report"

  Refreshing what upstream serves is `luria remotes --resolve`, the only
  command in the workflow that touches the network. The lockfile is
  committed, so CI and an offline checkout answer the question the same way.

### Added

- Four decisions taken from a review of whether the schema is serving the
  record. Two are adopted here, two are proposals:
  - [ADR-010](record/decisions.d/ADR-010.md) (Active) — a practice's `source:` is a list, and the
    relationship is declared rather than merely required.
  - [ADR-013](record/decisions.d/ADR-013.md) (Active) — codes are allocated at merge, not at filing.
  - [ADR-011](record/decisions.d/ADR-011.md) (Proposed) — lineage between documents becomes a field instead
    of a paragraph repeated in every note that participates in a chain.
  - [ADR-012](record/decisions.d/ADR-012.md) (Proposed) — a practice declares its altitude, and one with no
    body cannot claim to be a design decision.

### Changed

- `source:` holds a list of LIT codes. All 144 practices migrate to
  single-element lists, which changes no meaning; [SOTA-132](record/practices.d/SOTA-132.md) gains the four
  further sources its body already named. The field is now declared as a
  reference to the LIT scheme, so the lint checks that every element names a
  real note rather than accepting any truthy value — and, with `many`,
  checks every element rather than stringifying the list and reading the
  first.
- Every scheme allocates at merge. `luria new` prints a temporary code and
  `luria concretize` assigns the number where merges serialize. Adopted
  because two branches opened the same afternoon both minted [LIT-144](record/literature.d/LIT-144.md) and
  [LIT-145](record/literature.d/LIT-145.md) for different papers, and nothing but a human reading both pull
  requests would have caught it.

### Documentation

- The evidence behind a practice is now countable, which makes the record's
  own promotion rule checkable: [LIT-121](record/literature.d/LIT-121.md) and [LIT-134](record/literature.d/LIT-134.md) each say a practice
  "stays Proposed until a result from outside the authors' group is in the
  record", and all eight Proposed practices do currently sit at exactly one
  source.

### Fixed

- Every arXiv identifier in the record now resolves to the paper the note
  names. Checked against the arXiv API: 53 of 139 did not, and all 53 are
  repaired. 22 were cosmetic — a truncated title, or a nickname the record
  had prepended (`AdamW:`, `DALL-E 2:`, `Imagen:`, `ControlNet:`), now set
  to the published title verbatim. One was worse than cosmetic: [LIT-031](record/literature.d/LIT-031.md) was
  filed as "Neural Networks are Surprisingly Modular" when the paper is
  "*Pruned* Neural Networks are Surprisingly Modular".
- 31 carried an identifier belonging to an unrelated paper — the migration's
  identifiers were plausible and wrong, so [LIT-099](record/literature.d/LIT-099.md) cited a paper on quantum
  secret sharing for PaLM 2, and [LIT-059](record/literature.d/LIT-059.md) cited electron losses in hypersonic
  flows for checkpointing. 15 named a work identifiable from the title or
  the recorded author and were repointed at it. BytePS ([LIT-051](record/literature.d/LIT-051.md)) and
  CheckFreq ([LIT-059](record/literature.d/LIT-059.md)) were published at OSDI and FAST and never posted to
  arXiv, so they take a `url:` under the source field group.

### Changed

- 16 notes were not citation errors but synthetic entries: a generic title,
  four generic bullets, an author unconnected to any such work, and no paper
  behind them. 39 practices — a little over a quarter of the registry — were
  sourced to them. Rather than retire the notes and leave those practices
  dangling, each was re-sourced to the real work its practices actually rest
  on, in place, with `history:` recording what the note used to claim:

  | was | now |
  |---|---|
  | "Gradient Clipping Helps Training Dynamic Neural Networks" | Pascanu et al., On the difficulty of training RNNs |
  | "Deep Neural Network Initialization for Large-Scale Models" | ReZero |
  | "A Systematic Approach to Data Loading in Deep Learning" | Analyzing and Mitigating Data Stalls in DNN Training |
  | "WebDataset: Efficient Data Loading for ML" | High Performance I/O For Large Scale Deep Learning |
  | "Training Instability Detection and Recovery" | GLM-130B |
  | "Tuning Large-Scale Distributed Training Communication" | Deep Gradient Compression |
  | "Efficient Checkpointing for Large-Scale Training" | CheckFreq |
  | "Compiler Optimization for Deep Learning" | TVM |
  | "Hardware-Aware Neural Network Training" | Data Movement Is All You Need |
  | "Optimizing CUDA Kernels for LLM Inference" | SARATHI |
  | "Analyzing the Learning Dynamics of LLMs" | On Layer Normalization in the Transformer Architecture |
  | "SGDR++" | SGDR |

- Nine practices moved to sources the record already held, because the right
  paper was already filed: [SOTA-050](record/practices.d/SOTA-050.md) to Attention Is All You Need, whose
  1/sqrt(d_k) it restates; [SOTA-052](record/practices.d/SOTA-052.md) to DeepNet; [SOTA-073](record/practices.d/SOTA-073.md), [SOTA-074](record/practices.d/SOTA-074.md) and
  [SOTA-076](record/practices.d/SOTA-076.md) to BytePS; [SOTA-113](record/practices.d/SOTA-113.md) to vLLM; [SOTA-114](record/practices.d/SOTA-114.md) to FlashAttention; [SOTA-098](record/practices.d/SOTA-098.md)
  to PaLM; [SOTA-099](record/practices.d/SOTA-099.md) to GLM-130B.
- [LIT-058](record/literature.d/LIT-058.md), [LIT-095](record/literature.d/LIT-095.md) and [LIT-110](record/literature.d/LIT-110.md) cite nothing and could have been retired;
  they are re-sourced too, since the entries were gesturing at real papers
  (Shallue et al. on batch size, LPIPS, Efficiently Scaling Transformer
  Inference) and a real note is worth more than a tidy attic.

### Removed

- [LIT-116](record/literature.d/LIT-116.md) is retired. TensorRT-LLM is software with no paper behind it, and
  the note carried no reading; it now names the project as its source rather
  than a physics preprint.

### Documentation

- Three re-sourced notes point out where a practice and its new source
  disagree, rather than papering over it: [SOTA-055](record/practices.d/SOTA-055.md) states an epoch-based
  checkpointing rule while CheckFreq's argument is that epochs are the wrong
  unit; [SOTA-078](record/practices.d/SOTA-078.md) and [SOTA-080](record/practices.d/SOTA-080.md) give buffer and worker numbers that are
  operational folklore rather than results in the WebDataset paper; [SOTA-100](record/practices.d/SOTA-100.md)
  asks for warmup proportional to model size while its new source shows the
  need for warmup is a property of where the normalization sits.

### Added

- oHC ([LIT-151](record/literature.d/LIT-151.md)) and the Qwen3.8-Next design report ([LIT-152](record/literature.d/LIT-152.md)), the two
  developments the offline session could not see. [LIT-152](record/literature.d/LIT-152.md) is the first
  place the record's three residual replacements — mHC, Attention Residuals
  and Qwen's Gated Residual — have been run in one harness, and they come
  out level, separated by inference cost rather than quality. [LIT-151](record/literature.d/LIT-151.md) proves
  that the doubly stochastic constraint [SOTA-136](record/practices.d/SOTA-136.md) recommends bounds the
  stream mixing from above but not below, so the widened streams homogenize
  with depth.

### Fixed

- Two misstatements in [LIT-119](record/literature.d/LIT-119.md), both checked against the blogpost's own
  source: Tulu3 is repeated 100 or more times over the 800 GT of
  SFT-pretraining, not 400; and the learnable-multiplier ablation is
  reported there as an unquantified plot, not as "up to a 20% relative gain
  on MMLU, BBH and GSM8K". The real numbers are the preprint's, and are now
  in [LIT-121](record/literature.d/LIT-121.md) where they belong: +1.10 average over seven benchmarks against
  a tuned Muon baseline, carried by BBH (+3.39) and GSM8K (+2.61), with
  MMLU flat.
- [LIT-131](record/literature.d/LIT-131.md) attributed "MuonClip" to the Kimi K3 report, which never uses the
  term — it says the weight-clipping mechanism introduced in Kimi K2 — and
  gave the context window as 1,048,576 tokens, a precision the report does
  not claim. The per-head Muon variant is now described rather than named.
- [LIT-140](record/literature.d/LIT-140.md) read a single 6.7% figure, measured at expansion rate n = 4, as a
  6–7% range across the three model sizes of the scaling study.
- [LIT-142](record/literature.d/LIT-142.md) called DeepSeek-V3.1-Terminus a dense model. It is a
  mixture-of-experts; what was dense was its attention.
- [LIT-135](record/literature.d/LIT-135.md) carried an unattributed report that the model over-thinks by
  default. What the card documents is that `reasoning_effort` defaults to
  `xhigh`, the deepest of its three settings.

### Changed

- [LIT-139](record/literature.d/LIT-139.md) no longer defers to secondary coverage on QK-Clip. The report
  says it directly — "we do not employ the QK-Clip technique in our Muon
  optimizer" — and gives the reason: an RMSNorm on the queries and the
  compressed KV entries, applied just before the core attention, already
  bounds the logits. [SOTA-131](record/practices.d/SOTA-131.md)'s remedy is one of two.
- [LIT-134](record/literature.d/LIT-134.md) and [LIT-140](record/literature.d/LIT-140.md) each claimed the two residual replacements had never
  been compared. [LIT-152](record/literature.d/LIT-152.md) compares them.

### Added

- The schedule and parameterization the record's 2025–2026 recipes assumed
  but did not hold: MiniCPM's warmup-stable-decay ([LIT-144](record/literature.d/LIT-144.md)), the controlled
  cooldown study ([LIT-145](record/literature.d/LIT-145.md)), the Power scheduler ([LIT-146](record/literature.d/LIT-146.md)), linear decay to
  zero ([LIT-147](record/literature.d/LIT-147.md)), µP ([LIT-148](record/literature.d/LIT-148.md)), u-µP ([LIT-149](record/literature.d/LIT-149.md)) and CompleteP ([LIT-150](record/literature.d/LIT-150.md)).
- Five practices with them: warmup-stable-decay ([SOTA-140](record/practices.d/SOTA-140.md)); linear decay
<!-- inactive-ok: SOTA-141 — a Proposed refinement of the decay, named as part of the schedule chain -->
  to zero ([SOTA-141](record/practices.d/SOTA-141.md), Proposed); a power-law peak learning rate that
  transfers across tokens and batch size ([SOTA-142](record/practices.d/SOTA-142.md)); µP transfer across
<!-- inactive-ok: SOTA-144 — a Proposed extension of µP transfer, named as part of the chain -->
  width ([SOTA-143](record/practices.d/SOTA-143.md)); CompleteP's transfer across depth ([SOTA-144](record/practices.d/SOTA-144.md), Proposed).
  The Falcon-H1-Tiny recipe now cites all three of the components it uses.

### Changed

<!-- inactive-ok: SOTA-039 — the retired cosine practice, named as the predecessor in the chain -->
- The single-cycle cosine practice from GPT-3 ([SOTA-039](record/practices.d/SOTA-039.md)) is Superseded by
  warmup-stable-decay, with the reason in its status note and body — the
  first migrated practice the record has retired on the evidence of what
  came after it. The schedule chain now reads warm restarts → one cosine
<!-- inactive-ok: SOTA-141 — a Proposed refinement of the decay, named as part of the schedule chain -->
  cycle → WSD, with the decay's end ([SOTA-141](record/practices.d/SOTA-141.md)) and peak ([SOTA-142](record/practices.d/SOTA-142.md)) as open
  refinements.

### Added

- The Falcon-H1-Tiny technical blogpost ([LIT-119](record/literature.d/LIT-119.md)) and eight practices drawn
  from it: Muon with AdamW-matched update RMS, learnable per-row/column
  multipliers, pretraining tiny models directly on the target SFT or
  reasoning mix, memorization-window-aware data repetition, depth and SSM
  width over MLP width at a fixed tiny budget, single-epoch DPO, filtering
  chain-of-thought traces from tiny specialized models' data, and
  loss-unmasked fill-in-the-middle training ([SOTA-121](record/practices.d/SOTA-121.md) – [SOTA-128](record/practices.d/SOTA-128.md)).
- The ten works the blogpost leans on for its decisions, so its citations
  resolve inside the record: the Falcon-H1 report, Learnable Multipliers,
  Muon is Scalable, Why Do Reasoning Models Loop, the FIM paper, the
  Qwen2.5-Coder report, AST-FIM, DeepSeekMath (GRPO), Falcon-H1R, and the
  tiny-reasoning write-up that is the record's second `url:`-only source
  ([LIT-120](record/literature.d/LIT-120.md) – [LIT-129](record/literature.d/LIT-129.md)).
- Olmo 3 ([LIT-130](record/literature.d/LIT-130.md)), and with it the recipe the blogpost departs from and
  the variation it names: the three-stage reasoning curriculum ([SOTA-129](record/practices.d/SOTA-129.md))
  and RL with verifiable rewards straight from the base model ([SOTA-130](record/practices.d/SOTA-130.md),
  Proposed). The anti-curriculum practice now names both, so the sequence
  can be followed rather than only its current end.
- Kimi K3 ([LIT-131](record/literature.d/LIT-131.md)) and the three papers its architecture and optimizer
  come from: Kimi K2 ([LIT-132](record/literature.d/LIT-132.md), MuonClip), Kimi Linear ([LIT-133](record/literature.d/LIT-133.md), Kimi Delta
  Attention) and Attention Residuals ([LIT-134](record/literature.d/LIT-134.md)). Three practices with them:
  QK-Clip when training with Muon at scale ([SOTA-131](record/practices.d/SOTA-131.md)), a ~3:1 interleave
  of linear and global attention ([SOTA-132](record/practices.d/SOTA-132.md)), and learned attention over
<!-- inactive-ok: SOTA-133 — a Proposed practice, named as the sibling variation -->
  preceding layers in place of the residual sum ([SOTA-133](record/practices.d/SOTA-133.md), Proposed). The
  Muon practice from the blogpost now points at its successor.
- Qwen3.8-27B ([LIT-135](record/literature.d/LIT-135.md)) and the design it inherits: Qwen3-Next ([LIT-136](record/literature.d/LIT-136.md)),
  which first shipped the 3:1 Gated DeltaNet to gated-attention hybrid,
  and the two papers each layer type comes from — Gated Delta Networks
  ([LIT-137](record/literature.d/LIT-137.md)) and Gated Attention ([LIT-138](record/literature.d/LIT-138.md)). Two practices with them: a
  sigmoid output gate per attention head ([SOTA-134](record/practices.d/SOTA-134.md)) and the gated delta
  rule for linear-attention layers ([SOTA-135](record/practices.d/SOTA-135.md)). The hybrid-attention
  practice now has two independent adopters and a written sequence.
- DeepSeek-V4 ([LIT-139](record/literature.d/LIT-139.md)) and the lines it extends: the residual — Hyper-
<!-- inactive-ok: LIT-141 — the superseded paper, named as the predecessor in the chain -->
  Connections ([LIT-141](record/literature.d/LIT-141.md), Superseded) → mHC ([LIT-140](record/literature.d/LIT-140.md)) — and sparse attention —
  NSA ([LIT-143](record/literature.d/LIT-143.md)) → DeepSeek-V3.2's DSA ([LIT-142](record/literature.d/LIT-142.md)) → V4's CSA/HCA. Four
<!-- inactive-ok: SOTA-136 — a Proposed practice, named as part of the residual chain -->
  practices: manifold-constrained hyper-connections ([SOTA-136](record/practices.d/SOTA-136.md), Proposed);
<!-- inactive-ok: SOTA-137 — a Superseded practice, named as the predecessor in the chain -->
  free hyper-connections ([SOTA-137](record/practices.d/SOTA-137.md), Superseded by it — the record's first
  practice filed retired, so the chain reads from the residual forward);
  natively trained sparse attention with a dense warm-up ([SOTA-138](record/practices.d/SOTA-138.md)); staged
  context extension ([SOTA-139](record/practices.d/SOTA-139.md)). The Muon practices gain a third laboratory.
- A DOI remote: `DOI:10.1145/3600006.3613165` written anywhere in the record
  resolves and links, as `ARXIV-` codes already did.

### Changed

- A reading note needs a source, not an arXiv id: at least one of `arxiv:`,
  `doi:`, `url:` ([ADR-009](record/decisions.d/ADR-009.md)). The first note filed under the new rule is a
  blogpost that was never posted to arXiv.
- luria 0.4.2 → 0.8.1 in the workflow, the actions and `pyproject.toml`.
  With it, retirement notes moved out of `status:` and into `status_note:`
  and `superseded_by:` on the eleven documents that carried one; the
  rendered index is unchanged. 0.8.1 reads remote codes in `superseded_by:`
  and directives in frontmatter, so [LIT-031](record/literature.d/LIT-031.md) names both of its successors and
  acknowledges the rejected one at the field.

### Documentation

- [DP-001](docs/design-principles.md#dp-1) is at v2: its applied-here paragraph names the field group rather
  than `requires = ["arxiv"]`.

### Removed

- The registry pipeline: `scripts.registry.cli`, the `Build Registry`
  workflow, the `build-registry` entry point, `data/REGISTRY.md`, and the
  flat registry listing injected into the README. The record generates the
  same corpus as a browsable view with working links and a status column
  that distinguishes records.
- The `web/` frontend and its deploy workflow, replaced by `luria site`.
- The topic-vocabulary specification in the LLM README templates, superseded
  by [ADR-003](record/decisions.d/ADR-003.md) and enforced since.
- The generated project-structure tree.

### Added

- A `Pages` workflow that publishes the record with `luria site`. **Requires
  Settings → Pages → Source set to "GitHub Actions" before the first deploy
  succeeds.**

### Changed

- README rendering moved into the `Docs` workflow's generate job, so exactly
  one job commits generated files and its commit carries a skip marker. Two
  committing workflows had left the branch tip unlinted.
- The luria actions are pinned to a released tag rather than `@main`.
- `data/` is frozen and documented as the import's provenance.

### Added

- A Luria record: `record/practices.d` (one document per recommendation),
  `record/literature.d` (one note per paper), decisions, design principles,
  a changelog and a curation journal. Browsable views are generated into
  `docs/`.
- The topic consolidation specified in 2024 and never applied: seven
  categories for practices, twelve for the reading list, with the
  one-primary-topic rule enforced by `luria lint`.
- arXiv as a configured remote — `ARXIV-1412.6980` written anywhere in the
  record resolves and links.

### Fixed

- Two papers had no arXiv identifier at all (Imagen and DALL-E 2); both now
  carry one, and `requires = ["arxiv"]` makes the omission impossible to
  repeat.
- PaLM appeared twice in the corpus under one identifier with two different
  takeaway lists. The entries are merged.
- The `sota_maybe` hedge on the AdamW paper reached no consumer, because the
  registry builder only ever read `sota`. It is now a `Deferred` practice.

### Changed

- Recommendation and paper statuses are now separate claims, and can
  disagree. Under the old schema both lived on the paper.
- The attic is a status (`Rejected`, or `Superseded` naming its successor)
  rather than a nested mapping nothing could resolve.

### Documentation

- Six decisions recording choices that had been implicit for years: the
  record adoption, the paper/practice split, the topic consolidation, the
  attic, the identifier scheme, and the deferred registry inversion.
