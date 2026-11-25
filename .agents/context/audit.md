# Audit setup

Read by the `repo-audit` skill (from `ai-common`). The skill holds the procedure; this file
holds what the audit covers here.

- **Repo and board:** `<owner>/<repo>`; the board, if any, is in `.agents/context/issues.md`.
- **Marker line:** `_Found in the <Mon YYYY> repository audit._`
- **Not covered here:** the learner's code quality (that's the `socratic-reviewer` agent, on
  request) and the learning content's correctness (that's a tutor session).

## Code explorer

Read: `labs/**` (structure only), `assessments/**`, `.agents/`, `.claude/`, `.gitignore`.
Hunt for:
- labs missing one of the README contract sections (including References and the
  `**Status:**` line), or with no `TEARDOWN.md`
- labs that depend on another lab's running state (shared networks, volumes, clusters)
- committed private keys, `.env` files, Terraform/Pulumi state, kubeconfigs
- compose files without a unique `name:`
- non-portable compose settings (`network_mode: host`, ports below 1024, docker.sock mounts)
- "Tested on" boxes ticked with no session note

## Docs, infra and CI explorer

Read: `docs/`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `.agents/context/`, `scripts/`, `.github/`.
Hunt for:
- broken relative links, or `[[` wiki-style links
- track READMEs not linked from the root `README.md`, or missing from `learning.md`
- stale roadmap-sync blocks (graph classes vs. the labs' Status lines)
- instructions or scripts that cover only one platform (Omarchy or Windows 11 Git Bash)
- overdue `Review-Queue.md` rows
- an `AGENTS.md` over 100 lines

## GitHub state explorer

Collect: issues, relations, board fields, PRs, branch protection.
Check:
- every lab issue has `type`, `track`, `level` and `priority` labels and is on the board
- blocked-by relationships match the prerequisite arrows in the root and track READMEs
- issue state agrees with the lab's Status line, where both exist

## Cheap reproductions

- `python3 scripts/check_docs.py`
- `bash scripts/prereqs.sh --check`
- `git ls-files | grep -E '\.(key|pem|tfstate)$'`
- `docker compose -f labs/<track>/<lab>/compose.yml config` (or `podman compose … config`)
