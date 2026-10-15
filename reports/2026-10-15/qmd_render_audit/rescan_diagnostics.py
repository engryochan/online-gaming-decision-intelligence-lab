"""Read-only diagnostics of project files; writes receipts only in this directory."""
from pathlib import Path
import collections, hashlib, json, os, re, subprocess
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()
counts=collections.Counter(); issues=[]; qmd=[]; skipped=[]
text_types={'.qmd','.md','.py','.r','.json','.yaml','.yml','.toml','.csv','.html','.js','.css','.tex','.lua','.bib'}
for directory,dirs,files in os.walk(ROOT,followlinks=False):
    dirs[:]=[d for d in dirs if d!='.git' and not (Path(directory)/d).is_symlink()]
    for name in files:
        p=Path(directory)/name; rel=p.relative_to(ROOT).as_posix()
        if p.is_symlink(): continue
        counts[p.suffix.lower() or '[no extension]']+=1
        # Disposable render mirrors are counted, but not treated as independent source documents.
        if p.is_relative_to(OUT/'staging') or p.is_relative_to(OUT/'jobs'): continue
        if p.suffix.lower() not in text_types: continue
        try: data=p.read_bytes(); s=data.decode('utf-8-sig')
        except UnicodeDecodeError:
            issues.append({'path':rel,'issue':'NON_UTF8_TEXT_REQUIRES_ENCODING_REVIEW'});continue
        except OSError as e:
            skipped.append({'path':rel,'error':type(e).__name__});continue
        if p.suffix.lower()=='.json':
            try: json.loads(s)
            except (ValueError,RecursionError) as e: issues.append({'path':rel,'issue':'JSON_PARSE_ERROR','detail':type(e).__name__})
        if p.suffix.lower()=='.qmd':
            qmd.append({'path':rel,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
            if not re.match(r'\A---\r?\n',s): issues.append({'path':rel,'issue':'QMD_NO_YAML_HEADER_REVIEW'})
            if re.search(r'^<<<<<<< |^>>>>>>> ',s,re.M): issues.append({'path':rel,'issue':'POSSIBLE_MERGE_MARKER'})
prior=json.loads((OUT/'results.json').read_text(encoding='utf-8'))
by_path={r['path']:r for r in prior}; current={r['path']:r for r in qmd}
stale=[r['path'] for r in qmd if r['path'] in by_path and r['sha256']!=by_path[r['path']]['source_sha256']]
missing=[r['path'] for r in prior if r['path'] not in current]
new=[r['path'] for r in qmd if r['path'] not in by_path]
output_missing=[r['path'] for r in prior if not (OUT/'rendered'/Path(r['path']).with_suffix('.html')).is_file()]
receipt={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
 'regular_file_type_counts':dict(counts.most_common()),'qmd_source_count':len(qmd),'qmd_sources':qmd,
 'stale_render_source_paths':stale,'new_qmd_paths':new,'removed_qmd_paths':missing,
 'missing_render_outputs':output_missing,'diagnostic_candidates':issues,'read_errors':skipped,
 'scope':'All regular-file extensions inventoried; selected text types UTF-8 checked and JSON parsed. Render staging/jobs counted but excluded as independent QMDs. Findings are review candidates, not factual certification.'}
(OUT/'rescan_diagnostics.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in receipt.items() if k not in {'qmd_sources','diagnostic_candidates','regular_file_type_counts'}},ensure_ascii=False))
print('diagnostic_candidates',len(issues),'file_count',sum(counts.values()))
