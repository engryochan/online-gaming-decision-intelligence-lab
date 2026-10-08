
CREATE TABLE IF NOT EXISTS spatial_reference(
 spatial_id TEXT PRIMARY KEY, spatial_kind TEXT NOT NULL CHECK(spatial_kind IN ('CONTEMPORARY_ISO','HISTORICAL_POLITY','HISTORICAL_PLACE','MARITIME','TRANSBOUNDARY','OTHER')),
 iso_alpha2 TEXT REFERENCES country(iso_alpha2), canonical_label TEXT NOT NULL, parent_spatial_id TEXT REFERENCES spatial_reference(spatial_id),
 geometry_ref TEXT, valid_from TEXT, valid_to TEXT, date_precision TEXT NOT NULL DEFAULT 'UNKNOWN',
 source_id TEXT REFERENCES source_evidence(source_id), review_status TEXT NOT NULL DEFAULT 'NOT_VERIFIED',
 CHECK(valid_from IS NULL OR valid_to IS NULL OR valid_from<=valid_to)
);
CREATE TABLE IF NOT EXISTS entity_identity(
 entity_uuid TEXT PRIMARY KEY, entity_kind TEXT NOT NULL CHECK(entity_kind IN ('LEGAL_ENTITY','HISTORICAL_ORGANIZATION','PUBLIC_BODY','BRAND','PERSON','PLACE','OTHER')),
 canonical_name TEXT NOT NULL, modern_legal_entity_id TEXT REFERENCES legal_entity(entity_id), confidence_status TEXT NOT NULL DEFAULT 'UNVERIFIED',
 created_at TEXT NOT NULL, UNIQUE(modern_legal_entity_id)
);
CREATE TABLE IF NOT EXISTS entity_alias(
 alias_id TEXT PRIMARY KEY, entity_uuid TEXT NOT NULL REFERENCES entity_identity(entity_uuid), name TEXT NOT NULL,
 language_tag TEXT, script_code TEXT, valid_from TEXT,valid_to TEXT,source_id TEXT REFERENCES source_evidence(source_id),
 assertion_status TEXT NOT NULL DEFAULT 'UNVERIFIED', CHECK(valid_from IS NULL OR valid_to IS NULL OR valid_from<=valid_to)
);
CREATE TABLE IF NOT EXISTS temporal_assertion(
 assertion_id TEXT PRIMARY KEY, subject_id TEXT NOT NULL REFERENCES entity_identity(entity_uuid), predicate TEXT NOT NULL,
 object_entity_id TEXT REFERENCES entity_identity(entity_uuid), literal_value TEXT, spatial_id TEXT REFERENCES spatial_reference(spatial_id),
 valid_from TEXT,valid_to TEXT,recorded_from TEXT NOT NULL,recorded_to TEXT,
 temporal_precision TEXT NOT NULL DEFAULT 'UNKNOWN',confidence_status TEXT NOT NULL DEFAULT 'UNVERIFIED',
 asserted_source_id TEXT REFERENCES source_evidence(source_id), license_gate TEXT NOT NULL DEFAULT 'REVIEW_REQUIRED',
 human_review TEXT NOT NULL DEFAULT 'PENDING',
 CHECK ((object_entity_id IS NOT NULL) <> (literal_value IS NOT NULL)),
 CHECK (valid_from IS NULL OR valid_to IS NULL OR valid_from<=valid_to),
 CHECK (recorded_to IS NULL OR recorded_from<=recorded_to)
);
CREATE TABLE IF NOT EXISTS classification_node(
 classification_id TEXT PRIMARY KEY, system_code TEXT NOT NULL, release_version TEXT NOT NULL, level_code TEXT NOT NULL,
 code TEXT NOT NULL, title_original TEXT NOT NULL,parent_id TEXT REFERENCES classification_node(classification_id),
 official_source_url TEXT,source_hash_sha256 TEXT, import_status TEXT NOT NULL DEFAULT 'UNVERIFIED',
 UNIQUE(system_code,release_version,code)
);
CREATE TABLE IF NOT EXISTS source_snapshot(
 snapshot_id TEXT PRIMARY KEY, source_id TEXT NOT NULL REFERENCES source_evidence(source_id),retrieved_at TEXT NOT NULL,
 content_hash_sha256 TEXT NOT NULL, license_status TEXT NOT NULL,access_basis TEXT NOT NULL,
 media_type TEXT, provenance_note TEXT, CHECK(length(content_hash_sha256)=64)
);
CREATE TABLE IF NOT EXISTS assertion_evidence(
 assertion_id TEXT NOT NULL REFERENCES temporal_assertion(assertion_id), snapshot_id TEXT NOT NULL REFERENCES source_snapshot(snapshot_id),
 evidence_role TEXT NOT NULL CHECK(evidence_role IN ('SUPPORTS','CONTRADICTS','CONTEXT')),
 PRIMARY KEY(assertion_id,snapshot_id,evidence_role)
);
CREATE TABLE IF NOT EXISTS global_coverage_gate(
 iso_alpha2 TEXT NOT NULL REFERENCES country(iso_alpha2), domain_code TEXT NOT NULL REFERENCES domain(domain_code),
 source_kind TEXT NOT NULL, source_identified INTEGER NOT NULL DEFAULT 0 CHECK(source_identified IN(0,1)),
 legally_accessible INTEGER NOT NULL DEFAULT 0 CHECK(legally_accessible IN(0,1)),
 real_records_loaded INTEGER NOT NULL DEFAULT 0 CHECK(real_records_loaded>=0),
 official_denominator INTEGER CHECK(official_denominator>=0), latest_snapshot_id TEXT REFERENCES source_snapshot(snapshot_id),
 verified_at TEXT, gate_status TEXT NOT NULL DEFAULT 'UNKNOWN',
 PRIMARY KEY(iso_alpha2,domain_code,source_kind)
);
CREATE TABLE IF NOT EXISTS ingestion_run(
 run_id TEXT PRIMARY KEY, source_id TEXT, input_sha256 TEXT, started_at TEXT NOT NULL,finished_at TEXT,
 records_read INTEGER NOT NULL DEFAULT 0, records_accepted INTEGER NOT NULL DEFAULT 0, records_rejected INTEGER NOT NULL DEFAULT 0,
 exit_state TEXT NOT NULL, error_summary TEXT
);
CREATE INDEX IF NOT EXISTS ix_temporal_subject_valid ON temporal_assertion(subject_id,valid_from,valid_to);
CREATE INDEX IF NOT EXISTS ix_temporal_recorded ON temporal_assertion(recorded_from,recorded_to);
CREATE INDEX IF NOT EXISTS ix_spatial_iso ON spatial_reference(iso_alpha2);
CREATE INDEX IF NOT EXISTS ix_alias_name ON entity_alias(name);
CREATE INDEX IF NOT EXISTS ix_cov_status ON global_coverage_gate(gate_status);
CREATE VIEW IF NOT EXISTS vw_global_gate_summary AS SELECT c.iso_alpha2,c.country_area_en,
 COUNT(g.source_kind) AS registered_channels,
 COALESCE(SUM(g.real_records_loaded),0) AS total_channel_record_events,
 SUM(CASE WHEN g.official_denominator IS NOT NULL THEN 1 ELSE 0 END) AS channels_with_official_denominator
 FROM country c LEFT JOIN global_coverage_gate g ON c.iso_alpha2=g.iso_alpha2 GROUP BY c.iso_alpha2,c.country_area_en;
