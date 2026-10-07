"""Propagate definitions only after byte equality; define dictionary metadata."""
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
old=ROOT/'reports/2026-10-07/governance_field_contracts/field_semantics_v8.csv'
a=read(old);b=[dict(r) for r in a];index={(r['path'],r['column_name']):r for r in a}
defs={'table':'資料字典所描述的 SQL 表名，不是該行自身的業務實體',
 'table_name_zh':'SPECS 中的表中文名稱，供字典顯示',
 'grain':'SPECS 中宣告的表記錄粒度；須與實際約束及資料合讀',
 'column':'資料字典所描述的 SQL 欄位名稱',
 'sql_type':'生成時 PRAGMA table_info 返回的 SQL 宣告型別',
 'not_null':'生成時 PRAGMA table_info 的 NOT NULL 宣告標記，不保證業務值有效',
 'primary_key':'生成時 PRAGMA table_info 的主鍵序位，非現實身份核實標記',
 'null_semantics':'生成器共用的未知／不適用及禁止補零說明，不是每個欄位完整缺值原因',
 'business_definition':'field_definition 函數輸出的定義文字，可能仍是通用說明',
 'example_use':'本生成器實際複製表粒度文字，不是獨立應用案例或已測效益'}
manifest={old:sha(old)};changes=[];aliases=[]
fabric=ROOT/'DGEF/fabric.py';manifest[fabric]=sha(fabric)
assert 'example_use=SPECS[name][2]' in fabric.read_text(encoding='utf-8-sig')
for r in b:
    if r['definition_status']!='UNRESOLVED':continue
    p=ROOT/r['path']
    if r['role']=='PREVIEW_SNAPSHOT':
        current=r['path'].split('/preview/',1)[1];q=ROOT/current
        assert p.read_bytes()==q.read_bytes()
        source=index[current,r['column_name']];assert source['definition_status']!='UNRESOLVED'
        assert r['column_index']==source['column_index']
        r['definition']=source['definition'];r['definition_status']=source['definition_status']
        r['definition_locator']='BYTE_IDENTICAL_COPY_OF '+current+'; '+source['definition_locator']
        manifest[q]=sha(q);aliases.append(dict(preview_path=r['path'],reference_path=current,column_name=r['column_name'],sha256=sha(p),proof='FULL_FILE_BYTE_EQUALITY',source_definition_status=source['definition_status']))
    elif r['path']=='DGEF/contracts/data_dictionary.csv':
        r['definition']=defs[r['column_name']];r['definition_status']='CONTEXT_DEFINED_OWNER_REVIEW_REQUIRED'
        r['definition_locator']='DGEF/fabric.py:168; dictionary construction from PRAGMA and SPECS'
    else:continue
    assert sha(p)==r['source_sha256'];manifest[p]=sha(p)
    changes.append(dict(path=r['path'],column_name=r['column_name'],definition=r['definition'],definition_status=r['definition_status'],definition_locator=r['definition_locator'],owner_approval='PENDING'))
assert len(changes)==25 and len(aliases)==15
assert len(a)==len(b)==1989
for x,y in zip(a,b):
    if x!=y:assert {k for k in x if x[k]!=y[k]}=={'definition','definition_status','definition_locator'}
assert sum(x!=y for x,y in zip(a,b))==25
remaining=[r for r in b if r['definition_status']=='UNRESOLVED'];assert len(remaining)==239
assert {r['role'] for r in remaining}=={'HISTORICAL_REPORT_OUTPUT'}
for p,h in manifest.items():assert sha(p)==h
write('field_semantics_v9.csv',b);write('definition_changes.csv',changes);write('byte_equal_definition_links.csv',aliases);write('remaining_unresolved.csv',remaining)
write('source_manifest.csv',[dict(path=p.relative_to(ROOT).as_posix(),sha256=h) for p,h in manifest.items()])
role_status=collections.Counter((r['role'],r['definition_status']) for r in b)
write('role_status_summary.csv',[dict(role=role,status=status,records=n) for (role,status),n in sorted(role_status.items())])
result=dict(pass_check=True,definitions_added=25,byte_equal_preview_fields=15,dictionary_metadata_fields=10,unchanged_records=1964,unresolved=239,unresolved_roles={'HISTORICAL_REPORT_OUTPUT':239},source_files_unchanged=len(manifest),current_external_facts='NOT_REVERIFIED',owner_approval='PENDING')
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
