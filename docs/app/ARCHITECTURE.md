# ARCHITECTURE — بنية التطبيق والحفاظ على البيانات

## 1. القرار التقني النهائي

بعد دراسة المشروع والمتطلبات (100% حفظ بيانات، Offline، بحث سريع، تحديث سهل، توسع، أداء، صيانة):

### المقارنة

| المعيار | Android Native (Kotlin + Compose + Room) | Web/PWA (Next.js + TS + IndexedDB) | الفائز |
|---------|-------------------------------------------|-------------------------------------|--------|
| **100% حفظ بيانات** | ممكن، لكن يحتاج تحويل JSON → Room Entities + Migration | مباشر: JSON → IndexedDB بدون فقدان، نفس Schema | Web |
| **Offline** | ممتاز (SQLite) | جيد جداً (Service Worker + IndexedDB 50MB+، bundle 3.5 MB مضغوط) | تعادل، Android أفضل قليلاً لكن Web كافٍ |
| **البحث السريع** | Room FTS5 سريع جداً | Fuse.js + Dexie + ممكن WASM SQLite (sql.js) <200ms لـ 8k سجل | تعادل |
| **سهولة التحديث** | يحتاج Release على Play Store + موافقة المستخدم | Deploy جديد + PWA auto-update، المستخدم يرى التحديث فوراً | Web |
| **قابلية التوسع** | فقط Android، تحتاج iOS لاحقاً codebase ثانٍ | Web يعمل على Android/iOS/Desktop بنفس الكود، ثم تغليف بـ Capacitor لـ Native | Web |
| **الأداء** | Native أفضل للخرائط الثقيلة | كافٍ لـ 5317 كيان، 11 MB JSON، مع Brotli + code splitting | تعادل للمرحلة الحالية |
| **سهولة الصيانة** | Kotlin فريق واحد، لكن CI/CD أثقل | Single codebase TypeScript، Vercel deploy، أسرع iteration | Web |
| **اكتشافية ومشاركة** | APK/APK link فقط | URLs قابلة للمشاركة (/SA/ENT-SA-... )، SEO، Open Graph | Web |

### القرار

**Phase APP-1: Web/PWA هو المنتج الأساسي.**

**السبب:**
1. يحقق شرط 100% حفظ بيانات بأقل تحويل (JSON→JSON)، أقل خطر فقدان.
2. يحقق Offline للبيانات الأساسية (الـ bundle 3.5 MB بعد Brotli).
3. أسهل تحديث للبيانات (Release Dataset → new bundle → deploy).
4. يسمح بمشاركة روابط الموسوعة (مهم لمشروع ثقافي).
5. نفس Data Contract يُستخدم لاحقاً لبناء Android Kotlin (Room) بدون إعادة تصميم البيانات.

**Phase APP-3 (لاحقاً):** نفس Web App يُغلف بـ **Capacitor** إلى Android APK، أو يُبنى **Kotlin app** منفصل يستهلك نفس `app-data.json` ويستورد إلى Room باستخدام `scripts/import_to_sqlite.py` الذي سنبنيه الآن.

> **إذن لا نختار Android كـ exclusive، بل نختار Shared Data Layer + PWA أولاً، مع قابلية Android Native لاحقاً.**

## 2. البنية العامة

```
Source Data (data/ + manifests/ + schema/)
      ↓
  validate.py (يجب PASS)
      ↓
  generate.py → Release Dataset (generated/json/*.json + metadata.json)
      ↓
  scripts/build_app_bundle.py  [APP-0]
      ↓
  app/public/data/
      - app-data.json.br (Brotli compressed canonical bundle)
      - manifests.json
      - schema.json (vocabularies)
      - counts.json (for completeness)
      ↓
  App Data Layer (TypeScript + Dexie)
      - IndexedDB: entities, aliases, relationships, claims, sources, denominators, coverage, snapshots, manifests
      - Search Index: Fuse.js index built on client from aliases + entities
      ↓
  UI Layer (Next.js App Router)
      - / → Home
      - /countries → Countries list
      - /[iso2] → Country page (SA, TN...)
      - /[iso2]/[entityId] → Entity page
      - /search?q=مقشن → Search
      - /sources → Sources list
      - /sources/[sourceId] → Source detail
      ↓
  Data Completeness Test (scripts/test_app_data_completeness.py)
      ↓
  PWA Service Worker (next-pwa)
      - precache app-data.json.br
      - offline fallback
      ↓
  Build → Vercel / Static Export → Live Preview
```

## 3. Shared Data Layer

### TypeScript Interfaces
`app/src/data/types.ts` — مولد جزئياً من `schema/vocabularies.json` + `DATA_CONTRACT.md`، يحوي كل AppEntity, AppAlias...

### Import Pipeline

```python
# scripts/build_app_bundle.py
- read generated/metadata.json -> expected counts
- read generated/json/canonical_bundle.json (11 MB)
- validate counts == expected
- for each family, check no field dropped (compare keys vs schema)
- compress with Brotli (quality 11)
- write app/public/data/app-data.json.br
- write app/public/data/counts.json
- write app/src/data/schema.ts (vocabularies as const)
```

### IndexedDB Schema (Dexie)

```ts
db.version(1).stores({
  entities: 'id, countryCode, entityType, status, canonicalName',
  aliases: 'id, entityId, name, kind, language',
  relationships: 'id, childId, parentId, relationshipType',
  claims: 'id, subjectId, predicate, status',
  sources: 'id, qualityTier, sourceType',
  denominators: 'id, countryCode, layer',
  coverage: 'id, countryCode, layer, denominatorId',
  snapshots: 'id, sourceId',
  manifests: 'iso2'
});
```

### SQLite Schema (للـ Android لاحقاً) — نفس الحقول

```sql
CREATE TABLE entities (id TEXT PRIMARY KEY, canonical_name TEXT, ... raw_json TEXT);
-- raw_json يحفظ كل الحقل الأصلي لضمان عدم الفقدان حتى لو نسينا عمود
```

حقل `raw_json` هو ضمان إضافي: حتى لو لم نعرض field في UI، يبقى محفوظ.

## 4. Search Architecture

- **Index Building (client-side, once):**
  - documents = entities.map(e => { id, canonicalName, countryCode, entityType, aliases: aliases.filter(a=>a.entityId==e.id).map(a=>a.name) })
  - Fuse.js options: keys: ['canonicalName','aliases'], threshold 0.3, includeScore, Arabic normalization (إزالة تشكيل، توحيد ي/ى)
- **FTS fallback:** إذا كبرت البيانات، نستخدم `sql.js` WASM SQLite FTS5.
- **مثال:** بحث "مقشن" → يجد alias.kind=local name="مقشن" → entity ENT-OM-WILAYA-...

## 5. Offline Strategy

- **PWA:** next-pwa Workbox
  - precache: `app-data.json.br`, static assets, pages
  - runtime cache: images, OSM tiles (إن استخدمت)
  - fallback: /offline page يظهر البيانات الأساسية من IndexedDB
- **Data:** بعد فك الضغط، تخزين في IndexedDB → كل navigation يقرأ من IndexedDB، لا fetch جديد
- **External links:** sources url/archive_url → تحتاج إنترنت، نعرض badge "يتطلب إنترنت"

## 6. Research Mode vs Explorer Mode

- **State:** Zustand store `useResearchMode` boolean, محفوظ في localStorage
- **Explorer:** يخفي raw JSON, IDs الطويلة truncated, يعرض أسماء فقط
- **Research:** يظهر كل شيء، مع زر Copy JSON, Copy ID, عرض verification_status, confidence, legacy_ids

## 7. CI / Data Completeness Gate

```yaml
# .github/workflows/validate.yml (إضافة)
- run: make validate
- run: make generate
- run: python3 scripts/build_app_bundle.py
- run: python3 scripts/test_app_data_completeness.py # يقارن counts + fields
- run: npm run build # Next.js build يجب أن ينجح حتى مع offline bundle
- run: npm run test:search # بحث عن عينات مثل "مقشن"
```

أي FAIL → يمنع merge.

## 8. عدم تكرار البيانات

- لا يوجد `const SA_REGIONS = 13` في كود الواجهة. كل الأرقام تأتي من `coverage` و `denominators`
- لا يوجد `Saudi has 13 regions` hard-coded. يُقرأ من `DEN-SA-REGIONS-20260815`
- حتى ترجمة نوع الكيان (sa_region → "منطقة إدارية") تأتي من قاموس `entity_type_labels_ar.json` منفصل، لكن العدد يأتي من البيانات

## 9. الأداء

- Bundle 11 MB JSON → Brotli 3.5 MB → فك ضغط client-side بـ 200ms
- Code splitting: صفحة الدولة تحمل فقط entities لتلك الدولة (filter countryCode)
- Lazy load للـ claims الثقيلة
- Images: لا صور حالياً، لكن عند إضافة أعلام، استخدام next/image + remote cache

## 10. الأمان والترخيص

- عرض license لكل Source و Denominator
- عدم عرض محتوى محمي بحقوق إلا بذكر المصدر
- الروابط الخارجية تفتح في tab جديد مع rel=noopener

## 11. بنية المجلدات المقترحة للـ App

```
app/
  public/
    data/
      app-data.json.br
      counts.json
      manifests.json
  src/
    app/ (Next.js App Router)
      page.tsx (Home)
      countries/page.tsx
      [iso2]/page.tsx (Country)
      [iso2]/[entityId]/page.tsx (Entity)
      search/page.tsx
      sources/page.tsx
      layout.tsx (RTL)
    components/
      EntityCard, ClaimCard, SourceCard, RelationshipTree, Timeline, SearchBox, ResearchToggle, CoverageTable, Breadcrumbs
    data/
      types.ts (AppEntity...)
      db.ts (Dexie)
      import.ts (load bundle → IndexedDB)
      search.ts (Fuse)
      labels.ts (ترجمة أنواع)
    lib/
      arabicNormalize.ts
      format.ts
  scripts/ (خارج app)
    build_app_bundle.py
    test_app_data_completeness.py
    import_to_sqlite.py (للـ Android لاحقاً)
```

## 12. لماذا هذا يضمن 100% بيانات؟

- App Bundle هو نسخة Brotli من canonical_bundle.json نفسه، لا إعادة كتابة
- IndexedDB يخزن raw_json لكل سجل
- TypeScript types تشمل `raw: RawEntity` fallback
- Data Completeness Test يفشل إذا نقص أي count أو field
- CI يمنع build إذا تغير counts بدون تفسير
