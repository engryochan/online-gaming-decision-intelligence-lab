from pathlib import Path
import csv,json,hashlib,subprocess,urllib.request,urllib.parse,datetime,sqlite3,re,struct,zlib
from html.parser import HTMLParser
from pypdf import PdfReader
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/76_ais_semantics_b53_20261011'
MAIN='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    assert rs
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
assert not (O/'baseline.json').exists(),'Never refresh baseline'
T.mkdir();(O/'raw').mkdir()
paths=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0');original=(R/MAIN).read_bytes()
protected={p:sha((R/p).read_bytes()) for p in paths if p and Path(p).suffix in ('.md','.qmd') and (R/p).is_file()}
base=dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),starting_status=subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),protected=protected,authorized_append=dict(path=MAIN,prefix_bytes=len(original),prefix_sha256=sha(original)))
(O/'baseline.json').write_text(json.dumps(base,indent=2),encoding='utf-8')
receipts=[]
def fetch(sid,url,limit,range_header=None):
    rec=dict(source_id=sid,url=url,final_url='',fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status='',content_range='',declared_content_length='',source_file='',sha256='',saved_bytes='',partial_response=bool(range_header),error='',evidence_scope='NEW_FETCH')
    b=b''
    try:
        headers={'User-Agent':'PublicResearchRegistry/1.0'}
        if range_header:headers['Range']=range_header
        with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=30) as response:
            b=response.read(limit+1);rec.update(http_status=response.status,final_url=response.url,content_range=response.headers.get('Content-Range',''),declared_content_length=response.headers.get('Content-Length',''))
        if range_header:b=b[:limit]
        else:assert len(b)<=limit
        p=O/'raw'/(sid+('.part' if range_header else '.pdf' if b.startswith(b'%PDF') else '.response'));p.write_bytes(b);rec.update(source_file=p.relative_to(R).as_posix(),sha256=sha(b),saved_bytes=len(b))
    except Exception as e:rec.update(error=type(e).__name__,http_status=getattr(e,'code',rec['http_status']));b=b''
    receipts.append(rec);return rec,b

for sid,url in [('B53DICTIONARY','https://coast.noaa.gov/data/marinecadastre/ais/data-dictionary.pdf'),('B53FAQ','https://coast.noaa.gov/data/marinecadastre/ais/faq.pdf'),('B53SUMMARY','https://coast.noaa.gov/data/marinecadastre/ais/point-data-summary.pdf'),('B53INPORT','https://www.fisheries.noaa.gov/inport/item/62733'),('B53PUBLICLAYER','https://coast.noaa.gov/arcgis/rest/services/MarineCadastre/AISVesselTransitCounts2019/MapServer/0?f=pjson')]:
    rec,b=fetch(sid,url,6000000)
write('registry_source_receipts.csv',receipts)
import pdfplumber
for sid in ['B53DICTIONARY','B53FAQ','B53SUMMARY']:
    rec=next(r for r in receipts if r['source_id']==sid)
    assert not rec['error']
    with pdfplumber.open(R/rec['source_file']) as pdf:
        pages=[dict(page=i+1,text=p.extract_text(),tables=p.extract_tables()) for i,p in enumerate(pdf.pages)]
        (O/(sid+'_extraction.json')).write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([dict(source_id=r['source_id'],http_status=r['http_status'],error=r['error']) for r in receipts]))
