# IEM Cologne 2025 Stage 1 / Play-In Backtest

## Summary

- Simulations: 30,000
- VRS snapshot: 2025-07-07, the closest Valve global snapshot before the 2025-07-23 Stage 1 start
- Match model: all Bo3, VRS logistic scale 400
- Prediction rule: choose the 8 teams with highest simulated Stage 2 advancement probability
- Backtest result: 6 / 8 actual Stage 2 advancers hit

## Predicted Advancers

FaZe, FURIA, GamerLegion, HEROIC, 3DMAX, Virtus.pro, Astralis, paiN

## Actual Advancers

3DMAX, Astralis, FURIA, FaZe, GamerLegion, HEROIC, Liquid, Ninjas in Pyjamas

## Hits

FaZe, FURIA, GamerLegion, HEROIC, 3DMAX, Astralis

## Advancement Probabilities

| Team | VRS Rank | Points | P(Advance) | Actual Advanced |
| --- | ---: | ---: | ---: | --- |
| FaZe | 7 | 1638 | 83.9% | yes |
| FURIA | 9 | 1591 | 79.3% | yes |
| GamerLegion | 11 | 1537 | 69.5% | yes |
| HEROIC | 12 | 1528 | 68.3% | yes |
| 3DMAX | 13 | 1519 | 66.5% | yes |
| Virtus.pro | 14 | 1515 | 64.9% | no |
| Astralis | 15 | 1512 | 63.9% | yes |
| paiN | 16 | 1488 | 60.0% | no |
| Liquid | 17 | 1378 | 42.4% | yes |
| B8 | 19 | 1370 | 40.4% | no |
| TYLOO | 20 | 1358 | 37.7% | no |
| MIBR | 22 | 1342 | 34.8% | no |
| Ninjas in Pyjamas | 23 | 1314 | 30.5% | yes |
| Complexity | 24 | 1294 | 27.8% | no |
| FlyQuest | 30 | 1200 | 16.2% | no |
| BIG | 33 | 1176 | 13.8% | no |

## Notes

- This is not a Pick'Em reward optimizer because IEM Cologne 2025 Stage 1 did not use the Major 3-0 / advance / 0-3 Pick'Em layout.
- It is a sanity backtest of the same VRS-to-win-probability model under the event's double-elimination Play-In bracket.
