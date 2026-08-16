#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='PS'];ids={r['id'] for r in e};sids={'SRC-PS-PCBS-16-GOVERNORATES','SRC-PS-MOLG-LOCAL-GOVERNMENT','SRC-UNESCO-WHC-PS-2026','SRC-UNESCO-WHC-PS-SEBASTIA-2026'}
 return {'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='PS'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='PS'],'manifest':L(ROOT/'manifests/PS.yml')}
def validate(d):
 f=L(ROOT/'data/imports/palestine/fixtures/statistical_governorates_2026.json');E={r['id']:r for r in d['entities']};C=d['claims'];err=[]
 def x(c,l,m):err.append({'code':c,'location':l,'message':m})
 if sum(r['entity_type']=='ps_governorate' for r in E.values())!=16 or sum(r['entity_type']=='cultural_site' for r in E.values())!=6 or len(E)!=23:x('PS_COUNTS','entities','country+16+6')
 for q in f['governorates']:
  eid='ENT-PS-GOVERNORATE-'+q['code']
  if E.get(eid,{}).get('canonical_name')!=q['name_ar'] or not any(c['subject_id']==eid and c['predicate']=='statistical_region' and c['value']['data']==q['statistical_region'] for c in C):x('PS_GOVERNORATE',eid,'identity/profile')
 if any(r.get('status') in {'de_facto','destroyed','displaced'} for r in E.values()):x('PS_UNSUPPORTED_STATUS','entities','no overlay evidence in this cycle')
 if {r['id']:r['value'] for r in d['denominators']}!={'DEN-PS-COUNTRY-SCOPE':1,'DEN-PS-GOVERNORATES':16,'DEN-PS-WEST-BANK':11,'DEN-PS-GAZA':5,'DEN-PS-WHC':6}:x('PS_DENOMINATORS','den','1/16/11/5/6')
 seb='ENT-PS-CULTURAL-SITE-1809'
 for pred in ['emergency_inscription','world_heritage_in_danger']:
  if not any(c['subject_id']==seb and c['predicate']==pred and c['value']['data'] is True and c['observed_at']=='2026-07-29' for c in C):x('PS_SEBASTIA_STATUS',seb,pred)
 if any(r['entity_type']=='ps_local_government_unit' for r in E.values()):x('PS_PREMATURE_LOCAL','entities','local authorities deferred')
 return err
def main():
 d=data();e=validate(d);met={k:len(d[k]) for k in ['entities','aliases','relationships','claims','sources','denominators','coverage']};write_json(ROOT/'reports/palestine_validation.json',{'schema_version':'2.0.0','country_code':'PS','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e});print(met);return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
