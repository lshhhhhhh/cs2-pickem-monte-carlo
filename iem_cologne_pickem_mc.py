#!/usr/bin/env python3
"""
Monte Carlo Pick'Em optimizer for CS2 Swiss stages.

Event structure and VRS strength data are loaded from files so the same code
can be reused for future Pick'Em stages.

Current implementation target: Stage 1 style 16-team Swiss Pick'Em only. Stage
2, Stage 3, and Playoffs are not modeled yet.
"""

from __future__ import annotations

import argparse
import csv
import html
import itertools
import json
import math
import random
import re
import sys
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PickSet = tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]
Result = tuple[dict[str, int], dict[str, int]]


@dataclass(frozen=True)
class Team:
    name: str
    seed: int
    vrs_rank: int
    points: int


def normalize_name(name: str) -> str:
    return re.sub(r"\s+", " ", name).strip().casefold()


def load_event(path: Path) -> tuple[str, list[dict[str, object]], list[tuple[str, str]], dict[str, object]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    teams = data["teams"]
    opening_matches = [tuple(match) for match in data["opening_matches"]]
    return data["event_name"], teams, opening_matches, data


def load_vrs_csv(path: Path) -> dict[str, tuple[int, int]]:
    rows: dict[str, tuple[int, int]] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows[normalize_name(row["team"])] = (int(row["vrs_rank"]), int(row["points"]))
    return rows


def build_teams(event_teams: list[dict[str, object]], vrs: dict[str, tuple[int, int]]) -> list[Team]:
    teams: list[Team] = []
    missing: list[str] = []
    for row in event_teams:
        name = str(row["name"])
        key = normalize_name(name)
        if key not in vrs:
            missing.append(name)
            continue
        rank, points = vrs[key]
        teams.append(Team(name=name, seed=int(row["seed"]), vrs_rank=rank, points=points))
    if missing:
        raise SystemExit(f"Missing VRS rows for: {', '.join(missing)}")
    return sorted(teams, key=lambda team: team.seed)


def strip_tags(value: str) -> str:
    value = re.sub(r"<script\b.*?</script>", " ", value, flags=re.IGNORECASE | re.DOTALL)
    value = re.sub(r"<style\b.*?</style>", " ", value, flags=re.IGNORECASE | re.DOTALL)
    value = re.sub(r"<[^>]+>", "\n", value)
    return html.unescape(value)


def parse_hltv_vrs_page(text: str) -> list[tuple[int, str, int]]:
    plain = strip_tags(text)
    pattern = re.compile(r"#\s*(\d+)\s+([^\n#()]+?)\s*\(\s*(\d+)\s+Valve points\s*\)", re.IGNORECASE)
    rows: list[tuple[int, str, int]] = []
    seen: set[str] = set()
    for rank_text, team, points_text in pattern.findall(plain):
        clean_team = re.sub(r"\s+", " ", team).strip()
        key = normalize_name(clean_team)
        if key in seen:
            continue
        seen.add(key)
        rows.append((int(rank_text), clean_team, int(points_text)))
    if not rows:
        raise SystemExit("Could not parse any VRS rows from the HLTV page.")
    return rows


def fetch_url(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def write_vrs_csv(rows: Iterable[tuple[int, str, int]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["team", "vrs_rank", "points"])
        for rank, team, points in rows:
            writer.writerow([team, rank, points])


def logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def bo3_from_map_prob(p_map: float) -> float:
    return p_map * p_map * (3.0 - 2.0 * p_map)


def win_probability(a: Team, b: Team, bo3: bool, scale: float) -> float:
    p_map = logistic((a.points - b.points) / scale)
    return bo3_from_map_prob(p_map) if bo3 else p_map


def make_pairings(group: list[str], wins: dict[str, int], opponents: dict[str, set[str]], teams: dict[str, Team]) -> list[tuple[str, str]]:
    def buchholz(name: str) -> int:
        return sum(wins[opp] for opp in opponents[name])

    ordered = sorted(group, key=lambda name: (-buchholz(name), teams[name].seed))
    pairings: list[tuple[str, str]] = []
    while ordered:
        first = ordered.pop(0)
        # Swiss rematches should be avoided; fall back only if unavoidable.
        idx = next((i for i, other in enumerate(ordered) if other not in opponents[first]), 0)
        second = ordered.pop(idx)
        pairings.append((first, second))
    return pairings


def simulate_stage(
    rng: random.Random,
    teams: dict[str, Team],
    opening_matches: list[tuple[str, str]],
    scale: float,
) -> Result:
    wins = {name: 0 for name in teams}
    losses = {name: 0 for name in teams}
    opponents: dict[str, set[str]] = {name: set() for name in teams}
    active = set(teams)

    pending = list(opening_matches)
    while pending:
        for a_name, b_name in pending:
            a = teams[a_name]
            b = teams[b_name]
            bo3 = wins[a_name] == 2 or losses[a_name] == 2
            p_a = win_probability(a, b, bo3=bo3, scale=scale)
            winner, loser = (a_name, b_name) if rng.random() < p_a else (b_name, a_name)
            wins[winner] += 1
            losses[loser] += 1
            opponents[a_name].add(b_name)
            opponents[b_name].add(a_name)
            if wins[winner] == 3:
                active.remove(winner)
            if losses[loser] == 3:
                active.remove(loser)

        pending = []
        for record_wins in (2, 1, 0):
            group = [name for name in active if wins[name] == record_wins]
            if group:
                pending.extend(make_pairings(group, wins, opponents, teams))

    return wins, losses


def summarize(results: list[Result], names: list[str]) -> dict[str, dict[str, float]]:
    total = len(results)
    summary = {name: defaultdict(float) for name in names}
    for wins, losses in results:
        for name in names:
            record = f"{wins[name]}-{losses[name]}"
            summary[name][record] += 1
            if wins[name] == 3:
                summary[name]["advance"] += 1
            if losses[name] == 3:
                summary[name]["eliminated"] += 1
    return {name: {key: value / total for key, value in values.items()} for name, values in summary.items()}


def pick_score(picks: PickSet, probs: dict[str, dict[str, float]]) -> float:
    three_oh, advance, zero_three = picks
    return (
        sum(probs[name].get("3-0", 0.0) for name in three_oh)
        + sum(probs[name].get("advance", 0.0) for name in advance)
        + sum(probs[name].get("0-3", 0.0) for name in zero_three)
    )


def optimize_expected(probs: dict[str, dict[str, float]], names: list[str]) -> tuple[float, PickSet]:
    best_score = -1.0
    best_picks: PickSet | None = None
    for three_oh in itertools.combinations(names, 2):
        remaining_after_30 = [name for name in names if name not in three_oh]
        for zero_three in itertools.combinations(remaining_after_30, 2):
            remaining = [name for name in remaining_after_30 if name not in zero_three]
            for advance in itertools.combinations(remaining, 6):
                picks = (three_oh, advance, zero_three)
                score = pick_score(picks, probs)
                if score > best_score:
                    best_score = score
                    best_picks = picks
    assert best_picks is not None
    return best_score, best_picks


def hit_distribution(picks: PickSet, results: Iterable[Result]) -> Counter[int]:
    three_oh, advance, zero_three = picks
    dist: Counter[int] = Counter()
    for wins, losses in results:
        hits = 0
        hits += sum(1 for name in three_oh if wins[name] == 3 and losses[name] == 0)
        hits += sum(1 for name in advance if wins[name] == 3)
        hits += sum(1 for name in zero_three if wins[name] == 0 and losses[name] == 3)
        dist[hits] += 1
    return dist


def build_hit_bitsets(results: list[Result], names: list[str]) -> dict[tuple[str, str], int]:
    bitsets: dict[tuple[str, str], int] = {}
    for category in ("3-0", "advance", "0-3"):
        for name in names:
            bits = 0
            for idx, (wins, losses) in enumerate(results):
                hit = (
                    (category == "3-0" and wins[name] == 3 and losses[name] == 0)
                    or (category == "advance" and wins[name] == 3)
                    or (category == "0-3" and wins[name] == 0 and losses[name] == 3)
                )
                if hit:
                    bits |= 1 << idx
            bitsets[(category, name)] = bits
    return bitsets


def bitset_hit_distribution(picks: PickSet, bitsets: dict[tuple[str, str], int], sample_count: int) -> Counter[int]:
    all_samples = (1 << sample_count) - 1
    exact = [0] * 11
    exact[0] = all_samples
    pick_bits = (
        [bitsets[("3-0", name)] for name in picks[0]]
        + [bitsets[("advance", name)] for name in picks[1]]
        + [bitsets[("0-3", name)] for name in picks[2]]
    )
    for bits in pick_bits:
        inverse = all_samples ^ bits
        next_exact = [0] * 11
        for hits in range(11):
            next_exact[hits] |= exact[hits] & inverse
            if hits < 10:
                next_exact[hits + 1] |= exact[hits] & bits
        exact = next_exact
    return Counter({hits: mask.bit_count() for hits, mask in enumerate(exact) if mask})


def optimize_threshold(
    probs: dict[str, dict[str, float]],
    results: list[Result],
    names: list[str],
    threshold: int,
    candidate_pool: int,
) -> tuple[float, PickSet, Counter[int]]:
    bitsets = build_hit_bitsets(results, names)
    three_candidates = sorted(names, key=lambda name: probs[name].get("3-0", 0.0), reverse=True)[: min(candidate_pool, len(names))]
    zero_candidates = sorted(names, key=lambda name: probs[name].get("0-3", 0.0), reverse=True)[: min(candidate_pool, len(names))]
    advance_candidates = sorted(names, key=lambda name: probs[name].get("advance", 0.0), reverse=True)[: min(candidate_pool + 4, len(names))]

    best_rate = -1.0
    best_picks: PickSet | None = None
    best_dist: Counter[int] = Counter()
    for three_oh in itertools.combinations(three_candidates, 2):
        for zero_three in itertools.combinations([name for name in zero_candidates if name not in three_oh], 2):
            remaining = [name for name in advance_candidates if name not in three_oh and name not in zero_three]
            if len(remaining) < 6:
                continue
            for advance in itertools.combinations(remaining, 6):
                picks = (three_oh, advance, zero_three)
                dist = bitset_hit_distribution(picks, bitsets, len(results))
                rate = sum(count for hits, count in dist.items() if hits >= threshold) / len(results)
                if rate > best_rate:
                    best_rate = rate
                    best_picks = picks
                    best_dist = dist
    assert best_picks is not None
    return best_rate, best_picks, best_dist


def format_percent(value: float) -> str:
    return f"{100.0 * value:5.1f}%"


def picks_lines(title: str, picks: PickSet) -> list[str]:
    three_oh, advance, zero_three = picks
    return [
        "",
        title,
        f"  3-0:      {', '.join(three_oh)}",
        f"  Advance:  {', '.join(advance)}",
        f"  0-3:      {', '.join(zero_three)}",
    ]


def render_output(
    event_name: str,
    teams: list[Team],
    probs: dict[str, dict[str, float]],
    results: list[Result],
    args: argparse.Namespace,
) -> tuple[str, str]:
    names = [team.name for team in sorted(teams, key=lambda item: item.seed)]
    lines: list[str] = [
        f"Event: {event_name}",
        f"Simulations: {args.sims:,} | VRS logistic scale: {args.scale:g} | seed: {args.seed}",
        "",
        "Team probabilities",
        "Team                 Rank  VRS  P(3-0)  P(adv)  P(0-3)  Most common records",
    ]
    for team in sorted(teams, key=lambda item: probs[item.name].get("advance", 0.0), reverse=True):
        row = probs[team.name]
        records = sorted(
            [(key, value) for key, value in row.items() if "-" in key],
            key=lambda item: item[1],
            reverse=True,
        )[:3]
        record_text = ", ".join(f"{record} {format_percent(prob).strip()}" for record, prob in records)
        lines.append(
            f"{team.name:20s} {team.vrs_rank:4d} {team.points:4d}  {format_percent(row.get('3-0', 0.0))}"
            f"  {format_percent(row.get('advance', 0.0))}  {format_percent(row.get('0-3', 0.0))}  {record_text}"
        )

    threshold_rate, threshold_picks, threshold_dist = optimize_threshold(
        probs, results, names, threshold=args.threshold, candidate_pool=args.candidate_pool
    )
    expected_hits = sum(hit * count for hit, count in threshold_dist.items()) / args.sims
    lines.extend(picks_lines(f"Reward-optimized picks by P(>={args.threshold} hits): {format_percent(threshold_rate)}", threshold_picks))
    lines.append(f"  Expected hits: {expected_hits:.3f} / 10")
    lines.append(
        "  Hit distribution: "
        + ", ".join(f"{hit}:{format_percent(count / args.sims).strip()}" for hit, count in sorted(threshold_dist.items()))
    )

    expected_score, expected_picks = optimize_expected(probs, names)
    expected_dist = hit_distribution(expected_picks, results)
    lines.extend(picks_lines(f"Reference only: best by expected correct picks: {expected_score:.3f} / 10", expected_picks))
    lines.append(f"  P(>={args.threshold} hits): {format_percent(sum(v for k, v in expected_dist.items() if k >= args.threshold) / args.sims)}")

    report = render_markdown_report(event_name, teams, probs, args, threshold_rate, threshold_picks, threshold_dist, expected_score, expected_picks, expected_dist)
    return "\n".join(lines), report


def render_markdown_report(
    event_name: str,
    teams: list[Team],
    probs: dict[str, dict[str, float]],
    args: argparse.Namespace,
    threshold_rate: float,
    threshold_picks: PickSet,
    threshold_dist: Counter[int],
    expected_score: float,
    expected_picks: PickSet,
    expected_dist: Counter[int],
) -> str:
    threshold_hits = sum(hit * count for hit, count in threshold_dist.items()) / args.sims
    expected_rate = sum(v for k, v in expected_dist.items() if k >= args.threshold) / args.sims
    rows = [
        "| Team | VRS Rank | Points | P(3-0) | P(Advance) | P(0-3) |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for team in sorted(teams, key=lambda item: probs[item.name].get("advance", 0.0), reverse=True):
        row = probs[team.name]
        rows.append(
            f"| {team.name} | {team.vrs_rank} | {team.points} | {format_percent(row.get('3-0', 0.0)).strip()} | "
            f"{format_percent(row.get('advance', 0.0)).strip()} | {format_percent(row.get('0-3', 0.0)).strip()} |"
        )

    def pick_block(picks: PickSet) -> str:
        return "\n".join(
            [
                f"- 3-0: {', '.join(picks[0])}",
                f"- Advance: {', '.join(picks[1])}",
                f"- 0-3: {', '.join(picks[2])}",
            ]
        )

    return "\n".join(
        [
            f"# {event_name} Pick'Em Report",
            "",
            "## Summary",
            "",
            f"- Simulations: {args.sims:,}",
            f"- Reward target: at least {args.threshold} correct picks",
            f"- VRS logistic scale: {args.scale:g}",
            f"- Random seed: {args.seed}",
            f"- Reward-optimized success probability: {format_percent(threshold_rate).strip()}",
            f"- Reward-optimized expected hits: {threshold_hits:.3f} / 10",
            "",
            "## Recommended Picks",
            "",
            pick_block(threshold_picks),
            "",
            "## Reference: Expected-Hit Optimizer",
            "",
            f"- Expected hits: {expected_score:.3f} / 10",
            f"- Probability of reward threshold: {format_percent(expected_rate).strip()}",
            "",
            pick_block(expected_picks),
            "",
            "## Team Probabilities",
            "",
            *rows,
            "",
            "## Notes",
            "",
            "- The reward optimizer maximizes the chance of crossing the Pick'Em reward threshold, not raw average hit count.",
            "- Swiss pairings after round 1 are approximated inside score groups by Buchholz, with rematches avoided where possible.",
            "- VRS points are translated into map win probability with a logistic curve; change `--scale` for sensitivity testing.",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", type=Path, default=Path("data/iem_cologne_2026_stage1.json"))
    parser.add_argument("--vrs-csv", type=Path, default=Path("data/vrs_2026-05-22.csv"))
    parser.add_argument("--vrs-url", help="Optional HLTV Valve ranking URL to fetch and convert to CSV before simulation.")
    parser.add_argument("--vrs-html", type=Path, help="Optional saved HLTV Valve ranking HTML/text file to convert to CSV before simulation.")
    parser.add_argument("--write-vrs-csv", type=Path, help="Where to save rows fetched from --vrs-url.")
    parser.add_argument("--sims", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=20260522)
    parser.add_argument("--scale", type=float, default=400.0, help="Lower values make VRS gaps more decisive.")
    parser.add_argument("--threshold", type=int, default=5)
    parser.add_argument("--candidate-pool", type=int, default=10)
    parser.add_argument("--report", type=Path, help="Optional markdown report output path.")
    args = parser.parse_args()

    if args.vrs_url and args.vrs_html:
        raise SystemExit("Use only one of --vrs-url or --vrs-html.")

    if args.vrs_url or args.vrs_html:
        source_text = fetch_url(args.vrs_url) if args.vrs_url else args.vrs_html.read_text(encoding="utf-8")
        rows = parse_hltv_vrs_page(source_text)
        if not args.write_vrs_csv:
            raise SystemExit("--vrs-url/--vrs-html requires --write-vrs-csv so the imported data is auditable.")
        write_vrs_csv(rows, args.write_vrs_csv)
        args.vrs_csv = args.write_vrs_csv

    event_name, event_teams, opening_matches, _event_data = load_event(args.event)
    teams = build_teams(event_teams, load_vrs_csv(args.vrs_csv))
    teams_by_name = {team.name: team for team in teams}
    unknown_matches = sorted({name for match in opening_matches for name in match if name not in teams_by_name})
    if unknown_matches:
        raise SystemExit(f"Opening matches reference unknown teams: {', '.join(unknown_matches)}")

    rng = random.Random(args.seed)
    results = [simulate_stage(rng, teams_by_name, opening_matches, args.scale) for _ in range(args.sims)]
    probs = summarize(results, [team.name for team in teams])
    text, report = render_output(event_name, teams, probs, results, args)
    print(text)

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
