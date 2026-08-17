# مصر (EG) — عرض مولّد من Schema 2.0.0

> **حدود التغطية:** التغطية المحلية غير مكتملة. لا تمثل هذه الصفحة جميع المدن أو القرى أو الأحياء أو الحارات، ولا يُستدل على التغطية من وجود ملف. البيانات المنظمة هي المصدر؛ هذه الصفحة عرض مولّد.

## التغطية والمقامات

أي نسبة 100% أدناه مقيدة بالدولة والطبقة والمقام المؤرخ واللقطة والمصدر الظاهرة في الصف نفسه؛ ولا تمتد إلى طبقة أخرى.

| الطبقة | تعريف المقام | المقام | مطابق | غير مطابق | مستبعد | مفقود | النسبة | تاريخ اللقطة | اللقطة | المصدر | الترخيص | مكتمل | سبب النقص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| country_scope | ISO country entity in the project's 22-country scope | 1 | 1 | 0 | 0 | 0 | 100% | 2026-08-15 | SNP-MIGRATION-2026-08-15 | SRC-ISO-3166-1-2020 | ISO copyright; reuse is subject to ISO terms of use | نعم | — |
| eg_governorate | Exact eg_governorate profile denominator. | 27 | 27 | 0 | 0 | 0 | 100% | 2026-08-16 | SNP-EG-PRODUCTION-20260816 | SRC-EG-CAPMAS-27-GOVERNORATES-2021 | Official Egypt statistical/government material; factual extraction with attribution; reuse terms not stated | نعم | — |
| eg_markaz_documented_subset | Documented markaz subset: 55 attested marakiz in four governorates (Daqahliya 18, Sharqia 13, Beheira 15, Minya 9); the national markaz universe remains open with no accepted atomic denominator. | 55 | 55 | 0 | 0 | 0 | 100% | 2026-08-16 | SNP-EG-PRODUCTION-20260816 | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Official Egypt statistical/government material; factual extraction with attribution; reuse terms not stated | نعم | — |
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
| ENT-EG-MARKAZ-079FC6085A04 | دمنهور | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate البحيرة: دمنهور |
| ENT-EG-MARKAZ-0F89A76D5772 | ميت غمر | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: ميت غمر |
| ENT-EG-MARKAZ-1415CE6556F4 | سمالوط | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate المنيا: سمالوط |
| ENT-EG-MARKAZ-1D2610C975E0 | الستاموني | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: الستاموني |
| ENT-EG-MARKAZ-1D65C7E6011C | فاقوس | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الشرقية: فاقوس |
| ENT-EG-MARKAZ-25CBE288EA01 | أبو المطامير | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate البحيرة: أبو المطامير |
| ENT-EG-MARKAZ-2A1E4FD359DE | المنصورة | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: المنصورة |
| ENT-EG-MARKAZ-2CD1FDEA7045 | الإبراهيمية | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الشرقية: الإبراهيمية |
| ENT-EG-MARKAZ-391EA53995F0 | الرحمانية | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate البحيرة: الرحمانية |
| ENT-EG-MARKAZ-3E7255651088 | العدوة | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate المنيا: العدوة |
| ENT-EG-MARKAZ-3F6B8F84472F | بني مزار | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate المنيا: بني مزار |
| ENT-EG-MARKAZ-47499CF8C4BD | مشتول السوق | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الشرقية: مشتول السوق |
| ENT-EG-MARKAZ-47E6DE529EE2 | شبراخيت | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate البحيرة: شبراخيت |
| ENT-EG-MARKAZ-480DA5AE313B | المطرية | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: المطرية |
| ENT-EG-MARKAZ-487CDB20D865 | المحمودية | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate البحيرة: المحمودية |
| ENT-EG-MARKAZ-4DAC6BD1B6E2 | بدر | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate البحيرة: بدر |
| ENT-EG-MARKAZ-4E89B503255A | نبروه | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: نبروه |
| ENT-EG-MARKAZ-536172057227 | كفر صقر | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الشرقية: كفر صقر |
| ENT-EG-MARKAZ-59EBBFA4FF1C | أولاد صقر | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الشرقية: أولاد صقر |
| ENT-EG-MARKAZ-5DBFABB1CECC | السنبلاوين | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: السنبلاوين |
| ENT-EG-MARKAZ-5DC8C47F34FB | ههيا | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الشرقية: ههيا |
| ENT-EG-MARKAZ-64BC431C83E3 | محلة دمنة | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: محلة دمنة |
| ENT-EG-MARKAZ-755E08625245 | تمي الأمديد | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: تمي الأمديد |
| ENT-EG-MARKAZ-785D0823A009 | أبو حمص | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate البحيرة: أبو حمص |
| ENT-EG-MARKAZ-794A7F7A2581 | مطاي | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate المنيا: مطاي |
| ENT-EG-MARKAZ-7E51008A6086 | طلخا | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: طلخا |
| ENT-EG-MARKAZ-812108E483A0 | ملوي | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate المنيا: ملوي |
| ENT-EG-MARKAZ-84EBAB2799D3 | بلقاس | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: بلقاس |
| ENT-EG-MARKAZ-8CE9CFF21B25 | الزقازيق | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الشرقية: الزقازيق |
| ENT-EG-MARKAZ-9A6B38CC493B | بني عبيد | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: بني عبيد |
| ENT-EG-MARKAZ-A3A71A0BF4D1 | ديرب نجم | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الشرقية: ديرب نجم |
| ENT-EG-MARKAZ-A5CC0F2B2ED1 | المنزلة | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: المنزلة |
| ENT-EG-MARKAZ-AC63EB7298A2 | منية النصر | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: منية النصر |
| ENT-EG-MARKAZ-AEA700EC7233 | دكرنس | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: دكرنس |
| ENT-EG-MARKAZ-AFD18A9497FF | مغاغة | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate المنيا: مغاغة |
| ENT-EG-MARKAZ-B0BB759F390E | إدكو | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate البحيرة: إدكو |
| ENT-EG-MARKAZ-B514A84A78CA | إيتاي البارود | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate البحيرة: إيتاي البارود |
| ENT-EG-MARKAZ-BCD51FD99F68 | أبو قرقاص | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate المنيا: أبو قرقاص |
| ENT-EG-MARKAZ-BFC0D17A2F9A | المنيا | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate المنيا: المنيا |
| ENT-EG-MARKAZ-C32DD2236903 | أبو حماد | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الشرقية: أبو حماد |
| ENT-EG-MARKAZ-C3AF3A7FFF3B | ميت سلسيل | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: ميت سلسيل |
| ENT-EG-MARKAZ-C5CB3C22818C | كوم حمادة | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate البحيرة: كوم حمادة |
| ENT-EG-MARKAZ-C6774903D0C0 | كفر الدوار | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate البحيرة: كفر الدوار |
| ENT-EG-MARKAZ-CB4CD8109E84 | حوش عيسى | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate البحيرة: حوش عيسى |
| ENT-EG-MARKAZ-D1AFFDC3B89E | شربين | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: شربين |
| ENT-EG-MARKAZ-D1CD047A4267 | الدلنجات | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate البحيرة: الدلنجات |
| ENT-EG-MARKAZ-DAA46DBFF35A | دير مواس | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate المنيا: دير مواس |
| ENT-EG-MARKAZ-DCB5B339047A | منيا القمح | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الشرقية: منيا القمح |
| ENT-EG-MARKAZ-E73EB9541AAC | بلبيس | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الشرقية: بلبيس |
| ENT-EG-MARKAZ-EA430E79C330 | وادي النطرون | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate البحيرة: وادي النطرون |
| ENT-EG-MARKAZ-ED7471683E75 | الحسينية | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الشرقية: الحسينية |
| ENT-EG-MARKAZ-EF5540E84226 | أبو كبير | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الشرقية: أبو كبير |
| ENT-EG-MARKAZ-F3050001F668 | رشيد | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate البحيرة: رشيد |
| ENT-EG-MARKAZ-F8AAC2E84A82 | الجمالية | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: الجمالية |
| ENT-EG-MARKAZ-FEE34036123A | أجا | eg_markaz | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | Markaz table, governorate الدقهلية: أجا |

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
| REL-EG-MARKAZ-0075CDB7F5BF5FB3 | ENT-EG-MARKAZ-DCB5B339047A | ENT-EG-GOVERNORATE-13 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-017573D01893585E | ENT-EG-MARKAZ-47499CF8C4BD | ENT-EG-GOVERNORATE-13 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-024AEC8F8E8B53E2 | ENT-EG-MARKAZ-D1CD047A4267 | ENT-EG-GOVERNORATE-18 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-0C43F6953B5A5B30 | ENT-EG-MARKAZ-E73EB9541AAC | ENT-EG-GOVERNORATE-13 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-0C6ADEF7BABA5E54 | ENT-EG-MARKAZ-8CE9CFF21B25 | ENT-EG-GOVERNORATE-13 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-0FBB89C196595349 | ENT-EG-MARKAZ-5DBFABB1CECC | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-15F9D1C9AE375C7A | ENT-EG-MARKAZ-480DA5AE313B | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-273066CDE0505963 | ENT-EG-MARKAZ-84EBAB2799D3 | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-29E5B52BB58657D2 | ENT-EG-MARKAZ-C5CB3C22818C | ENT-EG-GOVERNORATE-18 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-2BAFEE66D0C95F0E | ENT-EG-MARKAZ-2CD1FDEA7045 | ENT-EG-GOVERNORATE-13 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-35FB8B409C6E5557 | ENT-EG-MARKAZ-079FC6085A04 | ENT-EG-GOVERNORATE-18 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-3663001B65DF5BCE | ENT-EG-MARKAZ-C6774903D0C0 | ENT-EG-GOVERNORATE-18 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-386B8A894F005FA4 | ENT-EG-MARKAZ-AC63EB7298A2 | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-3912ECE715645E4C | ENT-EG-MARKAZ-ED7471683E75 | ENT-EG-GOVERNORATE-13 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-3928796E4C7A5488 | ENT-EG-MARKAZ-47E6DE529EE2 | ENT-EG-GOVERNORATE-18 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-395AC751375357F0 | ENT-EG-MARKAZ-536172057227 | ENT-EG-GOVERNORATE-13 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-3FAECB2B61FD5ABA | ENT-EG-MARKAZ-64BC431C83E3 | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-4AEE2FECA8BF5F22 | ENT-EG-MARKAZ-25CBE288EA01 | ENT-EG-GOVERNORATE-18 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-5BD7C7381EB95364 | ENT-EG-MARKAZ-4E89B503255A | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-5FDB006AB389508E | ENT-EG-MARKAZ-487CDB20D865 | ENT-EG-GOVERNORATE-18 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-6295DF3E52175ADD | ENT-EG-MARKAZ-794A7F7A2581 | ENT-EG-GOVERNORATE-24 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-70F2CE7263AF5979 | ENT-EG-MARKAZ-FEE34036123A | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-7B8648DDF01E5C3A | ENT-EG-MARKAZ-BFC0D17A2F9A | ENT-EG-GOVERNORATE-24 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-7CFC7DA3C5F65B6C | ENT-EG-MARKAZ-59EBBFA4FF1C | ENT-EG-GOVERNORATE-13 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-843392CE96BF541A | ENT-EG-MARKAZ-B514A84A78CA | ENT-EG-GOVERNORATE-18 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-8BF6920057865294 | ENT-EG-MARKAZ-1D2610C975E0 | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-95F9EC9381B55500 | ENT-EG-MARKAZ-7E51008A6086 | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-982CB014B97F56D4 | ENT-EG-MARKAZ-785D0823A009 | ENT-EG-GOVERNORATE-18 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-9E400DAFDDFD5417 | ENT-EG-MARKAZ-812108E483A0 | ENT-EG-GOVERNORATE-24 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-A80FB5A9FAE45542 | ENT-EG-MARKAZ-1415CE6556F4 | ENT-EG-GOVERNORATE-24 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-AD13B0882DE15368 | ENT-EG-MARKAZ-C3AF3A7FFF3B | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-B39F55449347586E | ENT-EG-MARKAZ-AEA700EC7233 | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-B5ED278F1EC658C8 | ENT-EG-MARKAZ-A3A71A0BF4D1 | ENT-EG-GOVERNORATE-13 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-BD464E210CF45028 | ENT-EG-MARKAZ-0F89A76D5772 | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-BE4C5AA5BC845381 | ENT-EG-MARKAZ-B0BB759F390E | ENT-EG-GOVERNORATE-18 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-C59D1DBD043D543C | ENT-EG-MARKAZ-3E7255651088 | ENT-EG-GOVERNORATE-24 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-CA8A05F6CB5B55B2 | ENT-EG-MARKAZ-F8AAC2E84A82 | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-CACA8AC5C4FB5DF7 | ENT-EG-MARKAZ-A5CC0F2B2ED1 | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-CCF47D173BDA55F1 | ENT-EG-MARKAZ-4DAC6BD1B6E2 | ENT-EG-GOVERNORATE-18 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-CCF613D688FC52A0 | ENT-EG-MARKAZ-2A1E4FD359DE | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-D0CB40B88AC75BB7 | ENT-EG-MARKAZ-EF5540E84226 | ENT-EG-GOVERNORATE-13 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-D7C8FCBEAF945F31 | ENT-EG-MARKAZ-3F6B8F84472F | ENT-EG-GOVERNORATE-24 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-DB1342ECEA5856EE | ENT-EG-MARKAZ-1D65C7E6011C | ENT-EG-GOVERNORATE-13 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-DCFAE85167EC5462 | ENT-EG-MARKAZ-755E08625245 | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-E02BFCCE6D7F5266 | ENT-EG-MARKAZ-5DC8C47F34FB | ENT-EG-GOVERNORATE-13 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-E03D4068D8555247 | ENT-EG-MARKAZ-D1AFFDC3B89E | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-E839580E36735348 | ENT-EG-MARKAZ-CB4CD8109E84 | ENT-EG-GOVERNORATE-18 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-E8E02CA4683F5822 | ENT-EG-MARKAZ-EA430E79C330 | ENT-EG-GOVERNORATE-18 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-EC4D3A09CCA35944 | ENT-EG-MARKAZ-DAA46DBFF35A | ENT-EG-GOVERNORATE-24 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-ED235261AD775AD2 | ENT-EG-MARKAZ-C32DD2236903 | ENT-EG-GOVERNORATE-13 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-F69D007C66B5565F | ENT-EG-MARKAZ-AFD18A9497FF | ENT-EG-GOVERNORATE-24 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-F7334BE150EC59AF | ENT-EG-MARKAZ-9A6B38CC493B | ENT-EG-GOVERNORATE-12 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-FAA25E054BC35FE8 | ENT-EG-MARKAZ-F3050001F668 | ENT-EG-GOVERNORATE-18 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-FAEF12DFA05D5690 | ENT-EG-MARKAZ-391EA53995F0 | ENT-EG-GOVERNORATE-18 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |
| REL-EG-MARKAZ-FE6C67F624045890 | ENT-EG-MARKAZ-BCD51FD99F68 | ENT-EG-GOVERNORATE-24 | administrative_parent | current | SRC-EG-MARKAZ-LISTS-MIRROR-2026 |

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
| CLM-EG-MRKPOP-161090951A1B50DF | ENT-EG-MARKAZ-755E08625245 | population | 211782 | local | medium | reported | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | 2024 population row: تمي الأمديد |
| CLM-EG-MRKPOP-1796D9EA1E915C61 | ENT-EG-MARKAZ-A5CC0F2B2ED1 | population | 393139 | local | medium | reported | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | 2024 population row: المنزلة |
| CLM-EG-MRKPOP-2088E6BA03DF5504 | ENT-EG-MARKAZ-64BC431C83E3 | population | 68239 | local | medium | reported | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | 2024 population row: محلة دمنة |
| CLM-EG-MRKPOP-39FCAF4F4308593D | ENT-EG-MARKAZ-FEE34036123A | population | 575127 | local | medium | reported | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | 2024 population row: أجا |
| CLM-EG-MRKPOP-4C72581E90AC5897 | ENT-EG-MARKAZ-4E89B503255A | population | 305150 | local | medium | reported | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | 2024 population row: نبروه |
| CLM-EG-MRKPOP-515E98B8B00F5CC7 | ENT-EG-MARKAZ-C3AF3A7FFF3B | population | 81875 | local | medium | reported | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | 2024 population row: ميت سلسيل |
| CLM-EG-MRKPOP-5F8575C7F7BF5EDD | ENT-EG-MARKAZ-480DA5AE313B | population | 203140 | local | medium | reported | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | 2024 population row: المطرية |
| CLM-EG-MRKPOP-6269087900B2548E | ENT-EG-MARKAZ-2A1E4FD359DE | population | 659238 | local | medium | reported | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | 2024 population row: المنصورة |
| CLM-EG-MRKPOP-6CA19AE931735D17 | ENT-EG-MARKAZ-F8AAC2E84A82 | population | 154949 | local | medium | reported | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | 2024 population row: الجمالية |
| CLM-EG-MRKPOP-911D00578C115415 | ENT-EG-MARKAZ-9A6B38CC493B | population | 143301 | local | medium | reported | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | 2024 population row: بني عبيد |
| CLM-EG-MRKPOP-A0807F1A86C75E63 | ENT-EG-MARKAZ-D1AFFDC3B89E | population | 460193 | local | medium | reported | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | 2024 population row: شربين |
| CLM-EG-MRKPOP-A5F381257ABD5618 | ENT-EG-MARKAZ-7E51008A6086 | population | 425606 | local | medium | reported | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | 2024 population row: طلخا |
| CLM-EG-MRKPOP-ADE381B391A851E0 | ENT-EG-MARKAZ-0F89A76D5772 | population | 703717 | local | medium | reported | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | 2024 population row: ميت غمر |
| CLM-EG-MRKPOP-C1A4E804E2115E0D | ENT-EG-MARKAZ-5DBFABB1CECC | population | 612345 | local | medium | reported | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | 2024 population row: السنبلاوين |
| CLM-EG-MRKPOP-D396925CDF8656CB | ENT-EG-MARKAZ-AC63EB7298A2 | population | 290526 | local | medium | reported | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | 2024 population row: منية النصر |
| CLM-EG-MRKPOP-E2109566C2C55979 | ENT-EG-MARKAZ-84EBAB2799D3 | population | 574876 | local | medium | reported | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | 2024 population row: بلقاس |
| CLM-EG-MRKPOP-F88FFFE41FF8592C | ENT-EG-MARKAZ-AEA700EC7233 | population | 383717 | local | medium | reported | SRC-EG-MARKAZ-LISTS-MIRROR-2026 | 2024 population row: دكرنس |

## جودة مصادر الادعاءات المنشورة

ادعاءات A/B: 27 من 27 (100.00%).

## المصادر الذرية المستخدمة

| المعرّف | الفئة | العنوان | الناشر | تاريخ النشر | تاريخ الاسترجاع | الترخيص | الرابط |
|---|---|---|---|---|---|---|---|
| SRC-EG-CAPMAS-27-GOVERNORATES-2021 | A | Egypt Family Health Survey 2021 — administrative geography | CAPMAS | — | 2026-08-16 | Official Egypt statistical/government material; factual extraction with attribution; reuse terms not stated | https://www.censusinfo.capmas.gov.eg/metadata-en-v4.2/index.php/catalog/665/download/1966 |
| SRC-EG-MARKAZ-LISTS-MIRROR-2026 | C | Markaz lists of four documented governorates — encyclopedic mirror of 2024 official rows | Encyclopedic mirror pages citing official 2024 governorate tables | — | 2026-08-16 | Official Egypt statistical/government material; factual extraction with attribution; reuse terms not stated | https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D9%85%D8%B1%D8%A7%D9%83%D8%B2_%D9%85%D8%B5%D8%B1 |
| SRC-EG-MLD-27-GOVERNORATES-2026 | A | Ministry of Local Development — 27 governorates | Ministry of Local Development | — | 2026-08-16 | Official Egypt statistical/government material; factual extraction with attribution; reuse terms not stated | https://www.mld.gov.eg/en/ |
| SRC-ISO-3166-1-2020 | A | ISO 3166-1:2020 — Codes for the representation of names of countries and their subdivisions — Part 1: Country code | International Organization for Standardization (ISO) | 2020-08 | 2026-08-15 | ISO copyright; reuse is subject to ISO terms of use | https://www.iso.org/obp/ui/#iso:std:iso:3166:-1:ed-4:v1:en |

---
_مولّد آليًا؛ لا تعدّل هذا الملف مباشرة._
