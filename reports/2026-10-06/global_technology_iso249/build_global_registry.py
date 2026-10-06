from pathlib import Path
import csv, json, hashlib, re, argparse
from collections import Counter

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
TABLE_REL=Path("Reference/tables/07_global_technology_iso249_20261006")
ANNEX_REL=Path("Reference/Global_Technology_ISO249_Registry.qmd")
ACTIVE_REL=Path("Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd")
DATE="2026-10-06"
def readcsv(p):
    with p.open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower()) if s.isascii() else s.casefold()
def writecsv(p, rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)
def mdtable(headers, rows):
    def esc(v): return str(v).replace("|","&#124;").replace("\n"," ")
    return "\n".join(["| "+" | ".join(headers)+" |","| "+" | ".join(["---"]*len(headers))+" |"]+["| "+" | ".join(esc(v) for v in r)+" |" for r in rows])+"\n"
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--apply",action="store_true")
    args=parser.parse_args()
    seed=json.loads((HERE/"curated_seed.json").read_text(encoding="utf-8"))
    search=json.loads((HERE/"country_search_log.json").read_text(encoding="utf-8"))["records"]
    baseline={r["path"]:r for r in readcsv(ROOT/"reports/2026-10-06/workspace_change_audit/global_start_files.csv")}
    if args.apply:
        for rel in (ACTIVE_REL,Path("AGENTS.md"),Path("Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd")):
            assert sha(ROOT/rel)==baseline[rel.as_posix()]["sha256"],f"User changes detected: {rel}"
        manifest=HERE/"delivery_manifest.json"
        if manifest.exists():
            for rel, digest in json.loads(manifest.read_text(encoding="utf-8"))["generated_sha256"].items():
                assert (ROOT/rel).exists() and sha(ROOT/rel)==digest,f"Generated file edited: {rel}"
        else:
            assert not (ROOT/ANNEX_REL).exists() and not (ROOT/TABLE_REL).exists(),"New output already exists; review first"
    outroot=ROOT if args.apply else HERE/"preview"
    old=ROOT/"Reference/tables/06_frontier_ecosystem_20261006"
    orgs=readcsv(old/"registry_frontier_organizations.csv")
    claims=readcsv(old/"registry_frontier_claims.csv")
    sources=readcsv(old/"registry_frontier_sources.csv")
    for o in orgs: o.update(origin_batch="FRONTIER_196",legal_domicile_state="UNKNOWN",world_frontier_rank_state="UNKNOWN")
    for c in claims: c["origin_batch"]="FRONTIER_196"
    for s in sources: s["origin_batch"]="FRONTIER_196"
    neworg=[]; tech=[]; neuro=[]; links=[]
    source_by_url={s["url"]:s["source_id"] for s in sources}
    def source(url, claim, state):
        if url in source_by_url: return source_by_url[url]
        sid=f"GTS{len([s for s in sources if s['source_id'].startswith('GTS')])+1:04d}"
        sources.append(dict(source_id=sid,url=url,supports=claim,source_class="PRIMARY_OFFICIAL",access_state="READABLE_SUPPORT" if state=="VERIFIED" else "INSUFFICIENT_OR_FAILED",checked_on=DATE,published_on="",archive_state="NO_RAW_HTTP_ARCHIVE",license_state="UNKNOWN",origin_batch="GLOBAL_249"))
        source_by_url[url]=sid
        return sid
    for i,row in enumerate(seed["organizations"],1):
        name,country,kind,domain,url,claim,*tail=row
        state=tail[0] if tail else "VERIFIED"
        sid=source(url,claim,state)
        eid=f"GTO{i:04d}"
        selection="ENABLING_POLICY_OR_ECOSYSTEM_NOT_TECHNOLOGY_RANK" if "POLICY" in domain or kind in ("GOVERNMENT_MINISTRY","TECHNOLOGY_PARK") else "FRONTIER_RESEARCH_CANDIDATE_NOT_RANKED"
        o=dict(entity_id=eid,display_name=name,entity_type=kind,primary_domain=domain,country_candidate_iso_alpha2=country,country_assignment_status="EDITORIAL_CANDIDATE_NOT_LEGAL_DOMICILE" if country else "MULTINATIONAL_OR_UNASSIGNED",legal_entity_status="DISPLAY_ORG_NOT_LEGAL_REGISTRY_VERIFIED",selection_status=selection,source_id=sid,as_of=DATE,origin_batch="GLOBAL_249",legal_domicile_state="UNKNOWN",world_frontier_rank_state="UNKNOWN")
        orgs.append(o);neworg.append(o)
        claims.append(dict(claim_id=f"GTC{i:04d}",entity_id=eid,claim=claim,evidence_state=state,verification_scope="PUBLIC_DESCRIPTION_ONLY" if state=="VERIFIED" else "NOT_VERIFIED_IN_BATCH",product_project_leads="",product_leads_state="UNKNOWN",performance_state="UNKNOWN",deployment_state="UNKNOWN",regulatory_state="UNKNOWN",source_id=sid,reviewed_on=DATE,origin_batch="GLOBAL_249"))
    for i,row in enumerate(seed["technologies"],1):
        name,domain,kind,url,claim,*tail=row;state=tail[0] if tail else "VERIFIED"
        sid=source(url,claim,state)
        same=[o for o in neworg if o["source_id"]==sid]
        # A shared source supports an editorial issuer link, not legal ownership.
        issuer=same[0]["entity_id"] if len(same)==1 else ""
        if name=="Layer 7-T": issuer=next(o["entity_id"] for o in neworg if o["display_name"]=="Precision Neuroscience")
        tech.append(dict(technology_id=f"GTT{i:04d}",display_name=name,record_type=kind,domain=domain,issuer_entity_id=issuer,issuer_relation_state="EDITORIAL_SOURCE_ASSOCIATION" if issuer else "UNKNOWN",public_description=claim,evidence_state=state,verification_scope="PUBLIC_DESCRIPTION_ONLY" if state=="VERIFIED" else "UNKNOWN",source_id=sid,version_state="UNKNOWN",license_state="UNKNOWN",availability_state="UNKNOWN",independent_performance_state="UNKNOWN",global_rank_state="UNKNOWN",regulatory_state="FDA_510K_K242618_LIMITED_DEVICE_USE" if name=="Layer 7-T" else "UNKNOWN",as_of=DATE))
    ndefs=[
      ("Neuralink","UNSPECIFIED_PROJECT","UNKNOWN","UNKNOWN","UNKNOWN","UNKNOWN","UNKNOWN","UNKNOWN"),
      ("Synchron","Stentrode","INVASIVE_ENDOVASCULAR","UNKNOWN","UNKNOWN","UNKNOWN","HUMAN_TRIALS_VENDOR_DESCRIPTION","INVESTIGATIONAL_VENDOR_DESCRIPTION"),
      ("Precision Neuroscience","Layer 7-T","INVASIVE_CORTICAL_SURFACE","ECoG","READ_AND_STIMULATE","NO_WIRELESS_DEVICE","UNKNOWN","FDA_510K_K242618_LIMITED_DEVICE_USE"),
      ("Paradromics","Connexus","IMPLANTABLE","UNKNOWN","READ_COMMUNICATION_INTENT","UNKNOWN","HUMAN_TRIALS_VENDOR_DESCRIPTION","UNKNOWN"),
      ("Blackrock Neurotech","UNSPECIFIED_PLATFORM","UNKNOWN","UNKNOWN","UNKNOWN","UNKNOWN","HUMAN_STUDIES_VENDOR_DESCRIPTION","UNKNOWN"),
      ("g.tec","g.NAUTILUS","NONINVASIVE_EEG","EEG","READ","UNKNOWN","UNKNOWN","UNKNOWN"),
      ("Neuroelectrics","Starstim","NONINVASIVE","EEG;tES","READ_AND_STIMULATE","REMOTE_PROTOCOL_DELIVERY_VENDOR_DESCRIPTION","UNKNOWN","UNKNOWN"),
      ("BrainGate","RESEARCH_CONSORTIUM","UNKNOWN","UNKNOWN","UNKNOWN","UNKNOWN","UNKNOWN","UNKNOWN"),
      ("Artinis","fNIRS_RESEARCH_DEVICES","NONINVASIVE_OPTICAL","fNIRS","MEASURE_HEMODYNAMICS","UNKNOWN","UNKNOWN","UNKNOWN"),
      ("NIRx","fNIRS_SYSTEMS","NONINVASIVE_OPTICAL","fNIRS","MEASURE_HEMODYNAMICS","UNKNOWN","UNKNOWN","UNKNOWN"),
      ("Magstim","NEUROSTIMULATION_DEVICES","UNKNOWN","UNKNOWN","UNKNOWN","UNKNOWN","UNKNOWN","UNKNOWN"),
      ("BrainsWay","Deep TMS","NONINVASIVE","TMS","STIMULATE","UNKNOWN","UNKNOWN","UNKNOWN"),
      ("DARPA N3","N3_TARGET_NOT_RESULT","NONSURGICAL_TARGET","UNKNOWN","BIDIRECTIONAL_TARGET","UNKNOWN","UNKNOWN","UNKNOWN"),
    ]
    for i,(name,project,invasive,modality,direction,remote,human,reg) in enumerate(ndefs,1):
        o=next(x for x in neworg if x["display_name"]==name)
        sid=o["source_id"]
        notes="Fields describe the named product or stated research goal; not the whole organization."
        if name=="Precision Neuroscience":
            sid=source_by_url["https://www.accessdata.fda.gov/cdrh_docs/pdf24/K242618.pdf"]
            notes="FDA PDF pp.4-6: temporary <30 days; 1024 contacts; no wireless; healthcare environment. Electrode clearance does not clear a chronic wireless BCI."
        if name=="Neuroelectrics": notes="Remote means network delivery of treatment protocols to a worn device; not distance brain reading or stimulation without a device. Trial links NCT04770337/NCT05205915 exist; status not verified."
        if name=="Synchron": notes="Vendor describes US/Australia clinical trials and states investigational, no commercial approval. No regulator-wide status inferred."
        if name=="DARPA N3": notes="Official archived page says program complete. Bidirectional and nonsurgical are goals; numerical goals are not measured information bandwidth."
        evidence="UNKNOWN" if name=="Neuralink" else "VERIFIED"
        neuro.append(dict(neuro_id=f"GTN{i:04d}",entity_id=o["entity_id"],project_name=project,country_candidate_iso_alpha2=o["country_candidate_iso_alpha2"],country_relation_state="EDITORIAL_NOT_NATIONAL_CAPABILITY",invasiveness=invasive,modality=modality,signal_direction=direction,direction_state="PROGRAM_TARGET_NOT_ACHIEVEMENT" if name=="DARPA N3" else ("PUBLIC_DESCRIPTION_ONLY" if direction!="UNKNOWN" else "UNKNOWN"),remote_state=remote,information_bandwidth_bits_per_second="",bandwidth_state="UNKNOWN",bandwidth_protocol="UNKNOWN",human_trial_state=human,trial_ids="NCT04770337;NCT05205915" if name=="Neuroelectrics" else "",trial_registry_status="UNKNOWN",clinical_phase="UNKNOWN",publication_ids="",publication_state="UNKNOWN",patent_ids="",patent_state="UNKNOWN",regulatory_state=reg,regulatory_jurisdiction="US" if name=="Precision Neuroscience" else "UNKNOWN",N0_N7_level="UNKNOWN",evidence_state=evidence,verification_scope="FIELD_LIMITED_PUBLIC_DESCRIPTION" if evidence=="VERIFIED" else "UNKNOWN",source_id=sid,notes=notes,as_of=DATE))
    countries=readcsv(ROOT/"Reference/tables/01_country_area/registry_country_area_iso3166_20261004_enhanced.csv")
    codes={c["iso_alpha2"] for c in countries}
    assert len(codes)==len(countries)==249
    assert {r["iso_alpha2"] for r in search}==codes
    assert all(r["search_state"]=="SEARCH_COMPLETED" for r in search)
    leads=[];coverage=[]
    claim_by_entity={c["entity_id"]:c for c in claims}
    for r in search:
        for j,x in enumerate(r["results"],1):
            leads.append(dict(lead_id=f"GL{r['iso_alpha2']}{j:02d}",iso_alpha2=r["iso_alpha2"],query=r["query"],title=x["title"],url=x["url"],provider=r.get("provider","TAVILY"),evidence_state="UNKNOWN",country_relationship_state="UNREVIEWED_SEARCH_RESULT",relevance_state="UNKNOWN_MAY_BE_IRRELEVANT",as_of=DATE))
        candidates=[o for o in orgs if r["iso_alpha2"] in re.split(r"[;,]",o["country_candidate_iso_alpha2"])]
        verified=[o for o in candidates if claim_by_entity[o["entity_id"]]["evidence_state"]=="VERIFIED"]
        coverage.append(dict(iso_alpha2=r["iso_alpha2"],name_en=r["name_en"],search_state=r["search_state"],broad_queries_completed=1,retry_count=len(r.get("attempt_history",[])),search_lead_count=len(r["results"]),editorial_entity_candidate_count=len(candidates),candidate_public_descriptions_verified=len(verified),country_relation_verified_count=sum(1 for p in links if p["iso_alpha2"]==r["iso_alpha2"]),country_frontier_capability_state="UNKNOWN",N0_N7_level="UNKNOWN",research_completion_state="BROAD_DISCOVERY_ONLY_ENTITY_AND_SECTOR_REVIEW_INCOMPLETE",query=r["query"],provider=r.get("provider","TAVILY"),searched_on=DATE))
    # Verified country relations are deliberately separate and narrowly scoped.
    synchron=next(o for o in neworg if o["display_name"]=="Synchron")
    for code in ("US","AU"):
        links.append(dict(relation_id=f"GTR{len(links)+1:04d}",entity_id=synchron["entity_id"],iso_alpha2=code,relation_type="VENDOR_DESCRIBED_TRIAL_LOCATION",claim="官方頁面描述在該地進行 Stentrode 臨床研究",evidence_state="VERIFIED",verification_scope="VENDOR_DESCRIPTION_NOT_TRIAL_STATUS_OR_DOMICILE",source_id=synchron["source_id"],as_of=DATE))
    for c in coverage: c["country_relation_verified_count"]=sum(p["iso_alpha2"]==c["iso_alpha2"] for p in links)
    legacy_leads=[dict(entity_id=c["entity_id"],product_project_leads=c["product_project_leads"],evidence_state="UNKNOWN",source_id=c["source_id"],notes="Inherited discovery terms; compound text is not a verified product registry.") for c in claims if c["origin_batch"]=="FRONTIER_196"]
    tables={"registry_country_technology_coverage.csv":coverage,"registry_global_organizations.csv":orgs,"registry_global_claims.csv":claims,"registry_global_sources.csv":sources,"registry_technology_products_tools.csv":tech,"registry_neurotechnology_global.csv":neuro,"registry_country_entity_relations.csv":links,"registry_country_search_leads.csv":leads,"registry_legacy_product_project_leads.csv":legacy_leads}
    for fn,rows in tables.items():writecsv(outroot/TABLE_REL/fn,rows)
    counts=dict(iso_entries=249,completed_country_queries=249,search_leads=len(leads),organizations=len(orgs),new_organizations=len(neworg),organization_public_descriptions_verified=sum(c["evidence_state"]=="VERIFIED" for c in claims),new_organization_public_descriptions_verified=sum(c["evidence_state"]=="VERIFIED" for c in claims if c["origin_batch"]=="GLOBAL_249"),technologies=len(tech),technology_public_descriptions_verified=sum(t["evidence_state"]=="VERIFIED" for t in tech),neuro_records=len(neuro),countries_with_editorial_entity_candidates=sum(c["editorial_entity_candidate_count"]>0 for c in coverage),countries_with_verified_frontier_level=0)
    text="""---
title: "全球科技登記：ISO 3166-1 249 國家／地區"
subtitle: "有來源的機構、產品、工具與神經科技；2026-10-06 首輪"
lang: zh-Hant
format:
  html:
    toc: true
    embed-resources: true
    theme: cosmo
execute:
  enabled: false
---

"""
    text+=f"""本附錄以項目現有 ISO 3166-1 母表的 **249 個國家／地區**為外鍵，記錄逐地實際檢索、機構公開描述與具名技術。保留原有 196 筆機構批次，新增 {len(neworg)} 筆候選，共 {len(orgs)} 筆；另有 {len(tech)} 筆產品／軟件／組件／工具／平台與 {len(neuro)} 筆神經科技登記。這是已完成的首輪檢索與部分實體核實，**並未完成每地每領域的全面查證，也不是全球全部科技實體或世界頂尖排名**。

## 範圍與證據判讀

ISO 清單包括國家、屬地與特殊地理區域，不能把 249 項都稱為主權國家。母表沿用 [ISO 國家代碼框架](https://www.iso.org/iso-3166-country-codes.html)，國名為項目母表英名；不以名稱作主鍵。

逐地完成一個廣泛科技檢索，保存 {len(leads)} 筆實際搜尋結果及查詢日誌。搜尋結果可能無關、過時或指向另一國機構，全部標記 UNKNOWN，不能自動升格為所在地機構。三次初次限流失敗均已重試，歷史保留。沒有候選機構的地區代表尚未找到／核實，並不代表沒有科技能力。

VERIFIED 僅適用於具體 claim 與來源支持的範圍：官網或官方文件確實描述該研究／產品。它不能延伸為獨立性能驗證、最新部署、臨床療效、合法使用或世界第一。國別候選欄為編輯定位，法律註冊地 UNKNOWN；跨國機構可不指派國家。已查證的國別關係另列窄義關係表，目前僅登記 Synchron 官網描述的美澳研究地點。

候選領域包含地緣學、戰略情報、軍工、宇航、GEOINT、AI、半導體／計算、量子、機械人／自主系統、生物／神經科技、能源／材料、大型科學與科研軟件。入選是後續技術查證優先清單；每項的全球排名仍 UNKNOWN。[WIPO GII 2026](https://www.wipo.int/en/web/global-innovation-index/2026/index)的經濟體與創新集群指標可供國際背景參考，不可轉換成所有 249 地區或每家企業的技術排名。

## 數據表與核實數量

"""
    for k,v in counts.items(): text+=f"- {k}: **{v}**\n"
    text+="\n"+mdtable(["資料表","內容"],[[f"[{fn}](tables/07_global_technology_iso249_20261006/{fn})",desc] for fn,desc in [
      ("registry_country_technology_coverage.csv","249 地區：查詢、線索數、候選數與未完成狀態"),
      ("registry_global_organizations.csv","歷史196筆加新增候選；顯示實體與法律法人分開"),
      ("registry_global_claims.csv","逐項短主張、VERIFIED／UNKNOWN與核實範圍"),
      ("registry_global_sources.csv","來源網址、日期、可讀狀態與支持範圍"),
      ("registry_technology_products_tools.csv","具名軟件／組件／工具／設備／平台"),
      ("registry_neurotechnology_global.csv","侵入性、模態、方向、遠程、頻寬、試驗與監管"),
      ("registry_country_entity_relations.csv","有來源的窄義國別關係"),
      ("registry_country_search_leads.csv","逐地實際結果；全部未審查線索"),
      ("registry_legacy_product_project_leads.csv","原196筆的產品／項目研究詞，未冒充已核實產品")
    ]])
    text+="\n## 新增機構與研究計畫\n\n"
    text+=mdtable(["ID","機構／計畫","國別候選","領域","公開描述","證據／来源"],[[o["entity_id"],o["display_name"],o["country_candidate_iso_alpha2"] or "跨國／未指派",o["primary_domain"],claim_by_entity[o["entity_id"]]["claim"],f'[{claim_by_entity[o["entity_id"]]["evidence_state"]}]({next(s["url"] for s in sources if s["source_id"]==o["source_id"])})'] for o in neworg])
    text+="\n## 具名技術、產品、工具與平台\n\n版本、授權、獨立效能、全球排名與一般可用性未核實；除明示的特定監管條目外均為 UNKNOWN。\n\n"
    text+=mdtable(["ID","名稱","類型","用途／核實范围","證據／來源"],[[t["technology_id"],t["display_name"],t["record_type"],t["public_description"],f'[{t["evidence_state"]}]({next(s["url"] for s in sources if s["source_id"]==t["source_id"])})'] for t in tech])
    text+="""\n## 神經科技：產品與目標分开

[Layer 7-T 的 FDA 文件](https://www.accessdata.fda.gov/cdrh_docs/pdf24/K242618.pdf)支持少於 30 天的皮質表面記錄、監測與刺激用途，描述 1024 接點、無無線功能及專業醫療環境使用。這個特定电極的 510(k) clearance 不等同研究中的長期無線 BCI 系統全面獲准；電極接點數也不能換算成語義信息頻寬。

[DARPA N3 官方存檔](https://www.darpa.mil/research/programs/next-generation-nonsurgical-neurotechnology)標記計畫完成。非手術與雙向屬研發目標，沒有在本登記中當作已達成性能。[Neuroelectrics](https://www.neuroelectrics.com/)描述遠端下發治療協議至佩戴設備；這不是無設備的遠距讀腦。fNIRS 量測血氧動力學，不等於直接解讀思想。

信息頻寬必須有任務、編碼、試驗條件、統計方法與 bits/s 證據；本批未建立可比較的頻寬證據。論文、專利、試驗登記狀態及正式臨床階段仍待逐項核實。官網人體研究說明以 VENDOR_DESCRIPTION 明示，不以網站宣傳當作試驗結果。ClinicalTrials.gov 兩個連結可辨識，但本輪頁面內容不足，狀態保留 UNKNOWN。N0～N7 評分必須先有固定定義與對應證據，本批不給任何國家或設備推測分數。

"""
    text+=mdtable(["機構／項目","侵入性","模態","方向","遠程／設備","證據"],[[next(o["display_name"] for o in orgs if o["entity_id"]==n["entity_id"])+" / "+n["project_name"],n["invasiveness"],n["modality"],n["signal_direction"],n["remote_state"],n["evidence_state"]] for n in neuro])
    text+="\n## 249 地區逐地检索覆蓋\n\n「公開描述已核實」只計數該國候選下的機構說明，不證明法律所在地或國家頂尖能力。所有國家科技等級仍 UNKNOWN。實際查询、網址與檢索來源見 CSV 及原始檢索日誌。\n\n"
    text+=mdtable(["ISO","國家／地區","檢索線索","機構候選","候選公開描述已核實","全面核實／國家等級"],[[c["iso_alpha2"],c["name_en"],c["search_lead_count"],c["editorial_entity_candidate_count"],c["candidate_public_descriptions_verified"],"未完成 / UNKNOWN"] for c in coverage])
    text+="""\n## 下一輪查證清單與文件保留

每個地區還需當地語言與各領域檢索，辨識本地機構、外地營運、研究合作與屬地／宗主國關係；搜尋線索先驗證國別相關性，再作為新實體。各前沿候選需補原始論文、可重現基準、專利公開號、監管原始文件與試驗方案，將目標、原型、人體研究、獲准用途及量產分開。

原196筆登記及原宇航報告保持不變。本附錄是獨立增補，主生態報告仅附加連結與本批摘要；本輪已有使用者變更的主報告 HTML 保留，不能視為本附錄的最新渲染結果。完整項目雜湊掃描只證明版本變動與保留狀態，不代表全項目文字已逐句事實查核。
"""
    p=outroot/ANNEX_REL;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding="utf-8")
    schema={"evidence_rule":"VERIFIED is claim/field-scoped, not entity-wide or global-rank verification.","country_rule":"ISO country/area mother is the key; editorial candidate associations are not verified domicile.","empty_numeric_rule":"Empty numeric fields mean UNKNOWN, never zero.","scope":"249 broad country queries; curated entity descriptions; no exhaustive country-sector/entity census.","snapshot_date":DATE,"timezone":"Asia/Tbilisi","counts":counts,"table_fields":{fn:list(rows[0]) for fn,rows in tables.items()},"limitations":["One broad query per country/area is insufficient for complete discovery.","Search leads may be irrelevant and are not entities.","No comparable global frontier benchmark or N0-N7 country score.","Most trial, publication, patent, licence and performance details remain UNKNOWN."]}
    (outroot/TABLE_REL/"data_dictionary.json").write_text(json.dumps(schema,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    outputs=[ANNEX_REL]+[TABLE_REL/fn for fn in tables]+[TABLE_REL/"data_dictionary.json"]
    if args.apply:
        block=f"""\n\n<!-- GLOBAL_TECHNOLOGY_ISO249_20261006_START -->
## 全球科技 ISO 249 地區首輪增補

本輪新增 [全球科技登記附錄](Global_Technology_ISO249_Registry.qmd)及 [HTML 閱讀版](Global_Technology_ISO249_Registry.html)，以既有 ISO 3166-1 母表的 249 個國家／地區為外鍵。已完成 249 次逐地廣泛檢索，留下 {len(leads)} 筆 UNKNOWN 搜尋線索；原196筆機構保留，新增 {len(neworg)} 筆，共 {len(orgs)} 筆候選。新增機構公開描述 {counts['new_organization_public_descriptions_verified']} 筆 VERIFIED，另列 {len(tech)} 筆技術／產品／軟件／組件／工具／平台及 {len(neuro)} 筆神經科技記錄。

上述196筆及其核實統計是原批次，不是全球附錄總數。VERIFIED 僅表示特定公開描述獲來源支持；逐國各領域核實、完整實體普查、全球頂尖排名及 N0～N7 國家等級均未完成。國別候選不是已核實法律所在地。新增 [數據字典](tables/07_global_technology_iso249_20261006/data_dictionary.json)及 [逐地覆蓋表](tables/07_global_technology_iso249_20261006/registry_country_technology_coverage.csv)明示所有尚未查證欄位。

DARPA N3 的雙向非手術性能屬目標；Layer 7-T 的 FDA 文件僅支持特定暫時性皮質電極用途，不能擴張為所有研究中 BCI 系統已獲准。詳見附錄來源與逐欄證據。
<!-- GLOBAL_TECHNOLOGY_ISO249_20261006_END -->
"""
        # Preserve existing bytes and line endings; append only.
        with (ROOT/ACTIVE_REL).open("ab") as f:f.write(block.encode("utf-8"))
        with (ROOT/"AGENTS.md").open("ab") as f:f.write("\n- 全球 ISO 249 科技增補位於 `Reference/Global_Technology_ISO249_Registry.qmd` 與 `Reference/tables/07_global_technology_iso249_20261006/`；原196筆為歷史批次。主報告只附加有界增補，不覆寫原宇航報告、使用者 HTML 或舊196筆資料。全球生成器預設 preview；apply 前核對基線與輸出雜湊，不以刷新基線繞過使用者修改。\n".encode("utf-8"))
        ref_rel=Path("Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd")
        with (ROOT/ref_rel).open("ab") as f:
            f.write("\n\n<!-- GLOBAL_ISO249_INDEX_20261006_START -->\n# 全球科技增補索引（2026-10-06）\n\n新增 [ISO 249 全球科技登記](Global_Technology_ISO249_Registry.qmd)與 [數據字典](tables/07_global_technology_iso249_20261006/data_dictionary.json)。已完成逐地廣泛檢索及部分具體機構／產品公開資料核實；歷史問答與196筆批次保留。神經科技已有具名項目逐欄登記，尚未完成全球普查，所有 N0～N7 國家分數仍 UNKNOWN。首輪檢索不等於249地區各領域已全面核實。\n<!-- GLOBAL_ISO249_INDEX_20261006_END -->\n".encode("utf-8"))
        manifest=dict(counts=counts,generated_sha256={r.as_posix():sha(ROOT/r) for r in outputs},preserved_historical_sha256={r:d["sha256"] for r,d in baseline.items() if r.startswith("Reference/Aerospace_Ecosystem_Report") or r.startswith("Reference/tables/06_frontier_ecosystem_20261006/")},preserved_user_html={"path":str(ACTIVE_REL.with_suffix(".html")).replace("\\","/"),"sha256":baseline[ACTIVE_REL.with_suffix(".html").as_posix()]["sha256"]},active_original_bytes=int(baseline[ACTIVE_REL.as_posix()]["bytes"]),active_original_sha256=baseline[ACTIVE_REL.as_posix()]["sha256"],reference_original_bytes=int(baseline[ref_rel.as_posix()]["bytes"]),reference_original_sha256=baseline[ref_rel.as_posix()]["sha256"])
        (HERE/"delivery_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"mode":"apply" if args.apply else "preview","counts":counts},ensure_ascii=False))
if __name__=="__main__":main()

