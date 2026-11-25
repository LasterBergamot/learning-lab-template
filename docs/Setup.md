# Setup

From a fresh machine to a working learning-lab setup, step by step. People follow this page,
and so does ai-common's `setup-project` skill. Each step has an **Expected** result. If you
don't get it, stop and fix that step before you go on.

Two platforms are supported, and every step covers both (see [Platforms](Platforms.md)):
- **Omarchy (Linux + Docker)**: the Omarchy VM, in bash.
- **Windows 11 (Git Bash + Podman)**: native Windows, with **Git Bash** as the only shell. No
  WSL2 distro.

## Ground rules

- `scripts/prereqs.sh` checks the tools and, on request, installs them. It shows every command
  and runs it only after you say yes. The AI never runs `sudo` or installs system tools for you.
- A lab that needs extra tools (Terraform, Flutter, …) pins them in its own `mise.toml`, or
  you add them with `scripts/prereqs.sh --track <id>`.
- Don't commit machine details. Protected folders and service names go in
  `~/.claude/hooks/local.sh`, which never enters a repo.

## 1. Bootstrap: git and a shell

| Omarchy | Windows 11 |
|---------|------------|
| git and bash are already there | Install Git for Windows: `winget install --id Git.Git -e` (PowerShell). It provides Git Bash; use Git Bash for every later step. |

```bash
git --version && bash --version | head -1
```

**Expected:** both print a version. On Windows, run it in Git Bash.

## 2. Clone your repo

Your own repo, created from the template (see the README's "Using this template").

```bash
git clone git@github.com:<owner>/<repo>.git && cd <repo>
```

**Expected:** the clone succeeds and `ls` shows `README.md`, `AGENTS.md`, `labs/` and `scripts/`.
Line endings are LF on both platforms (`.gitattributes`); don't change `core.autocrlf` for
this repo.

## 3. Check free disk space

```bash
df -h ~
```

**Expected:** at least 20 GB free. Less is enough for light labs only: free up space, or do
heavy labs on the bigger machine ([Isolation](Isolation.md)). Record the number in Isolation's
resource budget.

## 4. Check the prerequisites

```bash
bash scripts/prereqs.sh --check
```

It checks git, python, gh, jq, curl, mise, uv, the APM CLI, a container engine with compose,
kind, kubectl and shellcheck.

**Expected:** a ✓/✗ list and a "Missing" count. Fix the ✗ lines in steps 5–7, then run it again.

## 5. Install what is missing

```bash
bash scripts/prereqs.sh --install
```

- **Omarchy** uses `sudo pacman -S --needed …` (or `yay` for AUR packages) and `mise use -g …`.
- **Windows 11** uses `winget install --id … -e` and `mise use -g …`.

Each command is printed first and runs only after a `y`. Install mise before the tools it
provides (uv, kind, kubectl, shellcheck, …), then open a new shell and activate it:

```bash
echo 'eval "$(mise activate bash)"' >> ~/.bashrc   # both platforms; Git Bash reads ~/.bashrc too
```

The APM CLI has no package: on Omarchy `curl -sSL https://aka.ms/apm-unix | sh`. On Windows,
follow the APM README (microsoft/apm on GitHub).

**Expected:** after a new shell, `bash scripts/prereqs.sh --check` shows no required tool
missing (exit code 0).

## 6. Log in to GitHub

```bash
gh auth login        # once per machine
gh auth status
```

**Expected:** logged in, with the `repo` and `workflow` scopes (`project` too if you use the
optional board: `gh auth refresh -s project`).

## 7. Container engine

### Omarchy: Docker

```bash
docker run --rm hello-world && docker compose version
```

**Expected:** the hello-world message and a Compose v2 version. If permission is denied, add
yourself to the `docker` group and log in again.

### Windows 11: Podman on the Hyper-V provider

1. Install Podman Desktop (`bash scripts/prereqs.sh --install` offers it through winget).
2. Enable Hyper-V (Windows Features). This needs Windows 11 Pro or Enterprise. On Windows Home,
   Podman can only use WSL2 as its backend; that's fine, it stays invisible and you still work
   only in Git Bash.
3. In Git Bash:

   ```bash
   echo 'export CONTAINERS_MACHINE_PROVIDER=hyperv' >> ~/.bashrc && source ~/.bashrc
   podman machine init
   podman machine start
   podman run --rm quay.io/podman/hello
   podman compose version
   ```

**Expected:** the hello message, and `podman compose` names the compose provider it uses
(docker-compose or podman-compose). If it has none, install one (Podman Desktop offers it).

## 8. Kubernetes tooling: kind and kubectl

Installed in step 5 through mise. Clusters are created per lab, not here.

```bash
kind version && kubectl version --client
# Windows 11 only, also in ~/.bashrc:
export KIND_EXPERIMENTAL_PROVIDER=podman
```

**Expected:** both print a version.

## 9. Machine setup (optional)

[dev-config](https://github.com/LasterBergamot/dev-config) installs the Claude Code status
line, the `permissions.deny` rules for disk-wiping commands, and the git aliases. Your own
dotfiles work just as well. To use dev-config, clone it next to this repo, then:

```bash
bash install.sh       # Omarchy
./install.ps1         # Windows 11, from PowerShell (it launches Git Bash)
```

Pick `claude-statusline`, `claude-settings-statusline`, `claude-settings-deny`, and
`git-aliases` if you want them.

**Expected:** `bash install.sh --list` reports these items as `up to date`.

## 10. Guard hooks from ai-common (Claude Code only, optional)

The guards ask before risky actions: commits, pushes, deletes, secret reads, network uploads,
writes outside the workspace. They are installed once per machine (user scope):

```bash
GITHUB_APM_PAT=$(gh auth token) apm install -g LasterBergamot/ai-common/packages/guards#<tag> --target claude
cp ~/.claude/hooks/guards/scripts/local.sh.example ~/.claude/hooks/local.sh
```

Use the newest ai-common tag. Fill `local.sh` with this machine's protected folders and
services; ai-common's `docs/USING.md` has the details. Other AI tools have no guard hooks: the
rules in `AGENTS.md` apply to them.

If you skip this step, `.claude/settings.json` still asks before state-changing git commands
and denies code edits under `labs/`.

**Expected:** a new Claude Code session lists the active guards at start. Asking it to run
`git push` makes it ask first, even in auto mode.

## 11. The AI tooling in this repo

Nothing to install: the skills and agents are committed, deployed by APM per tool
(`.claude/skills/`, `.agents/skills/`). Run `apm install` only after changing the ai-common tag
in `apm.yml`. Every tool reads `AGENTS.md`; `CLAUDE.md` and `GEMINI.md` import it.

**Expected:** in Claude Code, `/` lists `socratic-tutor`, `plan-lab`, `prereq-check`,
`session-log`, `review-quiz`, `assessment-prep`, `import-matrix` and `roadmap-sync`. Asking
"write me a FastAPI hello world" gets questions back, not code.

## 12. Check the no-code guard (Claude Code)

Ask Claude to create `labs/scratch/main.py`.

**Expected:** the write is denied by `permissions.deny`. Creating `labs/scratch/NOTES.md`
works; delete the folder afterwards.

## 13. Check the docs tooling

```bash
python3 scripts/check_docs.py     # on Windows, python if python3 is not found
```

**Expected:** `OK` and exit code 0. CI runs the same check on Linux and Windows.

## Finish

Make three lists: what was installed, what is running, and what failed or was skipped. The
setup is complete only when every step you ran matched its **Expected** result.

## Continuing on another machine

```bash
git pull
bash scripts/prereqs.sh --check --track <id>   # the track you are working on
```

The lab's `NOTES.md` says where you stopped. Everything else (Status lines, the review queue,
assessments) is in the repo too.
