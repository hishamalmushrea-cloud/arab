#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p): return json.loads(p.read_text(encoding='utf8'))
def main():
 f=L(ROOT/'data/imports/yemen/fixtures/first_level_2026.json'); e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='YE']; ids={r['id'] for r in e}; families={'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='YE'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='YE']}; sids={'SRC-YE-CSO-ADMIN-DEFINITION-LEGACY','SRC-YE-NIC-GOVERNORATES-LEGACY','SRC-YE-LAW-31-SOCOTRA-REPORT-2013','SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR','SRC-YE-CENSUS-2004-LEGACY-FRAME','SRC-OSM-AMANAT-SECTIONS-2026'}; families['sources']=[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids]; E={r['id']:r for r in e}; findings=[]
 for q in f['units']:
  eid='ENT-YE-'+('CAPITAL-MUNICIPALITY' if q['kind']=='capital_municipality' else 'GOVERNORATE')+'-'+q['code']
  if E.get(eid,{}).get('canonical_name')!=q['name_ar']: findings.append({'severity':'P1','record_id':eid,'message':'fixture identity mismatch'})
 if E.get('ENT-YE-GOVERNORATE-22',{}).get('valid_from')!='2013-12-18': findings.append({'severity':'P1','record_id':'Socotra','message':'Law issuance date mismatch'})
 fd=L(ROOT/'data/imports/yemen/fixtures/districts_2026.json'); code2eid={q['code']:('ENT-YE-'+('CAPITAL-MUNICIPALITY' if q['kind']=='capital_municipality' else 'GOVERNORATE')+'-'+q['code']) for q in f['units']}
 rel_by_child={r['child_id']:r for r in families['relationships']}
 dis=[r for r in e if r['entity_type']=='ye_district']
 want={(code2eid[g['code']],n) for g in fd['governorates'] for n in g['districts']}; got={(rel_by_child.get(r['id'],{}).get('parent_id'),r['canonical_name']) for r in dis}
 if want!=got or len(dis)!=333: findings.append({'severity':'P1','record_id':'districts','message':'district universe deviates from checksum-bound 333-district fixture'})
 if any(r.get('verification_status')!='probable' for r in dis): findings.append({'severity':'P1','record_id':'districts','message':'district status must remain probable'})
 fl=L(ROOT/'data/imports/yemen/fixtures/amanat_lanes_2026.json')
 lanes=[r for r in e if r['entity_type']=='lane']; hays=[r for r in e if r['entity_type']=='neighborhood' and r.get('canonical_source_id')=='SRC-YE-NIC-AMANAT-CENSUS-2004']
 if len(lanes)!=104 or len(hays)!=3: findings.append({'severity':'P1','record_id':'lanes','message':'lane universe must equal the checksum-bound 104-lane fixture with 3 hays'})
 if any(r.get('verification_status') not in {'probable','unverified'} for r in lanes): findings.append({'severity':'P1','record_id':'lanes','message':'lane status must remain probable or unverified'})
 lpop=[c for c in families['claims'] if c.get('predicate')=='population' and c.get('subject_id') in {r['id'] for r in lanes}]
 if len(lpop)!=33 or any(c.get('published') for c in lpop): findings.append({'severity':'P1','record_id':'lane_populations','message':'33 unpublished 2004 lane population claims required'})
 cult=[c for c in families['claims'] if c.get('predicate') in {'food_dish','dialect_profile','language_presence'}]
 if len(cult)!=19 or any(c.get('published') for c in cult): findings.append({'severity':'P1','record_id':'culture','message':'19 unpublished cultural claims required'})
 dcm=[c for c in families['claims'] if c.get('predicate') in {'clothing_item','craft_custom','market_presence'}]
 if len(dcm)!=14 or any(c.get('published') or c.get('verification_status')!='local_reported' for c in dcm): findings.append({'severity':'P1','record_id':'dress_crafts_markets','message':'14 unpublished local_reported dress/craft/market claims required'})
 fu=L(ROOT/'data/imports/yemen/fixtures/amanat_urban_sections_2026.json')
 secs=[r for r in e if r.get('canonical_source_id')=='SRC-OSM-AMANAT-SECTIONS-2026']; want_sections=sum(len(t['sections']) for t in fu['districts'])
 if len(secs)!=want_sections or len(hays)!=3: findings.append({'severity':'P1','record_id':'urban_sections','message':'section universe must equal the checksum-bound fixture and leave the three cycle-1 hays untouched'})
 if any(r.get('coordinates') is not None or r.get('verification_status') not in {'probable','unverified'} for r in secs): findings.append({'severity':'P1','record_id':'urban_sections','message':'sections carry no coordinate and stay probable/unverified'})
 sec_ids={r['id'] for r in secs}
 if any(c.get('subject_id') in sec_ids for c in families['claims']): findings.append({'severity':'P1','record_id':'urban_sections','message':'no claim may attach to a named urban section in this cycle'})
 if any(rel_by_child.get(r['id'],{}).get('relationship_type')!='located_in' for r in secs): findings.append({'severity':'P1','record_id':'urban_sections','message':'every section needs a located_in relationship'})
 for o in fu['open_districts']:
  parent=next((z['district_id'] for z in fu['districts'] if z['code']==o['code']),None)
  if parent and any((rel_by_child.get(r['id']) or {}).get('parent_id')==parent for r in secs): findings.append({'severity':'P1','record_id':o['district'],'message':'open district must not carry any entity'})
  if not o.get('reason'): findings.append({'severity':'P1','record_id':o['district'],'message':'open district needs its recorded reason'})
 covs={r['id']:r for r in families['coverage']}
 for t in fu['districts']:
  cov=covs.get('COV-YE-URBAN-SECTIONS-'+t['code']); matched=len(t['sections'])
  if not cov or cov.get('matched')!=matched or cov.get('complete') or cov.get('coverage_percentage')!=round(100.0*matched/t['frame_lanes_2004'],2): findings.append({'severity':'P1','record_id':t['district'],'message':'district coverage must stay bounded and incomplete'})
 snaps={r['id']:r for r in read_jsonl(ROOT/'data/snapshots/snapshots.jsonl')}
 s2=snaps.get('SNP-YE-URBAN-SECTIONS-20260923')
 if not s2 or s2.get('captured_at')!='2026-09-23' or not s2.get('checksum'): findings.append({'severity':'P1','record_id':'urban_snapshot','message':'the dated urban-section snapshot must exist and carry its checksum'})
 if snaps.get('SNP-YE-PRODUCTION-20260817',{}).get('captured_at')!='2026-08-17': findings.append({'severity':'P1','record_id':'production_snapshot','message':'the accepted production snapshot must keep its own date'})
 if any(c.get('predicate')=='food_dish' and c['value']['data'].get('name')=='المندي' and c.get('classification')!='shared' for c in cult): findings.append({'severity':'P1','record_id':'المندي','message':'shared dish must not become exclusive'})
 sample={k:{'population':len(v),'sample_size':len(v),'sample_percentage':100.0,'record_ids':sorted(x['id'] for x in v)} for k,v in families.items()}; write_json(ROOT/'data/review/yemen_review_samples.json',{'schema_version':'2.0.0','country_code':'YE','families':sample}); write_json(ROOT/'reports/yemen_review_samples.json',{'schema_version':'2.0.0','country_code':'YE','families':sample}); n=sum(len(v) for v in families.values()); ok=not findings; result={k:{'sampled':len(v),'passed':len(v) if ok else 0,'failed':0 if ok else len(v),'status':'PASS' if ok else 'FAIL'} for k,v in families.items()}; write_json(ROOT/'reports/yemen_independent_review.json',{'schema_version':'2.0.0','country_code':'YE','status':'PASS' if ok else 'FAIL','p0':0,'critical_p1':len(findings),'method':'Independent full-population comparison against the checksum-bound 22-unit fixture, the 333-district inventory, the 104-lane Amanat inventory, the named-urban-section snapshot fixture of depth cycle 2, the 19-claim cultural frame, and the 14-claim dress/crafts/markets frame, including status enforcement (probable/unverified/local_reported), coordinate and claim absence on section places, per-district bounded coverage, dated snapshots, unpublished weak-source content, and shared-dish non-exclusivity.','families':result,'total_sampled':n,'total_passed':n if ok else 0,'findings':findings}); print(n); return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
