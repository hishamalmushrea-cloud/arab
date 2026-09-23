# Djibouti Production Expansion Closeout

## Decision
**PASS.** Djibouti Production Micro Pilot accepted on exact commit `daee882315df72f7dfa89e8b580e0c27c54e56a3`.
## Scope
Five decentralized regions, special-status Djibouti City, three city communes, thirteen regional sub-prefectures.
## Snapshot
`SNP-DJ-PRODUCTION-20260816`; RGPH-3 population reference 2024-05-20.
## Manifest
Special-city and regional paths are separate and closed.
## Denominators
Country 1; regions 5; special city 1; city communes 3; sub-prefectures 13.
## Entities
23 total; 22 new.
## Aliases
0; exact French official forms used canonically, with no invented Arabic forms.
## Relationships
22 exact topology-specific parents.
## Claims
6 provisional RGPH-3 population Claims reconciling to 1,066,809.
## Sources
5 A-tier Presidency, law, INSTAD, decentralisation, and Interior sources.
## Coverage
5/5 regions; 1/1 special city; 3/3 city communes; 13/13 sub-prefectures.
## Cultural coverage
Zero inscribed World Heritage properties documented; ten tentative sites not promoted.
## Dialect coverage
0 Claims.
## Independent review
PASS locally: 66/66.
## Negative tests
PASS locally: 8/8 special-city/region, commune/sub-prefecture, population, and denominator mutations.
## P0/P1
0/0.
## make check
PASS: Phase 5 88/88 plus five production gates 21/21; full `make check` = 193 checks.
## GitHub CI
PASS: Push Action `31968106953` and PR Action `31968109485`.
## Remaining limitations
No arrondissement/zone denominator; broad culture/dialect unclosed; RGPH results provisional.
## Lessons learned
Special-capital topology must be parallel, not forced into regional hierarchy.
## Transferability
Schema 2.0.0 supports parallel administrative profiles without change.
## Recommended next country
Morocco Micro Pilot: region then parallel prefecture/province semantics.

## Depth cycle 1 (2026-09-21)

The accepted topology is untouched (5 regions · special-city Djibouti-Ville · 3 communes · 13 sub-prefectures, each with its RGPH-3 population), and the depth cycle adds **40 claims and 12 places** on top of it: 46 claims, 35 entities, 34 relationships, 19 sources (7 A · 1 B · 6 E, plus the five accepted official sources).

**Published spine (10 claims, all verified, all on A sources).** Three inscribed UNESCO elements — **Xeedho 02001 (2023, Urgent Safeguarding List; Djibouti is the only submitting State, so it is the one element that may carry `national`)**, **Xeer Ciise 02087 (2024, Representative List, Ethiopia–Djibouti–Somalia, `shared`)** and **the zaffa 02283 (2025, Representative List, seven submitting States, `shared`)** — plus the 30 August 2007 ratification, the 2026 nomination of the Afar Madqa recorded as a **pending nomination** (published as a stated nomination, never as an inscription), and articles 1–2 of the 1992 (rev. 2010) Constitution: official languages Arabic and French, state religion, and the capital.

**Classified body (30 unpublished claims).** 8 language presences (Arabic and French published from article 1; Somali `som` and Afar `aar` stay unpublished with the ISO 639-3 registry as a second source; Djiboutian Arabic, Omani Arabic, one immigrant group and a sign language with **no ISO code claimed at all** because the registry entry could not be verified), 1 dialect profile (Northern Somali), 1 script profile (Latin, the Somali alphabet, Qafar Feera and the Arabic-script transcription) and 1 language institution (Regional Somali Language Academy, Djibouti City, 2013, three States). Then 12 dishes (لاهوه · الفه فاه · ييتاكلت الرطب · الحلاوة الطحينية · السمبوسة · تيبس الإبل · حليب آري · أودكاش · الباري · الباستو · الشاه الجيبوتي · البونا), 3 dress items (الديري وموعد سوقه الخميس · الغوغارة · عطور الفوح والجااوي والمسقطي), 2 crafts (حياكة السلال · الشرشارات), and 3 customs, one of which is the declared **folk narrative** (برد الأسنان بالمبرد الحديدي) and one of which is the wedding-ritual account that the 1999 press report and the UNESCO Xeedho description both touch.

**No numbers.** No speaker count or share is recorded anywhere; the mirror's figures are explicitly left out, and the validator, the negative suite and the independent review all reject any count or share field.

**Places — no denominator.** 12 places inside Djibouti City (10 `quarter`: الحي الأوروبي · الحي الأفريقي · الهضبة الوسطى · بلبلة · أمبولي · بولاوس · المرابو · الهيرون · إنجيلا · عريبة; and 2 `market`: السوق المركزي (الكيسات) · ساحة محمود حربي) carry **one `located_in` relation to the city only**: no administrative parent, no population, no percentage, no claim, and no inference into the three communes.

**A stated discrepancy.** The English mirror gives Djibouti City 35 sub-prefectures while the accepted decentralisation roadmap counts 13 sub-prefectures nationally; the difference is recorded as an unpublished note on the city, the accepted value stays 13, and a mutation fails if the mirror value is allowed to replace it.

**Verification.** Independent full review **144/144** (35 entities, 34 relationships, 46 claims, 19 sources, 5 denominators, 5 coverage), required mutations **43/43**, `validate.py` clean at 2,740 claims, and the Djibouti gate at 21 checks including a clean worktree.
