#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='SO'];ids={r['id'] for r in e};sids={'SRC-SO-MOP-FMS-2026','SRC-SO-MOIFAR-NORTHEAST-2026','SRC-SO-SONNA-NORTHEAST-DECLARATION-2026','SRC-SO-SENATE-CONSTITUENCY','SRC-SO-MPWR-FIVE-FMS-2025'}
 return {'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='SO'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='SO'],'manifest':L(ROOT/'manifests/SO.yml')}
def validate(d):
 f=L(ROOT/'data/imports/somalia/fixtures/federal_frames_2026.json');E={r['id']:r for r in d['entities']};C=d['claims'];err=[]
 def x(c,l,m):err.append({'code':c,'location':l,'message':m})
 fs=[r for r in E.values() if r['entity_type']=='so_federal_member_state'];regions=[r for r in E.values() if r['entity_type']=='so_region']
 if len(E)!=9 or len(fs)!=7 or len(regions)!=1:x('SO_COUNTS','entities','country+7 MOP-frame FMS+Banadir')
 for q in f['federal_member_states']:
  eid='ENT-SO-FMS-'+q['code']
  if E.get(eid,{}).get('canonical_name')!=q['name'] or not any(c['subject_id']==eid and c['predicate']=='federal_planning_profile' and c['value']['data']==q['profile'] for c in C):x('SO_FRAME_PROFILE',eid,'identity/profile')
 if E.get('ENT-SO-REGION-BRA',{}).get('canonical_name')!='Banadir Regional Administration' or E.get('ENT-SO-REGION-BRA',{}).get('entity_type')!='so_region':x('SO_BANADIR_PARALLEL','Banadir','must remain regional administration')
 sl=E.get('ENT-SO-FMS-06',{});slc=next((c for c in C if c.get('subject_id')==sl.get('id') and c.get('predicate')=='federal_planning_profile'),{})
 if sl.get('status')!='claimed' or slc.get('classification')!='disputed':x('SO_SOMALILAND_NARRATIVE','Somaliland','claimed entity and disputed narrative required')
 ne=E.get('ENT-SO-FMS-07',{});tr=next((c for c in C if c.get('predicate')=='federal_member_transition'),None)
 if ne.get('valid_from')!='2026-01-17' or not tr or tr['value']['data'].get('predecessor_name')!='SSC-Khaatumo' or tr['value']['data'].get('full_member_declaration')!='2026-01-17':x('SO_NORTHEAST_TRANSITION','North East','transition dates/provenance')
 if any('SSC' in r.get('canonical_name','') or 'Khaatumo' in r.get('canonical_name','') for r in E.values()):x('SO_SSC_DUPLICATE','entities','SSC is predecessor, not duplicate current entity')
 expected={'DEN-SO-COUNTRY-SCOPE':1,'DEN-SO-MOP-FMS':7,'DEN-SO-STANDARD-FIVE':5,'DEN-SO-SOMALILAND-NARRATIVE':1,'DEN-SO-NORTHEAST':1,'DEN-SO-BANADIR':1,'DEN-SO-REGIONS':None,'DEN-SO-DISTRICTS':None}
 if {r['id']:r['value'] for r in d['denominators']}!=expected:x('SO_DENOMINATORS','denominators','authority-specific and unavailable layers')
 if any(r['entity_type']=='so_district' for r in E.values()):x('SO_PREMATURE_LOWER','entities','districts unavailable')
 if any(r.get('status') in {'de_facto','destroyed','displaced','disputed'} for r in E.values()):x('SO_UNSUPPORTED_OVERLAY','entities','no control/condition overlay')
 rel=[r for r in d['relationships'] if r.get('child_id')!='ENT-SO-COUNTRY']
 if len(rel)!=8 or any(r.get('parent_id')!='ENT-SO-COUNTRY' for r in rel):x('SO_PARENT','relationships','all frame entities parent to country')
 cov={r['id']:r for r in d['coverage']}
 if cov.get('COV-SO-MOP-FMS',{}).get('matched')!=7 or cov.get('COV-SO-MOP-FMS',{}).get('snapshot_date')!='2026-08-17':x('SO_COVERAGE_FRESHNESS','coverage','7/7 current MOP frame')
 for i in ['COV-SO-REGIONS','COV-SO-DISTRICTS']:
  r=cov.get(i,{})
  if r.get('denominator') is not None or r.get('coverage_percentage') is not None or r.get('complete') is not False:x('SO_UNAVAILABLE_LOWER',i,'null denominator and no percentage')
 return err
def main():
 d=data();e=validate(d);met={k:len(d[k]) for k in ['entities','aliases','relationships','claims','sources','denominators','coverage']};write_json(ROOT/'reports/somalia_validation.json',{'schema_version':'2.0.0','country_code':'SO','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e});print(met);return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
