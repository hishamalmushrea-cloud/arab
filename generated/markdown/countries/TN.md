# تونس (TN) — عرض مولّد من Schema v1

> **حدود التغطية:** التغطية المحلية غير مكتملة. لا تمثل هذه الصفحة جميع المدن أو القرى أو الأحياء أو الحارات، ولا يُستدل على التغطية من وجود ملف. البيانات المنظمة هي المصدر؛ هذه الصفحة عرض مولّد.

## التغطية والمقامات

أي نسبة 100% أدناه مقيدة بالدولة والطبقة والمقام المؤرخ واللقطة والمصدر الظاهرة في الصف نفسه؛ ولا تمتد إلى طبقة أخرى.

| الطبقة | تعريف المقام | المقام | مطابق | غير مطابق | مستبعد | مفقود | النسبة | تاريخ المقام | اللقطة | المصدر | مكتمل | سبب النقص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cities | Officially delimited city/place layer | — | 0 | 1 | 0 | — | — | 2026-08-15 | SNP-MIGRATION-2026-08-15 | — | لا | No official national city denominator and no canonical source for the lone legacy Djerba city row. |
| country_scope | ISO country entity in the project's 22-country scope | 1 | 1 | 0 | 0 | 0 | 100% | 2026-08-15 | SNP-MIGRATION-2026-08-15 | SRC-ISO-3166-1-2020 | نعم | — |
| delegations | Delegations in the official detailed governorate-by-governorate table | 264 | 264 | 0 | 264 | 0 | 100% | 2026-08-15 | SNP-TN-ADMIN-2026-08-15 | SRC-TN-MOI-DELEGATIONS-2013 | نعم | — |
| governorates | Governorates listed in the official detailed table | 24 | 24 | 0 | 24 | 0 | 100% | 2026-08-15 | SNP-TN-ADMIN-2026-08-15 | SRC-TN-MOI-DELEGATIONS-2013 | نعم | — |
| imadas | Territorial sectors (imadas) by governorate and delegation | — | 0 | 0 | 0 | — | — | 2026-08-15 | SNP-MIGRATION-2026-08-15 | SRC-TN-MOI-IMADAS-2013 | لا | No dated national denominator was verified and no imada rows were imported. |
| municipalities_2018 | Municipalities after the 2016 national remapping, as reported in the dated 2018 synthesis | 350 | 0 | 0 | 0 | 350 | 0% | 2018-04-06 | SNP-MIGRATION-2026-08-15 | SRC-TN-DGCL-MUNICIPALITIES-2018 | لا | No municipality entities were present in a source-compliant legacy layer and none were mass-added. |
| populated_settlements | Officially available populated settlements below the declared administrative tiers | — | 0 | 0 | 57 | — | — | 2026-08-15 | SNP-MIGRATION-2026-08-15 | — | لا | No official dated denominator; legacy microplace/cultural rows remain quarantined pending atomic place-level sources. |

## الكيانات

| المعرّف | الاسم | النوع | الحالة | المصدر القانوني/المرجعي | المحدد داخل المصدر |
|---|---|---|---|---|---|
| ENT-TN-COUNTRY | تونس | country | current | SRC-ISO-3166-1-2020 | ISO alpha-2 entry TN |
| ENT-TN-DELEGATION-00555D763B13 | حاسي الفريد | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القصرين; delegation حاسي الفريد |
| ENT-TN-DELEGATION-00E4826B36E2 | سجنان | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بنزرت; delegation سجنان |
| ENT-TN-DELEGATION-00EC6583A4A3 | بني حسان | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المنستير; delegation بني حسان |
| ENT-TN-DELEGATION-00F12985BEC9 | بني خيار | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate نابل; delegation بني خيار |
| ENT-TN-DELEGATION-010FEC49E881 | دوز الجنوبية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قبلي; delegation دوز الجنوبية |
| ENT-TN-DELEGATION-01345A7C882C | المحمدية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بن عروس; delegation المحمدية |
| ENT-TN-DELEGATION-0156C9A906A2 | الوردية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation الوردية |
| ENT-TN-DELEGATION-028DF902ABF9 | نفزة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate باجة; delegation نفزة |
| ENT-TN-DELEGATION-02E328685503 | الصخيرة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate صفاقس; delegation الصخيرة |
| ENT-TN-DELEGATION-0410399059C4 | توزر | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate توزر; delegation توزر |
| ENT-TN-DELEGATION-05852EF74252 | جبنيانة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate صفاقس; delegation جبنيانة |
| ENT-TN-DELEGATION-05AAF8FA23F6 | الزاوية القصيبة الثريات | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سوسة; delegation الزاوية القصيبة الثريات |
| ENT-TN-DELEGATION-05E0AB3C372D | السرس | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate الكاف; delegation السرس |
| ENT-TN-DELEGATION-06F62E53748D | بومهل البساتين | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بن عروس; delegation بومهل البساتين |
| ENT-TN-DELEGATION-08BF6BF26FFF | قفصة الشمالية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قفصة; delegation قفصة الشمالية |
| ENT-TN-DELEGATION-08DFD967FB8E | باجة الجنوبية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate باجة; delegation باجة الجنوبية |
| ENT-TN-DELEGATION-09D1B99F85DC | كسرى | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سليانة; delegation كسرى |
| ENT-TN-DELEGATION-0A43143796F7 | طبرقة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate جندوبة; delegation طبرقة |
| ENT-TN-DELEGATION-0AAD4BD027D5 | الدهماني | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate الكاف; delegation الدهماني |
| ENT-TN-DELEGATION-0B11B353C556 | حي الخضراء | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation حي الخضراء |
| ENT-TN-DELEGATION-0B9CE76F3AD6 | منزل شاكر | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate صفاقس; delegation منزل شاكر |
| ENT-TN-DELEGATION-0E56BD3D1B3A | الزهراء | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بن عروس; delegation الزهراء |
| ENT-TN-DELEGATION-10DD70515DA0 | المدينة الجديدة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بن عروس; delegation المدينة الجديدة |
| ENT-TN-DELEGATION-1172E32A37EA | قصيبة المديوني | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المنستير; delegation قصيبة المديوني |
| ENT-TN-DELEGATION-11CCF21EE571 | رواد | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate أريانة; delegation رواد |
| ENT-TN-DELEGATION-14077DE6F00B | دار شعبان الفهري | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate نابل; delegation دار شعبان الفهري |
| ENT-TN-DELEGATION-148C846991C4 | جومين | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بنزرت; delegation جومين |
| ENT-TN-DELEGATION-14FA2AE0C064 | حمام سوسة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سوسة; delegation حمام سوسة |
| ENT-TN-DELEGATION-15A144D6467E | الحنشة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate صفاقس; delegation الحنشة |
| ENT-TN-DELEGATION-15D8C5E6532A | ذهيبة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تطاوين; delegation ذهيبة |
| ENT-TN-DELEGATION-17B9E0494EC7 | بئر علي بن خليفة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate صفاقس; delegation بئر علي بن خليفة |
| ENT-TN-DELEGATION-17D9D56D8808 | القطار | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قفصة; delegation القطار |
| ENT-TN-DELEGATION-184C444E7833 | جدليان | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القصرين; delegation جدليان |
| ENT-TN-DELEGATION-19EB9068FDEB | حمام الشط | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بن عروس; delegation حمام الشط |
| ENT-TN-DELEGATION-1A266F9B008F | أولاد الشامخ | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المهدية; delegation أولاد الشامخ |
| ENT-TN-DELEGATION-1F3317733151 | سيدي حسين | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation سيدي حسين |
| ENT-TN-DELEGATION-210B7D8A5B50 | جربة أجيم | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate مدنين; delegation جربة أجيم |
| ENT-TN-DELEGATION-21A9D436EAA7 | تمغزة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate توزر; delegation تمغزة |
| ENT-TN-DELEGATION-21E89D9190E3 | سوق الجديد | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سيدي بوزيد; delegation سوق الجديد |
| ENT-TN-DELEGATION-2230C03437B2 | سكرة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate أريانة; delegation سكرة |
| ENT-TN-DELEGATION-22BE73F7EFB2 | باب سويقة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation باب سويقة |
| ENT-TN-DELEGATION-25551A4A8808 | قربة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate نابل; delegation قربة |
| ENT-TN-DELEGATION-2576985BFCE5 | الكرم | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation الكرم |
| ENT-TN-DELEGATION-2592EE0518F8 | الجديدة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate منوبة; delegation الجديدة |
| ENT-TN-DELEGATION-27DFBC8894A9 | لكريب | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سليانة; delegation لكريب |
| ENT-TN-DELEGATION-28027896EDDD | مقرين | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بن عروس; delegation مقرين |
| ENT-TN-DELEGATION-28A3B2254932 | رأس الجبل | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بنزرت; delegation رأس الجبل |
| ENT-TN-DELEGATION-29092E1ECD11 | تاكلسة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate نابل; delegation تاكلسة |
| ENT-TN-DELEGATION-2A637B595634 | ملولش | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المهدية; delegation ملولش |
| ENT-TN-DELEGATION-2D3CF4EC1C11 | غمراسن | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تطاوين; delegation غمراسن |
| ENT-TN-DELEGATION-2F6C05AAB735 | الروحية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سليانة; delegation الروحية |
| ENT-TN-DELEGATION-3178EC239E79 | جبل الجلود | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation جبل الجلود |
| ENT-TN-DELEGATION-3240C5021B36 | دقاش | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate توزر; delegation دقاش |
| ENT-TN-DELEGATION-336FE0336AC9 | المطوية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قابس; delegation المطوية |
| ENT-TN-DELEGATION-3487617C49DD | سوسة المدينة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سوسة; delegation سوسة المدينة |
| ENT-TN-DELEGATION-34E2240B6A54 | مجاز الباب | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate باجة; delegation مجاز الباب |
| ENT-TN-DELEGATION-3512572DC050 | دوز الشمالية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قبلي; delegation دوز الشمالية |
| ENT-TN-DELEGATION-3568AB5821B0 | القيروان الجنوبية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القيروان; delegation القيروان الجنوبية |
| ENT-TN-DELEGATION-36BABB1475F8 | تطاوين الشمالية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تطاوين; delegation تطاوين الشمالية |
| ENT-TN-DELEGATION-36D776E11570 | غار الدماء | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate جندوبة; delegation غار الدماء |
| ENT-TN-DELEGATION-3757F6B83BE1 | ساقية الداير | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate صفاقس; delegation ساقية الداير |
| ENT-TN-DELEGATION-37E43863E13C | سليانة الجنوبية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سليانة; delegation سليانة الجنوبية |
| ENT-TN-DELEGATION-381871ACE873 | منزل الحبيب | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قابس; delegation منزل الحبيب |
| ENT-TN-DELEGATION-386953CDE2D6 | المنستير | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المنستير; delegation المنستير |
| ENT-TN-DELEGATION-390678B1D4C7 | البئر الأحمر | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تطاوين; delegation البئر الأحمر |
| ENT-TN-DELEGATION-39EFA7D5C92F | ماطر | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بنزرت; delegation ماطر |
| ENT-TN-DELEGATION-3C575B9AF71B | المرسى | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation المرسى |
| ENT-TN-DELEGATION-3CEADA31C198 | برقو | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سليانة; delegation برقو |
| ENT-TN-DELEGATION-3D8C44AF7D14 | عين دراهم | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate جندوبة; delegation عين دراهم |
| ENT-TN-DELEGATION-3DDA099AD6C7 | المرناقية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate منوبة; delegation المرناقية |
| ENT-TN-DELEGATION-4021556E2BEF | غزالة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بنزرت; delegation غزالة |
| ENT-TN-DELEGATION-40268C8E9C06 | سيدي البشير | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation سيدي البشير |
| ENT-TN-DELEGATION-40F8C393FB98 | الكاف الغربية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate الكاف; delegation الكاف الغربية |
| ENT-TN-DELEGATION-434F19B638E3 | بلخير | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قفصة; delegation بلخير |
| ENT-TN-DELEGATION-43EBF7A156A6 | الفحص | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate زغوان; delegation الفحص |
| ENT-TN-DELEGATION-44DC92075FFF | سوق الأحد | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قبلي; delegation سوق الأحد |
| ENT-TN-DELEGATION-46D8F9A49020 | الشراردة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القيروان; delegation الشراردة |
| ENT-TN-DELEGATION-46FFC1059453 | الفوار | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قبلي; delegation الفوار |
| ENT-TN-DELEGATION-47EFAA8BC79F | الجم | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المهدية; delegation الجم |
| ENT-TN-DELEGATION-498ED0DE384B | سيدي بوعلي | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سوسة; delegation سيدي بوعلي |
| ENT-TN-DELEGATION-4A4ADB1F39D5 | رمادة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تطاوين; delegation رمادة |
| ENT-TN-DELEGATION-4A822090C35C | سليمان | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate نابل; delegation سليمان |
| ENT-TN-DELEGATION-4AE753194B10 | منزل بوزلفة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate نابل; delegation منزل بوزلفة |
| ENT-TN-DELEGATION-4E58B3CD9CB1 | المكنين | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المنستير; delegation المكنين |
| ENT-TN-DELEGATION-4F055D8E4C5F | حي التضامن | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate أريانة; delegation حي التضامن |
| ENT-TN-DELEGATION-529F20CCEFFA | بنزرت الجنوبية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بنزرت; delegation بنزرت الجنوبية |
| ENT-TN-DELEGATION-52AE19694D81 | فوسانة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القصرين; delegation فوسانة |
| ENT-TN-DELEGATION-533D4E540C29 | نصر الله | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القيروان; delegation نصر الله |
| ENT-TN-DELEGATION-5589DBA6CB89 | صفاقس الغربية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate صفاقس; delegation صفاقس الغربية |
| ENT-TN-DELEGATION-55B6CFADA185 | المتلوي | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قفصة; delegation المتلوي |
| ENT-TN-DELEGATION-57457D07E717 | أم العرائس | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قفصة; delegation أم العرائس |
| ENT-TN-DELEGATION-584902C8EEE0 | جربة حومة السوق | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate مدنين; delegation جربة حومة السوق |
| ENT-TN-DELEGATION-5B401B5FE360 | قابس الجنوبية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قابس; delegation قابس الجنوبية |
| ENT-TN-DELEGATION-5BAD0A66CCEB | الحامة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قابس; delegation الحامة |
| ENT-TN-DELEGATION-5BB9BF889AC5 | مارث | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قابس; delegation مارث |
| ENT-TN-DELEGATION-5C87693EF7C1 | التحرير | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation التحرير |
| ENT-TN-DELEGATION-5CA39F3BFF07 | أكودة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سوسة; delegation أكودة |
| ENT-TN-DELEGATION-5CE249CD9A5F | الغريبة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate صفاقس; delegation الغريبة |
| ENT-TN-DELEGATION-5D1C1977A0A6 | بورويس | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سليانة; delegation بورويس |
| ENT-TN-DELEGATION-5D5CDCB7496E | سيدي علوان | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المهدية; delegation سيدي علوان |
| ENT-TN-DELEGATION-5D62B4C8161F | سبيطلة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القصرين; delegation سبيطلة |
| ENT-TN-DELEGATION-5E40024695DE | غار الملح | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بنزرت; delegation غار الملح |
| ENT-TN-DELEGATION-5E9C54B26170 | العلا | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القيروان; delegation العلا |
| ENT-TN-DELEGATION-6027493801C5 | العمران | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation العمران |
| ENT-TN-DELEGATION-6334381D4972 | منوبة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate منوبة; delegation منوبة |
| ENT-TN-DELEGATION-6417F8B088EB | قصر هلال | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المنستير; delegation قصر هلال |
| ENT-TN-DELEGATION-64B47287C7CC | عمدون | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate باجة; delegation عمدون |
| ENT-TN-DELEGATION-64DB1B613F50 | دوار هيشر | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate منوبة; delegation دوار هيشر |
| ENT-TN-DELEGATION-64DEA9083EA0 | شربان | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المهدية; delegation شربان |
| ENT-TN-DELEGATION-678C562CAA1C | فوشانة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بن عروس; delegation فوشانة |
| ENT-TN-DELEGATION-69C4DE6E547E | منزل بوزيان | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سيدي بوزيد; delegation منزل بوزيان |
| ENT-TN-DELEGATION-6DD1C12A1852 | قليبية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate نابل; delegation قليبية |
| ENT-TN-DELEGATION-6EC1A2137D0E | الوسلاتية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القيروان; delegation الوسلاتية |
| ENT-TN-DELEGATION-6EFE1FF87CAA | جرجيس | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate مدنين; delegation جرجيس |
| ENT-TN-DELEGATION-6F8D6872B9E9 | بئر الحفي | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سيدي بوزيد; delegation بئر الحفي |
| ENT-TN-DELEGATION-706200A5C126 | السواسي | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المهدية; delegation السواسي |
| ENT-TN-DELEGATION-7075A1113804 | قابس المدينة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قابس; delegation قابس المدينة |
| ENT-TN-DELEGATION-70B00114B3C2 | الشبيكة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القيروان; delegation الشبيكة |
| ENT-TN-DELEGATION-714F4FED1031 | البقالطة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المنستير; delegation البقالطة |
| ENT-TN-DELEGATION-755242916060 | الرقاب | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سيدي بوزيد; delegation الرقاب |
| ENT-TN-DELEGATION-762D553CB7DA | الزهور | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القصرين; delegation الزهور |
| ENT-TN-DELEGATION-7667BCFBBD94 | رادس | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بن عروس; delegation رادس |
| ENT-TN-DELEGATION-7893E2F13C86 | هبيرة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المهدية; delegation هبيرة |
| ENT-TN-DELEGATION-78A6B0904A2B | مكثر | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سليانة; delegation مكثر |
| ENT-TN-DELEGATION-7A57DEB42C2E | قفصة الجنوبية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قفصة; delegation قفصة الجنوبية |
| ENT-TN-DELEGATION-7B1B28620EBA | وادي مليز | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate جندوبة; delegation وادي مليز |
| ENT-TN-DELEGATION-7D060F057E64 | قلعة الأندلس | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate أريانة; delegation قلعة الأندلس |
| ENT-TN-DELEGATION-7D47DBFD2C6B | الوردانين | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المنستير; delegation الوردانين |
| ENT-TN-DELEGATION-7D9681B14049 | غنوش | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قابس; delegation غنوش |
| ENT-TN-DELEGATION-7E9A8227F3FE | حفوز | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القيروان; delegation حفوز |
| ENT-TN-DELEGATION-7F9EBE1F4EA1 | صيادة لمطة بوحجر | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المنستير; delegation صيادة لمطة بوحجر |
| ENT-TN-DELEGATION-819F7F2E27F9 | جندوبة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate جندوبة; delegation جندوبة |
| ENT-TN-DELEGATION-82A4AF3884E0 | بني خداش | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate مدنين; delegation بني خداش |
| ENT-TN-DELEGATION-83574F602607 | قبلي الجنوبية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قبلي; delegation قبلي الجنوبية |
| ENT-TN-DELEGATION-8460EAF855E4 | بن عروس | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بن عروس; delegation بن عروس |
| ENT-TN-DELEGATION-8708C7088CBC | قرمبالية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate نابل; delegation قرمبالية |
| ENT-TN-DELEGATION-88077D99D243 | صواف | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate زغوان; delegation صواف |
| ENT-TN-DELEGATION-89139C7B1553 | المزونة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سيدي بوزيد; delegation المزونة |
| ENT-TN-DELEGATION-89B5CE300A2D | باجة الشمالية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate باجة; delegation باجة الشمالية |
| ENT-TN-DELEGATION-8B2B3E3BDE8C | بومرداس | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المهدية; delegation بومرداس |
| ENT-TN-DELEGATION-8B659FB150BF | العيون | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القصرين; delegation العيون |
| ENT-TN-DELEGATION-8C1A5CC41315 | القصر | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قفصة; delegation القصر |
| ENT-TN-DELEGATION-8CAB25CD1628 | البطان | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate منوبة; delegation البطان |
| ENT-TN-DELEGATION-8CCC58460F99 | الميدة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate نابل; delegation الميدة |
| ENT-TN-DELEGATION-8CD3CBC66F17 | قصور الساف | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المهدية; delegation قصور الساف |
| ENT-TN-DELEGATION-907386F80604 | أريانة المدينة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate أريانة; delegation أريانة المدينة |
| ENT-TN-DELEGATION-909BD4DC039A | نابل | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate نابل; delegation نابل |
| ENT-TN-DELEGATION-920707B361CE | أوتيك | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بنزرت; delegation أوتيك |
| ENT-TN-DELEGATION-93C5837DFCBF | باردو | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation باردو |
| ENT-TN-DELEGATION-9571A404E72D | الصمار | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تطاوين; delegation الصمار |
| ENT-TN-DELEGATION-9846A16575C2 | المكناسي | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سيدي بوزيد; delegation المكناسي |
| ENT-TN-DELEGATION-996BCFD91FDD | مطماطة الجديدة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قابس; delegation مطماطة الجديدة |
| ENT-TN-DELEGATION-997BFDED88CF | بوسالم | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate جندوبة; delegation بوسالم |
| ENT-TN-DELEGATION-99CBAA7046B8 | طبربة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate منوبة; delegation طبربة |
| ENT-TN-DELEGATION-99EBA5A17CB9 | طينة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate صفاقس; delegation طينة |
| ENT-TN-DELEGATION-9AB968FD4EE0 | تالة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القصرين; delegation تالة |
| ENT-TN-DELEGATION-9ADFA1D292D9 | مساكن | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سوسة; delegation مساكن |
| ENT-TN-DELEGATION-9BE55C4562EE | السيجومي | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation السيجومي |
| ENT-TN-DELEGATION-9CCDCAF94A4A | القيروان الشمالية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القيروان; delegation القيروان الشمالية |
| ENT-TN-DELEGATION-9D12AE8B04F4 | الجريصة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate الكاف; delegation الجريصة |
| ENT-TN-DELEGATION-9D23A36B72E1 | جمال | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المنستير; delegation جمال |
| ENT-TN-DELEGATION-9D652FC873EB | سوسة جوهرة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سوسة; delegation سوسة جوهرة |
| ENT-TN-DELEGATION-9F59B0DA797D | وادي الليل | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate منوبة; delegation وادي الليل |
| ENT-TN-DELEGATION-A16A1E882313 | الرديف | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قفصة; delegation الرديف |
| ENT-TN-DELEGATION-A1AD72837943 | بلطة بوعوان | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate جندوبة; delegation بلطة بوعوان |
| ENT-TN-DELEGATION-A20DE8BF6185 | سيدي عيش | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قفصة; delegation سيدي عيش |
| ENT-TN-DELEGATION-A2C2D831ECC0 | جندوبة الشمالية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate جندوبة; delegation جندوبة الشمالية |
| ENT-TN-DELEGATION-A43DBAE26B8A | صفاقس المدينة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate صفاقس; delegation صفاقس المدينة |
| ENT-TN-DELEGATION-A5B79B7F0981 | سيدي علي بن عون | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سيدي بوزيد; delegation سيدي علي بن عون |
| ENT-TN-DELEGATION-A638A51CF8F7 | المظيلة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قفصة; delegation المظيلة |
| ENT-TN-DELEGATION-A6449AC11294 | حمام الأنف | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بن عروس; delegation حمام الأنف |
| ENT-TN-DELEGATION-A6D2E459547E | السبيخة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القيروان; delegation السبيخة |
| ENT-TN-DELEGATION-A8FC78D96A53 | برج العامري | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate منوبة; delegation برج العامري |
| ENT-TN-DELEGATION-A9463801F6AD | ماجل بلعباس | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القصرين; delegation ماجل بلعباس |
| ENT-TN-DELEGATION-A97443748914 | تبرسق | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate باجة; delegation تبرسق |
| ENT-TN-DELEGATION-A9A2E64081DA | حاجب العيون | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القيروان; delegation حاجب العيون |
| ENT-TN-DELEGATION-A9FD50013858 | بنبلة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المنستير; delegation بنبلة |
| ENT-TN-DELEGATION-AADE7E444312 | بنزرت الشمالية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بنزرت; delegation بنزرت الشمالية |
| ENT-TN-DELEGATION-AC41B378E3D9 | النفيضة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سوسة; delegation النفيضة |
| ENT-TN-DELEGATION-ACB1178786DC | الهوارية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate نابل; delegation الهوارية |
| ENT-TN-DELEGATION-AD509F0A9D79 | سبالة أولاد عسكر | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سيدي بوزيد; delegation سبالة أولاد عسكر |
| ENT-TN-DELEGATION-AF66ED06B9B8 | قعفور | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سليانة; delegation قعفور |
| ENT-TN-DELEGATION-AFAE2BE79F31 | قابس الغربية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قابس; delegation قابس الغربية |
| ENT-TN-DELEGATION-AFCCE19F1CD3 | بوعرقوب | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate نابل; delegation بوعرقوب |
| ENT-TN-DELEGATION-B06C74E3ED6B | السند | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قفصة; delegation السند |
| ENT-TN-DELEGATION-B0C081DB1344 | الساحلين | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المنستير; delegation الساحلين |
| ENT-TN-DELEGATION-B117D836FA70 | مدنين الجنوبية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate مدنين; delegation مدنين الجنوبية |
| ENT-TN-DELEGATION-B1DB2FE90D10 | عقارب | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate صفاقس; delegation عقارب |
| ENT-TN-DELEGATION-B426671C7506 | المنزه | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation المنزه |
| ENT-TN-DELEGATION-B5CD972E98C1 | سيدي بوزيد الشرقية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سيدي بوزيد; delegation سيدي بوزيد الشرقية |
| ENT-TN-DELEGATION-B63E32B2BC3F | جلمة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سيدي بوزيد; delegation جلمة |
| ENT-TN-DELEGATION-B8BFE8FFB2B8 | المروج | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بن عروس; delegation المروج |
| ENT-TN-DELEGATION-B95D26E1207F | الحمامات | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate نابل; delegation الحمامات |
| ENT-TN-DELEGATION-BACCAA713057 | سليانة الشمالية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سليانة; delegation سليانة الشمالية |
| ENT-TN-DELEGATION-BDF031A58E55 | طبلبة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المنستير; delegation طبلبة |
| ENT-TN-DELEGATION-BE40270E2393 | المحرس | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate صفاقس; delegation المحرس |
| ENT-TN-DELEGATION-BE50E5DE6BD2 | العروسة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سليانة; delegation العروسة |
| ENT-TN-DELEGATION-BFF07C1D0C4A | كندار | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سوسة; delegation كندار |
| ENT-TN-DELEGATION-C12FC68E8013 | بني خلاد | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate نابل; delegation بني خلاد |
| ENT-TN-DELEGATION-C151EAFA4BD1 | قلعة سنان | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate الكاف; delegation قلعة سنان |
| ENT-TN-DELEGATION-C2548493A23C | الشابة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المهدية; delegation الشابة |
| ENT-TN-DELEGATION-C41B01AE892E | فريانة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القصرين; delegation فريانة |
| ENT-TN-DELEGATION-C433D277206E | سوسة سيدي عبد الحميد | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سوسة; delegation سوسة سيدي عبد الحميد |
| ENT-TN-DELEGATION-C73B8495072E | الزريبة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate زغوان; delegation الزريبة |
| ENT-TN-DELEGATION-C7B4FEE5AE08 | منزل تميم | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate نابل; delegation منزل تميم |
| ENT-TN-DELEGATION-C93CA450F43B | حلق الوادي | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation حلق الوادي |
| ENT-TN-DELEGATION-CA29D85670F9 | القلعة الكبرى | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سوسة; delegation القلعة الكبرى |
| ENT-TN-DELEGATION-CB0D8DF8758C | العالية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بنزرت; delegation العالية |
| ENT-TN-DELEGATION-CB23A7885CA7 | نفطة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate توزر; delegation نفطة |
| ENT-TN-DELEGATION-CC12560912DD | المدينة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation المدينة |
| ENT-TN-DELEGATION-CC185FFE164C | المنيهلة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate أريانة; delegation المنيهلة |
| ENT-TN-DELEGATION-CC6DBA2640FB | صفاقس الجنوبية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate صفاقس; delegation صفاقس الجنوبية |
| ENT-TN-DELEGATION-CCDB3F1D6604 | تستور | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate باجة; delegation تستور |
| ENT-TN-DELEGATION-CEF958458571 | قرطاج | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation قرطاج |
| ENT-TN-DELEGATION-D06EBCEA26BA | بوفيشة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سوسة; delegation بوفيشة |
| ENT-TN-DELEGATION-D2E46DB3C8BC | القلعة الخصبة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate الكاف; delegation القلعة الخصبة |
| ENT-TN-DELEGATION-D3ABF7936ACA | تطاوين الجنوبية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تطاوين; delegation تطاوين الجنوبية |
| ENT-TN-DELEGATION-D4441080949B | الكاف الشرقية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate الكاف; delegation الكاف الشرقية |
| ENT-TN-DELEGATION-D4FC46D8AB0D | مرناق | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بن عروس; delegation مرناق |
| ENT-TN-DELEGATION-D52472FD9496 | زغوان | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate زغوان; delegation زغوان |
| ENT-TN-DELEGATION-D555F337D568 | حيدرة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القصرين; delegation حيدرة |
| ENT-TN-DELEGATION-D592FC6CD4D2 | الكبارية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation الكبارية |
| ENT-TN-DELEGATION-D59DE8736127 | حمام الأغزاز | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate نابل; delegation حمام الأغزاز |
| ENT-TN-DELEGATION-D75198EE6BB5 | الزهور | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation الزهور |
| ENT-TN-DELEGATION-D77747883E55 | ساقية سيدي يوسف | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate الكاف; delegation ساقية سيدي يوسف |
| ENT-TN-DELEGATION-D8723103173B | العامرة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate صفاقس; delegation العامرة |
| ENT-TN-DELEGATION-DAC482090AC5 | حزوة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate توزر; delegation حزوة |
| ENT-TN-DELEGATION-DB05A1325AE3 | سيدي بوزيد الغربية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سيدي بوزيد; delegation سيدي بوزيد الغربية |
| ENT-TN-DELEGATION-DEB9F3EFCD2D | قبلي الشمالية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قبلي; delegation قبلي الشمالية |
| ENT-TN-DELEGATION-E3E9C5077EA4 | القصور | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate الكاف; delegation القصور |
| ENT-TN-DELEGATION-E401587A83A1 | سيدي الهاني | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سوسة; delegation سيدي الهاني |
| ENT-TN-DELEGATION-E45902371203 | أولاد حفوز | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سيدي بوزيد; delegation أولاد حفوز |
| ENT-TN-DELEGATION-E56B524C71BE | المهدية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المهدية; delegation المهدية |
| ENT-TN-DELEGATION-E6F9AC3B6A1F | بوعرادة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سليانة; delegation بوعرادة |
| ENT-TN-DELEGATION-E83D07EB9C29 | قرقنة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate صفاقس; delegation قرقنة |
| ENT-TN-DELEGATION-E8E2CE15323A | قبلاط | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate باجة; delegation قبلاط |
| ENT-TN-DELEGATION-E8E567F03E9D | تيبار | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate باجة; delegation تيبار |
| ENT-TN-DELEGATION-E8F02D6B4EF9 | القلعة الصغرى | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سوسة; delegation القلعة الصغرى |
| ENT-TN-DELEGATION-EA875BA2BFE0 | ساقية الزيت | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate صفاقس; delegation ساقية الزيت |
| ENT-TN-DELEGATION-ECE5F1EB80F4 | الناظور | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate زغوان; delegation الناظور |
| ENT-TN-DELEGATION-EE60D65B9935 | مدنين الشمالية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate مدنين; delegation مدنين الشمالية |
| ENT-TN-DELEGATION-EE9A7B5ED169 | سيدي ثابت | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate أريانة; delegation سيدي ثابت |
| ENT-TN-DELEGATION-EF5957AC15F4 | هرقلة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سوسة; delegation هرقلة |
| ENT-TN-DELEGATION-EFAC1514C55E | زرمدين | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate المنستير; delegation زرمدين |
| ENT-TN-DELEGATION-F0023FB066A4 | سوسة الرياض | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate سوسة; delegation سوسة الرياض |
| ENT-TN-DELEGATION-F0E269317685 | القصرين الشمالية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القصرين; delegation القصرين الشمالية |
| ENT-TN-DELEGATION-F12F59DBC46E | فرنانة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate جندوبة; delegation فرنانة |
| ENT-TN-DELEGATION-F153AA210A4D | نبر | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate الكاف; delegation نبر |
| ENT-TN-DELEGATION-F3529789545D | منزل بورقيبة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بنزرت; delegation منزل بورقيبة |
| ENT-TN-DELEGATION-F66C4659B2C0 | جربة ميدون | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate مدنين; delegation جربة ميدون |
| ENT-TN-DELEGATION-F68992D7EA16 | العمران الأعلى | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation العمران الأعلى |
| ENT-TN-DELEGATION-F6FA367C4B52 | سيدي مخلوف | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate مدنين; delegation سيدي مخلوف |
| ENT-TN-DELEGATION-F7614EE1CE5C | مطماطة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate قابس; delegation مطماطة |
| ENT-TN-DELEGATION-F7ED1EE6DC53 | منزل جميل | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بنزرت; delegation منزل جميل |
| ENT-TN-DELEGATION-F7ED4B759BD6 | بن قردان | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate مدنين; delegation بن قردان |
| ENT-TN-DELEGATION-F9557E5DC693 | بوحجلة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القيروان; delegation بوحجلة |
| ENT-TN-DELEGATION-FA7572893BAA | القصرين الجنوبية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القصرين; delegation القصرين الجنوبية |
| ENT-TN-DELEGATION-FCEB64E05ED0 | جرزونة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بنزرت; delegation جرزونة |
| ENT-TN-DELEGATION-FD2AE43A4C3D | سبيبة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate القصرين; delegation سبيبة |
| ENT-TN-DELEGATION-FE081F997DC5 | الحرائرية | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation الحرائرية |
| ENT-TN-DELEGATION-FE6A0D05DF67 | بئر مشارقة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate زغوان; delegation بئر مشارقة |
| ENT-TN-DELEGATION-FE7ADA16AB50 | باب البحر | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate تونس; delegation باب البحر |
| ENT-TN-DELEGATION-FF2BD30691C0 | تاجروين | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate الكاف; delegation تاجروين |
| ENT-TN-DELEGATION-FFE2346B14CF | تينجة | tn_delegation | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate بنزرت; delegation تينجة |
| ENT-TN-GOVERNORATE-07DB5E6D265C | سوسة | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: سوسة |
| ENT-TN-GOVERNORATE-0D738EAC753C | الكاف | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: الكاف |
| ENT-TN-GOVERNORATE-1864AE41D5B4 | قبلي | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: قبلي |
| ENT-TN-GOVERNORATE-36E4260B310C | القصرين | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: القصرين |
| ENT-TN-GOVERNORATE-467CAA2B1928 | قفصة | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: قفصة |
| ENT-TN-GOVERNORATE-47F772AA4A84 | سيدي بوزيد | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: سيدي بوزيد |
| ENT-TN-GOVERNORATE-5BC9A7217C8C | المنستير | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: المنستير |
| ENT-TN-GOVERNORATE-78D6D85AF6A0 | أريانة | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: أريانة |
| ENT-TN-GOVERNORATE-7A4D0C3A889C | جندوبة | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: جندوبة |
| ENT-TN-GOVERNORATE-81845FB6BE40 | زغوان | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: زغوان |
| ENT-TN-GOVERNORATE-902616FE3988 | مدنين | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: مدنين |
| ENT-TN-GOVERNORATE-97D2B1489F90 | صفاقس | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: صفاقس |
| ENT-TN-GOVERNORATE-A460B4F223EB | سليانة | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: سليانة |
| ENT-TN-GOVERNORATE-B1787F907937 | بنزرت | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: بنزرت |
| ENT-TN-GOVERNORATE-CC06DF550344 | منوبة | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: منوبة |
| ENT-TN-GOVERNORATE-D28A09D558AD | القيروان | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: القيروان |
| ENT-TN-GOVERNORATE-D5ED89886664 | بن عروس | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: بن عروس |
| ENT-TN-GOVERNORATE-D7972CC63F7E | توزر | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: توزر |
| ENT-TN-GOVERNORATE-DAC2A2592975 | تطاوين | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: تطاوين |
| ENT-TN-GOVERNORATE-DB8D5C457676 | تونس | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: تونس |
| ENT-TN-GOVERNORATE-DF747014232C | قابس | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: قابس |
| ENT-TN-GOVERNORATE-E7D96FEF5043 | المهدية | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: المهدية |
| ENT-TN-GOVERNORATE-EA2D44B4F25E | باجة | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: باجة |
| ENT-TN-GOVERNORATE-EA30E853F598 | نابل | tn_governorate | current | SRC-TN-MOI-DELEGATIONS-2013 | Governorate row: نابل |

## الأسماء البديلة

| المعرّف | الكيان | الاسم | اللغة | النوع | المصدر |
|---|---|---|---|---|---|
| ALS-31E885FF7E5B58E0 | ENT-TN-GOVERNORATE-DAC2A2592975 | Tataouine | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-33BEDB52495E529F | ENT-TN-COUNTRY | Tunisia | en | english | SRC-ISO-3166-1-2020 |
| ALS-376D1A7D26775068 | ENT-TN-GOVERNORATE-07DB5E6D265C | Sousse | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-3D23716770A05FBD | ENT-TN-GOVERNORATE-7A4D0C3A889C | Jendouba | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-4B03E9EBE9CD595D | ENT-TN-GOVERNORATE-CC06DF550344 | Manouba | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-5F2083C63B1E5C5C | ENT-TN-GOVERNORATE-0D738EAC753C | Le Kef | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-6364872D7FEF5635 | ENT-TN-GOVERNORATE-36E4260B310C | Kasserine | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-63B773E11C405B03 | ENT-TN-GOVERNORATE-467CAA2B1928 | Gafsa | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-65DAC7046AB05D2A | ENT-TN-GOVERNORATE-81845FB6BE40 | Zaghouan | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-6D07DB7131AA5FCB | ENT-TN-GOVERNORATE-B1787F907937 | Bizerte | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-705DF3E503935E0A | ENT-TN-GOVERNORATE-1864AE41D5B4 | Kébili | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-77976CD893CA5023 | ENT-TN-GOVERNORATE-D5ED89886664 | Ben Arous | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-7D312CBDBD745402 | ENT-TN-GOVERNORATE-47F772AA4A84 | Sidi Bouzid | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-95E7AA120D3157F0 | ENT-TN-GOVERNORATE-A460B4F223EB | Siliana | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-B087C05516625DCD | ENT-TN-GOVERNORATE-DF747014232C | Gabès | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-B29DD9A2F9235C0A | ENT-TN-GOVERNORATE-78D6D85AF6A0 | Ariana | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-BADFA9AAE724503A | ENT-TN-GOVERNORATE-E7D96FEF5043 | Mahdia | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-C403152AA07C5A77 | ENT-TN-GOVERNORATE-EA2D44B4F25E | Béja | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-E0B5680387745246 | ENT-TN-GOVERNORATE-97D2B1489F90 | Sfax | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-E26A416CE72A556C | ENT-TN-GOVERNORATE-902616FE3988 | Médenine | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-E86630D3C7BA544D | ENT-TN-GOVERNORATE-D28A09D558AD | Kairouan | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-EA5711FEAC1456B1 | ENT-TN-GOVERNORATE-5BC9A7217C8C | Monastir | und | transliteration | SRC-TN-INS-RGPH-2014 |
| ALS-F4943BA428DC5BBD | ENT-TN-GOVERNORATE-D7972CC63F7E | Tozeur | und | transliteration | SRC-TN-INS-RGPH-2014 |

## علاقات الإدارة/الموقع

| المعرّف | الابن | الأب | العلاقة | الحالة | المصدر |
|---|---|---|---|---|---|
| REL-0065F972C22954F4 | ENT-TN-DELEGATION-D52472FD9496 | ENT-TN-GOVERNORATE-81845FB6BE40 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-00A92B936ACE54EB | ENT-TN-DELEGATION-909BD4DC039A | ENT-TN-GOVERNORATE-EA30E853F598 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-00EA34FF244F57FA | ENT-TN-DELEGATION-27DFBC8894A9 | ENT-TN-GOVERNORATE-A460B4F223EB | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-00F7274A59A65617 | ENT-TN-DELEGATION-D555F337D568 | ENT-TN-GOVERNORATE-36E4260B310C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-012696ED8FD25F91 | ENT-TN-DELEGATION-69C4DE6E547E | ENT-TN-GOVERNORATE-47F772AA4A84 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-014E7E8C4F575D50 | ENT-TN-DELEGATION-5E40024695DE | ENT-TN-GOVERNORATE-B1787F907937 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-01BEC31D05BB595A | ENT-TN-DELEGATION-533D4E540C29 | ENT-TN-GOVERNORATE-D28A09D558AD | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-01D9F8CBFF7C57BE | ENT-TN-DELEGATION-21A9D436EAA7 | ENT-TN-GOVERNORATE-D7972CC63F7E | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-01EA2B89EA0E56AD | ENT-TN-GOVERNORATE-07DB5E6D265C | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-02E83CDF18CD562B | ENT-TN-GOVERNORATE-47F772AA4A84 | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-0392FE60A7565CD6 | ENT-TN-DELEGATION-F9557E5DC693 | ENT-TN-GOVERNORATE-D28A09D558AD | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-054F0E61DA695CDA | ENT-TN-DELEGATION-2F6C05AAB735 | ENT-TN-GOVERNORATE-A460B4F223EB | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-06BBB552AB3F5D6E | ENT-TN-DELEGATION-A1AD72837943 | ENT-TN-GOVERNORATE-7A4D0C3A889C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-09A6EFFBA88C53F2 | ENT-TN-DELEGATION-A16A1E882313 | ENT-TN-GOVERNORATE-467CAA2B1928 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-09E1DAFC56575625 | ENT-TN-DELEGATION-09D1B99F85DC | ENT-TN-GOVERNORATE-A460B4F223EB | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-0A8646B1D34B5B06 | ENT-TN-DELEGATION-A8FC78D96A53 | ENT-TN-GOVERNORATE-CC06DF550344 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-0B9B5DA16D825912 | ENT-TN-DELEGATION-BE40270E2393 | ENT-TN-GOVERNORATE-97D2B1489F90 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-0BB08C783C2E59DB | ENT-TN-GOVERNORATE-D28A09D558AD | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-0BC65830B22A5C7F | ENT-TN-DELEGATION-15A144D6467E | ENT-TN-GOVERNORATE-97D2B1489F90 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-0D3A7057F9B85C3A | ENT-TN-DELEGATION-93C5837DFCBF | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-0F1CC81B870A5161 | ENT-TN-DELEGATION-52AE19694D81 | ENT-TN-GOVERNORATE-36E4260B310C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-10DA47F0909C5E89 | ENT-TN-DELEGATION-14FA2AE0C064 | ENT-TN-GOVERNORATE-07DB5E6D265C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-110F03AC15915B60 | ENT-TN-DELEGATION-CB23A7885CA7 | ENT-TN-GOVERNORATE-D7972CC63F7E | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-112553D6BB6B59B3 | ENT-TN-DELEGATION-8B2B3E3BDE8C | ENT-TN-GOVERNORATE-E7D96FEF5043 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-14200CE4B01F5A88 | ENT-TN-DELEGATION-A638A51CF8F7 | ENT-TN-GOVERNORATE-467CAA2B1928 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-15004C6BADB05F70 | ENT-TN-DELEGATION-7075A1113804 | ENT-TN-GOVERNORATE-DF747014232C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-1675FE4C9E3C56CF | ENT-TN-DELEGATION-9F59B0DA797D | ENT-TN-GOVERNORATE-CC06DF550344 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-174F37E614ED5DC7 | ENT-TN-DELEGATION-7B1B28620EBA | ENT-TN-GOVERNORATE-7A4D0C3A889C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-18B23DB4CA0C5797 | ENT-TN-GOVERNORATE-DB8D5C457676 | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-1A41DD1E353E5733 | ENT-TN-DELEGATION-FCEB64E05ED0 | ENT-TN-GOVERNORATE-B1787F907937 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-1AC0FD1127D650EA | ENT-TN-DELEGATION-F68992D7EA16 | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-1BB9B7182CD05DF0 | ENT-TN-DELEGATION-A2C2D831ECC0 | ENT-TN-GOVERNORATE-7A4D0C3A889C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-1C4135585F2F5AA2 | ENT-TN-DELEGATION-9CCDCAF94A4A | ENT-TN-GOVERNORATE-D28A09D558AD | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-1D58754B95925300 | ENT-TN-DELEGATION-8B659FB150BF | ENT-TN-GOVERNORATE-36E4260B310C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-1DCC79316ADA585B | ENT-TN-DELEGATION-9571A404E72D | ENT-TN-GOVERNORATE-DAC2A2592975 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-1DFE9FD3E9465734 | ENT-TN-DELEGATION-8460EAF855E4 | ENT-TN-GOVERNORATE-D5ED89886664 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-1E6E01560F765F47 | ENT-TN-DELEGATION-5CE249CD9A5F | ENT-TN-GOVERNORATE-97D2B1489F90 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-1EB61462BE0D5B18 | ENT-TN-DELEGATION-9AB968FD4EE0 | ENT-TN-GOVERNORATE-36E4260B310C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-2106629697635B98 | ENT-TN-DELEGATION-B117D836FA70 | ENT-TN-GOVERNORATE-902616FE3988 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-21378F00249553BE | ENT-TN-DELEGATION-7D47DBFD2C6B | ENT-TN-GOVERNORATE-5BC9A7217C8C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-214FEF19B23B53F2 | ENT-TN-DELEGATION-381871ACE873 | ENT-TN-GOVERNORATE-DF747014232C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-229E5BD15CC25296 | ENT-TN-DELEGATION-A20DE8BF6185 | ENT-TN-GOVERNORATE-467CAA2B1928 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-24062C46405F5187 | ENT-TN-DELEGATION-06F62E53748D | ENT-TN-GOVERNORATE-D5ED89886664 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-248FD8AD08A75853 | ENT-TN-DELEGATION-755242916060 | ENT-TN-GOVERNORATE-47F772AA4A84 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-25B41B95C84A537B | ENT-TN-DELEGATION-FFE2346B14CF | ENT-TN-GOVERNORATE-B1787F907937 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-2877224DEEE0536B | ENT-TN-DELEGATION-29092E1ECD11 | ENT-TN-GOVERNORATE-EA30E853F598 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-28D785CB42CB5B4A | ENT-TN-DELEGATION-390678B1D4C7 | ENT-TN-GOVERNORATE-DAC2A2592975 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-29AD7D693A0C54F7 | ENT-TN-DELEGATION-5BB9BF889AC5 | ENT-TN-GOVERNORATE-DF747014232C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-2A9535C9C5895AE0 | ENT-TN-GOVERNORATE-97D2B1489F90 | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-2B08AB1877515463 | ENT-TN-DELEGATION-CCDB3F1D6604 | ENT-TN-GOVERNORATE-EA2D44B4F25E | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-2BF1693B5BB656DC | ENT-TN-DELEGATION-88077D99D243 | ENT-TN-GOVERNORATE-81845FB6BE40 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-2C3A6468711C5315 | ENT-TN-DELEGATION-B1DB2FE90D10 | ENT-TN-GOVERNORATE-97D2B1489F90 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-2C4DF12F054D55BE | ENT-TN-DELEGATION-02E328685503 | ENT-TN-GOVERNORATE-97D2B1489F90 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-2DF828229F0151EC | ENT-TN-DELEGATION-E401587A83A1 | ENT-TN-GOVERNORATE-07DB5E6D265C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-2EDE1C4A90F55508 | ENT-TN-DELEGATION-3512572DC050 | ENT-TN-GOVERNORATE-1864AE41D5B4 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-30B1D63B9B6F51A7 | ENT-TN-DELEGATION-9BE55C4562EE | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-342B302CC4995151 | ENT-TN-DELEGATION-78A6B0904A2B | ENT-TN-GOVERNORATE-A460B4F223EB | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-34C58F0576C85A5D | ENT-TN-GOVERNORATE-0D738EAC753C | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-364902FACFEA5C54 | ENT-TN-DELEGATION-7E9A8227F3FE | ENT-TN-GOVERNORATE-D28A09D558AD | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-37159CE76025564B | ENT-TN-DELEGATION-8C1A5CC41315 | ENT-TN-GOVERNORATE-467CAA2B1928 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-38FDB77CD5B95DB8 | ENT-TN-DELEGATION-6EFE1FF87CAA | ENT-TN-GOVERNORATE-902616FE3988 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-39832D8D712A5205 | ENT-TN-DELEGATION-01345A7C882C | ENT-TN-GOVERNORATE-D5ED89886664 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-39EEE709428B5CD6 | ENT-TN-DELEGATION-08DFD967FB8E | ENT-TN-GOVERNORATE-EA2D44B4F25E | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-3A160DDD8B405081 | ENT-TN-DELEGATION-D3ABF7936ACA | ENT-TN-GOVERNORATE-DAC2A2592975 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-3C9D1B4492915876 | ENT-TN-DELEGATION-F7614EE1CE5C | ENT-TN-GOVERNORATE-DF747014232C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-3CFDED089F085EA9 | ENT-TN-DELEGATION-AADE7E444312 | ENT-TN-GOVERNORATE-B1787F907937 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-3E28D87F8D195F6E | ENT-TN-DELEGATION-EA875BA2BFE0 | ENT-TN-GOVERNORATE-97D2B1489F90 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-3F568B2DFFDF5E8E | ENT-TN-DELEGATION-89B5CE300A2D | ENT-TN-GOVERNORATE-EA2D44B4F25E | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-3FBE0AEA66095F26 | ENT-TN-DELEGATION-6027493801C5 | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-3FEE7652FA5D5B10 | ENT-TN-DELEGATION-5D62B4C8161F | ENT-TN-GOVERNORATE-36E4260B310C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-400F842AFE7B5D95 | ENT-TN-DELEGATION-FD2AE43A4C3D | ENT-TN-GOVERNORATE-36E4260B310C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-428C862B0F0B5595 | ENT-TN-DELEGATION-0A43143796F7 | ENT-TN-GOVERNORATE-7A4D0C3A889C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-42F097F0E6CC518C | ENT-TN-DELEGATION-BFF07C1D0C4A | ENT-TN-GOVERNORATE-07DB5E6D265C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-434C627B3EF05DED | ENT-TN-GOVERNORATE-5BC9A7217C8C | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-43E3F2D831315DE5 | ENT-TN-DELEGATION-4A4ADB1F39D5 | ENT-TN-GOVERNORATE-DAC2A2592975 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-45F170C8AFF05EF0 | ENT-TN-DELEGATION-2576985BFCE5 | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-467788937389505B | ENT-TN-DELEGATION-CC12560912DD | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-47C38EB02F975289 | ENT-TN-DELEGATION-99CBAA7046B8 | ENT-TN-GOVERNORATE-CC06DF550344 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-4863DBECDDED5F3F | ENT-TN-DELEGATION-A6449AC11294 | ENT-TN-GOVERNORATE-D5ED89886664 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-48CB0773913C55D8 | ENT-TN-GOVERNORATE-D7972CC63F7E | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-4B8D341C9C7A52A8 | ENT-TN-DELEGATION-55B6CFADA185 | ENT-TN-GOVERNORATE-467CAA2B1928 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-4D6F85A2BA625749 | ENT-TN-DELEGATION-7D060F057E64 | ENT-TN-GOVERNORATE-78D6D85AF6A0 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-4E220E17A8AF5EEB | ENT-TN-DELEGATION-22BE73F7EFB2 | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-50D133C816CB5182 | ENT-TN-DELEGATION-15D8C5E6532A | ENT-TN-GOVERNORATE-DAC2A2592975 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-50EB3F92DF555A25 | ENT-TN-DELEGATION-5C87693EF7C1 | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-50F35549600D5CB2 | ENT-TN-DELEGATION-6334381D4972 | ENT-TN-GOVERNORATE-CC06DF550344 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-5103E830B7725310 | ENT-TN-DELEGATION-5D1C1977A0A6 | ENT-TN-GOVERNORATE-A460B4F223EB | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-5106CE96CAA1598E | ENT-TN-DELEGATION-C12FC68E8013 | ENT-TN-GOVERNORATE-EA30E853F598 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-517D86F1DCDA58CC | ENT-TN-DELEGATION-F6FA367C4B52 | ENT-TN-GOVERNORATE-902616FE3988 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-53E85539D92D5BFC | ENT-TN-DELEGATION-0AAD4BD027D5 | ENT-TN-GOVERNORATE-0D738EAC753C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-5444FBB34ABE5080 | ENT-TN-DELEGATION-819F7F2E27F9 | ENT-TN-GOVERNORATE-7A4D0C3A889C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-5516B09584315F0C | ENT-TN-DELEGATION-2592EE0518F8 | ENT-TN-GOVERNORATE-CC06DF550344 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-55CEDD36DCF15842 | ENT-TN-DELEGATION-FF2BD30691C0 | ENT-TN-GOVERNORATE-0D738EAC753C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-56DFD4435EAC53AF | ENT-TN-DELEGATION-714F4FED1031 | ENT-TN-GOVERNORATE-5BC9A7217C8C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-57CEA641CD2453D0 | ENT-TN-DELEGATION-89139C7B1553 | ENT-TN-GOVERNORATE-47F772AA4A84 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-57EC604463835942 | ENT-TN-DELEGATION-64DEA9083EA0 | ENT-TN-GOVERNORATE-E7D96FEF5043 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-5828D5E315DF5F66 | ENT-TN-DELEGATION-E8E2CE15323A | ENT-TN-GOVERNORATE-EA2D44B4F25E | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-5855C46F06165260 | ENT-TN-DELEGATION-2D3CF4EC1C11 | ENT-TN-GOVERNORATE-DAC2A2592975 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-5B8F2080FF985B77 | ENT-TN-DELEGATION-14077DE6F00B | ENT-TN-GOVERNORATE-EA30E853F598 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-5D4FB569454C5D5E | ENT-TN-DELEGATION-0410399059C4 | ENT-TN-GOVERNORATE-D7972CC63F7E | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-5D8F7A564A375094 | ENT-TN-DELEGATION-17D9D56D8808 | ENT-TN-GOVERNORATE-467CAA2B1928 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-5DC4D2ECFE615AA4 | ENT-TN-DELEGATION-7893E2F13C86 | ENT-TN-GOVERNORATE-E7D96FEF5043 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-5DE5E71A7E9E5072 | ENT-TN-DELEGATION-39EFA7D5C92F | ENT-TN-GOVERNORATE-B1787F907937 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-5E4ED03143E45ED7 | ENT-TN-DELEGATION-010FEC49E881 | ENT-TN-GOVERNORATE-1864AE41D5B4 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-5EC2067FCE35558A | ENT-TN-DELEGATION-3DDA099AD6C7 | ENT-TN-GOVERNORATE-CC06DF550344 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-5EF42113211E56C3 | ENT-TN-DELEGATION-FA7572893BAA | ENT-TN-GOVERNORATE-36E4260B310C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-5EFE70FFC8975B18 | ENT-TN-DELEGATION-F7ED1EE6DC53 | ENT-TN-GOVERNORATE-B1787F907937 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-60169A0E9F0050E1 | ENT-TN-DELEGATION-A9FD50013858 | ENT-TN-GOVERNORATE-5BC9A7217C8C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-6020647418575186 | ENT-TN-DELEGATION-E45902371203 | ENT-TN-GOVERNORATE-47F772AA4A84 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-602E245892A7508B | ENT-TN-DELEGATION-3487617C49DD | ENT-TN-GOVERNORATE-07DB5E6D265C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-6075E6F01C5A5BD7 | ENT-TN-DELEGATION-3240C5021B36 | ENT-TN-GOVERNORATE-D7972CC63F7E | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-60EE87F000585568 | ENT-TN-DELEGATION-907386F80604 | ENT-TN-GOVERNORATE-78D6D85AF6A0 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-60F84200EB405CB2 | ENT-TN-DELEGATION-36D776E11570 | ENT-TN-GOVERNORATE-7A4D0C3A889C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-627C2B5C667D5650 | ENT-TN-DELEGATION-17B9E0494EC7 | ENT-TN-GOVERNORATE-97D2B1489F90 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-63F3DB72F1F55491 | ENT-TN-DELEGATION-AF66ED06B9B8 | ENT-TN-GOVERNORATE-A460B4F223EB | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-63F7F17AD78F5EA2 | ENT-TN-DELEGATION-0156C9A906A2 | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-65BFA5BA86E759E4 | ENT-TN-DELEGATION-F3529789545D | ENT-TN-GOVERNORATE-B1787F907937 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-66554F7E00DB516C | ENT-TN-DELEGATION-2A637B595634 | ENT-TN-GOVERNORATE-E7D96FEF5043 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-66EE985E71995346 | ENT-TN-DELEGATION-28A3B2254932 | ENT-TN-GOVERNORATE-B1787F907937 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-67C6EB6141B2544C | ENT-TN-DELEGATION-9ADFA1D292D9 | ENT-TN-GOVERNORATE-07DB5E6D265C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-68BCAE55858B5026 | ENT-TN-DELEGATION-BDF031A58E55 | ENT-TN-GOVERNORATE-5BC9A7217C8C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-69E50770D8565D06 | ENT-TN-DELEGATION-19EB9068FDEB | ENT-TN-GOVERNORATE-D5ED89886664 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-6CFEF713FE045163 | ENT-TN-DELEGATION-C73B8495072E | ENT-TN-GOVERNORATE-81845FB6BE40 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-6D019A3344845C82 | ENT-TN-GOVERNORATE-902616FE3988 | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-6D13A543B18D5D24 | ENT-TN-DELEGATION-B8BFE8FFB2B8 | ENT-TN-GOVERNORATE-D5ED89886664 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-6D23720C0F6B5A2C | ENT-TN-DELEGATION-CC185FFE164C | ENT-TN-GOVERNORATE-78D6D85AF6A0 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-6D9FD4E4D4BE5E99 | ENT-TN-DELEGATION-A43DBAE26B8A | ENT-TN-GOVERNORATE-97D2B1489F90 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-6F4B5E9BFE2356B5 | ENT-TN-GOVERNORATE-DF747014232C | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-70C7F5F479D75F33 | ENT-TN-DELEGATION-336FE0336AC9 | ENT-TN-GOVERNORATE-DF747014232C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-7187D063FE3B5ADB | ENT-TN-DELEGATION-D8723103173B | ENT-TN-GOVERNORATE-97D2B1489F90 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-72D392DF8EC85874 | ENT-TN-DELEGATION-7F9EBE1F4EA1 | ENT-TN-GOVERNORATE-5BC9A7217C8C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-77E3016515B4575D | ENT-TN-DELEGATION-434F19B638E3 | ENT-TN-GOVERNORATE-467CAA2B1928 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-7A6A251243F4592F | ENT-TN-DELEGATION-99EBA5A17CB9 | ENT-TN-GOVERNORATE-97D2B1489F90 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-7A8CFB4B04CB5ECC | ENT-TN-DELEGATION-B95D26E1207F | ENT-TN-GOVERNORATE-EA30E853F598 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-7B2F08A00828557E | ENT-TN-DELEGATION-3757F6B83BE1 | ENT-TN-GOVERNORATE-97D2B1489F90 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-7B4EDD077B3958E5 | ENT-TN-DELEGATION-F0023FB066A4 | ENT-TN-GOVERNORATE-07DB5E6D265C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-7BA7462DCAAD58DE | ENT-TN-DELEGATION-7D9681B14049 | ENT-TN-GOVERNORATE-DF747014232C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-7C384C4EA4745444 | ENT-TN-DELEGATION-EE9A7B5ED169 | ENT-TN-GOVERNORATE-78D6D85AF6A0 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-7C6B267DC3025725 | ENT-TN-DELEGATION-706200A5C126 | ENT-TN-GOVERNORATE-E7D96FEF5043 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-7D46C0E15AE3585A | ENT-TN-DELEGATION-21E89D9190E3 | ENT-TN-GOVERNORATE-47F772AA4A84 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-7D662F8F25E55363 | ENT-TN-DELEGATION-00555D763B13 | ENT-TN-GOVERNORATE-36E4260B310C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-7E448EBBA2175B3D | ENT-TN-GOVERNORATE-36E4260B310C | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-7F284D46D1305E7C | ENT-TN-DELEGATION-00EC6583A4A3 | ENT-TN-GOVERNORATE-5BC9A7217C8C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-80E810628C2057A6 | ENT-TN-DELEGATION-8CAB25CD1628 | ENT-TN-GOVERNORATE-CC06DF550344 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-8254D9F3A5745C3D | ENT-TN-DELEGATION-00F12985BEC9 | ENT-TN-GOVERNORATE-EA30E853F598 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-8262FA90B18552C8 | ENT-TN-DELEGATION-F0E269317685 | ENT-TN-GOVERNORATE-36E4260B310C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-83A92EC1A73E5DCF | ENT-TN-DELEGATION-BACCAA713057 | ENT-TN-GOVERNORATE-A460B4F223EB | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-86304782AB6C5339 | ENT-TN-DELEGATION-C433D277206E | ENT-TN-GOVERNORATE-07DB5E6D265C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-865B49DA76F656BD | ENT-TN-DELEGATION-4021556E2BEF | ENT-TN-GOVERNORATE-B1787F907937 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-879C0D26B5785403 | ENT-TN-DELEGATION-B06C74E3ED6B | ENT-TN-GOVERNORATE-467CAA2B1928 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-89FA09BFB0E95C8B | ENT-TN-DELEGATION-4E58B3CD9CB1 | ENT-TN-GOVERNORATE-5BC9A7217C8C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-8A6E288CC08B56CB | ENT-TN-DELEGATION-FE081F997DC5 | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-8BE64277956B5BF3 | ENT-TN-DELEGATION-5589DBA6CB89 | ENT-TN-GOVERNORATE-97D2B1489F90 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-8C6135F6FA0E552A | ENT-TN-DELEGATION-7A57DEB42C2E | ENT-TN-GOVERNORATE-467CAA2B1928 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-8E4FEF1A77745FE4 | ENT-TN-DELEGATION-210B7D8A5B50 | ENT-TN-GOVERNORATE-902616FE3988 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-8E72028A7A1D522C | ENT-TN-DELEGATION-2230C03437B2 | ENT-TN-GOVERNORATE-78D6D85AF6A0 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-8FB5514934BF5EEF | ENT-TN-DELEGATION-00E4826B36E2 | ENT-TN-GOVERNORATE-B1787F907937 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-905EBDF3060D5EB8 | ENT-TN-DELEGATION-D06EBCEA26BA | ENT-TN-GOVERNORATE-07DB5E6D265C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-90AFCDC811A1592B | ENT-TN-DELEGATION-5CA39F3BFF07 | ENT-TN-GOVERNORATE-07DB5E6D265C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-910E4D602A7A5037 | ENT-TN-DELEGATION-584902C8EEE0 | ENT-TN-GOVERNORATE-902616FE3988 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-918072D1097A5831 | ENT-TN-DELEGATION-9D23A36B72E1 | ENT-TN-GOVERNORATE-5BC9A7217C8C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-922F690B97B454F6 | ENT-TN-DELEGATION-64B47287C7CC | ENT-TN-GOVERNORATE-EA2D44B4F25E | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-9258470454655B72 | ENT-TN-DELEGATION-5D5CDCB7496E | ENT-TN-GOVERNORATE-E7D96FEF5043 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-9279B51D70AB51AB | ENT-TN-DELEGATION-9D652FC873EB | ENT-TN-GOVERNORATE-07DB5E6D265C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-92BEA442588B54A5 | ENT-TN-GOVERNORATE-EA30E853F598 | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-94595347802C5E1E | ENT-TN-DELEGATION-6DD1C12A1852 | ENT-TN-GOVERNORATE-EA30E853F598 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-94BD46AC9D595A7F | ENT-TN-DELEGATION-529F20CCEFFA | ENT-TN-GOVERNORATE-B1787F907937 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-954EDF2D9EB25114 | ENT-TN-DELEGATION-5E9C54B26170 | ENT-TN-GOVERNORATE-D28A09D558AD | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-98E4D1CE84CA50CD | ENT-TN-DELEGATION-EF5957AC15F4 | ENT-TN-GOVERNORATE-07DB5E6D265C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-9B4C189E39A8570A | ENT-TN-DELEGATION-E3E9C5077EA4 | ENT-TN-GOVERNORATE-0D738EAC753C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-9B508A5A5F925878 | ENT-TN-DELEGATION-40F8C393FB98 | ENT-TN-GOVERNORATE-0D738EAC753C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-9C8498C9E8F85301 | ENT-TN-DELEGATION-6417F8B088EB | ENT-TN-GOVERNORATE-5BC9A7217C8C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-9D13EBD6F4E1562D | ENT-TN-DELEGATION-EFAC1514C55E | ENT-TN-GOVERNORATE-5BC9A7217C8C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-9D90C71EEFE35954 | ENT-TN-GOVERNORATE-A460B4F223EB | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-9DDB616AEB355F78 | ENT-TN-DELEGATION-C93CA450F43B | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-9F4CE0CD3D2C55CF | ENT-TN-DELEGATION-8CD3CBC66F17 | ENT-TN-GOVERNORATE-E7D96FEF5043 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-9F7E8D1535AE540A | ENT-TN-DELEGATION-11CCF21EE571 | ENT-TN-GOVERNORATE-78D6D85AF6A0 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-A049CFFFB5B2538E | ENT-TN-DELEGATION-A9A2E64081DA | ENT-TN-GOVERNORATE-D28A09D558AD | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-A079C960F088509C | ENT-TN-DELEGATION-E83D07EB9C29 | ENT-TN-GOVERNORATE-97D2B1489F90 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-A155504C13505598 | ENT-TN-DELEGATION-DEB9F3EFCD2D | ENT-TN-GOVERNORATE-1864AE41D5B4 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-A24C64F6A18F5476 | ENT-TN-DELEGATION-64DB1B613F50 | ENT-TN-GOVERNORATE-CC06DF550344 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-A261948EBC6B5A65 | ENT-TN-GOVERNORATE-81845FB6BE40 | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-A2D310EB82CD57CE | ENT-TN-DELEGATION-36BABB1475F8 | ENT-TN-GOVERNORATE-DAC2A2592975 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-A308E3E232DC5CC5 | ENT-TN-DELEGATION-3178EC239E79 | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-A30D9BC1B8CF57D9 | ENT-TN-DELEGATION-46FFC1059453 | ENT-TN-GOVERNORATE-1864AE41D5B4 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-A6058FCAF1E85461 | ENT-TN-DELEGATION-6EC1A2137D0E | ENT-TN-GOVERNORATE-D28A09D558AD | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-A62705DF431F564B | ENT-TN-DELEGATION-0E56BD3D1B3A | ENT-TN-GOVERNORATE-D5ED89886664 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-A7542E1F1FA159F4 | ENT-TN-DELEGATION-762D553CB7DA | ENT-TN-GOVERNORATE-36E4260B310C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-A84B0896BA415CAF | ENT-TN-DELEGATION-B0C081DB1344 | ENT-TN-GOVERNORATE-5BC9A7217C8C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-A8F3C611C509506A | ENT-TN-DELEGATION-57457D07E717 | ENT-TN-GOVERNORATE-467CAA2B1928 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-AB1D5AD2DD2B5447 | ENT-TN-DELEGATION-F7ED4B759BD6 | ENT-TN-GOVERNORATE-902616FE3988 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-AB1DE1B8BAE25229 | ENT-TN-DELEGATION-D59DE8736127 | ENT-TN-GOVERNORATE-EA30E853F598 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-AB5E7646BF495503 | ENT-TN-DELEGATION-A97443748914 | ENT-TN-GOVERNORATE-EA2D44B4F25E | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-ACD88477D7C95436 | ENT-TN-DELEGATION-10DD70515DA0 | ENT-TN-GOVERNORATE-D5ED89886664 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-AD5ECDFC8242570D | ENT-TN-DELEGATION-9D12AE8B04F4 | ENT-TN-GOVERNORATE-0D738EAC753C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-AF120AB2A91B518D | ENT-TN-DELEGATION-B5CD972E98C1 | ENT-TN-GOVERNORATE-47F772AA4A84 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-AF833D6A0F4E5AA2 | ENT-TN-DELEGATION-8708C7088CBC | ENT-TN-GOVERNORATE-EA30E853F598 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-AFEAE5C28A845549 | ENT-TN-DELEGATION-996BCFD91FDD | ENT-TN-GOVERNORATE-DF747014232C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-B0BBB796992750CC | ENT-TN-DELEGATION-70B00114B3C2 | ENT-TN-GOVERNORATE-D28A09D558AD | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-B118756D461D59BA | ENT-TN-DELEGATION-BE50E5DE6BD2 | ENT-TN-GOVERNORATE-A460B4F223EB | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-B12B0EEF9A1C5B24 | ENT-TN-DELEGATION-E56B524C71BE | ENT-TN-GOVERNORATE-E7D96FEF5043 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-B29E35571B0C56DD | ENT-TN-DELEGATION-1F3317733151 | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-B2C10998AA3C53EE | ENT-TN-DELEGATION-920707B361CE | ENT-TN-GOVERNORATE-B1787F907937 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-B3DE64AF478A5903 | ENT-TN-DELEGATION-D592FC6CD4D2 | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-B40CE4747BC054BB | ENT-TN-DELEGATION-47EFAA8BC79F | ENT-TN-GOVERNORATE-E7D96FEF5043 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-B423395218695FD3 | ENT-TN-DELEGATION-CEF958458571 | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-B45AFF9C12A755E3 | ENT-TN-DELEGATION-F66C4659B2C0 | ENT-TN-GOVERNORATE-902616FE3988 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-B646D513AB2254D8 | ENT-TN-DELEGATION-CA29D85670F9 | ENT-TN-GOVERNORATE-07DB5E6D265C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-B6C93C3965F2502D | ENT-TN-GOVERNORATE-EA2D44B4F25E | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-B71411B958B1564B | ENT-TN-DELEGATION-1A266F9B008F | ENT-TN-GOVERNORATE-E7D96FEF5043 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-B789B3DE7BFD5940 | ENT-TN-DELEGATION-C7B4FEE5AE08 | ENT-TN-GOVERNORATE-EA30E853F598 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-B8496EAFED425D83 | ENT-TN-DELEGATION-F12F59DBC46E | ENT-TN-GOVERNORATE-7A4D0C3A889C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-BA08A42AFBBA59A0 | ENT-TN-GOVERNORATE-78D6D85AF6A0 | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-BAB7860F14F05C69 | ENT-TN-DELEGATION-43EBF7A156A6 | ENT-TN-GOVERNORATE-81845FB6BE40 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-BD93B1BDEC30527A | ENT-TN-DELEGATION-A5B79B7F0981 | ENT-TN-GOVERNORATE-47F772AA4A84 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-BDD02568893C5F74 | ENT-TN-DELEGATION-3C575B9AF71B | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-BE1C20452FB55D45 | ENT-TN-DELEGATION-05E0AB3C372D | ENT-TN-GOVERNORATE-0D738EAC753C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-BE28AD9BEDC05C75 | ENT-TN-DELEGATION-9846A16575C2 | ENT-TN-GOVERNORATE-47F772AA4A84 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-BEB08A4CF06651CE | ENT-TN-DELEGATION-4AE753194B10 | ENT-TN-GOVERNORATE-EA30E853F598 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-C1B1E0A4C3575B76 | ENT-TN-DELEGATION-25551A4A8808 | ENT-TN-GOVERNORATE-EA30E853F598 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-C1B97469EDFD5DDB | ENT-TN-DELEGATION-0B11B353C556 | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-C2727F670B725158 | ENT-TN-DELEGATION-B426671C7506 | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-C426776D02115E4A | ENT-TN-DELEGATION-82A4AF3884E0 | ENT-TN-GOVERNORATE-902616FE3988 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-C45EE61418D6587D | ENT-TN-DELEGATION-678C562CAA1C | ENT-TN-GOVERNORATE-D5ED89886664 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-C48F22C4ACBF5613 | ENT-TN-GOVERNORATE-CC06DF550344 | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-C5368E4376D45060 | ENT-TN-DELEGATION-028DF902ABF9 | ENT-TN-GOVERNORATE-EA2D44B4F25E | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-C64A1041E748580D | ENT-TN-DELEGATION-386953CDE2D6 | ENT-TN-GOVERNORATE-5BC9A7217C8C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-C7C4FBEEB8935CD4 | ENT-TN-DELEGATION-DB05A1325AE3 | ENT-TN-GOVERNORATE-47F772AA4A84 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-C8B08D8AFC515D8B | ENT-TN-GOVERNORATE-E7D96FEF5043 | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-C975DEEC55605956 | ENT-TN-DELEGATION-ECE5F1EB80F4 | ENT-TN-GOVERNORATE-81845FB6BE40 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-CB7FCDDE9C9B5119 | ENT-TN-DELEGATION-3568AB5821B0 | ENT-TN-GOVERNORATE-D28A09D558AD | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-CC42501894AB5834 | ENT-TN-DELEGATION-83574F602607 | ENT-TN-GOVERNORATE-1864AE41D5B4 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-CC5A15DA96425031 | ENT-TN-DELEGATION-4F055D8E4C5F | ENT-TN-GOVERNORATE-78D6D85AF6A0 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-CC99ACE2DAF5543D | ENT-TN-DELEGATION-AD509F0A9D79 | ENT-TN-GOVERNORATE-47F772AA4A84 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-CE90DF9818325799 | ENT-TN-DELEGATION-E8F02D6B4EF9 | ENT-TN-GOVERNORATE-07DB5E6D265C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-CED87D5261825014 | ENT-TN-DELEGATION-5BAD0A66CCEB | ENT-TN-GOVERNORATE-DF747014232C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-D01C2589819C58B5 | ENT-TN-DELEGATION-498ED0DE384B | ENT-TN-GOVERNORATE-07DB5E6D265C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-D14DD6A399FF5EF1 | ENT-TN-DELEGATION-05AAF8FA23F6 | ENT-TN-GOVERNORATE-07DB5E6D265C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-D1B3DF4AE60955CE | ENT-TN-DELEGATION-37E43863E13C | ENT-TN-GOVERNORATE-A460B4F223EB | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-D2648CEC15395F4C | ENT-TN-DELEGATION-CB0D8DF8758C | ENT-TN-GOVERNORATE-B1787F907937 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-D6614488A816595B | ENT-TN-DELEGATION-CC6DBA2640FB | ENT-TN-GOVERNORATE-97D2B1489F90 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-D8F17B1881475D72 | ENT-TN-DELEGATION-3D8C44AF7D14 | ENT-TN-GOVERNORATE-7A4D0C3A889C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-D9CEBAD0DAF85992 | ENT-TN-DELEGATION-08BF6BF26FFF | ENT-TN-GOVERNORATE-467CAA2B1928 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-DA1E1E61898352F1 | ENT-TN-DELEGATION-5B401B5FE360 | ENT-TN-GOVERNORATE-DF747014232C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-DC09ED697EF75EE1 | ENT-TN-DELEGATION-0B9CE76F3AD6 | ENT-TN-GOVERNORATE-97D2B1489F90 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-DCDF9D0CD3715F4C | ENT-TN-DELEGATION-ACB1178786DC | ENT-TN-GOVERNORATE-EA30E853F598 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-DD323DC401D95236 | ENT-TN-GOVERNORATE-467CAA2B1928 | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-DD6ACD0C18595ADB | ENT-TN-DELEGATION-184C444E7833 | ENT-TN-GOVERNORATE-36E4260B310C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-DD9DF2B726B55673 | ENT-TN-GOVERNORATE-7A4D0C3A889C | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-DDA0A36734FD56AF | ENT-TN-DELEGATION-4A822090C35C | ENT-TN-GOVERNORATE-EA30E853F598 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-DDAA2A55C7115C52 | ENT-TN-DELEGATION-8CCC58460F99 | ENT-TN-GOVERNORATE-EA30E853F598 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-DE488D9F1B765896 | ENT-TN-DELEGATION-C2548493A23C | ENT-TN-GOVERNORATE-E7D96FEF5043 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-DEE6F052B22C50CB | ENT-TN-DELEGATION-E6F9AC3B6A1F | ENT-TN-GOVERNORATE-A460B4F223EB | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-E033D0A2C6875CDC | ENT-TN-DELEGATION-C151EAFA4BD1 | ENT-TN-GOVERNORATE-0D738EAC753C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-E193704FF6F35C65 | ENT-TN-GOVERNORATE-B1787F907937 | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-E2A8D77ED0345D90 | ENT-TN-GOVERNORATE-D5ED89886664 | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-E38DC695725B5355 | ENT-TN-DELEGATION-34E2240B6A54 | ENT-TN-GOVERNORATE-EA2D44B4F25E | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-E3B0762A2D4F5010 | ENT-TN-DELEGATION-148C846991C4 | ENT-TN-GOVERNORATE-B1787F907937 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-E4C2D65C991C51DA | ENT-TN-DELEGATION-7667BCFBBD94 | ENT-TN-GOVERNORATE-D5ED89886664 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-E4E3CFCBA08E51B6 | ENT-TN-DELEGATION-46D8F9A49020 | ENT-TN-GOVERNORATE-D28A09D558AD | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-E5A130B8D28D522C | ENT-TN-DELEGATION-EE60D65B9935 | ENT-TN-GOVERNORATE-902616FE3988 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-E62691803D9D5E36 | ENT-TN-DELEGATION-28027896EDDD | ENT-TN-GOVERNORATE-D5ED89886664 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-E6B4B19E72A05E5C | ENT-TN-DELEGATION-C41B01AE892E | ENT-TN-GOVERNORATE-36E4260B310C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-E73F2225FAEA5A96 | ENT-TN-DELEGATION-D4FC46D8AB0D | ENT-TN-GOVERNORATE-D5ED89886664 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-E7A618D80769509B | ENT-TN-GOVERNORATE-1864AE41D5B4 | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-E816596FC2C258D4 | ENT-TN-DELEGATION-1172E32A37EA | ENT-TN-GOVERNORATE-5BC9A7217C8C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-E8566832B40E5844 | ENT-TN-DELEGATION-AFAE2BE79F31 | ENT-TN-GOVERNORATE-DF747014232C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-E94342E459725276 | ENT-TN-DELEGATION-40268C8E9C06 | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-EA27E71149105539 | ENT-TN-DELEGATION-FE7ADA16AB50 | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-EABA1E3ECB6B5AF6 | ENT-TN-DELEGATION-3CEADA31C198 | ENT-TN-GOVERNORATE-A460B4F223EB | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-EC31244689195005 | ENT-TN-DELEGATION-D4441080949B | ENT-TN-GOVERNORATE-0D738EAC753C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-EEEF01F6B6A75D76 | ENT-TN-DELEGATION-A6D2E459547E | ENT-TN-GOVERNORATE-D28A09D558AD | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-F0E7CCF5AB3C5F50 | ENT-TN-DELEGATION-FE6A0D05DF67 | ENT-TN-GOVERNORATE-81845FB6BE40 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-F11B720446205F03 | ENT-TN-DELEGATION-B63E32B2BC3F | ENT-TN-GOVERNORATE-47F772AA4A84 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-F4F239BF44E25EE3 | ENT-TN-DELEGATION-A9463801F6AD | ENT-TN-GOVERNORATE-36E4260B310C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-F518062AEE255192 | ENT-TN-DELEGATION-AC41B378E3D9 | ENT-TN-GOVERNORATE-07DB5E6D265C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-F51BCB22D98A5C45 | ENT-TN-DELEGATION-D2E46DB3C8BC | ENT-TN-GOVERNORATE-0D738EAC753C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-F562BC19E0965109 | ENT-TN-DELEGATION-05852EF74252 | ENT-TN-GOVERNORATE-97D2B1489F90 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-F593E2B616BF5D59 | ENT-TN-GOVERNORATE-DAC2A2592975 | ENT-TN-COUNTRY | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-F758738C8DFC5D61 | ENT-TN-DELEGATION-F153AA210A4D | ENT-TN-GOVERNORATE-0D738EAC753C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-F92ACD8420AB59BD | ENT-TN-DELEGATION-44DC92075FFF | ENT-TN-GOVERNORATE-1864AE41D5B4 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-F951EBD7962B5FDE | ENT-TN-DELEGATION-D77747883E55 | ENT-TN-GOVERNORATE-0D738EAC753C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-FB26D9C3EC4558FB | ENT-TN-DELEGATION-D75198EE6BB5 | ENT-TN-GOVERNORATE-DB8D5C457676 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-FC558EED7E0C5E51 | ENT-TN-DELEGATION-997BFDED88CF | ENT-TN-GOVERNORATE-7A4D0C3A889C | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-FCF7CD573DC15915 | ENT-TN-DELEGATION-AFCCE19F1CD3 | ENT-TN-GOVERNORATE-EA30E853F598 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-FED0048E83355286 | ENT-TN-DELEGATION-6F8D6872B9E9 | ENT-TN-GOVERNORATE-47F772AA4A84 | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-FFAD51AB466855F8 | ENT-TN-DELEGATION-E8E567F03E9D | ENT-TN-GOVERNORATE-EA2D44B4F25E | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |
| REL-FFAF972C3FA556D0 | ENT-TN-DELEGATION-DAC482090AC5 | ENT-TN-GOVERNORATE-D7972CC63F7E | administrative_parent | current | SRC-TN-MOI-DELEGATIONS-2013 |

## الادعاءات

| المعرّف | الموضوع | المحمول | القيمة | الوحدة | تاريخ الرصد | الحالة | المصدر |
|---|---|---|---|---|---|---|---|
| CLM-01F01217FD73549E | ENT-TN-GOVERNORATE-EA2D44B4F25E | population | 303032 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-0440FF23CF945934 | ENT-TN-GOVERNORATE-81845FB6BE40 | population | 176945 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-1923488F27265729 | ENT-TN-GOVERNORATE-07DB5E6D265C | population | 674971 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-299066B220135F49 | ENT-TN-GOVERNORATE-E7D96FEF5043 | population | 410812 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-30573A2341B65E91 | ENT-TN-GOVERNORATE-78D6D85AF6A0 | population | 576088 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-32FC870867E75D62 | ENT-TN-GOVERNORATE-7A4D0C3A889C | population | 401477 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-4095A0B2719859AE | ENT-TN-GOVERNORATE-0D738EAC753C | population | 243156 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-476452C4482C56BE | ENT-TN-GOVERNORATE-EA30E853F598 | population | 787920 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-5F89225106935E96 | ENT-TN-GOVERNORATE-1864AE41D5B4 | population | 156961 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-6E14E7C897B25972 | ENT-TN-GOVERNORATE-47F772AA4A84 | population | 429912 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-7A745A4522155266 | ENT-TN-GOVERNORATE-DAC2A2592975 | population | 149453 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-905829C036E15A70 | ENT-TN-GOVERNORATE-DF747014232C | population | 374300 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-90B00BCDE9A95D2A | ENT-TN-GOVERNORATE-5BC9A7217C8C | population | 548828 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-97F4430A55E65437 | ENT-TN-GOVERNORATE-D7972CC63F7E | population | 107912 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-A092AE81190758A5 | ENT-TN-GOVERNORATE-D28A09D558AD | population | 570559 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-A583EEC3020E5A4B | ENT-TN-GOVERNORATE-D5ED89886664 | population | 631842 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-A74E4DB0722059B7 | ENT-TN-GOVERNORATE-B1787F907937 | population | 568219 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-A968DAF688615537 | ENT-TN-GOVERNORATE-DB8D5C457676 | population | 1056247 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-D08DFE66D5125784 | ENT-TN-GOVERNORATE-97D2B1489F90 | population | 955421 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-D267C300CB5C52FD | ENT-TN-GOVERNORATE-A460B4F223EB | population | 223087 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-E435BAEFC3495119 | ENT-TN-GOVERNORATE-36E4260B310C | population | 439243 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-E5866320AD6A5143 | ENT-TN-GOVERNORATE-467CAA2B1928 | population | 337331 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-F94336D7DA555AE3 | ENT-TN-GOVERNORATE-CC06DF550344 | population | 379518 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |
| CLM-FA70F590185150F4 | ENT-TN-GOVERNORATE-902616FE3988 | population | 479520 | person | 2014-04-23 | verified | SRC-TN-INS-RGPH-2014 |

## المصادر الذرية المستخدمة

| المعرّف | العنوان | الناشر | تاريخ النشر | تاريخ الاسترجاع | الترخيص | الرابط |
|---|---|---|---|---|---|---|
| SRC-ISO-3166-1-2020 | ISO 3166-1:2020 — Codes for the representation of names of countries and their subdivisions — Part 1: Country code | International Organization for Standardization (ISO) | 2020-08 | 2026-08-15 | ISO copyright; reuse is subject to ISO terms of use | https://www.iso.org/obp/ui/#iso:std:iso:3166:-1:ed-4:v1:en |
| SRC-TN-DGCL-MUNICIPALITIES-2018 | Rapport de synthèse sur la nouvelle carte des municipalités | Direction Générale des Collectivités Locales, Tunisie | 2018-04-06 | 2026-08-15 | License not stated in the publication metadata | http://www.collectiviteslocales.gov.tn/wp-content/uploads/2018/04/Rapport_synthese_vf-2018.pdf |
| SRC-TN-INS-RGPH-2014 | Recensement Général de la Population et de l'Habitat 2014 — Principaux indicateurs | Institut National de la Statistique, Tunisie | 2015-04 | 2026-08-15 | License not stated in the publication metadata | https://www.ins.tn/sites/default/files/publication/pdf/RGPH%202014-V0.pdf |
| SRC-TN-MOI-DELEGATIONS-2013 | معتمديات ولايات الجمهورية | وزارة الداخلية التونسية — الإدارة العامة للشؤون الجهوية | 2013-06-25 | 2026-08-15 | License not stated on the source page | https://opendata.interieur.gov.tn/ar/catalog/delegations-par-gouvernorats-de-la-republique |
| SRC-TN-MOI-IMADAS-2013 | Secteurs territoriaux (imadas) par gouvernorat et délégation | Ministère de l'Intérieur tunisien — Direction Générale des Affaires Régionales | 2013-07-15 | 2026-08-15 | License not stated on the source page | https://opendata.interieur.gov.tn/fr/catalog/secteurs-territoriaux-par-gouvernorat-et-delegation |

---
_مولّد آليًا؛ لا تعدّل هذا الملف مباشرة._
