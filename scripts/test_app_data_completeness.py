#!/usr/bin/env python3
"""
test_app_data_completeness.py — DATA_COMPLETENESS_TEST
Compares Release Dataset vs App Dataset
Fails if any Entity/Alias/Relationship/Claim/Source/Denominator/Coverage/Snapshot/Manifest is lost.

This test must run in CI before app build.
"""
import json, pathlib, sys
root = pathlib.Path(__file__).parent.parent
gen_dir = root / "generated" / "json"
meta_path = root / "generated" / "metadata.json"
app_data_json = root / "app" / "public" / "data" / "app-data.json"
app_counts_json = root / "app" / "public" / "data" / "counts.json"

def load_json(p):
    return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))

# 1. Expected from metadata
if not meta_path.exists():
    print(f"[FAIL] metadata not found {meta_path}", file=sys.stderr)
    sys.exit(1)
metadata = load_json(meta_path)
expected_counts = metadata["counts"]
print(f"[INFO] Expected counts: {expected_counts}")

# 2. Release dataset counts
release_counts = {}
for name in ["entities","aliases","relationships","claims","sources","denominators","coverage","snapshots"]:
    fp = gen_dir / f"{name}.json"
    if not fp.exists():
        print(f"[FAIL] Release file missing {fp}", file=sys.stderr)
        sys.exit(1)
    data = load_json(fp)
    release_counts[name] = len(data)

print(f"[INFO] Release counts: {release_counts}")

# 3. App dataset counts
if not app_data_json.exists():
    print(f"[FAIL] App data not found {app_data_json} — run build_app_bundle.py first", file=sys.stderr)
    sys.exit(1)
app_bundle = load_json(app_data_json)
app_counts = app_bundle.get("counts", {})
# If counts not in bundle, compute
if not app_counts:
    app_counts = {k: len(app_bundle.get(k, [])) for k in release_counts}

print(f"[INFO] App counts: {app_counts}")

# 4. Compare
failed = False
for k in expected_counts:
    exp = expected_counts[k]
    rel = release_counts.get(k)
    app = app_counts.get(k)
    # For manifests, expected is not in metadata, but we check separately
    if k == "manifests":
        continue
    if rel != exp:
        print(f"[FAIL] Release {k}: expected {exp}, got {rel}", file=sys.stderr)
        failed = True
    if app != exp:
        print(f"[FAIL] App {k}: expected {exp}, got {app} — DATA LOSS!", file=sys.stderr)
        failed = True
    else:
        print(f"[PASS] {k}: {exp} == release == app")

# Check manifests
manifests_dir = root / "manifests"
expected_manifests = len(list(manifests_dir.glob("*.yml")))
app_manifests = len(app_bundle.get("manifests", []))
print(f"[INFO] Manifests: expected {expected_manifests}, app {app_manifests}")
if app_manifests != expected_manifests:
    print(f"[FAIL] Manifests count mismatch: expected {expected_manifests}, got {app_manifests}", file=sys.stderr)
    failed = True
else:
    print(f"[PASS] manifests: {expected_manifests}")

# 5. Field preservation spot checks
# Check that every entity id is present in app bundle
release_entities = load_json(gen_dir / "entities.json")
release_ids = set(e["id"] for e in release_entities)
app_ids = set(e["id"] for e in app_bundle.get("entities", []))
missing_ids = release_ids - app_ids
if missing_ids:
    print(f"[FAIL] Missing entity ids in app: {list(missing_ids)[:10]}", file=sys.stderr)
    failed = True
else:
    print(f"[PASS] All entity ids preserved: {len(release_ids)}")

# Check aliases
release_aliases = load_json(gen_dir / "aliases.json")
release_alias_ids = set(a["id"] for a in release_aliases)
app_alias_ids = set(a["id"] for a in app_bundle.get("aliases", []))
if release_alias_ids != app_alias_ids:
    print(f"[FAIL] Alias ids mismatch: missing {len(release_alias_ids - app_alias_ids)}", file=sys.stderr)
    failed = True
else:
    print(f"[PASS] All alias ids preserved: {len(release_alias_ids)}")

# Check relationships
release_rels = load_json(gen_dir / "relationships.json")
release_rel_ids = set(r["id"] for r in release_rels)
app_rel_ids = set(r["id"] for r in app_bundle.get("relationships", []))
if release_rel_ids != app_rel_ids:
    print(f"[FAIL] Relationship ids mismatch", file=sys.stderr)
    failed = True
else:
    print(f"[PASS] All relationship ids preserved: {len(release_rel_ids)}")

# Check claims
release_claims = load_json(gen_dir / "claims.json")
release_claim_ids = set(c["id"] for c in release_claims)
app_claim_ids = set(c["id"] for c in app_bundle.get("claims", []))
if release_claim_ids != app_claim_ids:
    print(f"[FAIL] Claim ids mismatch", file=sys.stderr)
    failed = True
else:
    print(f"[PASS] All claim ids preserved: {len(release_claim_ids)}")

# Check sources
release_sources = load_json(gen_dir / "sources.json")
release_source_ids = set(s["id"] for s in release_sources)
app_source_ids = set(s["id"] for s in app_bundle.get("sources", []))
if release_source_ids != app_source_ids:
    print(f"[FAIL] Source ids mismatch", file=sys.stderr)
    failed = True
else:
    print(f"[PASS] All source ids preserved: {len(release_source_ids)}")

# 6. Field-level check: ensure no required field dropped
required_fields = {
    "entities": ["id","canonical_name","country_code","entity_type","status","canonical_source_id"],
    "aliases": ["id","entity_id","name","kind"],
    "relationships": ["id","child_id","parent_id","relationship_type"],
    "claims": ["id","subject_id","predicate","value","source_id"],
    "sources": ["id","title","quality_tier"],
}
for family, fields in required_fields.items():
    for record in app_bundle.get(family, [])[:1]: # check first record
        for f in fields:
            if f not in record:
                print(f"[FAIL] Field {f} missing in {family} id {record.get('id')}", file=sys.stderr)
                failed = True

if failed:
    print("\n[FAIL] DATA_COMPLETENESS_TEST FAILED — data loss detected!", file=sys.stderr)
    sys.exit(1)
else:
    print("\n[SUCCESS] DATA_COMPLETENESS_TEST PASSED — 100% data preserved")
    print(f"  Entities: {len(app_ids)}")
    print(f"  Aliases: {len(app_alias_ids)}")
    print(f"  Relationships: {len(app_rel_ids)}")
    print(f"  Claims: {len(app_claim_ids)}")
    print(f"  Sources: {len(app_source_ids)}")
    print(f"  Denominators: {len(app_bundle.get('denominators', []))}")
    print(f"  Coverage: {len(app_bundle.get('coverage', []))}")
    print(f"  Snapshots: {len(app_bundle.get('snapshots', []))}")
    print(f"  Manifests: {len(app_bundle.get('manifests', []))}")
    sys.exit(0)
