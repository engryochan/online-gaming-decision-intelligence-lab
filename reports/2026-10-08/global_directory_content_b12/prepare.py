from pathlib import Path
import subprocess,json,hashlib
O=Path(__file__).resolve().parent;R=O.parents[2]
baseline={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'status':subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),'protected':{}}
for name in ['Reference/Aerospace_Ecosystem_Report.qmd','Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']:
    baseline['protected'][name]=hashlib.sha256((R/name).read_bytes()).hexdigest()
(O/'baseline.json').write_text(json.dumps(baseline,indent=2)+'\n',encoding='utf-8')
s=(O.parent/'global_directory_content_b10/collect.py').read_text(encoding='utf-8').replace('35_global_directory_content_b10','37_global_directory_content_b12').replace('B10 pending','B12 pending')
needle="coverage=collections.Counter(urlparse(r['url']).hostname for r in previous)"
s=s.replace(needle,"previous+=read(R/'Reference/tables/35_global_directory_content_b10_20261008/directory_fetch_manifest.csv')+read(R/'Reference/tables/35_global_directory_content_b10_20261008/pagination_fetch_manifest.csv')\n"+needle)
(O/'collect.py').write_text(s,encoding='utf-8')
s=(O.parent/'global_directory_content_b10/ledger.py').read_text(encoding='utf-8').replace("T=R/'Reference/tables/35_global_directory_content_b10_20261008'","T=R/'Reference/tables/37_global_directory_content_b12_20261008'")
s=s.replace("'35_global_directory_content_b10_20261008']","'35_global_directory_content_b10_20261008','37_global_directory_content_b12_20261008']")
(O/'ledger.py').write_text(s,encoding='utf-8')
