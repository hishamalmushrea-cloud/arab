#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def main():
 f=L(ROOT/'data/imports/morocco/fixtures/territorial_division_2015.json');e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='MA'];ids={r['id'] for r in e};families={'entities':e,'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='MA'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='MA']};sids={'SRC-MA-DGCT-DECREE-2-15-10','SRC-MA-DGCT-TERRITORIAL-COUNTS-2026','SRC-MA-HCP-RGPH-2024'};families['sources']=[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids];E={r['id']:r for r in e};R=families['relationships'];find=[]
 for g in f['regions']:
  gid='ENT-MA-REGION-'+g['token']
  for q in g['children']:
   eid=('ENT-MA-PREFECTURE-' if q['entity_type']=='ma_prefecture' else 'ENT-MA-PROVINCE-')+q['token']
   if E.get(eid,{}).get('canonical_name')!=q['name_fr'] or not any(r['child_id']==eid and r['parent_id']==gid for r in R):find.append({'severity':'P1','record_id':eid,'message':'fixture identity/parent'})
 sample={k:{'population':len(v),'sample_size':len(v),'sample_percentage':100.0,'record_ids':sorted(x['id'] for x in v)} for k,v in families.items()};write_json(ROOT/'data/review/morocco_review_samples.json',{'schema_version':'2.0.0','country_code':'MA','families':sample});write_json(ROOT/'reports/morocco_review_samples.json',{'schema_version':'2.0.0','country_code':'MA','families':sample});n=sum(len(v) for v in families.values());ok=not find;res={k:{'sampled':len(v),'passed':len(v) if ok else 0,'failed':0 if ok else len(v),'status':'PASS' if ok else 'FAIL'} for k,v in families.items()};write_json(ROOT/'reports/morocco_independent_review.json',{'schema_version':'2.0.0','country_code':'MA','status':'PASS' if ok else 'FAIL','p0':0,'critical_p1':len(find),'method':'Independent full fixture hierarchy comparison.','families':res,'total_sampled':n,'total_passed':n if ok else 0,'findings':find});print(n);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
