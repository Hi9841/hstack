---
name: setup
description: Install Hstack skills into the shared skills folder. Use when the user says install Hstack, set up Hstack, or add one Hstack skill.
disable-model-invocation: true
---

# Setup

Install skills from this repo into the folder the agents already read.

## Install

From the repo root:

```powershell
powershell -NoProfile -File .\scripts\install.ps1
```

That links every skill folder. On this machine Grok, Codex, Cursor, Claude, and `.agents` all read `Desktop\Skills`, so one link installs every host.

## One skill

```powershell
powershell -NoProfile -File .\scripts\install.ps1 -Only bro
```

## Status

```powershell
powershell -NoProfile -File .\scripts\install.ps1 -List
```

`-List` and `-DryRun` change nothing.

## Leave these alone

`grill-with-docs-ui`, `how-to-choose-an-llm`, and `migration-kit` have their own git checkouts in the skills folder. The script does not replace those. They are already installed from those checkouts.

If a folder differs from this repo and is not a git checkout, the script leaves it and reports `differs`. Do not delete it.

## Categories

Categories are not defined. If the user asks to install a category, say that, then list the folder names. Do not invent groups.
