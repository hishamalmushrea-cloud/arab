// أنواع التطبيق — مطابقة 100% لـ DATA_CONTRACT.md
// كل حقل من Release Dataset محفوظ

export type EntityStatus = 'current' | 'historical' | 'destroyed' | 'displaced' | 'disputed' | 'de_facto' | 'claimed' | 'proposed' | 'transitional' | 'uncertain' | 'renamed' | 'merged' | 'abolished' | string;
export type ClaimStatus = 'verified' | 'reported' | 'disputed' | 'historical' | 'uncertain' | 'retracted' | string;
export type VerificationStatus = 'verified' | 'source_verified' | 'partial' | 'ambiguous' | 'rejected' | string;
export type Confidence = 'high' | 'medium' | 'low' | string;
export type AliasKind = 'alternative' | 'english' | 'transliteration' | 'local' | 'historical' | 'former' | 'abbreviation' | 'official_variant' | string;
export type RelationshipType = 'administrative_parent' | 'located_in' | 'capital_of' | 'seat_of' | 'historic_successor' | 'claimed_by' | 'boundary_intersects' | 'associated_with' | 'variety_of' | 'form_of' | 'attested_in' | string;
export type ClaimClassification = 'official' | 'popular' | 'shared' | 'regional' | 'historical' | 'disputed' | 'national' | 'emirate_specific' | 'local' | string;
export type DenominatorStatus = 'official' | 'conflicted' | 'unavailable' | 'provisional' | string;
export type SourceQualityTier = 'A' | 'B' | 'C' | 'D' | string;
export type SourceType = 'official_dataset' | 'official_register' | 'law' | 'census' | 'official_report' | 'standard' | 'academic' | 'archive' | 'project_audit' | string;

export interface RawEntity {
  canonical_name: string;
  canonical_name_language: string;
  canonical_source_id: string;
  confidence: Confidence;
  coordinates: { lat: number; lon: number } | null | { latitude: number; longitude: number } | any;
  country_code: string;
  entity_type: string;
  id: string;
  legacy_ids: string[];
  notes: string | null;
  schema_version: string;
  source_locator: string;
  status: EntityStatus;
  valid_from: string | null;
  valid_to: string | null;
  verification_status: VerificationStatus;
  [key: string]: any;
}

export interface AppEntity {
  id: string;
  canonicalName: string;
  canonicalNameLanguage: string;
  canonicalSourceId: string;
  sourceLocator: string;
  countryCode: string;
  entityType: string;
  status: EntityStatus;
  validFrom: string | null;
  validTo: string | null;
  coordinates: { lat: number; lon: number } | null;
  confidence: Confidence;
  verificationStatus: VerificationStatus;
  legacyIds: string[];
  notes: string | null;
  schemaVersion: string;
  raw: RawEntity;
  // derived
  aliases?: AppAlias[];
  children?: AppEntity[];
  parent?: AppEntity | null;
  allRelationships?: AppRelationship[];
  claims?: AppClaim[];
}

export interface AppAlias {
  id: string;
  entityId: string;
  name: string;
  language: string | null;
  script: string | null;
  kind: AliasKind;
  status: EntityStatus;
  validFrom: string | null;
  validTo: string | null;
  sourceId: string;
  sourceLocator: string;
  schemaVersion: string;
  raw: any;
}

export interface AppRelationship {
  id: string;
  childId: string;
  parentId: string;
  relationshipType: RelationshipType;
  status: EntityStatus;
  validFrom: string | null;
  validTo: string | null;
  confidence: Confidence;
  verificationStatus: VerificationStatus;
  sourceId: string;
  sourceLocator: string;
  notes: string | null;
  schemaVersion: string;
  raw: any;
}

export interface AppClaim {
  id: string;
  subjectId: string;
  predicate: string;
  value: { type: string; data: any };
  classification: ClaimClassification;
  status: ClaimStatus;
  confidence: Confidence;
  verificationStatus: VerificationStatus;
  sensitivity: string;
  published: boolean;
  observedAt: string | null;
  validFrom: string | null;
  validTo: string | null;
  sourceId: string;
  sourceLocator: string;
  secondSourceId: string | null;
  secondSourceLocator: string | null;
  unit: string | null;
  lexicalContext: {
    form: string | null;
    meaning: string | null;
    placeId: string | null;
    language: string | null;
    dialect: string | null;
    variety: string | null;
    register: string | null;
    studyDate: string | null;
    speakerOrStudy: string | null;
    ipa: string | null;
  } | null;
  notes: string | null;
  schemaVersion: string;
  raw: any;
}

export interface AppSource {
  id: string;
  title: string;
  publisher?: string | null;
  author?: string | null;
  organization?: string | null;
  countryCodes: string[];
  url: string | null;
  archiveUrl: string | null;
  publicationDate: string | null;
  retrievedAt: string | null;
  language: string | null;
  license: string | null;
  qualityTier: SourceQualityTier;
  sourceType: SourceType;
  checksum: string | null;
  locator: string | null;
  notes: string | null;
  schemaVersion: string;
  raw: any;
}

export interface AppDenominator {
  id: string;
  countryCode: string;
  layer: string;
  definition: string;
  denominator: number;
  asOf: string | null;
  snapshotDate: string | null;
  sourceId: string;
  sourceLocator: string;
  status: DenominatorStatus;
  license: string | null;
  missingReason: string | null;
  notes: string | null;
  value: number;
  schemaVersion: string;
  raw: any;
}

export interface AppCoverage {
  id: string;
  countryCode: string;
  layer: string;
  denominatorId: string;
  denominator: number | null;
  matched: number;
  unmatched: number;
  excluded: number;
  exclusionReasons: string[];
  missing: number | null;
  missingReason: string | null;
  coveragePercentage: number | null;
  complete: boolean;
  snapshotId: string;
  snapshotDate: string | null;
  sourceId: string;
  license: string | null;
  notes: string | null;
  schemaVersion: string;
  raw: any;
}

export interface AppSnapshot {
  id: string;
  title: string;
  capturedAt: string;
  sourceId: string;
  scope: string;
  method: string;
  checksum: string | null;
  notes: string | null;
  schemaVersion: string;
  raw: any;
}

export interface AppManifest {
  iso2?: string;
  nameAr?: string;
  country?: { entity_id: string; iso2: string; name_ar: string };
  coverageRecordIds?: string[];
  hierarchy?: any[];
  caveats?: string[];
  _filename?: string;
  raw: any;
}

export interface AppBundle {
  schema_version: string;
  counts: Record<string, number>;
  entities: RawEntity[];
  aliases: any[];
  relationships: any[];
  claims: any[];
  sources: any[];
  denominators: any[];
  coverage: any[];
  snapshots: any[];
  manifests: any[];
}

// تحويل raw → App
export function toAppEntity(raw: RawEntity): AppEntity {
  let coords: { lat: number; lon: number } | null = null;
  if (raw.coordinates) {
    if (typeof raw.coordinates === 'object') {
      const c: any = raw.coordinates;
      if ('lat' in c && 'lon' in c) coords = { lat: c.lat, lon: c.lon };
      else if ('latitude' in c && 'longitude' in c) coords = { lat: c.latitude, lon: c.longitude };
      else if (Array.isArray(c) && c.length === 2) coords = { lat: c[0], lon: c[1] };
    }
  }
  return {
    id: raw.id,
    canonicalName: raw.canonical_name,
    canonicalNameLanguage: raw.canonical_name_language,
    canonicalSourceId: raw.canonical_source_id,
    sourceLocator: raw.source_locator,
    countryCode: raw.country_code,
    entityType: raw.entity_type,
    status: raw.status,
    validFrom: raw.valid_from || null,
    validTo: raw.valid_to || null,
    coordinates: coords,
    confidence: raw.confidence,
    verificationStatus: raw.verification_status,
    legacyIds: raw.legacy_ids || [],
    notes: raw.notes || null,
    schemaVersion: raw.schema_version,
    raw,
  };
}

export function toAppAlias(raw: any): AppAlias {
  return {
    id: raw.id,
    entityId: raw.entity_id,
    name: raw.name,
    language: raw.language || null,
    script: raw.script || null,
    kind: raw.kind,
    status: raw.status,
    validFrom: raw.valid_from || null,
    validTo: raw.valid_to || null,
    sourceId: raw.source_id,
    sourceLocator: raw.source_locator,
    schemaVersion: raw.schema_version,
    raw,
  };
}

export function toAppRelationship(raw: any): AppRelationship {
  return {
    id: raw.id,
    childId: raw.child_id,
    parentId: raw.parent_id,
    relationshipType: raw.relationship_type,
    status: raw.status,
    validFrom: raw.valid_from || null,
    validTo: raw.valid_to || null,
    confidence: raw.confidence,
    verificationStatus: raw.verification_status,
    sourceId: raw.source_id,
    sourceLocator: raw.source_locator,
    notes: raw.notes || null,
    schemaVersion: raw.schema_version,
    raw,
  };
}

export function toAppClaim(raw: any): AppClaim {
  return {
    id: raw.id,
    subjectId: raw.subject_id,
    predicate: raw.predicate,
    value: raw.value,
    classification: raw.classification,
    status: raw.status,
    confidence: raw.confidence,
    verificationStatus: raw.verification_status,
    sensitivity: raw.sensitivity,
    published: raw.published,
    observedAt: raw.observed_at || null,
    validFrom: raw.valid_from || null,
    validTo: raw.valid_to || null,
    sourceId: raw.source_id,
    sourceLocator: raw.source_locator,
    secondSourceId: raw.second_source_id || null,
    secondSourceLocator: raw.second_source_locator || null,
    unit: raw.unit || null,
    lexicalContext: raw.lexical_context || null,
    notes: raw.notes || null,
    schemaVersion: raw.schema_version,
    raw,
  };
}

export function toAppSource(raw: any): AppSource {
  return {
    id: raw.id,
    title: raw.title,
    publisher: raw.publisher || null,
    author: raw.author || null,
    organization: raw.organization || null,
    countryCodes: raw.country_codes || [],
    url: raw.url || null,
    archiveUrl: raw.archive_url || null,
    publicationDate: raw.publication_date || null,
    retrievedAt: raw.retrieved_at || null,
    language: raw.language || null,
    license: raw.license || null,
    qualityTier: raw.quality_tier,
    sourceType: raw.source_type,
    checksum: raw.checksum || null,
    locator: raw.locator || null,
    notes: raw.notes || null,
    schemaVersion: raw.schema_version,
    raw,
  };
}

export function toAppDenominator(raw: any): AppDenominator {
  return {
    id: raw.id,
    countryCode: raw.country_code,
    layer: raw.layer,
    definition: raw.definition,
    denominator: raw.denominator,
    asOf: raw.as_of || null,
    snapshotDate: raw.snapshot_date || null,
    sourceId: raw.source_id,
    sourceLocator: raw.source_locator,
    status: raw.status,
    license: raw.license || null,
    missingReason: raw.missing_reason || null,
    notes: raw.notes || null,
    value: raw.value,
    schemaVersion: raw.schema_version,
    raw,
  };
}

export function toAppCoverage(raw: any): AppCoverage {
  return {
    id: raw.id,
    countryCode: raw.country_code,
    layer: raw.layer,
    denominatorId: raw.denominator_id,
    denominator: raw.denominator ?? null,
    matched: raw.matched,
    unmatched: raw.unmatched,
    excluded: raw.excluded,
    exclusionReasons: raw.exclusion_reasons || [],
    missing: raw.missing ?? null,
    missingReason: raw.missing_reason || null,
    coveragePercentage: raw.coverage_percentage ?? null,
    complete: raw.complete,
    snapshotId: raw.snapshot_id,
    snapshotDate: raw.snapshot_date || null,
    sourceId: raw.source_id,
    license: raw.license || null,
    notes: raw.notes || null,
    schemaVersion: raw.schema_version,
    raw,
  };
}

export function toAppSnapshot(raw: any): AppSnapshot {
  return {
    id: raw.id,
    title: raw.title,
    capturedAt: raw.captured_at,
    sourceId: raw.source_id,
    scope: raw.scope,
    method: raw.method,
    checksum: raw.checksum || null,
    notes: raw.notes || null,
    schemaVersion: raw.schema_version,
    raw,
  };
}
