#!/usr/bin/env python3
"""Independent Kuwait production semantics."""
import hashlib,json
from model import ROOT,read_jsonl,write_json
G={'ENT-KW-GOVERNORATE-CAPITAL':('العاصمة','Capital',574839),'ENT-KW-GOVERNORATE-HAWALLI':('حولي','Hawalli',926170),'ENT-KW-GOVERNORATE-AL-AHMADI':('الأحمدي','Al-Ahmadi',923784),'ENT-KW-GOVERNORATE-AL-JAHRA':('الجهراء','Al-Jahra',566861),'ENT-KW-GOVERNORATE-AL-FARWANIYA':('الفروانية','Al-Farwaniya',1109819),'ENT-KW-GOVERNORATE-MUBARAK-AL-KABEER':('مبارك الكبير','Mubarak Al-Kabeer',279666)}
S={'SRC-KW-CSB-CENSUS-GOVERNORATES-2021','SRC-KW-CSB-CENSUS-METHODOLOGY-2021','SRC-UNESCO-WHC-KW-2026'}
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='KW'];ids={r['id'] for r in e}
 return {'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='KW'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='KW'],'snapshots':[r for r in read_jsonl(ROOT/'data/snapshots/snapshots.jsonl') if r.get('id','').startswith('SNP-KW-')],'sources':[load(p) for p in (ROOT/'data/sources').glob('*.json') if load(p).get('id') in S],'manifest':load(ROOT/'manifests/KW.yml')}
def validate(d):
 err=[]
 def E(c,l,m):err.append({'code':c,'location':l,'message':m})
 es={r['id']:r for r in d['entities']};al={r['entity_id']:r for r in d['aliases']};rels=d['relationships'];cl=d['claims'];ss={r['id']:r for r in d['sources']};ds={r['id']:r for r in d['denominators']};cv={r['id']:r for r in d['coverage']}
 if set(es)!={'ENT-KW-COUNTRY',*G}:E('KW_ENTITY_UNIVERSE','entities','expected country plus six governorates only')
 for eid,(ar,en,pop) in G.items():
  r=es.get(eid,{})
  if r.get('entity_type')!='kw_governorate' or r.get('canonical_name')!=ar:E('KW_GOVERNORATE_IDENTITY',eid,'type/name mismatch')
  if al.get(eid,{}).get('name')!=en:E('KW_ALIAS',eid,'English alias mismatch')
  q=[x for x in rels if x.get('child_id')==eid]
  if len(q)!=1 or q[0].get('parent_id')!='ENT-KW-COUNTRY' or q[0].get('relationship_type')!='administrative_parent':E('KW_WRONG_PARENT',eid,'wrong governorate parent')
  q=[x for x in cl if x.get('subject_id')==eid and x.get('predicate')=='population']
  if len(q)!=1 or q[0].get('value',{}).get('data')!=pop or q[0].get('observed_at')!='2021-01-01' or not q[0].get('second_source_id'):E('KW_POPULATION',eid,'reconciled 2021 population mismatch/undated')
 if len(d['aliases'])!=6 or len(rels)!=6 or len(cl)!=6:E('KW_COUNTS','KW','expected 6 aliases/relationships/claims')
 for r in cl:
  if r.get('source_id') not in ss or not r.get('source_locator'):E('KW_CLAIM_SOURCE',r.get('id','?'),'unaccepted source/locator')
  if r.get('predicate','').startswith('lexical_'):E('KW_UNSUPPORTED_DIALECT',r['id'],'no corpus accepted')
  if r.get('predicate')!='population':E('KW_CULTURAL_LEAKAGE',r['id'],'unsupported claim on governorate')
 if set(ss)!=S or any(x.get('quality_tier')!='A' for x in ss.values()):E('KW_SOURCES','sources','expected exact three A-tier sources')
 if {k:v.get('value') for k,v in ds.items()}!={'DEN-KW-COUNTRY-SCOPE':1,'DEN-KW-GOVERNORATES-2021':6,'DEN-KW-WHC-20260816':0}:E('KW_DENOMINATORS','denominators','expected 1/6/0')
 for cid,n in {'COV-KW-COUNTRY-SCOPE':1,'COV-KW-GOVERNORATES-2021':6,'COV-KW-WHC-20260816':0}.items():
  r=cv.get(cid,{})
  if r.get('matched')!=n or r.get('denominator')!=n or not r.get('complete') or r.get('coverage_percentage')!=100.0:E('KW_COVERAGE',cid,'coverage mismatch')
 m=d['manifest'];gl=next((r for r in m.get('hierarchy',[]) if r.get('entity_type')=='kw_governorate'),{})
 if gl.get('scope_status')!='closed' or gl.get('denominator')!=6:E('KW_MANIFEST','KW','governorates not closed')
 for t in ['kw_area','kw_block']:
  l=next((r for r in m.get('hierarchy',[]) if r.get('entity_type')==t),{})
  if l.get('scope_status')!='unavailable' or l.get('denominator') is not None:E('KW_FAKE_LOWER_LAYER',t,'lower denominator invented')
 if len(d['snapshots'])!=1 or d['snapshots'][0].get('checksum')!='sha256:'+hashlib.sha256((ROOT/'data/imports/kuwait/snapshot_manifest.json').read_bytes()).hexdigest():E('KW_SNAPSHOT','snapshot','checksum mismatch')
 return err
def main():
 d=data();e=validate(d);m={'entities':len(d['entities']),'new_entities':len(d['entities'])-1,'aliases':len(d['aliases']),'relationships':len(d['relationships']),'claims':len(d['claims']),'sources':len(d['sources']),'denominators':len(d['denominators']),'coverage_records':len(d['coverage']),'ab_claims':sum(r.get('source_id') in S for r in d['claims']),'dialect_claims':sum(r.get('predicate','').startswith('lexical_') for r in d['claims'])};write_json(ROOT/'reports/kuwait_validation.json',{'schema_version':'2.0.0','country_code':'KW','snapshot_date':'2026-08-16','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':m,'errors':e});print(json.dumps(m,sort_keys=True));print('Kuwait production semantic validation '+('passed.' if not e else 'failed.'));return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
