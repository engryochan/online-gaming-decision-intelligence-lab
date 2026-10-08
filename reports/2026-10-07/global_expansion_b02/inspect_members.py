from pathlib import Path
from lxml import html
import json
t=html.fromstring((Path(__file__).parent/'raw/members_iframe.html').read_bytes());tb=t.xpath('//table')[0]
print(json.dumps([(r.get('class'),len(r.xpath('./td|./th'))) for r in tb.xpath('./thead/tr|./tbody/tr|./tr')[:8]]))
for a in t.xpath('//a[@href]'):
 text=' '.join(a.itertext()).strip();h=a.get('href')
 if 'page=' in h or 'pager' in str(a.get('class')) or 'Next' in text:print(json.dumps([text,h,a.get('rel')]))
print(json.dumps([' '.join(x.itertext()).strip() for x in t.xpath('//*[contains(@class,"view-header") or contains(@class,"view-footer")]')]))
