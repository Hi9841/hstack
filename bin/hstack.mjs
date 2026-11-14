#!/usr/bin/env node
// Installs hstack on this machine:
//   AGENTS.md         -> <home>/AGENTS.md
//   skills/*, agents/ -> <home>/Desktop/skills/
// Files with the same name are overwritten. Other files in the target are kept.

import { cpSync, existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const home = homedir();
const skillsDest = join(home, "Desktop", "skills");
const dryRun = args.includes("--dry-run");

if (args.includes("--help") || args.includes("-h")) {
  console.log(`hstack - install Hi's skills and global AGENTS.md

usage: hstack [--list] [--dry-run]

  (no flag)   copy AGENTS.md to ${home}
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

// The source AGENTS.md links to C:/Users/hi/... Point those links at this machine's home.
const agentsMd = readFileSync(join(root, "AGENTS.md"), "utf8").replaceAll(
  "C:/Users/hi/",
  `${home.replaceAll("\\", "/")}/`,
);
const agentsMdDest = join(home, "AGENTS.md");
if (existsSync(agentsMdDest) && readFileSync(agentsMdDest, "utf8") !== agentsMd) {
  console.log(`backup  ${agentsMdDest}.bak`);
  if (!dryRun) cpSync(agentsMdDest, `${agentsMdDest}.bak`);
}
console.log(`copy    AGENTS.md -> ${agentsMdDest}`);
if (!dryRun) writeFileSync(agentsMdDest, agentsMd);

if (!dryRun) mkdirSync(skillsDest, { recursive: true });
for (const name of [...skills.map((skill) => join("skills", skill)), "agents"]) {
  const target = join(skillsDest, name.replace(/^skills[\\/]/, ""));
  if (!dryRun) cpSync(join(root, name), target, { recursive: true, force: true });
}
console.log(`copy    ${skills.length} skills + agents/ -> ${skillsDest}`);
console.log(dryRun ? "dry run: nothing copied" : "done");
