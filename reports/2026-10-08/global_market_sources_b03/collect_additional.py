from pathlib import Path
from urllib.request import urlopen,Request
from urllib.error import HTTPError
import csv,json,hashlib,zipfile,io
O=Path(__file__).parent;R=O.parents[2];T=R/'Reference/tables/28_global_market_sources_b03_20261008'
manifest=[];records=[]
feeds=[('JSE_ISIN_FULL','https://clientportal.jse.co.za/Reports/Downloadable-Files/Download?filepath=ISIN%2FEquities%2Fisinfull_e.zip'),
       ('SEC_TICKER_EXCHANGE','https://www.sec.gov/files/company_tickers_exchange.json')]
for label,url in feeds:
    try:
        with urlopen(Request(url,headers={'User-Agent':'ResearchSourceInventory/1.0'}),timeout=20) as response:
            b=response.read();status=response.status;final=response.url
    except HTTPError as e:b=e.read();status=e.code;final=e.url
    except Exception as e:
        manifest.append(dict(source=label,url=url,status='NETWORK_ERROR',error_type=type(e).__name__));continue
    (O/'raw'/(label+'.response')).write_bytes(b)
    result=dict(source=label,url=url,final_url=final,http_status=status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),retrieved_on='2026-10-08')
    manifest.append(result)
    if status!=200:continue
    if label=='JSE_ISIN_FULL':
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            members=[]
            for name in z.namelist():
                if name.endswith('/'):continue
                content=z.read(name);lines=content.decode('utf-8',errors='backslashreplace').splitlines()
                members.append(dict(member=name,bytes=len(content),sha256=hashlib.sha256(content).hexdigest(),physical_lines=len(lines)))
                for number,line in enumerate(lines,1):
                    records.append(dict(source=label,member=name,source_line=number,raw_record=line,
                                        semantic_status='RAW_FIXED_WIDTH_LINE_PENDING_FIELD_DICTIONARY_NOT_UNIQUE_COMPANY'))
            result['archive_members']=json.dumps(members);result['source_lines']=sum(x['physical_lines'] for x in members)
    else:
        data=json.loads(b);result['source_rows']=len(data['data']);result['fields']=json.dumps(data['fields'])
        for number,row in enumerate(data['data'],1):records.append(dict(source=label,source_line=number,raw_record=json.dumps(dict(zip(data['fields'],row))),semantic_status='SOURCE_TICKER_RECORD_NOT_ALL_COMPANIES_CERTIFIED'))
def write(name,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (T/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
write('additional_collection_manifest.csv',manifest);write('registry_additional_source_records.csv',records)
print(json.dumps(manifest),flush=True)
