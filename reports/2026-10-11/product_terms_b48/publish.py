from pathlib import Path
import subprocess, sys, argparse

O = Path(__file__).resolve().parent
R = O.parents[2]
SCOPES = ['.gitattributes', 'reports/2026-10-11/product_terms_b48', 'Reference/tables/71_product_terms_b48_20261011',
          'Reference/Product_Terms_B48_20261011.qmd', 'Reference/Product_Terms_B48_20261011.html'] + [
          n+'/product_terms_b48_20261011.md' for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']]

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
             ['git','commit','-m','Preserve per product license obligations and revision evidence B48'],
             ['git','push']])

if __name__ == '__main__':
    main()
