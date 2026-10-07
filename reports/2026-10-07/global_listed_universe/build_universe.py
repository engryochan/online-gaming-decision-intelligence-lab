from pathlib import Path
import csv,json,hashlib,sqlite3,collections
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).parent
TABLE=ROOT/'Reference/tables/19_global_listed_company_universe_20261007'
TABLE.mkdir(exist_ok=True)
def write(name,rows):
    with (TABLE/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
rows=[];manifest=[]
for feed in ['nasdaqlisted','otherlisted']:
    p=OUT/'raw'/f'{feed}.txt'; lines=p.read_text(encoding='utf-8-sig').splitlines()
    assert lines[-1].startswith('File Creation Time:')
    data=list(csv.DictReader(lines[:-1],delimiter='|'))
    assert all(None not in r and all(v is not None for v in r.values()) for r in data)
    manifest.append(dict(feed=feed,url=f'https://www.nasdaqtrader.com/dynamic/SymDir/{feed}.txt',sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rows=len(data),source_creation_time_raw=lines[-1],retrieved_on='2026-10-07'))
    for i,r in enumerate(data,1):
        rows.append(dict(security_record_id=f'{feed}:{i}',feed=feed,source_row=i,symbol=r.get('Symbol',r.get('ACT Symbol')),security_name=r['Security Name'],exchange_code='NASDAQ' if feed=='nasdaqlisted' else r['Exchange'],market_country_iso_alpha2='US',issuer_country_iso_alpha2='UNKNOWN',issuer_identity_state='UNRESOLVED',ETF=r['ETF'],test_issue=r['Test Issue'],financial_status=r.get('Financial Status',''),technology_evidence_state='UNKNOWN',raw_fields_json=json.dumps(r,ensure_ascii=False)))
assert len({r['security_record_id'] for r in rows})==len(rows)
write('registry_listed_security.csv',rows);write('source_manifest.csv',manifest)
mother=ROOT/'Reference/tables/10_global_technology_iso249_20261006_b04/registry_country_technology_coverage.csv'
with mother.open(encoding='utf-8-sig',newline='') as f: countries=list(csv.DictReader(f))
assert len(countries)==249 and len({r['iso_alpha2'] for r in countries})==249
coverage=[dict(iso_alpha2=r['iso_alpha2'],name_en=r['name_en'],market_feed_state='PARTIAL_OFFICIAL_FEEDS_INGESTED' if r['iso_alpha2']=='US' else 'NOT_YET_INGESTED',security_rows=len(rows) if r['iso_alpha2']=='US' else 0,all_exchanges_complete='UNKNOWN',all_companies_complete='UNKNOWN',issuer_domicile_coverage='UNKNOWN',absence_of_market='UNKNOWN',mother_raw_json=json.dumps(r,ensure_ascii=False)) for r in countries]
write('registry_country_market_coverage.csv',coverage)
counts=collections.Counter((r['feed'],r['exchange_code'],r['ETF'],r['test_issue']) for r in rows)
write('market_security_analysis.csv',[dict(feed=k[0],exchange_code=k[1],ETF=k[2],test_issue=k[3],security_records=v,unique_company_count='UNKNOWN') for k,v in sorted(counts.items())])
neuro=[dict(capability_id='BBI_BRAINNET',title='BrainNet',source_url='https://arxiv.org/abs/1809.08632v3',related_journal_doi='10.1038/s41598-019-41895-7',evidence_scope='AUTHOR_PREPRINT_ABSTRACT_VERIFIED',human_groups=5,humans_per_group=3,average_task_accuracy=0.813,read_modality='EEG',write_modality='TMS_OCCIPITAL',transport='INTERNET_WITH_EXTERNAL_HARDWARE',payload='ROTATE_OR_KEEP_BLOCK_DECISION',semantic_mind_transfer='UNKNOWN',information_bandwidth_bits_per_second='UNKNOWN',N0_N7_level='UNKNOWN',clinical_authorization='UNKNOWN')]
write('registry_neural_interaction_evidence.csv',neuro)
db=OUT/'listed_universe.sqlite'
assert not db.exists(), 'Keep prior snapshots; do not overwrite database'
con=sqlite3.connect(db)
for name,data in [('securities',rows),('countries',coverage),('sources',manifest),('neural_interaction',neuro)]:
    fields=list(data[0]);con.execute('CREATE TABLE '+name+' ('+','.join('"'+x+'" TEXT' for x in fields)+')')
    con.executemany('INSERT INTO '+name+' VALUES ('+','.join('?' for _ in fields)+')',[[str(r[x]) for x in fields] for r in data])
con.execute("CREATE VIEW non_test_non_etf_securities AS SELECT * FROM securities WHERE ETF='N' AND test_issue='N'")
con.commit()
assert con.execute('SELECT COUNT(*) FROM securities').fetchone()[0]==len(rows)
for feed in ['nasdaqlisted','otherlisted']:
    originals=list(csv.DictReader((OUT/'raw'/f'{feed}.txt').read_text(encoding='utf-8-sig').splitlines()[:-1],delimiter='|'))
    restored=[json.loads(x[0]) for x in con.execute('SELECT raw_fields_json FROM securities WHERE feed=? ORDER BY CAST(source_row AS INTEGER)',(feed,))]
    assert originals==restored
validation=dict(security_rows=len(rows),country_rows=len(coverage),raw_fields_roundtrip=True,source_manifest=manifest,non_test_non_etf_security_rows=con.execute('SELECT COUNT(*) FROM non_test_non_etf_securities').fetchone()[0],unique_company_count='UNKNOWN',global_exhaustive=False,sec_download_state='HTTP_REQUEST_RATE_THRESHOLD_REJECTED')
con.close();(OUT/'validation.json').write_text(json.dumps(validation,indent=2)+'\n',encoding='utf-8')
report='''---
title: "全球上市公司全量收錄：證券母表與腦際互動證據（首批）"
lang: zh-Hant
format: html
---

## 收錄範圍與驗收

本批完整接收 Nasdaq 官方兩份名錄全部 {n} 筆證券列，沒有按公司知名度或科技題材抽選。檔案時間原文均為 `File Creation Time: 1007202607:00`；時間區未自行推定。原始檔、SHA256、每列原始欄位及資料庫均保留。原始欄位逐列 JSON 還原比對通過。

249 國家／地區母表沿用項目既有 ISO 3166-1 表；[ISO 標準](https://www.iso.org/iso-3166-country-codes.html)不是國家認證。本批只有美國上市市場的部分官方來源，其餘 248 條目明列尚未接收；不能據此判定當地無交易所。全球每一家上市公司的收錄工作尚未完成，美國全市場也未宣稱完成。

## 數據表與查詢

- [全部證券列](tables/19_global_listed_company_universe_20261007/registry_listed_security.csv)：{n} 列，包括 ETF、測試證券、股類、權證等；任何原始欄位均存入 `raw_fields_json`。
- [249 條目市場覆蓋](tables/19_global_listed_company_universe_20261007/registry_country_market_coverage.csv)：區分市場所在地與發行人註冊地，後者目前 UNKNOWN。
- [市場分組分析](tables/19_global_listed_company_universe_20261007/market_security_analysis.csv)：按來源、交易所原碼、ETF 與測試旗標計數。
- [來源與雜湊](tables/19_global_listed_company_universe_20261007/source_manifest.csv)。官方[欄位定義](https://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs)、[Nasdaq 名錄](https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt)、[其他市場名錄](https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt)。未知交易所代碼保留原碼，不猜名稱。
- SQLite：`reports/2026-10-07/global_listed_universe/listed_universe.sqlite`，表 `securities`、`countries`、`sources`、`neural_interaction`；視圖 `non_test_non_etf_securities`。

排除測試與 ETF 後仍有 {candidate} 筆**證券**，不能當成 {candidate} 家公司。普通股、存託憑證、優先股及權證可能對應同一發行人；非 ETF 也可能是其他基金。SEC [發行人對照下載](https://www.sec.gov/files/company_tickers_exchange.json)本輪遭網站拒絕，未建立虛構 CIK、公司唯一數或發行人國籍。名錄是當前快照，未聲稱涵蓋所有歷史退市公司。

## 業務定義與價值

證券主鍵以來源及列號確保原文留存；後續以市場、代碼及有效期間建立跨批鍵。公司主表須另以監管登記識別碼／LEI及官方註冊資料解析，上市關係採多對多；註冊地、總部與交易市場各自登記。名稱相似不可直接合併。全市場母表支援公司技術暴露、跨市場重複上市及供應鏈分析，但每一家公司是否屬前沿科技須另有論文、專利、產品或監管證據，不能從上市本身推論。

下一階段逐國確認所有交易所及官方完整名錄、接收全部列、對賬來源總數、解析發行人及上市關係，再連結現有科技登記。缺失、來源拒絕、未授權取得與尚未查證分別保留狀態；249 覆蓋列不是249國完成證明。

## 遠程腦際互動：實驗與待驗證能力

[BrainNet 作者版本 v3](https://arxiv.org/abs/1809.08632v3)摘要描述五组三人參與者，平均任務正確率 0.813。EEG 解碼是否旋轉遊戲方塊的決策，經網路傳輸，由 TMS 刺激接收者枕葉；接收者再透過 EEG 作出選擇。相關期刊 DOI 為 [10.1038/s41598-019-41895-7](https://doi.org/10.1038/s41598-019-41895-7)，本輪期刊正文無法讀取，所以來源等級限定為作者版本摘要核實。

[神經互動證據表](tables/19_global_listed_company_universe_20261007/registry_neural_interaction_evidence.csv)登記這項硬體及網路介導的有限決策互動。完整思想、記憶或情緒傳輸、無器件遠程心靈相通、人體臨床授權及 bits/s 資訊帶寬均為 UNKNOWN；0.813 是特定任務正確率，不能轉換成心靈交流帶寬。未建立 N0～N7 定義與判準前不授予國家等級，也未以此單篇歷史實驗宣稱當今最高技術。
'''.format(n=len(rows),candidate=validation['non_test_non_etf_security_rows'])
(ROOT/'Reference/Global_Listed_Company_Universe_20261007.qmd').write_text(report,encoding='utf-8')
print(json.dumps(validation,ensure_ascii=True))
