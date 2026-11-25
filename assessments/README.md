# Skill assessments

Preparation for skill evaluations: **your** knowledge, measured against a competency matrix
with levels (for example prompt engineering: Novice, Intermediate, Advanced). A Socratic tutor
prepares you for one level at a time. The AI writes no code here either.

## Layout

```
assessments/<subject>/          e.g. assessments/prompt-engineering/
├── matrix.md                   your paste, verbatim, plus a normalised table with competency IDs
├── readiness.md                one row per competency: status, last checked, note
├── sessions/YYYY-MM-DD-<level>.md
└── mock/YYYY-MM-DD-<level>.md
```

Start a subject from `assessments/_template/`.

## How it works

1. **Import:** run `import-matrix <subject>` and paste the matrix. The paste is stored
   verbatim. Then it is normalised into one row per competency per level, with IDs such as
   `PE-07-ADV`. Duplicate rows and blank cells are listed under Import notes, not dropped.
2. **Prepare:** run `assessment-prep <subject> <level>`. It starts with a short diagnostic per
   competency, coaches the gaps with questions (the hint ladder: question → pointer → concept →
   doc link), and moves a status up only when you demonstrate it. Levels are cumulative, so the
   lower levels are checked first.
3. **Mock:** the same skill runs a mock evaluation and scores each competency in `mock/`.
4. **Review:** recall questions go into [the review queue](../docs/Review-Queue.md) (`review-quiz`), and
   `roadmap-sync` updates the readiness heatmap in [docs/Assessments.md](../docs/Assessments.md).

**Statuses:** `not-started` ⬜ · `learning` 🟨 · `can-explain` 🟦 · `ready` 🟩

No subject has been imported yet.
