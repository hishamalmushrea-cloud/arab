# Next Country Decision

## Current country

Bahrain — Direct Structured Expansion.

## Current result

**PASS.** Exact Bahrain release commit `b4971929b4e4aac31ac24bf364fc8f1de49177e7`; local `make check`, 88-check Phase 5 gate, 21-check Bahrain gate, Push Action, and PR Action all pass.

## Remaining countries

Kuwait, Qatar, Oman, Djibouti, Morocco, Algeria, Egypt, Mauritania, Lebanon, Comoros, Palestine, Iraq, Libya, Yemen, Syria, Somalia, Sudan.

## Ranking

| Rank | Country | Mode | Priority | Reason | Risk |
|---:|---|---|:---:|---|---|
| 1 | Kuwait | Direct Structured Expansion | P1 | compact governorate layer; strong expected government/statistical sources; best test of governorate vs address area/block | address units may be mistaken for municipalities |
| 2 | Qatar | Direct Structured Expansion | P1 | bounded municipality layer and strong statistics | municipality/zone/district/fareej conflation |
| 3 | Oman | Micro Pilot | P2 | stable governorate/wilaya model | deeper wilaya/niyaba denominator and decree dates |
| 4 | Djibouti | Micro Pilot | P2 | manageable size | special capital structure and parallel municipal/sub-prefecture paths |
| 5 | Morocco | Micro Pilot | P2 | strong authority expected | prefecture/province parallelism and commune denominator |
| 6 | Algeria | Micro Pilot | P2 | official hierarchy sources expected | scale and announced transitions |
| 7 | Egypt | Full Pilot | P3 | strong statistics | very large dual rural/urban lower hierarchy |
| 8 | Mauritania | Micro Pilot | P3 | three principal tiers | conflicting local denominators/source quality |
| 9 | Lebanon | Micro Pilot | P3 | bounded upper layers | recent temporal change and municipal unions |
| 10 | Comoros | Full Pilot | P3 | small record count | weak/conflicting island/prefecture/commune authority |
| 11 | Palestine | Full Pilot | P4 | strong statistical evidence | legal/de facto/disputed/displaced semantics |
| 12 | Iraq | Full Pilot | P4 | official and regional sources | federal/Kurdistan paths, disputed areas, Halabja timing |
| 13 | Libya | Full Pilot | P4 | existing bounded baseline | divided/variable current municipal denominator |
| 14 | Yemen | Full Pilot | P4 | known legal hierarchy | war, capital municipality, legal/de facto divergence |
| 15 | Syria | Full Pilot | P4 | legal hierarchy known | rapidly changing status, destruction/displacement |
| 16 | Somalia | Full Pilot | P4 | federal-member structure | Somaliland and competing territorial claims |
| 17 | Sudan | Full Pilot | P4 | legal state layer | war and highest current/status volatility |

## Recommended next country

**Kuwait — Direct Structured Expansion.**

## Why

It is the highest remaining readiness candidate after Bahrain, keeps operational load bounded, and provides a non-duplicative transfer test: the system must distinguish six governorates from address areas and numbered blocks. Expected source quality is high through Kuwait government, the Public Authority for Civil Information, and the Central Statistical Bureau.

## Why not the alternatives

Qatar is close but offers a similar compact direct cycle and is slightly riskier at zone/district/fareej boundaries. Oman needs a micro-pilot for wilaya/niyaba depth and decree timing. Groups B–D introduce scale, parallel structures, weak denominators, or conflict before two production-direct cycles have stabilized the workflow.

## Expected difficulty

Moderate. The upper denominator should be straightforward; the main QA burden is refusing to convert address/statistical units into administrative hierarchy and documenting unavailable lower denominators.
