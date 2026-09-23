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
| **Somalia** | **1** | **عنصران يونسكويان مدرجان وكلاهما ملف مشترك (لا عنصر وطني): الزير عيسى 02087 (إثيوبيا · جيبوتي · الصومال) والزفّة 02283 (سبع دول) + صفر مواقع تراث عالمي مُدرجة وثلاثة ملفات قائمة مؤقتة 6752/6753/6754 + سبع مواد دستورية (والمادة 9 لا تسمّي عاصمة) + 35 دعوى مصنّفة + 4 أماكن بلا مقام (no denominator)** | ✅ **2026-09-23** |

## Current country

**United Arab Emirates (AE) — depth-expansion cycle 1.**

## Rationale (dependency / risk / available information)

- Somalia is closed with both of its inscribed elements shared and none exclusive, so the *shared-only* case is now proven end to end alongside the exclusive case (Djibouti's Xeedho, Mauritania's three sole submissions).
- The UAE is the last country of the Gulf/Indian-Ocean group without a cultural depth cycle: it already appears as a co-submitting State on common files (الزفّة 02283، الحناء، الخط العربي، النخلة، البشت) and its accepted layer is bounded by its own fixture, manifest, denominators and scripts.
- The accepted UAE layer is unusually honest about what it does **not** know: nine closed denominators (seven emirates, Abu Dhabi 3، Dubai 9 قطاعات، Sharjah 9، Ajman 3، أم القيوين 2، رأس الخيمة 5، الفجيرة 2) and **three explicitly unavailable ones** (مجتمعات دبي، الأماكن المأهولة، الأحياء) — so the cycle verifies these first and refuses to fill the unavailable three by inference.
- Risk to record rather than resolve: where a State page cannot be read for a list, the field stays explicitly empty instead of being filled from a mirror (as with Mauritania's natural-property criteria and Somalia's garbled coordinate string).

## Scope of the UAE depth cycle (opened 2026-09-23)

1. **Verify first:** re-confirm the seven emirates and the nine closed denominators from the checksum-bound fixture, and keep `DEN-AE-DUBAI-PLANNING-COMMUNITIES`، `DEN-AE-POPULATED-PLACES`، `DEN-AE-NEIGHBORHOODS` **unavailable** with no percentage and no inferred entity.
2. **Published spine:** the UNESCO ICH elements on which the UAE appears — including the shared files الزفّة 02283، الحناء 02116، الخط العربي 01718، النخلة 01902، النقش على المعادن 01951 والبشت — each asserted exactly as published and stayed `shared`، plus the World Heritage properties and tentative list as read from the World Heritage State page, the ratification dates, and the constitutional articles that speak to language, religion and the union.
3. **Heritage places:** sites and quarters that carry a real listing as places with `located_in` only — no administrative parent, no population claim, no percentage, no invented coordinates.
4. **Classified local knowledge:** العربية and الإنجليزية واللغات الأخرى as classified rows, an Emirati dialect profile, dishes, dress, crafts, customs and markets — all classified, tier-capped and unpublished unless an authoritative list publishes them.
5. **Deliberate absences:** no speaker counts, no population, no share, no unread field filled from a mirror, and a published **zero** recorded as zero where the source says zero.

## Queue after the current country

الإمارات → الدورات من الدرجة الثانية بترتيب الفلسفة §12: اليمن (المتبقي 8 مديريات أمانة العاصمة + 687 زقاقًا) → السعودية → مصر → المغرب → الجزائر → العراق → فلسطين → عُمان → السودان. لا يتغيّر الترتيب إلا بسبب موثَّق متعلق بالاعتماد أو الخطر.

## Standing depth gaps carried forward

- Yemen: lane tables for the remaining 8 Amanat districts + 2 suburb blocks, field-dated lexical corpus, unverified-content backlog review.
- Cairo 21 shiakhas, Baghdad 66 mahallas, Damascus 16 lanes, Palestine ~45 sites (HTTP 403) — open frames, not forgotten.
- `data/backlog/unverified_content/` review is a depth-cycle obligation, not optional cleanup.

## Release status

The bounded first-layer release decision in `reports/FINAL_ARABIC_ENCYCLOPEDIA_RELEASE.md` (`COMPLETE WITH DOCUMENTED LIMITATIONS`) is unchanged; depth expansion is additive and never rewrites accepted layers.
