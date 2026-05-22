# CS2 Pick'Em Monte Carlo

Monte Carlo optimizer for CS2 Pick'Em Swiss stages.

Current scope: this repository currently implements **Stage 1 only** for IEM
Cologne Major 2026. It does not yet model Stage 2, Stage 3, or Playoffs picks.

## Current Stage 1 Result

![IEM Cologne 2026 Stage 1 Pick'Em result](assets/pickem_result_card.png)

Reward target: maximize the chance of getting at least 5 correct Stage 1 picks.

| Pick category | Teams |
| --- | --- |
| `3-0` | SINNERS, BIG |
| `Advance` | GamerLegion, B8, BetBoom, MIBR, Lynn Vision, HEROIC |
| `0-3` | FlyQuest, THUNDER dOWNUNDER |

Model estimate: `P(hits >= 5) = 66.8%` in two 30,000-simulation convergence
checks. Full report: [`reports/iem_cologne_2026_stage1_report.md`](reports/iem_cologne_2026_stage1_report.md).

The main objective is the in-game reward threshold, for example "get five
correct Pick'Em predictions", not simply the highest average number of correct
picks.

## Quick Start

```powershell
python .\iem_cologne_pickem_mc.py --sims 10000 --report reports\iem_cologne_2026_stage1_report.md
```

The default event is IEM Cologne Major 2026 Stage 1, using:

- `data/iem_cologne_2026_stage1.json`
- `data/vrs_2026-05-22.csv`

## Updating VRS

Manual CSV workflow:

1. Copy the latest VRS values into a CSV with columns `team,vrs_rank,points`.
2. Run the optimizer with `--vrs-csv`:

```powershell
python .\iem_cologne_pickem_mc.py --vrs-csv data\vrs_new.csv --sims 10000
```

HLTV page workflow:

```powershell
python .\iem_cologne_pickem_mc.py --vrs-url "https://www.hltv.org/valve-ranking/teams/2026/may/22?teamId=7020" --write-vrs-csv data\vrs_2026-05-22_from_hltv.csv --sims 10000
```

If HLTV blocks direct Python requests, save the ranking page HTML from a
browser and import it offline:

```powershell
python .\iem_cologne_pickem_mc.py --vrs-html downloads\hltv_vrs.html --write-vrs-csv data\vrs_from_saved_page.csv --sims 10000
```

The fetched CSV is saved first so the data used by the simulation is auditable.

## Reusing For Future Events

Create a new event JSON with:

- `event_name`
- `teams`: seed and team name
- `opening_matches`: round 1 pairings
- optional metadata under `format` and `sources`

Then run:

```powershell
python .\iem_cologne_pickem_mc.py --event data\future_event.json --vrs-csv data\future_vrs.csv
```

## Model Assumptions

- 16-team Swiss stage.
- Teams advance at 3 wins and are eliminated at 3 losses.
- Round 1 and non-decider matches are Bo1.
- Advancement and elimination matches are Bo3.
- Later Swiss rounds are paired inside score groups by Buchholz score, avoiding rematches where possible.
- VRS point difference is translated into map win probability with a logistic curve.

Useful options:

- `--scale`: lower values make VRS gaps more decisive. Default: `400`.
- `--threshold`: reward threshold. Default: `5`.
- `--candidate-pool`: search breadth for reward optimization. Default: `10`.
- `--seed`: random seed for reproducibility.
- `--report`: write a markdown report.

## Simulation Count

For IEM Cologne Major 2026 Stage 1, 10,000 simulations were enough to identify
the same reward-optimized pick set across several random seeds. Two additional
30,000-simulation checks with seeds `101` and `102` also returned the same
recommended picks with `P(hits >= 5) = 66.8%`.

This is evidence of practical convergence for the current model, not a formal
guarantee. Model assumptions and VRS freshness matter more than the remaining
Monte Carlo sampling error.
