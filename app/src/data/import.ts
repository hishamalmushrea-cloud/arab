import { db } from './db';

export interface ImportResult {
  entities: number;
  aliases: number;
  relationships: number;
  claims: number;
  sources: number;
  denominators: number;
  coverage: number;
  snapshots: number;
  manifests: number;
}

export async function importBundle(bundle: any): Promise<ImportResult> {
  // clear old
  await db.entities.clear();
  await db.aliases.clear();
  await db.relationships.clear();
  await db.claims.clear();
  await db.sources.clear();
  await db.denominators.clear();
  await db.coverage.clear();
  await db.snapshots.clear();
  await db.manifests.clear();

  // Entities
  const entities = (bundle.entities || []).map((raw: any) => ({
    id: raw.id,
    countryCode: raw.country_code,
    entityType: raw.entity_type,
    status: raw.status,
    canonicalName: raw.canonical_name,
    raw,
  }));

  // Aliases
  const aliases = (bundle.aliases || []).map((raw: any) => ({
    id: raw.id,
    entityId: raw.entity_id,
    name: raw.name,
    kind: raw.kind,
    language: raw.language || null,
    raw,
  }));

  const relationships = (bundle.relationships || []).map((raw: any) => ({
    id: raw.id,
    childId: raw.child_id,
    parentId: raw.parent_id,
    relationshipType: raw.relationship_type,
    raw,
  }));

  const claims = (bundle.claims || []).map((raw: any) => ({
    id: raw.id,
    subjectId: raw.subject_id,
    predicate: raw.predicate,
    status: raw.status,
    raw,
  }));

  const sources = (bundle.sources || []).map((raw: any) => ({
    id: raw.id,
    qualityTier: raw.quality_tier,
    sourceType: raw.source_type,
    raw,
  }));

  const denominators = (bundle.denominators || []).map((raw: any) => ({
    id: raw.id,
    countryCode: raw.country_code,
    layer: raw.layer,
    raw,
  }));

  const coverage = (bundle.coverage || []).map((raw: any) => ({
    id: raw.id,
    countryCode: raw.country_code,
    layer: raw.layer,
    raw,
  }));

  const snapshots = (bundle.snapshots || []).map((raw: any) => ({
    id: raw.id,
    sourceId: raw.source_id,
    raw,
  }));

  const manifests = (bundle.manifests || []).map((raw: any) => ({
    iso2: raw.country?.iso2 || raw.iso2 || raw._filename?.replace('.yml','') || 'XX',
    _filename: raw._filename || '',
    raw,
  }));

  // bulkPut
  await db.entities.bulkPut(entities);
  await db.aliases.bulkPut(aliases);
  await db.relationships.bulkPut(relationships);
  await db.claims.bulkPut(claims);
  await db.sources.bulkPut(sources);
  await db.denominators.bulkPut(denominators);
  await db.coverage.bulkPut(coverage);
  await db.snapshots.bulkPut(snapshots);
  await db.manifests.bulkPut(manifests);

  return {
    entities: entities.length,
    aliases: aliases.length,
    relationships: relationships.length,
    claims: claims.length,
    sources: sources.length,
    denominators: denominators.length,
    coverage: coverage.length,
    snapshots: snapshots.length,
    manifests: manifests.length,
  };
}

export async function loadBundleFromPublic(): Promise<any> {
  const res = await fetch('/data/app-data.json');
  if (!res.ok) throw new Error(`Failed to load app-data.json: ${res.status}`);
  const bundle = await res.json();
  return bundle;
}

export async function isDBPopulated(): Promise<boolean> {
  const count = await db.entities.count();
  return count > 0;
}
