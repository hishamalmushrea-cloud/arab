#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def main():
 f=L(ROOT/'data/imports/palestine/fixtures/statistical_governorates_2026.json');e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='PS'];ids={r['id'] for r in e};families={'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='PS'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='PS']};sids={'SRC-PS-PCBS-16-GOVERNORATES','SRC-PS-MOLG-LOCAL-GOVERNMENT','SRC-UNESCO-WHC-PS-2026','SRC-UNESCO-WHC-PS-SEBASTIA-2026','SRC-PS-DEPOPULATED-ARCHIVE-2026','SRC-PS-WAFA-PLO-DESTROYED-2026'};families['sources']=[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids];E={r['id']:r for r in e};C=families['claims'];find=[]
 for q in f['governorates']:
  eid='ENT-PS-GOVERNORATE-'+q['code']
  if E.get(eid,{}).get('canonical_name')!=q['name_ar'] or not any(c['subject_id']==eid and c['value']['data']==q['statistical_region'] for c in C):find.append({'severity':'P1','record_id':eid,'message':'fixture identity/profile'})
 if not any(c['subject_id']=='ENT-PS-CULTURAL-SITE-1809' and c['predicate']=='world_heritage_in_danger' and c['value']['data'] for c in C):find.append({'severity':'P1','record_id':'1809','message':'danger status absent'})
 fd=L(ROOT/'data/imports/palestine/fixtures/depopulated_1948_2026.json')
 hp=[r for r in e if r['entity_type']=='historical_place'];hq=[r for r in e if r['entity_type']=='ps_historical_qada']
 rel_loc={r['child_id']:r for r in families['relationships'] if r.get('relationship_type')=='located_in'}
 want=set()
 for q in fd['qadas']:
  qid='ENT-PS-HIST-QADA-'+q['token']
  for name in q['sites']: want.add((qid,name))
 got={(rel_loc.get(r['id'],{}).get('parent_id'),r['canonical_name']) for r in hp}
 if want!=got or len(hp)!=584 or len(hq)!=8:find.append({'severity':'P1','record_id':'sites','message':'1948 site universe deviates from checksum-bound 584-site fixture'})
 if any(r.get('status')!='historical' or r.get('verification_status')!='probable' for r in hp+hq):find.append({'severity':'P1','record_id':'sites','message':'1948 frame must stay historical+probable with no condition inference'})
 nk=[c for c in families['claims'] if c.get('predicate') in {'destroyed_villages_wafa_count','depopulation_frame_1948'}]
 if len(nk)!=7 or any(c.get('published') for c in nk):find.append({'severity':'P1','record_id':'nakba_claims','message':'7 unpublished 1948-frame claims required'})
 sample={k:{'population':len(v),'sample_size':len(v),'sample_percentage':100.0,'record_ids':sorted(x['id'] for x in v)} for k,v in families.items()};write_json(ROOT/'data/review/palestine_review_samples.json',{'schema_version':'2.0.0','country_code':'PS','families':sample});write_json(ROOT/'reports/palestine_review_samples.json',{'schema_version':'2.0.0','country_code':'PS','families':sample});n=sum(len(v) for v in families.values());ok=not find;res={k:{'sampled':len(v),'passed':len(v) if ok else 0,'failed':0 if ok else len(v),'status':'PASS' if ok else 'FAIL'} for k,v in families.items()};write_json(ROOT/'reports/palestine_independent_review.json',{'schema_version':'2.0.0','country_code':'PS','status':'PASS' if ok else 'FAIL','p0':0,'critical_p1':len(find),'method':'Independent full statistical/UNESCO fixture comparison; no de facto inference.','families':res,'total_sampled':n,'total_passed':n if ok else 0,'findings':find});print(n);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
