from pathlib import Path
from urllib.request import urlopen
import json,hashlib
O=Path(__file__).parent;D=O/'raw'; m=json.loads((O/'source_manifest.json').read_text());sha=(O/'pinned_commit.txt').read_text().strip()
for url,name in [('https://raw.githubusercontent.com/Seshat-Global-History-Databank/cliopatria/'+sha+'/LICENSE.md','LICENSE.md'),('https://correlatesofwar.org/wp-content/uploads/State-System-Membership-Codebook-V2024.pdf','cow_codebook.pdf'),('https://unstats.un.org/unsd/methodology/m49/overview/','un_m49_overview.html')]:
 with urlopen(url,timeout=90) as r:b=r.read();final=r.url;date=r.headers.get('Date')
 p=D/name;assert not p.exists();p.write_bytes(b);m.append(dict(url=url,final_url=final,file=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),server_date=date));print(name,len(b),flush=True)
 (O/'source_manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
