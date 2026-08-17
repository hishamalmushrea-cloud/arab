#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_libya import data,validate
def main():
 b=data();o=[]
 def r(n,fn,c):d=copy.deepcopy(b);fn(d);o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in validate(d))})
 r('LY_93_AS_COMPLETE',lambda d:d['entities'].__setitem__(slice(None),[x for x in d['entities'] if x.get('entity_type')!='ly_municipality']+[x for x in d['entities'] if x.get('entity_type')=='ly_municipality'][:93]),'LY_COUNTS')
 r('LY_SHABIYA_CURRENT',lambda d:next(x for x in d['entities'] if x['entity_type']=='ly_shabiya_historical').update(status='current'),'LY_HISTORICAL_SEMANTICS')
 r('LY_SHABIYA_PARENT_MUNICIPALITY',lambda d:next(x for x in d['relationships'] if 'SHABIYA' in x['child_id']).update(parent_id=next(x['id'] for x in d['entities'] if x['entity_type']=='ly_municipality')),'LY_PARENT')
 r('LY_DENOM_143_LABEL',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-LY-CURRENT-MUNICIPALITIES').update(value=143),'LY_DENOMINATORS')
 r('LY_EFFECTIVE_CONTROL_INFERENCE',lambda d:next(x for x in d['entities'] if x['entity_type']=='ly_municipality').update(status='de_facto'),'LY_CURRENT_SEMANTICS')
 r('LY_FAKE_MAHALLA',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-LY-MAHALLA-X','entity_type':'ly_mahalla'}),'LY_PREMATURE_MAHALLA')
 r('LY_COVERAGE_93',lambda d:next(x for x in d['coverage'] if x['id']=='COV-LY-CURRENT-MUNICIPALITIES').update(matched=93),'LY_CURRENT_COVERAGE')
 r('LY_SOURCE_CHECKSUM',lambda d:next(x for x in d['sources'] if x['id']=='SRC-LY-MOLG-MUNICIPALITIES-2026').update(checksum='sha256:bad'),'LY_SOURCE_FRESHNESS')
 ok=all(x['detected'] for x in o);write_json(ROOT/'reports/libya_negative_tests.json',{'schema_version':'2.0.0','country_code':'LY','status':'PASS' if ok else 'FAIL','required':8,'detected':sum(x['detected'] for x in o),'mutations':o});print(o);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
