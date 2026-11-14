#!/usr/bin/env python3
"""Small, dependency-free process benchmark. Runs must be comparable; startup is included."""
import argparse
import hashlib
import json
import os
import platform
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone


def percentile(xs, p):
    ordered = sorted(xs)
    if len(ordered) == 1:
        return ordered[0]
    rank = (len(ordered) - 1) * p / 100.0
    low, high = int(rank), min(int(rank) + 1, len(ordered) - 1)
    return ordered[low] * (high - rank) + ordered[high] * (rank - low)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--warmups', type=int, default=3)
    ap.add_argument('--rounds', type=int, default=15)
    ap.add_argument('--timeout', type=float, default=300.0)
    ap.add_argument('--cwd', default=None)
    ap.add_argument('--output', required=True)
    ap.add_argument('--env', action='append', default=[], metavar='NAME=VALUE')
    ap.add_argument('--verify-stdout', action='store_true', help='Require identical stdout across all runs')
    ap.add_argument('command', nargs=argparse.REMAINDER, help='-- executable args...')
    args = ap.parse_args()
    cmd = args.command[1:] if args.command and args.command[0] == '--' else args.command
    if not cmd or args.rounds < 1 or args.warmups < 0 or args.timeout <= 0:
        ap.error('Supply -- executable args; rounds>=1, warmups>=0 and timeout>0')
    env = os.environ.copy()
    for item in args.env:
        if '=' not in item or not item.split('=', 1)[0]:
            ap.error('--env must look like NAME=VALUE')
        key, value = item.split('=', 1)
        env[key] = value
    samples_ms, hashes = [], []
    for i in range(args.warmups + args.rounds):
        start = time.perf_counter_ns()
        try:
            completed = subprocess.run(cmd, cwd=args.cwd, env=env, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, timeout=args.timeout, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            sys.exit(f'Run {i+1} failed: {exc}')
        elapsed_ms = (time.perf_counter_ns() - start) / 1e6
        if completed.returncode:
            sys.exit(f'Run {i+1} returned {completed.returncode}: {completed.stderr.decode(errors="replace")[-3000:]}')
        if i >= args.warmups:
            samples_ms.append(elapsed_ms)
            hashes.append(hashlib.sha256(completed.stdout).hexdigest())
            print(f'run {i-args.warmups+1:>3}/{args.rounds}: {elapsed_ms:.3f} ms', file=sys.stderr)
    if args.verify_stdout and len(set(hashes)) > 1:
        sys.exit('Output varied between measured runs (--verify-stdout). Results were NOT accepted.')
    result = {
        'schema': 'low-level-systems-bench-v1', 'created_utc': datetime.now(timezone.utc).isoformat(),
        'command': cmd, 'cwd': args.cwd or os.getcwd(), 'warmups': args.warmups,
        'rounds': args.rounds, 'platform': platform.platform(),
        'python': platform.python_version(), 'samples_ms': samples_ms,
        'stdout_sha256': hashes if args.verify_stdout else None,
        'summary_ms': {'median': statistics.median(samples_ms), 'mean': statistics.mean(samples_ms),
                       'min': min(samples_ms), 'max': max(samples_ms),
                       'p95': percentile(samples_ms, 95) if len(samples_ms) >= 20 else None,
                       'p99': percentile(samples_ms, 99) if len(samples_ms) >= 100 else None},
        'warning': 'This times the entire process including startup; compare interleaved A/B for rigorous claims.'
    }
    with open(args.output, 'w', encoding='utf-8') as fp:
        json.dump(result, fp, indent=2)
        fp.write('\n')
    print(json.dumps(result['summary_ms'], indent=2))
    print(f'Saved: {args.output}')


if __name__ == '__main__':
    main()
