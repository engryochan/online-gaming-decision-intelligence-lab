"""Finish the fixed 703-column review boundary, without recursive new-output claims."""
from pathlib import Path
import csv,json,hashlib,collections
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
csv.field_size_limit(16*1024*1024)
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not (OUT/'validation.json').exists(),'Use a new batch'
old=ROOT/'reports/2026-10-07/review_artifact_contracts/incremental_field_contracts_v4.csv';sources={old:sha(old)}
defs={
 'path':'摘要或追溯記錄所描述的歷史來源文件路徑，按表用途限定',
 'rows':'摘要所述來源表當批行數，不表示已核實機構數',
 'unique_registry_ids':'該歷史表內 registry_id 唯一性檢查標記，不代表跨批次实体已消歧',
 'counted_field':'此摘要計數所採用的來源欄位名',
 'counts_json':'指定來源欄位原值的頻數 JSON，不自動構成事实核實統計',
 'table':'摘要對照的來源表名，須連同来源版本限定',
 'columns':'摘要所述來源表欄位數，非獨立概念数',
 'proposed_replacements':'本表提出替換通用定義的欄位數，非已批准數',
 'status':'所屬摘要的局部狀態分類，須依 counted_field 或定義上下文判讀',
 'records':'該摘要指定狀態的記錄頻數，非現實實體總數',
 'unique_iso_alpha2':'本地母表唯一國別鍵數，非今日官方清單認證',
 'blank_official_name':'本地母表正式英文名稱空字串行數，不表示正式名不存在',
 'asset_id':'由資產路徑雜湊截取得的索引鍵，非內容永久身份或法人鍵',
 'sha256':'被索引文件的當批内容指紋，非真實性證明',
 'bytes':'被索引文件位元組數，非資料覆蓋程度',
 'role':'該資產或摘要採用的資料用途角色，非证据等级',
 'family':'編輯報告文件族，非獨立證據來源等級',
 'canonical_target':'该整合批次定位的目標報告，非今日覆寫授權',
 'business_value_proposal':'當批用途提案，非已測收益',
 'definition_status':'資產／欄位定義審閱狀態，非事实核實狀態',
 'source':'整合覆蓋追溯的原始來源文件',
 'source_line':'原始來源區塊的历史起始行號，後续編輯可能移動',
 'block_sha256':'原始文本區塊的內容指紋，用於覆蓋比對，不验证主張',
 'characters':'原始文本區塊字符數，不是位元組數或資訊價值',
 'state':'該区塊在整合批次已覆蓋或附加的記錄狀態，非 VERIFIED',
 'target':'该區塊所在的整合目標文件路徑',
 'source_snapshot':'当批保留的原始來源快照，不表示今日現況',
 'redacted_display':'區塊顯示文字是否與原文因遮蔽而不同；原始快照另外保留',
 'preview_path':'字典沿用定義時比對的預覽文件路徑',
 'reference_path':'比對的 Reference 文件路徑，仍受該批內容版本限定',
 'column_name':'沿用定義時對應的原欄位名，須核對位置與文件内容',
 'proof':'當批沿用定義所採用的比對證明，不代表業務已批准',
 'source_definition_status':'沿用來源定義當時的成熟度，不隨後版自动刷新',
 'git_status':'當批 Git 提供的變更／改名分類，啟發式相似不證明同一來源',
 'old_path':'舊版或已搬移來源的路徑，不授權恢復文件',
 'current_path':'當批定位的現行／候選路徑，須與對照依據合讀',
 'old_sha256':'舊版對照文件内容指紋',
 'current_sha256':'當批現行／候選文件内容指紋，不代表今後一直相同',
 'byte_identical':'完整原位元內容是否相同；False 不直接代表資訊遺漏',
 'text_equal_after_newline_normalization':'按當批方法規範化換行後的文字等值，非位元相同',
 'mapping_basis':'來源路徑對照的記錄依據，不將 Git 猜測自动升級为確定映射',
 'claim_id':'所屬審閱批次的主張鍵，不代表全球永久主張身份',
 'baseline_sha256':'該主張定位所對照的歷史基線内容指紋',
 'baseline_line':'該主張在歷史基線的定位行號，非今日行號',
 'baseline_snapshot':'保留的歷史基線快照路徑',
 'match_state':'主張文字在基線中的匹配分類，不證明語義真實',
 'topic':'該批受檢主張的編輯主題',
 'statement':'该批受檢主張文字，須與證據與範圍合讀',
 'evidence_state':'该批主張審阅的證據狀態，不扩展到未審閱部分',
 'verification_scope':'該主張的核實范围与限制，不可在引用時省略',
 'primary_url':'受檢主張引用的一手來源 URL，不保證今日可達',
 'locator':'受檢主張的來源定位說明',
 'reviewed_on':'该批審阅日期，非永續有效核實',
 'source_body_snapshot':'該批保存的來源正文／摘錄快照，不自动等于完整原始 HTTP',
 'reviewer':'該批審閱者標記，不取代業務批准與部署权限',
 'source_sha256':'來源表当批内容指紋',
 'grain':'來源表記錄粒度提案，须另審實際口徑',
 'decision_use':'该資料的預期決策用途，不是已驗證效果',
 'value_basis':'用途價值評估基礎文字，非已測收益',
 'eligible_for_cross_batch_sum':'是否允許跨批次加總的記錄標記；NO 防止版本重複計數',
 'owner':'資料負責人標記；UNASSIGNED 保留未指派',
 'review_state':'用途或資料審閱状态，非来源事实证据状态',
 'version':'服務名錄的歷史版本標籤，不是現行網站版本',
 'V':'該歷史版本 V 狀態行數，須連同核實範圍，不作全面 VERIFIED 機構數',
 'P':'該歷史版本 P 狀態行數，保留限定與待決',
 'U':'該歷史版本 U 狀態行數，未知不等於不存在',
 'cumulative_log_rows':'相對原基線的累積修訂行數，非相鄰版本新增數',
 'ids_and_unlogged_rows_preserved':'该批 ID／未列日志原行保全檢查標記，非來源事實驗證',
 'log_base_and_target_matches':'累積日志與原基線及目标版對照的檢查標記，非性能認證'}
a=read(old);b=[dict(r) for r in a];changes=[]
for r in b:
    if r['definition_status']!='INCREMENTAL_FIELD_REVIEW_PENDING':continue
    p=ROOT/r['path'];sources[p]=sha(p);assert sha(p)==r['source_sha256'];c=r['column_name'];assert c in defs,c
    r['definition']=defs[c];r['definition_status']='PROPOSED_REVIEW_ARTIFACT_CONTEXT';r['definition_locator']=r['path']+'; source header and scoped artifact interpretation; owner review required'
    changes.append(dict(path=r['path'],column_name=c,definition=defs[c],definition_locator=r['definition_locator'],business_approval='PENDING'))
assert len(changes)==94 and len(b)==703
for x,y in zip(a,b):
    for k in x:
        if k not in {'definition','definition_status','definition_locator'}:assert x[k]==y[k]
assert not any(r['definition_status']=='INCREMENTAL_FIELD_REVIEW_PENDING' for r in b)
for p,h in sources.items():assert sha(p)==h
write('incremental_field_contracts_v5.csv',b);write('definition_changes.csv',changes)
write('source_manifest.csv',[dict(path=p.relative_to(ROOT).as_posix(),sha256=h) for p,h in sources.items()])
counts=collections.Counter(r['definition_status'] for r in b)
write('definition_status_summary.csv',[dict(status=k,records=v) for k,v in sorted(counts.items())])
result=dict(pass_check=True,definitions_added=94,total_incremental_columns=703,remaining_pending=0,definition_status_counts=dict(counts),source_files_unchanged=len(sources),business_approval='PENDING',all_facts_verified=False,scope='FIXED_71_ARTIFACT_BOUNDARY_ONLY')
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
