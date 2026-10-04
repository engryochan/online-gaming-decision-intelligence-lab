"""Fetch only allowlisted public registry/API responses, with raw provenance."""
from pathlib import Path
import concurrent.futures,hashlib,json,urllib.parse,urllib.request
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
INBOX=HERE/'inbox';INBOX.mkdir(exist_ok=True)
REQUESTS=[]
def add(key,kind,base,params):REQUESTS.append(dict(key=key,kind=kind,url=base+'?'+urllib.parse.urlencode(params)))
for i,q in enumerate(['Chinese Academy of Sciences','Tsinghua University','Harbin Institute of Technology','National Aeronautics and Space Administration','European Space Agency','Japan Aerospace Exploration Agency','Indian Space Research Organisation','Centre National de la Recherche Scientifique']):
 add('ror_'+str(i),'ROR','https://api.ror.org/v2/organizations',{'query':q})
for country in ('CN','US','DE','JP','IN'):
 add('lei_'+country,'LEI','https://api.gleif.org/api/v1/lei-records',{'page[size]':20,'filter[entity.legalAddress.country]':country})
for obj in ('1','2','433','101955','162173'):
 add('sbdb_'+obj,'SBDB','https://ssd-api.jpl.nasa.gov/sbdb.api',{'sstr':obj,'phys-par':1})
add('exoplanets','EXOPLANET','https://exoplanetarchive.ipac.caltech.edu/TAP/sync',{'query':'select top 20 pl_name,hostname,discoverymethod,disc_year from pscomppars order by pl_name','format':'json'})
for obj in ('399','499','301'):
 add('horizons_'+obj,'HORIZONS','https://ssd.jpl.nasa.gov/api/horizons.api',{'format':'json','COMMAND':"'"+obj+"'",'EPHEM_TYPE':"'VECTORS'",'CENTER':"'500@10'",'START_TIME':"'2026-10-04'",'STOP_TIME':"'2026-10-05'",'STEP_SIZE':"'1 d'",'OUT_UNITS':"'AU-D'",'REF_PLANE':"'ECLIPTIC'",'REF_SYSTEM':"'ICRF'",'VEC_TABLE':"'2'",'CSV_FORMAT':"'YES'"})
def fetch(r):
 meta=dict(r,retrieved_at=datetime.now(timezone.utc).isoformat(),status='FAILED')
 try:
  req=urllib.request.Request(r['url'],headers={'User-Agent':'DGEF-public-research/1.0','Accept':'application/json'})
  with urllib.request.urlopen(req,timeout=40) as stream:
   data=stream.read(8*1024*1024+1);meta['http_status']=stream.status
  if len(data)>8*1024*1024:raise ValueError('Response size limit exceeded')
  parsed=json.loads(data)
  if isinstance(parsed,dict) and ('errors' in parsed or 'error' in parsed):raise ValueError('API error:'+str(parsed.get('errors',parsed.get('error')))[:200])
  digest=hashlib.sha256(data).hexdigest();filename=r['key']+'_'+digest[:12]+'.json'
  (INBOX/filename).write_bytes(data);meta.update(status='FETCHED',sha256=digest,bytes=len(data),file=filename)
 except Exception as e:meta['error']=str(e)[:350]
 return meta
if __name__=='__main__':
 # NASA API policy requests one call at a time; whole batch is serial for reproducibility.
 rows=[]
 for r in REQUESTS:
  result=fetch(r);rows.append(result);print(json.dumps({k:result[k] for k in ('key','status')},ensure_ascii=True),flush=True)
 (INBOX/'manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'success':sum(r['status']=='FETCHED' for r in rows),'failed':sum(r['status']=='FAILED' for r in rows)}),flush=True)
