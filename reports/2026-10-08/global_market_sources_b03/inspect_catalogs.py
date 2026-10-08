from pathlib import Path
from lxml import html
O=Path(__file__).parent
for path in sorted((O/'raw').glob('IOSCO_*.response')):
    t=html.fromstring(path.read_bytes())
    print(path.name,[(a.text_content().strip(),a.get('href')) for a in t.xpath('//a[@href]') if any(k in a.get('href').lower() for k in ('page=','pageno','page_no','start='))])
    print('pagination',[(a.text_content().strip(),a.get('href')) for a in t.xpath('//*[contains(@class,"pagination")]//a')])
t=html.fromstring((O/'raw/WFE.response').read_bytes())
print('WFE',[(x.text_content().strip()[:80],x.xpath('.//a/@href')) for x in t.xpath('//section[@id="member-list"]//li') if not x.xpath('.//a') or any('world-exchanges.org' in u for u in x.xpath('.//a/@href'))])
