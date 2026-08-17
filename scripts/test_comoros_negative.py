#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_comoros import data,validate
def main():
 b=data();o=[]
 def r(n,fn,c):d=copy.deepcopy(b);fn(d);o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in validate(d))})
 r('KM_MAYOTTE_CURRENT',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-KM-ISLAND-MAYOTTE','canonical_name':'Mayotte','entity_type':'km_island'}),'KM_MAYOTTE_CURRENT')
 r('KM_PREF_WRONG_ISLAND',lambda d:next(x for x in d['relationships'] if x['child_id'].startswith('ENT-KM-PREFECTURE')).update(parent_id='ENT-KM-ISLAND-MWALI'),'KM_PREFECTURE_PARENT')
 r('KM_COMMUNE_WRONG_PREF',lambda d:next(x for x in d['relationships'] if x['child_id'].startswith('ENT-KM-COMMUNE')).update(parent_id='ENT-KM-PREFECTURE-DJANDO'),'KM_COMMUNE_PARENT')
 r('KM_58_COMMUNES',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-KM-COMMUNES').update(value=58),'KM_DENOMINATORS')
 r('KM_OLD_ZERO_WHC',lambda d:next(x for x in d['claims'] if x['predicate']=='world_heritage_inscription_year')['value'].update(data=0),'KM_WHC_2026')
 r('KM_DROP_ISLAND',lambda d:d['entities'].__setitem__(slice(None),[x for x in d['entities'] if x.get('entity_type')!='km_island']),'KM_COUNTS')
 r('KM_COMMUNE_AS_VILLAGE',lambda d:next(x for x in d['entities'] if x.get('entity_type')=='km_commune').update(entity_type='village'),'KM_COUNTS')
 r('KM_DROP_COMMUNE',lambda d:d['entities'].pop(),'KM_COUNTS')
 ok=all(x['detected'] for x in o);write_json(ROOT/'reports/comoros_negative_tests.json',{'schema_version':'2.0.0','country_code':'KM','status':'PASS' if ok else 'FAIL','required':8,'detected':sum(x['detected'] for x in o),'mutations':o});print(o);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
