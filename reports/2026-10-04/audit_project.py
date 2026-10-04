from pathlib import Path
import hashlib, json, csv, re, ast
from html.parser import HTMLParser
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
class Visible(HTMLParser):
    def __init__(self): super().__init__(); self.skip=0; self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'): self.skip+=1
    def handle_endtag(self,tag):
        if tag in ('script','style'): self.skip=max(0,self.skip-1)
        if tag in ('p','div','tr','h1','h2','h3','li'): self.parts.append('\n')
    def handle_data(self,data):
        if not self.skip: self.parts.append(data)
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.relative_to(ROOT).parts and 'reports' not in p.relative_to(ROOT).parts)
inventory=[]; texts={}; hashes=defaultdict(list); links=[]; outlines=[]; tables=[]
for p in files:
    rel=p.relative_to(ROOT).as_posix()
    try: b=p.read_bytes()
    except OSError as e:
        inventory.append(dict(path=rel,bytes=p.stat().st_size,sha256='',lines=0,review_method='READ FAILED: '+str(e)))
        continue
    digest=hashlib.sha256(b).hexdigest(); hashes[digest].append(rel)
    status=''; content=''
    if p.suffix=='.pdf':
        try:
            from pypdf import PdfReader
            doc=PdfReader(p); content='\n'.join(page.extract_text() or '' for page in doc.pages); status=f'PDF extracted: {len(doc.pages)} pages (text only; visual layout not checked)'
        except Exception as e: status='PDF extraction failed: '+str(e)
    elif p.suffix=='.woff': status='binary font: no prose review'
    else:
        try: content=b.decode('utf-8-sig'); status='UTF-8 decoded'
        except UnicodeDecodeError:
            try: content=b.decode('gb18030'); status='GB18030 decoded'
            except UnicodeDecodeError: status='unreadable binary'
        if p.suffix=='.html' and content:
            parser=Visible(); parser.feed(content); content=''.join(parser.parts); status+='; HTML visible text extracted (no browser execution)'
        if p.suffix=='.py':
            try: ast.parse(content); status+='; Python syntax PASS'
            except SyntaxError as e: status+='; Python syntax FAIL: '+str(e)
    inventory.append(dict(path=rel,bytes=len(b),sha256=digest,lines=len(content.splitlines()),review_method=status))
    if content:
        texts[rel]=content
        for i,line in enumerate(content.splitlines(),1):
            if re.match(r'^#{1,4}\s',line): outlines.append(f'{rel}:{i}: {line[:200]}')
            if line.lstrip().startswith('|'): tables.append((rel,i,line))
            for url in re.findall(r'https?://[^\s<>\]\)\"]+',line): links.append(dict(path=rel,line=i,url=url.rstrip('.,;。；')))
with (OUT/'tables/04_file_audit/file_inventory.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=inventory[0]); w.writeheader(); w.writerows(inventory)
(OUT/'extracted_text.json').write_text(json.dumps(texts,ensure_ascii=False),encoding='utf-8')
(OUT/'outline.txt').write_text('\n'.join(outlines),encoding='utf-8')
with (OUT/'tables/03_sources_evidence/source_urls.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['path','line','url']);w.writeheader();w.writerows(links)
unique={}
for p,i,line in tables:
    normalized=re.sub(r'\s+',' ',line).strip()
    if normalized not in unique: unique[normalized]=(p,i)
(OUT/'unique_tables.txt').write_text('\n'.join(f'{p}:{i}: {line}' for line,(p,i) in unique.items()),encoding='utf-8')
duplicates=[v for v in hashes.values() if len(v)>1]
(OUT/'duplicate_files.json').write_text(json.dumps(duplicates,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(files=len(files),bytes=sum(x['bytes'] for x in inventory),extracted_files=len(texts),extracted_lines=sum(x['lines'] for x in inventory),duplicate_groups=len(duplicates),unique_table_rows=len(unique),failed=[x for x in inventory if 'FAILED' in x['review_method']],python=[x for x in inventory if x['path'].endswith('.py')],pdf=[x for x in inventory if x['path'].endswith('.pdf')]),ensure_ascii=True,indent=2))
