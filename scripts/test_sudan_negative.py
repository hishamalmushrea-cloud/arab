#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_sudan import data,validate
def main():
 b=data();o=[]
 def r(n,fn,c):d=copy.deepcopy(b);fn(d);o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in validate(d))})
 r('SD_17_CURRENT',lambda d:d['entities'].__setitem__(slice(None),[x for x in d['entities'] if x['id']!='ENT-SD-STATE-18']),'SD_COUNTS')
 r('SD_REMOVE_RECONCILIATION',lambda d:d['claims'].__setitem__(slice(None),[x for x in d['claims'] if x['predicate']!='administrative_denominator_reconciliation']),'SD_RECONCILIATION')
 r('SD_ABYEI_AS_STATE',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-SD-STATE-ABYEI','canonical_name':'أبيي'}),'SD_ABYEI_ORDINARY')
 r('SD_LEGAL_AS_DE_FACTO',lambda d:next(x for x in d['entities'] if x['id']=='ENT-SD-STATE-01').update(status='de_facto'),'SD_UNSUPPORTED_OVERLAY')
 r('SD_DISPLACED_WITHOUT_SOURCE',lambda d:next(x for x in d['entities'] if x['id']=='ENT-SD-STATE-07').update(status='displaced'),'SD_UNSUPPORTED_OVERLAY')
 r('SD_PREMATURE_LOCALITY',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-SD-LOCALITY-X','entity_type':'sd_locality'}),'SD_PREMATURE_LOWER')
 r('SD_WRONG_DENOMINATOR',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-SD-STATES').update(value=17),'SD_DENOMINATORS')
 r('SD_FAKE_LOCALITY_PERCENT',lambda d:next(x for x in d['coverage'] if x['id']=='COV-SD-LOCALITIES').update(denominator=189,coverage_percentage=1.0),'SD_UNAVAILABLE_LOWER')
 r('SD_WRONG_PARENT',lambda d:next(x for x in d['relationships'] if x['child_id']=='ENT-SD-STATE-18').update(parent_id='ENT-SD-STATE-01'),'SD_PARENT')
 ok=all(x['detected'] for x in o);write_json(ROOT/'reports/sudan_negative_tests.json',{'schema_version':'2.0.0','country_code':'SD','status':'PASS' if ok else 'FAIL','required':9,'detected':sum(x['detected'] for x in o),'mutations':o});return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
