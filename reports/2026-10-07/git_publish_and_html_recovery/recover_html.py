"""Lossless QMD snapshots; use this renderer for byte-identical HTML output.

Ordinary Quarto rendering adds its own document shell and is not byte-identical.
The raw HTML block is the editable source; no hidden payload overrides edits.
"""
from pathlib import Path
import argparse, hashlib, json, subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
MANIFEST = HERE / 'recovery_manifest.json'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def render(record, destination):
    source = (ROOT / record['qmd']).read_bytes()
    start = record['begin'].encode() + b'\n'
    end = b'\n' + record['end'].encode() + b'\n'
    if source.count(start) != 1 or source.count(end) != 1:
        raise ValueError('Missing or ambiguous source delimiters: ' + record['qmd'])
    data = source.split(start, 1)[1].split(end, 1)[0]
    output = destination / record['html']
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    return dict(html=record['html'], output_sha256=sha(data),
                source_html_unchanged=sha((ROOT / record['html']).read_bytes()) == record['sha256'],
                byte_identical=data == (ROOT / record['html']).read_bytes())

def recover():
    audit = json.loads((HERE / 'workspace_audit.json').read_text(encoding='utf-8'))
    excluded = {r['path'] for r in audit['candidate_secret_files']}
    records, withheld = [], []
    attrs = []
    for item in audit['html_without_same_stem_qmd']:
        name = item['path']
        if name in excluded:
            withheld.append(dict(html=name, reason='Credential candidate; no derivative created'))
            continue
        html = ROOT / name
        qmd = html.with_suffix('.qmd')
        if qmd.exists():
            raise FileExistsError(str(qmd))
        data = html.read_bytes()
        digest = sha(data)
        fence = '`' * 8
        while fence.encode() in data:
            fence += '`'
        begin, end = fence + '{=html}', fence
        relative = qmd.relative_to(ROOT).as_posix()
        history = subprocess.check_output(['git', 'log', '--all', '--format=%H', '--', relative], cwd=ROOT).decode().splitlines()
        md = html.with_suffix('.md')
        # Exact existing bytes stay inside the raw block, including BOM/newlines.
        header = ('---\nformat: html\nexecute:\n  enabled: false\n'
                  'recovery-kind: lossless-html-snapshot\n'
                  'original-html: ' + json.dumps(name, ensure_ascii=False) + '\n'
                  'original-sha256: ' + digest + '\n---\n\n'
                  '<!-- Byte-exact renderer: reports/2026-10-07/git_publish_and_html_recovery/recover_html.py --render. '
                  'Quarto default rendering is not byte-exact. -->\n\n')
        qmd.write_bytes(header.encode('utf-8') + begin.encode() + b'\n' + data + b'\n' + end.encode() + b'\n')
        records.append(dict(html=name, qmd=relative, sha256=digest, bytes=len(data),
                            classifier=item['classifier'], begin=begin, end=end,
                            qmd_history_commits=history, markdown_candidate=md.relative_to(ROOT).as_posix() if md.exists() else None,
                            provenance='Current HTML snapshot; original author Markdown not claimed recovered'))
        attrs.append('"' + relative + '" -text\n')
    with (ROOT / '.gitattributes').open('a', encoding='utf-8', newline='\n') as f:
        f.writelines(attrs)
    MANIFEST.write_text(json.dumps(dict(records=records, withheld=withheld), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return records

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    records = json.loads(MANIFEST.read_text(encoding='utf-8'))['records'] if args.render else recover()
    destination = HERE / 'preview'
    results = [render(r, destination) for r in records]
    receipt = dict(count=len(results), all_byte_identical=all(r['byte_identical'] for r in results),
                   all_originals_unchanged=all(r['source_html_unchanged'] for r in results), results=results)
    (HERE / 'byte_exact_acceptance.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in receipt.items() if k != 'results'}))
    if not receipt['all_byte_identical'] or not receipt['all_originals_unchanged']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
