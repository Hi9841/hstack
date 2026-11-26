#!/usr/bin/env python
"""Summarize a V8/JSC .cpuprofile (Chrome DevTools format) as text.

Prints total, attributed, and unattributed profile time, then top functions by self time,
top functions by inclusive (total) time, and self time grouped by full source URL.

Usage:
    python cpuprofile.py PROFILE.cpuprofile [--top 25] [--filter TEXT] [--focus TEXT]

--filter and --focus match against the full function name and source URL before display
shortening, so distinct files with the same basename never collide. Times are in ms.
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
    parts = [p for p in url.split("/") if p]
    if len(parts) >= 2:
        return f"{parts[-2]}/{parts[-1]}"
    return parts[-1] if parts else url


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("profile")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--filter", default=None)
    ap.add_argument("--focus", default=None, help="show callees below the first frame whose full label matches")
    args = ap.parse_args()

    with open(args.profile, encoding="utf-8") as fh:
        prof = json.load(fh)

    raw_nodes = prof.get("nodes")
    if not isinstance(raw_nodes, list) or not raw_nodes:
        print("error: profile has no valid nodes array")
        return 1

    nodes = {n["id"]: n for n in raw_nodes if isinstance(n, dict) and "id" in n}
    parent: dict[int, int] = {}
    for n in nodes.values():
        for child in n.get("children", []):
            parent[child] = n["id"]

    samples = prof.get("samples", [])
    deltas = prof.get("timeDeltas", [])
    if not isinstance(samples, list) or not samples:
        print("error: profile has no samples")
        return 1
    if not isinstance(deltas, list):
        print("error: profile has invalid timeDeltas")
        return 1

    missing_nodes = [sid for sid in samples if sid not in nodes]
    if missing_nodes:
        print(f"error: {len(missing_nodes)} samples reference unknown node IDs (first: {missing_nodes[0]})")
        return 1

    n_samples = len(samples)
    if len(deltas) < n_samples:
        print(
            f"warning: timeDeltas ({len(deltas)}) shorter than samples ({n_samples}); "
            "missing deltas treated as 0"
        )
        deltas = list(deltas) + [0] * (n_samples - len(deltas))

    start_time = prof.get("startTime", 0) or 0
    end_time = prof.get("endTime", 0) or 0
    span_us = max(0, end_time - start_time) if (end_time > start_time) else 0
    deltas_sum = sum(max(0, d) for d in deltas[:n_samples])

    # In DevTools .cpuprofile, deltas[0] precedes sample[0], and deltas[i+1] spans sample[i] -> sample[i+1].
    # Attribute any remaining tail (span_us - deltas_sum) to the final sample.
    durations: list[float] = [0.0] * n_samples
    for i in range(n_samples - 1):
        durations[i] = max(0.0, float(deltas[i + 1]))
    tail_us = max(0.0, float(span_us - deltas_sum)) if span_us > 0 else 0.0
    if n_samples == 1 and tail_us == 0.0 and deltas[0] > 0:
        durations[0] = float(deltas[0])
    else:
        durations[n_samples - 1] = tail_us

    attributed_us = sum(durations)
    total_us = float(span_us) if span_us > 0 else max(attributed_us, float(deltas_sum))
    unattributed_us = max(0.0, total_us - attributed_us)
    if total_us <= 0:
        print("error: profile has zero measurable duration")
        return 1

    # Aggregate by full identity (name, full URL, line, column) before display shortening.
    def full_key(node_id: int) -> tuple[str, str, int, int]:
        cf = nodes[node_id].get("callFrame", {})
        name = cf.get("functionName") or "(anonymous)"
        url = (cf.get("url") or "").replace("\\", "/")
        line = int(cf.get("lineNumber", -1)) + 1
        col = int(cf.get("columnNumber", -1)) + 1
        return (name, url, line, col)

    def full_text(key: tuple[str, str, int, int]) -> str:
        name, url, line, col = key
        loc = f"{url or '(native)'}:{line}" + (f":{col}" if col > 0 else "")
        return f"{name} [{loc}]"

    def display_func(key: tuple[str, str, int, int], ambiguous_short: set[str]) -> str:
        name, url, line, col = key
        shown_url = url if short_url(url) in ambiguous_short else short_url(url)
        loc = f"{shown_url}:{line}" + (f":{col}" if col > 0 else "")
        return f"{name}  [{loc}]"

    self_us: dict[tuple[str, str, int, int], float] = defaultdict(float)
    incl_us: dict[tuple[str, str, int, int], float] = defaultdict(float)
    file_us: dict[str, float] = defaultdict(float)
    focus_us: dict[tuple[str, str, int, int], float] = defaultdict(float)
    focus_total = 0.0
    idle_names = {"(idle)", "(program)", "(garbage collector)", "(root)"}

    for node_id, dur in zip(samples, durations):
        if dur <= 0:
            continue
        k = full_key(node_id)
        self_us[k] += dur
        fname = k[0]
        furl = k[1]
        file_bucket = fname if fname in idle_names else (furl or "(native)")
        file_us[file_bucket] += dur

        seen: set[tuple[str, str, int, int]] = set()
        stack: list[tuple[str, str, int, int]] = []
        cur: int | None = node_id
        while cur is not None:
            ck = full_key(cur)
            stack.append(ck)
            if ck not in seen:
                seen.add(ck)
                incl_us[ck] += dur
            cur = parent.get(cur)

        if args.focus:
            hits = [i for i, ck in enumerate(stack) if args.focus in full_text(ck)]
            if hits:
                focus_total += dur
                for ck in set(stack[: hits[-1]]):
                    focus_us[ck] += dur

    # Detect distinct full URLs that collide under short_url so display stays unambiguous.
    short_to_full: dict[str, set[str]] = defaultdict(set)
    for url in file_us:
        if url not in idle_names:
            short_to_full[short_url(url)].add(url)
    ambiguous_short = {s for s, fulls in short_to_full.items() if len(fulls) > 1}

    def show_files() -> None:
        print("\n== self time by file/package")
        rows = sorted(file_us.items(), key=lambda kv: kv[1], reverse=True)
        if args.filter:
            rows = [r for r in rows if args.filter in r[0]]
        for url, us in rows[: args.top]:
            shown = url if (url in idle_names or short_url(url) in ambiguous_short) else short_url(url)
            print(f"{us / 1000:9.1f} ms  {us / total_us * 100:5.1f}%  {shown}")

    def show_funcs(title: str, table: dict[tuple[str, str, int, int], float], flt: str | None = None) -> None:
        print(f"\n== {title}")
        rows = sorted(table.items(), key=lambda kv: kv[1], reverse=True)
        if flt:
            rows = [r for r in rows if flt in full_text(r[0])]
        for k, us in rows[: args.top]:
            print(f"{us / 1000:9.1f} ms  {us / total_us * 100:5.1f}%  {display_func(k, ambiguous_short)}")

    print(f"profile: {args.profile}")
    print(
        f"total {total_us / 1000:.1f} ms  attributed {attributed_us / 1000:.1f} ms  "
        f"unattributed {unattributed_us / 1000:.1f} ms  samples {n_samples}"
    )
    show_files()
    show_funcs("self time by function", self_us, args.filter)
    show_funcs("inclusive time by function", incl_us, args.filter)
    if args.focus:
        show_funcs(f"callees of '{args.focus}' (total {focus_total / 1000:.1f} ms)", focus_us)
    return 0


if __name__ == "__main__":
    sys.exit(main())
