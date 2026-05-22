# IEM Cologne Major 2026 Stage 1 Pick'Em Report

This report covers Stage 1 only. It does not include Stage 2, Stage 3, or
Playoffs Pick'Em predictions.

## Summary

- Simulations: 10,000
- Reward target: at least 5 correct picks
- VRS logistic scale: 400
- Random seed: 20260522
- Reward-optimized success probability: 66.1%
- Reward-optimized expected hits: 4.971 / 10

## Recommended Picks

- 3-0: SINNERS, BIG
- Advance: GamerLegion, B8, BetBoom, MIBR, Lynn Vision, HEROIC
- 0-3: FlyQuest, THUNDER dOWNUNDER

## Reference: Expected-Hit Optimizer

- Expected hits: 4.986 / 10
- Probability of reward threshold: 65.6%

- 3-0: BIG, SINNERS
- Advance: GamerLegion, B8, HEROIC, BetBoom, MIBR, Lynn Vision
- 0-3: NRG, FlyQuest

## Team Probabilities

| Team | VRS Rank | Points | P(3-0) | P(Advance) | P(0-3) |
| --- | ---: | ---: | ---: | ---: | ---: |
| GamerLegion | 11 | 1739 | 34.2% | 88.4% | 1.9% |
| B8 | 16 | 1608 | 19.7% | 74.3% | 4.6% |
| BetBoom | 18 | 1575 | 21.7% | 73.0% | 4.6% |
| MIBR | 19 | 1545 | 23.8% | 71.8% | 4.2% |
| Lynn Vision | 25 | 1438 | 15.0% | 58.4% | 7.4% |
| HEROIC | 23 | 1469 | 12.7% | 58.2% | 8.2% |
| SINNERS | 28 | 1391 | 13.0% | 51.9% | 8.4% |
| BIG | 26 | 1422 | 11.1% | 50.8% | 10.6% |
| M80 | 29 | 1389 | 9.0% | 46.4% | 13.3% |
| TYLOO | 27 | 1391 | 9.1% | 45.9% | 13.5% |
| Liquid | 36 | 1327 | 8.2% | 39.8% | 13.9% |
| Sharks | 43 | 1296 | 6.2% | 35.7% | 17.1% |
| Gaimin Gladiators | 47 | 1285 | 5.2% | 32.4% | 19.9% |
| NRG | 42 | 1296 | 4.1% | 30.1% | 23.4% |
| THUNDER dOWNUNDER | 56 | 1222 | 4.2% | 26.1% | 21.9% |
| FlyQuest | 74 | 1135 | 2.7% | 16.7% | 27.0% |

## Notes

- The reward optimizer maximizes the chance of crossing the Pick'Em reward threshold, not raw average hit count.
- Swiss pairings after round 1 are approximated inside score groups by Buchholz, with rematches avoided where possible.
- VRS points are translated into map win probability with a logistic curve; change `--scale` for sensitivity testing.

## Convergence Check

- The 10,000-simulation recommendation was stable across several random seeds.
- Two additional 30,000-simulation runs with seeds `101` and `102` both returned the same reward-optimized picks:
  - 3-0: SINNERS, BIG
  - Advance: GamerLegion, B8, BetBoom, MIBR, Lynn Vision, HEROIC
  - 0-3: FlyQuest, THUNDER dOWNUNDER
- Both 30,000-simulation runs estimated `P(hits >= 5)` at 66.8%.
- This supports practical convergence for the current model, but it is not a formal guarantee.
