# BLAST.tv Austin Major 2025 Stage 1 Pick'Em Report

## Summary

- Simulations: 30,000
- Reward target: at least 5 correct picks
- VRS logistic scale: 400
- Random seed: 20260522
- Reward search: candidate-pruned search
- Reward-optimized success probability: 29.9%
- Reward-optimized expected hits: 3.752 / 10

## Recommended Picks

- 3-0: HEROIC, FlyQuest
- Advance: Complexity, TYLOO, B8, Lynn Vision, NRG, BetBoom
- 0-3: Fluxo, Metizport

## Reference: Expected-Hit Optimizer

- Expected hits: 3.758 / 10
- Probability of reward threshold: 29.4%

- 3-0: HEROIC, Nemiga
- Advance: Complexity, B8, TYLOO, Lynn Vision, FlyQuest, NRG
- 0-3: Fluxo, Metizport

## Team Probabilities

| Team | VRS Rank | Points | P(3-0) | P(3-1/3-2) | P(0-3) |
| --- | ---: | ---: | ---: | ---: | ---: |
| HEROIC | 13 | 1552 | 37.4% | 54.6% | 1.1% |
| Complexity | 17 | 1433 | 23.8% | 58.9% | 2.8% |
| TYLOO | 18 | 1358 | 23.0% | 53.9% | 3.9% |
| B8 | 20 | 1275 | 15.3% | 50.2% | 6.6% |
| FlyQuest | 24 | 1213 | 18.2% | 44.0% | 6.7% |
| Lynn Vision | 25 | 1212 | 14.8% | 44.2% | 7.6% |
| NRG | 32 | 1121 | 7.9% | 36.6% | 14.1% |
| BetBoom | 36 | 1102 | 7.7% | 33.5% | 13.9% |
| OG | 38 | 1097 | 6.6% | 32.6% | 17.1% |
| Imperial | 41 | 1074 | 7.4% | 31.0% | 16.2% |
| Nemiga | 45 | 1045 | 8.3% | 28.9% | 15.7% |
| Chinggis Warriors | 40 | 1087 | 5.0% | 31.8% | 19.1% |
| Wildcard | 48 | 1037 | 7.8% | 27.6% | 15.2% |
| Legacy | 49 | 1035 | 6.6% | 27.6% | 17.8% |
| Fluxo | 55 | 999 | 5.0% | 23.4% | 21.5% |
| Metizport | 60 | 959 | 5.1% | 21.1% | 20.8% |

## Notes

- The reward optimizer maximizes the chance of crossing the Pick'Em reward threshold, not raw average hit count.
- Swiss pairings after round 1 are approximated inside score groups by Buchholz, with rematches avoided where possible.
- VRS points are translated into map win probability with a logistic curve; change `--scale` for sensitivity testing.
