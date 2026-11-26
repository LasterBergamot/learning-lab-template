#!/usr/bin/env bash
# Bring the latest template changes into this repo, step by step. Run it from anywhere in the repo:
#
#   bash scripts/template-sync.sh             check, merge on a template-sync branch, push, open a PR
#   bash scripts/template-sync.sh --check     only list the template commits this repo doesn't have
#   bash scripts/template-sync.sh --continue  after fixing conflicts and committing: push, open a PR
#   bash scripts/template-sync.sh --local     merge straight into main and push, without a PR
#
# Options: --yes (don't ask before each step), --baseline <commit> (see below).
#
# Every step says what it does and prints each command before running it. It needs git; gh is
# needed only to open and merge the PR.
#
# The template's URL is the first non-comment line of .github/template-source. A repo made with
# "Use this template" shares no history with the template, so the first sync records a baseline:
# the template commit this repo started from, merged with "-s ours" (history only, no file
# changes). The script finds it by matching this repo's first commit against the template's
# commits. When that doesn't work, a "baseline: <commit>" line in .github/template-source or
# --baseline <commit> names it. After that every sync is a normal merge, so only what changed in
# the template comes in. Sync PRs are merged with a merge commit, never squashed: the merge commit
# is how the next sync knows what is already here.
set -euo pipefail

mode='pr'
yes=0
baseline_arg=''
while [ $# -gt 0 ]; do
  case "$1" in
    --check) mode='check'; shift ;;
    --continue) mode='continue'; shift ;;
    --local) mode='local'; shift ;;
    --yes|-y) yes=1; shift ;;
    --baseline) baseline_arg=${2:?--baseline needs a commit}; shift 2 ;;
    -h|--help) sed -n '2,21p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Unknown option: $1 (see --help)" >&2; exit 2 ;;
  esac
done

cd "$(git rev-parse --show-toplevel)"

n=0
step() { n=$((n + 1)); printf '\n==> %d. %s\n' "$n" "$*"; }
run() { printf '  + %s\n' "$*"; "$@"; }
die() { printf '\n%s\n' "$*" >&2; exit 1; }
confirm() {
  [ "$yes" = 1 ] && return 0
  local answer=''
  [ -t 0 ] || return 1
  read -r -p "  $1 [y/N] " answer
  case "$answer" in y|Y|yes) return 0 ;; *) return 1 ;; esac
}
short() { git rev-parse --short "$1"; }

src_file=.github/template-source
[ -f "$src_file" ] || die "No $src_file: this repo doesn't name its template."
url=$(grep -v -e '^#' -e '^[[:space:]]*$' -e '^baseline:' "$src_file" | head -n 1 | tr -d '[:space:]')
[ -n "$url" ] || die "$src_file has no URL."
baseline_file=$(sed -n 's/^baseline:[[:space:]]*\([0-9a-fA-F]\{7,40\}\).*/\1/p' "$src_file" | head -n 1)

remote=template
branch=template-sync
main=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##' || true)
main=${main:-main}
upstream="$remote/main"
has_origin=0
git remote get-url origin >/dev/null 2>&1 && has_origin=1

merge_in_progress() { git rev-parse -q --verify MERGE_HEAD >/dev/null; }

publish() {
  if [ "$mode" = local ]; then
    step "Push $main"
    [ "$has_origin" = 1 ] || { echo "  No origin remote: nothing to push."; return 0; }
    if confirm "Push $main to origin?"; then run git push origin "$main"
    else echo "  Not pushed. Later: git push origin $main"; fi
    return 0
  fi

  step "Push the $branch branch"
  [ "$has_origin" = 1 ] || die "No origin remote. Merge locally instead: git switch $main && git merge --no-ff $branch"
  run git push --force-with-lease -u origin "$branch"

  local origin_url
  origin_url=$(git remote get-url origin)
  if ! command -v gh >/dev/null 2>&1 || ! printf '%s' "$origin_url" | grep -q 'github\.com'; then
    step "Open the PR yourself"
    echo "  gh isn't available or origin isn't on GitHub. Open a PR from $branch into $main and"
    echo "  merge it with a merge commit (not squash), or merge locally:"
    echo "    git switch $main && git merge --no-ff $branch && git push origin $main"
    return 0
  fi

  step "Open the PR"
  if gh pr view "$branch" --json state --jq .state 2>/dev/null | grep -q OPEN; then
    echo "  A PR for $branch is already open: $(gh pr view "$branch" --json url --jq .url)"
  else
    run gh pr create --base "$main" --head "$branch" --title "Sync with the template" \
      --body "Template changes up to $(short "$upstream"), from scripts/template-sync.sh. Merge with a **merge commit**, not a squash, so the next sync starts from here."
  fi

  step "Wait for CI, then merge with a merge commit"
  if ! confirm "Wait for the checks and merge now?"; then
    echo "  Later: gh pr checks $branch --watch && gh pr merge $branch --merge --delete-branch"
    return 0
  fi
  sleep 10   # give the checks a moment to register
  if ! run gh pr checks "$branch" --watch; then
    confirm "The checks failed or none ran. Merge anyway?" || die "Not merged. Fix the PR, then: gh pr merge $branch --merge --delete-branch"
  fi
  run gh pr merge "$branch" --merge --delete-branch
  run git switch "$main"
  run git pull --ff-only origin "$main"
  git branch -D "$branch" >/dev/null 2>&1 || true
  echo
  echo "Done: $main includes the template up to $(short "$upstream")."
}

if [ "$mode" = continue ]; then
  [ "$(git rev-parse --abbrev-ref HEAD)" = "$branch" ] || die "--continue runs on the $branch branch. Switch to it first."
  if merge_in_progress || [ -n "$(git ls-files -u)" ]; then
    die "The merge isn't finished. Fix the files, run 'git add' on each, then 'git commit', then run --continue again."
  fi
  git rev-parse -q --verify "$upstream" >/dev/null || run git fetch --quiet "$remote" main
  publish
  exit 0
fi

if [ "$mode" != check ]; then
  step "Check that the working tree is clean"
  merge_in_progress && die "A merge is in progress. Finish it (git add, git commit) and run --continue, or undo it: git merge --abort"
  if ! git diff --quiet || ! git diff --cached --quiet; then
    die "Uncommitted changes: commit or stash them first."
  fi
  echo "  Clean."
fi

step "Fetch the template ($url)"
if git remote get-url "$remote" >/dev/null 2>&1; then
  git remote set-url "$remote" "$url"
else
  run git remote add "$remote" "$url"
fi
run git fetch --quiet "$remote" main

if [ "$mode" != check ]; then
  step "Update $main"
  [ "$(git rev-parse --abbrev-ref HEAD)" = "$main" ] || run git switch "$main"
  [ "$has_origin" = 1 ] && run git pull --quiet --ff-only origin "$main"
fi

step "Compare with the template"
baseline=''
if git merge-base HEAD "$upstream" >/dev/null 2>&1; then
  if git merge-base --is-ancestor "$upstream" HEAD; then
    echo "  Up to date with the template ($(short "$upstream")). Nothing to do."
    exit 0
  fi
  echo "  Template commits not here yet:"
  git log --oneline "HEAD..$upstream" | sed 's/^/    /'
else
  baseline=${baseline_arg:-$baseline_file}
  if [ -z "$baseline" ]; then
    # "Use this template" copies the template's files into a fresh first commit, so the trees match.
    root=$(git rev-list --max-parents=0 HEAD | tail -n 1)
    root_tree=$(git rev-parse "$root^{tree}")
    baseline=$(git log --format='%H %T' "$upstream" | awk -v t="$root_tree" '$2 == t { print $1; exit }')
  fi
  [ -n "$baseline" ] || die "This repo shares no history with the template, and no template commit matches its
first commit. Find the template commit you started from, then run:
  bash scripts/template-sync.sh --baseline <commit>
or add a line 'baseline: <commit>' to $src_file."
  git merge-base --is-ancestor "$baseline" "$upstream" || die "$baseline is not on the template's main branch."
  echo "  First sync. Baseline (the template commit this repo started from): $(short "$baseline")"
  if [ "$(git rev-parse "$baseline")" = "$(git rev-parse "$upstream")" ]; then
    echo "  No template changes since then."
  else
    echo "  Template commits since then:"
    git log --oneline "$baseline..$upstream" | sed 's/^/    /'
  fi
fi
[ "$mode" = check ] && exit 0

confirm "Merge these into this repo?" || die "Stopped. Nothing changed."

if [ "$mode" = pr ]; then
  step "Create the $branch branch"
  git rev-parse -q --verify "refs/heads/$branch" >/dev/null &&
    die "A local $branch branch already exists. Finish it with --continue, or delete it: git branch -D $branch"
  run git switch -c "$branch"
fi

if [ -n "$baseline" ]; then
  step "Record the baseline (history only, no file changes)"
  run git merge --quiet -s ours --allow-unrelated-histories --no-edit \
    -m "Record the template baseline ($(short "$baseline"))" "$baseline"
fi

if ! git merge-base --is-ancestor "$upstream" HEAD; then
  step "Merge the template changes"
  if ! run git merge --no-ff --no-edit -m "Merge template updates ($(short "$upstream"))" "$upstream"; then
    echo >&2
    echo "Conflicts in:" >&2
    git diff --name-only --diff-filter=U | sed 's/^/  /' >&2
    if [ "$mode" = pr ]; then next='bash scripts/template-sync.sh --continue'; else next="git push origin $main"; fi
    die "Fix them, run 'git add' on each file, then 'git commit'. Then: $next
To undo the whole sync instead: git merge --abort"
  fi
fi

publish
