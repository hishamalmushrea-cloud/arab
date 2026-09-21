#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_egypt import data,validate
def main():
 b=data();o=[]
 def r(n,fn,c):d=copy.deepcopy(b);fn(d);o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in validate(d))})
 r('EG_CITY_AS_GOVERNORATE',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-EG-GOVERNORATE-CITY-X'}),'EG_COUNTS')
 r('EG_WRONG_PROFILE',lambda d:next(x for x in d['claims'] if x['subject_id']=='ENT-EG-GOVERNORATE-01')['value'].update(data='mixed_urban_rural'),'EG_PROFILE')
 r('EG_WRONG_PARENT',lambda d:next(x for x in d['relationships']).update(parent_id='ENT-EG-GOVERNORATE-01'),'EG_PARENT')
 r('EG_DENOM_28',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-EG-GOVERNORATES').update(value=28),'EG_DENOMINATORS')
 r('EG_FABRICATED_MARKAZ',lambda d:d['entities'].append({**next(x for x in d['entities'] if x['entity_type']=='eg_markaz'),'id':'ENT-EG-MARKAZ-X','canonical_name':'مركز مختلق'}),'EG_COUNTS')
 r('EG_MARKAZ_PROMOTED_TO_VERIFIED',lambda d:next(x for x in d['entities'] if x['entity_type']=='eg_markaz').update(verification_status='verified'),'EG_MARKAZ_STATUS')
 r('EG_MARKAZ_POP_PUBLISHED',lambda d:next(x for x in d['claims'] if x.get('predicate')=='population').update(published=True),'EG_MARKAZ_POP')
 r('EG_MARKAZ_WRONG_GOVERNORATE',lambda d:next(x for x in d['relationships'] if x['child_id'].startswith('ENT-EG-MARKAZ')).update(parent_id='ENT-EG-GOVERNORATE-01'),'EG_MARKAZ_FIXTURE')
 r('EG_SHIYAKHA_UNDER_MARKAZ',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-EG-SHIYAKHA-X','entity_type':'eg_shiyakha'}),'EG_PREMATURE_LOWER')
 r('EG_CLOSE_QISM_WITHOUT_DENOM',lambda d:next(x for x in d['manifest']['hierarchy'] if x['entity_type']=='eg_qism').update(scope_status='closed'),'EG_LOWER_SCOPE')
 r('EG_ALIAS_MISMATCH',lambda d:next(x for x in d['aliases']).update(name='wrong'),'EG_ALIAS')
 ok=all(x['detected'] for x in o);write_json(ROOT/'reports/egypt_negative_tests.json',{'schema_version':'2.0.0','country_code':'EG','status':'PASS' if ok else 'FAIL','required':11,'detected':sum(x['detected'] for x in o),'mutations':o});print(o);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
