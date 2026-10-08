from pathlib import Path
O=Path(__file__).resolve().parent
source=(O.parent/'global_directory_content_b06/download.py').read_text(encoding='utf-8')
source=source.replace('31_global_directory_content_b06','32_global_directory_content_b07').replace('REGULATORY_SECURITIZATION_FILING_SOURCE_ROW_NOT_COMPANY_UNIVERSE','SOURCE_FILE_ROW_SCHEMA_AND_ENTITY_SCOPE_PENDING')
source=source.replace("csv.reader(io.StringIO(text),delimiter=';')","csv.reader(io.StringIO(text),delimiter=(';' if text.splitlines()[0].count(';')>=text.splitlines()[0].count(',') else ','))")
(O/'download.py').write_text(source,encoding='utf-8')
for name in ['publish_check.py','verify_staged.py']:
    source=(O.parent/'global_directory_content_b06'/name).read_text(encoding='utf-8')
    source=source.replace('31_global_directory_content_b06','32_global_directory_content_b07').replace('B06_20261008','B07_20261008').replace('# B06 credential','# B07 credential').replace('global_directory_content_b06/**/*.response','global_directory_content_b07/**/*.response')
    if name=='verify_staged.py':
        source=source.replace("replace('B05_20261008','B06_20261008')","replace('B05_20261008','B07_20261008')").replace("replace('global_directory_content_b05/','global_directory_content_b06/')","replace('global_directory_content_b05/','global_directory_content_b07/')").replace("replace('30_global_directory_content_b05','32_global_directory_content_b07')","replace('30_global_directory_content_b05','32_global_directory_content_b07')")
    (O/name).write_text(source,encoding='utf-8')
