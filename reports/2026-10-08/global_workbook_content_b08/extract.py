from pathlib import Path
import sys,csv,json,hashlib,io,zipfile,sqlite3,collections,datetime,subprocess
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/33_global_workbook_content_b08_20261008';T.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(O/'local_runtime'))
import xlrd,openpyxl
from importlib.metadata import version
assert version('xlrd')=='2.0.2'
assert not (T/'global_workbook_content_b08.sqlite').exists(),'Preserve completed batch'
protected=['Reference/Aerospace_Ecosystem_Report.qmd','Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']
(O/'baseline.json').write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),status=subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),files={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in protected}),indent=2)+'\n',encoding='utf-8')
con=sqlite3.connect(T/'global_workbook_content_b08.sqlite');con.execute('CREATE TABLE workbook_rows(workbook_sha256 TEXT,sheet_index INTEGER,sheet_name TEXT,row_number INTEGER,values_json TEXT,types_json TEXT,formats_json TEXT,extras_json TEXT)')
fields=['workbook_sha256','sheet_index','sheet_name','row_number','values_json','types_json','formats_json','extras_json']
stream=(T/'registry_workbook_rows.csv').open('w',encoding='utf-8-sig',newline='');writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
manifests=[];sheets=[];observations=[];seen=set();totalrows=0;totalcells=0
def dumps(value):return json.dumps(value,ensure_ascii=False,default=str,separators=(',',':'))
def write(name,rows):
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with (T/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
def emit(sha,si,sn,number,values,types,formats,extras):
    global totalrows,totalcells
    row=dict(workbook_sha256=sha,sheet_index=si,sheet_name=sn,row_number=number,values_json=dumps(values),types_json=dumps(types),formats_json=dumps(formats),extras_json=dumps(extras))
    writer.writerow(row);con.execute('INSERT INTO workbook_rows VALUES (?,?,?,?,?,?,?,?)',[row[k] for k in fields]);totalrows+=1;totalcells+=len(values)
def workbook(data,label,url):
    sha=hashlib.sha256(data).hexdigest();observations.append(dict(source_url=url,object_path=label,workbook_sha256=sha))
    if sha in seen:return
    seen.add(sha);record=dict(workbook_sha256=sha,object_path=label,source_url=url,bytes=len(data));manifests.append(record)
    try:
        ole=data.startswith(bytes.fromhex('d0cf11e0a1b11ae1'))
        if ole:
            book=xlrd.open_workbook(file_contents=data,formatting_info=True,on_demand=True,logfile=io.StringIO());record.update(format='XLS_BIFF',reader='xlrd_2.0.2',formula_policy='CACHED_RESULTS_ONLY_FORMULA_TEXT_REMAINS_IN_RAW',date_mode=book.datemode,sheet_count=book.nsheets)
            for si in range(book.nsheets):
                sh=book.sheet_by_index(si);assert sh.nrows*sh.ncols<=3000000,'WORKSHEET_CELL_LIMIT'
                sheets.append(dict(workbook_sha256=sha,sheet_index=si+1,sheet_name=sh.name,rows=sh.nrows,columns=sh.ncols,visibility=sh.visibility,merged_ranges_json=dumps(sh.merged_cells),date_mode=book.datemode,coverage='ALL_READER_REPORTED_RECTANGULAR_ROWS'))
                for rn in range(sh.nrows):
                    cells=sh.row(rn);formats=[book.format_map[book.xf_list[c.xf_index].format_key].format_str for c in cells]
                    emit(sha,si+1,sh.name,rn+1,[c.value for c in cells],[c.ctype for c in cells],formats,{})
                book.unload_sheet(si)
            book.release_resources()
        else:
            book=openpyxl.load_workbook(io.BytesIO(data),read_only=False,data_only=False,keep_links=True)
            record.update(format='OOXML',reader='openpyxl_'+openpyxl.__version__,formula_policy='FORMULA_TEXT_NO_RECALCULATION',sheet_count=len(book.worksheets))
            for si,sh in enumerate(book.worksheets,1):
                assert sh.max_row*sh.max_column<=3000000,'WORKSHEET_CELL_LIMIT'
                sheets.append(dict(workbook_sha256=sha,sheet_index=si,sheet_name=sh.title,rows=sh.max_row,columns=sh.max_column,visibility=sh.sheet_state,merged_ranges_json=dumps([str(x) for x in sh.merged_cells.ranges]),date_mode=str(book.epoch),coverage='ALL_READER_REPORTED_RECTANGULAR_ROWS'))
                iterator=sh.iter_rows();first=next(iterator,None)
                if first is None:
                    emit(sha,si,sh.title,1,[None]*sh.max_column,['n']*sh.max_column,['General']*sh.max_column,{'reader_note':'IMPLICIT_EMPTY_WORKSHEET_RECTANGLE'})
                import itertools
                for rn,cells in enumerate(itertools.chain([first],iterator) if first is not None else [],1):
                    extras={c.coordinate:dict(formula=c.value if c.data_type=='f' else None,hyperlink=c.hyperlink.target if c.hyperlink else None,comment=c.comment.text if c.comment else None) for c in cells if c.data_type=='f' or c.hyperlink or c.comment}
                    emit(sha,si,sh.title,rn,[c.value for c in cells],[c.data_type for c in cells],[c.number_format for c in cells],extras)
            book.close()
        record['status']='ROWS_EXTRACTED_WITH_EXPLICIT_READER_LIMITATIONS'
    except Exception as e:record.update(status='REVIEW_REQUIRED_PARTIAL_ROWS_MAY_EXIST',error=type(e).__name__)
    con.commit();stream.flush();print('workbooks',len(manifests),'rows',totalrows,flush=True)
archives=[]
def inspect(data,label,url,depth=0):
    if data.startswith(bytes.fromhex('d0cf11e0a1b11ae1')):return workbook(data,label,url)
    if zipfile.is_zipfile(io.BytesIO(data)):
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            if 'xl/workbook.xml' in z.namelist():return workbook(data,label,url)
            for info in z.infolist():
                if info.is_dir():continue
                item=dict(source_url=url,object_path=label+'::'+info.filename,bytes=info.file_size,depth=depth+1);archives.append(item)
                if info.file_size>50000000 or depth>=3:item['status']='SIZE_OR_DEPTH_LIMIT_PENDING';continue
                content=z.read(info);item['sha256']=hashlib.sha256(content).hexdigest();item['status']='MEMBER_OBSERVED'
                if info.filename.lower().endswith(('.xls','.xlsx','.xlsm','.zip')):inspect(content,item['object_path'],url,depth+1)
    elif label.lower().endswith(('.xls','.xlsx')):archives.append(dict(source_url=url,object_path=label,bytes=len(data),status='NON_BIFF_NON_OOXML_CONTENT_REVIEW'))
sources=[]
for batch in ['30_global_directory_content_b05_20261008','31_global_directory_content_b06_20261008','32_global_directory_content_b07_20261008']:
    path=R/'Reference/tables'/batch/'direct_file_fetch_manifest.csv'
    for row in csv.DictReader(path.open(encoding='utf-8-sig')):
        if not row.get('file'):continue
        data=(R/row['file']).read_bytes();sha=hashlib.sha256(data).hexdigest();assert sha==row['sha256']
        sources.append(dict(batch=batch,source_url=row['url'],raw_file=row['file'],sha256=sha,bytes=len(data),truncated=row.get('truncated','UNKNOWN')))
        if row.get('truncated')=='True':continue
        inspect(data,row['file'],row['url'])
stream.close();con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
write('registry_input_source_observations.csv',sources);write('registry_workbook_observations.csv',observations);write('registry_workbook_manifest.csv',manifests);write('registry_worksheet_dimensions.csv',sheets);write('registry_archive_member_review.csv',archives)
for path in sorted(T.glob('*.csv')):
    if path.name=='registry_workbook_rows.csv':continue
    with path.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);keys=reader.fieldnames;rows=list(reader)
        if not keys:continue
        name=path.stem;con.execute('CREATE TABLE "'+name+'" ('+','.join('"'+k+'" TEXT' for k in keys)+')');con.executemany('INSERT INTO "'+name+'" VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rows])
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';con.close()
summary=dict(input_observations=len(sources),unique_input_hashes=len({r['sha256'] for r in sources}),workbook_observations=len(observations),unique_workbooks=len(manifests),worksheets=len(sheets),rows=totalrows,cells=totalcells,status_counts=dict(collections.Counter(r['status'] for r in manifests)),format_counts=dict(collections.Counter(r.get('format','UNKNOWN') for r in manifests)),archive_member_observations=len(archives),integrity='ok',global_complete=False)
(O/'extraction_acceptance.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary))
