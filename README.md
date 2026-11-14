# hstack

Hi's agent skills and global `AGENTS.md`. Each skill is a plain [Agent Skill](https://agentskills.io) folder: `skills/<name>/SKILL.md`.

## Install on a new machine

Use one of these commands. Each command needs Node.js 20 or later and GitHub access to this private repo.

```bash
npx github:Hi9841/hstack
bunx github:Hi9841/hstack
pnpm dlx github:Hi9841/hstack
```

The installer does these steps:

1. It copies `AGENTS.md` to your home folder (`%USERPROFILE%\AGENTS.md`). If an older, different `AGENTS.md` is there, it keeps a copy as `AGENTS.md.bak`. It changes the `C:/Users/hi/` links to your home folder.
2. It copies all skills and `agents/` to `%USERPROFILE%\Desktop\skills`. It overwrites files with the same name. It does not delete other files.

Options: `--list` shows the skills. `--dry-run` shows what the installer will copy, but copies nothing.

If you have a clone of the repo, double-click `install.cmd`. It runs the same installer.

To install only some skills into Claude Code, Codex, Cursor or other agents, use the [skills CLI](https://skills.sh):

```bash
npx skills add Hi9841/hstack
```

## Layout

| Path | Contents |
|---|---|
| `skills/` | One folder for each skill |
| `agents/` | Agent persona files |
| `AGENTS.md` | Global working preferences for all repos |
| `bin/hstack.mjs` | The installer (no dependencies) |
| `install.cmd` | Double-click wrapper for the installer |

## Skills

- [`12-yos-agent`](skills/12-yos-agent/SKILL.md)
- [`abuse-fraud-review`](skills/abuse-fraud-review/SKILL.md)
- [`audit-agents`](skills/audit-agents/SKILL.md)
- [`audit-animations`](skills/audit-animations/SKILL.md)
- [`axi`](skills/axi/SKILL.md)
- [`benchmark-checklist`](skills/benchmark-checklist/SKILL.md)
- [`blast-radius`](skills/blast-radius/SKILL.md)
- [`break-ui`](skills/break-ui/SKILL.md)
- [`build-design-systems`](skills/build-design-systems/SKILL.md)
- [`build-gpui-apps`](skills/build-gpui-apps/SKILL.md)
- [`choose-llm`](skills/choose-llm/SKILL.md)
- [`choose-stacks`](skills/choose-stacks/SKILL.md)
- [`code-migration`](skills/code-migration/SKILL.md)
- [`cpp-guide`](skills/cpp-guide/SKILL.md)
- [`create-verification-skill`](skills/create-verification-skill/SKILL.md)
- [`domain-modeling`](skills/domain-modeling/SKILL.md)
- [`emil-design-eng`](skills/emil-design-eng/SKILL.md)
- [`eval-skills`](skills/eval-skills/SKILL.md)
- [`explore-unknowns`](skills/explore-unknowns/SKILL.md)
- [`fluid-functionalism`](skills/fluid-functionalism/SKILL.md)
- [`gestures`](skills/gestures/SKILL.md)
- [`grill-with-docs-ui`](skills/grill-with-docs-ui/SKILL.md)
- [`grilling`](skills/grilling/SKILL.md)
- [`ian-xhs-carousel`](skills/ian-xhs-carousel/SKILL.md)
- [`ian-xiaohei-illustrations`](skills/ian-xiaohei-illustrations/SKILL.md)
- [`ian-xiaohei-scenes`](skills/ian-xiaohei-scenes/SKILL.md)
- [`low-level-systems-engineering`](skills/low-level-systems-engineering/SKILL.md)
- [`maintain-verification-skill`](skills/maintain-verification-skill/SKILL.md)
- [`mobile-native`](skills/mobile-native/SKILL.md)
- [`native-feel-cross-platform-desktop`](skills/native-feel-cross-platform-desktop/SKILL.md)
- [`oploop`](skills/oploop/SKILL.md)
- [`optimize-anything`](skills/optimize-anything/SKILL.md)
- [`planning-with-files`](skills/planning-with-files/SKILL.md)
- [`pr`](skills/pr/SKILL.md)
- [`principle-fix-root-causes`](skills/principle-fix-root-causes/SKILL.md)
- [`principle-foundational-thinking`](skills/principle-foundational-thinking/SKILL.md)
- [`principle-laziness-protocol`](skills/principle-laziness-protocol/SKILL.md)
- [`principle-prove-it-works`](skills/principle-prove-it-works/SKILL.md)
- [`principle-subtract-before-you-add`](skills/principle-subtract-before-you-add/SKILL.md)
- [`principle-type-system-discipline`](skills/principle-type-system-discipline/SKILL.md)
- [`prototype`](skills/prototype/SKILL.md)
- [`rossark-motion-skill`](skills/rossark-motion-skill/SKILL.md)
- [`security-audit`](skills/security-audit/SKILL.md)
- [`simplified-technical-english`](skills/simplified-technical-english/SKILL.md)
- [`stack-diagram`](skills/stack-diagram/SKILL.md)
- [`teach-duo`](skills/teach-duo/SKILL.md)
- [`typescript-best-practices`](skills/typescript-best-practices/SKILL.md)
- [`unslop`](skills/unslop/SKILL.md)
- [`untangle-codebase`](skills/untangle-codebase/SKILL.md)
- [`write-skills`](skills/write-skills/SKILL.md)
- [`write-spec`](skills/write-spec/SKILL.md)
- [`writing-for-agents`](skills/writing-for-agents/SKILL.md)
