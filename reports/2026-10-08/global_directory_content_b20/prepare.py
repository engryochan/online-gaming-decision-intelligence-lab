from pathlib import Path
import subprocess,json,hashlib
O=Path(__file__).resolve().parent;R=O.parents[2]
assert not (O/'baseline.json').exists(),'Preserve existing baseline; do not regenerate completed batch'
b={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'status':subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),'protected':{}}
for p in ['Reference/Aerospace_Ecosystem_Report.qmd','Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']:b['protected'][p]=hashlib.sha256((R/p).read_bytes()).hexdigest()
(O/'baseline.json').write_text(json.dumps(b,indent=2)+'\n',encoding='utf-8')
for name in ['collect.py','ledger.py','deliver.py','validate.py','publish_check.py']:
    s=(O.parent/'global_directory_content_b18'/name).read_text(encoding='utf-8').replace('43_global_directory_content_b18','45_global_directory_content_b20').replace('global_directory_content_b18','global_directory_content_b20').replace('B18','B20')
    if name=='collect.py':
        s=s.replace('from urllib.parse import urlparse','from urllib.parse import urlparse,urldefrag')
        s=s.replace('coverage=collections.Counter',"previous+=read(R/'Reference/tables/43_global_directory_content_b18_20261008/directory_fetch_manifest.csv')+read(R/'Reference/tables/44_global_directory_followup_b19_20261008/pagination_fetch_manifest.csv')\ncoverage=collections.Counter")
        s=s.replace("done={r['url'] for r in previous}","done={urldefrag(r['url'])[0] for r in previous}").replace('if url in done','if urldefrag(url)[0] in done')
    if name=='ledger.py':s=s.replace("'45_global_directory_content_b20_20261008']","'43_global_directory_content_b18_20261008','44_global_directory_followup_b19_20261008','45_global_directory_content_b20_20261008']")
    if name=='deliver.py':s=s.replace('B16、B17 已嘗試','B16、B17、B18、B19 已嘗試')
    assert not (O/name).exists(),'Preserve existing scripts'
    (O/name).write_text(s,encoding='utf-8')
