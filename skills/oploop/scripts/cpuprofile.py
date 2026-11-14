#!/usr/bin/env python
"""Summarize a V8/JSC .cpuprofile (Chrome DevTools format) as text.

Prints total profile time, then the top functions by self time, the top functions by
inclusive (total) time, and self time grouped by source file or package.

Usage:
    python cpuprofile.py PROFILE.cpuprofile [--top 25] [--filter TEXT]

--filter keeps only frames whose function name or URL contains TEXT (inclusive view).
Times are in milliseconds. Self time is time in the function body. Inclusive time is
self time plus time in all callees, counted once per stack, so recursion does not
double count.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict


def short_url(url: str) -> str:
    if not url:
        return "(native)"
    url = url.replace("\\", "/")
    match = re.search(r"node_modules/(?:\.bun/[^/]+/node_modules/)?((?:@[^/]+/)?[^/]+)", url)
    if match:
        return "pkg:" + match.group(1)
    match = re.search(r"packages/([^/]+)/(.*)$", url)
    if match:
        return f"{match.group(1)}/{match.group(2)}"
    return url.rsplit("/", 1)[-1] or url


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("profile")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--filter", default=None)
    ap.add_argument("--focus", default=None, help="show callees below the first frame whose label contains this text")
    args = ap.parse_args()

    with open(args.profile, encoding="utf-8") as fh:
        prof = json.load(fh)
    nodes = {n["id"]: n for n in prof["nodes"]}
    parent: dict[int, int] = {}
    for n in prof["nodes"]:
        for child in n.get("children", []):
            parent[child] = n["id"]

    samples = prof.get("samples", [])
    deltas = prof.get("timeDeltas", [])
    if not samples:
        print("profile has no samples")
        return 1
    # Each sample's duration is the delta to the next sample, in microseconds.
    durations = [deltas[i + 1] if i + 1 < len(deltas) else 0 for i in range(len(samples))]
    total_us = (prof.get("endTime", 0) - prof.get("startTime", 0)) or sum(durations)

    def label(node_id: int) -> str:
        cf = nodes[node_id]["callFrame"]
        name = cf.get("functionName") or "(anonymous)"
        return f"{name}  [{short_url(cf.get('url', ''))}:{cf.get('lineNumber', -1) + 1}]"

    self_us: dict[str, float] = defaultdict(float)
    incl_us: dict[str, float] = defaultdict(float)
    file_us: dict[str, float] = defaultdict(float)
    focus_us: dict[str, float] = defaultdict(float)
    focus_total = 0.0
    idle_names = {"(idle)", "(program)", "(garbage collector)", "(root)"}
    for node_id, dur in zip(samples, durations):
        if dur <= 0:
            continue
        cf = nodes[node_id]["callFrame"]
        self_us[label(node_id)] += dur
        file_us[short_url(cf.get("url", "")) if cf.get("functionName") not in idle_names else cf.get("functionName")] += dur
        seen = set()
        stack = []
        cur = node_id
        while cur is not None:
            key = label(cur)
            stack.append(key)
            if key not in seen:
                seen.add(key)
                incl_us[key] += dur
            cur = parent.get(cur)
        if args.focus:
            # stack is leaf-first; find the outermost frame that matches, count frames below it.
            hits = [i for i, key in enumerate(stack) if args.focus in key]
            if hits:
                focus_total += dur
                for key in set(stack[: hits[-1]]):
                    focus_us[key] += dur

    def show(title: str, table: dict[str, float], flt: str | None = None) -> None:
        print(f"\n== {title}")
        rows = sorted(table.items(), key=lambda kv: kv[1], reverse=True)
        if flt:
            rows = [r for r in rows if flt in r[0]]
        for key, us in rows[: args.top]:
            print(f"{us / 1000:9.1f} ms  {us / total_us * 100:5.1f}%  {key}")

    print(f"profile: {args.profile}")
    print(f"total {total_us / 1000:.1f} ms, samples {len(samples)}")
    show("self time by file/package", file_us)
    show("self time by function", self_us)
    show("inclusive time by function", incl_us, args.filter)
    if args.focus:
        show(f"callees of '{args.focus}' (total {focus_total / 1000:.1f} ms)", focus_us)
    return 0


if __name__ == "__main__":
    sys.exit(main())
