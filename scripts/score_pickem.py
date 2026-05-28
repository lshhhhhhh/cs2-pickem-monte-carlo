#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", type=Path, required=True)
    parser.add_argument("--three-oh", nargs=2, required=True)
    parser.add_argument("--advance", nargs=6, required=True)
    parser.add_argument("--zero-three", nargs=2, required=True)
    args = parser.parse_args()

    event = json.loads(args.event.read_text(encoding="utf-8"))
    records = event["actual_records"]
    hits: list[str] = []
    misses: list[str] = []

    for name in args.three_oh:
        wins, losses = records[name]
        (hits if wins == 3 and losses == 0 else misses).append(f"3-0: {name} actual {wins}-{losses}")

    for name in args.advance:
        wins, losses = records[name]
        (hits if wins == 3 else misses).append(f"Advance: {name} actual {wins}-{losses}")

    for name in args.zero_three:
        wins, losses = records[name]
        (hits if wins == 0 and losses == 3 else misses).append(f"0-3: {name} actual {wins}-{losses}")

    print(f"Hits: {len(hits)} / 10")
    print("\nCorrect")
    for line in hits:
        print(f"- {line}")
    print("\nMissed")
    for line in misses:
        print(f"- {line}")


if __name__ == "__main__":
    main()
