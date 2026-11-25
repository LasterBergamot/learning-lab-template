# Assessments

Preparation for skill evaluations: your own knowledge, not AI skills. You paste a competency
matrix, for example the Novice / Intermediate / Advanced levels for prompt engineering, and a
Socratic tutor prepares you for the level you choose.

## How it works

1. **Import the matrix:** `import-matrix <subject>` with the pasted matrix. It writes
   `assessments/<subject>/matrix.md` (your paste verbatim, plus a normalised table where every
   competency has an ID such as `PE-07-ADV`). It also writes `readiness.md` and flags duplicate
   rows and blank cells for you to resolve.
2. **Prepare for a level:** `assessment-prep <subject> <level>`. The tutor runs a short
   diagnostic per competency, coaches the gaps with questions, and ends with a mock evaluation.
   Levels are cumulative, so preparing for Advanced checks the Intermediate gaps first.
3. **Track readiness:** each competency moves through *not started → learning → can explain →
   ready*. The date it was last checked is recorded, so old "ready" marks can be re-checked.
4. **See it here:** `roadmap-sync` regenerates the heatmap below from each subject's
   `readiness.md`.

Where a concept differs by vendor (for example, sampling parameters that exist in one LLM API
but not another), the tutor asks you to check the vendor's documentation instead of asserting
an answer.

## Files

| Path | Holds |
|---|---|
| `assessments/<subject>/matrix.md` | The matrix, verbatim, plus the normalised competency × level table |
| `assessments/<subject>/readiness.md` | One row per competency ID: status and date last checked |
| `assessments/<subject>/sessions/YYYY-MM-DD-<level>.md` | Session logs |
| `assessments/<subject>/mock/` | Mock evaluations and their scores |

## Legend

| Mark | Status |
|---|---|
| ⬜ | not started |
| 🟨 | learning |
| 🟦 | can explain |
| 🟩 | ready |

## Heatmaps

<!-- roadmap-sync:start -->
_No subjects yet. Subjects appear here after `import-matrix`._
<!-- roadmap-sync:end -->
