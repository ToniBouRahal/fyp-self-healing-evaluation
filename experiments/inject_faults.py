#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess


def run(command: list[str]) -> None:
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        raise SystemExit(f"Command failed: {' '.join(command)}")


def pod_crash(namespace: str, selector: str) -> None:
    run(["kubectl", "delete", "pod", "-n", namespace, "-l", selector])


def memory_pressure(namespace: str, deployment: str) -> None:
    patch = (
        '{"spec":{"template":{"spec":{"containers":[{"name":"api","resources":'
        '{"limits":{"memory":"64Mi"},"requests":{"memory":"32Mi"}}}]}}}}'
    )
    run(["kubectl", "patch", "deployment", deployment, "-n", namespace, "-p", patch])


def bad_config(namespace: str, deployment: str) -> None:
    patch = '{"spec":{"template":{"spec":{"containers":[{"name":"api","image":"nginx:bad-tag"}]}}}}'
    run(["kubectl", "patch", "deployment", deployment, "-n", namespace, "-p", patch])


def main() -> None:
    parser = argparse.ArgumentParser(description="Inject failure scenarios")
    parser.add_argument("scenario", choices=["pod-crash", "memory-pressure", "bad-config"])
    parser.add_argument("--namespace", default="default")
    parser.add_argument("--selector", default="app=demo-api")
    parser.add_argument("--deployment", default="demo-api")
    args = parser.parse_args()

    if args.scenario == "pod-crash":
        pod_crash(args.namespace, args.selector)
    elif args.scenario == "memory-pressure":
        memory_pressure(args.namespace, args.deployment)
    elif args.scenario == "bad-config":
        bad_config(args.namespace, args.deployment)


if __name__ == "__main__":
    main()
