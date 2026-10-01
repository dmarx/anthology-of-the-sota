---
status: Active
title: 'Textoshop: Interactions Inspired by Drawing Software to Facilitate Text Editing'
version: 1
tags:
- deployment-and-society
- in-context-learning
date: '2026-10-01'
published: '2024-09-25'
arxiv: '2409.17088'
first_author: 'Masson'
keywords:
- 'writing'
- 'interface-metaphors'
- 'drawing-interaction'
- 'LLM'
- 'AI'
implementations:
- 'm-damien/Textoshop'
summary: >-
  Masson, Kim and Chevalier (2024), ARXIV-2409.17088 (CHI 2025). A
  GPT-4o-backed text editor that replaces typed prompts with drawing-software
  operations, each of which sends an engineered prompt. Resizing a selection
  shortens or expands it, rotating it reorders the words, a colour picker sets
  tone, boolean operations merge passages, and layers hold versions. In a
  within-subject study with 12 participants, against a text editor plus a
  ChatGPT replica on the same model, participants rated themselves more
  successful (4.6 vs 3.9), gave a SUS of 90 against 69, and finished tasks
  55 s faster. The quality of the resulting text was not measured.
---

# LIT-tmp5cmgx: Textoshop: Interactions Inspired by Drawing Software to Facilitate Text Editing

Masson, Kim and Chevalier (2024) — ARXIV-2409.17088. Published at CHI 2025.

## Key takeaways

- **The design maps drawing operations to edits.** Words are treated as
  pixels, sentences as regions and tones as colours. Dragging the edge of a
  selection lengthens or shortens it without changing its meaning. Rotating
  it reorders the words, for example from passive to active voice. The tools
  are a tone brush, a tone eyedropper, a smudge that paraphrases, a
  singular/plural and a tense changer that fix agreement across the text, an
  eraser, a repair tool and a free prompt. The tone picker maps formality,
  sentiment and complexity to RGB, with 11³ = 1331 settings. Unite,
  intersect, subtract and exclude merge two passages by their ideas. Layers
  store edits anchored to the text beneath them.
- **Every operation is a prompt to GPT-4o** with heuristics around it. Each
  is a compiled prompt, not a different model. A resize prompts each sentence
  in parallel, and the original sentence is always kept as the source, so
  expanding again works from the full text and not from the shortened one.
  The one engineering finding is about length. **GPT-4o "was unreliable when
  prompted to resize a text by a certain amount of words"**, so the system
  asks for 8 resizings at slightly different word counts and chooses the
  combination of parts closest to the target. The authors call this "often
  imperfect" and measure nothing about it.
- **The study had 12 participants, a 4-minute cap per task, and one hour
  each.** The design was within-subject and counterbalanced, with four tasks:
  shorten or expand, change tone, organise and integrate fragments, and
  answer customers from an email template. The baseline was a text editor
  with an integrated ChatGPT replica on the same model, and any external
  tool was allowed. Only one participant used one (Grammarly). Results are
  95% bootstrapped CIs on the mean difference:
  - self-rated success +0.71 [0.27, 1.17] (4.6 vs 3.9);
  - SUS +21.25 [12.5, 32.91] (90 vs 69);
  - time −55 s [26 s, 1 min 26 s], largest for shorten/expand (−1 min 29 s)
    and smallest for organising fragments (−13 s).
  In the baseline, participants wrote 2.7 prompts per task, about 269
  characters each. "Writing using a template was easy" is the only statement
  whose CI crosses zero.
- **What is not measured.** The quality of the edited text is not measured,
  and neither is whether it kept the original's meaning. Success is
  self-rated. All participants were familiar with drawing tools, and the
  authors expect the advantage to shrink for people who are not. Use was
  observed for one session only.
- **The qualitative finding is about control.** Participants called the
  chat baseline hard to steer. One said "you had to be very, very specific
  otherwise it would do something completely different". Another said that
  asking for casual text produced text "way too casual". A slider or a drag
  handle gave a graded control that a typed instruction did not. The
  weaknesses were that edits were hard to see before accepting them, that
  the tool forced pointing where writers wanted the keyboard, and that
  layers did not match anyone's mental model.

## Standing in the anthology

Filed under `deployment-and-society` on the precedent of LIT-503, an
assistive-interface paper, and LIT-717, which studies what an AI assistant
does to people writing with it. The fit is loose. This is a lab usability
study of a prototype. It is not an audit of a deployed system, and the
record has no topic for human–AI interaction design. If more papers like
this one are filed, that topic should be added under ADR-059, and this
paper should then take it first.

Against the record's writing-assistant practices it is the kind of evidence
they warn about. SOTA-298, drawn from LIT-487, says to measure a writing
assistant by the outcome it was deployed to improve, and not by proxies.
Textoshop measures neither outcome nor text. It measures perceived success,
usability and time. SOTA-303 asks which phase a time-saving tool speeds up.
Here the phase is revision of text that already exists, and the paper
observes, without measuring, that participants kept reorganising ideas
after their drafts were finished. SOTA-291 asks for a specific affordance to
be evaluated. Each task here isolates one, but only at individual level and
over one session.

The `in-context-learning` tag is for the one portable claim. A fixed model
whose instructions are compiled from graded controls was easier to steer
than the same model under free-text prompting. Separately, a frontier model
could not hit a word count from an instruction and needed sampling plus
selection. Neither claim is ablated, and neither is strong enough to source
a practice.

Unread — no NOTE.
