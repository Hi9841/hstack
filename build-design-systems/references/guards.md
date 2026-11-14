# Guards

Pick the guards that this product needs. Each one is a test or a check step that the one check command runs.
Prove each one: break it on purpose, see red, revert.

## Token drift

- Each generated file (CSS variables, a Rust or Swift module, a theme JSON) is compared with a fresh run of the
  generator. A difference fails and names the generate command.
- A theme file that a renderer loads (a third-party theme format, a platform asset) is compared with the
  token file, token by token.
- A copy of the token file anywhere else fails.

## No literals

- A test reads the component and story sources, code only (drop comments), and fails on a hex colour, an
  `rgb(`/`rgba(` call, or a named white or black. Match whole words: a call that converts a colour is not a
  literal. Test files may hold colours.
- On a JS or TS product, write this as an Oxlint rule (anti-slop plugin) instead of a test, so the editor shows it.

## Ratchets

A ratchet counts a bad pattern per file and only lets the count go down. Use it when the old code has many
cases and a full clean-up is not the task.

- The file is committed, one line per file: `path<TAB>count`. Sort it, so a diff is easy to read.
- The check fails when a count goes up or a new file appears with a count. The error names the file, the count,
  the pattern and the fix (the named style or token to use).
- `--update` writes the lower counts. It refuses to write a higher one.
- Good patterns to count: a hand-set text size, line height, weight or font face outside the named type styles;
  a hand-set radius or spacing; a hand-built list row where a shared table or row part exists.

## Gallery self-tests

- Every story is in exactly one group, and no group is empty.
- Search finds a story by part of its name, and Enter opens the first match.
- Every component in the inventory has a story.
- The gallery's own layout holds in a small window (the theme picker stays in view, the list scrolls).
- Tests find elements by stable ids (`nav-row-<story>`, `theme-picker`), never by position or by text that
  changes.

## Component inventory

A manifest (JSON) lists each component: id, name, kind, group, the platforms that draw it, its page in the
design tool, its props, slots and states. A check fails when a component in code has no entry, when an entry
has no code, or when a platform has no part and the entry does not say why.

## Parity between renderers

Use this only when two renderers draw the same part (a desktop app and a website). Each renderer draws the part
in a window of fixed size and writes the boxes of its named regions as JSON (`{"name": [x, y, w, h]}`). The
check compares the two with a small tolerance and names each region that differs.

## Reference pictures

- Build from the commit under test, not from the files in the folder, so a loose edit cannot pass or fail it.
- Write the new pictures to a scratch folder and compare them there; only `--update` writes the committed folder.
- Name pictures `<page-slug>-<theme>.png`.
- Write and compare them on one named machine. A picture from another machine (another GPU, font hinting or
  screen scale) is not a reference.
