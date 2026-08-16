#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_kuwait import data,validate
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
 run('KW_CULTURAL_LEAKAGE',lambda d:d['claims'].append({**d['claims'][-1],'id':'CLM-KW-MUT','predicate':'traditional_food'}),'KW_CULTURAL_LEAKAGE')
 run('KW_ALIAS_AS_ENTITY',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-KW-CITY-ALIAS'}),'KW_ENTITY_UNIVERSE')
 ok=all(x['detected'] for x in out);write_json(ROOT/'reports/kuwait_negative_tests.json',{'schema_version':'2.0.0','country_code':'KW','status':'PASS' if ok else 'FAIL','required':9,'detected':sum(x['detected'] for x in out),'mutations':out});[print(f"[{'PASS' if x['detected'] else 'FAIL'}] {x['mutation']}") for x in out];return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
