from pathlib import Path
import csv,json,collections
O=Path(__file__).parent;T=O.parents[2]/'Reference/tables/30_global_directory_content_b05_20261008'
def read(name):return list(csv.DictReader((T/name).open(encoding='utf-8-sig')))
print('downloads',json.dumps([(r['target_url'],r['label'][:90]) for r in read('registry_directory_observed_download_links.csv')],ensure_ascii=True))
print('pagination',json.dumps([(r['target_url'],r['label']) for r in read('registry_directory_observed_pagination.csv')],ensure_ascii=True))
group=collections.defaultdict(list)
for r in read('registry_directory_all_table_rows.csv'):group[(r['source_url'],r['table'])].append(r)
print('tables',json.dumps([dict(source=k[0],table=k[1],rows=len(v),headers=v[0]['headers_json'],first=v[0]['cells_json'],second=v[1]['cells_json'] if len(v)>1 else '') for k,v in group.items()],ensure_ascii=True))
