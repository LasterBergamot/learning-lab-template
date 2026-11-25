---
paths:
  - "assessments/**"
---

# Skill assessments

`assessments/<subject>/` prepares the learner for one level of a skill matrix (for example the
prompt-engineering Novice / Intermediate / Advanced levels). It is about the learner's
knowledge, not about AI skills. Start a subject from `assessments/_template/`.

- `matrix.md` has two parts. **Source** holds the learner's paste, **verbatim**: never reword,
  reorder or "fix" it; the repo is public and the learner chose to publish it as-is.
  **Normalised** is a table with one row per competency and stable IDs
  (`<SUBJECT>-<NN>-<LEVEL>`, e.g. `PE-07-ADV`). The `import-matrix` skill builds it and lists
  duplicate rows and blank cells under **Import notes** instead of silently dropping them.
- `readiness.md` has one row per competency ID: status `not-started` ⬜, `learning` 🟨,
  `can-explain` 🟦 or `ready` 🟩, plus the date last checked and a one-line note. Only the
  learner's demonstrated answers move a status up, never the tutor's explanation.
- Levels are cumulative. Preparing for Advanced starts by checking the Intermediate and Novice
  rows it builds on.
- `sessions/YYYY-MM-DD-<level>.md` holds the session logs; `mock/YYYY-MM-DD-<level>.md` holds
  the mock evaluations (questions, the learner's answers, the score per competency).
- `docs/Assessments.md` (the heatmap) is generated from the `readiness.md` files by
  `roadmap-sync`. Don't edit the generated block by hand.
- No code here either: assessment prep is questions, explanations and links.
- Online sources used in prep go into the subject's `README.md` under **References**.
