# Oman Governorate/Wilayat Denominator Reconciliation

## Decision

- Current governorates: **11 — accepted denominator candidate**.
- Current wilayats: **63 — accepted count candidate, record-level enumeration not yet accepted**.
- Niyabahs/administrative centres: **denominator unavailable**.

No authoritative records are emitted by this review.

## Evidence

1. Royal Decree 36/2022, effective 16 June 2022, Article 2 enumerates 11 governorates and their wilayats. Article 3 requires Royal Decree for governorate/wilayat creation and Ministerial Decision for niyabahs and administrative centres.
2. Oman News Agency states that Al Jabal Al Akhdar and Sinaw were accorded wilayat status, raising the national total from 61 to **63**.
3. Current government material identifies Al Jabal Al Akhdar under Ad Dakhiliyah (nine wilayats) and Sinaw under North Ash Sharqiyah (seven wilayats).
4. The accessible NCSI GIS coded domain still exposes the older 61-code universe and therefore cannot be treated as the current denominator without refresh/reconciliation.

## Translation defect found

The accessible English rendering of Decree 36/2022 Article 2 appears incomplete/inconsistent for Dhofar: its prose rendering omits Sadah and renders Muqshin ambiguously as “Qishn”, while the decree's organisational annex and current official materials recognize the ten-wilayat Dhofar structure. The project must not silently normalize this defect.

## Safe migration rule

The production fixture must be assembled from:

- 11 governorate entries from Article 2;
- the 61 pre-addition coded identities only as identity leads;
- explicit addition/confirmation of Al Jabal Al Akhdar and Sinaw from current official evidence;
- record-level reconciliation of Dhofar against the decree annex/current government source;
- checksum-bound Arabic/English forms before IDs are emitted.

Until that reconciliation is complete, the project may close the 11-governorate layer, but it must not claim 63/63 wilayat record coverage or create niyabah entities.
