"""Reversible, byte-preserving table-file migration within this checkout."""
from pathlib import Path
import csv, hashlib, json, os, zipfile
from table_layout import table_category

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'reports/2026-10-04/table_reclassification'
EXT={'.csv','.tsv','.xlsx','.xls','.parquet','.feather','.rds','.sqlite','.db','.duckdb'}
SKIP={'.git','.Rproj.user','__pycache__','.venv','renv','node_modules'}
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def scan():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and p.suffix.lower() in EXT and not any(x in SKIP or x.startswith('test-') for x in p.relative_to(ROOT).parts) and OUT not in p.parents)
def target(p):
    rel=p.relative_to(ROOT); s=rel.as_posix(); n=p.name
    if rel.parent==Path('Reference'):
        cat='01_country_area' if n.startswith('registry_country') else '02_admin_units' if n.startswith('registry_admin') else '03_governance_monarchies' if n.startswith('registry_sovereign') else '04_gaming_catalogue'
        return ROOT/'Reference/tables'/cat/n,cat
    if rel.parent==Path('DGEF/artifacts/tables'):
        cat=table_category(p.stem);return p.parent/cat/n,cat
    if s=='DGEF/data_dictionary.csv':return ROOT/'DGEF/contracts'/n,'data_dictionary'
    if rel.parent==Path('reports/2026-10-04') and p.suffix in {'.csv','.tsv'}:
        cat='01_services' if n=='strategy_services_registry.csv' else '02_catalogue_extraction' if n in {'catalogue_seed.tsv','original_172_entries.csv','gaming_70_entries.csv'} else '03_sources_evidence' if n in {'source_urls.csv','entity_source_evidence.csv','live_checks.tsv'} else '04_file_audit'
        return p.parent/'tables'/cat/n,cat
    if s=='reports/2026-10-04/dgef/表施工与数据覆盖对账.csv':return p.parent/'tables/coverage'/n,'coverage'
    return p,'database_snapshot' if p.suffix in {'.sqlite','.db','.duckdb'} else 'existing_dictionary_classification'

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/'migration_manifest.json').exists():raise RuntimeError('Migration already recorded; do not repeat blindly')
    rows=[]
    for p in scan():
        dest,cat=target(p)
        assert dest.resolve().is_relative_to(ROOT.resolve())
        if dest!=p and dest.exists():raise FileExistsError(dest)
        rows.append(dict(old_path=p.relative_to(ROOT).as_posix(),new_path=dest.relative_to(ROOT).as_posix(),category=cat,bytes=p.stat().st_size,sha256=digest(p),moved=dest!=p))
    (OUT/'migration_manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    with zipfile.ZipFile(OUT/'before_reclassification.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
        for r in rows:z.write(ROOT/r['old_path'],r['old_path'])
    for r in rows:
        if r['moved']:
            dest=ROOT/r['new_path'];dest.parent.mkdir(parents=True,exist_ok=True)
            (ROOT/r['old_path']).rename(dest)
    changes=[]
    # Correct executable paths and present-day documentation, preserving JSON/CSV
    # evidence payloads, response snapshots, and the attachment transcript verbatim.
    for p in ROOT.rglob('*'):
        if not p.is_file() or p.suffix not in {'.py','.md','.qmd','.html','.sql'}:continue
        if any(x in SKIP or x.startswith('test-') for x in p.relative_to(ROOT).parts) or OUT in p.parents or ROOT/'DGEF/inbox' in p.parents:continue
        if p.name=='reclassify_tables.py':continue
        raw=p.read_bytes()
        try:text=raw.decode('utf-8-sig')
        except UnicodeDecodeError:continue
        old=text
        for r in sorted(rows,key=lambda x:len(x['old_path']),reverse=True):
            if not r['moved']:continue
            a,b=r['old_path'],r['new_path']
            # Match full project paths or local relative paths as standalone path tokens.
            bases=[ROOT, p.parent]
            if p.suffix=='.py':bases += [ROOT/'DGEF',ROOT/'reports/2026-10-04',ROOT/'reports/2026-10-04/dgef']
            pairs={(a,b)}
            for base in bases:
                aa=os.path.relpath(ROOT/a,base).replace('\\','/');bb=os.path.relpath(ROOT/b,base).replace('\\','/')
                pairs.add((aa,bb))
            import re
            for aa,bb in sorted(pairs,key=lambda x:len(x[0]),reverse=True):
                text=re.sub(r'(?<![\w/\\])'+re.escape(aa)+r'(?![\w])',lambda m:bb,text)
        if text!=old:
            with zipfile.ZipFile(OUT/'before_reference_updates.zip','a',compression=zipfile.ZIP_DEFLATED) as z:z.writestr(p.relative_to(ROOT).as_posix(),raw)
            p.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+text.encode('utf-8'))
            changes.append(p.relative_to(ROOT).as_posix())
    assert all(digest(ROOT/r['new_path'])==r['sha256'] for r in rows)
    fields=list(rows[0])
    with (OUT/'数据表分类总索引.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rows)
    lines=['# 数据表分类总索引','','分类保留原始文件名、版本日期、记录粒度与全部字节。数据库及已有ODS字典目录保留其职责；JSON响应、HTML报告和SQL定义不冒充独立数据表。','', '| 分类 | 文件数 |','|---|---|']
    from collections import Counter
    for k,v in sorted(Counter(r['category'] for r in rows).items()):lines.append(f'| {k} | {v} |')
    lines+=['','## 文件定位','','| 类别 | 当前文件 |','|---|---|']
    for r in rows:
        link=os.path.relpath(ROOT/r['new_path'],OUT).replace('\\','/')
        lines.append(f"| {r['category']} | [{Path(r['new_path']).name}](<{link}>) |")
    lines+=['','旧路径记载在历史证据及数据库来源URI中继续保留，使用migration_manifest.json或CSV索引定位现址；不改写历史原始数据。','']
    (OUT/'README.md').write_text('\n'.join(lines),encoding='utf-8')
    (OUT/'reference_updates.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'inventoried':len(rows),'moved':sum(r['moved'] for r in rows),'reference_files_updated':len(changes),'all_file_hashes_preserved':True}))
if __name__=='__main__':main()
