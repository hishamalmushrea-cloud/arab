# UI_UX_SPEC — مواصفة واجهة المستخدم (عربي RTL موسوعي حديث)

## 1. المبادئ

- **RTL من البداية:** `dir="rtl" lang="ar"` في layout.tsx، Tailwind RTL plugin، لا LTR إلا لأكواد IDs
- **الجمال لا يحذف بيانات:** كل معلومة موجودة، حتى لو في Accordion متقدم
- **موسوعي حديث:** Cards, Tabs, Breadcrumbs, Timeline, Relationship Explorer، ليس جدول JSON خام
- **وضعان:** Explorer (سهل) و Research (تفصيلي)

## 2. نظام الألوان والحالات

- خلفية: `#FFFEFB` (ورقي)
- نص أساسي: `#1A1A1A`
- ثانوي: `#6B7280`
- حدود: `#E5E7EB`
- Badge موثق: 🟢 أخضر #10B981
- جزئي: 🟡 أصفر #F59E0B
- تاريخي: 🟠 برتقالي #F97316
- غير مؤكد: ⚪ رمادي #9CA3AF
- متنازع/مدّعى: 🔴 أحمر #EF4444
- مرفوض: ⚫ أسود #111827

## 3. الخطوط

- عربي: IBM Plex Sans Arabic أو Tajawal
- إنجليزي/كود: JetBrains Mono للأكواد IDs
- أحجام: h1 32px, h2 24px, body 16px, caption 14px

## 4. الصفحة الرئيسية `/`

**Header:**
- شعار "العرب" + Research Mode Toggle (مفتاح)
- شريط بحث كبير وسط الصفحة (placeholder: "ابحث عن مكان، اسم بديل، محافظة... مثل: مقشن، الرياض، حلبجة")

**Hero Stats:**
- 5317 كيان، 22 دولة، 151 مصدر، 2245 معلومة موثقة، 28 لقطة — أرقام حية من counts.json، ليست hard-coded

**شبكة الدول:**
- 22 بطاقة دولة: علم (إن مرخص، وإلا أيقونة)، اسم عربي، ISO2، عدد الكيانات، عدد الطبقات المكتملة (من coverage.complete)، آخر snapshot date

**تصفح سريع:**
- حسب نوع المكان: قائمة entity_types الأكثر شيوعاً (tn_imada 2084, sa_markaz 1521...)
- حسب الحالة: current, historical, proposed
- حسب التغطية: طبقات مكتملة / غير مكتملة

**أحدث التحديثات:**
- Snapshots مرتبة بـ captured_at تنازلي، كل snapshot يظهر title + scope + date

**حالة البيانات:**
- رابط إلى /coverage يظهر 112 denominator/coverage

**Footer:**
- روابط: المصادر، التغطية، البيانات الخام (JSON/CSV download)، عن المشروع، الترخيص

## 5. صفحة الدول `/countries`

- Search + Filter حسب المجموعة الإقليمية (شبه الجزيرة، الهلال، وادي النيل، المغرب العربي، القرن الإفريقي) من 00_الخطة_التنفيذية.md لكن لا hard-code أعداد، بل فلترة countryCode
- جدول: الدولة | ISO | عدد Entities | عدد Claims | عدد Sources | الطبقات المكتملة | آخر Snapshot | القيود (إن وجد missing_reason)

## 6. صفحة الدولة `/[iso2]` مثال `/SA`

**Breadcrumbs:** الرئيسية > الدول > السعودية

**Header الدولة:**
- اسم عربي + إنجليزي، ISO2، entity country
- caveats من manifest كـ Alert أصفر
- Stats: 13 منطقة، 141 محافظة، 1521 مركز (كلها من coverage، لا hard-code)

**Tabs (8-10):**
1. **نظرة عامة:** تعريف الدولة من Entity + counts + caveats
2. **التقسيم الإداري:** يعرض hierarchy من manifest: لكل level بطاقة تظهر local_names, authority_name, denominator, license, source_ids
3. **الطبقات:** جدول Coverage: layer | definition | denominator | matched | unmatched | excluded | coverage% | complete | missing_reason | source
4. **الأماكن:** قائمة Entities لهذه الدولة، مع فلتر حسب entity_type + status + search محلي. Pagination 50
5. **الخريطة (مبدئياً إحداثيات):** قائمة الكيانات التي لها coordinates + زر "عرض على OSM". لا خريطة وهمية إن لا توجد إحداثيات. رسالة: "2746 كياناً لها إحداثيات موثقة من أصل 5317"
6. **المصادر:** كل Sources حيث country_codes contains iso2 أو source_id مرتبط بـ entities of this country
7. **التغطية والقيود:** نصوص notes من coverage و denominators، خاصة status=conflicted/unavailable
8. **البيانات الخام:** JSON viewer لـ manifest + coverage لهذه الدولة + زر تحميل CSV

## 7. صفحة المكان `/[iso2]/[entityId]` مثال `/SA/ENT-SA-REGION-RIYADH`

**Breadcrumbs:** الرئيسية > السعودية > منطقة الرياض

**Header الكيان:**
- Badge الحالة (current/historical...) + Badge التحقق
- الاسم الرسمي كبير + اللغة
- النوع المترجم: "منطقة إدارية" + الكود الأصلي sa_region
- الدولة + الوالد (رابط) + عدد الأبناء

**Tabs:**

### Tab 1: الهوية
- canonical_name + language
- الأسماء البديلة: جدول مجمع حسب kind (alternative, english, historical...) كل alias يظهر name, language, script, kind, status, valid_from/to, source + locator
- نوع الكيان + وصف
- الدولة، الوالد (administrative_parent)، الأبناء (list)، العلاقات الأخرى (located_in, boundary_intersects...) مع تمييز نوع العلاقة
- الحالة + valid_from/to + Timeline (إذا له أكثر من status عبر الزمن من relationships)
- الإحداثيات إن وجدت: lat/lon + دقة + مصدر + زر OSM
- المصدر القانوني: canonical_source_id + locator + license
- legacy_ids + notes + schema_version (في Research Mode)
- raw JSON collapsible

### Tab 2: المعلومات (Claims)
- مجمعة حسب predicate (population, administrative_center, etc.)
- كل Claim card:
  - value (مع type و unit)
  - classification (official/popular/shared...)
  - status + confidence + verification_status + badges
  - observed_at, valid_from/to
  - source + locator + second_source إن وجد
  - lexical_context إن وجد: form, meaning, language, dialect, ipa...
  - notes
- إذا claim.status=disputed/uncertain → يظهر في قسم منفصل "معلومات غير محسومة" مع سبب

### Tab 3: المصادر
- كل مصدر مرتبط: canonical + من Aliases + من Relationships + من Claims
- بطاقة المصدر: title, publisher, author, source_type, quality_tier (A/B/C/D), language, license, publication_date, retrieved_at, url (link خارجي + badge "يتطلب إنترنت"), archive_url, checksum, locator, notes

### Tab 4: العلاقات
- شجرة تفاعلية: الوالد في الأعلى، الحالي في الوسط، الأبناء في الأسفل
- قائمة كاملة لكل Relationships مع نوعها، حالتها، فترتها، ثقتها، مصدرها
- boundary_intersects تظهر بلون مختلف مع نص "تقاطع حدودي، ليس والد إداري"

### Tab 5: التاريخ والقيود
- Timeline إذا له valid_from/to متعددة أو status تاريخي
- إذا status=historical/proposed/claimed/disputed → يعرض notes و missing_reason
- إذا لا توجد إحداثيات → رسالة "لا توجد إحداثيات موثقة في لقطة 2026-08-15"

### Tab 6: البيانات الخام (Research Mode فقط)
- raw Entity JSON
- raw Aliases JSON array
- raw Relationships JSON array
- raw Claims JSON array
- زر Copy JSON

## 8. البحث `/search?q=...`

- Input كبير مع Arabic normalization (إزالة تشكيل، توحيد ة/ه، ي/ى)
- يبحث في: canonical_name, alias.name (كل الأنواع), entity_type, country_code
- نتائج مع: 
  - اسم مطابق تماماً → Badge "مطابق"
  - Alias → يظهر "اسم بديل: مقشن (محلي)"
  - Historical → Badge "تاريخي"
- كل نتيجة بطاقة: اسم، نوع، دولة، والد، حالة، عدد Claims
- فلترة: الدولة، النوع، الحالة، له إحداثيات؟
- مثال البحث عن "مقشن" يجب أن يجد ENT-OM-WILAYA-... حتى لو alias

## 9. صفحة المصادر `/sources` و `/sources/[id]`

- قائمة 151 مصدر مع فلتر حسب quality_tier, source_type, country
- كل مصدر بطاقة: title, publisher, type, tier, license, publication_date, عدد الكيانات التي تستخدمه
- صفحة تفصيلية: كل الحقول + قائمة الكيانات والClaims التي تستخدمه + رابط url/archive_url

## 10. صفحة التغطية `/coverage`

- جدول 112 coverage مع فلتر حسب الدولة والطبقة
- كل صف: layer, definition, denominator, matched, coverage%, complete, status, missing_reason
- إذا coverage_percentage=null → يعرض missing_reason بدل نسبة مخترعة
- رابط إلى Denominator detail

## 11. وضع الباحث Toggle

- Switch في Header: "وضع الباحث"
- محفوظ في localStorage
- Explorer OFF: واجهة نظيفة، IDs مخفية، raw مطوي
- Research ON: يظهر كل IDs، verification_status, confidence, legacy_ids, schema_version, raw JSON expandable, snapshots, denominators

## 12. التصميم المتجاوب

- Mobile: Tabs تتحول إلى Accordion، بطاقات عمودية
- Desktop: Sidebar للفلترة + Main content
- RTL: كل شيء من اليمين لليسار، بما في ذلك Breadcrumbs (الرئيسية أولاً يميناً)

## 13. عدم فقدان البيانات في UI

- أي حقل null → يعرض "غير متوفر في هذه اللقطة" + missing_reason إن وجد، لا يحذف الصف
- أي علاقة → تظهر، حتى boundary_intersects
- أي alias → يظهر ويُبحث
- أي claim حتى controversial → يظهر في قسم "غير محسوم" مع مصدره
- زر "عرض البيانات الخام" في كل صفحة

## 14. أمثلة User Flows

- مستخدم يبحث "الرياض" → يجد ENT-SA-REGION-RIYADH + ENT-SA-CITY-RIYADH (إن وجد) + aliases
- باحث يريد مصادر السعودية → /SA تبويب المصادر → يرى 8 مصادر قانونية + UNESCO + GASTAT
- باحث يريد لماذا ليست هناك أحياء في SA → /SA تبويب التغطية → يرى layer neighborhoods missing_reason=denominator_unavailable + license

## 15. الأداء

- Search <200ms
- Entity page <500ms بعد تحميل bundle
- Bundle 3.5 MB Brotli → تحميل أول مرة 2-3 ثانية على 3G، ثم offline فوري
