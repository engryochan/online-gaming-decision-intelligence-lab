from pathlib import Path
import subprocess,json,re,hashlib
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent;O.mkdir(parents=True,exist_ok=True)
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
paths=[x.decode('utf-8') for x in git('ls-files','-z','--cached','--others','--exclude-standard').split(b'\0') if x];paths=sorted(set(paths));findings=[];large=[];orphans=[]
research_csv=[x.decode('utf-8') for x in git('ls-files','-z','--others','--ignored','--exclude-standard','reports').split(b'\0') if x and x.decode('utf-8').endswith('.csv')]
paths=sorted(set(paths+research_csv))
patterns=[('PRIVATE_KEY',re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----')),('TOKEN_FORMAT',re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}|AKIA[A-Z0-9]{16}|sk-proj-[A-Za-z0-9_-]{30,}|xox[baprs]-[A-Za-z0-9-]{20,})')),('CREDENTIAL_LITERAL',re.compile(rb'''(?im)["']?(?:password|passwd|pwd|api[_-]?key|client[_-]?secret|access[_-]?token|secret[_-]?key)["']?\s*[:=]\s*["']([^"'\r\n]{4,})["']'''))]
anchors={'PRIVATE_KEY':[b'-----begin'],'TOKEN_FORMAT':[b'ghp_',b'gho_',b'ghu_',b'ghs_',b'ghr_',b'github_pat_',b'akia',b'sk-proj-',b'xox'],'CREDENTIAL_LITERAL':[b'password',b'passwd',b'pwd',b'api_key',b'api-key',b'apikey',b'client_secret',b'client-secret',b'access_token',b'access-token',b'secret_key',b'secret-key']}
patterns.append(('MAPBOX_SECRET_TOKEN',re.compile(rb'sk\.eyJ[A-Za-z0-9_.-]+')))
anchors['MAPBOX_SECRET_TOKEN']=[b'sk.eyj']
placeholders={'password','changeme','your_password','your_api_key','your-api-key','your-password','example','placeholder','<password>','<api_key>','none','null','unknown','unresolved'}
for name in paths:
 p=R/name
 if not p.is_file() or p.is_symlink():continue
 n=p.stat().st_size
 if n>95*1024*1024:large.append(dict(path=name,bytes=n))
 if p.suffix.lower()=='.html' and not p.with_suffix('.qmd').exists():orphans.append(dict(path=name,bytes=n,classifier='RAW_OR_ARCHIVE' if '/raw/' in name or '/originals/' in name or '/preview/' in name or '_files/' in name else 'DELIVERABLE_CANDIDATE'))
 # Chunk scanning includes binary files; overlapping windows avoid boundary misses.
 hits=set()
 with p.open('rb') as f:
  tail=b''
  while True:
   chunk=f.read(4*1024*1024)
   if not chunk:break
   data=tail+chunk;lower=data.lower()
   for kind,pat in patterns:
    windows=[]
    for anchor in anchors[kind]:
     start=0
     while True:
      at=lower.find(anchor,start)
      if at<0:break
      windows.append(data[max(0,at-2):at+512]);start=at+len(anchor)
    for match in (match for window in windows for match in pat.finditer(window)):
     value=match.group(1) if kind=='CREDENTIAL_LITERAL' else match.group(0)
     low=value.decode('utf-8','ignore').lower().strip()
     if kind=='CREDENTIAL_LITERAL' and (low in placeholders or low.startswith(('your_','your-','${','{{','<','process.env','os.environ')) or len(low)>256):continue
     hits.add(kind)
   tail=data[-4096:]
 if hits:findings.append(dict(path=name,categories=sorted(hits),status='REVIEW_REQUIRED_NO_VALUE_DISCLOSED'))
out=dict(files_scanned=len(paths),candidate_secret_files=findings,large_files=large,html_without_same_stem_qmd=orphans)
(O/'workspace_audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(files=len(paths),secret_candidates=len(findings),large_files=large,html_orphans=len(orphans)),ensure_ascii=True))
