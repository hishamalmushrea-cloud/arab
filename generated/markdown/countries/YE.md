# اليمن (YE) — عرض مولّد من Schema 2.0.0

> **حدود التغطية:** التغطية المحلية غير مكتملة. لا تمثل هذه الصفحة جميع المدن أو القرى أو الأحياء أو الحارات، ولا يُستدل على التغطية من وجود ملف. البيانات المنظمة هي المصدر؛ هذه الصفحة عرض مولّد.

## التغطية والمقامات

أي نسبة 100% أدناه مقيدة بالدولة والطبقة والمقام المؤرخ واللقطة والمصدر الظاهرة في الصف نفسه؛ ولا تمتد إلى طبقة أخرى.

| الطبقة | تعريف المقام | المقام | مطابق | غير مطابق | مستبعد | مفقود | النسبة | تاريخ اللقطة | اللقطة | المصدر | الترخيص | مكتمل | سبب النقص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ye_amanat_lane_2004 | Amanat Al Asimah lane universe: 791 lanes across 10 districts plus two suburb blocks under the NIC census-2004 frame; 104 lane identities attested (Old Sanaa 69, Tahrir 35); the remaining 687 lanes are an open documented frame. | 791 | 104 | 687 | 0 | 687 | 13.15% | 2026-08-17 | SNP-YE-PRODUCTION-20260817 | SRC-YE-NIC-AMANAT-CENSUS-2004 | Factual extraction with attribution; publisher reuse terms not stated | لا | lane_inventories_not_yet_reconciled: per-district lane name tables for the remaining eight districts and two suburb blocks are attested to exist in the 2004 census frame but are not yet retrieved; no name is fabricated |
| ye_capital_municipality_current | Amanat Al Asimah is one parallel first-level capital municipality. | 1 | 1 | 0 | 0 | 0 | 100% | 2026-08-17 | SNP-YE-PRODUCTION-20260817 | SRC-YE-NIC-GOVERNORATES-LEGACY | Factual extraction with attribution; publisher reuse terms not stated | نعم | — |
| country_scope | ISO country entity in the project's 22-country scope | 1 | 1 | 0 | 0 | 0 | 100% | 2026-08-15 | SNP-MIGRATION-2026-08-15 | SRC-ISO-3166-1-2020 | ISO copyright; reuse is subject to ISO terms of use | نعم | — |
| ye_district_current | National 333-district frame from the archived official CSO administrative-definitions page; identities attested via the NIC catalogue mirror and carry probable status pending an atomic official coded register. | 333 | 333 | 0 | 0 | 0 | 100% | 2026-08-17 | SNP-YE-PRODUCTION-20260817 | SRC-YE-CENSUS-2004-LEGACY-FRAME | Factual extraction with attribution; publisher reuse terms not stated | نعم | — |
| ye_first_level_current | Reconciled legal universe: legacy 21 plus Socotra under Law 31/2013. | 22 | 22 | 0 | 0 | 0 | 100% | 2026-08-17 | SNP-YE-PRODUCTION-20260817 | SRC-YE-LAW-31-SOCOTRA-REPORT-2013 | Factual extraction with attribution; publisher reuse terms not stated | نعم | — |
| ye_governorate_current | Twenty legacy governorates plus Socotra; excludes Amanat Al Asimah. | 21 | 21 | 0 | 0 | 0 | 100% | 2026-08-17 | SNP-YE-PRODUCTION-20260817 | SRC-YE-LAW-31-SOCOTRA-REPORT-2013 | Factual extraction with attribution; publisher reuse terms not stated | نعم | — |
| ye_first_level_legacy_pre_socotra | Historical source frame: 20 governorates plus Capital Municipality; Socotra absent. | 21 | 21 | 0 | 0 | 0 | 100% | 2026-08-17 | SNP-YE-PRODUCTION-20260817 | SRC-YE-CSO-ADMIN-DEFINITION-LEGACY | Factual extraction with attribution; publisher reuse terms not stated | نعم | — |

## الكيانات

| المعرّف | الاسم | النوع | الحالة | المصدر القانوني/المرجعي | المحدد داخل المصدر |
|---|---|---|---|---|---|
| ENT-YE-CAPITAL-MUNICIPALITY-01 | أمانة العاصمة | ye_capital_municipality | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: أمانة العاصمة |
| ENT-YE-COUNTRY | اليمن | country | current | SRC-ISO-3166-1-2020 | ISO alpha-2 entry YE |
| ENT-YE-DISTRICT-033FEF147059 | حريب | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate مأرب: حريب |
| ENT-YE-DISTRICT-0433DE028E03 | تريم | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: تريم |
| ENT-YE-DISTRICT-05072004A1BE | الطيال | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صنعاء: الطيال |
| ENT-YE-DISTRICT-065D10E84F28 | المتون | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الجوف: المتون |
| ENT-YE-DISTRICT-06EE7480D08D | كحلان عفار | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: كحلان عفار |
| ENT-YE-DISTRICT-07D021680938 | صعفان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صنعاء: صعفان |
| ENT-YE-DISTRICT-0918A396268C | الحميدات | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الجوف: الحميدات |
| ENT-YE-DISTRICT-0931C242D57C | المغربة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: المغربة |
| ENT-YE-DISTRICT-0A309AF13104 | كحلان الشرف | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: كحلان الشرف |
| ENT-YE-DISTRICT-0A49FF236843 | عنس | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ذمار: عنس |
| ENT-YE-DISTRICT-0B501AB3B00D | القناوص | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: القناوص |
| ENT-YE-DISTRICT-0C80320ECE5F | ميفعة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate شبوة: ميفعة |
| ENT-YE-DISTRICT-0D0A5492DA68 | صنعاء القديمة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أمانة العاصمة: صنعاء القديمة |
| ENT-YE-DISTRICT-0E3A8FC6CC9C | الجوبة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate مأرب: الجوبة |
| ENT-YE-DISTRICT-0F3C31473843 | خب والشعف | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الجوف: خب والشعف |
| ENT-YE-DISTRICT-0F4FEB79DB77 | المعافر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: المعافر |
| ENT-YE-DISTRICT-0F723F77FC89 | باقم | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صعدة: باقم |
| ENT-YE-DISTRICT-0FB5E523A676 | مجز | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صعدة: مجز |
| ENT-YE-DISTRICT-104F8DEB7391 | الرضمة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: الرضمة |
| ENT-YE-DISTRICT-10FD63FD9C4E | القبيطة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate لحج: القبيطة |
| ENT-YE-DISTRICT-12BC71EC7FE7 | يهر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate لحج: يهر |
| ENT-YE-DISTRICT-13F900E880AE | ضوران أنس | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ذمار: ضوران أنس |
| ENT-YE-DISTRICT-14DB253EFEEC | أزال | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أمانة العاصمة: أزال |
| ENT-YE-DISTRICT-14F726E0F79B | رازح | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صعدة: رازح |
| ENT-YE-DISTRICT-1626EA2FDE59 | مأرب الوادي | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate مأرب: مأرب الوادي |
| ENT-YE-DISTRICT-165FE8764D7C | صوير | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: صوير |
| ENT-YE-DISTRICT-16A786CA1AB5 | مدغل الجدعان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate مأرب: مدغل الجدعان |
| ENT-YE-DISTRICT-16B2C03EFD2F | نجرة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: نجرة |
| ENT-YE-DISTRICT-1A140B15A926 | الحصن | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صنعاء: الحصن |
| ENT-YE-DISTRICT-1C2D2568B2F5 | حجة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: حجة |
| ENT-YE-DISTRICT-1D133E1F36EE | المسيمير | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate لحج: المسيمير |
| ENT-YE-DISTRICT-1D9E23C30969 | ماهلية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate مأرب: ماهلية |
| ENT-YE-DISTRICT-1DC1BF36340C | المضاربة والعارة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate لحج: المضاربة والعارة |
| ENT-YE-DISTRICT-1DC8CC6E5663 | الشيخ عثمان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عدن: الشيخ عثمان |
| ENT-YE-DISTRICT-1E779AE3FA2C | اللحية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: اللحية |
| ENT-YE-DISTRICT-1FD28938AA85 | حطيب | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate شبوة: حطيب |
| ENT-YE-DISTRICT-21776B6BC7C0 | أرحب | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صنعاء: أرحب |
| ENT-YE-DISTRICT-2200C6BC9A3B | الحشاء | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الضالع: الحشاء |
| ENT-YE-DISTRICT-2314C712E180 | المفتاح | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: المفتاح |
| ENT-YE-DISTRICT-23C2ED53561D | حرض | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: حرض |
| ENT-YE-DISTRICT-23CDC8A23150 | بكيل المير | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: بكيل المير |
| ENT-YE-DISTRICT-25A23003C30E | القطن | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: القطن |
| ENT-YE-DISTRICT-25DEBC9F4331 | رضوم | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate شبوة: رضوم |
| ENT-YE-DISTRICT-25FC82D1C847 | حبان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate شبوة: حبان |
| ENT-YE-DISTRICT-2776D12E3A5A | ظليمة حبور | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: ظليمة حبور |
| ENT-YE-DISTRICT-292F5EBF6255 | رخية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: رخية |
| ENT-YE-DISTRICT-294CCD62A649 | دمت | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الضالع: دمت |
| ENT-YE-DISTRICT-2C424C87C3BE | نهم | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صنعاء: نهم |
| ENT-YE-DISTRICT-2CB5A0681CCB | بلاد الروس | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صنعاء: بلاد الروس |
| ENT-YE-DISTRICT-2D0F0D552D30 | الحزم | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الجوف: الحزم |
| ENT-YE-DISTRICT-2D9751BEFD41 | الصومعة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: الصومعة |
| ENT-YE-DISTRICT-2EA5F8194AE6 | دهر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate شبوة: دهر |
| ENT-YE-DISTRICT-2F724D7BA06B | ذيبين | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: ذيبين |
| ENT-YE-DISTRICT-2FAA44D3AC59 | حبيش | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: حبيش |
| ENT-YE-DISTRICT-3095B13BD169 | العدين | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: العدين |
| ENT-YE-DISTRICT-30DAD3916C7F | صيرة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عدن: صيرة |
| ENT-YE-DISTRICT-30E672BCD16C | شبام كوكبان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المحويت: شبام كوكبان |
| ENT-YE-DISTRICT-31B68AB824FB | حريضة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: حريضة |
| ENT-YE-DISTRICT-32589B7B0574 | الوحدة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أمانة العاصمة: الوحدة |
| ENT-YE-DISTRICT-32BF31B664DD | فرع العدين | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: فرع العدين |
| ENT-YE-DISTRICT-33BD3C230D4D | ذباب | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: ذباب |
| ENT-YE-DISTRICT-343E52EBFF3E | سيئون | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: سيئون |
| ENT-YE-DISTRICT-352DD2903C6B | سحار | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صعدة: سحار |
| ENT-YE-DISTRICT-35494423C71B | ردفان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate لحج: ردفان |
| ENT-YE-DISTRICT-3578EDCD8379 | كمران | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: كمران |
| ENT-YE-DISTRICT-35AEF4E9A32F | صباح | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: صباح |
| ENT-YE-DISTRICT-3691E8E68566 | سامع | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: سامع |
| ENT-YE-DISTRICT-372E17209D86 | مرخة السفلى | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate شبوة: مرخة السفلى |
| ENT-YE-DISTRICT-376C1EFDE465 | الطلح | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate شبوة: الطلح |
| ENT-YE-DISTRICT-39E111D17A62 | عسيلان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate شبوة: عسيلان |
| ENT-YE-DISTRICT-39E8FCE337F8 | الصليف | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: الصليف |
| ENT-YE-DISTRICT-3B5EACB6791E | الرياشية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: الرياشية |
| ENT-YE-DISTRICT-3BE7603D86AA | حجر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: حجر |
| ENT-YE-DISTRICT-3C88F00E0434 | وصاب العالي | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ذمار: وصاب العالي |
| ENT-YE-DISTRICT-3F2CDF08FF59 | صرواح | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate مأرب: صرواح |
| ENT-YE-DISTRICT-3F95B5A1F5BF | الظاهر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صعدة: الظاهر |
| ENT-YE-DISTRICT-3FD301BC5889 | عتق | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate شبوة: عتق |
| ENT-YE-DISTRICT-42B7313C7FBC | العبر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: العبر |
| ENT-YE-DISTRICT-4340895CDA75 | حورة ووادي العين | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: حورة ووادي العين |
| ENT-YE-DISTRICT-446ED56B418D | رماه | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: رماه |
| ENT-YE-DISTRICT-451865966A05 | الجميمة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: الجميمة |
| ENT-YE-DISTRICT-46EDAA04F1E4 | مبين | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: مبين |
| ENT-YE-DISTRICT-4956B0EDBB4F | المحفد | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أبين: المحفد |
| ENT-YE-DISTRICT-49A67B33D4F6 | أسلم | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: أسلم |
| ENT-YE-DISTRICT-4AA53C0EC80A | الصافية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أمانة العاصمة: الصافية |
| ENT-YE-DISTRICT-4B0908476AEB | ساه | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: ساه |
| ENT-YE-DISTRICT-4BA89AD1F972 | خيران المحرق | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: خيران المحرق |
| ENT-YE-DISTRICT-4C439AF1AFB0 | غيل باوزير | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: غيل باوزير |
| ENT-YE-DISTRICT-4D33D22350C1 | الحيمة الخارجية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صنعاء: الحيمة الخارجية |
| ENT-YE-DISTRICT-4EF0E76CBCBE | جهران | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ذمار: جهران |
| ENT-YE-DISTRICT-4F5F82AB5A4B | المنصورة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عدن: المنصورة |
| ENT-YE-DISTRICT-5018BFC1B1CD | حيس | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: حيس |
| ENT-YE-DISTRICT-51FD6B9DA297 | الزهرة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: الزهرة |
| ENT-YE-DISTRICT-52D0EDBD39F9 | الخبت | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المحويت: الخبت |
| ENT-YE-DISTRICT-53046A0ECF0A | المطمة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الجوف: المطمة |
| ENT-YE-DISTRICT-534C0BB78FAF | حريب القرامش | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate مأرب: حريب القرامش |
| ENT-YE-DISTRICT-542E3C3E2498 | لودر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أبين: لودر |
| ENT-YE-DISTRICT-547879558CC8 | مدينة المحويت | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المحويت: مدينة المحويت |
| ENT-YE-DISTRICT-553E34DD89E5 | كشر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: كشر |
| ENT-YE-DISTRICT-56AC99FF49C5 | بني صريم | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: بني صريم |
| ENT-YE-DISTRICT-56B913F53DDF | يافع | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate لحج: يافع |
| ENT-YE-DISTRICT-5874DE54BE90 | ساقين | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صعدة: ساقين |
| ENT-YE-DISTRICT-588D6221966A | حفاش | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المحويت: حفاش |
| ENT-YE-DISTRICT-598617DCC9E2 | السبرة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: السبرة |
| ENT-YE-DISTRICT-5A842A6DBAA5 | سنحان وبني بهلول | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صنعاء: سنحان وبني بهلول |
| ENT-YE-DISTRICT-5A9F2A23F434 | مغرب عنس | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ذمار: مغرب عنس |
| ENT-YE-DISTRICT-5AF8EE7DF37B | مدينة البيضاء | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: مدينة البيضاء |
| ENT-YE-DISTRICT-5B193F871C0B | الضليعة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: الضليعة |
| ENT-YE-DISTRICT-5B3DC69A6DAA | الزيدية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: الزيدية |
| ENT-YE-DISTRICT-5B7E0D3911E9 | كسمة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ريمة: كسمة |
| ENT-YE-DISTRICT-5BAC2FFCE67A | بني حشيش | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صنعاء: بني حشيش |
| ENT-YE-DISTRICT-5C351EFED33D | رجوزة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الجوف: رجوزة |
| ENT-YE-DISTRICT-5DD68C44EA2D | صبر الموادم | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: صبر الموادم |
| ENT-YE-DISTRICT-61CFCDE24752 | صالة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: صالة |
| ENT-YE-DISTRICT-6226424AD261 | السدة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: السدة |
| ENT-YE-DISTRICT-6310172A6217 | الميناء | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: الميناء |
| ENT-YE-DISTRICT-63A390C4F786 | الوضيع | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أبين: الوضيع |
| ENT-YE-DISTRICT-63BB7185E88A | صعدة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صعدة: صعدة |
| ENT-YE-DISTRICT-6460ADF1477D | التحيتا | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: التحيتا |
| ENT-YE-DISTRICT-646E3ADBE273 | الصفراء | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صعدة: الصفراء |
| ENT-YE-DISTRICT-65071A18A413 | شهارة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: شهارة |
| ENT-YE-DISTRICT-650F379AC352 | الغيل | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الجوف: الغيل |
| ENT-YE-DISTRICT-669821052CAE | ناطع | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: ناطع |
| ENT-YE-DISTRICT-68BAE1D63E1B | ثمود | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: ثمود |
| ENT-YE-DISTRICT-6977F8781716 | بني سعد | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المحويت: بني سعد |
| ENT-YE-DISTRICT-69BDA32168F2 | كتاف والبقع | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صعدة: كتاف والبقع |
| ENT-YE-DISTRICT-6A6F873FC88E | أحور | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أبين: أحور |
| ENT-YE-DISTRICT-6AE718FCAB9D | المصلوب | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الجوف: المصلوب |
| ENT-YE-DISTRICT-6C5553B14876 | الحيمة الداخلية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صنعاء: الحيمة الداخلية |
| ENT-YE-DISTRICT-6DA2C08658F7 | خراب المراشي | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الجوف: خراب المراشي |
| ENT-YE-DISTRICT-6E1AFA623AA9 | جبلة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: جبلة |
| ENT-YE-DISTRICT-6EC516CCD215 | ميفعة عنس | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ذمار: ميفعة عنس |
| ENT-YE-DISTRICT-709511780C1F | الروضة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate شبوة: الروضة |
| ENT-YE-DISTRICT-70F8D63E845A | السود | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: السود |
| ENT-YE-DISTRICT-7118E686CE5C | الشحر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: الشحر |
| ENT-YE-DISTRICT-72EE049B7479 | قفلة عذر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: قفلة عذر |
| ENT-YE-DISTRICT-739659576F38 | حوث | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: حوث |
| ENT-YE-DISTRICT-7404F9883573 | مذيخرة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: مذيخرة |
| ENT-YE-DISTRICT-74E342076015 | نصاب | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate شبوة: نصاب |
| ENT-YE-DISTRICT-7674A695145D | مدينة حجة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: مدينة حجة |
| ENT-YE-DISTRICT-76A6620AA445 | حجر الصيعر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: حجر الصيعر |
| ENT-YE-DISTRICT-76E243B0933F | رحبة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate مأرب: رحبة |
| ENT-YE-DISTRICT-787E62D8D1ED | قفل شمر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: قفل شمر |
| ENT-YE-DISTRICT-79940EEFA8D6 | ذي السفال | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: ذي السفال |
| ENT-YE-DISTRICT-79B799391DBA | بني الحارث | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أمانة العاصمة: بني الحارث |
| ENT-YE-DISTRICT-79ECC1C462F0 | برع | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: برع |
| ENT-YE-DISTRICT-7A30BAC54EA1 | شرعب السلام | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: شرعب السلام |
| ENT-YE-DISTRICT-7A8B3F4C86CE | خدير | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: خدير |
| ENT-YE-DISTRICT-7B5F50DB6F09 | عبس | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: عبس |
| ENT-YE-DISTRICT-7B786227BB09 | مشرعة وحدنان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: مشرعة وحدنان |
| ENT-YE-DISTRICT-7C65D454F2CB | مدينة ذمار | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ذمار: مدينة ذمار |
| ENT-YE-DISTRICT-7CF90B02044A | الحالي | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: الحالي |
| ENT-YE-DISTRICT-7E679D8F544C | بدبدة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate مأرب: بدبدة |
| ENT-YE-DISTRICT-7F304E92DBDC | سيحوت | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المهرة: سيحوت |
| ENT-YE-DISTRICT-7F7296329D17 | عين | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate شبوة: عين |
| ENT-YE-DISTRICT-7F8590D98431 | همدان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صنعاء: همدان |
| ENT-YE-DISTRICT-7FA28B1D5590 | الحداء | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ذمار: الحداء |
| ENT-YE-DISTRICT-8002C2FD003F | زنجبار | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أبين: زنجبار |
| ENT-YE-DISTRICT-802EC45625E8 | مجزر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate مأرب: مجزر |
| ENT-YE-DISTRICT-804B4533AB7D | المدان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: المدان |
| ENT-YE-DISTRICT-807F4DB14A6C | بني العوام | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: بني العوام |
| ENT-YE-DISTRICT-823C6A739BA6 | العبدية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate مأرب: العبدية |
| ENT-YE-DISTRICT-83065FF40884 | حيفان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: حيفان |
| ENT-YE-DISTRICT-8428A87F1D17 | حوف | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المهرة: حوف |
| ENT-YE-DISTRICT-8460476DCB8E | مرخة العليا | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate شبوة: مرخة العليا |
| ENT-YE-DISTRICT-88F7D4016A19 | مكيراس | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: مكيراس |
| ENT-YE-DISTRICT-8A7971BE6494 | برط العنان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الجوف: برط العنان |
| ENT-YE-DISTRICT-8AAF8F5B82BD | خولان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صنعاء: خولان |
| ENT-YE-DISTRICT-8B10137720B6 | الزاهر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: الزاهر |
| ENT-YE-DISTRICT-8B2F6F7EA855 | جبل راس | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: جبل راس |
| ENT-YE-DISTRICT-8B6A6EB01D85 | الغيظة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المهرة: الغيظة |
| ENT-YE-DISTRICT-8BC2557EB095 | حيدان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صعدة: حيدان |
| ENT-YE-DISTRICT-8BD370F8731E | بروم ميفع | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: بروم ميفع |
| ENT-YE-DISTRICT-8BDEDA7C1216 | السبعين | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أمانة العاصمة: السبعين |
| ENT-YE-DISTRICT-8CE2B39E219D | المغلاف | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: المغلاف |
| ENT-YE-DISTRICT-8D1FE0A3B90E | المراوعة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: المراوعة |
| ENT-YE-DISTRICT-8D41703EBFCA | الجراحي | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: الجراحي |
| ENT-YE-DISTRICT-8DBCF25A3C04 | زمخ ومنوخ | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: زمخ ومنوخ |
| ENT-YE-DISTRICT-8DC6946811C7 | ردمان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: ردمان |
| ENT-YE-DISTRICT-8EB93E2762E1 | مودية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أبين: مودية |
| ENT-YE-DISTRICT-8F091A151FB7 | العشة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: العشة |
| ENT-YE-DISTRICT-8F312AB9F09C | الجعفرية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ريمة: الجعفرية |
| ENT-YE-DISTRICT-91239A72B646 | الجبين | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ريمة: الجبين |
| ENT-YE-DISTRICT-913764BA1074 | الثورة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أمانة العاصمة: الثورة |
| ENT-YE-DISTRICT-91FC283FB86F | حديبو | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أرخبيل سقطرى: حديبو |
| ENT-YE-DISTRICT-92E89E2813D1 | ثلاء | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: ثلاء |
| ENT-YE-DISTRICT-9317B1BD1D22 | القف | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: القف |
| ENT-YE-DISTRICT-93398C0E13D0 | إب | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: إب |
| ENT-YE-DISTRICT-93DCE1F6EB27 | مقبنة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: مقبنة |
| ENT-YE-DISTRICT-93F3DE81AA16 | الصلو | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: الصلو |
| ENT-YE-DISTRICT-942F4091B179 | شرعب الرونة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: شرعب الرونة |
| ENT-YE-DISTRICT-956C3E044180 | نعمان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: نعمان |
| ENT-YE-DISTRICT-958A6A68E709 | بني مطر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صنعاء: بني مطر |
| ENT-YE-DISTRICT-95E9982FBE3D | المخادر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: المخادر |
| ENT-YE-DISTRICT-96DB47A73B23 | شبام | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: شبام |
| ENT-YE-DISTRICT-9891B73E7004 | الخوخة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: الخوخة |
| ENT-YE-DISTRICT-98EA7C3E6DB0 | البريقة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عدن: البريقة |
| ENT-YE-DISTRICT-99CFC1DB6096 | بني ضبيان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صنعاء: بني ضبيان |
| ENT-YE-DISTRICT-9B538E99DAC8 | الحوك | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: الحوك |
| ENT-YE-DISTRICT-9B60EF09A40F | الحشوة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صعدة: الحشوة |
| ENT-YE-DISTRICT-9C67F2E23275 | الزاهر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الجوف: الزاهر |
| ENT-YE-DISTRICT-9E8A7D700B0B | قعطبة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الضالع: قعطبة |
| ENT-YE-DISTRICT-9EE3E11CB0EB | بيحان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate شبوة: بيحان |
| ENT-YE-DISTRICT-9EE75F17D39D | حيران | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: حيران |
| ENT-YE-DISTRICT-9F5570A96C63 | قشن | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المهرة: قشن |
| ENT-YE-DISTRICT-9FADFAC7198E | قلنسية وعبد الكوري | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أرخبيل سقطرى: قلنسية وعبد الكوري |
| ENT-YE-DISTRICT-A250EE80CF1A | بيت الفقيه | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: بيت الفقيه |
| ENT-YE-DISTRICT-A292EC4F527C | جحانة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صنعاء: جحانة |
| ENT-YE-DISTRICT-A463DACF3CB6 | الشرية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: الشرية |
| ENT-YE-DISTRICT-A5D2F69F758D | ميدي | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: ميدي |
| ENT-YE-DISTRICT-A6B75266D1A9 | زبيد | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: زبيد |
| ENT-YE-DISTRICT-A6FB66C5ECA5 | بعدان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: بعدان |
| ENT-YE-DISTRICT-A8AA8F14CB2C | الحد | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate لحج: الحد |
| ENT-YE-DISTRICT-A8B8A5CD3FBF | كعيدنة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: كعيدنة |
| ENT-YE-DISTRICT-A8CA41D514B9 | حزم العدين | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: حزم العدين |
| ENT-YE-DISTRICT-A9D7A4C3D54D | التواهي | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عدن: التواهي |
| ENT-YE-DISTRICT-AB82175BC3E7 | الشعر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: الشعر |
| ENT-YE-DISTRICT-AC6CE47F9EAC | السخنة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: السخنة |
| ENT-YE-DISTRICT-ACAB4CBF0D7B | المنيرة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: المنيرة |
| ENT-YE-DISTRICT-AE45CB68FD4D | القاهرة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: القاهرة |
| ENT-YE-DISTRICT-AE8E198DC118 | الأزارق | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الضالع: الأزارق |
| ENT-YE-DISTRICT-AF094FD3C015 | المقاطرة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate لحج: المقاطرة |
| ENT-YE-DISTRICT-AF4815895C90 | مناخة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صنعاء: مناخة |
| ENT-YE-DISTRICT-B07AAB9E72E7 | شرس | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: شرس |
| ENT-YE-DISTRICT-B1F0E38668C1 | عمد | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: عمد |
| ENT-YE-DISTRICT-B2F6C38D1264 | الطويلة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المحويت: الطويلة |
| ENT-YE-DISTRICT-B34D34825FD7 | المنار | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ذمار: المنار |
| ENT-YE-DISTRICT-B3B815F79E0B | الحوطة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate لحج: الحوطة |
| ENT-YE-DISTRICT-B47D431C1ECB | يبعث | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: يبعث |
| ENT-YE-DISTRICT-B4F44899183C | خارف | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: خارف |
| ENT-YE-DISTRICT-B524252BB901 | دوعن | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: دوعن |
| ENT-YE-DISTRICT-B552F7D2FAC0 | الخلق | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الجوف: الخلق |
| ENT-YE-DISTRICT-B57553945EE2 | ملحان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المحويت: ملحان |
| ENT-YE-DISTRICT-B5F7C15A1F5C | تبن | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate لحج: تبن |
| ENT-YE-DISTRICT-B658D82576AF | السلفية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ريمة: السلفية |
| ENT-YE-DISTRICT-B701F9FC27CD | المخاء | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: المخاء |
| ENT-YE-DISTRICT-B8523E935425 | الشاهل | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: الشاهل |
| ENT-YE-DISTRICT-B87079F1B50B | قطابر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صعدة: قطابر |
| ENT-YE-DISTRICT-BAD1D4C614B3 | شحن | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المهرة: شحن |
| ENT-YE-DISTRICT-BCDA6CAE197A | منعر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المهرة: منعر |
| ENT-YE-DISTRICT-BE1A5F40193B | المحويت | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المحويت: المحويت |
| ENT-YE-DISTRICT-BEDDE4981D2D | القفر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: القفر |
| ENT-YE-DISTRICT-BF9A51A87374 | عيال سريح | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: عيال سريح |
| ENT-YE-DISTRICT-BFFEFB10C965 | معين | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أمانة العاصمة: معين |
| ENT-YE-DISTRICT-C01C14B304BD | ولد ربيع | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: ولد ربيع |
| ENT-YE-DISTRICT-C0E4384AF33C | يريم | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: يريم |
| ENT-YE-DISTRICT-C13CCD787700 | الحجيلة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: الحجيلة |
| ENT-YE-DISTRICT-C1D2EC2541C8 | الرجم | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المحويت: الرجم |
| ENT-YE-DISTRICT-C1FDA9357E37 | جبل حبشي | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: جبل حبشي |
| ENT-YE-DISTRICT-C2AD9C4D2E62 | الشعيب | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الضالع: الشعيب |
| ENT-YE-DISTRICT-C2D49926C501 | المسيلة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المهرة: المسيلة |
| ENT-YE-DISTRICT-C491CA31100A | الظهار | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: الظهار |
| ENT-YE-DISTRICT-C4BC6892EF5B | قارة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: قارة |
| ENT-YE-DISTRICT-C561C7BB14C4 | الوازعية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: الوازعية |
| ENT-YE-DISTRICT-C5EEE47721D2 | السوادية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: السوادية |
| ENT-YE-DISTRICT-C69F5E78137C | رصد | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أبين: رصد |
| ENT-YE-DISTRICT-C724A2C11182 | جيشان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أبين: جيشان |
| ENT-YE-DISTRICT-C873922BFB8A | خنفر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أبين: خنفر |
| ENT-YE-DISTRICT-C8B07FA2C17E | باجل | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: باجل |
| ENT-YE-DISTRICT-C8BE202C1C59 | المحابشة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: المحابشة |
| ENT-YE-DISTRICT-C8C38826F75F | الشغادرة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: الشغادرة |
| ENT-YE-DISTRICT-C8CE3C7740EF | حصوين | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المهرة: حصوين |
| ENT-YE-DISTRICT-C996BC43E56E | عمران | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: عمران |
| ENT-YE-DISTRICT-C9B176134BAE | الملاجم | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: الملاجم |
| ENT-YE-DISTRICT-CBEBC035AC93 | الضالع | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الضالع: الضالع |
| ENT-YE-DISTRICT-CD0F9B765A42 | بني قيس الطور | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: بني قيس الطور |
| ENT-YE-DISTRICT-CD3ABA2FB17C | شعوب | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أمانة العاصمة: شعوب |
| ENT-YE-DISTRICT-CDBDFC1AE39E | أفلح الشام | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: أفلح الشام |
| ENT-YE-DISTRICT-CF6F8E93C4A3 | منبه | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صعدة: منبه |
| ENT-YE-DISTRICT-CFB4248B3437 | السودة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: السودة |
| ENT-YE-DISTRICT-CFDAC6D2692B | طور الباحة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate لحج: طور الباحة |
| ENT-YE-DISTRICT-D041CED5311F | دار سعد | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عدن: دار سعد |
| ENT-YE-DISTRICT-D12629213B2C | الطفة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: الطفة |
| ENT-YE-DISTRICT-D182B5914779 | ذي ناعم | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: ذي ناعم |
| ENT-YE-DISTRICT-D2D2AFDAA25A | غمر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صعدة: غمر |
| ENT-YE-DISTRICT-D5AA4AE74D1D | غيل بن يمين | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: غيل بن يمين |
| ENT-YE-DISTRICT-D7117933D9F0 | حرف سفيان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: حرف سفيان |
| ENT-YE-DISTRICT-D77BFBC3CD1C | جبل مراد | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate مأرب: جبل مراد |
| ENT-YE-DISTRICT-D7BBCE221251 | وصاب السافل | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ذمار: وصاب السافل |
| ENT-YE-DISTRICT-D7D24DDAD0F0 | العرش | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: العرش |
| ENT-YE-DISTRICT-D8DF23A36FEE | رداع | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: رداع |
| ENT-YE-DISTRICT-D975362BD5E8 | الصعيد | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate شبوة: الصعيد |
| ENT-YE-DISTRICT-DB4E49B8E1D3 | جردان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate شبوة: جردان |
| ENT-YE-DISTRICT-DC535AFC71B6 | وضرة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: وضرة |
| ENT-YE-DISTRICT-DD9D968D8BD3 | المعلا | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عدن: المعلا |
| ENT-YE-DISTRICT-DDB5631E7CD3 | شداء | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate صعدة: شداء |
| ENT-YE-DISTRICT-DF0BF1C11D20 | المنصورية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: المنصورية |
| ENT-YE-DISTRICT-E087030B2DB4 | خمر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: خمر |
| ENT-YE-DISTRICT-E0980CC43D4D | النادرة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: النادرة |
| ENT-YE-DISTRICT-E120BDD66087 | المفلحي | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate لحج: المفلحي |
| ENT-YE-DISTRICT-E1785B215D1C | ماوية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: ماوية |
| ENT-YE-DISTRICT-E180E6770A49 | السوم | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: السوم |
| ENT-YE-DISTRICT-E2BD72BF2810 | جحاف | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الضالع: جحاف |
| ENT-YE-DISTRICT-E33DDDC70FEF | رغوان | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate مأرب: رغوان |
| ENT-YE-DISTRICT-E3684E2E47C3 | عرماء | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate شبوة: عرماء |
| ENT-YE-DISTRICT-E50DC40F1400 | مدينة المكلا | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: مدينة المكلا |
| ENT-YE-DISTRICT-E7D3B2891EDC | التعزية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: التعزية |
| ENT-YE-DISTRICT-E7F1BF46642A | الشمايتين | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: الشمايتين |
| ENT-YE-DISTRICT-E839F89C9F87 | حبيل جبر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate لحج: حبيل جبر |
| ENT-YE-DISTRICT-E8E60E671E9F | خور مكسر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عدن: خور مكسر |
| ENT-YE-DISTRICT-E8F2D99A46B0 | مسورة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: مسورة |
| ENT-YE-DISTRICT-EA20E28BF121 | الديس | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: الديس |
| ENT-YE-DISTRICT-EA280530112A | الضحى | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: الضحى |
| ENT-YE-DISTRICT-EAA63A9025C3 | مستباء | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: مستباء |
| ENT-YE-DISTRICT-EB728445AE7C | عتمة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ذمار: عتمة |
| ENT-YE-DISTRICT-EC2057E04E60 | حات | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate المهرة: حات |
| ENT-YE-DISTRICT-ECFF19F2D7BD | الدريهمي | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الحديدة: الدريهمي |
| ENT-YE-DISTRICT-ED0F5742101A | مزهر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ريمة: مزهر |
| ENT-YE-DISTRICT-EDC8715A318E | التحرير | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أمانة العاصمة: التحرير |
| ENT-YE-DISTRICT-EE26CF34BF89 | مسور | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: مسور |
| ENT-YE-DISTRICT-EE6126DE1F80 | المواسط | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: المواسط |
| ENT-YE-DISTRICT-EEFD005FAB08 | بلاد الطعام | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ريمة: بلاد الطعام |
| ENT-YE-DISTRICT-EF580ADE7028 | الحصين | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الضالع: الحصين |
| ENT-YE-DISTRICT-EF62F26A902A | ريدة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: ريدة |
| ENT-YE-DISTRICT-EFDF4402C58B | جبن | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate الضالع: جبن |
| ENT-YE-DISTRICT-F325B7461C35 | المشنة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: المشنة |
| ENT-YE-DISTRICT-F4F6AFC6C830 | جبل الشرق | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate ذمار: جبل الشرق |
| ENT-YE-DISTRICT-F63838ACC699 | أرياف المكلا | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: أرياف المكلا |
| ENT-YE-DISTRICT-F6AE9AF84B6D | الملاح | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate لحج: الملاح |
| ENT-YE-DISTRICT-F6D20BB04EC1 | المسراخ | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: المسراخ |
| ENT-YE-DISTRICT-F87300499026 | سباح | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أبين: سباح |
| ENT-YE-DISTRICT-F8F45A27E6C6 | حالمين | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate لحج: حالمين |
| ENT-YE-DISTRICT-FABF888F3565 | المظفر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: المظفر |
| ENT-YE-DISTRICT-FACF6A88734B | البيضاء | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: البيضاء |
| ENT-YE-DISTRICT-FCA1BC82806C | سرار | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate أبين: سرار |
| ENT-YE-DISTRICT-FD372417DB1C | موزع | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate تعز: موزع |
| ENT-YE-DISTRICT-FD56EE8891F8 | مأرب | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate مأرب: مأرب |
| ENT-YE-DISTRICT-FDD1806EF7B1 | أفلح اليمن | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: أفلح اليمن |
| ENT-YE-DISTRICT-FE432D7CA8CF | جبل عيال يزيد | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate عمران: جبل عيال يزيد |
| ENT-YE-DISTRICT-FE757E407900 | وشحة | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حجة: وشحة |
| ENT-YE-DISTRICT-FE959F530DA8 | السياني | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate إب: السياني |
| ENT-YE-DISTRICT-FEF8FAFC3ABC | الريدة وقصيعر | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate حضرموت: الريدة وقصيعر |
| ENT-YE-DISTRICT-FF7A755C8713 | القريشية | ye_district | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | District catalogue, governorate البيضاء: القريشية |
| ENT-YE-GOVERNORATE-02 | صنعاء | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: صنعاء |
| ENT-YE-GOVERNORATE-03 | عدن | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: عدن |
| ENT-YE-GOVERNORATE-04 | حضرموت | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: حضرموت |
| ENT-YE-GOVERNORATE-05 | تعز | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: تعز |
| ENT-YE-GOVERNORATE-06 | الحديدة | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: الحديدة |
| ENT-YE-GOVERNORATE-07 | إب | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: إب |
| ENT-YE-GOVERNORATE-08 | أبين | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: أبين |
| ENT-YE-GOVERNORATE-09 | البيضاء | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: البيضاء |
| ENT-YE-GOVERNORATE-10 | لحج | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: لحج |
| ENT-YE-GOVERNORATE-11 | مأرب | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: مأرب |
| ENT-YE-GOVERNORATE-12 | شبوة | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: شبوة |
| ENT-YE-GOVERNORATE-13 | الجوف | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: الجوف |
| ENT-YE-GOVERNORATE-14 | المهرة | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: المهرة |
| ENT-YE-GOVERNORATE-15 | المحويت | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: المحويت |
| ENT-YE-GOVERNORATE-16 | صعدة | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: صعدة |
| ENT-YE-GOVERNORATE-17 | حجة | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: حجة |
| ENT-YE-GOVERNORATE-18 | الضالع | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: الضالع |
| ENT-YE-GOVERNORATE-19 | عمران | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: عمران |
| ENT-YE-GOVERNORATE-20 | ذمار | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: ذمار |
| ENT-YE-GOVERNORATE-21 | ريمة | ye_governorate | current | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: ريمة |
| ENT-YE-GOVERNORATE-22 | أرخبيل سقطرى | ye_governorate | current | SRC-YE-LAW-31-SOCOTRA-REPORT-2013 | Law 31/2013, issued 18 December 2013, Article 2 extract |
| ENT-YE-LANE-0917117AF865 | الأبزر | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 1: الأبزر |
| ENT-YE-LANE-0BE4AA7A5349 | بئر خيران | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir بير العزب lane table, seq 6: بئر خيران |
| ENT-YE-LANE-0C2126A297D0 | بحر رجرج | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 39: بحر رجرج |
| ENT-YE-LANE-134DEFCA2093 | عشة الرعدي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 20: عشة الرعدي |
| ENT-YE-LANE-14BCFECA9108 | شكر | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 55: شكر |
| ENT-YE-LANE-16408FDBEC40 | بستان المنصور | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir بير العزب lane table, seq 3: بستان المنصور |
| ENT-YE-LANE-165BF76712BF | بنك الدم | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 12: بنك الدم |
| ENT-YE-LANE-16AEECE3ABA1 | القاضي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 16: القاضي |
| ENT-YE-LANE-182E0F4A927E | سكرة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 47: سكرة |
| ENT-YE-LANE-1F76BF2D6F3A | المدرسة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 26: المدرسة |
| ENT-YE-LANE-252ACC42E15F | المفتون | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 30: المفتون |
| ENT-YE-LANE-26DB46908A04 | الخراز | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 13: الخراز |
| ENT-YE-LANE-290BA46F61E8 | الفليحي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 22: الفليحي |
| ENT-YE-LANE-2B1FF8F8F604 | القزالي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 24: القزالي |
| ENT-YE-LANE-2B3DE055513E | بير السويدي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 10: بير السويدي |
| ENT-YE-LANE-2BBE570D0DC0 | الكدس | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 25: الكدس |
| ENT-YE-LANE-2C4F4D16C5A4 | خضير | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 43: خضير |
| ENT-YE-LANE-2E61754A883E | باب السباح | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 36: باب السباح |
| ENT-YE-LANE-2FB043F2810E | الباشا | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 3: الباشا |
| ENT-YE-LANE-304F5B7CECA0 | نعمان | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 68: نعمان |
| ENT-YE-LANE-359917D3B8F2 | سوق سيلان | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 52: سوق سيلان |
| ENT-YE-LANE-36E5D92EC112 | الحرقان | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 9: الحرقان |
| ENT-YE-LANE-372BEF6ACE7C | الجوافة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 8: الجوافة |
| ENT-YE-LANE-37563B0670BE | الشراعي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 11: الشراعي |
| ENT-YE-LANE-3C0F6E926BEC | الجديد | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 6: الجديد |
| ENT-YE-LANE-3D93EE13CD2D | النهرين | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 34: النهرين |
| ENT-YE-LANE-40466FEC534E | الطواشي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 20: الطواشي |
| ENT-YE-LANE-40492988EE63 | البهمة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 14: البهمة |
| ENT-YE-LANE-41923508B2A7 | بئر البهمة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir بير العزب lane table, seq 7: بئر البهمة |
| ENT-YE-LANE-427157ECCEE9 | كباس | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 62: كباس |
| ENT-YE-LANE-42A6E433FC88 | الشراعي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 17: الشراعي |
| ENT-YE-LANE-42F12D9E12FD | موسى | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 66: موسى |
| ENT-YE-LANE-44403FF71438 | الحسوسة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 10: الحسوسة |
| ENT-YE-LANE-4907B2752000 | الميدان | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 32: الميدان |
| ENT-YE-LANE-4E04BA538404 | سبأ | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 46: سبأ |
| ENT-YE-LANE-4FB76B4DBE1F | معاذ | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 64: معاذ |
| ENT-YE-LANE-5121E51CECAE | باب عبيلة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir بير العزب lane table, seq 8: باب عبيلة |
| ENT-YE-LANE-56E01258DBCF | الزمر | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 15: الزمر |
| ENT-YE-LANE-5A7850F341DC | الدفعي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 14: الدفعي |
| ENT-YE-LANE-5A8CE104F6F7 | عقيل | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 58: عقيل |
| ENT-YE-LANE-5ABE74FA1C2E | بستان شارب | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 42: بستان شارب |
| ENT-YE-LANE-5DE7BF9C0236 | بستان علي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 15: بستان علي |
| ENT-YE-LANE-5E013021454E | الجامع الكبير | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 5: الجامع الكبير |
| ENT-YE-LANE-5EE221168E77 | شعوب | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 54: شعوب |
| ENT-YE-LANE-629072F5A63D | بستان السلطان | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 41: بستان السلطان |
| ENT-YE-LANE-63D5E9207817 | سوق المخلاص | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 50: سوق المخلاص |
| ENT-YE-LANE-64C1122A5FA2 | ياسر | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 69: ياسر |
| ENT-YE-LANE-67FA831417EE | الشهيدين | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 18: الشهيدين |
| ENT-YE-LANE-6C36AFBA441C | البلقة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 1: البلقة |
| ENT-YE-LANE-6E6377B84F49 | بروم | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 40: بروم |
| ENT-YE-LANE-6F713DAD95E5 | الأسطى | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 19: الأسطى |
| ENT-YE-LANE-72DD0B1A030D | البكيرية | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 4: البكيرية |
| ENT-YE-LANE-7ACA57E13B36 | نصير | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 67: نصير |
| ENT-YE-LANE-7C21C11A3807 | الحميدي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 11: الحميدي |
| ENT-YE-LANE-7ED0686FEF9A | بئر البهمة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 5: بئر البهمة |
| ENT-YE-LANE-80981A37774B | محمود | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 63: محمود |
| ENT-YE-LANE-8200CD5B9C67 | الكويت | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 2: الكويت |
| ENT-YE-LANE-84BCBE337109 | قبة المهدي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 61: قبة المهدي |
| ENT-YE-LANE-8719D6C9ECD5 | سمرة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 53: سمرة |
| ENT-YE-LANE-878D9221976F | المطيط | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 29: المطيط |
| ENT-YE-LANE-8830E05ED613 | الطبري | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 19: الطبري |
| ENT-YE-LANE-8D80EFA1FF0C | النظارة – الجديد | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 33: النظارة – الجديد |
| ENT-YE-LANE-8E3EE5B3BBA7 | القيادة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 18: القيادة |
| ENT-YE-LANE-92B33AD8D3E4 | قاع العلفي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir القاع lane table, seq 3: قاع العلفي |
| ENT-YE-LANE-92FA0009DBED | محمود (سوق البقر) | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 49: محمود (سوق البقر) |
| ENT-YE-LANE-9459B2D3C52F | بير البهمة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir بير العزب lane table, seq 4: بير البهمة |
| ENT-YE-LANE-9542F77A0F05 | المنصورة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 31: المنصورة |
| ENT-YE-LANE-9FC91519B497 | القاضي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir بير العزب lane table, seq 5: القاضي |
| ENT-YE-LANE-9FD6236B4D4A | السائلة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 16: السائلة |
| ENT-YE-LANE-9FDCF622B9E3 | العلمي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 21: العلمي |
| ENT-YE-LANE-A2F057FE508F | قاع العلفي-حمادي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir القاع lane table, seq 4: قاع العلفي-حمادي |
| ENT-YE-LANE-AE5FC81BC5AA | الإذاعة الشمالية | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 8: الإذاعة الشمالية |
| ENT-YE-LANE-AFF6A929142D | البونية | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir بير العزب lane table, seq 1: البونية |
| ENT-YE-LANE-B0206741CAC7 | خضير صرحة الوادي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 44: خضير صرحة الوادي |
| ENT-YE-LANE-B19FA396EFE3 | المصباغة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 28: المصباغة |
| ENT-YE-LANE-B3FA878CB1AF | الرجامي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir القاع lane table, seq 6: الرجامي |
| ENT-YE-LANE-B500010F53DB | الجامعة القديمة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 3: الجامعة القديمة |
| ENT-YE-LANE-B8BDE33CAC28 | طلحة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 57: طلحة |
| ENT-YE-LANE-BB6E5B517014 | معمر | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 65: معمر |
| ENT-YE-LANE-C02942555FD3 | بئر الشمس | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 13: بئر الشمس |
| ENT-YE-LANE-C08CD392511C | الكهرباء | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 7: الكهرباء |
| ENT-YE-LANE-C1A90FF85A0A | المذهب | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 27: المذهب |
| ENT-YE-LANE-C1D9BCA791DF | الأبهر | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 2: الأبهر |
| ENT-YE-LANE-C1DEE507ADA1 | بير أبو شملة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 4: بير أبو شملة |
| ENT-YE-LANE-C5084ED0E0D9 | سوق البقر | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 48: سوق البقر |
| ENT-YE-LANE-C5FDB3A299BA | باب السلام | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 37: باب السلام |
| ENT-YE-LANE-C643A5E7F61B | السلال | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir القاع lane table, seq 7: السلال |
| ENT-YE-LANE-C6CA8DAE2D18 | غمدان | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 60: غمدان |
| ENT-YE-LANE-CBF979D31CF2 | صلاح الدين | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 56: صلاح الدين |
| ENT-YE-LANE-CFF1C696409D | الجلاء | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 7: الجلاء |
| ENT-YE-LANE-D336D4C95FCF | الصياد | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir بير العزب lane table, seq 2: الصياد |
| ENT-YE-LANE-DA804AA02A6F | القاع | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir القاع lane table, seq 1: القاع |
| ENT-YE-LANE-DF0B26F1B7EB | الإذاعة الجنوبية | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 17: الإذاعة الجنوبية |
| ENT-YE-LANE-DF2E167B5236 | القبة | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 23: القبة |
| ENT-YE-LANE-DFE70124C2E5 | المترب | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir القاع lane table, seq 5: المترب |
| ENT-YE-LANE-E026A28A6AFF | غرقة القليس | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 59: غرقة القليس |
| ENT-YE-LANE-E5BCE121D129 | باب الروم | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 6: باب الروم |
| ENT-YE-LANE-E615D4B856D5 | باب القاع | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir القاع lane table, seq 2: باب القاع |
| ENT-YE-LANE-E702B92883DC | الخارجية | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 12: الخارجية |
| ENT-YE-LANE-E8A9611015AE | الوشلي | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 35: الوشلي |
| ENT-YE-LANE-F240619DCC6D | داود | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 45: داود |
| ENT-YE-LANE-F30FD711EB83 | باب اليمن | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 38: باب اليمن |
| ENT-YE-LANE-F644D5A656DC | بئر خيران | lane | current | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 9: بئر خيران |
| ENT-YE-LANE-FFC3D64F3CCD | سوق الملح | lane | current | SRC-YE-LANE-PAGES-MIRROR | Old Sanaa 69-lane inventory, seq 51: سوق الملح |
| ENT-YE-NEIGHBORHOOD-1BEE27CD8482 | القاع | neighborhood | current | SRC-YE-NIC-AMANAT-CENSUS-2004 | Tahrir district hay: القاع |
| ENT-YE-NEIGHBORHOOD-680F16A2B6E5 | بير العزب | neighborhood | current | SRC-YE-NIC-AMANAT-CENSUS-2004 | Tahrir district hay: بير العزب |
| ENT-YE-NEIGHBORHOOD-9C76154F62EC | التحرير | neighborhood | current | SRC-YE-NIC-AMANAT-CENSUS-2004 | Tahrir district hay: التحرير |

## الأسماء البديلة

| المعرّف | الكيان | الاسم | اللغة | النوع | المصدر |
|---|---|---|---|---|---|
| ALS-ABB3D1667B985AE9 | ENT-YE-COUNTRY | Yemen | en | english | SRC-ISO-3166-1-2020 |

## علاقات الإدارة/الموقع

| المعرّف | الابن | الأب | العلاقة | الحالة | المصدر |
|---|---|---|---|---|---|
| REL-YE-01C280E932F650DE | ENT-YE-DISTRICT-EAA63A9025C3 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-023BA922803A53E6 | ENT-YE-DISTRICT-446ED56B418D | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-02490B0D1B695BFF | ENT-YE-DISTRICT-942F4091B179 | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-02B4BA69AF8155FD | ENT-YE-DISTRICT-9F5570A96C63 | ENT-YE-GOVERNORATE-14 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-02C269A720E654D5 | ENT-YE-DISTRICT-C1D2EC2541C8 | ENT-YE-GOVERNORATE-15 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-0312F4D5D8655CBE | ENT-YE-DISTRICT-B2F6C38D1264 | ENT-YE-GOVERNORATE-15 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-038CAF5C793D57BC | ENT-YE-DISTRICT-1FD28938AA85 | ENT-YE-GOVERNORATE-12 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-03B25E70DF285AC2 | ENT-YE-DISTRICT-C491CA31100A | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-042A31D12979558D | ENT-YE-DISTRICT-C01C14B304BD | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-043E84C9681A5D60 | ENT-YE-DISTRICT-0E3A8FC6CC9C | ENT-YE-GOVERNORATE-11 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-05EEDE4BC2E45BDC | ENT-YE-DISTRICT-B524252BB901 | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-068C7B891778593E | ENT-YE-DISTRICT-53046A0ECF0A | ENT-YE-GOVERNORATE-13 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-06BA54D9F02F5FCB | ENT-YE-DISTRICT-EC2057E04E60 | ENT-YE-GOVERNORATE-14 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-06F154E4875D5234 | ENT-YE-DISTRICT-E7D3B2891EDC | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-087D62E572185325 | ENT-YE-DISTRICT-BE1A5F40193B | ENT-YE-GOVERNORATE-15 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-08A514BFC36853CE | ENT-YE-DISTRICT-EA280530112A | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-08AE697C502950D3 | ENT-YE-DISTRICT-E7F1BF46642A | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-09357AC958B45D05 | ENT-YE-DISTRICT-25DEBC9F4331 | ENT-YE-GOVERNORATE-12 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-09EFAC3348275BC1 | ENT-YE-DISTRICT-0A309AF13104 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-0A50605149FE5C89 | ENT-YE-DISTRICT-72EE049B7479 | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-0AEA6104489F548C | ENT-YE-DISTRICT-E087030B2DB4 | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-0AF4805795CE5D15 | ENT-YE-DISTRICT-76E243B0933F | ENT-YE-GOVERNORATE-11 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-0B96D901819656D6 | ENT-YE-DISTRICT-AE45CB68FD4D | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-0BB22E439A9F5432 | ENT-YE-DISTRICT-3095B13BD169 | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-0E49779DBDF45E49 | ENT-YE-DISTRICT-06EE7480D08D | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-0E6B3ED7F42F5683 | ENT-YE-DISTRICT-8F312AB9F09C | ENT-YE-GOVERNORATE-21 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-0EFEEBAB31BF5426 | ENT-YE-GOVERNORATE-19 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-0FED7D05014456F8 | ENT-YE-DISTRICT-FE959F530DA8 | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-121C0A8D89A25FA6 | ENT-YE-DISTRICT-C9B176134BAE | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-13AB78539A405124 | ENT-YE-DISTRICT-91239A72B646 | ENT-YE-GOVERNORATE-21 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-1444B929012D535A | ENT-YE-DISTRICT-7404F9883573 | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-1471A07A50F651F9 | ENT-YE-DISTRICT-FE757E407900 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-14749A8EACE455FC | ENT-YE-DISTRICT-065D10E84F28 | ENT-YE-GOVERNORATE-13 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-167087204B535131 | ENT-YE-DISTRICT-C2D49926C501 | ENT-YE-GOVERNORATE-14 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-17F9D1F584CC532A | ENT-YE-DISTRICT-7F7296329D17 | ENT-YE-GOVERNORATE-12 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-18716C6EBC18599F | ENT-YE-DISTRICT-F87300499026 | ENT-YE-GOVERNORATE-08 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-18AA9E9031D358C7 | ENT-YE-DISTRICT-376C1EFDE465 | ENT-YE-GOVERNORATE-12 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-1A00FF560B2250F7 | ENT-YE-DISTRICT-804B4533AB7D | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-1B6ADCA9A8FF51E9 | ENT-YE-DISTRICT-B34D34825FD7 | ENT-YE-GOVERNORATE-20 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-1BEF141056095728 | ENT-YE-DISTRICT-4C439AF1AFB0 | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-1DE3FD4D7B3359EB | ENT-YE-DISTRICT-7B5F50DB6F09 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-1E09637F9B98565E | ENT-YE-DISTRICT-88F7D4016A19 | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-1F03F99ED3595B01 | ENT-YE-DISTRICT-3691E8E68566 | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-206ED655E54D55F9 | ENT-YE-DISTRICT-650F379AC352 | ENT-YE-GOVERNORATE-13 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-20779EFD4B8C5E85 | ENT-YE-DISTRICT-6E1AFA623AA9 | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-20F9DCE1B7FC50CF | ENT-YE-DISTRICT-4EF0E76CBCBE | ENT-YE-GOVERNORATE-20 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-21FA26B8D96156F7 | ENT-YE-DISTRICT-D182B5914779 | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-232C7588482C5B5D | ENT-YE-DISTRICT-95E9982FBE3D | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-236DF92ABEFA5B5E | ENT-YE-DISTRICT-9FADFAC7198E | ENT-YE-GOVERNORATE-22 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-23B5BC8CF83C5453 | ENT-YE-DISTRICT-913764BA1074 | ENT-YE-CAPITAL-MUNICIPALITY-01 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-23E0486AAEF7532A | ENT-YE-DISTRICT-33BD3C230D4D | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-24EF8BB4765B5CCE | ENT-YE-DISTRICT-EDC8715A318E | ENT-YE-CAPITAL-MUNICIPALITY-01 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-253EFC7C2A285196 | ENT-YE-DISTRICT-25FC82D1C847 | ENT-YE-GOVERNORATE-12 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-26D810F8E42D5BCC | ENT-YE-DISTRICT-C1FDA9357E37 | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-26F3FE3FEA355028 | ENT-YE-DISTRICT-79ECC1C462F0 | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-2971860D21135F78 | ENT-YE-DISTRICT-C8BE202C1C59 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-2A57E9B60344516A | ENT-YE-DISTRICT-4956B0EDBB4F | ENT-YE-GOVERNORATE-08 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-2B53E494AA0F5C21 | ENT-YE-DISTRICT-5BAC2FFCE67A | ENT-YE-GOVERNORATE-02 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-2CC294118FA054CA | ENT-YE-DISTRICT-DF0BF1C11D20 | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-2DC6A45A91035B1D | ENT-YE-GOVERNORATE-16 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-2E22B6AE676151DC | ENT-YE-DISTRICT-EE6126DE1F80 | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-2F21286FE7D4574C | ENT-YE-GOVERNORATE-11 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-2F47E35371CC5FEE | ENT-YE-DISTRICT-A463DACF3CB6 | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-2F9848483E575A61 | ENT-YE-DISTRICT-65071A18A413 | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-2FD8058207AC546E | ENT-YE-DISTRICT-9B60EF09A40F | ENT-YE-GOVERNORATE-16 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-3072F82733ED5861 | ENT-YE-DISTRICT-30E672BCD16C | ENT-YE-GOVERNORATE-15 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-30A33326E0C35651 | ENT-YE-GOVERNORATE-03 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-30F5A30013EF5B19 | ENT-YE-DISTRICT-1D133E1F36EE | ENT-YE-GOVERNORATE-10 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-3140EFD401775127 | ENT-YE-DISTRICT-A292EC4F527C | ENT-YE-GOVERNORATE-02 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-31BE5C69AEE054D0 | ENT-YE-DISTRICT-ED0F5742101A | ENT-YE-GOVERNORATE-21 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-31EC4CC10D28513B | ENT-YE-DISTRICT-7B786227BB09 | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-3260CCEDACFD502E | ENT-YE-DISTRICT-2EA5F8194AE6 | ENT-YE-GOVERNORATE-12 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-335DA8F92D4852BF | ENT-YE-DISTRICT-7E679D8F544C | ENT-YE-GOVERNORATE-11 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-33E499BA686E5CC6 | ENT-YE-DISTRICT-2314C712E180 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-357467CD210F54CC | ENT-YE-DISTRICT-E1785B215D1C | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-35BD1974CFDE50B0 | ENT-YE-DISTRICT-451865966A05 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-36035E16DFC659AB | ENT-YE-DISTRICT-5A842A6DBAA5 | ENT-YE-GOVERNORATE-02 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-3637FAF776635DDC | ENT-YE-DISTRICT-83065FF40884 | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-3766F3B12F525D9C | ENT-YE-DISTRICT-C69F5E78137C | ENT-YE-GOVERNORATE-08 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-37A7CE12F7BC5D71 | ENT-YE-DISTRICT-DD9D968D8BD3 | ENT-YE-GOVERNORATE-03 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-3931D8718C895491 | ENT-YE-DISTRICT-D12629213B2C | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-3AC651A4964A5676 | ENT-YE-GOVERNORATE-22 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-LAW-31-SOCOTRA-REPORT-2013 |
| REL-YE-3C3912FEB31D577C | ENT-YE-DISTRICT-3FD301BC5889 | ENT-YE-GOVERNORATE-12 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-3C8DCC66BD9F5B88 | ENT-YE-DISTRICT-C996BC43E56E | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-3D8AA23859B95385 | ENT-YE-DISTRICT-A8CA41D514B9 | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-3E8AEEA33A605560 | ENT-YE-DISTRICT-5B7E0D3911E9 | ENT-YE-GOVERNORATE-21 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-40494EE0BD1F5AA9 | ENT-YE-DISTRICT-9B538E99DAC8 | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-408E060CD79E5675 | ENT-YE-DISTRICT-7A8B3F4C86CE | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-412F0C843BEB5194 | ENT-YE-DISTRICT-5B193F871C0B | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-438355A716615BFB | ENT-YE-DISTRICT-2F724D7BA06B | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-44FD080EA7445F00 | ENT-YE-DISTRICT-49A67B33D4F6 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-45E11E17B34D5048 | ENT-YE-DISTRICT-598617DCC9E2 | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-46026B0389F65B4C | ENT-YE-DISTRICT-13F900E880AE | ENT-YE-GOVERNORATE-20 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-471F5DBF7FA5534A | ENT-YE-DISTRICT-39E8FCE337F8 | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-47EA032C6C4B5566 | ENT-YE-DISTRICT-C8CE3C7740EF | ENT-YE-GOVERNORATE-14 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-49FA4128EEB35A3D | ENT-YE-DISTRICT-2CB5A0681CCB | ENT-YE-GOVERNORATE-02 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-4A3C237D442A52D3 | ENT-YE-DISTRICT-EF580ADE7028 | ENT-YE-GOVERNORATE-18 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-4A93EB8A8CC65379 | ENT-YE-DISTRICT-B1F0E38668C1 | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-4CE855AA6FC75DA5 | ENT-YE-GOVERNORATE-13 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-4CE9958BBB5E5A0C | ENT-YE-DISTRICT-8D41703EBFCA | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-4D87F6C1FB7A59B8 | ENT-YE-GOVERNORATE-08 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-4DCCE4C3A3B05D24 | ENT-YE-DISTRICT-D77BFBC3CD1C | ENT-YE-GOVERNORATE-11 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-4EA9D81D8CB3552C | ENT-YE-DISTRICT-9EE75F17D39D | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-4EBCDF1F4E1C50E3 | ENT-YE-DISTRICT-FACF6A88734B | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-51C1FD7B52E75069 | ENT-YE-DISTRICT-823C6A739BA6 | ENT-YE-GOVERNORATE-11 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-51E6DFF99EDD54B2 | ENT-YE-DISTRICT-5DD68C44EA2D | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-5228AA50E63B5B7C | ENT-YE-CAPITAL-MUNICIPALITY-01 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-5245CEDA7C2C56A0 | ENT-YE-DISTRICT-A5D2F69F758D | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-5299C76148835893 | ENT-YE-DISTRICT-A250EE80CF1A | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-533E84CCF5AC50B7 | ENT-YE-DISTRICT-39E111D17A62 | ENT-YE-GOVERNORATE-12 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-534395FC39EA5500 | ENT-YE-DISTRICT-91FC283FB86F | ENT-YE-GOVERNORATE-22 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-534B3D21153F5F6F | ENT-YE-DISTRICT-BEDDE4981D2D | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-54C72FEC9C2C53B0 | ENT-YE-DISTRICT-BFFEFB10C965 | ENT-YE-CAPITAL-MUNICIPALITY-01 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-54E7B595EF355E52 | ENT-YE-DISTRICT-B552F7D2FAC0 | ENT-YE-GOVERNORATE-13 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-553AE21D5D405459 | ENT-YE-DISTRICT-5C351EFED33D | ENT-YE-GOVERNORATE-13 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-5672D89AE1BB5F69 | ENT-YE-GOVERNORATE-14 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-569F884DD77B5274 | ENT-YE-DISTRICT-8460476DCB8E | ENT-YE-GOVERNORATE-12 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-57050EDCD1535624 | ENT-YE-DISTRICT-21776B6BC7C0 | ENT-YE-GOVERNORATE-02 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-578F23D5A64B5955 | ENT-YE-DISTRICT-35AEF4E9A32F | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-588B4CB9640D5064 | ENT-YE-DISTRICT-9C67F2E23275 | ENT-YE-GOVERNORATE-13 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-5942273D4688548B | ENT-YE-DISTRICT-14DB253EFEEC | ENT-YE-CAPITAL-MUNICIPALITY-01 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-59455649D7BF5387 | ENT-YE-DISTRICT-FABF888F3565 | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-59D96EEE6C325EF1 | ENT-YE-DISTRICT-A8B8A5CD3FBF | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-5A046BC80E71598F | ENT-YE-DISTRICT-5B3DC69A6DAA | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-5B0F4C2BFA045108 | ENT-YE-DISTRICT-EA20E28BF121 | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-5B19F619290650A4 | ENT-YE-DISTRICT-8428A87F1D17 | ENT-YE-GOVERNORATE-14 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-5C863275D1CD5A3D | ENT-YE-DISTRICT-D7117933D9F0 | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-5CB1D01F3D1452FC | ENT-YE-DISTRICT-4F5F82AB5A4B | ENT-YE-GOVERNORATE-03 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-5D6F49BA028756D6 | ENT-YE-DISTRICT-CFDAC6D2692B | ENT-YE-GOVERNORATE-10 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-5F233F3272F351ED | ENT-YE-DISTRICT-D041CED5311F | ENT-YE-GOVERNORATE-03 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-6014204C5B225662 | ENT-YE-DISTRICT-C2AD9C4D2E62 | ENT-YE-GOVERNORATE-18 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-608B47D68D805BCA | ENT-YE-DISTRICT-8002C2FD003F | ENT-YE-GOVERNORATE-08 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-60D1910C092F58E5 | ENT-YE-DISTRICT-8A7971BE6494 | ENT-YE-GOVERNORATE-13 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-60FB6E5884265718 | ENT-YE-DISTRICT-56AC99FF49C5 | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-616E37D74EDD5B03 | ENT-YE-DISTRICT-30DAD3916C7F | ENT-YE-GOVERNORATE-03 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-618EBDDE1D21522D | ENT-YE-DISTRICT-63A390C4F786 | ENT-YE-GOVERNORATE-08 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-62B7FE45031C5779 | ENT-YE-DISTRICT-14F726E0F79B | ENT-YE-GOVERNORATE-16 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-6461D8CA771C50F3 | ENT-YE-DISTRICT-C5EEE47721D2 | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-64948E70A395594F | ENT-YE-DISTRICT-6226424AD261 | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-6535C6A6EF745FC0 | ENT-YE-DISTRICT-F6AE9AF84B6D | ENT-YE-GOVERNORATE-10 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-655767516DD65D15 | ENT-YE-DISTRICT-294CCD62A649 | ENT-YE-GOVERNORATE-18 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-65721EA3D77B5DAC | ENT-YE-DISTRICT-958A6A68E709 | ENT-YE-GOVERNORATE-02 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-65F08326E86554A7 | ENT-YE-DISTRICT-51FD6B9DA297 | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-66262F38C9E355F9 | ENT-YE-DISTRICT-E50DC40F1400 | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-6640F76E268F5292 | ENT-YE-DISTRICT-93398C0E13D0 | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-66CB26AC65085E56 | ENT-YE-DISTRICT-10FD63FD9C4E | ENT-YE-GOVERNORATE-10 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-671A79AD9CB85912 | ENT-YE-DISTRICT-AC6CE47F9EAC | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-67B5B613AFDC5097 | ENT-YE-DISTRICT-0C80320ECE5F | ENT-YE-GOVERNORATE-12 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-68FFF806D9C45925 | ENT-YE-DISTRICT-DDB5631E7CD3 | ENT-YE-GOVERNORATE-16 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-69D42F8782A95809 | ENT-YE-DISTRICT-8EB93E2762E1 | ENT-YE-GOVERNORATE-08 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-6A32D461E329576C | ENT-YE-DISTRICT-0FB5E523A676 | ENT-YE-GOVERNORATE-16 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-6A50B245494A5C2B | ENT-YE-DISTRICT-7F8590D98431 | ENT-YE-GOVERNORATE-02 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-6B9342200FE95D67 | ENT-YE-DISTRICT-802EC45625E8 | ENT-YE-GOVERNORATE-11 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-6B9B8024C83B5B93 | ENT-YE-DISTRICT-ECFF19F2D7BD | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-6D818293BD9758FD | ENT-YE-DISTRICT-0F3C31473843 | ENT-YE-GOVERNORATE-13 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-6E26ADE6BD055B89 | ENT-YE-DISTRICT-ACAB4CBF0D7B | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-6E3EEE2B521A562E | ENT-YE-DISTRICT-8BD370F8731E | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-6F7E41D2F24F5B4F | ENT-YE-DISTRICT-C873922BFB8A | ENT-YE-GOVERNORATE-08 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-702C92678B115B73 | ENT-YE-DISTRICT-FDD1806EF7B1 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-70FE3139F30053BD | ENT-YE-DISTRICT-1E779AE3FA2C | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-715FCFD9E97F571C | ENT-YE-DISTRICT-DC535AFC71B6 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-736C2FC31CE45F12 | ENT-YE-DISTRICT-7A30BAC54EA1 | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-74EA3A9F4C6957AE | ENT-YE-DISTRICT-1DC8CC6E5663 | ENT-YE-GOVERNORATE-03 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-7511C5B8518A581A | ENT-YE-DISTRICT-B701F9FC27CD | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-759F1609DBB057FE | ENT-YE-DISTRICT-3F95B5A1F5BF | ENT-YE-GOVERNORATE-16 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-760AF7422BE05594 | ENT-YE-DISTRICT-A6B75266D1A9 | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-7696A4AAEE225CCC | ENT-YE-DISTRICT-EFDF4402C58B | ENT-YE-GOVERNORATE-18 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-76998081E443582C | ENT-YE-DISTRICT-6460ADF1477D | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-7726ECD2EB915CCF | ENT-YE-DISTRICT-B57553945EE2 | ENT-YE-GOVERNORATE-15 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-77FECFEE5F4A5BBE | ENT-YE-DISTRICT-3F2CDF08FF59 | ENT-YE-GOVERNORATE-11 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-7827C5AEBBA85C2F | ENT-YE-DISTRICT-F8F45A27E6C6 | ENT-YE-GOVERNORATE-10 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-793F9903AE2358F0 | ENT-YE-GOVERNORATE-15 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-79F07A6DABAA5B04 | ENT-YE-DISTRICT-32589B7B0574 | ENT-YE-CAPITAL-MUNICIPALITY-01 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-7AC7AD5C2D5C554E | ENT-YE-DISTRICT-B8523E935425 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-7BC745EC295A520B | ENT-YE-DISTRICT-8BC2557EB095 | ENT-YE-GOVERNORATE-16 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-7C8403F363C756F3 | ENT-YE-DISTRICT-534C0BB78FAF | ENT-YE-GOVERNORATE-11 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-7C93209922E954F7 | ENT-YE-GOVERNORATE-20 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-7CE560C38FA55FF9 | ENT-YE-DISTRICT-0D0A5492DA68 | ENT-YE-CAPITAL-MUNICIPALITY-01 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-7D14D7397DE05F6B | ENT-YE-DISTRICT-9EE3E11CB0EB | ENT-YE-GOVERNORATE-12 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-7D3F598D867C5DA9 | ENT-YE-DISTRICT-B658D82576AF | ENT-YE-GOVERNORATE-21 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-7D8D26A1A26052EB | ENT-YE-DISTRICT-31B68AB824FB | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-7DFA932B4E9A5E5B | ENT-YE-DISTRICT-9E8A7D700B0B | ENT-YE-GOVERNORATE-18 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-7EEEE095C6DA5B94 | ENT-YE-DISTRICT-AF094FD3C015 | ENT-YE-GOVERNORATE-10 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-7FA9E89819D0571F | ENT-YE-DISTRICT-8D1FE0A3B90E | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-7FD02BFCD30453A0 | ENT-YE-DISTRICT-A6FB66C5ECA5 | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-8128835E462356D1 | ENT-YE-DISTRICT-FEF8FAFC3ABC | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-8133E485A4B35388 | ENT-YE-DISTRICT-16A786CA1AB5 | ENT-YE-GOVERNORATE-11 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-81B8025059505A38 | ENT-YE-DISTRICT-0A49FF236843 | ENT-YE-GOVERNORATE-20 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-82512B8387B65C10 | ENT-YE-DISTRICT-2D9751BEFD41 | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-83691F2B7F99540E | ENT-YE-DISTRICT-99CFC1DB6096 | ENT-YE-GOVERNORATE-02 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-84695E6003C95895 | ENT-YE-DISTRICT-BCDA6CAE197A | ENT-YE-GOVERNORATE-14 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-8632DF97EA3F57A9 | ENT-YE-DISTRICT-16B2C03EFD2F | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-89847A1176015C2B | ENT-YE-DISTRICT-6DA2C08658F7 | ENT-YE-GOVERNORATE-13 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-8BBE7E5B1DB658A6 | ENT-YE-DISTRICT-8B10137720B6 | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-8D37F4CE61895811 | ENT-YE-DISTRICT-B5F7C15A1F5C | ENT-YE-GOVERNORATE-10 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-906B304B2A5F5B25 | ENT-YE-DISTRICT-63BB7185E88A | ENT-YE-GOVERNORATE-16 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-911641E6096459AB | ENT-YE-DISTRICT-CD3ABA2FB17C | ENT-YE-CAPITAL-MUNICIPALITY-01 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-9162471BAE0E5976 | ENT-YE-DISTRICT-4340895CDA75 | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-91BDC647876A5DB4 | ENT-YE-DISTRICT-CBEBC035AC93 | ENT-YE-GOVERNORATE-18 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-924209DE9D335D4F | ENT-YE-DISTRICT-588D6221966A | ENT-YE-GOVERNORATE-15 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-946D764A06125546 | ENT-YE-DISTRICT-1C2D2568B2F5 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-95E76920A7935D89 | ENT-YE-DISTRICT-7C65D454F2CB | ENT-YE-GOVERNORATE-20 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-9602AD76EE645EB3 | ENT-YE-DISTRICT-8B2F6F7EA855 | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-96FBECF3EFAF5A7C | ENT-YE-DISTRICT-B4F44899183C | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-976DB16FF79A58B6 | ENT-YE-DISTRICT-6A6F873FC88E | ENT-YE-GOVERNORATE-08 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-9799E9FEDBDD54BF | ENT-YE-DISTRICT-EB728445AE7C | ENT-YE-GOVERNORATE-20 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-99BE86B6749858AA | ENT-YE-DISTRICT-553E34DD89E5 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-99E3244B6C4959CD | ENT-YE-DISTRICT-CD0F9B765A42 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-9B267EB4FE4B5A6D | ENT-YE-DISTRICT-9317B1BD1D22 | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-9B33F7337DD250FF | ENT-YE-GOVERNORATE-05 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-9BCE33456FAC5A74 | ENT-YE-DISTRICT-6EC516CCD215 | ENT-YE-GOVERNORATE-20 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-9CF33FFB0AEF5F1F | ENT-YE-DISTRICT-CF6F8E93C4A3 | ENT-YE-GOVERNORATE-16 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-9D0EA55F1E885D64 | ENT-YE-DISTRICT-1D9E23C30969 | ENT-YE-GOVERNORATE-11 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-9DA310218E0C56AE | ENT-YE-DISTRICT-5AF8EE7DF37B | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-9DEDC0A6BB5C59ED | ENT-YE-DISTRICT-EE26CF34BF89 | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-9F7C2DBF1E925EAF | ENT-YE-GOVERNORATE-10 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-9F88ACE697EA5B92 | ENT-YE-DISTRICT-3B5EACB6791E | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A008580541E95DDC | ENT-YE-GOVERNORATE-18 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-A059F9B313685928 | ENT-YE-DISTRICT-372E17209D86 | ENT-YE-GOVERNORATE-12 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A08842E695BD5BE9 | ENT-YE-DISTRICT-AF4815895C90 | ENT-YE-GOVERNORATE-02 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A0B4288F9AEB53BB | ENT-YE-DISTRICT-2D0F0D552D30 | ENT-YE-GOVERNORATE-13 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A10D1003E9295DBF | ENT-YE-DISTRICT-6310172A6217 | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A24D68BD22265CB4 | ENT-YE-DISTRICT-C8C38826F75F | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A26A2622C16954D9 | ENT-YE-DISTRICT-C13CCD787700 | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A416185FA4C45566 | ENT-YE-DISTRICT-92E89E2813D1 | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A4672BDF9FFE562B | ENT-YE-DISTRICT-4BA89AD1F972 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A46DCFDD6BF35E27 | ENT-YE-DISTRICT-D8DF23A36FEE | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A4B48AB6414A5C2C | ENT-YE-DISTRICT-A9D7A4C3D54D | ENT-YE-GOVERNORATE-03 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A525D1B86B4B5E9A | ENT-YE-DISTRICT-2200C6BC9A3B | ENT-YE-GOVERNORATE-18 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A55E3BE548D25105 | ENT-YE-DISTRICT-79B799391DBA | ENT-YE-CAPITAL-MUNICIPALITY-01 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A6400CDB88365531 | ENT-YE-DISTRICT-B07AAB9E72E7 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A7B5BC1602D6548F | ENT-YE-DISTRICT-5A9F2A23F434 | ENT-YE-GOVERNORATE-20 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A91D31CC17795D48 | ENT-YE-DISTRICT-CFB4248B3437 | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A94C387E5FD05167 | ENT-YE-DISTRICT-6C5553B14876 | ENT-YE-GOVERNORATE-02 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A97B5E4FD84D5462 | ENT-YE-DISTRICT-FD56EE8891F8 | ENT-YE-GOVERNORATE-11 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A97CCDF1022A5EB8 | ENT-YE-DISTRICT-8BDEDA7C1216 | ENT-YE-CAPITAL-MUNICIPALITY-01 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-A9A8C802D58357FA | ENT-YE-DISTRICT-033FEF147059 | ENT-YE-GOVERNORATE-11 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-AA10BD01C377565B | ENT-YE-DISTRICT-93F3DE81AA16 | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-AA5F43E283BF5F95 | ENT-YE-DISTRICT-93DCE1F6EB27 | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-AAA84110E2315BE2 | ENT-YE-DISTRICT-CDBDFC1AE39E | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-AB3EDBFE7D38521F | ENT-YE-DISTRICT-7CF90B02044A | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-AB4FE7CF2C045DCA | ENT-YE-DISTRICT-0F723F77FC89 | ENT-YE-GOVERNORATE-16 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-ABAD5EC223945015 | ENT-YE-DISTRICT-1A140B15A926 | ENT-YE-GOVERNORATE-02 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-ADD6E44B923A5372 | ENT-YE-DISTRICT-98EA7C3E6DB0 | ENT-YE-GOVERNORATE-03 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-AF11227CE5095DB9 | ENT-YE-DISTRICT-D7BBCE221251 | ENT-YE-GOVERNORATE-20 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-AF4B861B3F4E5BA2 | ENT-YE-DISTRICT-4B0908476AEB | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-AFD6B352F89A5567 | ENT-YE-DISTRICT-E120BDD66087 | ENT-YE-GOVERNORATE-10 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-B01DC54B6FA750DD | ENT-YE-DISTRICT-709511780C1F | ENT-YE-GOVERNORATE-12 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-B035C66C98335305 | ENT-YE-DISTRICT-FF7A755C8713 | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-B07596336B3B5E78 | ENT-YE-DISTRICT-32BF31B664DD | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-B31392299D38503C | ENT-YE-DISTRICT-68BAE1D63E1B | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-B3F0E8DBC8B95A8F | ENT-YE-DISTRICT-0433DE028E03 | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-B4208056B1BF5A68 | ENT-YE-GOVERNORATE-04 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-B485B74879A651BD | ENT-YE-DISTRICT-787E62D8D1ED | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-B53F1C7B8050564D | ENT-YE-DISTRICT-46EDAA04F1E4 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-B5C929A6185A5279 | ENT-YE-DISTRICT-52D0EDBD39F9 | ENT-YE-GOVERNORATE-15 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-B683FB111BB55102 | ENT-YE-DISTRICT-8DBCF25A3C04 | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-B72313AFEBFF5DB3 | ENT-YE-DISTRICT-FD372417DB1C | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-B8F7AB1A04E658CE | ENT-YE-DISTRICT-0B501AB3B00D | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-B9D28C881D925F9E | ENT-YE-DISTRICT-D2D2AFDAA25A | ENT-YE-GOVERNORATE-16 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-BABBD0E838D95983 | ENT-YE-DISTRICT-0918A396268C | ENT-YE-GOVERNORATE-13 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-BB968328D2905DDC | ENT-YE-DISTRICT-2776D12E3A5A | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-BB9D6CF87F345918 | ENT-YE-DISTRICT-69BDA32168F2 | ENT-YE-GOVERNORATE-16 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-BC091196DCCA554B | ENT-YE-GOVERNORATE-12 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-BD61FC5D8BD75C1A | ENT-YE-DISTRICT-7F304E92DBDC | ENT-YE-GOVERNORATE-14 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-BE1042ED425755B8 | ENT-YE-DISTRICT-A8AA8F14CB2C | ENT-YE-GOVERNORATE-10 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-BE9908B75E775C9E | ENT-YE-DISTRICT-42B7313C7FBC | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-C025736D81455601 | ENT-YE-DISTRICT-E3684E2E47C3 | ENT-YE-GOVERNORATE-12 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-C2F74C103C5253D8 | ENT-YE-DISTRICT-35494423C71B | ENT-YE-GOVERNORATE-10 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-C34859BAB1FE5168 | ENT-YE-DISTRICT-EEFD005FAB08 | ENT-YE-GOVERNORATE-21 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-C4EE05313C47595C | ENT-YE-DISTRICT-70F8D63E845A | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-C7ED3B79174A56E4 | ENT-YE-DISTRICT-56B913F53DDF | ENT-YE-GOVERNORATE-10 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-C87D6BEFA4E1543E | ENT-YE-DISTRICT-9891B73E7004 | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-C8D302D5A32453F9 | ENT-YE-DISTRICT-2C424C87C3BE | ENT-YE-GOVERNORATE-02 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-CA7128E6C2185C7A | ENT-YE-DISTRICT-1626EA2FDE59 | ENT-YE-GOVERNORATE-11 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-CB096B6885CA5426 | ENT-YE-DISTRICT-8DC6946811C7 | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-CC44726F13775F87 | ENT-YE-DISTRICT-3578EDCD8379 | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-CCD4893B653C5C68 | ENT-YE-DISTRICT-165FE8764D7C | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-CD1E86300F0C5E52 | ENT-YE-DISTRICT-4D33D22350C1 | ENT-YE-GOVERNORATE-02 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-CD76E4FD6699576E | ENT-YE-DISTRICT-C0E4384AF33C | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-CDD18C29E45054B0 | ENT-YE-DISTRICT-E0980CC43D4D | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-CF2050ADA3FB51BC | ENT-YE-DISTRICT-646E3ADBE273 | ENT-YE-GOVERNORATE-16 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-CF729860DF305964 | ENT-YE-DISTRICT-B3B815F79E0B | ENT-YE-GOVERNORATE-10 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-CF9A5A6C968651A1 | ENT-YE-DISTRICT-292F5EBF6255 | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-D125309553875D3A | ENT-YE-DISTRICT-E180E6770A49 | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-D126117DB9995651 | ENT-YE-DISTRICT-7118E686CE5C | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-D181FDBDA1F45EB8 | ENT-YE-DISTRICT-352DD2903C6B | ENT-YE-GOVERNORATE-16 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-D1A54BF31C9C56B6 | ENT-YE-DISTRICT-3C88F00E0434 | ENT-YE-GOVERNORATE-20 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-D1E4A7EB4DF65D8A | ENT-YE-DISTRICT-B87079F1B50B | ENT-YE-GOVERNORATE-16 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-D204E5F16EC25F12 | ENT-YE-DISTRICT-D975362BD5E8 | ENT-YE-GOVERNORATE-12 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-D46851AB69F75F2A | ENT-YE-DISTRICT-FCA1BC82806C | ENT-YE-GOVERNORATE-08 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-D494CF80FFBF5645 | ENT-YE-DISTRICT-AB82175BC3E7 | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-D5175355817D5036 | ENT-YE-DISTRICT-8B6A6EB01D85 | ENT-YE-GOVERNORATE-14 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-D5CF000EF4A55123 | ENT-YE-DISTRICT-7674A695145D | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-D819B2ADDFD95D14 | ENT-YE-DISTRICT-956C3E044180 | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-D89DCB0682785BF2 | ENT-YE-DISTRICT-4AA53C0EC80A | ENT-YE-CAPITAL-MUNICIPALITY-01 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-D8BB9F3672FB5A32 | ENT-YE-GOVERNORATE-02 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-D8E390A2AFA158C2 | ENT-YE-DISTRICT-E2BD72BF2810 | ENT-YE-GOVERNORATE-18 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-D9F462887D0C54A3 | ENT-YE-GOVERNORATE-09 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-DA70E39E36305948 | ENT-YE-DISTRICT-F4F6AFC6C830 | ENT-YE-GOVERNORATE-20 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-DB75FE5C3E435874 | ENT-YE-DISTRICT-BAD1D4C614B3 | ENT-YE-GOVERNORATE-14 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-DBA40BEC594E50A1 | ENT-YE-DISTRICT-8CE2B39E219D | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-DBB38CB31BE65BDC | ENT-YE-DISTRICT-E839F89C9F87 | ENT-YE-GOVERNORATE-10 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-DCFD9EA244E95938 | ENT-YE-DISTRICT-E8E60E671E9F | ENT-YE-GOVERNORATE-03 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-DDD279FDBBF45BB6 | ENT-YE-DISTRICT-0931C242D57C | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-DE4B893577805E0C | ENT-YE-DISTRICT-BF9A51A87374 | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-DF676FC096C95939 | ENT-YE-DISTRICT-547879558CC8 | ENT-YE-GOVERNORATE-15 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-E05F51145E52578A | ENT-YE-DISTRICT-6AE718FCAB9D | ENT-YE-GOVERNORATE-13 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-E0D7A9F63D895952 | ENT-YE-GOVERNORATE-06 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-E11B8B44D67A579A | ENT-YE-DISTRICT-23CDC8A23150 | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-E1A45B8F8BF750A5 | ENT-YE-DISTRICT-05072004A1BE | ENT-YE-GOVERNORATE-02 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-E222BBBD5C5255E6 | ENT-YE-DISTRICT-D5AA4AE74D1D | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-E2500886694B58B0 | ENT-YE-DISTRICT-2FAA44D3AC59 | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-E2853BAFC5DD5103 | ENT-YE-DISTRICT-F63838ACC699 | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-E2A7F1F44AF4552C | ENT-YE-DISTRICT-8AAF8F5B82BD | ENT-YE-GOVERNORATE-02 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-E2D6EAEB89765606 | ENT-YE-DISTRICT-FE432D7CA8CF | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-E6D8132488725434 | ENT-YE-DISTRICT-79940EEFA8D6 | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-E7311C4137DB58FA | ENT-YE-DISTRICT-F325B7461C35 | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-E76A35E041D6562C | ENT-YE-GOVERNORATE-21 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-E78F744D5D24572B | ENT-YE-DISTRICT-6977F8781716 | ENT-YE-GOVERNORATE-15 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-E7942AFF8A455C49 | ENT-YE-DISTRICT-8F091A151FB7 | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-E7D1673CA9685327 | ENT-YE-DISTRICT-104F8DEB7391 | ENT-YE-GOVERNORATE-07 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-E849BBA85CF8510F | ENT-YE-DISTRICT-5018BFC1B1CD | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-E85739309C17522A | ENT-YE-DISTRICT-E8F2D99A46B0 | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-E94C6DA447EE57C9 | ENT-YE-DISTRICT-F6D20BB04EC1 | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-EAE49B72E1EB5ED8 | ENT-YE-DISTRICT-61CFCDE24752 | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-EB80D24EE870527F | ENT-YE-DISTRICT-C4BC6892EF5B | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-EC54F3096A90516F | ENT-YE-DISTRICT-3BE7603D86AA | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-ECC05A4672B75091 | ENT-YE-DISTRICT-B47D431C1ECB | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-ED99A0C5A20E546A | ENT-YE-DISTRICT-807F4DB14A6C | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-EDBED0C96D8C5440 | ENT-YE-DISTRICT-25A23003C30E | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-EDF749FF821F55C6 | ENT-YE-DISTRICT-C8B07FA2C17E | ENT-YE-GOVERNORATE-06 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-EE7859A35FCF509D | ENT-YE-DISTRICT-5874DE54BE90 | ENT-YE-GOVERNORATE-16 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-EEEACCB94F295F0A | ENT-YE-DISTRICT-0F4FEB79DB77 | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-EF6226E2E7C85170 | ENT-YE-DISTRICT-C724A2C11182 | ENT-YE-GOVERNORATE-08 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-F04E07E566E853E9 | ENT-YE-DISTRICT-D7D24DDAD0F0 | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-F1557633505F5004 | ENT-YE-DISTRICT-343E52EBFF3E | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-F163507E8D565291 | ENT-YE-DISTRICT-DB4E49B8E1D3 | ENT-YE-GOVERNORATE-12 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-F21CF39167C95E92 | ENT-YE-DISTRICT-12BC71EC7FE7 | ENT-YE-GOVERNORATE-10 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-F6A27CAB9FB65778 | ENT-YE-DISTRICT-739659576F38 | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-F6F24BB7569B5534 | ENT-YE-DISTRICT-76A6620AA445 | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-F7469E7FC8245981 | ENT-YE-DISTRICT-C561C7BB14C4 | ENT-YE-GOVERNORATE-05 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-F746BE1A36CE5B7A | ENT-YE-GOVERNORATE-17 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-F747F6BFDE1F572A | ENT-YE-DISTRICT-7FA28B1D5590 | ENT-YE-GOVERNORATE-20 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-F9BABBB65D645C2A | ENT-YE-DISTRICT-23C2ED53561D | ENT-YE-GOVERNORATE-17 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-FA345B79BF4955B0 | ENT-YE-DISTRICT-07D021680938 | ENT-YE-GOVERNORATE-02 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-FB919AE52591566C | ENT-YE-DISTRICT-EF62F26A902A | ENT-YE-GOVERNORATE-19 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-FC613E5792BE58BF | ENT-YE-DISTRICT-542E3C3E2498 | ENT-YE-GOVERNORATE-08 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-FC6EB35695C65A3D | ENT-YE-DISTRICT-AE8E198DC118 | ENT-YE-GOVERNORATE-18 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-FCE8598364FC581B | ENT-YE-DISTRICT-96DB47A73B23 | ENT-YE-GOVERNORATE-04 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-FD3ACF3F53D35925 | ENT-YE-DISTRICT-669821052CAE | ENT-YE-GOVERNORATE-09 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-FE8257A9CCCE574F | ENT-YE-DISTRICT-74E342076015 | ENT-YE-GOVERNORATE-12 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-FEC682FC6C515606 | ENT-YE-DISTRICT-1DC1BF36340C | ENT-YE-GOVERNORATE-10 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-FF43E2BCDBD354CA | ENT-YE-GOVERNORATE-07 | ENT-YE-COUNTRY | administrative_parent | current | SRC-YE-NIC-GOVERNORATES-LEGACY |
| REL-YE-FF95FC84045654B0 | ENT-YE-DISTRICT-E33DDDC70FEF | ENT-YE-GOVERNORATE-11 | administrative_parent | current | SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR |
| REL-YE-HAY-02BE2B12D3195EF5 | ENT-YE-NEIGHBORHOOD-680F16A2B6E5 | ENT-YE-DISTRICT-EDC8715A318E | located_in | current | SRC-YE-NIC-AMANAT-CENSUS-2004 |
| REL-YE-HAY-9ECDB7BE4D6253DD | ENT-YE-NEIGHBORHOOD-9C76154F62EC | ENT-YE-DISTRICT-EDC8715A318E | located_in | current | SRC-YE-NIC-AMANAT-CENSUS-2004 |
| REL-YE-HAY-C5E5C3947F6158C2 | ENT-YE-NEIGHBORHOOD-1BEE27CD8482 | ENT-YE-DISTRICT-EDC8715A318E | located_in | current | SRC-YE-NIC-AMANAT-CENSUS-2004 |
| REL-YE-LANE-0066D635476D5CA2 | ENT-YE-LANE-E026A28A6AFF | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-020671AD140D5AD2 | ENT-YE-LANE-C643A5E7F61B | ENT-YE-NEIGHBORHOOD-1BEE27CD8482 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-03960A0153635537 | ENT-YE-LANE-8E3EE5B3BBA7 | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-0694BC5BBC1E5FCA | ENT-YE-LANE-165BF76712BF | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-07A142D9FF825609 | ENT-YE-LANE-8200CD5B9C67 | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-0FBF71C63D5B5611 | ENT-YE-LANE-372BEF6ACE7C | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-10FE91D98E05559E | ENT-YE-LANE-AE5FC81BC5AA | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-116379C2D2F15788 | ENT-YE-LANE-0917117AF865 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-1465EDBF839052AC | ENT-YE-LANE-629072F5A63D | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-17F6F42C428F5A9D | ENT-YE-LANE-DA804AA02A6F | ENT-YE-NEIGHBORHOOD-1BEE27CD8482 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-186E2F1B04AD554D | ENT-YE-LANE-DF2E167B5236 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-199169414B405ED4 | ENT-YE-LANE-B3FA878CB1AF | ENT-YE-NEIGHBORHOOD-1BEE27CD8482 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-1B06D3C1DA255445 | ENT-YE-LANE-E702B92883DC | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-1C9A933E550D572F | ENT-YE-LANE-290BA46F61E8 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-1D5BF25C21D35A96 | ENT-YE-LANE-F644D5A656DC | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-1E49D7E2D9AD5260 | ENT-YE-LANE-DFE70124C2E5 | ENT-YE-NEIGHBORHOOD-1BEE27CD8482 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-1FA15FFE4160568C | ENT-YE-LANE-44403FF71438 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-233D1A93D6815AA1 | ENT-YE-LANE-4E04BA538404 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-2475A56EDB915D09 | ENT-YE-LANE-5E013021454E | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-26DDBA24D5D35692 | ENT-YE-LANE-9FDCF622B9E3 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-277B655741A654F7 | ENT-YE-LANE-B19FA396EFE3 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-27DCA7E43A8950F0 | ENT-YE-LANE-C6CA8DAE2D18 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-2824A67B37BD5AE1 | ENT-YE-LANE-B500010F53DB | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-2BBCA426BE6E576E | ENT-YE-LANE-7ED0686FEF9A | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-2CE212E28D665AE5 | ENT-YE-LANE-8830E05ED613 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-30A3CB2487F254CE | ENT-YE-LANE-16408FDBEC40 | ENT-YE-NEIGHBORHOOD-680F16A2B6E5 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-313E9CDC1AB15349 | ENT-YE-LANE-40492988EE63 | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-33FD4B286A8D5416 | ENT-YE-LANE-C1DEE507ADA1 | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-36ABF01739A356C5 | ENT-YE-LANE-182E0F4A927E | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-36CAEA51D7CC5A0A | ENT-YE-LANE-67FA831417EE | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-3C9E15E70469596D | ENT-YE-LANE-CBF979D31CF2 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-41C63C5977C65CC7 | ENT-YE-LANE-FFC3D64F3CCD | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-42925A20AF0452A3 | ENT-YE-LANE-0BE4AA7A5349 | ENT-YE-NEIGHBORHOOD-680F16A2B6E5 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-46EF29E4EB1352BC | ENT-YE-LANE-427157ECCEE9 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-4A1E57665B235527 | ENT-YE-LANE-C5FDB3A299BA | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-4AA45EC4EB995477 | ENT-YE-LANE-5A7850F341DC | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-4D719E5D54F254B5 | ENT-YE-LANE-4907B2752000 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-4E0FF899D5E351DE | ENT-YE-LANE-D336D4C95FCF | ENT-YE-NEIGHBORHOOD-680F16A2B6E5 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-4F8AB1FDB3555D24 | ENT-YE-LANE-41923508B2A7 | ENT-YE-NEIGHBORHOOD-680F16A2B6E5 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-5206B4CAA6555FF9 | ENT-YE-LANE-40466FEC534E | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-56B1871E1C69501A | ENT-YE-LANE-2B1FF8F8F604 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-5966E03F124C5908 | ENT-YE-LANE-6C36AFBA441C | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-5C65568615695F40 | ENT-YE-LANE-B8BDE33CAC28 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-5F986E5E712B58D2 | ENT-YE-LANE-8719D6C9ECD5 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-605609FF994758B1 | ENT-YE-LANE-0C2126A297D0 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-605D932CBA645530 | ENT-YE-LANE-2BBE570D0DC0 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-662DAF11A1DF5881 | ENT-YE-LANE-C1A90FF85A0A | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-667114BE6CE85C3B | ENT-YE-LANE-92B33AD8D3E4 | ENT-YE-NEIGHBORHOOD-1BEE27CD8482 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-6BBEAE2AECAA595E | ENT-YE-LANE-2B3DE055513E | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-7286D5BF9E5C591C | ENT-YE-LANE-2FB043F2810E | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-7782F32637895919 | ENT-YE-LANE-7C21C11A3807 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-7C58DA63D0BC57FF | ENT-YE-LANE-AFF6A929142D | ENT-YE-NEIGHBORHOOD-680F16A2B6E5 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-800B6A15CB655B98 | ENT-YE-LANE-5EE221168E77 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-8198019BAFA95F92 | ENT-YE-LANE-2E61754A883E | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-836AAB25B1915FF1 | ENT-YE-LANE-CFF1C696409D | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-83D0BB9D130B5B5D | ENT-YE-LANE-14BCFECA9108 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-8916C075EFB4560B | ENT-YE-LANE-C5084ED0E0D9 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-8CF0B23C978F5268 | ENT-YE-LANE-3C0F6E926BEC | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-8F9B2BA56E5552A3 | ENT-YE-LANE-80981A37774B | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-96D932372B395F21 | ENT-YE-LANE-252ACC42E15F | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-9D9B0355C0325EEB | ENT-YE-LANE-E5BCE121D129 | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-A200B3C17CF95B2E | ENT-YE-LANE-C1D9BCA791DF | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-A436390D5EF656B8 | ENT-YE-LANE-304F5B7CECA0 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-A4E752B1532A509E | ENT-YE-LANE-DF0B26F1B7EB | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-A5E5D71CC49B5063 | ENT-YE-LANE-84BCBE337109 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-AD18D865ECAE5B6A | ENT-YE-LANE-36E5D92EC112 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-AFF0BFEC20225B95 | ENT-YE-LANE-B0206741CAC7 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-B1A65341014456DC | ENT-YE-LANE-878D9221976F | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-B3D7423B58A251A7 | ENT-YE-LANE-C02942555FD3 | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-B7BC594C23865623 | ENT-YE-LANE-26DB46908A04 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-BA3E76732DF35549 | ENT-YE-LANE-9459B2D3C52F | ENT-YE-NEIGHBORHOOD-680F16A2B6E5 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-BBE2B8E24918555B | ENT-YE-LANE-16AEECE3ABA1 | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-BBFBBE152B765B1F | ENT-YE-LANE-4FB76B4DBE1F | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-BC8FDA8AE8F55099 | ENT-YE-LANE-64C1122A5FA2 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-BE0E34C2168B5C56 | ENT-YE-LANE-3D93EE13CD2D | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-BEB75C7DB2525457 | ENT-YE-LANE-7ACA57E13B36 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-C0176FB5A9735A32 | ENT-YE-LANE-42A6E433FC88 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-C175EDD9785C59C3 | ENT-YE-LANE-5ABE74FA1C2E | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-C4BF35448902579A | ENT-YE-LANE-92FA0009DBED | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-C59C22E7E3A853D0 | ENT-YE-LANE-42F12D9E12FD | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-C6BFFF464427584D | ENT-YE-LANE-72DD0B1A030D | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-C876F4BEF550515B | ENT-YE-LANE-1F76BF2D6F3A | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-CE4D0DF03C305855 | ENT-YE-LANE-5A8CE104F6F7 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-CE968AF2D2345F8B | ENT-YE-LANE-E8A9611015AE | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-D002AC7C99475A80 | ENT-YE-LANE-5121E51CECAE | ENT-YE-NEIGHBORHOOD-680F16A2B6E5 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-D2E57A8A25C1540E | ENT-YE-LANE-C08CD392511C | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-D6A7295F8C4F503B | ENT-YE-LANE-134DEFCA2093 | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-DB8B687DAC695127 | ENT-YE-LANE-359917D3B8F2 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-E10640C1202055BC | ENT-YE-LANE-5DE7BF9C0236 | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-E6F23F85ACA152EA | ENT-YE-LANE-8D80EFA1FF0C | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-E79642D297D7556A | ENT-YE-LANE-F30FD711EB83 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-E98F4F2E3F935AF0 | ENT-YE-LANE-BB6E5B517014 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-E9AD7A15DD505070 | ENT-YE-LANE-A2F057FE508F | ENT-YE-NEIGHBORHOOD-1BEE27CD8482 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-E9B5DC8D8B145D6E | ENT-YE-LANE-2C4F4D16C5A4 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-EA525B987CEF53BA | ENT-YE-LANE-63D5E9207817 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-F1BCEB6F3190598A | ENT-YE-LANE-9542F77A0F05 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-F247FE5808685DDA | ENT-YE-LANE-F240619DCC6D | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-F3A117C29032590A | ENT-YE-LANE-56E01258DBCF | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-F73DAC5F1F155207 | ENT-YE-LANE-9FD6236B4D4A | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-F73DAD9077F859C9 | ENT-YE-LANE-E615D4B856D5 | ENT-YE-NEIGHBORHOOD-1BEE27CD8482 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-F93623241F785461 | ENT-YE-LANE-37563B0670BE | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-FA4432A196D151FC | ENT-YE-LANE-9FC91519B497 | ENT-YE-NEIGHBORHOOD-680F16A2B6E5 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-FB19EB0B83365BF4 | ENT-YE-LANE-6F713DAD95E5 | ENT-YE-NEIGHBORHOOD-9C76154F62EC | located_in | current | SRC-YE-LANE-PAGES-MIRROR |
| REL-YE-LANE-FCDA48BF813F58BF | ENT-YE-LANE-6E6377B84F49 | ENT-YE-DISTRICT-0D0A5492DA68 | located_in | current | SRC-YE-LANE-PAGES-MIRROR |

## الادعاءات

| المعرّف | الموضوع | المحمول | القيمة | التصنيف | الثقة | الحالة | المصدر | المحدد |
|---|---|---|---|---|---|---|---|---|
| CLM-YE-0A3F4FCE3D8C5EC1 | ENT-YE-GOVERNORATE-04 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: حضرموت |
| CLM-YE-10B28D73A23952D4 | ENT-YE-GOVERNORATE-02 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: صنعاء |
| CLM-YE-179934E4C04F57F9 | ENT-YE-GOVERNORATE-06 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: الحديدة |
| CLM-YE-1D9C461F61CC5EA2 | ENT-YE-GOVERNORATE-12 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: شبوة |
| CLM-YE-271E88F53B745F97 | ENT-YE-GOVERNORATE-08 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: أبين |
| CLM-YE-296F8A8737AB55E9 | ENT-YE-GOVERNORATE-10 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: لحج |
| CLM-YE-29E1EB3BA6B15942 | ENT-YE-GOVERNORATE-09 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: البيضاء |
| CLM-YE-3433124D777B510D | ENT-YE-GOVERNORATE-14 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: المهرة |
| CLM-YE-3E9FAEB3B8B8595C | ENT-YE-GOVERNORATE-22 | administrative_profile | governorate | official | medium | verified | SRC-YE-LAW-31-SOCOTRA-REPORT-2013 | Law 31/2013, issued 18 December 2013, Article 2 extract |
| CLM-YE-5792777D2BD7561E | ENT-YE-GOVERNORATE-13 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: الجوف |
| CLM-YE-638F99BDEDA35B84 | ENT-YE-GOVERNORATE-21 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: ريمة |
| CLM-YE-6E24D44178B65E37 | ENT-YE-GOVERNORATE-15 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: المحويت |
| CLM-YE-71D3383DDE475AC7 | ENT-YE-GOVERNORATE-20 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: ذمار |
| CLM-YE-9866B8E0174E512D | ENT-YE-GOVERNORATE-22 | establishment_instrument | {'capital': 'حديبو', 'district_count': 2, 'effective_clause_verified': False, 'instrument_type': 'law', 'issuance_date': '2013-12-18', 'law_number': 31, 'year': 2013} | official | medium | verified | SRC-YE-LAW-31-SOCOTRA-REPORT-2013 | Report title and Article 2 extract, 18 December 2013 |
| CLM-YE-997CE3AFAB025966 | ENT-YE-GOVERNORATE-05 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: تعز |
| CLM-YE-AFBAFD0F210C5BE0 | ENT-YE-GOVERNORATE-07 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: إب |
| CLM-YE-C7CEA784CE33589F | ENT-YE-GOVERNORATE-03 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: عدن |
| CLM-YE-CEB5516785665D60 | ENT-YE-GOVERNORATE-19 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: عمران |
| CLM-YE-DIALECT-28823916E584560C | ENT-YE-GOVERNORATE-06 | dialect_profile | {'features': ['إيقاع أسرع', 'مفردات بحرية ومزارعية', 'روافد أفريقية تاريخية'], 'group': 'التهامية', 'sample_words': [], 'scope': 'سهل تهامة من الحديدة إلى المخا'} | regional | low | reported | SRC-YE-DIALECT-PAGES-MIRROR | Dialect group profile: التهامية |
| CLM-YE-DIALECT-5AB67120752D54D5 | ENT-YE-GOVERNORATE-02 | dialect_profile | {'features': ['القاف تنطق g', 'الضاد تنطق ظاء', 'ترقيق الراء والحاء والخاء', 'إبدال الدال طاء في بعض الكلمات مثل صدم إلى صطم'], 'group': 'الصنعانية', 'sample_words': [{'m': 'حينما هو', 'w': 'حينهو'}, {'m': 'كمل أو خلص', 'w': 'معادبش'}, {'m': 'لأجل', 'w': 'على ميد'}], 'scope': 'صنعاء والمرتفعات الوسطى'} | regional | low | reported | SRC-YE-DIALECT-PAGES-MIRROR | Dialect group profile: الصنعانية |
| CLM-YE-DIALECT-5F6F1861AF725AAC | ENT-YE-GOVERNORATE-05 | dialect_profile | {'features': ['الثاء تنطق تاء مثل ثاني إلى تاني', 'الجيم تنطق g', 'نفي الماضي بإلحاق كاف وشين مثل ما عملكش'], 'group': 'التعزية العدنية', 'sample_words': [{'m': 'لم أجد', 'w': 'ما حصلتوش'}, {'m': 'سأعمل وأرد لك مالك ولن أنكر ما أعطيتني', 'w': 'شاشقي وشندي لك مو شنكرك'}], 'scope': 'تعز وعدن والجنوب الأدنى'} | regional | low | reported | SRC-YE-DIALECT-PAGES-MIRROR | Dialect group profile: التعزية العدنية |
| CLM-YE-DIALECT-9FAFAB13546B53AB | ENT-YE-GOVERNORATE-10 | dialect_profile | {'features': ['القاف تنطق غينا مثل قال إلى غال', 'تاء الفاعل تستبدل بكاف مثل رحك ونمك وأكلك', 'نون النسوة يسبقها ياء ساكنة مثل سافرين'], 'group': 'اليافعية', 'sample_words': [{'m': 'لماذا', 'w': 'لمه'}, {'m': 'هل ذهبت إلى البلاد', 'w': 'شي سرك البلاد'}, {'m': 'تعب وملل', 'w': 'عثق وضبح'}, {'m': 'ضرب', 'w': 'لبج'}], 'scope': 'يافع في جبال لحج والضالع'} | regional | low | reported | SRC-YE-DIALECT-PAGES-MIRROR | Dialect group profile: اليافعية |
| CLM-YE-DIALECT-E1A49686097750B9 | ENT-YE-GOVERNORATE-04 | dialect_profile | {'features': ['قلب الجيم ياء في بعض مدن الساحل مثل رجال إلى ريال', 'جيم معتشة في وادي دوعن', 'دمج الضاد والظاء في صوت واحد'], 'group': 'الحضرمية', 'sample_words': [{'m': 'مرحبا', 'w': 'حيابك'}, {'m': 'سيكون لك؛ با بدل سوف', 'w': 'بايقع لك'}, {'m': 'سطح المنزل', 'w': 'الريم'}, {'m': 'ذهب', 'w': 'دحق'}, {'m': 'سيارة؛ أثر الهجرة', 'w': 'موتر'}], 'scope': 'حضرموت مع مؤثرات هجرة شرق أفريقيا والهند'} | regional | low | reported | SRC-YE-DIALECT-PAGES-MIRROR | Dialect group profile: الحضرمية |
| CLM-YE-DISH-0A174E3A8D5A56E4 | ENT-YE-GOVERNORATE-02 | food_dish | {'description': 'مرق لحم مع حلبة مخفوقة وسحويق وبهارات، تقدم فائرة في إناء حجري يسمى المدرة أو المفحح وتؤكل بالخبز اليمني', 'name': 'السلتة', 'note': 'أصلها المرتفعات وصنعاء خاصة وانتشارها وطني؛ لا تنسب ملكية حصرية لمدينة واحدة', 'occasion': 'غداء يومي شعبي وخاصة في رمضان'} | national | low | reported | SRC-YE-CUISINE-PAGES-MIRROR | Dish entry: السلتة |
| CLM-YE-DISH-17618A15AEB95382 | ENT-YE-COUNTRY | food_dish | {'description': 'كالمندي لكن يدفن اللحم أو الدجاج مع الأرز في حفرة ويحاط بالفحم، ويقدم مع الزبادي وصلصة الطماطم الحارة', 'name': 'المدفون', 'note': 'منتشر يمنيا', 'occasion': 'ولائم'} | national | low | reported | SRC-YE-CUISINE-PAGES-MIRROR | Dish entry: المدفون |
| CLM-YE-DISH-1A3C1559AD375CAC | ENT-YE-GOVERNORATE-04 | food_dish | {'description': 'حلويات حضرمية مرتبطة بعسل الوديان اليمني الشهير', 'name': 'بنت الصحن الحضرمية والذمول الحلو وعسل الوديان', 'note': 'حضرموت الداخلية: وديان زراعية وقوافل تجارية تاريخية', 'occasion': 'ضيافة'} | local | low | reported | SRC-YE-CUISINE-PAGES-MIRROR | Dish entry: بنت الصحن الحضرمية والذمول الحلو وعسل الوديان |
| CLM-YE-DISH-5B96D43A90735FB3 | ENT-YE-GOVERNORATE-02 | food_dish | {'description': 'لحم عجل أو شاة يطبخ على حرارة عالية في أوان فخارية مع مرق وثوم وفلفل حار وبهارات ويقدم ساخنا مع خبز التنور', 'name': 'الفحسة', 'note': 'صنعانية الأصل', 'occasion': 'غداء أساسي في صنعاء وحاضرة في المناسبات'} | local | low | reported | SRC-YE-CUISINE-PAGES-MIRROR | Dish entry: الفحسة |
| CLM-YE-DISH-5EFA675ABD595EC8 | ENT-YE-GOVERNORATE-04 | food_dish | {'description': 'معجنات محشوة بالتمر أو اللحم', 'name': 'الذمول', 'note': 'حضرموت', 'occasion': 'فطور'} | local | low | reported | SRC-YE-CUISINE-PAGES-MIRROR | Dish entry: الذمول |
| CLM-YE-DISH-7017944E20EA5F81 | ENT-YE-GOVERNORATE-11 | food_dish | {'description': 'لحم مشوي على شبك فوق الجمر', 'name': 'المظبي', 'note': 'المرتفعات والبدو', 'occasion': 'وليمة'} | regional | low | reported | SRC-YE-CUISINE-PAGES-MIRROR | Dish entry: المظبي |
| CLM-YE-DISH-77001218C3255017 | ENT-YE-GOVERNORATE-06 | food_dish | {'description': 'خبز إسفنجي خفيف يشبه الإنجيرا الإثيوبية', 'name': 'اللحوح', 'note': 'تهامة والجنوب', 'occasion': 'فطور رمضان'} | regional | low | reported | SRC-YE-CUISINE-PAGES-MIRROR | Dish entry: اللحوح |
| CLM-YE-DISH-84CB68C301315387 | ENT-YE-GOVERNORATE-03 | food_dish | {'description': 'خبز محشو بتأثير هندي وإندونيسي', 'name': 'المطبق', 'note': 'عدن وتهامة؛ أثر ميناء عدن الدولي', 'occasion': 'فطور'} | regional | low | reported | SRC-YE-CUISINE-PAGES-MIRROR | Dish entry: المطبق |
| CLM-YE-DISH-85BFDA57F2AD5CA5 | ENT-YE-COUNTRY | food_dish | {'description': 'مزيج دقيق وماء وسمن يعجن كقبة يتوسطها تجويف يملأ بالمرق واللحم ويؤكل بإصبعين من اليد اليمنى', 'name': 'العصيدة', 'note': 'المرتفعات والجنوب', 'occasion': 'رمضان والمناسبات'} | national | low | reported | SRC-YE-CUISINE-PAGES-MIRROR | Dish entry: العصيدة |
| CLM-YE-DISH-A50FAA7B401A5063 | ENT-YE-COUNTRY | food_dish | {'description': 'فطيرة طبقات عجين مدهونة بالزبدة أو السمن تؤكل بالعسل وحبة البركة', 'name': 'بنت الصحن', 'note': 'تنسب إلى صنعاء وحضرموت معا؛ نسبة مزدوجة تسجل كما وردت', 'occasion': 'فطور وحلوى ومناسبات'} | national | low | reported | SRC-YE-CUISINE-PAGES-MIRROR | Dish entry: بنت الصحن |
| CLM-YE-DISH-CC2DE1C94E1C509F | ENT-YE-GOVERNORATE-03 | food_dish | {'description': 'أرز وسمك بتأثير بحري', 'name': 'الصيادية', 'note': 'الساحل: الحديدة وعدن', 'occasion': 'غداء ساحلي'} | regional | low | reported | SRC-YE-CUISINE-PAGES-MIRROR | Dish entry: الصيادية |
| CLM-YE-DISH-D558D0133F405E43 | ENT-YE-GOVERNORATE-04 | food_dish | {'description': 'لحم أو دجاج يطهى مع الأرز في حفرة تنور تحت الأرض على جمر الفحم فيكتسب نكهة مدخنة، ويقدم مع السحويق والسلطة', 'name': 'المندي', 'note': 'حضرمي الأصل وانتشر إلى كل اليمن ثم الجزيرة العربية؛ التصنيف مشترك التزاما بعدم الملكية الحصرية', 'occasion': 'الولائم الكبرى والأعراس'} | shared | low | reported | SRC-YE-CUISINE-PAGES-MIRROR | Dish entry: المندي |
| CLM-YE-E19CD1553E23558B | ENT-YE-GOVERNORATE-11 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: مأرب |
| CLM-YE-E32110FF388D5F18 | ENT-YE-GOVERNORATE-16 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: صعدة |
| CLM-YE-E6F9307F0013553F | ENT-YE-GOVERNORATE-18 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: الضالع |
| CLM-YE-F0E19F6876595282 | ENT-YE-CAPITAL-MUNICIPALITY-01 | administrative_profile | capital_municipality | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: أمانة العاصمة |
| CLM-YE-F7FB744B44E157BE | ENT-YE-GOVERNORATE-17 | administrative_profile | governorate | official | high | verified | SRC-YE-NIC-GOVERNORATES-LEGACY | Governorates catalogue entry: حجة |
| CLM-YE-LANENAME-1D44EDB9395654F8 | ENT-YE-LANE-E026A28A6AFF | name_origin_narrative | تحمل الحارة اسم كنيسة القليس التي بناها أبرهة ثم زالت؛ بقي الاسم معلمًا لغويًا على الموضع | historical | low | reported | SRC-YE-LANE-PAGES-MIRROR | Naming note for lane غرقة القليس |
| CLM-YE-LANENAME-2827BE8754A25DC6 | ENT-YE-LANE-C6CA8DAE2D18 | name_origin_narrative | تحمل الحارة اسم قصر غمدان الشهير الزائل منذ ما يزيد على 1400 سنة؛ استمرار الاسم دليل استمرارية عمرانية | historical | low | reported | SRC-YE-LANE-PAGES-MIRROR | Naming note for lane غمدان |
| CLM-YE-LANENAME-B0BD9B3DFF585DD1 | ENT-YE-LANE-64C1122A5FA2 | name_origin_narrative | سميت الحارة نسبة إلى حمام ياسر؛ المرفق أعطى اسمه للحارة، ويرجح تزامن الحمام مع مسجد الأبهر وحمامه 1374م | historical | low | reported | SRC-YE-LANE-PAGES-MIRROR | Naming note for lane ياسر |
| CLM-YE-LANEPOP-0647E6D95C195577 | ENT-YE-LANE-16408FDBEC40 | population | 2049 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir بير العزب lane table, seq 3: بستان المنصور |
| CLM-YE-LANEPOP-0A776F0B290657B5 | ENT-YE-LANE-165BF76712BF | population | 1221 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 12: بنك الدم |
| CLM-YE-LANEPOP-1804DA47FDF55D07 | ENT-YE-LANE-AE5FC81BC5AA | population | 2852 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 8: الإذاعة الشمالية |
| CLM-YE-LANEPOP-19FAFE2AEAD556A8 | ENT-YE-LANE-D336D4C95FCF | population | 3147 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir بير العزب lane table, seq 2: الصياد |
| CLM-YE-LANEPOP-1E70CC8ADD88524F | ENT-YE-LANE-2B3DE055513E | population | 1885 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 10: بير السويدي |
| CLM-YE-LANEPOP-39B5373893F75FFE | ENT-YE-LANE-6C36AFBA441C | population | 5263 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 1: البلقة |
| CLM-YE-LANEPOP-3D9AE96ED83C5472 | ENT-YE-LANE-9FC91519B497 | population | 424 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir بير العزب lane table, seq 5: القاضي |
| CLM-YE-LANEPOP-41F0B9F22E1C558C | ENT-YE-LANE-C02942555FD3 | population | 1094 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 13: بئر الشمس |
| CLM-YE-LANEPOP-42D6A7069C5F5104 | ENT-YE-LANE-36E5D92EC112 | population | 2784 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Census-2004-citing lane page: الحرقان |
| CLM-YE-LANEPOP-4F91ACC583775AAC | ENT-YE-LANE-C08CD392511C | population | 2960 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 7: الكهرباء |
| CLM-YE-LANEPOP-5ED9EF67E1175C17 | ENT-YE-LANE-B8BDE33CAC28 | population | 669 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Census-2004-citing lane page: طلحة |
| CLM-YE-LANEPOP-7E4C9E1D46F85E47 | ENT-YE-LANE-134DEFCA2093 | population | 152 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 20: عشة الرعدي |
| CLM-YE-LANEPOP-7F87F7AB081556DA | ENT-YE-LANE-C1D9BCA791DF | population | 995 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Census-2004-citing lane page: الأبهر |
| CLM-YE-LANEPOP-8585C27A45595A91 | ENT-YE-LANE-5121E51CECAE | population | 190 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir بير العزب lane table, seq 8: باب عبيلة |
| CLM-YE-LANEPOP-89BFE59EBD4B5B46 | ENT-YE-LANE-E5BCE121D129 | population | 2992 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 6: باب الروم |
| CLM-YE-LANEPOP-8CF1475782BC5833 | ENT-YE-LANE-0BE4AA7A5349 | population | 259 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir بير العزب lane table, seq 6: بئر خيران |
| CLM-YE-LANEPOP-9757597D10D45732 | ENT-YE-LANE-C1DEE507ADA1 | population | 3103 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 4: بير أبو شملة |
| CLM-YE-LANEPOP-99D4BCA4F2465D0A | ENT-YE-LANE-B500010F53DB | population | 4731 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 3: الجامعة القديمة |
| CLM-YE-LANEPOP-9D4A26AD639A5A06 | ENT-YE-LANE-40492988EE63 | population | 665 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 14: البهمة |
| CLM-YE-LANEPOP-A1D0E9B5DFDB5E00 | ENT-YE-LANE-F240619DCC6D | population | 780 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Census-2004-citing lane page: داود |
| CLM-YE-LANEPOP-A8BD56925EE952F2 | ENT-YE-LANE-8200CD5B9C67 | population | 5230 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 2: الكويت |
| CLM-YE-LANEPOP-AADF6859298C50E4 | ENT-YE-LANE-37563B0670BE | population | 1816 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 11: الشراعي |
| CLM-YE-LANEPOP-BEA58CF5850F565F | ENT-YE-LANE-6F713DAD95E5 | population | 169 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 19: الأسطى |
| CLM-YE-LANEPOP-C180BF679DF55E98 | ENT-YE-LANE-AFF6A929142D | population | 3287 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir بير العزب lane table, seq 1: البونية |
| CLM-YE-LANEPOP-C9C2F86E462456CE | ENT-YE-LANE-9459B2D3C52F | population | 892 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir بير العزب lane table, seq 4: بير البهمة |
| CLM-YE-LANEPOP-CAB418613EB35CEC | ENT-YE-LANE-56E01258DBCF | population | 518 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Census-2004-citing lane page: الزمر |
| CLM-YE-LANEPOP-CBADC3A3F28454BC | ENT-YE-LANE-41923508B2A7 | population | 258 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir بير العزب lane table, seq 7: بئر البهمة |
| CLM-YE-LANEPOP-D32F67ECCC0C58E0 | ENT-YE-LANE-8E3EE5B3BBA7 | population | 209 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 18: القيادة |
| CLM-YE-LANEPOP-DB58BCA9E9A3547C | ENT-YE-LANE-DF0B26F1B7EB | population | 243 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 17: الإذاعة الجنوبية |
| CLM-YE-LANEPOP-DF58999600E055B5 | ENT-YE-LANE-16AEECE3ABA1 | population | 265 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 16: القاضي |
| CLM-YE-LANEPOP-E6E59085EC9B5769 | ENT-YE-LANE-5DE7BF9C0236 | population | 295 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 15: بستان علي |
| CLM-YE-LANEPOP-E6E7C2D5E2155109 | ENT-YE-LANE-7ED0686FEF9A | population | 3046 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 5: بئر البهمة |
| CLM-YE-LANEPOP-ED3466EAE44C581A | ENT-YE-LANE-F644D5A656DC | population | 2598 | local | medium | reported | SRC-YE-LANE-PAGES-MIRROR | Tahrir التحرير lane table, seq 9: بئر خيران |
| CLM-YE-LANG-85CA21640C9650FE | ENT-YE-GOVERNORATE-14 | language_presence | {'description': 'لغة سامية جنوبية حية في المهرة وأطراف سقطرى', 'language': 'المهرية'} | regional | medium | reported | SRC-YE-DIALECT-PAGES-MIRROR | Language note: المهرية |
| CLM-YE-LANG-FC4A22F0753257C5 | ENT-YE-GOVERNORATE-22 | language_presence | {'description': 'لغة سامية جنوبية مستقلة في أرخبيل سقطرى غير مفهومة لمتحدثي العربية', 'language': 'السقطرية'} | regional | medium | reported | SRC-YE-DIALECT-PAGES-MIRROR | Language note: السقطرية |

## جودة مصادر الادعاءات المنشورة

ادعاءات A/B: 23 من 23 (100.00%).

## المصادر الذرية المستخدمة

| المعرّف | الفئة | العنوان | الناشر | تاريخ النشر | تاريخ الاسترجاع | الترخيص | الرابط |
|---|---|---|---|---|---|---|---|
| SRC-ISO-3166-1-2020 | A | ISO 3166-1:2020 — Codes for the representation of names of countries and their subdivisions — Part 1: Country code | International Organization for Standardization (ISO) | 2020-08 | 2026-08-15 | ISO copyright; reuse is subject to ISO terms of use | https://www.iso.org/obp/ui/#iso:std:iso:3166:-1:ed-4:v1:en |
| SRC-YE-CENSUS-2004-LEGACY-FRAME | B | Census 2004 administrative frame — archived CSO administrative definitions | Central Statistical Organization Yemen via Internet Archive | 2018-09-30 | 2026-08-17 | Factual extraction with attribution; publisher reuse terms not stated | https://web.archive.org/web/20180930200530/http://www.cso-yemen.org/content.php?lng=arabic&id=277 |
| SRC-YE-CSO-ADMIN-DEFINITION-LEGACY | A | Administrative divisions definition: 20 governorates plus Capital Municipality | Central Statistical Organization Yemen | — | 2026-08-17 | Factual extraction with attribution; publisher reuse terms not stated | https://www.cso-yemen.com/content.php?lng=arabic&id=277 |
| SRC-YE-CUISINE-PAGES-MIRROR | E | Yemeni cuisine — encyclopedic and press mirror pages | Encyclopedic mirror pages and Arabic press features on Yemeni cuisine | — | 2026-08-17 | Factual extraction with attribution; publisher reuse terms not stated | https://ar.wikipedia.org/wiki/%D9%85%D8%B7%D8%A8%D8%AE_%D9%8A%D9%85%D9%86%D9%8A |
| SRC-YE-DIALECT-PAGES-MIRROR | E | Yemeni dialect groups — encyclopedic mirror pages | Encyclopedic mirror pages on Yemeni dialect groups and lexicon | — | 2026-08-17 | Factual extraction with attribution; publisher reuse terms not stated | https://ar.wikipedia.org/wiki/%D9%84%D9%87%D8%AC%D8%A9_%D9%8A%D9%85%D9%86%D9%8A%D8%A9 |
| SRC-YE-LANE-PAGES-MIRROR | C | Old Sanaa and Tahrir lane inventories — encyclopedic mirror pages | Encyclopedic mirror pages citing census 2004 and heritage documentation | — | 2026-08-17 | Factual extraction with attribution; publisher reuse terms not stated | https://ar.wikipedia.org/wiki/%D8%B5%D9%86%D8%B9%D8%A7%D8%A1_%D8%A7%D9%84%D9%82%D8%AF%D9%8A%D9%85%D8%A9 |
| SRC-YE-LAW-31-SOCOTRA-REPORT-2013 | B | Report of Law 31/2013 establishing Socotra Archipelago Governorate | Yafa News, reporting the issued Republic of Yemen law | 2013-12-18 | 2026-08-17 | Factual extraction with attribution; publisher reuse terms not stated | https://yafa-news.net/archives/82470 |
| SRC-YE-NIC-AMANAT-CENSUS-2004 | A | Amanat Al Asimah administrative classification and census 2004 frame | National Information Center Yemen | — | 2026-08-17 | Factual extraction with attribution; publisher reuse terms not stated | http://www.yemen-nic.info/gover/sanaacity/brife/ |
| SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR | C | District catalogue of the Republic of Yemen — encyclopedic mirror of the NIC frame | Marefa encyclopedic mirror citing the National Information Center | — | 2026-08-17 | Factual extraction with attribution; publisher reuse terms not stated | https://www.marefa.org/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D9%85%D8%AF%D9%8A%D8%B1%D9%8A%D8%A7%D8%AA_%D8%A7%D9%84%D8%AC%D9%85%D9%87%D9%88%D8%B1%D9%8A%D8%A9_%D8%A7%D9%84%D9%8A%D9%85%D9%86%D9%8A%D8%A9 |
| SRC-YE-NIC-GOVERNORATES-LEGACY | A | Governorates of the Republic — enumerated legacy catalogue | National Information Center Yemen | — | 2026-08-17 | Factual extraction with attribution; publisher reuse terms not stated | http://www.yemen-nic.info/yemen/gover/ |

---
_مولّد آليًا؛ لا تعدّل هذا الملف مباشرة._
