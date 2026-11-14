#!/usr/bin/env python3
"""Smoke test bundled scripts using a tiny deterministic Python subprocess."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).parent


def call(*args):
    completed = subprocess.run([sys.executable, str(HERE / args[0]), *map(str, args[1:])],
                               capture_output=True, text=True, check=False)
    if completed.returncode:
        raise AssertionError(f'{args[0]} failed:\n{completed.stdout}\n{completed.stderr}')
    return completed.stdout


def main():
    with tempfile.TemporaryDirectory() as folder:
        base = Path(folder) / 'base.json'
        new = Path(folder) / 'new.json'
        call('bench.py', '--warmups', '0', '--rounds', '3', '--output', base,
             '--verify-stdout', '--', sys.executable, '-c', 'print(42)')
        call('bench.py', '--warmups', '0', '--rounds', '3', '--output', new,
             '--verify-stdout', '--', sys.executable, '-c', 'print(42)')
        assert len(json.loads(base.read_text())['samples_ms']) == 3
        call('compare_bench.py', base, new, '--resamples', '100')
        call('roofline.py', '--operations', '2e9', '--bytes', '1e9',
             '--peak-ops-per-second', '1e12', '--bandwidth-bytes-per-second', '1e11')
        input_path = Path(folder) / 'input.txt'
        input_path.write_text('sample', encoding='utf-8')
        # Both programs read file and print the same output; exact text differential.
        template = (f'"{sys.executable}" -c "import sys;print(open(sys.argv[1]).read())" {{input}}')
        call('correctness.py', '--reference', template, '--candidate', template, '--case', input_path)
        call('check-skill.py')
    print('OK: bundled Python scripts passed smoke tests.')


if __name__ == '__main__':
    main()
