# موسوعة العرب — تطبيق Android أصلي (Kotlin + Jetpack Compose + Room)

## الحالة: APP-1 Android MVP جاهز للفتح في Android Studio ✅

هذا المشروع هو **تطبيق Android أصلي** (ليس WebView) يقرأ نفس Release Dataset الذي يستخدمه تطبيق الويب، مع ضمان 100% حفظ البيانات.

### البيانات:
- **Source:** `app/src/main/assets/app-data.json` (8.8 MB) — نفس `generated/json/canonical_bundle.json` → `app/public/data/app-data.json`
- **Counts:** 5317 Entity, 3261 Alias, 5706 Relationship, 2245 Claim, 151 Source, 112 Denominator, 112 Coverage, 28 Snapshot, 22 Manifest
- **Preservation:** كل سجل يحفظ `rawJson` كاملاً في Room — حتى لو نسينا عمود في UI، يبقى محفوظ

### كيف يعمل Offline؟
1. أول تشغيل: `DataImporter.importFromAssets()` يقرأ `assets/app-data.json` (8.8 MB) → يحول إلى Room Entities مع `rawJson` → يبني `search_index` (canonical + alias normalized)
2. بعدها: كل navigation يقرأ من Room (SQLite) — لا يحتاج إنترنت
3. الروابط الخارجية (source url/archive_url) تحتاج إنترنت فقط

### البحث:
- يبحث في `search_index` حيث `canonicalName` + `aliasesConcatenated` + `normalizedName`
- تطبيع عربي: إزالة تشكيل، توحيد إأآا→ا، ى→ي، ة→ه
- مثال: البحث عن "مقشن" يجد الكيان حتى لو كان alias محلي

### الصفحات (Compose Navigation):
- `home` — إحصائيات من البيانات (ليس hard-coded) + شبكة الدول
- `countries` — 22 دولة
- `country/{iso2}` — 6 Tabs: نظرة عامة، تقسيم إداري، طبقات، أماكن، تغطية وقيود، خام
- `entity/{iso2}/{entityId}` — 7 Tabs: هوية (كل الحقول)، أسماء بديلة (كل kind)، معلومات/Claims (كل classification/status/lexical_context)، علاقات (مع boundary_intersects تنبيه)، مصادر (license/url), خريطة (إحداثيات فقط إن وجدت، لا اختراع), خام JSON
- `search` — بحث شامل

### كيف تفتح في Android Studio؟

1. افتح Android Studio Hedgehog أو أحدث
2. File → Open → اختر مجلد `android/` (هذا المجلد، ليس الجذر)
3. انتظر Sync Gradle (سيحمل dependencies: Compose BOM, Room 2.6.1, Navigation Compose)
4. ضع جهاز Android أو Emulator (minSdk 26)
5. Run → app

أول تشغيل سيستغرق ~10 ثواني لاستيراد 8.8 MB JSON إلى Room — بعدها Offline فوري.

### الاختبارات:

- **DATA_COMPLETENESS_TEST** مدمج في `ImportResult.isComplete()` — يتحقق 5317/3261/5706/2245/151/112/112/28/22
- **Room counts** — بعد الاستيراد: `SELECT COUNT(*) FROM entities` يجب = 5317

### الفرق بين هذا وتطبيق الويب؟

| | Web/PWA (app/) | Android Native (android/) |
|---|---|---|
| التقنية | Next.js + Dexie IndexedDB | Kotlin + Compose + Room SQLite |
| البيانات | نفس app-data.json | نفس app-data.json في assets |
| البحث | Fuse.js | Room search_index + normalized Arabic |
| Offline | Service Worker + IndexedDB | Room SQLite |
| فتح في | Browser Preview port 3000 | Android Studio |

كلاهما يحافظ على 100% من البيانات ويستخدم نفس DATA_CONTRACT.

### ملاحظات:

- لا يوجد `const SA_REGIONS = 13` في الكود — كل الأرقام من Coverage/Denominator
- لا اختراع إحداثيات: إذا `latitude==null` نعرض "لا توجد إحداثيات موثقة"
- `boundary_intersects` لا تعرض كوالد إداري بل كـ "تقاطع حدودي"
- `rawJson` محفوظ لكل سجل — Research Mode يعرضه

### Build:

```bash
cd android
./gradlew assembleDebug
# APK في app/build/outputs/apk/debug/
```

### TODO APP-2:

- PWA Service Worker
- Map: عرض إحداثيات 2746 فقط، زر OSM
- Timeline: valid_from/to
- Relationship Explorer شجرة
- Export CSV/JSON
