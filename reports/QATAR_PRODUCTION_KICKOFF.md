# Qatar Production Expansion — Kickoff

## Status

**STARTED — evidence assessment only; no Qatar production Entity/Claim/Source/Denominator added yet.**

## Mode

Direct Structured Expansion. First closure target: eight municipalities. Zones, districts, blocks, fareej, and cities remain separate concepts and are not inferred.

## Initial evidence

- Planning and Statistics Authority Census 2020 detailed results enumerates Doha, Al Rayyan, Al Wakra, Umm Slal, Al Khor and Al Thakhira, Al Shamal, Al Daayen, and Al Sheehaniya with 2020 population totals.
- Qatar National Master Plan states that Municipality Spatial Development Plans cover each of the nation's eight municipalities and enumerates the same eight.
- PSA's historical documentation states municipality → zone → block, but that older ten-municipality topology must not be reused as the current eight-municipality denominator.
- UNESCO evidence indicates Al Zubarah Archaeological Site is the inscribed property candidate; the State Party register must be opened and checksum-bound before emission.

## Principal risks

1. `municipality`, numbered `zone`, district, block, city, and fareej conflation.
2. Reusing the historical ten-municipality structure as current.
3. Spelling variants (`Umm Slal/Salal`, `Al Daayen/Al Dhaayen`, `Al Sheehaniya/Al Shahaniya`) creating duplicate entities.
4. Treating census population as legal municipality creation evidence.
5. Assigning city Claims to municipality entities.

## Planned controls

- Exact eight-name bilingual/current denominator from two official authorities.
- Census populations dated 2020 only, with source-specific spelling preserved as Aliases.
- No zones/blocks without a separate current denominator and topology.
- Mutations for historical-ten-as-current, zone-as-municipality, city/municipality leakage, spelling duplicates, wrong parent, foreign source, population tampering, and unsupported dialect.

## Next action

Persist exact PSA Census 2020 municipality rows and QNMP eight-municipality enumeration, reconcile spellings by parent/type, then build the deterministic importer and review fixtures.
