#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_djibouti import data,validate
def main():
 b=data();o=[]
 def r(n,fn,c):d=copy.deepcopy(b);fn(d);o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in validate(d))})
 r('DJ_CITY_AS_REGION',lambda d:next(x for x in d['entities'] if x['id']=='ENT-DJ-DJIBOUTI-CITY').update(entity_type='dj_region'),'DJ_COUNTS')
 r('DJ_COMMUNE_UNDER_REGION',lambda d:next(x for x in d['relationships'] if x['child_id']=='ENT-DJ-COMMUNE-RAS-DIKA').update(parent_id='ENT-DJ-REGION-ARTA'),'DJ_COMMUNE_PATH')
 r('DJ_SUBPREF_UNDER_CITY',lambda d:next(x for x in d['relationships'] if x['child_id'].startswith('ENT-DJ-SUBPREFECTURE')).update(parent_id='ENT-DJ-DJIBOUTI-CITY'),'DJ_SUBPREFECTURE_PATH')
 r('DJ_DROP_REGION',lambda d:d['entities'].__setitem__(slice(None),[x for x in d['entities'] if x['id']!='ENT-DJ-REGION-ARTA']),'DJ_COUNTS')
 r('DJ_POP_TAMPER',lambda d:next(x for x in d['claims'] if x['subject_id']=='ENT-DJ-REGION-ARTA')['value'].update(data=1),'DJ_POPULATION')
 r('DJ_POP_TOTAL',lambda d:next(x for x in d['claims'])['value'].update(data=1),'DJ_POP_RECONCILIATION')
 r('DJ_FAKE_COMMUNE_COUNT',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-DJ-CITY-COMMUNES').update(value=6),'DJ_DENOMINATORS')
 r('DJ_FAKE_SUBPREF_COUNT',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-DJ-SUBPREFECTURES').update(value=15),'DJ_DENOMINATORS')
 ok=all(x['detected'] for x in o);write_json(ROOT/'reports/djibouti_negative_tests.json',{'schema_version':'2.0.0','country_code':'DJ','status':'PASS' if ok else 'FAIL','required':8,'detected':sum(x['detected'] for x in o),'mutations':o});print(o);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
