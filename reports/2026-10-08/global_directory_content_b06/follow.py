from pathlib import Path
import sys,threading,json,csv
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/31_global_directory_content_b06_20261008'
sys.path.insert(0,str(O.parent/'global_directory_content_b05'))
import intake
intake.O=O;intake.T=T;intake.D=O/'raw'
intake.locks={}
source=(O.parent/'global_directory_content_b05/paginate.py').read_text(encoding='utf-8')
source=source.replace('registry_directory_observed_pagination.csv','registry_pagination_links.csv').replace('pagination_progress.jsonl','pagination_progress_v2.jsonl')
source=source.replace("if len(results)+len(batch)>500:\n            gaps.extend(dict(**item,reason='BATCH_PAGE_LIMIT_REVIEW_PENDING') for item in batch);break", "if len(results)+len(batch)>100:\n            remaining=max(0,100-len(results))\n            gaps.extend(dict(**item,reason='BATCH_PAGE_LIMIT_REVIEW_PENDING') for item in batch[remaining:])\n            batch=batch[:remaining]\n            if not batch:break")
exec(compile(source,str(O/'follow.py'),'exec'))
