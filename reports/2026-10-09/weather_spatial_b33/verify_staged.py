from pathlib import Path
import subprocess,json,hashlib
O=Path(__file__).resolve().parent;R=O.parents[2]
names=subprocess.check_output(['git','diff','--cached','--name-only','-z']).decode().split('\0');names=[n for n in names if n]
allowed=lambda n:n=='.gitattributes' or n.startswith(('reports/2026-10-09/weather_spatial_b33/','Reference/tables/58_weather_spatial_b33_20261009/')) or n in ['Reference/Weather_Spatial_B33_20261009.qmd','Reference/Weather_Spatial_B33_20261009.html'] or n in [d+'/weather_spatial_b33_20261009.md' for d in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']]
assert names and all(allowed(n) for n in names),'Unexpected staged files'
for p,h in json.loads((O/'baseline.json').read_text(encoding='utf-8'))['protected'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
manifest=__import__('csv').DictReader((R/'Reference/tables/58_weather_spatial_b33_20261009/registry_fetch_manifest.csv').open(encoding='utf-8-sig'))
count=0
for r in manifest:
    if r['file']:
        assert r['file'] in names
        assert hashlib.sha256(subprocess.check_output(['git','show',':'+r['file']])).hexdigest()==r['sha256'];count+=1
assert not json.loads((O/'credential_scan.json').read_text())['candidates']
(O/'staged_acceptance.json').write_text(json.dumps(dict(files_checked=len(names),raw_files_byte_verified=count,protected_files_unchanged=True,user_parallel_changes_excluded=True),indent=2)+'\n',encoding='utf-8')
print('PASS: exact staging scope, protected hashes, raw staged bytes and credential scan')
