from pathlib import Path
import json,hashlib,subprocess,re
O=Path(__file__).resolve().parent;R=O.parents[2];D=Path('C:/Users/PPCCpcpc/Downloads');a=json.loads((O/'audit.json').read_text(encoding='utf-8'));b=json.loads((O/'baseline.json').read_text(encoding='utf-8'))
assert len(a['files'])==15 and not any('error'in r for r in a['files'])
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for data in iter(lambda:f.read(8*1024*1024),b''):h.update(data)
    return h.hexdigest()
assert {p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file() and not p.is_symlink()}=={r['name'] for r in a['files']}
for r in a['files']:assert digest(D/r['name'])==r['sha256'],r['name']
for p,h in b['protected'].items():
    data=(R/p).read_bytes()
    if 'Geostrategy' in p:data=data.split(b'\n\n<!-- DOWNLOADS_ESSENCE_REVIEW_20261008 -->')[0]
    assert hashlib.sha256(data).hexdigest()==h,p
names=['README.md','DGEF/README.md','V2.0.1/governance/README.md','V2.0.1/governance/source_review_contract.md','Reference/global_dns_download_audit_v2_2_0.md','Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Reference/Downloads_Essence_Review_20261008.qmd','Reference/Downloads_Essence_Review_20261008.html']
names += [p.relative_to(R).as_posix() for p in O.iterdir() if p.is_file() and p.name!='progress.json' and p.name!='validation_receipt.json']
source_hashes={r['sha256'] for r in a['files']};assert all(digest(R/n) not in source_hashes for n in names)
s=(R/'reports/2026-10-07/git_publish_and_html_recovery/audit.py').read_text(encoding='utf-8');ns={'re':re};exec(s[s.index('patterns='):s.index('for name in paths:')],ns)
hits=[]
for n in names:
    data=(R/n).read_bytes()
    for kind,pat in ns['patterns']:
        for m in pat.finditer(data):
            val=m[1] if kind=='CREDENTIAL_LITERAL' else m[0];low=val.decode('utf-8','ignore').lower().strip()
            if kind=='CREDENTIAL_LITERAL' and (low in ns['placeholders'] or low.startswith(('your_','your-','${','{{','<','process.env','os.environ')) or len(low)>256):continue
            hits.append({'path':n,'category':kind})
assert not hits,json.dumps(hits)
out={'source_files_rehashed_and_unchanged':15,'protected_content_preserved':3,'raw_files_copied':0,'business_records_imported':0,'credential_candidates_in_delivery':0,'semantic_claims_fully_verified':False,'iso_authenticity_verified':False,'delivery_files':names}
(O/'validation_receipt.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k!='delivery_files'}))
