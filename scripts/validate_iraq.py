#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='IQ'];ids={r['id'] for r in e};sids={'SRC-IQ-COSIT-GOVERNORATES-2023','SRC-IQ-LAW-7-HALABJA-2025','SRC-IQ-DECREE-21-HALABJA-2025','SRC-IQ-KRSO-FOUR-GOVERNORATES'}
 return {'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='IQ'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='IQ'],'manifest':L(ROOT/'manifests/IQ.yml')}
def validate(d):
 f=L(ROOT/'data/imports/iraq/fixtures/governorate_profiles_2025.json');E={r['id']:r for r in d['entities']};C=d['claims'];err=[]
 def x(c,l,m):err.append({'code':c,'location':l,'message':m})
 if sum(r['entity_type']=='iq_governorate' for r in E.values())!=19 or len(E)!=20:x('IQ_COUNTS','entities','country+19')
 for q in f['governorates']:
  eid='ENT-IQ-GOVERNORATE-'+q['code']
  if E.get(eid,{}).get('canonical_name')!=q['name_ar'] or not any(c['subject_id']==eid and c['predicate']=='administrative_profile' and c['value']['data']==q['profile'] for c in C):x('IQ_PROFILE',eid,'identity/profile')
 h=E.get('ENT-IQ-GOVERNORATE-19',{})
 if h.get('valid_from')!='2025-05-05' or not any(c['subject_id']==h.get('id') and c['predicate']=='federal_establishment_law' and c['value']['data']['law_number']==7 for c in C):x('IQ_HALABJA_LAW','Halabja','law/date')
 if {r['id']:r['value'] for r in d['denominators']}!={'DEN-IQ-COUNTRY-SCOPE':1,'DEN-IQ-GOVERNORATES':19,'DEN-IQ-KRI-PROFILE':4,'DEN-IQ-FEDERAL-NON-KRI':15}:x('IQ_DENOMINATORS','den','1/19/4/15')
 if any(r['entity_type'] in {'iq_district','iq_subdistrict'} for r in E.values()):x('IQ_PREMATURE_LOWER','entities','lower deferred')
 if any(r.get('status') in {'de_facto','disputed'} for r in E.values()):x('IQ_UNSUPPORTED_OVERLAY','entities','overlay absent')
 return err
def main():
 d=data();e=validate(d);met={k:len(d[k]) for k in ['entities','aliases','relationships','claims','sources','denominators','coverage']};write_json(ROOT/'reports/iraq_validation.json',{'schema_version':'2.0.0','country_code':'IQ','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e});print(met);return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
