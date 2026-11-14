#!/usr/bin/env python3
"""Validate required skill files and local Markdown links (including references to scripts)."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ['SKILL.md', 'README.md', 'SOURCES.md',
            'examples/trit.md', 'examples/hot-loop-review.md',
            'templates/experiment.md', 'templates/performance-report.md',
            'scripts/bench.py', 'scripts/compare_bench.py', 'scripts/correctness.py',
            'scripts/roofline.py', 'scripts/profile-linux.sh', 'scripts/profile-windows.ps1']
REQUIRED += [f'references/{i:02d}-{name}.md' for i, name in enumerate([
    'performance-workflow', 'performance-models', 'cpu-architecture', 'memory-layout',
    'simd-and-kernels', 'compilers-and-assembly', 'concurrency', 'io-and-systems',
    'benchmarking-profiling', 'correctness-and-security', 'inference-and-numerics'], 1)]
REQUIRED += ['references/annotated-bibliography.md']


def main():
    errors = []
    for f in REQUIRED:
        p = ROOT / f
        if not p.is_file() or p.stat().st_size < 20:
            errors.append(f'Missing or empty: {f}')
    checked = 0
    for md in ROOT.rglob('*.md'):
        content = md.read_text(encoding='utf-8')
        # Ignore external URLs and anchor-only refs; local links must exist.
        for link in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', content):
            link = link.strip().split('#', 1)[0]
            if not link or link.startswith(('http://', 'https://', 'mailto:', 'app://')):
                continue
            if '<' in link or '>' in link:
                continue
            target = (md.parent / unquote(link)).resolve()
            if not target.is_relative_to(ROOT) or not target.exists():
                errors.append(f'Broken link: {md.relative_to(ROOT)} -> {link}')
            checked += 1
    print(f'Checked {len(list(ROOT.rglob("*.md")))} Markdown documents, {checked} local links, {len(REQUIRED)} required paths.')
    for error in errors:
        print('ERROR:', error)
    if errors:
        return 1
    print('OK: skill structure and internal Markdown links are valid.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
