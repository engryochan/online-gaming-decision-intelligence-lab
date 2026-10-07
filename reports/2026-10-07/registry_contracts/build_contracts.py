"""Guarded B04 research snapshot, field contracts and evidence-scoped SQL views."""
from pathlib import Path
import csv,json,hashlib,sqlite3,re,sys,collections
from decimal import Decimal,InvalidOperation
sys.stdout.reconfigure(encoding='utf-8');csv.field_size_limit(16*1024*1024)
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent;OUT.mkdir(parents=True,exist_ok=True)
DB=OUT/'global_registry_b04_query.sqlite'
if DB.exists():raise SystemExit('Delivered output exists; use a new batch')
REL='Reference/tables/10_global_technology_iso249_20261006_b04'
base={r['path']:r for r in csv.DictReader((ROOT/'reports/2026-10-06/workspace_change_audit/registry_contracts_20261007_start_files.csv').open(encoding='utf-8-sig'))}
def sha(b):return hashlib.sha256(b).hexdigest()
tables={};headers={};manifest=[]
for p in sorted((ROOT/REL).glob('*.csv')):
    raw=p.read_bytes();path=p.relative_to(ROOT).as_posix();assert sha(raw)==base[path]['sha256']
    with p.open(encoding='utf-8-sig',newline='') as f:reader=csv.DictReader(f);rows=list(reader);h=reader.fieldnames
    assert all(None not in r for r in rows)
    tables[p.stem]=rows;headers[p.stem]=h;manifest.append(dict(path=path,sha256=sha(raw),rows=len(rows),columns=len(h)))
prior=list(csv.DictReader((ROOT/'reports/2026-10-07/semantic_evidence_review/field_semantics.csv').open(encoding='utf-8-sig')))
existing={ (Path(r['path']).stem,r['column_name']):r for r in prior if r['path'].startswith(REL+'/')}
definitions={}
def define(names,text,value,unit='NOT_APPLICABLE'):
    for name in names.split(','):definitions[name]=(text,value,unit)
define('display_name,project_name,name_en','機構／產品顯示名、具名項目或國家地區英文名；依所屬表区分，名稱不是穩定識別碼','人類閱讀與搜索')
define('relation_id','一條機構与ISO條目關係主張的識別鍵；具體關係見 relation_type','關係去重與追溯')
define('relation_type','關係類型；例如設施所在地不同於法人住所，不能相互替代','國別歸屬的語義限制')
define('entity_type','編輯登記的機構類型；不代表已核法律實體類型','分類檢索')
define('primary_domain,domain','本表機構主領域或產品技術領域標籤；不同於 DGEF 世界域','領域覆蓋与選型')
define('selection_status','登記時的編輯選入理由或候選分類；不能作世界頂尖資格證明','選樣偏差與範圍追溯')
define('product_leads_state','產品／項目線索的審核狀態；線索不等於已登記正式產品','查證排程')
define('supports','來源被登記為支持哪些描述的摘要；不是整個主張自動VERIFIED','證據支持範圍')
define('source_class','來源類型，例如官方或研究論文；來源類型不等於主張真實或獨立重現','證據權重与審核')
define('access_state','本次取得來源正文与可支持内容的狀態；不保證今日仍可讀','可驗證性與失效追蹤')
define('archive_state','原始來源正文是否封存的狀態；未封存須保留取證缺口','證據保存風險')
define('published_on','來源標示發布日期；空值代表未記錄，不用檢查日期替代','來源有效時間','SOURCE_DATE')
define('notes','具體記錄的證據限制、場景與研究備註；不作結構化核實標籤','防止結論超出範圍')
define('broad_queries_completed','初批對國別执行的廣泛搜索查詢次數，非全領域普查完成度','搜索工作覆蓋','COUNT')
define('retry_count','初批搜索資料 attempt_history 項目數；未保證全是失败後重試','搜索過程追溯','COUNT')
define('search_lead_count','初批搜索返回線索數，可能無關；不同於當期機構數','探索線索與後續審核','COUNT')
define('editorial_entity_candidate_count','依候選國別代碼拆分後歸入該ISO條目的機構記錄數；跨國機構可多次归入國別','候選覆蓋；不跨國相加當唯一機構數','COUNT')
define('candidate_public_descriptions_verified','現行生成器計該國候選機構任意範圍 VERIFIED 主張，包含研究隸屬關係；不等同僅 PUBLIC_DESCRIPTION_ONLY','保留舊統計口徑；分範圍視圖另列','COUNT')
define('country_relation_verified_count','現行生成器計該ISO所有關係行；本快照10行恰均VERIFIED，但未來須按狀態過濾','國別關係數與核實狀態分離','COUNT')
define('neuro_id','具名神經技術／項目记录的識別鍵，不代表一家公司或一個人體試驗','項目去重')
define('direction_state','讀取／寫入／雙向方向主張的核實範圍；項目目標不等於已實現功能','目標與成果分離')
define('bandwidth_state,information_bandwidth_state','本表資訊帶寬是否已按具體協議測量／報告的狀態；速率數字不自动换成bits/s','避免 words/min、訊號頻寬或下行速率混用')
define('publication_state,patent_state','文獻／專利記錄的核實狀態；有識別碼不表示已審全文或實作','科研與知識產權成熟度')
define('record_type','技術记录種類：软件、平台、成像模式、硬體、研究协议或数据库等，並非獨立公司','同類比較与分類')
define('issuer_entity_id','產品與機構的公开歸屬候選鍵；不自動代表法律擁有權','產品機構橋接')
define('issuer_relation_state','產品／技術与機構公開关联的核實範圍，與股權／知識產權分別核實','歸屬證據邊界')
define('public_description','來源所支持的具名技術功能描述；不代表實測性能、採用或監管批准','技術候選篩選')
define('version_state','具体版本核实狀態；名稱存在不代表已核當期版次','版本選型')
define('availability_state','產品或服務可取得／使用狀態；公告不等於所有客戶與地區已可用','採購與部署可行性')
define('metric_id','一項來源條件下的數值记录鍵；多項数值可来自同一技術或论文','測量去重')
define('metric_name','所報數值的測量概念標籤；同單位不代表同一測量对象或任务','同口徑比較')
define('value','來源報告或規格中的值，原字串保留；數值化投影不替代原值與条件','量化比較','REFER_TO_UNIT_AND_METRIC')
define('statistic','平均、中位、廠商規格、最佳宣稱、重採樣網格等统计／声明口徑；不能當同一性能指標','測量與規格分類')
define('participant_count','來源此研究／測量的參與者數；非人體規格項可留空，不能填零','樣本與外推限制','COUNT')
define('conditions','測量任務、产品模式、樣本、星座配置、處理級別与适用前提；比较時必帶','防止脫離場景使用數值')
define('study_date','來源研究或規格的日期；不等於本批審核時間','時間一致性','SOURCE_DATE')
define('doi','數位物件識別碼；僅定位文獻，不證明已審全文','文獻可追溯')
define('general_population_state','數值是否可代表一般人群的证据状态；個別試驗或非人體規格不得推廣','外推限制')
define('world_record_state','世界紀錄主張的核实狀態；收錄數值不證明全球最佳','排名治理')
define('event_id,event_date,event_type','產品生命周期事件鍵、發生日期或類型；區分公告與獨立部署驗證','事件時間線','SOURCE_DATE_FOR_EVENT_DATE')
define('country_candidate_iso_alpha2','編輯候選國別代碼列表，可用分號／逗號分隔；每個代碼連ISO母表，不等同法人住所或國家能力','跨國候選檢索','ISO_ALPHA2_LIST')
contracts=[]
for table,h in headers.items():
    key=h[0];grain={'registry_country_entity_relations':'一條機構—ISO關係主張','registry_country_technology_coverage':'一個ISO條目的研究覆蓋狀態','registry_global_claims':'一條機構公開描述或隸屬主張','registry_global_organizations':'一個編輯登記機構候選','registry_global_sources':'一次版本化來源支持登記','registry_neurotechnology_global':'一個具名神經技術／項目','registry_technology_lifecycle_events':'一個具名技術生命周期事件','registry_technology_metrics':'一個技術與來源條件下的數值','registry_technology_products_tools':'一個具名技術／產品／服務記錄'}[table]
    assert len({r[key] for r in tables[table]})==len(tables[table]) and all(r[key] for r in tables[table])
    for col in h:
        if col in definitions:meaning,value,unit=definitions[col];basis='SOURCE_IMPLEMENTATION_AND_PROPOSED_SEMANTICS'
        else:
            old=existing[(table,col)];assert old['definition_status']!='UNRESOLVED';meaning,value,unit=old['definition'],old['business_value'],old['unit'];basis='PRIOR_PROPOSED_SEMANTICS_CONTEXT_REVIEW'
        contracts.append(dict(table=table,column=col,grain=grain,definition=meaning,business_value=value,unit=unit,primary_key=col==key,status='CONTEXT_DEFINED_OWNER_REVIEW_REQUIRED',basis=basis,null_policy='RAW_EMPTY_PRESERVED; UNKNOWN_NOT_ZERO',source_path=REL+'/'+table+'.csv',owner='UNASSIGNED'))
contractmap={(r['table'],r['column']):r for r in contracts};resolved=0
for r in prior:
    key=(Path(r['path']).stem,r['column_name'])
    if key in contractmap and ('global_technology_iso249' in r['path']):
        c=contractmap[key];resolved+=r['definition_status']=='UNRESOLVED';r.update(definition=c['definition'],definition_status='CONTEXT_DEFINED_OWNER_REVIEW_REQUIRED',definition_locator='reports/2026-10-07/registry_contracts/field_contracts.csv: '+'.'.join(key),grain=c['grain'],business_value=c['business_value'],unit=c['unit'])
def output(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
output('field_contracts.csv',contracts);output('field_semantics_v2.csv',prior);output('source_manifest.csv',manifest)
keys={name:h[0] for name,h in headers.items()};references={'source_id':('registry_global_sources','source_id'),'entity_id':('registry_global_organizations','entity_id'),'issuer_entity_id':('registry_global_organizations','entity_id'),'technology_id':('registry_technology_products_tools','technology_id'),'iso_alpha2':('registry_country_technology_coverage','iso_alpha2')}
projections=[];candidates=[]
orgs=tables['registry_global_organizations'];countries={r['iso_alpha2'] for r in tables['registry_country_technology_coverage']}
for r in orgs:
    for code in filter(None,(x.strip() for x in re.split('[;,]',r['country_candidate_iso_alpha2']))):
        assert code in countries
        candidates.append(dict(entity_id=r['entity_id'],iso_alpha2=code,relation_state='EDITORIAL_CANDIDATE_NOT_VERIFIED_DOMICILE',raw_country_list=r['country_candidate_iso_alpha2']))
for r in tables['registry_technology_metrics']:
    try: value=float(Decimal(r['value'])) if r['value'].strip() else None
    except InvalidOperation:value=None
    projections.append(dict(metric_id=r['metric_id'],numeric_value=value,unit=r['unit'],metric_name=r['metric_name'],statistic=r['statistic'],conditions=r['conditions'],interpretation='SOURCE_REPORTED_OR_DECLARED_NOT_INDEPENDENT_BENCHMARK'))
with sqlite3.connect(DB) as db:
    db.execute('pragma foreign_keys=ON')
    # Raw text is byte-value faithful; logical missing source references use NULLIF views.
    for table,h in headers.items():
        defs=['"'+c+'" TEXT NOT NULL'+(' PRIMARY KEY CHECK("'+c+'"<>\'\')' if c==h[0] else '') for c in h]
        db.execute('create table '+table+' ('+','.join(defs)+') STRICT')
        db.executemany('insert into '+table+' values ('+','.join('?' for _ in h)+')',[tuple(r[c] for c in h) for r in tables[table]])
    db.executescript('''CREATE TABLE entity_country_candidates(entity_id TEXT NOT NULL REFERENCES registry_global_organizations(entity_id),iso_alpha2 TEXT NOT NULL REFERENCES registry_country_technology_coverage(iso_alpha2),relation_state TEXT NOT NULL,raw_country_list TEXT NOT NULL,PRIMARY KEY(entity_id,iso_alpha2)) STRICT;
CREATE TABLE metric_numeric_projection(metric_id TEXT PRIMARY KEY REFERENCES registry_technology_metrics(metric_id),numeric_value REAL,unit TEXT NOT NULL,metric_name TEXT NOT NULL,statistic TEXT NOT NULL,conditions TEXT NOT NULL,interpretation TEXT NOT NULL) STRICT;
CREATE INDEX claims_entity ON registry_global_claims(entity_id);
CREATE INDEX candidate_country ON entity_country_candidates(iso_alpha2);
CREATE INDEX relations_country ON registry_country_entity_relations(iso_alpha2);''')
    for table,rows in [('entity_country_candidates',candidates),('metric_numeric_projection',projections)]:
        db.executemany('insert into '+table+' values ('+','.join('?' for _ in rows[0])+')',[tuple(r.values()) for r in rows])
    db.executescript('''CREATE VIEW v_country_evidence_coverage AS SELECT c.iso_alpha2,c.name_en,
(SELECT COUNT(*) FROM entity_country_candidates b WHERE b.iso_alpha2=c.iso_alpha2) AS candidate_entity_count,
(SELECT COUNT(*) FROM entity_country_candidates b WHERE b.iso_alpha2=c.iso_alpha2 AND EXISTS(SELECT 1 FROM registry_global_claims a WHERE a.entity_id=b.entity_id AND a.evidence_state='VERIFIED')) AS candidate_any_scope_verified_count,
(SELECT COUNT(*) FROM entity_country_candidates b WHERE b.iso_alpha2=c.iso_alpha2 AND EXISTS(SELECT 1 FROM registry_global_claims a WHERE a.entity_id=b.entity_id AND a.evidence_state='VERIFIED' AND a.verification_scope='PUBLIC_DESCRIPTION_ONLY')) AS candidate_public_description_only_count,
(SELECT COUNT(*) FROM registry_country_entity_relations r WHERE r.iso_alpha2=c.iso_alpha2 AND r.evidence_state='VERIFIED') AS verified_country_relation_count,
c.country_frontier_capability_state,c.N0_N7_level FROM registry_country_technology_coverage c;
CREATE VIEW v_claims_with_source AS SELECT a.*,s.url AS evidence_url,s.source_class,s.access_state,s.archive_state FROM registry_global_claims a LEFT JOIN registry_global_sources s ON s.source_id=NULLIF(a.source_id,'');
CREATE VIEW v_metrics_with_context AS SELECT m.*,p.numeric_value,p.interpretation,t.display_name FROM registry_technology_metrics m JOIN metric_numeric_projection p USING(metric_id) JOIN registry_technology_products_tools t USING(technology_id);
CREATE VIEW v_neuro_bandwidth_missing AS SELECT neuro_id,entity_id,project_name,bandwidth_state,bandwidth_protocol,N0_N7_level FROM registry_neurotechnology_global WHERE information_bandwidth_bits_per_second='';''')
    assert db.execute('pragma integrity_check').fetchone()[0]=='ok' and not db.execute('pragma foreign_key_check').fetchall()
    reference_checks=0
    for table,rows in tables.items():
        for col,(target,key) in references.items():
            if col not in headers[table] or table==target:continue
            assert not db.execute('select count(*) from '+table+' r where r."'+col+'"<>\'\' and not exists(select 1 from '+target+' t where t."'+key+'"=r."'+col+'")').fetchone()[0]
            reference_checks+=1
        got=db.execute('select '+','.join('"'+c+'"' for c in headers[table])+' from '+table+' order by rowid').fetchall()
        assert got==[tuple(r[c] for c in headers[table]) for r in rows]
    coverage=[dict(zip([c[0] for c in db.execute('select * from v_country_evidence_coverage').description],r)) for r in db.execute('select * from v_country_evidence_coverage')]
    counts=dict(organizations=len(orgs),sources=len(tables['registry_global_sources']),claims=len(tables['registry_global_claims']),technologies=len(tables['registry_technology_products_tools']),metrics=len(projections),countries=len(coverage),candidate_country_memberships=len(candidates),countries_with_candidates=sum(r['candidate_entity_count']>0 for r in coverage),claims_public_description_verified=db.execute("select count(*) from registry_global_claims where evidence_state='VERIFIED' and verification_scope='PUBLIC_DESCRIPTION_ONLY'").fetchone()[0],claims_affiliation_verified=db.execute("select count(*) from registry_global_claims where evidence_state='VERIFIED' and verification_scope='PUBLISHED_RESEARCH_AFFILIATION'").fetchone()[0],neuro_bandwidth_unknown=db.execute('select count(*) from v_neuro_bandwidth_missing').fetchone()[0])
output('country_evidence_coverage.csv',coverage);output('entity_country_candidates.csv',candidates);output('metric_numeric_projection.csv',projections)
for m in manifest:assert sha((ROOT/m['path']).read_bytes())==m['sha256'],'Source changed during build'
receipt=dict(status='PASS_SOURCE_PRESERVATION_AND_QUERY_CONTRACTS',source_tables=len(tables),field_contracts=len(contracts),prior_field_records=len(prior),unresolved_records_given_context=resolved,unresolved_remaining=sum(r['definition_status']=='UNRESOLVED' for r in prior),reference_checks=reference_checks,counts=counts,raw_csv_roundtrip='ALL_CELLS_EQUAL',foreign_key_check='PASS',new_external_verification='TWO_OFFICIAL_IMAGERY_DEFINITIONS_ONLY',owner_approval=False)
(OUT/'validation.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(receipt,ensure_ascii=False,indent=2))
