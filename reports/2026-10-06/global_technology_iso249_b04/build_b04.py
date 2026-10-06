from pathlib import Path
import csv,json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
OLD=ROOT/'Reference/tables/09_global_technology_iso249_20261006_b03'
REL=Path('Reference/tables/10_global_technology_iso249_20261006_b04')
QMD=Path('Reference/Global_Technology_ISO249_Registry_B04.qmd')
BASELINE='reports/2026-10-06/workspace_change_audit/global_b04_start_files.csv'
APPEND=[Path('Reference/Global_Technology_ISO249_Registry.qmd'),Path('Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd')]
DATE='2026-10-06'
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(str(x).replace('|','&#124;').replace('\n',' ') for x in r)+' |' for r in rows])+'\n'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--apply',action='store_true');a=ap.parse_args()
    baseline={r['path']:r for r in read(ROOT/BASELINE)}
    if a.apply:
        assert not (ROOT/REL).exists() and not (ROOT/QMD).exists(),'Existing output: review required'
        for p in APPEND:assert sha(ROOT/p)==baseline[p.as_posix()]['sha256'],f'User changed {p}'
        for p in OLD.iterdir():assert sha(p)==baseline[p.relative_to(ROOT).as_posix()]['sha256'],f'Input changed {p}'
    base=ROOT if a.apply else HERE/'preview'
    seed=json.loads((HERE/'curated_seed.json').read_text(encoding='utf-8'))
    tables={p.name:read(p) for p in OLD.glob('*.csv')}
    orgs=tables['registry_global_organizations.csv'];sources=tables['registry_global_sources.csv']
    tech=tables['registry_technology_products_tools.csv'];metrics=tables['registry_technology_metrics.csv']
    owners={o['display_name']:o['entity_id'] for o in orgs};new=[];events=[]
    # This batch uses distinct source assessments even when a URL appeared historically.
    urlsid={}
    def source(url,claim,state):
        if url in urlsid:return urlsid[url]
        sid=f'GDS{len(urlsid)+1:04d}';urlsid[url]=sid
        sources.append(dict(source_id=sid,url=url,supports=claim,source_class='PRIMARY_OFFICIAL',access_state='READABLE_SUPPORT' if state=='VERIFIED' else 'INSUFFICIENT_OR_FAILED',checked_on=DATE,published_on='',archive_state='NO_RAW_HTTP_ARCHIVE',license_state='UNKNOWN',origin_batch='GLOBAL_249_B04'))
        return sid
    for i,(name,domain,kind,owner,url,claim,state) in enumerate(seed['technologies'],1):
        sid=source(url,claim,state)
        row=dict(technology_id=f'GDT{i:04d}',display_name=name,record_type=kind,domain=domain,issuer_entity_id=owners[owner],issuer_relation_state='PUBLIC_SOURCE_ASSOCIATION_NOT_LEGAL_OWNERSHIP' if state=='VERIFIED' else 'UNKNOWN',public_description=claim,evidence_state=state,verification_scope='PUBLIC_DESCRIPTION_ONLY' if state=='VERIFIED' else 'UNKNOWN',source_id=sid,version_state='UNKNOWN',license_state='UNKNOWN',availability_state='UNKNOWN',independent_performance_state='NOT_REPLICATED_IN_THIS_REVIEW',global_rank_state='UNKNOWN',regulatory_state='UNKNOWN',as_of=DATE)
        tech.append(row);new.append(row)
    byname={r['display_name']:r for r in new}
    for i,(name,metric,value,unit,stat,n,conditions,pub,doi) in enumerate(seed['metrics'],1):
        t=byname[name]
        metrics.append(dict(metric_id=f'GDM{i:04d}',technology_id=t['technology_id'],entity_id=t['issuer_entity_id'],metric_name=metric,value=value,unit=unit,statistic=stat,participant_count=n,conditions=conditions,study_date=pub,doi=doi,evidence_state='VERIFIED',verification_scope='OFFICIAL_DECLARED_SPECIFICATION_NOT_MEASURED_BENCHMARK',source_id=t['source_id'],information_bandwidth_state='NOT_NEURO_INFORMATION_BANDWIDTH',general_population_state='NOT_APPLICABLE',world_record_state='UNKNOWN',reviewed_on=DATE))
    for i,e in enumerate(seed['events'],1):
        t=byname[e['technology']];sid=source(e['url'],e['claim'],'VERIFIED')
        events.append(dict(event_id=f'GDE{i:04d}',technology_id=t['technology_id'],entity_id=t['issuer_entity_id'],event_date=e['date'],event_type=e['event'],claim=e['claim'],evidence_state='VERIFIED',verification_scope='VENDOR_ANNOUNCEMENT_ONLY',independent_deployment_state='UNKNOWN',source_id=sid,reviewed_on=DATE))
    tables['registry_technology_lifecycle_events.csv']=events
    counts=dict(organizations=len(orgs),new_organizations=0,technologies=len(tech),new_technologies=len(new),new_descriptions_verified=sum(r['evidence_state']=='VERIFIED' for r in new),reported_metrics=len(metrics),new_metrics=len(seed['metrics']),neuro_records=len(tables['registry_neurotechnology_global.csv']),countries_with_editorial_candidates=103,lifecycle_events=len(events))
    (base/REL).mkdir(parents=True,exist_ok=True)
    for fn,rows in tables.items():
        with (base/REL/fn).open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    dictionary=dict(batch='B04',as_of=DATE,counts=counts,table_fields={fn:list(rows[0]) for fn,rows in tables.items()},evidence_rules=['VERIFIED is claim-specific public description or official specification.','Vendor announcements do not establish independent deployment.','GSD, ground SAR resolution, slant resolution and resampled pixels differ.','No military acceptance, legal domicile, global rank or license applicability inferred.'],source_anomalies=seed['source_anomalies'])
    (base/REL/'data_dictionary.json').write_text(json.dumps(dictionary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    sidurl={s['source_id']:s['url'] for s in sources}
    text=(HERE/'report_intro.md').read_text(encoding='utf-8')
    text+=f"\n本批新增{len(new)}筆技術／服務：10筆公開描述VERIFIED、2筆UNKNOWN；6筆條件化規格與1筆公司公告事件。累計{len(orgs)}筆機構候選、{len(tech)}筆技術／服務、{len(metrics)}筆數值；神經科技維持16筆。\n\n## 本批技術與服務\n\n"
    text+=table(['ID','名稱','角色','公開描述／待查主張','證據與來源'],[[t['technology_id'],t['display_name'],t['record_type'],t['public_description'],f"[{t['evidence_state']}]({sidurl[t['source_id']]})"] for t in new])
    text+='\n## 規格與前提\n\n'+table(['指標','數值','口徑','前提','來源'],[[m['metric_name'],m['value']+' '+m['unit'],m['statistic'],m['conditions'],f"[來源]({sidurl[m['source_id']]})"] for m in metrics if m['metric_id'].startswith('GDM')])
    text+='\n## 整合數據表\n\n'+table(['數據表','連結'],[[fn,f'[{fn}](tables/10_global_technology_iso249_20261006_b04/{fn})'] for fn in tables])
    text+='\n[數據字典與來源限制](tables/10_global_technology_iso249_20261006_b04/data_dictionary.json)。先前批次保留；本輪不新增未核實的國別能力結論。\n'
    (base/QMD).parent.mkdir(parents=True,exist_ok=True);(base/QMD).write_text(text,encoding='utf-8')
    if a.apply:
        block='\n\n<!-- GLOBAL_ISO249_B04_START -->\n## 全球科技第四批增補\n\n新增[軍工AI、宇航影像與戰略服務平台](Global_Technology_ISO249_Registry_B04.qmd)及[HTML](Global_Technology_ISO249_Registry_B04.html)。12筆具名產品／服務、6筆帶前提規格與1筆公司公告事件；完整整合表位於10目錄。累計371筆機構候選、71筆技術／服務。官方描述與獨立效能、完整星座條件與實際服務開放分開；ISO249全面核實仍未完成。\n<!-- GLOBAL_ISO249_B04_END -->\n'
        for p in APPEND:
            with (ROOT/p).open('ab') as f:f.write(block.encode('utf-8'))
        manifest=dict(counts=counts,new_output_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in [ROOT/QMD,*sorted((ROOT/REL).iterdir())]},append_prefixes={p.as_posix():dict(bytes=int(baseline[p.as_posix()]['bytes']),sha256=baseline[p.as_posix()]['sha256']) for p in APPEND},baseline_file=BASELINE)
        (HERE/'delivery_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(counts))
if __name__=='__main__':main()
