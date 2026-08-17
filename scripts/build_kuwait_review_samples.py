#!/usr/bin/env python3
from model import ROOT,write_json
from validate_kuwait import data
def main():
 d=data();f={}
 for k in ['entities','aliases','relationships','claims','sources','denominators','coverage']:
  ids=sorted(r['id'] for r in d[k]);f[k]={'population':len(ids),'sample_size':len(ids),'sample_percentage':100.0,'record_ids':ids}
 x={'schema_version':'2.0.0','country_code':'KW','snapshot_date':'2026-08-16','selection_method':'Full review of small Kuwait production population; stable sorted IDs.','families':f};write_json(ROOT/'data/review/kuwait_review_samples.json',x);write_json(ROOT/'reports/kuwait_review_samples.json',x);print('Kuwait full review sample',sum(v['sample_size'] for v in f.values()))
if __name__=='__main__':main()
