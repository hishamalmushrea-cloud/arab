# DATA_INVENTORY — جرد البيانات الكامل للتطبيق

> **المبدأ:** لا تُفقد معلومة. كل ملف في Release Dataset يجب أن يصل إلى التطبيق، ولو في قسم متقدم.
> **Source of Truth:** `data/` (Schema 2.0.0) → `generated/` هو Release Dataset الذي يستهلكه التطبيق مباشرة.

## 1. الملخص العددي (من generated/metadata.json 2026-08-17)

| النوع | الملف المصدر | Schema المطبق | العدد | حجم JSON المولد | طريقة التحميل للتطبيق | طريقة العرض |
|-------|--------------|---------------|-------|----------------|-----------------------|-------------|
| Entities | `data/entities/entities.jsonl` | `schema/entity.schema.json` | 5317 | 3.7 MB | `generated/json/entities.json` → IndexedDB / SQLite table `entities` + index على `id`, `country_code`, `entity_type`, `status` | صفحة المكان: الهوية، الوالد، الأبناء، الإحداثيات، الحالة، الفترة الزمنية |
| Aliases | `data/aliases/aliases.jsonl` | `schema/alias.schema.json` | 3261 | 1.4 MB | `aliases.json` → table `aliases` indexed `entity_id`, `name` (FTS) | صفحة المكان تبويب الأسماء البديلة + محرك البحث |
| Relationships | `data/relationships/relationships.jsonl` | `schema/relationship.schema.json` | 5706 | 2.9 MB | `relationships.json` → table `relationships` indexed `child_id`, `parent_id`, `relationship_type` | صفحة المكان: شجرة الوالد/الأبناء، مستكشف العلاقات، boundary_intersects |
| Claims | `data/claims/claims.jsonl` | `schema/claim.schema.json` | 2245 | 1.8 MB | `claims.json` → table `claims` indexed `subject_id`, `predicate`, `status` | صفحة المكان: جميع Claims (classified official/popular/shared... )، مع source locator |
| Sources | `data/sources/*.json` (151 ملف ذري) | `schema/source.schema.json` | 151 | 139 KB | `sources.json` → table `sources` indexed `id`, `quality_tier` | صفحة المصدر: العنوان، الناشر، النوع، التاريخ، الرابط، locator, license, checksum |
| Snapshots | `data/snapshots/snapshots.jsonl` | `schema/snapshot.schema.json` | 28 | 17 KB | `snapshots.json` → table `snapshots` indexed `id`, `source_id` | صفحة Country → قسم Snapshot + تفاصيل الالتقاط |
| Denominators | `data/coverage/denominators.jsonl` | `schema/denominator.schema.json` | 112 | 76 KB | `denominators.json` → table `denominators` | صفحة Country → التغطية: المقام، التعريف، المصدر، الحالة official/conflicted/unavailable/provisional |
| Coverage | `data/coverage/coverage.jsonl` | `schema/coverage.schema.json` | 112 | 81 KB | `coverage.json` → table `coverage` | صفحة Country → جدول matched/unmatched/excluded/missing + coverage_percentage |
| Manifests | `manifests/{ISO2}.yml` (JSON-compatible) | `schema/manifest.schema.json` | 22 | ضمن generated | تحميل مباشر `manifests/*.yml` → table `manifests` | صفحة الدولة: caveats، hierarchy allowed_parent_types، coverage_record_ids |
| Canonical Bundle | ناتج `generate.py` | مجمع كل الأنواع | 8 عائلات | 11 MB | **المصدر الرئيسي للـ App Import** → `canonical_bundle.json` يحوي جميع العائلات بنسخة موحدة | يستخدم لـ Data Completeness Test |

## 2. الحقول التي يجب ألا تُفقد (Field-level Inventory)

### Entity fields (16 حقلاً من entities.jsonl sample)
- `id` (ENT-...), `canonical_name`, `canonical_name_language`, `canonical_source_id`, `source_locator`, `country_code`, `entity_type` (103 نوع مسموح، 61 فعال), `status` [current, historical, destroyed, displaced, disputed, de_facto, claimed, proposed, transitional, uncertain, renamed, merged, abolished] — العدد الحالي: current 5278, historical 27, proposed 11, claimed 1
- `valid_from`, `valid_to`, `coordinates` {lat, lon nullable} — 2746 لديها إحداثيات، البقية null (لا نخترع)
- `confidence` [high/medium/low], `verification_status` [verified/source_verified/partial/ambiguous/rejected...], `legacy_ids` [], `notes`, `schema_version`

### Alias fields
- `id`, `entity_id`, `name`, `language`, `script` [Arab/Latn...], `kind` [alternative/english/transliteration/local/historical/former/abbreviation/official_variant], `status`, `valid_from`, `valid_to`, `source_id`, `source_locator`, `schema_version`

### Relationship fields
- `id`, `child_id`, `parent_id`, `relationship_type` [administrative_parent, located_in, capital_of, seat_of, historic_successor, claimed_by, boundary_intersects, associated_with, variety_of, form_of, attested_in], `status`, `valid_from`, `valid_to`, `confidence`, `verification_status`, `source_id`, `source_locator`, `notes`, `schema_version`

### Claim fields (أكثر تعقيداً)
- `id`, `subject_id`, `predicate`, `value` {type: string/integer/number/boolean/date/json, data: ...}, `classification` [official/popular/shared/regional/historical/disputed/national/emirate_specific/local], `status` [verified/reported/disputed/historical/uncertain/retracted] — الحالي verified 2230, historical 7, reported 7, disputed 1
- `confidence`, `verification_status`, `sensitivity` [ordinary], `published` bool, `observed_at`, `valid_from`, `valid_to`, `source_id`, `source_locator`, `second_source_id` nullable, `second_source_locator`, `unit`, `lexical_context` {form, meaning, place_id, language, dialect, variety, register, study_date, speaker_or_study, ipa} nullable, `notes`, `schema_version`

### Source fields
- `id`, `title`, `publisher`, `author` nullable, `organization` nullable, `url`, `archive_url` nullable, `publication_date` nullable, `retrieved_at`, `language`, `country_codes` [], `license`, `quality_tier` [A/B/C/D], `source_type` [official_dataset, official_register, law, census, official_report, standard, academic, archive, project_audit], `checksum` nullable, `locator`, `notes`, `schema_version`

### Denominator fields
- `id`, `country_code`, `layer`, `definition`, `denominator` int, `as_of`, `snapshot_date`, `source_id`, `source_locator`, `status` [official/conflicted/unavailable/provisional], `license`, `missing_reason` nullable, `notes`, `value`, `schema_version`

### Coverage fields
- `id`, `country_code`, `layer`, `denominator_id`, `denominator` int nullable, `matched`, `unmatched`, `excluded`, `exclusion_reasons` [], `missing` nullable, `missing_reason` nullable, `coverage_percentage` float nullable, `complete` bool, `snapshot_id`, `snapshot_date`, `source_id`, `license`, `notes`, `schema_version`

### Snapshot fields
- `id`, `title`, `captured_at`, `source_id`, `scope`, `method`, `checksum` nullable, `notes`, `schema_version`

### Manifest fields (SA example)
- `country` {entity_id, iso2, name_ar}, `coverage_record_ids` [], `hierarchy` [] كل عنصر: `entity_type`, `level`, `denominator`, `denominator_id`, `coverage_record_id`, `allowed_parent_types`, `local_names`, `authority_name`, `scope_status` [closed/open], `snapshot_date`, `source_ids`, `license`, `notes`, `caveat`, `temporal_statuses`, `verification_status`, `special_cases`, `caveats` []

### Statuses & Temporal
- entity_statuses: 13 قيمة (vocabularies.json)
- claim_statuses: 6 قيم
- verification_statuses: 5 قيم
- confidence_levels: 3
- denominator_statuses: 4
- valid_from/valid_to: ISO date nullable
- snapshot_date / captured_at / observed_at

### Generated outputs
- `generated/json/canonical_bundle.json` (يضم كل شيء) — سيكون المدخل للـ App Import Pipeline
- `generated/csv/*.csv` — للباحثين، سيعرض رابط تحميل في Research Mode
- `generated/html/*` — مرجع قديم، لا يستخدم كمصدر

## 3. طريقة التحميل إلى التطبيق (Import Strategy)

1. **Source:** يبقى `data/` هو Source of Truth، لكن التطبيق لا يقرأه مباشرة في الـ Runtime.
2. **Build-time:** `make generate` → ينتج `generated/json/*.json`
3. **App Bundle Builder:** سكربت `scripts/build_app_bundle.py` (سننشئه في APP-0)
   - يقرأ `canonical_bundle.json`
   - يتحقق من counts مقابل metadata.json
   - يضغط بـ Brotli (من 21 MB → ~3.5 MB)
   - ينتج `app/public/data/app-data.json.br` + `app/public/data/manifests.json`
   - ينتج `app/src/data/schema.ts` من `vocabularies.json` لضمان التوافق
4. **Runtime:** 
   - Web/PWA: Service Worker يحمل الـ bundle عند أول زيارة → فك ضغط → تخزين في IndexedDB عبر Dexie
   - Android (لاحقاً): نفس الـ JSON → Room SQLite via `scripts/import_to_sqlite.py`

## 4. طريقة العرض (بدون فقدان)

- كل field يظهر، حتى لو في قسم "البيانات الخام" collapsible
- إذا field = null → يعرض "غير متوفر" مع سبب من missing_reason إن وجد، لا يحذف
- العلاقات: لا نخفي boundary_intersects، نعرضها كـ "تقاطع حدودي (ليس والد إداري)"
- Claims: حتى disputed/uncertain تظهر مع 🟠 وسبب
- Sources: license و quality_tier و locator إلزامية في العرض

## 5. القيود المعلنة التي يجب عرضها

- `denominator.status = unavailable/provisional/conflicted` → يعرض كـ "المقام غير متاح" مع notes
- `coverage.missing_reason = denominator_unavailable` → لا نحسب نسبة، نعرض السبب
- `manifest.caveats` → تظهر في صفحة الدولة كـ "تنبيهات منهجية"
- الإحداثيات الغائبة: لا نعرض خريطة وهمية، نعرض "لا توجد إحداثيات موثقة لهذا الكيان في هذه اللقطة"

## 6. الاختبار الآلي للاكتمال

سكربت `scripts/test_app_data_completeness.py` سيقارن:
- generated/metadata.json counts vs app bundle counts
- كل id في data/ يجب أن يكون في app database
- كل field في schema يجب أن يكون محفوظ (حتى لو null)

أي فقدان = FAIL يمنع build.
