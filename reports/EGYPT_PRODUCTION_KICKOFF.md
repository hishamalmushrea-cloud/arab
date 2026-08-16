# Egypt Production Expansion — Full Pilot Kickoff

## Status
**STARTED — research only; no authoritative Egypt production records emitted.**

## Mode
Full Pilot because 27 governorates branch into different rural and urban paths: markaz/local unit/village versus qism/shiyakha.

## Initial evidence
- Ministry of Local Development confirms all 27 governorates.
- CAPMAS official survey/census metadata enumerates the same 27 and distinguishes four wholly urban governorates from the remaining governorates with urban and rural populations.
- CAPMAS coding must be used to prevent city/governorate and markaz/qism conflation.

## Required topology profiles
1. Urban governorates: governorate → qism → shiyakha where officially enumerated.
2. Mixed/rural governorates: governorate → markaz → local unit/village, with urban qism paths kept separate.
3. Frontier governorates: no assumption that sparse settlement or city names form complete lower denominators.

## Next action
Checksum the 27-governorate CAPMAS universe, establish exact Arabic/English codes, then select one urban and one mixed governorate as the full-pilot topology pair before any national lower-level expansion.
