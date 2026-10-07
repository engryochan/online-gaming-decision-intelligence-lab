"""Define review deltas, SQL contracts and hypothetical tests; leave other roles pending."""
from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
csv.field_size_limit(16*1024*1024)
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not (OUT/'validation.json').exists(),'Use a new batch'
old=ROOT/'reports/2026-10-07/projection_contracts/incremental_field_contracts_v3.csv'
sources={old:sha(old)}
defs={
 'path':'此審閱記錄所描述的來源表／文件路徑，非審閱表自身路徑',
 'table':'合同／提案所描述的表名，須連同來源路徑限定',
 'column_name':'合同／修訂所描述的原始欄位名',
 'column':'合同所描述的原始欄位名',
 'previous_definition':'修訂前的定義文字，保存歷史不自動推定錯誤',
 'proposed_definition':'本批提出的待審定義文字，非已批准合同',
 'definition':'本批記錄的定義或上下文文字，須合讀定義狀態',
 'definition_locator':'本批定義引用的來源定位或解讀方法，非批准證明',
 'definition_status':'合同的定義成熟度與審閱狀態，不是現實主張證據狀態',
 'previous_status':'修訂前的定義狀態，非機構能力狀態',
 'proposed_status':'定義修訂後提出的狀態，非業務已批准或事实已核实',
 'owner_approval':'業務負責人審批狀態；PENDING 不當作已批准',
 'business_approval':'業務審批狀態，與結構校驗通過分開',
 'current_facts':'本批是否重新核實現實事實的範圍標記',
 'external_fact_reverification':'本批外部事實重新驗證範圍，不由有定義推定已核',
 'current_fact_verification':'本批現行事實核查標記，NOT_PERFORMED 保留未核',
 'facts_verified':'本批事實驗證範圍標記，不代表審閱表各行全部真實',
 'current_external_fact_verification':'本批現行外部事實驗證標記，未執行不升級为核實',
 'current_external_facts':'本批外部現況核查範圍標記',
 'fact_reverification':'本批來源事實重新核查範圍標記',
 'grain':'合同採用的來源表記錄粒度，仍需業務確認',
 'sql_type':'核對來源 SQL schema 的宣告型別，非業務有效性證明',
 'declared_not_null':'PRAGMA 的 NOT NULL 宣告標記，不拒绝所有空字串',
 'primary_key_position':'PRAGMA 中的主鍵序位，不是身份核實標記',
 'foreign_key_targets':'JSON 記錄的來源 schema 外鍵目的表與欄位，不证明現實关系真實',
 'table_ddl':'來源表 CREATE TABLE 文字；不包含所有 trigger 或部署权限',
 'null_policy':'合同的空值與未知處理說明，禁止補零不代替全部缺值原因',
 'business_value_proposal':'定義或資料用途提案，不是已測收益',
 'business_value':'欄位用途提案，不是 ROI 測量',
 'owner':'資料／定義負責人標記，UNASSIGNED 表示未指派',
 'source_csv_sha256':'來源 CSV 在該批核對時的內容指紋',
 'source_database_sha256':'來源数据库在該批核對時的內容指紋',
 'source_sha256':'來源文件的當批內容指紋，非真實性證明',
 'unit':'來源欄位單位或未定／不適用標記，不直接强轉數值',
 'primary_key':'合同標記的來源主鍵信息，不證明法律身份',
 'status':'合同的審阅／定義狀態，不是源主張證據狀態',
 'basis':'合同定義的文件／方法依據，不直接賦予證據品質等級',
 'source_path':'合同追溯的来源表路徑',
 'row_count':'来源資料表在該批的行數，不是新機構數',
 'blank_count':'来源欄位當批空字串數，不代替完整缺值語義',
 'case':'記憶體副本控制測試的案例名，非現行資料違規記錄',
 'legacy_selected':'假設許可及單欄變更後，原視圖是否選入該測試行',
 'review_selected':'相同測試条件下候選篩選 SQL 是否選入該行',
 'expected_review':'測試設計預期的候選選入結果，不是人工訓練授權',
 'pass_check':'实际候選结果是否符合该測試預期，不是全部生產安全驗收'}
a=read(old);b=[dict(r) for r in a];changes=[]
for r in b:
    if r['definition_status']!='INCREMENTAL_FIELD_REVIEW_PENDING':continue
    name=Path(r['path']).name
    if name not in {'definition_changes.csv','field_contracts.csv','control_tests.csv'}:continue
    p=ROOT/r['path'];sources[p]=sha(p);assert sha(p)==r['source_sha256'];c=r['column_name'];assert c in defs,c
    r['definition']=defs[c];r['definition_status']='PROPOSED_REVIEW_ARTIFACT_CONTEXT';r['definition_locator']=r['path']+'; scoped header and artifact purpose; owner review required'
    changes.append(dict(path=r['path'],column_name=c,definition=defs[c],definition_locator=r['definition_locator'],business_approval='PENDING'))
assert len(b)==703
for x,y in zip(a,b):
    for k in x:
        if k not in {'definition','definition_status','definition_locator'}:assert x[k]==y[k]
remaining=[r for r in b if r['definition_status']=='INCREMENTAL_FIELD_REVIEW_PENDING']
assert len(changes)+len(remaining)==193
for p,h in sources.items():assert sha(p)==h
write('incremental_field_contracts_v4.csv',b);write('definition_changes.csv',changes);write('remaining_pending.csv',remaining)
write('source_manifest.csv',[dict(path=p.relative_to(ROOT).as_posix(),sha256=h) for p,h in sources.items()])
result=dict(pass_check=True,definitions_added=len(changes),remaining_pending=len(remaining),total_incremental_columns=703,source_files_unchanged=len(sources),business_approval='PENDING',current_facts_verified=False)
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
