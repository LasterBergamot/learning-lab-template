#!/usr/bin/env python3
"""Print where the learner stands: labs in progress, due reviews, what is ready to start. Stdlib only.

The `learn` skill (from ai-common) runs this at the start of a session instead of reading every
README itself. It reads, and never writes:

- every track README (`labs/<track>/README.md`): the lab graph between the `roadmap-sync`
  markers and the lab table under it. A graph node's id is its lab's id with `-` replaced by
  `_` (lab `ml-math` is node `ml_math`), so order doesn't matter; `scripts/check_docs.py`
  checks that every node has a row and every row a node;
- every lab folder (`labs/<track>/<lab>/`): the README's `**Status:**` and `**Tier:**`, the last
  `## Session YYYY-MM-DD: <goal>` entry in `NOTES.md` (its **Where I stopped** and **Next step**
  lines) and the unanswered rows in `QUESTIONS.md`;
- the root `README.md` graph: which tracks come before which;
- `docs/Review-Queue.md`: the rows whose **Next due** date has passed;
- `assessments/<subject>/readiness.md`: the competency statuses.

"Ready to start" means a lab that hasn't started whose predecessors in its track graph are all
`done`. Prerequisite tracks are shown next to it, not enforced: `prereq-check` judges those.

    python3 scripts/lab-status.py                 # the overview, from the repo root
    python3 scripts/lab-status.py --track ai      # one track only
    python3 scripts/lab-status.py --json          # everything, for tools
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

STATUSES = ("todo", "learning", "building", "done")
STATUS = re.compile(r"^\*\*Status:\*\*\s*(todo|learning|building|done)\b", re.MULTILINE)
TIER = re.compile(r"\*\*Tier:\*\*\s*(T\d)")
BLOCK = re.compile(r"<!-- roadmap-sync:start -->(.*?)<!-- roadmap-sync:end -->", re.DOTALL)
NODE = re.compile(r"^\s*([A-Za-z0-9_]+)\[")
HEADER = re.compile(r"^(```|%%|(flowchart|graph|classDef|class)\s)")
EDGE_PART = re.compile(r"^\s*([A-Za-z0-9_]+)")
LAB_ROW = re.compile(r"^\|\s*`([^`]+)`:\s*(.*?)\s*\|")
SESSION = re.compile(r"^## Session (\d{4}-\d{2}-\d{2})(?::\s*(.*))?$", re.MULTILINE)
FIELD = re.compile(r"^- \*\*([^*]+?):\*\*\s*(.*)$")
QUEUE = re.compile(r"<!-- review-queue:start -->(.*?)<!-- review-queue:end -->", re.DOTALL)
READINESS = ("not-started", "learning", "can-explain", "ready")


@dataclass
class Lab:
    track: str
    id: str
    title: str
    status: str = "todo"
    folder: str | None = None
    tier: str | None = None
    after: list[str] = field(default_factory=list)  # lab ids that come first in the track graph
    last_session: str | None = None
    last_goal: str | None = None
    stopped: str | None = None
    next_step: str | None = None
    open_questions: int = 0


@dataclass
class Track:
    id: str
    name: str
    status: str = "todo"
    after: list[str] = field(default_factory=list)  # track ids that come first in the root graph
    labs: list[Lab] = field(default_factory=list)


def node_id(lab_id: str) -> str:
    """The graph node id of a lab: its id with `-` replaced by `_` (Mermaid ids can't hold `-`)."""
    return lab_id.replace("-", "_")


def graph(text: str) -> tuple[list[str], list[tuple[str, str]]]:
    """Node ids in declaration order and the edges, from the first roadmap-sync block."""
    match = BLOCK.search(text)
    if not match:
        return [], []
    nodes: list[str] = []
    edges: list[tuple[str, str]] = []
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if not stripped or HEADER.match(stripped):
            continue
        if "-->" in line:
            ids = [m.group(1) for part in line.split("-->") if (m := EDGE_PART.match(part))]
            edges += list(zip(ids, ids[1:]))
            continue
        if node := NODE.match(line):
            nodes.append(node.group(1))
    return nodes, edges


def sections(text: str) -> dict[str, str]:
    """`- **Field:** value` lines of a notes entry, with indented continuation lines joined."""
    fields: dict[str, str] = {}
    current = None
    for line in text.splitlines():
        if m := FIELD.match(line):
            current = m.group(1).strip().lower()
            fields[current] = m.group(2).strip()
        elif current and line.startswith("  ") and line.strip():
            fields[current] += " " + line.strip()
        elif not line.strip():
            continue
        else:
            current = None
    return fields


def read_notes(lab: Lab, folder: Path) -> None:
    """The last session entry of the lab's NOTES.md."""
    notes = folder / "NOTES.md"
    if not notes.exists():
        return
    text = notes.read_text(encoding="utf-8")
    entries = list(SESSION.finditer(text))
    if not entries:
        return
    last = entries[-1]
    lab.last_session, lab.last_goal = last.group(1), last.group(2)
    end = text.find("\n## ", last.end())
    fields = sections(text[last.end(): end if end != -1 else len(text)])
    lab.stopped = fields.get("where i stopped")
    lab.next_step = fields.get("next step")


def read_questions(lab: Lab, folder: Path) -> None:
    """Rows of QUESTIONS.md whose Answer cell is still empty."""
    path = folder / "QUESTIONS.md"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or set(cells[0]) <= set("-: ") or cells[0].lower() == "question":
            continue
        if cells[0].startswith("<"):
            continue  # the template's placeholder row
        if not cells[2] or cells[2].startswith("<"):
            lab.open_questions += 1


def read_track(root: Path, track_dir: Path, warnings: list[str]) -> Track:
    text = (track_dir / "README.md").read_text(encoding="utf-8")
    title = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), track_dir.name)
    track = Track(id=track_dir.name, name=title.removesuffix(" Track"))
    nodes, edges = graph(text)
    rows = [(m.group(1), m.group(2)) for line in text.splitlines() if (m := LAB_ROW.match(line))]
    node_to_lab = {node_id(lab_id): lab_id for lab_id, _ in rows}
    for node in nodes:
        if node not in node_to_lab:
            warnings.append(f"labs/{track.id}/README.md: graph node {node} has no lab row (expected a row for lab id {node.replace('_', '-')})")
    for lab_id, _ in rows:
        if node_id(lab_id) not in nodes:
            warnings.append(f"labs/{track.id}/README.md: lab {lab_id} has no graph node {node_id(lab_id)}")
    labs = {lab_id: Lab(track=track.id, id=lab_id, title=title) for lab_id, title in rows}
    for src, dst in edges:
        if src in node_to_lab and dst in node_to_lab:
            labs[node_to_lab[dst]].after.append(node_to_lab[src])
    # Lab folders, including any that aren't in the table yet.
    for readme in sorted(track_dir.glob("*/README.md")):
        lab_id = readme.parent.name
        if lab_id.startswith("_"):
            continue
        lab = labs.setdefault(lab_id, Lab(track=track.id, id=lab_id, title=lab_id))
        if lab_id not in dict(rows):
            warnings.append(f"labs/{track.id}/{lab_id}/: has a folder but no row in the track table")
        body = readme.read_text(encoding="utf-8")
        lab.folder = readme.parent.relative_to(root).as_posix()
        if status := STATUS.search(body):
            lab.status = status.group(1)
        else:
            warnings.append(f"{lab.folder}/README.md: no valid **Status:** line, counted as todo")
        if tier := TIER.search(body):
            lab.tier = tier.group(1)
        read_notes(lab, readme.parent)
        read_questions(lab, readme.parent)
        if lab.status in ("learning", "building") and lab.last_session and not lab.next_step:
            warnings.append(f"{lab.folder}/NOTES.md: the last session has no **Next step:** line")
    track.labs = list(labs.values())
    states = {lab.status for lab in track.labs}
    if track.labs and states == {"done"}:
        track.status = "done"
    elif "building" in states:
        track.status = "building"
    elif "learning" in states or "done" in states:
        track.status = "learning"
    return track


def review_queue(root: Path, today: dt.date) -> dict:
    path = root / "docs" / "Review-Queue.md"
    result = {"total": 0, "due": 0, "due_by_topic": {}}
    if not path.exists():
        return result
    match = QUEUE.search(path.read_text(encoding="utf-8"))
    for line in (match.group(1) if match else "").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or cells[0].lower() == "question" or set(cells[0]) <= set("-: "):
            continue
        result["total"] += 1
        try:
            due = dt.date.fromisoformat(cells[2])
        except ValueError:
            continue
        if due <= today:
            result["due"] += 1
            result["due_by_topic"][cells[1]] = result["due_by_topic"].get(cells[1], 0) + 1
    return result


def assessments(root: Path) -> list[dict]:
    subjects = []
    base = root / "assessments"
    for readiness in sorted(base.glob("*/readiness.md")) if base.is_dir() else []:
        if readiness.parent.name.startswith("_"):
            continue
        text = readiness.read_text(encoding="utf-8")
        target = re.search(r"^Target level:\s*([^.\n]+)", text, re.MULTILINE)
        counts = {s: 0 for s in READINESS}
        for line in text.splitlines():
            if line.startswith("| `"):
                for status in READINESS:
                    if re.search(rf"\b{status}\b", line):
                        counts[status] += 1
                        break
        subjects.append({"subject": readiness.parent.name, "target": target.group(1).strip() if target else None, **counts})
    return subjects


def collect(root: Path, today: dt.date) -> dict:
    warnings: list[str] = []
    labs_dir = root / "labs"
    track_dirs = sorted(d for d in labs_dir.iterdir() if d.is_dir() and not d.name.startswith("_") and (d / "README.md").exists())
    tracks = {d.name: read_track(root, d, warnings) for d in track_dirs}
    root_readme = root / "README.md"
    _, track_edges = graph(root_readme.read_text(encoding="utf-8")) if root_readme.exists() else ([], [])
    for src, dst in track_edges:
        if dst in tracks:
            tracks[dst].after.append(src)

    ready = []
    for track in tracks.values():
        done = {lab.id for lab in track.labs if lab.status == "done"}
        for lab in track.labs:
            if lab.status == "todo" and all(a in done for a in lab.after):
                ready.append({
                    "track": track.id,
                    "lab": lab.id,
                    "title": lab.title,
                    "folder": lab.folder,
                    "builds_on": lab.after,
                    "tracks_not_done": [t for t in track.after if t in tracks and tracks[t].status != "done"],
                })
    return {
        "today": today.isoformat(),
        "tracks": [asdict(t) for t in tracks.values()],
        "in_progress": [asdict(lab) for t in tracks.values() for lab in t.labs if lab.status in ("learning", "building")],
        "done": [f"{lab.track}/{lab.id}" for t in tracks.values() for lab in t.labs if lab.status == "done"],
        "ready": ready,
        "review_queue": review_queue(root, today),
        "assessments": assessments(root),
        "warnings": warnings,
    }


def text_report(data: dict, track: str | None) -> str:
    keep = (lambda t: t == track) if track else (lambda t: True)
    out = [f"Learning status ({data['today']})", ""]

    out.append("In progress")
    in_progress = [lab for lab in data["in_progress"] if keep(lab["track"])]
    for lab in in_progress:
        session = f"last session {lab['last_session']}" if lab["last_session"] else "no session logged yet"
        if lab["last_goal"]:
            session += f": {lab['last_goal']}"
        out.append(f"  {lab['track']}/{lab['id']}  {lab['status']}  ({lab['folder']}) · {session}")
        if lab["stopped"]:
            out.append(f"    stopped: {lab['stopped']}")
        if lab["next_step"]:
            out.append(f"    next:    {lab['next_step']}")
        if lab["open_questions"]:
            out.append(f"    open questions: {lab['open_questions']}")
    if not in_progress:
        out.append("  none")

    queue = data["review_queue"]
    out += ["", f"Review queue: {queue['due']} due of {queue['total']}"]
    for topic, n in sorted(queue["due_by_topic"].items()):
        if keep(topic.split("/")[0]) or not track:
            out.append(f"  {topic}: {n}")

    if data["assessments"] and not track:
        out += ["", "Assessments"]
        for a in data["assessments"]:
            counts = ", ".join(f"{a[s]} {s}" for s in READINESS)
            out.append(f"  {a['subject']} (target {a['target'] or '?'}): {counts}")

    out += ["", "Ready to start (every earlier lab in the track graph is done)"]
    by_track: dict[str, list[dict]] = {}
    for item in data["ready"]:
        if keep(item["track"]):
            by_track.setdefault(item["track"], []).append(item)
    tracks = {t["id"]: t for t in data["tracks"]}
    for track_id, items in by_track.items():
        names = []
        for item in items:
            name = item["lab"]
            if item["builds_on"]:
                name += f" (after {', '.join(item['builds_on'])})"
            if item["folder"]:
                name += " [folder ready]"
            names.append(name)
        line = f"  {track_id}: {', '.join(names)}"
        pending = items[0]["tracks_not_done"]
        if pending:
            line += f"  · track prerequisites not done: {', '.join(f'{t} ({tracks[t]['status']})' for t in pending)}"
        out.append(line)
    if not by_track:
        out.append("  none")

    done = [d for d in data["done"] if keep(d.split("/")[0])]
    out += ["", f"Done: {', '.join(done) if done else 'none'}"]

    started = [t for t in data["tracks"] if t["status"] != "todo" and keep(t["id"])]
    if started:
        out.append("Tracks started: " + ", ".join(f"{t['id']} ({t['status']})" for t in started))

    if data["warnings"]:
        out += ["", "Warnings"] + [f"  {w}" for w in data["warnings"]]
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--track", help="show one track only (its id, e.g. ai)")
    parser.add_argument("--json", action="store_true", help="print everything as JSON")
    parser.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today(), help="the date to judge due reviews by (YYYY-MM-DD)")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent, help="the repo root (default: this script's repo)")
    args = parser.parse_args()

    root = args.root.resolve()
    if not (root / "labs").is_dir():
        print(f"no labs/ folder under {root}", file=sys.stderr)
        return 1
    data = collect(root, args.today)
    if args.track and args.track not in {t["id"] for t in data["tracks"]}:
        print(f"unknown track: {args.track}", file=sys.stderr)
        return 1
    print(json.dumps(data, indent=2) if args.json else text_report(data, args.track))
    return 0


if __name__ == "__main__":
    sys.exit(main())
