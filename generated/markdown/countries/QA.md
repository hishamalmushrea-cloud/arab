# قطر (QA) — عرض مولّد من Schema 2.0.0

> **حدود التغطية:** التغطية المحلية غير مكتملة. لا تمثل هذه الصفحة جميع المدن أو القرى أو الأحياء أو الحارات، ولا يُستدل على التغطية من وجود ملف. البيانات المنظمة هي المصدر؛ هذه الصفحة عرض مولّد.

## التغطية والمقامات

أي نسبة 100% أدناه مقيدة بالدولة والطبقة والمقام المؤرخ واللقطة والمصدر الظاهرة في الصف نفسه؛ ولا تمتد إلى طبقة أخرى.

| الطبقة | تعريف المقام | المقام | مطابق | غير مطابق | مستبعد | مفقود | النسبة | تاريخ اللقطة | اللقطة | المصدر | الترخيص | مكتمل | سبب النقص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| country_scope | ISO country entity in the project's 22-country scope | 1 | 1 | 0 | 0 | 0 | 100% | 2026-08-15 | SNP-MIGRATION-2026-08-15 | SRC-ISO-3166-1-2020 | ISO copyright; reuse is subject to ISO terms of use | نعم | — |
| qa_municipality | All eight Census 2020 municipalities, independently cross-checked by QNMP. | 8 | 8 | 0 | 0 | 0 | 100% | 2026-08-16 | SNP-QA-PRODUCTION-20260816 | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | Qatar government statistical publication; factual extraction with attribution; reuse terms not stated | نعم | — |
| world_heritage_property | Al Zubarah, property 1402. | 1 | 1 | 0 | 0 | 0 | 100% | 2026-08-16 | SNP-QA-PRODUCTION-20260816 | SRC-UNESCO-WHC-QA-1402 | CC BY-SA 3.0 IGO for property descriptions | نعم | — |

## الكيانات

| المعرّف | الاسم | النوع | الحالة | المصدر القانوني/المرجعي | المحدد داخل المصدر |
|---|---|---|---|---|---|
| ENT-QA-ARCHAEOLOGICAL-SITE-AL-ZUBARAH | Al Zubarah Archaeological Site | archaeological_site | current | SRC-UNESCO-WHC-QA-1402 | UNESCO property 1402; cultural; inscribed 2013 |
| ENT-QA-COUNTRY | قطر | country | current | SRC-ISO-3166-1-2020 | ISO alpha-2 entry QA |
| ENT-QA-MUNICIPALITY-AL-DAAYEN | الظعاين | qa_municipality | current | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | Census 2020 municipality row: الظعاين / Al Daayen; population=100083 |
| ENT-QA-MUNICIPALITY-AL-KHOR-AL-THAKHIRA | الخور والذخيرة | qa_municipality | current | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | Census 2020 municipality row: الخور والذخيرة / Al Khor and Al Thakhira; population=140453 |
| ENT-QA-MUNICIPALITY-AL-RAYYAN | الريان | qa_municipality | current | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | Census 2020 municipality row: الريان / Al Rayyan; population=826786 |
| ENT-QA-MUNICIPALITY-AL-SHAMAL | الشمال | qa_municipality | current | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | Census 2020 municipality row: الشمال / Al Shamal; population=16730 |
| ENT-QA-MUNICIPALITY-AL-SHEEHANIYA | الشحانية | qa_municipality | current | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | Census 2020 municipality row: الشحانية / Al Sheehaniya; population=161240 |
| ENT-QA-MUNICIPALITY-AL-WAKRA | الوكرة | qa_municipality | current | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | Census 2020 municipality row: الوكرة / Al Wakra; population=265102 |
| ENT-QA-MUNICIPALITY-DOHA | الدوحة | qa_municipality | current | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | Census 2020 municipality row: الدوحة / Doha; population=1186023 |
| ENT-QA-MUNICIPALITY-UMM-SLAL | أم صلال | qa_municipality | current | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | Census 2020 municipality row: أم صلال / Umm Slal; population=149701 |

## الأسماء البديلة

| المعرّف | الكيان | الاسم | اللغة | النوع | المصدر |
|---|---|---|---|---|---|
| ALS-QA-0BCFAC6C85485D69 | ENT-QA-MUNICIPALITY-AL-KHOR-AL-THAKHIRA | Al Khor and Al Thakhira | en | official_variant | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 |
| ALS-QA-609500C5A25A5CF7 | ENT-QA-MUNICIPALITY-AL-SHEEHANIYA | Al Sheehaniya | en | official_variant | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 |
| ALS-QA-6E4564185B3458E2 | ENT-QA-MUNICIPALITY-AL-RAYYAN | Al Rayyan | en | official_variant | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 |
| ALS-QA-7B38B842018851AC | ENT-QA-MUNICIPALITY-AL-WAKRA | Al Wakra | en | official_variant | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 |
| ALS-QA-91B0E0DFB33756D4 | ENT-QA-ARCHAEOLOGICAL-SITE-AL-ZUBARAH | موقع الزبارة الأثري | ar | official_variant | SRC-UNESCO-WHC-QA-1402 |
| ALS-QA-BD0BEF8FFA355FAF | ENT-QA-MUNICIPALITY-DOHA | Doha | en | official_variant | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 |
| ALS-QA-C15CE83FBA1F5619 | ENT-QA-MUNICIPALITY-AL-SHAMAL | Al Shamal | en | official_variant | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 |
| ALS-QA-D329AE79623D5BA9 | ENT-QA-MUNICIPALITY-AL-DAAYEN | Al Daayen | en | official_variant | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 |
| ALS-QA-D979F12CA5775A44 | ENT-QA-MUNICIPALITY-UMM-SLAL | Umm Slal | en | official_variant | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 |

## علاقات الإدارة/الموقع

| المعرّف | الابن | الأب | العلاقة | الحالة | المصدر |
|---|---|---|---|---|---|
| REL-QA-1E65D833B5CA5329 | ENT-QA-MUNICIPALITY-AL-RAYYAN | ENT-QA-COUNTRY | administrative_parent | current | SRC-QA-QNMP-EIGHT-MUNICIPALITIES-2026 |
| REL-QA-2203A0E5AA0C5136 | ENT-QA-MUNICIPALITY-AL-WAKRA | ENT-QA-COUNTRY | administrative_parent | current | SRC-QA-QNMP-EIGHT-MUNICIPALITIES-2026 |
| REL-QA-34AD9CF1E67C55F4 | ENT-QA-MUNICIPALITY-AL-KHOR-AL-THAKHIRA | ENT-QA-COUNTRY | administrative_parent | current | SRC-QA-QNMP-EIGHT-MUNICIPALITIES-2026 |
| REL-QA-355D651ED7A1571C | ENT-QA-ARCHAEOLOGICAL-SITE-AL-ZUBARAH | ENT-QA-COUNTRY | associated_with | current | SRC-UNESCO-WHC-QA-1402 |
| REL-QA-4E9940AFDA32595C | ENT-QA-MUNICIPALITY-AL-SHAMAL | ENT-QA-COUNTRY | administrative_parent | current | SRC-QA-QNMP-EIGHT-MUNICIPALITIES-2026 |
| REL-QA-A1D99487D6FD59CD | ENT-QA-MUNICIPALITY-DOHA | ENT-QA-COUNTRY | administrative_parent | current | SRC-QA-QNMP-EIGHT-MUNICIPALITIES-2026 |
| REL-QA-A5B7D5A651255B5B | ENT-QA-MUNICIPALITY-UMM-SLAL | ENT-QA-COUNTRY | administrative_parent | current | SRC-QA-QNMP-EIGHT-MUNICIPALITIES-2026 |
| REL-QA-B399353A78D25E12 | ENT-QA-MUNICIPALITY-AL-SHEEHANIYA | ENT-QA-COUNTRY | administrative_parent | current | SRC-QA-QNMP-EIGHT-MUNICIPALITIES-2026 |
| REL-QA-E656E6E35BFF574C | ENT-QA-MUNICIPALITY-AL-DAAYEN | ENT-QA-COUNTRY | administrative_parent | current | SRC-QA-QNMP-EIGHT-MUNICIPALITIES-2026 |

## الادعاءات

| المعرّف | الموضوع | المحمول | القيمة | التصنيف | الثقة | الحالة | المصدر | المحدد |
|---|---|---|---|---|---|---|---|---|
| CLM-QA-1959ECEEA7BE5FC0 | ENT-QA-MUNICIPALITY-AL-SHEEHANIYA | population | 161240 | official | high | verified | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | Census 2020 municipality row: الشحانية / Al Sheehaniya; population=161240 |
| CLM-QA-74B9B7CB2FB559ED | ENT-QA-MUNICIPALITY-AL-SHAMAL | population | 16730 | official | high | verified | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | Census 2020 municipality row: الشمال / Al Shamal; population=16730 |
| CLM-QA-833689E2EA475E1A | ENT-QA-MUNICIPALITY-AL-DAAYEN | population | 100083 | official | high | verified | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | Census 2020 municipality row: الظعاين / Al Daayen; population=100083 |
| CLM-QA-9CE84D3291315A3D | ENT-QA-MUNICIPALITY-AL-RAYYAN | population | 826786 | official | high | verified | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | Census 2020 municipality row: الريان / Al Rayyan; population=826786 |
| CLM-QA-ADA92432E7E05580 | ENT-QA-MUNICIPALITY-UMM-SLAL | population | 149701 | official | high | verified | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | Census 2020 municipality row: أم صلال / Umm Slal; population=149701 |
| CLM-QA-AE2B5A396BA2599A | ENT-QA-MUNICIPALITY-AL-KHOR-AL-THAKHIRA | population | 140453 | official | high | verified | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | Census 2020 municipality row: الخور والذخيرة / Al Khor and Al Thakhira; population=140453 |
| CLM-QA-BF2FCF9C09B35146 | ENT-QA-ARCHAEOLOGICAL-SITE-AL-ZUBARAH | world_heritage_category | cultural | official | high | verified | SRC-UNESCO-WHC-QA-1402 | UNESCO property 1402; cultural; inscribed 2013 |
| CLM-QA-C438257FCC6155BF | ENT-QA-MUNICIPALITY-DOHA | population | 1186023 | official | high | verified | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | Census 2020 municipality row: الدوحة / Doha; population=1186023 |
| CLM-QA-CBE42CBC252E5A05 | ENT-QA-ARCHAEOLOGICAL-SITE-AL-ZUBARAH | world_heritage_inscription_year | 2013 | official | high | verified | SRC-UNESCO-WHC-QA-1402 | UNESCO property 1402; cultural; inscribed 2013 |
| CLM-QA-DFCE11B7B84355D0 | ENT-QA-MUNICIPALITY-AL-WAKRA | population | 265102 | official | high | verified | SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | Census 2020 municipality row: الوكرة / Al Wakra; population=265102 |

## جودة مصادر الادعاءات المنشورة

ادعاءات A/B: 10 من 10 (100.00%).

## المصادر الذرية المستخدمة

| المعرّف | الفئة | العنوان | الناشر | تاريخ النشر | تاريخ الاسترجاع | الترخيص | الرابط |
|---|---|---|---|---|---|---|---|
| SRC-ISO-3166-1-2020 | A | ISO 3166-1:2020 — Codes for the representation of names of countries and their subdivisions — Part 1: Country code | International Organization for Standardization (ISO) | 2020-08 | 2026-08-15 | ISO copyright; reuse is subject to ISO terms of use | https://www.iso.org/obp/ui/#iso:std:iso:3166:-1:ed-4:v1:en |
| SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020 | A | Qatar Census 2020 — Population by Municipality | Planning and Statistics Authority | — | 2026-08-16 | Qatar government statistical publication; factual extraction with attribution; reuse terms not stated | https://www.psa.gov.qa/en/statistics1/StatisticsSite/Census/census2020/results/Pages/default.aspx |
| SRC-QA-QNMP-EIGHT-MUNICIPALITIES-2026 | A | Municipality Spatial Development Plans — eight municipalities | Qatar National Master Plan / Ministry of Municipality | — | 2026-08-16 | Qatar government statistical publication; factual extraction with attribution; reuse terms not stated | https://www.mme.gov.qa/QatarMasterPlan/English/MSDP-Municipalities.aspx?panel=about |
| SRC-UNESCO-WHC-QA-1402 | A | Al Zubarah Archaeological Site | UNESCO World Heritage Centre | — | 2026-08-16 | CC BY-SA 3.0 IGO for property descriptions | https://whc.unesco.org/en/list/1402 |

---
_مولّد آليًا؛ لا تعدّل هذا الملف مباشرة._
