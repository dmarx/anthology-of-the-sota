---
status: Read
paper: LIT-tmpov7yl
title: 'ViT-VQGAN: where the codebook advice comes from'
version: 1
date: '2026-09-21'
summary: >-
  Read to give `SOTA-306` its origin, and it corrected the practice in three
  places. The advice is not "use small code vectors" but "factorize lookup
  from embedding"; `ℓ₂`-normalization is ablated and is the largest single
  effect in the table; and the dimension-4 row shows 96% codebook usage with
  near-worst FID, so utilization is necessary and not sufficient.
---

# NOTE-tmptxi4l: ViT-VQGAN: where the codebook advice comes from

## Contribution

Diagnosed why VQ codebooks die and fixed it, which is what made large
codebooks usable. Before this, VQGAN's practical setting was 1024 codes plus
top-`k`/top-`p` sampling heuristics at generation time; after it, 8192 codes
sampled at temperature 1.0 with no heuristics at all. The paper's claim is
that those heuristics were compensating for a vocabulary most of whose entries
were dead, and its evidence is that removing the cause removes the need.

Two mechanisms: a factorized code — lookup in a low-dimensional space,
embedding in a high-dimensional one — and `ℓ₂`-normalization of both sides of
the nearest-neighbour comparison.

## Key insight

Codebook lookup and code embedding are different jobs and had been forced to
share a space. Nearest-neighbour search wants low dimension, because in 768 or
256 dimensions distances concentrate and one entry wins nearly every query.
The *embedding* the decoder consumes wants high dimension, because that is
where the capacity is. Project down to look up, project back up to use, and
both get what they need — usage goes from 4% to 95% and FID from 3.68 to 1.50
with throughput unchanged.

## Assumptions

- Codebook entries are initialized from a normal distribution and then
  `ℓ₂`-normalized, so the lookup is cosine similarity on a sphere. The stated
  reason is training stability as well as quality.
- `β = 0.25` for the commitment loss, "in all our experiments" — inherited
  from VQ-VAE and not re-examined here either.
- Loss weights come from a hyperparameter sweep run once and then applied
  unchanged to CelebA-HQ, FFHQ and ImageNet:
  `L = L_VQ + 0.1 L_Adv + 0.1 L_Perceptual + 0.1 L_Logit-laplace + 1.0 L₂`.
- Stage 1 and stage 2 are trained separately; every generation number depends
  on a transformer trained over frozen tokens.

## Key results

- **Table 4, codebook learning** (base encoder/decoder, ViT, StyleGAN
  discriminator; throughput 954–960 across every row, so all of this is free):

  | lookup dim | `ℓ₂` | ℓ1 ↓ | ℓ2 ↓ | IS ↑ | FID ↓ | usage |
  |---|---|---|---|---|---|---|
  | 256 | ✓ | 3.60 | 4.28 | 160.1 | 3.68 | **4%** |
  | 128 | ✓ | 3.41 | 3.93 | 173.9 | 2.77 | 14% |
  | 64 | ✓ | 3.18 | 3.37 | 179.5 | 2.50 | 37% |
  | **16** | ✓ | 3.00 | 2.96 | **191.2** | **1.50** | 95% |
  | 8 | ✓ | 2.98 | 2.92 | 189.5 | 1.52 | 96% |
  | 4 | ✓ | 3.55 | 4.18 | 143.8 | 3.68 | **96%** |
  | 32 | **✗** | 4.13 | 5.41 | 123.6 | **5.44** | **2%** |

- **Removing `ℓ₂`-normalization is worse than any dimension choice.** At
  lookup dimension 32, dropping it takes usage to 2% and FID to 5.44 — below
  the 256-dimensional row. It is not a refinement on top of factorization; it
  is the larger of the two effects.
- **Generation, ImageNet `256×256`:** IS **175.1**, FID **4.17**, against
  vanilla VQGAN's 70.6 and 17.04, with `32×32` codes and a codebook of 8192.
- **Representation:** VIM-L linear-probe accuracy **73.2%** against iGPT-L's
  60.3% at comparable size, and above iGPT-XL, which trained on extra web
  images at larger scale.
- **Architecture:** the ViT encoder-decoder beats the CNN on both quality and
  throughput; the StyleGAN discriminator is more stable and better than the
  PatchGAN VQGAN used.
- **Loss attribution:** logit-laplace loss contributes to codebook usage while
  `ℓ₂` and perceptual losses contribute to FID. Stated as a finding of the
  sweep, without the per-term ablation that would pin it.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Factorizing lookup from embedding raises codebook usage and reconstruction quality | strong | Table 4, six dimensions, monotone until the optimum, throughput controlled |
| C2 | `ℓ₂`-normalizing both sides is necessary, not cosmetic | strong | one row, but a decisive one — usage 2%, FID worse than every alternative |
| C3 | High codebook usage is necessary and not sufficient | strong | the dimension-4 row: 96% usage, 3.68 FID |
| C4 | VQGAN's top-`k`/top-`p` heuristics were compensating for dead codes | moderate | this system needs none of them at 8192 codes, which is consistent with the claim and is not the controlled comparison |
| C5 | ViT beats CNN, StyleGAN beats PatchGAN | moderate | inside one system, alongside the other changes |
| C6 | Logit-laplace drives usage, `ℓ₂` and perceptual drive FID | weak | reported as the outcome of a sweep, no per-term ablation shown |

## Method

Stage 1: ViT encoder to `32×32` positions; linear projection to a
low-dimensional lookup space; `ℓ₂`-normalize encoder outputs and codebook;
nearest neighbour by Euclidean distance on the sphere, which is cosine
similarity; project the matched code back up; ViT decoder. Trained with
logit-laplace, `ℓ₂`, perceptual (VGG) and adversarial (StyleGAN discriminator)
losses. Stage 2: an autoregressive transformer over the rasterized 1024-token
sequence, sampled at temperature 1.0 without top-`k` or top-`p`.

## Concepts

- **dead codes** — entries rarely or never selected. The paper attributes them
  to poor codebook initialization and treats their count as the quantity to
  fix.
- **factorized code** — the pair (low-dimensional lookup vector,
  high-dimensional embedding), connected by a learned projection. The
  distinction descendants blur when they say "low code dimension".
- **codebook usage** — here, the percentage of codes used given a batch of 256
  test images, averaged over the test set. Not the same definition
  [LIT-497](../literature.d/LIT-497.md) uses (a 65,536-sample queue), so the numbers are not
  directly comparable across the two.
- **VIM** — vector-quantized image modeling: the two-stage recipe, tokens then
  transformer, evaluated both generatively and by linear probe.

## Connections

Extends [LIT-496](../literature.d/LIT-496.md) directly, and says so in the title. Extended by
[LIT-497](../literature.d/LIT-497.md), which credits exactly these two design choices and
reimplements them without the factorization. [LIT-494](../literature.d/LIT-494.md) rediscovers
the dimension effect independently, on a different architecture, without
citing either.

## Recommendations

- **R1** — factorize the code: look up in a low-dimensional space, embed in a
  high-dimensional one. *Filed*, as the correction to `SOTA-306`.
- **R2** — `ℓ₂`-normalize encoder outputs and codebook entries, and initialize
  the codebook from a normal distribution. *Filed*, promoted inside `SOTA-306`
  from an unablated design detail to a measured requirement.
- **R3** — measure codebook usage, and do not stop there. *Filed*, with the
  dimension-4 row as the reason.
- **R4** — before reaching for top-`k` or top-`p` to fix generation diversity,
  check how many of your codes are alive. **Not filed as a practice.** The
  claim is well motivated and the paper demonstrates one half of it — a fixed
  codebook needing no heuristics — without running the comparison that would
  separate "heuristics unnecessary" from "heuristics not tried". A candidate
  with a cheap experiment behind it.

## Bearing on the record

Corrects [SOTA-306](../practices.d/SOTA-306.md) in three places, which is the reason this was
worth filing rather than leaving as a citation:

1. The practice said "make the code vectors low-dimensional". The origin says
   factorize — the codebook *embedding* can stay wide, and in this
   implementation it does. Both framings produce the effect; only one names
   the mechanism.
2. The practice carried `ℓ₂`-normalization as "reported as part of the same
   design and not separately ablated in either paper here". That was true of
   the two papers the record then held and is false of this one, where it is
   ablated and is the largest effect in the table.
3. The practice said utilization is "the mechanism". The dimension-4 row says
   it is a necessary condition that can be satisfied while quality collapses.

Nothing here touches [SOTA-305](../practices.d/SOTA-305.md): this paper reports reconstruction
FID at one token count and does not sweep it.

## Limitations

- **The two mechanisms are not separated from each other.** Every normalized
  row is also factorized; the single un-normalized row is at dimension 32.
  There is no un-normalized, un-factorized control, so the interaction is
  unmeasured.
- **One dataset for the ablation.** Table 4 is ImageNet.
- **Usage is defined per batch of 256 test images**, which will read higher
  than a definition over a longer queue. Cross-paper usage comparisons in this
  line are not apples to apples, and none of the papers says so.
- **The heuristics claim is argued, not controlled.** No row shows this
  tokenizer with top-`k` restored, or vanilla VQGAN with a fixed codebook.
- **Loss-term attribution is asserted from a sweep** rather than ablated.
- **`β = 0.25` is inherited unexamined**, at a codebook 16× larger than the
  one it was tuned on.
- **The architecture changes ride along.** ViT-vs-CNN and
  StyleGAN-vs-PatchGAN are in the same table as the codebook rows but not
  crossed with them, so how much of the headline FID is codebook and how much
  is architecture is not recoverable.

## Open questions

- **Does factorization beat a plainly low-dimensional codebook?**
  [LIT-497](../literature.d/LIT-497.md) gets comparable results without it. That comparison —
  factorized versus narrow, same everything else — is not in either paper and
  would tell practitioners which of the two framings to build.
- **Where is the optimum, and what sets it?** 16 here, 8 in LlamaGen, 3 in
  GaussianToken. Three points, no account of what determines it.
- **Do the sampling heuristics really become unnecessary?** One controlled
  table — this tokenizer with and without top-`k`, vanilla VQGAN with and
  without a fixed codebook — would settle `R4` and is cheap.
