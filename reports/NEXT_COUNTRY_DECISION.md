# Next Country Decision

## Policy baseline

As of 2026-08-17 the project operates under **Maximum Arabic Knowledge Coverage** (`00_فلسفة_الموسوعة.md`, Schema 2.1.0). All 22 bounded first-layer country cycles remain accepted; the project is now in **depth-expansion mode**: proving places exist down to villages, neighborhoods, and lanes, then collecting the maximum useful local information (history, dialect, food, dress, crafts, markets, stories) with explicit confidence statuses instead of deletion.

## Current country

**Yemen (YE) — depth-expansion cycle 1.**

## Rationale (dependency / risk / available information)

- Yemen has the largest documented first-to-second-level gap in the project: 22/22 first-level units accepted but only a fraction of the 333 districts (مديريات) recorded.
- Rich available material already inside the repository: 535 legacy CSV rows, صنعاء القديمة lane inventory (104 documented lanes with classified sources for the remaining ~687), and extensive Markdown city files.
- High availability of local sources (official CSO frame, heritage books, local press) fits the new tier-E policy.
- Listed first in the user priority set: Yemen, Saudi Arabia, Egypt, Morocco, Algeria, Iraq, Palestine, Oman, Sudan.

## Scope of the Yemen depth cycle

1. ✅ **District (مديرية) layer — DONE (2026-08-17):** 333/333 attested district identities entered across all 22 first-level units at `probable` status, anchored to the archived official CSO 333-district frame; `DEN-YE-DISTRICTS`/`COV-YE-DISTRICTS` closed at the frame; gate mutations forbid unattested additions and premature promotion to verified.
2. صنعاء lanes: continue from the documented 104; new lanes enter at `local_reported`/`unverified` when only weak sources attest them — never invented.
3. Local knowledge claims per place: naming origin (folk narratives as ⚪ `folk_narrative`), dialect words, food, dress, crafts, markets — classified national/regional/local/shared.
4. Previously dropped unverified Yemen material is staged in `data/backlog/unverified_content/` and re-evaluated in this cycle.
5. Upgrade path: reconcile an atomic official coded district register to promote identities from `probable` to `verified`.

## Queue after Yemen

Saudi Arabia → Egypt → Morocco → Algeria → Iraq → Palestine → Oman → Sudan, then the remaining countries by available-information density. Order may only change on documented dependency/risk grounds.

## Release status

The bounded first-layer release decision in `reports/FINAL_ARABIC_ENCYCLOPEDIA_RELEASE.md` (`COMPLETE WITH DOCUMENTED LIMITATIONS`) is unchanged; depth expansion is additive and never rewrites accepted layers.
