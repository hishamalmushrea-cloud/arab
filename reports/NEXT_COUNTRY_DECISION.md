# Next Country Decision

## Policy baseline

As of 2026-09-23 the project operates under **Maximum Arabic Knowledge Coverage** (`00_فلسفة_الموسوعة.md`, Schema 2.1.0). All 22 bounded first-layer country cycles remain accepted; the project is in **depth-expansion mode**: proving places exist down to villages, neighborhoods, and lanes, then collecting the maximum useful local information (history, dialect, food, dress, crafts, markets, stories) with explicit confidence statuses instead of deletion.

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
| Djibouti | 1 | 3 published UNESCO ICH elements (الخيدو 02001 USL وطني وحيد الدولة · الزير عيسى 02087 بثلاث دول · الزفّة 02283 بسبع دول) + الدستور + التصديق وترشيح 2026 + 30 دعوى مصنّفة + 12 مكانًا داخل العاصمة (no denominator) | ✅ 2026-09-21 |
| Mauritania | 1 | 9 published UNESCO ICH elements (تْحِيدِن 00524 USL وطني وحيد الدولة · المحضرة 01960 وطني · سامبا غيلاديو 01692 وطني · ستة ملفات مشتركة) + موقعا التراث العالمي (القصور 750 ثقافي · بانك دارغان 506 طبيعي) + القائمة المؤقتة 2001 + 5 مواد دستورية + 29 دعوى مصنّفة + 7 أماكن بلا مقام (no denominator) | ✅ 2026-09-21 |
| Somalia | 1 | عنصران يونسكويان مدرجان وكلاهما ملف مشترك (لا عنصر وطني): الزير عيسى 02087 (إثيوبيا · جيبوتي · الصومال) والزفّة 02283 (سبع دول) + صفر مواقع تراث عالمي مُدرجة وثلاثة ملفات قائمة مؤقتة 6752/6753/6754 + سبع مواد دستورية (والمادة 9 لا تسمّي عاصمة) + 35 دعوى مصنّفة + 4 أماكن بلا مقام (no denominator) | ✅ 2026-09-23 |
| **United Arab Emirates** | **1** | **7 ملفات يونسكوية مصنَّفة: عنصر وطني وحيد الدولة هو العزي 01268 على قائمة الصون العاجل، وستة ملفات مشتركة (00744 · 01012 · 01718 · 01902 · 02116 · 02283)؛ و13 ملفًا مؤجَّلًا لقائمة الدول المقدِّمة بلا وسم نطاق؛ وسجل المادة 18 للبرنامج 02473؛ و4 ترشيحات معلنة لسنة 2026؛ و3 مواقع تراث عالمي مُدرجة (1343 · 1735 · 1724) و15 ملفًا مؤقتًا وصفر مساعدات منشور؛ و3 صفوف لغوية مؤجَّلة ولهجة `afb`؛ و12 طبقًا و3 حرف و3 أعراف وروايتان؛ و3 أماكن `located_in` فقط؛ مع إبقاء السجلات الثلاثة غير المتاحة بلا نسبة** | ✅ **2026-09-23** |

## Current country

**Yemen (YE) — depth cycle 2** (the first country of the second-degree depth order in `00_فلسفة_الموسوعة.md` §12).

## Rationale (dependency / risk / available information)

- The UAE depth cycle closed the last Gulf gap without a single fabricated scope label: thirteen inscribed files are carried with reference, year and list only, because their submitting-State lists were not read. That is the honest state of the record, and the negative suite now fails the build if any of them is labelled national or shared.
- The UAE also proved a *dated-snapshot split* pattern: the accepted pilot snapshot (2026-08-15) keeps its own checksum while the depth cycle gets its own snapshot (2026-09-23), so a later reading never silently re-dates an earlier accepted layer.
- Yemen is the first country of the second-degree list, and it carries the largest *unfinished enumerable* frame in the repository: 8 Amanat al-Asimah districts still lack lane tables out of 791 lanes, and the Amanat district frame itself is the smallest gap left that can be closed with a real dated registry rather than a mirror.
- Yemen already has the second-largest accepted depth body (32 depth claims plus 61 `LANEPOP`/`DISH`/`DIALECT`/`DRESS`/`CRAFT` records), so cycle 2 extends an existing spine instead of starting a new one — and the remaining lane work is *enumeration*, the highest-value gap per §10 (useful information before organization).

## Scope of the Yemen depth cycle 2 (opened 2026-09-23)

1. **Finish the lane frame:** add the remaining 8 Amanat al-Asimah district lane tables toward the 791-lane registry, with the registry as denominator and no extrapolation from the 104 already recorded.
2. **Verify before extending:** re-confirm the 333 `probable` districts against the accepted frame; promote to `verified` only with a dated official enumeration.
3. **Second-degree cultural bodies** for governorates not yet covered, in the same classified-and-unpublished pattern: dialect profiles with dated lexical context, dishes, dress, crafts and markets.
4. **Historical places** enter `located_in`-only with no denominator, no population and no coordinates unless the source supplies them.
5. **Deliberate absences:** no speaker counts, no population, no share, no unread field filled from a mirror, and every deliberate zero published as zero.

## Queue after the current country

اليمن (دورة عمق 2) → السعودية → مصر → المغرب → الجزائر → العراق → فلسطين → عُمان → السودان. لا يتغيّر الترتيب إلا بسبب موثَّق متعلق بالاعتماد أو الخطر.

## Standing depth gaps carried forward

- UAE cycle 2 (documented, not forgotten): the thirteen deferred element files' submitting-State lists, the three property pages' criteria and emirates, a working constitutional text, and a dated enumerable registry before any settlement or neighborhood layer.
- Cairo 21 shiakhas, Baghdad 66 mahallas, Damascus 16 lanes, Palestine ~45 sites (HTTP 403) — open frames, not forgotten.
- `data/backlog/unverified_content/` review is a depth-cycle obligation, not optional cleanup.

## Release status

The bounded first-layer release decision in `reports/FINAL_ARABIC_ENCYCLOPEDIA_RELEASE.md` (`COMPLETE WITH DOCUMENTED LIMITATIONS`) is unchanged; depth expansion is additive and never rewrites accepted layers. The UAE depth cycle is released by `reports/UAE_DEPTH_CLOSEOUT.md` and guarded by `make uae`.
