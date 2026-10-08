from pathlib import Path
import urllib.request,urllib.error,hashlib,csv,json,sqlite3,sys
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/38_global_directory_followup_b13_20261008'
sys.path.insert(0,str(O.parent/'global_directory_content_b05'));import intake
intake.O=O;intake.T=T
rows=[]
for old in csv.DictReader((T/'registry_file_acquisition_gaps.csv').open(encoding='utf-8-sig')):
    if old['url']==old['requested_url']:continue
    u=old['url'];r={'url':u,'prior_requested_url':old['requested_url'],'retry_reason':'PRESERVE_LITERAL_PLUS_IN_PATH','checked_on':'2026-10-08'}
    try:
        with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'ResearchDirectory/1.0'}),timeout=30) as response:
            data=response.read(20000001);r.update(http_status=response.status,final_url=response.url,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),truncated=len(data)>20000000)
        p=O/'downloads'/(hashlib.sha256((u+'literal-plus-retry').encode()).hexdigest()[:20]+'.response');p.write_bytes(data);r['file']=p.relative_to(R).as_posix()
    except urllib.error.HTTPError as e:r.update(http_status=e.code,error='HTTPError')
    except Exception as e:r['error']=type(e).__name__
    rows.append(r)
intake.write('registry_literal_url_retry_receipts.csv',rows)
con=sqlite3.connect(T/'global_directory_followup_b13.sqlite');fields=list(dict.fromkeys(k for r in rows for k in r));name='registry_literal_url_retry_receipts'
con.execute('CREATE TABLE '+name+' ('+','.join('"'+k+'" TEXT' for k in fields)+')')
con.executemany('INSERT INTO '+name+' VALUES ('+','.join('?' for k in fields)+')',[[r.get(k,'') for k in fields] for r in rows]);con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';con.close()
q=R/'Reference/Global_Directory_Followup_B13_20261008.qmd';q.write_text(q.read_text(encoding='utf-8')+'\n## 原始網址重試\n\n下載器將 EnEx 路徑中的字面加號編碼為 %2B，可能影響伺服器路由。本輪按來源原始網址重試並保留初次失敗收據，重試 HTTP 狀態為 '+json.dumps([r.get('http_status',r.get('error')) for r in rows])+'。重試收據另表入庫，不抹除初次觀測。\n',encoding='utf-8')
a=json.loads((O/'delivery_acceptance.json').read_text());a['sqlite_counts'][name]=len(rows);a['literal_url_retry']=rows;(O/'delivery_acceptance.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(rows))
