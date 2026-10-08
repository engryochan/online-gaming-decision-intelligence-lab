"""Stage reviewed research CSV files without forcing ignored secrets/runtime."""
from pathlib import Path
import json, subprocess

root = Path(__file__).resolve().parents[3]
audit = json.loads((Path(__file__).parent / 'workspace_audit.json').read_text(encoding='utf-8'))
excluded = {r['path'] for r in audit['candidate_secret_files']}
paths = [p.decode('utf-8') for p in subprocess.check_output(
    ['git', 'ls-files', '-z', '--others', '--ignored', '--exclude-standard', 'reports'], cwd=root).split(b'\0')
    if p and p.decode('utf-8').endswith('.csv')]
for path in paths:
    if path not in excluded:
        subprocess.run(['git', 'add', '-f', '--', path], cwd=root, check=True)
subprocess.run(['git', 'add', '--all'], cwd=root, check=True)
print(json.dumps(dict(research_csv_staged=len([p for p in paths if p not in excluded]))))
