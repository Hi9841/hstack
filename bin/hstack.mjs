#!/usr/bin/env node
// Installs hstack on this machine:
//   AGENTS.md         -> <home>/AGENTS.md
//   CLAUDE.md         -> <home>/.claude/CLAUDE.md
//   skills/*, agents/ -> <home>/Desktop/skills/
// Files with the same name are overwritten. Other files in the target are kept.

import { cpSync, existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const home = homedir();
const claudeDest = join(home, ".claude", "CLAUDE.md");
const skillsDest = join(home, "Desktop", "skills");
const dryRun = args.includes("--dry-run");

if (args.includes("--help") || args.includes("-h")) {
  console.log(`hstack - install Hi's skills, AGENTS.md, and CLAUDE.md

usage: hstack [--list] [--dry-run]

  (no flag)   copy AGENTS.md to ${home}
              copy CLAUDE.md to ${claudeDest}
              copy the skills to ${skillsDest}
  --list      show the skills in this package
  --dry-run   show what would be copied, copy nothing`);
  process.exit(0);
}

const skills = readdirSync(join(root, "skills"), { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name)
  .sort();

if (args.includes("--list")) {
  for (const name of skills) console.log(name);
  process.exit(0);
}

// A git checkout on Windows can turn LF into CRLF, so compare and write with LF only.
const readLf = (path) => readFileSync(path, "utf8").replaceAll("\r\n", "\n");

const installTextFile = (label, content, dest) => {
  if (existsSync(dest) && readLf(dest) !== content) {
    console.log(`backup  ${dest}.bak`);
    if (!dryRun) cpSync(dest, `${dest}.bak`);
  }
  console.log(`copy    ${label} -> ${dest}`);
  if (!dryRun) {
    mkdirSync(dirname(dest), { recursive: true });
    writeFileSync(dest, content);
  }
};

// The source AGENTS.md links to C:/Users/hi/... Point those links at this machine's home.
const agentsMd = readLf(join(root, "AGENTS.md")).replaceAll(
  "C:/Users/hi/",
  `${home.replaceAll("\\", "/")}/`,
);
installTextFile("AGENTS.md", agentsMd, join(home, "AGENTS.md"));
installTextFile("CLAUDE.md", readLf(join(root, "CLAUDE.md")), claudeDest);

if (!dryRun) mkdirSync(skillsDest, { recursive: true });
for (const name of [...skills.map((skill) => join("skills", skill)), "agents"]) {
  const target = join(skillsDest, name.replace(/^skills[\\/]/, ""));
  if (!dryRun) cpSync(join(root, name), target, { recursive: true, force: true });
}
console.log(`copy    ${skills.length} skills + agents/ -> ${skillsDest}`);
console.log(dryRun ? "dry run: nothing copied" : "done");
