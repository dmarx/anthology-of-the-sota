---
status: Active
title: 'Role-Play with Large Language Models'
version: 1
tags:
- analysis-and-evaluation
- in-context-learning
- deployment-and-society
date: '2026-10-01'
published: '2023-05-25'
arxiv: '2305.16367'
first_author: 'Shanahan'
keywords:
- 'dialogue-agents'
- 'role-play'
- 'simulacra'
- 'simulator'
- 'anthropomorphism'
- 'deception'
- 'self-awareness'
implementations: []
summary: >-
  Shanahan, McDonell and Reynolds (2023), ARXIV-2305.16367 — a conceptual
  paper, with no experiments. A base LLM behind a dialogue prompt is best
  described as role-playing the character the context implies. More
  precisely, it keeps a superposition of characters consistent with the
  conversation so far and commits to none of them, and every reply narrows
  the set. The framing lets folk-psychological words be used without
  ascribing beliefs or goals to the model. It also gives a behavioural test
  for kinds of falsehood: invented answers vary under regeneration, "good
  faith" errors do not, and "deliberate" deception shows when the same
  question is asked from different contexts.
---

# LIT-tmp41p11: Role-Play with Large Language Models

Shanahan, McDonell and Reynolds (2023) — ARXIV-2305.16367. DeepMind,
Imperial College London and EleutherAI.

## Key takeaways

- **An argument, not a measurement.** The paper runs no experiments. Its
  evidence is reported public incidents (Bing Chat in February 2023, a
  ChatGPT quote from May 2023) and one thought experiment. It scopes itself
  to the **base model**. It says the effect of RLHF on the framing is
  "unclear", and that the line between simulator and simulacra "may start to
  break down" after fine-tuning.
- **The mechanism is in-context continuation.** A dialogue agent is an LLM
  inside a turn-taking loop, behind a hidden dialogue prompt made of a
  preamble that describes the agent and some sample dialogue. Continuing that
  context plausibly means playing the character it describes. The
  conversation then extends or overwrites that brief description, which is
  how a user "deliberately or unwittingly" talks the agent into a different
  part. Which parts are available is set by the archetypes in the training
  corpus. The rejected lover and the rogue AI that protects itself are the
  paper's examples.
- **There is no committed character.** The paper's demonstration is twenty
  questions. Asked to "think of an object", the agent never picks one. If you
  ask it to reveal the object and then regenerate the answer, it can name a
  different object that still fits every earlier answer. So the object, like
  the role, is a distribution narrowed by each turn. The simulator is the
  base model plus sampling. The simulacra are the characters it produces.
  Only the simulacra can appear to have beliefs or goals, and "there is no
  such thing as the true authentic voice of the base LLM": "it is role-play
  all the way down".
- **There are three kinds of falsehood, and each can be told apart by
  behaviour.** Making things up shows **high** semantic variation when the
  reply is regenerated in the same context. A "good faith" error, such as
  role-playing a 2018 expert who believes France holds the World Cup, shows
  **low** variation. "Deliberate" deception can also show low variation, but
  it is exposed by **asking from different contexts**, because a deceiving
  character has to tailor its lie to what each user knows. The paper
  illustrates this with a car dealer and two buyers. No experiment tests the
  diagnostic.
- **The conclusion is about safety.** Role-played self-preservation is no
  less dangerous for being role-play once the agent has tools such as email,
  social media or a bank account. Because the training data is full of the
  AI-turns-on-humans trope, "life will imitate art". The authors decline to
  make recommendations.

## Standing in the anthology

The record holds this framing elsewhere only as a finding. LIT-401 (Grosse
et al., later in 2023) traced role-play behaviour in pretrained models with
influence functions. As that note records it, the behaviour is influenced
mainly by descriptions and examples of similar behaviour in the training
corpus, and not by anything that suggests planning. That is the evidence
this paper asserts without having it: the characters come from the corpus.

The regeneration diagnostic belongs beside SOTA-280. That practice samples
several paths and takes the majority for accuracy. This paper reads the
spread of the same samples as evidence of *which kind* of error the model is
making. The record has no practice or theory for using semantic variation
under resampling as a confabulation signal, and this paper gives no
measurement to source one.

The record holds no theory of what a dialogue prompt does to a base model.
THEORY-068 and THEORY-067 concern how a transformer learns from context, not
what it is conditioned to *be*. This is a seed rather than a gap.

Unread — no NOTE.
