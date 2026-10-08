from pathlib import Path
import hashlib,json
O=Path(__file__).parent;R=O.parents[2];T=R/'Reference/tables/27_global_expansion_b02_20261007';save=O/'failed_build_01';assert not save.exists();save.mkdir();receipt=[]
for p in [O/'global_universe_v5.sqlite',T/'registry_euronext_download_all_rows.csv',T/'registry_market_label_MIC_candidates.csv']:
 assert p.resolve().is_relative_to(R.resolve()) and p.exists();target=save/p.name;assert target.resolve().is_relative_to(R.resolve()) and not target.exists();sha=hashlib.sha256(p.read_bytes()).hexdigest();p.rename(target);receipt.append(dict(original=str(p.relative_to(R)),preserved=str(target.relative_to(R)),sha256=sha))
(save/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print('Incomplete generated artifacts retained before corrected build')
