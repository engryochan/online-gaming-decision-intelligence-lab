from pathlib import Path
import subprocess,json,hashlib
O=Path(__file__).resolve().parent;R=O.parents[2]
b={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'status':subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),'protected':{}}
for p in ['Reference/Aerospace_Ecosystem_Report.qmd','Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']:b['protected'][p]=hashlib.sha256((R/p).read_bytes()).hexdigest()
(O/'baseline.json').write_text(json.dumps(b,indent=2)+'\n',encoding='utf-8')
s=(O.parent/'global_directory_content_b12/collect.py').read_text(encoding='utf-8').replace('37_global_directory_content_b12','39_global_directory_content_b14').replace('B12 pending','B14 pending')
needle="coverage=collections.Counter(urlparse(r['url']).hostname for r in previous)"
extra="previous+=read(R/'Reference/tables/37_global_directory_content_b12_20261008/directory_fetch_manifest.csv')+read(R/'Reference/tables/37_global_directory_content_b12_20261008/pagination_fetch_manifest.csv')+read(R/'Reference/tables/38_global_directory_followup_b13_20261008/pagination_fetch_manifest.csv')\n"
s=s.replace(needle,extra+needle)
(O/'collect.py').write_text(s,encoding='utf-8')
s=(O.parent/'global_directory_content_b12/ledger.py').read_text(encoding='utf-8').replace("T=R/'Reference/tables/37_global_directory_content_b12_20261008'","T=R/'Reference/tables/39_global_directory_content_b14_20261008'").replace("'37_global_directory_content_b12_20261008']","'37_global_directory_content_b12_20261008','38_global_directory_followup_b13_20261008','39_global_directory_content_b14_20261008']")
(O/'ledger.py').write_text(s,encoding='utf-8')
for name in ['deliver.py','validate.py','publish_check.py']:
    s=(O.parent/'global_directory_content_b12'/name).read_text(encoding='utf-8').replace('37_global_directory_content_b12','39_global_directory_content_b14').replace('global_directory_content_b12','global_directory_content_b14').replace('B12','B14')
    if name=='deliver.py':s=s.replace('B05、B06、B07、B10 已嘗試','B05、B06、B07、B10、B12、B13 已嘗試')
    if name=='publish_check.py':s=s.replace('採集程序曾輸出 HTML 編碼轉換警告，未逐頁定位；','')
    (O/name).write_text(s,encoding='utf-8')
