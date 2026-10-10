from pathlib import Path
import subprocess, sys, argparse

O = Path(__file__).resolve().parent
R = O.parents[2]
SCOPES = ['.gitattributes', 'reports/2026-10-09/cmr_availability_b46', 'Reference/tables/70_cmr_availability_b46_20261009',
          'Reference/CMR_Availability_B46_20261009.qmd', 'Reference/CMR_Availability_B46_20261009.html'] + [
          n+'/cmr_availability_b46_20261009.md' for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']]

def execute(commands, runner=subprocess.run):
    for command in commands:
        runner(command, cwd=R, check=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    assert not subprocess.check_output(['git','diff','--cached','--name-only'], cwd=R), 'Index must be empty before scoped staging'
    execute([[sys.executable,str(O/'security.py')], [sys.executable,str(O/'verify.py'),'--preflight']])
    if not args.publish:
        return
    execute([['git','add','--']+SCOPES,
             [sys.executable,str(O/'verify.py')],
             ['git','add','--',str(O/'staged_acceptance.json')],
             [sys.executable,str(O/'verify.py')],
             ['git','add','--',str(O/'staged_acceptance.json')],
             ['git','commit','-m','Probe every ASF collection count and preserve product rights evidence B46'],
             ['git','push']])

if __name__ == '__main__':
    main()
