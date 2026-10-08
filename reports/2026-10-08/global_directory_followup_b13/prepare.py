from pathlib import Path
import json,subprocess,hashlib,shutil
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/38_global_directory_followup_b13_20261008';T.mkdir(parents=True,exist_ok=True)
base=R/'Reference/tables/37_global_directory_content_b12_20261008'
baseline={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'status':subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),'protected':{}}
for p in ['Reference/Aerospace_Ecosystem_Report.qmd','Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']:
    baseline['protected'][p]=hashlib.sha256((R/p).read_bytes()).hexdigest()
(O/'baseline.json').write_text(json.dumps(baseline,indent=2)+'\n',encoding='utf-8')
for name in ['registry_download_links.csv','registry_pagination_links.csv']:shutil.copyfile(base/name,T/name)
s=(O.parent/'global_directory_content_b10/paginate.py').read_text(encoding='utf-8')
s=s.replace("T=R/'Reference/tables/35_global_directory_content_b10_20261008'","T=R/'Reference/tables/38_global_directory_followup_b13_20261008'")
s=s.replace('32_global_directory_content_b07_20261008/registry_pagination_link_observations.csv','35_global_directory_content_b10_20261008/registry_pagination_link_observations.csv')
s=s.replace("'35_global_directory_content_b10_20261008']","'35_global_directory_content_b10_20261008','37_global_directory_content_b12_20261008']").replace('B10 explicit','B13 explicit').replace("intake.D=O/'raw';intake.locks={}","intake.D=O/'raw';intake.D.mkdir(exist_ok=True);intake.locks={}")
(O/'paginate.py').write_text(s,encoding='utf-8')
s=(O.parent/'global_directory_content_b10/files.py').read_text(encoding='utf-8').replace('35_global_directory_content_b10','38_global_directory_followup_b13')
s=s.replace("links=read(T/'registry_download_links.csv')","links=read(T/'registry_download_links.csv')+read(T/'registry_pagination_download_links.csv')")
s=s.replace("'32_global_directory_content_b07_20261008']","'32_global_directory_content_b07_20261008','35_global_directory_content_b10_20261008']")
s=s.replace("selected=set(other+montreal[:10]+montreal[-10:])","selected=set(byurl)")
s=s.replace("safe=':/?=&%#'","safe=':/?=&%#+'").replace("intake.D=O/'raw';intake.locks={}","intake.D=O/'raw';intake.D.mkdir(exist_ok=True);intake.locks={}")
(O/'files.py').write_text(s,encoding='utf-8')
