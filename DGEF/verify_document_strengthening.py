"""Check the actual appended documents and preserve original bytes."""
from pathlib import Path
import hashlib,json,re,zipfile
from strengthen_documents import ROOT,OUT,TARGETS
checks=[]
with zipfile.ZipFile(OUT/'before_two_document_updates.zip') as z:
    for p in TARGETS:
        name=p.relative_to(ROOT).as_posix();old=z.read(name);current=p.read_bytes()
        assert current.startswith(old),name
        addition=current[len(old):].decode('utf-8')
        for topic in ['redteam／','critic／','killcritic／','blindspot／','cheatsheet／','blueprint／','actionplan／']:
            assert '### '+topic in addition,(name,topic)
        for link in re.findall(r'\]\(([^)]+)\)',addition):
            if not link.startswith('https://'):assert (p.parent/link).is_file(),(name,link)
        checks.append({'path':name,'prefix_preserved':True,'seven_topics_present':True,'new_local_links_resolve':True,'sha256':hashlib.sha256(current).hexdigest()})
for file in ['qmd_parse.json','md_parse.json']:
    ast=json.loads((OUT/file).read_text(encoding='utf-8'));assert ast['blocks']
result={'document_checks':checks,'pandoc_qmd_parse':'PASS','pandoc_md_parse':'PASS','quarto_execution':'NOT_RUN','review_limitations':['One active RStudio lock unreadable','Existing create_ogdil.py syntax error not repaired','Binary contents not semantically or visually certified','No all-external-claims recertification']}
(OUT/'acceptance.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
for file in ['qmd_parse.json','md_parse.json']:(OUT/file).unlink()
print(json.dumps(result,ensure_ascii=True))
