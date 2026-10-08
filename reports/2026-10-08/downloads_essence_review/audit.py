from pathlib import Path
import csv,json,hashlib,zipfile,io,sqlite3,subprocess,collections,re,time
import openpyxl
O=Path(__file__).resolve().parent;R=O.parents[2];D=Path('C:/Users/PPCCpcpc/Downloads')
assert not (O/'audit.json').exists(),'Preserve completed audit'
baseline={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'status':subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),'protected':{}}
for p in ['Reference/Aerospace_Ecosystem_Report.qmd','Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']:
    baseline['protected'][p]=hashlib.sha256((R/p).read_bytes()).hexdigest()
(O/'baseline.json').write_text(json.dumps(baseline,indent=2)+'\n',encoding='utf-8')
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
    return h.hexdigest()
def workbook(data):
    wb=openpyxl.load_workbook(io.BytesIO(data),read_only=True,data_only=False);out=[]
    for s in wb:
        rows=nonempty=formulas=0;headers=[]
        for cells in s.iter_rows(values_only=True):
            rows+=1;nonempty+=any(v is not None for v in cells);formulas+=sum(isinstance(v,str) and v.startswith('=') for v in cells)
            if len(headers)<2 and any(v is not None for v in cells):headers.append([str(v)[:140] if v is not None else '' for v in cells[:10]])
        out.append({'sheet':s.title,'rows':rows,'nonempty_rows':nonempty,'formulas':formulas,'header_rows':headers})
    wb.close();return out
results=[]
for p in sorted(D.rglob('*')):
    if not p.is_file() or p.is_symlink():continue
    before=p.stat();r={'name':p.relative_to(D).as_posix(),'bytes':before.st_size,'sha256':digest(p),'raw_copy_or_record_import':False}
    print('Reviewing '+p.name,flush=True)
    try:
        if p.suffix.lower()=='.zip':
            with zipfile.ZipFile(p) as z:
                members=[]
                for inf in z.infolist():
                    if inf.is_dir():continue
                    m={'name':inf.filename,'bytes':inf.file_size,'crc32':format(inf.CRC,'08x')}
                    h=hashlib.sha256()
                    with z.open(inf) as f:
                        for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
                    m['content_sha256']=h.hexdigest();m['full_stream_crc_checked']=True
                    if inf.filename.lower().endswith('.csv'):
                        with z.open(inf) as f:
                            reader=csv.reader(io.TextIOWrapper(f,encoding='utf-8-sig',newline=''));fields=next(reader);n=bad=0
                            selected=[(i,k) for i,k in enumerate(fields) if k in ['Entity.LegalAddress.Country','Entity.EntityStatus','Registration.RegistrationStatus','Relationship.RelationshipType','ExceptionCategory','ExceptionReason']]
                            counts={k:collections.Counter() for _,k in selected}
                            for cells in reader:
                                n+=1;bad+=len(cells)!=len(fields)
                                for i,k in selected:counts[k][cells[i] if i<len(cells) else '<ABSENT>']+=1
                            m.update(data_rows=n,columns=len(fields),field_count_mismatch=bad,headers=fields,code_counts={k:dict(v) for k,v in counts.items()})
                    members.append(m)
                r.update(kind='ARCHIVE_FULL_STREAM_AND_CSV_STRUCTURE',members=members)
        elif p.suffix.lower()=='.xlsx':r.update(kind='WORKBOOK_ALL_READABLE_ROWS',sheets=workbook(p.read_bytes()))
        elif p.suffix.lower()=='.sqlite':
            con=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True);integrity=con.execute('PRAGMA integrity_check').fetchone()[0];tables=[]
            for (name,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'"):
                q='"'+name.replace('"','""')+'"';tables.append({'table':name,'rows':con.execute('SELECT count(*) FROM '+q).fetchone()[0],'columns':[x[1] for x in con.execute('PRAGMA table_info('+q+')')]})
            con.close();r.update(kind='READ_ONLY_SQLITE_STRUCTURE_AND_INTEGRITY',integrity=integrity,tables=tables)
        elif p.suffix.lower()=='.rar':
            names=subprocess.check_output(['tar','-tf',str(p)]).decode('utf-8',errors='replace').splitlines();members=[]
            for name in names:
                if name.endswith('/'):continue
                data=subprocess.check_output(['tar','-xOf',str(p),name]);m={'name':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
                if name.lower().endswith('.xlsx'):
                    # Contact headers and names stay local; publish aggregate shape only.
                    m['sheets']=[{k:v for k,v in s.items() if k!='header_rows'} for s in workbook(data)]
                else:m['review']='BINARY_MEMBER_NOT_SEMANTICALLY_DECODED'
                members.append(m)
            r.update(kind='RAR_MEMBER_STREAM_AND_READABLE_WORKBOOK_ROWS',members=members)
        elif p.suffix.lower()=='.csv':
            with p.open(encoding='utf-8-sig',newline='') as f:
                reader=csv.reader(f);head=next(reader);rows=list(reader)
            r.update(kind='CSV_ALL_ROWS',headers=head,data_rows=len(rows),field_count_mismatch=sum(len(x)!=len(head) for x in rows))
            if 'ISIC_Rev' in p.name:
                idx=next((i for i,k in enumerate(head) if 'code' in k.lower()),0);r['code_length_counts']=dict(collections.Counter(len(x[idx]) for x in rows));r['unique_codes']=len({x[idx] for x in rows})
        elif p.suffix.lower() in ['.txt','.md','.ini']:
            data=p.read_bytes()
            try:t=data.decode('utf-8-sig');encoding='UTF8'
            except UnicodeDecodeError:t=data.decode('utf-16');encoding='UTF16'
            r.update(kind='TEXT_ALL_DECODED',encoding=encoding,lines=len(t.splitlines()),characters=len(t),heading_count=len(re.findall(r'^#+ ',t,re.M)),review='GENERATED_OR_RESEARCH_TEXT_REQUIRES_PRIMARY_SOURCE_CLAIM_REVIEW')
            if p.name=='Aerospace_Ecosystem_Report.md':
                local=R/'Reference/Aerospace_Ecosystem_Report.qmd';a=local.read_text(encoding='utf-8-sig');r['project_text_identical_normalized_newlines']=a.replace('\r\n','\n')==t.replace('\r\n','\n')
        elif p.suffix.lower()=='.iso':
            with p.open('rb') as f:f.seek(32768);descriptor=f.read(2048)
            r.update(kind='ISO_FULL_FILE_HASH_AND_VOLUME_DESCRIPTOR_ONLY',iso9660_magic=descriptor[1:6].decode('ascii',errors='replace'),volume_id=descriptor[40:72].decode('ascii',errors='replace').strip(),software_content_verification='NOT_EXECUTED_NOT_AUTHENTICATED',project_use='NONE')
        else:r['review']='FORMAT_UNSUPPORTED'
    except Exception as e:r.update(error=type(e).__name__,review='INCOMPLETE_REQUIRES_FOLLOWUP')
    after=p.stat();assert before.st_size==after.st_size and before.st_mtime_ns==after.st_mtime_ns,'Source changed during audit'
    r['source_unmodified_stat_check']=True;results.append(r)
    (O/'progress.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(O/'audit.json').write_text(json.dumps({'source_root':str(D),'files':results,'file_count':len(results),'original_files_or_data_records_imported':0,'hash_is_not_official_signature':True},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'files':len(results),'errors':sum('error'in r for r in results)}),flush=True)
