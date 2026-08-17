# Yemen Production Expansion Closeout

## Decision
**PASS.** Yemen Full Pilot stage one accepted on exact release commit `24531638822f9d9da5f2d5f5e8f2b7307b46c894`; the legal/statistical first-level layer is closed.
## Scope
21 current governorates plus the parallel Amanat Al Asimah capital municipality: 22 first-level identities.
## Snapshot
`SNP-YE-PRODUCTION-20260817`.
## Evidence reconciliation
The official CSO/NIC legacy frame enumerates 20 governorates plus Capital Municipality. Law 31/2013, reported issued on 2013-12-18, establishes Socotra Archipelago Governorate. The current 22-unit universe is therefore the legacy 21 plus Socotra, without silently rewriting the historical frame.
## Entities
23 Yemen entities total: country, 21 governorates, and one capital municipality.
## Relationships
22 current country-parent relationships. No conflict-control parentage is inferred.
## Claims
23 source-backed Claims: one administrative profile per unit and one Socotra establishment-instrument Claim.
## Sources
3 atomic sources: official CSO definition, official NIC legacy enumeration, and contemporaneous Law 31/2013 report.
## Denominators and coverage
- current first level: 22/22
- current governorates: 21/21
- capital municipality: 1/1
- historical pre-Socotra first level: 21/21
- districts and uzlas: denominator unavailable; no records emitted
## Socotra temporal boundary
Law 31/2013 and its issuance/establishment date of 2013-12-18 are recorded. The complete official-gazette text and exact effective-clause wording were not retrievable; `effective_clause_verified=false`, and no wording was invented.
## Independent review
PASS locally: full population 82/82.
## Negative tests
PASS locally: 9/9, including Amanat-as-governorate, silent Socotra omission, legal-as-de-facto, unsupported destruction, premature lower levels, wrong parent, stale coverage, and fabricated effective-clause mutations.
## P0/P1
0/0.
## make check
PASS: Phase 5 88/88 plus fifteen production gates 21/21; full `make check` = 403 checks.
## GitHub CI
PASS on exact release commit: Push Action `31977549949` and PR Action `31977551453`.
## Limitations
No current district/uzla coded register accepted; no effective-control, disputed, destroyed, or displaced overlay; no broad cultural/dialect import; official-gazette full text remains unavailable.
## Transferability
Schema 2.0.0 transfers without change. Parallel first-level types and legal/de-facto separation are preserved.
## Recommended next country
Syria — Full Pilot, beginning with the 14 legal governorates and separately dated status overlays.

## Depth-expansion cycle 1 — district layer (2026-08-17)

First cycle executed under the **Maximum Arabic Knowledge Coverage** policy (`00_فلسفة_الموسوعة.md`).

- **333/333 district identities** entered across all 22 first-level units, matching the archived official CSO 333-district national frame.
- Identities are attested from the NIC district-catalogue encyclopedic mirror (tier C) anchored to the archived CSO administrative-definitions page (tier B, Internet Archive capture 2018-09-30).
- Every district carries `verification_status: probable` — **not** verified — pending reconciliation with an atomic official coded register; the semantic gate rejects promotion to verified (`YE_DISTRICT_STATUS`) and any unattested addition (`YE_COUNTS`).
- `DEN-YE-DISTRICTS` = 333 (official frame); `COV-YE-DISTRICTS` = 333 matched. Uzlas remain denominator-unavailable with zero fabricated records.
- 12/12 negative mutations detected, including new district-frame mutations; independent review covers the full 752-record population.
- No conflict, control, damage, or displacement inference; the legal/statistical frame stays separate from war overlays.

## Depth-expansion cycle 2 — Amanat lane layer (2026-08-17)

Second cycle under **Maximum Arabic Knowledge Coverage**: the lane (حارة) layer enters as **places**, not administrative tiers.

- **Official frame:** NIC Amanat classification — 10 districts, 89 hays, **791 lanes** (census 2004). `DEN-YE-AMANAT-LANES` = 791.
- **104 attested lane identities** (13.15% of the frame, `complete=false`, 687 documented missing — never fabricated):
  - **Old Sanaa: 69 lanes** at `probable` (heritage-cited inventory; UNESCO World Heritage 1986, danger list 2015).
  - **Tahrir: 35 lanes** across 3 hays — التحرير (20) and بير العزب (8) at `probable` with 2004 census homes/households/population tables; **القاع (7) at `unverified`** (names-only by subtraction; historical قاع اليهود whose community emigrated).
- **33 lane population claims** (2004 census, `observed_at: 2004-12-16`) — `status: reported`, **unpublished**, never projected to the present.
- **3 naming-origin narratives** (ياسر/غمدان/غرقة القليس) at `local_reported`, classification `historical`, unpublished — first use of the narrative-not-fact contract.
- Orthographic near-duplicates (بير/بئر البهمة in one hay) are distinct census rows; identity keys carry the inventory sequence to avoid false merging.
- Gate: 17/17 mutations (5 new: fabricated lane, lane promoted to verified, lane population published, narrative promoted to fact, coverage forced complete); independent review **1,004/1,004**.

## Depth-expansion cycle 3 — cultural local knowledge (2026-08-17)

Third cycle: dishes, dialect profiles, and language presence enter as **classified claims**, never as published facts.

- **12 dish claims** (`food_dish`, tier-E mirror source, `local_reported`, unpublished): السلتة (national, أصلها صنعاني), الفحسة (local صنعاء), **المندي (shared — حضرمي الأصل انتشر للجزيرة؛ البوابة ترفض جعله حصريًا)**, المدفون, بنت الصحن, العصيدة, اللحوح (تهامة), الصيادية (الساحل), المطبق (عدن — أثر الميناء), الذمول والحلويات الحضرمية, المظبي.
- **5 dialect profiles** (`dialect_profile`, `local_reported`, unpublished): الصنعانية والتعزية-العدنية والحضرمية واليافعية والتهامية — بخصائص النطق وعينات المفردات بمعانيها (حينهو، معادبش، حيابك، بايقع لك، رحك/نمك/أكلك، لمه...). upgrade path: مدونة لهجية ميدانية بتواريخ دراسة عبر `lexical_context`.
- **2 language-presence claims** (`probable`): السقطرية (سقطرى) والمهرية (المهرة) — لغتان ساميتان جنوبيتان حيتان.
- Every claim is anchored to its place entity (governorate/country), carries explicit classification (national/regional/local/shared), and stays unpublished pending stronger sourcing.
- Gate: **21/21 mutations** (4 new: dish published from weak source, المندي claimed exclusive, dialect promoted to verified, language claim dropped); independent review **1,023/1,023**.
