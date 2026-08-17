# الصومال (SO) — عرض مولّد من Schema 2.0.0

> **حدود التغطية:** التغطية المحلية غير مكتملة. لا تمثل هذه الصفحة جميع المدن أو القرى أو الأحياء أو الحارات، ولا يُستدل على التغطية من وجود ملف. البيانات المنظمة هي المصدر؛ هذه الصفحة عرض مولّد.

## التغطية والمقامات

أي نسبة 100% أدناه مقيدة بالدولة والطبقة والمقام المؤرخ واللقطة والمصدر الظاهرة في الصف نفسه؛ ولا تمتد إلى طبقة أخرى.

| الطبقة | تعريف المقام | المقام | مطابق | غير مطابق | مستبعد | مفقود | النسبة | تاريخ اللقطة | اللقطة | المصدر | الترخيص | مكتمل | سبب النقص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| so_banadir_regional_administration | Banadir parallel regional administration. | 1 | 1 | 0 | 0 | 0 | 100% | 2026-08-17 | SNP-SO-PRODUCTION-20260817 | SRC-SO-MOP-FMS-2026 | Official Somalia federal material; factual extraction with attribution; reuse terms not stated | نعم | — |
| country_scope | ISO country entity in the project's 22-country scope | 1 | 1 | 0 | 0 | 0 | 100% | 2026-08-15 | SNP-MIGRATION-2026-08-15 | SRC-ISO-3166-1-2020 | ISO copyright; reuse is subject to ISO terms of use | نعم | — |
| so_district_record_universe | so_district_record_universe | — | 0 | 0 | 0 | — | — | 2026-08-17 | SNP-SO-PRODUCTION-20260817 | SRC-SO-MOP-FMS-2026 | Official Somalia federal material; factual extraction with attribution; reuse terms not stated | لا | No authority-reconciled national denominator is accepted across overlapping federal, Somaliland, Puntland, North East, and Banadir structures. |
| so_federal_member_state_mop_frame | Seven FMS in current Ministry of Planning frame. | 7 | 7 | 0 | 0 | 0 | 100% | 2026-08-17 | SNP-SO-PRODUCTION-20260817 | SRC-SO-MOP-FMS-2026 | Official Somalia federal material; factual extraction with attribution; reuse terms not stated | نعم | — |
| so_fms_north_east_current | North East full member from 2026-01-17. | 1 | 1 | 0 | 0 | 0 | 100% | 2026-08-17 | SNP-SO-PRODUCTION-20260817 | SRC-SO-SONNA-NORTHEAST-DECLARATION-2026 | Official Somalia federal material; factual extraction with attribution; reuse terms not stated | نعم | — |
| so_region_record_universe | so_region_record_universe | — | 0 | 0 | 0 | — | — | 2026-08-17 | SNP-SO-PRODUCTION-20260817 | SRC-SO-MOP-FMS-2026 | Official Somalia federal material; factual extraction with attribution; reuse terms not stated | لا | No authority-reconciled national denominator is accepted across overlapping federal, Somaliland, Puntland, North East, and Banadir structures. |
| so_fms_somaliland_fgs_narrative | FGS planning/Senate narrative only. | 1 | 1 | 0 | 0 | 0 | 100% | 2026-08-17 | SNP-SO-PRODUCTION-20260817 | SRC-SO-SENATE-CONSTITUENCY | Official Somalia federal material; factual extraction with attribution; reuse terms not stated | نعم | — |
| so_federal_member_state_standard_five | Five standard operational FMS in 2025 baseline. | 5 | 5 | 0 | 0 | 0 | 100% | 2026-08-17 | SNP-SO-PRODUCTION-20260817 | SRC-SO-MPWR-FIVE-FMS-2025 | Official Somalia federal material; factual extraction with attribution; reuse terms not stated | نعم | — |

## الكيانات

| المعرّف | الاسم | النوع | الحالة | المصدر القانوني/المرجعي | المحدد داخل المصدر |
|---|---|---|---|---|---|
| ENT-SO-COUNTRY | الصومال | country | current | SRC-ISO-3166-1-2020 | ISO alpha-2 entry SO |
| ENT-SO-FMS-01 | Puntland State of Somalia | so_federal_member_state | current | SRC-SO-MOP-FMS-2026 | Ministry of Planning FMS entry: Puntland State of Somalia |
| ENT-SO-FMS-02 | Hirshabelle State of Somalia | so_federal_member_state | current | SRC-SO-MOP-FMS-2026 | Ministry of Planning FMS entry: Hirshabelle State of Somalia |
| ENT-SO-FMS-03 | Jubaland State of Somalia | so_federal_member_state | current | SRC-SO-MOP-FMS-2026 | Ministry of Planning FMS entry: Jubaland State of Somalia |
| ENT-SO-FMS-04 | SouthWest State of Somalia | so_federal_member_state | current | SRC-SO-MOP-FMS-2026 | Ministry of Planning FMS entry: SouthWest State of Somalia |
| ENT-SO-FMS-05 | Galmudug State of Somalia | so_federal_member_state | current | SRC-SO-MOP-FMS-2026 | Ministry of Planning FMS entry: Galmudug State of Somalia |
| ENT-SO-FMS-06 | Somaliland | so_federal_member_state | claimed | SRC-SO-MOP-FMS-2026 | Ministry of Planning FMS entry: Somaliland |
| ENT-SO-FMS-07 | North East State of Somalia | so_federal_member_state | current | SRC-SO-SONNA-NORTHEAST-DECLARATION-2026 | Presidential full-member declaration, 17 January 2026 |
| ENT-SO-REGION-BRA | Banadir Regional Administration | so_region | current | SRC-SO-MOP-FMS-2026 | Banadir Regional Administration listed separately after seven FMS |

## الأسماء البديلة

| المعرّف | الكيان | الاسم | اللغة | النوع | المصدر |
|---|---|---|---|---|---|
| ALS-6ACA6DF2077A5A4E | ENT-SO-COUNTRY | Somalia | en | english | SRC-ISO-3166-1-2020 |

## علاقات الإدارة/الموقع

| المعرّف | الابن | الأب | العلاقة | الحالة | المصدر |
|---|---|---|---|---|---|
| REL-SO-15F856D41BDD5F2D | ENT-SO-FMS-04 | ENT-SO-COUNTRY | administrative_parent | current | SRC-SO-MOP-FMS-2026 |
| REL-SO-22BAC8ECCEDF521B | ENT-SO-REGION-BRA | ENT-SO-COUNTRY | administrative_parent | current | SRC-SO-MOP-FMS-2026 |
| REL-SO-8064C67EA10C5C05 | ENT-SO-FMS-06 | ENT-SO-COUNTRY | administrative_parent | claimed | SRC-SO-MOP-FMS-2026 |
| REL-SO-902245AF6C4756C1 | ENT-SO-FMS-05 | ENT-SO-COUNTRY | administrative_parent | current | SRC-SO-MOP-FMS-2026 |
| REL-SO-B07E206503BD5430 | ENT-SO-FMS-07 | ENT-SO-COUNTRY | administrative_parent | current | SRC-SO-SONNA-NORTHEAST-DECLARATION-2026 |
| REL-SO-DDFE7F2FD3935B5D | ENT-SO-FMS-01 | ENT-SO-COUNTRY | administrative_parent | current | SRC-SO-MOP-FMS-2026 |
| REL-SO-E8FE1103BF2B55A1 | ENT-SO-FMS-02 | ENT-SO-COUNTRY | administrative_parent | current | SRC-SO-MOP-FMS-2026 |
| REL-SO-FA7D0F6A0D3B5F85 | ENT-SO-FMS-03 | ENT-SO-COUNTRY | administrative_parent | current | SRC-SO-MOP-FMS-2026 |

## الادعاءات

| المعرّف | الموضوع | المحمول | القيمة | التصنيف | الثقة | الحالة | المصدر | المحدد |
|---|---|---|---|---|---|---|---|---|
| CLM-SO-073A90765B755ACB | ENT-SO-FMS-01 | federal_planning_profile | standard_fms | official | high | verified | SRC-SO-MOP-FMS-2026 | Ministry of Planning FMS entry: Puntland State of Somalia |
| CLM-SO-5EC6ABC9D87655DE | ENT-SO-REGION-BRA | federal_planning_profile | banadir_regional_administration | official | high | verified | SRC-SO-MOP-FMS-2026 | Banadir Regional Administration listed separately from seven FMS |
| CLM-SO-9DC8FCC100F95D89 | ENT-SO-FMS-07 | federal_planning_profile | new_fms | official | high | verified | SRC-SO-MOIFAR-NORTHEAST-2026 | Ministry of Planning FMS entry: North East State of Somalia |
| CLM-SO-A36F4F5AB281571B | ENT-SO-FMS-03 | federal_planning_profile | standard_fms | official | high | verified | SRC-SO-MOP-FMS-2026 | Ministry of Planning FMS entry: Jubaland State of Somalia |
| CLM-SO-A578C8D65BC05197 | ENT-SO-FMS-06 | federal_planning_profile | fgs_federal_planning_narrative | disputed | high | verified | SRC-SO-MOP-FMS-2026 | Ministry of Planning FMS entry: Somaliland |
| CLM-SO-BCD9733CE79055A9 | ENT-SO-FMS-02 | federal_planning_profile | standard_fms | official | high | verified | SRC-SO-MOP-FMS-2026 | Ministry of Planning FMS entry: Hirshabelle State of Somalia |
| CLM-SO-CB16E4AF0EBC5BA3 | ENT-SO-FMS-04 | federal_planning_profile | standard_fms | official | high | verified | SRC-SO-MOP-FMS-2026 | Ministry of Planning FMS entry: SouthWest State of Somalia |
| CLM-SO-D002B800321F5B6C | ENT-SO-FMS-05 | federal_planning_profile | standard_fms | official | high | verified | SRC-SO-MOP-FMS-2026 | Ministry of Planning FMS entry: Galmudug State of Somalia |
| CLM-SO-FD512D683B8F50A5 | ENT-SO-FMS-07 | federal_member_transition | {'constitution_adopted': '2025-07-30', 'full_member_declaration': '2026-01-17', 'leadership_elected': '2025-08-30', 'parliament_formed': '2025-08-17', 'predecessor_name': 'SSC-Khaatumo'} | official | high | verified | SRC-SO-MOIFAR-NORTHEAST-2026 | State formation completion and inauguration, 17 January 2026 |

## جودة مصادر الادعاءات المنشورة

ادعاءات A/B: 9 من 9 (100.00%).

## المصادر الذرية المستخدمة

| المعرّف | الفئة | العنوان | الناشر | تاريخ النشر | تاريخ الاسترجاع | الترخيص | الرابط |
|---|---|---|---|---|---|---|---|
| SRC-ISO-3166-1-2020 | A | ISO 3166-1:2020 — Codes for the representation of names of countries and their subdivisions — Part 1: Country code | International Organization for Standardization (ISO) | 2020-08 | 2026-08-15 | ISO copyright; reuse is subject to ISO terms of use | https://www.iso.org/obp/ui/#iso:std:iso:3166:-1:ed-4:v1:en |
| SRC-SO-MOIFAR-NORTHEAST-2026 | A | Formal establishment of North Eastern State | Ministry of Interior, Federal Affairs and Reconciliation | 2026-01-17 | 2026-08-17 | Official Somalia federal material; factual extraction with attribution; reuse terms not stated | https://moifar.gov.so/en/2026/01/17/federal-leadership-attends-inauguration-ceremony-of-the-president-of-the-north-eastern-state-of-somalia/ |
| SRC-SO-MOP-FMS-2026 | A | Federal Member States | Federal Government of Somalia, Ministry of Planning | — | 2026-08-17 | Official Somalia federal material; factual extraction with attribution; reuse terms not stated | https://mop.gov.so/federal-member-states/ |
| SRC-SO-MPWR-FIVE-FMS-2025 | A | 2025 project assessment: five Federal Member States | Federal Ministry of Public Works | 2025-04-01 | 2026-08-17 | Official Somalia federal material; factual extraction with attribution; reuse terms not stated | https://mpwr.gov.so/wp-content/uploads/2025/04/Draft-ESIA-April-15-2025-Beledwyne-Draft-II-AfDB-Reviewed-March-2025-Bank-FINAL-REVIEW-14042025.pdf |
| SRC-SO-SENATE-CONSTITUENCY | A | Senate constituency | Upper House of the Federal Parliament of Somalia | — | 2026-08-17 | Official Somalia federal material; factual extraction with attribution; reuse terms not stated | https://senate.gov.so/senate-constituency/?lang=en |
| SRC-SO-SONNA-NORTHEAST-DECLARATION-2026 | A | President declares North East State a full Federal Member State | Somali National News Agency | 2026-01-17 | 2026-08-17 | Official Somalia federal material; factual extraction with attribution; reuse terms not stated | https://sonna.so/en/president-hassan-sheikh-mohamud-declares-north-east-state-a-full-federal-member-state/ |

---
_مولّد آليًا؛ لا تعدّل هذا الملف مباشرة._
