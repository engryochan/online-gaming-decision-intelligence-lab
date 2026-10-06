from pathlib import Path
import csv,json,hashlib,re,argparse
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
TABLE=Path("Reference/tables/07_global_technology_iso249_20261006")
def read(p):
    with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(base, delivery=False):
    coverage=read(base/TABLE/"registry_country_technology_coverage.csv")
    orgs=read(base/TABLE/"registry_global_organizations.csv")
    claims=read(base/TABLE/"registry_global_claims.csv")
    sources=read(base/TABLE/"registry_global_sources.csv")
    tech=read(base/TABLE/"registry_technology_products_tools.csv")
    neuro=read(base/TABLE/"registry_neurotechnology_global.csv")
    leads=read(base/TABLE/"registry_country_search_leads.csv")
    rels=read(base/TABLE/"registry_country_entity_relations.csv")
    mother=read(ROOT/"Reference/tables/01_country_area/registry_country_area_iso3166_20261004_enhanced.csv")
    codes={r["iso_alpha2"] for r in mother}
    assert len(coverage)==249 and {r["iso_alpha2"] for r in coverage}==codes
    def keys(rows,key):
        values={r[key] for r in rows};assert len(values)==len(rows),f"Duplicate {key}";return values
    eids=keys(orgs,"entity_id");sids=keys(sources,"source_id")
    keys(claims,"claim_id");keys(tech,"technology_id");keys(neuro,"neuro_id");keys(leads,"lead_id");keys(rels,"relation_id")
    urls={s["source_id"]:s for s in sources}
    for rows in (orgs,claims,tech,neuro,rels):
        for r in rows:
            assert r["source_id"] in sids or (not r["source_id"] and r.get("origin_batch")=="FRONTIER_196" and r.get("evidence_state","UNKNOWN")=="UNKNOWN")
            if "entity_id" in r:assert r["entity_id"] in eids
            if r.get("issuer_entity_id"):assert r["issuer_entity_id"] in eids
            if r.get("evidence_state")=="VERIFIED":assert urls[r["source_id"]]["access_state"]=="READABLE_SUPPORT",r
    assert len({re.sub(r"\W","",o["display_name"]).casefold() for o in orgs})==len(orgs)
    for o in orgs:
        if o["origin_batch"]=="GLOBAL_249":
            assert all(c in codes for c in o["country_candidate_iso_alpha2"].split(";") if c)
        assert o["world_frontier_rank_state"]=="UNKNOWN"
    for c in coverage:
        assert c["search_state"]=="SEARCH_COMPLETED" and c["N0_N7_level"]=="UNKNOWN"
        assert sum(l["iso_alpha2"]==c["iso_alpha2"] for l in leads)==int(c["search_lead_count"])
    for l in leads:assert l["iso_alpha2"] in codes and l["evidence_state"]=="UNKNOWN"
    for n in neuro:assert n["N0_N7_level"]=="UNKNOWN" and n["bandwidth_state"]=="UNKNOWN" and n["information_bandwidth_bits_per_second"]==""
    old=ROOT/"Reference/tables/06_frontier_ecosystem_20261006"
    for fn,combined in (("registry_frontier_organizations.csv",orgs),("registry_frontier_claims.csv",claims),("registry_frontier_sources.csv",sources)):
        original=read(old/fn);imported=[r for r in combined if r["origin_batch"]=="FRONTIER_196"]
        assert len(original)==len(imported)
        if fn!="registry_frontier_sources.csv": assert len(original)==196
        assert all(all(new[k]==v for k,v in row.items()) for row,new in zip(original,imported))
    p=base/"Reference/Global_Technology_ISO249_Registry.qmd"
    for target in re.findall(r"\]\((tables/[^)]+)\)",p.read_text(encoding="utf-8")):assert (p.parent/target).exists(),target
    result={"state":"PASS","checks":["249 unique ISO foreign keys","search result counts match country coverage","entity/source/product/neuro relationships","VERIFIED claims require readable primary or inherited source support","no country score or numeric bandwidth invented","old196 batch content retained","all annex table links resolve"],"counts":{"countries":len(coverage),"organizations":len(orgs),"technologies":len(tech),"neuro_records":len(neuro),"search_leads":len(leads)}}
    if delivery:
        manifest=json.loads((HERE/"delivery_manifest.json").read_text(encoding="utf-8"))
        for rel,digest in manifest["generated_sha256"].items():assert sha(ROOT/rel)==digest,rel
        for rel,digest in manifest["preserved_historical_sha256"].items():assert sha(ROOT/rel)==digest,rel
        user=manifest["preserved_user_html"];assert sha(ROOT/user["path"])==user["sha256"]
        active=ROOT/"Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd"
        assert hashlib.sha256(active.read_bytes()[:manifest["active_original_bytes"]]).hexdigest()==manifest["active_original_sha256"]
        ref=ROOT/"Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd"
        assert hashlib.sha256(ref.read_bytes()[:manifest["reference_original_bytes"]]).hexdigest()==manifest["reference_original_sha256"]
        result["preservation"]="Original aerospace report and assets, old196 tables, user HTML unchanged; active QMD and reference original bytes retained with append-only additions."
        html=ROOT/"Reference/Global_Technology_ISO249_Registry.html"
        assert html.exists()
        rendered=html.read_text(encoding="utf-8")
        assert all(x in rendered for x in ("GTO0103","GTT0044","N3_TARGET_NOT_RESULT","AW","ZW"))
        result["html_sha256"]=sha(html)
        result["checks"].append("new annex rendered; representative final records present")
    return result
if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--preview",action="store_true");args=parser.parse_args()
    result=check(HERE/"preview" if args.preview else ROOT,not args.preview)
    (HERE/("preview_validation.json" if args.preview else "delivery_validation.json")).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False))

