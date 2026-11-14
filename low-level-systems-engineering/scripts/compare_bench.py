#!/usr/bin/env python3
"""Exploratory comparison of process benchmark JSON files; lower runtime is better."""
import argparse
import json
import random
import statistics


def pct(xs, p):
    ys = sorted(xs)
    rank = (len(ys) - 1) * p
    lo = int(rank)
    hi = min(lo + 1, len(ys)-1)
    return ys[lo] * (hi-rank) + ys[hi] * (rank-lo)


def load(path):
    with open(path, encoding='utf-8') as fp:
        obj = json.load(fp)
    samples = obj.get('samples_ms')
    if obj.get('schema') != 'low-level-systems-bench-v1' or not isinstance(samples, list) or not samples:
        raise ValueError(f'{path} is not a valid bench.py result')
    xs = [float(x) for x in samples]
    if any(x <= 0 or not x < float('inf') for x in xs):
        raise ValueError(f'{path} contains nonpositive or nonfinite times')
    return xs


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('baseline')
    ap.add_argument('candidate')
    ap.add_argument('--resamples', type=int, default=3000)
    ap.add_argument('--seed', type=int, default=1337)
    ap.add_argument('--minimum-improvement-pct', type=float, default=1.0)
    args = ap.parse_args()
    if args.resamples < 100:
        ap.error('Use at least 100 resamples')
    base, cand = load(args.baseline), load(args.candidate)
    rng = random.Random(args.seed)
    b, c = statistics.median(base), statistics.median(cand)
    ratios = []
    for _ in range(args.resamples):
        bs = statistics.median(rng.choices(base, k=len(base)))
        cs = statistics.median(rng.choices(cand, k=len(cand)))
        ratios.append(bs / cs)
    observed = abs(b-c)
    pooled = base + cand
    count = 0
    for _ in range(args.resamples):
        shuffled = pooled[:]
        rng.shuffle(shuffled)
        delta = abs(statistics.median(shuffled[:len(base)]) - statistics.median(shuffled[len(base):]))
        if delta >= observed - 1e-12:
            count += 1
    p_value = (count + 1) / (args.resamples + 1)
    print(f'baseline median:    {b:.6f} ms (n={len(base)})')
    print(f'candidate median:   {c:.6f} ms (n={len(cand)})')
    print(f'speedup:            {b/c:.4f}x')
    print(f'latency reduction:  {100*(b-c)/b:+.2f}%')
    print(f'bootstrap 95% CI:   {pct(ratios, 0.025):.4f}x to {pct(ratios, 0.975):.4f}x')
    print(f'permutation p-value (two-sided, exploratory): {p_value:.4f}')
    meaningful = (100 * (b-c) / b) >= args.minimum_improvement_pct
    print(f'practically meaningful at chosen threshold: {meaningful}')
    print('\nCaution: assumes roughly independent comparable runs. Do NOT treat this as proof of product speedup;')
    print('use alternated/randomized A/B, control thermal/frequency drift, and verify correctness and tail latency.')


if __name__ == '__main__':
    main()
