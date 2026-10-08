from pathlib import Path
import re,json,sqlite3
O=Path(__file__).parent
d=(O/'global_source_registry_b03.sqlite').read_bytes()
pattern=re.compile(rb'''(?im)["']?(password|passwd|pwd|api[_-]?key|client[_-]?secret|access[_-]?token|secret[_-]?key)["']?\s*[:=]\s*["']([^"'\r\n]{4,})["']''')
results=[]
for match in pattern.finditer(d):
    value=match.group(2)
    results.append(dict(field=match.group(1).decode(),length=len(value),starts_http=value.startswith(b'http'),contains_binary=any(c<32 for c in value),redacted=True))
print(json.dumps(results))
token=re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}|AKIA[A-Z0-9]{16}|sk-proj-[A-Za-z0-9_-]{30,}|xox[baprs]-[A-Za-z0-9-]{20,})')
with sqlite3.connect(O/'global_source_registry_b03.sqlite') as con:
    for match in token.finditer(d):
        value=match.group().decode();locations=[]
        for (table,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'"):
            cols=[row[1] for row in con.execute('PRAGMA table_info("'+table+'")')]
            for col in cols:
                count=con.execute('SELECT COUNT(*) FROM "'+table+'" WHERE instr("'+col+'",?)>0',(value,)).fetchone()[0]
                if count:locations.append(dict(table=table,column=col,rows=count))
        print(json.dumps(dict(format='AWS_STYLE' if value.startswith('AKIA') else 'OTHER',length=len(value),locations=locations,redacted=True)))
