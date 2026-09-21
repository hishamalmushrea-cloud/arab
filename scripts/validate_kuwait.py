#!/usr/bin/env python3
"""Independent Kuwait production semantics (base layer plus depth cycle 1)."""
import hashlib,json
from model import ROOT,read_jsonl,write_json
G={'ENT-KW-GOVERNORATE-CAPITAL':('العاصمة','Capital',574839),'ENT-KW-GOVERNORATE-HAWALLI':('حولي','Hawalli',926170),'ENT-KW-GOVERNORATE-AL-AHMADI':('الأحمدي','Al-Ahmadi',923784),'ENT-KW-GOVERNORATE-AL-JAHRA':('الجهراء','Al-Jahra',566861),'ENT-KW-GOVERNORATE-AL-FARWANIYA':('الفروانية','Al-Farwaniya',1109819),'ENT-KW-GOVERNORATE-MUBARAK-AL-KABEER':('مبارك الكبير','Mubarak Al-Kabeer',279666)}
S={'SRC-KW-CSB-CENSUS-GOVERNORATES-2021','SRC-KW-CSB-CENSUS-METHODOLOGY-2021','SRC-UNESCO-WHC-KW-2026','SRC-KW-UNESCO-ICH-2026','SRC-KW-DIALECT-MIRROR-2026','SRC-KW-DIALECT-LOANS-2026','SRC-KW-CUISINE-MIRROR-2026','SRC-KW-DRESS-HERITAGE-2026','SRC-KW-KUNA-FIRJAN-2017','SRC-KW-MIRQAB-HERITAGE-2026','SRC-KW-SIGN-LANGUAGE-MIRROR-2026'}
ICH='SRC-KW-UNESCO-ICH-2026'; WEAK={'SRC-KW-DIALECT-MIRROR-2026','SRC-KW-DIALECT-LOANS-2026','SRC-KW-CUISINE-MIRROR-2026','SRC-KW-DRESS-HERITAGE-2026','SRC-KW-MIRQAB-HERITAGE-2026','SRC-KW-SIGN-LANGUAGE-MIRROR-2026','SRC-KW-KUNA-FIRJAN-2017'}
QUARTERS={'شرق','الوسط','جبل','المرقاب'}
SHARED_DISHES={'مجبوس','مرقوق','هريس','جريش','تشريبة','القيمات (لقيمات)'}
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='KW'];ids={r['id'] for r in e}
 return {'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='KW'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='KW'],'snapshots':[r for r in read_jsonl(ROOT/'data/snapshots/snapshots.jsonl') if r.get('id','').startswith('SNP-KW-')],'sources':[load(p) for p in (ROOT/'data/sources').glob('*.json') if load(p).get('id') in S],'manifest':load(ROOT/'manifests/KW.yml')}
def validate(d):
 err=[]
 def E(c,l,m):err.append({'code':c,'location':l,'message':m})
 es={r['id']:r for r in d['entities']};al={r['entity_id']:r for r in d['aliases']};rels=d['relationships'];cl=d['claims'];ss={r['id']:r for r in d['sources']};ds={r['id']:r for r in d['denominators']};cv={r['id']:r for r in d['coverage']}
 places={r['id']:r for r in d['entities'] if r['entity_type'] in {'quarter','lane'}}
 expected_entities={'ENT-KW-COUNTRY',*G,*places}
 if set(es)!=expected_entities:E('KW_ENTITY_UNIVERSE','entities','expected country plus six governorates plus historic places only')
 if len(places)!=17 or sum(1 for r in places.values() if r['entity_type']=='lane')!=1:E('KW_ENTITY_UNIVERSE','entities','expected four quarters, twelve firjan, and one sikka')
 for eid,(ar,en,pop) in G.items():
  r=es.get(eid,{})
  if r.get('entity_type')!='kw_governorate' or r.get('canonical_name')!=ar:E('KW_GOVERNORATE_IDENTITY',eid,'type/name mismatch')
  if al.get(eid,{}).get('name')!=en:E('KW_ALIAS',eid,'English alias mismatch')
  q=[x for x in rels if x.get('child_id')==eid]
  if len(q)!=1 or q[0].get('parent_id')!='ENT-KW-COUNTRY' or q[0].get('relationship_type')!='administrative_parent':E('KW_WRONG_PARENT',eid,'wrong governorate parent')
  q=[x for x in cl if x.get('subject_id')==eid and x.get('predicate')=='population']
  if len(q)!=1 or q[0].get('value',{}).get('data')!=pop or q[0].get('observed_at')!='2021-01-01' or not q[0].get('second_source_id'):E('KW_POPULATION',eid,'reconciled 2021 population mismatch/undated')
 for eid,r in places.items():
  if r.get('status')!='historical' or r.get('verification_status')!='local_reported':E('KW_QUARTER_HISTORICAL',eid,'historic quarter must stay historical and local_reported')
  if r.get('canonical_source_id') not in {'SRC-KW-KUNA-FIRJAN-2017','SRC-KW-MIRQAB-HERITAGE-2026'}:E('KW_QUARTER_SOURCE',eid,'unexpected quarter source')
  if [x for x in rels if x.get('child_id')==eid and x.get('relationship_type')=='administrative_parent']:E('KW_QUARTER_PARENT',eid,'historic place must not carry an administrative parent')
  loc=[x for x in rels if x.get('child_id')==eid and x.get('relationship_type')=='located_in']
  if len(loc)!=1 or es.get(loc[0]['parent_id'],{}).get('id') in {None}:E('KW_QUARTER_LOCATED_IN',eid,'historic place requires exactly one located_in relation')
  if [x for x in cl if x.get('subject_id')==eid and x.get('predicate')=='population']:E('KW_QUARTER_POPULATION',eid,'no population claim may be invented for a historic quarter')
 if sum(1 for r in cl if r['predicate']=='population')!=6:E('KW_COUNTS','KW','expected six population claims')
 for r in cl:
  if r.get('source_id') not in ss or not r.get('source_locator'):E('KW_CLAIM_SOURCE',r.get('id','?'),'unaccepted source/locator')
  if r.get('predicate')=='population':
   if r.get('classification')!='official' or not r.get('published') or r.get('verification_status')!='verified':E('KW_POPULATION','KW','population claim contract')
  elif r.get('source_id')==ICH:
   if r.get('verification_status')!='verified' or not r.get('published') or r.get('classification') not in {'shared','national'}:E('KW_ICH_CONTRACT',r['id'],'UNESCO element must be verified, published, and classified shared/national')
   if r.get('predicate','') in {'food_dish','clothing_item','custom_practice','craft_custom','intangible_cultural_practice'} and not r.get('classification'):E('KW_ICH_CONTRACT',r['id'],'missing classification')
  else:
   if r.get('published'):E('KW_DEPTH_PUBLISHED_FROM_WEAK',r['id'],'weak-source claim may not be published')
   if r.get('verification_status') not in {'probable','local_reported','unverified','folk_narrative'}:E('KW_DEPTH_CONTRACT',r['id'],'weak-source claim exceeds the local_reported cap')
   if not r.get('classification'):E('KW_DEPTH_CONTRACT',r['id'],'depth claim requires explicit classification')
 depth=[r for r in cl if r.get('id','').startswith('CLM-KW-DEPTH')]
 if len(depth)!=38:E('KW_DEPTH_COUNTS','KW',f'expected 38 depth claims, got {len(depth)}')
 if len([r for r in depth if r['predicate']=='language_presence'])!=2 or len([r for r in depth if r['predicate']=='dialect_profile'])!=5:E('KW_DEPTH_COUNTS','KW','language and dialect counts')
 if len([r for r in depth if r['predicate']=='food_dish'])!=17 or len([r for r in depth if r['predicate']=='clothing_item'])!=7:E('KW_DEPTH_COUNTS','KW','dish and dress counts')
 for nm in SHARED_DISHES:
  q=next((r for r in depth if r['predicate']=='food_dish' and r['value']['data'].get('name')==nm),None)
  if not q or q.get('classification')!='shared':E('KW_SHARED_NOT_EXCLUSIVE','KW',f'{nm} must stay shared')
 if not any(r['predicate']=='name_origin_narrative' and r.get('classification')=='historical' for r in depth):E('KW_DEPTH_COUNTS','KW','missing naming narrative')
 if set(ss)!=S or any(x.get('quality_tier') not in {'A','B','E'} for x in ss.values()):E('KW_SOURCES','sources','expected exact eleven KW sources')
 if sum(1 for x in ss.values() if x.get('quality_tier')=='E')!=6 or sum(1 for x in ss.values() if x.get('quality_tier')=='A')!=4 or sum(1 for x in ss.values() if x.get('quality_tier')=='B')!=1:E('KW_SOURCES','sources','tier mix changed')
 if any(x.get('quality_tier')=='E' and (x.get('country_codes')!=['KW']) for x in ss.values()):E('KW_SOURCE_COUNTRY','sources','depth source must be Kuwait-only')
 if {k:v.get('value') for k,v in ds.items()}!={'DEN-KW-COUNTRY-SCOPE':1,'DEN-KW-GOVERNORATES-2021':6,'DEN-KW-WHC-20260816':0}:E('KW_DENOMINATORS','denominators','expected 1/6/0')
 for cid,n in {'COV-KW-COUNTRY-SCOPE':1,'COV-KW-GOVERNORATES-2021':6,'COV-KW-WHC-20260816':0}.items():
  r=cv.get(cid,{})
  if r.get('matched')!=n or r.get('denominator')!=n or not r.get('complete') or r.get('coverage_percentage')!=100.0:E('KW_COVERAGE',cid,'coverage mismatch')
 m=d['manifest'];gl=next((r for r in m.get('hierarchy',[]) if r.get('entity_type')=='kw_governorate'),{})
 if gl.get('scope_status')!='closed' or gl.get('denominator')!=6:E('KW_MANIFEST','KW','governorates not closed')
 for t in ['kw_area','kw_block']:
  l=next((r for r in m.get('hierarchy',[]) if r.get('entity_type')==t),{})
  if l.get('scope_status')!='unavailable' or l.get('denominator') is not None:E('KW_FAKE_LOWER_LAYER',t,'lower denominator invented')
 layers={l['layer']:l for l in m.get('pilot_layers',[])}
 hq=layers.get('historic_city_quarters',{})
 if hq.get('denominator') is not None or hq.get('scope_status') not in {'open','bounded'} or hq.get('coverage_record_id'):E('KW_QUARTER_MANIFEST','KW','historic quarters must carry no denominator and no coverage record')
 if sorted(hq.get('entity_types',[]))!=['lane','quarter']:E('KW_QUARTER_MANIFEST','KW','quarter/lane layer declaration')
 ich=layers.get('unesco_intangible_heritage',{})
 if ich.get('denominator')!=7:E('KW_ICH_CONTRACT','KW','UNESCO ICH layer denominator must be the seven inscribed elements')
 if len(d['snapshots'])!=1 or d['snapshots'][0].get('checksum')!='sha256:'+hashlib.sha256((ROOT/'data/imports/kuwait/snapshot_manifest.json').read_bytes()).hexdigest():E('KW_SNAPSHOT','snapshot','checksum mismatch')
 return err
def main():
 d=data();e=validate(d);m={'entities':len(d['entities']),'new_entities':len(d['entities'])-1,'aliases':len(d['aliases']),'relationships':len(d['relationships']),'claims':len(d['claims']),'sources':len(d['sources']),'denominators':len(d['denominators']),'coverage_records':len(d['coverage']),'ab_claims':sum(r.get('source_id') in S and ss_tier(d,r) in {'A','B'} for r in d['claims']),'depth_claims':sum(r['id'].startswith('CLM-KW-DEPTH') for r in d['claims']),'historic_places':sum(r['entity_type'] in {'quarter','lane'} for r in d['entities'])};write_json(ROOT/'reports/kuwait_validation.json',{'schema_version':'2.0.0','country_code':'KW','snapshot_date':'2026-09-20','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':m,'errors':e});print(json.dumps(m,sort_keys=True));print('Kuwait production semantic validation '+('passed.' if not e else 'failed.'));return 0 if not e else 1
def ss_tier(d,r):
 return next((x.get('quality_tier') for x in d['sources'] if x.get('id')==r.get('source_id')),None)
if __name__=='__main__':raise SystemExit(main())
