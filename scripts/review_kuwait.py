#!/usr/bin/env python3
"""Independent full Kuwait review; does not import importer or semantic validator."""
import hashlib,json
from model import ROOT,read_jsonl,write_json
ICH='SRC-KW-UNESCO-ICH-2026'; SHARED_DISHES={'مجبوس','مرقوق','هريس','جريش','تشريبة','القيمات (لقيمات)'}
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
 s=load(ROOT/'data/review/kuwait_review_samples.json');f=load(ROOT/'data/imports/kuwait/fixtures/census_governorates_2021.json');m=load(ROOT/'data/imports/kuwait/snapshot_manifest.json');depth=load(ROOT/'data/imports/kuwait/fixtures/cultural_depth_2026.json');find=[]
 def bad(fam,r,msg):find.append({'severity':'P1','family':fam,'record_id':r,'message':msg})
 for x in m['records']:
  p=ROOT/x['path'];b=p.read_bytes()
  if len(b)!=x['bytes'] or hashlib.sha256(b).hexdigest()!=x['sha256']:bad('sources',x['path'],'checksum mismatch')
 es=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='KW'];ids={r['id'] for r in es};A=[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids];R=[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids];C=[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids];D=[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='KW'];V=[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='KW'];sourceids=set(s['families']['sources']['record_ids']);S=[load(p) for p in (ROOT/'data/sources').glob('*.json') if load(p).get('id') in sourceids];families={'entities':es,'aliases':A,'relationships':R,'claims':C,'sources':S,'denominators':D,'coverage':V}
 tiers={x['id']:x.get('quality_tier') for x in S}
 expected={r['name_ar']:(r['name_en'],r['population']) for r in f['records']};actual={r['canonical_name']:r for r in es if r['entity_type']=='kw_governorate'}
 if set(expected)!=set(actual):bad('entities','KW-governorates','six-name set mismatch')
 for ar,(en,pop) in expected.items():
  eid=actual.get(ar,{}).get('id')
  if not eid:continue
  if not any(x['entity_id']==eid and x['name']==en for x in A):bad('aliases',eid,'English alias mismatch')
  if not any(x['child_id']==eid and x['parent_id']=='ENT-KW-COUNTRY' for x in R):bad('relationships',eid,'country parent missing')
  if not any(x['subject_id']==eid and x['predicate']=='population' and x['value']['data']==pop and x['second_source_id'] for x in C):bad('claims',eid,'population/reconciliation mismatch')
 if sum(r['population'] for r in f['records'])+f['not_stated_population']!=f['total_population']:bad('claims','KW-total','table does not reconcile')
 # Depth contract verified independently of the importer and the semantic validator.
 places=[x for x in es if x['entity_type'] in {'quarter','lane'}]
 if len(places)!=len(depth['quarters']['city_quarters'])+len(depth['quarters']['firjan'])+len(depth['quarters']['sikak']):bad('entities','KW-historic-places','historic place count mismatch')
 if {x['canonical_name'] for x in places}<{q['name'] for q in depth['quarters']['city_quarters']}|{q['name'] for q in depth['quarters']['firjan']}:bad('entities','KW-historic-places','fixture firjan missing from entities')
 if any(x['status']!='historical' for x in places):bad('entities','KW-historic-places','historic place is not historical')
 if any(x['canonical_source_id'] not in {'SRC-KW-KUNA-FIRJAN-2017','SRC-KW-MIRQAB-HERITAGE-2026'} for x in places):bad('entities','KW-historic-places','unexpected historic source')
 if any(y['relationship_type']=='administrative_parent' for x in places for y in R if y['child_id']==x['id']):bad('relationships','KW-historic-places','historic place carries an administrative parent')
 if any(not [y for y in R if y['child_id']==x['id'] and y['relationship_type']=='located_in'] for x in places):bad('relationships','KW-historic-places','historic place lacks located_in')
 if any(y['predicate']=='population' for x in places for y in C if y['subject_id']==x['id']):bad('claims','KW-historic-places','invented population on a historic place')
 ich=[x for x in C if x.get('source_id')==ICH]
 if len(ich)!=len(depth['ich_elements']):bad('claims','KW-ich','UNESCO element claim count mismatch')
 if any(not x.get('published') or x.get('verification_status')!='verified' or not x.get('classification') for x in ich):bad('claims','KW-ich','UNESCO element contract')
 if any(x['classification'] not in {'shared','national'} for x in ich):bad('claims','KW-ich','UNESCO element misclassified')
 weak=[x for x in C if tiers.get(x.get('source_id'))=='E']
 if any(x.get('published') for x in weak):bad('claims','KW-depth','tier-E claim published')
 if any(x.get('verification_status') not in {'probable','local_reported','unverified','folk_narrative'} for x in weak):bad('claims','KW-depth','tier-E claim exceeds the local_reported cap')
 if any(not x.get('classification') for x in weak):bad('claims','KW-depth','tier-E claim without classification')
 for nm in SHARED_DISHES:
  q=next((x for x in C if x['predicate']=='food_dish' and x['value']['data'].get('name')==nm),None)
  if not q or q.get('classification')!='shared':bad('claims','KW-shared',f'{nm} is not classified shared')
 if any(len(x['value']['data'].get('sample_words',[]))!=0 and not all(len(w)==2 for w in x['value']['data']['sample_words']) for x in C if x['predicate']=='dialect_profile'):bad('claims','KW-dialect','dialect sample words lack glosses')
 result={}
 for fam,rows in families.items():
  selected=set(s['families'][fam]['record_ids']);actualids={r['id'] for r in rows};ff=[x for x in find if x['family']==fam];ok=selected==actualids and not ff;result[fam]={'population':len(rows),'sampled':len(selected),'passed':len(selected) if ok else len(selected)-len(ff),'failed':0 if ok else len(ff),'sample_percentage':100.0,'status':'PASS' if ok else 'FAIL'}
 ok=not find and all(x['status']=='PASS' for x in result.values());report={'schema_version':'2.0.0','country_code':'KW','snapshot_date':'2026-09-20','status':'PASS' if ok else 'FAIL','method':'Independent full review against checksum-bound CSB/UNESCO/heritage fixtures; importer and semantic validator not imported.','p0':0,'critical_p1':len(find),'families':result,'total_sampled':sum(x['sampled'] for x in result.values()),'total_passed':sum(x['passed'] for x in result.values()),'findings':find};write_json(ROOT/'reports/kuwait_independent_review.json',report);[print(f"[{x['status']}] {k}: {x['passed']}/{x['sampled']}") for k,x in result.items()];return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
