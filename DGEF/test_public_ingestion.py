"""Acceptance checks for the actual downloaded and imported public snapshots."""
from pathlib import Path
import csv,hashlib,json,sqlite3,unittest
import fabric as f
HERE=f.HERE;OUT=f.ROOT/'reports/2026-10-04/dgef'
class PublicSnapshots(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=sqlite3.connect((HERE/'artifacts/dgef.sqlite').as_uri()+'?mode=ro',uri=True)
  cls.c.execute('PRAGMA foreign_keys=ON')
  cls.c.execute('ATTACH DATABASE ? AS baseline',((OUT/'before_public_ingestion.sqlite').as_uri()+'?mode=ro',))
 @classmethod
 def tearDownClass(cls):cls.c.close()
 def test_every_original_database_row_preserved(self):
  names=[r[0] for r in self.c.execute("SELECT name FROM baseline.sqlite_master WHERE type='table'")]
  for n in names:
   cols=','.join('"'+r[1]+'"' for r in self.c.execute(f'PRAGMA baseline.table_info({n})'))
   self.assertEqual(self.c.execute(f'SELECT {cols} FROM baseline.{n} EXCEPT SELECT {cols} FROM main.{n}').fetchall(),[],n)
 def test_all_response_hashes_and_dataset_lineage(self):
  manifest=json.loads((HERE/'inbox/manifest.json').read_text(encoding='utf-8'))
  self.assertEqual(len(manifest),26)
  for r in manifest:
   self.assertEqual(r['status'],'FETCHED',r['key'])
   self.assertEqual(hashlib.sha256((HERE/'inbox'/r['file']).read_bytes()).hexdigest(),r['sha256'])
   self.assertIsNotNone(self.c.execute('SELECT dataset_id FROM registry_dataset WHERE file_sha256=?',(r['sha256'],)).fetchone())
 def test_integrity_and_foreign_keys(self):
  self.assertEqual(self.c.execute('PRAGMA integrity_check').fetchone()[0],'ok')
  self.assertEqual(self.c.execute('PRAGMA foreign_key_check').fetchall(),[])
 def test_no_facility_centroids_promoted(self):
  self.assertEqual(self.c.execute("SELECT count(*) FROM registry_entity_location WHERE cosmic_domain LIKE 'EARTH_%'").fetchone()[0],0)
  self.assertEqual(self.c.execute('SELECT count(*) FROM registry_entity_location').fetchone()[0],6)
 def test_vectors_roundtrip_and_units(self):
  for r in json.loads((HERE/'inbox/manifest.json').read_text(encoding='utf-8')):
   if r['kind']!='HORIZONS':continue
   body=json.loads((HERE/'inbox'/r['file']).read_text(encoding='utf-8'))['result']
   text=body.split('$$SOE')[1].split('$$EOE')[0]
   expected=sorted(tuple(float(x) for x in next(csv.reader([line]))[2:8]) for line in text.strip().splitlines())
   actual=self.c.execute('SELECT x,y,z,vx,vy,vz FROM registry_entity_location l JOIN registry_source s USING(source_id) WHERE s.canonical_uri=?',(r['url'],)).fetchall()
   self.assertEqual(expected,sorted(actual))
  self.assertEqual(self.c.execute("SELECT count(*) FROM registry_entity_location WHERE time_scale!='TDB' OR position_unit!='AU' OR velocity_unit!='AU/day' OR central_body!='Sun'").fetchone()[0],0)
 def test_legal_source_fields_roundtrip(self):
  for payload,name,form,status in self.c.execute("SELECT i.record_payload,e.canonical_name,l.legal_form,l.registration_status FROM registry_ingest_record i JOIN registry_entity e USING(entity_id) JOIN registry_legal_entity l USING(entity_id) WHERE i.external_key IN (SELECT external_id FROM bridge_entity_external_id WHERE id_system='LEI')"):
   a=json.loads(payload)['attributes'];self.assertEqual(name,a['entity']['legalName']['name']);self.assertEqual(form,a['entity']['legalForm']['id']);self.assertEqual(status,a['registration']['status'])
 def test_no_fictional_padding_or_unreviewed_training(self):
  for n in ('registry_virtual_world','registry_virtual_entity','registry_simulation_run','registry_synthetic_population'):
   self.assertEqual(self.c.execute(f'SELECT count(*) FROM {n}').fetchone()[0],0)
  self.assertEqual(self.c.execute('SELECT count(*) FROM v_model_features_approved').fetchone()[0],0)

if __name__=='__main__':unittest.main(verbosity=2)
