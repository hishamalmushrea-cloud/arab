#!/usr/bin/env python3
"""Independent full Kuwait review; does not import importer or semantic validator."""
import hashlib,json
from model import ROOT,read_jsonl,write_json
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
 s=load(ROOT/'data/review/kuwait_review_samples.json');f=load(ROOT/'data/imports/kuwait/fixtures/census_governorates_2021.json');m=load(ROOT/'data/imports/kuwait/snapshot_manifest.json');find=[]
 def bad(fam,r,msg):find.append({'severity':'P1','family':fam,'record_id':r,'message':msg})
 for x in m['records']:
  p=ROOT/x['path'];b=p.read_bytes()
  if len(b)!=x['bytes'] or hashlib.sha256(b).hexdigest()!=x['sha256']:bad('sources',x['path'],'checksum mismatch')
 es=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='KW'];ids={r['id'] for r in es};A=[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids];R=[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids];C=[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids];D=[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='KW'];V=[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='KW'];sourceids=set(s['families']['sources']['record_ids']);S=[load(p) for p in (ROOT/'data/sources').glob('*.json') if load(p).get('id') in sourceids];families={'entities':es,'aliases':A,'relationships':R,'claims':C,'sources':S,'denominators':D,'coverage':V}
 expected={r['name_ar']:(r['name_en'],r['population']) for r in f['records']};actual={r['canonical_name']:r for r in es if r['entity_type']=='kw_governorate'}
 if set(expected)!=set(actual):bad('entities','KW-governorates','six-name set mismatch')
 for ar,(en,pop) in expected.items():
  eid=actual.get(ar,{}).get('id')
  if not eid:continue
  if not any(x['entity_id']==eid and x['name']==en for x in A):bad('aliases',eid,'English alias mismatch')
  if not any(x['child_id']==eid and x['parent_id']=='ENT-KW-COUNTRY' for x in R):bad('relationships',eid,'country parent missing')
  if not any(x['subject_id']==eid and x['predicate']=='population' and x['value']['data']==pop and x['second_source_id'] for x in C):bad('claims',eid,'population/reconciliation mismatch')
 if sum(r['population'] for r in f['records'])+f['not_stated_population']!=f['total_population']:bad('claims','KW-total','table does not reconcile')
 if any(x['predicate']!='population' for x in C):bad('claims','KW-scope','unsupported non-population claim')
 result={}
 for fam,rows in families.items():
  selected=set(s['families'][fam]['record_ids']);actualids={r['id'] for r in rows};ff=[x for x in find if x['family']==fam];ok=selected==actualids and not ff;result[fam]={'population':len(rows),'sampled':len(selected),'passed':len(selected) if ok else len(selected)-len(ff),'failed':0 if ok else len(ff),'sample_percentage':100.0,'status':'PASS' if ok else 'FAIL'}
 ok=not find and all(x['status']=='PASS' for x in result.values());report={'schema_version':'2.0.0','country_code':'KW','snapshot_date':'2026-08-16','status':'PASS' if ok else 'FAIL','method':'Independent full review against checksum-bound CSB/UNESCO fixtures; importer and semantic validator not imported.','p0':0,'critical_p1':len(find),'families':result,'total_sampled':sum(x['sampled'] for x in result.values()),'total_passed':sum(x['passed'] for x in result.values()),'findings':find};write_json(ROOT/'reports/kuwait_independent_review.json',report);[print(f"[{x['status']}] {k}: {x['passed']}/{x['sampled']}") for k,x in result.items()];return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
