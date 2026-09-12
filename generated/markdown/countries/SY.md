# سوريا (SY) — عرض مولّد من Schema 2.0.0

> **حدود التغطية:** التغطية المحلية غير مكتملة. لا تمثل هذه الصفحة جميع المدن أو القرى أو الأحياء أو الحارات، ولا يُستدل على التغطية من وجود ملف. البيانات المنظمة هي المصدر؛ هذه الصفحة عرض مولّد.

## التغطية والمقامات

أي نسبة 100% أدناه مقيدة بالدولة والطبقة والمقام المؤرخ واللقطة والمصدر الظاهرة في الصف نفسه؛ ولا تمتد إلى طبقة أخرى.

| الطبقة | تعريف المقام | المقام | مطابق | غير مطابق | مستبعد | مفقود | النسبة | تاريخ اللقطة | اللقطة | المصدر | الترخيص | مكتمل | سبب النقص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| country_scope | ISO country entity in the project's 22-country scope | 1 | 1 | 0 | 0 | 0 | 100% | 2026-08-15 | SNP-MIGRATION-2026-08-15 | SRC-ISO-3166-1-2020 | ISO copyright; reuse is subject to ISO terms of use | نعم | — |
| sy_governorate_damascus_special | Damascus city forms one governorate. | 1 | 1 | 0 | 0 | 0 | 100% | 2026-08-17 | SNP-SY-PRODUCTION-20260817 | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | Official Syrian institutional/statistical material; factual extraction with attribution; reuse terms not stated | نعم | — |
| sy_district | Current official count of districts, including 14 governorate-center districts; record layer open. | 68 | 0 | 68 | 0 | 68 | 0% | 2026-08-17 | SNP-SY-PRODUCTION-20260817 | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | Official Syrian institutional/statistical material; factual extraction with attribution; reuse terms not stated | لا | Record-level current register not yet accepted; official count is retained as an open denominator. |
| sy_governorate | Current institutional governorates. | 14 | 14 | 0 | 0 | 0 | 100% | 2026-08-17 | SNP-SY-PRODUCTION-20260817 | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | Official Syrian institutional/statistical material; factual extraction with attribution; reuse terms not stated | نعم | — |
| sy_governorate_other | Governorates other than Damascus special case. | 13 | 13 | 0 | 0 | 0 | 100% | 2026-08-17 | SNP-SY-PRODUCTION-20260817 | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | Official Syrian institutional/statistical material; factual extraction with attribution; reuse terms not stated | نعم | — |
| sy_subdistrict | Current official count of subdistricts; record layer open. | 227 | 0 | 227 | 0 | 227 | 0% | 2026-08-17 | SNP-SY-PRODUCTION-20260817 | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | Official Syrian institutional/statistical material; factual extraction with attribution; reuse terms not stated | لا | Record-level current register not yet accepted; official count is retained as an open denominator. |

## الكيانات

| المعرّف | الاسم | النوع | الحالة | المصدر القانوني/المرجعي | المحدد داخل المصدر |
|---|---|---|---|---|---|
| ENT-SY-COUNTRY | سوريا | country | current | SRC-ISO-3166-1-2020 | ISO alpha-2 entry SY |
| ENT-SY-GOVERNORATE-01 | دمشق | sy_governorate | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 | SANA governorate navigation category: دمشق |
| ENT-SY-GOVERNORATE-02 | حلب | sy_governorate | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 | SANA governorate navigation category: حلب |
| ENT-SY-GOVERNORATE-03 | حماة | sy_governorate | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 | SANA governorate navigation category: حماة |
| ENT-SY-GOVERNORATE-04 | حمص | sy_governorate | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 | SANA governorate navigation category: حمص |
| ENT-SY-GOVERNORATE-05 | دير الزور | sy_governorate | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 | SANA governorate navigation category: دير الزور |
| ENT-SY-GOVERNORATE-06 | ريف دمشق | sy_governorate | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 | SANA governorate navigation category: ريف دمشق |
| ENT-SY-GOVERNORATE-07 | اللاذقية | sy_governorate | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 | SANA governorate navigation category: اللاذقية |
| ENT-SY-GOVERNORATE-08 | السويداء | sy_governorate | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 | SANA governorate navigation category: السويداء |
| ENT-SY-GOVERNORATE-09 | الحسكة | sy_governorate | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 | SANA governorate navigation category: الحسكة |
| ENT-SY-GOVERNORATE-10 | الرقة | sy_governorate | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 | SANA governorate navigation category: الرقة |
| ENT-SY-GOVERNORATE-11 | إدلب | sy_governorate | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 | SANA governorate navigation category: إدلب |
| ENT-SY-GOVERNORATE-12 | القنيطرة | sy_governorate | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 | SANA governorate navigation category: القنيطرة |
| ENT-SY-GOVERNORATE-13 | درعا | sy_governorate | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 | SANA governorate navigation category: درعا |
| ENT-SY-GOVERNORATE-14 | طرطوس | sy_governorate | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 | SANA governorate navigation category: طرطوس |

## الأسماء البديلة

| المعرّف | الكيان | الاسم | اللغة | النوع | المصدر |
|---|---|---|---|---|---|
| ALS-9D7C59A808BE5A24 | ENT-SY-COUNTRY | Syrian Arab Republic | en | english | SRC-ISO-3166-1-2020 |

## علاقات الإدارة/الموقع

| المعرّف | الابن | الأب | العلاقة | الحالة | المصدر |
|---|---|---|---|---|---|
| REL-SY-04E359F7B5C3527A | ENT-SY-GOVERNORATE-05 | ENT-SY-COUNTRY | administrative_parent | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 |
| REL-SY-288BB2305BCC5BFA | ENT-SY-GOVERNORATE-12 | ENT-SY-COUNTRY | administrative_parent | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 |
| REL-SY-5EECA9B4111C5A9F | ENT-SY-GOVERNORATE-09 | ENT-SY-COUNTRY | administrative_parent | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 |
| REL-SY-7558C22BF88056A2 | ENT-SY-GOVERNORATE-06 | ENT-SY-COUNTRY | administrative_parent | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 |
| REL-SY-85AB5978C3BF5EE0 | ENT-SY-GOVERNORATE-10 | ENT-SY-COUNTRY | administrative_parent | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 |
| REL-SY-94BD42C8287558D9 | ENT-SY-GOVERNORATE-03 | ENT-SY-COUNTRY | administrative_parent | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 |
| REL-SY-97B204A52450505E | ENT-SY-GOVERNORATE-14 | ENT-SY-COUNTRY | administrative_parent | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 |
| REL-SY-BF630D5F5D685FF9 | ENT-SY-GOVERNORATE-11 | ENT-SY-COUNTRY | administrative_parent | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 |
| REL-SY-CB9B9B1101BC5AA6 | ENT-SY-GOVERNORATE-13 | ENT-SY-COUNTRY | administrative_parent | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 |
| REL-SY-E636D299B997587F | ENT-SY-GOVERNORATE-01 | ENT-SY-COUNTRY | administrative_parent | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 |
| REL-SY-E725BA3552605C58 | ENT-SY-GOVERNORATE-07 | ENT-SY-COUNTRY | administrative_parent | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 |
| REL-SY-ECB40BD195285435 | ENT-SY-GOVERNORATE-02 | ENT-SY-COUNTRY | administrative_parent | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 |
| REL-SY-F34A8598A0255CFC | ENT-SY-GOVERNORATE-08 | ENT-SY-COUNTRY | administrative_parent | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 |
| REL-SY-F6CDC15153D85068 | ENT-SY-GOVERNORATE-04 | ENT-SY-COUNTRY | administrative_parent | current | SRC-SY-SANA-GOVERNORATE-NAV-2026 |

## الادعاءات

| المعرّف | الموضوع | المحمول | القيمة | التصنيف | الثقة | الحالة | المصدر | المحدد |
|---|---|---|---|---|---|---|---|---|
| CLM-SY-123CE751865F507B | ENT-SY-GOVERNORATE-02 | administrative_profile | ordinary_governorate | official | high | verified | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | SANA governorate navigation category: حلب |
| CLM-SY-14FBE6F35B8B5D33 | ENT-SY-GOVERNORATE-13 | administrative_profile | ordinary_governorate | official | high | verified | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | SANA governorate navigation category: درعا |
| CLM-SY-1E423EC2C84E5139 | ENT-SY-GOVERNORATE-07 | administrative_profile | ordinary_governorate | official | high | verified | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | SANA governorate navigation category: اللاذقية |
| CLM-SY-1FA068EF1B145DD5 | ENT-SY-GOVERNORATE-08 | administrative_profile | ordinary_governorate | official | high | verified | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | SANA governorate navigation category: السويداء |
| CLM-SY-2CA8D50B97C2504B | ENT-SY-GOVERNORATE-09 | administrative_profile | ordinary_governorate | official | high | verified | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | SANA governorate navigation category: الحسكة |
| CLM-SY-2E84A603F1715277 | ENT-SY-GOVERNORATE-03 | administrative_profile | ordinary_governorate | official | high | verified | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | SANA governorate navigation category: حماة |
| CLM-SY-4F50BB777347595F | ENT-SY-GOVERNORATE-12 | administrative_profile | ordinary_governorate | official | high | verified | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | SANA governorate navigation category: القنيطرة |
| CLM-SY-5972BC6ED0A55816 | ENT-SY-GOVERNORATE-01 | administrative_profile | damascus_city_governorate | official | high | verified | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | Administrative divisions: Damascus city is a governorate in its own right |
| CLM-SY-7FF5CDB24D345A4B | ENT-SY-GOVERNORATE-04 | administrative_profile | ordinary_governorate | official | high | verified | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | SANA governorate navigation category: حمص |
| CLM-SY-943147B66C675266 | ENT-SY-GOVERNORATE-14 | administrative_profile | ordinary_governorate | official | high | verified | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | SANA governorate navigation category: طرطوس |
| CLM-SY-CD377C87984E5000 | ENT-SY-GOVERNORATE-11 | administrative_profile | ordinary_governorate | official | high | verified | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | SANA governorate navigation category: إدلب |
| CLM-SY-D811512A02875BF4 | ENT-SY-GOVERNORATE-05 | administrative_profile | ordinary_governorate | official | high | verified | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | SANA governorate navigation category: دير الزور |
| CLM-SY-DDBF2ADE192B5F88 | ENT-SY-GOVERNORATE-06 | administrative_profile | ordinary_governorate | official | high | verified | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | SANA governorate navigation category: ريف دمشق |
| CLM-SY-DEPTH-00576FD83F9D5BC8 | ENT-SY-GOVERNORATE-02 | food_dish | {'description': 'غميس الفلفل الحلبي المجفف بالجوز ودبس الرمان', 'name': 'المحمرة', 'note': 'حلبية أصيلة والفلفل الحلبي علامة مطبخها', 'occasion': 'مقبلات'} | local | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dish entry: المحمرة |
| CLM-SY-DEPTH-031BE1A7845F5A29 | ENT-SY-COUNTRY | food_dish | {'description': 'باذنجان صغير محشو بالجوز والفلفل والثوم مخلل في زيت الزيتون', 'name': 'المكدوس', 'note': '', 'occasion': 'مؤونة الشتاء'} | national | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dish entry: المكدوس |
| CLM-SY-DEPTH-07BFBB31BD0D5EF2 | ENT-SY-GOVERNORATE-01 | food_dish | {'description': 'الشاكرية لحم ضأن في الزبادي، وحراق أصبعه عدس وعجين بدبس الرمان', 'name': 'الشاكرية وحراق أصبعه', 'note': 'دمشق', 'occasion': 'غداء وشتاء'} | local | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dish entry: الشاكرية وحراق أصبعه |
| CLM-SY-DEPTH-0CE5436587EC589B | ENT-SY-GOVERNORATE-01 | food_dish | {'description': 'خبز محمص يسقى بمرق الحمص أو اللحم مع السمن والمكسرات؛ من أنواعها فتة المكدوس وفتة المقادم', 'name': 'الفتة الشامية', 'note': 'دمشقية', 'occasion': 'فطور وعزائم'} | local | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dish entry: الفتة الشامية |
| CLM-SY-DEPTH-27C746450B055F82 | ENT-SY-COUNTRY | dialect_profile | {'features': ['كلمات آرامية باقية في العربية الشامية'], 'group': 'الجذر الآرامي المشترك', 'sample_words': [{'m': 'حر شديد؛ آرامية', 'w': 'شوب'}, {'m': 'بشر أو نادى؛ آرامية', 'w': 'كرز'}, {'m': 'سكين كبيرة؛ آرامية', 'w': 'ساطور'}, {'m': 'نعل؛ آرامية', 'w': 'تاسومة'}], 'scope': 'عموم الشام'} | regional | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dialect profile: الجذر الآرامي المشترك |
| CLM-SY-DEPTH-2DF7D8821700540D | ENT-SY-GOVERNORATE-09 | language_presence | {'description': 'لغة سامية حية في قرى الجزيرة كالمالكية ورأس العين ولغة طقسية للكنائس السريانية', 'language': 'السريانية الآرامية'} | regional | medium | reported | SRC-SY-CULTURE-MIRROR-2026 | Language note: السريانية الآرامية |
| CLM-SY-DEPTH-33D286A730BE562E | ENT-SY-GOVERNORATE-02 | food_dish | {'description': 'عجينة برغل ولحم مدقوق تحشى باللحم والمكسرات؛ من أنواعها المقلية والنية واللبنية والسماقية والسفرجلية والمبرومة وحلب مشهورة بها خصوصا', 'name': 'الكبة', 'note': 'رمز شامي مشترك بين سوريا ولبنان والعراق — لا ملكية حصرية؛ الشهرة الحلبية مرسوة', 'occasion': 'الولائم ورمضان'} | shared | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dish entry: الكبة |
| CLM-SY-DEPTH-374D81F5805A577E | ENT-SY-GOVERNORATE-09 | language_presence | {'description': 'لغة إيرانية غربية في الحسكة والقامشلي وعفرين وعين العرب', 'language': 'الكردية (الكرمانجية)'} | regional | medium | reported | SRC-SY-CULTURE-MIRROR-2026 | Language note: الكردية (الكرمانجية) |
| CLM-SY-DEPTH-3BC0E7BECFB056BB | ENT-SY-GOVERNORATE-02 | language_presence | {'description': 'لغة الجالية الأرمنية التاريخية في حلب ودمشق والجزيرة', 'language': 'الأرمنية'} | regional | medium | reported | SRC-SY-CULTURE-MIRROR-2026 | Language note: الأرمنية |
| CLM-SY-DEPTH-50D675EF655C58AD | ENT-SY-GOVERNORATE-01 | clothing_item | {'description': 'حرير منسوج بخيوط ذهبية علامة دمشق النسيجية للمناسبات', 'gender': 'نسائي', 'name': 'البروكار الدمشقي'} | local | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dress entry: البروكار الدمشقي |
| CLM-SY-DEPTH-533FB2089EE75040 | ENT-SY-GOVERNORATE-07 | dialect_profile | {'features': ['تفخيم تام للألف: عامل إلى عومل', 'ميل إلى الكسر في اللاذقية وجبلة'], 'group': 'الساحلية', 'sample_words': [{'m': 'انظر', 'w': 'عين'}, {'m': 'هذا هو', 'w': 'ليكو'}, {'m': 'ارفعها', 'w': 'إبا'}], 'scope': 'اللاذقية وجبلة وطرطوس وبانياس'} | regional | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dialect profile: الساحلية |
| CLM-SY-DEPTH-66BDD13C92A252F6 | ENT-SY-GOVERNORATE-02 | language_presence | {'description': 'تركية أوغوزية في قرى تركمانية بحلب واللاذقية وحمص وحماة والرقة؛ حصرها الدقيق يحتاج مصدرا أكاديميا', 'language': 'التركمانية'} | regional | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Language note: التركمانية |
| CLM-SY-DEPTH-6AB9965FD6815759 | ENT-SY-GOVERNORATE-02 | clothing_item | {'description': 'قماش متعدد الألوان بتطريز دقيق وبطانة مزخرفة من تراث حلب النسيجي', 'gender': 'مشترك', 'name': 'الإيكات الحلبي'} | local | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dress entry: الإيكات الحلبي |
| CLM-SY-DEPTH-729C25305E6452A8 | ENT-SY-GOVERNORATE-13 | dialect_profile | {'features': ['قريبة من بدوية الجنوب والأردن', 'هاظ هو بالتفخيم'], 'group': 'الحورانية', 'sample_words': [], 'scope': 'درعا والسويداء وحوران'} | regional | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dialect profile: الحورانية |
| CLM-SY-DEPTH-7A62ECBBF42550BB | ENT-SY-GOVERNORATE-01 | dialect_profile | {'features': ['القاف همزة: قال إلى آل', 'تفخيم خفيف للألف', 'النحت الدمشقي: شو بدك ومدري', 'أوزان التصغير: كنباية وشنطاية'], 'group': 'الشامية الدمشقية', 'sample_words': [{'m': 'يا أمي', 'w': 'يامو'}, {'m': 'إلى الأمام مباشرة', 'w': 'دغري'}, {'m': 'هذا هو', 'w': 'شحو'}, {'m': 'يا رجل', 'w': 'يا زلمة'}], 'scope': 'دمشق ووسط سوريا'} | regional | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dialect profile: الشامية الدمشقية |
| CLM-SY-DEPTH-862D69E794E0576A | ENT-SY-GOVERNORATE-02 | dialect_profile | {'features': ['إمالة الألف إلى الياء: عامل إلى عيمل', 'قاف مفخمة خلافا للدمشقية', 'معجم مغاير يحتاج معجما خاصا'], 'group': 'الحلبية', 'sample_words': [{'m': 'يا أبي', 'w': 'يوب'}, {'m': 'اجلس', 'w': 'بروك'}, {'m': 'أبدا نهائيا', 'w': 'طاول طاول'}, {'m': 'إلى الأمام؛ مقابل دغري الدمشقية', 'w': 'سيوي'}, {'m': 'كوع', 'w': 'عوجة'}], 'scope': 'حلب وشمالها'} | regional | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dialect profile: الحلبية |
| CLM-SY-DEPTH-8C1BB7B19EC9552A | ENT-SY-GOVERNORATE-07 | clothing_item | {'description': 'الشروال الفضفاض للساحل والريف، والزبون والشروال والزينار للزي الكردي في الحسكة وعفرين', 'gender': 'رجالي', 'name': 'الشروال الساحلي والزي الكردي'} | regional | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dress entry: الشروال الساحلي والزي الكردي |
| CLM-SY-DEPTH-94B8892A57955E18 | ENT-SY-COUNTRY | food_dish | {'description': 'ورق العنب المحشو بالأرز واللحم', 'name': 'اليبرق والمحاشي', 'note': 'شامي عثماني مشترك', 'occasion': 'مناسبات'} | shared | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dish entry: اليبرق والمحاشي |
| CLM-SY-DEPTH-A323BA1ED7F756C6 | ENT-SY-GOVERNORATE-05 | dialect_profile | {'features': ['فراتية قريبة من لهجات غرب العراق', 'بدوية الجذور'], 'group': 'الديرية', 'sample_words': [], 'scope': 'دير الزور والرقة والشرق'} | regional | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dialect profile: الديرية |
| CLM-SY-DEPTH-AF715DD26F685965 | ENT-SY-COUNTRY | food_dish | {'description': 'عدس وأرز أو برغل وبصل مقلي', 'name': 'المجدرة', 'note': 'مشترك شامي', 'occasion': 'يومي وصيامي'} | shared | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dish entry: المجدرة |
| CLM-SY-DEPTH-B6AA695F697B56D3 | ENT-SY-COUNTRY | clothing_item | {'description': 'رداء طويل فضفاض؛ والصاية قمباز من قماش مزخرف كالإيكات الحلبي والبروكار الدمشقي', 'gender': 'رجالي', 'name': 'القمباز والصاية'} | national | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dress entry: القمباز والصاية |
| CLM-SY-DEPTH-C60E36451F80583B | ENT-SY-COUNTRY | clothing_item | {'description': 'غطاء رأس أحمر من اللباد دخل مع العثمانيين وظل رمزا حضريا دمشقيا وحلبيا حتى القرن العشرين', 'gender': 'رجالي', 'name': 'الطربوش'} | historical | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dress entry: الطربوش |
| CLM-SY-DEPTH-C820251DFC485D7F | ENT-SY-GOVERNORATE-02 | food_dish | {'description': 'لحم غنم مطحون على السيخ بالفلفل الحلبي', 'name': 'الكباب الحلبي', 'note': 'حلب', 'occasion': 'وليمة'} | local | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dish entry: الكباب الحلبي |
| CLM-SY-DEPTH-DD020FDAB9685F91 | ENT-SY-COUNTRY | food_dish | {'description': 'التبولة بقدونس وبرغل وطماطم وليمون، والفتوش سلطة بالخبز المقرمش ودبس الرمان', 'name': 'التبولة والفتوش', 'note': 'شامية مشتركة مع لبنان — لا حصرية', 'occasion': 'مقبلات'} | shared | low | reported | SRC-SY-CULTURE-MIRROR-2026 | Dish entry: التبولة والفتوش |
| CLM-SY-F1D7FCFDC0F65101 | ENT-SY-GOVERNORATE-10 | administrative_profile | ordinary_governorate | official | high | verified | SRC-SY-SIA-ADMIN-DIVISIONS-2026 | SANA governorate navigation category: الرقة |

## جودة مصادر الادعاءات المنشورة

ادعاءات A/B: 14 من 14 (100.00%).

## المصادر الذرية المستخدمة

| المعرّف | الفئة | العنوان | الناشر | تاريخ النشر | تاريخ الاسترجاع | الترخيص | الرابط |
|---|---|---|---|---|---|---|---|
| SRC-ISO-3166-1-2020 | A | ISO 3166-1:2020 — Codes for the representation of names of countries and their subdivisions — Part 1: Country code | International Organization for Standardization (ISO) | 2020-08 | 2026-08-15 | ISO copyright; reuse is subject to ISO terms of use | https://www.iso.org/obp/ui/#iso:std:iso:3166:-1:ed-4:v1:en |
| SRC-SY-CULTURE-MIRROR-2026 | E | Syrian dialects, languages, cuisine, and dress — encyclopedic mirror pages | Encyclopedic mirror pages on Syrian culture | — | 2026-08-17 | Official Syrian institutional/statistical material; factual extraction with attribution; reuse terms not stated | https://ar.wikipedia.org/wiki/%D9%84%D9%87%D8%AC%D8%A7%D8%AA_%D8%B3%D9%88%D8%B1%D9%8A%D8%A9 |
| SRC-SY-SANA-GOVERNORATE-NAV-2026 | A | Current governorate navigation and presidency appointments | Syrian Arab News Agency | — | 2026-08-17 | Official Syrian institutional/statistical material; factual extraction with attribution; reuse terms not stated | https://sana.sy/presidency/ |
| SRC-SY-SIA-ADMIN-DIVISIONS-2026 | A | Administrative divisions of Syria | Syrian Investment Authority | — | 2026-08-17 | Official Syrian institutional/statistical material; factual extraction with attribution; reuse terms not stated | https://invest.gov.sy/Home/WhySyria |

---
_مولّد آليًا؛ لا تعدّل هذا الملف مباشرة._
