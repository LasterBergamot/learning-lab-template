# Doc map

Read by the `update-documentation` skill (from `ai-common`). The skill holds the procedure;
this file says which docs this repo has and the steps specific to it.

## Where the docs are

- Everything is plain Markdown in the repo, read on GitHub or locally. There is **no wiki**.
  Links are relative Markdown links (`[Setup](docs/Setup.md)`); `[[...]]` links are not
  allowed. Mermaid diagrams render on GitHub.
- `README.md` (root) is the router for people: what this is, how it works, prerequisites
  (`scripts/prereqs.sh`), the track-level progress graph (Progress section), a link to every track README, and
  working across machines. Keep it accurate when any of those change.
- `CLAUDE.md` is the router for Claude Code (under 100 lines). Context files:
  `.claude/context/`. Also: `.claude/rules/`, `.claude/output-styles/socratic.md`,
  `.claude/settings.json`.
- `labs/<track>/README.md` (track pages) and `labs/<track>/<lab>/README.md` (lab briefs), each
  with a References section. `assessments/**`.

## Pages

| File | Covers |
|------|--------|
| `README.md` | Router: what, how, prerequisites, progress overview graph, track links, machines |
| `CLAUDE.md` | AI rules and router for Claude Code |
| `docs/Setup.md` | Machine setup runbook for Linux with Docker (Omarchy or any distro), built on `scripts/prereqs.sh`. The `setup-project` skill follows it |
| `docs/Template.md` | The template this repo comes from (`.github/template-source`), creating a repo from it, and the sync |
| `docs/Platforms.md` | The supported platform (Linux with Docker) and the portability rules |
| `docs/Isolation.md` | Isolation tiers T0–T5, resource and disk budget, teardown rules |
| `docs/How-I-Learn.md` | The Socratic method used here, the skills, spaced review |
| `docs/Tool-Landscape.md` | Overlapping tools compared |
| `docs/Glossary.md` | Terms, in the learner's words |
| `docs/Review-Queue.md` | Spaced-repetition recall questions and their due dates |
| `docs/Assessments.md` | Readiness heatmap per assessment subject (generated block) |
| `labs/<id>/README.md` | One per track: why, prerequisites, lab graph, lab table, References |

## Steps specific to this repo

- Run `python3 scripts/check_docs.py` after doc changes: relative links resolve, lab Status
  lines are valid, every track README is linked from the root README, no `[[` links. CI runs it
  on Linux (`.github/workflows/check.yml`).
- After a lab or assessment status changes, run `roadmap-sync`. It owns the blocks between
  `<!-- roadmap-sync:start -->` and `<!-- roadmap-sync:end -->`; never edit them by hand.
- A new track: a `labs/<id>/README.md`, a node and a link in the root `README.md`, a row in
  `.claude/context/learning.md` (Tracks) and a `track:<id>` label.
- Online sources go into the References section of the relevant README (see `learning.md`).
- A new tool comparison goes in `docs/Tool-Landscape.md`, not in a lab brief.
- Instructions target Linux with Docker and bash only; don't add Windows, Git Bash or Podman variants.
