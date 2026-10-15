"""Record individually reviewed official software descriptions and bounded updates."""
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
items=[
 (1,'PyTorch','Python 張量與動態神經網絡軟件','https://github.com/pytorch/pytorch','Repository description and README'),
 (2,'TensorFlow','機器學習平台','https://www.tensorflow.org/','An end-to-end platform for machine learning'),
 (3,'JAX','陣列計算與程式變換 Python 函式庫','https://docs.jax.dev/en/latest/','High performance array computing'),
 (4,'Qiskit','量子計算及演算法研究軟件','https://www.ibm.com/quantum/qiskit','Qiskit; Quantum information science toolkit'),
 (5,'Cirq','建立、操作及執行量子電路的 Python 框架','https://github.com/quantumlib/Cirq','README introduction'),
 (6,'PennyLane','量子計算、量子機器學習與量子化學軟件','https://github.com/PennyLaneAI/pennylane','README introduction'),
 (8,'NASA F Prime','飛行與嵌入式應用軟件框架','https://github.com/nasa/fprime','A Flight-Proven, Multi-Platform, Open-Source Flight Software Framework'),
 (9,'OpenMDAO','系統分析與多學科優化 Python 平台','https://github.com/OpenMDAO/OpenMDAO','README introduction'),
 (10,'Polars','DataFrame 函式庫','https://pola.rs/','Open source library / Polars'),
 (11,'DuckDB','分析型 SQL 資料庫','https://duckdb.org/','Database anywhere; DuckDB'),
 (12,'Kubernetes','容器應用部署、擴展與管理系統','https://kubernetes.io/','Production-Grade Container Orchestration'),
 (13,'PostgreSQL','物件關聯式資料庫系統','https://www.postgresql.org/about/','What is PostgreSQL?'),
 (14,'GDAL','柵格與向量地理空間格式轉換函式庫及工具','https://gdal.org/en/stable/','Introduction'),
 (15,'QGIS','地圖製作、圖層編輯及空間分析工具','https://qgis.org/','Create maps; Edit layers; Process and analyze'),
 (16,'Eclipse SUMO','微觀、多模態交通模擬軟件','https://eclipse.dev/sumo/','Simulation of Urban MObility introduction'),
 (17,'CARLA','自動駕駛研究模擬器','https://carla.org/','Introduction'),
 (18,'OpenStreetMap','社群協作維護的地圖資料項目','https://www.openstreetmap.org/about','About / Community Driven'),
 (19,'STAC','描述與編目時空資產的共同結構規範','https://stacspec.org/en/','What is STAC; The STAC Specification'),
 (20,'MNE','神經生理資料探索、視覺化與分析 Python 套件','https://mne.tools/stable/index.html','MNE-Python Homepage'),
 (21,'NITRC','神經影像資源登記、資料儲存與計算資源平台','https://www.nitrc.org/','Neuroimaging Resources Registry; Data Repository; Cloud Computing Environment'),
 (22,'ROS 2','建立機械人應用的軟件函式庫與工具','https://github.com/ros2/ros2','About / README'),
 (25,'BCI2000','供腦機介面研究的一般用途軟件系統','https://www.bci2000.org/mediawiki/index.php/Main_Page','What is BCI2000?'),
]
ledger=json.loads((OUT/'verified_facts.json').read_text(encoding='utf-8'))
for n,(num,name,claim,url,loc) in enumerate(items,49):
    ident=f'F{n:03}'
    if not any(x['id']==ident for x in ledger['facts']):
        ledger['facts'].append(dict(id=ident,claim=f'{name} 官方描述為{claim}。',status='SUPPORTED',source=url,locator=loc,
            document='Reference/Global_Technology_ISO249_Registry.qmd',registry_id=f'GTT{num:04}',checked_on='2026-10-15',
            boundary='僅核實公開用途／類型；未執行軟件、測量性能、核實最新版本／完整授權條款，亦未證明本項目部署、任務認證或臨床效能。'))
(OUT/'verified_facts.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8',newline='')
p=ROOT/'Reference/Global_Technology_ISO249_Registry.qmd';raw=p.read_bytes();marker='<!-- SOFTWARE_FACT_REVIEW_20261015 -->'
if marker.encode() not in raw:
    before=hashlib.sha256(raw).hexdigest();(OUT/'original_bytes'/f'{before}.bin').write_bytes(raw)
    addition='\n\n'+marker+'\n\n## 2026-10-15 軟件與規範續核\n\n'
    addition+='本輪逐項讀取下列22個項目的官方文件或官方程式庫，支持其基本用途描述。NASA cFS 沿用本輪台帳 F001 的限定判讀，不重複計數；不延伸至效能排名、任務認證、臨床效能、部署完成或特定版本授權。\n\n'
    addition+='| 登記 ID | 項目 | 本次來源支持的用途 | 官方來源 |\n| --- | --- | --- | --- |\n'
    addition+=''.join(f'| GTT{num:04} | {name} | {claim} | [來源]({url}) |\n' for num,name,claim,url,loc in items)
    addition+='\nGTT0019（STAC）與 GTT0025（BCI2000）在本次取得正文支持；上方 UNKNOWN 為2026-10-06歷史取得狀態，不覆寫舊 CSV。本節不是 STAC 指定版本符合性驗證，也不是 BCI2000 臨床許可。GTT0023（Orekit）官方頁仍有存取挑戰，GTT0024（Gazebo）首頁無可讀正文，兩者繼續待查。\n'
    with p.open('ab') as f:f.write(addition.replace('\n','\r\n').encode())
    after=hashlib.sha256(p.read_bytes()).hexdigest()
    receipt=dict(before_sha256=before,after_sha256=after,original_bytes_preserved=p.read_bytes().startswith(raw),new_supported_claims=len(items),
        still_unreadable=[dict(id='GTT0023',url='https://www.orekit.org/site-orekit-latest/index.html',result='Access challenge'),dict(id='GTT0024',url='https://gazebosim.org/',result='No readable body')],external_fact_review_complete=False)
    (OUT/'software_review_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8',newline='')
    changes=json.loads((OUT/'source_changes.json').read_text(encoding='utf-8'))
    target=next(x for x in changes if x['path']==p.relative_to(ROOT).as_posix());target['after_sha256']=after
    target['change']='bounded quantum and software public-description review; all pre-existing bytes preserved'
    (OUT/'source_changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8',newline='')
print('facts',len(ledger['facts']))
