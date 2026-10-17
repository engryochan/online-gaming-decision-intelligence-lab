"""Expand review coverage to rendered paragraphs/tables, including HTML snapshots.
This inventories unreviewed text, not atomic claims or verified facts.
"""
from pathlib import Path
from lxml import html
import gzip,hashlib,json,re
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
results=json.loads((OUT/'results.json').read_text(encoding='utf-8'))
documents=[];total=0
target=OUT/'rendered_passages_20261016.jsonl.gz'
with target.open('wb') as raw, gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as stream:
    for row in results:
        p=OUT/'rendered'/Path(row['path']).with_suffix('.html');data=p.read_bytes()
        tree=html.fromstring(data);roottree=tree.getroottree();count=0
        # tr retains context across table cells. Prefer paragraphs inside list items over the whole list.
        for node in tree.xpath('//p | //tr | //li[not(.//p) and not(.//li)] | //h1 | //h2 | //h3 | //h4 | //h5 | //h6'):
            ancestors=list(node.iterancestors())
            if any(a.tag in {'pre','code','script','style'} for a in ancestors):continue
            # Some saved pages have unclosed outer navigation. A nested main still contains the article.
            nearest_main=next((i for i,a in enumerate(ancestors) if a.tag=='main'),None)
            if nearest_main is not None:
                if any(a.tag in {'nav','footer'} for a in ancestors[:nearest_main]):continue
            elif any(a.tag in {'nav','header','footer'} for a in ancestors):continue
            if any(a.tag=='tr' for a in node.iterancestors()):continue
            text=' '.join(node.text_content().split())
            if not text:continue
            count+=1;total+=1
            record=dict(document=row['path'],source_sha256=row['source_sha256'],html_xpath=roottree.getpath(node),
                element=node.tag,text=text,text_sha256=hashlib.sha256(text.encode()).hexdigest(),review_state='UNREVIEWED_PASSAGE')
            stream.write((json.dumps(record,ensure_ascii=False)+'\n').encode())
        if row.get('renderer') in {'lossless-html-snapshot','html-snapshot-with-markdown-appendix'}:
            # A recovered report can intentionally store prose as escaped Markdown in pre.
            for pre in tree.xpath('//pre[not(.//code)]'):
                text=pre.text_content()
                if not re.match(r'\s*#\s+\S',text):continue
                for index,paragraph in enumerate(re.split(r'\r?\n\s*\r?\n',text),1):
                    paragraph=paragraph.strip()
                    if not paragraph:continue
                    total+=1;count+=1
                    record=dict(document=row['path'],source_sha256=row['source_sha256'],html_xpath=roottree.getpath(pre),
                        preformatted_paragraph=index,element='preformatted_markdown_prose',text=paragraph,
                        text_sha256=hashlib.sha256(paragraph.encode()).hexdigest(),review_state='UNREVIEWED_PASSAGE')
                    stream.write((json.dumps(record,ensure_ascii=False)+'\n').encode())
        documents.append(dict(path=row['path'],passages=count,source_sha256=row['source_sha256'],
            current_source_hash_matches=hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['source_sha256'],
            rendered_sha256=hashlib.sha256(data).hexdigest(),renderer=row.get('renderer','Quarto HTML')))
manifest=dict(created_on='2026-10-16',documents=documents,document_count=len(documents),passage_occurrences=total,
    updated_on=json.loads((OUT/'verified_facts.json').read_text(encoding='utf-8')).get('last_updated','2026-10-16'),
    documents_with_extracted_passages=sum(d['passages']>0 for d in documents),
    documents_without_selected_passages=[d['path'] for d in documents if not d['passages']],
    compressed_bytes=target.stat().st_size,compressed_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
    all_source_hashes_current=all(d['current_source_hash_matches'] for d in documents),
    scope='Rendered paragraph/list/table-row/headings inventory for 358 QMDs, including HTML snapshots. Nested main takes precedence over malformed outer navigation; escaped Markdown prose in pre is a labelled fallback. Text is unreviewed; not a complete atomic-claim inventory. Code, navigation, scripts, images/OCR, text outside selected elements and remote dynamic content are not substantively verified. XPath refers to the recorded HTML hash, not source line numbers.',
    external_fact_review_complete=False)
(OUT/'rendered_passages_20261016_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8',newline='')
print(json.dumps({k:v for k,v in manifest.items() if k!='documents'},ensure_ascii=True))
