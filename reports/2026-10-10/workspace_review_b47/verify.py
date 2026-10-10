from pathlib import Path
import hashlib, json, csv, subprocess, sys

O=Path(__file__).resolve().parent
R=O.parents[2]
def sha(data): return hashlib.sha256(data).hexdigest()
base=json.loads((O/'baseline.json').read_text(encoding='utf-8'))
changed=[p for p,h in base['protected'].items() if not (R/p).is_file() or sha((R/p).read_bytes())!=h]
assert not changed, 'Protected documents changed after this batch began: '+repr(changed)
assert not json.loads((O/'credential_scan.json').read_text())['candidates'], 'Credential candidate requires review'
rows=json.loads((O/'content_review.json').read_text())
if '--preflight' not in sys.argv:
    from publish import SCOPES
    names=[n for n in subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).decode().split('\0') if n]
    assert names and all(any(n==s or n.startswith(s+'/') for s in SCOPES) for n in names), 'Unexpected staged path'
    # Compare through Git's configured clean filters; prior raw evidence above
    # is independently checked with SHA256 and is never newline-normalized.
    for n in names:
        expected=subprocess.check_output(['git','hash-object','--path='+n,n],cwd=R).strip()
        actual=subprocess.check_output(['git','rev-parse',':'+n],cwd=R).strip()
        assert expected==actual, 'Staged content differs after configured Git filters: '+n
    acceptance=dict(staged_files=len(names),protected_document_hashes_unchanged=True,
                    starting_worktree_status=base.get('starting_status','NOT_CAPTURED_IN_BASELINE'),reviewed_committed_paths=rows['committed_changed_paths'],
                    credential_candidates=0,staged_scope_verified=True,staged_git_filtered_content_verified=True)
    (O/'staged_acceptance.json').write_text(json.dumps(acceptance,indent=2)+'\n',encoding='utf-8')
print('PASS: current baseline, prior source bytes, credentials and applicable staging checks')
