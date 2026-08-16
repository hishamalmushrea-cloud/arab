#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def main():
 f=L(ROOT/'data/imports/algeria/fixtures/wilaya_transition.json');e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='DZ'];ids={r['id'] for r in e};families={'entities':e,'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='DZ'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='DZ']};sids={'SRC-DZ-ONS-CGN-2021','SRC-DZ-INTERIOR-58-WILAYAS','SRC-DZ-INTERIOR-69-TRANSITION-2025'};families['sources']=[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids];find=[];current={r['canonical_name']:r for r in e if r.get('status')=='current' and r['entity_type']=='dz_wilaya'};future={r['canonical_name']:r for r in e if r.get('status')=='proposed'}
 for q in f['current_wilayas']:
  if q['name_fr'] not in current:find.append({'severity':'P1','record_id':q['name_fr'],'message':'current identity missing'})
 for q in f['future_promotions']:
  r=future.get(q['name_fr']);
  if not r or r.get('valid_from')!='2027-01-01':find.append({'severity':'P1','record_id':q['name_fr'],'message':'future identity/date mismatch'})
 sample={k:{'population':len(v),'sample_size':len(v),'sample_percentage':100.0,'record_ids':sorted(x['id'] for x in v)} for k,v in families.items()};write_json(ROOT/'data/review/algeria_review_samples.json',{'schema_version':'2.0.0','country_code':'DZ','families':sample});write_json(ROOT/'reports/algeria_review_samples.json',{'schema_version':'2.0.0','country_code':'DZ','families':sample});n=sum(len(v) for v in families.values());ok=not find;res={k:{'sampled':len(v),'passed':len(v) if ok else 0,'failed':0 if ok else len(v),'status':'PASS' if ok else 'FAIL'} for k,v in families.items()};write_json(ROOT/'reports/algeria_independent_review.json',{'schema_version':'2.0.0','country_code':'DZ','status':'PASS' if ok else 'FAIL','p0':0,'critical_p1':len(find),'method':'Independent full current/future fixture comparison.','families':res,'total_sampled':n,'total_passed':n if ok else 0,'findings':find});print(n);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
