# Hstack

Private skill stack. Each skill is one folder with a SKILL.md.

pstack and gstack stay upstream. This repo is not a fork of either.

## Install

```powershell
git clone https://github.com/Hi9841/hstack.git
cd hstack
powershell -NoProfile -File .\scripts\install.ps1
```

The script links each skill into `Desktop\Skills` when that folder exists. On this machine Grok, Codex, Cursor, Claude, and `.agents` all read that folder, so one install covers every host.

One skill:

```powershell
powershell -NoProfile -File .\scripts\install.ps1 -Only bro
```

Status, without changes:

```powershell
powershell -NoProfile -File .\scripts\install.ps1 -List
```

`grill-with-docs-ui`, `how-to-choose-an-llm`, and `migration-kit` keep their own git checkouts. The script does not replace those.
