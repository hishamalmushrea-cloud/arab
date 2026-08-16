# Libya Production Expansion Closeout

## Decision
**RELEASE CANDIDATE** pending exact-commit CI.
## Scope
Exact 141-name Ministry municipality catalogue, 22 historical 2006 sha‘biyat, mahallas unavailable.
## Snapshot
`SNP-LY-MUNICIPALITIES-2026-08-17`.
## Manifest
Current municipality and historical sha‘biya layers closed separately; mahallas unavailable.
## Denominators
Country 1; current municipalities 141; historical sha‘biyat 22; mahallas null.
## Entities
164 total: country, 141 municipalities, 22 historical sha‘biyat.
## Aliases
6 retained source-backed aliases.
## Relationships
163 country-parent relations; historical/current layers never mixed.
## Claims
0; no control/culture inference added.
## Sources
3 A-tier Ministry/law/BSC sources.
## Coverage
141/141 current catalogue; 22/22 historical 2006; mahallas unavailable.
## Cultural coverage
Not imported in refresh.
## Dialect coverage
0 Claims.
## Independent review
PASS locally: 344/344.
## Negative tests
PASS locally 8/8 subset/history/parent/count/control/mahalla/freshness mutations.
## P0/P1
0/0.
## make check
Pending clean commit.
## GitHub CI
Pending.
## Remaining limitations
No mahalla denominator; catalogue does not prove effective control; alternate-authority lists not unioned; culture/dialect deferred.
## Lessons learned
Rendered numbering gaps are not missing records; count exact names, bind checksum, and keep control overlays separate.
## Transferability
Schema 2.0.0 transfers without change.
## Recommended next country
Yemen Full Pilot for governorates, Capital Municipality, war-time de facto overlays, and district/uzla depth.
