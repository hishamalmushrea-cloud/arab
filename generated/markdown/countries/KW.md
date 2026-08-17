# الكويت (KW) — عرض مولّد من Schema 2.0.0

> **حدود التغطية:** التغطية المحلية غير مكتملة. لا تمثل هذه الصفحة جميع المدن أو القرى أو الأحياء أو الحارات، ولا يُستدل على التغطية من وجود ملف. البيانات المنظمة هي المصدر؛ هذه الصفحة عرض مولّد.

## التغطية والمقامات

أي نسبة 100% أدناه مقيدة بالدولة والطبقة والمقام المؤرخ واللقطة والمصدر الظاهرة في الصف نفسه؛ ولا تمتد إلى طبقة أخرى.

| الطبقة | تعريف المقام | المقام | مطابق | غير مطابق | مستبعد | مفقود | النسبة | تاريخ اللقطة | اللقطة | المصدر | الترخيص | مكتمل | سبب النقص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| country_scope | ISO country entity in the project's 22-country scope | 1 | 1 | 0 | 0 | 0 | 100% | 2026-08-15 | SNP-MIGRATION-2026-08-15 | SRC-ISO-3166-1-2020 | ISO copyright; reuse is subject to ISO terms of use | نعم | — |
| kw_governorate | All six current governorates enumerated in the official 2021 registration-census table. | 6 | 6 | 0 | 0 | 0 | 100% | 2026-08-16 | SNP-KW-PRODUCTION-20260816 | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 | Kuwait government statistical publication; factual extraction with attribution; reuse terms not stated | نعم | — |
| world_heritage_property | All inscribed World Heritage properties for Kuwait: zero. Six tentative-list sites are outside this denominator. | 0 | 0 | 0 | 0 | 0 | 100% | 2026-08-16 | SNP-KW-PRODUCTION-20260816 | SRC-UNESCO-WHC-KW-2026 | CC BY-SA 3.0 IGO for property descriptions | نعم | — |

## الكيانات

| المعرّف | الاسم | النوع | الحالة | المصدر القانوني/المرجعي | المحدد داخل المصدر |
|---|---|---|---|---|---|
| ENT-KW-COUNTRY | الكويت | country | current | SRC-ISO-3166-1-2020 | ISO alpha-2 entry KW |
| ENT-KW-GOVERNORATE-AL-AHMADI | الأحمدي | kw_governorate | current | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 | 2021 census Table 1 row: الأحمدي / Al-Ahmadi; total=923784 |
| ENT-KW-GOVERNORATE-AL-FARWANIYA | الفروانية | kw_governorate | current | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 | 2021 census Table 1 row: الفروانية / Al-Farwaniya; total=1109819 |
| ENT-KW-GOVERNORATE-AL-JAHRA | الجهراء | kw_governorate | current | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 | 2021 census Table 1 row: الجهراء / Al-Jahra; total=566861 |
| ENT-KW-GOVERNORATE-CAPITAL | العاصمة | kw_governorate | current | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 | 2021 census Table 1 row: العاصمة / Capital; total=574839 |
| ENT-KW-GOVERNORATE-HAWALLI | حولي | kw_governorate | current | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 | 2021 census Table 1 row: حولي / Hawalli; total=926170 |
| ENT-KW-GOVERNORATE-MUBARAK-AL-KABEER | مبارك الكبير | kw_governorate | current | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 | 2021 census Table 1 row: مبارك الكبير / Mubarak Al-Kabeer; total=279666 |

## الأسماء البديلة

| المعرّف | الكيان | الاسم | اللغة | النوع | المصدر |
|---|---|---|---|---|---|
| ALS-KW-61E9AF0EA2985661 | ENT-KW-GOVERNORATE-CAPITAL | Capital | en | official_variant | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 |
| ALS-KW-B44EE9DB5D2A500F | ENT-KW-GOVERNORATE-AL-FARWANIYA | Al-Farwaniya | en | official_variant | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 |
| ALS-KW-D30D6C7467DB5549 | ENT-KW-GOVERNORATE-AL-AHMADI | Al-Ahmadi | en | official_variant | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 |
| ALS-KW-E85279B2E4B25E08 | ENT-KW-GOVERNORATE-MUBARAK-AL-KABEER | Mubarak Al-Kabeer | en | official_variant | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 |
| ALS-KW-F06C4C902907556B | ENT-KW-GOVERNORATE-AL-JAHRA | Al-Jahra | en | official_variant | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 |
| ALS-KW-F977092B11F8594B | ENT-KW-GOVERNORATE-HAWALLI | Hawalli | en | official_variant | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 |

## علاقات الإدارة/الموقع

| المعرّف | الابن | الأب | العلاقة | الحالة | المصدر |
|---|---|---|---|---|---|
| REL-KW-34B31553E7585BEB | ENT-KW-GOVERNORATE-AL-FARWANIYA | ENT-KW-COUNTRY | administrative_parent | current | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 |
| REL-KW-38324C62A8C9503E | ENT-KW-GOVERNORATE-AL-AHMADI | ENT-KW-COUNTRY | administrative_parent | current | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 |
| REL-KW-7DD4F721AED65D74 | ENT-KW-GOVERNORATE-MUBARAK-AL-KABEER | ENT-KW-COUNTRY | administrative_parent | current | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 |
| REL-KW-85A2A5D262EE51A5 | ENT-KW-GOVERNORATE-CAPITAL | ENT-KW-COUNTRY | administrative_parent | current | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 |
| REL-KW-D5A1B0CD06525DCA | ENT-KW-GOVERNORATE-HAWALLI | ENT-KW-COUNTRY | administrative_parent | current | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 |
| REL-KW-EA735DA3C1B85DBC | ENT-KW-GOVERNORATE-AL-JAHRA | ENT-KW-COUNTRY | administrative_parent | current | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 |

## الادعاءات

| المعرّف | الموضوع | المحمول | القيمة | التصنيف | الثقة | الحالة | المصدر | المحدد |
|---|---|---|---|---|---|---|---|---|
| CLM-KW-0101789BB4D55DDD | ENT-KW-GOVERNORATE-AL-JAHRA | population | 566861 | official | high | verified | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 | 2021 census Table 1 row: الجهراء / Al-Jahra; total=566861 |
| CLM-KW-206F0FEA5A3F555B | ENT-KW-GOVERNORATE-MUBARAK-AL-KABEER | population | 279666 | official | high | verified | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 | 2021 census Table 1 row: مبارك الكبير / Mubarak Al-Kabeer; total=279666 |
| CLM-KW-49BA618406F55A03 | ENT-KW-GOVERNORATE-HAWALLI | population | 926170 | official | high | verified | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 | 2021 census Table 1 row: حولي / Hawalli; total=926170 |
| CLM-KW-B96FAA39512251D6 | ENT-KW-GOVERNORATE-AL-AHMADI | population | 923784 | official | high | verified | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 | 2021 census Table 1 row: الأحمدي / Al-Ahmadi; total=923784 |
| CLM-KW-D5399D0A15C751C0 | ENT-KW-GOVERNORATE-CAPITAL | population | 574839 | official | high | verified | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 | 2021 census Table 1 row: العاصمة / Capital; total=574839 |
| CLM-KW-E8FD297081805484 | ENT-KW-GOVERNORATE-AL-FARWANIYA | population | 1109819 | official | high | verified | SRC-KW-CSB-CENSUS-GOVERNORATES-2021 | 2021 census Table 1 row: الفروانية / Al-Farwaniya; total=1109819 |

## جودة مصادر الادعاءات المنشورة

ادعاءات A/B: 6 من 6 (100.00%).

## المصادر الذرية المستخدمة

| المعرّف | الفئة | العنوان | الناشر | تاريخ النشر | تاريخ الاسترجاع | الترخيص | الرابط |
|---|---|---|---|---|---|---|---|
| SRC-ISO-3166-1-2020 | A | ISO 3166-1:2020 — Codes for the representation of names of countries and their subdivisions — Part 1: Country code | International Organization for Standardization (ISO) | 2020-08 | 2026-08-15 | ISO copyright; reuse is subject to ISO terms of use | https://www.iso.org/obp/ui/#iso:std:iso:3166:-1:ed-4:v1:en |
| SRC-KW-CSB-CENSUS-GOVERNORATES-2021 | A | Kuwait Registration Census 2021 — population by governorate | Central Statistical Bureau | — | 2026-08-16 | Kuwait government statistical publication; factual extraction with attribution; reuse terms not stated | https://census.csb.gov.kw/Census_Gov |
| SRC-UNESCO-WHC-KW-2026 | A | World Heritage List — Kuwait State Party | UNESCO World Heritage Centre | — | 2026-08-16 | CC BY-SA 3.0 IGO for property descriptions | https://whc.unesco.org/en/statesparties/kw |

---
_مولّد آليًا؛ لا تعدّل هذا الملف مباشرة._
