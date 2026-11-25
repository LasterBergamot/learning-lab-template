#!/usr/bin/env python3
"""Check learning-lab's Markdown: links, lab Status lines, track links. Stdlib only.

Runs the same on Omarchy (Linux) and Windows 11 (Git Bash), locally and in CI
(`.github/workflows/check.yml`). It checks that:

- every relative Markdown link resolves to a file or folder in the repo (web links, anchors,
  placeholders such as `<track>` and the two `_template/` folders are skipped);
- no `[[...]]` wiki-style link is used (the repo has no wiki);
- every lab README (`labs/<track>/<lab>/README.md`, not the template) carries a valid
  `**Status:** todo|learning|building|done` line;
- every track README (`labs/<track>/README.md`) is linked from the root `README.md`.

Folders deployed by APM (`.claude/skills`, `.claude/agents`, `.agents/skills`) and
`apm_modules/` are not checked: they are generated, and fixed upstream in ai-common.

    python3 scripts/check_docs.py          # from the repo root; exit 1 on any problem
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {
    ".git",
    "apm_modules",
    ".apm-local",
    "node_modules",
    ".claude/skills",
    ".claude/agents",
    ".agents/skills",
}
STATUS = re.compile(r"^\*\*Status:\*\*\s*(todo|learning|building|done)\b", re.MULTILINE)
STATUS_ANY = re.compile(r"^\*\*Status:\*\*", re.MULTILINE)
FENCE = re.compile(r"^(```|~~~).*?^\1[^\n]*$", re.MULTILINE | re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")
TEMPLATES = (ROOT / "labs" / "_template", ROOT / "assessments" / "_template")
LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")


def markdown_files() -> list[Path]:
    """Every Markdown file in the repo, minus the generated and vendored folders."""
    files = []
    for path in sorted(ROOT.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        if any(rel == d or rel.startswith(d + "/") for d in SKIP_DIRS):
            continue
        files.append(path)
    return files


def prose(text: str) -> str:
    """The text without fenced code blocks and inline code, where links are not links."""
    return INLINE_CODE.sub("", FENCE.sub("", text))


def check_links(path: Path, text: str) -> list[str]:
    """Relative links that don't resolve, and wiki-style links.

    The templates (`labs/_template/`, `assessments/_template/`) are skipped for relative links:
    those are written for the location the template is copied to.
    """
    problems = []
    body = prose(text)
    if "[[" in body:
        problems.append(f"{rel(path)}: uses a [[...]] wiki-style link; use a relative Markdown link")
    if any(path.is_relative_to(t) for t in TEMPLATES):
        return problems
    for target in LINK.findall(body):
        if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE) or target.startswith("#"):
            continue  # http(s), mailto and other schemes; in-page anchors
        if "<" in target or "{" in target or re.fullmatch(r"[A-Z_]+", target):
            continue  # template placeholders: <track>, {id}, URL
        file_part = unquote(target.split("#", 1)[0])
        if not file_part:
            continue
        base = ROOT if file_part.startswith("/") else path.parent
        resolved = (base / file_part.lstrip("/")).resolve()
        if not resolved.exists():
            problems.append(f"{rel(path)}: broken link -> {target}")
    return problems


def check_status(lab_readmes: list[Path]) -> list[str]:
    """Lab READMEs (`labs/<track>/<lab>/README.md`) without a valid Status line.

    Track READMEs and the lab template are not checked: tracks have no Status of their own (their
    graph node is derived from their labs), and the template holds a placeholder.
    """
    problems = []
    for path in lab_readmes:
        text = path.read_text(encoding="utf-8")
        if STATUS.search(text):
            continue
        if STATUS_ANY.search(text):
            problems.append(f"{rel(path)}: invalid **Status:** value (use todo, learning, building or done)")
        else:
            problems.append(f"{rel(path)}: missing the **Status:** line under the title")
    return problems


def check_track_links(tracks: list[Path]) -> list[str]:
    """Track READMEs the root README doesn't link to."""
    readme = ROOT / "README.md"
    if not readme.exists():
        return ["README.md: missing"]
    linked = set()
    for target in LINK.findall(prose(readme.read_text(encoding="utf-8"))):
        file_part = unquote(target.split("#", 1)[0]).strip("/")
        if file_part:
            linked.add(Path(file_part).as_posix().removesuffix("/README.md").rstrip("/"))
    problems = []
    for path in tracks:
        track_dir = path.parent.relative_to(ROOT).as_posix()
        if track_dir not in linked:
            problems.append(f"README.md: no link to the track README {rel(path)}")
    return problems


def rel(path: Path) -> str:
    """Repo-relative path with forward slashes, the same on Linux and Windows."""
    return path.relative_to(ROOT).as_posix()


def main() -> int:
    """Run every check and print the problems; returns the process exit code."""
    files = markdown_files()
    problems: list[str] = []
    for path in files:
        problems += check_links(path, path.read_text(encoding="utf-8"))

    labs = ROOT / "labs"
    track_dirs = sorted(d for d in labs.iterdir() if d.is_dir() and not d.name.startswith("_")) if labs.is_dir() else []
    tracks = [d / "README.md" for d in track_dirs if (d / "README.md").exists()]
    lab_readmes = [p for d in track_dirs for p in sorted(d.glob("*/README.md"))]
    problems += check_status(lab_readmes)
    problems += check_track_links(tracks)

    for problem in problems:
        print(f"::error::{problem}" if "GITHUB_ACTIONS" in os.environ else problem)
    if problems:
        print(f"{len(problems)} problem(s) in {len(files)} Markdown files.", file=sys.stderr)
        return 1
    print(f"OK: {len(files)} Markdown files, {len(tracks)} tracks, {len(lab_readmes)} lab READMEs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
