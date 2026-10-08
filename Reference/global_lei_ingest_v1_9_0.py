#!/usr/bin/env python3
"""Offline GLEIF JSON:API ingest. Never retrieves network data. Stdlib-only."""
import argparse,csv,hashlib,json,sqlite3,datetime,pathlib,re,sys,uuid
LEI_RE=re.compile(r'^[A-Z0-9]{20}$')
SCHEMA='''
CREATE TABLE IF NOT EXISTS gleif_lei_record(
 lei TEXT PRIMARY KEY, entity_name TEXT NOT NULL, country_code TEXT NOT NULL REFERENCES country(iso_alpha2),
 entity_status TEXT, registration_status TEXT, legal_form_id TEXT, source_id TEXT NOT NULL,
 imported_at TEXT NOT NULL, file_sha256 TEXT NOT NULL, raw_record_json TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS gleif_import_batch(batch_id TEXT PRIMARY KEY, file_sha256 TEXT NOT NULL, source_url TEXT NOT NULL,
 collected_at TEXT NOT NULL, imported_at TEXT NOT NULL, read_count INTEGER NOT NULL, accepted_count INTEGER NOT NULL,
 rejected_count INTEGER NOT NULL, rejected_file TEXT NOT NULL);
'''
def records(data):
 if isinstance(data,list): return data
 if isinstance(data,dict):
  if isinstance(data.get('data'),list): return data['data']
  if isinstance(data.get('data'),dict): return [data['data']]
  if isinstance(data.get('records'),list): return data['records']
 raise ValueError('Expected GLEIF JSON:API data object/array or records array')
def run(inp,db,source_url,collected_at,rejects):
 raw=pathlib.Path(inp).read_bytes(); sha=hashlib.sha256(raw).hexdigest(); payload=json.loads(raw)
 vals=records(payload); now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 conn=sqlite3.connect(db);conn.execute('PRAGMA foreign_keys=ON');conn.executescript(SCHEMA)
 countries={x[0] for x in conn.execute('SELECT iso_alpha2 FROM country')}
 ok=0; errors=[];seen=set(); batch='sha256:'+sha
 with conn:
  if conn.execute('SELECT 1 FROM gleif_import_batch WHERE batch_id=?',(batch,)).fetchone():
   print(json.dumps({'status':'DUPLICATE_SKIPPED','sha256':sha},ensure_ascii=False));return
  for ix,obj in enumerate(vals):
   try:
    if not isinstance(obj,dict):raise ValueError('NOT_OBJECT')
    attr=obj.get('attributes') or {}
    ent=attr.get('entity') or {}
    lei=(obj.get('id') or attr.get('lei') or '').upper()
    name=ent.get('legalName') or {}
    if isinstance(name,dict):name=name.get('name') or ''
    reg=ent.get('legalAddress') or ent.get('headquartersAddress') or {}
    country=(reg.get('country') or '').upper()
    if not LEI_RE.fullmatch(lei):raise ValueError('INVALID_LEI_FORMAT')
    if not isinstance(name,str) or not name.strip():raise ValueError('MISSING_LEGAL_NAME')
    if country not in countries:raise ValueError('COUNTRY_NOT_IN_ISO_BASELINE')
    if lei in seen:raise ValueError('DUPLICATE_LEI_IN_BATCH')
    seen.add(lei)
    status=ent.get('status');rs=(attr.get('registration') or {}).get('status')
    form=ent.get('legalForm') or {}; legal_form=form.get('id') if isinstance(form,dict) else None
    conn.execute('INSERT INTO gleif_lei_record VALUES(?,?,?,?,?,?,?,?,?,?) ON CONFLICT(lei) DO UPDATE SET entity_name=excluded.entity_name,country_code=excluded.country_code,entity_status=excluded.entity_status,registration_status=excluded.registration_status,legal_form_id=excluded.legal_form_id,source_id=excluded.source_id,imported_at=excluded.imported_at,file_sha256=excluded.file_sha256,raw_record_json=excluded.raw_record_json',
      (lei,name.strip(),country,status,rs,legal_form,'GLEIF_PUBLIC_API',now,sha,json.dumps(obj,ensure_ascii=False)))
    ok+=1
   except Exception as e:errors.append({'index':ix,'reason':str(e),'record_id':obj.get('id') if isinstance(obj,dict) else None})
  with open(rejects,'w',encoding='utf-8',newline='') as f:
   writer=csv.DictWriter(f,fieldnames=['index','reason','record_id']);writer.writeheader();writer.writerows(errors)
  conn.execute('INSERT INTO gleif_import_batch VALUES(?,?,?,?,?,?,?,?,?)',(batch,sha,source_url,collected_at,now,len(vals),ok,len(errors),str(rejects)))
 print(json.dumps({'status':'IMPORTED','read':len(vals),'accepted':ok,'rejected':len(errors),'sha256':sha,'foreign_key_violations':len(conn.execute('PRAGMA foreign_key_check').fetchall())},ensure_ascii=False))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--db',required=True);ap.add_argument('--source-url',required=True);ap.add_argument('--collected-at',required=True);ap.add_argument('--rejects',required=True);a=ap.parse_args()
 run(a.input,a.db,a.source_url,a.collected_at,a.rejects)
