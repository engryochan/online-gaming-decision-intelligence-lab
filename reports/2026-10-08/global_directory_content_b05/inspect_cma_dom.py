import csv,json
from lxml import html
import intake
rows=list(csv.DictReader((intake.T/'directory_fetch_manifest.csv').open(encoding='utf-8-sig')))
r=next(r for r in rows if 'cmauganda.co.ug/cma-licensed-firms' in r['url'])
tree=html.fromstring((intake.R/r['file']).read_bytes())
heading=next(n for n in tree.xpath('//h2') if n.text_content().strip()=='Stock Brokers')
print([(n.tag,n.get('class','')) for n in heading.iterancestors()][:6])
parent=heading.getparent().getparent()
print(html.tostring(parent,encoding='unicode')[:4500])
