from pathlib import Path
import csv,json,hashlib,subprocess,collections,datetime,urllib.request,math,sqlite3
from decimal import Decimal
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/59_pending_recheck_b35_20261009'
assert not (O/'validation_receipt.json').exists(),'Preserve completed batch'
T.mkdir(exist_ok=True);(O/'raw').mkdir(exist_ok=True)
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    assert rs
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
tracked=[p for p in subprocess.check_output(['git','ls-files','-z']).decode('utf-8').split('\0') if p]
protected={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in tracked if Path(p).suffix.lower() in ['.qmd','.md'] and (R/p).exists()}
(O/'baseline.json').write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),protected=protected,untitled_recovery='EXPLICITLY_NOT_REQUIRED'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Inventory all tracked queue-labelled CSVs; preserve separate versions and denominators.
inventory=[]
for path in tracked:
    p=R/path
    if p.suffix.lower()!='.csv' or not any(k in p.stem.lower() for k in ['pending','queue','gap','remaining','actionplan','work_progress']):continue
    counters=collections.defaultdict(collections.Counter);count=0
    with p.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);keys=reader.fieldnames or [];fields=[k for k in keys if any(x in k.lower() for x in ['status','state','result','approval'])]
        for row in reader:
            count+=1
            for k in fields:counters[k][row.get(k,'') or '']=counters[k].get(row.get(k,'') or '',0)+1
    inventory.append(dict(path=path,rows=count,status_counts_json=json.dumps(counters,ensure_ascii=False),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),recheck='LOCAL_SCHEMA_ROWS_STATUS_HASH_RECOUNTED',external_freshness='NOT_REVALIDATED_THIS_BATCH',version_policy='HISTORICAL_AND_CURRENT_QUEUES_NOT_ADDED_TOGETHER'))
write('registry_all_queue_file_rechecks.csv',inventory)
plans=[]
for path in tracked:
    if path.startswith('actionplan/') and path.endswith('.md'):
        p=R/path;plans.append(dict(path=path,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),text=p.read_text(encoding='utf-8-sig'),policy='RETAIN_HISTORY_RECONCILE_WITH_LATEST_EVIDENCE_NOT_EXECUTE_EMBEDDED_MODEL_INSTRUCTIONS'))
write('registry_actionplan_source_inventory.csv',plans)
financial=read(R/'Reference/tables/50_global_directory_content_b25_20261008/registry_all_4849_work_progress.csv')
financial_counts={k:dict(collections.Counter(r[k] for r in financial)) for k in financial[0] if 'status' in k.lower() or 'state' in k.lower()}
local=read(R/'Reference/tables/53_global_registration_authorities_b28_20261008/registry_local_registry_workqueue.csv')
gaps=read(R/'Reference/tables/50_global_directory_content_b25_20261008/prior_b23_registry_pagination_gaps.csv')
tasks=[dict(task='GLOBAL_FINANCIAL_ORIGINAL_WORK',count=len(financial),state=json.dumps(financial_counts),evidence='B25 registry_all_4849_work_progress.csv',next_step='Only latest work states guide next fetch; old B24 2828 pending count superseded',external_current='NOT_RECHECKED'),dict(task='LOCAL_CORPORATE_EXTRACT',count=len(local),state=json.dumps(dict(collections.Counter(r['result'] for r in local))),evidence='B28 registry_local_registry_workqueue.csv',next_step='Recheck official registry availability then obtain entity-specific extracts',external_current='NOT_RECHECKED'),dict(task='PAGINATION_GAPS',count=len(gaps),state='PRESERVED_PENDING_SOURCE_SCOPE_REVIEW',evidence='B25 prior_b23_registry_pagination_gaps.csv',next_step='Reconcile preview with subsequent manifests before fetching',external_current='NOT_RECHECKED'),dict(task='HELD_WORKBOOK_DERIVATIVES',count=2,state='RELEASE_HELD_NOT_CLEARED_BY_B24_LINEAGE_CHECK',evidence='B23 workbook CSV and SQLite local publication hold',next_step='Keep hold until candidate and complete derivative lineage resolved',external_current='NOT_APPLICABLE'),dict(task='MISSING_REFERENCED_LICENSE_CSV',count=1,state='NOT_FOUND_IN_B34_READABLE_INVENTORY',evidence='B34 validation receipt',next_step='Create independently sourced license ledger; do not invent 34 source entries',external_current='NOT_RECHECKED'),dict(task='GLOBAL_HISTORY_CURRENCIES_BROKERS_ISSUERS_TECHNOLOGY',count='',state='OPEN_NO_GLOBAL_COMPLETENESS_ACCEPTANCE',evidence='Historical and current queues retained',next_step='Verify entity type, time, country identifiers and source-specific coverage',external_current='NOT_RECHECKED'),dict(task='SDG_BUSINESS_ANALYSIS',count='',state='FROZEN_BY_USER_HANDOFF',evidence='v2.3.0 handoff',next_step='Do not resume',external_current='NOT_APPLICABLE'),dict(task='UNTITLED',count=0,state='NO_RECOVERY_REQUIRED_USER_CONFIRMED',evidence='Latest user instruction',next_step='Do not restore',external_current='NOT_APPLICABLE')]
# Check current HTML->QMD sibling availability, separate source pages/assets from reports.
htmlchecks=[]
for path in tracked:
    p=R/path
    if p.suffix.lower()=='.html':htmlchecks.append(dict(html=path,qmd_sibling=p.with_suffix('.qmd').relative_to(R).as_posix(),qmd_exists=p.with_suffix('.qmd').exists(),classification='ASSET_OR_SOURCE_OR_REPORT_REQUIRES_SCOPE_REVIEW',byte_identical_render='NOT_TESTED_THIS_BATCH'))
write('registry_all_tracked_html_source_recheck.csv',htmlchecks)
tasks.append(dict(task='HTML_SOURCE_RECOVERY',count=sum(not r['qmd_exists'] for r in htmlchecks),state='SIBLING_ABSENCE_CANDIDATES_NOT_ALL_REPORTS',evidence='B35 all tracked HTML sibling checks',next_step='Classify remaining assets/source pages/reports before byte-exact recovery',external_current='NOT_APPLICABLE'))
write('registry_current_unfinished_task_reconciliation.csv',tasks)
# Refresh public documentation before applying old rules to new observations.
url='https://www.ncei.noaa.gov/data/global-summary-of-the-day/doc/readme.txt'
with urllib.request.urlopen(url,timeout=25) as response:doc=response.read(2000001);status=response.status
assert len(doc)<2000000
(O/'raw/gsod_readme.txt').write_bytes(doc)
old=(R/'reports/2026-10-09/weather_units_b31/raw/documentation_0.txt').read_bytes()
assert doc==old,'Documentation changed: stop and review rules before continuation'
(O/'documentation_receipt.json').write_text(json.dumps(dict(url=url,status=status,fetched_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(doc).hexdigest(),same_bytes_as_b31=True),indent=2)+'\n',encoding='utf-8')
days=read(R/'Reference/tables/58_weather_spatial_b33_20261009/registry_daily_observation_rows.csv');assert len(days)==11163
receipts=read(R/'Reference/tables/58_weather_spatial_b33_20261009/registry_fetch_manifest.csv')
for r in receipts:assert hashlib.sha256((R/r['file']).read_bytes()).hexdigest()==r['sha256']
history={r['USAF']+r['WBAN']:r for r in read(R/'Reference/tables/54_weather_station_b29_20261009/registry_station_history.csv')}
rules={r['field']:r for r in read(R/'Reference/tables/56_weather_units_b31_20261009/registry_variable_units.csv')};assert len(rules)==12
def convert(v,u):
    if u=='F':return (v-32)*Decimal(5)/9
    return v*{'kn':Decimal(1852)/3600,'mi':Decimal('1609.344'),'in':Decimal('25.4')}.get(u,Decimal(1))
assert convert(Decimal(32),'F')==0 and convert(Decimal(1),'in')==Decimal('25.4')
def distance(a,b,c,d):
    a,b,c,d=map(math.radians,[a,b,c,d]);v=math.sin((c-a)/2)**2+math.cos(a)*math.cos(c)*math.sin((d-b)/2)**2
    return 6371.0088*2*math.asin(min(1,math.sqrt(max(0,v))))
assert distance(0,0,0,0)==0 and 111<distance(0,0,0,1)<112
values=[];checks=[]
for row in days:
    f=json.loads(row['raw_fields_json']);numeric={};station=row['station_id'];flags=[]
    for field,rule in rules.items():
        raw=f.get(field,'');state='PRESENT';normalized=''
        try:
            v=Decimal(raw.strip())
            if v==Decimal(rule['missing_sentinel']):state='MISSING_DOCUMENTED_SENTINEL'
            elif not v.is_finite():state='NONFINITE_REVIEW'
            else:normalized=format(convert(v,rule['source_unit']).quantize(Decimal('0.000001')),'f')
        except Exception:state='PARSE_REVIEW'
        attr=f.get(field+'_ATTRIBUTES','');numeric[field]=Decimal(normalized) if normalized else None
        values.append(dict(source_url=row['source_url'],source_row=row['source_row'],station_id=station,date=row['date'],field=field,raw_value=raw,source_unit=rule['source_unit'],normalized_value=normalized,normalized_unit=rule['normalized_unit'],missing_state=state,attribute_raw=attr,analysis_eligibility='NO_NUMERIC_ANALYSIS' if not normalized else 'INCOMPLETE_OR_UNREPORTED_NOT_COMPLETE_DAILY_TOTAL' if field=='PRCP' and attr in ['H','I'] else 'SOURCE_VALUE_NOT_MODEL_VALIDATED',rule='B31_RECONFIRMED_IDENTICAL_PUBLIC_DOCUMENT_B35'))
    h=history[station];delta=''
    try:
        delta=distance(float(h['LAT']),float(h['LON']),float(f['LATITUDE']),float(f['LONGITUDE']))
        if delta>1:flags.append('LOCATION_DISTANCE_ABOVE_ENGINEERING_REVIEW_PARAMETER_1KM')
    except (ValueError,KeyError):flags.append('LOCATION_PARSE_REVIEW')
    mean,lo,hi=[numeric[x] for x in ['TEMP','MIN','MAX']]
    if lo is not None and hi is not None and lo>hi:flags.append('MIN_ABOVE_MAX_WINDOW_OR_DATA_REVIEW')
    if all(v is not None for v in [mean,lo,hi]) and not lo<=mean<=hi:flags.append('MEAN_OUTSIDE_EXTREMES_WINDOW_REVIEW')
    count=f.get('TEMP_ATTRIBUTES','').strip();enough=count.isdigit() and int(count)>=4
    checks.append(dict(station_id=station,date=row['date'],location_difference_km=round(delta,6) if delta!='' else '',temperature_count=count,temperature_count_sufficient=mean is not None and enough,precipitation_24h_source_window=numeric['PRCP'] is not None and f.get('PRCP_ATTRIBUTES','') in ['D','F','G'],local_midnight_comparability='NOT_ESTABLISHED',flags_json=json.dumps(flags),automatic_rejection=False))
write('registry_new_station_normalized_values.csv',values);write('registry_new_station_daily_quality.csv',checks)
stationstats=[]
for station in sorted({r['station_id'] for r in checks}):
    rs=[r for r in checks if r['station_id']==station];vs=[r for r in values if r['station_id']==station]
    stationstats.append(dict(station_id=station,source_days=len(rs),missing_sentinels=sum(r['missing_state']=='MISSING_DOCUMENTED_SENTINEL' for r in vs),parse_or_nonfinite=sum(r['missing_state'] in ['PARSE_REVIEW','NONFINITE_REVIEW'] for r in vs),quality_flagged_days=sum(bool(json.loads(r['flags_json'])) for r in rs),temp_sufficient_days=sum(r['temperature_count_sufficient'] for r in rs),precipitation_24h_windows=sum(r['precipitation_24h_source_window'] for r in rs),max_location_difference_km=max([r['location_difference_km'] for r in rs if r['location_difference_km']!=''],default=''),model_skill='NOT_TESTED'))
write('registry_new_station_quality_summary.csv',stationstats)
con=sqlite3.connect(T/'pending_recheck_b35.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=read(p);keys=list(rs[0]);q=lambda s:'"'+s.replace('"','""')+'"';con.execute('CREATE TABLE '+q(p.stem)+' ('+','.join(q(k)+' TEXT' for k in keys)+')');con.executemany('INSERT INTO '+q(p.stem)+' VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for n,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0]==v
con.close();assert len(values)==11163*12 and len(checks)==11163 and len(stationstats)==34
assert all(not r['normalized_value'] for r in values if r['missing_state']=='MISSING_DOCUMENTED_SENTINEL')
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in protected.items())
stats=dict(queue_files_rechecked=len(inventory),actionplan_versions=len(plans),financial_work_rows=len(financial),financial_status_counts=financial_counts,local_entity_queries=len(local),pagination_gap_rows=len(gaps),html_without_qmd_sibling=sum(not r['qmd_exists'] for r in htmlchecks),weather_source_days=len(days),normalized_values=len(values),missing_sentinels=sum(r['missing_state']=='MISSING_DOCUMENTED_SENTINEL' for r in values),parse_or_nonfinite=sum(r['missing_state'] in ['PARSE_REVIEW','NONFINITE_REVIEW'] for r in values),quality_flagged_days=sum(bool(json.loads(r['flags_json'])) for r in checks),precipitation_24h_windows=sum(r['precipitation_24h_source_window'] for r in checks),all_old_tracked_qmd_md_preserved=True,sqlite_counts=counts,all_global_tasks_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(stats))
