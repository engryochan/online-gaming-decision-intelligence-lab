from pathlib import Path
import json,subprocess,hashlib
O=Path(__file__).resolve().parent;R=O.parents[2]
source=(O.parent/'global_directory_content_b07/collect.py').read_text(encoding='utf-8')
source=source.replace('32_global_directory_content_b07','35_global_directory_content_b10').replace('B07 pending URL signals','B10 pending path and query signals')
needle="coverage=collections.Counter(urlparse(r['url']).hostname for r in previous)"
source=source.replace(needle,"previous+=read(R/'Reference/tables/32_global_directory_content_b07_20261008/directory_fetch_manifest.csv')+read(R/'Reference/tables/32_global_directory_content_b07_20261008/pagination_fetch_manifest.csv')\n"+needle)
source=source.replace("signals=re.findall(r'issuer|equit|securit|stock|compan|instrument|participant|register|licen|broker|member|listing|directory',url,re.I)","signals=re.findall(r'issuer|equit|securit|stock|compan|instrument|participant|register|licen|broker|member|listing|directory|empresas|emittent|notiert|titres|listed|dealing|admitted',urlparse(url).path+'?'+urlparse(url).query,re.I)")
source=source.replace('score=len(signals)','score=len(signals)+(4 if any(s.lower() in [\'directory\',\'register\',\'listing\',\'listed\'] for s in signals) else 0)-(8 if any(s in urlparse(url).path.lower() for s in [\'/news/\',\'/blog/\',\'/press/\',\'/login\']) else 0)')
source=source.replace('>=180','>=220').replace('[:180]','[:220]')
(O/'collect.py').write_text(source,encoding='utf-8')
baseline=dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),status=subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),protected={})
for name in ['Reference/Aerospace_Ecosystem_Report.qmd','Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']:
    baseline['protected'][name]=hashlib.sha256((R/name).read_bytes()).hexdigest()
(O/'baseline.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(head=baseline['head'],protected_files=len(baseline['protected']))))
