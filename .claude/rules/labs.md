---
paths:
  - "labs/**"
---

# Labs

`CLAUDE.md` holds the rules; this file repeats the lab-specific ones. A lab is a
self-contained folder `labs/<track>/<lab>/`, started from `labs/_template/`. The learner writes
everything in it except the Markdown. The AI never writes lab code.

## What the AI may touch here

- Only `*.md`: `README.md` (the brief), `NOTES.md`, `QUESTIONS.md`, `TEARDOWN.md`.
- Everything else is the learner's: code, Dockerfiles/Containerfiles, compose files, manifests,
  IaC, scripts, configs, keys and certificates. `.claude/settings.json` denies Edit on those
  file types under `labs/`. Don't work around the rule with Bash redirection, `sed -i`, `tee`
  or a heredoc either: the rule is about who writes the code, not about which tool does it.
- Reading the learner's files to ask questions about them is fine.

## Lab README contract

Every lab README (`labs/_template/README.md`) has these sections:
- Goal, and why it lasts
- Prerequisites, as links to other labs and their issues
- Key concepts and 5–10 guiding questions
- Milestones: understand → build → break → fix → explain
- Isolation tier (T0–T5, `docs/Isolation.md`), platforms tested, RAM and disk cost
- Teardown (`TEARDOWN.md`)
- **References**: every online source used for this lab, one line each
  (`- [Title](URL) — what it is for`), official sources first

Right under the title, every lab README has the progress line:
`**Status:** <todo|learning|building|done> · **Tier:** T<n> · **Tested on:** Linux/Docker ⬜`.
`scripts/check_docs.py` (CI) fails on a missing or invalid Status. `roadmap-sync` colours the
graphs in `labs/<track>/README.md` and the root `README.md` from it.

## Sources

Every online source used while planning, tutoring or checking prerequisites for a lab goes into
that lab's References section; track-wide sources go into `labs/<track>/README.md`.

## Isolation

- No lab depends on another lab's running state. Shared infrastructure is copied into the lab,
  not linked.
- A compose file has a unique top-level `name:` (`<track>-<lab>`), so its networks and volumes
  are scoped to the lab.
- One kind cluster per lab, named after it, deleted in the teardown.
- Cloud labs use emulators first (LocalStack, Azurite, GCP emulators). For real accounts: a
  budget alert, a per-lab project or account, and `destroy` in the teardown. Never commit
  credentials or state files (`.gitignore` covers `*.tfstate*`, `.terraform/`, keys).
- Check `docker system df` before a heavy lab. Heavy labs (OpenShift Local, Spinnaker, Db2, the
  Android emulator) need enough RAM and disk in the VM (`docs/Isolation.md`, Resource budget).

## Platform: Linux with Docker

The learner's files must work on any Linux machine with Docker (Omarchy in a VM, any other
distro). When reviewing or briefing, point out anything that won't:
- Compose spec only, run with `docker compose`.
- No `network_mode: host`, and no host ports below 1024.
- Bind mounts with relative paths; no absolute host paths, no SELinux `:Z` assumptions.
- LF line endings (`.gitattributes`). A CRLF script fails inside a container.
- Kubernetes via kind.
- The README's "Tested on" box is ticked only after a real run.
