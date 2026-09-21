# Next Country Decision

## Policy baseline

As of 2026-08-17 the project operates under **Maximum Arabic Knowledge Coverage** (`00_فلسفة_الموسوعة.md`, Schema 2.1.0). All 22 bounded first-layer country cycles remain accepted; the project is now in **depth-expansion mode**: proving places exist down to villages, neighborhoods, and lanes, then collecting the maximum useful local information (history, dialect, food, dress, crafts, markets, stories) with explicit confidence statuses instead of deletion.

Depth expansion is additive: it never rewrites an accepted layer, and `published` stays restricted to `verified`/`source_verified`.

## Completed depth cycles

| Country | Cycle(s) | Entered | Status |
| --- | --- | --- | --- |
| Tunisia | 1 | 3 languages (incl. لغة سند المنقرضة), 5 dialect profiles, 8 dishes, 4 dress | ✅ 2026-08-17 |
| Yemen | 1–4 | 333/333 districts `probable`; 104/791 Amanat lanes; 12 dishes, 5 dialects, 2 languages, 7 dress, 4 crafts, 3 markets | ✅ 2026-08-17 |
| Jordan | 1 | language/dialect/food/dress depth claims anchored to accepted layers | ✅ |
| Libya | 1 | 5 language presences, dialect/dish/dress depth; mahallas unavailable | ✅ |
| Morocco | 1 | depth claims with regional vocabulary | ✅ |
| Oman | 1 | depth claims with wilaya anchoring | ✅ |
| Algeria | 1 | depth claims with Tamazight layer | ✅ |
| Lebanon | 1 | depth claims with Levantine shared partition | ✅ |
| Sudan | 1 | depth claims with Nilotic/African language layer | ✅ |
| Syria | 1 | depth claims incl. historic quarters | ✅ |
| Palestine | 1 | depth claims anchored to governorates | ✅ |
| Saudi Arabia | 1 | depth claims; published Najdi/Hijazi spine | ✅ |
| Egypt | 1 | depth claims anchored to governorates | ✅ |
| Iraq | 1 | depth claims anchored to governorates | ✅ |
| Kuwait | 1 | 7 published UNESCO ICH elements + 38 unpublished classified claims + 4 quarters/12 فرجان/1 سكة (no denominator) | ✅ 2026-09-20 |
| Bahrain | 1 | 5 published UNESCO ICH elements (الفجري national) + 38 unpublished classified claims + مدينة المحرق/14 فريجًا/6 قرى/3 حالات (no denominator) | ✅ 2026-09-20 |
| Qatar | 1 | 7 published UNESCO ICH elements — all shared, no exclusive element — + 33 unpublished classified claims + 3 فرجان/سوق واقف (no denominator) | ✅ 2026-09-20 |
| **Comoros** | **1** | **1 published UNESCO ICH element (زفّة العرس 02283، ملف بسبع دول) + 3 أحكام دستورية + معالم الموقع (30.47 هكتار) + 30 دعوى مصنّفة + 6 مدن تاريخية (no denominator)** | ✅ **2026-09-20** |

## Current country

**Djibouti (DJ) — depth-expansion cycle 1.**

## Rationale (dependency / risk / available information)

- Comoros is closed, and its published element is a **seven-State file that includes Djibouti**: the zaffa 02283 claim can be published for Djibouti under the same shared contract without any new exclusivity claim.
- Djibouti's accepted layer is bounded and machine-verified: 5 regions, the special city of Djibouti with 3 communes, and 13 sub-prefectures, reconciled against the 2024 census reference date (total 1,066,809 · city 776,966).
- Available inside the repository: `data/imports/djibouti/fixtures/topology_2024.json`, `source_catalog.json`, `research/`, `manifests/DJ.yml`, and the gate `scripts/check_djibouti_gate.py`.
- The Gulf/Indian-Ocean group without depth now has three members (Djibouti · Mauritania · Somalia) plus the UAE; Djibouti is first because its shared element is already in the published spine of a closed neighbour.

## Scope of the Djibouti depth cycle

1. **Verify first:** re-confirm the accepted region/city/commune/sub-prefecture topology from the checksum-bound fixture; no lower denominator is inferred from neighborhoods or quarters.
2. **Published spine:** the shared zaffa element for Djibouti (`shared`, never national), and any additional UNESCO element on which Djibouti appears, with the submitting-State list asserted exactly as published.
3. **Heritage places:** historic quarters of Djibouti-Ville and the old urban cores as places with `located_in` only — no administrative parent, no population claim, no percentage.
4. **Classified local knowledge:** Somali and Afar language presence (with no speaker counts), dialects, dishes (skoudehkaris، فطيرة…), dress, crafts (salt, fishing, incense) and customs — all classified, tier-capped and unpublished unless an authoritative list publishes them.
5. **Deliberate zeros are recorded as zeros:** where no source is accepted (for example a minority language or a heritage denominator), the layer stays open with no denominator instead of an invented figure.

## Queue after Djibouti

Mauritania → Somalia → UAE (completing the no-depth group), then a second-order depth cycle in the philosophy order: Yemen (remaining 8 Amanat districts + 687 lanes) → Saudi Arabia → Egypt → Morocco → Algeria → Iraq → Palestine → Oman → Sudan. Order may only change on documented dependency/risk grounds.

## Standing depth gaps carried forward

- Yemen: lane tables for the remaining 8 Amanat districts + 2 suburb blocks, field-dated lexical corpus, unverified-content backlog review.
- Cairo 21 shiakhas, Baghdad 66 mahallas, Damascus 16 lanes, Palestine ~45 sites (HTTP 403) — open frames, not forgotten.
- `data/backlog/unverified_content/` review is a depth-cycle obligation, not optional cleanup.

## Release status

The bounded first-layer release decision in `reports/FINAL_ARABIC_ENCYCLOPEDIA_RELEASE.md` (`COMPLETE WITH DOCUMENTED LIMITATIONS`) is unchanged; depth expansion is additive and never rewrites accepted layers.
