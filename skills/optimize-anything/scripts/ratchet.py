#!/usr/bin/env python
"""One-way performance budgets. A number may fall forever and rise never.

Budget file (checked in, one JSON object):

    {
      "render/commits-per-interaction": {"value": 42, "unit": "commits"},
      "bundle/transfer-bytes": {"value": 180000, "unit": "bytes"}
    }

Usage:
    ratchet.py check --budget perf-budget.json --metric bundle/transfer-bytes \
        --command "node scripts/size.mjs"
    ratchet.py check --budget perf-budget.json --metric bundle/transfer-bytes \
        --value 171000 --update
    ratchet.py set   --budget perf-budget.json --metric bundle/transfer-bytes --value 171000
    ratchet.py list  --budget perf-budget.json

Exit codes: 0 pass, 1 regression, 2 usage or IO error.
stdout: structured key/value lines, or --json. stderr: unused.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

PROG = "ratchet"


def fail(message: str, code: int = 2) -> "None":
    print(f"error: {message}")
    print(f"hint: run '{PROG} --help' for usage")
    raise SystemExit(code)


def load_budget(path: pathlib.Path) -> dict:
    if not path.exists():
        fail(f"budget file not found: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"budget file is not valid JSON: {path}: {exc}")
    if not isinstance(data, dict):
        fail(f"budget file must be a JSON object of metric entries: {path}")
    return data


def save_budget(path: pathlib.Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def tidy(value: float) -> float | int:
    """Keep integral budgets integral so the checked-in file reads cleanly."""
    return int(value) if float(value).is_integer() else value


def parse_number(raw: str) -> float:
    try:
        return float(raw.strip().split()[-1])
    except (ValueError, IndexError):
        fail(f"could not read a number out of: {raw!r}")


def measure(command: str) -> float:
    try:
        done = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=900
        )
    except subprocess.TimeoutExpired:
        fail(f"measure command timed out after 900s: {command}")
    if done.returncode != 0:
        tail = (done.stderr or done.stdout or "").strip().splitlines()[-5:]
        fail(
            f"measure command exited {done.returncode}: {command}\n"
            + "\n".join(f"  {line}" for line in tail)
        )
    lines = [line for line in done.stdout.strip().splitlines() if line.strip()]
    if not lines:
        fail(f"measure command printed nothing: {command}")
    return parse_number(lines[-1])


def emit(payload: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, sort_keys=True))
        return
    for key, value in payload.items():
        if value is not None:
            print(f"{key.replace('_', ' ')}: {value}")


def cmd_check(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.budget)
    budget = load_budget(path)
    name = args.metric
    entry = budget.get(name)
    if entry is None:
        fail(
            f"no budget for metric {name!r} in {path}\n"
            f"hint: {PROG} set --budget {path} --metric {name} --value <current>"
        )
    if "value" not in entry:
        fail(f"budget entry for {name!r} has no 'value': {entry}")

    limit = float(entry["value"])
    unit = entry.get("unit", "")
    current = measure(args.command) if args.command else float(args.value)
    tolerance = limit * (args.tolerance / 100.0)

    if current > limit + tolerance:
        delta = current - limit
        pct = (delta / limit * 100.0) if limit else float("inf")
        emit(
            {
                "status": "fail",
                "metric": name,
                "budget": f"{limit:g} {unit}".strip(),
                "current": f"{current:g} {unit}".strip(),
                "over_by": f"{delta:g} ({pct:.1f}%)",
                "next": "fix the regression; do not raise the budget to make CI green",
            },
            args.json,
        )
        return 1

    tightened = False
    if current < limit and args.update:
        budget[name] = {
            "value": tidy(current),
            **({"unit": unit} if unit else {}),
            "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "reason": entry.get("reason", "ratcheted"),
        }
        save_budget(path, budget)
        tightened = True

    pct = ((current - limit) / limit * 100.0) if limit else 0.0
    emit(
        {
            "status": "pass",
            "metric": name,
            "budget": f"{limit:g} {unit}".strip(),
            "current": f"{current:g} {unit}".strip(),
            "change": f"{pct:+.1f}%",
            "ratcheted": tightened,
            "file": str(path) if tightened else None,
        },
        args.json,
    )
    return 0


def cmd_set(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.budget)
    budget = load_budget(path) if path.exists() else {}
    previous = budget.get(args.metric, {}).get("value")
    entry = {
        "value": tidy(args.value),
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }
    if args.unit:
        entry["unit"] = args.unit
    if args.reason:
        entry["reason"] = args.reason
    budget[args.metric] = entry
    save_budget(path, budget)
    emit(
        {
            "status": "set",
            "metric": args.metric,
            "previous": previous,
            "budget": f"{float(args.value):g}",
            "file": str(path),
        },
        args.json,
    )
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.budget)
    budget = load_budget(path)
    if not budget:
        emit({"status": "empty", "metrics": 0, "file": str(path)}, args.json)
        return 0
    if args.json:
        print(json.dumps(budget, indent=2, sort_keys=True))
        return 0
    print(f"metrics: {len(budget)}")
    for name in sorted(budget):
        entry = budget[name]
        value = f"{float(entry['value']):g}" if "value" in entry else "?"
        unit = entry.get("unit", "")
        print(f"  {name}: {value} {unit}".rstrip())


def main() -> int:
    parser = argparse.ArgumentParser(prog=PROG, add_help=True)
    parser.add_argument("--json", action="store_true", help="emit JSON instead of key/value lines")
    subs = parser.add_subparsers(dest="cmd", required=True)

    check = subs.add_parser("check", help="compare a measurement to its budget")
    check.add_argument("--budget", required=True)
    check.add_argument("--metric", required=True)
    check.add_argument("--value", type=float, help="use this number instead of measuring")
    check.add_argument("--command", help="shell command whose last stdout line is the number")
    check.add_argument(
        "--tolerance", type=float, default=0.0, help="percent above budget still allowed"
    )
    check.add_argument(
        "--update", action="store_true", help="lower the ceiling when the number improved"
    )
    check.set_defaults(func=cmd_check)

    setter = subs.add_parser("set", help="set or loosen a budget (needs a reason)")
    setter.add_argument("--budget", required=True)
    setter.add_argument("--metric", required=True)
    setter.add_argument("--value", type=float, required=True)
    setter.add_argument("--unit")
    setter.add_argument("--reason", help="why the budget moves; required to loosen")
    setter.set_defaults(func=cmd_set)

    lister = subs.add_parser("list", help="show every budget")
    lister.add_argument("--budget", required=True)
    lister.set_defaults(func=cmd_list)

    args = parser.parse_args()
    if args.cmd == "check" and args.value is None and not args.command:
        fail("check needs --value or --command")
    if args.cmd == "set" and not args.reason:
        previous = None
        if pathlib.Path(args.budget).exists():
            previous = json.loads(pathlib.Path(args.budget).read_text(encoding="utf-8")).get(
                args.metric, {}
            ).get("value")
        if previous is not None and float(args.value) > float(previous):
            fail(
                f"loosening a budget needs --reason (was {previous:g}, now {args.value:g})\n"
                "hint: prefer leaving the ceiling in place and fixing the regression"
            )
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
