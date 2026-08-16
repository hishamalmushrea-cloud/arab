# Egypt Production Expansion Closeout

## Decision
**PASS.** Egypt Production Full Pilot stage one accepted on exact commit `ac5b159f31600e42c306dfd2ef2d305534cb4c77`.
## Scope
27 governorates and explicit four-urban/23-mixed administrative profiles; lower topology deferred.
## Snapshot
`SNP-EG-PRODUCTION-20260816`; CAPMAS profile reference 2021.
## Manifest
Governorates/profile layers closed; markaz, qism, local-unit, shiyakha unavailable.
## Denominators
Country 1; governorates 27; urban-only profiles 4; mixed profiles 23.
## Entities
28 total; 27 new.
## Aliases
27 official English forms.
## Relationships
27 country parents.
## Claims
27 official administrative-profile Claims.
## Sources
3 A-tier CAPMAS/MLD/code sources.
## Coverage
27/27 governorates; 4/4 urban-only; 23/23 mixed.
## Cultural coverage
Not imported in Full Pilot stage 1.
## Dialect coverage
0 Claims.
## Independent review
PASS locally: 120/120.
## Negative tests
PASS locally 8/8 city/governorate, profile, parent, denominator, lower-path and alias mutations.
## P0/P1
0/0.
## make check
PASS: Phase 5 88/88 plus eight production gates 21/21; full `make check` = 256 checks.
## GitHub CI
PASS: Push Action `31971681490` and PR Action `31971683328`.
## Remaining limitations
No markaz/qism/local-unit/shiyakha records; Cairo/Giza lower topology remains next stage; population/culture deferred.
## Lessons learned
Governorate profile must precede lower imports; city identity and rural/urban paths cannot be inferred from names.
## Transferability
Schema 2.0.0 supports parallel lower profiles without change.
## Recommended next country
Mauritania Micro Pilot for wilaya/moughataa/commune denominator reconciliation.
