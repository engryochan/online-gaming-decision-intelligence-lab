from pathlib import Path
import csv,json,hashlib,subprocess,urllib.request,re,datetime,sqlite3
from concurrent.futures import ThreadPoolExecutor
from lxml import html
csv.field_size_limit(2147483647)
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/52_global_registry_identity_b27_20261008';T.mkdir(exist_ok=True)
assert not (O/'validation_receipt.json').exists(),'Preserve completed batch'
protected=[R/'Reference/Aerospace_Ecosystem_Report.qmd',R/'Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd',R/'Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']+list(R.glob('Reference/geo_defense_space_handoff_v2_3_0*'))
baseline={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
(O/'baseline.json').write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),protected=baseline),indent=2)+'\n',encoding='utf-8')
def write(n,rs):
    if not rs:return
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
D=O/'raw';D.mkdir(exist_ok=True)
def fetch(url):
    r=dict(url=url,checked_on='2026-10-08',http_status='',file='',sha256='',error='')
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ResearchRegistry/1.0'}),timeout=20) as response:
            data=response.read(3000001);r['http_status']=response.status
        assert len(data)<=3000000,'Body limit'
        p=D/(hashlib.sha256(url.encode()).hexdigest()[:20]+'.response');p.write_bytes(data);r.update(file=p.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest())
    except Exception as e:r['error']=type(e).__name__
    return r
issuer_url='https://progress.market/en/list-of-issuers-179/178'
receipt=fetch(issuer_url);receipts=[receipt];issuers=[]
if receipt['file']:
    root=html.fromstring((R/receipt['file']).read_bytes())
    for table in root.xpath('//table'):
        rs=table.xpath('.//tr')
        headers=[' '.join(c.text_content().split()) for c in rs[0].xpath('./th|./td')] if rs else []
        if 'LEI' not in headers:continue
        for row in rs[1:]:
            cells=[' '.join(c.text_content().split()) for c in row.xpath('./td')]
            if len(cells)!=len(headers):continue
            f=dict(zip(headers,cells));syms=[a.text_content().strip() for a in row.xpath('.//a')]
            issuers.append(dict(source_url=issuer_url,issuer=f.get('Issuer',''),lei=f['LEI'],symbols_json=json.dumps(syms),headquarters=f.get('Headquarters',''),evidence='EXCHANGE_ISSUER_ASSERTION_NOT_LEGAL_REGISTRY_VERIFICATION'))
write('registry_exchange_issuer_assertions.csv',issuers)
with ThreadPoolExecutor(max_workers=6) as pool:
    receipts+=list(pool.map(fetch,['https://api.gleif.org/api/v1/lei-records/'+r['lei'] for r in issuers]))
leirows=[]
for r in receipts[1:]:
    row=dict(lei=r['url'].rsplit('/',1)[1],api_url=r['url'],http_status=r['http_status'],legal_name='',entity_status='',registration_status='',registration_authority_id='',registration_authority_entity_id='',evidence='FETCH_FAILED_OR_SCHEMA_PENDING')
    if r['file']:
        try:
            a=json.loads((R/r['file']).read_bytes())['data']['attributes'];e=a['entity'];reg=a['registration'];authority=e.get('registeredAs','')
            row.update(legal_name=e['legalName']['name'],entity_status=e.get('status',''),registration_status=reg.get('status',''),registration_authority_id=e.get('registeredAt',{}).get('id',''),registration_authority_entity_id=authority,evidence='GLEIF_API_ATTRIBUTES_PARSED_NOT_ALL_CLAIMS_INDEPENDENTLY_VERIFIED')
        except Exception:row['evidence']='JSON_SCHEMA_REVIEW_PENDING'
    leirows.append(row)
write('registry_gleif_identity_observations.csv',leirows);write('source_fetch_manifest.csv',receipts)
def isin_ok(s):
    if not re.fullmatch('[A-Z]{2}[A-Z0-9]{9}[0-9]',s):return False
    digits=''.join(str(ord(c)-55) if c.isalpha() else c for c in s)
    total=0
    for i,c in enumerate(reversed(digits)):
        n=int(c)*(2 if i%2 else 1);total+=n//10+n%10
    return total%10==0
source=R/'Reference/tables/50_global_directory_content_b25_20261008/registry_structured_directory_records.csv'
rows=list(csv.DictReader(source.open(encoding='utf-8-sig')));checks=[];links={s:r for r in issuers for s in json.loads(r['symbols_json'])}
for index,r in enumerate(rows,1):
    if not any(d in r['source_url'] for d in ['nasdng.com','progress.market']):continue
    f=json.loads(r['fields_json']);isin=f.get('ISIN','');sym=f.get('Symbol','');issuer=links.get(sym,{})
    listing=f.get('Listing Date',f.get('Date Admitted',''));delisting=f.get('Delisting Date','');fmt='%m/%d/%Y' if isin else '%d %b, %Y'
    try:start=datetime.datetime.strptime(listing,fmt).date().isoformat();date_status='PARSED'
    except ValueError:start='';date_status='DATE_PARSE_PENDING'
    try:end=datetime.datetime.strptime(delisting,'%m/%d/%Y').date().isoformat() if delisting not in ['', '-'] else ''
    except ValueError:end='';date_status='DATE_PARSE_PENDING'
    checks.append(dict(b25_projection_id=index,source_url=r['source_url'],source_table=r['table'],source_row=r['row'],symbol=sym,isin=isin,isin_checksum='PASS' if isin and isin_ok(isin) else ('FAIL' if isin else 'NOT_PROVIDED'),listing_date_original=listing,listing_date_iso=start,delisting_date_original=delisting,delisting_date_iso=end,date_parse_status=date_status,status_assertion='DELISTING_DATE_PRESENT' if end else 'NO_DELISTING_DATE_NOT_PROOF_OF_ACTIVE',exchange_asserted_lei=issuer.get('lei',''),issuer_match='EXACT_SYMBOL_EXCHANGE_ASSERTION' if issuer else 'NO_CURRENT_ISSUER_MATCH',company_identity_verified='UNKNOWN'))
write('registry_security_identity_checks.csv',checks)
con=sqlite3.connect(T/'global_registry_identity_b27.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=list(csv.DictReader(p.open(encoding='utf-8-sig')));fields=list(rs[0]);q=lambda s:'"'+s.replace('"','""')+'"'
    con.execute('CREATE TABLE '+q(p.stem)+' ('+','.join(q(k)+' TEXT' for k in fields)+')');con.executemany('INSERT INTO '+q(p.stem)+' VALUES ('+','.join('?' for k in fields)+')',[[r[k] for k in fields] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for n,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0]==v
con.close();assert len(checks)==60 and sum(bool(r['isin']) for r in checks)==12
for r in receipts:
    if r['file']:assert hashlib.sha256((R/r['file']).read_bytes()).hexdigest()==r['sha256']
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in baseline.items())
stats=dict(record_checks=len(checks),isin_pass=sum(r['isin_checksum']=='PASS' for r in checks),delisting_dates=sum(bool(r['delisting_date_iso']) for r in checks),issuer_assertions=len(issuers),symbol_links=sum(bool(r['exchange_asserted_lei']) for r in checks),gleif_parsed=sum(r['evidence'].startswith('GLEIF_API') for r in leirows),sqlite_counts=counts,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
notes={'redteam':'交易代碼不可代替LEI，校驗碼通過不可證明證券真實；來源原件雜湊核對。','critic':'60條逐項檢查為48 admitted與12證券記錄；證券和法人數不能混加。','killcritic':'ISIN校驗、日期解碼及精確symbol到發行人映射均有逐項結果；無匹配不自動填假LEI。','blindspot':'無下市日期不代表仍交易；歷史證券可能無現行發行人匹配；GLEIF登記與法人存續狀態分開。','blueprint':'來源版本 → 證券識別碼 → 交易所發行人LEI斷言 → GLEIF身份觀測；各層保留證據，不把聯結當全部主張核實。','cheatsheet':'ISIN校驗通過≠官方配號核實；LEI存在≠公司現行上市；CURRENT登記≠法人存續；UNKNOWN≠0。','actionplan':'已檢查60條身份候選；續核登記機關ID、原清單2608項未嘗試及既有分頁／封存待辦。'}
for n,s in notes.items():(R/n/'global_registry_b27_20261008.md').write_text('# '+n+'｜B27\n\n'+s+'\n\n[報告](../Reference/Global_Registry_Identity_B27_20261008.qmd)。\n',encoding='utf-8')
report='''---
title: "全球登記 B27：60條身份候選、ISIN、日期與LEI來源聯結"
date: 2026-10-08
format:
  html:
    toc: true
    embed-resources: true
---

## 本輪逐項结果

'''+f"已檢查 {stats['record_checks']} 條原候選。12個ISIN中 {stats['isin_pass']} 個格式與Luhn校驗通過；{stats['delisting_dates']} 條有可解碼下市日期；交易所發行人頁保存 {stats['issuer_assertions']} 條斷言、精確symbol聯結 {stats['symbol_links']} 條證券；GLEIF API解析 {stats['gleif_parsed']} 條身份觀測。未知法人身份仍 UNKNOWN。"+'''

## 證據與限制

[Progress證券頁](https://progress.market/en/securities-27/26)含歷史下市日期及多種證券；[發行人頁](https://progress.market/en/list-of-issuers-179/178)另列LEI與對應交易代碼。日期按來源格式解碼，空值或橫線不當作已確認現行上市。交易所symbol聯結為来源斷言，不是独立工商驗證。GLEIF逐項API URL與HTTP收據另表記錄；法人狀態與LEI登記狀態分開。

NASD的48條保存記錄沒有ISIN／LEI；本輪網頁工具未取得，沿用B25原件核查日期，不杜撰法人鍵。股票、債券、發行人與券商皆不可混成公司總數。校驗碼只是格式檢查，不表示配號或法律身份已核實。七向文件已更新；舊版本、主報告與交接文件未覆寫。

## 可對賬交付

[60條逐項檢查](tables/52_global_registry_identity_b27_20261008/registry_security_identity_checks.csv)、[發行人斷言](tables/52_global_registry_identity_b27_20261008/registry_exchange_issuer_assertions.csv)、[GLEIF身份觀測](tables/52_global_registry_identity_b27_20261008/registry_gleif_identity_observations.csv)、[收據](tables/52_global_registry_identity_b27_20261008/source_fetch_manifest.csv)、[SQLite](tables/52_global_registry_identity_b27_20261008/global_registry_identity_b27.sqlite)。資料庫行數、完整性與原始回應雜湊通過。原清單2,608項未嘗試及所有歷史／分頁缺口仍保留，全球完整性UNKNOWN。未匯入Windows Downloads原件或明細。
'''
(R/'Reference/Global_Registry_Identity_B27_20261008.qmd').write_text(report,encoding='utf-8');print(json.dumps(stats))
