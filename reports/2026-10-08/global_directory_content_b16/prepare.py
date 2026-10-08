from pathlib import Path
import subprocess,json,hashlib
O=Path(__file__).resolve().parent;R=O.parents[2]
b={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'status':subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),'protected':{}}
for p in ['Reference/Aerospace_Ecosystem_Report.qmd','Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']:b['protected'][p]=hashlib.sha256((R/p).read_bytes()).hexdigest()
(O/'baseline.json').write_text(json.dumps(b,indent=2)+'\n',encoding='utf-8')
s=(O.parent/'global_directory_content_b14/collect.py').read_text(encoding='utf-8').replace('39_global_directory_content_b14','41_global_directory_content_b16').replace('B14 pending','B16 pending')
needle="coverage=collections.Counter(urlparse(r['url']).hostname for r in previous)"
s=s.replace(needle,"previous+=read(R/'Reference/tables/39_global_directory_content_b14_20261008/directory_fetch_manifest.csv')+read(R/'Reference/tables/39_global_directory_content_b14_20261008/pagination_fetch_manifest.csv')+read(R/'Reference/tables/40_global_directory_followup_b15_20261008/pagination_fetch_manifest.csv')\n"+needle)
(O/'collect.py').write_text(s,encoding='utf-8')
s=(O.parent/'global_directory_content_b14/ledger.py').read_text(encoding='utf-8').replace("T=R/'Reference/tables/39_global_directory_content_b14_20261008'","T=R/'Reference/tables/41_global_directory_content_b16_20261008'").replace("'39_global_directory_content_b14_20261008']","'39_global_directory_content_b14_20261008','40_global_directory_followup_b15_20261008','41_global_directory_content_b16_20261008']")
(O/'ledger.py').write_text(s,encoding='utf-8')
for name in ['deliver.py','validate.py','publish_check.py']:
    s=(O.parent/'global_directory_content_b14'/name).read_text(encoding='utf-8').replace('39_global_directory_content_b14','41_global_directory_content_b16').replace('global_directory_content_b14','global_directory_content_b16').replace('B14','B16')
    if name=='deliver.py':s=s.replace('B10、B12、B13 已嘗試','B10、B12、B13、B14、B15 已嘗試')
    (O/name).write_text(s,encoding='utf-8')
