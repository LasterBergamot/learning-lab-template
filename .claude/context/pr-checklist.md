# Before and while creating a PR

Read by the `create-pr` and `triage-dependabot` skills. The skills hold the procedure; this
file holds the values. This is a solo learning repo, so the checklist is light.

## Repo and branches

- **Repo:** `<owner>/<repo>`. **Base branch:** `main`.
- **Branch names:** `lab/<track>-<lab>`, `assess/<subject>-<level>`, `docs/<topic>`, `chore/<topic>`.
- **Protected:** none yet. Direct pushes to `main` are fine for notes; use a PR when a change
  spans several labs or touches `.claude/`, `scripts/` or `.github/`.
- **Merge method:** squash, except template sync PRs (branch `template-sync`): those use a
  merge commit (`gh pr merge --merge`), so the next sync knows what is already in. **Commit subjects:** imperative, sentence case, no prefix
  (e.g. "Add the TLS lab brief").

## Dependabot

- Not enabled. Labs pin their own toolchains (`mise.toml`, lock files) and are not maintained
  products. If it gets enabled later, list the alerts with
  `gh api repos/<owner>/<repo>/dependabot/alerts`.
- **Core dependencies:** none.

## Gates, in order

1. No lab code written by the AI: the diff's non-Markdown files under `labs/` are the learner's.
2. No secrets, private keys or state files in the diff (`*.key`, `*.pem`, `*.tfstate*`, `.env`).
3. `python3 scripts/check_docs.py` passes (links, Status lines, track links).
4. `bash -n scripts/*.sh`, `shellcheck scripts/*.sh` and `jq . .claude/settings.json` succeed.
5. Both platforms covered: any script, setup step or lab instruction in the diff works on
   Omarchy (Linux/Docker) and Windows 11 (Git Bash/Podman). CI runs on both.

## Docs

- Run `update-documentation` (doc map: `.claude/context/docs.md`).
- No docs-touched CI check. A change to a lab's status should also run `roadmap-sync`.
