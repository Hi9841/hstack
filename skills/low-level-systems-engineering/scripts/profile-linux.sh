#!/usr/bin/env bash
set -euo pipefail

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 command [args...] (runs application twice)" >&2
  exit 2
fi
if ! command -v perf >/dev/null 2>&1; then
  echo 'perf was not found. Install linux perf tools for your kernel.' >&2
  exit 2
fi

printf '%s\n' '== perf stat: repeated hardware events =='
perf stat -r 5 -e cycles,instructions,branches,branch-misses,cache-misses -- "$@"
printf '%s\n' '== perf record: sampled stacks =='
perf record -o perf.data -g --call-graph dwarf -- "$@"
printf '%s\n' 'Open perf.data using: perf report -i perf.data'
printf '%s\n' 'Warning: these counters vary across microarchitectures, and profiling can perturb timing.'
