# Learning setup

Read by the learning skills (`socratic-tutor`, `plan-lab`, `prereq-check`, `assessment-prep`,
`import-matrix`, `session-log`, `review-quiz`, `roadmap-sync`) and the `socratic-reviewer` agent
from `ai-common`. The skills hold the procedure; this file holds this repo's values.

## Paths

- **Graph pages:** the root `README.md` (its **Progress** section: one node per track) and every
  `labs/<track>/README.md` (one node per lab). There are no `docs/Home.md`, `docs/Learning-Paths.md`
  or `docs/Track-*.md` pages any more.
- **Root router:** `README.md` (what, how, prerequisites, Progress, a link to every track README)
- **Track pages:** `labs/<track>/README.md` (why it matters, prerequisites, the lab-level graph, lab table, References)
- **Lab READMEs:** `labs/<track>/<lab>/README.md` (the brief, with a `**Status:**` line and a References section)
- **Lab template:** `labs/_template/` (`README.md`, `NOTES.md`, `QUESTIONS.md`, `TEARDOWN.md`)
- **Assessments root:** `assessments/`, one subject per `assessments/<subject>/`
- **Assessment template:** `assessments/_template/` (`matrix.md`, `readiness.md`, `sessions/`, `mock/`)
- **Docs:** `docs/`, cross-cutting pages only (Setup, Platforms, Isolation, How-I-Learn, Tool-Landscape, Glossary, Review-Queue, Assessments). Plain Markdown in the repo, relative links; there is no wiki.
- **Review queue:** `docs/Review-Queue.md`
- **Assessment heatmap:** `docs/Assessments.md`
- **Glossary:** `docs/Glossary.md`
- **Tool comparison:** `docs/Tool-Landscape.md`

## Tutor

- **Language:** English.
- **Hint ladder:** question → pointer → concept → doc link. Climb one rung at a time; say which
  rung you're on.
- **No-code rule:** never write lab code, config or infrastructure, not even pseudocode or a
  "corrected" copy. Exceptions: naming an API, command or flag; linking official docs; quoting
  and reading the learner's own code to ask about it.
- **Style:** one question at a time; ask for a prediction before a run; end a topic with
  "explain it back"; be explicit about vendor differences and send the learner to vendor docs.
- `CLAUDE.md` holds the same rules, and the output style `.claude/output-styles/socratic.md`
  sets them for every session.

## Sources

- Every online source used for a topic, track or lab (official docs, RFCs, specs, articles,
  roadmaps, videos) is added to the **References** section of the relevant README: the lab's
  `labs/<track>/<lab>/README.md`, or the track's `labs/<track>/README.md` for track-wide ones.
- One line per source: `- [Title](URL) — what it is for`. No duplicates; prefer official sources.
- Assessment sources go into `assessments/<subject>/README.md` under **References** (create the
  section if missing).

## Picking up a track or lab

- Before a track or lab starts, `prereq-check` runs: the prerequisites in this repo (track and
  lab READMEs, the graphs, their Status lines, NOTES, open questions, overdue review questions)
  and online sources for missing prerequisites. It proposes, the learner decides.

## Tracks

| Track id (`track:<id>`) | Name | Track page |
|---|---|---|
| `foundations` | Foundations | `labs/foundations/README.md` |
| `security` | Security | `labs/security/README.md` |
| `identity` | Identity and Access | `labs/identity/README.md` |
| `jvm` | JVM | `labs/jvm/README.md` |
| `testing` | Testing (needs `jvm` and `containers`) | `labs/testing/README.md` |
| `python` | Python | `labs/python/README.md` |
| `concurrency` | Concurrency Models | `labs/concurrency/README.md` |
| `mobile` | Mobile | `labs/mobile/README.md` |
| `containers` | Containers | `labs/containers/README.md` |
| `virtualization` | Virtualization | `labs/virtualization/README.md` |
| `orchestration` | Orchestration | `labs/orchestration/README.md` |
| `observability` | Observability | `labs/observability/README.md` |
| `iac` | Infrastructure as Code | `labs/iac/README.md` |
| `cloud` | Cloud | `labs/cloud/README.md` |
| `eventing` | Eventing and Streaming | `labs/eventing/README.md` |
| `data` | Data | `labs/data/README.md` |
| `distributed` | Distributed Systems | `labs/distributed/README.md` |
| `architecture` | Architecture and Craft | `labs/architecture/README.md` |
| `ai` | AI | `labs/ai/README.md` |
| `classics` | Classics | `labs/classics/README.md` |

A new track gets a folder `labs/<id>/` with a `README.md`, a row here, a node in the root
`README.md` graph and a `track:<id>` label (`.claude/context/issues.md`).

## Levels

- **Lab levels** (`level:*` labels): `level:1-understand`, `level:2-apply`, `level:3-build`,
  `level:4-teach`.
- **Assessment levels:** taken from each subject's `matrix.md` (e.g. Novice, Intermediate,
  Advanced). They are **cumulative**: a level includes everything below it.

## Platforms

- **Linux / Docker:** Omarchy (or another Linux), bash. Its RAM and disk are in
  `docs/Isolation.md` (Resource budget).
- **Windows 11 / Podman:** Git Bash only, no WSL2 distro; the Podman machine uses the Hyper-V
  provider. Heavy labs run on whichever machine has more RAM and disk.
- Every lab README records "Tested on" for both. Portability rules: `docs/Platforms.md` and `.claude/rules/labs.md`.
- Every instruction, script and teardown covers both platforms in the same change.

## Session logs

- **Labs:** append to `labs/<track>/<lab>/NOTES.md` under a dated `## Session YYYY-MM-DD` heading.
- **Assessments:** `assessments/<subject>/sessions/YYYY-MM-DD-<level>.md`.
- Write in the learner's words: what they figured out, what's still open, and the next step.

## Review queue

- File: `docs/Review-Queue.md`. The queue is the table between `<!-- review-queue:start -->`
  and `<!-- review-queue:end -->`, columns `Question | Lab/Competency | Next due | Interval`
  (interval like `3d`). Rows above the markers are examples; never edit them.
- **Intervals:** 1, 3, 7, 14, 30 days. A correct recall moves to the next interval; a miss
  goes back to 1 day. After 30 days a correct recall retires the question.

## Visualization

- **Source of truth:** the `**Status:**` line under the title of every lab README, one of
  `todo`, `learning`, `building`, `done`:
  `**Status:** learning · **Tier:** T1 · **Tested on:** Linux/Docker ✅ Windows/Podman ⬜`.
  Milestones map to it: understand → `learning`; build, break, fix → `building`; explain it
  back → `done`. The learner changes it, or `session-log` proposes the change. It is committed
  like any other edit, so it travels with git. GitHub issues, if any, are extras.
- **Graphs:** Mermaid in the root `README.md` Progress section (one node per track) and in every
  `labs/<track>/README.md` (one node per lab). Arrows mean "learn this first".
- **Status classes:** `classDef todo`, `learning`, `building`, `done`, one `class <ids> <status>`
  line per status. A track node is `done` when all its labs are done, `learning`/`building`
  when any lab has started (the furthest along wins), otherwise `todo`. A planned lab without a
  folder counts as `todo`.
- **Generated blocks** sit between `<!-- roadmap-sync:start -->` and `<!-- roadmap-sync:end -->`.
  Only `roadmap-sync` edits inside them, and only the `class` lines.
- **Readiness heatmap** in `docs/Assessments.md`: statuses `not-started` ⬜, `learning` 🟨,
  `can-explain` 🟦, `ready` 🟩.
- GitHub's Mermaid renderer ignores `click` links, so a table under each graph links the lab
  READMEs. Keep each graph under about 40 nodes.
- `scripts/check_docs.py` (CI) fails on a lab README without a valid Status line.
