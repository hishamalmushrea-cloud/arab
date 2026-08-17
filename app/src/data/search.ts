import Fuse from 'fuse.js';
import { normalizeArabic } from '@/lib/arabicNormalize';
import { db } from './db';

export interface SearchDoc {
  id: string;
  canonicalName: string;
  normalizedName: string;
  entityType: string;
  countryCode: string;
  status: string;
  aliases: string[];
  normalizedAliases: string[];
  typeLabelAr: string;
}

let fuseInstance: Fuse<SearchDoc> | null = null;

export async function buildSearchIndex(): Promise<Fuse<SearchDoc>> {
  if (fuseInstance) return fuseInstance;

  const entities = await db.entities.toArray();
  const aliases = await db.aliases.toArray();

  const aliasMap = new Map<string, string[]>();
  for (const a of aliases) {
    if (!aliasMap.has(a.entityId)) aliasMap.set(a.entityId, []);
    aliasMap.get(a.entityId)!.push(a.name);
  }

  const docs: SearchDoc[] = entities.map(e => {
    const als = aliasMap.get(e.id) || [];
    return {
      id: e.id,
      canonicalName: e.canonicalName,
      normalizedName: normalizeArabic(e.canonicalName),
      entityType: e.raw.entity_type,
      countryCode: e.countryCode,
      status: e.status,
      aliases: als,
      normalizedAliases: als.map(normalizeArabic),
      typeLabelAr: getTypeLabelAr(e.raw.entity_type)
    };
  });

  fuseInstance = new Fuse(docs, {
    keys: [
      { name: 'canonicalName', weight: 2 },
      { name: 'normalizedName', weight: 2 },
      { name: 'aliases', weight: 1.5 },
      { name: 'normalizedAliases', weight: 1.5 },
      { name: 'id', weight: 0.5 }
    ],
    threshold: 0.3,
    ignoreLocation: true,
    includeScore: true,
    minMatchCharLength: 2,
  });

  return fuseInstance;
}

export async function searchEntities(query: string, filters?: { countryCode?: string; entityType?: string; status?: string }) {
  const fuse = await buildSearchIndex();
  if (!query.trim()) {
    // بدون بحث، أرجع الكل مع فلترة
    let all = await db.entities.toArray();
    if (filters?.countryCode) all = all.filter(e => e.countryCode === filters.countryCode);
    if (filters?.entityType) all = all.filter(e => e.raw.entity_type === filters.entityType);
    if (filters?.status) all = all.filter(e => e.status === filters.status);
    return all.slice(0, 100).map(e => ({ item: { id: e.id, canonicalName: e.canonicalName } as any, score: 0 }));
  }
  const results = fuse.search(query);
  let filtered = results;
  if (filters?.countryCode) filtered = filtered.filter(r => r.item.countryCode === filters.countryCode);
  if (filters?.entityType) filtered = filtered.filter(r => r.item.entityType === filters.entityType);
  if (filters?.status) filtered = filtered.filter(r => r.item.status === filters.status);
  return filtered.slice(0, 100);
}

function getTypeLabelAr(type: string): string {
  const map: Record<string, string> = {
    'country': 'دولة',
    'sa_region': 'منطقة (سعودية)',
    'sa_governorate': 'محافظة (سعودية)',
    'sa_markaz': 'مركز (سعودية)',
    'tn_governorate': 'ولاية (تونس)',
    'tn_delegation': 'معتمدية',
    'tn_municipality': 'بلدية (تونس)',
    'tn_imada': 'عمادة',
    'jo_governorate': 'محافظة (أردن)',
    'jo_liwa': 'لواء',
    'jo_qada': 'قضاء',
    'ae_emirate': 'إمارة',
    'bh_governorate': 'محافظة (بحرين)',
    'kw_governorate': 'محافظة (كويت)',
    'dz_wilaya': 'ولاية (جزائر)',
    'ma_region': 'جهة',
    'ma_province': 'إقليم',
    'om_governorate': 'محافظة (عُمان)',
    'om_wilaya': 'ولاية (عُمان)',
    'eg_governorate': 'محافظة (مصر)',
    'lb_governorate': 'محافظة (لبنان)',
    'lb_district': 'قضاء',
    'ly_municipality': 'بلدية (ليبيا)',
    'ly_shabiya_historical': 'شعبية تاريخية',
    'city': 'مدينة',
    'village': 'قرية',
    'town': 'بلدة',
  };
  return map[type] || type;
}

export function clearSearchCache() {
  fuseInstance = null;
}
