"""Define metadata columns separately from the business fields they describe."""
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
old=ROOT/'reports/2026-10-07/incremental_catalogue_review/incremental_column_catalogue.csv'
schema_source=ROOT/'reports/2026-10-07/semantic_evidence_review/build_semantic_catalog.py'
queue_source=ROOT/'reports/2026-10-07/governance_field_contracts/review.py'
sources={p:sha(p) for p in [old,schema_source,queue_source]}
semantic={'path':'目錄所描述資料表的歷史相對路徑，不是這份目錄自身的文件路徑',
 'table':'目錄所描述的表名；跨批次以 path 限定，不僅靠同名表連接',
 'column_index':'被描述表的欄位位置，從 1 起算，非实体順序',
 'column_name':'被描述表的原欄名，不代表欄位業務意義已批准',
 'role':'被描述來源表的資料角色分類，不是對象核實等級',
 'source_sha256':'被描述來源文件當批內容指紋，用來判斷版本漂移',
 'row_count':'被描述來源表的當批資料行數，不等於機構總數',
 'blank_count':'被描述欄位讀取值為空字串的行數；不自動等於所有 SQL NULL 原因',
 'distinct_nonblank':'當批非空原值的不同字串數，不等於獨立實體數',
 'definition':'當版記錄的欄位定義或提案文字，須合讀定義狀態',
 'definition_status':'當版定義成熟度及待審狀態，不是來源現實主張證據狀態',
 'definition_locator':'定義來源定位與方法說明；存在定位不等於業務批准',
 'grain':'被描述表的記錄粒度或待确认口徑',
 'business_value':'被描述欄位的業務用途提案，不是已測 ROI',
 'unit':'被描述欄位的單位標記或未知／不適用描述',
 'sql_type':'被描述欄位的 SQL 型別或 NOT_ESTABLISHED；不能據此强轉數值',
 'sql_not_null':'已建立 schema 時的 NOT NULL 宣告標記，未知留空',
 'sql_primary_key':'已建立 schema 時的主鍵序位，未知留空，不等於法人身份認證',
 'null_policy':'被描述資料的未知／不適用／未記錄及禁止補零說明',
 'owner':'定義或資料的負責人標記；UNASSIGNED 表示尚未指派',
 'value_evaluation':'業務價值評估成熟度標記，PROPOSED_NO_MEASURED_ROI 不代表已量測收益',
 'business_definition_status':'舊 column_catalog 的定義審閱狀態，不與後版狀態機械等同',
 'business_definition':'舊 column_catalog 的原始定義／需確認文字，保留其版本範圍'}
queue={'iso_alpha2':'待核查條目的 ISO 兩字母代碼，不代表本隊列重新核實官方清單',
 'iso_alpha3':'同一待核查條目的三字母代碼',
 'historical_status':'從歷史母表保留的元首資料狀態，非今日認證',
 'historical_verification_as_of':'歷史母表聲稱的核查截止日，不以本輪日期替代',
 'historical_power_model_eligible':'歷史母表的模型候選範圍標記，不授權訓練',
 'review_status':'此證據工作隊列的待審處理狀態，不是主張已核實',
 'required_evidence':'預期需取得的官方證據清單，不表示已取得',
 'current_holder_verified':'本隊列對現任人物核實標記；當批均 UNKNOWN',
 'current_power_verified':'本隊列對當前權限核實標記；當批均 UNKNOWN',
 'training_permission':'本隊列的權限邊界說明，不取代來源訓練许可評估'}
a=read(old);b=[dict(r,definition_locator='',business_approval='PENDING') for r in a];changes=[]
for r in b:
    if r['role'] not in {'SEMANTIC_CATALOGUE_OR_VERSION','PENDING_EVIDENCE_QUEUE'}:continue
    p=ROOT/r['path'];sources[p]=sha(p);assert sha(p)==r['source_sha256']
    defs=semantic if r['role']=='SEMANTIC_CATALOGUE_OR_VERSION' else queue
    c=r['column_name'];assert c in defs,c
    r['definition']=defs[c];r['definition_status']='CONTEXT_DEFINED_OWNER_REVIEW_REQUIRED'
    r['definition_locator']=(schema_source if defs is semantic else queue_source).relative_to(ROOT).as_posix()+'; schema construction and source header'
    changes.append(dict(path=r['path'],column_name=c,definition=r['definition'],definition_locator=r['definition_locator'],business_approval='PENDING'))
assert len(changes)==437,len(changes)
assert len(b)==703
for x,y in zip(a,b):
    for k in x:
        if k not in {'definition','definition_status'}:assert x[k]==y[k]
remaining=[r for r in b if r['definition_status']=='INCREMENTAL_FIELD_REVIEW_PENDING'];assert len(remaining)==266
for p,h in sources.items():assert sha(p)==h
write('incremental_field_contracts_v2.csv',b);write('definition_changes.csv',changes);write('remaining_pending.csv',remaining)
write('source_manifest.csv',[dict(path=p.relative_to(ROOT).as_posix(),sha256=h) for p,h in sources.items()])
result=dict(pass_check=True,incremental_columns=703,definitions_added=437,remaining_pending=266,source_files_unchanged=len(sources),business_approval='PENDING',all_facts_verified=False,new_organizations=0)
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
