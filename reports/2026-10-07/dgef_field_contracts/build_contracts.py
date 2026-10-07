"""Build review contracts without changing DGEF sources or old semantic catalogues."""
from pathlib import Path
import csv, json, sqlite3, hashlib, collections

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
csv.field_size_limit(16*1024*1024)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

assert not (OUT/'validation.json').exists(), 'Delivered batch already exists; use a new batch'
old=ROOT/'reports/2026-10-07/registry_contracts/field_semantics_v2.csv'
dictionary=ROOT/'DGEF/contracts/data_dictionary.csv'
database=ROOT/'DGEF/artifacts/dgef.sqlite'
schema=ROOT/'DGEF/schema.sql'
rows=read(old); entries={(r['table'],r['column']):r for r in read(dictionary)}
definitions={}
for line in (OUT/'proposed_definitions.tsv').read_text(encoding='utf-8').splitlines():
    key,value=line.split('\t',1);assert key not in definitions;definitions[key]=value
sources={p:sha(p) for p in [old,dictionary,database,schema]}
db=sqlite3.connect(database.as_uri()+'?mode=ro',uri=True)
assert db.execute('pragma integrity_check').fetchone()[0]=='ok'
assert not db.execute('pragma foreign_key_check').fetchall()
contracts=[];changed=[];used=set()
for r in rows:
    if r['role']!='DGEF_EXPORT':continue
    p=ROOT/r['path'];sources[p]=sha(p);assert sha(p)==r['source_sha256']
    t=r['table'];c=r['column_name'];key=(t,c)
    columns={x[1]:x for x in db.execute(f'pragma table_info("{t}")')}
    info=columns[c];fk=[x for x in db.execute(f'pragma foreign_key_list("{t}")') if x[3]==c]
    ddl=db.execute("select sql from sqlite_master where type='table' and name=?",(t,)).fetchone()[0]
    declared=entries.get(key)
    grain=declared['grain'] if declared else r['grain']
    before=dict(r)
    if r['definition_status']=='DOCUMENTED_GENERIC_REVIEW':
        assert c in definitions,c;used.add(c)
        r['definition']=definitions[c]+'；本表粒度：'+grain
        r['definition_status']='PROPOSED_TABLE_CONTRACT_REVIEW'
        r['definition_locator']='reports/2026-10-07/dgef_field_contracts/proposed_definitions.tsv: '+c
        changed.append(dict(path=r['path'],table=t,column_name=c,previous_definition=before['definition'],proposed_definition=r['definition'],previous_status=before['definition_status'],proposed_status=r['definition_status']))
    if fk:
        business='以明確外鍵支持追溯與關聯；不自動核實關係的現實含義'
    elif info[5]:business='識別本表粒度中的記錄，支援重複檢查與更新定位'
    else:business='保留該欄位的描述、分類或測量上下文；價值與使用口徑待負責人確認'
    contracts.append(dict(path=r['path'],table=t,column_name=c,grain=grain,
        previous_definition=before['definition'],definition=r['definition'],definition_status=r['definition_status'],
        sql_type=info[2],declared_not_null=info[3],primary_key_position=info[5],
        foreign_key_targets=json.dumps([{'table':x[2],'column':x[4]} for x in fk],ensure_ascii=False),
        table_ddl=ddl,null_policy='SQL_NULL_IS_NOT_ZERO; CSV_EMPTY_REQUIRES_SOURCE_CONTEXT',
        business_value_proposal=business,owner='UNASSIGNED',business_approval='PENDING',
        source_csv_sha256=sha(p),source_database_sha256=sources[database]))
db.close()
assert len(changed)==148
assert len(contracts)==411
assert len(rows)==1989
assert sum(r['definition_status']=='UNRESOLVED' for r in rows)==424
assert not any(r['role']=='DGEF_EXPORT' and r['definition_status']=='DOCUMENTED_GENERIC_REVIEW' for r in rows)
for p,h in sources.items():assert sha(p)==h,str(p)
write('field_contracts.csv',contracts);write('definition_changes.csv',changed);write('field_semantics_v3.csv',rows)
write('source_manifest.csv',[dict(path=p.relative_to(ROOT).as_posix(),sha256=h) for p,h in sources.items()])
write('table_contract_summary.csv',[dict(table=t,columns=sum(c['table']==t for c in contracts),proposed_replacements=sum(c['table']==t for c in changed)) for t in sorted({c['table'] for c in contracts})])
result=dict(field_records=len(rows),dgef_contracts=len(contracts),tables=len({c['table'] for c in contracts}),generic_definitions_replaced=len(changed),distinct_proposed_terms=len(used),unresolved=424,source_files_unchanged=len(sources),status_counts=dict(collections.Counter(r['definition_status'] for r in rows)),business_approval='PENDING')
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
