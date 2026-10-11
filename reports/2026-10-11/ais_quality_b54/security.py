from pathlib import Path
import sys
O=Path(__file__).resolve().parent;R=O.parents[2]
T=R/'Reference/tables/77_ais_quality_b54_20261011'
sys.path.insert(0,str(R/'reports/2026-10-08'/'global_directory_content_b05'))
import intake
intake.O=O;intake.T=T
s=(R/'reports/2026-10-08'/'global_directory_content_b05/security.py').read_text(encoding='utf-8')
s=s.replace('Global_Directory_Content_Expansion_B05_20261008','AIS_Quality_B54_20261011')
s=s.replace('for root in [O,T]:',"for root in [O,T]+[R/n for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']]:")
s=s.replace("R/'Reference/AIS_Quality_B54_20261011.html']:","R/'Reference/AIS_Quality_B54_20261011.html',R/'Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd']:")
exec(compile(s,str(O/'security.py'),'exec'))
assert not findings,'Hold publication pending candidate review'
