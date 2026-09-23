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
| Comoros | 1 | 1 published UNESCO ICH element (زفّة العرس 02283، ملف بسبع دول) + 3 أحكام دستورية + معالم الموقع (30.47 هكتار) + 30 دعوى مصنّفة + 6 مدن تاريخية (no denominator) | ✅ 2026-09-20 |
| Djibouti | 1 | 3 published UNESCO ICH elements (الخيدو 02001 USL وطني وحيد الدولة · الزير عيسى 02087 بثلاث دول · الزفّة 02283 بسبع دول) + الدستور (اللغات الرسمية والدين والعاصمة) + التصديق وترشيح 2026 + 30 دعوى مصنّفة + 12 مكانًا داخل العاصمة (no denominator) | ✅ 2026-09-21 |
| **Mauritania** | **1** | **9 published UNESCO ICH elements (تْحِيدِن 00524 USL وطني وحيد الدولة · المحضرة 01960 وطني · سامبا غيلاديو 01692 وطني · ستة ملفات مشتركة) + موقعا التراث العالمي (القصور 750 ثقافي · بانك دارغان 506 طبيعي) + القائمة المؤقتة 2001 + 5 مواد دستورية + 29 دعوى مصنّفة + 7 أماكن بلا مقام (no denominator)** | ✅ **2026-09-21** |

## Current country

**Somalia (SO) — depth-expansion cycle 1.**

## Rationale (dependency / risk / available information)

- Mauritania is closed with three sole-submission elements (one of them on the Urgent Safeguarding List) and six shared files, so both sides of the ICH contract — exclusive and shared — are proven before Somalia.
- Somalia is the last country of the Gulf/Indian-Ocean group without depth after Djibouti, and it already appears as a co-submitting State in the zaffa 02283 file, so the shared-element contract transfers without a new exclusivity claim.
- Somalia's accepted layer is bounded (its own fixtures, manifest and gate `scripts/check_somalia_gate.py`), so the cycle verifies the accepted denominators first and then builds the classified body (Somali and Maay, dialects, poetry, dishes, dress, crafts, customs) with no speaker counts and no inherited denominators.
- Risk to record rather than resolve: where a State page cannot be read for a list (as the natural property's criteria could not be read for Mauritania), the field stays explicitly empty instead of being filled from a mirror.

## Scope of the Mauritania depth cycle (completed 2026-09-21)

1. **Verify first:** re-confirm the 15 wilayas (three Nouakchott + twelve regional) from the checksum-bound fixture; keep the 63 moughataas known/open and the commune conflict (219/220) disputed with no denominator.
2. **Published spine:** nine inscribed UNESCO elements with the submitting-State list asserted exactly as published, the 2006-11-15 ratification, the three declared 2026 nominations as pending nominations, the two World Heritage properties, the 2001 tentative list and the constitutional articles.
3. **Heritage places:** the four ksour cities and three archaeological sites as places with `located_in` only — no administrative parent, no population claim, no percentage, no coordinates.
4. **Classified local knowledge:** Hassaniya and its dialect profile, the script profile, dishes, dress, crafts and customs — all classified, tier-capped and unpublished unless an authoritative list publishes them.
5. **Deliberate zeros are recorded as zeros:** the natural property's criteria are recorded empty because they were not read, and every unpublished language row states the no-count rule in the record itself.

## Queue after the current country

Somalia → UAE (completing the no-depth group), then a second-order depth cycle in the philosophy order: Yemen (remaining 8 Amanat districts + 687 lanes) → Saudi Arabia → Egypt → Morocco → Algeria → Iraq → Palestine → Oman → Sudan. Order may only change on documented dependency/risk grounds.

## Standing depth gaps carried forward

- Yemen: lane tables for the remaining 8 Amanat districts + 2 suburb blocks, field-dated lexical corpus, unverified-content backlog review.
- Cairo 21 shiakhas, Baghdad 66 mahallas, Damascus 16 lanes, Palestine ~45 sites (HTTP 403) — open frames, not forgotten.
- `data/backlog/unverified_content/` review is a depth-cycle obligation, not optional cleanup.

## Release status

The bounded first-layer release decision in `reports/FINAL_ARABIC_ENCYCLOPEDIA_RELEASE.md` (`COMPLETE WITH DOCUMENTED LIMITATIONS`) is unchanged; depth expansion is additive and never rewrites accepted layers.
