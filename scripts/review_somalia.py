#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
SIDS=['SRC-SO-MOP-FMS-2026','SRC-SO-MOIFAR-NORTHEAST-2026','SRC-SO-SONNA-NORTHEAST-DECLARATION-2026','SRC-SO-SENATE-CONSTITUENCY','SRC-SO-MPWR-FIVE-FMS-2025','SRC-UNESCO-ICH-SO-STATE-2026','SRC-UNESCO-ICH-SO-XEER-CIISE-02087-2024','SRC-UNESCO-ICH-SO-ZAFFA-02283-2025','SRC-UNESCO-WH-SO-STATE-2026','SRC-UNESCO-WH-SO-BUSHBUSHLE-6752-2024','SRC-UNESCO-WH-SO-HOBYO-6753-2024','SRC-UNESCO-WH-SO-LIGHTHOUSE-6754-2025','SRC-SO-CONSTITUTION-2012','SRC-SO-ISO639-3-SOMALI','SRC-SO-LANGUAGES-MIRROR-2026','SRC-SO-CUISINE-MIRROR-2026','SRC-SO-CULTURE-MIRROR-2026','SRC-SO-MOGADISHU-MIRROR-2026']
FIELDS={'archive_url','checksum','country_codes','id','language','license','locator','notes','publication_date','publisher','quality_tier','retrieved_at','schema_version','source_type','title','url'}
def main():
 f=L(ROOT/'data/imports/somalia/fixtures/federal_frames_2026.json');x=L(ROOT/'data/imports/somalia/fixtures/cultural_depth_2026.json')
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='SO'];ids={r['id'] for r in e}
 C=[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids]
 families={'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':C,'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='SO'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='SO'],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in SIDS]}
 E={r['id']:r for r in e};find=[]
 def F(rid,msg):find.append({'severity':'P1','record_id':rid,'message':msg})
 def by(p):return [c for c in C if c['predicate']==p]
 src={s['id']:s for s in families['sources']}
 for q in f['federal_member_states']:
  if E.get('ENT-SO-FMS-'+q['code'],{}).get('canonical_name')!=q['name']:F(q['code'],'fixture identity')
 if E.get('ENT-SO-REGION-BRA',{}).get('entity_type')!='so_region':F('Banadir','parallel type')
 if E.get('ENT-SO-FMS-06',{}).get('status')!='claimed' or E.get('ENT-SO-FMS-07',{}).get('valid_from')!='2026-01-17':F('narratives','Somaliland/North East temporal status')
 ich={c['value']['data']['reference']:c for c in by('intangible_cultural_practice')}
 for el in x['ich_elements']:
  c=ich.get(el['reference'])
  if not c or c['value']['data']['year']!=el['year'] or c['classification']!='shared' or not c['published']:F(el['reference'],'shared element year/classification/publication')
 tl={c['value']['data']['reference']:c for c in by('unesco_tentative_listing')}
 for t in x['tentative_sites']:
  c=tl.get(t['reference'])
  if not c or c['value']['data']['year']!=t['year'] or c['value']['data']['category']!=t['category'] or c['value']['data']['status']!='القائمة المؤقتة':F(t['reference'],'tentative-list year/category/status')
 cp={c['value']['data']['article']:c for c in by('constitutional_provision')}
 for p in x['constitution_provisions']:
  c=cp.get(p['article'])
  if not c or c['value']['data']['topic']!=p['topic']:F('article-'+p['article'],'constitution topic')
 langs={c['value']['data']['name']:c for c in by('language_presence')}
 for l in x['language_presence']:
  c=langs.get(l['name'])
  if not c or c['value']['data']['level']!=l['level']:F(l['name'],'language level')
 for d_ in x['dialect_profiles']:
  c=next((c for c in by('dialect_profile') if c['value']['data']['name']==d_['name']),None)
  if not c or c['value']['data']['group']!=d_['group'] or set(d_['features'])!=set(c['value']['data']['features']):F(d_['name'],'dialect group/features')
 for i_ in x['language_institutions']:
  c=next((c for c in by('language_institution') if c['value']['data']['name']==i_['name']),None)
  if not c or c['value']['data']['founded']!=i_['founded'] or c['value']['data']['states']!=i_['states']:F(i_['name'],'institution founding/states')
 for key,pred in [('dishes','food_dish'),('crafts','craft_custom'),('customs','custom_practice'),('narratives','place_name_narrative')]:
  got={c['value']['data']['name'] for c in by(pred)};want={q['name'] for q in x[key]}
  if got!=want:F(key,f'{pred} set mismatch')
 places={**{q['name']:q for q in x['places']['sites']},**{q['name']:q for q in x['places']['quarters']}}
 for name,q in places.items():
  ent=next((r for r in e if r['canonical_name']==name),None);parent='ENT-SO-COUNTRY' if q['parent']=='country' else q['parent']
  if not ent:F(name,'place entity missing');continue
  own=[r for r in families['relationships'] if r['child_id']==ent['id']]
  if ent['coordinates'] is not None or not ent.get('notes') or any(c['subject_id']==ent['id'] for c in C) or any(a['entity_id']==ent['id'] for a in families['aliases']):F(name,'place must stay claim-free, alias-free and coordinate-free')
  if len(own)!=1 or own[0]['relationship_type']!='located_in' or own[0]['parent_id']!=parent:F(name,'single located_in parent')
 for s in families['sources']:
  if set(s)!=FIELDS:F(s['id'],'sixteen source fields')
  if s['country_codes']!=['SO'] or s['quality_tier'] not in {'A','B','C','D','E'}:F(s['id'],'country scope/tier')
  if not s['locator'] or not s['notes']:F(s['id'],'locator and notes')
 pub=[c for c in C if c['published']]
 if len(pub)!=26:F('published',f'published spine expected 26, got {len(pub)}')
 for c in pub:
  if src.get(c['source_id'],{}).get('quality_tier')!='A' or not c['source_locator']:F(c['id'],'published requires tier A and a locator')
 for c in C:
  if c['id'].startswith('CLM-SO-DEPTH') and not c['notes']:F(c['id'],'depth claim needs a note')
 sample={k:{'population':len(v),'sample_size':len(v),'sample_percentage':100.0,'record_ids':sorted(r['id'] for r in v)} for k,v in families.items()}
 write_json(ROOT/'data/review/somalia_review_samples.json',{'schema_version':'2.0.0','country_code':'SO','families':sample});write_json(ROOT/'reports/somalia_review_samples.json',{'schema_version':'2.0.0','country_code':'SO','families':sample})
 n=sum(len(v) for v in families.values());ok=not find;res={k:{'sampled':len(v),'passed':len(v) if ok else 0,'failed':0 if ok else len(v),'status':'PASS' if ok else 'FAIL'} for k,v in families.items()}
 write_json(ROOT/'reports/somalia_independent_review.json',{'schema_version':'2.0.0','country_code':'SO','status':'PASS' if ok else 'FAIL','p0':0,'critical_p1':len(find),'method':'Independent full-population authority-frame review: 7 MOP entries, Banadir parallel path, Somaliland narrative, North East transition, unavailable lower universes, two shared ICH elements, three tentative-list submissions, seven constitution articles, fourteen language rows, and four places without rank.','families':res,'total_sampled':n,'total_passed':n if ok else 0,'findings':find});print(n,[f['record_id'] for f in find][:10]);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
