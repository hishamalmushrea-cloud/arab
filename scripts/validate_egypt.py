#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='EG'];ids={r['id'] for r in e};sids={'SRC-EG-CAPMAS-27-GOVERNORATES-2021','SRC-EG-MLD-27-GOVERNORATES-2026','SRC-EG-CAPMAS-GOVERNORATE-CODES','SRC-EG-MARKAZ-LISTS-MIRROR-2026'}
 return {'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='EG'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='EG'],'manifest':L(ROOT/'manifests/EG.yml')}
def validate(d):
 f=L(ROOT/'data/imports/egypt/fixtures/governorate_profiles.json');E={r['id']:r for r in d['entities']};err=[]
 def x(c,l,m):err.append({'code':c,'location':l,'message':m})
 gs=[r for r in E.values() if r['entity_type']=='eg_governorate'];mk=[r for r in E.values() if r['entity_type']=='eg_markaz']
 if len(gs)!=27 or len(mk)!=55 or len(E)!=83:x('EG_COUNTS','entities','country+27+55 marakiz')
 fk=L(ROOT/'data/imports/egypt/fixtures/markaz_depth_2026.json')
 rel_by_child={r['child_id']:r for r in d['relationships']}
 want={('ENT-EG-GOVERNORATE-'+g['code'],n) for g in fk['governorates'] for n in g['marakiz']}
 got={(rel_by_child.get(r['id'],{}).get('parent_id'),r['canonical_name']) for r in mk}
 if want!=got:x('EG_MARKAZ_FIXTURE','marakiz','markaz (parent,name) set must equal the checksum-bound 55-markaz fixture')
 if any(r.get('verification_status')!='probable' for r in mk):x('EG_MARKAZ_STATUS','marakiz','markaz identities carry probable status')
 mpop=[c for c in d['claims'] if c.get('predicate')=='population' and c.get('subject_id') in {r['id'] for r in mk}]
 if len(mpop)!=17 or any(c.get('published') for c in mpop):x('EG_MARKAZ_POP','claims','17 unpublished probable 2024 markaz population claims')
 for q in f['governorates']:
  eid='ENT-EG-GOVERNORATE-'+q['code'];r=E.get(eid,{})
  if r.get('canonical_name')!=q['name_ar']:x('EG_IDENTITY',eid,'name')
  if not any(c['subject_id']==eid and c['predicate']=='administrative_profile' and c['value']['data']==q['profile'] for c in d['claims']):x('EG_PROFILE',eid,'profile')
  if not any(a['entity_id']==eid and a['name']==q['name_en'] for a in d['aliases']):x('EG_ALIAS',eid,'English alias')
 gov_ids={r['id'] for r in gs}
 rel1=[r for r in d['relationships'] if r['child_id'] in gov_ids]
 if len(rel1)!=27 or any(r['parent_id']!='ENT-EG-COUNTRY' for r in rel1):x('EG_PARENT','relationships','country parents')
 rel2=[r for r in d['relationships'] if r['child_id'] in {z['id'] for z in mk}]
 if len(rel2)!=55 or any(r['parent_id'] not in gov_ids for r in rel2):x('EG_MARKAZ_PARENT','relationships','all 55 marakiz parent to a governorate')
 if {r['id']:r['value'] for r in d['denominators']}!={'DEN-EG-COUNTRY-SCOPE':1,'DEN-EG-GOVERNORATES':27,'DEN-EG-URBAN-PROFILES':4,'DEN-EG-MIXED-PROFILES':23,'DEN-EG-MARKAZ-DOCUMENTED':55}:x('EG_DENOMINATORS','den','1/27/4/23/55')
 dmk=next((r for r in d['denominators'] if r['id']=='DEN-EG-MARKAZ-DOCUMENTED'),{})
 if dmk.get('status')!='official' or 'subset' not in dmk.get('layer',''):x('EG_MARKAZ_DENOM_STATUS','den','subset denominator must stay an explicitly-labeled documented subset')
 if any(r['entity_type'] in {'eg_qism','eg_local_unit','eg_shiyakha'} for r in E.values()):x('EG_PREMATURE_LOWER','entities','qism/local-unit/shiyakha deferred')
 for t in ['eg_qism','eg_local_unit','eg_shiyakha']:
  q=next(z for z in d['manifest']['hierarchy'] if z['entity_type']==t)
  if q.get('scope_status')!='unavailable':x('EG_LOWER_SCOPE',t,'must unavailable')
 return err
def main():
 d=data();e=validate(d);met={k:len(d[k]) for k in ['entities','aliases','relationships','claims','sources','denominators','coverage']};write_json(ROOT/'reports/egypt_validation.json',{'schema_version':'2.0.0','country_code':'EG','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e});print(met);return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
