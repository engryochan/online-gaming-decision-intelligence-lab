from pathlib import Path
import csv,json,hashlib,sqlite3,re,subprocess
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/76_ais_semantics_b53_20261011'
MAIN='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    assert rs
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
assert not (O/'validation_receipt.json').exists(),'Do not overwrite delivery'
base=json.loads((O/'baseline.json').read_text());assert all(sha((R/p).read_bytes())==h for p,h in base['protected'].items())
receipts=read(T/'registry_source_receipts.csv');rm={r['source_id']:r for r in receipts}
dictionary=json.loads((O/'B53DICTIONARY_extraction.json').read_text(encoding='utf-8'))
assert len(dictionary)==2
old=dictionary[0]['tables'][0];new=dictionary[1]['tables'][0];assert len(old)==18 and len(new)==18
header=read(R/'Reference/tables/75_access_resolution_b52_20261011/registry_noaa_2019_csv_header.csv')
assert [r[1] for r in old[1:]]==[r['column_name'] for r in header]
text=dictionary[0]['text'];m=re.search(r'Updated:\s*(.+)',text);date=m[1] if m else 'NOT_PARSED'
defs=[]
for page,table,period in [(1,old,'2018-2024'),(2,new,'2025-PRESENT')]:
    for row in table[1:]:
        if page==1:ordinal,name,description,example,unit,resolution,typ,size=row;domain=null='NOT_SPECIFIED_FOR_2018_2024'
        else:ordinal,name,description,example,unit,domain,null,typ,size=row;resolution='NOT_SPECIFIED_IN_THIS_TABLE'
        defs.append(dict(schema_period=period,source_page=page,ordinal=ordinal,column_name=name,description=description,example=example,unit=unit,resolution=resolution,source_type=typ,source_size_or_bytes=size,valid_domain=domain,null_allowed=null,
            raw_table_row_json=json.dumps(row,ensure_ascii=False),source_file=rm['B53DICTIONARY']['source_file'],source_sha256=rm['B53DICTIONARY']['sha256'],dictionary_updated=date,verification='DOCUMENT_SCHEMA_MATCH_NOT_FULL_DATA_VALIDATION'))
write('registry_versioned_field_dictionary.csv',defs)
mapping={'MMSI':'mmsi','BaseDateTime':'base_date_time','LAT':'latitude','LON':'longitude','SOG':'sog','COG':'cog','Heading':'heading','VesselName':'vessel_name','IMO':'imo','CallSign':'call_sign','VesselType':'vessel_type','Status':'status','Length':'length','Width':'width','Draft':'draft','Cargo':'cargo','TransceiverClass':'transceiver'}
newmap={r['column_name']:r for r in defs if r['schema_period']=='2025-PRESENT'}
changes=[]
for r in defs[:17]:
    n=newmap[mapping[r['column_name']]]
    changes.append(dict(old_column=r['column_name'],new_column=n['column_name'],old_ordinal=r['ordinal'],new_ordinal=n['ordinal'],old_type=r['source_type'],new_type=n['source_type'],old_size=r['source_size_or_bytes'],new_size=n['source_size_or_bytes'],old_unit=r['unit'],new_unit=n['unit'],migration_policy='PRESERVE_SOURCE_STRING_AND_PERIOD_NO_AUTOMATIC_CAST_OR_TRUNCATION',new_domain_applied_to_2019=False,source_sha256=r['source_sha256']))
write('registry_schema_migration_comparison.csv',changes)
summary=json.loads((O/'B53SUMMARY_extraction.json').read_text(encoding='utf-8'))[0]['tables'][0]
write('registry_official_annual_summary.csv',[dict(year=r[0],period=r[1],scope=r[2],file_type=r[3],declared_files=r[4],declared_records_billions=r[5],declared_compressed_gb=r[6],declared_uncompressed_gb_estimate=r[7],source_comments=r[8],source_file=rm['B53SUMMARY']['source_file'],source_sha256=rm['B53SUMMARY']['sha256'],scope_of_verification='SOURCE_DECLARATION_NOT_DOWNLOADED_FILE_COUNTS_OR_BYTES') for r in summary[1:]])
faq=json.loads((O/'B53FAQ_extraction.json').read_text(encoding='utf-8'));assert len(faq)==11
rules=[('COVERAGE',1,'地面接收、区域覆盖；不是全球卫星AIS'),('DOWNSAMPLING',3,'取整分钟处理；样本非全部原始广播'),('TYPE_PROVENANCE',4,'2019类型等字段经AVIS校订；Cargo保留原类型来源'),('IDENTITY',5,'船名／发射器可变；实体关系需时态核对'),('COG_SENTINEL',7,'文档列示360.0为不可用标记；2019自动应用仍待样本核对'),('SOG_SENTINEL',7,'文档列示102.3为不可用标记；2019自动应用仍待样本核对'),('HEADING_SENTINEL',7,'511的说明限定pre-2015，禁止机械套到2019'),('NEGATIVE_REPAIR',7,'当前版本未列旧搜索摘要的负值加常数规则；暂不自动修正'),('USE_SCOPE',10,'规划用途与Level C条件需逐用途审查，不发出转售许可')]
write('registry_quality_and_use_rules.csv',[dict(rule_id=k,source_page=page,assessment=v,policy='RETAIN_RAW_VALUE_AND_EVIDENCE_REVIEW_NOT_AUTO_CORRECTION',source_file=rm['B53FAQ']['source_file'],source_sha256=rm['B53FAQ']['sha256']) for k,page,v in rules])
layer=json.loads((R/rm['B53PUBLICLAYER']['source_file']).read_bytes())
write('registry_public_layer_access.csv',[dict(url=rm['B53PUBLICLAYER']['url'],http_status=rm['B53PUBLICLAYER']['http_status'],api_error_code=layer.get('error',{}).get('code',''),full_response_json=json.dumps(layer),schema_fetched='error' not in layer,source_file=rm['B53PUBLICLAYER']['source_file'],source_sha256=rm['B53PUBLICLAYER']['sha256'])])
for name in ['registry_noaa_2019_daily_objects.csv','registry_noaa_2019_csv_header.csv','registry_gap_resolution.csv']:
    write('preserved_'+name,read(R/'Reference/tables/75_access_resolution_b52_20261011'/name))
con=sqlite3.connect(T/'ais_semantics_b53.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=read(p);ks=list(rs[0]);con.execute('CREATE TABLE "'+p.stem+'" ('+','.join('"'+k+'" TEXT' for k in ks)+')');con.executemany('INSERT INTO "'+p.stem+'" VALUES ('+','.join('?' for k in ks)+')',[[r[k] for k in ks] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for k,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+k+'"').fetchone()[0]==v
con.close()
stats=dict(dictionary_pages=2,dictionary_updated=date,versioned_field_rows=34,field_mappings=17,previous_2019_header_exact_match=True,faq_pages=11,summary_pages=1,annual_summary_rows=len(summary)-1,quality_and_use_rules=9,source_receipts=5,http_errors=sum(bool(r['error']) for r in receipts),public_layer_api_error=layer.get('error',{}).get('code',''),full_data_rows_validated=0,automatic_corrections_applied=0,sqlite_counts=counts,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
report='''---
title: "B53：AIS年代化欄位字典、品質與用途核對"
date: 2026-10-11
lang: zh-TW
format:
  html:
    toc: true
    embed-resources: true
---

## 2019欄位與新版本隔離

取得[官方字典](https://coast.noaa.gov/data/marinecadastre/ais/data-dictionary.pdf)，明列2018–2024與2025起兩套17欄結構。2019部分檔表頭與舊期欄名及順序完全一致；只核schema，不是全檔驗證。MMSI以文字識別，UTC時間保留、座標十進位度、SOG為節、COG及Heading為度，尺寸為米。字典declared type、size與domain保留原欄，不能把展示精度當作實際量測精度。

跨期欄位有改名、座標順序改變、Heading／Cargo／尺寸型別及文字長度變動，逐欄映射保存；新期有效範圍及null要求不套2019，不能自動轉型、截字或補零。抽取器替代字元保留原文與PDF，規範化欄位另行核；來源PDF仍是覆核依據。

## 品質與使用邊界

[官方FAQ](https://coast.noaa.gov/data/marinecadastre/ais/faq.pdf)為地面接收與歷史規劃資料，覆蓋、取整分鐘、AVIS校訂與使用條件分列於規則表。它不是全球衛星AIS。COG／SOG缺值標記及Heading的年代適用性保留待樣本核對；當期文件未找到舊搜索摘要的負值加常數规则，不自动修正。公共领域与Level C條件不能簡化為任意原始資料收費轉售。

## 年度規模與公開服務實測

[官方年度摘要](https://coast.noaa.gov/data/marinecadastre/ais/point-data-summary.pdf)列2019有365檔、約27億記錄、壓縮99.1 GB、解壓估283 GB。這些是來源宣告，不是本項目全量實測。其他年份与Total行一并保留，空白記錄數保持空值，不補零。2025摘要是不完整年度，不能當全年資料量。

另讀[2019 InPort元資料](https://www.fisheries.noaa.gov/inport/item/62733)保存版本證據。NOAA托管的2019 Transit Counts圖層端點本次也回應HTTP200內含499 Token Required；沒有取得schema，不能因域名屬NOAA就假定服務無帳戶限制。原CSV公開目錄與圖層服務繼續分開。

## 驗收與交付

'''+json.dumps(stats,ensure_ascii=False)+'''。

[34筆年代化字典](tables/76_ais_semantics_b53_20261011/registry_versioned_field_dictionary.csv)、[17項跨期比較](tables/76_ais_semantics_b53_20261011/registry_schema_migration_comparison.csv)、[年度摘要](tables/76_ais_semantics_b53_20261011/registry_official_annual_summary.csv)、[品質與用途規則](tables/76_ais_semantics_b53_20261011/registry_quality_and_use_rules.csv)、[來源收據](tables/76_ais_semantics_b53_20261011/registry_source_receipts.csv)、[SQLite](tables/76_ais_semantics_b53_20261011/ais_semantics_b53.sqlite)。

## 接續施工與成本控制

先核逐用途權利；再選有界歷史時段與一般商船彙總樣本，串流讀取而非一次載入全年度。原字串、UTC、來源版本與缺值原因保留；合成測試與來源樣本驗證分開。以整檔CRC／雜湊、日期分區完整性、欄位數、時空及單位檢查、重複与空值率驗收，不用船名單獨認定法人或持有人。資料不可因記錄缺少而判定無船舶活動。

既有星盾、Grok／xAI、Meteomatics、ArcGIS與全部全球清單保留，未新增即時追蹤、武器目標或私有連線。本輪未驗證全量記錄品質、商用清關或全球覆蓋；SDG分析凍結，Untitled不恢復。
'''
(R/'Reference/AIS_Semantics_B53_20261011.qmd').write_text(report,encoding='utf-8')
original=(R/MAIN).read_bytes();append='\n\n<!-- AIS_SEMANTICS_B53_20261011_BEGIN -->\n## 2026-10-11 歷史AIS欄位與用途核對 B53\n\n新增[AIS年代化字典與品質報告](AIS_Semantics_B53_20261011.qmd)，34筆雙期欄位及17項映射；2019表頭核對通過，禁止套用2025新型別與範圍。官方FAQ品質／用途條件與年度規模保留，Token Required服務不冒充可取用；未下載全量或自動修正原始數值。\n<!-- AIS_SEMANTICS_B53_20261011_END -->\n'
(R/MAIN).write_bytes(original+append.encode('utf-8'))
(O/'append_receipt.json').write_text(json.dumps(dict(path=MAIN,prefix_bytes=len(original),prefix_sha256=sha(original),append_sha256=sha(append.encode('utf-8'))),indent=2),encoding='utf-8')
notes={'redteam':'新年代型別／有效域不可套舊資料；公共域標記不取消特定用途條件。','critic':'schema一致不代表27億记录质量驗證；圖層HTTP200內含499仍是受限。','killcritic':'年代化字典與差異映射讓錯單位、截字及錯套缺值可事前發現。','blindspot':'地面AIS不是全球衛星資料；名冊、船舶與時態識別不可混同。','blueprint':'逐用途權利→年代字典→有界歷史串流樣本→檔案完整性與缺值驗收→彙總研究。','cheatsheet':'2019用2018–2024字典；2025另表；原字串、UTC與缺值原因保存。','actionplan':'核具體研究用途後，以小型歷史商船彙總樣本驗schema、單位、空值與完整性。'}
for n,v in notes.items():(R/n/'ais_semantics_b53_20261011.md').write_text('# '+n+' | B53\n\n'+v+'\n\n[報告](../Reference/AIS_Semantics_B53_20261011.qmd)。\n',encoding='utf-8')
print(json.dumps(stats))
