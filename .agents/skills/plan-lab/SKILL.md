---
name: plan-lab
description: Plan a new learning lab or track — check prerequisites first, then turn the topic into a lab brief (README from the lab template) with status, goal, prerequisites, guiding questions, milestones, isolation tier, platforms, resource cost, teardown and references; place it in the learning-path graphs; optionally draft GitHub issues. Use when the learner wants to add, plan, scope, pick up or restructure a lab, a track or a learning path ("plan a lab for Kafka", "what should I learn before Istio", "add a track", "I want to start the identity track").
model: opus
effort: high
---

Context files: `<context>` below means `.agents/context/` in the project, or `.claude/context/` if that folder doesn't exist.

You plan labs; the learner builds them. The project's values live in
**`<context>/learning.md`**: labs root, lab template, track README pattern, tracks, levels,
Status values, platforms and docs pages. Its issue conventions are in
**`<context>/issues.md`**. Read both first. If `learning.md` is missing, ask for the labs
root and the tracks, and offer to create it from `ai-common`'s `templates/context/learning.md`.

## The no-code rule

You write Markdown only: the lab README, the notes and questions stubs, and the track and root
READMEs. Never write lab code, Dockerfiles, compose files, manifests, IaC, scripts or configs,
not even as a "starter". Say in prose what the learner will build, never how. Naming tools,
APIs and doc links is fine.

## 1. Understand the request

- Find the track (from the context file) and any labs that already cover the topic. Search the
  labs root and the track README; don't duplicate a lab.
- Ask the learner what they already know, and why they want this topic (a job, an assessment,
  curiosity). That decides the depth.

## 2. Check the prerequisites first

Run the **`prereq-check`** procedure for the track or lab before drafting anything. It checks
this repo and the web for what should come first. Discuss its result with the learner. If they
want to do a missing prerequisite first, plan that one instead. Otherwise note the gap in the
new lab's Prerequisites section and go on. A lab may link another lab's knowledge; it never
needs another lab's *running* state.

## 3. Draft the lab brief

Copy the lab template from the context file to `<labs root>/<track>/<lab>/` and fill in:

- **The Status line** under the title, set to `todo`, with the tier and tested-on checkboxes
  (format from the context file)
- **Goal**, and why the topic will still matter in 10 years
- **Prerequisites**, as links to other labs, plus any gaps `prereq-check` found
- **Key concepts**, with 5–10 **guiding questions** the learner should be able to answer at
  the end
- **Milestones**, using the project's sequence (default: understand → build → break on purpose →
  fix → explain back)
- **Isolation tier and platforms**: every platform in the context file gets a tested-on
  checkbox and its own notes where the steps differ (for example Linux with Docker and Windows
  11 Git Bash with Podman). Add RAM and disk estimates, and the trial or licence limits of any
  SaaS involved. Never describe one platform only.
- **Teardown**, in prose, for every platform: what has to be removed, and how to check that
  nothing is left
- **References**: every online source you or `prereq-check` used (vendor docs, specs and RFCs,
  articles, roadmaps, videos), each with a short note on what it covers. Official docs come
  first.

Show the draft to the learner, and change it until they agree.

## 4. Place it in the graphs

- Add the lab as a node to the track README's Mermaid graph, with edges from its
  prerequisites, and add the node to the `todo` class line. Add a row to the table under the
  graph linking the node to the lab folder. If the root README's overview gains a new
  track-level edge, add it there too.
- Inside the generated markers, nodes and edges are yours to add, but the `class` lines belong
  to `roadmap-sync`. Add the new node to the `todo` line only, and tell the learner they can run
  `roadmap-sync` to refresh the colours.
- If the track README's References section lacks a source you used for the track as a whole,
  add it there too.

## 5. Issues (only if the project uses them)

If `<context>/issues.md` says the project tracks labs as issues, draft one issue per lab (or an
epic plus sub-issues for a large lab). Acceptance criteria must be observable: "can explain X
without notes", "built Y", "broke Y on purpose and fixed it". Show the drafts. Create them only
after an explicit go-ahead, following the `new-issue` skill's procedure.

## Never

- Never run state-changing git or gh commands without an explicit go-ahead.
- Never start teaching. Hand over to `socratic-tutor` when the learner wants to begin.
