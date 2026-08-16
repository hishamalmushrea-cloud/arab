#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_qatar import data,validate
def main():
 b=data();o=[]
 def r(n,fn,c):d=copy.deepcopy(b);fn(d);e=validate(d);o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in e)})
 r('QA_WRONG_PARENT',lambda d:next(x for x in d['relationships'] if x['child_id'].startswith('ENT-QA-MUNICIPALITY')).update(parent_id='ENT-QA-MUNICIPALITY-DOHA'),'QA_WRONG_PARENT')
 r('QA_ZONE_AS_MUNICIPALITY',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-QA-MUNICIPALITY-ZONE-1','entity_type':'qa_municipality'}),'QA_ENTITY_UNIVERSE')
 r('QA_HISTORICAL_TEN_CURRENT',lambda d:d['entities'].extend([{**d['entities'][-1],'id':'ENT-QA-MUNICIPALITY-OLD-A'},{**d['entities'][-1],'id':'ENT-QA-MUNICIPALITY-OLD-B'}]),'QA_ENTITY_UNIVERSE')
 r('QA_POPULATION_TAMPER',lambda d:next(x for x in d['claims'] if x['predicate']=='population')['value'].update(data=1),'QA_POPULATION')
 r('QA_UNDATED',lambda d:next(x for x in d['claims'] if x['predicate']=='population').update(observed_at=None),'QA_POPULATION')
 r('QA_CITY_LEAKAGE',lambda d:d['claims'].append({**d['claims'][-1],'id':'CLM-QA-MUT','subject_id':'ENT-QA-MUNICIPALITY-DOHA','predicate':'city_status'}),'QA_CITY_LEAKAGE')
 r('QA_DIALECT',lambda d:d['claims'].append({**d['claims'][-1],'id':'CLM-QA-DIA','predicate':'lexical_form'}),'QA_DIALECT')
 r('QA_LOWER_DENOMINATOR',lambda d:next(x for x in d['manifest']['hierarchy'] if x['entity_type']=='qa_zone').update(denominator=98,scope_status='closed'),'QA_LOWER_LAYER')
 ok=all(x['detected'] for x in o);write_json(ROOT/'reports/qatar_negative_tests.json',{'schema_version':'2.0.0','country_code':'QA','status':'PASS' if ok else 'FAIL','required':8,'detected':sum(x['detected'] for x in o),'mutations':o});print(o);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
