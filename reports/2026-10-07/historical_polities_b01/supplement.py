from pathlib import Path
import csv,json,hashlib,sqlite3
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent;D=O/'raw';T=R/'Reference/tables/26_historical_polities_b01_20261007'
checks=json.loads((O/'financial_source_checks.json').read_text())
rows=[dict(iso_alpha2='US',source='SEC_ACTIVE_BROKER_DEALERS',source_url=checks[0]['source_url'],scope='SEC registered active broker-dealers, source September 2026',access_status='HTTP_403_NO_ROWS_INGESTED',ingested_records=0,completion='UNKNOWN',next_requirement='Receive official full file and validate tab-delimited layout, date, CIK uniqueness and coverage'),dict(iso_alpha2='US',source='FINRA_BROKER_DEALER_FIRM_LIST',source_url='https://developer.finra.org/docs',scope='Active FINRA registered firms and firms with termination requests; excludes terminated firms',access_status='DOCUMENTED_FIRM_OR_ORGANIZATION_CREDENTIALS_NOT_AVAILABLE',ingested_records=0,completion='UNKNOWN',next_requirement='Authorized production access; reconcile record-total headers with pages up to 500 records; mock data is not evidence')]
with (T/'registry_financial_source_gap_checks.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
c=sqlite3.connect(O/'historical_polities_v1.sqlite');c.execute('CREATE TABLE financial_source_checks(source TEXT PRIMARY KEY,fields_json TEXT)');c.executemany('INSERT INTO financial_source_checks VALUES(?,?)',[(r['source'],json.dumps(r)) for r in rows]);c.commit();assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok';c.close()
p=R/'Reference/Global_Historical_Polities_B01_20261007.qmd';b=p.read_text(encoding='utf-8');b+='''
## 本輪金融來源再查

[美國政府資料目錄](https://catalog.data.gov/dataset/company-information-about-active-broker-dealers)已列2026年9月SEC活躍券商檔案；實際下載返回HTTP 403，未接收任何券商列，錯誤回應與指紋保留。目錄說明此類自動彙編資料未經SEC逐項獨立審閱，成功取得也不能直接視作內容全面核實。

[FINRA正式文件](https://developer.finra.org/docs)提供brokerDealerFirmList，要求Firm或Organization憑證，分頁須對賬record-total；涵蓋活躍及提出終止請求的公司，排除已終止公司。本輪未取得正式存取，未使用Mock樣本充當公司資料。

- [下載與正式存取缺口](tables/26_historical_polities_b01_20261007/registry_financial_source_gap_checks.csv)
- [下載實測回執](../reports/2026-10-07/historical_polities_b01/financial_source_checks.json)

瀏覽器已實測1800年初始圖、公元前3400年篩選、公元100年Roman名稱篩選與記錄點選；來源時段91至105顯示成功。這驗證篩選與顯示功能，沒有核定羅馬疆界。
''';p.write_text(b,encoding='utf-8')
tests=dict(default_year_1800_records=130,year_minus3400_records=1,year_minus3400_name='Sumerian City-States',year100_search_Roman_records=1,selected_record='CLIO:001215',displayed_source_years=[91,105],screenshot='map_browser_proof.png',browser_test_passed=True,independent_historical_fact_review_complete=False)
(O/'map_browser_acceptance.json').write_text(json.dumps(tests,indent=2)+'\n',encoding='utf-8')
manifest=[]
for p in sorted(T.glob('*.csv')):
 if p.name!='integration_input_manifest.csv':manifest.append(dict(path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
with (T/'integration_input_manifest.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=['path','sha256']);w.writeheader();w.writerows(manifest)
old=json.loads((O/'source_manifest.json').read_text());more=[('sec_datagov_catalog.html','https://catalog.data.gov/dataset/company-information-about-active-broker-dealers'),('sec_broker_download_error.html',checks[0]['source_url'])]
for name,url in more:
 p=D/name;old.append(dict(url=url,file=name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),http_status=403 if 'error' in name else 200))
(O/'source_manifest.json').write_text(json.dumps(old,indent=2)+'\n',encoding='utf-8')
print('Financial access gaps and browser acceptance added')
