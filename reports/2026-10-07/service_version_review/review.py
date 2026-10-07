"""Read historical service snapshots and cumulative logs; never run merge scripts."""
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
old=ROOT/'reports/2026-10-07/provenance_field_review/field_semantics_v9.csv'
builder=ROOT/'reports/2026-10-04/build_catalogue.py'
merge=ROOT/'reports/2026-10-04/cross_document_consistency/merge_registry_r2.py'
sources={p:sha(p) for p in [old,builder,merge]}
service_defs={'id':'原抽取名錄的批次行鍵 E 序號；版本沿用，不是全球永久法人鍵',
 'category':'種子清單的編輯分類，非法律登記行業或世界排名',
 'name':'種子清單的展示名稱；匹配不完成法人消歧',
 'role':'種子清單的用途／角色描述，非独立性能核查',
 'status':'該歷史版本的 V/P/U 審閱狀態，須與 verified_scope 及日期合讀，不自動延伸至今日',
 'verification_url':'該版本引用的核查 URL；不是本批即時可達或內容正確的證明',
 'source_context':'原抽取文本的局部上下文；生成器最多保留 600 字元，不等於完整原文',
 'matching_files':'名稱／別名匹配的文件數，不是獨立來源數、機構數或能力指標'}
log_defs={'id':'沿用原抽取名錄的批次行鍵，指向本版累積修訂的名錄行',
 'name':'原基線名錄的展示名稱，不是本版重新核實法人名',
 'old_status':'原始基線名錄的狀態，不是上一版狀態；本日志為相對原基線的累積修訂',
 'new_status':'截至本版所納入批次的最終修訂狀態，不是今日重新認證',
 'old_verification_url':'原始基線名錄的核查 URL，不是上一版 URL',
 'new_verification_url':'本版累積修訂後實際寫入的 URL；U 判定可能保留原 URL，URL 不單獨判定狀態'}
a=read(old);b=[dict(r) for r in a];changes=[]
for r in b:
    if r['definition_status']!='UNRESOLVED':continue
    service=r['path'].startswith('reports/2026-10-04/tables/01_services/strategy_services_registry')
    log=r['path'].startswith('reports/2026-10-04/cross_document_consistency/tables/registry_r') and r['path'].endswith('_changes.csv')
    if not service and not log:continue
    p=ROOT/r['path'];sources[p]=sha(p);assert sha(p)==r['source_sha256']
    defs=service_defs if service else log_defs;c=r['column_name'];assert c in defs
    r['definition']=defs[c];r['definition_status']='CONTEXT_DEFINED_OWNER_REVIEW_REQUIRED'
    r['definition_locator']='reports/2026-10-04/build_catalogue.py:35; merge_registry_r2.py:79-94' if service else 'reports/2026-10-04/cross_document_consistency/merge_registry_r2.py:79-94'
    changes.append(dict(path=r['path'],column_name=c,definition=r['definition'],definition_locator=r['definition_locator'],owner_approval='PENDING',current_external_facts='NOT_REVERIFIED'))
assert len(changes)==78,len(changes)
remaining=[r for r in b if r['definition_status']=='UNRESOLVED'];assert len(remaining)==161
for x,y in zip(a,b):
    if x!=y:assert {k for k in x if x[k]!=y[k]}=={'definition','definition_status','definition_locator'}
base=ROOT/'reports/2026-10-04/tables/01_services/strategy_services_registry.csv';base_rows=read(base);base_index={r['id']:r for r in base_rows};assert len(base_index)==len(base_rows)
summaries=[]
for version in ['base','r2','r3','r4','r5','r6']:
    p=base if version=='base' else base.with_name('strategy_services_registry_20261004_'+version+'.csv')
    sources[p]=sha(p);rows=read(p);assert [r['id'] for r in rows]==[r['id'] for r in base_rows]
    index={r['id']:r for r in rows};logs=[]
    if version!='base':
        lp=ROOT/f'reports/2026-10-04/cross_document_consistency/tables/registry_{version}_changes.csv';sources[lp]=sha(lp);logs=read(lp)
        assert len({r['id'] for r in logs})==len(logs)
        for log in logs:
            prior=base_index[log['id']];current=index[log['id']]
            assert log['old_status']==prior['status'] and log['old_verification_url']==prior['verification_url']
            assert log['new_status']==current['status'] and log['new_verification_url']==current['verification_url']
        ids={r['id'] for r in logs}
        for r in rows:
            if r['id'] not in ids:assert all(r[k]==base_index[r['id']][k] for k in base_rows[0])
    counts=collections.Counter(r['status'] for r in rows)
    summaries.append(dict(version=version,path=p.relative_to(ROOT).as_posix(),rows=len(rows),V=counts['V'],P=counts['P'],U=counts['U'],cumulative_log_rows=len(logs),ids_and_unlogged_rows_preserved=True,log_base_and_target_matches=True))
for p,h in sources.items():assert sha(p)==h
write('field_semantics_v10.csv',b);write('definition_changes.csv',changes);write('remaining_unresolved.csv',remaining);write('version_summary.csv',summaries)
write('source_manifest.csv',[dict(path=p.relative_to(ROOT).as_posix(),sha256=h) for p,h in sources.items()])
result=dict(pass_check=True,definitions_added=78,unresolved=161,unchanged_records=1911,versions=summaries,source_files_unchanged=len(sources),log_semantics='CUMULATIVE_RELATIVE_TO_ORIGINAL_BASE',current_facts_verified=False,owner_approval='PENDING')
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(pass_check=True,definitions_added=78,unresolved=161,version_rows=[r['rows'] for r in summaries],latest_status_counts={k:summaries[-1][k] for k in ['V','P','U']})))
