from pathlib import Path
import csv,json,hashlib,re,argparse
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
OLD=ROOT/"Reference/tables/08_global_technology_iso249_20261006_b02"
REL=Path("Reference/tables/09_global_technology_iso249_20261006_b03")
QMD=Path("Reference/Global_Technology_ISO249_Registry_B03.qmd")
DATE="2026-10-06"
def read(p):
    with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(h,rows):
    return "\n".join(["| "+" | ".join(h)+" |","| "+" | ".join(["---"]*len(h))+" |"]+["| "+" | ".join(str(v).replace("|","&#124;").replace("\n"," ") for v in r)+" |" for r in rows])+"\n"
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--apply",action="store_true");args=ap.parse_args()
    baseline={r["path"]:r for r in read(ROOT/"reports/2026-10-06/workspace_change_audit/global_b03_start_files.csv")}
    append_paths=[Path("Reference/Global_Technology_ISO249_Registry.qmd"),Path("Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd")]
    if args.apply:
        assert not (ROOT/REL).exists() and not (ROOT/QMD).exists(),"Existing B03 output: review required"
        for p in append_paths:assert digest(ROOT/p)==baseline[p.as_posix()]["sha256"],f"User changed {p}"
    base=ROOT if args.apply else HERE/"preview"
    seed=json.loads((HERE/"curated_seed.json").read_text(encoding="utf-8"))
    orgs=read(OLD/"registry_global_organizations.csv");claims=read(OLD/"registry_global_claims.csv")
    sources=read(OLD/"registry_global_sources.csv");tech=read(OLD/"registry_technology_products_tools.csv")
    neuro=read(OLD/"registry_neurotechnology_global.csv");rels=read(OLD/"registry_country_entity_relations.csv")
    coverage=read(OLD/"registry_country_technology_coverage.csv")
    new=[];newtech=[];metrics=read(OLD/"registry_technology_metrics.csv");newneuro=[]
    urlsid={r["url"]:r["source_id"] for r in sources}
    def source(url,claim,state="VERIFIED",kind="PRIMARY_OFFICIAL"):
        if url in urlsid:return urlsid[url]
        sid=f"GCS{1+sum(s['source_id'].startswith('GCS') for s in sources):04d}"
        sources.append(dict(source_id=sid,url=url,supports=claim,source_class=kind,access_state="READABLE_SUPPORT" if state=="VERIFIED" else "INSUFFICIENT_OR_FAILED",checked_on=DATE,published_on="",archive_state="NO_RAW_HTTP_ARCHIVE",license_state="UNKNOWN",origin_batch="GLOBAL_249_B03"))
        urlsid[url]=sid;return sid
    for i,row in enumerate(seed["organizations"],1):
        name,country,kind,domain,url,claim,*tail=row;state=tail[0] if tail else "VERIFIED"
        sid=source(url,claim,state,"PRIMARY_RESEARCH_PAPER" if "nature.com" in url else "PRIMARY_OFFICIAL")
        eid=f"GCO{i:04d}"
        selection="PROJECT_EVIDENCE_PRESENT_NOT_GLOBAL_RANK" if name in ("IT4Innovations","Google Quantum AI") else "COVERAGE_RESEARCH_LEAD_NOT_FRONTIER_QUALIFIED"
        o=dict(entity_id=eid,display_name=name,entity_type=kind,primary_domain=domain,country_candidate_iso_alpha2=country,country_assignment_status="EDITORIAL_CANDIDATE_NOT_LEGAL_DOMICILE" if country else "MULTINATIONAL_OR_UNASSIGNED",legal_entity_status="DISPLAY_ORG_NOT_LEGAL_REGISTRY_VERIFIED",selection_status=selection,source_id=sid,as_of=DATE,origin_batch="GLOBAL_249_B03",legal_domicile_state="UNKNOWN",world_frontier_rank_state="UNKNOWN")
        orgs.append(o);new.append(o)
        claims.append(dict(claim_id=f"GCC{i:04d}",entity_id=eid,claim=claim,evidence_state=state,verification_scope="PUBLISHED_RESEARCH_AFFILIATION" if "nature.com" in url else ("PUBLIC_DESCRIPTION_ONLY" if state=="VERIFIED" else "UNKNOWN"),product_project_leads="",product_leads_state="UNKNOWN",performance_state="UNKNOWN",deployment_state="UNKNOWN",regulatory_state="UNKNOWN",source_id=sid,reviewed_on=DATE,origin_batch="GLOBAL_249_B03"))
    for i,row in enumerate(seed["technologies"],1):
        name,domain,kind,owner,url,claim,*tail=row;state=tail[0] if tail else "VERIFIED"
        sid=source(url,claim,state,"PRIMARY_RESEARCH_PAPER" if "nature.com" in url else "PRIMARY_OFFICIAL_OR_AUTHOR_REPOSITORY")
        eid=next(o["entity_id"] for o in new if o["display_name"]==owner)
        t=dict(technology_id=f"GCT{i:04d}",display_name=name,record_type=kind,domain=domain,issuer_entity_id=eid,issuer_relation_state="PUBLIC_SOURCE_ASSOCIATION_NOT_LEGAL_OWNERSHIP",public_description=claim,evidence_state=state,verification_scope="PUBLISHED_STUDY_DESCRIPTION" if kind=="RESEARCH_PROTOCOL" else "PUBLIC_DESCRIPTION_ONLY",source_id=sid,version_state="UNKNOWN",license_state="UNKNOWN",availability_state="UNKNOWN",independent_performance_state="NOT_REPLICATED_IN_THIS_REVIEW",global_rank_state="UNKNOWN",regulatory_state="UNKNOWN",as_of=DATE)
        tech.append(t);newtech.append(t)
    byname={t["display_name"]:t for t in newtech}
    for i,row in enumerate(seed["metrics"],1):
        name,metric,value,unit,stat,n,conditions,pub,doi=row;t=byname[name]
        metrics.append(dict(metric_id=f"GCM{i:04d}",technology_id=t["technology_id"],entity_id=t["issuer_entity_id"],metric_name=metric,value=value,unit=unit,statistic=stat,participant_count=n,conditions=conditions,study_date=pub,doi=doi,evidence_state="VERIFIED",verification_scope="PAPER_REPORTED_RESULT_NOT_INDEPENDENT_REPLICATION",source_id=t["source_id"],information_bandwidth_state="UNKNOWN",general_population_state="UNKNOWN",world_record_state="UNKNOWN",reviewed_on=DATE))
    for name,code,kind,claim in [
      ("Centre Spatial Guyanais","GF","FACILITY_LOCATION","官方描述位於Guyane的太空設施；不是GF主權或法律註冊地"),
      ("NSF Amundsen-Scott South Pole Station","AQ","FACILITY_LOCATION","官方列地理南極90°S科研站；不是南極主權或法律註冊地")]:
        o=next(o for o in new if o["display_name"]==name)
        rels.append(dict(relation_id=f"GCR{1+sum(r['relation_id'].startswith('GCR') for r in rels):04d}",entity_id=o["entity_id"],iso_alpha2=code,relation_type=kind,claim=claim,evidence_state="VERIFIED",verification_scope="PUBLIC_LOCATION_NOT_DOMICILE_OR_COUNTRY_RANK",source_id=o["source_id"],as_of=DATE))
    for m in metrics:
        if m["metric_id"].startswith("GCM"):
            m["general_population_state"]="NOT_APPLICABLE"
            if not m["doi"]:m["verification_scope"]="OFFICIAL_DECLARED_SPECIFICATION_NOT_MEASURED_BENCHMARK"
    for c in coverage:
        matched=[o for o in orgs if c["iso_alpha2"] in re.split("[;,]",o["country_candidate_iso_alpha2"])]
        c["editorial_entity_candidate_count"]=len(matched)
        c["candidate_public_descriptions_verified"]=sum(next(cl["evidence_state"] for cl in claims if cl["entity_id"]==o["entity_id"])=="VERIFIED" for o in matched)
        c["country_relation_verified_count"]=sum(r["iso_alpha2"]==c["iso_alpha2"] for r in rels)
    counts=dict(organizations=len(orgs),new_organizations=len(new),new_organization_descriptions_verified=sum(c["origin_batch"]=="GLOBAL_249_B03" and c["evidence_state"]=="VERIFIED" for c in claims),organization_descriptions_verified=sum(c["evidence_state"]=="VERIFIED" for c in claims),technologies=len(tech),new_technologies=len(newtech),neuro_records=len(neuro),published_studies=len(newneuro),reported_metrics=len(metrics),countries_with_editorial_candidates=sum(int(c["editorial_entity_candidate_count"])>0 for c in coverage))
    tables={"registry_global_organizations.csv":orgs,"registry_global_claims.csv":claims,"registry_global_sources.csv":sources,"registry_technology_products_tools.csv":tech,"registry_neurotechnology_global.csv":neuro,"registry_country_entity_relations.csv":rels,"registry_country_technology_coverage.csv":coverage,"registry_technology_metrics.csv":metrics}
    (base/REL).mkdir(parents=True,exist_ok=True)
    for fn,rows in tables.items():
        with (base/REL/fn).open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    dictionary=dict(counts=counts,batch="B03",as_of=DATE,evidence_rules=["VERIFIED is claim-specific.","Paper metrics are verified as reported, not independently replicated.","Candidate country is not legal domicile or national frontier rank.","80ms increment is not end-to-end latency or information bandwidth.","Research infrastructure and policy roles do not constitute world-leading technology."],table_fields={fn:list(rows[0]) for fn,rows in tables.items()},source_anomalies=seed["source_anomalies"])
    (base/REL/"data_dictionary.json").write_text(json.dumps(dictionary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    orgclaim={c["entity_id"]:c for c in claims};sidurl={s["source_id"]:s["url"] for s in sources}
    text=(HERE/"report_intro.md").read_text(encoding="utf-8")
    text+=f"\n本批新增 {len(new)} 筆機構／設施候選，其中 {counts['new_organization_descriptions_verified']} 筆公開描述已核實；新增 {len(newtech)} 筆具名技術／工具及5筆帶條件數值。累計 {len(orgs)} 筆機構候選、{len(tech)} 筆技術／工具、{len(neuro)} 筆神經科技記錄、{len(metrics)} 筆數值。249母表中有編輯候選的地區為 {counts['countries_with_editorial_candidates']}；這不是已完成核實的國家數。\n\n"
    text+="## 本批技術與數值\n\n"
    text+=table(["ID","技術／工具","類型","公開描述","來源"],[[t["technology_id"],t["display_name"],t["record_type"],t["public_description"],f'[來源]({sidurl[t["source_id"]]})'] for t in newtech])
    text+=table(["指標","數值","口徑","條件","來源"],[[m["metric_name"],m["value"]+" "+m["unit"],m["statistic"],m["conditions"],f'[來源]({sidurl[m["source_id"]]})'] for m in metrics if m["metric_id"].startswith("GCM")])
    text+="\n## 新增機構與待核實線索\n\nUNKNOWN行是待查線索，並未核實其主張；VERIFIED僅支持所列公開描述。一般大學、國家研究院與設施尚未因入表取得世界前沿資格。\n\n"
    text+=table(["ID","名稱","地區候選","領域","描述／待核實主張","證據"],[[o["entity_id"],o["display_name"],o["country_candidate_iso_alpha2"] or "未分配",o["primary_domain"],orgclaim[o["entity_id"]]["claim"],f'[{orgclaim[o["entity_id"]]["evidence_state"]}]({sidurl[o["source_id"]]})'] for o in new])
    text+="\n## 整合數據表\n\n"
    text+=table(["數據表","連結"],[[fn,f'[{fn}](tables/09_global_technology_iso249_20261006_b03/{fn})'] for fn in tables])
    text+="\n[數據字典與來源異常](tables/09_global_technology_iso249_20261006_b03/data_dictionary.json)。先前952筆逐地搜索線索仍保留於07目錄；未將未知搜索結果機械升格。全球所有組織與技術的查證尚未完成。\n"
    (base/QMD).parent.mkdir(parents=True,exist_ok=True);(base/QMD).write_text(text,encoding="utf-8")
    if args.apply:
        for p in append_paths:
            block="\n\n<!-- GLOBAL_ISO249_B03_START -->\n## 全球科技第三批增補\n\n新增 [第三批量子、HPC與地區證據](Global_Technology_ISO249_Registry_B03.qmd)及 [HTML](Global_Technology_ISO249_Registry_B03.html)。完整整合表位於09目錄；累計"+str(len(orgs))+"筆機構候選、"+str(len(tech))+"筆技術與"+str(len(neuro))+"筆神經科技記錄。新增量子、HPC與科研設施資料；量子實驗結果、理論峰值與設施所在地分開記錄，不能推導國家排名。首批與歷史批次保留，249地區全面核實仍未完成。\n<!-- GLOBAL_ISO249_B03_END -->\n"
            with (ROOT/p).open("ab") as f:f.write(block.encode("utf-8"))
        manifest={"counts":counts,"new_output_sha256":{p.relative_to(ROOT).as_posix():digest(p) for p in [ROOT/QMD,*sorted((ROOT/REL).iterdir())]},"append_prefixes":{p.as_posix():{"bytes":int(baseline[p.as_posix()]["bytes"]),"sha256":baseline[p.as_posix()]["sha256"]} for p in append_paths},"baseline_file":"reports/2026-10-06/workspace_change_audit/global_b03_start_files.csv"}
        (HERE/"delivery_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(counts))
if __name__=="__main__":main()

