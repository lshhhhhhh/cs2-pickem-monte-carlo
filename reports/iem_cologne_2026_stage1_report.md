# IEM Cologne Major 2026 Stage 1 Pick'Em Report

## Summary

- Simulations: 10,000
- Reward target: at least 5 correct picks
- VRS logistic scale: 400
- Random seed: 20260522
- Reward-optimized success probability: 66.6%
- Reward-optimized expected hits: 4.968 / 10

## Recommended Picks

- 3-0: SINNERS, TYLOO
- Advance: GamerLegion, B8, MIBR, BetBoom, Lynn Vision, HEROIC
- 0-3: FlyQuest, THUNDER dOWNUNDER

## Reference: Expected-Hit Optimizer

- Expected hits: 5.005 / 10
- Probability of reward threshold: 66.4%

- 3-0: BIG, SINNERS
- Advance: GamerLegion, B8, HEROIC, BetBoom, MIBR, Lynn Vision
- 0-3: NRG, FlyQuest

## Team Probabilities

| Team | VRS Rank | Points | P(3-0) | P(Advance) | P(0-3) |
| --- | ---: | ---: | ---: | ---: | ---: |
| GamerLegion | 11 | 1726 | 34.7% | 88.7% | 1.8% |
| B8 | 16 | 1591 | 18.9% | 73.3% | 4.7% |
| MIBR | 19 | 1544 | 24.3% | 73.2% | 3.9% |
| BetBoom | 17 | 1562 | 22.1% | 73.1% | 4.2% |
| Lynn Vision | 24 | 1442 | 16.1% | 60.8% | 6.7% |
| HEROIC | 23 | 1447 | 12.0% | 56.9% | 8.5% |
| SINNERS | 30 | 1382 | 12.8% | 52.1% | 8.1% |
| BIG | 27 | 1415 | 11.2% | 51.9% | 10.4% |
| TYLOO | 29 | 1390 | 9.8% | 48.1% | 12.6% |
| M80 | 31 | 1379 | 9.0% | 46.3% | 13.3% |
| Liquid | 41 | 1309 | 7.8% | 39.5% | 13.9% |
| Sharks | 46 | 1282 | 6.3% | 35.7% | 16.8% |
| NRG | 50 | 1271 | 3.7% | 28.7% | 24.2% |
| Gaimin Gladiators | 53 | 1237 | 4.3% | 28.2% | 22.7% |
| THUNDER dOWNUNDER | 57 | 1211 | 4.1% | 26.0% | 22.0% |
| FlyQuest | 76 | 1130 | 2.9% | 17.7% | 26.4% |

## Notes

- The reward optimizer maximizes the chance of crossing the Pick'Em reward threshold, not raw average hit count.
- Swiss pairings after round 1 are approximated inside score groups by Buchholz, with rematches avoided where possible.
- VRS points are translated into map win probability with a logistic curve; change `--scale` for sensitivity testing.
