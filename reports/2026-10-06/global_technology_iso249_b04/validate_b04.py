from pathlib import Path
import csv,json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
REL=Path('Reference/tables/10_global_technology_iso249_20261006_b04')
OLD=ROOT/'Reference/tables/09_global_technology_iso249_20261006_b03'
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');a=ap.parse_args()
base=HERE/'preview' if a.preview else ROOT
tables={p.name:read(p) for p in (base/REL).glob('*.csv')}
orgs=tables['registry_global_organizations.csv'];tech=tables['registry_technology_products_tools.csv'];metrics=tables['registry_technology_metrics.csv']
eids={r['entity_id'] for r in orgs};tids={r['technology_id'] for r in tech};sources={r['source_id']:r for r in tables['registry_global_sources.csv']}
assert len(orgs)==len(eids)==371 and len(tech)==len(tids)==71 and len(metrics)==17
keys=['event_id','metric_id','relation_id','neuro_id','claim_id','technology_id','entity_id','source_id']
for fn,rows in tables.items():
    if (OLD/fn).exists():
        previous=read(OLD/fn);assert rows[:len(previous)]==previous,'Historical rows changed: '+fn
    identity=next((k for k in keys if k in rows[0]),'iso_alpha2')
    assert len({r[identity] for r in rows})==len(rows),fn
    for r in rows:
        if r.get('entity_id'):assert r['entity_id'] in eids
        if r.get('issuer_entity_id'):assert r['issuer_entity_id'] in eids
        if r.get('technology_id'):assert r['technology_id'] in tids
        if 'source_id' in r:assert r['source_id'] in sources or (r.get('origin_batch')=='FRONTIER_196' and not r['source_id'])
        if r.get('evidence_state')=='VERIFIED':assert sources[r['source_id']]['access_state']=='READABLE_SUPPORT'
mother=read(ROOT/'Reference/tables/01_country_area/registry_country_area_iso3166_20261004_enhanced.csv')
coverage=tables['registry_country_technology_coverage.csv'];assert len(coverage)==249 and {r['iso_alpha2'] for r in coverage}=={r['iso_alpha2'] for r in mother}
assert sum(int(r['editorial_entity_candidate_count'])>0 for r in coverage)==103
new=[r for r in tech if r['technology_id'].startswith('GDT')];assert len(new)==12 and sum(r['evidence_state']=='VERIFIED' for r in new)==10
assert all(r['global_rank_state']=='UNKNOWN' and r['license_state']=='UNKNOWN' for r in new)
assert all(r['participant_count']=='' and r['general_population_state']=='NOT_APPLICABLE' for r in metrics if r['metric_id'].startswith('GDM'))
assert all('16 satellites' in r['conditions'] for r in metrics if r['metric_name'] in ('CONSTELLATION_REVISIT_RATE','COLLECTION_TO_DELIVERY_TIME'))
events=tables['registry_technology_lifecycle_events.csv'];assert len(events)==1 and events[0]['independent_deployment_state']=='UNKNOWN'
volatile=[]
if not a.preview:
    manifest=json.loads((HERE/'delivery_manifest.json').read_text(encoding='utf-8'))
    for p,d in manifest['new_output_sha256'].items():assert sha(ROOT/p)==d,p
    for p,r in manifest['append_prefixes'].items():assert hashlib.sha256((ROOT/p).read_bytes()[:r['bytes']]).hexdigest()==r['sha256'],p
    for r in read(ROOT/manifest['baseline_file']):
        p=ROOT/r['path'];isvolatile=r['tracked']=='False' and r['path'].startswith('.Rproj.user/')
        if not p.exists() or sha(p)!=r['sha256']:
            if isvolatile:volatile.append(r['path'])
            else:assert r['path'] in manifest['append_prefixes'],'Pre-existing file changed: '+r['path']
    html=ROOT/'Reference/Global_Technology_ISO249_Registry_B04.html'
    rendered=html.read_text(encoding='utf-8');assert all(x in rendered for x in ('GDT0012','16 satellites','0.125'))
result=dict(state='PASS',counts=dict(organizations=371,technologies=71,metrics=17,new_verified_descriptions=10,new_unknown_descriptions=2),checks=['all historical CSV rows retained','249 ISO keys and unchanged country coverage','unique IDs and source/entity/technology foreign keys','scoped VERIFIED sources','constellation conditions retained','original documents preserved with two append-only indexes'],untracked_runtime_changes=volatile)
(HERE/('preview_validation.json' if a.preview else 'delivery_validation.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
