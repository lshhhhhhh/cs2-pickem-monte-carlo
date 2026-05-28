# IEM Cologne Major 2026 Stage 1 Pick'Em Report

## Summary

- Simulations: 30,000
- Reward target: at least 5 correct picks
- VRS logistic scale: 400
- Random seed: 20260522
- Reward search: candidate-pruned search
- Reward-optimized success probability: 67.4%
- Reward-optimized expected hits: 4.996 / 10

## Recommended Picks

- 3-0: SINNERS, BIG
- Advance: GamerLegion, BetBoom, B8, MIBR, Lynn Vision, HEROIC
- 0-3: FlyQuest, THUNDER dOWNUNDER

## Reference: Expected-Hit Optimizer

- Expected hits: 5.020 / 10
- Probability of reward threshold: 67.3%

- 3-0: BIG, SINNERS
- Advance: GamerLegion, B8, HEROIC, BetBoom, MIBR, Lynn Vision
- 0-3: NRG, FlyQuest

## Team Probabilities

| Team | VRS Rank | Points | P(3-0) | P(Advance) | P(0-3) |
| --- | ---: | ---: | ---: | ---: | ---: |
| GamerLegion | 11 | 1726 | 35.0% | 88.4% | 1.8% |
| BetBoom | 17 | 1562 | 22.4% | 74.2% | 4.1% |
| B8 | 16 | 1591 | 18.6% | 73.9% | 4.6% |
| MIBR | 19 | 1544 | 24.0% | 73.1% | 4.0% |
| Lynn Vision | 24 | 1442 | 16.3% | 60.9% | 6.6% |
| HEROIC | 23 | 1447 | 12.2% | 56.3% | 8.6% |
| SINNERS | 30 | 1382 | 13.2% | 52.5% | 8.1% |
| BIG | 27 | 1415 | 11.5% | 52.2% | 10.1% |
| TYLOO | 29 | 1390 | 9.1% | 48.4% | 12.6% |
| M80 | 31 | 1379 | 8.6% | 45.6% | 13.1% |
| Liquid | 41 | 1309 | 7.7% | 39.3% | 14.1% |
| Sharks | 46 | 1282 | 6.3% | 34.9% | 16.9% |
| NRG | 50 | 1271 | 3.7% | 28.8% | 24.2% |
| Gaimin Gladiators | 53 | 1237 | 4.4% | 27.6% | 23.1% |
| THUNDER dOWNUNDER | 57 | 1211 | 4.1% | 25.7% | 21.8% |
| FlyQuest | 76 | 1130 | 3.0% | 18.2% | 26.3% |

## Notes

- The reward optimizer maximizes the chance of crossing the Pick'Em reward threshold, not raw average hit count.
- Swiss pairings after round 1 are approximated inside score groups by Buchholz, with rematches avoided where possible.
- VRS points are translated into map win probability with a logistic curve; change `--scale` for sensitivity testing.
