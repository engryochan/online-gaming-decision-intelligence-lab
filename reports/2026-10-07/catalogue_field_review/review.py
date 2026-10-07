"""Verify UTF-8 headers and define ten catalogue/lead fields without source edits."""
from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
csv.field_size_limit(16*1024*1024)
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);return reader.fieldnames,list(reader)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not (OUT/'validation.json').exists(),'Use a new batch'
old=ROOT/'reports/2026-10-07/country_layer_contracts/field_semantics_v6.csv'
_,a=read(old);b=[dict(r) for r in a];sources={old:sha(old)}
gaming=list((ROOT/'Reference/tables/04_gaming_catalogue').glob('*.csv'));assert len(gaming)==1
p=gaming[0];text=p.read_bytes().decode('utf-8-sig',errors='strict');assert '\ufffd' not in text
header,data=read(p);assert header==['序号','游戏','官方出处','处理结果','安装包已下载']
defs={'序号':'本地遊戲清單行序號，不是永久實體識別鍵',
      '游戏':'本地登記的遊戲名稱；不代表已取得授權或安裝包',
      '官方出处':'清單記錄的官方來源連結；本批未重新核實內容與授權',
      '处理结果':'歷史處理過程與限制說明；不當作當前可用性認證',
      '安装包已下载':'歷史下載狀態標記；不代表本批已查驗檔案存在或可執行'}
lead_defs={'lead_id':'國別搜尋回應行的批次鍵；由查詢國別與回應序號生成，不是機構鍵',
 'title':'搜尋提供方返回的頁面標題；非官方組織規範名稱',
 'country_relationship_state':'搜尋命中的國別關係審核狀態；UNREVIEWED_SEARCH_RESULT 不建立國別歸屬',
 'relevance_state':'搜尋結果相關性狀態；UNKNOWN_MAY_BE_IRRELEVANT 保留不相關可能',
 'notes':'歷史產品／計劃線索限定說明；複合研究詞不升級為已核實產品登記'}
generator=ROOT/'reports/2026-10-06/global_technology_iso249/build_global_registry.py';sources[generator]=sha(generator)
changes=[]
for r in b:
    if r['role']!='REFERENCE_DATA' or r['definition_status']!='UNRESOLVED':continue
    c=r['column_name'];source=ROOT/r['path']
    isgaming=source==p
    islead=r['table'] in {'registry_country_search_leads','registry_legacy_product_project_leads'}
    if not isgaming and not islead:continue
    definition=defs[c] if isgaming else lead_defs[c]
    sources[source]=sha(source);assert sha(source)==r['source_sha256']
    source_header,source_rows=read(source);assert source_header[int(r['column_index'])-1]==c
    assert len(source_rows)==int(r['row_count'])
    r['definition']=definition;r['definition_status']='CONTEXT_DEFINED_OWNER_REVIEW_REQUIRED'
    r['definition_locator']=r['path']+':1; header and row context' if isgaming else generator.relative_to(ROOT).as_posix()+'; leads construction and legacy lead notes'
    changes.append(dict(path=r['path'],column_name=c,definition=definition,definition_locator=r['definition_locator'],owner_approval='PENDING'))
assert len(changes)==10
for x,y in zip(a,b):
    if x!=y:assert {k for k in x if x[k]!=y[k]}=={'definition','definition_status','definition_locator'}
assert sum(x!=y for x,y in zip(a,b))==10
remaining=[r for r in b if r['definition_status']=='UNRESOLVED'];assert len(remaining)==292
for source,h in sources.items():assert sha(source)==h
write('field_semantics_v7.csv',b);write('definition_changes.csv',changes);write('remaining_unresolved.csv',remaining)
write('source_manifest.csv',[dict(path=source.relative_to(ROOT).as_posix(),sha256=h) for source,h in sources.items()])
result=dict(pass_check=True,definitions_added=10,unresolved=292,unchanged_records=1979,gaming_header=header,gaming_utf8_replacement_characters=0,gaming_rows=len(data),source_files_unchanged=len(sources),current_products_or_license_facts='NOT_REVERIFIED',business_approval='PENDING')
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=True))
