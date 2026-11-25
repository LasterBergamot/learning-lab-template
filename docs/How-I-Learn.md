# How I Learn

This page explains the learning method used in this repo and how the AI fits into it.

## Why Socratic

When someone else's code works, you learn little. You learn when you have to predict, try,
fail and explain. So the AI here acts as a tutor that asks questions. It starts from what you
already know, points out gaps with questions, and lets you write every line yourself.

## The hint ladder

When you're stuck, the tutor climbs one rung at a time and stops as soon as you can continue:

1. **A question**: "What happens to the handshake if the client doesn't trust the issuer?"
2. **A pointer**: "Look at what the server sends in the Certificate message."
3. **A concept**: a short explanation of the idea in prose, without code.
4. **A doc link**: the official documentation section that covers it.

The tutor never goes past rung 4. It may name an API, a flag or a config key, but it does not
write code, config files or commands for the lab.

## Lab milestones

Every lab moves through the same five milestones. Each one is a checkbox in the lab README:

1. **Understand**: you can explain the concept and answer the lab's guiding questions.
2. **Build**: you made it work yourself.
3. **Break**: you broke it on purpose (expired cert, killed broker, partitioned network).
4. **Fix**: you diagnosed the failure and fixed it.
5. **Explain**: you explained it back without notes, as if teaching someone else.

The lab README's `**Status:**` line follows the milestones: `todo` before you start,
`learning` while you work on Understand, `building` during Build, Break and Fix, and `done`
once you have explained it back. You change it yourself, or `session-log` proposes the change.
`roadmap-sync` then colours the graphs in the [root README](../README.md#progress) and the track
READMEs.

## Starting a session

Start Claude Code at the repo root and run `/learn`, or say what you want: "continue rag",
"what should I learn next?", "I want to learn Kafka". It shows the labs in progress (where you
stopped and the next step, from `NOTES.md`), due reviews and what is ready to start. If you
want something new, it asks a few questions about what you want to learn, checks the repo and
the web, and recommends a handful of labs with reasons. Your answers aren't saved; only the lab
you pick is, as its brief. Then it moves into the lab folder and hands over to the skill that
fits: `socratic-tutor` to continue, `plan-lab` for a new lab, `review-quiz` or
`assessment-prep`.

## Before you pick something up

When you start a new track or lab, the AI first runs `prereq-check`. It looks in this repo
(the prerequisites and their Status, your notes, open questions, overdue recall questions) and
online (official docs, well-known roadmaps) for anything you should learn first. It only
proposes. You decide whether to go back or carry on. Every online source it uses goes into the
References section of the relevant README.

## Explain it back

At the end of a session, the tutor asks you to explain the topic in your own words. It then
asks follow-ups wherever your explanation is vague. Your explanation, not the AI's, goes into
the lab's `NOTES.md`.

## Spaced review

Knowledge fades unless it is recalled. `session-log` turns each session into a few recall
questions in [Review Queue](Review-Queue.md). `review-quiz` asks the ones that are due. A question you answer
well gets a longer interval; one you miss comes back sooner.

## Session logs

Each session ends with `session-log`. It records what you covered, your explanation, open
questions, the online sources you used (into the lab's References section), a proposed
`**Status:**` change, and any follow-up issues (as drafts you approve). Lab sessions go in the
lab's `NOTES.md`; assessment sessions go in `assessments/<subject>/sessions/`. Every entry has
the same fields (the lab template's `NOTES.md` shows them), ending with **Where I stopped** and
**Next step**, which is what `/learn` reads to pick up next time. It finishes by
proposing a checkpoint commit and push, so you can continue on any machine. It always
asks first.

## The AI skills and agents

They come from ai-common's `learning` package, deployed by APM to `.claude/skills/` and
`.claude/agents/` (see `CLAUDE.md`). Each one says which model it runs on and with how much
effort, so deep tutoring gets a strong model and bookkeeping gets a cheap, fast one.

| Skill or agent | What it does | Model | Effort |
|---|---|---|---|
| `learn` | The entry point: shows where you stand, recommends what to pick up (repo, a short interview, the web), moves into the lab folder and hands over to the skills below | opus | medium |
| `socratic-tutor` | Runs a learning session: probes what you know, asks, climbs the hint ladder, ends with a summary and open questions | opus | high |
| `prereq-check` | Before you pick up a track or lab: checks this repo's prerequisites and their Status, then online sources for missing ones; proposes, you decide | opus | high |
| `plan-lab` | Turns a topic into a lab brief from the template, with prerequisite links, sources, issue drafts and a node in the track graph | opus | high |
| `assessment-prep` | Prepares you for one level of a skill matrix: diagnostic, targeted coaching, mock evaluation, readiness update | opus | high |
| `import-matrix` | Turns a pasted competency matrix into `matrix.md` (verbatim + normalised table) and `readiness.md`; flags duplicate and blank cells | sonnet | medium |
| `session-log` | Writes the session into notes, adds sources and recall questions, proposes the Status change and a checkpoint commit | sonnet | medium |
| `review-quiz` | Spaced-repetition quiz from the review queue; updates the due dates | sonnet | medium |
| `roadmap-sync` | Reads every lab's `**Status:**` line and updates the Mermaid graph colours and the readiness heatmaps | haiku | medium |
| agent `socratic-reviewer` | Read-only review of your lab code that asks questions about problems instead of giving fixes | sonnet | high |

The generic workflow skills from ai-common are also installed: `new-issue`,
`update-documentation`, `repo-audit`, `create-pr`, `setup-project`, and the
`convention-reviewer` agent.

## Where things go

- Lab briefs and notes: `labs/<track>/<lab>/README.md`, `NOTES.md`, `QUESTIONS.md`.
- Skill evaluations: `assessments/<subject>/` (see [Assessments](Assessments.md)).
- The map of what to learn before what: [the progress overview](../README.md#progress).
