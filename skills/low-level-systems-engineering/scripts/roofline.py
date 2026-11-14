#!/usr/bin/env python3
"""Simple Roofline upper-bound estimate; user must supply consistent units and measured capacities."""
import argparse
import math


def positive_float(s):
    value = float(s)
    if not math.isfinite(value) or value <= 0:
        raise argparse.ArgumentTypeError('must be finite and > 0')
    return value


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--operations', type=positive_float, required=True, help='useful operations in one run')
    ap.add_argument('--bytes', type=positive_float, required=True, help='bytes transferred at selected memory level')
    ap.add_argument('--peak-ops-per-second', type=positive_float, required=True)
    ap.add_argument('--bandwidth-bytes-per-second', type=positive_float, required=True)
    ap.add_argument('--measured-seconds', type=positive_float)
    args = ap.parse_args()
    intensity = args.operations / args.bytes
    bw_ceiling = intensity * args.bandwidth_bytes_per_second
    ceiling = min(bw_ceiling, args.peak_ops_per_second)
    minimum_time = args.operations / ceiling
    bound = 'compute' if args.peak_ops_per_second <= bw_ceiling else 'bandwidth'
    print(f'arithmetic intensity: {intensity:.6g} useful operations/byte')
    print(f'bandwidth roof:      {bw_ceiling:.6g} operations/s')
    print(f'compute roof:        {args.peak_ops_per_second:.6g} operations/s')
    print(f'predicted upper bound: {ceiling:.6g} operations/s ({bound}-limited in this simplified model)')
    print(f'theoretical minimum: {minimum_time:.6g} s')
    if args.measured_seconds:
        actual = args.operations / args.measured_seconds
        print(f'measured useful rate: {actual:.6g} operations/s ({actual / ceiling * 100:.2f}% of roof)')
    print('Caution: choose DRAM/L2/L1 bytes and bandwidth consistently; this excludes many other ceilings.')


if __name__ == '__main__':
    main()
