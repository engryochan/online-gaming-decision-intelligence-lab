"""Repair navigation only in newly generated Quarto HTML, never historical HTML snapshots."""
from pathlib import Path
from urllib.parse import unquote,urlsplit,quote
from html import unescape,escape
import json,os,re
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
DELIVERY=OUT/'rendered'
rows=json.loads((OUT/'results.json').read_text(encoding='utf-8'))
prior=json.loads((OUT/'delivery_link_repairs.json').read_text(encoding='utf-8')) if (OUT/'delivery_link_repairs.json').exists() else {}
changed=prior.get('changed_documents',[]);missing=[];origins=[]
for row in rows:
    if row.get('renderer') in {'lossless-html-snapshot','html-snapshot-with-markdown-appendix'}:continue
    p=DELIVERY/Path(row['path']).with_suffix('.html')
    data=p.read_text(encoding='utf-8');edits=[]
    canonical=ROOT/'Reference'/Path(row['path']).name
    origin=None
    if canonical.is_file() and canonical!=(ROOT/row['path']):
        def title(path):
            m=re.search(r'(?m)^title:\s*(.+)$',path.read_text(encoding='utf-8-sig')[:6000])
            return m[1].strip() if m else None
        if title(canonical) and title(canonical)==title(ROOT/row['path']):
            origin=canonical.parent
            origins.append(dict(document=row['path'],reference_origin=canonical.relative_to(ROOT).as_posix(),
                                evidence='same filename and identical frontmatter title; only unresolved references use this origin'))
    def replace(match):
        raw=match[2];ref=unescape(raw);parts=urlsplit(ref)
        if parts.scheme or parts.netloc or not parts.path or parts.path.startswith('/'):return match[0]
        dest=(p.parent/unquote(parts.path)).resolve()
        if not dest.is_relative_to(DELIVERY):return match[0]
        rel=dest.relative_to(DELIVERY)
        replacement=None
        if dest.suffix.lower()=='.qmd' and dest.with_suffix('.html').is_file():
            replacement=os.path.relpath(dest.with_suffix('.html'),p.parent).replace('\\','/')
        elif dest.exists():return match[0]
        elif (ROOT/rel).is_file():
            # Linked datasets remain in the same workspace; no duplicate large archives.
            replacement=os.path.relpath(ROOT/rel,p.parent).replace('\\','/')
        elif origin:
            candidate=(origin/unquote(parts.path)).resolve()
            if candidate.is_relative_to(ROOT) and candidate.is_file():
                candidate_rel=candidate.relative_to(ROOT)
                rendered=DELIVERY/candidate_rel.with_suffix('.html')
                if candidate.suffix.lower()=='.qmd' and rendered.is_file():candidate=rendered
                elif candidate.suffix.lower()=='.html' and (DELIVERY/candidate_rel).is_file():candidate=DELIVERY/candidate_rel
                replacement=os.path.relpath(candidate,p.parent).replace('\\','/')
            else:
                missing.append(dict(document=row['path'],href=ref));return match[0]
        else:
            missing.append(dict(document=row['path'],href=ref));return match[0]
        replacement=quote(replacement,safe='/')
        if parts.query:replacement+='?'+parts.query
        if parts.fragment:replacement+='#'+parts.fragment
        edits.append(dict(before=ref,after=replacement))
        return match[1]+escape(replacement,quote=True)+match[3]
    updated=re.sub(r'(<a\b[^>]*?\bhref=")([^"]*)(")',replace,data,flags=re.I)
    if edits:
        p.write_text(updated,encoding='utf-8',newline='')
        changed.append(dict(document=row['path'],edits=edits))
merged={}
for entry in changed:merged.setdefault(entry['document'],[]).extend(entry['edits'])
changed=[dict(document=doc,edits=edits) for doc,edits in sorted(merged.items())]
(OUT/'delivery_link_repairs.json').write_text(json.dumps(dict(changed_documents=changed,validated_reference_origins=origins,unresolved_links=missing,
    scope='Newly generated Quarto HTML only. QMD links lead to rendered HTML; existing data/document links lead back to the original workspace. Snapshots remain byte-preserved.'),ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(changed_documents=len(changed),link_repairs=sum(len(x['edits']) for x in changed),unresolved_links=len(missing))))
