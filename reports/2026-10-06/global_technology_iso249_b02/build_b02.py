from pathlib import Path
import csv,json,hashlib,re,argparse
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
OLD=ROOT/"Reference/tables/07_global_technology_iso249_20261006"
REL=Path("Reference/tables/08_global_technology_iso249_20261006_b02")
QMD=Path("Reference/Global_Technology_ISO249_Registry_B02.qmd")
DATE="2026-10-06"
def read(p):
    with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(h,rows):
    return "\n".join(["| "+" | ".join(h)+" |","| "+" | ".join(["---"]*len(h))+" |"]+["| "+" | ".join(str(v).replace("|","&#124;").replace("\n"," ") for v in r)+" |" for r in rows])+"\n"
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--apply",action="store_true");args=ap.parse_args()
    baseline={r["path"]:r for r in read(ROOT/"reports/2026-10-06/workspace_change_audit/global_b02_start_files.csv")}
    append_paths=[Path("Reference/Global_Technology_ISO249_Registry.qmd"),Path("Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd")]
    if args.apply:
        assert not (ROOT/REL).exists() and not (ROOT/QMD).exists(),"Existing B02 output: review required"
        for p in append_paths:assert digest(ROOT/p)==baseline[p.as_posix()]["sha256"],f"User changed {p}"
    base=ROOT if args.apply else HERE/"preview"
    seed=json.loads((HERE/"curated_seed.json").read_text(encoding="utf-8"))
    orgs=read(OLD/"registry_global_organizations.csv");claims=read(OLD/"registry_global_claims.csv")
    sources=read(OLD/"registry_global_sources.csv");tech=read(OLD/"registry_technology_products_tools.csv")
    neuro=read(OLD/"registry_neurotechnology_global.csv");rels=read(OLD/"registry_country_entity_relations.csv")
    coverage=read(OLD/"registry_country_technology_coverage.csv")
    new=[];newtech=[];metrics=[];newneuro=[]
    urlsid={r["url"]:r["source_id"] for r in sources}
    def source(url,claim,state="VERIFIED",kind="PRIMARY_OFFICIAL"):
        if url in urlsid:return urlsid[url]
        sid=f"GBS{1+sum(s['source_id'].startswith('GBS') for s in sources):04d}"
        sources.append(dict(source_id=sid,url=url,supports=claim,source_class=kind,access_state="READABLE_SUPPORT" if state=="VERIFIED" else "INSUFFICIENT_OR_FAILED",checked_on=DATE,published_on="",archive_state="NO_RAW_HTTP_ARCHIVE",license_state="UNKNOWN",origin_batch="GLOBAL_249_B02"))
        urlsid[url]=sid;return sid
    for i,row in enumerate(seed["organizations"],1):
        name,country,kind,domain,url,claim,*tail=row;state=tail[0] if tail else "VERIFIED"
        sid=source(url,claim,state,"PRIMARY_RESEARCH_PAPER" if "nature.com" in url else "PRIMARY_OFFICIAL")
        eid=f"GBO{i:04d}"
        selection="ENABLING_POLICY_OR_RESEARCH_INFRASTRUCTURE_NOT_RANKED" if domain in ("TECHNOLOGY_POLICY","RESEARCH_FUNDING") else "FRONTIER_RESEARCH_CANDIDATE_NOT_RANKED"
        o=dict(entity_id=eid,display_name=name,entity_type=kind,primary_domain=domain,country_candidate_iso_alpha2=country,country_assignment_status="EDITORIAL_CANDIDATE_NOT_LEGAL_DOMICILE" if country else "MULTINATIONAL_OR_UNASSIGNED",legal_entity_status="DISPLAY_ORG_NOT_LEGAL_REGISTRY_VERIFIED",selection_status=selection,source_id=sid,as_of=DATE,origin_batch="GLOBAL_249_B02",legal_domicile_state="UNKNOWN",world_frontier_rank_state="UNKNOWN")
        orgs.append(o);new.append(o)
        claims.append(dict(claim_id=f"GBC{i:04d}",entity_id=eid,claim=claim,evidence_state=state,verification_scope="PUBLISHED_RESEARCH_AFFILIATION" if "nature.com" in url else ("PUBLIC_DESCRIPTION_ONLY" if state=="VERIFIED" else "UNKNOWN"),product_project_leads="",product_leads_state="UNKNOWN",performance_state="UNKNOWN",deployment_state="UNKNOWN",regulatory_state="UNKNOWN",source_id=sid,reviewed_on=DATE,origin_batch="GLOBAL_249_B02"))
    for i,row in enumerate(seed["technologies"],1):
        name,domain,kind,owner,url,claim,*tail=row;state=tail[0] if tail else "VERIFIED"
        sid=source(url,claim,state,"PRIMARY_RESEARCH_PAPER" if "nature.com" in url else "PRIMARY_OFFICIAL_OR_AUTHOR_REPOSITORY")
        eid=next(o["entity_id"] for o in new if o["display_name"]==owner)
        t=dict(technology_id=f"GBT{i:04d}",display_name=name,record_type=kind,domain=domain,issuer_entity_id=eid,issuer_relation_state="PUBLIC_SOURCE_ASSOCIATION_NOT_LEGAL_OWNERSHIP",public_description=claim,evidence_state=state,verification_scope="PUBLISHED_STUDY_DESCRIPTION" if kind=="RESEARCH_PROTOCOL" else "PUBLIC_DESCRIPTION_ONLY",source_id=sid,version_state="UNKNOWN",license_state="UNKNOWN",availability_state="UNKNOWN",independent_performance_state="NOT_REPLICATED_IN_THIS_REVIEW",global_rank_state="UNKNOWN",regulatory_state="UNKNOWN",as_of=DATE)
        tech.append(t);newtech.append(t)
    byname={t["display_name"]:t for t in newtech}
    for i,row in enumerate(seed["metrics"],1):
        name,metric,value,unit,stat,n,conditions,pub,doi=row;t=byname[name]
        metrics.append(dict(metric_id=f"GBM{i:04d}",technology_id=t["technology_id"],entity_id=t["issuer_entity_id"],metric_name=metric,value=value,unit=unit,statistic=stat,participant_count=n,conditions=conditions,study_date=pub,doi=doi,evidence_state="VERIFIED",verification_scope="PAPER_REPORTED_RESULT_NOT_INDEPENDENT_REPLICATION",source_id=t["source_id"],information_bandwidth_state="UNKNOWN",general_population_state="UNKNOWN",world_record_state="UNKNOWN",reviewed_on=DATE))
    for i,t in enumerate([t for t in newtech if t["record_type"]=="RESEARCH_PROTOCOL"],1):
        template={k:"UNKNOWN" for k in neuro[0]}
        sid=t["source_id"];study=[m for m in metrics if m["technology_id"]==t["technology_id"]]
        template.update(neuro_id=f"GBN{i:04d}",entity_id=t["issuer_entity_id"],project_name=t["display_name"],country_candidate_iso_alpha2="US",country_relation_state="PUBLISHED_AUTHOR_AFFILIATION_NOT_NATIONAL_LEVEL",invasiveness="INVASIVE_INTRACORTICAL" if i==1 else "INVASIVE_CORTICAL_SURFACE",modality="MICROELECTRODE" if i==1 else "ECoG",signal_direction="READ_ATTEMPTED_SPEECH",direction_state="PUBLISHED_RESEARCH_DESCRIPTION",remote_state="UNKNOWN",information_bandwidth_bits_per_second="",bandwidth_state="UNKNOWN",human_trial_state="PUBLISHED_SINGLE_PARTICIPANT_STUDY",trial_ids="",trial_registry_status="UNKNOWN",clinical_phase="UNKNOWN",publication_ids=study[0]["doi"],publication_state="VERIFIED_PUBLISHED_ARTICLE",patent_ids="",patent_state="UNKNOWN",regulatory_state="UNKNOWN",N0_N7_level="UNKNOWN",evidence_state="VERIFIED",verification_scope="PUBLISHED_STUDY_LIMITED_SCOPE",source_id=sid,notes="Published single-participant research, not general mind reading, commercial approval or measured bits/s. See registry_technology_metrics.csv.",as_of=DATE)
        neuro.append(template);newneuro.append(template)
    for name,code,kind,claim in [
      ("ALMA","CL","FACILITY_LOCATION","官網描述智利 Chajnantor 觀測設施及智利合作"),
      ("Georgia Innovation and Technology Agency","GE","OFFICIAL_CONTACT_LOCATION","官網聯絡地址為 Tbilisi, Georgia；排除美國Georgia州誤配"),
      ("BITRI","BW","PUBLIC_NATIONAL_RESEARCH_AFFILIATION","官網描述 Botswana 國家研究中心"),
      ("SIRDC","ZW","PUBLIC_GOVERNMENT_RESEARCH_AFFILIATION","官網描述由 Zimbabwe 政府建立"),
      ("National Academy of Sciences Armenia","AM","PUBLIC_NATIONAL_RESEARCH_AFFILIATION","官方頁面標示亞美尼亞國家科學院"),
      ("ANAS","AZ","PUBLIC_NATIONAL_RESEARCH_AFFILIATION","官方頁面標示 Azerbaijan National Academy of Sciences")]:
        o=next(o for o in new if o["display_name"]==name)
        rels.append(dict(relation_id=f"GBR{1+sum(r['relation_id'].startswith('GBR') for r in rels):04d}",entity_id=o["entity_id"],iso_alpha2=code,relation_type=kind,claim=claim,evidence_state="VERIFIED",verification_scope="PUBLIC_LOCATION_OR_AFFILIATION_NOT_DOMICILE_OR_COUNTRY_RANK",source_id=o["source_id"],as_of=DATE))
    for c in coverage:
        matched=[o for o in orgs if c["iso_alpha2"] in re.split("[;,]",o["country_candidate_iso_alpha2"])]
        c["editorial_entity_candidate_count"]=len(matched)
        c["candidate_public_descriptions_verified"]=sum(next(cl["evidence_state"] for cl in claims if cl["entity_id"]==o["entity_id"])=="VERIFIED" for o in matched)
        c["country_relation_verified_count"]=sum(r["iso_alpha2"]==c["iso_alpha2"] for r in rels)
    counts=dict(organizations=len(orgs),new_organizations=len(new),new_organization_descriptions_verified=sum(c["origin_batch"]=="GLOBAL_249_B02" and c["evidence_state"]=="VERIFIED" for c in claims),organization_descriptions_verified=sum(c["evidence_state"]=="VERIFIED" for c in claims),technologies=len(tech),new_technologies=len(newtech),neuro_records=len(neuro),published_studies=len(newneuro),reported_metrics=len(metrics),countries_with_editorial_candidates=sum(int(c["editorial_entity_candidate_count"])>0 for c in coverage))
    tables={"registry_global_organizations.csv":orgs,"registry_global_claims.csv":claims,"registry_global_sources.csv":sources,"registry_technology_products_tools.csv":tech,"registry_neurotechnology_global.csv":neuro,"registry_country_entity_relations.csv":rels,"registry_country_technology_coverage.csv":coverage,"registry_technology_metrics.csv":metrics}
    (base/REL).mkdir(parents=True,exist_ok=True)
    for fn,rows in tables.items():
        with (base/REL/fn).open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    dictionary=dict(counts=counts,batch="B02",as_of=DATE,evidence_rules=["VERIFIED is claim-specific.","Paper metrics are verified as reported, not independently replicated.","Candidate country is not legal domicile or national frontier rank.","80ms increment is not end-to-end latency or information bandwidth.","Research infrastructure and policy roles do not constitute world-leading technology."],table_fields={fn:list(rows[0]) for fn,rows in tables.items()},source_anomalies=seed["source_anomalies"])
    (base/REL/"data_dictionary.json").write_text(json.dumps(dictionary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    orgclaim={c["entity_id"]:c for c in claims};sidurl={s["source_id"]:s["url"] for s in sources}
    text="""---
title: "全球科技登記第二批：機構覆蓋、先進計算與人體 BCI 證據"
lang: zh-TW
format:
  html:
    toc: true
    embed-resources: true
    theme: cosmo
execute:
  enabled: false
---

"""
    text+=f"""本批核實 {len(new)} 筆新增機構／科研單位／計畫候選，補入 {len(newtech)} 筆具名技術與工具、3篇人体BCI原始研究及6筆帶測試條件的數值記錄。累計 {len(orgs)} 筆機構候選、{len(tech)} 筆技術、{len(neuro)} 筆神經科技項目。249地區母表與原首輪檢索日誌保持不變；有編輯候選的地區由61增至{counts['countries_with_editorial_candidates']}。尚未建立候選的地區依然需要當地語言專項核實。

這不是全球全部科技普查或頂尖排名。大型科研設施、國家研究機構及政策資助單位分別登記角色；國家級機構不因入表就成為世界頂尖。性能主張須保留日期、樣本與任務。[首批附錄](Global_Technology_ISO249_Registry.qmd)與原報告保留；本批完整整合表在新的08目錄，避免覆寫07資料。

## 三篇人体研究與測試條件

[Willett等2023研究](https://www.nature.com/articles/s41586-023-06377-x)記錄一位ALS參與者的皮質內微電極嘗試語音解碼：報告62 words/min；125000詞條件WER為23.8%，50詞條件為9.1%。後兩者不是同一詞彙難度。結果不能推廣成一般人口或全部植入器件的性能，也不是自由思想讀取。

[Metzger等2023研究](https://www.nature.com/articles/s41586-023-06443-4)使用一位參與者的皮質表面記錄；文本解碼中位速度78 words/min、中位WER25%。頁面列2024作者更正，數字依目前可讀摘要；本輪未完整復核更正影響。它與前項的平均速度、任務及統計口徑不同，不能直接排全球名次。

[Littlejohn等2025技術報告](https://www.nature.com/articles/s41593-025-01905-6)描述一位參與者的流式語音合成，摘要列80ms神經解碼增量。這是演算法步長，不是端到端延遲，更不是bits/s。論文資料存取條件混合，本輪沒有下載人體資料或執行重現。[作者軟件倉庫](https://github.com/cheoljun95/streaming.braindecoder)已可讀；存在代碼不代表可自由商用或本輪已重現。

以上是2023／2025有日期的研究例證，並未證明它們仍是2026全球最新或最高性能。N0～N7與信息頻寬仍UNKNOWN；正式臨床階段、試驗登記狀態、專利及監管狀態尚未查證。

"""
    text+=table(["項目","指標","數值","統計","樣本","條件"],[[byname[next(t["display_name"] for t in newtech if t["technology_id"]==m["technology_id"])]["display_name"],m["metric_name"],m["value"]+" "+m["unit"],m["statistic"],m["participant_count"],m["conditions"]] for m in metrics])
    text+="\n## 半導體與大型科研設施\n\n[Rapidus官網](https://www.rapidus.inc/en/)描述2025年開始試產、2027年計畫量產；試產與量產分開。2nm是官方製程名稱，本輪未獨立量測物理尺寸或性能。Cerebras、Groq等只核實具名計算產品與架構公開描述，不採用官網最高性能宣傳作獨立比較。\n\n[ALMA官網](https://www.almaobservatory.org/en/about-alma/)描述智利設施及跨國合作。設施所在地、參與國、科研產出與各國自主製造能力分開；不以跨國天文設施給某國科技整體分數。\n\n"
    text+=table(["ID","技術／工具","類型","核實範圍","來源"],[[t["technology_id"],t["display_name"],t["record_type"],t["public_description"],f'[來源]({sidurl[t["source_id"]]})'] for t in newtech])
    text+="\n## 新增機構／科研單位\n\n"
    text+=table(["ID","名稱","國別候選","領域","公開描述","證據"],[[o["entity_id"],o["display_name"],o["country_candidate_iso_alpha2"] or "跨國",o["primary_domain"],orgclaim[o["entity_id"]]["claim"],f'[{orgclaim[o["entity_id"]]["evidence_state"]}]({sidurl[o["source_id"]]})'] for o in new])
    text+="\n## 整合資料與来源異常\n\n"
    text+=table(["資料","連結"],[[fn,f'[{fn}](tables/08_global_technology_iso249_20261006_b02/{fn})'] for fn in tables])
    text+="\n[數據字典](tables/08_global_technology_iso249_20261006_b02/data_dictionary.json)含計數、欄位、證據邊界與來源異常。首次逐地搜索952筆線索仍見07目錄；本批沒有把其中未知關係的結果升格為實體。\n\nGhana的候選主域名本輪返回博彩內容，原因未查明，標記CONTENT_MISMATCH而非科研證據；改用CSIR-INSTI的2024官方年報，僅支持其當年研究業務。BITRI與SIRDC使用可讀的無www官方About頁；失敗網址保留於來源異常。Georgia新增GITA官方Tbilisi地址關係，以排除先前美國Georgia州搜尋誤配。\n\n下一輪仍須核實其餘地區的具體項目、原始成果與部署條件；沒有找到或核實候選不代表沒有能力。\n"
    (base/QMD).parent.mkdir(parents=True,exist_ok=True);(base/QMD).write_text(text,encoding="utf-8")
    if args.apply:
        for p in append_paths:
            block="\n\n<!-- GLOBAL_ISO249_B02_START -->\n## 全球科技第二批增補\n\n新增 [第二批科技與原始研究證據](Global_Technology_ISO249_Registry_B02.qmd)及 [HTML](Global_Technology_ISO249_Registry_B02.html)。完整整合表位於08目錄；累計"+str(len(orgs))+"筆機構候選、"+str(len(tech))+"筆技術與"+str(len(neuro))+"筆神經科技記錄。3篇人體BCI原始研究另列6筆數值與測試條件；論文報告結果不等於獨立重現或世界排名。首批與歷史批次保留，249地區全面核實仍未完成。\n<!-- GLOBAL_ISO249_B02_END -->\n"
            with (ROOT/p).open("ab") as f:f.write(block.encode("utf-8"))
        manifest={"counts":counts,"new_output_sha256":{p.relative_to(ROOT).as_posix():digest(p) for p in [ROOT/QMD,*sorted((ROOT/REL).iterdir())]},"append_prefixes":{p.as_posix():{"bytes":int(baseline[p.as_posix()]["bytes"]),"sha256":baseline[p.as_posix()]["sha256"]} for p in append_paths},"baseline_file":"reports/2026-10-06/workspace_change_audit/global_b02_start_files.csv"}
        (HERE/"delivery_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(counts))
if __name__=="__main__":main()

