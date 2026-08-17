import Dexie, { Table } from 'dexie';

export interface DBEntity {
  id: string;
  countryCode: string;
  entityType: string;
  status: string;
  canonicalName: string;
  raw: any;
}

export interface DBAlias {
  id: string;
  entityId: string;
  name: string;
  kind: string;
  language: string | null;
  raw: any;
}

export interface DBRelationship {
  id: string;
  childId: string;
  parentId: string;
  relationshipType: string;
  raw: any;
}

export interface DBClaim {
  id: string;
  subjectId: string;
  predicate: string;
  status: string;
  raw: any;
}

export interface DBSource {
  id: string;
  qualityTier: string;
  sourceType: string;
  raw: any;
}

export interface DBCoverage {
  id: string;
  countryCode: string;
  layer: string;
  raw: any;
}

export class ArabDB extends Dexie {
  entities!: Table<DBEntity>;
  aliases!: Table<DBAlias>;
  relationships!: Table<DBRelationship>;
  claims!: Table<DBClaim>;
  sources!: Table<DBSource>;
  denominators!: Table<any>;
  coverage!: Table<DBCoverage>;
  snapshots!: Table<any>;
  manifests!: Table<any>;

  constructor() {
    super('ArabEncyclopediaDB');
    this.version(1).stores({
      entities: 'id, countryCode, entityType, status, canonicalName, *raw.canonical_name',
      aliases: 'id, entityId, name, kind, language',
      relationships: 'id, childId, parentId, relationshipType',
      claims: 'id, subjectId, predicate, status',
      sources: 'id, qualityTier, sourceType',
      denominators: 'id, countryCode, layer',
      coverage: 'id, countryCode, layer',
      snapshots: 'id, sourceId',
      manifests: 'iso2, _filename'
    });
  }
}

export const db = new ArabDB();
