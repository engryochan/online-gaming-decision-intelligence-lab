"""Acceptance and red-team tests on temporary databases, never live facts."""
import csv,json,sqlite3,tempfile,unittest,uuid
from pathlib import Path
import fabric as f

class FabricAcceptance(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory(prefix='test-',dir=f.HERE);cls.path=Path(cls.tmp.name)
  cls.report=f.build(cls.path)
  cls.c=sqlite3.connect(cls.path/'dgef.sqlite');cls.c.execute('PRAGMA foreign_keys=ON')
 @classmethod
 def tearDownClass(cls):cls.c.close();cls.tmp.cleanup()
 def test_all_requested_table_names(self):
  attachment=Path(r'C:\Users\PPCCpcpc\OneDrive\Desktop\参考_册三.txt').read_text(encoding='utf-8-sig')
  names=set(f.re.findall(r'\b(?:registry_[a-z_]+|bridge_entity_external_id|space_(?:organization|program|mission|vehicle|object|facility_public|research_output)|cosmic_domain)\b',attachment))
  actual={r[0] for r in self.c.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')")}
  self.assertFalse(names-actual,names-actual)
 def test_baseline_preservation_roundtrip(self):
  for table,path in [('registry_country_area',f.ROOT/'Reference/tables/01_country_area/registry_country_area_iso3166_m49_e164_20261004.csv'),('registry_admin_unit',f.ROOT/'Reference/tables/02_admin_units/registry_admin_units_iso3166_2_20261004.csv')]:
   originals=f.read_csv(path)
   restored=[json.loads(r[0]) for r in self.c.execute(f'SELECT baseline_json FROM {table}')]
   self.assertEqual(sorted(map(lambda r:json.dumps(r,sort_keys=True),originals)),sorted(map(lambda r:json.dumps(r,sort_keys=True),restored)))
 def test_stable_idempotent_reimport(self):
  before=list(self.c.execute('SELECT entity_id,canonical_name FROM registry_entity ORDER BY entity_id'))
  counts={n:self.c.execute(f'SELECT count(*) FROM {n}').fetchone()[0] for n in f.SPECS}
  f.build(self.path)
  self.assertEqual(before,list(self.c.execute('SELECT entity_id,canonical_name FROM registry_entity ORDER BY entity_id')))
  self.assertEqual(counts,{n:self.c.execute(f'SELECT count(*) FROM {n}').fetchone()[0] for n in f.SPECS})
 def test_uuid7_semantics(self):
  for (eid,) in self.c.execute('SELECT entity_id FROM registry_entity'):
   u=uuid.UUID(eid.split('::')[1]);self.assertEqual(u.version,7);self.assertEqual(u.variant,uuid.RFC_4122)
 def test_baseline_foreign_keys_and_indexes(self):
  self.assertEqual(self.c.execute('PRAGMA integrity_check').fetchone()[0],'ok')
  self.assertEqual(self.c.execute('PRAGMA foreign_key_check').fetchall(),[])
  self.assertEqual(self.c.execute('SELECT count(*) FROM registry_country_area').fetchone()[0],249)
  self.assertEqual(self.c.execute('SELECT count(*) FROM registry_admin_unit').fetchone()[0],5046)
  self.assertIn('USING INDEX',str(self.report['query_plan_country_admin']))
 def test_no_automatic_vendor_identity_or_training(self):
  self.assertEqual(self.c.execute('SELECT count(*) FROM staging_service_catalogue WHERE candidate_entity_id IS NOT NULL').fetchone()[0],0)
  self.assertEqual(self.c.execute('SELECT count(*) FROM v_model_features_approved').fetchone()[0],0)
 def reject(self,sql,args=()):
  self.c.execute('SAVEPOINT attack')
  try:
   with self.assertRaises(sqlite3.IntegrityError):self.c.execute(sql,args)
  finally:self.c.execute('ROLLBACK TO attack');self.c.execute('RELEASE attack')
 def test_orphan_and_invalid_world_rejected(self):
  self.reject("INSERT INTO registry_entity_relation VALUES ('attack','missing','owns','missing','SOURCE_COUNTRY','VERIFIED','2026-10-04',NULL,'2026-10-04')")
  self.reject("INSERT INTO registry_entity VALUES ('DUECG-EID::bad','UNRESOLVED','bad','UNKNOWN_WORLD','active','2026-10-04',NULL,'2026-10-04')")
  self.reject("INSERT INTO registry_entity VALUES ('DUECG-EID::bad','UNRESOLVED','bad','REAL-TWIN','active','2026-10-04',NULL,'2026-10-04')")
 def test_unknown_not_zero_and_license_gates(self):
  c=self.c;c.execute('SAVEPOINT training')
  eid=c.execute('SELECT entity_id FROM registry_entity LIMIT 1').fetchone()[0]
  try:
   c.execute("INSERT INTO registry_observation VALUES ('TEST',?,'TEST',NULL,'count',1,0,'MEASURED',NULL,'SOURCE_COUNTRY','OBSERVED','2026-10-04',NULL,'2026-10-04')",(eid,))
   self.assertIsNone(c.execute("SELECT value FROM registry_observation WHERE observation_id='TEST'").fetchone()[0])
   self.assertEqual(c.execute('SELECT count(*) FROM v_model_features_approved').fetchone()[0],0)
   c.execute("UPDATE registry_observation SET value=0 WHERE observation_id='TEST'")
   self.assertEqual(c.execute('SELECT count(*) FROM v_model_features_approved').fetchone()[0],0)
   c.execute("UPDATE registry_license_policy SET ml_training_allowed=1 WHERE policy_id='UNKNOWN'")
   self.assertEqual(c.execute('SELECT count(*) FROM v_model_features_approved').fetchone()[0],1)
   c.execute("UPDATE registry_entity SET world_domain='SIM' WHERE entity_id=?",(eid,))
   self.assertEqual(c.execute('SELECT count(*) FROM v_model_features_approved').fetchone()[0],0)
  finally:c.execute('ROLLBACK TO training');c.execute('RELEASE training')
 def test_location_insert_update_frame_and_unknown_gates(self):
  c=self.c;c.execute('SAVEPOINT spatial')
  eid=c.execute('SELECT entity_id FROM registry_entity LIMIT 1').fetchone()[0]
  try:
   c.execute("INSERT INTO registry_spatial_frame VALUES ('TEST','EARTH_SURFACE','Earth','test axes only','m','m/s','https://example.invalid/test')")
   sql="INSERT INTO registry_entity_location(location_observation_id,entity_id,cosmic_domain,spatial_frame,central_body,epoch,time_scale,x,y,z,position_unit,velocity_unit,source_solution,disclosure_precision,source_id,evidence_state,valid_from,transaction_time) VALUES ('TEST',?,'EARTH_SURFACE','TEST','Earth','2026-10-04','UTC',1,2,3,'m','m/s','TEST','PUBLIC_GENERAL','SOURCE_COUNTRY',?,'2026-10-04','2026-10-04')"
   self.reject(sql,(eid,'UNKNOWN'))
   c.execute(sql,(eid,'OBSERVED'))
   self.reject("UPDATE registry_entity_location SET cosmic_domain='GALACTIC' WHERE location_observation_id='TEST'")
   self.reject("UPDATE registry_entity_location SET epoch=NULL WHERE location_observation_id='TEST'")
   self.reject("UPDATE registry_entity_location SET disclosure_precision='REDACTED' WHERE location_observation_id='TEST'")
   self.reject("UPDATE registry_entity_location SET position_unit='degree' WHERE location_observation_id='TEST'")
  finally:c.execute('ROLLBACK TO spatial');c.execute('RELEASE spatial')

if __name__=='__main__':unittest.main(verbosity=2)
