#!/usr/bin/env python3
"""Monte Carlo backtest for IEM Cologne 2025 Stage 1 / Play-In."""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from iem_cologne_pickem_mc import Team, build_teams, format_percent, load_event, load_vrs_csv, win_probability


def play_match(rng: random.Random, teams: dict[str, Team], a: str, b: str, scale: float) -> tuple[str, str]:
    p_a = win_probability(teams[a], teams[b], bo3=True, scale=scale)
    return (a, b) if rng.random() < p_a else (b, a)


def simulate_playin(
    rng: random.Random,
    teams: dict[str, Team],
    opening_matches: list[tuple[str, str]],
    scale: float,
) -> set[str]:
    first_round = [play_match(rng, teams, a, b, scale) for a, b in opening_matches]
    upper = [
        play_match(rng, teams, first_round[0][0], first_round[1][0], scale),
        play_match(rng, teams, first_round[2][0], first_round[3][0], scale),
        play_match(rng, teams, first_round[4][0], first_round[5][0], scale),
        play_match(rng, teams, first_round[6][0], first_round[7][0], scale),
    ]
    lower_round_1 = [
        play_match(rng, teams, first_round[0][1], first_round[1][1], scale),
        play_match(rng, teams, first_round[2][1], first_round[3][1], scale),
        play_match(rng, teams, first_round[4][1], first_round[5][1], scale),
        play_match(rng, teams, first_round[6][1], first_round[7][1], scale),
    ]
    lower_final = [
        play_match(rng, teams, upper[0][1], lower_round_1[2][0], scale),
        play_match(rng, teams, upper[2][1], lower_round_1[0][0], scale),
        play_match(rng, teams, upper[1][1], lower_round_1[3][0], scale),
        play_match(rng, teams, upper[3][1], lower_round_1[1][0], scale),
    ]
    return {match[0] for match in upper} | {match[0] for match in lower_final}


def summarize(advancers_by_sim: list[set[str]], names: list[str]) -> dict[str, float]:
    counts = Counter(name for advancers in advancers_by_sim for name in advancers)
    total = len(advancers_by_sim)
    return {name: counts[name] / total for name in names}


def save_sims(advancers_by_sim: list[set[str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for advancers in advancers_by_sim:
            handle.write(json.dumps(sorted(advancers), ensure_ascii=False) + "\n")


def render_report(
    event_name: str,
    teams: list[Team],
    probs: dict[str, float],
    predicted: list[str],
    actual: set[str],
    args: argparse.Namespace,
) -> str:
    hits = [name for name in predicted if name in actual]
    rows = [
        "| Team | VRS Rank | Points | P(Advance) | Actual Advanced |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for team in sorted(teams, key=lambda item: probs[item.name], reverse=True):
        rows.append(
            f"| {team.name} | {team.vrs_rank} | {team.points} | {format_percent(probs[team.name]).strip()} | "
            f"{'yes' if team.name in actual else 'no'} |"
        )
    return "\n".join(
        [
            f"# {event_name} Backtest",
            "",
            "## Summary",
            "",
            f"- Simulations: {args.sims:,}",
            f"- VRS snapshot: 2025-07-07, the closest Valve global snapshot before the 2025-07-23 Stage 1 start",
            f"- Match model: all Bo3, VRS logistic scale {args.scale:g}",
            f"- Prediction rule: choose the 8 teams with highest simulated Stage 2 advancement probability",
            f"- Backtest result: {len(hits)} / 8 actual Stage 2 advancers hit",
            "",
            "## Predicted Advancers",
            "",
            ", ".join(predicted),
            "",
            "## Actual Advancers",
            "",
            ", ".join(sorted(actual)),
            "",
            "## Hits",
            "",
            ", ".join(hits),
            "",
            "## Advancement Probabilities",
            "",
            *rows,
            "",
            "## Notes",
            "",
            "- This is not a Pick'Em reward optimizer because IEM Cologne 2025 Stage 1 did not use the Major 3-0 / advance / 0-3 Pick'Em layout.",
            "- It is a sanity backtest of the same VRS-to-win-probability model under the event's double-elimination Play-In bracket.",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", type=Path, default=Path("data/iem_cologne_2025_stage1.json"))
    parser.add_argument("--vrs-csv", type=Path, default=Path("data/vrs_2025-07-07_iem_cologne_stage1.csv"))
    parser.add_argument("--sims", type=int, default=30_000)
    parser.add_argument("--seed", type=int, default=20260707)
    parser.add_argument("--scale", type=float, default=400.0)
    parser.add_argument("--report", type=Path, default=Path("reports/iem_cologne_2025_stage1_backtest_report.md"))
    parser.add_argument("--save-sims", type=Path, default=Path("runs/iem_cologne_2025_stage1_vrs_2025-07-07_seed20260707_30000.jsonl"))
    args = parser.parse_args()

    event_name, event_teams, opening_matches, event_data = load_event(args.event)
    teams = build_teams(event_teams, load_vrs_csv(args.vrs_csv))
    teams_by_name = {team.name: team for team in teams}
    names = [team.name for team in teams]
    actual = set(event_data["actual_advancers"])

    rng = random.Random(args.seed)
    advancers_by_sim = [simulate_playin(rng, teams_by_name, opening_matches, args.scale) for _ in range(args.sims)]
    probs = summarize(advancers_by_sim, names)
    predicted = [team.name for team in sorted(teams, key=lambda item: probs[item.name], reverse=True)[:8]]
    hits = [name for name in predicted if name in actual]

    if args.save_sims:
        save_sims(advancers_by_sim, args.save_sims)

    lines = [
        f"Event: {event_name}",
        f"Simulations: {args.sims:,} | VRS logistic scale: {args.scale:g} | seed: {args.seed}",
        "",
        "Predicted Stage 2 advancers:",
        "  " + ", ".join(predicted),
        f"Backtest hits: {len(hits)} / 8",
        "  " + ", ".join(hits),
        "",
        "Team advancement probabilities",
        "Team                 Rank  VRS  P(adv)  Actual",
    ]
    for team in sorted(teams, key=lambda item: probs[item.name], reverse=True):
        lines.append(
            f"{team.name:20s} {team.vrs_rank:4d} {team.points:4d}  {format_percent(probs[team.name])}  "
            f"{'yes' if team.name in actual else 'no'}"
        )
    print("\n".join(lines))

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(render_report(event_name, teams, probs, predicted, actual, args) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
