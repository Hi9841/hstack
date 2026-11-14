#!/usr/bin/env python
# /// script
# requires-python = ">=3.10"
# dependencies = ["psutil>=5.9"]
# ///
"""Interleaved A/B benchmark for OpLoop.

Runs side A and side B in alternating order (A B A B ...), so that warmup, caches,
and drift affect both sides equally. For each run it records wall time, peak RSS of
the full process tree (sampled), and the exit status.

A run ends when one of these occurs:
  - the process exits                       (default)
  - a line of output matches --ready REGEX  (programs that do not exit: TUI, server)
  - --hold SECONDS pass                     (idle memory: sample, then stop)
  - --timeout SECONDS pass                  (counted as an error)

Usage:
    uv run bench.py --name J1-startup --a "bun run dev --version" --a-cwd ../baseline \
        --b "bun run dev --version" --b-cwd ../work --runs 10 --warmup 2
    uv run bench.py --name J2-serve --a "..." --b "..." --ready "listening on"
    uv run bench.py --name J3-idle --a "..." --b "..." --hold 20 --metric rss

Exit codes: 0 done, 1 a side had errors, 2 usage error.
stdout: one summary block. --out FILE appends one JSON line per side per call.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import queue
import re
import shlex
import statistics
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone

import psutil

SAMPLE_INTERVAL_S = 0.01


def tree_rss(proc: psutil.Process) -> int:
    """Sum RSS over the process and all its descendants. Processes may exit mid-scan."""
    total = 0
    try:
        procs = [proc, *proc.children(recursive=True)]
    except psutil.Error:
        return 0
    for p in procs:
        try:
            total += p.memory_info().rss
        except psutil.Error:
            pass
    return total


def kill_tree(proc: psutil.Process) -> None:
    try:
        procs = [*proc.children(recursive=True), proc]
    except psutil.Error:
        procs = [proc]
    for p in procs:
        try:
            p.kill()
        except psutil.Error:
            pass
    psutil.wait_procs(procs, timeout=5)


def pump(stream, lines: queue.Queue) -> None:
    for raw in iter(stream.readline, b""):
        lines.put(raw.decode("utf-8", errors="replace"))
    lines.put(None)


def run_once(cmd: list[str] | str, cwd: str | None, env: dict, args) -> dict:
    ready = re.compile(args.ready) if args.ready else None
    start = time.perf_counter()
    popen = subprocess.Popen(
        cmd,
        cwd=cwd,
        env=env,
        shell=args.shell,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    proc = psutil.Process(popen.pid)
    lines: queue.Queue = queue.Queue()
    threading.Thread(target=pump, args=(popen.stdout, lines), daemon=True).start()

    peak = 0
    end_reason = "exit"
    tail: list[str] = []
    while True:
        peak = max(peak, tree_rss(proc))
        elapsed = time.perf_counter() - start
        try:
            while True:
                line = lines.get_nowait()
                if line is None:
                    break
                tail = (tail + [line])[-20:]
                if ready and ready.search(line):
                    end_reason = "ready"
                    break
        except queue.Empty:
            pass
        if end_reason == "ready":
            break
        if popen.poll() is not None:
            break
        if args.hold and elapsed >= args.hold:
            end_reason = "hold"
            break
        if elapsed >= args.timeout:
            end_reason = "timeout"
            break
        time.sleep(SAMPLE_INTERVAL_S)

    wall_ms = (time.perf_counter() - start) * 1000
    if end_reason == "exit":
        code = popen.returncode
        ok = code == 0
    else:
        code = None
        ok = end_reason in ("ready", "hold")
        kill_tree(proc)
    return {
        "wall_ms": wall_ms,
        "peak_rss_mb": peak / (1024 * 1024),
        "ok": ok,
        "end": end_reason,
        "code": code,
        "tail": "".join(tail)[-2000:] if not ok else "",
    }


def mann_whitney_p(a: list[float], b: list[float]) -> float:
    """Two-sided Mann-Whitney U test, normal approximation with tie correction."""
    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        return float("nan")
    pooled = sorted([(v, 0) for v in a] + [(v, 1) for v in b])
    ranks = [0.0] * len(pooled)
    ties = 0.0
    i = 0
    while i < len(pooled):
        j = i
        while j + 1 < len(pooled) and pooled[j + 1][0] == pooled[i][0]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[k] = avg
        t = j - i + 1
        ties += t**3 - t
        i = j + 1
    r1 = sum(r for r, (_, side) in zip(ranks, pooled) if side == 0)
    u1 = r1 - n1 * (n1 + 1) / 2
    mu = n1 * n2 / 2
    n = n1 + n2
    sigma = math.sqrt(n1 * n2 / 12 * ((n + 1) - ties / (n * (n - 1))))
    if sigma == 0:
        return 1.0
    z = (abs(u1 - mu) - 0.5) / sigma
    return math.erfc(max(z, 0) / math.sqrt(2))


def summarize(values: list[float]) -> dict:
    if not values:
        return {"median": float("nan"), "min": float("nan"), "max": float("nan")}
    return {"median": statistics.median(values), "min": min(values), "max": max(values)}


def parse_cmd(text: str, shell: bool):
    return text if shell else shlex.split(text, posix=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True, help="journey ID, for example J1-startup")
    ap.add_argument("--a", required=True, help="command for side A (baseline)")
    ap.add_argument("--b", required=True, help="command for side B (candidate)")
    ap.add_argument("--a-cwd", default=None)
    ap.add_argument("--b-cwd", default=None)
    ap.add_argument("--runs", type=int, default=10, help="measured runs per side")
    ap.add_argument("--warmup", type=int, default=1, help="unmeasured runs per side")
    ap.add_argument("--ready", default=None, help="stop the run when output matches this regex")
    ap.add_argument("--hold", type=float, default=0, help="stop the run after this many seconds (ok)")
    ap.add_argument("--timeout", type=float, default=120, help="stop the run as an error after this many seconds")
    ap.add_argument("--metric", choices=["wall", "rss"], default="wall", help="metric for the verdict")
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--shell", action="store_true", help="run the commands through the system shell")
    ap.add_argument("--env", action="append", default=[], help="KEY=VALUE for both sides (repeatable)")
    ap.add_argument("--out", default=None, help="append JSON lines to this file")
    args = ap.parse_args()

    env = dict(os.environ)
    for item in args.env:
        if "=" not in item:
            print(f"error: --env needs KEY=VALUE, got {item!r}")
            return 2
        key, value = item.split("=", 1)
        env[key] = value

    sides = {
        "A": (parse_cmd(args.a, args.shell), args.a_cwd),
        "B": (parse_cmd(args.b, args.shell), args.b_cwd),
    }
    for _ in range(args.warmup):
        for label in ("A", "B"):
            run_once(*sides[label], env, args)

    results: dict[str, list[dict]] = {"A": [], "B": []}
    for i in range(args.runs):
        order = ("A", "B") if i % 2 == 0 else ("B", "A")
        for label in order:
            results[label].append(run_once(*sides[label], env, args))

    key = "wall_ms" if args.metric == "wall" else "peak_rss_mb"
    unit = "ms" if args.metric == "wall" else "MB"
    stats = {}
    errors = 0
    for label in ("A", "B"):
        good = [r for r in results[label] if r["ok"]]
        bad = [r for r in results[label] if not r["ok"]]
        errors += len(bad)
        stats[label] = {
            "wall": summarize([r["wall_ms"] for r in good]),
            "rss": summarize([r["peak_rss_mb"] for r in good]),
            "ok": len(good),
            "errors": len(bad),
            "values": [r[key] for r in good],
        }
        if bad:
            first = bad[0]
            print(f"[{label}] {len(bad)} failed runs. First: end={first['end']} code={first['code']}")
            if first["tail"]:
                print(f"[{label}] output tail:\n{first['tail']}")

    a_vals, b_vals = stats["A"]["values"], stats["B"]["values"]
    p = mann_whitney_p(a_vals, b_vals)
    a_med = stats["A"]["wall" if args.metric == "wall" else "rss"]["median"]
    b_med = stats["B"]["wall" if args.metric == "wall" else "rss"]["median"]
    change = (b_med - a_med) / a_med * 100 if a_med else float("nan")
    significant = not math.isnan(p) and p < args.alpha
    if errors:
        verdict = "inconclusive (errors)"
    elif not significant:
        verdict = "no measurable difference"
    else:
        verdict = "B faster/smaller" if b_med < a_med else "B slower/larger"

    print(f"journey   {args.name}   metric {args.metric}   runs {args.runs}/side   warmup {args.warmup}")
    for label in ("A", "B"):
        s = stats[label]
        print(
            f"{label}  wall median {s['wall']['median']:.1f} ms  range {s['wall']['min']:.1f}-{s['wall']['max']:.1f}"
            f"   peak rss median {s['rss']['median']:.1f} MB  range {s['rss']['min']:.1f}-{s['rss']['max']:.1f}"
            f"   ok {s['ok']}  errors {s['errors']}"
        )
    print(f"change {change:+.1f}% ({unit})   p={p:.4f}   significant={significant}   verdict: {verdict}")

    if args.out:
        stamp = datetime.now(timezone.utc).isoformat()
        with open(args.out, "a", encoding="utf-8") as fh:
            for label in ("A", "B"):
                s = dict(stats[label])
                s.pop("values")
                fh.write(json.dumps({
                    "time": stamp, "journey": args.name, "side": label,
                    "cmd": args.a if label == "A" else args.b,
                    "cwd": args.a_cwd if label == "A" else args.b_cwd,
                    "metric": args.metric, "runs": args.runs, **s,
                    "change_pct": change, "p": p, "verdict": verdict,
                }) + "\n")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
