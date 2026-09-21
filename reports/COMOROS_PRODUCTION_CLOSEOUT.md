# Comoros Production Expansion Closeout

## Decision
**PASS.** Comoros Production Full Pilot accepted on exact commit `3681548a0a694f3e9a53e4569b06a0d14aa4d6de`.
## Scope
Three Union-administered autonomous islands, 16 prefectures, 54 communes, one 2026 World Heritage serial property; Mayotte excluded from current administration.
## Snapshot
`SNP-KM-PRODUCTION-20260817`.
## Manifest
Current Union-administered hierarchy closed; claimed territory not represented as current.
## Denominators
Country 1; islands 3; prefectures 16; communes 54; World Heritage 1.
## Entities
75 total; 74 new.
## Aliases
0; exact legal/census forms canonical.
## Relationships
74 exact administrative/contextual links.
## Claims
Three island child-count Claims and three World Heritage Claims: 6.
## Sources
3 A-tier Justice/INSEED/UNESCO sources.
## Coverage
3/3 islands; 16/16 prefectures; 54/54 communes; 1/1 World Heritage property.
## Cultural coverage
2026 serial property documented; older zero-property State Party metadata superseded.
## Dialect coverage
0 Claims.
## Independent review
PASS locally: 168/168.
## Negative tests
PASS locally 8/8 Mayotte/topology/count/UNESCO-time mutations.
## P0/P1
0/0.
## make check
PASS: Phase 5 88/88 plus eleven production gates 21/21; full `make check` = 319 checks.
## GitHub CI
PASS: Push Action `31973993057` and PR Action `31973995114`.
## Remaining limitations
Village components not imported; claimed-territory scope not modeled; broad culture/dialect deferred.
## Lessons learned
Administrative control, constitutional claim, and archipelago geography require separate scopes; external registry updates require temporal freshness.
## Transferability
Schema 2.0.0 transfers without change.
## Recommended next country
Palestine Full Pilot with legal/statistical governorates and separate de facto/disputed/destroyed/displaced evidence.

---

# Depth cycle 1 — Maximum Arabic Knowledge Coverage (2026-09-20)

The accepted 3/16/54 Union hierarchy above is unchanged. This additive cycle opens Comoros under `00_فلسفة_الموسوعة.md` with a checksum-bound fixture and no rewrite of any accepted layer.

## New checksum-bound input

`data/imports/comoros/fixtures/cultural_depth_2026.json` (18,766 bytes, sha256 `b4c174d2…f7b4`) added as the second record in `data/imports/comoros/snapshot_manifest.json`; `SNP-KM-PRODUCTION-20260817` binds the manifest bytes.

## Published spine — one shared UNESCO element and three constitutional provisions

**زفّة العرس التقليدي (The zaffa in the traditional wedding), element 02283, inscribed 2025 (20.COM) on the Representative List** — a **seven-State file** (Djibouti · Comoros · UAE · Iraq · Jordan · Mauritania · Somalia), so the claim is `verified`, `published` and `shared`: no exclusivity is claimed for Comoros. The value carries the registered description (bridal procession, cleansing and henna, symbolic acts such as milk, an egg or a relative's cape, music, shouts, sweets and flowers, intergenerational transmission).

Three **constitutional provisions** entered from the 2018 Constitution as published by the Constitute Project: Article 9 (official languages are Shikomor, French and Arabic), Article 6 (territorial composition) and Article 10 (Moroni is the capital, its status fixed by law). The Article 6 claim records the constitutional position **and states in the same record that Mayotte is outside the current Union administration accepted in this repository**, so the claim can never be read as an administrative fact.

## Property facts

Criteria `(iii)(iv)`, property area **30.47 ha** and buffer zone **131.68 ha** are published on the existing property entity `ENT-KM-CULTURAL-SITE-HISTORIC-SULTANATES-MEDINAS`. The six serial components are recorded as an unpublished list (see below) because the description page read in this cycle names six historic towns without enumerating them.

## Classified local knowledge (unpublished)

30 further depth claims, none published: 3 official-language and 2 minority-language presence claims (Malagasy and Swahili stay `local_reported` with no speaker counts), 5 dialect profiles (shiNgazidja · shiNdzuani · shiMwali · shiMaore with their eastern/western grouping, plus a shared numerals-and-phrases profile carrying the 1–10 numeral table and six glossed phrases), 10 dishes (مكاترا فوترا · لانغوست بالفانيليا · مشاكي · تسولولا · روتي يا هوما بامبا · أمبريفادس بالكاري · أرز جزر القمر · كاري دجاج قمري · روجيل · القهوة العربية مع مكاترا فطرة), 3 dress items (الشيروماني · السارونج · الجبة والشال), 1 craft/economy claim (الزراعات العطرية: الفانيليا والقرنفل وجوز الهند وزيت اليلنغ يلانغ), 2 customs (الزواج الكبير/زواج العادة · مجلس الذكر), and 1 unpublished component-names list.

**No speaker count or share is recorded anywhere:** the validator and the independent review both reject any speaker figure for Comorian, and the minority languages stay unpublished.

## Heritage medinas — no denominator

Six places entered as `quarter` with `located_in` to the island only: مدينة موروني التاريخية، نتسودجيني، إتساندرا، إيكوني (القمر الكبرى) وموتسامودو ودوموني (أنجوان). No administrative parent, no claim attached, no population, no percentage — the accepted 54-commune set does not contain every historic toponym, so no lower-layer parent is inferred.

## Coverage and denominators

Unchanged closed layers: 3 islands, 16 prefectures, 54 communes and one World Heritage property, all 100%. The intangible-heritage layer declares **1/1 element** as its own denominator with no coverage record, and the medina and classified-knowledge layers declare no denominator at all.

## Independent review and negative tests

Independent full review: **229/229** records (81 entities, 80 relationships, 40 claims, 18 sources, 5 denominators, 5 coverage). Required mutations: **36/36**, adding guards for UNESCO unpublishing, de-sharing the seven-State element, wrong year, submitting-States tamper, losing a constitutional article, silencing the Mayotte note, unpublishing an official language, publishing a minority language, losing the ISO code set, inserting a speaker share, medina-as-current, medina administrative parent, wrong island, medina as city, claims attached to a medina, medina source upgrade, publishing weak depth, promoting a dialect, unglossed dialect entries, property-area tamper, publishing component names, source-tier inflation, claiming exclusivity in a classification, and layer-denominator inflation, plus the two second-source pairing guards added after the general validator caught six depth claims that carried a second source without its locator.

## Remaining limitations

No dated heritage-place denominator; no independent confirmation of the six component names from the property page itself; no lexical corpus with third-party provenance beyond a learner set; and Mayotte's own administration is deliberately outside the current scope while remaining inside the constitutional claim.

## Post-commit repair (2026-09-21)

After the depth cycle was committed, `scripts/validate.py` surfaced six unpublished depth claims (three dishes, one dress item, two customs) that carried `second_source_id` without a `second_source_locator`. The fixture was completed with a real locator for every second source (19,533 bytes, sha256 `f6f54f3d…f572d`; the manifest record and the eighteen depth-source checksums follow the fixture bytes), and the importer now passes `second_loc` through the dish, dress and custom loops instead of dropping it.

The gap was closed at the KM layer as well: `validate_comoros.py` gained the `KM_SECOND_SOURCE_PAIR` invariant (a second source never stands without its own locator, and a locator never stands alone) and the negative suite gained two mutations covering both directions — **36/36**. The published spine is untouched: still 16 published claims, all on A/B sources, and every depth claim keeps its classification and its non-publication.
