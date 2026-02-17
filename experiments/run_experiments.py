#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import datetime as dt
import subprocess
import time
from pathlib import Path

SCENARIOS = ["pod-crash", "memory-pressure", "bad-config"]


def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def run(command: list[str]) -> None:
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(command)}")


def wait_for_recovery(namespace: str, deployment: str, timeout: int = 300) -> int:
    start = time.time()
    while time.time() - start < timeout:
        output = subprocess.check_output(
            [
                "kubectl",
                "get",
                "deployment",
                deployment,
                "-n",
                namespace,
                "-o",
                "jsonpath={.status.readyReplicas}",
            ],
            text=True,
        ).strip()
        if output and int(output) > 0:
            return int(time.time() - start)
        time.sleep(5)
    return timeout


def main() -> None:
    parser = argparse.ArgumentParser(description="Run healing experiments")
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--namespace", default="default")
    parser.add_argument("--deployment", default="demo-api")
    parser.add_argument("--output", default="experiments/results.csv")
    args = parser.parse_args()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["scenario", "iteration", "started_at", "recovery_seconds"])
        writer.writeheader()

        for scenario in SCENARIOS:
            for iteration in range(1, args.iterations + 1):
                started_at = now().isoformat()
                run(["python", "experiments/inject_faults.py", scenario, "--namespace", args.namespace])
                recovery_seconds = wait_for_recovery(args.namespace, args.deployment)
                writer.writerow(
                    {
                        "scenario": scenario,
                        "iteration": iteration,
                        "started_at": started_at,
                        "recovery_seconds": recovery_seconds,
                    }
                )


if __name__ == "__main__":
    main()
