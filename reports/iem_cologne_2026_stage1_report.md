# IEM Cologne Major 2026 Stage 1 Pick'Em Report

## Summary

- Simulations: 30,000
- Reward target: at least 5 correct picks
- VRS logistic scale: 400
- Random seed: 20260522
- Reward search: candidate-pruned search
- Reward-optimized success probability: 32.7%
- Reward-optimized expected hits: 3.854 / 10

## Recommended Picks

- 3-0: GamerLegion, MIBR
- Advance: B8, BetBoom, Lynn Vision, HEROIC, BIG, TYLOO
- 0-3: FlyQuest, NRG

## Reference: Expected-Hit Optimizer

- Expected hits: 3.854 / 10
- Probability of reward threshold: 32.4%

- 3-0: GamerLegion, MIBR
- Advance: B8, HEROIC, BetBoom, BIG, SINNERS, Lynn Vision
- 0-3: NRG, FlyQuest

## Team Probabilities

| Team | VRS Rank | Points | P(3-0) | P(3-1/3-2) | P(0-3) |
| --- | ---: | ---: | ---: | ---: | ---: |
| GamerLegion | 11 | 1726 | 35.0% | 53.4% | 1.8% |
| BetBoom | 17 | 1562 | 22.4% | 51.8% | 4.1% |
| B8 | 16 | 1591 | 18.6% | 55.3% | 4.6% |
| MIBR | 19 | 1544 | 24.0% | 49.1% | 4.0% |
| Lynn Vision | 24 | 1442 | 16.3% | 44.6% | 6.6% |
| HEROIC | 23 | 1447 | 12.2% | 44.2% | 8.6% |
| SINNERS | 30 | 1382 | 13.2% | 39.3% | 8.1% |
| BIG | 27 | 1415 | 11.5% | 40.8% | 10.1% |
| TYLOO | 29 | 1390 | 9.1% | 39.3% | 12.6% |
| M80 | 31 | 1379 | 8.6% | 37.0% | 13.1% |
| Liquid | 41 | 1309 | 7.7% | 31.7% | 14.1% |
| Sharks | 46 | 1282 | 6.3% | 28.6% | 16.9% |
| NRG | 50 | 1271 | 3.7% | 25.1% | 24.2% |
| Gaimin Gladiators | 53 | 1237 | 4.4% | 23.2% | 23.1% |
| THUNDER dOWNUNDER | 57 | 1211 | 4.1% | 21.6% | 21.8% |
| FlyQuest | 76 | 1130 | 3.0% | 15.2% | 26.3% |

## Notes

- The reward optimizer maximizes the chance of crossing the Pick'Em reward threshold, not raw average hit count.
- Swiss pairings after round 1 are approximated inside score groups by Buchholz, with rematches avoided where possible.
- VRS points are translated into map win probability with a logistic curve; change `--scale` for sensitivity testing.
