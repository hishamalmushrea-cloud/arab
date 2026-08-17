#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='DZ'];ids={r['id'] for r in e};sids={'SRC-DZ-ONS-CGN-2021','SRC-DZ-INTERIOR-58-WILAYAS','SRC-DZ-INTERIOR-69-TRANSITION-2025'}
 return {'entities':e,'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='DZ'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='DZ'],'manifest':L(ROOT/'manifests/DZ.yml')}
def validate(d):
 f=L(ROOT/'data/imports/algeria/fixtures/wilaya_transition.json');E=d['entities'];R=d['relationships'];C=d['claims'];err=[]
 def x(c,l,m):err.append({'code':c,'location':l,'message':m})
 current=[r for r in E if r.get('entity_type')=='dz_wilaya' and r.get('status')=='current'];future=[r for r in E if r.get('entity_type')=='dz_wilaya' and r.get('status')=='proposed']
 if len(current)!=58 or len(future)!=11 or len(E)!=70:x('DZ_COUNTS','entities','country+58+11')
 if any(r.get('valid_from')!='2027-01-01' for r in future):x('DZ_FUTURE_DATE','future','effective date')
 if any(r.get('status')!='proposed' for r in future):x('DZ_FUTURE_STATUS','future','not proposed')
 if len(R)!=69 or any(r['parent_id']!='ENT-DZ-COUNTRY' for r in R):x('DZ_PARENT','relationships','country parents')
 vals={r['predicate']:r['value']['data'] for r in C}
 if vals!={'current_wilaya_count':58,'future_wilaya_count':69,'commune_count':1541}:x('DZ_CLAIMS','claims',str(vals))
 if {r['id']:r['value'] for r in d['denominators']}!={'DEN-DZ-COUNTRY-SCOPE':1,'DEN-DZ-WILAYAS-CURRENT-2021':58,'DEN-DZ-WILAYAS-FUTURE-2027':69}:x('DZ_DENOMINATORS','den','1/58/69')
 if any(r.get('entity_type') in {'dz_commune','dz_daira'} for r in E):x('DZ_PREMATURE_LOWER','entities','lower units deferred')
 q=next(r for r in d['manifest']['hierarchy'] if r['entity_type']=='dz_wilaya')
 if q.get('denominator')!=58:x('DZ_CURRENT_MANIFEST','manifest','current must remain58')
 return err
def main():
 d=data();e=validate(d);met={k:len(d[k]) for k in ['entities','relationships','claims','sources','denominators','coverage']};write_json(ROOT/'reports/algeria_validation.json',{'schema_version':'2.0.0','country_code':'DZ','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e});print(met);return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
