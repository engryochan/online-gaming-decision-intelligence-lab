from pathlib import Path
import sys
O=Path(__file__).resolve().parent;R=O.parents[2]
T=R/'Reference/tables/53_global_registration_authorities_b28_20261008'
sys.path.insert(0,str(O.parent/'global_directory_content_b05'))
import intake
intake.O=O;intake.T=T
s=(O.parent/'global_directory_content_b05/security.py').read_text(encoding='utf-8')
s=s.replace('Global_Directory_Content_Expansion_B05_20261008','Global_Registration_Authorities_B28_20261008')
s=s.replace('for root in [O,T]:',"for root in [O,T]+[R/n for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']]:")
exec(compile(s,str(O/'security.py'),'exec'))
assert not findings,'Hold publication pending candidate review'
