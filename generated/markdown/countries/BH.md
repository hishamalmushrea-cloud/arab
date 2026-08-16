# البحرين (BH) — عرض مولّد من Schema 2.0.0

> **حدود التغطية:** التغطية المحلية غير مكتملة. لا تمثل هذه الصفحة جميع المدن أو القرى أو الأحياء أو الحارات، ولا يُستدل على التغطية من وجود ملف. البيانات المنظمة هي المصدر؛ هذه الصفحة عرض مولّد.

## التغطية والمقامات

أي نسبة 100% أدناه مقيدة بالدولة والطبقة والمقام المؤرخ واللقطة والمصدر الظاهرة في الصف نفسه؛ ولا تمتد إلى طبقة أخرى.

| الطبقة | تعريف المقام | المقام | مطابق | غير مطابق | مستبعد | مفقود | النسبة | تاريخ اللقطة | اللقطة | المصدر | الترخيص | مكتمل | سبب النقص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| country_scope | ISO country entity in the project's 22-country scope | 1 | 1 | 0 | 0 | 0 | 100% | 2026-08-15 | SNP-MIGRATION-2026-08-15 | SRC-ISO-3166-1-2020 | ISO copyright; reuse is subject to ISO terms of use | نعم | — |
| bh_governorate | All current governorates enumerated by the official 2024 area dataset; Central is absent after the documented 2014 redivision. | 4 | 4 | 0 | 0 | 0 | 100% | 2026-08-16 | SNP-BH-PRODUCTION-20260816 | SRC-BH-SLRB-GOVERNORATE-AREA-2024 | Bahrain Open Data Policy: republication and distribution permitted, subject to applicable laws | نعم | — |
| world_heritage_property | All inscribed World Heritage properties for Bahrain at the retrieval snapshot; six tentative-list sites are excluded by definition. | 3 | 3 | 0 | 0 | 0 | 100% | 2026-08-16 | SNP-BH-PRODUCTION-20260816 | SRC-UNESCO-WHC-BH-2026 | CC BY-SA 3.0 IGO for property descriptions | نعم | — |

## الكيانات

| المعرّف | الاسم | النوع | الحالة | المصدر القانوني/المرجعي | المحدد داخل المصدر |
|---|---|---|---|---|---|
| ENT-BH-ARCHAEOLOGICAL-SITE-DILMUN-BURIAL-MOUNDS | Dilmun Burial Mounds | archaeological_site | current | SRC-UNESCO-WHC-BH-1542 | World Heritage property 1542; Dilmun Burial Mounds; inscribed 2019; category Cultural |
| ENT-BH-ARCHAEOLOGICAL-SITE-QALAT-AL-BAHRAIN | Qal’at al-Bahrain – Ancient Harbour and Capital of Dilmun | archaeological_site | current | SRC-UNESCO-WHC-BH-1192 | World Heritage property 1192; Qal’at al-Bahrain – Ancient Harbour and Capital of Dilmun; inscribed 2005; category Cultural |
| ENT-BH-COUNTRY | البحرين | country | current | SRC-ISO-3166-1-2020 | ISO alpha-2 entry BH |
| ENT-BH-CULTURAL-SITE-PEARLING | Pearling, Testimony of an Island Economy | cultural_site | current | SRC-UNESCO-WHC-BH-1364 | World Heritage property 1364; Pearling, Testimony of an Island Economy; inscribed 2012; category Cultural |
| ENT-BH-GOVERNORATE-CAPITAL | العاصمة | bh_governorate | current | SRC-BH-SLRB-GOVERNORATE-AREA-2024 | 2024 API record N=76: العاصمة / Capital; area=79.23 km² |
| ENT-BH-GOVERNORATE-MUHARRAQ | المحرق | bh_governorate | current | SRC-BH-SLRB-GOVERNORATE-AREA-2024 | 2024 API record N=77: المحرق / Muharraq; area=74.1 km² |
| ENT-BH-GOVERNORATE-NORTHERN | الشمالية | bh_governorate | current | SRC-BH-SLRB-GOVERNORATE-AREA-2024 | 2024 API record N=78: الشمالية / Northern; area=145.69 km² |
| ENT-BH-GOVERNORATE-SOUTHERN | الجنوبية | bh_governorate | current | SRC-BH-SLRB-GOVERNORATE-AREA-2024 | 2024 API record N=79: الجنوبية / Southern; area=488.77 km² |

## الأسماء البديلة

| المعرّف | الكيان | الاسم | اللغة | النوع | المصدر |
|---|---|---|---|---|---|
| ALS-BH-27B502B38FC25880 | ENT-BH-ARCHAEOLOGICAL-SITE-QALAT-AL-BAHRAIN | قلعة البحرين- مرفأ قديم وعاصمة دلمون | ar | official_variant | SRC-UNESCO-WHC-BH-1192 |
| ALS-BH-366BE4D7C17D5FA9 | ENT-BH-CULTURAL-SITE-PEARLING | طريق اللؤلؤ: شاهد على اقتصاد جزيرة | ar | official_variant | SRC-BH-BACA-PEARLING-PATH |
| ALS-BH-5919774242D25CBA | ENT-BH-ARCHAEOLOGICAL-SITE-DILMUN-BURIAL-MOUNDS | مدافن دلمون الأثرية | ar | official_variant | SRC-UNESCO-WHC-BH-1542 |
| ALS-BH-5F05226536365D92 | ENT-BH-GOVERNORATE-CAPITAL | Capital | en | official_variant | SRC-BH-SLRB-GOVERNORATE-AREA-2024 |
| ALS-BH-6AAE177C6A285BE3 | ENT-BH-GOVERNORATE-MUHARRAQ | Muharraq | en | official_variant | SRC-BH-SLRB-GOVERNORATE-AREA-2024 |
| ALS-BH-C5463B1ED9F95C86 | ENT-BH-GOVERNORATE-SOUTHERN | Southern | en | official_variant | SRC-BH-SLRB-GOVERNORATE-AREA-2024 |
| ALS-BH-ED7BDF8AE3FA5703 | ENT-BH-GOVERNORATE-NORTHERN | Northern | en | official_variant | SRC-BH-SLRB-GOVERNORATE-AREA-2024 |

## علاقات الإدارة/الموقع

| المعرّف | الابن | الأب | العلاقة | الحالة | المصدر |
|---|---|---|---|---|---|
| REL-BH-03937398B18A57E8 | ENT-BH-CULTURAL-SITE-PEARLING | ENT-BH-COUNTRY | associated_with | current | SRC-UNESCO-WHC-BH-1364 |
| REL-BH-6318F911AB8E5A7E | ENT-BH-GOVERNORATE-MUHARRAQ | ENT-BH-COUNTRY | administrative_parent | current | SRC-BH-SLRB-GOVERNORATE-AREA-2024 |
| REL-BH-6603FAFDA7E7584D | ENT-BH-GOVERNORATE-NORTHERN | ENT-BH-COUNTRY | administrative_parent | current | SRC-BH-SLRB-GOVERNORATE-AREA-2024 |
| REL-BH-74923BC8432D534C | ENT-BH-GOVERNORATE-CAPITAL | ENT-BH-COUNTRY | administrative_parent | current | SRC-BH-SLRB-GOVERNORATE-AREA-2024 |
| REL-BH-8A624FAA17FB5E8F | ENT-BH-ARCHAEOLOGICAL-SITE-DILMUN-BURIAL-MOUNDS | ENT-BH-COUNTRY | associated_with | current | SRC-UNESCO-WHC-BH-1542 |
| REL-BH-B1F43343491A54C0 | ENT-BH-GOVERNORATE-SOUTHERN | ENT-BH-COUNTRY | administrative_parent | current | SRC-BH-SLRB-GOVERNORATE-AREA-2024 |
| REL-BH-E45C5AD33DD550E3 | ENT-BH-ARCHAEOLOGICAL-SITE-QALAT-AL-BAHRAIN | ENT-BH-COUNTRY | associated_with | current | SRC-UNESCO-WHC-BH-1192 |

## الادعاءات

| المعرّف | الموضوع | المحمول | القيمة | التصنيف | الثقة | الحالة | المصدر | المحدد |
|---|---|---|---|---|---|---|---|---|
| CLM-BH-12D120CC06C85150 | ENT-BH-GOVERNORATE-SOUTHERN | area | 488.77 | official | high | verified | SRC-BH-SLRB-GOVERNORATE-AREA-2024 | 2024 API record N=79: الجنوبية / Southern; area=488.77 km² |
| CLM-BH-430640AC1C2E595C | ENT-BH-ARCHAEOLOGICAL-SITE-QALAT-AL-BAHRAIN | world_heritage_inscription_year | 2005 | official | high | verified | SRC-UNESCO-WHC-BH-1192 | World Heritage property 1192; Qal’at al-Bahrain – Ancient Harbour and Capital of Dilmun; inscribed 2005; category Cultural |
| CLM-BH-50A68C15FDB45649 | ENT-BH-ARCHAEOLOGICAL-SITE-DILMUN-BURIAL-MOUNDS | world_heritage_category | cultural | official | high | verified | SRC-UNESCO-WHC-BH-1542 | World Heritage property 1542; Dilmun Burial Mounds; inscribed 2019; category Cultural |
| CLM-BH-6C77E6837C3D5FB6 | ENT-BH-ARCHAEOLOGICAL-SITE-QALAT-AL-BAHRAIN | documented_chronology | continuous human presence from about 2300 BCE to the 16th century CE | historical | high | verified | SRC-UNESCO-WHC-BH-1192 | property 1192 brief description; occupation chronology |
| CLM-BH-831A35C8D8BA5CB0 | ENT-BH-ARCHAEOLOGICAL-SITE-DILMUN-BURIAL-MOUNDS | world_heritage_inscription_year | 2019 | official | high | verified | SRC-UNESCO-WHC-BH-1542 | World Heritage property 1542; Dilmun Burial Mounds; inscribed 2019; category Cultural |
| CLM-BH-876A95FD648C5BB2 | ENT-BH-GOVERNORATE-MUHARRAQ | area | 74.1 | official | high | verified | SRC-BH-SLRB-GOVERNORATE-AREA-2024 | 2024 API record N=77: المحرق / Muharraq; area=74.1 km² |
| CLM-BH-94F864F2C5D55216 | ENT-BH-ARCHAEOLOGICAL-SITE-DILMUN-BURIAL-MOUNDS | documented_chronology | built between 2200 and 1750 BCE across 21 archaeological component sites | historical | high | verified | SRC-UNESCO-WHC-BH-1542 | property 1542 brief description; construction range and serial component count |
| CLM-BH-A3D4A78157D15078 | ENT-BH-GOVERNORATE-NORTHERN | area | 145.69 | official | high | verified | SRC-BH-SLRB-GOVERNORATE-AREA-2024 | 2024 API record N=78: الشمالية / Northern; area=145.69 km² |
| CLM-BH-A749E261CC5C5923 | ENT-BH-CULTURAL-SITE-PEARLING | world_heritage_category | cultural | official | high | verified | SRC-UNESCO-WHC-BH-1364 | World Heritage property 1364; Pearling, Testimony of an Island Economy; inscribed 2012; category Cultural |
| CLM-BH-BA120E308FC95C6A | ENT-BH-CULTURAL-SITE-PEARLING | world_heritage_inscription_year | 2012 | official | high | verified | SRC-UNESCO-WHC-BH-1364 | World Heritage property 1364; Pearling, Testimony of an Island Economy; inscribed 2012; category Cultural |
| CLM-BH-DD44E9ADC99757F3 | ENT-BH-ARCHAEOLOGICAL-SITE-QALAT-AL-BAHRAIN | world_heritage_category | cultural | official | high | verified | SRC-UNESCO-WHC-BH-1192 | World Heritage property 1192; Qal’at al-Bahrain – Ancient Harbour and Capital of Dilmun; inscribed 2005; category Cultural |
| CLM-BH-EABE29983FB351B2 | ENT-BH-CULTURAL-SITE-PEARLING | heritage_route_extent | more than 3 kilometres from the pearling oyster beds near Qal’at Bu Mahir to Siyadi House in Muharraq | official | high | verified | SRC-BH-BACA-PEARLING-PATH | official Arabic Pearling Path project description |
| CLM-BH-F7D50330EDCF5043 | ENT-BH-GOVERNORATE-CAPITAL | area | 79.23 | official | high | verified | SRC-BH-SLRB-GOVERNORATE-AREA-2024 | 2024 API record N=76: العاصمة / Capital; area=79.23 km² |

## جودة مصادر الادعاءات المنشورة

ادعاءات A/B: 13 من 13 (100.00%).

## المصادر الذرية المستخدمة

| المعرّف | الفئة | العنوان | الناشر | تاريخ النشر | تاريخ الاسترجاع | الترخيص | الرابط |
|---|---|---|---|---|---|---|---|
| SRC-BH-BACA-PEARLING-PATH | A | طريق اللؤلؤ | هيئة البحرين للثقافة والآثار | — | 2026-08-16 | Bahrain Authority for Culture and Antiquities; factual extraction with attribution | https://www.culture.gov.bh/ar/authority/infra_projects/Name,14932,ar.php |
| SRC-BH-SLRB-GOVERNORATE-AREA-2024 | A | Area by Governorate — 2024 records | Survey and Land Registration Bureau | — | 2026-08-16 | Bahrain Open Data Policy: republication and distribution permitted, subject to applicable laws | https://www.data.gov.bh/explore/dataset/02-area-by-governorate-2023/ |
| SRC-ISO-3166-1-2020 | A | ISO 3166-1:2020 — Codes for the representation of names of countries and their subdivisions — Part 1: Country code | International Organization for Standardization (ISO) | 2020-08 | 2026-08-15 | ISO copyright; reuse is subject to ISO terms of use | https://www.iso.org/obp/ui/#iso:std:iso:3166:-1:ed-4:v1:en |
| SRC-UNESCO-WHC-BH-1192 | A | Qal’at al-Bahrain – Ancient Harbour and Capital of Dilmun | UNESCO World Heritage Centre | — | 2026-08-16 | CC BY-SA 3.0 IGO for property descriptions | https://whc.unesco.org/en/list/1192 |
| SRC-UNESCO-WHC-BH-1364 | A | Pearling, Testimony of an Island Economy | UNESCO World Heritage Centre | — | 2026-08-16 | CC BY-SA 3.0 IGO for property descriptions | https://whc.unesco.org/en/list/1364 |
| SRC-UNESCO-WHC-BH-1542 | A | Dilmun Burial Mounds | UNESCO World Heritage Centre | — | 2026-08-16 | CC BY-SA 3.0 IGO for property descriptions | https://whc.unesco.org/en/list/1542 |
| SRC-UNESCO-WHC-BH-2026 | A | World Heritage List — Bahrain properties | UNESCO World Heritage Centre | — | 2026-08-16 | CC BY-SA 3.0 IGO for property descriptions | https://whc.unesco.org/en/statesparties/bh |

---
_مولّد آليًا؛ لا تعدّل هذا الملف مباشرة._
