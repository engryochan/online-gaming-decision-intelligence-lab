"""Fetch only allowlisted public registry/API responses, with raw provenance."""
from pathlib import Path
import hashlib,json,ssl,subprocess,urllib.parse,urllib.request
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
for key,url in [('chang_e_5','https://www.cnsa.gov.cn/n6758823/n6758844/n6760243/n6760249/c6810583/content.html'),('artemis','https://www.nasa.gov/humans-in-space/artemis/'),('kennedy','https://www.nasa.gov/kennedy/'),('jpl','https://www.nasa.gov/jpl/')]:
 REQUESTS.append(dict(key=key,kind='OFFICIAL_WEB',url=url))
def fetch(r):
 meta=dict(r,retrieved_at=datetime.now(timezone.utc).isoformat(),status='FAILED')
 try:
  req=urllib.request.Request(r['url'],headers={'User-Agent':'DGEF-public-research/1.0','Accept':'application/json'})
  try:
   with urllib.request.urlopen(req,timeout=40) as stream:
    data=stream.read(8*1024*1024+1);meta['http_status']=stream.status
   meta['tls_backend']='Python_default_verified'
  except urllib.error.URLError as error:
   if not isinstance(error.reason,ssl.SSLCertVerificationError):raise
   # Schannel uses the existing Windows trust store; no insecure flag or trust modification.
   run=subprocess.run(['curl.exe','--fail','--silent','--show-error','--max-time','40',r['url']],capture_output=True,check=True)
   data=run.stdout;meta.update(http_status=200,tls_backend='Windows_Schannel_default_verified')
  if len(data)>8*1024*1024:raise ValueError('Response size limit exceeded')
  if r['kind']!='OFFICIAL_WEB':
   parsed=json.loads(data)
   if isinstance(parsed,dict) and ('errors' in parsed or 'error' in parsed):raise ValueError('API error:'+str(parsed.get('errors',parsed.get('error')))[:200])
  digest=hashlib.sha256(data).hexdigest();filename=r['key']+'_'+digest[:12]+('.html' if r['kind']=='OFFICIAL_WEB' else '.json')
  (INBOX/filename).write_bytes(data);meta.update(status='FETCHED',sha256=digest,bytes=len(data),file=filename)
 except Exception as e:meta['error']=str(e)[:350]
 return meta
if __name__=='__main__':
 # NASA API policy requests one call at a time; whole batch is serial for reproducibility.
 rows=[]
 previous={r['key']:r for r in json.loads((INBOX/'manifest.json').read_text(encoding='utf-8'))} if (INBOX/'manifest.json').exists() else {}
 for r in REQUESTS:
  old=previous.get(r['key']);result=old if old and old['status']=='FETCHED' else fetch(r)
  rows.append(result);print(json.dumps({k:result[k] for k in ('key','status')},ensure_ascii=True),flush=True)
 (INBOX/'manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'success':sum(r['status']=='FETCHED' for r in rows),'failed':sum(r['status']=='FAILED' for r in rows)}),flush=True)
