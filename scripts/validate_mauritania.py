#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='MR'];ids={r['id'] for r in e};sids={'SRC-MR-DGAT-15-63-2026','SRC-MR-ANSADE-RGPH5-2024','SRC-MR-ANSADE-PEER-REVIEW-2024'}
 return {'entities':e,'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='MR'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='MR'],'manifest':L(ROOT/'manifests/MR.yml')}
def validate(d):
 f=L(ROOT/'data/imports/mauritania/fixtures/wilaya_profiles.json');E={r['id']:r for r in d['entities']};C=d['claims'];err=[]
 def x(c,l,m):err.append({'code':c,'location':l,'message':m})
 if len(E)!=16 or sum(r['entity_type']=='mr_wilaya' for r in E.values())!=15:x('MR_COUNTS','entities','country+15')
 for q in f['wilayas']:
  eid='ENT-MR-WILAYA-'+q['code']
  if E.get(eid,{}).get('canonical_name')!=q['name_fr'] or not any(c['subject_id']==eid and c['predicate']=='administrative_profile' and c['value']['data']==q['profile'] for c in C):x('MR_PROFILE',eid,'identity/profile')
 vals={c['predicate']:c['value']['data'] for c in C if c['subject_id']=='ENT-MR-COUNTRY'}
 if vals!={'moughataa_count':63,'commune_count_candidates':[219,220]}:x('MR_COUNTS_CLAIMS','claims',str(vals))
 if {r['id']:r['value'] for r in d['denominators']}!={'DEN-MR-COUNTRY-SCOPE':1,'DEN-MR-WILAYAS':15,'DEN-MR-NOUAKCHOTT-WILAYAS':3,'DEN-MR-REGIONAL-WILAYAS':12}:x('MR_DENOMINATORS','den','1/15/3/12')
 if any(r['entity_type'] in {'mr_moughataa','mr_commune'} for r in E.values()):x('MR_PREMATURE_LOWER','entities','lower deferred')
 m=d['manifest'];mo=next(q for q in m['hierarchy'] if q['entity_type']=='mr_moughataa');co=next(q for q in m['hierarchy'] if q['entity_type']=='mr_commune')
 if mo.get('denominator')!=63 or mo.get('scope_status')!='open':x('MR_MOUGHATAA_SCOPE','manifest','63 open')
 if co.get('denominator') is not None or co.get('scope_status')!='open':x('MR_COMMUNE_CONFLICT','manifest','no denominator')
 return err
def main():
 d=data();e=validate(d);met={k:len(d[k]) for k in ['entities','relationships','claims','sources','denominators','coverage']};write_json(ROOT/'reports/mauritania_validation.json',{'schema_version':'2.0.0','country_code':'MR','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e});print(met);return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
