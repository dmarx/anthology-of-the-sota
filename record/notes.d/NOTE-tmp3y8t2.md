---
status: Read
paper: LIT-tmpyiwh4
title: 'FLUX.1 Kontext'
version: 1
date: '2026-09-23'
summary: >-
  The FLUX.1 architecture, and an editing model built by appending context
  latents to the token sequence. It is a system report: human preference
  against other systems, latency, one reconstruction table, and no
  ablations. Main text and appendix A read.
---

# NOTE-tmp3y8t2: FLUX.1 Kontext

## Contribution

The only published description of FLUX.1's architecture. Kontext shows
that one flow model can do text-to-image and in-context editing by
treating context images as extra tokens.

## Key insight

**Editing as in-context generation.** A context image in the same latent
space is appended to the sequence, with a RoPE time offset. The model can
then attend to it at any resolution or aspect ratio, and more than one
image fits without architectural change.

## Key results

- FLUX-VAE reconstruction: PSNR 31.1 and LPIPS 0.332, against SD3's VAE at
  29.6 and 0.452 (Table 1)
- Human preference on KontextBench: best on local editing, text editing
  and character reference, and second on global editing and style
  reference. Fastest latency among the compared APIs (Figure 7)
- The logit-normal shift identity: μ = log α (appendix A.2)

## Limitations

- **No ablations.** The one design comparison, channel-wise concatenation,
  is a sentence with no numbers
- **Human preference against black-box systems** on the authors' own
  benchmark
- **Multi-turn editing still degrades**, as §5 says
