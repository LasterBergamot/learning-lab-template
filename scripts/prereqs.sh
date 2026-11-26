#!/usr/bin/env bash
# Checks (and on request installs) the tools learning-lab needs on Linux: Omarchy (for example
# Try Omarchy for Windows, a Linux VM) or any other Arch-based distro gets pacman, yay (AUR) and
# mise installs; any other distro gets mise installs and the package names to install yourself.
# It never touches dev-config's or ai-common's installs; it points to them instead.
#
# Usage: bash scripts/prereqs.sh [options]
#   --check           list every core tool with its version or what is missing (default)
#   --install         like --check, then offer to install each missing tool (asks y/N per tool,
#                     prints the exact command first; nothing runs without a yes)
#   --ci              check only what CI needs (git, python); exit 1 if any is missing
#   --track <ids>     also check the optional tools of these tracks (comma-separated, or "all")
#   -h, --help        this help
#
# Exit code: 0 when every required tool is present, 1 otherwise (optional tools never fail).
set -u

if [[ $(uname -s) != Linux ]]; then
  printf 'learning-lab supports Linux only (this is %s); see docs/Platforms.md.\n' "$(uname -s)" >&2
  exit 2
fi
PACMAN=0; PLATFORM='Linux'
if command -v pacman >/dev/null 2>&1; then PACMAN=1; PLATFORM='Linux (pacman)'; fi

MODE=check; TRACKS=''
while (($#)); do
  case $1 in
    --check)   MODE=check ;;
    --install) MODE=install ;;
    --ci)      MODE=ci ;;
    --track)   shift; TRACKS=${1:-} ;;
    --track=*) TRACKS=${1#*=} ;;
    -h|--help) sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) printf 'unknown option: %s (try --help)\n' "$1" >&2; exit 2 ;;
  esac
  shift
done

# --- the tool table ------------------------------------------------------------------------
# id | scope | tracks | binary | pacman package | mise spec | note
#   scope:  ci = needed by CI and everywhere; core = every machine; opt = only with --track
#   binary: the command to look for; PYTHON and ENGINE are special-cased below
#   install preference: mise spec (any distro) > pacman (Arch-based distros) > note only
#   pacman package names are Arch's; on other distros the name is usually close
# Package ids marked "(verify)" in the note are best guesses; check them before relying on them.
TOOLS=(
  "git|ci||git|git||"
  "python|ci||PYTHON|python||"
  "gh|core||gh|github-cli||then: gh auth login"
  "jq|core||jq|jq||"
  "curl|core||curl|curl||"
  "mise|core||mise|mise||other distros: curl https://mise.run | sh; then activate it in ~/.bashrc: eval \"\$(mise activate bash)\""
  "uv|core||uv||uv@latest|"
  "apm|core||apm|||APM CLI: curl -sSL https://aka.ms/apm-unix | sh"
  "engine|core||ENGINE|docker docker-compose||Docker with the compose plugin; enable the service (docs/Setup.md)"
  "kind|core||kind||kind@latest|"
  "kubectl|core||kubectl||kubectl@latest|"
  "shellcheck|core||shellcheck|shellcheck|shellcheck@latest|lints scripts/*.sh"
  "openssl|opt|security,identity|openssl|openssl||"
  "java|opt|jvm,testing,identity,eventing,data|java||java@temurin-25|"
  "maven|opt|jvm,testing,identity|mvn||maven@latest|"
  "gradle|opt|jvm,testing|gradle||gradle@latest|"
  "node|opt|mobile,ai|node||node@lts|"
  "flutter|opt|mobile|flutter||flutter@latest|mise backend for flutter (verify)"
  "helm|opt|orchestration|helm||helm@latest|"
  "opentofu|opt|iac,cloud|tofu||opentofu@latest|"
  "terraform|opt|iac|terraform||terraform@latest|"
  "pulumi|opt|iac,cloud|pulumi||pulumi@latest|"
  "ansible|opt|iac|ansible|ansible||"
  "aws|opt|cloud|aws|aws-cli-v2||"
  "gcloud|opt|cloud|gcloud|AUR:google-cloud-cli||AUR package via yay (verify)"
  "az|opt|cloud|az|azure-cli||"
  "qemu|opt|virtualization|qemu-system-x86_64|qemu-full||needs nested virtualization in the VM (docs/Platforms.md)"
  "ollama|opt|ai|ollama|ollama||CPU-only in the VM; small models"
)

# --- helpers --------------------------------------------------------------------------------
have() { command -v "$1" >/dev/null 2>&1; }
first_line() { head -n 1 | tr -d '\r'; }
run_ver() {  # run a version command with a timeout when available; print its first line
  if have timeout; then timeout 20 "$@" 2>&1 | first_line; else "$@" 2>&1 | first_line; fi
}

track_selected() {  # $1 = the tool's comma-separated tracks
  [[ -n $TRACKS ]] || return 1
  [[ $TRACKS == all ]] && return 0
  local t
  for t in ${1//,/ }; do [[ ",$TRACKS," == *",$t,"* ]] && return 0; done
  return 1
}

# Sets VER (version text) and returns 0 when the tool is usable.
probe() {  # $1 = binary column
  VER=''
  case $1 in
    PYTHON)
      local py
      for py in python3 python; do
        if have "$py" && VER=$(run_ver "$py" --version) && [[ $VER == Python\ 3* ]]; then
          VER="$VER ($py)"; return 0
        fi
      done
      VER=''; return 1 ;;
    ENGINE)
      local c
      have docker || return 1
      VER="docker: $(run_ver docker --version)"
      if c=$(run_ver docker compose version) && [[ $c == *[0-9]* ]]; then
        VER="$VER; compose: $c"
      else
        VER="$VER; compose: MISSING"
      fi
      return 0 ;;
    java)    have java    && VER=$(run_ver java -version) ;;
    kubectl) have kubectl && VER=$(run_ver kubectl version --client) ;;
    *)       have "$1"    && VER=$(run_ver "$1" --version) ;;
  esac
  # A mise shim with no version set answers "mise ERROR …": that tool is not installed.
  [[ -n $VER && $VER != mise\ ERROR* ]] && return 0
  VER=''
  # Installed through mise but mise is not activated in this shell?
  if have mise && mise which "$1" >/dev/null 2>&1; then
    VER="installed via mise, but not on PATH: activate mise in ~/.bashrc"
  fi
  return 1
}

install_cmd() {  # prints the install command for this machine, or nothing
  local pac=$1 mis=$2
  if [[ -n $mis ]] && have mise; then printf 'mise use -g %s' "$mis"; return; fi
  (( PACMAN )) || return 0
  if [[ $pac == AUR:* ]]; then
    have yay && printf 'yay -S --needed %s' "${pac#AUR:}"
  elif [[ -n $pac ]]; then
    printf 'sudo pacman -S --needed %s' "$pac"
  fi
}

ask_yn() {
  [[ -t 0 ]] || { printf '    [skipped: no terminal]\n'; return 1; }
  local a; read -r -p "    Run it? [y/N] " a
  [[ $a == [yY]* ]]
}

# --- main -----------------------------------------------------------------------------------
printf 'learning-lab prerequisites on %s (mode: %s%s)\n\n' "$PLATFORM" "$MODE" \
  "${TRACKS:+, tracks: $TRACKS}"

MISSING_REQUIRED=0; MISSING_OPTIONAL=0
declare -a TODO=()
for row in "${TOOLS[@]}"; do
  IFS='|' read -r id scope tracks bin pac mis note <<<"$row"
  case $MODE in
    ci) [[ $scope == ci ]] || continue ;;
    *)  [[ $scope == opt ]] && ! track_selected "$tracks" && continue ;;
  esac
  label=$id; [[ $scope == opt ]] && label="$id (optional)"
  if probe "$bin"; then
    printf '  ✓ %-22s %s\n' "$label" "${VER:0:90}"
    if [[ $bin == ENGINE && $VER == *'compose: MISSING'* ]]; then
      printf '      ! no compose provider: see docs/Setup.md\n'
    fi
  else
    printf '  ✗ %-22s %s\n' "$label" "${VER:-missing}"
    [[ -n $note ]] && printf '      note: %s\n' "$note"
    if [[ $scope == opt ]]; then MISSING_OPTIONAL=$((MISSING_OPTIONAL + 1)); else MISSING_REQUIRED=$((MISSING_REQUIRED + 1)); fi
    TODO+=("$row")
  fi
done

printf '\nMissing: %d required, %d optional.\n' "$MISSING_REQUIRED" "$MISSING_OPTIONAL"

if [[ $MODE == install && ${#TODO[@]} -gt 0 ]]; then
  printf '\nInstalling: each command is shown first and runs only after a yes.\n'
  for row in "${TODO[@]}"; do
    IFS='|' read -r id scope tracks bin pac mis note <<<"$row"
    cmd=$(install_cmd "$pac" "$mis")
    printf '\n  %s\n' "$id"
    if [[ -z $cmd ]]; then
      [[ -n $mis ]] && ! have mise && printf '    install mise first, then re-run (it installs %s)\n' "$mis"
      (( PACMAN )) || [[ -z $pac ]] || printf '    no pacman here: install it with your package manager (Arch name: %s)\n' "${pac#AUR:}"
      printf '    no automatic install here: %s\n' "${note:-see docs/Setup.md}"
      continue
    fi
    printf '    $ %s\n' "$cmd"
    if ask_yn; then
      # Word splitting is intended: the command is built from fixed table values.
      # shellcheck disable=SC2086
      $cmd || printf '    failed (exit %d)\n' "$?"
    fi
  done
  printf '\nOpen a new shell (so PATH and mise activation apply) and run --check again.\n'
fi

if [[ $MODE != ci ]]; then
  printf '\nMachine setup that this script does not do: dev-config (status line, deny rules, git\n'
  printf 'aliases) and the ai-common guard hooks. See docs/Setup.md.\n'
fi

(( MISSING_REQUIRED == 0 ))
