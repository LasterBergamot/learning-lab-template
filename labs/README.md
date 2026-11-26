# Labs

One folder per track, one folder per lab inside it: `labs/<track>/<lab>/`, for example
`labs/security/tls-pki/` or `labs/testing/tdd-katas/`. Each track folder has a `README.md` with
the track's planned labs, a progress graph and its references. The track list and the overview
graph are in the [root README](../README.md#tracks).

```
labs/
├── _template/            copied for every new lab
├── <track>/
│   ├── README.md         the track: why it lasts, prerequisites, graph, lab table, references
│   └── <lab>/
│       ├── README.md     the brief: Status line, goal, prerequisites, questions, milestones,
│       │                 tier, platforms, teardown, references
│       ├── NOTES.md      your notes and the dated session summaries
│       ├── QUESTIONS.md  open questions, with your guess before you look anything up
│       ├── TEARDOWN.md   how to remove everything the lab created
│       └── …             your code, compose files, configs: written by you, not by the AI
```

## Starting a lab

Ask Claude Code for `plan-lab <track>/<lab>`. It runs `prereq-check` first, then copies
[`_template/`](_template/README.md), writes the brief, links the prerequisites, adds the
sources it used to References, and fills in the lab's row in the track README. Or copy the
template by hand.

## The Status line

Every lab README has this line right under its title:

```markdown
**Status:** learning · **Tier:** T1 · **Tested on:** Linux/Docker ✅
```

`todo` → `learning` → `building` → `done`, following the milestones (see
[How I Learn](../docs/How-I-Learn.md#lab-milestones)). It is a committed line, so progress
moves with git to every machine. `roadmap-sync` reads all Status lines and colours the graphs.
CI fails on a missing or invalid one.

## Rules

- A lab never depends on another lab's running state. See [Isolation](../docs/Isolation.md).
- The compose project `name:` and the kind cluster name are `<track>-<lab>`.
- Private keys, `.env` files and IaC state are git-ignored. Keep it that way.
- The lab works on Linux with Docker (Omarchy or any other distro). See
  [Platforms](../docs/Platforms.md).
- Every online source you or the AI used goes into the lab's References section.
- Commit at the end of each session, so you can continue on any machine.
