"""Read-only source profiling and definition crosswalk; writes only this review folder."""
from pathlib import Path
import csv, json, hashlib, sqlite3, re, sys, collections
sys.stdout.reconfigure(encoding='utf-8'); csv.field_size_limit(16*1024*1024)
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent; OUT.mkdir(exist_ok=True,parents=True)
if (OUT/'semantic_catalog.sqlite').exists(): raise SystemExit('Existing delivered batch: use a new batch, do not overwrite.')
BASE=ROOT/'reports/2026-10-06/workspace_change_audit/semantics_20261007_start_files.csv'
expected={r['path']:r['sha256'] for r in csv.DictReader(BASE.open(encoding='utf-8-sig'))}
def sha(b): return hashlib.sha256(b).hexdigest()
def guarded(path):
    b=(ROOT/path).read_bytes()
    assert sha(b)==expected[path], 'Source changed: '+path
    return b
original=list(csv.DictReader((ROOT/'reports/2026-10-07/project_information_integration/column_catalog.csv').open(encoding='utf-8-sig')))
dictionary={ (r['table'],r['column']):r for r in csv.DictReader((ROOT/'DGEF/contracts/data_dictionary.csv').open(encoding='utf-8-sig')) }
defs={}
def define(names,meaning,value,unit='NOT_APPLICABLE'):
    for name in names.split(','): defs[name]=(meaning,value,unit)
define('entity_id,registry_entity_id','穩定內部實體識別鍵；命名空間及對象依所屬表，不以相似名稱自動合併','跨表實體追溯')
define('source_id','來源登記鍵；僅指來源，不代表該來源全部說法已核實','主張證據追溯')
define('claim_id','一項可定位主張的識別鍵；真偽與有效範圍另列','主張審核與衝突管理')
define('dataset_id','資料集登記鍵；版本與來源由資料集表限定','重現加工輸入')
define('technology_id,product_project_leads','技術記錄鍵或產品／項目候選線索；候選不等於正式實體','技術選型與後續查證')
define('evidence_state,claim_status,verification_status','特定記錄或主張的證據狀態；VERIFIED 僅限可定位範圍','隔離未知、宣稱與核實')
define('verification_scope,verified_scope','核實涵蓋的主張、條件與邊界；不把公開描述擴展成性能或部署證明','限定決策可信範圍')
define('performance_state,independent_performance_state','性能主張或獨立性能驗證狀態；不是性能數值','避免宣傳數字冒充測試')
define('deployment_state,independent_deployment_state','部署證據狀態；產品存在不等於實際部署','採用成熟度評估')
define('regulatory_state,regulatory_jurisdiction','監管狀態或其司法區；版次與日期需另定位','臨床／採購條件評估')
define('license_state,license_review,training_permission','授權審核狀態；需定位產品／資料／权重與版本','用途准入')
define('commercial_use_allowed,ml_training_allowed,redistribution_allowed','特定授權政策下的商用／訓練／再散布許可；NULL 不當 FALSE 或 TRUE','使用權限決策','BOOLEAN_OR_NULL')
define('iso_alpha2,country_iso_alpha2','ISO 3166-1 alpha-2 國家／地區代碼；代碼版次與關係另記','母表連結','ISO_ALPHA2')
define('iso_alpha3,country_iso_alpha3','ISO 3166-1 alpha-3 國家／地區代碼；不直接判主權','國別對照','ISO_ALPHA3')
define('country_candidate_iso_alpha2','編輯候選國別關聯；不直接證明法律住所、部署國或國家能力','國別查證候選','ISO_ALPHA2_CANDIDATE')
define('country_frontier_capability_state,N0_N7_level','國家能力或神經技術分級狀態；缺測試定義或證據維持 UNKNOWN','防止無證據國別排名')
define('legal_entity_status,legal_domicile_state,country_assignment_status,country_relation_state','法人、住所或國別關係的獨立核實狀態；與機構存在不同','法人與地理歸屬核實')
define('origin_batch,review_batch','資料首次引入或本次審核的批次標識；不同快照不能直接累加','版本與批次去重')
define('valid_from,valid_to','現實關係／記錄的有效起訖；未知終止時間留空，不當已終止','歷史狀態重建','SOURCE_DATE_OR_TIMESTAMP')
define('transaction_time','資料系統記錄時間；與現實事件發生時間不同','雙時間追溯','SOURCE_TIMESTAMP')
define('as_of,checked_on,reviewed_on,searched_on,retrieved_at,reviewed_at,checked_at','資料截至／檢查／審核／搜索／取得時間；各欄依操作分別解讀，時區不可猜','新鮮度與審核時點','SOURCE_DATE_OR_TIMESTAMP')
define('information_bandwidth_bits_per_second','資訊帶寬測量值；需協議、任務、噪音、樣本與誤差，未公開留空','可比較訊號傳輸能力','bits/s')
define('bandwidth_protocol','資訊帶寬測試協議或方法；沒有方法不能直接比較數值','測量可重現')
define('invasiveness','介面侵入性分類；需具體植入／介入部位與程序證據','技術風險與成熟度')
define('modality','量測／刺激模態，例如 EEG、ECoG、微電極、fNIRS、TMS；不能等同功能證明','技術分類')
define('signal_direction','讀取、寫入或雙向功能；需任務與人體／動物等條件','能力方向比較')
define('remote_state','遠端相關主張狀態；網路存取與距離腦訊號量測分別核實','防止遠端概念混用')
define('human_trial_state,clinical_phase,trial_registry_status','人體試驗證據、臨床階段或登記狀態；試驗登記不等於結果或許可','臨床成熟度')
define('publication_ids,patent_ids,trial_ids','文獻、專利或試驗識別碼集合；取得識別碼不代表正文已審','證據回溯')
define('world_domain','REAL-TWIN／HISTORY／SIM／FICTION 世界域；仍需具體觀測與現實性標籤','隔離真實、歷史、模擬与虛構')
define('world_frontier_rank_state,global_rank_state','排名主張的核實狀態；先定義樣本、指標與比較協議','比較口徑治理')
define('frame_id,spatial_frame','座標參考系識別或描述；必須與中心、軸向、單位與時間一致','空間數據可比較')
define('epoch,time_scale','觀測曆元或時間尺度；UTC／TDB 等不機械混換','時空一致性','SOURCE_DEFINED')
define('x,y,z,vx,vy,vz','指定參考系與曆元下的向量分量；單位從 position_unit／velocity_unit 取得','軌道與位置計算','REFER_TO_UNIT_COLUMN')
define('position_unit,velocity_unit,unit','值的單位；不能從欄名或數值大小猜測單位','避免量綱錯誤','UNIT_LABEL')
define('numerator,denominator','指標分子／分母；母體、時間與排除規則須明確，未知分母留空','覆盖與比例評估')
define('match_score','候選實體匹配分數；不是事實機率，不自動授權合併','人工復核優先序')
define('match_method,match_basis','身份／名稱匹配的方法或依據；須保留可重現條件','關係驗證')
define('content_hash,file_sha256,sha256','內容指紋；完整性核對不能證明內容真實','版本與變更定位','HASH')
define('record_payload,raw_json,baseline_json','原始資料或基線的序列化內容；保留來源粒度与授權，不能公開當作已審結果','原文無損與重現','JSON_OR_SOURCE_TEXT')
define('external_id,external_key,id_system,external_version','外部識別碼、命名空間或其版本；外部ID必須帶來源與版本','避免跨庫串號')
define('ingest_id,transform_version','接入記錄鍵或轉換程式版本；連結來源与加工過程','加工血緣')
define('row_count,bytes','記錄列數或位元組數；不代表機構、資訊或成果數','完整性与儲存規劃','ROW_OR_BYTE_BY_COLUMN')
define('query,provider','搜索查詢或其提供方；搜索完成不等於世界普查完成','搜索覆蓋可重現')
define('url,canonical_uri,primary_url,evidence_url,source_file,source_line','來源位址、檔案或行號；連結存在不代表內容可讀或支持主張','證據定位')
define('claim,original_claim','一項待審或歷史主張的文字；與其證據狀態一起使用','保存研究命題')
define('search_state,research_completion_state','搜索操作或研究完成狀態；不等於國家能力或完整母體覆蓋','工作進度治理')
db=sqlite3.connect((ROOT/'DGEF/artifacts/dgef.sqlite').as_uri()+'?mode=ro',uri=True)
assert db.execute('pragma integrity_check').fetchone()[0]=='ok'; assert not db.execute('pragma foreign_key_check').fetchall()
schemas={}; tablecounts=[]
for (name,) in db.execute("select name from sqlite_master where type='table'"):
    schemas[name]={x[1]:x for x in db.execute('pragma table_info("'+name+'")')}
    tablecounts.append(dict(table=name,rows=db.execute('select count(*) from "'+name+'"').fetchone()[0]))
fields=[]; cards=[]; problems=[]
for path in sorted({r['path'] for r in original}):
    raw=guarded(path); role='PREVIEW_SNAPSHOT' if '/preview/' in path else 'HISTORICAL_REPORT_OUTPUT' if path.startswith('reports/') else 'DGEF_EXPORT' if path.startswith('DGEF/artifacts/') else 'REFERENCE_DATA' if path.startswith('Reference/tables/') else 'OTHER'
    try:
        import io
        records=list(csv.reader(io.StringIO(raw.decode('utf-8-sig'),newline=''),delimiter='\t' if path.endswith('.tsv') else ',')); header=records[0]; data=records[1:]
    except Exception as e:
        problems.append(dict(path=path,kind='PARSE_ERROR',details=type(e).__name__)); continue
    table=Path(path).stem; grain=next((v['grain'] for (t,c),v in dictionary.items() if t==table),'REVIEW_REQUIRED')
    for index,col in enumerate(header):
        vals=[r[index] if index<len(r) else '' for r in data]; nonblank=[v for v in vals if v.strip()]; inherited=dictionary.get((table,col)) if role=='DGEF_EXPORT' else None
        definition,value,unit=defs.get(col,('尚未完成欄位語義核實；需來源業務定義、單位、粒度與用途','待資料負責人確認','UNKNOWN'))
        status='PROPOSED_CONTEXT_REVIEW' if col in defs else 'UNRESOLVED'
        locator='build_semantic_catalog.py: explicit proposed glossary' if col in defs else ''
        if inherited and col not in defs:
            definition=inherited['business_definition']; locator='DGEF/contracts/data_dictionary.csv: '+table+'.'+col
            status='DOCUMENTED_GENERIC_REVIEW' if '定义受所属表粒度' in definition else 'DOCUMENTED_CONTEXT_REVIEW'
        sql=schemas.get(table,{}).get(col) if role=='DGEF_EXPORT' else None
        if '\ufffd' in col: problems.append(dict(path=path,kind='HEADER_ENCODING_DAMAGE',details='column '+str(index+1)))
        fields.append(dict(path=path,table=table,column_index=index+1,column_name=col,role=role,source_sha256=sha(raw),row_count=len(data),blank_count=len(vals)-len(nonblank),distinct_nonblank=len(set(nonblank)),definition=definition,definition_status=status,definition_locator=locator,grain=grain,business_value=value,unit=unit,sql_type=sql[2] if sql else 'NOT_ESTABLISHED',sql_not_null=sql[3] if sql else '',sql_primary_key=sql[5] if sql else '',null_policy='UNKNOWN_NOT_APPLICABLE_OR_NOT_RECORDED; DO_NOT_IMPUTE_ZERO',owner='UNASSIGNED',value_evaluation='PROPOSED_NO_MEASURED_ROI'))
    cards.append(dict(path=path,source_sha256=sha(raw),role=role,rows=len(data),columns=len(header),grain=grain,decision_use='實體／主張／證據追溯' if role in ('DGEF_EXPORT','REFERENCE_DATA') else '歷史版本與加工可重現',value_basis='qualitative proposal; not measured benefit',eligible_for_cross_batch_sum='NO',owner='UNASSIGNED',review_state='REVIEW_REQUIRED'))
def output(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
output('field_semantics.csv',fields); output('data_value_cards.csv',cards); output('dgef_table_counts.csv',tablecounts)
if problems: output('quality_issues.csv',problems)
counts=dict(collections.Counter(x['definition_status'] for x in fields)); roles=dict(collections.Counter(x['role'] for x in fields))
receipt=dict(head='20439fb820a835b4f1d3a9007b1064ee3819cb79',input_table_files=len(cards),field_records=len(fields),prior_catalog_records=len(original),definition_status_counts=counts,role_counts=roles,dgef_tables=len(schemas),dgef_integrity='ok',dgef_foreign_key_errors=0,parse_errors=sum(x['kind']=='PARSE_ERROR' for x in problems),header_encoding_issues=sum(x['kind']=='HEADER_ENCODING_DAMAGE' for x in problems),recovered_ingest_rows=next(x['rows'] for x in cards if x['path'].endswith('/registry_ingest_record.csv')),external_fact_review='SCOPED',business_definitions_owner_approved=False)
for path in {r['path'] for r in original}: guarded(path)
catalog=OUT/'semantic_catalog.sqlite'
if catalog.exists(): raise SystemExit('Existing catalog: refuse overwrite; use new batch')
with sqlite3.connect(catalog) as target:
    for table,rows in [('field_semantics',fields),('data_value_cards',cards),('dgef_table_counts',tablecounts)]:
        target.execute('create table '+table+' ('+','.join('"'+k+'" TEXT' for k in rows[0])+')')
        target.executemany('insert into '+table+' values ('+','.join('?' for _ in rows[0])+')',[tuple(str(v) for v in r.values()) for r in rows])
    target.execute('create unique index field_identity on field_semantics(path,column_index)')
    assert target.execute('pragma integrity_check').fetchone()[0]=='ok'
(OUT/'validation.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(receipt,ensure_ascii=False,indent=2))
