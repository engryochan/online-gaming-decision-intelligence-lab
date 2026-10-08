#!/usr/bin/env python3
"""Global registry offline ingestion v1.4.0. No network calls. Stdlib only.
Usage:
 python global_registry_ingest_v1_4_0.py verify --country global_country_registry_v1_3_0.csv
 python global_registry_ingest_v1_4_0.py isic --input ISIC_Rev_5_english_structure.csv --outdir output
 python global_registry_ingest_v1_4_0.py lei --input LEI-JSON-file.json --outdir output
All ingested records retain source attribution, never claim global completeness.
"""
import argparse,csv,hashlib,json,re,sys,datetime
from pathlib import Path

def digest(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def read_csv(path):
 with open(path,'r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def emit(path,heads,rows):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=heads,extrasaction='ignore');w.writeheader();w.writerows(rows)
def country_verify(path):
 rows=read_csv(path)
 codes=[r['iso_alpha2'] for r in rows]
 assert len(rows)==249,f'expected 249 found {len(rows)}'
 assert len(codes)==len(set(codes)),'duplicate iso_alpha2'
 assert all(re.fullmatch(r'[A-Z]{2}',s) for s in codes),'invalid iso_alpha2'
 assert all(re.fullmatch(r'\d{3}',r['iso_numeric']) for r in rows),'invalid numeric code'
 return {'countries':len(rows),'distinct_iso_alpha2':len(set(codes)),'source_sha256':digest(path)}
def isic_import(src,outdir):
 rows=read_csv(src)
 if not rows:raise ValueError('empty official file')
 cols=list(rows[0]); low={c.lower().strip():c for c in cols}
 # UNSD structure typically Section, Division, Group, Class, Description columns
 def pick(names):
  for n in names:
   for k,c in low.items():
    if k==n or k.replace(' ','_')==n:return c
  return None
 section=pick(['section']); div=pick(['division']); group=pick(['group']); clas=pick(['class']); title=pick(['description','title','label','name','activity'])
 if not all([section,div,group,clas,title]):
  raise ValueError('Official CSV schema unrecognized: '+','.join(cols)+'; manual mapping required, ingestion BLOCKED')
 output=[]; seen=set(); rejected=[]
 for n,r in enumerate(rows,2):
  vals=[(r.get(k) or '').strip() for k in (section,div,group,clas)]
  levels=[('section',vals[0]),('division',vals[1]),('group',vals[2]),('class',vals[3])]
  nonempty=[(level,v) for level,v in levels if v]
  if not nonempty:continue
  level,code=nonempty[-1]
  fmt={'section':r'[A-Z]', 'division':r'\d{2}', 'group':r'\d{3}', 'class':r'\d{4}'}
  if not re.fullmatch(fmt[level],code):rejected.append((n,'bad_code',code));continue
  key=(level,code)
  if key in seen:rejected.append((n,'duplicate',code));continue
  seen.add(key)
  parent={'section':'','division':vals[0],'group':vals[1],'class':vals[2]}[level]
  output.append({'classification':'ISIC','release':'Rev.5','level':level,'code':code,'parent_code':parent,'official_english_title':(r.get(title) or '').strip(),'source_url':'https://unstats.un.org/unsd/classifications/Econ/isic','source_file_sha256':digest(src),'verification_status':'OFFICIAL_FILE_IMPORTED_UNVERIFIED_RELEASE'})
 # Closure: reject orphaned nodes; some country classification schemas encode implied parents differently, so fail closed.
 existing={(r['level'],r['code']) for r in output}
 for r in output:
  if r['level']=='section':continue
  expected={'division':'section','group':'division','class':'group'}[r['level']]
  if (expected,r['parent_code']) not in existing:rejected.append((0,'parent_missing',r['code']+'->'+r['parent_code']))
 status='PASS' if not rejected and output else 'BLOCKED'
 report={'status':status,'source_sha256':digest(src),'extracted':len(output),'errors':rejected[:100],'error_count':len(rejected),'note':'Review input source authenticity and official errata before promoting to verified status.'}
 p=Path(outdir);p.mkdir(parents=True,exist_ok=True)
 emit(p/'isic_rev5_import.csv',list(output[0]) if output else ['classification'],output)
 (p/'isic_import_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 if status!='PASS':raise ValueError('ISIC import BLOCKED: '+str(report)[:400])
 return report

def lei_import(src,outdir):
 """Supports GLEIF API JSON:API responses with data:[{type,id,attributes,relationships}].
 Does not claim to parse full GLEIF CDF XML, which needs a separate schema-specific adapter.
 """
 obj=json.loads(Path(src).read_text(encoding='utf-8-sig'))
 records=obj.get('data',[]) if isinstance(obj,dict) else obj
 if not isinstance(records,list):raise ValueError('expected JSON:API data array')
 rows=[];errors=[];seen=set()
 for i,x in enumerate(records):
  a=x.get('attributes') or {}; lei=x.get('id','')
  if not re.fullmatch(r'[A-Z0-9]{20}',lei):errors.append((i,'invalid_lei'));continue
  if lei in seen:errors.append((i,'duplicate_lei'));continue
  seen.add(lei)
  entity=a.get('entity') or {}; legal=entity.get('legalName') or {}; reg=entity.get('registeredAt') or {}; regaddr=entity.get('legalAddress') or {}
  if isinstance(legal,str):legal={'name':legal}
  country=regaddr.get('country') or ''
  rows.append({'lei':lei,'legal_name':legal.get('name',''),'legal_name_language':legal.get('language',''),'legal_address_country':country,'legal_jurisdiction':entity.get('legalJurisdiction',''),'entity_status':entity.get('status',''),'registration_authority_id':reg.get('id','') if isinstance(reg,dict) else '','source_file_sha256':digest(src),'source_type':'GLEIF_API_JSONAPI','evidence_grade':'SOURCE_RECORD_UNVERIFIED','retrieved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')})
 p=Path(outdir);p.mkdir(parents=True,exist_ok=True)
 heads=['lei','legal_name','legal_name_language','legal_address_country','legal_jurisdiction','entity_status','registration_authority_id','source_file_sha256','source_type','evidence_grade','retrieved_at_utc']
 emit(p/'gleif_lei_import.csv',heads,rows)
 report={'status':'PASS' if not errors else 'REVIEW_REQUIRED','records':len(rows),'rejected':len(errors),'rejections':errors[:50],'source_sha256':digest(src),'note':'GLEIF API JSON only; all fields need appropriate license, dates, and secondary registry crosschecks.'}
 (p/'gleif_lei_import_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 return report

def main():
 ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest='action',required=True)
 p=sub.add_parser('verify');p.add_argument('--country',required=True)
 for name in ['isic','lei']:
  p=sub.add_parser(name);p.add_argument('--input',required=True);p.add_argument('--outdir',required=True)
 a=ap.parse_args()
 try:
  r=country_verify(a.country) if a.action=='verify' else isic_import(a.input,a.outdir) if a.action=='isic' else lei_import(a.input,a.outdir)
  print(json.dumps(r,ensure_ascii=False,indent=2))
 except Exception as e:print('BLOCKED:',str(e),file=sys.stderr);sys.exit(2)
if __name__=='__main__': main()
