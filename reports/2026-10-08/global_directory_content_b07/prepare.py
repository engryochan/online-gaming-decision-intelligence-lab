from pathlib import Path
import json,subprocess,hashlib
O=Path(__file__).resolve().parent;R=O.parents[2]
source=(O.parent/'global_directory_content_b06/collect.py').read_text(encoding='utf-8')
source=source.replace('31_global_directory_content_b06','32_global_directory_content_b07').replace('B06 pending URL signals','B07 pending URL signals')
source=source.replace("done={r['url'] for r in previous}","previous+=read(R/'Reference/tables/31_global_directory_content_b06_20261008/directory_fetch_manifest.csv')+read(R/'Reference/tables/31_global_directory_content_b06_20261008/pagination_fetch_manifest.csv')\ncoverage=collections.Counter(urlparse(r['url']).hostname for r in previous)\ndone={r['url'] for r in previous}")
source=source.replace('for host in sorted(hosts):','for host in sorted(hosts,key=lambda h:(coverage[h],h)):').replace('>=160','>=180').replace('[:160]','[:180]')
(O/'collect.py').write_text(source,encoding='utf-8')
baseline=dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),status=subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),protected={})
for name in ['Reference/Aerospace_Ecosystem_Report.qmd','Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']:
    baseline['protected'][name]=hashlib.sha256((R/name).read_bytes()).hexdigest()
(O/'baseline.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(head=baseline['head'],protected_files=len(baseline['protected']))))
