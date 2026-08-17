#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_syria import data,validate
def main():
 b=data();o=[]
 def r(n,fn,c):d=copy.deepcopy(b);fn(d);o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in validate(d))})
 r('SY_REMOVE_GOVERNORATE',lambda d:d['entities'].__setitem__(slice(None),[x for x in d['entities'] if x['id']!='ENT-SY-GOVERNORATE-14']),'SY_COUNTS')
 r('SY_MERGE_DAMASCUS_RURAL',lambda d:next(x for x in d['entities'] if x['id']=='ENT-SY-GOVERNORATE-06').update(canonical_name='دمشق'),'SY_DAMASCUS_DISTINCTION')
 r('SY_DAMASCUS_ORDINARY_PROFILE',lambda d:next(x for x in d['claims'] if x['subject_id']=='ENT-SY-GOVERNORATE-01')['value'].update(data='ordinary_governorate'),'SY_FIXTURE_PROFILE')
 r('SY_LEGAL_AS_DE_FACTO',lambda d:next(x for x in d['entities'] if x['id']=='ENT-SY-GOVERNORATE-02').update(status='de_facto'),'SY_UNSUPPORTED_OVERLAY')
 r('SY_DESTROYED_WITHOUT_SOURCE',lambda d:next(x for x in d['entities'] if x['id']=='ENT-SY-GOVERNORATE-04').update(status='destroyed'),'SY_UNSUPPORTED_OVERLAY')
 r('SY_PREMATURE_DISTRICT',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-SY-DISTRICT-X','entity_type':'sy_district'}),'SY_PREMATURE_LOWER')
 r('SY_WRONG_DISTRICT_DENOMINATOR',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-SY-DISTRICTS').update(value=60),'SY_DENOMINATORS')
 r('SY_FAKE_LOWER_COMPLETION',lambda d:next(x for x in d['coverage'] if x['id']=='COV-SY-DISTRICTS').update(matched=68,unmatched=0,missing=0,complete=True),'SY_OPEN_LOWER')
 r('SY_WRONG_PARENT',lambda d:next(x for x in d['relationships'] if x['child_id']=='ENT-SY-GOVERNORATE-14').update(parent_id='ENT-SY-GOVERNORATE-02'),'SY_PARENT')
 r('SY_STALE_COVERAGE',lambda d:next(x for x in d['coverage'] if x['id']=='COV-SY-GOVERNORATES').update(snapshot_date='2010-01-01'),'SY_COVERAGE_FRESHNESS')
 ok=all(x['detected'] for x in o);write_json(ROOT/'reports/syria_negative_tests.json',{'schema_version':'2.0.0','country_code':'SY','status':'PASS' if ok else 'FAIL','required':len(o),'detected':sum(x['detected'] for x in o),'mutations':o});print(o);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
