from pathlib import Path
O=Path(__file__).resolve().parent
source=(O.parent/'global_directory_content_b07/paginate.py').read_text(encoding='utf-8')
source=source.replace("T=R/'Reference/tables/32_global_directory_content_b07_20261008'","T=R/'Reference/tables/35_global_directory_content_b10_20261008'")
source=source.replace("read(R/'Reference/tables/31_global_directory_content_b06_20261008/registry_pagination_gaps.csv')","read(R/'Reference/tables/32_global_directory_content_b07_20261008/registry_pagination_link_observations.csv')")
source=source.replace("'32_global_directory_content_b07_20261008']","'32_global_directory_content_b07_20261008','35_global_directory_content_b10_20261008']")
source=source.replace('>=80','>=100').replace('[:80]','[:100]').replace('B07 explicit pagination','B10 explicit pagination')
(O/'paginate.py').write_text(source,encoding='utf-8')
source=(O.parent/'global_directory_content_b07/download.py').read_text(encoding='utf-8').replace('32_global_directory_content_b07','35_global_directory_content_b10')
(O/'download.py').write_text(source,encoding='utf-8')
source=(O.parent/'global_directory_content_b07/retry_unicode.py').read_text(encoding='utf-8').replace('32_global_directory_content_b07','35_global_directory_content_b10')
(O/'retry_unicode.py').write_text(source,encoding='utf-8')
for name in ['publish_check.py','verify_staged.py']:
    source=(O.parent/'global_directory_content_b07'/name).read_text(encoding='utf-8').replace('32_global_directory_content_b07','35_global_directory_content_b10').replace('B07_20261008','B10_20261008').replace('# B07 credential','# B10 credential').replace('global_directory_content_b07/**/*.response','global_directory_content_b10/**/*.response').replace("'global_directory_content_b07/'","'global_directory_content_b10/'")
    (O/name).write_text(source,encoding='utf-8')
