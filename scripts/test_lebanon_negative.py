#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_lebanon import data,validate
def main():
 b=data();o=[]
 def r(n,fn,c):d=copy.deepcopy(b);fn(d);o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in validate(d))})
 r('LB_EIGHT_AS_CURRENT',lambda d:next(x for x in d['claims'] if x['predicate']=='current_governorate_count')['value'].update(data=8),'LB_TEMPORAL_COUNTS')
 r('LB_KESERWAN_OLD_PARENT',lambda d:next(x for x in d['relationships'] if x['child_id']=='ENT-LB-DISTRICT-KESERWAN').update(parent_id='ENT-LB-GOVERNORATE-MOUNT-LEBANON'),'LB_CURRENT_PARENT')
 r('LB_JBEIL_OLD_PARENT',lambda d:next(x for x in d['relationships'] if x['child_id']=='ENT-LB-DISTRICT-JBEIL').update(parent_id='ENT-LB-GOVERNORATE-MOUNT-LEBANON'),'LB_CURRENT_PARENT')
 r('LB_TWO_PARENTS',lambda d:d['relationships'].append({**next(x for x in d['relationships'] if x['child_id']=='ENT-LB-DISTRICT-JBEIL'),'id':'REL-LB-MUT','parent_id':'ENT-LB-GOVERNORATE-MOUNT-LEBANON'}),'LB_CURRENT_PARENT')
 r('LB_DROP_HISTORICAL_CLAIM',lambda d:d['claims'].__setitem__(slice(None),[x for x in d['claims'] if not(x['subject_id']=='ENT-LB-DISTRICT-JBEIL' and x['predicate']=='previous_governorate')]),'LB_HISTORICAL_PARENT')
 r('LB_DENOM_8_CURRENT',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-LB-GOVERNORATES-CURRENT').update(value=8),'LB_DENOMINATORS')
 r('LB_PREMATURE_MUNICIPALITY',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-LB-MUNICIPALITY-X','entity_type':'lb_municipality'}),'LB_PREMATURE_MUNICIPALITY')
 r('LB_WRONG_DISTRICT_SET',lambda d:d['relationships'].pop(),'LB_PARENT_SET')
 ok=all(x['detected'] for x in o);write_json(ROOT/'reports/lebanon_negative_tests.json',{'schema_version':'2.0.0','country_code':'LB','status':'PASS' if ok else 'FAIL','required':8,'detected':sum(x['detected'] for x in o),'mutations':o});print(o);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
