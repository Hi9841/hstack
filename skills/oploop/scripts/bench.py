#!/usr/bin/env python
# /// script
# requires-python = ">=3.10"
# dependencies = ["psutil>=5.9"]
# ///
"""Counterbalanced block A/B benchmark for OpLoop.

Runs side A and side B in counterbalanced blocks (A B, B A, ...), preserving block IDs
for drift control. Records event-timestamped wall time, sampled peak memory (process
tree RSS or custom --mem-probe), exit code, raw stdout SHA-256, and AC power state.

Completion modes (mutually exclusive):
  - default (exit)     : target must exit with code 0 before --timeout
  - --ready REGEX      : output (stdout or stderr) must match REGEX before exit/timeout
  - --hold SECONDS     : target must stay alive for at least --hold seconds

Validation:
  - --expect REGEX     : raw stdout must match REGEX (stderr never satisfies --expect)
  - --check-eq         : raw stdout SHA-256 must match between A and B per block and
                         within side A, and stdout must be non-empty
  - --mem-cap MIB      : sampled peak memory must stay at or below this MiB limit
  - --require-ac       : check for AC power before the session and around each trial

Note on memory: built-in tree_rss sums RSS across the process tree every 10 ms. It can
double-count shared pages and miss shorter peaks. Pass --mem-probe for GPU or unified
memory, or enforce an OS resource limit when exceeding the cap is unacceptable.

Usage:
    uv run bench.py --name J1-startup --a "bun run dev --version" --a-cwd ../prev \
        --b "bun run dev --version" --b-cwd ../work --runs 10 --warmup 2 --out ledger.jsonl
    uv run bench.py --name J2-serve --a "..." --b "..." --ready "listening on" --graceful-stop 3
    uv run bench.py --name J3-idle --a "..." --b "..." --hold 20 --metric rss --mem-cap 4096
    uv run bench.py --show ledger.jsonl

Exit codes: 0 run completed without run/validation/environment errors, 1 error or
invalidated trial, 2 usage error.
"""

from __future__ import annotations

import argparse
import contextlib
import ctypes
import errno
import glob
import hashlib
import itertools
import json
import math
import os
import queue
import random
import re
import shlex
import signal
import statistics
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime, timezone

import psutil

SAMPLE_INTERVAL_S = 0.01
MIN_STAT_BLOCKS = 6


def finite_or_none(val: float | None, digits: int | None = None) -> float | None:
    if val is None or not math.isfinite(val):
        return None
    return round(val, digits) if digits is not None else val


def power_status() -> str:
    """Return 'ac', 'battery', or 'unknown'."""
    try:
        if sys.platform == "win32":
            class _PowerStatus(ctypes.Structure):
                _fields_ = [
                    ("ACLineStatus", ctypes.c_byte),
                    ("BatteryFlag", ctypes.c_byte),
                    ("BatteryLifePercent", ctypes.c_byte),
                    ("SystemStatusFlag", ctypes.c_byte),
                    ("BatteryLifeTime", ctypes.c_ulong),
                    ("BatteryFullLifeTime", ctypes.c_ulong),
                ]

            status = _PowerStatus()
            if not ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(status)):
                return "unknown"
            line = status.ACLineStatus & 0xFF
            if line == 1:
                return "ac"
            if line == 0:
                return "battery"
            return "unknown"
        if sys.platform == "darwin":
            res = subprocess.run(
                ["pmset", "-g", "batt"], capture_output=True, text=True, timeout=5
            )
            if res.returncode != 0 or not res.stdout.strip():
                return "unknown"
            if "AC Power" in res.stdout:
                return "ac"
            if "Battery Power" in res.stdout:
                return "battery"
            return "unknown"
        paths = glob.glob("/sys/class/power_supply/*/online")
        if not paths:
            return "unknown"
        vals = []
        for path in paths:
            try:
                vals.append(open(path, encoding="utf-8").read().strip())
            except OSError:
                continue
        if not vals:
            return "unknown"
        if "1" in vals:
            return "ac"
        if "0" in vals:
            return "battery"
        return "unknown"
    except Exception:
        return "unknown"


def _is_lock_contention(exc: OSError) -> bool:
    if sys.platform == "win32":
        winerr = getattr(exc, "winerror", None)
        return winerr in (33, 36) or exc.errno in (errno.EACCES, errno.EAGAIN, errno.EDEADLK)
    return exc.errno in (errno.EACCES, errno.EAGAIN, errno.EWOULDBLOCK)


@contextlib.contextmanager
def acquire_lock(lock_path: str | None, timeout_s: float = 300.0):
    """Acquire an exclusive cross-process file lock with bounded wait."""
    if not lock_path:
        yield
        return
    parent = os.path.dirname(os.path.abspath(lock_path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    fh = open(lock_path, "a+b")
    locked = False
    deadline = time.monotonic() + timeout_s
    try:
        if sys.platform == "win32":
            import msvcrt

            fh.seek(0)
            if os.path.getsize(lock_path) == 0:
                fh.write(b"\0")
                fh.flush()
            while True:
                try:
                    fh.seek(0)
                    msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
                    locked = True
                    break
                except OSError as exc:
                    if not _is_lock_contention(exc):
                        raise
                    if time.monotonic() >= deadline:
                        raise TimeoutError(
                            f"timed out after {timeout_s:.1f}s waiting for lock {lock_path}"
                        ) from exc
                    time.sleep(0.1)
        else:
            import fcntl

            while True:
                try:
                    fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    locked = True
                    break
                except OSError as exc:
                    if not _is_lock_contention(exc):
                        raise
                    if time.monotonic() >= deadline:
                        raise TimeoutError(
                            f"timed out after {timeout_s:.1f}s waiting for lock {lock_path}"
                        ) from exc
                    time.sleep(0.1)
        yield
    finally:
        if locked:
            try:
                if sys.platform == "win32":
                    import msvcrt

                    fh.seek(0)
                    msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
            except OSError:
                pass
        fh.close()


class _WindowsJob:
    """Best-effort Windows Job Object to own and terminate an entire process tree."""

    def __init__(self) -> None:
        self.handle = None
        if sys.platform != "win32":
            return
        try:
            k32 = ctypes.windll.kernel32
            k32.CreateJobObjectW.restype = ctypes.c_void_p
            k32.CreateJobObjectW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p]
            job = k32.CreateJobObjectW(None, None)
            if not job:
                return

            class _IO_COUNTERS(ctypes.Structure):
                _fields_ = [(n, ctypes.c_uint64) for n in (
                    "ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
                    "ReadTransferCount", "WriteTransferCount", "OtherTransferCount",
                )]

            class _BASIC_LIMIT(ctypes.Structure):
                _fields_ = [
                    ("PerProcessUserTimeLimit", ctypes.c_int64),
                    ("PerJobUserTimeLimit", ctypes.c_int64),
                    ("LimitFlags", ctypes.c_uint32),
                    ("MinimumWorkingSetSize", ctypes.c_size_t),
                    ("MaximumWorkingSetSize", ctypes.c_size_t),
                    ("ActiveProcessLimit", ctypes.c_uint32),
                    ("Affinity", ctypes.c_size_t),
                    ("PriorityClass", ctypes.c_uint32),
                    ("SchedulingClass", ctypes.c_uint32),
                ]

            class _EXTENDED_LIMIT(ctypes.Structure):
                _fields_ = [
                    ("BasicLimitInformation", _BASIC_LIMIT),
                    ("IoInfo", _IO_COUNTERS),
                    ("ProcessMemoryLimit", ctypes.c_size_t),
                    ("JobMemoryLimit", ctypes.c_size_t),
                    ("PeakProcessMemoryUsed", ctypes.c_size_t),
                    ("PeakJobMemoryUsed", ctypes.c_size_t),
                ]

            info = _EXTENDED_LIMIT()
            info.BasicLimitInformation.LimitFlags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            k32.SetInformationJobObject.argtypes = [
                ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32
            ]
            k32.SetInformationJobObject.restype = ctypes.c_int
            if k32.SetInformationJobObject(job, 9, ctypes.byref(info), ctypes.sizeof(info)):
                self.handle = job
            else:
                k32.CloseHandle.argtypes = [ctypes.c_void_p]
                k32.CloseHandle(job)
        except Exception:
            self.handle = None

    def assign(self, popen: subprocess.Popen) -> bool:
        if not self.handle or sys.platform != "win32":
            return False
        try:
            k32 = ctypes.windll.kernel32
            k32.AssignProcessToJobObject.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
            k32.AssignProcessToJobObject.restype = ctypes.c_int
            return bool(k32.AssignProcessToJobObject(self.handle, int(popen._handle)))
        except Exception:
            return False

    def terminate(self) -> None:
        if not self.handle or sys.platform != "win32":
            return
        try:
            k32 = ctypes.windll.kernel32
            k32.TerminateJobObject.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
            k32.TerminateJobObject.restype = ctypes.c_int
            k32.TerminateJobObject(self.handle, 1)
        except Exception:
            pass

    def close(self) -> None:
        if not self.handle or sys.platform != "win32":
            return
        try:
            k32 = ctypes.windll.kernel32
            k32.CloseHandle.argtypes = [ctypes.c_void_p]
            k32.CloseHandle(self.handle)
        except Exception:
            pass
        self.handle = None


def tree_rss(proc: psutil.Process) -> int | None:
    """Sum RSS over the process and descendants, or None if no process could be read."""
    total = 0
    read_any = False
    try:
        procs = [proc, *proc.children(recursive=True)]
    except psutil.Error:
        return None
    for p in procs:
        try:
            total += p.memory_info().rss
            read_any = True
        except psutil.Error:
            pass
    return total if read_any else None


def stop_owned_processes(
    popen: subprocess.Popen,
    proc: psutil.Process | None,
    job: _WindowsJob | None,
    graceful_s: float = 0.0,
) -> list[int]:
    """Terminate owned process group/job and descendants. Return any surviving PIDs."""
    tracked: dict[int, psutil.Process] = {}
    if proc is not None:
        try:
            for p in [proc, *proc.children(recursive=True)]:
                tracked[p.pid] = p
        except psutil.Error:
            tracked[popen.pid] = proc

    if graceful_s > 0:
        if sys.platform != "win32":
            try:
                os.killpg(popen.pid, signal.SIGTERM)
            except OSError:
                pass
        for p in list(tracked.values()):
            try:
                p.terminate()
            except psutil.Error:
                pass
        if tracked:
            _, alive = psutil.wait_procs(list(tracked.values()), timeout=graceful_s)
            tracked = {p.pid: p for p in alive}

    if sys.platform != "win32":
        try:
            os.killpg(popen.pid, signal.SIGKILL)
        except OSError:
            pass
    if job is not None:
        job.terminate()

    if proc is not None:
        try:
            for p in [proc, *proc.children(recursive=True)]:
                tracked[p.pid] = p
        except psutil.Error:
            pass
    for p in list(tracked.values()):
        try:
            p.kill()
        except psutil.Error:
            pass
    survivors: list[int] = []
    if tracked:
        _, alive = psutil.wait_procs(list(tracked.values()), timeout=5)
        survivors = [p.pid for p in alive if p.is_running()]
    try:
        popen.wait(timeout=2)
    except subprocess.TimeoutExpired:
        if popen.pid not in survivors:
            survivors.append(popen.pid)
    return survivors


def pump_bytes(stream, stream_name: str, q: queue.Queue) -> None:
    """Read raw byte lines and enqueue (timestamp, stream_name, raw_bytes)."""
    try:
        for raw in iter(stream.readline, b""):
            q.put((time.perf_counter(), stream_name, raw))
    finally:
        q.put((time.perf_counter(), stream_name, None))


class ExternalMemSampler(threading.Thread):
    """Sample memory in bytes using an external command with strict error tracking."""

    def __init__(self, cmd: str, interval_s: float, cap_bytes: int | None, probe_env: dict):
        super().__init__(daemon=True)
        self.cmd = cmd
        self.interval_s = max(0.05, interval_s)
        self.cap_bytes = cap_bytes
        self.probe_env = probe_env
        self.peak: int | None = None
        self.samples_ok = 0
        self.samples_failed = 0
        self.last_error = ""
        self.tripped = False
        self.stop_event = threading.Event()
        self._lock = threading.Lock()
        self._current_proc: subprocess.Popen | None = None

    def _sample_once(self) -> None:
        if self.stop_event.is_set():
            return
        proc = None
        try:
            proc = subprocess.Popen(
                self.cmd,
                shell=True,
                env=self.probe_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            with self._lock:
                self._current_proc = proc
            out_b, err_b = proc.communicate(timeout=30)
            if self.stop_event.is_set():
                return
            if proc.returncode != 0:
                self.samples_failed += 1
                err_txt = err_b.decode("utf-8", errors="replace").strip()
                self.last_error = f"exit {proc.returncode}: {err_txt[:200]}"
                return
            text = out_b.decode("utf-8", errors="replace").strip()
            if not text:
                self.samples_failed += 1
                self.last_error = "empty stdout from --mem-probe"
                return
            raw_val = float(text.splitlines()[-1].strip())
            if not math.isfinite(raw_val) or raw_val < 0:
                self.samples_failed += 1
                self.last_error = f"invalid reading from --mem-probe: {text!r}"
                return
            val = int(raw_val)
            self.samples_ok += 1
            if self.peak is None or val > self.peak:
                self.peak = val
            if self.cap_bytes is not None and val > self.cap_bytes:
                self.tripped = True
        except Exception as exc:
            if not self.stop_event.is_set():
                self.samples_failed += 1
                self.last_error = repr(exc)
            if proc is not None and proc.poll() is None:
                try:
                    proc.kill()
                    proc.wait(timeout=2)
                except Exception:
                    pass
        finally:
            with self._lock:
                self._current_proc = None

    def abort_and_join(self) -> None:
        self.stop_event.set()
        with self._lock:
            proc = self._current_proc
        if proc is not None and proc.poll() is None:
            try:
                proc.kill()
            except Exception:
                pass
        self.join(timeout=10)

    def run(self) -> None:
        self._sample_once()
        while not self.stop_event.wait(self.interval_s):
            self._sample_once()


def run_once(
    cmd: list[str] | str,
    cwd: str | None,
    env: dict,
    args,
    side: str,
    block: int,
    phase: str,
) -> dict:
    ready_re = re.compile(args.ready) if args.ready else None
    expect_re = re.compile(args.expect) if args.expect else None
    cap_bytes = int(args.mem_cap * 1024 * 1024) if args.mem_cap is not None else None
    mode = "ready" if ready_re else ("hold" if args.hold > 0 else "exit")

    popen_kwargs: dict = {
        "cwd": cwd,
        "env": env,
        "shell": args.shell,
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
    }
    if sys.platform == "win32":
        popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        popen_kwargs["start_new_session"] = True

    job = _WindowsJob() if sys.platform == "win32" else None
    start = time.perf_counter()
    popen = subprocess.Popen(cmd, **popen_kwargs)
    if job is not None:
        job.assign(popen)

    try:
        proc: psutil.Process | None = psutil.Process(popen.pid)
    except psutil.Error:
        proc = None

    exit_event = threading.Event()
    exit_ts_box: list[float] = []

    def wait_for_exit() -> None:
        popen.wait()
        exit_ts_box.append(time.perf_counter())
        exit_event.set()

    waiter = threading.Thread(target=wait_for_exit, daemon=True)
    waiter.start()

    q: queue.Queue = queue.Queue()
    out_reader = threading.Thread(target=pump_bytes, args=(popen.stdout, "stdout", q), daemon=True)
    err_reader = threading.Thread(target=pump_bytes, args=(popen.stderr, "stderr", q), daemon=True)
    out_reader.start()
    err_reader.start()

    probe_env = dict(env)
    probe_env.update(
        {
            "OPLOOP_TARGET_PID": str(popen.pid),
            "OPLOOP_SIDE": side,
            "OPLOOP_BLOCK": str(block),
            "OPLOOP_PHASE": phase,
            "OPLOOP_JOURNEY": args.name or "",
        }
    )
    probe = (
        ExternalMemSampler(args.mem_probe, args.mem_probe_interval, cap_bytes, probe_env)
        if args.mem_probe
        else None
    )
    if probe:
        probe.start()

    peak_bytes: int | None = None
    rss_samples_ok = 0
    end_reason = "exit"
    event_ts: float | None = None
    stdout_tail: list[str] = []
    stderr_tail: list[str] = []
    stdout_digest = hashlib.sha256() if args.check_eq else None
    stdout_bytes = 0
    expect_matched = expect_re is None
    ready_matched = False
    ready_ts: float | None = None
    closed_streams = 0
    survivors: list[int] = []
    drain_failed = False
    observed_exit_code: int | None = None
    harness_stopped = False

    def drain_queue() -> None:
        nonlocal closed_streams, stdout_bytes, expect_matched, ready_matched, ready_ts
        try:
            while True:
                ts, stream_name, raw = q.get_nowait()
                if raw is None:
                    closed_streams += 1
                    continue
                decoded = raw.decode("utf-8", errors="replace")
                if stream_name == "stdout":
                    stdout_bytes += len(raw)
                    if stdout_digest is not None:
                        stdout_digest.update(raw)
                    stdout_tail.append(decoded)
                    if len(stdout_tail) > 20:
                        del stdout_tail[:-20]
                    if expect_re and not expect_matched and expect_re.search(decoded):
                        expect_matched = True
                else:
                    stderr_tail.append(decoded)
                    if len(stderr_tail) > 20:
                        del stderr_tail[:-20]
                if ready_re and not ready_matched and ready_re.search(decoded):
                    ready_matched = True
                    ready_ts = ts
        except queue.Empty:
            pass

    try:
        while True:
            if probe:
                if probe.peak is not None:
                    peak_bytes = probe.peak if peak_bytes is None else max(peak_bytes, probe.peak)
                if probe.tripped:
                    end_reason = "mem_cap"
                    event_ts = time.perf_counter()
                    break
                if probe.samples_failed > 0:
                    end_reason = "mem_probe_error"
                    event_ts = time.perf_counter()
                    break
            elif proc is not None:
                cur_rss = tree_rss(proc)
                if cur_rss is not None:
                    rss_samples_ok += 1
                    peak_bytes = cur_rss if peak_bytes is None else max(peak_bytes, cur_rss)
                    if cap_bytes is not None and cur_rss > cap_bytes:
                        end_reason = "mem_cap"
                        event_ts = time.perf_counter()
                        break

            drain_queue()
            if mode == "ready" and ready_matched:
                end_reason = "ready"
                event_ts = ready_ts or time.perf_counter()
                break

            now = time.perf_counter()
            elapsed = now - start
            if exit_event.is_set():
                end_reason = "exit"
                event_ts = exit_ts_box[0] if exit_ts_box else now
                break
            if mode == "hold" and elapsed >= args.hold:
                end_reason = "hold"
                event_ts = now
                break
            if elapsed >= args.timeout:
                end_reason = "timeout"
                event_ts = now
                break
            exit_event.wait(timeout=SAMPLE_INTERVAL_S)
    finally:
        if end_reason in ("ready", "hold") and args.drain_cmd and not exit_event.is_set():
            try:
                drain_res = subprocess.run(
                    args.drain_cmd, shell=True, env=probe_env, capture_output=True, text=True, timeout=60
                )
                if drain_res.returncode != 0:
                    drain_failed = True
            except Exception:
                drain_failed = True

        observed_exit_code = popen.poll()
        if observed_exit_code is None:
            harness_stopped = True
            survivors = stop_owned_processes(popen, proc, job, graceful_s=args.graceful_stop)
        else:
            # Ensure no stray children outlive a wrapper that already exited.
            survivors = stop_owned_processes(popen, proc, job, graceful_s=0.0)

        if job is not None:
            job.close()
        waiter.join(timeout=2)
        out_reader.join(timeout=2)
        err_reader.join(timeout=2)
        drain_queue()

        if probe:
            probe.abort_and_join()
            if probe.peak is not None:
                peak_bytes = probe.peak if peak_bytes is None else max(peak_bytes, probe.peak)

    wall_ms = ((event_ts or time.perf_counter()) - start) * 1000.0
    mem_source = "probe" if probe else "tree_rss"
    mem_samples = probe.samples_ok if probe else rss_samples_ok

    # Mode-specific completion semantics
    if mode == "ready" and end_reason == "exit":
        if ready_matched:
            end_reason = "ready"
            if ready_ts is not None:
                wall_ms = (ready_ts - start) * 1000.0
        else:
            end_reason = "exited_before_ready"
    elif mode == "hold" and end_reason == "exit":
        end_reason = "exited_before_hold"

    # Evaluate final status strictly across all end conditions
    flags: list[str] = []
    ok = True

    if probe and (probe.samples_failed > 0 or probe.samples_ok == 0):
        ok = False
        flags.append("MEM_PROBE_FAIL")
        if end_reason in ("exit", "ready", "hold"):
            end_reason = "mem_probe_error"
    if probe and probe.tripped:
        ok = False
        flags.append("MEM_CAP")
        end_reason = "mem_cap"
    if end_reason == "mem_cap":
        ok = False
        flags.append("MEM_CAP")
    if (args.metric == "rss" or cap_bytes is not None) and mem_samples == 0:
        ok = False
        flags.append("MEM_NO_SAMPLE")

    if end_reason == "timeout":
        ok = False
        flags.append("TIMEOUT")
    elif end_reason == "exited_before_ready":
        ok = False
        flags.append("NOT_READY")
    elif end_reason == "exited_before_hold":
        ok = False
        flags.append("EARLY_EXIT")
    elif end_reason == "exit" and observed_exit_code != 0:
        ok = False
        flags.append("EXIT_ERROR")
    elif end_reason in ("ready", "hold") and (not harness_stopped) and observed_exit_code not in (0, None):
        ok = False
        flags.append("EXIT_ERROR")

    if ok and not expect_matched:
        ok = False
        end_reason = "expect_mismatch"
        flags.append("EXPECT_FAIL")
    if drain_failed:
        ok = False
        flags.append("DRAIN_FAIL")
    if survivors:
        ok = False
        flags.append("ORPHAN_PROCESS")

    diag_parts = []
    if stdout_tail:
        diag_parts.append("stdout:\n" + "".join(stdout_tail)[-1000:])
    if stderr_tail:
        diag_parts.append("stderr:\n" + "".join(stderr_tail)[-1000:])
    if probe and probe.last_error:
        diag_parts.append("mem-probe: " + probe.last_error)

    return {
        "wall_ms": wall_ms,
        "peak_mem_mib": (peak_bytes / (1024 * 1024)) if peak_bytes is not None else None,
        "mem_source": mem_source,
        "mem_samples": mem_samples,
        "ok": ok,
        "end": end_reason,
        "code": observed_exit_code,
        "harness_stopped": harness_stopped,
        "stdout_sha256": stdout_digest.hexdigest() if stdout_digest is not None else None,
        "stdout_bytes": stdout_bytes,
        "flags": sorted(set(flags)),
        "tail": "\n".join(diag_parts) if not ok else "",
    }


def paired_permutation_p(diffs: list[float], max_exact_n: int = 14, resamples: int = 10000, seed: int = 0) -> float | None:
    """Two-sided exact/MC paired Wilcoxon signed-rank permutation test across blocks."""
    if len(diffs) < MIN_STAT_BLOCKS:
        return None
    nz = [d for d in diffs if d != 0.0]
    m = len(nz)
    if m == 0:
        return 1.0
    indexed = sorted((abs(d), i) for i, d in enumerate(nz))
    ranks = [0.0] * m
    i = 0
    while i < m:
        j = i
        while j + 1 < m and indexed[j + 1][0] == indexed[i][0]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[indexed[k][1]] = avg_rank
        i = j + 1
    signed = [r if d > 0 else -r for r, d in zip(ranks, nz)]
    observed = abs(sum(signed))
    if observed == 0.0:
        return 1.0
    if m <= max_exact_n:
        total = 1 << m
        exceed = 0
        for signs in itertools.product((-1.0, 1.0), repeat=m):
            stat = abs(sum(s * r for s, r in zip(signs, ranks)))
            if stat >= observed - 1e-12:
                exceed += 1
        return exceed / total
    rng = random.Random(seed)
    exceed = 0
    for _ in range(resamples):
        stat = abs(sum(r if rng.getrandbits(1) else -r for r in ranks))
        if stat >= observed - 1e-12:
            exceed += 1
    return (exceed + 1) / (resamples + 1)


def block_bootstrap_change_ci(
    pairs: list[tuple[float, float]], resamples: int = 2000, seed: int = 0
) -> tuple[float | None, float | None]:
    """Deterministic percentile bootstrap 95% CI resampling complete (A, B) blocks."""
    n = len(pairs)
    if n < MIN_STAT_BLOCKS:
        return (None, None)
    rng = random.Random(seed)
    deltas: list[float] = []
    for _ in range(resamples):
        sample = [pairs[rng.randrange(n)] for _ in range(n)]
        ma = statistics.median(a for a, _ in sample)
        if ma == 0:
            continue
        mb = statistics.median(b for _, b in sample)
        deltas.append((mb - ma) / ma * 100.0)
    if len(deltas) < 20:
        return (None, None)
    deltas.sort()
    lo = deltas[int(0.025 * len(deltas))]
    hi = deltas[min(len(deltas) - 1, int(0.975 * len(deltas)))]
    return (lo, hi)


def summarize(values: list[float]) -> dict:
    clean = [v for v in values if v is not None and math.isfinite(v)]
    if not clean:
        return {"median": None, "min": None, "max": None}
    return {
        "median": statistics.median(clean),
        "min": min(clean),
        "max": max(clean),
    }


def parse_cmd(text: str, shell: bool) -> str | list[str]:
    if shell:
        return text
    if sys.platform != "win32":
        return shlex.split(text, posix=True)
    # Preserve Windows backslashes while stripping balanced outer quotes on tokens.
    tokens = shlex.split(text, posix=False)
    cleaned: list[str] = []
    for tok in tokens:
        if len(tok) >= 2 and tok[0] == tok[-1] and tok[0] in ('"', "'"):
            cleaned.append(tok[1:-1])
        else:
            cleaned.append(tok)
    return cleaned


def append_jsonl(path: str | None, record: dict) -> None:
    if not path:
        return
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    line = json.dumps(record, allow_nan=False) + "\n"
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(line)
        fh.flush()


def show_ledger(path: str) -> int:
    """Print a compact summary table from a --out JSONL file, reporting incomplete runs."""
    if not os.path.exists(path):
        print(f"error: ledger file not found: {path}")
        return 2
    summaries: list[dict] = []
    trial_sessions: dict[str, dict] = {}
    summarized_sessions: set[str] = set()
    legacy_rows: list[dict] = []
    corrupt_lines = 0

    with open(path, encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            text = raw.strip()
            if not text:
                continue
            try:
                obj = json.loads(text)
            except json.JSONDecodeError:
                corrupt_lines += 1
                print(f"warning: skipped malformed JSON at line {lineno}")
                continue
            rec_type = obj.get("type")
            if rec_type == "summary":
                summaries.append(obj)
                if obj.get("session_id"):
                    summarized_sessions.add(obj["session_id"])
            elif rec_type == "trial":
                sid = obj.get("session_id", f"line-{lineno}")
                info = trial_sessions.setdefault(
                    sid, {"time": obj.get("time", ""), "journey": obj.get("journey", ""), "trials": 0}
                )
                info["trials"] += 1
            else:
                legacy_rows.append(obj)

    # Convert legacy paired rows into displayable summaries
    idx = 0
    while idx < len(legacy_rows):
        cur = legacy_rows[idx]
        nxt = legacy_rows[idx + 1] if idx + 1 < len(legacy_rows) else None
        if (
            cur.get("side") == "A"
            and nxt is not None
            and nxt.get("side") == "B"
            and cur.get("time") == nxt.get("time")
            and cur.get("journey") == nxt.get("journey")
        ):
            metric = cur.get("metric", "wall")
            summaries.append(
                {
                    "time": cur.get("time", ""),
                    "journey": cur.get("journey", ""),
                    "metric": metric,
                    "A": {metric: cur.get(metric, {})},
                    "B": {metric: nxt.get(metric, {})},
                    "change_pct": cur.get("change_pct"),
                    "p": cur.get("p"),
                    "eligible_keep": None,
                    "verdict": cur.get("verdict", ""),
                    "flags": cur.get("flags", []),
                }
            )
            idx += 2
        else:
            idx += 1

    incomplete = [
        (sid, info) for sid, info in trial_sessions.items() if sid not in summarized_sessions
    ]
    if not summaries and not incomplete:
        print(f"0 runs recorded in {path}")
        return 0

    header = (
        f"{'time':19}  {'journey':18}  {'metric':6}  {'A med':>9}  {'B med':>9}  "
        f"{'change':>8}  {'p':>6}  {'keep':5}  {'verdict':30}  flags"
    )
    print(header)
    print("-" * len(header))
    for s in summaries:
        metric = s.get("metric", "wall")
        a_med = s.get("A", {}).get(metric, {}).get("median")
        b_med = s.get("B", {}).get(metric, {}).get("median")
        a_str = f"{a_med:.1f}" if isinstance(a_med, (int, float)) and math.isfinite(a_med) else "-"
        b_str = f"{b_med:.1f}" if isinstance(b_med, (int, float)) and math.isfinite(b_med) else "-"
        chg = s.get("change_pct")
        chg_str = f"{chg:+.1f}%" if isinstance(chg, (int, float)) and math.isfinite(chg) else "-"
        pval = s.get("p")
        p_str = f"{pval:.4f}" if isinstance(pval, (int, float)) and math.isfinite(pval) else "-"
        keep = s.get("eligible_keep")
        keep_str = "yes" if keep is True else ("no" if keep is False else "-")
        stamp = str(s.get("time", ""))[:19]
        journey = str(s.get("journey", ""))[:18]
        verdict = str(s.get("verdict", ""))[:30]
        flags = ",".join(s.get("flags", []))
        print(
            f"{stamp:19}  {journey:18}  {metric:6}  {a_str:>9}  {b_str:>9}  "
            f"{chg_str:>8}  {p_str:>6}  {keep_str:5}  {verdict:30}  {flags}"
        )
    for sid, info in incomplete:
        stamp = str(info.get("time", ""))[:19]
        journey = str(info.get("journey", ""))[:18]
        print(
            f"{stamp:19}  {journey:18}  {'-':6}  {'-':>9}  {'-':>9}  "
            f"{'-':>8}  {'-':>6}  {'no':5}  {'incomplete (' + str(info['trials']) + ' trials)':30}  INCOMPLETE"
        )
    extra = f", {len(incomplete)} incomplete" if incomplete else ""
    extra += f", {corrupt_lines} malformed lines" if corrupt_lines else ""
    print(f"\n{len(summaries)} benchmark summaries{extra} in {path}")
    return 0


def validate_args(args) -> str | None:
    missing = [f for f, v in (("--name", args.name), ("--a", args.a), ("--b", args.b)) if not v]
    if missing:
        return f"missing required flags: {', '.join(missing)} (or pass --show FILE)"
    if args.ready and args.hold > 0:
        return "--ready and --hold are mutually exclusive"
    if args.runs < 1:
        return "--runs must be at least 1"
    if args.warmup < 0:
        return "--warmup must be 0 or greater"
    if not (math.isfinite(args.timeout) and args.timeout > 0):
        return "--timeout must be a finite number greater than 0"
    if not (math.isfinite(args.hold) and args.hold >= 0):
        return "--hold must be a finite number >= 0"
    if not (math.isfinite(args.graceful_stop) and args.graceful_stop >= 0):
        return "--graceful-stop must be a finite number >= 0"
    if not (math.isfinite(args.lock_timeout) and args.lock_timeout > 0):
        return "--lock-timeout must be a finite number greater than 0"
    if not (math.isfinite(args.alpha) and 0 < args.alpha < 1):
        return "--alpha must be between 0 and 1"
    if not (math.isfinite(args.min_improvement) and args.min_improvement >= 0):
        return "--min-improvement must be a finite number >= 0"
    if args.mem_cap is not None and not (math.isfinite(args.mem_cap) and args.mem_cap > 0):
        return "--mem-cap must be a finite number greater than 0"
    if not (math.isfinite(args.mem_probe_interval) and args.mem_probe_interval > 0):
        return "--mem-probe-interval must be a finite number greater than 0"
    for label, pattern in (("--ready", args.ready), ("--expect", args.expect)):
        if pattern:
            try:
                re.compile(pattern)
            except re.error as exc:
                return f"invalid regex for {label}: {exc}"
    for label, cwd in (("--a-cwd", args.a_cwd), ("--b-cwd", args.b_cwd)):
        if cwd and not os.path.isdir(cwd):
            return f"{label} directory does not exist: {cwd}"
    for label, cmd_text in (("--a", args.a), ("--b", args.b)):
        parsed = parse_cmd(cmd_text, args.shell)
        if not parsed:
            return f"{label} command is empty"
    return None


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--show", default=None, help="print summary table from a --out JSONL file and exit")
    ap.add_argument("--name", default=None, help="journey ID, for example J1-startup")
    ap.add_argument("--a", default=None, help="command for side A (control)")
    ap.add_argument("--b", default=None, help="command for side B (candidate)")
    ap.add_argument("--a-cwd", default=None)
    ap.add_argument("--b-cwd", default=None)
    ap.add_argument("--runs", type=int, default=10, help="measured blocks per side (>=6 for alpha=0.05)")
    ap.add_argument("--warmup", type=int, default=1, help="unmeasured warmup blocks per side")
    ap.add_argument("--ready", default=None, help="target must match this regex on stdout or stderr")
    ap.add_argument("--hold", type=float, default=0, help="target must stay alive for this many seconds")
    ap.add_argument("--timeout", type=float, default=120, help="fail a run after this many seconds")
    ap.add_argument("--metric", choices=["wall", "rss"], default="wall", help="primary metric")
    ap.add_argument("--alpha", type=float, default=0.05, help="two-sided permutation p-value threshold")
    ap.add_argument("--min-improvement", type=float, default=0.0, help="minimum useful percentage reduction")
    ap.add_argument("--shell", action="store_true", help="run --a and --b through the system shell")
    ap.add_argument("--env", action="append", default=[], help="KEY=VALUE for both sides (repeatable)")
    ap.add_argument("--out", default=None, help="append strict JSONL trial and summary records here")
    ap.add_argument("--require-ac", action="store_true", help="require verified AC power before the session and around each trial")
    ap.add_argument("--mem-cap", type=float, default=None, help="abort a run above this sampled MiB cap")
    ap.add_argument("--mem-probe", default=None, help="shell command printing target memory in bytes")
    ap.add_argument("--mem-probe-interval", type=float, default=1.0, help="seconds between probe polls")
    ap.add_argument("--expect", default=None, help="require raw stdout to match this regex")
    ap.add_argument("--check-eq", action="store_true", help="require non-empty matching raw stdout bytes")
    ap.add_argument("--graceful-stop", type=float, default=0.0, help="seconds to wait on terminate before kill")
    ap.add_argument("--drain-cmd", default=None, help="shell command to drain server before stop")
    ap.add_argument("--lock", default=None, help="exclusive lock file path to serialize runs")
    ap.add_argument("--lock-timeout", type=float, default=300.0, help="max seconds to wait for --lock")
    args = ap.parse_args()

    if args.show:
        return show_ledger(args.show)

    err = validate_args(args)
    if err:
        print(f"error: {err}")
        return 2

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
    session_id = uuid.uuid4().hex[:12]
    flags: list[str] = []
    warmup_results: dict[str, list[dict]] = {"A": [], "B": []}
    results: dict[str, list[dict]] = {"A": [], "B": []}

    def check_ac(stage: str) -> bool:
        if not args.require_ac:
            return True
        st = power_status()
        if st == "ac":
            return True
        if st == "battery":
            flags.append("ON_BATTERY")
            print(f"error: battery power detected ({stage})")
        else:
            flags.append("POWER_UNKNOWN")
            print(f"error: cannot verify AC power ({stage})")
        return False

    try:
        lock_ctx = acquire_lock(args.lock, timeout_s=args.lock_timeout)
    except Exception as exc:
        print(f"error: lock setup failed: {exc}")
        return 1

    try:
        with lock_ctx:
            if not check_ac("before start"):
                return 1

            for w in range(args.warmup):
                order = ("A", "B") if w % 2 == 0 else ("B", "A")
                for label in order:
                    if not check_ac(f"before warmup block {w} side {label}"):
                        return 1
                    res = run_once(*sides[label], env, args, side=label, block=w, phase="warmup")
                    warmup_results[label].append(res)
                    append_jsonl(
                        args.out,
                        {
                            "type": "trial",
                            "session_id": session_id,
                            "time": datetime.now(timezone.utc).isoformat(),
                            "journey": args.name,
                            "phase": "warmup",
                            "block": w,
                            "side": label,
                            "wall_ms": finite_or_none(res["wall_ms"], 3),
                            "peak_mem_mib": finite_or_none(res["peak_mem_mib"], 3),
                            "mem_source": res["mem_source"],
                            "mem_samples": res["mem_samples"],
                            "ok": res["ok"],
                            "end": res["end"],
                            "code": res["code"],
                            "stdout_sha256": res["stdout_sha256"],
                            "stdout_bytes": res["stdout_bytes"],
                            "flags": res["flags"],
                        },
                    )
                    if not check_ac(f"after warmup block {w} side {label}"):
                        return 1
                    if not res["ok"]:
                        flags.append("WARMUP_FAIL")
                        flags.extend(res["flags"])
                        print(f"[{label}] warmup block {w} failed: end={res['end']} code={res['code']}")
                        if res["tail"]:
                            print(res["tail"])

            for i in range(args.runs):
                order = ("A", "B") if i % 2 == 0 else ("B", "A")
                for label in order:
                    if not check_ac(f"before block {i} side {label}"):
                        return 1
                    res = run_once(*sides[label], env, args, side=label, block=i, phase="measured")
                    results[label].append(res)
                    append_jsonl(
                        args.out,
                        {
                            "type": "trial",
                            "session_id": session_id,
                            "time": datetime.now(timezone.utc).isoformat(),
                            "journey": args.name,
                            "phase": "measured",
                            "block": i,
                            "side": label,
                            "wall_ms": finite_or_none(res["wall_ms"], 3),
                            "peak_mem_mib": finite_or_none(res["peak_mem_mib"], 3),
                            "mem_source": res["mem_source"],
                            "mem_samples": res["mem_samples"],
                            "ok": res["ok"],
                            "end": res["end"],
                            "code": res["code"],
                            "stdout_sha256": res["stdout_sha256"],
                            "stdout_bytes": res["stdout_bytes"],
                            "flags": res["flags"],
                        },
                    )
                    if not check_ac(f"after block {i} side {label}"):
                        return 1

            key = "wall_ms" if args.metric == "wall" else "peak_mem_mib"
            unit = "ms" if args.metric == "wall" else "MiB"
            stats = {}
            errors = 0
            for label in ("A", "B"):
                good = [r for r in results[label] if r["ok"]]
                bad = [r for r in results[label] if not r["ok"]]
                errors += len(bad)
                for r in bad:
                    flags.extend(r["flags"])
                stats[label] = {
                    "wall": summarize([r["wall_ms"] for r in good]),
                    "rss": summarize([r["peak_mem_mib"] for r in good if r["peak_mem_mib"] is not None]),
                    "ok": len(good),
                    "errors": len(bad),
                    "mem_source": good[0]["mem_source"] if good else ("probe" if args.mem_probe else "tree_rss"),
                }
                if bad:
                    first = bad[0]
                    print(f"[{label}] {len(bad)} failed runs. First: end={first['end']} code={first['code']}")
                    if first["tail"]:
                        print(f"[{label}] diagnostic tail:\n{first['tail']}")

            # Paired blocks where both sides succeeded and produced valid metric readings
            valid_pairs: list[tuple[float, float]] = []
            for a_res, b_res in zip(results["A"], results["B"]):
                if a_res["ok"] and b_res["ok"]:
                    va, vb = a_res[key], b_res[key]
                    if va is not None and vb is not None and math.isfinite(va) and math.isfinite(vb):
                        valid_pairs.append((va, vb))

            if args.check_eq:
                ok_a = [r for r in results["A"] if r["ok"]]
                ok_b = [r for r in results["B"] if r["ok"]]
                if ok_a and ok_b:
                    if all(r["stdout_bytes"] == 0 for r in ok_a) and all(r["stdout_bytes"] == 0 for r in ok_b):
                        flags.append("EMPTY_OUTPUT")
                        print("[check-eq] both sides produced 0 stdout bytes")
                    a_hashes = {r["stdout_sha256"] for r in ok_a}
                    if len(a_hashes) > 1:
                        flags.append("A_NONDETERMINISTIC")
                        print(f"[check-eq] side A produced {len(a_hashes)} distinct raw stdout digests")
                    for idx_b, (a_res, b_res) in enumerate(zip(results["A"], results["B"])):
                        if a_res["ok"] and b_res["ok"] and a_res["stdout_sha256"] != b_res["stdout_sha256"]:
                            flags.append("OUTPUT_DIFF")
                            print(
                                f"[check-eq] block {idx_b} raw stdout mismatch: "
                                f"A={a_res['stdout_sha256'][:12]} B={b_res['stdout_sha256'][:12]}"
                            )
                            break

            flags = sorted(set(flags))
            diffs = [b - a for a, b in valid_pairs]
            p = paired_permutation_p(diffs)
            ci_lo, ci_hi = block_bootstrap_change_ci(valid_pairs)
            a_med = stats["A"]["wall" if args.metric == "wall" else "rss"]["median"]
            b_med = stats["B"]["wall" if args.metric == "wall" else "rss"]["median"]
            change = ((b_med - a_med) / a_med * 100.0) if (a_med is not None and b_med is not None and a_med != 0) else None
            improvement_pct = (-change) if change is not None else None

            invalid = bool(errors or flags)
            insufficient = len(valid_pairs) < MIN_STAT_BLOCKS
            eligible_keep = (
                (not invalid)
                and (not insufficient)
                and (p is not None and p < args.alpha)
                and (improvement_pct is not None and improvement_pct >= args.min_improvement)
                and (ci_hi is not None and ci_hi < -args.min_improvement)
            )
            regression = (
                (not invalid)
                and (not insufficient)
                and (p is not None and p < args.alpha)
                and (change is not None and change > 0.0)
                and (ci_lo is not None and ci_lo > 0.0)
            )

            if invalid:
                verdict = f"inconclusive ({','.join(flags) or 'errors'})"
            elif insufficient:
                verdict = f"inconclusive (need>={MIN_STAT_BLOCKS}_blocks)"
            elif eligible_keep:
                verdict = "keep_eligible (B improved)"
            elif regression:
                verdict = "regression (B worse)"
            else:
                verdict = "no measurable improvement"

            def fmt(v: float | None) -> str:
                return f"{v:.1f}" if v is not None and math.isfinite(v) else "-"

            print(
                f"journey   {args.name}   metric {args.metric}   blocks {len(valid_pairs)}/{args.runs}   "
                f"warmup {args.warmup}   mem_source {stats['A']['mem_source']}"
            )
            for label in ("A", "B"):
                s = stats[label]
                print(
                    f"{label}  wall median {fmt(s['wall']['median'])} ms  range {fmt(s['wall']['min'])}-{fmt(s['wall']['max'])}"
                    f"   sampled peak {fmt(s['rss']['median'])} MiB  range {fmt(s['rss']['min'])}-{fmt(s['rss']['max'])}"
                    f"   ok {s['ok']}  errors {s['errors']}"
                )
            chg_text = f"{change:+.1f}%" if change is not None else "-"
            ci_text = f"   ci95=[{ci_lo:+.1f}%, {ci_hi:+.1f}%]" if (ci_lo is not None and ci_hi is not None) else ""
            p_text = f"{p:.4f}" if p is not None else "-"
            flag_text = f"   flags={','.join(flags)}" if flags else ""
            print(
                f"change {chg_text} ({unit}){ci_text}   p={p_text}   "
                f"eligible_keep={eligible_keep}{flag_text}   verdict: {verdict}"
            )

            append_jsonl(
                args.out,
                {
                    "type": "summary",
                    "session_id": session_id,
                    "time": datetime.now(timezone.utc).isoformat(),
                    "journey": args.name,
                    "cmd_a": args.a,
                    "cmd_b": args.b,
                    "cwd_a": args.a_cwd,
                    "cwd_b": args.b_cwd,
                    "metric": args.metric,
                    "unit": unit,
                    "runs_requested": args.runs,
                    "valid_pairs": len(valid_pairs),
                    "warmup": args.warmup,
                    "min_improvement_pct": args.min_improvement,
                    "A": {
                        "wall": {k: finite_or_none(v, 3) for k, v in stats["A"]["wall"].items()},
                        "rss": {k: finite_or_none(v, 3) for k, v in stats["A"]["rss"].items()},
                        "ok": stats["A"]["ok"],
                        "errors": stats["A"]["errors"],
                    },
                    "B": {
                        "wall": {k: finite_or_none(v, 3) for k, v in stats["B"]["wall"].items()},
                        "rss": {k: finite_or_none(v, 3) for k, v in stats["B"]["rss"].items()},
                        "ok": stats["B"]["ok"],
                        "errors": stats["B"]["errors"],
                    },
                    "change_pct": finite_or_none(change, 3),
                    "ci95_low_pct": finite_or_none(ci_lo, 2),
                    "ci95_high_pct": finite_or_none(ci_hi, 2),
                    "p": finite_or_none(p, 6),
                    "eligible_keep": eligible_keep,
                    "flags": flags,
                    "verdict": verdict,
                },
            )
            return 1 if invalid else 0
    except TimeoutError as exc:
        print(f"error: {exc}")
        return 1
    except OSError as exc:
        print(f"error: lock error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
