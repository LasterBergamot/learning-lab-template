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

When the template changes, your repo gets the change as a pull request:

- **Automatically:** `.github/workflows/template-sync.yml` runs `scripts/template-sync.sh` on
  a `template-sync` branch and opens a PR, or updates the one that is already open. It runs:
  - **when the template's main branch changes**, if your repo is in the template's notify list
    (see below);
  - **once a day** otherwise. That run ends after a few seconds without a PR when nothing
    changed. Set the repository variable `TEMPLATE_SYNC_POLL` to `false` to turn it off once
    your repo is notified;
  - **by hand**, from the Actions tab ("Template sync" → Run workflow).
- **By hand**, on either platform:

  ```bash
  git switch -c template-sync
  bash scripts/template-sync.sh
  ```

  Then push the branch and open the PR.

Three rules keep it working:

- **Merge sync PRs with a merge commit, never squash or rebase.** The merge commit is how git
  knows which template changes you already have. After a squash, the next sync tries to apply
  them again.
- **Framework changes go to the template first**, then come back through a sync. A framework
  change made only in your repo can conflict with the next sync.
- **Resolve conflicts locally.** On a conflict the workflow fails. Run the script by hand, fix
  the files it lists, then `git add` and `git commit`.

### How the first sync works

A repo made with "Use this template" shares no history with the template. On the first sync,
the script finds the template commit whose files match your repo's first commit. It records
that commit with `git merge -s ours`, which joins the histories without changing any files.
From then on every sync is a normal merge. You get only what changed in the template, and
your own content stays as it is.

If your repo wasn't made with "Use this template", or its first commit no longer matches, pass
the template commit you started from: `bash scripts/template-sync.sh --baseline <commit>`.

### Getting notified

GitHub can't start a workflow in one repo when another repo changes, unless the changed repo
sends an event. The template's `.github/workflows/template-notify.yml` does that. After every
push to the template's main branch, it sends a `template-updated` event to each repo in the
template's `TEMPLATE_SYNC_REPOS` variable. It uses a `TEMPLATE_DISPATCH_TOKEN` secret that
needs **Contents: read and write** on those repos, so only repos that the token's owner can
write to can be listed: the template owner's own repos. Everyone else gets the daily check.

```bash
# In the template repo, once (the token owner can write to every listed repo):
gh variable set TEMPLATE_SYNC_REPOS -R LasterBergamot/learning-lab-template -b "owner/repo other/repo"
gh secret set TEMPLATE_DISPATCH_TOKEN -R LasterBergamot/learning-lab-template   # paste the token
# In the notified repo, to stop the daily check:
gh variable set TEMPLATE_SYNC_POLL -b false
```

### Tokens and what they allow

The sync workflow uses `GITHUB_TOKEN` by default, which has two limits. It can't push a sync that
changes files under `.github/workflows/`, and the PRs it opens don't start CI. For full syncs,
add a repository secret named `TEMPLATE_SYNC_TOKEN`. Make it a fine-grained personal access
token for your repo, with **Contents**, **Pull requests** and **Workflows** set to read and
write. If you don't add one, enable Settings → Actions → General → "Allow GitHub Actions to
create and approve pull requests", or the workflow can't open the PR.

That setting lets `GITHUB_TOKEN` open PRs and post approving reviews, in every workflow of the
repo. It doesn't give the right to merge. Merging depends on the workflow's own permissions
(`contents: write`) and on branch protection. The sync workflow never approves or merges; you
do. Workflows started from forks get a read-only token, so outside PRs can't use the setting.
A one-repo fine-grained token is narrower, and it avoids the setting altogether.
