"""Read-only projection and receipt semantics; retain old artifacts unchanged."""
from pathlib import Path
import csv,json,hashlib,sqlite3,collections
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
csv.field_size_limit(16*1024*1024)
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not (OUT/'validation.json').exists(),'Use a new batch'
old=ROOT/'reports/2026-10-07/incremental_contracts/incremental_field_contracts_v2.csv'
code=ROOT/'reports/2026-10-07/registry_contracts/build_contracts.py';sources={p:sha(p) for p in [old,code]}
projection={
 'iso_alpha2':'查詢投影採用的 ISO 國別／地區鍵，需按來源版本解讀',
 'name_en':'來源母表的展示英文名稱，非本批重新核實名稱',
 'candidate_entity_count':'該條目候選關聯表的行數，非已核實法律住所機構数',
 'candidate_any_scope_verified_count':'候選機構存在任意範圍 VERIFIED 主張的數量，不限公開描述',
 'candidate_public_description_only_count':'候選機構存在 VERIFIED 且 PUBLIC_DESCRIPTION_ONLY 主張的數量',
 'verified_country_relation_count':'該條目證據狀態為 VERIFIED 的國別關係行數，非候選機構總數',
 'country_frontier_capability_state':'原母表的國別能力核查狀態；UNKNOWN 不由機構數推定能力',
 'N0_N7_level':'原母表保留的神經科技分級欄；本快照全部 UNKNOWN，未作排名',
 'entity_id':'候選關聯所指的組織登記鍵，須連接其來源與身份狀態',
 'relation_state':'編輯國別候選關係標記，不認證法律住所或主權',
 'raw_country_list':'來源原始候選國別串，投影拆分時保留，不能推定法人國籍',
 'metric_id':'數值投影所指的原始指標行鍵，非通用指標定義鍵',
 'numeric_value':'原值经 Decimal／float 轉換的數值；空或無法轉換留缺值，非獨立量測',
 'unit':'原指標行所報單位，仍須核对量綱及口徑',
 'metric_name':'原指標名稱，不代表跨來源已可比較',
 'statistic':'原指標的統計或口徑描述，須連同條件返回',
 'conditions':'原指標適用測量條件文字，不可在比較時省略',
 'interpretation':'投影的來源報告／宣稱限制，非獨立 benchmark 證明'}
receipt={
 'path':'此回執記錄的來源或受檢文件相對路徑，按所屬回執判定',
 'sha256':'此回執時點的文件內容指紋，非現行事實核實標記',
 'bytes':'當批文件位元組數，非語義內容量或資料完整程度',
 'rows':'當批資料行數，非機構或主張核實總量',
 'columns':'當批表欄位數，非獨立業務概念總量',
 'family':'整合報告的編輯文件族標記，非來源證據等級',
 'target':'該整合批次的目標文件路徑，未授權今日覆寫',
 'snapshot':'當批來源保留快照路徑，須核對其指紋',
 'scope':'該回執的检查／交付範圍說明，不代表全項目事實已核實',
 'before_sha256':'此次歷史變更前的內容指紋，缺檔時可能空置',
 'after_sha256':'此次歷史變更後的內容指紋，不能代替今日現況核對',
 'before_snapshot':'此次變更前保留的來源快照路徑',
 'state':'两個歷史快照的增刪改分類，不自動推定改動原因',
 'untargeted_text_preserved':'該歷史修訂宣稱非目標文字保留的標記，仍受当批验证方法限定'}
inputs={'column_name':'提案所指的原始欄位名，須連同表／粒度解讀',
 'table':'定義提案的目標表名，不與同名跨批次表機械合併',
 'definition':'待審定義文字，不等於已批准合同',
 'proposed_definition':'待審定義文字，來源或審批状态須保留',
 'source_code_path':'定義提案引用的歷史生成程式路徑，不在本批執行'}
a=read(old);b=[dict(r) for r in a];changes=[]
for r in b:
    if r['definition_status']!='INCREMENTAL_FIELD_REVIEW_PENDING':continue
    role=r['role'];defs=projection if role=='DERIVED_QUERY_PROJECTION' else receipt if role=='PROVENANCE_RECEIPT' else inputs if role=='PROPOSED_DEFINITION_INPUT' else None
    if defs is None:continue
    p=ROOT/r['path'];sources[p]=sha(p);assert sha(p)==r['source_sha256'];c=r['column_name'];assert c in defs,c
    r['definition']=defs[c];r['definition_status']='CONTEXT_DEFINED_OWNER_REVIEW_REQUIRED'
    r['definition_locator']=code.relative_to(ROOT).as_posix()+'; projection SQL' if role=='DERIVED_QUERY_PROJECTION' else r['path']+'; recorded header and scoped receipt/input context'
    changes.append(dict(path=r['path'],column_name=c,definition=r['definition'],definition_locator=r['definition_locator'],business_approval='PENDING'))
assert len(changes)==73,len(changes)
remaining=[r for r in b if r['definition_status']=='INCREMENTAL_FIELD_REVIEW_PENDING'];assert len(remaining)==193
folder=ROOT/'reports/2026-10-07/registry_contracts';database=folder/'global_registry_b04_query.sqlite';sources[database]=sha(database)
with sqlite3.connect(database.as_uri()+'?mode=ro',uri=True) as db:
    db.row_factory=sqlite3.Row
    for name,table in [('country_evidence_coverage.csv','v_country_evidence_coverage'),('entity_country_candidates.csv','entity_country_candidates'),('metric_numeric_projection.csv','metric_numeric_projection')]:
        p=folder/name;raw=read(p);dbrows=[dict(r) for r in db.execute('select * from '+table)]
        # Compare unordered full rows; SQLite NULL corresponds to empty projection cell.
        normalize=lambda rows:sorted(tuple((k,'' if row[k] is None else str(row[k])) for k in sorted(row)) for row in rows)
        assert normalize(raw)==normalize(dbrows),name
    totals=dict(db.execute('select count(*) n,sum(candidate_entity_count) memberships,sum(candidate_any_scope_verified_count) any_scope,sum(candidate_public_description_only_count) description_only,sum(verified_country_relation_count) country_relations from v_country_evidence_coverage').fetchone())
for p,h in sources.items():assert sha(p)==h
for x,y in zip(a,b):
    for k in x:
        if k not in {'definition','definition_status','definition_locator'}:assert x[k]==y[k]
write('incremental_field_contracts_v3.csv',b);write('definition_changes.csv',changes);write('remaining_pending.csv',remaining)
write('source_manifest.csv',[dict(path=p.relative_to(ROOT).as_posix(),sha256=h) for p,h in sources.items()])
result=dict(pass_check=True,definitions_added=73,total_incremental_columns=703,remaining_pending=193,projection_csv_sqlite_full_rows='PASS',projection_totals=totals,source_files_unchanged=len(sources),business_approval='PENDING',current_facts_verified=False)
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
