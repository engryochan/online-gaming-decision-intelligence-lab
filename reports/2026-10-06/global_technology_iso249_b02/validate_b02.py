from pathlib import Path
import csv,json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
REL=Path("Reference/tables/08_global_technology_iso249_20261006_b02")
def read(p):
    with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ap=argparse.ArgumentParser();ap.add_argument("--preview",action="store_true");a=ap.parse_args()
base=HERE/"preview" if a.preview else ROOT
tables={p.name:read(p) for p in (base/REL).glob("*.csv")}
orgs=tables["registry_global_organizations.csv"];claims=tables["registry_global_claims.csv"]
sources=tables["registry_global_sources.csv"];tech=tables["registry_technology_products_tools.csv"]
metrics=tables["registry_technology_metrics.csv"];neuro=tables["registry_neurotechnology_global.csv"]
eids={o["entity_id"] for o in orgs};sids={s["source_id"] for s in sources};tids={t["technology_id"] for t in tech}
assert len(eids)==len(orgs)==335 and len(tids)==len(tech)==54
for filename,key in [("registry_global_organizations.csv","entity_id"),("registry_global_claims.csv","claim_id"),("registry_global_sources.csv","source_id"),("registry_technology_products_tools.csv","technology_id"),("registry_neurotechnology_global.csv","neuro_id"),("registry_country_entity_relations.csv","relation_id"),("registry_technology_metrics.csv","metric_id")]:
    rows=tables[filename];assert len({r[key] for r in rows})==len(rows)
    old=ROOT/"Reference/tables/07_global_technology_iso249_20261006"/filename
    if old.exists():
        expected=read(old);assert rows[:len(expected)]==expected,"Historical rows changed: "+filename
    for r in rows:
        if "source_id" in r:assert r["source_id"] in sids or (r.get("origin_batch")=="FRONTIER_196" and not r["source_id"])
        if r.get("entity_id"):assert r["entity_id"] in eids
        if r.get("issuer_entity_id"):assert r["issuer_entity_id"] in eids
        if r.get("evidence_state")=="VERIFIED":
            assert next(s["access_state"] for s in sources if s["source_id"]==r["source_id"])=="READABLE_SUPPORT"
codes={c["iso_alpha2"] for c in read(ROOT/"Reference/tables/01_country_area/registry_country_area_iso3166_20261004_enhanced.csv")}
coverage=tables["registry_country_technology_coverage.csv"];assert len(coverage)==249 and {c["iso_alpha2"] for c in coverage}==codes
assert len(metrics)==6 and all(m["technology_id"] in tids and m["participant_count"]=="1" for m in metrics)
assert all(n["N0_N7_level"]=="UNKNOWN" and n["information_bandwidth_bits_per_second"]=="" for n in neuro)
inc=next(m for m in metrics if m["unit"]=="ms");assert inc["metric_name"]=="NEURAL_DECODING_INCREMENT" and inc["value"]=="80"
assert all(c["country_frontier_capability_state"]=="UNKNOWN" for c in coverage)
assert len({o["display_name"].casefold() for o in orgs})==len(orgs)
for c in coverage:
    matched=[o for o in orgs if c["iso_alpha2"] in o["country_candidate_iso_alpha2"].replace(",",";").split(";")]
    assert int(c["editorial_entity_candidate_count"])==len(matched)
checks=["335 unique entity IDs","54 unique technology IDs","249 ISO foreign keys and candidate counts","old batch rows retained","VERIFIED source references","six study-specific metrics with units and sample","no invented country rank or information bandwidth"]
volatile_changes=[]
if not a.preview:
    m=json.loads((HERE/"delivery_manifest.json").read_text(encoding="utf-8"))
    for p,d in m["new_output_sha256"].items():assert sha(ROOT/p)==d
    for p,r in m["append_prefixes"].items():assert hashlib.sha256((ROOT/p).read_bytes()[:r["bytes"]]).hexdigest()==r["sha256"]
    baseline=read(ROOT/m["baseline_file"]);changed=[]
    for r in baseline:
        p=ROOT/r["path"]
        volatile=r["tracked"]=="False" and r["path"].startswith(".Rproj.user/")
        if not p.exists():
            if volatile:
                volatile_changes.append({"path":r["path"],"state":"REMOVED_DURING_SESSION_CAUSE_UNKNOWN"})
                continue
            raise AssertionError("Pre-existing file removed: "+r["path"])
        if sha(p)!=r["sha256"] and r["path"] not in m["append_prefixes"]:
            if volatile:volatile_changes.append({"path":r["path"],"state":"CHANGED_DURING_SESSION_CAUSE_UNKNOWN"})
            else:changed.append(r["path"])
    assert not changed,changed
    html=ROOT/"Reference/Global_Technology_ISO249_Registry_B02.html";assert html.exists()
    text=html.read_text(encoding="utf-8");assert all(s in text for s in ("GBO0036","GBT0010","62","23.8","80"))
    checks+=["new HTML rendered","pre-existing documents and data preserved except two append-only sources; untracked Rproj runtime changes separately recorded"]
result={"state":"PASS","checks":checks,"counts":{"organizations":335,"technologies":54,"neuro_projects":16,"research_metrics":6},"untracked_runtime_changes":volatile_changes,"runtime_note":"These Rproj changes were observed during the session; no restoration or attribution is attempted."}
(HERE/("preview_validation.json" if a.preview else "delivery_validation.json")).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result))

