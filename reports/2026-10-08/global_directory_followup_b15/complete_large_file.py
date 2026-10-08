from pathlib import Path
import urllib.request,hashlib,csv,json,zipfile,sqlite3,sys
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/40_global_directory_followup_b15_20261008'
sys.path.insert(0,str(O.parent/'global_directory_content_b05'));import intake
intake.O=O;intake.T=T
rows=[];members=[]
for old in csv.DictReader((T/'registry_file_acquisition_gaps.csv').open(encoding='utf-8-sig')):
    if old.get('truncated')!='True':continue
    u=old['url'];p=O/'downloads'/(hashlib.sha256((u+'full-retry').encode()).hexdigest()[:20]+'.response');assert not p.exists()
    h=hashlib.sha256();size=0
    with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'ResearchDirectory/1.0'}),timeout=30) as response,p.open('wb') as f:
        expected=response.headers.get('Content-Length');status=response.status
        while True:
            chunk=response.read(1048576)
            if not chunk:break
            size+=len(chunk);assert size<=200000000,'Explicit 200MB safety bound'
            f.write(chunk);h.update(chunk)
    if expected:assert int(expected)==size
    r=dict(url=u,http_status=status,file=p.relative_to(R).as_posix(),bytes=size,sha256=h.hexdigest(),content_length=expected or '',truncated=False,prior_partial_file=old['file'],prior_partial_sha256=old['sha256'],scope='HISTORICAL_CLEARING_MARGIN_LEVELS_NOT_ENTITY_DIRECTORY');rows.append(r)
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None
        for info in z.infolist():
            if info.is_dir():continue
            digest=hashlib.sha256()
            with z.open(info) as f:
                for chunk in iter(lambda:f.read(1048576),b''):digest.update(chunk)
            members.append(dict(url=u,member=info.filename,bytes=info.file_size,sha256=digest.hexdigest(),status='CRC_AND_MEMBER_HASH_VERIFIED_SEMANTICS_PENDING'))
intake.write('registry_full_file_retry_receipts.csv',rows);intake.write('registry_full_retry_archive_members.csv',members)
a=json.loads((O/'delivery_acceptance.json').read_text());con=sqlite3.connect(T/'global_directory_followup_b15.sqlite')
for name,data in [('registry_full_file_retry_receipts',rows),('registry_full_retry_archive_members',members)]:
    fields=list(dict.fromkeys(k for r in data for k in r));con.execute('CREATE TABLE '+name+' ('+','.join('"'+k+'" TEXT' for k in fields)+')');con.executemany('INSERT INTO '+name+' VALUES ('+','.join('?' for k in fields)+')',[[r.get(k,'') for k in fields] for r in data]);a['sqlite_counts'][name]=len(data)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';con.close()
a['full_file_retries']=rows;(O/'delivery_acceptance.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
q=R/'Reference/Global_Directory_Followup_B15_20261008.qmd';q.write_text(q.read_text(encoding='utf-8')+f'\n## 大檔及工作簿解析限制\n\nHKEX 歷史保證金 ZIP 初次觸及 20MB 接收上限，部分回應及收據保留；本輪重新串流取得完整檔，共 {sum(r["bytes"] for r in rows):,} 位元組，核對 Content-Length、ZIP CRC 與 {len(members)} 個成員雜湊通過。追加收據與成員表另行入庫，未覆蓋初次資料。此檔是歷史清算風險參數，不是公司名錄。\n\nopenpyxl 提示不支援部分資料驗證擴充；本輪未重寫任何來源工作簿，原始內容保留。抽取行不代表全部工作簿物件已解析。原始下載及後續完整重試合計 54 個網址已保存或沿用，Nasdaq 頻寬報告仍為 404。\n',encoding='utf-8')
print(json.dumps(dict(full_files=len(rows),bytes=sum(r['bytes'] for r in rows),members=len(members))))
