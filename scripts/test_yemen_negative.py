#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_yemen import data,validate
def main():
 b=data(); o=[]
 def r(n,fn,c):
  d=copy.deepcopy(b); fn(d); o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in validate(d))})
 r('YE_AMANAT_AS_GOVERNORATE_ALIAS',lambda d:d['aliases'].append({'entity_id':'ENT-YE-CAPITAL-MUNICIPALITY-01','name':'محافظة أمانة العاصمة'}),'YE_AMANAT_ALIAS')
 r('YE_SOCOTRA_REMOVED_FROM_CURRENT',lambda d:d['entities'].__setitem__(slice(None),[x for x in d['entities'] if x['id']!='ENT-YE-GOVERNORATE-22']),'YE_COUNTS')
 r('YE_LEGACY_DENOMINATOR_AS_CURRENT',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-YE-FIRST-LEVEL').update(value=21),'YE_DENOMINATORS')
 r('YE_LEGAL_LIST_AS_DE_FACTO',lambda d:next(x for x in d['entities'] if x['id']=='ENT-YE-GOVERNORATE-03').update(status='de_facto'),'YE_UNSUPPORTED_OVERLAY')
 r('YE_DESTROYED_WITHOUT_DATED_SOURCE',lambda d:next(x for x in d['entities'] if x['id']=='ENT-YE-GOVERNORATE-05').update(status='destroyed'),'YE_UNSUPPORTED_OVERLAY')
 r('YE_PREMATURE_DISTRICT',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-YE-DISTRICT-X','entity_type':'ye_district'}),'YE_PREMATURE_LOWER')
 r('YE_WRONG_PARENT',lambda d:next(x for x in d['relationships'] if x['child_id']=='ENT-YE-GOVERNORATE-22').update(parent_id='ENT-YE-GOVERNORATE-04'),'YE_PARENT')
 r('YE_STALE_COVERAGE',lambda d:next(x for x in d['coverage'] if x['id']=='COV-YE-FIRST-LEVEL').update(snapshot_date='2013-12-18'),'YE_COVERAGE_FRESHNESS')
 r('YE_EFFECTIVE_CLAUSE_FABRICATED',lambda d:next(x for x in d['claims'] if x.get('predicate')=='establishment_instrument')['value']['data'].update(effective_clause_verified=True),'YE_SOCOTRA_LAW')
 ok=all(x['detected'] for x in o); write_json(ROOT/'reports/yemen_negative_tests.json',{'schema_version':'2.0.0','country_code':'YE','status':'PASS' if ok else 'FAIL','required':len(o),'detected':sum(x['detected'] for x in o),'mutations':o}); print(o); return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
