#!/usr/bin/env python3

import sys
import statistics

def parse_latencies(file_path):
    latencies = []
    with open(file_path) as f:
        for line in f:
            try:
                latencies.append(float(line.strip()))
            except ValueError:
                continue
    return latencies

def percentile(data, p):
    data.sort()
    k = int(len(data) * p)
    return data[min(k, len(data) - 1)]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: p95_p99_parser.py latency.txt")
        sys.exit(1)

    data = parse_latencies(sys.argv[1])
    print(f"P50: {percentile(data, 0.50)} ms")
    print(f"P95: {percentile(data, 0.95)} ms")
    print(f"P99: {percentile(data, 0.99)} ms")
