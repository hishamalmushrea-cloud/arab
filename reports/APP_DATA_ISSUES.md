# APP_DATA_ISSUES — سجل مشاكل البيانات المكتشفة أثناء تصميم التطبيق

> **القاعدة:** لا نصلح البيانات صامتاً داخل التطبيق. أي إصلاح يجب أن يمر عبر Source Dataset → generate → Release Dataset.

## تاريخ الفحص: 2026-08-17
## المدقق: APP-0 Data Inventory

### 1. ملخص عام

- Validation الحالي: **PASS مع صفر أخطاء** (scripts/validate.py)
- Counts مطابقة لـ metadata.json: 5317/3261/5706/2245/151/112/112/28
- لا يوجد duplicate IDs، لا orphans، لا cycles

### 2. مشاكل غير حرجة (By Design — وليست أخطاء)

#### 2.1 الإحداثيات
- 2746 كياناً فقط لها coordinates (من 5317) → **51.6%**
- الباقي null بتصميم (notes تقول "Administrative entities do not receive invented point coordinates")
- **الإجراء في التطبيق:** لا نعرض خريطة وهمية. نعرض رسالة "لا توجد إحداثيات موثقة لهذا الكيان في لقطة 2026-08-15" + نعرض زر OSM فقط إن وجدت.
- **لا يحتاج إصلاح.**

#### 2.2 حالات Entity غير current
- current: 5278
- historical: 27 (مثل ly_shabiya_historical)
- proposed: 11 (مثل dz_wilaya المستقبلية 11 ولاية لنفاذ 2027)
- claimed: 1
- **التطبيق:** يجب عرض Timeline وBadge واضح. ليست مشكلة.

#### 2.3 حالات Claim غير verified
- verified: 2230
- historical: 7
- reported: 7
- disputed: 1
- **التطبيق:** عرضها في قسم "معلومات غير محسومة/تاريخية" مع تحذير، لا تحذف.

#### 2.4 Denominators غير official
- بعض denominators status=conflicted/unavailable/provisional (مثل SA current-national governorate conflicted, neighborhoods denominator_unavailable)
- **هذا مقصود** حسب schema_v2.md لتجنب اختراع مقام.
- **التطبيق:** يعرض missing_reason بدل نسبة. لا يحتاج إصلاح.

#### 2.5 Coverage غير مكتمل
- complete=true لـ 95 طبقة، false لـ 17 طبقة (neighborhoods, populated_places...)
- **مقصود.** التطبيق يجب أن يعرض "المقام غير متاح" لا 0%.

#### 2.6 Alleged محافظات/ولايات counts متضاربة (موثقة في manifests.caveats)
- SA: Saudipedia يذكر 150 محافظة وطنياً بينما الجداول الإقليمية 1528 وتستخرج 1521 — تم توثيقه كـ conflicted denominator، وليس خطأ في التطبيق.
- **الإجراء:** عرض caveats في صفحة الدولة.

### 3. مشاكل محتملة تحتاج مراجعة (ليست مانعة لـ APP-1)

#### 3.1 Tunisia imada عدد كبير
- 2084 عمادة، لكن بعضها قد يكون بدون إحداثيات. لا مشكلة، لكن في الخريطة سنعرض فقط التي لها إحداثيات.

#### 3.2 السعودية ماركز 1521 مع notes "factual extraction"
- قانوني، لكن يجب التأكد license عرضها في التطبيق (Source copyright; factual extraction with attribution) — سنعرض license في كل Coverage.

#### 3.3 بعض Aliases language null?
- فحص عينة: كل aliases لها language (ar/en/fr...) — جيد.

#### 3.4 بعض Claims second_source_id null (معظمها)
- مقصود حسب Schema: فقط الحساسة تحتاج مصدر ثانٍ. لا مشكلة.

### 4. لا يوجد BLOCKER لـ APP-0 / APP-1

- لا فقدان بيانات متوقع
- لا schema mismatch
- لا broken links (951 link checked, 0 broken حسب validate)

### 5. ما سيتم إصلاحه عبر Source Dataset لاحقاً (إن لزم)

- إذا اكتشفنا أثناء بناء التطبيق أن ترجمة entity_type للعربية ناقصة، سنضيف ملف `app/src/data/labels_ar.json` منفصل، لا نعدل البيانات الأصلية.
- إذا وجدنا أن "مقشن" لا يظهر في البحث بسبب normalization، سنحسن `arabicNormalize.ts` في التطبيق، لا نعدل alias.

### 6. توصية

- متابعة APP-0 و APP-1 بدون إصلاح بيانات.
- أي مشكلة تظهر أثناء `test_app_data_completeness.py` تُسجل هنا أولاً.

**الحالة:** ✅ جاهز للانتقال إلى APP-1
