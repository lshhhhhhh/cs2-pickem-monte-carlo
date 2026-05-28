# BLAST.tv Austin Major 2025 Stage 1 Pick'Em Report

## Summary

- Simulations: 30,000
- Reward target: at least 5 correct picks
- VRS logistic scale: 400
- Random seed: 20260522
- Reward search: candidate-pruned search
- Reward-optimized success probability: 66.8%
- Reward-optimized expected hits: 4.963 / 10

## Recommended Picks

- 3-0: NRG, BetBoom
- Advance: HEROIC, Complexity, TYLOO, B8, FlyQuest, Lynn Vision
- 0-3: Fluxo, Metizport

## Reference: Expected-Hit Optimizer

- Expected hits: 4.969 / 10
- Probability of reward threshold: 66.6%

- 3-0: NRG, Nemiga
- Advance: Complexity, HEROIC, B8, TYLOO, Lynn Vision, FlyQuest
- 0-3: Fluxo, Metizport

## Team Probabilities

| Team | VRS Rank | Points | P(3-0) | P(Advance) | P(0-3) |
| --- | ---: | ---: | ---: | ---: | ---: |
| HEROIC | 13 | 1552 | 37.4% | 92.0% | 1.1% |
| Complexity | 17 | 1433 | 23.8% | 82.8% | 2.8% |
| TYLOO | 18 | 1358 | 23.0% | 76.9% | 3.9% |
| B8 | 20 | 1275 | 15.3% | 65.4% | 6.6% |
| FlyQuest | 24 | 1213 | 18.2% | 62.2% | 6.7% |
| Lynn Vision | 25 | 1212 | 14.8% | 59.1% | 7.6% |
| NRG | 32 | 1121 | 7.9% | 44.5% | 14.1% |
| BetBoom | 36 | 1102 | 7.7% | 41.2% | 13.9% |
| OG | 38 | 1097 | 6.6% | 39.1% | 17.1% |
| Imperial | 41 | 1074 | 7.4% | 38.5% | 16.2% |
| Nemiga | 45 | 1045 | 8.3% | 37.2% | 15.7% |
| Chinggis Warriors | 40 | 1087 | 5.0% | 36.8% | 19.1% |
| Wildcard | 48 | 1037 | 7.8% | 35.4% | 15.2% |
| Legacy | 49 | 1035 | 6.6% | 34.2% | 17.8% |
| Fluxo | 55 | 999 | 5.0% | 28.5% | 21.5% |
| Metizport | 60 | 959 | 5.1% | 26.2% | 20.8% |

## Notes

- The reward optimizer maximizes the chance of crossing the Pick'Em reward threshold, not raw average hit count.
- Swiss pairings after round 1 are approximated inside score groups by Buchholz, with rematches avoided where possible.
- VRS points are translated into map win probability with a logistic curve; change `--scale` for sensitivity testing.
