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

Syncing is manual: you decide when to bring template changes in. One script does every step,
the same on Linux and in Git Bash on Windows:

```bash
bash scripts/template-sync.sh --check   # only list what's new in the template
bash scripts/template-sync.sh           # sync through a PR
```

The sync goes step by step. It prints each command before running it, and asks before merging
and before merging the PR (`--yes` skips the questions):

1. Checks that the working tree is clean.
2. Fetches the template named in `.github/template-source`, adding a `template` remote if
   needed.
3. Switches to `main` and pulls.
4. Lists the template commits this repo doesn't have yet, or says it's up to date and stops.
5. Creates a `template-sync` branch and merges them. The first time, it records the baseline
   first (see below).
6. Pushes the branch and opens a PR with `gh`.
7. Waits for CI and merges the PR **with a merge commit**, then switches back to an updated
   `main`.

Other modes:

- `--continue`: after a conflict. The script stops and lists the files. Fix them, run `git add`
  on each, then `git commit`, then `bash scripts/template-sync.sh --continue`. `git merge --abort`
  undoes the whole sync instead.
- `--local`: merge straight into `main` and push, without a PR.
- Without `gh`, or with an origin that isn't on GitHub, it pushes the branch and tells you how
  to merge it yourself.

To hear about changes without checking, watch the template repo on GitHub (Watch → Custom).

Two rules keep it working:

- **Merge sync PRs with a merge commit, never squash or rebase.** The merge commit is how git
  knows which template changes you already have. After a squash, the next sync tries to apply
  them again. The script merges this way for you.
- **Framework changes go to the template first**, then come back through a sync. A framework
  change made only in your repo can conflict with the next sync.

### How the first sync works

A repo made with "Use this template" shares no history with the template. On the first sync,
the script finds the template commit whose files match your repo's first commit. It records
that commit with `git merge -s ours`, which joins the histories without changing any files.
From then on every sync is a normal merge. You get only what changed in the template, and
your own content stays as it is.

If your repo wasn't made with "Use this template", or its first commit no longer matches, name
the template commit you started from. Either add a `baseline: <commit>` line to
`.github/template-source`, or run `bash scripts/template-sync.sh --baseline <commit>` once.
