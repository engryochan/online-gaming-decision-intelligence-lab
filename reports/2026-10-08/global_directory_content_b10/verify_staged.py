from pathlib import Path
import sys
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/35_global_directory_content_b10_20261008'
sys.path.insert(0,str(O.parent/'global_directory_content_b05'))
import intake
intake.O=O;intake.T=T
source=(O.parent/'global_directory_content_b05/verify_staged.py').read_text(encoding='utf-8')
source=source.replace('B05_20261008','B10_20261008').replace('30_global_directory_content_b05','35_global_directory_content_b10').replace('global_directory_content_b05/','global_directory_content_b10/')
exec(compile(source,str(O/'verify_staged.py'),'exec'))
