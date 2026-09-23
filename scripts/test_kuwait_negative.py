#!/usr/bin/env python3
"""Required Kuwait negative mutations: base layer plus depth cycle 1."""
import copy
from model import ROOT,write_json
from validate_kuwait import data,validate
def firij(d): return next(r for r in d['entities'] if r['entity_type']=='quarter')
def dish(d,name):
 for r in d['claims']:
  if r.get('predicate')=='food_dish' and r['value']['data'].get('name')==name: return r
 raise SystemExit('missing fixture dish '+name)
def main():
 b=data();out=[]
 def run(n,fn,code):
  d=copy.deepcopy(b);fn(d);e=validate(d);out.append({'mutation':n,'expected_code':code,'detected':any(x['code']==code for x in e)})
 run('KW_WRONG_PARENT',lambda d:next(r for r in d['relationships'] if r['child_id']=='ENT-KW-GOVERNORATE-CAPITAL').update(parent_id='ENT-KW-GOVERNORATE-HAWALLI'),'KW_WRONG_PARENT')
 run('KW_AREA_AS_GOVERNORATE',lambda d:next(r for r in d['entities'] if r['id']=='ENT-KW-GOVERNORATE-CAPITAL').update(entity_type='kw_area'),'KW_GOVERNORATE_IDENTITY')
 run('KW_BLOCK_AS_MUNICIPALITY',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-KW-BLOCK-1','entity_type':'kw_block'}),'KW_ENTITY_UNIVERSE')
 run('KW_FOREIGN_SOURCE',lambda d:next(r for r in d['claims'] if r['predicate']=='population').update(source_id='SRC-BH-SLRB-GOVERNORATE-AREA-2024'),'KW_CLAIM_SOURCE')
 run('KW_POPULATION_TAMPER',lambda d:next(r for r in d['claims'] if r['subject_id']=='ENT-KW-GOVERNORATE-CAPITAL')['value'].update(data=1),'KW_POPULATION')
 run('KW_UNDATED_CENSUS',lambda d:next(r for r in d['claims'] if r['predicate']=='population').update(observed_at=None),'KW_POPULATION')
 run('KW_TENTATIVE_AS_INSCRIBED',lambda d:next(r for r in d['denominators'] if r['id']=='DEN-KW-WHC-20260816').update(value=6,denominator=6),'KW_DENOMINATORS')
 run('KW_CULTURAL_LEAKAGE',lambda d:d['claims'].append({**dish(d,'مجبوس'),'id':'CLM-KW-MUT-LEAK','subject_id':'ENT-KW-GOVERNORATE-CAPITAL','classification':None,'source_id':next(r['id'] for r in d['sources'] if r['quality_tier']=='E')}),'KW_DEPTH_CONTRACT')
 run('KW_ALIAS_AS_ENTITY',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-KW-CITY-ALIAS'}),'KW_ENTITY_UNIVERSE')
 run('KW_SHARED_NOT_EXCLUSIVE',lambda d:dish(d,'مجبوس').update(classification='national'),'KW_SHARED_NOT_EXCLUSIVE')
 run('KW_DEPTH_PUBLISHED_FROM_WEAK',lambda d:dish(d,'قبوط').update(published=True),'KW_DEPTH_PUBLISHED_FROM_WEAK')
 run('KW_DIALECT_PROMOTED',lambda d:next(r for r in d['claims'] if r['predicate']=='dialect_profile').update(verification_status='verified'),'KW_DEPTH_CONTRACT')
 run('KW_FIRIJ_AS_CURRENT',lambda d:firij(d).update(status='current'),'KW_QUARTER_HISTORICAL')
 run('KW_FIRIJ_ADMIN_PARENT',lambda d:d['relationships'].append({**d['relationships'][-1],'id':'REL-KW-MUT-PARENT','child_id':firij(d)['id'],'parent_id':'ENT-KW-GOVERNORATE-CAPITAL','relationship_type':'administrative_parent'}),'KW_QUARTER_PARENT')
 run('KW_ICH_UNPUBLISHED',lambda d:next(r for r in d['claims'] if r.get('source_id')=='SRC-KW-UNESCO-ICH-2026').update(published=False),'KW_ICH_CONTRACT')
 run('KW_QUARTER_POPULATION',lambda d:d['claims'].append({**d['claims'][0],'id':'CLM-KW-MUT-POP','subject_id':firij(d)['id']}),'KW_QUARTER_POPULATION')
 ok=all(x['detected'] for x in out);write_json(ROOT/'reports/kuwait_negative_tests.json',{'schema_version':'2.0.0','country_code':'KW','status':'PASS' if ok else 'FAIL','required':len(out),'detected':sum(x['detected'] for x in out),'mutations':out});[print(f"[{'PASS' if x['detected'] else 'FAIL'}] {x['mutation']}") for x in out];return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
