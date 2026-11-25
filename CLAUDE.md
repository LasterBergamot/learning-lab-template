# learning-lab: Claude Code context

@AGENTS.md

`AGENTS.md` (imported above) is the canonical router and rule set for every AI tool. This file
adds only what is specific to Claude Code.

## Claude-only extras

- **Output style:** `.claude/output-styles/socratic.md` is the project default
  (`"outputStyle": "socratic"` in `.claude/settings.json`). It sets the tutor behaviour from
  `AGENTS.md` for every session.
- **Hard enforcement:** `.claude/settings.json` denies Edit on code file types under `labs/`
  and asks before state-changing git and gh commands. The deny rules don't stop writes through
  Bash, so the `AGENTS.md` rule is what counts: no lab code by any route.
- **Path rules:** `.claude/rules/labs.md` loads for `labs/**`, `.claude/rules/assessments.md`
  for `assessments/**`.
- **Skills and agents:** `.claude/skills/` and `.claude/agents/` are deployed by APM from
  `ai-common`. Never edit them here. `model:` and `effort:` in their frontmatter are honoured by
  Claude Code only.
- **Guards:** ai-common's guard hooks (user scope) are Claude-only.
- Explore and Plan subagents load neither this file nor the rules: put the paths they need in
  their prompt.
