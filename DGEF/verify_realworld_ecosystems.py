"""Verify evidence keys, temporal semantics and additive document integration."""
from pathlib import Path
import csv,hashlib,json,re,zipfile
from update_realworld_ecosystems import ROOT,OUT,TABLES
receipt=json.loads((OUT/'build_receipt.json').read_text(encoding='utf-8'))
def read(name):
    with (TABLES/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
sources=read('sources.csv');capabilities=read('provider_capabilities.csv');obs=read('realworld_observations.csv');relations=read('public_relationships.csv');contracts=read('industry_chain_contracts.csv')
keys={r['source_id'] for r in sources};assert len(keys)==len(sources)==21
for table in [capabilities,obs,relations]:
    for r in table:assert r['source_id'] in keys,r
assert len(capabilities)==18 and len(obs)==8 and len(relations)==2 and len(contracts)==9
assert all(r['world_scope']=='REAL_WORLD' for r in capabilities)
assert all(r['performance_state']=='NOT_INDEPENDENTLY_TESTED' for r in capabilities)
assert all(r['supremacy_verified']=='NO' and r['raw_http_snapshot']=='NOT_ARCHIVED' for r in sources)
for r in obs:
    assert r['observation_period']=='2025' and r['published_on']=='2026-04-27' and r['checked_on']=='2026-10-04'
    assert r['price_basis']=='CONSTANT_2024_PRICES' if 'growth' in r['metric'] else True
for r in relations:assert r['contract_value']==r['supplier_tier']==''
for name,expected in receipt['table_sha256'].items():assert hashlib.sha256((TABLES/name).read_bytes()).hexdigest()==expected
documents=[]
with zipfile.ZipFile(OUT/'before_documents.zip') as z:
    for n in receipt['targets']:
        p=ROOT/n;old=z.read(n);current=p.read_bytes();assert current.startswith(old)
        addition=current[len(old):].decode('utf-8')
        for topic in ['redteam／','critic／','killcritic／','blindspot／','cheatsheet／','blueprint／','actionplan／']:assert '### '+topic in addition
        for url in re.findall(r'\]\(([^)]+)\)',addition):
            if not url.startswith('https://'):assert (p.parent/url).is_file(),url
        documents.append({'path':n,'prefix_preserved':True,'seven_topics':True,'new_local_links':'PASS'})
for n in ['md_parse.json','qmd_parse.json']:assert json.loads((OUT/n).read_text(encoding='utf-8'))['blocks']
result={'provider_records':18,'sources':21,'observations':8,'relations':2,'chain_design_rows':9,'source_keys':'PASS','time_price_basis_and_unknowns':'PASS','table_sha256':'PASS','documents':documents,'pandoc_full_parse':'PASS','quarto_execution':'NOT_RUN','existing_database':'UNCHANGED_BY_BUILD'}
(OUT/'acceptance.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
for n in ['md_parse.json','qmd_parse.json']:(OUT/n).unlink()
print(json.dumps(result,ensure_ascii=True))
