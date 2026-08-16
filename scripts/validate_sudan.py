#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='SD'];ids={r['id'] for r in e};sids={'SRC-SD-PRESIDENCY-STATES-CATALOGUE','SRC-SD-EMBASSY-QATAR-18-STATES','SRC-SD-CBS-AUTHORITY'}
 return {'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='SD'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='SD']}
def validate(d):
 f=L(ROOT/'data/imports/sudan/fixtures/states_2026.json');E={r['id']:r for r in d['entities']};C=d['claims'];e=[]
 def x(c,l,m):e.append({'code':c,'location':l,'message':m})
 if len(E)!=19 or sum(r['entity_type']=='sd_state' for r in E.values())!=18:x('SD_COUNTS','entities','country+18 states')
 for q in f['states']:
  eid='ENT-SD-STATE-'+q['code']
  if E.get(eid,{}).get('canonical_name')!=q['name_ar'] or not any(c['subject_id']==eid and c['predicate']=='administrative_profile' for c in C):x('SD_FIXTURE',eid,'identity/profile')
 rec=next((c for c in C if c.get('predicate')=='administrative_denominator_reconciliation'),{})
 if rec.get('value',{}).get('data',{}).get('accepted_current')!=18 or rec.get('value',{}).get('data',{}).get('stale_rejected')!=17:x('SD_RECONCILIATION','claims','18 accepted/17 rejected')
 if any('أبيي' in r.get('canonical_name','') for r in E.values()):x('SD_ABYEI_ORDINARY','entities','Abyei not ordinary state')
 if any(r['entity_type'] in {'sd_locality','sd_administrative_unit'} for r in E.values()):x('SD_PREMATURE_LOWER','entities','lower unavailable')
 if any(r.get('status') in {'de_facto','destroyed','displaced','disputed'} for r in E.values()):x('SD_UNSUPPORTED_OVERLAY','entities','legal frame cannot encode war status')
 if {r['id']:r['value'] for r in d['denominators']}!={'DEN-SD-COUNTRY-SCOPE':1,'DEN-SD-STATES':18,'DEN-SD-LOCALITIES':None,'DEN-SD-ADMIN-UNITS':None}:x('SD_DENOMINATORS','denominators','1/18/null/null')
 rel=[r for r in d['relationships'] if r.get('child_id')!='ENT-SD-COUNTRY']
 if len(rel)!=18 or any(r.get('parent_id')!='ENT-SD-COUNTRY' for r in rel):x('SD_PARENT','relationships','18 country parents')
 cov={r['id']:r for r in d['coverage']}
 if cov.get('COV-SD-STATES',{}).get('matched')!=18 or cov.get('COV-SD-STATES',{}).get('snapshot_date')!='2026-08-17':x('SD_FRESHNESS','coverage','18 current snapshot')
 for i in ['COV-SD-LOCALITIES','COV-SD-ADMIN-UNITS']:
  r=cov.get(i,{})
  if r.get('denominator') is not None or r.get('coverage_percentage') is not None:x('SD_UNAVAILABLE_LOWER',i,'no denominator/percentage')
 return e
def main():
 d=data();e=validate(d);met={k:len(d[k]) for k in ['entities','aliases','relationships','claims','sources','denominators','coverage']};write_json(ROOT/'reports/sudan_validation.json',{'schema_version':'2.0.0','country_code':'SD','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e});print(met);return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
