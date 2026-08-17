#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='OM'];ids={r['id'] for r in e};sids={'SRC-OM-RD-36-2022-GOVERNORATES','SRC-OM-ONA-63-WILAYATS-2022','SRC-OM-NCSI-ADMIN-CODES-2026'}
 return {'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='OM'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='OM'],'manifest':L(ROOT/'manifests/OM.yml')}
def validate(d):
 f=L(ROOT/'data/imports/oman/fixtures/legal_hierarchy_2022.json');E={r['id']:r for r in d['entities']};err=[]
 def x(c,l,m):err.append({'code':c,'location':l,'message':m})
 gs=[r for r in E.values() if r['entity_type']=='om_governorate'];ws=[r for r in E.values() if r['entity_type']=='om_wilaya']
 if len(gs)!=11 or len(ws)!=63 or len(E)!=75:x('OM_COUNTS','entities','country+11+63 expected')
 for g in f['governorates']:
  gid='ENT-OM-GOVERNORATE-'+g['code'];q=E.get(gid,{})
  if q.get('canonical_name')!=g['name_ar']:x('OM_GOVERNORATE',gid,'identity')
  children={r['child_id'] for r in d['relationships'] if r.get('parent_id')==gid}
  expected={'ENT-OM-WILAYA-'+w['code'] for w in g['wilayats']}
  if children!=expected:x('OM_WILAYAT_PARENT',gid,'child set mismatch')
  if not any(c['subject_id']==gid and c['predicate']=='wilayat_count' and c['value']['data']==len(expected) for c in d['claims']):x('OM_CHILD_COUNT',gid,'count claim')
 if len(d['aliases'])!=74 or len(d['relationships'])!=74 or len(d['claims'])!=11:x('OM_RECORD_COUNTS','OM','74/74/11')
 if {r['id']:r['value'] for r in d['denominators']}!={'DEN-OM-COUNTRY-SCOPE':1,'DEN-OM-GOVERNORATES-2022':11,'DEN-OM-WILAYATS-2022':63}:x('OM_DENOMINATORS','den','1/11/63')
 if any(r['entity_type']=='om_niyaba' for r in E.values()):x('OM_NIYABA','entities','unsupported niyabah')
 m=d['manifest'];n=next(q for q in m['hierarchy'] if q['entity_type']=='om_niyaba')
 if n.get('denominator') is not None or n.get('scope_status')!='unavailable':x('OM_NIYABA_DENOM','manifest','fake denominator')
 if 'ENT-OM-WILAYA-0509' not in E or 'ENT-OM-WILAYA-0907' not in E:x('OM_ADDITIONS','entities','two additions absent')
 if 'ENT-OM-WILAYA-0210' not in E or E.get('ENT-OM-WILAYA-0208',{}).get('canonical_name')!='مقشن':x('OM_DHOFAR','Dhofar','translation reconciliation')
 return err
def main():
 d=data();e=validate(d);met={k:len(d[k]) for k in ['entities','aliases','relationships','claims','sources','denominators','coverage']};write_json(ROOT/'reports/oman_validation.json',{'schema_version':'2.0.0','country_code':'OM','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e});print(met);return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
