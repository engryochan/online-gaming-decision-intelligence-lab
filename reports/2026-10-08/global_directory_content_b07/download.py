from pathlib import Path
import sys,csv,json,hashlib,io,zipfile,urllib.request
from concurrent.futures import ThreadPoolExecutor
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/32_global_directory_content_b07_20261008'
sys.path.insert(0,str(O.parent/'global_directory_content_b05'))
import intake
intake.O=O;intake.T=T
def read(n):return list(csv.DictReader((T/n).open(encoding='utf-8-sig')))
source=(O.parent/'global_directory_content_b05/complete.py').read_text(encoding='utf-8')
source=source[source.index('urls='):source.index('summary=dict(cma_cards=')]
source=source.replace("registry_directory_observed_download_links.csv","registry_download_links.csv")
exec(compile(source,str(O/'download.py'),'exec'))
csvrows=[]
for result in results:
    if result.get('file') and result['url'].lower().endswith('.csv') and not result.get('truncated'):
        data=(R/result['file']).read_bytes()
        try:text=data.decode('utf-8-sig');encoding='UTF8'
        except UnicodeDecodeError:text=data.decode('latin1');encoding='LATIN1_REVERSIBLE_SOURCE_ENCODING_UNCONFIRMED'
        for number,cells in enumerate(csv.reader(io.StringIO(text),delimiter=(';' if text.splitlines()[0].count(';')>=text.splitlines()[0].count(',') else ',')),1):
            csvrows.append(dict(source_url=result['url'],row=number,encoding=encoding,cells_json=json.dumps(cells,ensure_ascii=False),role='SOURCE_FILE_ROW_SCHEMA_AND_ENTITY_SCOPE_PENDING'))
intake.write('registry_download_csv_rows.csv',csvrows)
(O/'download_acceptance.json').write_text(json.dumps(dict(unique_links=len(urls),saved=sum('file' in r for r in results),archive_members=len(members),workbook_rows=len(rows),csv_rows=len(csvrows)),indent=2)+'\n',encoding='utf-8')
print((O/'download_acceptance.json').read_text())
