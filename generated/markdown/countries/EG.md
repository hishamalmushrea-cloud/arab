# مصر (EG) — عرض مولّد من Schema 2.0.0

> **حدود التغطية:** التغطية المحلية غير مكتملة. لا تمثل هذه الصفحة جميع المدن أو القرى أو الأحياء أو الحارات، ولا يُستدل على التغطية من وجود ملف. البيانات المنظمة هي المصدر؛ هذه الصفحة عرض مولّد.

## التغطية والمقامات

أي نسبة 100% أدناه مقيدة بالدولة والطبقة والمقام المؤرخ واللقطة والمصدر الظاهرة في الصف نفسه؛ ولا تمتد إلى طبقة أخرى.

| الطبقة | تعريف المقام | المقام | مطابق | غير مطابق | مستبعد | مفقود | النسبة | تاريخ اللقطة | اللقطة | المصدر | الترخيص | مكتمل | سبب النقص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| country_scope | ISO country entity in the project's 22-country scope | 1 | 1 | 0 | 0 | 0 | 100% | 2026-08-15 | SNP-MIGRATION-2026-08-15 | SRC-ISO-3166-1-2020 | ISO copyright; reuse is subject to ISO terms of use | نعم | — |
| eg_governorate | Exact eg_governorate profile denominator. | 27 | 27 | 0 | 0 | 0 | 100% | 2026-08-16 | SNP-EG-PRODUCTION-20260816 | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | Official Egypt statistical/government material; factual extraction with attribution; reuse terms not stated | نعم | — |
| eg_governorate_mixed_profile | Exact eg_governorate_mixed_profile profile denominator. | 23 | 23 | 0 | 0 | 0 | 100% | 2026-08-16 | SNP-EG-PRODUCTION-20260816 | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | Official Egypt statistical/government material; factual extraction with attribution; reuse terms not stated | نعم | — |
| eg_governorate_urban_profile | Exact eg_governorate_urban_profile profile denominator. | 4 | 4 | 0 | 0 | 0 | 100% | 2026-08-16 | SNP-EG-PRODUCTION-20260816 | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | Official Egypt statistical/government material; factual extraction with attribution; reuse terms not stated | نعم | — |

## الكيانات

| المعرّف | الاسم | النوع | الحالة | المصدر القانوني/المرجعي | المحدد داخل المصدر |
|---|---|---|---|---|---|
| ENT-EG-COUNTRY | مصر | country | current | SRC-ISO-3166-1-2020 | ISO alpha-2 entry EG |
| ENT-EG-GOVERNORATE-01 | القاهرة | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 01: القاهرة / Cairo; profile=urban_only |
| ENT-EG-GOVERNORATE-02 | الإسكندرية | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 02: الإسكندرية / Alexandria; profile=urban_only |
| ENT-EG-GOVERNORATE-03 | بورسعيد | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 03: بورسعيد / Port Said; profile=urban_only |
| ENT-EG-GOVERNORATE-04 | السويس | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 04: السويس / Suez; profile=urban_only |
| ENT-EG-GOVERNORATE-11 | دمياط | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 11: دمياط / Damietta; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-12 | الدقهلية | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 12: الدقهلية / Dakahlia; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-13 | الشرقية | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 13: الشرقية / Sharkia; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-14 | القليوبية | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 14: القليوبية / Qalyubia; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-15 | كفر الشيخ | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 15: كفر الشيخ / Kafr El Sheikh; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-16 | الغربية | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 16: الغربية / Gharbia; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-17 | المنوفية | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 17: المنوفية / Menoufia; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-18 | البحيرة | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 18: البحيرة / Beheira; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-19 | الإسماعيلية | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 19: الإسماعيلية / Ismailia; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-21 | الجيزة | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 21: الجيزة / Giza; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-22 | بني سويف | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 22: بني سويف / Beni Suef; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-23 | الفيوم | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 23: الفيوم / Fayoum; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-24 | المنيا | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 24: المنيا / Minya; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-25 | أسيوط | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 25: أسيوط / Assiut; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-26 | سوهاج | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 26: سوهاج / Sohag; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-27 | قنا | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 27: قنا / Qena; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-28 | أسوان | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 28: أسوان / Aswan; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-29 | الأقصر | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 29: الأقصر / Luxor; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-31 | البحر الأحمر | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 31: البحر الأحمر / Red Sea; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-32 | الوادي الجديد | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 32: الوادي الجديد / New Valley; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-33 | مطروح | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 33: مطروح / Matrouh; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-34 | شمال سيناء | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 34: شمال سيناء / North Sinai; profile=mixed_urban_rural |
| ENT-EG-GOVERNORATE-35 | جنوب سيناء | eg_governorate | current | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 35: جنوب سيناء / South Sinai; profile=mixed_urban_rural |

## الأسماء البديلة

| المعرّف | الكيان | الاسم | اللغة | النوع | المصدر |
|---|---|---|---|---|---|
| ALS-EG-015DE42C14E05244 | ENT-EG-GOVERNORATE-01 | Cairo | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-16F0AC98B87E5B97 | ENT-EG-GOVERNORATE-21 | Giza | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-231063A302F9510F | ENT-EG-GOVERNORATE-15 | Kafr El Sheikh | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-29CEF361CA8B5AD4 | ENT-EG-GOVERNORATE-03 | Port Said | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-2E0D39727D5E5557 | ENT-EG-GOVERNORATE-25 | Assiut | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-32423A1C4FFC5B3C | ENT-EG-GOVERNORATE-34 | North Sinai | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-401F4547DCED5105 | ENT-EG-GOVERNORATE-32 | New Valley | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-4A4F691BC0035719 | ENT-EG-GOVERNORATE-18 | Beheira | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-52BDF9F7948050EC | ENT-EG-GOVERNORATE-23 | Fayoum | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-5559DF8A869A54B3 | ENT-EG-GOVERNORATE-04 | Suez | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-7332FD553FFB5C64 | ENT-EG-GOVERNORATE-33 | Matrouh | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-7A2D2394EBCE5D53 | ENT-EG-GOVERNORATE-31 | Red Sea | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-7CFC08A0967F5149 | ENT-EG-GOVERNORATE-19 | Ismailia | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-81B8F88A2D7052B8 | ENT-EG-GOVERNORATE-24 | Minya | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-897D6314200454ED | ENT-EG-GOVERNORATE-17 | Menoufia | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-8A6881CBCF9C52C9 | ENT-EG-GOVERNORATE-13 | Sharkia | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-94B7AA684B9E5180 | ENT-EG-GOVERNORATE-22 | Beni Suef | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-9DC3F9D1F3205368 | ENT-EG-GOVERNORATE-12 | Dakahlia | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-A2804824EA3158C0 | ENT-EG-GOVERNORATE-29 | Luxor | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-AC770C65BD4F5D57 | ENT-EG-GOVERNORATE-02 | Alexandria | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-AFFDDE15886A55C1 | ENT-EG-GOVERNORATE-35 | South Sinai | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-B50CF03FDD685603 | ENT-EG-GOVERNORATE-28 | Aswan | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-B86C17FE6EF9507B | ENT-EG-GOVERNORATE-27 | Qena | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-BF3C3B2E26C45D14 | ENT-EG-GOVERNORATE-16 | Gharbia | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-FB9546A1A09B5DF5 | ENT-EG-GOVERNORATE-26 | Sohag | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-FEE652B921305A5B | ENT-EG-GOVERNORATE-14 | Qalyubia | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |
| ALS-EG-FF71BE22A0CA5AC8 | ENT-EG-GOVERNORATE-11 | Damietta | en | official_variant | SRC-EG-CAPMAS-27-GOVERNORATES-2021 |

## علاقات الإدارة/الموقع

| المعرّف | الابن | الأب | العلاقة | الحالة | المصدر |
|---|---|---|---|---|---|
| REL-EG-005E209EBB9D5D49 | ENT-EG-GOVERNORATE-24 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-01A0F8AA80C35ACC | ENT-EG-GOVERNORATE-03 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-07D21D1D404856CB | ENT-EG-GOVERNORATE-34 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-11DC1648ACF25B9C | ENT-EG-GOVERNORATE-16 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-18FBFDF85F475E59 | ENT-EG-GOVERNORATE-15 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-1F3F94A90D485495 | ENT-EG-GOVERNORATE-31 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-2EB56EAC4415504D | ENT-EG-GOVERNORATE-19 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-3129861BA2895F8F | ENT-EG-GOVERNORATE-11 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-37BC25C77FAB5CB2 | ENT-EG-GOVERNORATE-25 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-4A6C4E986C0352EA | ENT-EG-GOVERNORATE-04 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-4DDAA87D333A559C | ENT-EG-GOVERNORATE-32 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-58F4BB5B4DF75B9C | ENT-EG-GOVERNORATE-26 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-6A56D47152EE5C5D | ENT-EG-GOVERNORATE-22 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-75D39CAA1D3C5F60 | ENT-EG-GOVERNORATE-27 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-7C17FE2D8D515ECE | ENT-EG-GOVERNORATE-13 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-80BB609CEDC7526D | ENT-EG-GOVERNORATE-35 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-8B88F877A7CA5356 | ENT-EG-GOVERNORATE-23 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-A4C4713F861F52CF | ENT-EG-GOVERNORATE-01 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-ABAD2258B6785898 | ENT-EG-GOVERNORATE-02 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-B92E7C5CECED5B30 | ENT-EG-GOVERNORATE-14 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-C07DC4F962195E5F | ENT-EG-GOVERNORATE-18 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-C0B3942BC46B5C4B | ENT-EG-GOVERNORATE-28 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-C2F67A70C65F52E0 | ENT-EG-GOVERNORATE-17 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-D282D092C66959AF | ENT-EG-GOVERNORATE-33 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-DD208ECC5F315483 | ENT-EG-GOVERNORATE-12 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-F74855FB08AE5614 | ENT-EG-GOVERNORATE-21 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |
| REL-EG-FFAE8CA0D68B5A3D | ENT-EG-GOVERNORATE-29 | ENT-EG-COUNTRY | administrative_parent | current | SRC-EG-MLD-27-GOVERNORATES-2026 |

## الادعاءات

| المعرّف | الموضوع | المحمول | القيمة | التصنيف | الثقة | الحالة | المصدر | المحدد |
|---|---|---|---|---|---|---|---|---|
| CLM-EG-2231209413405157 | ENT-EG-GOVERNORATE-25 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 25: أسيوط / Assiut; profile=mixed_urban_rural |
| CLM-EG-2483777A5D3A5484 | ENT-EG-GOVERNORATE-35 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 35: جنوب سيناء / South Sinai; profile=mixed_urban_rural |
| CLM-EG-25988E32036D5950 | ENT-EG-GOVERNORATE-14 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 14: القليوبية / Qalyubia; profile=mixed_urban_rural |
| CLM-EG-2EB3AF7DF21051B7 | ENT-EG-GOVERNORATE-19 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 19: الإسماعيلية / Ismailia; profile=mixed_urban_rural |
| CLM-EG-31EF463188135F51 | ENT-EG-GOVERNORATE-34 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 34: شمال سيناء / North Sinai; profile=mixed_urban_rural |
| CLM-EG-43BD7BE36FB85AF1 | ENT-EG-GOVERNORATE-17 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 17: المنوفية / Menoufia; profile=mixed_urban_rural |
| CLM-EG-45BB1519204257D3 | ENT-EG-GOVERNORATE-27 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 27: قنا / Qena; profile=mixed_urban_rural |
| CLM-EG-46D8250E0DD65B8B | ENT-EG-GOVERNORATE-18 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 18: البحيرة / Beheira; profile=mixed_urban_rural |
| CLM-EG-509E3F6895725169 | ENT-EG-GOVERNORATE-16 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 16: الغربية / Gharbia; profile=mixed_urban_rural |
| CLM-EG-539EB1F981FF5B03 | ENT-EG-GOVERNORATE-31 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 31: البحر الأحمر / Red Sea; profile=mixed_urban_rural |
| CLM-EG-682CA5366CA45608 | ENT-EG-GOVERNORATE-03 | administrative_profile | urban_only | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 03: بورسعيد / Port Said; profile=urban_only |
| CLM-EG-697801AC3FCA5D44 | ENT-EG-GOVERNORATE-15 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 15: كفر الشيخ / Kafr El Sheikh; profile=mixed_urban_rural |
| CLM-EG-69A31071622B5A07 | ENT-EG-GOVERNORATE-22 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 22: بني سويف / Beni Suef; profile=mixed_urban_rural |
| CLM-EG-6B46941006A15070 | ENT-EG-GOVERNORATE-26 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 26: سوهاج / Sohag; profile=mixed_urban_rural |
| CLM-EG-6CA9630052C05B38 | ENT-EG-GOVERNORATE-32 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 32: الوادي الجديد / New Valley; profile=mixed_urban_rural |
| CLM-EG-7C66269835425478 | ENT-EG-GOVERNORATE-12 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 12: الدقهلية / Dakahlia; profile=mixed_urban_rural |
| CLM-EG-8960B8704B99572D | ENT-EG-GOVERNORATE-23 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 23: الفيوم / Fayoum; profile=mixed_urban_rural |
| CLM-EG-8A3FB554A9295D09 | ENT-EG-GOVERNORATE-04 | administrative_profile | urban_only | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 04: السويس / Suez; profile=urban_only |
| CLM-EG-C032B1FED7C25EE8 | ENT-EG-GOVERNORATE-33 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 33: مطروح / Matrouh; profile=mixed_urban_rural |
| CLM-EG-C268282D54E65454 | ENT-EG-GOVERNORATE-29 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 29: الأقصر / Luxor; profile=mixed_urban_rural |
| CLM-EG-D33F09D38D385FBF | ENT-EG-GOVERNORATE-21 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 21: الجيزة / Giza; profile=mixed_urban_rural |
| CLM-EG-E66FA53EB8BB5470 | ENT-EG-GOVERNORATE-11 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 11: دمياط / Damietta; profile=mixed_urban_rural |
| CLM-EG-E7AE87A1E4E659FB | ENT-EG-GOVERNORATE-01 | administrative_profile | urban_only | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 01: القاهرة / Cairo; profile=urban_only |
| CLM-EG-E9ABE687E4E35B8A | ENT-EG-GOVERNORATE-24 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 24: المنيا / Minya; profile=mixed_urban_rural |
| CLM-EG-EC1CBB6150425C3D | ENT-EG-GOVERNORATE-13 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 13: الشرقية / Sharkia; profile=mixed_urban_rural |
| CLM-EG-ED51AFE7AE5B5C2F | ENT-EG-GOVERNORATE-02 | administrative_profile | urban_only | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 02: الإسكندرية / Alexandria; profile=urban_only |
| CLM-EG-EF8D5264334E5A7B | ENT-EG-GOVERNORATE-28 | administrative_profile | mixed_urban_rural | official | high | verified | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | CAPMAS governorate code 28: أسوان / Aswan; profile=mixed_urban_rural |

## جودة مصادر الادعاءات المنشورة

ادعاءات A/B: 27 من 27 (100.00%).

## المصادر الذرية المستخدمة

| المعرّف | الفئة | العنوان | الناشر | تاريخ النشر | تاريخ الاسترجاع | الترخيص | الرابط |
|---|---|---|---|---|---|---|---|
| SRC-EG-CAPMAS-27-GOVERNORATES-2021 | A | Egypt Family Health Survey 2021 — administrative geography | CAPMAS | — | 2026-08-16 | Official Egypt statistical/government material; factual extraction with attribution; reuse terms not stated | https://www.censusinfo.capmas.gov.eg/metadata-en-v4.2/index.php/catalog/665/download/1966 |
| SRC-EG-MLD-27-GOVERNORATES-2026 | A | Ministry of Local Development — 27 governorates | Ministry of Local Development | — | 2026-08-16 | Official Egypt statistical/government material; factual extraction with attribution; reuse terms not stated | https://www.mld.gov.eg/en/ |
| SRC-ISO-3166-1-2020 | A | ISO 3166-1:2020 — Codes for the representation of names of countries and their subdivisions — Part 1: Country code | International Organization for Standardization (ISO) | 2020-08 | 2026-08-15 | ISO copyright; reuse is subject to ISO terms of use | https://www.iso.org/obp/ui/#iso:std:iso:3166:-1:ed-4:v1:en |

---
_مولّد آليًا؛ لا تعدّل هذا الملف مباشرة._
