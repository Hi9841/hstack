# Working preferences

Global working preferences across all repositories. Project facts stay in project instructions.

## Writing standard (Always active)

- Always write in Simplified Technical English (ASD-STE100) via [$simplified-technical-english](file:///C:/Users/hi/Desktop/skills/simplified-technical-english/SKILL.md). Keep technical explanations, procedures, instructions, and reports direct, precise, active, and unambiguous.

## Core doctrine

- Purpose is code stewardship: Care about the code itself; pride of craft produces simpler, more resilient systems.
- When principles collide, pick the path that cuts future maintenance cost. Separation of concerns is the root.
- Ask before touching unrelated modules, modifying public contracts, or running commands with external side effects.
- Done means verified in proportion to risk and reported in 2-4 lines. Never add agent co-authors (Remove if they exist).

## Tools and runtime

- Package managers: JS/TS uses pnpm if `pnpm-lock.yaml` exists, else Bun. Python: uv. Rust: cargo. Go: go.
- Search: FFF and tgrep.
- JS/TS lint: Use Oxlint with the vendored anti-slop plugin (`tools/oxlint/anti-slop/`). If a repo does not have it, install it with [$install-anti-slop](file:///C:/Users/hi/Desktop/skills/install-anti-slop/SKILL.md). Run Oxlint before you report done.
- Lint feedback loop: When you find a code-quality defect that a lint rule can catch, do not only fix it. Add a rule to the repo's Oxlint config, or write a new anti-slop rule in `tools/oxlint/anti-slop/rules/` if no rule exists. Then fix all violations. Tell the owner which rule you added.
- Mobile and Mac testing: Use Revyl CLI exclusively for mobile app testing, simulators, and Mac testing.
- Skills: Master skills live at [Desktop/skills](file:///C:/Users/hi/Desktop/skills) (mirrored in `.agents/skills`). Every agent should invoke the relevant skill for specialized tasks.
