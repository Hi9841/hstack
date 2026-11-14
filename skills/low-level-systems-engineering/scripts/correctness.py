#!/usr/bin/env python3
"""Exact stdout/return-code differential check over input cases (no shell invocation)."""
import argparse
import hashlib
import shlex
import subprocess
import sys


def run(template, case, timeout):
    # This is intentionally a command string parser, not a shell evaluator.
    argv = [part.replace('{input}', case) for part in shlex.split(template)]
    return subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=timeout, check=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--reference', required=True, help='quoted executable and args, include {input}')
    ap.add_argument('--candidate', required=True, help='quoted executable and args, include {input}')
    ap.add_argument('--case', action='append', required=True, help='input file, repeat for more cases')
    ap.add_argument('--timeout', type=float, default=120)
    ap.add_argument('--compare-stderr', action='store_true')
    args = ap.parse_args()
    if args.timeout <= 0:
        ap.error('timeout must be positive')
    failed = 0
    for case in args.case:
        try:
            baseline = run(args.reference, case, args.timeout)
            candidate = run(args.candidate, case, args.timeout)
        except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
            print(f'FAIL {case}: {exc}')
            failed += 1
            continue
        correct = (baseline.returncode == candidate.returncode
                   and baseline.stdout == candidate.stdout
                   and (not args.compare_stderr or baseline.stderr == candidate.stderr))
        if correct:
            print(f'PASS {case} (stdout sha256={hashlib.sha256(baseline.stdout).hexdigest()[:16]})')
        else:
            print(f'FAIL {case}: return codes {baseline.returncode}/{candidate.returncode}, '
                  f'stdout bytes {len(baseline.stdout)}/{len(candidate.stdout)}')
            failed += 1
    print(f'{len(args.case)-failed}/{len(args.case)} exact-output cases passed')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
