"""Preserve completed probes and label an interrupted outstanding response."""
from pathlib import Path
import csv,json
O=Path(__file__).parent;T=O.parents[2]/'Reference/tables/28_global_market_sources_b03_20261008'
rows=[json.loads(line) for line in (O/'probe_progress.jsonl').read_text(encoding='utf-8').splitlines()]
done={r['url'] for r in rows}
for record in csv.DictReader((T/'registry_global_source_endpoints.csv').open(encoding='utf-8-sig')):
    if record['url'] not in done:
        rows.append(dict(url=record['url'],http_status='',checked_on='2026-10-08',status='INTERRUPTED_PENDING_RESPONSE',
                         note='Probe was dispatched; response not completed when run was interrupted. Not a confirmed HTTP error or site refusal.'))
fields=list(dict.fromkeys(k for row in rows for k in row))
with (T/'registry_endpoint_live_checks.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
print(json.dumps(dict(response_receipts=len(done),interrupted=len(rows)-len(done))))
