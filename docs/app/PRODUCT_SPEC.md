# PRODUCT_SPEC — مواصفة المنتج: تطبيق موسوعة العرب

## 1. الرؤية

تحويل **مشروع العرب (Schema 2.0.0)** من مستودع بيانات إلى **تطبيق موسوعي عربي حقيقي** يحافظ على 100% من البيانات، يعمل Offline، ويقدم تجربة باحث ومستكشف.

## 2. المشكلة الحالية

- البيانات منظمة ومحققة (5317 كيان، 151 مصدر، validation PASS) لكنها بلا واجهة.
- `generated/html` جدول خام لا يصلح لمستخدم عادي.
- لا بحث سريع على الأسماء البديلة.
- لا عرض للعلاقات، التاريخ، القيود، المصادر بشكل موسوعي.

## 3. الهدف (Product Goal)

**بناء واجهة كاملة فوق Release Dataset** تضمن:

- كل Entity/Alias/Relationship/Claim/Source/Denominator/Coverage/Snapshot/Manifest قابل للوصول
- حتى المعلومات غير الموثقة تظهر كـ UNVERIFIED مع سبب
- لا حذف، لا اختصار، لا بيانات وهمية
- Read-only في النسخة الأولى

## 4. ما لن نفعله (Non-Goals) في APP-1

- لا إضافة دول جديدة
- لا توسيع مدن/قرى (ممنوع التوسع البحثي)
- لا نظام مساهمات/كتابة من المستخدمين
- لا خريطة polygons ضخمة قبل وجود هندسة موثقة
- لا اختراع إحداثيات مفقودة

## 5. المستخدمون

- **Explorer (عادي):** يبحث عن "الرياض" أو "مقشن" ويجد معلومات موثوقة سريعة
- **Researcher (باحث):** يحتاج IDs، مصادر، denominators، timeline، verification_status، raw JSON
- **المطور:** يريد تحميل CSV/JSON الأصلي

## 6. المتطلبات الوظيفية

### الصفحة الرئيسية
- بحث عام (يشمل canonical_name + alias.name + historical)
- شبكة الدول العربية الـ22 مع علم (إن مرخص) + عدد Entities + حالة التغطية
- تصفح حسب نوع المكان (country, governorate, wilaya, markaz, municipality...)
- قسم "أحدث التحديثات" من snapshots مرتبة بـ captured_at
- قسم "حالة البيانات" إجمالي counts + complete vs incomplete layers

### صفحة الدول العربية
- قائمة 22 دولة
- لكل دولة: الاسم العربي، ISO2، عدد Entities، عدد Claims، عدد Sources، آخر Snapshot، عدد الطبقات المكتملة من Coverage

### صفحة الدولة (مثال SA)
أقسام (Tabs):
- نظرة عامة: entity country + caveats من manifest + counts
- التقسيم الإداري: hierarchy من manifest + جدول Coverage/Denominator
- الطبقات: لكل layer (sa_region, sa_governorate, sa_markaz...) بطاقة تظهر definition, denominator, matched, unmatched, excluded, coverage_percentage, license, source
- الأماكن: قائمة Entities لهذه الدولة مع فلترة حسب النوع والحالة
- المصادر: كل Sources الخاصة بهذه الدولة
- التغطية والقيود: نص missing_reason إن وجد
- البيانات الخام: manifest JSON + coverage JSON

### صفحة المكان (Entity Page)
**الهوية:**
- الاسم الرسمي + اللغة
- الأسماء البديلة مجمعة حسب kind و language
- النوع + ترجمة عربية لنوع الكيان
- الدولة + الوالد (parent) + الأبناء (children) + العلاقات الأخرى (boundary_intersects, located_in...)
- الحالة (current/historical...) مع Badge
- الفترة الزمنية valid_from/to + Timeline إن تعددت الحالات
- الإحداثيات إن وجدت + زر فتح في OSM (لا نخترع خريطة إن لا توجد)
- المصدر القانوني canonical_source_id + locator

**المعلومات:**
- جميع Claims حيث subject_id = هذا الكيان، مجمعة حسب predicate
- كل Claim يظهر value, classification, status, confidence, verification, source, second_source إن وجد, lexical_context إن وجد

**المصادر:**
- كل Sources المرتبطة (canonical + من Claims + من Aliases + من Relationships)
- بطاقة المصدر: title, publisher, type, quality_tier, license, publication_date, retrieved_at, url (يتطلب إنترنت), archive_url, checksum, locator

**العلاقات:**
- شجرة الوالد/الأبناء
- كل Relationships مع نوعها وحالتها ومصدرها
- لا نخفي أي علاقة، حتى boundary_intersects

**البيانات الخام (Research Mode):**
- raw Entity JSON
- raw Aliases JSON
- raw Claims JSON

### البحث
- يعمل على: canonical_name, alias.name (كل الأنواع), entity_type, country_code, historical names
- مثال "مقشن" يجد ENT-OM-WILAYA-... حتى لو كان alias
- نتائج مع تمييز: اسم مطابق تماماً، alias، تاريخي
- فلترة حسب الدولة والنوع والحالة
- FTS سريع Offline (IndexedDB + Fuse.js أو SQLite FTS5)

### وضع الباحث (Research Mode Toggle)
- Explorer Mode: واجهة نظيفة، يخفي IDs الطويلة، يركز على الأسماء والمصادر المختصرة
- Research Mode: يظهر كل شيء: ENT-..., CLM-..., SRC-..., REL-..., verification_status, confidence, legacy_ids, schema_version, raw JSON, denominators, snapshots

### الخرائط
- Phase 1: عرض الإحداثيات المتوفرة فقط (2746 كيان). لا polygon، لا تخمين.
- زر "عرض على OpenStreetMap"
- Phase 2 لاحقاً: polygons عندما تتوفر من مصدر رسمي

### حالة التوثيق
Mapping واضح:
- verified/source_verified → 🟢 موثق
- partial → 🟡 موثق جزئياً
- reported/historical → 🟠 تاريخي/منقول
- ambiguous/uncertain → ⚪ غير محسوم
- disputed → 🔴 متنازع
- rejected/retracted → ⚫ مرفوض/مسحوب

إذا ظهرت حالة جديدة → تعرض كما هي.

### التواريخ
- Current/Historic badge
- valid_from/to
- snapshot_date
- captured_at
- Timeline إذا Entity له أكثر من relationship بحالات زمنية مختلفة

### Offline
- البيانات الأساسية (entities, aliases, relationships, claims, sources, denominators, coverage, snapshots, manifests) تعمل Offline
- الروابط الخارجية (url, archive_url) تحتاج إنترنت، نعرض تنبيه
- PWA: Service Worker precache للـ bundle المضغوط

## 7. المتطلبات غير الوظيفية

- RTL عربي من البداية
- الأداء: بحث < 200ms لـ 5317 entity + 3261 alias Offline
- التحديث: عند صدور Release Dataset جديد، التطبيق يحدث bundle ويعيد Data Completeness Test
- لا نسخة ثانية من البيانات في كود الواجهة

## 8. التقنية (مقارنة أولية)

انظر ARCHITECTURE.md — القرار النهائي: **Web/PWA أولاً (Next.js 14 + TypeScript + Tailwind + Dexie IndexedDB) مع Data Contract يسمح ببناء Android Kotlin لاحقاً بنفس العقد.**

## 9. مقاييس النجاح

- 100% من counts مطابقة لـ metadata.json
- Data Completeness Test ينجح في CI
- بحث "مقشن" يجد الكيان حتى لو alias
- كل Entity page تعرض على الأقل: هوية، مصادر، علاقات، claims (إن وجدت)، raw
- يعمل Offline بعد أول تحميل
- لا broken links داخلية

## 10. المراحل

- **APP-0:** Inventory, Contract, Architecture, UI/UX Spec, Import Strategy, Completeness Test (هذا الملف)
- **APP-1:** Home, Countries, Country page, Entity page, Search, Sources, Research Mode, Offline bundle
- **APP-2:** Maps (coordinates), Timeline, Relationship Explorer, Coverage advanced filters
- **APP-3:** Offline optimization, performance, release packaging, final QA
