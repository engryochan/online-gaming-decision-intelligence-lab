from pathlib import Path
import subprocess,json,hashlib,shutil
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/40_global_directory_followup_b15_20261008';T.mkdir(parents=True,exist_ok=True)
b={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'status':subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),'protected':{}}
for p in ['Reference/Aerospace_Ecosystem_Report.qmd','Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']:b['protected'][p]=hashlib.sha256((R/p).read_bytes()).hexdigest()
(O/'baseline.json').write_text(json.dumps(b,indent=2)+'\n',encoding='utf-8')
for n in ['registry_download_links.csv','registry_pagination_links.csv']:shutil.copyfile(R/'Reference/tables/39_global_directory_content_b14_20261008'/n,T/n)
s=(O.parent/'global_directory_followup_b13/paginate.py').read_text(encoding='utf-8').replace("T=R/'Reference/tables/38_global_directory_followup_b13_20261008'","T=R/'Reference/tables/40_global_directory_followup_b15_20261008'").replace('35_global_directory_content_b10_20261008/registry_pagination_link_observations.csv','38_global_directory_followup_b13_20261008/registry_pagination_link_observations.csv')
s=s.replace("'37_global_directory_content_b12_20261008']","'37_global_directory_content_b12_20261008','38_global_directory_followup_b13_20261008','39_global_directory_content_b14_20261008']").replace('B13 explicit','B15 explicit')
(O/'paginate.py').write_text(s,encoding='utf-8')
s=(O.parent/'global_directory_followup_b13/files.py').read_text(encoding='utf-8').replace('38_global_directory_followup_b13','40_global_directory_followup_b15')
s=s.replace("'35_global_directory_content_b10_20261008']","'35_global_directory_content_b10_20261008','38_global_directory_followup_b13_20261008']")
(O/'files.py').write_text(s,encoding='utf-8')
