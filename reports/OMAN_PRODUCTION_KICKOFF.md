# Oman Production Expansion — Micro Pilot Kickoff

## Status

**STARTED — evidence assessment only; no Oman production records emitted yet.**

## Mode

Micro Pilot. Oman introduces a deeper legal hierarchy and explicit legal timing: 11 governorates, wilayats, and minister-created sub-wilayas/administrative centres.

## Primary evidence found

- Royal Decree 36/2022 Governorates System, Article 2, enumerates 11 governorates and their wilayats; Article 3 distinguishes Royal-Decree creation/amendment/abolition of governorates/wilayas from ministerial decisions for niyabahs and administrative centres.
- Ministry of Economy planning material states 11 governorates and 61 wilayats.
- NCSI GIS coded domains expose bilingual governorate and wilayat codes, but must be reconciled against the legal decree before import.

## Key finding

The reconciliation now supports **11 current governorates** and a **63-wilayat count candidate**: Oman News Agency confirms that Al Jabal Al Akhdar and Sinaw raised the total from 61 to 63. However, the accessible English decree rendering is inconsistent for Dhofar (Sadah omission and ambiguous “Qishn” rendering), while NCSI's exposed coded domain remains at the older 61 identities. Therefore 63/63 record coverage is not yet asserted. See `reports/OMAN_DENOMINATOR_RECONCILIATION.md`.

## Risks

- Mixing governorate municipality branches with wilayat entities.
- Treating niyabah as a universal third level when its creation is ministerial and selective.
- Using pre-2022 counts after legal additions.
- Spelling variants creating duplicate wilayat identities.
- Assigning World Heritage serial components to guessed parents.

## Next action

Persist the complete Royal Decree enumeration and current NCSI coded domain, compute the exact current governorate/wilayat denominator, document every discrepancy, then choose the bounded micro-pilot scope before emitting records.
