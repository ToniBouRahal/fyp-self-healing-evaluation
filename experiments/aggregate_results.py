#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import statistics
from collections import defaultdict


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate MTTR results")
    parser.add_argument("--input", default="experiments/results.csv")
    args = parser.parse_args()

    values: dict[str, list[float]] = defaultdict(list)
    with open(args.input, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            values[row["scenario"]].append(float(row["recovery_seconds"]))

    print("scenario,mean_seconds,median_seconds,p95_seconds")
    for scenario, series in sorted(values.items()):
        series_sorted = sorted(series)
        idx = max(0, min(len(series_sorted) - 1, int(round(0.95 * (len(series_sorted) - 1)))))
        print(
            f"{scenario},{statistics.mean(series):.2f},{statistics.median(series):.2f},{series_sorted[idx]:.2f}"
        )


if __name__ == "__main__":
    main()
