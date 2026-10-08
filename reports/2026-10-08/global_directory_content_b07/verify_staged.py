from pathlib import Path
import sys
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/32_global_directory_content_b07_20261008'
sys.path.insert(0,str(O.parent/'global_directory_content_b05'))
import intake
intake.O=O;intake.T=T
source=(O.parent/'global_directory_content_b05/verify_staged.py').read_text(encoding='utf-8')
source=source.replace('B05_20261008','B07_20261008').replace('30_global_directory_content_b05','32_global_directory_content_b07').replace('global_directory_content_b05/','global_directory_content_b07/')
exec(compile(source,str(O/'verify_staged.py'),'exec'))
