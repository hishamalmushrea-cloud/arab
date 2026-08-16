# Next Country Decision

## Current country

Kuwait — Direct Structured Expansion.

## Current result

**RELEASE CANDIDATE.** Kuwait local data, semantic validation, 34/34 independent review, and 9/9 mutations pass; exact-commit CI is pending.

## Remaining countries

Qatar, Oman, Djibouti, Morocco, Algeria, Egypt, Mauritania, Lebanon, Comoros, Palestine, Iraq, Libya, Yemen, Syria, Somalia, Sudan.

## Ranking

| Rank | Country | Mode | Priority | Reason | Risk |
|---:|---|---|:---:|---|---|
| 1 | Qatar | Direct Structured Expansion | P1 | bounded municipality layer and strong statistics | municipality/zone/district/fareej conflation |
| 2 | Oman | Micro Pilot | P2 | stable governorate/wilaya model | deeper wilaya/niyaba denominator and decree dates |
| 3 | Djibouti | Micro Pilot | P2 | manageable size | special capital structure and parallel municipal/sub-prefecture paths |
| 4 | Morocco | Micro Pilot | P2 | strong authority expected | prefecture/province parallelism and commune denominator |
| 5 | Algeria | Micro Pilot | P2 | official hierarchy sources expected | scale and announced transitions |
| 6 | Egypt | Full Pilot | P3 | strong statistics | very large dual rural/urban lower hierarchy |
| 7 | Mauritania | Micro Pilot | P3 | three principal tiers | conflicting local denominators/source quality |
| 8 | Lebanon | Micro Pilot | P3 | bounded upper layers | recent temporal change and municipal unions |
| 9 | Comoros | Full Pilot | P3 | small record count | weak/conflicting island/prefecture/commune authority |
| 10 | Palestine | Full Pilot | P4 | strong statistical evidence | legal/de facto/disputed/displaced semantics |
| 11 | Iraq | Full Pilot | P4 | official and regional sources | federal/Kurdistan paths, disputed areas, Halabja timing |
| 12 | Libya | Full Pilot | P4 | existing bounded baseline | divided/variable current municipal denominator |
| 13 | Yemen | Full Pilot | P4 | known legal hierarchy | war, capital municipality, legal/de facto divergence |
| 14 | Syria | Full Pilot | P4 | legal hierarchy known | rapidly changing status, destruction/displacement |
| 15 | Somalia | Full Pilot | P4 | federal-member structure | Somaliland and competing territorial claims |
| 16 | Sudan | Full Pilot | P4 | legal state layer | war and highest current/status volatility |

## Recommended next country

**Qatar — Direct Structured Expansion.**

## Why

Qatar is now the highest remaining direct-expansion candidate. It tests a distinct boundary: municipalities versus numbered zones, districts, and fareej, with strong expected Ministry of Municipality and Planning and Statistics Authority evidence.

## Why not the alternatives

Oman needs a micro-pilot for wilaya/niyaba depth and decree timing. Groups B–D introduce scale, parallel structures, weak denominators, or conflict before two production-direct cycles have stabilized the workflow.

## Expected difficulty

Moderate. The municipality denominator should be bounded; the primary QA burden is preventing zone/district/fareej conflation and documenting unavailable lower denominators.
