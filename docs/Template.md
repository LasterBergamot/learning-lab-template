# Template

Every learning-lab repo is created from
[learning-lab-template](https://github.com/LasterBergamot/learning-lab-template), and
`.github/template-source` records which template it came from. The template holds the
framework: `AGENTS.md`, `docs/`, `scripts/`, `.agents/`, `.claude/`, `.github/`, and the
`_template` folders and track READMEs. Your repo holds your progress: labs, notes, Status
lines, the review queue and assessments.

## Create your repo

1. Click **Use this template** on GitHub, or run:

   ```bash
   gh repo create <your-repo> --template LasterBergamot/learning-lab-template --public --clone
   ```

   `--private` works too. You get one fresh commit with none of the template's history.
2. Keep `.github/template-source` as it is. It is how the sync finds the template.
3. Replace the placeholders: `grep -rn '<owner>/<repo>' .agents docs` finds them. Set `author`
   in `apm.yml`, and add your name to `LICENSE` for your own content.
4. Follow [Setup](Setup.md). Steps 9 and 10 (dev-config and ai-common's guard
   hooks) are optional.

## Stay in sync

Syncing is manual: you decide when to bring template changes in.

**See what's new:**

```bash
git fetch template && git log --oneline HEAD..template/main
```

The first time, add the remote: `git remote add template "$(grep -v '^#' .github/template-source)"`.
After that, `scripts/template-sync.sh` keeps it pointed at `.github/template-source`. To hear
about changes without checking, watch the template repo on GitHub (Watch → Custom).

**Sync**, the same on Linux and in Git Bash on Windows:

```bash
git switch main && git pull
git switch -c template-sync
bash scripts/template-sync.sh     # "Up to date" means there is nothing to do
git push -u origin template-sync
gh pr create --title "Sync with the template" --fill
gh pr merge --merge --delete-branch   # a merge commit: see the rules below
```

You can also merge the branch into main locally and push. A PR is optional; it gives you CI on
both platforms and a diff to read.

Three rules keep it working:

- **Merge sync PRs with a merge commit, never squash or rebase.** The merge commit is how git
  knows which template changes you already have. After a squash, the next sync tries to apply
  them again.
- **Framework changes go to the template first**, then come back through a sync. A framework
  change made only in your repo can conflict with the next sync.
- **Conflicts** stop the script with a list of files. Fix them, run `git add` on each, then
  `git commit`. `git merge --abort` undoes the whole sync.

### How the first sync works

A repo made with "Use this template" shares no history with the template. On the first sync,
the script finds the template commit whose files match your repo's first commit. It records
that commit with `git merge -s ours`, which joins the histories without changing any files.
From then on every sync is a normal merge. You get only what changed in the template, and
your own content stays as it is.

If your repo wasn't made with "Use this template", or its first commit no longer matches, pass
the template commit you started from: `bash scripts/template-sync.sh --baseline <commit>`.
