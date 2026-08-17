# عُمان (OM) — عرض مولّد من Schema 2.0.0

> **حدود التغطية:** التغطية المحلية غير مكتملة. لا تمثل هذه الصفحة جميع المدن أو القرى أو الأحياء أو الحارات، ولا يُستدل على التغطية من وجود ملف. البيانات المنظمة هي المصدر؛ هذه الصفحة عرض مولّد.

## التغطية والمقامات

أي نسبة 100% أدناه مقيدة بالدولة والطبقة والمقام المؤرخ واللقطة والمصدر الظاهرة في الصف نفسه؛ ولا تمتد إلى طبقة أخرى.

| الطبقة | تعريف المقام | المقام | مطابق | غير مطابق | مستبعد | مفقود | النسبة | تاريخ اللقطة | اللقطة | المصدر | الترخيص | مكتمل | سبب النقص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| country_scope | ISO country entity in the project's 22-country scope | 1 | 1 | 0 | 0 | 0 | 100% | 2026-08-15 | SNP-MIGRATION-2026-08-15 | SRC-ISO-3166-1-2020 | ISO copyright; reuse is subject to ISO terms of use | نعم | — |
| om_governorate | All governorates in Decree 36/2022. | 11 | 11 | 0 | 0 | 0 | 100% | 2026-08-16 | SNP-OM-PRODUCTION-20260816 | SRC-OM-RD-36-2022-GOVERNORATES | Official Oman legal/statistical material; factual extraction with attribution; reuse terms not stated | نعم | — |
| om_wilaya | All legal wilayats after Al Jabal Al Akhdar and Sinaw additions. | 63 | 63 | 0 | 0 | 0 | 100% | 2026-08-16 | SNP-OM-PRODUCTION-20260816 | SRC-OM-RD-36-2022-GOVERNORATES | Official Oman legal/statistical material; factual extraction with attribution; reuse terms not stated | نعم | — |

## الكيانات

| المعرّف | الاسم | النوع | الحالة | المصدر القانوني/المرجعي | المحدد داخل المصدر |
|---|---|---|---|---|---|
| ENT-OM-COUNTRY | عُمان | country | current | SRC-ISO-3166-1-2020 | ISO alpha-2 entry OM |
| ENT-OM-GOVERNORATE-01 | مسقط | om_governorate | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 01: Muscat; 6 wilayats |
| ENT-OM-GOVERNORATE-02 | ظفار | om_governorate | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 02: Dhofar; 10 wilayats |
| ENT-OM-GOVERNORATE-03 | مسندم | om_governorate | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 03: Musandam; 4 wilayats |
| ENT-OM-GOVERNORATE-04 | البريمي | om_governorate | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 04: Al Buraimi; 3 wilayats |
| ENT-OM-GOVERNORATE-05 | الداخلية | om_governorate | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 05: Ad Dakhiliyah; 9 wilayats |
| ENT-OM-GOVERNORATE-06 | شمال الباطنة | om_governorate | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 06: North Al Batinah; 6 wilayats |
| ENT-OM-GOVERNORATE-07 | جنوب الباطنة | om_governorate | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 07: South Al Batinah; 6 wilayats |
| ENT-OM-GOVERNORATE-08 | جنوب الشرقية | om_governorate | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 08: South Ash Sharqiyah; 5 wilayats |
| ENT-OM-GOVERNORATE-09 | شمال الشرقية | om_governorate | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 09: North Ash Sharqiyah; 7 wilayats |
| ENT-OM-GOVERNORATE-10 | الظاهرة | om_governorate | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 10: Adh Dhahirah; 3 wilayats |
| ENT-OM-GOVERNORATE-11 | الوسطى | om_governorate | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 11: Al Wusta; 4 wilayats |
| ENT-OM-WILAYA-0101 | مسقط | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Muscat under Muscat; reconciled code 0101 |
| ENT-OM-WILAYA-0102 | مطرح | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Muttrah under Muscat; reconciled code 0102 |
| ENT-OM-WILAYA-0103 | العامرات | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Al Amerat under Muscat; reconciled code 0103 |
| ENT-OM-WILAYA-0104 | بوشر | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Bawshar under Muscat; reconciled code 0104 |
| ENT-OM-WILAYA-0105 | السيب | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: As Seeb under Muscat; reconciled code 0105 |
| ENT-OM-WILAYA-0106 | قريات | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Qurayyat under Muscat; reconciled code 0106 |
| ENT-OM-WILAYA-0201 | صلالة | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Salalah under Dhofar; reconciled code 0201 |
| ENT-OM-WILAYA-0202 | طاقة | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Taqah under Dhofar; reconciled code 0202 |
| ENT-OM-WILAYA-0203 | مرباط | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Mirbat under Dhofar; reconciled code 0203 |
| ENT-OM-WILAYA-0204 | رخيوت | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Rakhyut under Dhofar; reconciled code 0204 |
| ENT-OM-WILAYA-0205 | ثمريت | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Thumrait under Dhofar; reconciled code 0205 |
| ENT-OM-WILAYA-0206 | ضلكوت | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Dhalkut under Dhofar; reconciled code 0206 |
| ENT-OM-WILAYA-0207 | المزيونة | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Al Mazyunah under Dhofar; reconciled code 0207 |
| ENT-OM-WILAYA-0208 | مقشن | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Muqshin under Dhofar; reconciled code 0208 |
| ENT-OM-WILAYA-0209 | شليم وجزر الحلانيات | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Shalim and the Hallaniyat Islands under Dhofar; reconciled code 0209 |
| ENT-OM-WILAYA-0210 | سدح | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Sadah under Dhofar; reconciled code 0210 |
| ENT-OM-WILAYA-0301 | خصب | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Khasab under Musandam; reconciled code 0301 |
| ENT-OM-WILAYA-0302 | دبا | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Dibba under Musandam; reconciled code 0302 |
| ENT-OM-WILAYA-0303 | بخاء | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Bukha under Musandam; reconciled code 0303 |
| ENT-OM-WILAYA-0304 | مدحاء | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Madha under Musandam; reconciled code 0304 |
| ENT-OM-WILAYA-0401 | البريمي | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Al Buraimi under Al Buraimi; reconciled code 0401 |
| ENT-OM-WILAYA-0402 | محضة | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Mahdha under Al Buraimi; reconciled code 0402 |
| ENT-OM-WILAYA-0403 | السنينة | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: As Sunaynah under Al Buraimi; reconciled code 0403 |
| ENT-OM-WILAYA-0501 | نزوى | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Nizwa under Ad Dakhiliyah; reconciled code 0501 |
| ENT-OM-WILAYA-0502 | بهلاء | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Bahla under Ad Dakhiliyah; reconciled code 0502 |
| ENT-OM-WILAYA-0503 | منح | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Manah under Ad Dakhiliyah; reconciled code 0503 |
| ENT-OM-WILAYA-0504 | الحمراء | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Al Hamra under Ad Dakhiliyah; reconciled code 0504 |
| ENT-OM-WILAYA-0505 | أدم | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Adam under Ad Dakhiliyah; reconciled code 0505 |
| ENT-OM-WILAYA-0506 | إزكي | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Izki under Ad Dakhiliyah; reconciled code 0506 |
| ENT-OM-WILAYA-0507 | سمائل | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Samail under Ad Dakhiliyah; reconciled code 0507 |
| ENT-OM-WILAYA-0508 | بدبد | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Bidbid under Ad Dakhiliyah; reconciled code 0508 |
| ENT-OM-WILAYA-0509 | الجبل الأخضر | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Al Jabal Al Akhdar under Ad Dakhiliyah; reconciled code 0509 |
| ENT-OM-WILAYA-0601 | صحار | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Sohar under North Al Batinah; reconciled code 0601 |
| ENT-OM-WILAYA-0602 | شناص | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Shinas under North Al Batinah; reconciled code 0602 |
| ENT-OM-WILAYA-0603 | لوى | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Liwa under North Al Batinah; reconciled code 0603 |
| ENT-OM-WILAYA-0604 | صحم | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Saham under North Al Batinah; reconciled code 0604 |
| ENT-OM-WILAYA-0605 | الخابورة | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Al Khaburah under North Al Batinah; reconciled code 0605 |
| ENT-OM-WILAYA-0606 | السويق | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: As Suwayq under North Al Batinah; reconciled code 0606 |
| ENT-OM-WILAYA-0701 | الرستاق | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Rustaq under South Al Batinah; reconciled code 0701 |
| ENT-OM-WILAYA-0702 | العوابي | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Al Awabi under South Al Batinah; reconciled code 0702 |
| ENT-OM-WILAYA-0703 | نخل | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Nakhal under South Al Batinah; reconciled code 0703 |
| ENT-OM-WILAYA-0704 | وادي المعاول | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Wadi Al Maawil under South Al Batinah; reconciled code 0704 |
| ENT-OM-WILAYA-0705 | بركاء | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Barka under South Al Batinah; reconciled code 0705 |
| ENT-OM-WILAYA-0706 | المصنعة | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Al Musannah under South Al Batinah; reconciled code 0706 |
| ENT-OM-WILAYA-0801 | صور | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Sur under South Ash Sharqiyah; reconciled code 0801 |
| ENT-OM-WILAYA-0802 | الكامل والوافي | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Al Kamil Wal Wafi under South Ash Sharqiyah; reconciled code 0802 |
| ENT-OM-WILAYA-0803 | جعلان بني بو حسن | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Jalan Bani Bu Hassan under South Ash Sharqiyah; reconciled code 0803 |
| ENT-OM-WILAYA-0804 | جعلان بني بو علي | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Jalan Bani Bu Ali under South Ash Sharqiyah; reconciled code 0804 |
| ENT-OM-WILAYA-0805 | مصيرة | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Masirah under South Ash Sharqiyah; reconciled code 0805 |
| ENT-OM-WILAYA-0901 | إبراء | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Ibra under North Ash Sharqiyah; reconciled code 0901 |
| ENT-OM-WILAYA-0902 | المضيبي | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Al Mudhaibi under North Ash Sharqiyah; reconciled code 0902 |
| ENT-OM-WILAYA-0903 | بدية | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Bidiyah under North Ash Sharqiyah; reconciled code 0903 |
| ENT-OM-WILAYA-0904 | القابل | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Al Qabil under North Ash Sharqiyah; reconciled code 0904 |
| ENT-OM-WILAYA-0905 | وادي بني خالد | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Wadi Bani Khalid under North Ash Sharqiyah; reconciled code 0905 |
| ENT-OM-WILAYA-0906 | دماء والطائيين | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Dema and Al Tayeen under North Ash Sharqiyah; reconciled code 0906 |
| ENT-OM-WILAYA-0907 | سناو | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Sinaw under North Ash Sharqiyah; reconciled code 0907 |
| ENT-OM-WILAYA-1001 | عبري | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Ibri under Adh Dhahirah; reconciled code 1001 |
| ENT-OM-WILAYA-1002 | ينقل | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Yanqul under Adh Dhahirah; reconciled code 1002 |
| ENT-OM-WILAYA-1003 | ضنك | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Dhank under Adh Dhahirah; reconciled code 1003 |
| ENT-OM-WILAYA-1101 | هيماء | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Haima under Al Wusta; reconciled code 1101 |
| ENT-OM-WILAYA-1102 | محوت | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Mahout under Al Wusta; reconciled code 1102 |
| ENT-OM-WILAYA-1103 | الدقم | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Duqm under Al Wusta; reconciled code 1103 |
| ENT-OM-WILAYA-1104 | الجازر | om_wilaya | current | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2: Al Jazir under Al Wusta; reconciled code 1104 |

## الأسماء البديلة

| المعرّف | الكيان | الاسم | اللغة | النوع | المصدر |
|---|---|---|---|---|---|
| ALS-OM-0094D1D81DDA5940 | ENT-OM-WILAYA-0103 | Al Amerat | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-041EF3E50E405F31 | ENT-OM-WILAYA-0403 | As Sunaynah | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-08330D879F355BBC | ENT-OM-WILAYA-0302 | Dibba | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-0CE5A28E737F5C64 | ENT-OM-WILAYA-0105 | As Seeb | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-11BDEFDE28685C2B | ENT-OM-WILAYA-0209 | Shalim and the Hallaniyat Islands | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-14782C197EBC5E07 | ENT-OM-WILAYA-0603 | Liwa | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-16C4CCDD2F015134 | ENT-OM-GOVERNORATE-03 | Musandam | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-1D28296DCBB8597A | ENT-OM-GOVERNORATE-04 | Al Buraimi | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-217AB96C17DF59A4 | ENT-OM-WILAYA-0601 | Sohar | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-224505DCF329564A | ENT-OM-WILAYA-0606 | As Suwayq | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-25A30F65320152B9 | ENT-OM-WILAYA-0207 | Al Mazyunah | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-2DEA20ACD0635113 | ENT-OM-GOVERNORATE-01 | Muscat | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-3606D532F2A35A8F | ENT-OM-WILAYA-0208 | Muqshin | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-360D31CB70815FBB | ENT-OM-GOVERNORATE-09 | North Ash Sharqiyah | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-36AF4C3C290A5550 | ENT-OM-GOVERNORATE-06 | North Al Batinah | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-382C6DA157D45A81 | ENT-OM-WILAYA-0401 | Al Buraimi | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-3ECD2F4EF59E5D31 | ENT-OM-WILAYA-0206 | Dhalkut | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-4119C5C973B852D1 | ENT-OM-WILAYA-0102 | Muttrah | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-426938F878DA5948 | ENT-OM-WILAYA-0204 | Rakhyut | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-440FC26A297D537F | ENT-OM-GOVERNORATE-10 | Adh Dhahirah | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-472A63CF512A521A | ENT-OM-WILAYA-0903 | Bidiyah | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-49F16AAE07EC5585 | ENT-OM-WILAYA-1103 | Duqm | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-4B62C1A33F155BC3 | ENT-OM-WILAYA-0505 | Adam | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-5215B0FAB0215FC5 | ENT-OM-WILAYA-0704 | Wadi Al Maawil | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-55190F795A94563B | ENT-OM-WILAYA-0904 | Al Qabil | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-56FE20F9331552AF | ENT-OM-WILAYA-0805 | Masirah | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-5F639F4ABDB05BC3 | ENT-OM-GOVERNORATE-08 | South Ash Sharqiyah | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-6239124D4F005611 | ENT-OM-WILAYA-0905 | Wadi Bani Khalid | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-64AF293D66965A44 | ENT-OM-WILAYA-1003 | Dhank | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-65D13838C30C5D20 | ENT-OM-WILAYA-0303 | Bukha | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-66EBD0E6443458FF | ENT-OM-WILAYA-0804 | Jalan Bani Bu Ali | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-67B617BB4B10545D | ENT-OM-WILAYA-0502 | Bahla | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-6892DC4869535B9C | ENT-OM-WILAYA-0205 | Thumrait | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-6AA74FAEB63B5B38 | ENT-OM-WILAYA-0706 | Al Musannah | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-6D109E77DAE7568B | ENT-OM-WILAYA-0202 | Taqah | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-6D8A52E2C999536B | ENT-OM-WILAYA-1002 | Yanqul | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-6F35FF4256F05A2A | ENT-OM-WILAYA-0106 | Qurayyat | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-71632B82DA285483 | ENT-OM-WILAYA-0507 | Samail | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-746605A14FF056AF | ENT-OM-WILAYA-1101 | Haima | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-754CB134B2B7535B | ENT-OM-WILAYA-0301 | Khasab | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-75E78AB4C85F5B44 | ENT-OM-WILAYA-0501 | Nizwa | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-7B85529EE19C5B25 | ENT-OM-WILAYA-0304 | Madha | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-8257E7A46549540B | ENT-OM-WILAYA-0506 | Izki | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-88D36DEDAF4356D5 | ENT-OM-WILAYA-0906 | Dema and Al Tayeen | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-8DEA078A092D5B28 | ENT-OM-WILAYA-0902 | Al Mudhaibi | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-8F4B109A4F3151AD | ENT-OM-WILAYA-1001 | Ibri | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-950FFE1D7081516B | ENT-OM-WILAYA-0705 | Barka | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-966AE25DAB84529D | ENT-OM-WILAYA-0201 | Salalah | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-A280706FAEC75045 | ENT-OM-WILAYA-0104 | Bawshar | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-A4069510FE725E5C | ENT-OM-WILAYA-0605 | Al Khaburah | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-A531B86FCC99533B | ENT-OM-WILAYA-0801 | Sur | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-AAB04F72E549594D | ENT-OM-WILAYA-0503 | Manah | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-ACFCD5FA45845AF6 | ENT-OM-GOVERNORATE-11 | Al Wusta | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-AD37FB58B931597D | ENT-OM-GOVERNORATE-02 | Dhofar | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-AF85AC1355F45FAA | ENT-OM-WILAYA-0907 | Sinaw | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-B74962F35B8E5F47 | ENT-OM-WILAYA-0803 | Jalan Bani Bu Hassan | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-BD2770C813575E90 | ENT-OM-WILAYA-0602 | Shinas | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-BEE366008AEC5CCC | ENT-OM-WILAYA-0701 | Rustaq | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-C512FCBC4FB357A9 | ENT-OM-WILAYA-0703 | Nakhal | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-C9E66025D79859C2 | ENT-OM-WILAYA-1102 | Mahout | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-CA9E6EB0A1065A51 | ENT-OM-WILAYA-0802 | Al Kamil Wal Wafi | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-CC9380B4F0885667 | ENT-OM-WILAYA-0901 | Ibra | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-D69144B690DF506D | ENT-OM-GOVERNORATE-05 | Ad Dakhiliyah | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-D78C3CAB59FE53B9 | ENT-OM-WILAYA-0508 | Bidbid | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-D86AB5D4B2B2517F | ENT-OM-WILAYA-0210 | Sadah | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-DA63978DE4565A8B | ENT-OM-GOVERNORATE-07 | South Al Batinah | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-DF2B075CFEE6530E | ENT-OM-WILAYA-0604 | Saham | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-E033ED4A30E15EDF | ENT-OM-WILAYA-0101 | Muscat | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-E1EF903980CF5601 | ENT-OM-WILAYA-0504 | Al Hamra | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-E35BCED79E165C24 | ENT-OM-WILAYA-1104 | Al Jazir | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-E8110627B9E85A5F | ENT-OM-WILAYA-0702 | Al Awabi | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-F5DBC805252C5D3A | ENT-OM-WILAYA-0402 | Mahdha | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-F781498062BD5F11 | ENT-OM-WILAYA-0203 | Mirbat | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |
| ALS-OM-F8CF0451E4E25953 | ENT-OM-WILAYA-0509 | Al Jabal Al Akhdar | en | official_variant | SRC-OM-RD-36-2022-GOVERNORATES |

## علاقات الإدارة/الموقع

| المعرّف | الابن | الأب | العلاقة | الحالة | المصدر |
|---|---|---|---|---|---|
| REL-OM-00663C7AAA195524 | ENT-OM-WILAYA-0303 | ENT-OM-GOVERNORATE-03 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-040A9D5E0337519A | ENT-OM-GOVERNORATE-06 | ENT-OM-COUNTRY | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-0ED70EB3A6575F4F | ENT-OM-WILAYA-0208 | ENT-OM-GOVERNORATE-02 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-0FCE09A776455C5B | ENT-OM-WILAYA-0803 | ENT-OM-GOVERNORATE-08 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-191900108B775694 | ENT-OM-WILAYA-0402 | ENT-OM-GOVERNORATE-04 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-1FE3504CF8535449 | ENT-OM-GOVERNORATE-07 | ENT-OM-COUNTRY | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-221E9F72C5475487 | ENT-OM-WILAYA-0602 | ENT-OM-GOVERNORATE-06 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-250944F6714E580C | ENT-OM-WILAYA-0210 | ENT-OM-GOVERNORATE-02 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-27F848EA5BC25AE4 | ENT-OM-WILAYA-1002 | ENT-OM-GOVERNORATE-10 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-29D6485CF03B5F12 | ENT-OM-WILAYA-0902 | ENT-OM-GOVERNORATE-09 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-2AD6F1E951F85732 | ENT-OM-WILAYA-0203 | ENT-OM-GOVERNORATE-02 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-2C1E6A7CCD0F50DF | ENT-OM-WILAYA-0904 | ENT-OM-GOVERNORATE-09 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-3416A9D5BDDD57B9 | ENT-OM-WILAYA-0105 | ENT-OM-GOVERNORATE-01 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-353DB3E4A7395291 | ENT-OM-WILAYA-0201 | ENT-OM-GOVERNORATE-02 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-3B48369326F85699 | ENT-OM-GOVERNORATE-01 | ENT-OM-COUNTRY | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-3B7F41FC85385462 | ENT-OM-GOVERNORATE-08 | ENT-OM-COUNTRY | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-3DB44D7DB62C5012 | ENT-OM-GOVERNORATE-09 | ENT-OM-COUNTRY | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-3DE81440C9495E33 | ENT-OM-WILAYA-0302 | ENT-OM-GOVERNORATE-03 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-40567F9445085E9A | ENT-OM-WILAYA-0506 | ENT-OM-GOVERNORATE-05 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-40B681ACE14C5EB8 | ENT-OM-WILAYA-0601 | ENT-OM-GOVERNORATE-06 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-40B9E762E6025AA6 | ENT-OM-WILAYA-0206 | ENT-OM-GOVERNORATE-02 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-47CC75FB858A5EE3 | ENT-OM-WILAYA-1003 | ENT-OM-GOVERNORATE-10 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-587ABC6A554F5F35 | ENT-OM-WILAYA-0301 | ENT-OM-GOVERNORATE-03 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-5D10F06512F65040 | ENT-OM-WILAYA-0501 | ENT-OM-GOVERNORATE-05 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-6084BA2BE1FE5E66 | ENT-OM-WILAYA-0706 | ENT-OM-GOVERNORATE-07 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-62060B91EBCA5F7B | ENT-OM-GOVERNORATE-05 | ENT-OM-COUNTRY | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-6678C99F0402589D | ENT-OM-WILAYA-1104 | ENT-OM-GOVERNORATE-11 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-6A21802ECBF05843 | ENT-OM-WILAYA-0508 | ENT-OM-GOVERNORATE-05 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-6AA4F3E188B55CC8 | ENT-OM-WILAYA-0202 | ENT-OM-GOVERNORATE-02 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-6B1472E594C45D16 | ENT-OM-WILAYA-0104 | ENT-OM-GOVERNORATE-01 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-6B7EDAC99A8C5FC5 | ENT-OM-WILAYA-0209 | ENT-OM-GOVERNORATE-02 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-6DC0950E7D1A51E0 | ENT-OM-WILAYA-0603 | ENT-OM-GOVERNORATE-06 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-6FD88CF9926A5071 | ENT-OM-WILAYA-0804 | ENT-OM-GOVERNORATE-08 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-7472EFE080A55708 | ENT-OM-WILAYA-0907 | ENT-OM-GOVERNORATE-09 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-7515A1994ED05A73 | ENT-OM-WILAYA-0604 | ENT-OM-GOVERNORATE-06 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-771E9F704A155DAD | ENT-OM-WILAYA-0204 | ENT-OM-GOVERNORATE-02 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-787B01C456FA5E21 | ENT-OM-WILAYA-0903 | ENT-OM-GOVERNORATE-09 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-7E6363DA02A3508B | ENT-OM-WILAYA-0801 | ENT-OM-GOVERNORATE-08 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-7E7D1A485EFD546E | ENT-OM-WILAYA-0504 | ENT-OM-GOVERNORATE-05 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-87F151BDDFDC5A4C | ENT-OM-WILAYA-0705 | ENT-OM-GOVERNORATE-07 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-88058A9BDD255844 | ENT-OM-GOVERNORATE-11 | ENT-OM-COUNTRY | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-8990C035ED805616 | ENT-OM-WILAYA-0505 | ENT-OM-GOVERNORATE-05 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-8EA2BB001328530E | ENT-OM-WILAYA-0507 | ENT-OM-GOVERNORATE-05 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-9409394F411A5BD2 | ENT-OM-WILAYA-0802 | ENT-OM-GOVERNORATE-08 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-95DC106A5A2752F8 | ENT-OM-WILAYA-0901 | ENT-OM-GOVERNORATE-09 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-98C14D7CD8AE5C62 | ENT-OM-WILAYA-1101 | ENT-OM-GOVERNORATE-11 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-9B5923E834CF563C | ENT-OM-WILAYA-0401 | ENT-OM-GOVERNORATE-04 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-9E1880D5114D5344 | ENT-OM-WILAYA-1102 | ENT-OM-GOVERNORATE-11 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-A0C156C97B4A5ED2 | ENT-OM-WILAYA-0103 | ENT-OM-GOVERNORATE-01 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-A2B8F3A539285877 | ENT-OM-WILAYA-0906 | ENT-OM-GOVERNORATE-09 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-A3C235C42E3C5767 | ENT-OM-WILAYA-0702 | ENT-OM-GOVERNORATE-07 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-A84EE0C8CA2257E0 | ENT-OM-WILAYA-1001 | ENT-OM-GOVERNORATE-10 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-A88ED615AB50565F | ENT-OM-WILAYA-0502 | ENT-OM-GOVERNORATE-05 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-AA94AE44E1AE5643 | ENT-OM-WILAYA-0205 | ENT-OM-GOVERNORATE-02 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-AB6786766B0D53C9 | ENT-OM-WILAYA-0606 | ENT-OM-GOVERNORATE-06 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-AC991777D72A525E | ENT-OM-WILAYA-0106 | ENT-OM-GOVERNORATE-01 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-AFF45FA9052C5D92 | ENT-OM-WILAYA-0905 | ENT-OM-GOVERNORATE-09 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-B189069F047759AE | ENT-OM-GOVERNORATE-03 | ENT-OM-COUNTRY | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-BAAB3550C8D553A7 | ENT-OM-GOVERNORATE-04 | ENT-OM-COUNTRY | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-C08F7B37CF385EB6 | ENT-OM-WILAYA-0304 | ENT-OM-GOVERNORATE-03 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-C44EAD94885E503B | ENT-OM-WILAYA-0503 | ENT-OM-GOVERNORATE-05 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-C7AAEE1209715DBD | ENT-OM-WILAYA-0701 | ENT-OM-GOVERNORATE-07 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-CDF8587A72845AAE | ENT-OM-WILAYA-0805 | ENT-OM-GOVERNORATE-08 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-D4502E21231556FD | ENT-OM-WILAYA-1103 | ENT-OM-GOVERNORATE-11 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-D7B0973CC2475AAE | ENT-OM-WILAYA-0101 | ENT-OM-GOVERNORATE-01 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-DBD9CB0EDD125F4B | ENT-OM-WILAYA-0605 | ENT-OM-GOVERNORATE-06 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-DC4122C619AE5067 | ENT-OM-WILAYA-0703 | ENT-OM-GOVERNORATE-07 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-E92B651E84F854B5 | ENT-OM-WILAYA-0102 | ENT-OM-GOVERNORATE-01 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-ECDDF1A274B852CD | ENT-OM-GOVERNORATE-10 | ENT-OM-COUNTRY | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-EF95C0AA1FA55B1D | ENT-OM-WILAYA-0704 | ENT-OM-GOVERNORATE-07 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-F09CFF8962EF5F1A | ENT-OM-WILAYA-0207 | ENT-OM-GOVERNORATE-02 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-F5BDD5E307FF57BB | ENT-OM-GOVERNORATE-02 | ENT-OM-COUNTRY | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-F7460886A1F1541F | ENT-OM-WILAYA-0509 | ENT-OM-GOVERNORATE-05 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |
| REL-OM-FFE118402F305B0C | ENT-OM-WILAYA-0403 | ENT-OM-GOVERNORATE-04 | administrative_parent | current | SRC-OM-RD-36-2022-GOVERNORATES |

## الادعاءات

| المعرّف | الموضوع | المحمول | القيمة | التصنيف | الثقة | الحالة | المصدر | المحدد |
|---|---|---|---|---|---|---|---|---|
| CLM-OM-0A8F1406D594597C | ENT-OM-GOVERNORATE-07 | wilayat_count | 6 | official | high | verified | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 07: South Al Batinah; 6 wilayats |
| CLM-OM-2EB8D4B278BC5DE8 | ENT-OM-GOVERNORATE-09 | wilayat_count | 7 | official | high | verified | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 09: North Ash Sharqiyah; 7 wilayats |
| CLM-OM-3B4A5C02B3FD5942 | ENT-OM-GOVERNORATE-08 | wilayat_count | 5 | official | high | verified | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 08: South Ash Sharqiyah; 5 wilayats |
| CLM-OM-50D028A978E75EC3 | ENT-OM-GOVERNORATE-11 | wilayat_count | 4 | official | high | verified | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 11: Al Wusta; 4 wilayats |
| CLM-OM-57629791149450E7 | ENT-OM-GOVERNORATE-03 | wilayat_count | 4 | official | high | verified | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 03: Musandam; 4 wilayats |
| CLM-OM-677017AC3DEE5B74 | ENT-OM-GOVERNORATE-01 | wilayat_count | 6 | official | high | verified | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 01: Muscat; 6 wilayats |
| CLM-OM-980ACCE3D407538A | ENT-OM-GOVERNORATE-06 | wilayat_count | 6 | official | high | verified | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 06: North Al Batinah; 6 wilayats |
| CLM-OM-AA337F02973E5551 | ENT-OM-GOVERNORATE-05 | wilayat_count | 9 | official | high | verified | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 05: Ad Dakhiliyah; 9 wilayats |
| CLM-OM-AC18B9BF672B5C24 | ENT-OM-GOVERNORATE-02 | wilayat_count | 10 | official | high | verified | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 02: Dhofar; 10 wilayats |
| CLM-OM-CCAD876FB17D5774 | ENT-OM-GOVERNORATE-04 | wilayat_count | 3 | official | high | verified | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 04: Al Buraimi; 3 wilayats |
| CLM-OM-D1C6158D0B495B02 | ENT-OM-GOVERNORATE-10 | wilayat_count | 3 | official | high | verified | SRC-OM-RD-36-2022-GOVERNORATES | Decree Article 2 governorate 10: Adh Dhahirah; 3 wilayats |

## جودة مصادر الادعاءات المنشورة

ادعاءات A/B: 11 من 11 (100.00%).

## المصادر الذرية المستخدمة

| المعرّف | الفئة | العنوان | الناشر | تاريخ النشر | تاريخ الاسترجاع | الترخيص | الرابط |
|---|---|---|---|---|---|---|---|
| SRC-ISO-3166-1-2020 | A | ISO 3166-1:2020 — Codes for the representation of names of countries and their subdivisions — Part 1: Country code | International Organization for Standardization (ISO) | 2020-08 | 2026-08-15 | ISO copyright; reuse is subject to ISO terms of use | https://www.iso.org/obp/ui/#iso:std:iso:3166:-1:ed-4:v1:en |
| SRC-OM-RD-36-2022-GOVERNORATES | A | Royal Decree 36/2022 — Governorates System | Sultanate of Oman / Official Gazette | 2022-06-16 | 2026-08-16 | Official Oman legal/statistical material; factual extraction with attribution; reuse terms not stated | https://bur.gov.om/assets/pdf/en/governorate-system.pdf |

---
_مولّد آليًا؛ لا تعدّل هذا الملف مباشرة._
