"""Validate current receipts and bytes; never rewrite sources or restore files."""
from pathlib import Path
import collections,gzip,hashlib,json,re,subprocess,os
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()
results=read('results.json');manifest=read('rendered_passages_20261016_manifest.json')
ledger=read('verified_facts.json');facts=ledger['facts'];errors=[]
checked_on=ledger.get('last_updated',ledger.get('checked_on'))
assert re.fullmatch(r'\d{4}-\d{2}-\d{2}',checked_on)
assert len({f['id'] for f in facts})==len(facts)
by_path={d['path']:d for d in manifest['documents']}
expected=set()
for directory,dirs,files in os.walk(ROOT,followlinks=False):
    dirs[:]=[d for d in dirs if d!='.git' and not (Path(directory)/d).is_symlink() and (Path(directory)/d)!=OUT]
    expected.update((Path(directory)/name).relative_to(ROOT).as_posix() for name in files
                    if name.lower().endswith('.qmd') and not (Path(directory)/name).is_symlink())
assert len({r['path'] for r in results})==len(results)
assert {r['path'] for r in results}==expected, 'Render receipt does not cover every current QMD'
assert set(by_path)==expected, 'Passage manifest does not cover every current QMD'
for r in results:
    source=ROOT/r['path'];html=OUT/'rendered'/Path(r['path']).with_suffix('.html')
    if r['exit_code'] or not html.is_file():errors.append(dict(path=r['path'],issue='RENDER_FAILED'));continue
    if sha(source)!=r['source_sha256']:errors.append(dict(path=r['path'],issue='SOURCE_CHANGED'))
    d=by_path.get(r['path'])
    if not d or d['source_sha256']!=r['source_sha256'] or d['rendered_sha256']!=sha(html):errors.append(dict(path=r['path'],issue='PASSAGE_MANIFEST_STALE'))
baseline=read('before.json');protected='Reference/Aerospace_Ecosystem_Report.qmd'
assert sha(ROOT/protected)==next(x['sha256'] for x in baseline['files'] if x['path']==protected)
assert sha(OUT/'rendered_passages_20261016.jsonl.gz')==manifest['compressed_sha256']
count=0;docs=collections.Counter()
with gzip.open(OUT/'rendered_passages_20261016.jsonl.gz','rt',encoding='utf-8') as f:
    for line in f:
        row=json.loads(line);count+=1;docs[row['document']]+=1
        assert row['review_state']=='UNREVIEWED_PASSAGE'
        assert row['text_sha256']==hashlib.sha256(row['text'].encode()).hexdigest()
assert count==manifest['passage_occurrences']
assert all(docs[d['path']]==d['passages'] for d in manifest['documents'])
paths=set(subprocess.check_output(['git','-c','core.longpaths=true','ls-files','-m','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0'))-{''}
large=[];hits=[]
patterns=[rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',rb'gh[pousr]_[A-Za-z0-9]{30,}',rb'AKIA[0-9A-Z]{16}',rb'sk-proj-[A-Za-z0-9_-]{60,}',rb'xox[baprs]-[0-9A-Za-z-]{30,}']
for rel in paths:
    p=ROOT/rel
    if not p.is_file():continue
    if p.stat().st_size>100*1024*1024:large.append(rel)
    data=gzip.decompress(p.read_bytes()) if p.name=='rendered_passages_20261016.jsonl.gz' else p.read_bytes()
    if any(re.search(pattern,data) for pattern in patterns):hits.append(rel)
preservation=[]
if (OUT/'continuation_20261017_baseline.json').exists():
    for r in read('continuation_20261017_baseline.json')['preexisting_pending_files']:
        preservation.append(dict(path=r['path'],unchanged_since_capture=(ROOT/r['path']).is_file() and sha(ROOT/r['path'])==r['sha256']))
receipt=dict(checked_on=checked_on,head_before_publication=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    successful_render_records=len(results),fact_count=len(facts),fact_statuses=dict(collections.Counter(f['status'] for f in facts)),
    validation_errors=errors,preexisting_user_changes=preservation,protected_aerospace_unchanged=True,gzip_json_records_validated=count,documents_with_selected_passages=len(docs),
    modified_or_new_files_reviewed=len(paths),over_100MiB=large,strict_credential_format_candidate_paths=hits,
    external_fact_review_complete=False,scope='Current source/output/paragraph hashes and records; strict-format credential preflight only; ignored credential/runtime exclusions respected. Not factual certification of pending passages.')
(OUT/('publication_'+checked_on.replace('-','')+'_preflight.json')).write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8',newline='')
print(json.dumps(receipt,ensure_ascii=True))
assert not errors and not large and not hits
