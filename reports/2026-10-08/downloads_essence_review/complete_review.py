from pathlib import Path
import csv,json,collections,sqlite3,hashlib
O=Path(__file__).resolve().parent;D=Path('C:/Users/PPCCpcpc/Downloads');p=O/'audit.json';a=json.loads(p.read_text(encoding='utf-8'))
for r in a['files']:
    source=D/r['name']
    if r['name']=='ISIC_Rev_5_english_structure.csv':
        data=source.read_bytes()
        try:text=data.decode('utf-8-sig');enc='UTF8'
        except UnicodeDecodeError:text=data.decode('cp1252');enc='CP1252_DECODED_OFFICIAL_ENCODING_UNCONFIRMED'
        import io
        reader=csv.reader(io.StringIO(text,newline=''));head=next(reader);rows=list(reader);idx=next((i for i,k in enumerate(head) if 'code' in k.lower()),0)
        r.update(kind='CSV_ALL_ROWS',encoding=enc,headers=head,data_rows=len(rows),field_count_mismatch=sum(len(x)!=len(head) for x in rows),code_length_counts=dict(collections.Counter(len(x[idx]) for x in rows)),unique_codes=len({x[idx] for x in rows}));r.pop('error',None);r.pop('review',None)
    if source.suffix=='.sqlite':
        try:
            con=sqlite3.connect(source.as_uri()+'?mode=ro&immutable=1',uri=True);tables=[];integrity=con.execute('PRAGMA integrity_check').fetchone()[0]
            for (n,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'"):
                q='"'+n.replace('"','""')+'"';tables.append({'table':n,'rows':con.execute('SELECT count(*) FROM '+q).fetchone()[0],'columns':[x[1] for x in con.execute('PRAGMA table_info('+q+')')]})
            con.close();r.update(kind='READ_ONLY_IMMUTABLE_SQLITE_STRUCTURE_AND_INTEGRITY',integrity=integrity,tables=tables);r.pop('error',None);r.pop('review',None)
        except sqlite3.OperationalError as e:r['diagnostic']=str(e)
byhash={r['sha256']:r for r in a['files'] if 'error' not in r}
for r in a['files']:
    if r['name'].endswith('.rar'):
        for m in r.get('members',[]):
            if not m.get('sheets') and m['sha256'] in byhash:
                m['review']='EXACT_SHA256_DUPLICATE_OF_REVIEWED_LOCAL_FILE';m['reviewed_file']=byhash[m['sha256']]['name']
p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps([{k:r[k] for k in ['name','data_rows','code_length_counts','integrity','error','diagnostic'] if k in r} for r in a['files'] if 'error' in r or 'ISIC_Rev' in r['name'] or r['name'].endswith('.sqlite')],ensure_ascii=True))
