import intake,re,json,zipfile,io,hashlib
O,T,R=intake.O,intake.T,intake.R
source=(R/'reports/2026-10-07/git_publish_and_html_recovery/audit.py').read_text(encoding='utf-8')
# Reuse the project scanner's patterns without running its workspace mutation.
namespace={'re':re}
exec(source[source.index('patterns='):source.index('for name in paths:')],namespace)
findings=[];scanned=0
def scan(data,label):
    global scanned
    scanned+=1
    decoded=re.sub(rb'\\x([0-9a-fA-F]{2})',lambda m:bytes([int(m[1],16)]),data)
    decoded=re.sub(rb'\\u00([0-9a-fA-F]{2})',lambda m:bytes([int(m[1],16)]),decoded)
    hits=set()
    for kind,pattern in namespace['patterns']:
        for match in pattern.finditer(decoded):
            value=match[1] if kind=='CREDENTIAL_LITERAL' else match[0]
            low=value.decode('utf-8','ignore').lower().strip()
            if kind=='CREDENTIAL_LITERAL' and (low in namespace['placeholders'] or low.startswith(('your_','your-','${','{{','<','process.env','os.environ')) or len(low)>256):continue
            hits.add(kind)
    if hits:findings.append(dict(path=label,categories=sorted(hits),sha256=hashlib.sha256(data).hexdigest(),review='REQUIRED_NO_VALUES_PRINTED'))
    if zipfile.is_zipfile(io.BytesIO(data)):
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for info in z.infolist():
                if not info.is_dir() and info.file_size<=50000000:scan(z.read(info),label+'::'+info.filename)
for root in [O,T]:
    for path in root.rglob('*'):
        if path.is_file() and '__pycache__' not in path.parts and path.name!='credential_scan.json':scan(path.read_bytes(),path.relative_to(R).as_posix())
for path in [R/'Reference/Global_Directory_Content_Expansion_B05_20261008.qmd',R/'Reference/Global_Directory_Content_Expansion_B05_20261008.html']:
    if path.exists():scan(path.read_bytes(),path.relative_to(R).as_posix())
out=dict(objects_scanned_including_archive_members=scanned,candidates=findings,values_disclosed=False)
(O/'credential_scan.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out))
