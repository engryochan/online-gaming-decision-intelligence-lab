from pathlib import Path
import subprocess, sys, argparse

O = Path(__file__).resolve().parent
R = O.parents[2]
SCOPES = ['Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd', '.gitattributes', 'reports/2026-10-11/ais_semantics_b53', 'Reference/tables/76_ais_semantics_b53_20261011',
          'Reference/AIS_Semantics_B53_20261011.qmd', 'Reference/AIS_Semantics_B53_20261011.html'] + [
          n+'/ais_semantics_b53_20261011.md' for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']]

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
             ['git','commit','-m','Preserve period specific AIS schemas and use limitations B53'],
             ['git','push']])

if __name__ == '__main__':
    main()
