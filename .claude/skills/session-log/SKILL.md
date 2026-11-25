---
name: session-log
description: Record a learning or assessment-prep session — write a summary in the learner's own words to the lab's notes (or the assessment's sessions folder), add recall questions to the review queue, record the online sources used, propose a Status change, and propose a checkpoint commit and push so the work can continue on another machine. Use at the end of a tutoring session, or when the learner says "log this", "save the session", "write up what I learned" or "add this to my notes".
model: sonnet
effort: medium
---

You record what happened in a session so the next one can build on it. The project's values
(where the notes go, the log format, the review-queue file and format) live in
**`.claude/context/learning.md`**. Read it first. If it is missing, ask where the notes go, and
offer to create the file from `ai-common`'s `templates/context/learning.md`.

You write Markdown only. Never write lab code, configs or scripts into the notes, even as a
"what I built" snippet. Describe what was built in prose, and link the learner's own files by
path instead.

## 1. Find the target

- A lab session goes to the lab's notes file (from the lab template in the context file).
- An assessment session goes to `<assessments root>/<subject>/sessions/YYYY-MM-DD-<level>.md`.
- If it is unclear which lab or subject the session was about, ask.

## 2. Write the entry

Use the session-log format from the context file. The default, appended under a
`## YYYY-MM-DD: <goal>` heading:

- **Goal**: what this session set out to do
- **What I can now explain**: in the learner's own words, quoted or closely paraphrased from
  the conversation, never your explanation
- **What I built or changed**: in prose, with links to the learner's files
- **Misconceptions fixed**: what was believed, and what is understood now
- **Still unclear / open questions**: also appended to the lab's questions file if it has one
- **Next step**

Show the entry before writing it, and apply the learner's corrections. It is their record.

## 3. Review queue

For each concept that was learned or fixed, add 1–2 recall questions to the review-queue file,
in its format, with `due` set to today + the first interval from the context file. Ask "why"
and "when" questions, not trivia.

## 4. Sources

Every online source used in the session (by you or the learner: docs, specs, RFCs, articles,
videos) goes into the **References** section of the relevant README: the lab README for a lab
session, the track README for a track-wide source, and for an assessment the subject's references
file from the context file (default `<assessments root>/<subject>/README.md`). Add a one-line note on what it covers. Don't duplicate an existing entry.

## 5. Status

If the session reached a milestone, propose the new value for the lab README's Status line
(values and their meaning from the context file; default: understand → `learning`; build,
break and fix → `building`; explained back → `done`). Change it only after the learner agrees,
and mention that `roadmap-sync` refreshes the graphs.

## 6. Follow-ups

- If the session found a missing prerequisite or a new lab idea, draft an issue following
  `.claude/context/issues.md` (if the project uses issues) or a note in the track README, and write
  it only after a go-ahead.
- If a guiding question in the lab README is now answered, tell the learner; don't tick
  milestones yourself.
- If a step was only done on one platform, note it in the lab README's tested-on line and in
  the open questions, so the other platform gets checked too.

## 7. Checkpoint commit

So the work can continue on another machine, end by proposing a checkpoint:

1. Show `git status` for the lab (or assessment) folder and the files changed in this session.
   Point out anything that must not be committed (keys, `.env` files, state files, build
   output). The project's `.gitignore` should already cover them; if it doesn't, say so.
2. Propose the exact commands: `git add <paths>`, a commit with the message
   `<track>/<lab>: <what was done>` (or `assessments/<subject>: <what was done>`), and a push.
3. Run them **only after the learner's explicit go-ahead**. Work-in-progress commits are fine.

## Never

- Never run state-changing git or gh commands without an explicit go-ahead.
