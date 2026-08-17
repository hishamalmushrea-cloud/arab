# DATA_CONTRACT — عقد تحويل البيانات إلى التطبيق (بدون فقدان)

> **القاعدة الذهبية:** تحويل 1:1 يحافظ على كل حقل. لا إعادة تسمية تحذف معنى، لا دمج يخفي تفصيلاً. إذا كان الحقل غير مناسب للعرض المباشر، يُحفظ في `raw` ويُعرض في Research Mode.

## 1. المبدأ

Release Dataset (Schema 2.0.0 JSON) → App Data Layer (TypeScript interfaces / Room Entities) → UI

- كل حقل أصلي يبقى بنفس الاسم أو بتحويل واضح موثق أدناه
- القيم `null` تبقى `null` ولا تُحول إلى `""`
- التواريخ تبقى ISO string
- الإحداثيات تبقى nullable ولا نخترع 0,0

## 2. Entity → AppEntity

**المصدر:** `Entity` من `entity.schema.json`
**الهدف:** `AppEntity`

```ts
interface AppEntity {
  // Identity — محفوظة تماماً
  id: string; // ENT-{ISO}-{...}
  canonicalName: string;
  canonicalNameLanguage: string; // en/ar/fr...
  canonicalSourceId: string;
  sourceLocator: string;
  countryCode: string; // ISO2
  entityType: string; // 103 نوع من vocabularies.json
  status: EntityStatus; // 13 قيمة
  validFrom: string | null; // ISO date
  validTo: string | null;
  coordinates: { lat: number; lon: number } | null;
  confidence: Confidence; // high/medium/low
  verificationStatus: VerificationStatus;
  legacyIds: string[];
  notes: string | null;
  schemaVersion: string; // 2.0.0

  // Derived — لا تحذف الأصل، تضيف فهارس
  aliases: AppAlias[]; // populated via alias.entity_id
  parent: AppEntity | null; // via relationships administrative_parent
  children: AppEntity[]; 
  allRelationships: AppRelationship[]; // كل العلاقات
  claims: AppClaim[]; // كل Claims subject_id = id
  source: AppSource; // canonicalSourceId resolved

  // UI helper — لا يحذف بيانات
  displayNameAr: string; // canonicalName إذا ar وإلا أول alias عربي
  displayTypeLabelAr: string; // ترجمة نوع الكيان للعرض (من قاموس)
  hasCoordinates: boolean;
  timeline: { status: string; from: string | null; to: string | null }[];
}
```

**قاعدة عدم الفقدان:** حتى `legacy_ids` و `notes` و `schema_version` تُحفظ وتُعرض في Research Mode تبويب "البيانات الخام".

## 3. Alias → AppAlias

```ts
interface AppAlias {
  id: string; // ALS-...
  entityId: string;
  name: string;
  language: string | null;
  script: string | null; // Arab/Latn
  kind: AliasKind; // 8 قيم
  status: EntityStatus;
  validFrom: string | null;
  validTo: string | null;
  sourceId: string;
  sourceLocator: string;
  schemaVersion: string;
  // resolved
  source: AppSource;
}
```

يُستخدم في البحث: أي بحث عن `name` يجد `entityId`. مثال "مقشن" حتى لو كان alias.

## 4. Relationship → AppRelationship

```ts
interface AppRelationship {
  id: string; // REL-...
  childId: string;
  parentId: string;
  relationshipType: RelationshipType; // 11 قيمة
  status: EntityStatus;
  validFrom: string | null;
  validTo: string | null;
  confidence: Confidence;
  verificationStatus: VerificationStatus;
  sourceId: string;
  sourceLocator: string;
  notes: string | null;
  schemaVersion: string;
  // resolved
  child: AppEntity;
  parent: AppEntity;
  source: AppSource;
}
```

**تحذير عرض:** `boundary_intersects` لا تُعرض كوالد إداري، بل كـ "تقاطع حدودي موثق" مع مصدره.

## 5. Claim → AppClaim

```ts
interface AppClaim {
  id: string; // CLM-...
  subjectId: string;
  predicate: string; // administrative_center, population, etc.
  value: { type: 'string'|'integer'|'number'|'boolean'|'date'|'json'; data: any };
  classification: ClaimClassification; // 9 قيم
  status: ClaimStatus; // verified/reported/disputed/historical/uncertain/retracted
  confidence: Confidence;
  verificationStatus: VerificationStatus;
  sensitivity: string; // ordinary
  published: boolean;
  observedAt: string | null;
  validFrom: string | null;
  validTo: string | null;
  sourceId: string;
  sourceLocator: string;
  secondSourceId: string | null;
  secondSourceLocator: string | null;
  unit: string | null;
  lexicalContext: {
    form: string | null;
    meaning: string | null;
    placeId: string | null;
    language: string | null;
    dialect: string | null;
    variety: string | null;
    register: string | null;
    studyDate: string | null;
    speakerOrStudy: string | null;
    ipa: string | null;
  } | null;
  notes: string | null;
  schemaVersion: string;
  // resolved
  subject: AppEntity;
  source: AppSource;
  secondSource: AppSource | null;
}
```

**عدم الفقدان:** حتى `lexical_context` كامل يُحفظ. إذا `value.type=json` يُعرض كـ JSON مع تنسيق.

## 6. Source → AppSource

```ts
interface AppSource {
  id: string; // SRC-...
  title: string;
  publisher: string | null;
  author: string | null;
  organization: string | null;
  countryCodes: string[];
  url: string | null;
  archiveUrl: string | null;
  publicationDate: string | null;
  retrievedAt: string | null;
  language: string | null;
  license: string | null;
  qualityTier: 'A'|'B'|'C'|'D';
  sourceType: SourceType; // 9 قيم
  checksum: string | null;
  locator: string | null;
  notes: string | null;
  schemaVersion: string;
}
```

**العرض:** license و quality_tier و locator و checksum تظهر في قسم "التوثيق المتقدم".

## 7. Denominator → AppDenominator

```ts
interface AppDenominator {
  id: string;
  countryCode: string;
  layer: string;
  definition: string;
  denominator: number;
  asOf: string | null;
  snapshotDate: string | null;
  sourceId: string;
  sourceLocator: string;
  status: 'official'|'conflicted'|'unavailable'|'provisional';
  license: string | null;
  missingReason: string | null;
  notes: string | null;
  value: number;
  schemaVersion: string;
  source: AppSource;
}
```

## 8. Coverage → AppCoverage

```ts
interface AppCoverage {
  id: string;
  countryCode: string;
  layer: string;
  denominatorId: string;
  denominator: number | null;
  matched: number;
  unmatched: number;
  excluded: number;
  exclusionReasons: string[];
  missing: number | null;
  missingReason: string | null;
  coveragePercentage: number | null;
  complete: boolean;
  snapshotId: string;
  snapshotDate: string | null;
  sourceId: string;
  license: string | null;
  notes: string | null;
  schemaVersion: string;
  denominator: AppDenominator;
  snapshot: AppSnapshot;
  source: AppSource;
}
```

**العرض:** إذا `coveragePercentage=null` → نعرض `missingReason` بدلاً من اختراع نسبة. إذا `complete=false` → نعرض القيود.

## 9. Snapshot → AppSnapshot

```ts
interface AppSnapshot {
  id: string;
  title: string;
  capturedAt: string;
  sourceId: string;
  scope: string;
  method: string;
  checksum: string | null;
  notes: string | null;
  schemaVersion: string;
  source: AppSource;
}
```

## 10. Manifest → AppManifest

```ts
interface AppManifest {
  iso2: string;
  nameAr: string;
  entityId: string;
  coverageRecordIds: string[];
  hierarchy: {
    entityType: string;
    level: number;
    denominator: number | null;
    denominatorId: string | null;
    coverageRecordId: string | null;
    allowedParentTypes: string[];
    localNames: string[];
    authorityName: string;
    scopeStatus: 'closed'|'open';
    snapshotDate: string | null;
    sourceIds: string[];
    license: string | null;
    notes: string | null;
    caveat: string | null;
    temporalStatuses: string[];
    verificationStatus: string;
    specialCases: any[];
  }[];
  caveats: string[];
  countryEntity: AppEntity;
}
```

## 11. خرائط الحالات للواجهة

**Entity Status → UI Badge:**

| status الأصلي | Badge في التطبيق | لون |
|---------------|-----------------|-----|
| current | حالي - موثق | 🟢 |
| historical | تاريخي | 🟠 |
| proposed | مقترح (لم ينفذ) | 🟡 |
| claimed | مدّعى | 🔴 |
| disputed | متنازع عليه | 🔴 |
| de_facto | فعلي (واقعي) | 🟡 |
| destroyed/displaced/abolished/merged/renamed | تاريخي - منتهي | ⚫ |
| uncertain | غير محسوم | ⚪ |

**Claim Status → Badge:**

| verified | 🟢 موثق |
| reported | 🟡 منقول (مصدر واحد) |
| disputed | 🔴 متنازع |
| historical | 🟠 تاريخي |
| uncertain | ⚪ غير مؤكد |
| retracted | ⚫ مسحوب |

إذا ظهرت حالة جديدة في البيانات غير المذكورة → تُعرض كما هي مع لون افتراضي ولا تُحذف.

## 12. ضمان عدم الفقدان

1. سكربت `scripts/build_app_bundle.py` يحفظ كل حقل كما هو، ويضيف فقط حقول مشتقة prefixed بـ `_derived` ولا يستبدل.
2. اختبار `test_app_data_completeness.py`:
   - يقارن عدد السجلات: 5317 entity, 3261 alias, 5706 relationship, 2245 claim, 151 source, 112 denom, 112 coverage, 28 snapshot, 22 manifest
   - لكل entity يتأكد كل field موجود (حتى لو null)
   - Hash للـ canonical_bundle قبل وبعد التحويل
3. TypeScript: `AppEntity` extends `RawEntity` مع `& { raw: RawEntity }` بحيث حتى لو نسيت field في الواجهة، يبقى في `raw` ويُعرض في Research Mode.

## 13. مثال تحويل (السعودية مركز)

Raw Entity:
```json
{"id":"ENT-SA-CENTER-...","canonical_name":"قيس","entity_type":"sa_markaz","status":"current","coordinates":null,...}
```

AppEntity:
```ts
{
  id: "ENT-SA-CENTER-...",
  canonicalName: "قيس",
  entityType: "sa_markaz",
  status: "current",
  coordinates: null,
  hasCoordinates: false,
  raw: { ...original... }
}
```

لا فقدان.
