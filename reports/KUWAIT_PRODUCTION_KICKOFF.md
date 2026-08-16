# Kuwait Production Expansion — Kickoff

## Status

**STARTED — evidence assessment only; no Kuwait production Entity/Claim/Source/Denominator has been added yet.**

## Mode

Direct Structured Expansion, with the governorate layer first. This is not a copy of Bahrain: Kuwait's principal risk is conflating governorates with address/statistical areas and numbered blocks.

## Initial authority map

1. Kuwait Government Online: administrative-governorate page enumerates Al Asimah, Hawalli, Al Farwaniyah, Mubarak Al-Kabeer, Al Ahmadi, and Al Jahra.
2. Central Statistical Bureau census portal: bilingual population table independently enumerates the same six governorates.
3. Public Authority for Civil Information: expected authority for civil/address units; no area/block denominator is accepted yet.
4. UNESCO State Party record: zero inscribed World Heritage properties and six tentative-list sites at the 2026-08-16 review snapshot; tentative sites must not be represented as inscribed properties.

## Evidence finding

The CSB census page contains an internal presentation inconsistency: prominent values near the top differ from the chart/table totals on the same page, while the downloadable table and chart agree with each other. Therefore no population Claim will be imported until the downloadable workbook, census reference date, and total are checksum-bound and reconciled. This does not prevent using the six-name enumeration as a cross-check for the governorate denominator.

Kuwait Government Online returned HTTP 403 to the automated page retriever although indexed official content exposes the six-name list. It remains a lead/cross-check, not the sole persisted production source.

## Planned first closure

- Six current `kw_governorate` entities only after an atomic official current-list source and date are persisted.
- Six country-parent relationships and bilingual Aliases.
- Denominator/coverage for exactly six governorates.
- No `kw_area` or `kw_block` records without a separate dated denominator and topology.
- Population Claims only after the CSB inconsistency is resolved from the downloadable official workbook.
- UNESCO tentative-list sites excluded from any inscribed-property denominator.

## Required mutations

Wrong governorate parent; area-as-governorate; block-as-municipality; foreign source; population mismatch; undated census Claim; tentative-as-inscribed; cultural leakage; Alias-as-Entity.

## Next action

Persist and checksum the CSB workbook or an equivalent dated official table, establish the exact census reference date, and locate a retrievable primary six-governorate administrative source. Then build the deterministic importer and independent review.
