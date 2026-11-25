---
name: import-matrix
description: Import a pasted skill/competency matrix (levels such as Novice / Intermediate / Advanced) into the assessments folder — keep the paste verbatim, build a normalised competency × level table with stable IDs, flag duplicate rows and blank cells, and create the readiness tracker. Use when the learner pastes a skill matrix, competency levels, an assessment rubric or evaluation criteria, or asks to add or update an assessment subject.
model: sonnet
effort: medium
---

Context files: `<context>` below means `.agents/context/` in the project, or `.claude/context/` if that folder doesn't exist.

You turn a pasted matrix into files that `assessment-prep` and `roadmap-sync` can read. The
project's values (assessments root, assessment template, readiness statuses) live in
**`<context>/learning.md`**. Read it first. If it is missing, ask for the assessments
folder, and offer to create the file from `ai-common`'s `templates/context/learning.md`.

You write Markdown only. You don't teach here; hand over to `assessment-prep` for that.

## 1. Subject and levels

- Ask for the subject's slug (kebab-case, for example `prompt-engineering`) and a 2–4 letter
  ID prefix (for example `PE`), unless the learner already gave them.
- Read the level names from the paste's header row (for example Novice, Intermediate,
  Advanced). Give each one a 3-letter code (`NOV`, `INT`, `ADV`). Confirm the order with the
  learner; levels are cumulative from left to right.

## 2. Parse

- Pasted matrices are messy: cells run over several lines, columns are tab-separated or
  misaligned, and a row's cells may be split. Rebuild the rows as **competency rows**: each row
  is one topic (for example "system vs user prompts"), and each column is a level's statement
  for that topic.
- Split a cell that holds several distinct statements into separate statements under the same
  row and level.
- Don't reword the statements. Fix only whitespace and obvious line-break splits.

## 3. Flag problems, don't fix them silently

List these for the learner before writing anything:
- **duplicate rows** (the same statements appearing twice), with a proposal to keep one
- **blank cells** (a level with no statement for a row): keep them blank and mark them `—`,
  and ask whether the level is meant to have nothing there
- **ambiguous splits**, where you are unsure which row or level a statement belongs to

Apply the learner's decisions.

## 4. Write the files

From the assessment template in the context file, in `<assessments root>/<subject>/`:

- `matrix.md`:
  1. a `## Source (verbatim)` section with the paste exactly as given, in a fenced `text` block
  2. a `## Competencies` table with the columns: ID, Topic, Level, Statement
  3. a `## Notes` section with the decisions from step 3

  IDs are `<PREFIX>-<NN>-<LVL>`: `NN` is the two-digit row number, `LVL` the level code. A row
  with several statements in one level adds a letter (`PE-03-INT-a`, `PE-03-INT-b`).
- `readiness.md`: one row per ID, with the columns ID, Level, Status (`not-started`), Last
  checked (empty) and Notes. Put it inside the generated markers from the context file if the
  template has them.
- `sessions/` and `mock/` folders, each with a `.gitkeep` or a short `README.md` if the
  template has one.

When you re-import an existing subject, keep the IDs of unchanged statements and keep their
readiness rows. Show which IDs are new, changed or removed before writing.

## 5. Report

Report the subject, the levels, the number of competencies per level, the flagged problems and
their resolution, and the next step: `assessment-prep <subject> <level>`. If the project wants
issues per subject (see `<context>/issues.md`), draft them, and create them only after a
go-ahead.
