# United Arab Emirates Depth Cycle 1 — Closeout

## Decision

**PASS.** The first UAE depth cycle is imported, validated, mutation-tested and independently reviewed without touching the accepted pilot layer. It adds the UNESCO intangible-heritage record, the World Heritage record, language and dialect rows, and classified local knowledge, and it keeps every unread field explicitly empty. No fifth country is started.

## Anchor

Depth annex to `reports/UAE_PILOT_FINAL.md`. Source-layer commit `0a97099` (recon and evidence retrieval, 2026-09-23); this closeout is released by the commit that adds the depth cycle below it. `make uae` must pass on a clean tree.

## Snapshots

- `SNP-AE-PILOT-20260815` (2026-08-15) stays bound to exactly four fixtures: administrative profile, cultural claims, source catalog, and the evidence manifest. The depth cycle does not rewrite its checksum.
- `SNP-AE-DEPTH-20260923` (2026-09-23) binds the depth fixture `data/imports/uae/fixtures/cultural_depth_2026.json` together with the 25-record evidence manifest. Date separation is deliberate: a retrieval date is not a legal commencement date and a September reading never silently re-dates an August layer.

## Sources added (19 → 25, evidence extracts 19 → 25)

| Source | Tier | Use |
| --- | --- | --- |
| `SRC-UNESCO-ICH-AE-STATE-2026` | A | ICH state page: ratifications, inscribed total, register entry, pending nominations |
| `SRC-UNESCO-ICH-AE-AL-AZI-01268-2017` | A | Al Azi element page: sole-submitter USL file 01268 |
| `SRC-UNESCO-WH-AE-STATE-2026` | A | World Heritage state page: accession, inscribed properties, tentative list, assistance |
| `SRC-AE-ISO639-3-ARABIC` | A | ISO 639-3 registration: `ara` macrolanguage and `afb` Gulf Arabic |
| `SRC-AE-CUISINE-MIRROR-2026` | E | Classification only: dish rows, unpublished |
| `SRC-AE-CULTURE-MIRROR-2026` | E | Classification only: language, dialect, craft, custom and narrative rows, unpublished |

Every extract is checksum-bound in `data/imports/uae/snapshot_manifest.json` and materialized by `scripts/build_uae_sources.py`; catalog IDs and manifest IDs must match or the build fails.

## Intangible cultural heritage (21 inscriptions on the state page)

Seven element files are classified in this cycle. **One** is a sole-submitter national element: **العزي `01268`** on the Urgent Safeguarding List (2017, 12.COM), a group poetry recital with no rhythm or instruments whose bearers are the poet, the performers, the chorus and the audience, and whose decline after the mid-twentieth century is recorded in the source. The other **six** are shared files: التغرودة `00744` (2012), العيالة `01012` (2014), الخط العربي `01718` (2021), النخلة `01902` (2022), الحناء `02116` (2024) and الزفّة `02283` (2025). A shared file is never promoted to `national`, and each keeps its own per-country source ID.

**Thirteen** further inscribed files are recorded with reference, year and list but **without any scope label** — المجلس `01076`, الرزفة `01078`, سباق الهجن `01576`, الأفلاج `01577`, الصقارة `01708`, التلي `01712`, الهدهدة `01717`, الهريس `01744`, القهوة العربية `02111`, السدو `02223`, البشت `02233`, الكحل `02261`, الأحلّة `02279`. Their submitting-State lists were not read in this cycle, so classifying them would be a guess. They are carried as unpublished `unesco_element_deferred_file` claims with the reason recorded, and a negative test fails the build if such a file is given a national or shared label.

The Article 18 register entry **`02473`** (Safeguarding programme for Al Sadu, 2025) stays a safeguarding programme, never an element. The four announced **2026** nominations (آلة العود · السعافيات · الهريس · الحناء) stay announced and are never recorded as inscriptions. Ratification of the 2003 Convention: **2005-05-02**; periodic reports were submitted on time (2011/2017/2022) with the next due 2028-12-15; the UAE served on the Committee 2006–2010 and 2024–2028.

## World Heritage

Accession **2001-05-11**. Three inscribed properties: **المواقع الثقافية في العين `1343`** (2011, cultural), **فايا `1735`** (2025, cultural) and **وادي وُرَيّة `1724`** (2026, natural). Approved international-assistance requests: **0** — a published zero, recorded as zero. Fifteen tentative-list files are recorded by reference and year (5660–5665 · 5941 · 6352 · 6464/6465 · 6641/6642/6643/6664 · 7039/7041) and are never styled as inscribed. Criteria and the emirate of each property were not read in this cycle, so both stay empty; a negative test fails the build if criteria are filled in from a mirror.

## Places

The three inscribed properties enter as places with **one `located_in` relationship to the country only**: no administrative parent is inferred, no coordinates are invented, no population claim is attached, and no alias is created. Wadi Wurayah keeps its natural-site type and is never described with cultural predicates.

## Languages, dialect and local knowledge (all unpublished or constitution-deferred)

- **Arabic** is recorded as the official language with ISO 639-3 `ara` as a second source; **English** as widely spoken; expatriate languages (Farsi, Hindi, Urdu, Bengali, Mandarin) as classified rows without any count. All three rows stay unpublished because the constitutional article was not read in this cycle — `constituteproject.org` returned 404 twice, and an unread page produces no claim.
- The Emirati dialect is tied to ISO 639-3 **`afb`** (Gulf Arabic); no "Emirati Arabic" ISO code exists.
- Twelve dishes (الهريس · المجبوس · المقلوبة · فريسة · فريد · جشيد · مشوي · رقاق · خمير · جباب · بلاليط · لقيمات), three crafts and symbols (الدلّة · السدو · التلي), three customs (بن/بنت naming, women keeping family names, coffee hospitality) and two published narratives (Trucial States naming; Sharjah as cultural capital 1998/2014) are classified at tier E and **unpublished**.
- **No speaker, population or share number appears anywhere in the cycle**; the guard is the repository-wide `count_leak` (percent sign, count words adjacent to digits, count keys), not a digit-only filter, so legitimate years stay legal while numbers of people do not.

## Claims, denominators and coverage

- Claims: 146 total (76 accepted pilot + **70 depth**), of which **109 published** (all tier A/B, 100.0%) and 37 declared weak and unpublished.
- Denominators and coverage: 17 each. The five depth layers carry **unavailable** denominator/coverage pairs with an explicit reason and **no percentage**: the documented totals (21 ICH inscriptions, 3 inscribed properties, 15 tentative files) are recorded as page facts, not as enumerable universes.
- The three layer registries that were unavailable stay unavailable: `DEN-AE-DUBAI-PLANNING-COMMUNITIES`, `DEN-AE-POPULATED-PLACES`, `DEN-AE-NEIGHBORHOODS` — all null, no percentage, no inferred entity.

## Quality evidence

| Check | Result |
| --- | --- |
| `python3 scripts/validate.py` | PASS (global, zero errors) |
| `python3 scripts/validate_uae.py` | PASS; P0 = 0, critical P1 = 0 |
| `python3 scripts/test_uae_negative.py` | **28/28** required mutations detected (8 pilot + 20 depth) |
| `python3 scripts/review_uae.py` | **45/45** independent samples passed across 10 families, each ≥ 10% |
| `python3 scripts/generate_uae_report.py --check` | current, exactly 23 sections |
| `make uae` | 21 checks on a clean tree |

## Evidence upgrade and the trace guard

The first pass of this cycle wrote six extracts that carried element titles, years and lists but **not** the numeric UNESCO references, while the depth claims asserted references such as `01268`, `5660` and `1343`. Every value came from the state pages that were read in the cycle, and the committed recon file `data/imports/uae/research/depth_research_2026-09-23.json` recorded them with their page URLs — but the checksum-bound extracts did not. Both state pages were therefore re-read on 2026-09-23 and transcribed again with the references as the pages publish them in their links (`.../al-ahalla-a-living-performing-art-in-the-united-arab-emirates-02279`, `whc.unesco.org/en/tentativelists/5660/`), and the extracts, the evidence manifest and the source catalog were re-checksummed together.

A new guard, `UAE_DEPTH_EVIDENCE_TRACE`, now resolves each published depth claim's `source_id` to its checksum-bound extract and fails the build if that claim's reference is absent from the extract text. It caught exactly one remaining case on its first run — the Al Azi element page extract, which quoted the element's 2017 inscription without its code — and that extract was completed as well. A matching negative mutation rewrites an element reference to an unbacked value and must fail, which is how the trace rule stays enforced rather than promised.

Every depth error code has its own mutation: shared-as-national, invented scope for a deferred file, publishing a deferred file, register-as-element, dropped pending nomination, dropped depth claim, filled criteria, duplicated tentative reference, duplicate inscription count, injected dish number, published weak source, place coordinates, second parent, place-bearing claim, re-typed natural site, merged pilot snapshot, downgraded source tier, removed layer denominator and shifted documented total.

## What remains open (next depth cycle for the same country)

1. Read the thirteen deferred element pages and record each file's submitting-State list, then classify honestly as shared or national.
2. Read the three property pages (criteria, emirate) and the 15 tentative files' pages; keep tentative separate from inscribed.
3. Find a working constitutional text for the UAE and publish the language, religion and union articles — or leave language rows unpublished.
4. Extend depth to settlements and neighborhoods only if a dated enumerable registry is found; otherwise the three unavailable denominators stay null.
