# أنواع الكيانات وحالاتها — Schema 2.0.0

`schema/vocabularies.json` هو المرجع التنفيذي. هذا الملف يشرح سبب الفصل بين الأنواع.

## قواعد عامة

- `country` كيان سياسي ضمن نطاق المشروع، وليس والدًا نصيًا ضمن كل صف.
- `city`, `town`, `village`, `settlement`, `populated_settlement`, `neighborhood`, `quarter`, `lane`, `historical_place`, و`refugee_camp` أنواع أماكن مأهولة/تاريخية مستقلة، وليست درجات إدارية تلقائيًا.
- `archaeological_site`, `market`, `landmark`, `natural_site`, `cultural_site`, و`gate` مواقع مستقلة؛ لا تُدمج في بلدية أو مدينة تحمل الاسم نفسه.
- `person` كيان شخصي يحتاج علاقة مكانية `associated_with` وادعاء دلالة موثقًا؛ ليس جزءًا من شجرة الإدارة.
- العاصمة مدينة وعلاقتها `capital_of`؛ لا يُنشأ نوع مركب مثل «ولاية+عاصمة».
- «المحافظة» و«الولاية» و«الإقليم» لا تُسوّى في نوع عام. النوع يحمل ISO البلد والمصطلح المحلي: `jo_governorate`, `tn_governorate`, `dz_wilaya`…
- الاسم التاريخي والإنجليزي والمحلي `Alias` ما دام يشير إلى الكيان نفسه. الوحدة السابقة ذات الحدود/الزمن المختلفين `Entity` تاريخي مستقل.

## الأنواع الإدارية حسب البلد

| ISO | البلد | الأنواع المرتبة أو المتوازية في v1 |
|---|---|---|
| JO | الأردن | `jo_governorate` → `jo_liwa` → `jo_qada`; والبلدية مسار محلي موازٍ حيث يلزم |
| AE | الإمارات | `ae_emirate` ثم نوع سياقي خاص بكل إمارة: `ae_abu_dhabi_municipality_jurisdiction`، `ae_dubai_planning_sector`/`ae_dubai_planning_community`، `ae_sharjah_municipality_jurisdiction`، `ae_ajman_constituent`، `ae_uaq_municipal_authority`، `ae_rak_administrative_area`، أو `ae_fujairah_municipal_authority`؛ لا توجد طبقة اتحادية سفلية موحدة |
| BH | البحرين | `bh_governorate` → `bh_area` → `bh_block`؛ الدائرة الانتخابية ليست بديلًا إداريًا تلقائيًا |
| DZ | الجزائر | `dz_wilaya` → `dz_daira` → `dz_commune`; الولايات المنتقلة إلى كامل الصلاحيات تبقى `proposed` أو `transitional` حتى تاريخ النفاذ |
| SA | السعودية | `sa_region` → `sa_governorate` → `sa_markaz` |
| SD | السودان | `sd_state` → `sd_locality` → `sd_administrative_unit`; توسم تغيرات الحرب/السيطرة زمنيًا |
| SO | الصومال | `so_federal_member_state`, `so_region`, `so_district`; مسارات الأمر الواقع/المتنازع لا تُدمج مع القانوني |
| IQ | العراق | `iq_governorate` → `iq_district` → `iq_subdistrict` |
| KW | الكويت | `kw_governorate` → `kw_area` → `kw_block` |
| MA | المغرب | `ma_region` → `ma_prefecture`/`ma_province` → `ma_commune` |
| YE | اليمن | `ye_governorate` أو `ye_capital_municipality` → `ye_district` → `ye_uzla` → مكان مأهول |
| TN | تونس | `tn_governorate` → `tn_delegation` → `tn_imada`; `tn_municipality` مسار لامركزي لا يُفترض مطابقته للمعتمدية |
| KM | جزر القمر | `km_island` → `km_prefecture` → `km_commune` |
| DJ | جيبوتي | `dj_region`/`djibouti_city` → `dj_subprefecture`/`dj_commune` حسب الاختصاص |
| SY | سوريا | `sy_governorate` → `sy_district` → `sy_subdistrict` |
| OM | عُمان | `om_governorate` → `om_wilaya` → `om_niyaba` |
| PS | فلسطين | `ps_governorate` → `ps_local_government_unit` أو `refugee_camp`/مكان مأهول مع توضيح الاختصاص |
| QA | قطر | `qa_municipality` → `qa_zone` → `qa_district` |
| LB | لبنان | `lb_governorate` → `lb_district` → `lb_municipality` |
| LY | ليبيا | `ly_municipality` حالي؛ `ly_shabiya_historical` تاريخي مستقل؛ `ly_mahalla` تحت بلدية موثقة فقط |
| EG | مصر | `eg_governorate` → `eg_markaz`/`eg_qism` → `eg_local_unit`/`eg_shiyakha` وفق حضري/ريفي |
| MR | موريتانيا | `mr_wilaya` → `mr_moughataa` → `mr_commune` |

الأنواع المتوازية لا تعني إمكان وضع أحدها والدًا للآخر. يحدد manifest المسارات الصحيحة لكل بلد، وتتحقق منها الأدوات.

### ملاحظة توافق الإمارات

الأنواع العامة القديمة `ae_municipal_region` و`ae_sector` و`ae_district` باقية في مفردات Schema 2.0.0.0.0 كي لا تنكسر السجلات القديمة، لكنها **مهملة للبيانات الإماراتية الجديدة** ولا يستخدمها الطيار الإماراتي. يرفض المدقق الخاص بالإمارات ظهورها في أي كيان محلي جديد. الأنواع السياقية لا تجعل «municipality jurisdiction»، و«planning sector»، و«constituent»، و«municipal authority»، و«administrative area» مترادفات؛ كل نوع يحتفظ بتعريف الجهة الرسمية واختصاصه ووالده في لقطة المصدر.

## الحالة الزمنية والقانونية

القيم المسموح بها:

- `current`: فاعل في اللقطة المعلنة.
- `historical`: انتهى قبل اللقطة؛ يجب تحديد الزمن قدر الإمكان.
- `destroyed`: المكان المادي مدمّر؛ لا يعني زوال الهوية التاريخية.
- `displaced`: مجتمع/سكان مهجّرون؛ لا يُستخدم بدل `destroyed`.
- `disputed`: الهوية أو التبعية محل نزاع موثق.
- `de_facto`: قائم فعليًا من غير مساواته بالوضع القانوني.
- `claimed`: مدّعى من جهة محددة.
- `proposed`: مقترح لم يدخل النفاذ.
- `transitional`: صدر التغيير لكن نفاذه/صلاحياته مرحلية.
- `uncertain`: المصدر لا يحسم الوضع؛ سبب عدم الحسم إلزامي في الملاحظات.
- `renamed`: وحدة سابقة تغيّر اسمها رسميًا مع حفظ هويتها الزمنية؛ الاسم السابق وحده يمكن أن يبقى Alias إذا لم تتغير هوية الوحدة.
- `merged`: وحدة سابقة انتهت باندماج موثق في وحدة أخرى؛ لا تدخل الشجرة الحالية.
- `abolished`: وحدة أُلغيَت رسميًا من دون افتراض خليفة غير موثق؛ لا تدخل الشجرة الحالية.

يمكن لعلاقات الكيان أن تحمل حالة مختلفة عنه. مدينة حالية مثلًا قد تكون علاقتها الإدارية `disputed`.

## أنواع Alias

`alternative`, `english`, `transliteration`, `local`, `historical`, `former`, `abbreviation`, `official_variant`. الاسم السابق الذي لا يغيّر هوية وحدود الكيان Alias زمني؛ أما إذا تغيّرت الوحدة أو الحدود تغيّرًا جوهريًا فكيان تاريخي مستقل وعلاقة `historic_successor`.
